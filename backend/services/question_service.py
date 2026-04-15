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
    def list_questions(self, stage=None, module=None, tag=None, page=1, page_size=20):
        offset = (page - 1) * page_size
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

        where_clause = " AND ".join(conditions)

        # 统计总数
        count_sql = f"SELECT COUNT(*) as total FROM question_master q WHERE {where_clause}"
        total = self._query_one(count_sql, params)['total']

        # 查询列表
        sql = f"""
            SELECT
                q.question_code, q.question_title, q.one_line_answer,
                q.stage_code, q.module_code, q.answer_certainty,
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
            SELECT question_code, question_title, one_line_answer, stage_code
            FROM question_master
            WHERE status = 'active' AND high_frequency_flag = 1
            ORDER BY updated_at DESC
            LIMIT ?
        """, (limit,))

    def get_newbie(self, limit=10):
        return self._query("""
            SELECT question_code, question_title, one_line_answer, stage_code
            FROM question_master
            WHERE status = 'active' AND newbie_flag = 1
            ORDER BY updated_at DESC
            LIMIT ?
        """, (limit,))

    # ---------- 最近更新 ----------
    def get_recent_updates(self, limit=10):
        return self._query("""
            SELECT DISTINCT
                q.question_code, q.question_title, q.one_line_answer,
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
        return self._query("""
            SELECT tag_code, tag_name
            FROM tag_dict
            WHERE tag_category = 'business' AND status = 'active'
            ORDER BY display_order
        """)
