#!/usr/bin/env python3
# ============================================================
# scripts/content/backfill_missing_updates.py
# 为缺少更新记录的问题回填首版更新日志
# 用法: python scripts/content/backfill_missing_updates.py [--dry-run]
# ============================================================

import os
import sqlite3
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'db', 'tax_knowledge.db')


def connect_db():
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库文件不存在: {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def main():
    dry_run = "--dry-run" in sys.argv
    conn = connect_db()

    rows = conn.execute("""
        SELECT q.id, q.question_code, q.version_no, q.created_at, q.updated_at
        FROM question_master q
        LEFT JOIN question_update_log u ON q.id = u.question_id
        WHERE q.status = 'active' AND u.id IS NULL
        ORDER BY q.question_code
    """).fetchall()

    if not rows:
        print("✅ 所有 active 问题均已有更新记录")
        conn.close()
        return

    print(f"📋 发现 {len(rows)} 条 active 问题缺少更新记录")

    inserted = 0
    for row in rows:
        version_no = row["version_no"] or 1
        update_date = row["updated_at"] or row["created_at"]
        if dry_run:
            print(f"  {row['question_code']} -> v{version_no} / {update_date}")
            continue

        conn.execute("""
            INSERT INTO question_update_log (
                question_id, version_no, update_date, update_type,
                update_reason, updated_by, reviewed_by, change_summary
            ) VALUES (?, ?, ?, 'update_new', ?, ?, ?, ?)
        """, (
            row["id"],
            version_no,
            update_date,
            "历史内容回填首版更新记录",
            "system_backfill",
            "",
            f"回填 {row['question_code']} 的首版更新记录",
        ))
        inserted += 1

    if not dry_run:
        conn.commit()
        print(f"✅ 已回填 {inserted} 条更新记录")
        remaining = conn.execute("""
            SELECT COUNT(*) FROM question_master q
            LEFT JOIN question_update_log u ON q.id = u.question_id
            WHERE q.status = 'active' AND u.id IS NULL
        """).fetchone()[0]
        print(f"📋 剩余缺更新记录问题: {remaining} 条")

    conn.close()


if __name__ == "__main__":
    main()
