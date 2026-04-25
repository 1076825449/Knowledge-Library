"""
部署相关测试：验证环境变量配置和 WSGI 入口可用。
"""

import importlib
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "backend"))


def test_config_reads_environment_variables(monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", "/tmp/tax.db")
    monkeypatch.setenv("HOST", "127.0.0.1")
    monkeypatch.setenv("PORT", "5999")
    monkeypatch.setenv("FLASK_DEBUG", "0")
    monkeypatch.setenv("SITE_URL", "https://example.com")

    import config

    reloaded = importlib.reload(config)

    assert reloaded.Config.DB_PATH == "/tmp/tax.db"
    assert reloaded.Config.HOST == "127.0.0.1"
    assert reloaded.Config.PORT == 5999
    assert reloaded.Config.DEBUG is False
    assert reloaded.Config.SITE_URL == "https://example.com"


def test_wsgi_app_loads():
    import wsgi

    assert wsgi.app is not None
