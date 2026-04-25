"""
数据库初始化和结构测试
"""
import pytest
import sqlite3
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
DB_PATH = ROOT_DIR / "database" / "db" / "tax_knowledge.db"


class TestDatabaseSchema:
    """验证数据库表结构和约束"""

    def test_db_exists(self):
        assert DB_PATH.exists(), f"数据库不存在: {DB_PATH}"

    def test_pragmas(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys")
        fk = cur.fetchone()[0]
        conn.close()
        assert fk == 1, "foreign_keys 应该为 ON"

    def test_tables_exist(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [r[0] for r in cur.fetchall()]
        conn.close()
        expected = {
            "local_rule_note", "policy_basis", "question_master",
            "question_policy_link", "question_relation", "question_tag_link",
            "question_update_log", "tag_dict", "users"
        }
        # sqlite_sequence 是 SQLite 内部表，不属于业务表
        user_tables = {t for t in tables if not t.startswith("sqlite_")}
        assert user_tables == expected, f"缺少表: {expected - user_tables}"

    def test_question_master_columns(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(question_master)")
        cols = {r[1] for r in cur.fetchall()}
        conn.close()
        required = {
            "id", "question_code", "question_title", "question_plain",
            "stage_code", "module_code", "question_type",
            "one_line_answer", "detailed_answer", "core_definition",
            "applicable_conditions", "exceptions_boundary",
            "practical_steps", "risk_warning",
            "scope_level", "local_region",
            "answer_certainty", "keywords",
            "high_frequency_flag", "newbie_flag",
            "status", "version_no", "created_at", "updated_at"
        }
        assert required.issubset(cols), f"缺少列: {required - cols}"

    def test_fk_enabled_on_connection(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys")
        assert cur.fetchone()[0] == 1
        conn.close()

    def test_tag_dict_has_stages_and_modules(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT tag_category, COUNT(*) FROM tag_dict GROUP BY tag_category")
        counts = dict(cur.fetchall())
        conn.close()
        assert counts.get("stage", 0) >= 6, "stage标签至少6个"
        assert counts.get("module", 0) >= 8, "module标签至少8个"

    def test_policy_basis_table_has_required_columns(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(policy_basis)")
        cols = {r[1] for r in cur.fetchall()}
        conn.close()
        required = {
            "id", "policy_code", "policy_name", "document_no", "policy_level", "current_status",
            "source_url", "source_org", "source_type", "last_verified_at",
            "verification_status", "verification_note",
        }
        assert required.issubset(cols), f"缺少列: {required - cols}"

    def test_active_questions_have_business_tags(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*)
            FROM question_master q
            LEFT JOIN question_tag_link qtl ON q.id = qtl.question_id
            WHERE q.status = 'active' AND qtl.id IS NULL
        """)
        missing = cur.fetchone()[0]
        conn.close()
        assert missing == 0, f"active 问题不应缺少标签，当前缺失 {missing} 条"

    def test_active_questions_have_update_logs(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*)
            FROM question_master q
            LEFT JOIN question_update_log qul ON q.id = qul.question_id
            WHERE q.status = 'active' AND qul.id IS NULL
        """)
        missing = cur.fetchone()[0]
        conn.close()
        assert missing == 0, f"active 问题不应缺少更新记录，当前缺失 {missing} 条"

    def test_active_questions_have_relations(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*)
            FROM question_master q
            LEFT JOIN question_relation qr ON q.id = qr.question_id
            WHERE q.status = 'active' AND qr.id IS NULL
        """)
        missing = cur.fetchone()[0]
        conn.close()
        assert missing == 0, f"active 问题不应缺少关联问题，当前缺失 {missing} 条"

    def test_high_frequency_questions_have_at_least_two_tags(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT q.id
                FROM question_master q
                WHERE q.status = 'active' AND q.high_frequency_flag = 1
                  AND (
                    SELECT COUNT(*)
                    FROM question_tag_link qtl
                    WHERE qtl.question_id = q.id
                  ) < 2
            )
        """)
        missing = cur.fetchone()[0]
        conn.close()
        assert missing == 0, f"高频问题至少应有 2 个标签，当前缺失 {missing} 条"

    def test_high_frequency_questions_have_at_least_two_policies(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT q.id
                FROM question_master q
                WHERE q.status = 'active' AND q.high_frequency_flag = 1
                  AND (
                    SELECT COUNT(*)
                    FROM question_policy_link qpl
                    WHERE qpl.question_id = q.id
                  ) < 2
            )
        """)
        missing = cur.fetchone()[0]
        conn.close()
        assert missing == 0, f"高频问题至少应有 2 条政策依据，当前缺失 {missing} 条"

    def test_high_frequency_questions_have_at_least_two_relations(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT q.id
                FROM question_master q
                WHERE q.status = 'active' AND q.high_frequency_flag = 1
                  AND (
                    SELECT COUNT(*)
                    FROM question_relation qr
                    WHERE qr.question_id = q.id
                  ) < 2
            )
        """)
        missing = cur.fetchone()[0]
        conn.close()
        assert missing == 0, f"高频问题至少应有 2 个关联问题，当前缺失 {missing} 条"

    def test_active_questions_have_structured_fields(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        checks = {
            "applicable_conditions": "适用条件",
            "exceptions_boundary": "例外与边界",
            "practical_steps": "实务处理步骤",
            "risk_warning": "风险提示",
        }
        for field, label in checks.items():
            cur.execute(f"""
                SELECT COUNT(*)
                FROM question_master
                WHERE status = 'active' AND ({field} IS NULL OR trim({field}) = '')
            """)
            missing = cur.fetchone()[0]
            assert missing == 0, f"active 问题不应缺少{label}，当前缺失 {missing} 条"
        conn.close()

    def test_etax_module_not_empty(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM question_master WHERE status = 'active' AND module_code = 'ETAX'")
        count = cur.fetchone()[0]
        conn.close()
        assert count > 0, "ETAX 模块不应为空"

    def test_etax_module_covers_all_stages(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT stage_code
            FROM question_master
            WHERE status = 'active' AND module_code = 'ETAX'
        """)
        stages = {row[0] for row in cur.fetchall()}
        conn.close()
        assert stages == {"SET", "OPR", "CHG", "CLS", "RSK", "SUS"}, \
            f"ETAX 模块应覆盖全部阶段，当前为 {sorted(stages)}"

    def test_stage_module_matrix_has_no_zero_slots(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT tag_code FROM tag_dict
            WHERE tag_category = 'stage'
            ORDER BY tag_code
        """)
        stages = [row[0] for row in cur.fetchall()]
        cur.execute("""
            SELECT tag_code FROM tag_dict
            WHERE tag_category = 'module'
            ORDER BY tag_code
        """)
        modules = [row[0] for row in cur.fetchall()]
        cur.execute("""
            SELECT stage_code, module_code, COUNT(*)
            FROM question_master
            WHERE status = 'active'
            GROUP BY stage_code, module_code
        """)
        counts = {(row[0], row[1]): row[2] for row in cur.fetchall()}
        conn.close()

        zero_slots = [
            f"{stage}-{module}"
            for stage in stages
            for module in modules
            if counts.get((stage, module), 0) == 0
        ]
        assert not zero_slots, f"阶段×模块矩阵不应有空槽，当前缺失: {zero_slots}"
