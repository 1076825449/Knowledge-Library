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
| `question_master` | 问题主表（24列，包含问题内容、政策依据、风险提示等所有字段）|
| `policy_basis` | 政策依据表（15列，包含文号、条款、政策层级、有效期等）|
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

| 指标 | 数量 |
|------|------|
| 问题总数 | 257 条（100% 有政策支撑）|
| 政策依据 | 89 条（全部有引用记录）|
| 政策链接 | 375 条 |

**问题分布（按模块）**

| 模块 | 数量 | 模块 | 数量 |
|------|------|------|------|
| REG | 43 | CIT | 18 |
| DEC | 34 | CLEAR | 18 |
| RISK | 39 | VAT | 16 |
| INV | 23 | IIT | 15 |
| PREF | 20 | FEE | 13 |
| SSF | 10 | TAX | 8 |

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
└─ tests/                # 测试套件（71 passed）
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

**当前测试状态：71 passed**

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
| `AGENTS.md` | 给 agent 立规则，规定优先级、禁止事项、决策顺序 |
| `TASKS.md` | 项目任务拆解清单，8 个 Phase，可逐阶段验收 |
| `CONTENT_SPEC.md` | 问题卡片写作规范，保证内容质量标准 |
| `PROJECT_STRUCTURE.md` | 目录结构规范 |
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
| Phase 8 | AI 检索预留 | ✅ 结构预留，数据就绪（257条/89条政策/375条链接） |

## 后续扩容方向（短板优先）

内容扩容不继续线性堆题，而是按以下优先级补短板：

1. **模块覆盖率低的模块**：TAX(8) / SSF(10) / FEE(13) / IIT(15) / VAT(16)
2. **高频问题群补强**：零申报、发票红字、欠税非正常户、注销清算等高频问题政策依据补强
3. **政策依据补强**：梳理仍可能存在空链接的问题；核查高频政策（GOV-Tax-001=28条引用）的支撑质量
4. **关联关系补强**：为问题补关联关系，提升知识库路径式使用体验
5. **内容质量审计**：通过 `priority_reinforce.py` 定期审计字段完整率和空值率

---

**创建日期**：2026-04-15
**最后更新**：2026-04-19
