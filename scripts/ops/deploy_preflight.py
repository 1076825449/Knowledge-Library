#!/usr/bin/env python3
"""部署前检查：验证关键文件、目录、配置和环境变量安全性。"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = [
    ROOT / "wsgi.py",
    ROOT / "Dockerfile",
    ROOT / "docker-compose.yml",
    ROOT / "Procfile",
    ROOT / "deploy" / "nginx" / "tax-knowledge.conf.example",
    ROOT / "deploy" / "systemd" / "tax-knowledge.service.example",
]

REQUIRED_DIRS = [
    ROOT / "database" / "db",
    ROOT / "database" / "backups",
    ROOT / "data" / "reports",
    ROOT / "data" / "exports",
]

# 不安全默认值（检测到这些值应阻断部署）
UNSAFE_DEFAULTS = {
    "ADMIN_PASSWORD": {"tax2026", "admin", "password", "changeme", "test123"},
    "SECRET_KEY": {
        "tax-knowledge-library-secret-2026",
        "secret-key-change-me",
        "changeme",
        "dev-secret",
    },
}


def check_file_writeable(path: Path) -> bool:
    """检查目录是否可写（用于数据库写入检查）"""
    if path.exists():
        return os.access(path, os.W_OK)
    # 目录不存在时检查父目录是否可创建
    parent = path.parent
    while not parent.exists():
        parent = parent.parent
    return os.access(parent, os.W_OK)


def main() -> int:
    ok = True
    errors = []

    print("=" * 60)
    print("企业税务知识库 — 部署前检查")
    print("=" * 60)

    # ---- 文件检查 ----
    print("\n[文件检查]")
    for path in REQUIRED_FILES:
        if path.exists():
            print(f"[PASS] {path.relative_to(ROOT)}")
        else:
            print(f"[FAIL] 缺失: {path.relative_to(ROOT)}")
            ok = False

    # ---- 目录检查 ----
    print("\n[目录检查]")
    for path in REQUIRED_DIRS:
        if path.exists():
            print(f"[PASS] {path.relative_to(ROOT)}")
        else:
            print(f"[WARN] 缺失目录，将运行时创建: {path.relative_to(ROOT)}")

    # ---- 安全检查 ----
    print("\n[安全配置检查]")

    # 检查 SECRET_KEY 和 ADMIN_PASSWORD
    for name, unsafe_values in UNSAFE_DEFAULTS.items():
        value = os.environ.get(name, "")
        if not value:
            print(f"[FAIL] {name} 未设置（生产环境必须设置）")
            ok = False
            errors.append(f"{name} 未设置")
        elif value.lower() in unsafe_values:
            print(f"[FAIL] {name} 使用不安全默认值（{value}）")
            ok = False
            errors.append(f"{name} 使用了不安全默认值")
        else:
            print(f"[PASS] {name} 已设置（已脱敏）")

    # 检查 FLASK_DEBUG
    debug_val = os.environ.get("FLASK_DEBUG", "").strip().lower()
    if debug_val in {"1", "true", "yes", "on"}:
        print("[FAIL] FLASK_DEBUG=1 生产环境禁止开启调试模式")
        ok = False
        errors.append("FLASK_DEBUG=1 生产环境禁止开启")
    else:
        print(f"[PASS] FLASK_DEBUG 未开启或关闭（当前: {debug_val or '未设置'})")

    # 检查数据库目录可写
    db_dir = ROOT / "database" / "db"
    if check_file_writeable(db_dir):
        print(f"[PASS] 数据库目录可写: database/db/")
    else:
        print(f"[FAIL] 数据库目录不可写: database/db/")
        ok = False
        errors.append("database/db/ 目录不可写")

    # ---- 环境变量建议 ----
    print("\n[环境变量建议]")
    for name in ["DATABASE_PATH", "HOST", "PORT", "SITE_NAME", "SITE_URL"]:
        value = os.environ.get(name)
        if value:
            print(f"[PASS] {name}={value}")
        else:
            print(f"[INFO] {name} 未设置（使用默认值）")

    # ---- 总结 ----
    print("\n" + "=" * 60)
    if errors:
        print("阻断项:")
        for e in errors:
            print(f"  - {e}")
    if ok:
        print("部署前检查通过")
        return 0
    print("部署前检查未通过，请修复上述阻断项后再部署")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
