"""
pytest 配置：werkzeug 版本兼容 patch

根因：Flask 2.3.0 的 flask/testing.py 直接引用 werkzeug.__version__，
而 Werkzeug 3.0+ 将 __version__ 移至 werkzeug.version.__version__。
此 patch 在 pytest 收集测试之前、任何测试代码导入 werkzeug 之前生效，
不影响其他使用 Werkzeug 3.x 的代码。

在 requirements.txt 中声明为 Werkzeug==3.0.1，
但 Xcode Python 3.9 环境实际装的是 Werkzeug 3.0.1，
而系统 site-packages 中的 Flask 是 2.3.0（来自 Xcode.app 自带的旧版）。
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
