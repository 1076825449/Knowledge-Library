#!/usr/bin/env python3
"""
阶段5数据库迁移：用户与权限系统
Usage: python scripts/ops/migrate_add_users.py --password YOUR_ADMIN_PASSWORD
"""
import sqlite3, os, sys, argparse
from pathlib import Path
from werkzeug.security import generate_password_hash

PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"

parser = argparse.ArgumentParser(description="创建管理员用户")
parser.add_argument("--password", required=True, help="初始 admin 密码（至少8位）")
args = parser.parse_args()

pw = args.password
if len(pw) < 8:
    print("ERROR: 密码长度至少8位")
    sys.exit(1)

conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()

existing = cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
).fetchone()

if existing:
    print("users 表已存在，跳过创建。")
else:
    cur.execute("""
        CREATE TABLE users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            username        TEXT    NOT NULL UNIQUE,
            password_hash   TEXT    NOT NULL,
            display_name    TEXT    NOT NULL DEFAULT '',
            role            TEXT    NOT NULL DEFAULT 'viewer',
            is_active       INTEGER NOT NULL DEFAULT 1,
            created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
            last_login      TEXT
        )
    """)
    print("users 表创建成功。")

pw_hash = generate_password_hash(pw)
cur.execute(
    "INSERT OR IGNORE INTO users (username, password_hash, display_name, role) VALUES (?, ?, ?, ?)",
    ("admin", pw_hash, "系统管理员", "admin")
)
if cur.rowcount == 0:
    print("admin 用户已存在，跳过创建。")
else:
    print("admin 用户创建成功。")

conn.commit()
conn.close()
print("迁移完成。")
