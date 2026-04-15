# ============================================================
# backend/config.py
# 应用配置
# ============================================================

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'db', 'tax_knowledge.db')

class Config:
    DB_PATH = DB_PATH
