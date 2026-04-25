# 企业全生命周期税务问题知识库

## 项目概述

本项目用于建设一个"企业全生命周期税务问题知识库网站"，特点是以"实际问题—答案"的形式组织内容，而非按文件罗列。

覆盖企业从**设立、开业、日常经营、变更、风险异常、停业、注销**的全生命周期。

> 当前项目已经具备数据库、网站原型、内容导入、质量巡检和 AI 导出预留能力，但不应理解为已经达到最终目标。后续执行顺序和验收口径以 [ROADMAP.md](ROADMAP.md) 为准。

## 快速开始

```bash
# 1. 克隆项目
git clone git@github.com:1076825449/Knowledge-Library.git
cd Knowledge-Library

# 2. 创建虚拟环境（Python 3.11+）
python -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化数据库（全新时）
bash scripts/db/init_db.sh

# 5. 启动服务
cd backend && python app.py
# 服务地址: http://localhost:5000
```

## 当前产品定位

当前项目已经不是“从零原型”，更准确地说，它是一个：

- 已完成结构化数据底座的知识库网站
- 已具备搜索、筛选、详情、关联问题和质量巡检闭环的 Beta 产品
- 可以进入正式上线准备，但还不应直接宣称为“最终正式版 1.0”

正式上线前的验收口径，请同时查看：

- [ROADMAP.md](ROADMAP.md)
- [TASKS_PROGRESS.md](TASKS_PROGRESS.md)
- [LAUNCH_CHECKLIST.md](LAUNCH_CHECKLIST.md)
- [CONTENT_REVIEW_PLAYBOOK.md](CONTENT_REVIEW_PLAYBOOK.md)
- [RELEASE_POSITIONING.md](RELEASE_POSITIONING.md)

## 核心设计

### 8 张核心表

| 表名 | 用途 |
|------|------|
| `question_master` | 问题主表（24列，包含问题内容、政策依据、风险提示等所有字段）|
| `policy_basis` | 政策依据表（21列，包含文号、条款、政策层级、有效期、官方来源与核验状态等）|
| `question_policy_link` | 问题-政策关联表（6列：问题ID、政策ID、支撑类型、说明、排序）|
| `tag_dict` | 标签字典表 |
| `question_tag_link` | 问题-标签关联表 |
| `question_update_log` | 问题更新记录表 |
| `question_relation` | 关联问题表 |
| `local_rule_note` | 地方口径表 |

### 分类体系

**生命周期阶段 (stage_code)**
- SET = 设立期
- OPR = 开业/日常经营期
- CHG = 变更期
- RSK = 风险异常期
- SUS = 停业期
- CLS = 注销期

**主题模块 (module_code)**
- REG = 登记管理
- DEC = 申报纳税
- INV = 发票管理
- VAT = 增值税
- CIT = 企业所得税
- IIT = 个人所得税
- SSF = 社保费
- FEE = 成本费用
- PREF = 优惠政策
- RISK = 风险应对
- CLEAR = 清税注销
- TAX = 税务综合
- ETAX = 电子税务局/系统办理

### 当前数据体量

项目运行中的真实统计以数据库和质量报告为准，不在 README 中长期维护静态数字。

如需查看当前规模，请优先使用：

```bash
sqlite3 database/db/tax_knowledge.db "SELECT COUNT(*) FROM question_master;"
python scripts/content/quality_report.py
python scripts/content/audit_policy_verification.py
```

### 政策依据核验口径

税务政策变化快，正式内容不能只看已有结构是否完整。当前已为 `policy_basis` 增加官方来源和核验字段：`source_url`、`source_org`、`source_type`、`last_verified_at`、`verification_status`、`verification_note`。

后续新增或复核内容时，应先运行 `python scripts/content/audit_policy_verification.py` 查看政策核验队列；`source_found` 只表示找到官方来源，不能等同于答案已通过现行政策复核。

正式上线前还必须运行：

```bash
python scripts/content/policy_launch_gate.py
```

只有该门禁返回 `PASS`，才允许把当前内容口径提升为正式上线口径。

## 项目文件结构

