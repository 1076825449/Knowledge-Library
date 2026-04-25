# ============================================================
# backend/config.py
# 应用配置
# ============================================================

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, 'database', 'db', 'tax_knowledge.db')


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}

class Config:
    DB_PATH = os.environ.get('DATABASE_PATH', DEFAULT_DB_PATH)
    # 编辑页面访问密码（修改这里或通过环境变量 ADMIN_PASSWORD 覆盖）
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'tax2026')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tax-knowledge-library-secret-2026')
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', '5000'))
    DEBUG = env_bool('FLASK_DEBUG', True)
    SITE_NAME = os.environ.get('SITE_NAME', '企业税务知识库')
    SITE_URL = os.environ.get('SITE_URL', f'http://127.0.0.1:{PORT}')
    SITE_DESCRIPTION = os.environ.get(
        'SITE_DESCRIPTION',
        '面向企业全生命周期税务问题的结构化知识库，提供问题卡片、政策依据、标签筛选与关联检索能力。'
    )
