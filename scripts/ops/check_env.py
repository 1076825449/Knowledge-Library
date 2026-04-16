#!/usr/bin/env python3
"""环境检查脚本 - 验证运行依赖"""

import sys
import socket
import os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "database" / "db" / "tax_knowledge.db"


def check_python_version():
    """检查 Python 版本 >= 3.9"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"[FAIL] Python 版本过低: {version.major}.{version.minor}.{version.micro}")
        print(f"[INFO] 需要 Python >= 3.9")
        return False
    print(f"[PASS] Python 版本: {version.major}.{version.minor}.{version.micro}")
    return True


def check_flask_installed():
    """检查 Flask 是否已安装"""
    try:
        import flask
        print(f"[PASS] Flask 已安装: {flask.__version__}")
        return True
    except ImportError:
        print(f"[FAIL] Flask 未安装")
        print(f"[INFO] 运行: pip install Flask==3.0.0")
        return False


def check_database_exists():
    """检查数据库文件是否存在"""
    if DB_PATH.exists():
        size = DB_PATH.stat().st_size
        print(f"[PASS] 数据库文件存在: {DB_PATH} ({size} bytes)")
        return True
    else:
        print(f"[FAIL] 数据库文件不存在: {DB_PATH}")
        return False


def check_port_5000():
    """检查端口 5000 是否被占用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex(('localhost', 5000))
        sock.close()
        if result == 0:
            print(f"[WARN] 端口 5000 已被占用")
            return False
        else:
            print(f"[PASS] 端口 5000 可用")
            return True
    except Exception as e:
        print(f"[WARN] 无法检查端口: {e}")
        return True


def check_fk_constraints():
    """检查数据库 FK 约束是否开启"""
    if not DB_PATH.exists():
        print(f"[SKIP] 数据库不存在，跳过 FK 检查")
        return True
    
    try:
        import sqlite3
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys")
        fk_enabled = cursor.fetchone()[0]
        conn.close()
        
        if fk_enabled:
            print(f"[PASS] FK 约束已启用")
            return True
        else:
            print(f"[FAIL] FK 约束未启用")
            print(f"[INFO] 连接后执行: PRAGMA foreign_keys = ON")
            return False
    except Exception as e:
        print(f"[FAIL] 检查 FK 约束失败: {e}")
        return False


def main():
    print("=" * 50)
    print("企业税务知识库 — 环境检查")
    print("=" * 50)
    
    checks = [
        ("Python 版本", check_python_version),
        ("Flask 安装", check_flask_installed),
        ("数据库文件", check_database_exists),
        ("端口 5000", check_port_5000),
        ("FK 约束", check_fk_constraints),
    ]
    
    results = []
    for name, func in checks:
        print(f"\n--- {name} ---")
        results.append(func())
    
    print("\n" + "=" * 50)
    if all(results):
        print("环境检查通过 ✓")
        return 0
    else:
        print("环境检查未完全通过，请修复上述问题")
        return 1


if __name__ == "__main__":
    sys.exit(main())