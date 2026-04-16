# 企业税务知识库 — 部署说明

## 快速启动

```bash
# 克隆项目
git clone git@github.com:1076825449/Knowledge-Library.git
cd Knowledge-Library

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动（开发模式）
cd backend && python app.py
# → http://localhost:5000
```

## 部署方式

### 方式一：直接运行（开发/最小部署）

```bash
source venv/bin/activate
cd backend
python app.py
# Flask debug 模式，监听 localhost:5000
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

### 方式一：使用已有数据库

项目克隆后，将已有的 `tax_knowledge.db` 复制到 `database/db/` 目录：

```bash
mkdir -p database/db
cp /path/to/backup/tax_knowledge_20260416.db database/db/tax_knowledge.db
```

### 方式二：从 SQL 脚本重建（全新）

```bash
# 创建空数据库并执行建表脚本
sqlite3 database/db/tax_knowledge.db < database/schema/001_create_core_tables.sql
sqlite3 database/db/tax_knowledge.db < database/schema/002_create_relation_tables.sql
sqlite3 database/db/tax_knowledge.db < database/schema/003_create_indexes.sql

# 验证建表
sqlite3 database/db/tax_knowledge.db ".tables"
# 应输出：local_rule_note policy_basis question_master question_policy_link
#         question_relation question_tag_link question_update_log tag_dict

# 验证 FK
sqlite3 database/db/tax_knowledge.db "PRAGMA foreign_keys;"
# 应输出：foreign_keys = 1
```

### 数据库备份与恢复

**备份：**
```bash
python scripts/ops/backup_db.py
# 备份保存到 database/backups/，保留最近10份
```

**恢复：**
```bash
# 查看可用备份
ls database/backups/

# 恢复指定备份
cp database/backups/tax_knowledge_YYYYMMDD_HHMMSS.db database/db/tax_knowledge.db
```

**定时备份（crontab）：**
```bash
# 每天凌晨3点备份
0 3 * * * cd /path/to/知识库 && /usr/bin/python3 scripts/ops/backup_db.py >> logs/backup.log 2>&1

# 每周日凌晨4点全量备份+推送
0 4 * * 0 cd /path/to/知识库 && /usr/bin/python3 scripts/ops/backup_db.py && git add database/backups/ && git commit -m "chore: 周备份" && git push
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `FLASK_ENV` | `development` | production 模式下关闭 debug |
| `FLASK_SECRET_KEY` | （空） | 生产环境应设置随机密钥 |
| `DATABASE_PATH` | `database/db/tax_knowledge.db` | 可指定外部数据库路径 |

## 测试

```bash
# 运行全部测试（需在项目根目录）
cd /path/to/知识库
pytest tests/ -v

# 运行指定测试
pytest tests/database/test_schema.py -v
pytest tests/backend/test_question_service.py -v

# 带覆盖率
pytest tests/ --cov=backend --cov=scripts --cov-report=term-missing
```

## 目录权限

```
database/db/          → 需要读写权限（SQLite 需要写锁文件）
database/backups/     → 需要写权限
logs/                 → 需要写权限（如启用日志）
data/exports/         → 自动创建（运行时）
```

## 目录结构

```
backend/           — Flask 应用（含路由、服务、配置）
frontend/          — Jinja2 模板和静态文件
database/
  db/              — SQLite 数据文件（不纳入版本控制）
  schema/          — 建表 SQL 脚本（可重建数据库）
  backups/         — 自动备份（保留10份）
scripts/
  content/         — 内容管理（导入、审计、报告）
  export/          — AI 检索数据导出
  ops/             — 运维脚本（备份、环境检查）
data/
  imports/         — 批量导入 JSON 源文件（纳入版本控制）
  exports/         — 导出数据（每次运行重新生成，不纳入版本控制）
tests/             — 测试套件
```

## 环境检查

```bash
python scripts/ops/check_env.py
# 检查：Python 版本、已安装包、数据库连接、FK 状态
```
