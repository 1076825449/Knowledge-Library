#!/usr/bin/env python3
# ============================================================
# scripts/ops/backup_db.py
# 数据库备份脚本
# 用法: python scripts/ops/backup_db.py
# ============================================================

import sqlite3
import os
import shutil
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'db', 'tax_knowledge.db')
BACKUPS_DIR = os.path.join(PROJECT_ROOT, 'database', 'backups')
MAX_KEEP = 10


def ensure_backups_dir():
    os.makedirs(BACKUPS_DIR, exist_ok=True)


def get_backup_filename():
    now = datetime.now()
    return f"tax_knowledge_{now.strftime('%Y%m%d_%H%M%S')}.db"


def list_backups():
    """返回按修改时间排序的备份文件列表"""
    if not os.path.exists(BACKUPS_DIR):
        return []
    files = [f for f in os.listdir(BACKUPS_DIR) if f.startswith('tax_knowledge_') and f.endswith('.db')]
    files.sort(key=lambda f: os.path.getmtime(os.path.join(BACKUPS_DIR, f)))
    return files


def cleanup_old_backups(backups):
    """删除超出保留数量的旧备份"""
    if len(backups) > MAX_KEEP:
        to_delete = backups[:len(backups) - MAX_KEEP]
        for fname in to_delete:
            fpath = os.path.join(BACKUPS_DIR, fname)
            os.remove(fpath)
            print(f"🗑️  已删除旧备份: {fname}")


def backup_database():
    ensure_backups_dir()

    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库文件不存在: {DB_PATH}")
        return None

    # 获取所有现有备份（排序）
    existing_backups = list_backups()

    # 执行备份（使用SQLite的backup API）
    backup_filename = get_backup_filename()
    backup_path = os.path.join(BACKUPS_DIR, backup_filename)

    print(f"📦 开始备份数据库...")
    print(f"   源文件: {DB_PATH}")
    print(f"   目标文件: {backup_path}")

    try:
        # 打开源数据库
        source_conn = sqlite3.connect(DB_PATH, timeout=30)
        source_conn.execute("PRAGMA foreign_keys = ON")

        # 创建备份连接
        dest_conn = sqlite3.connect(backup_path)

        # 执行备份
        source_conn.backup(dest_conn)

        dest_conn.close()
        source_conn.close()

        print(f"✅ 备份成功: {backup_path}")
        print(f"   备份文件大小: {os.path.getsize(backup_path) / 1024:.1f} KB")

        # 清理旧备份
        all_backups = list_backups()
        cleanup_old_backups(all_backups)

        # 显示当前保留的备份
        remaining = list_backups()
        print(f"\n📁 当前保留的备份 ({len(remaining)}/{MAX_KEEP}):")
        for i, f in enumerate(remaining, 1):
            fpath = os.path.join(BACKUPS_DIR, f)
            size = os.path.getsize(fpath) / 1024
            mtime = datetime.fromtimestamp(os.path.getmtime(fpath)).strftime('%Y-%m-%d %H:%M:%S')
            print(f"   {i}. {f} ({size:.1f} KB, {mtime})")

        return backup_path

    except Exception as e:
        print(f"❌ 备份失败: {e}")
        # 如果备份文件被创建但备份失败，删除它
        if os.path.exists(backup_path):
            os.remove(backup_path)
        return None


def main():
    print("=" * 60)
    print("税务知识库数据库备份")
    print("=" * 60)
    print(f"保留策略: 最近 {MAX_KEEP} 个备份")
    print()

    backup_path = backup_database()

    if backup_path:
        print()
        print(f"✅ 备份完成")
        print(f"📄 备份文件路径: {backup_path}")
    else:
        print()
        print(f"❌ 备份失败")


if __name__ == '__main__':
    main()
