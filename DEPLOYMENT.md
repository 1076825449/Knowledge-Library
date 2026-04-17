# 企业税务知识库 — 部署说明

## 快速启动

```bash
git clone git@github.com:1076825449/Knowledge-Library.git
cd Knowledge-Library

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
bash scripts/db/init_db.sh

cd backend && python app.py
# → http://localhost:5000
```

## 部署方式

### 方式一：直接运行（开发 / 最小部署）

```bash
source venv/bin/activate
cd backend && python app.py
# Flask 监听 localhost:5000
```

### 方式二：Gunicorn（生产推荐）

```bash
pip install gunicorn
cd backend
gunicorn -w 2 -b 0.0.0.0:5000 --timeout 60 app:app
```

### 方式三：Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "--timeout", "60", "backend/app:app"]
```

```bash
docker build -t tax-knowledge .
docker run -d -p 5000:5000 \
  -v $(pwd)/database/db:/app/database/db \
  tax-knowledge
```

## 数据库初始化与恢复

### 方式一：使用初始化脚本（推荐）

```bash
bash scripts/db/init_db.sh
# 脚本依次执行：建表 → 字典数据 → 示例问题 → 扩展问题 → 标签和关系
```

### 方式二：从 SQL 脚本重建（全新）

```bash
mkdir -p database/db
sqlite3 database/db/tax_knowledge.db < database/schema/001_create_core_tables.sql
sqlite3 database/db/tax_knowledge.db < database/schema/002_create_relation_tables.sql
sqlite3 database/db/tax_knowledge.db < database/schema/003_create_indexes.sql
sqlite3 database/db/tax_knowledge.db < database/seed/001_seed_dicts.sql
sqlite3 database/db/tax_knowledge.db < database/seed/002_seed_sample_data.sql
sqlite3 database/db/tax_knowledge.db < database/seed/003_seed_expand_content.sql
sqlite3 database/db/tax_knowledge.db < database/seed/003b_seed_tags_and_relations.sql

# 验证
sqlite3 database/db/tax_knowledge.db ".tables"
# 应输出：local_rule_note policy_basis question_master question_policy_link
#         question_relation question_tag_link question_update_log tag_dict

sqlite3 database/db/tax_knowledge.db "PRAGMA foreign_keys;"
# 应输出：foreign_keys = 1
```

### 方式三：使用已有数据库

```bash
mkdir -p database/db
cp /path/to/backup/tax_knowledge.db database/db/tax_knowledge.db
```

### 数据库备份与恢复

**备份：**
```bash
python scripts/ops/backup_db.py
# 备份保存到 database/backups/，保留最近10份
```

**恢复：**
```bash
ls database/backups/
cp database/backups/tax_knowledge_YYYYMMDD_HHMMSS.db database/db/tax_knowledge.db
```

**定时备份（crontab）：**
```bash
# 每天凌晨3点备份
0 3 * * * cd /path/to/Knowledge-Library && /usr/bin/python3 scripts/ops/backup_db.py >> logs/backup.log 2>&1
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `FLASK_ENV` | `development` | production 模式下关闭 debug |
| `FLASK_SECRET_KEY` | （空） | 生产环境必须设置随机密钥 |
| `ADMIN_PASSWORD` | `tax2026` | 编辑页面访问密码，生产环境必须更换 |
| `DATABASE_PATH` | `database/db/tax_knowledge.db` | 可指定外部数据库路径 |

**重要**：首次部署前必须更改 `ADMIN_PASSWORD`：
```bash
export ADMIN_PASSWORD='your-strong-password-here'
cd backend && python app.py
```

## 测试

```bash
# 运行全部测试
python3 -m pytest tests/ -q

# 运行指定测试
python3 -m pytest tests/backend/test_routes.py -v
python3 -m pytest tests/database/ -v

# 带覆盖率
pip install pytest-cov
python3 -m pytest tests/ --cov=backend --cov-report=term-missing
```

## 目录权限

```
database/db/      → 需要读写权限（SQLite 需要写锁文件）
database/backups/ → 需要写权限
logs/             → 需要写权限（如启用日志）
data/exports/     → 自动创建（运行时）
```

## 目录结构总览

```
backend/           — Flask 应用（含路由、服务、配置）
frontend/          — Jinja2 模板和静态文件
database/
  schema/          — 建表 SQL 脚本（可重建数据库）
  seed/            — 初始化数据
  db/              — SQLite 数据文件（不纳入版本控制）
  backups/         — 自动备份（保留10份）
scripts/
  db/init_db.sh   — 数据库初始化脚本
  content/         — 内容管理（导入、审计、报告）
  export/          — AI 检索数据导出
  ops/             — 运维脚本（备份、环境检查）
data/
  imports/         — 批量导入 JSON 源文件（纳入版本控制）
  exports/         — 导出数据（每次运行重新生成，不纳入版本控制）
tests/             — 测试套件
```
