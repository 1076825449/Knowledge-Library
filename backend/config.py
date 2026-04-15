# ============================================================
# backend/config.py
# 应用配置
# ============================================================

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'db', 'tax_knowledge.db')

class Config:
    DB_PATH = DB_PATH
    # 编辑页面访问密码（修改这里或通过环境变量 ADMIN_PASSWORD 覆盖）
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'tax2026')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tax-knowledge-library-secret-2026')
