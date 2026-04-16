# 企业税务知识库 — 部署说明

## 方式一：直接运行（最小部署）
```bash
# 1. 安装依赖
pip install Flask==3.0.0 Jinja2==3.1.3 Werkzeug==3.0.1

# 2. 启动
cd backend
python app.py
# 默认监听 localhost:5000
```

## 方式二：Gunicorn 部署
```bash
pip install gunicorn
cd backend
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

## 方式三：Docker 部署
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "backend/app.py"]
```

## 环境变量
- FLASK_ENV=production  # 关闭 debug 模式
- DATABASE_PATH=/path/to/tax_knowledge.db

## 目录结构
```
backend/          — Flask 应用
frontend/         — 静态文件和模板
database/         — SQLite 数据库和备份
scripts/          — 运维脚本
data/imports/     — 批量导入 JSON
data/exports/     — AI 导出数据
data/reports/     — 质量报告
```

## 备份策略
```bash
# 每周备份
python scripts/ops/backup_db.py

# crontab 示例（每周日凌晨3点）
# 0 3 * * 0 cd /path/to/knowledge-base && /usr/bin/python3 scripts/ops/backup_db.py
```