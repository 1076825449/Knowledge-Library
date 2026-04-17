"""
pytest 配置：werkzeug 版本兼容 patch

根因：Flask 2.3.0 的 flask/testing.py 直接引用 werkzeug.__version__，
而 Werkzeug 3.0+ 将 __version__ 移至 werkzeug.version.__version__。

此 patch 在 pytest 收集阶段最早执行，早于所有测试模块的 import，
只影响 werkzeug 模块的版本属性查询，不修改任何 Flask/Werkzeug 内部逻辑，
不影响 Werkzeug 3.x 的其他功能（wsgi/test/serving 等均不受影响）。

hermes venv（Flask 3.0.0）下此 patch 不触发任何行为变更：
Flask 3.0 不引用 werkzeug.__version__，werkzeug 3.0 本身无 __version__ 顶域属性，
所以 patch 只是多打了一个兼容属性，不影响任何代码路径。
"""
import sys


def pytest_configure(config):
    """在 pytest 收集阶段最早期执行，早于所有测试模块的 import"""
    import werkzeug
    # werkzeug 2.x/3.x 把版本信息放在 werkzeug.version 模块
    try:
        import werkzeug.version
        werkzeug.__version__ = werkzeug.version.__version__
    except ImportError:
        # werkzeug 1.x 没有 werkzeug.version，尝试从 __init__.__version__
        werkzeug.__version__ = getattr(werkzeug, "__version__", "0.0.0")
