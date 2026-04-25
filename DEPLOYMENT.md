# 企业税务知识库 — 部署说明

## 目标

本项目当前采用单体部署：

- Web：Flask + Gunicorn
- 数据：SQLite 文件
- 静态资源：由 Flask 直接提供

适合以下场景：

- 本地私有部署
- 单机内网部署
- 轻量云主机部署
- 容器化单实例部署

不适合以下场景：

- 多实例横向扩容且共用 SQLite
- 高频并发写入
- 复杂后台协作编辑

## 部署前检查

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/ops/check_env.py
python -m pytest tests/ -q
python scripts/content/quality_report.py
```

## 环境变量

生产部署至少应设置以下变量：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SECRET_KEY` | `tax-knowledge-library-secret-2026` | Flask 会话密钥，生产必须替换 |
| `ADMIN_PASSWORD` | `tax2026` | 后台编辑密码，生产必须替换 |
| `HOST` | `0.0.0.0` | 监听地址 |
| `PORT` | `5000` | 服务端口 |
| `FLASK_DEBUG` | `0` | 生产环境必须关闭 |
| `DATABASE_PATH` | `database/db/tax_knowledge.db` | SQLite 数据库文件路径 |
| `SITE_URL` | `http://127.0.0.1:5000` | 站点对外访问地址，用于 canonical / sitemap / robots |
| `SITE_NAME` | `企业税务知识库` | 站点名称 |
| `SITE_DESCRIPTION` | 内置默认描述 | 站点公共描述文案 |

示例：

```bash
export SECRET_KEY='replace-with-a-long-random-secret'
export ADMIN_PASSWORD='replace-with-a-strong-password'
export HOST='0.0.0.0'
export PORT='5000'
export FLASK_DEBUG='0'
export DATABASE_PATH='/opt/tax-knowledge/database/db/tax_knowledge.db'
export SITE_URL='https://your-domain.example.com'
```

## 方式一：Gunicorn 直接部署

这是当前最推荐的最小生产方案。

```bash
git clone <your-repo-url>
cd Knowledge-Library

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

mkdir -p database/db database/backups data/reports data/exports

# 全新初始化时执行
bash scripts/db/init_db.sh

# 已有数据库时，把数据库文件放到 DATABASE_PATH 指向的位置
gunicorn --workers 2 --threads 4 --timeout 60 --bind 0.0.0.0:5000 wsgi:app
```

如果使用 systemd，推荐的 `ExecStart` 类似：

```ini
ExecStart=/opt/tax-knowledge/.venv/bin/gunicorn --workers 2 --threads 4 --timeout 60 --bind 0.0.0.0:5000 wsgi:app
WorkingDirectory=/opt/tax-knowledge
```

## 方式二：Docker 部署

仓库已经提供：

- [Dockerfile](/Volumes/外接硬盘/vibe coding/网站/知识库/Dockerfile)
- [docker-compose.yml](/Volumes/外接硬盘/vibe coding/网站/知识库/docker-compose.yml)
- [Procfile](/Volumes/外接硬盘/vibe coding/网站/知识库/Procfile)
- [wsgi.py](/Volumes/外接硬盘/vibe coding/网站/知识库/wsgi.py)
- [deploy/nginx/tax-knowledge.conf.example](/Volumes/外接硬盘/vibe coding/网站/知识库/deploy/nginx/tax-knowledge.conf.example)
- [deploy/systemd/tax-knowledge.service.example](/Volumes/外接硬盘/vibe coding/网站/知识库/deploy/systemd/tax-knowledge.service.example)

构建镜像：

```bash
docker build -t tax-knowledge:latest .
```

运行容器：

```bash
docker run -d \
  --name tax-knowledge \
  -p 5000:5000 \
  -e SECRET_KEY='replace-with-a-long-random-secret' \
  -e ADMIN_PASSWORD='replace-with-a-strong-password' \
  -e FLASK_DEBUG='0' \
  -e DATABASE_PATH='/app/database/db/tax_knowledge.db' \
  -v $(pwd)/database/db:/app/database/db \
  -v $(pwd)/database/backups:/app/database/backups \
  tax-knowledge:latest
```

如果是全新容器部署，先在宿主机初始化数据库：

```bash
bash scripts/db/init_db.sh
```

再挂载 `database/db` 目录启动容器。

也可以直接使用：

```bash
docker compose up -d --build
```

## 方式三：支持 Procfile 的平台

仓库根目录已提供 [Procfile](/Volumes/外接硬盘/vibe coding/网站/知识库/Procfile)：

```bash
web: gunicorn --workers 2 --threads 4 --timeout 60 --bind 0.0.0.0:${PORT:-5000} wsgi:app
```

适用于支持 Procfile 的轻量 PaaS，但前提仍是：

- 平台允许持久化或挂载 SQLite 文件
- 只运行单实例

如果平台不支持持久化磁盘，不建议直接部署当前 SQLite 版本。

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
data/reports/     → 建议保留写权限（质量巡检报告输出）
```

## 上线后最小运维动作

推荐固定执行以下动作：

```bash
# 部署前检查
python scripts/ops/deploy_preflight.py

# 每次内容批量更新后
python scripts/content/quality_report.py
python -m pytest tests/ -q

# 每天或每次重要更新后
python scripts/ops/backup_db.py
```

## 当前部署结论

截至当前仓库状态，项目已经具备最小生产部署闭环：

- 支持 `DATABASE_PATH / PORT / HOST / FLASK_DEBUG` 环境变量
- 支持 `SITE_URL / SITE_NAME / SITE_DESCRIPTION` 站点级环境变量
- 提供 Gunicorn WSGI 入口
- 提供 Dockerfile
- 提供 Procfile
- 提供数据库初始化、备份、质量巡检和测试命令
- 提供 `robots.txt`、`sitemap.xml` 和公开说明页面

后续如果继续产品化，下一步应考虑：

1. 反向代理（Nginx/Caddy）
2. HTTPS 与域名接入
3. SQLite 向 PostgreSQL/MySQL 迁移预案
4. 管理员操作日志与只读公开访问分层
