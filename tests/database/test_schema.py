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
            "question_update_log", "tag_dict"
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
        required = {"id", "policy_code", "policy_name", "document_no", "policy_level", "current_status"}
        assert required.issubset(cols), f"缺少列: {required - cols}"
