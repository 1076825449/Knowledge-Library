"""
pytest 配置：Werkzeug 版本兼容 patch + 测试环境变量

兼容旧测试环境下可能存在的 `werkzeug.__version__` 查询，
但避免直接读取该弃用属性而触发告警。

测试环境变量：
- ADMIN_PASSWORD：测试用管理员密码（不影响生产）
- TAX_DB_PATH：指向测试数据库（由 svc fixture 设置，与 Config.DB_PATH 读取的键一致）
"""
import os
import sys
from pathlib import Path

# 不在这里覆盖 DATABASE_PATH/T
# TAX_DB_PATH，因为 test_routes.py 的 make_auth_client fixture 会在需要时设置
# conftest.py 的 import-time 设置会破坏已有测试（它们依赖真实数据库路径）
# 只确保 ADMIN_PASSWORD 存在
os.environ.setdefault("ADMIN_PASSWORD", "test-admin-password-2026")

from importlib.metadata import version, PackageNotFoundError


def pytest_configure(config):
    """在 pytest 收集阶段最早期执行，早于所有测试模块的 import"""
    import werkzeug
    try:
        werkzeug.__version__ = version("werkzeug")
    except PackageNotFoundError:
        werkzeug.__version__ = "0.0.0"
