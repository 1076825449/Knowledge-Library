# ============================================================
# backend/services/question_service.py
# 问题数据访问服务
# ============================================================

import sqlite3
from config import Config

def dict_from_row(row, columns):
    return dict(zip(columns, row))

class QuestionService:
    def __init__(self):
        self.db_path = Config.DB_PATH

    def _query(self, sql, params=None):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def _query_one(self, sql, params=None):
        rows = self._query(sql, params)
        return rows[0] if rows else None

    # ---------- 问题列表 ----------
    def list_questions(self, stage=None, module=None, tag=None, page=1, page_size=20, hf=None, newbie=None, keyword=None, region=None, status=None, qtype=None):
        offset = (page - 1) * page_size
        # status 逻辑：显式传入值时使用该值，否则默认只看 active
        if status:
            conditions = ["q.status = ?"]
            params = [status]
        else:
            conditions = ["q.status = 'active'"]
            params = []

        if stage:
            conditions.append("q.stage_code = ?")
            params.append(stage)
        if module:
            conditions.append("q.module_code = ?")
            params.append(module)
        if tag:
            conditions.append("""
                q.id IN (
                    SELECT question_id FROM question_tag_link
                    JOIN tag_dict ON question_tag_link.tag_id = tag_dict.id
                    WHERE tag_dict.tag_code = ?
                )
            """)
            params.append(tag)
        if hf:
            conditions.append("q.high_frequency_flag = 1")
        if newbie:
            conditions.append("q.newbie_flag = 1")
        if keyword:
            pattern = f"%{keyword}%"
            conditions.append("""
                (q.question_title LIKE ? OR q.keywords LIKE ? OR q.one_line_answer LIKE ?)
            """)
            params.extend([pattern, pattern, pattern])
        if region:
            conditions.append("q.scope_level = ?")
            params.append(region)
        if qtype:
            conditions.append("q.question_type = ?")
            params.append(qtype)

        where_clause = " AND ".join(conditions)

        # 统计总数
        count_sql = f"SELECT COUNT(*) as total FROM question_master q WHERE {where_clause}"
        total = self._query_one(count_sql, params)['total']

        # 查询列表
        sql = f"""
            SELECT
                q.question_code, q.question_title, q.question_plain, q.one_line_answer,
                q.stage_code, q.module_code, q.question_type, q.answer_certainty,
                q.high_frequency_flag, q.newbie_flag, q.updated_at
            FROM question_master q
            WHERE {where_clause}
            ORDER BY q.high_frequency_flag DESC, q.updated_at DESC
            LIMIT ? OFFSET ?
        """
        params.extend([page_size, offset])
        questions = self._query(sql, params)

        return {
            'questions': questions,
            'total': total,
            'page': page,
            'page_size': page_size
        }

    # ---------- 问题详情 ----------
    def get_question_detail(self, question_code):
        # 基本信息
        q = self._query_one(
            "SELECT * FROM question_master WHERE question_code = ?",
            (question_code,)
        )
        if not q:
            return None

        # 政策依据
        policies = self._query("""
            SELECT p.*, qpl.support_type, qpl.support_note
            FROM question_policy_link qpl
            JOIN policy_basis p ON qpl.policy_id = p.id
            WHERE qpl.question_id = ?
            ORDER BY qpl.display_order
        """, (q['id'],))

        # 标签
        tags = self._query("""
            SELECT t.tag_code, t.tag_name, t.tag_category, qtl.is_primary
            FROM question_tag_link qtl
            JOIN tag_dict t ON qtl.tag_id = t.id
            WHERE qtl.question_id = ?
            ORDER BY qtl.is_primary DESC, qtl.display_order
        """, (q['id'],))

        # 关联问题
        relations = self._query("""
            SELECT q2.question_code, q2.question_title, q2.one_line_answer,
                   qr.relation_type
            FROM question_relation qr
            JOIN question_master q2 ON qr.related_id = q2.id
            WHERE qr.question_id = ? AND q2.status = 'active'
            ORDER BY qr.display_order
        """, (q['id'],))

        # 下一步推荐（同module + 下一stage，最接近生命周期下一步的问题）
        next_stage_sub = """
            SELECT t2.tag_code
            FROM tag_dict t1
            JOIN tag_dict t2 ON t2.display_order > t1.display_order
                             AND t2.tag_category = 'stage'
                             AND t1.tag_category = 'stage'
            WHERE t1.tag_code = ?
            ORDER BY t2.display_order
            LIMIT 1
        """
        next_step_questions = self._query(f"""
            SELECT question_code, question_title, one_line_answer, stage_code
            FROM question_master
            WHERE module_code = ?
              AND status = 'active'
              AND stage_code = ({next_stage_sub})
            ORDER BY updated_at DESC
            LIMIT 3
        """, (q['module_code'], q['stage_code']))

        # 更新记录
        updates = self._query("""
            SELECT version_no, update_date, update_type, update_reason,
                   updated_by, reviewed_by, change_summary
            FROM question_update_log
            WHERE question_id = ?
            ORDER BY version_no DESC
        """, (q['id'],))

        # 地方口径
        local_notes = self._query("""
            SELECT region_code, region_name, local_content,
                   authority_name, effective_date, source_url
            FROM local_rule_note
            WHERE question_id = ?
        """, (q['id'],))

        return {
            **q,
            'policies': policies,
            'tags': tags,
            'relations': relations,
            'next_step_questions': next_step_questions,
            'updates': updates,
            'local_notes': local_notes
        }

    # ---------- 阶段和模块 ----------
    def get_stages(self):
        return self._query("""
            SELECT tag_code, tag_name
            FROM tag_dict
            WHERE tag_category = 'stage'
            ORDER BY display_order
        """)

    def get_modules(self):
        return self._query("""
            SELECT tag_code, tag_name
            FROM tag_dict
            WHERE tag_category = 'module'
            ORDER BY display_order
        """)

    # ---------- 高频/新手 ----------
    def get_high_frequency(self, limit=10):
        return self._query("""
            SELECT question_code, question_plain, question_title, one_line_answer, stage_code
            FROM question_master
            WHERE status = 'active' AND high_frequency_flag = 1
            ORDER BY updated_at DESC
            LIMIT ?
        """, (limit,))

    def get_newbie(self, limit=10):
        return self._query("""
            SELECT question_code, question_plain, question_title, one_line_answer, stage_code
            FROM question_master
            WHERE status = 'active' AND newbie_flag = 1
            ORDER BY updated_at DESC
            LIMIT ?
        """, (limit,))

    # ---------- 最近更新 ----------
    def get_recent_updates(self, limit=10):
        return self._query("""
            SELECT DISTINCT
                q.question_code, q.question_plain, q.question_title, q.one_line_answer,
                q.stage_code, q.updated_at,
                qul.change_summary
            FROM question_master q
            JOIN (
                SELECT question_id, MAX(update_date) as max_date
                FROM question_update_log
                GROUP BY question_id
            ) latest ON q.id = latest.question_id
            JOIN question_update_log qul ON q.id = qul.question_id
                AND qul.update_date = latest.max_date
            WHERE q.status = 'active'
            ORDER BY qul.update_date DESC
            LIMIT ?
        """, (limit,))

    # ---------- 搜索 ----------
    def search_questions(self, keyword, page=1, page_size=20):
        offset = (page - 1) * page_size
        pattern = f"%{keyword}%"
        conditions = """
            q.status = 'active' AND (
                q.question_title LIKE ? OR q.keywords LIKE ? OR q.one_line_answer LIKE ?
            )
        """
        params = (pattern, pattern, pattern)

        # 统计
        total = self._query_one(
            f"SELECT COUNT(*) as total FROM question_master q WHERE {conditions}",
            params
        )['total']

        # 列表
        sql = f"""
            SELECT
                q.question_code, q.question_title, q.one_line_answer,
                q.stage_code, q.module_code, q.answer_certainty,
                q.high_frequency_flag, q.newbie_flag
            FROM question_master q
            WHERE {conditions}
            ORDER BY
                CASE WHEN q.question_title LIKE ? THEN 0 ELSE 1 END,
                q.high_frequency_flag DESC,
                q.updated_at DESC
            LIMIT ? OFFSET ?
        """
        params_with_priority = (pattern, pattern, pattern, pattern, page_size, offset)
        questions = self._query(sql, params_with_priority)

        return {
            'keyword': keyword,
            'questions': questions,
            'total': total,
            'page': page,
            'page_size': page_size
        }

    # ---------- 标签 ----------
    def get_all_tags(self):
        return self._query("""
            SELECT tag_code, tag_name, tag_category
            FROM tag_dict
            WHERE status = 'active'
            ORDER BY tag_category, display_order
        """)

    def get_business_tags(self):
        """返回 tag_category='business' 的业务标签（唯一口径）"""
        return self._query("""
            SELECT tag_code, tag_name
            FROM tag_dict
            WHERE tag_category = 'business' AND status = 'active'
            ORDER BY display_order
        """)

    def get_question_types(self):
        """返回所有问题类型（用于筛选器）"""
        return self._query("""
            SELECT DISTINCT question_type as type_code
            FROM question_master
            WHERE status = 'active' AND question_type IS NOT NULL
            ORDER BY question_type
        """)

    def get_stats(self):
        """返回首页统计数字：总问题数、高频数、新手数、政策依据数"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM question_master WHERE status = 'active'")
        total_questions = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM question_master WHERE status = 'active' AND high_frequency_flag = 1")
        total_hf = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM question_master WHERE status = 'active' AND newbie_flag = 1")
        total_newbie = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM policy_basis")
        total_policies = cur.fetchone()[0]
        conn.close()
        return {
            'total_questions': total_questions,
            'total_hf': total_hf,
            'total_newbie': total_newbie,
            'total_policies': total_policies
        }

    # ---------- 新增问题 ----------
    def _generate_code(self, stage_code, module_code):
        """生成下一个问题编码，如 OPR-DEC-003"""
        prefix = f"{stage_code}-{module_code}-"
        rows = self._query(
            "SELECT question_code FROM question_master WHERE question_code LIKE ? ORDER BY question_code DESC LIMIT 1",
            (f"{prefix}%",)
        )
        if not rows:
            return f"{prefix}001"
        last = rows[0]['question_code']
        num = int(last.split('-')[-1]) + 1
        return f"{prefix}{num:03d}"

    def create_question(self, data):
        """新增一条问题，返回 question_code"""
        import datetime
        # 必填字段校验
        required = ['question_title', 'stage_code', 'module_code', 'one_line_answer']
        missing = [f for f in required if not data.get(f, '').strip()]
        if missing:
            raise ValueError(f"缺少必填字段：{', '.join(missing)}")
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()

        # 生成编码
        code = self._generate_code(data['stage_code'], data['module_code'])

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("""
            INSERT INTO question_master (
                question_code, question_title, question_plain,
                stage_code, module_code, question_type,
                one_line_answer, detailed_answer, core_definition,
                applicable_conditions, exceptions_boundary,
                practical_steps, risk_warning,
                scope_level, local_region,
                answer_certainty, keywords,
                high_frequency_flag, newbie_flag,
                status, version_no, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
        """, (
            code,
            data['question_title'],
            data.get('question_plain', data['question_title']),
            data['stage_code'],
            data['module_code'],
            data.get('question_type', 'type_whether'),
            data['one_line_answer'],
            data.get('detailed_answer', ''),
            data.get('core_definition', ''),
            data.get('applicable_conditions', ''),
            data.get('exceptions_boundary', ''),
            data.get('practical_steps', ''),
            data.get('risk_warning', ''),
            data.get('scope_level', 'scope_national'),
            data.get('local_region', ''),
            data.get('answer_certainty', 'certain_clear'),
            data.get('keywords', ''),
            1 if data.get('high_frequency_flag') else 0,
            1 if data.get('newbie_flag') else 0,
            data.get('status', 'active'),
            now, now
        ))
        question_id = cur.lastrowid

        # 写入更新记录
        cur.execute("""
            INSERT INTO question_update_log (
                question_id, version_no, update_date, update_type,
                update_reason, updated_by, reviewed_by, change_summary
            ) VALUES (?, 1, ?, 'create', ?, ?, ?, ?)
        """, (
            question_id, now,
            data.get('update_reason', '新增问题'),
            data.get('created_by', 'system'),
            data.get('reviewed_by', ''),
            data.get('change_summary', f'创建问题 {code}')
        ))

        # 写入标签关联
        tag_codes = data.get('tags')
        if tag_codes:
            if isinstance(tag_codes, str):
                tag_codes = [tag_codes]
            for tag_code in tag_codes:
                cur.execute("SELECT id FROM tag_dict WHERE tag_code = ?", (tag_code,))
                tag_row = cur.fetchone()
                if tag_row:
                    cur.execute("""
                        INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, is_primary, display_order)
                        VALUES (?, ?, 0, 1)
                    """, (question_id, tag_row[0]))

        conn.commit()
        conn.close()
        return code

    # ---------- 政策依据相关 ----------

    def get_all_policies(self):
        """获取所有政策依据，供录入时选择"""
        return self._query("""
            SELECT id, policy_code, policy_name, document_no, policy_level, current_status
            FROM policy_basis
            ORDER BY policy_level, policy_name
        """)

    def add_policy_link(self, question_code, policy_id, support_type, support_note='', display_order=1):
        """将政策依据关联到问题"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute(
            "SELECT id FROM question_master WHERE question_code = ?",
            (question_code,)
        )
        row = cur.fetchone()
        if not row:
            conn.close()
            raise ValueError(f"问题不存在: {question_code}")
        question_id = row[0]
        try:
            cur.execute("""
                INSERT INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order)
                VALUES (?, ?, ?, ?, ?)
            """, (question_id, policy_id, support_type, support_note, display_order))
            conn.commit()
            result = True
        except sqlite3.IntegrityError:
            # 已存在则更新
            cur.execute("""
                UPDATE question_policy_link
                SET support_type = ?, support_note = ?, display_order = ?
                WHERE question_id = ? AND policy_id = ?
            """, (support_type, support_note, display_order, question_id, policy_id))
            conn.commit()
            result = True
        finally:
            conn.close()
        return result

    # ---------- 更新问题 ----------
    def update_question(self, question_code, data):
        """更新问题内容，返回 True"""
        import datetime
        # 必填字段校验（只在校验data中存在的字段）
        required = ['question_title', 'one_line_answer']
        missing = [f for f in required if f in data and not data.get(f, '').strip()]
        if missing:
            raise ValueError(f"字段不能为空：{', '.join(missing)}")
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 获取现有 version_no
        cur.execute("SELECT id, version_no FROM question_master WHERE question_code = ?", (question_code,))
        row = cur.fetchone()
        if not row:
            conn.close()
            raise ValueError(f"问题不存在: {question_code}")
        question_id, old_version = row
        new_version = old_version + 1

        # 构造更新字段（只更新非空字段）
        field_assigns = []
        params = []
        allowed = [
            'question_title', 'question_plain', 'stage_code', 'module_code',
            'question_type', 'one_line_answer', 'detailed_answer',
            'core_definition', 'applicable_conditions', 'exceptions_boundary',
            'practical_steps', 'risk_warning', 'scope_level', 'local_region',
            'answer_certainty', 'keywords', 'high_frequency_flag', 'newbie_flag', 'status'
        ]
        for f in allowed:
            if f in data and data[f] is not None:
                field_assigns.append(f"{f} = ?")
                val = data[f]
                # 处理 checkbox 值（字符串 '1'/'0' 转 int）
                if f in ('high_frequency_flag', 'newbie_flag'):
                    val = 1 if val == '1' else 0
                params.append(val)

        if field_assigns:
            field_assigns.append("updated_at = ?")
            params.append(now)
            field_assigns.append("version_no = ?")
            params.append(new_version)
            params.append(question_id)
            sql = f"UPDATE question_master SET {', '.join(field_assigns)} WHERE id = ?"
            cur.execute(sql, params)

        # 处理标签关联
        tag_codes = data.get('tags')
        if tag_codes:
            if isinstance(tag_codes, str):
                tag_codes = [tag_codes]
            # 删除旧标签关联
            cur.execute("DELETE FROM question_tag_link WHERE question_id = ?", (question_id,))
            # 写入新标签关联
            for tag_code in tag_codes:
                cur.execute("SELECT id FROM tag_dict WHERE tag_code = ?", (tag_code,))
                tag_row = cur.fetchone()
                if tag_row:
                    cur.execute("""
                        INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, is_primary, display_order)
                        VALUES (?, ?, 0, 1)
                    """, (question_id, tag_row[0]))

        # 写入更新记录
        cur.execute("""
            INSERT INTO question_update_log (
                question_id, version_no, update_date, update_type,
                update_reason, updated_by, reviewed_by, change_summary
            ) VALUES (?, ?, ?, 'update_revise', ?, ?, ?, ?)
        """, (
            question_id, new_version, now,
            data.get('update_reason', '内容更新'),
            data.get('updated_by', 'system'),
            data.get('reviewed_by', ''),
            data.get('change_summary', f'更新问题 {question_code} 至 v{new_version}')
        ))

        # 处理关联问题
        relations = data.get('relations')
        if relations:
            import datetime as dt2
            rel_conn = sqlite3.connect(self.db_path)
            rel_conn.execute("PRAGMA foreign_keys = ON")
            rel_cur = rel_conn.cursor()
            rel_cur.execute("DELETE FROM question_relation WHERE question_id = ?", (question_id,))
            if isinstance(relations, list):
                for rel in relations:
                    if isinstance(rel, dict) and rel.get('related_code'):
                        rel_cur.execute(
                            "SELECT id FROM question_master WHERE question_code = ?",
                            (rel['related_code'],)
                        )
                        row = rel_cur.fetchone()
                        if row:
                            rel_cur.execute("""
                                INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
                                VALUES (?, ?, ?, ?)
                            """, (
                                question_id, row[0],
                                rel.get('relation_type', 'related'),
                                int(rel.get('display_order', 1))
                            ))
            rel_conn.commit()
            rel_conn.close()

        conn.commit()
        conn.close()
        return True

    # ---------- 新增标签 ----------
    def create_tag(self, tag_code, tag_name, tag_category='business'):
        """创建新标签，返回 True；tag_code 已存在则抛出 ValueError"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT id FROM tag_dict WHERE tag_code = ?", (tag_code,))
        if cur.fetchone():
            conn.close()
            raise ValueError(f"标签编码已存在：{tag_code}")
        cur.execute("""
            INSERT INTO tag_dict (tag_code, tag_name, tag_category, status, display_order)
            VALUES (?, ?, ?, 'active', 99)
        """, (tag_code, tag_name, tag_category))
        conn.commit()
        conn.close()
        return True

    # ---------- 关联问题维护 ----------
    def get_question_relations(self, question_id):
        """返回指定问题的所有关联问题"""
        return self._query("""
            SELECT qr.id, qr.related_id, qr.relation_type, qr.display_order,
                   q2.question_code, q2.question_title, q2.one_line_answer
            FROM question_relation qr
            JOIN question_master q2 ON qr.related_id = q2.id
            WHERE qr.question_id = ?
            ORDER BY qr.display_order
        """, (question_id,))

    def upsert_question_relations(self, question_id, relations):
        """
        替换问题的全部关联关系。
        relations: list of dicts like {"related_code": "OPR-DEC-001", "relation_type": "related", "display_order": 1}
        """
        import datetime
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        # 删除旧关联
        cur.execute("DELETE FROM question_relation WHERE question_id = ?", (question_id,))
        # 写入新关联
        for rel in relations:
            if not rel.get('related_code'):
                continue
            cur.execute("SELECT id FROM question_master WHERE question_code = ?", (rel['related_code'],))
            row = cur.fetchone()
            if not row:
                continue  # 编码不存在则跳过
            related_id = row[0]
            relation_type = rel.get('relation_type', 'related')
            display_order = int(rel.get('display_order', 1))
            cur.execute("""
                INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
                VALUES (?, ?, ?, ?)
            """, (question_id, related_id, relation_type, display_order))
        conn.commit()
        conn.close()
        return True

    # ---------- 删除政策关联 ----------
    def remove_policy_link(self, question_code, policy_id):
        """解除问题与政策的关联"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("SELECT id FROM question_master WHERE question_code = ?", (question_code,))
        row = cur.fetchone()
        if not row:
            conn.close()
            raise ValueError(f"问题不存在: {question_code}")
        cur.execute(
            "DELETE FROM question_policy_link WHERE question_id = ? AND policy_id = ?",
            (row[0], policy_id)
        )
        conn.commit()
        conn.close()
        return True
