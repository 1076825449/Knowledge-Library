# ============================================================
# backend/services/quality_gate.py
# 内容质量门禁服务
# ============================================================

import sqlite3
import os
from pathlib import Path
from typing import Dict, List, Any


class QualityGate:
    """内容质量门禁：校验单条问题是否可以提交审核或发布"""

    def __init__(self, db_path: str = None):
        if db_path:
            self.db_path = db_path
        else:
            from config import Config
            self.db_path = Config.DB_PATH
        # 确保数据库文件存在（测试隔离场景下 Config.DB_PATH 可能指向已删除的临时文件）
        if not os.path.exists(self.db_path):
            from pathlib import Path
            default_db = str(Path(__file__).parent.parent.parent / 'database' / 'db' / 'tax_knowledge.db')
            if os.path.exists(default_db):
                self.db_path = default_db

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ------------------------------------------------------------------ #
    #  public API
    # ------------------------------------------------------------------ #

    def validate_for_review(self, question_code: str) -> Dict[str, Any]:
        """
        editor 提交审核前的校验。
        允许 warnings，但严重错误（errors）应阻止提交。
        """
        q = self._get_question(question_code)
        if not q:
            return {'ok': False, 'errors': ['问题不存在'], 'warnings': []}

        errors = []
        warnings = []

        # 1. 必填字段（最核心的不能为空）
        if not q['question_title'] or not q['question_title'].strip():
            errors.append('问题标题不能为空')
        if not q['question_plain'] or not q['question_plain'].strip():
            warnings.append('问题简述（口语化）未填写')
        if not q['one_line_answer'] or not q['one_line_answer'].strip():
            errors.append('一句话结论不能为空')
        if not q['stage_code']:
            errors.append('未选择生命周期阶段')
        if not q['module_code']:
            errors.append('未选择主题模块')
        if not q['question_type']:
            warnings.append('未选择问题类型')

        # 2. 业务标签
        tags = self._get_question_tags(q['id'])
        if not tags:
            warnings.append('未选择业务标签')

        # 3. 政策依据
        policies = self._get_question_policies(q['id'])
        if not policies:
            warnings.append('未关联政策依据（建议至少1条）')

        # 4. detailed_answer 充实度
        if q['detailed_answer']:
            if len(q['detailed_answer'].strip()) < 20:
                warnings.append('详细解答内容偏少（<20字），建议补充完整')
        else:
            warnings.append('详细解答未填写')

        # 5. 答案稳定性标注
        if not q['answer_certainty']:
            warnings.append('未标注结论稳定度')

        # 6. 高频问题额外检查
        if q['high_frequency_flag']:
            if len(q['detailed_answer'].strip()) < 50:
                warnings.append('高频问题详细解答建议更完整')
            if not policies:
                warnings.append('高频问题建议关联政策依据')
            related = self._get_related_questions(q['id'])
            if len(related) < 1:
                warnings.append('高频问题建议至少关联1条相关问题')

        # 7. 风险提示
        if not q['risk_warning'] or len(q['risk_warning'].strip()) < 10:
            warnings.append('风险提示未填写或内容偏少')

        # 8. 适用条件
        if not q['applicable_conditions'] or len(q['applicable_conditions'].strip()) < 10:
            warnings.append('适用条件未填写或内容偏少')

        # 9. 状态检查
        if q['status'] not in ('draft', 'rejected'):
            errors.append(f'当前状态（{q["status"]}）不允许提交审核')

        ok = len(errors) == 0
        return {
            'ok': ok,
            'errors': errors,
            'warnings': warnings,
            'question_code': question_code,
            'status': q['status'],
        }

    def validate_for_publish(self, question_code: str, reviewer_override_note: str = None) -> Dict[str, Any]:
        """
        reviewer/admin 发布（approve）前的严格校验。
        必须全部通过才能发布 active。
        """
        q = self._get_question(question_code)
        if not q:
            return {'ok': False, 'errors': ['问题不存在'], 'warnings': []}

        errors = []
        warnings = []

        # 1. 必填字段（发布时必须完整）
        if not q['question_title'] or not q['question_title'].strip():
            errors.append('问题标题不能为空')
        if not q['one_line_answer'] or not q['one_line_answer'].strip():
            errors.append('一句话结论不能为空')
        if not q['stage_code']:
            errors.append('未选择生命周期阶段')
        if not q['module_code']:
            errors.append('未选择主题模块')
        if not q['detailed_answer'] or len(q['detailed_answer'].strip()) < 20:
            errors.append('详细解答内容不足（至少20字）')
        if not q['applicable_conditions'] or len(q['applicable_conditions'].strip()) < 10:
            errors.append('适用条件内容不足')

        # 2. 业务标签（必须）
        tags = self._get_question_tags(q['id'])
        if not tags:
            errors.append('必须至少选择1个业务标签')

        # 3. 政策依据（必须）
        policies = self._get_question_policies(q['id'])
        if not policies:
            errors.append('必须至少关联1条政策依据')

        # 4. 高频问题额外要求
        if q['high_frequency_flag']:
            related = self._get_related_questions(q['id'])
            if len(related) < 2:
                errors.append('高频问题必须至少关联2条相关问题')
            if len(policies) < 2:
                errors.append('高频问题必须至少关联2条政策依据')

        # 5. 答案稳定性标注
        if not q['answer_certainty']:
            errors.append('必须标注结论稳定度')

        # 6. 风险提示（必须有实质内容）
        if not q['risk_warning'] or len(q['risk_warning'].strip()) < 10:
            errors.append('风险提示内容不足')

        # 7. 政策状态阻断检查
        if policies:
            for p in policies:
                if p['verification_status'] == 'needs_update':
                    errors.append(f'政策依据「{p["policy_name"]}」状态为"待更新"，请先核验政策有效性')
                elif p['verification_status'] == 'source_pending':
                    errors.append(f'政策依据「{p["policy_name"]}」状态为"来源待核实"，请先核实来源')
                elif p['verification_status'] == 'manual_local_review':
                    if not reviewer_override_note:
                        errors.append(f'政策依据「{p["policy_name"]}」需要人工地方口径复核，请填写复核说明')
                    else:
                        warnings.append(f'政策「{p["policy_name"]}」已人工复核说明：{reviewer_override_note}')

        # 8. 状态检查
        if q['status'] != 'pending_review':
            errors.append(f'当前状态（{q["status"]}）不允许发布')

        # 9. 地方口径不能污染全国口径
        if q['scope_level'] == 'scope_national':
            # 全国口径内容不能是地方口径
            pass  # 目前不强制校验具体内容，由审核人判断

        ok = len(errors) == 0
        return {
            'ok': ok,
            'errors': errors,
            'warnings': warnings,
            'question_code': question_code,
            'status': q['status'],
        }

    # ------------------------------------------------------------------ #
    #  helpers
    # ------------------------------------------------------------------ #

    def _get_question(self, question_code: str) -> Dict[str, Any]:
        conn = self._conn()
        q = conn.execute(
            "SELECT * FROM question_master WHERE question_code = ?", (question_code,)
        ).fetchone()
        conn.close()
        return dict(q) if q else None

    def _get_question_tags(self, question_id: int) -> List[Dict[str, Any]]:
        conn = self._conn()
        rows = conn.execute("""
            SELECT t.* FROM tag_dict t
            JOIN question_tag_link l ON l.tag_id = t.id
            WHERE l.question_id = ? AND l.is_primary = 0
            LIMIT 20
        """, (question_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def _get_question_policies(self, question_id: int) -> List[Dict[str, Any]]:
        conn = self._conn()
        rows = conn.execute("""
            SELECT p.id, p.policy_name, p.document_no, p.verification_status,
                   l.support_type, l.support_note
            FROM policy_basis p
            JOIN question_policy_link l ON l.policy_id = p.id
            WHERE l.question_id = ?
            LIMIT 10
        """, (question_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def _get_related_questions(self, question_id: int) -> List[Dict[str, Any]]:
        conn = self._conn()
        rows = conn.execute("""
            SELECT r.*, q.question_code, q.question_title
            FROM question_relation r
            JOIN question_master q ON q.id = r.related_question_id
            WHERE r.question_id = ?
            LIMIT 10
        """, (question_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
