#!/usr/bin/env python3
# ============================================================
# scripts/content/migrate_etax_questions.py
# 将明显属于电子税务局/系统办理的问题迁移到 ETAX 模块
# 用法: python scripts/content/migrate_etax_questions.py [--dry-run]
# ============================================================

import os
import sqlite3
import sys
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'db', 'tax_knowledge.db')

MIGRATIONS = [
    ("SET-TAX-003", "SET-ETAX-001"),
    ("OPR-TAX-018", "OPR-ETAX-001"),
    ("OPR-TAX-013", "OPR-ETAX-002"),
]


def connect_db():
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库文件不存在: {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def ensure_code_available(conn, new_code, old_code):
    row = conn.execute(
        "SELECT id FROM question_master WHERE question_code = ?",
        (new_code,),
    ).fetchone()
    if row:
        current = conn.execute(
            "SELECT id FROM question_master WHERE question_code = ?",
            (old_code,),
        ).fetchone()
        return current and row["id"] == current["id"]
    return True


def main():
    dry_run = "--dry-run" in sys.argv
    conn = connect_db()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for old_code, new_code in MIGRATIONS:
        row = conn.execute("""
            SELECT id, question_code, question_title, module_code, version_no
            FROM question_master
            WHERE question_code = ?
        """, (old_code,)).fetchone()
        if not row:
            print(f"⚠️ 未找到题目: {old_code}")
            continue

        if not ensure_code_available(conn, new_code, old_code):
            print(f"⚠️ 目标编码已被其他题目占用，跳过: {new_code}")
            continue

        if dry_run:
            print(f"{old_code} ({row['module_code']}) -> {new_code} (ETAX)")
            continue

        new_version = (row["version_no"] or 1) + 1
        conn.execute("""
            UPDATE question_master
            SET module_code = 'ETAX',
                question_code = ?,
                updated_at = ?,
                version_no = ?
            WHERE id = ?
        """, (new_code, now, new_version, row["id"]))

        conn.execute("""
            INSERT INTO question_update_log (
                question_id, version_no, update_date, update_type,
                update_reason, updated_by, reviewed_by, change_summary
            ) VALUES (?, ?, ?, 'update_revise', ?, ?, ?, ?)
        """, (
            row["id"],
            new_version,
            now,
            "归位至 ETAX 模块",
            "system_migration",
            "",
            f"{old_code} 迁移为 {new_code}，模块调整为 ETAX",
        ))

        print(f"✅ {old_code} -> {new_code}")

    if not dry_run:
        conn.commit()
        total_etax = conn.execute(
            "SELECT COUNT(*) FROM question_master WHERE module_code = 'ETAX'"
        ).fetchone()[0]
        print(f"📋 当前 ETAX 模块问题数: {total_etax}")

    conn.close()


if __name__ == "__main__":
    main()
