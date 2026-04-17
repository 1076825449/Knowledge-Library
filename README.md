# 企业全生命周期税务问题知识库

## 项目概述

本项目用于建设一个"企业全生命周期税务问题知识库网站"，特点是以"实际问题—答案"的形式组织内容，而非按文件罗列。

覆盖企业从**设立、开业、日常经营、变更、风险异常、停业、注销**的全生命周期。

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

## 核心设计

### 8 张核心表

| 表名 | 用途 |
|------|------|
| `question_master` | 问题主表 |
| `policy_basis` | 政策依据表 |
| `question_policy_link` | 问题-政策关联表 |
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
- ETAX = 电子税务局/系统办理

## 项目文件结构

```
project-root/
├─ README.md              # 本文件
├─ AGENTS.md              # agent 行为约束
├─ TASKS.md               # 项目任务清单
├─ CONTENT_SPEC.md        # 问题卡片写作规范
├─ PROJECT_MANIFEST.md    # 项目总纲
├─ PROJECT_STRUCTURE.md   # 目录结构规范
├─ DEVELOPMENT.md         # 开发说明
├─ DEPLOYMENT.md          # 部署说明
├─ requirements.txt
├─ .env.example
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
│   └─ exports/          # 导出数据（运行时生成）
│
└─ tests/                # 测试套件
    ├─ backend/          # 路由 + 服务层测试
    └─ content/          # 内容脚本测试
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
```

当前测试状态：**71 passed**

### 数据库

```bash
# 初始化（全新）
bash scripts/db/init_db.sh

# 备份
python scripts/ops/backup_db.py
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
| `PROJECT_MANIFEST.md` | 项目总纲，介绍项目定位、愿景、设计原则 |
| `AGENTS.md` | 给 agent 立规则，规定优先级、禁止事项、决策顺序 |
| `TASKS.md` | 任务拆解清单，8 个 Phase，可逐阶段验收 |
| `CONTENT_SPEC.md` | 问题卡片写作规范，保证内容质量标准 |
| `DEVELOPMENT.md` | 开发说明，环境准备、日常命令、Git 工作流 |
| `DEPLOYMENT.md` | 部署说明，生产部署方式、备份恢复 |

## 当前阶段完成状态

| Phase | 内容 | 状态 |
|-------|------|------|
| Phase 0 | 项目基础文件与规范 | ✅ 已完成 |
| Phase 1 | 数据库与数据底座 | ✅ 已完成 |
| Phase 2 | 示例数据与内容模型验证 | ✅ 已完成 |
| Phase 3 | 后端读取能力 | ✅ 已完成 |
| Phase 4 | 网站最小可用前端 | ✅ 已完成 |
| Phase 5 | 检索、筛选增强 | ✅ 已完成 |
| Phase 6 | 内容录入便利化 | ✅ 已完成 |
| Phase 7 | 地方口径与专业增强 | ✅ 已完成 |
| Phase 8 | AI 检索预留 | ✅ 结构预留（内容未实现） |

---

**创建日期**：2026-04-15
**最后更新**：2026-04-18
