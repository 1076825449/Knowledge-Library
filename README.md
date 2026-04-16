# 企业全生命周期税务问题知识库

## 项目概述

本项目用于建设一个"企业全生命周期税务问题知识库网站"，特点是以"实际问题—答案"的形式组织内容，而非按文件罗列。

覆盖企业从**设立、开业、日常经营、变更、风险异常、停业、注销**的全生命周期。

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
├─ PROJECT_MANIFEST.md     # 项目总纲
├─ PROJECT_STRUCTURE.md    # 目录结构规范
├─ .gitignore
├─ .env.example
│
├─ database/              # 数据库
│   ├─ schema/            # 建表 SQL（按顺序执行）
│   ├─ seed/              # 初始化数据
│   ├─ queries/           # 常用查询示例
│   ├─ db/                # 数据库文件（.gitignore 忽略）
│   └─ README.md
│
├─ frontend/              # 前端（骨架）
├─ backend/               # 后端（骨架）
├─ scripts/              # 辅助脚本（骨架）
├─ docs/                 # 补充文档（骨架）
├─ tests/                # 测试（骨架）
├─ data/                 # 导入导出数据（骨架）
└─ assets/               # 静态资源（骨架）
```

## 真实运行方式

```bash
# 启动服务（无需安装任何依赖）
cd /Volumes/外接硬盘/vibe\ coding/知识库
python backend/app.py
# 访问 http://localhost:5000

# 编辑功能（新建/编辑问题）
# 首次访问 /question/new 或 /question/<code>/edit 时需输入管理员密码
# 默认密码：tax2026
# 修改密码：export ADMIN_PASSWORD=你的密码 && python backend/app.py
```

### 一键初始化数据库（如需重新创建）

```bash
cd /Volumes/外接硬盘/vibe\ coding/知识库
bash scripts/db/init_db.sh
```

脚本会自动：建表 → 初始化字典 → 插入示例问题 → 插入扩展问题（15条）→ 插入标签关联与问题关系

## 常用查询

```sql
-- 按阶段查询问题
SELECT question_code, question_title, one_line_answer
FROM question_master
WHERE stage_code = 'SET' AND status = 'active';

-- 查询问题详情与政策依据
SELECT q.question_title, p.policy_name, p.document_no, qpl.support_type
FROM question_master q
JOIN question_policy_link qpl ON q.id = qpl.question_id
JOIN policy_basis p ON qpl.policy_id = p.id
WHERE q.question_code = 'SET-REG-001';

-- 查询高频问题
SELECT question_code, question_title FROM question_master
WHERE high_frequency_flag = 1 AND status = 'active';

-- 查询最近更新
SELECT question_code, question_title, updated_at
FROM question_master ORDER BY updated_at DESC LIMIT 10;
```

## 核心文档说明

| 文档 | 作用 |
|------|------|
| `PROJECT_MANIFEST.md` | 项目总纲，介绍项目定位、愿景、设计原则 |
| `AGENTS.md` | 给 agent 立规则，规定优先级、禁止事项、决策顺序 |
| `TASKS.md` | 任务拆解清单，8 个 Phase，可逐阶段验收 |
| `CONTENT_SPEC.md` | 问题卡片写作规范，保证内容质量标准 |
| `PROJECT_STRUCTURE.md` | 目录结构规范，规定文件摆放位置 |

## 设计原则

1. **问题卡片为核心** - 一个问题就是一个独立知识单元
2. **内容与依据分离** - 问题内容不与政策依据混在一起
3. **结构稳定可扩展** - 新增问题通过新增记录实现，不破坏整体结构
4. **便于后续扩展** - 支持网站展示、AI检索、向量化的结构化清洗

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

## 技术栈（当前实际）

- **数据库**：SQLite（`database/db/tax_knowledge.db`）
- **后端**：Python Flask（`backend/app.py` 单入口）
- **前端**：Jinja2 服务端模板（`frontend/templates/`），无前端框架
- **样式**：原生CSS（`frontend/static/css/style.css`）

---

**创建日期**：2026-04-15
**最后更新**：2026-04-15
