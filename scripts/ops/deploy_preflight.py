#!/usr/bin/env python3
"""部署前检查：验证关键文件、目录和配置是否齐全。"""

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


def main() -> int:
    ok = True

    print("=" * 60)
    print("部署前检查")
    print("=" * 60)

    print("\n[文件检查]")
    for path in REQUIRED_FILES:
        if path.exists():
            print(f"[PASS] {path.relative_to(ROOT)}")
        else:
            print(f"[FAIL] 缺失: {path.relative_to(ROOT)}")
            ok = False

    print("\n[目录检查]")
    for path in REQUIRED_DIRS:
        if path.exists():
            print(f"[PASS] {path.relative_to(ROOT)}")
        else:
            print(f"[WARN] 缺失目录，将在运行时创建: {path.relative_to(ROOT)}")

    print("\n[环境变量建议]")
    for name in ["SECRET_KEY", "ADMIN_PASSWORD", "DATABASE_PATH", "HOST", "PORT", "FLASK_DEBUG"]:
        value = os.environ.get(name)
        if value:
            masked = value if name in {"HOST", "PORT", "FLASK_DEBUG", "DATABASE_PATH"} else "***set***"
            print(f"[PASS] {name}={masked}")
        else:
            print(f"[WARN] 未设置 {name}")

    print("\n" + "=" * 60)
    if ok:
        print("部署前检查通过")
        return 0
    print("部署前检查未通过")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
