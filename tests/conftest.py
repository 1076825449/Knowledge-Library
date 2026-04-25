"""
pytest 配置：Werkzeug 版本兼容 patch

兼容旧测试环境下可能存在的 `werkzeug.__version__` 查询，
但避免直接读取该弃用属性而触发告警。
"""
from importlib.metadata import version, PackageNotFoundError


def pytest_configure(config):
    """在 pytest 收集阶段最早期执行，早于所有测试模块的 import"""
    import werkzeug
    try:
        werkzeug.__version__ = version("werkzeug")
    except PackageNotFoundError:
        werkzeug.__version__ = "0.0.0"