```
Knowledge-Library/
├─ README.md              # 本文件
├─ AGENTS.md              # agent 行为约束
├─ TASKS.md               # 项目任务清单
├─ CONTENT_SPEC.md        # 问题卡片写作规范
├─ PROJECT_STRUCTURE.md   # 目录结构规范
├─ requirements.txt
├─ .env.example
│
├─ .github/workflows/     # GitHub Actions CI
│
├─ backend/               # Flask 应用
│   ├─ app.py            # 主入口（localhost:5000）
│   ├─ config.py         # 数据库路径配置
│   ├─ routes/           # 路由（questions, search, tags）
│   └─ services/         # 业务逻辑（QuestionService）
│
├─ frontend/             # Jinja2 模板 + CSS
│   └─ templates/         # HTML 模板
│
├─ database/
│   ├─ schema/           # 建表 SQL（按顺序执行）
│   ├─ seed/             # 初始化数据
│   ├─ db/               # 数据库文件（.gitignore 忽略）
│   └─ backups/          # 自动备份
│
├─ scripts/
│   ├─ db/init_db.sh    # 数据库初始化脚本
│   ├─ content/          # 内容管理（导入、审计、报告）
│   ├─ export/            # AI 检索导出
│   └─ ops/              # 运维脚本（备份、环境检查）
│
├─ data/
│   ├─ imports/          # 批量导入 JSON 源文件
│   ├─ exports/          # 导出数据（运行时生成）
│   └─ reports/          # 质量报告（运行时生成）
│
└─ tests/                # 测试套件
```

## 常用命令

### 启动服务（开发）

```bash
source venv/bin/activate
cd backend && python app.py
# http://localhost:5000
```

### 测试

```bash
# 运行全部测试
python3 -m pytest tests/ -q

# 运行指定测试文件
python3 -m pytest tests/backend/test_routes.py -v

# 环境检查
python scripts/ops/check_env.py

# 内容质量报告
python scripts/content/priority_reinforce.py
```

> 测试状态以当前环境实际执行结果为准，不在 README 中固定写死。

### 数据库

```bash
# 初始化（全新）
bash scripts/db/init_db.sh

# 备份
python scripts/ops/backup_db.py
```

### 部署

```bash
# 部署前检查
python scripts/ops/deploy_preflight.py

# Gunicorn 生产入口
make prod

# Docker Compose
docker compose up -d --build
```

### 公开页面与 SEO 路由

```bash
# 公开说明页
/about
/methodology
/launch-readiness

# 站点 SEO 基础路由
/robots.txt
/sitemap.xml
```

### 数据导出（AI 检索用）

```bash
python scripts/export/export_for_ai.py
python scripts/export/export_chunks.py
```

## 技术栈

- **数据库**：SQLite（`database/db/tax_knowledge.db`）
- **后端**：Python Flask（`backend/app.py` 单入口）
- **前端**：Jinja2 服务端模板（`frontend/templates/`），无前端框架
- **样式**：原生 CSS（`frontend/static/css/style.css`）

## 核心文档

| 文档 | 作用 |
|------|------|
| `AGENTS.md` | 给 agent 立规则，规定优先级、禁止事项、决策顺序 |
| `TASKS.md` | 项目任务拆解清单，8 个 Phase，可逐阶段验收 |
| `CONTENT_SPEC.md` | 问题卡片写作规范，保证内容质量标准 |
| `PROJECT_STRUCTURE.md` | 目录结构规范 |
| `DEVELOPMENT.md` | 开发说明，环境准备、日常命令、Git 工作流 |
| `DEPLOYMENT.md` | 部署说明，生产部署方式、备份恢复 |

## 当前阶段判断

按 [ROADMAP.md](ROADMAP.md) 的执行口径，当前项目应理解为：

- 数据底座已建立
- 网站最小闭环已建立
- 内容规模已具备基础体量
- AI 导出已有结构预留
- 但仍处于“统一口径 + 补结构质量 + 补覆盖短板”的阶段

当前最重要的不是继续宣称更多阶段“已完成”，而是优先解决：

1. 文档、数据库、页面、录入口径不完全一致
2. active 内容中仍存在结构字段、标签、更新记录、关联关系缺口
3. 录入维护闭环仍需继续打磨
4. 检索体验和 AI 检索 contract 仍需进一步统一

## 后续优先方向

后续工作优先顺序固定如下：

1. 统一事实源与枚举口径
2. 修正页面、API、表单、脚本之间的查询与展示分叉
3. 补齐结构字段、业务标签、更新记录、关联问题
4. 补齐 ETAX 和薄弱阶段 × 模块覆盖
5. 强化录入闭环、质量守门、检索体验
6. 推进 AI 检索增强与运营化内容复审

## 当前交付状态

截至当前仓库状态，项目已经完成以下闭环：

- 数据结构闭环
- 网站可运行闭环
- 内容质量守门闭环
- 高频问题密度闭环
- 阶段 × 模块覆盖闭环
- 最小生产部署闭环（Gunicorn / Docker / Procfile / WSGI）
- 公开说明与上线准备闭环（about / methodology / launch-readiness / robots / sitemap）

详细路线和验收标准见 [ROADMAP.md](ROADMAP.md)。

---

**创建日期**：2026-04-15
**最后更新**：2026-04-23
