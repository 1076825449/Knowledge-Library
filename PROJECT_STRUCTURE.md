# PROJECT_STRUCTURE.md

## 1. 文件目的

本文件用于规定"企业全生命周期税务问题知识库网站"项目的推荐目录结构、文件组织方式、命名原则和分层思路。

目标是：

- 让项目从一开始就有清晰结构
- 避免文档、SQL、页面、脚本、数据混乱堆放
- 让 agent 能快速知道每类文件应该放在哪里
- 为后续网站开发、数据维护、搜索增强、AI 扩展预留空间

**本文件是一份推荐结构说明。在实际开发中可以做适度调整，但总体原则不应被破坏。**

---

## 2. 总体原则

### 2.1 按职责分层，而不是按临时方便堆放

应区分：
- 项目文档
- 数据库脚本
- 初始数据
- 后端或数据访问层
- 前端页面
- 组件
- 内容导入导出工具
- 测试
- 构建与运行配置

### 2.2 文档优先放在清晰位置

本项目文档非常重要，不能散放。必须明确区分：
- 总纲类文档
- agent 规则类文档
- 内容规范类文档
- 项目任务类文档
- 技术说明类文档

### 2.3 数据层与展示层分开

不能把数据库结构、示例数据、页面代码、抓取脚本混在一起。

### 2.4 未来扩展要有位置

当前阶段先做最小可用，但目录应预留：
- 搜索增强
- 后台录入
- 地方口径
- AI 检索
- 测试
- 部署

---

## 3. 推荐顶层目录结构

```
project-root/
├─ README.md
├─ AGENTS.md
├─ TASKS.md
├─ CONTENT_SPEC.md
├─ PROJECT_STRUCTURE.md
├─ LICENSE
├─ .gitignore
├─ .env.example
│
├─ docs/
├─ database/
├─ scripts/
├─ data/
├─ backend/
├─ frontend/
├─ tests/
└─ assets/
```

---

## 4. 根目录文件说明

| 文件 | 说明 |
|------|------|
| `README.md` | 项目总纲、产品定位、知识工程原则、网站目标、阶段规划说明 |
| `AGENTS.md` | 给 agent 的执行规则、优先级和禁止事项 |
| `TASKS.md` | 项目任务拆解与阶段清单 |
| `CONTENT_SPEC.md` | 问题卡片写作规范、内容字段标准、审核标准 |
| `PROJECT_STRUCTURE.md` | 即本文件，规定目录和文件组织方式 |
| `LICENSE` | 开源协议或内部项目版权说明 |
| `.gitignore` | 忽略不应提交到仓库的文件 |
| `.env.example` | 环境变量示例文件 |

---

## 5. docs/ 目录

**作用：** 存放补充性的项目文档、专题说明、开发说明、接口文档、页面说明等。

```
docs/
├─ product/      # 产品层面文档
├─ content/       # 内容建设文档
├─ tech/         # 技术实现文档
├─ api/          # API 文档
└─ changelogs/   # 变更记录
```

| 子目录 | 内容示例 |
|--------|---------|
| `docs/product/` | `homepage_spec.md`, `search_spec.md`, `detail_page_spec.md`, `roadmap.md` |
| `docs/content/` | `tag_guide.md`, `review_flow.md`, `policy_citation_guide.md`, `local_rule_guide.md` |
| `docs/tech/` | `database_notes.md`, `search_design.md`, `deployment.md`, `architecture.md` |
| `docs/api/` | `endpoints.md`, `response_examples.md` |
| `docs/changelogs/` | `2026-04.md`, `release_notes.md` |

---

## 6. database/ 目录

**作用：** 存放数据库相关内容，包括建表 SQL、初始化字典 SQL、示例数据 SQL、数据迁移脚本、数据库文件（如 SQLite）、查询示例、数据结构说明。

```
database/
├─ schema/          # 建表 SQL
├─ seed/             # 初始化数据
├─ migrations/       # 迁移脚本
├─ queries/          # 查询示例
├─ db/               # 数据库文件
└─ README.md
```

### 6.1 database/schema/ 建表顺序

| 文件 | 内容 |
|------|------|
| `001_create_core_tables.sql` | question_master, policy_basis, tag_dict |
| `002_create_relation_tables.sql` | question_policy_link, question_tag_link, question_update_log, question_relation, local_rule_note |
| `003_create_indexes.sql` | 所有索引 |

### 6.2 database/seed/ 初始化数据顺序

| 文件 | 内容 |
|------|------|
| `001_seed_dicts.sql` | 生命周期阶段、主题模块、问题类型、状态等字典 |
| `002_seed_sample_data.sql` | 示例问题、政策依据、关联数据 |

### 6.3 database/queries/ 常用查询

| 文件 | 说明 |
|------|------|
| `get_question_detail.sql` | 查询问题详情与政策依据 |
| `get_questions_by_stage.sql` | 按阶段查询 |
| `get_questions_by_tag.sql` | 按标签查询 |
| `get_recent_updates.sql` | 最近更新 |
| `search_questions.sql` | 关键词搜索 |

---

## 7. scripts/ 目录

**作用：** 存放辅助脚本，包括初始化脚本、导入导出脚本、数据清洗脚本、批量生成脚本、本地运行辅助脚本。

```
scripts/
├─ db/          # 数据库脚本
├─ import/       # 导入脚本
├─ export/       # 导出脚本
├─ content/      # 内容辅助脚本
└─ dev/          # 开发辅助脚本
```

| 子目录 | 脚本示例 |
|--------|---------|
| `scripts/db/` | `init_db.sh`, `reset_db.sh`, `backup_db.sh` |
| `scripts/import/` | `import_questions.py`, `import_policies.py`, `import_tags.py` |
| `scripts/export/` | `export_questions_to_json.py`, `export_for_search.py`, `export_for_ai_chunks.py` |
| `scripts/content/` | `validate_question_fields.py`, `check_missing_policy_links.py` |
| `scripts/dev/` | `start_dev.sh`, `lint.sh`, `format.sh` |

---

## 8. data/ 目录

**作用：** 存放非数据库直连的结构化数据文件、临时导入导出文件、内容草稿转换结果等。

```
data/
├─ imports/      # 准备导入数据库的原始文件
├─ exports/       # 数据库导出的结构化文件
├─ templates/     # 录入模板
└─ drafts/        # 尚未正式入库的内容草稿
```

| 子目录 | 内容示例 |
|--------|---------|
| `data/imports/` | `sample_questions.csv`, `sample_policies.csv` |
| `data/exports/` | `questions.json`, `policy_basis.json`, `search_index.json` |
| `data/templates/` | `question_card_template.csv`, `policy_basis_template.csv` |
| `data/drafts/` | `first_batch_questions.md`, `pending_review_questions.csv` |

---

## 9. backend/ 目录

**作用：** 存放后端逻辑。当前为单文件Flask入口（`backend/app.py`），路由和业务逻辑均在内。

```
backend/
├─ app.py              # Flask 唯一入口，所有路由在此
├─ config.py           # 数据库路径、管理员密码、密钥配置
├─ routes/             # API蓝图（前后端分离备用）
│   ├─ questions.py   # 问题列表/详情API
│   ├─ search.py     # 搜索API
│   └─ tags.py        # 标签API
├─ services/          # 业务逻辑层
│   └─ question_service.py  # 问题CRUD、搜索、详情查询
└─ README.md
```

|| 子目录 | 内容 |
|--------|------|
|| `backend/routes/` | `questions.py`, `search.py`, `tags.py` |
|| `backend/services/` | `question_service.py`（唯一服务文件）|

---

## 10. frontend/ 目录

**当前实际：** 使用 Jinja2 服务端模板（无前端框架），由 Flask `render_template()` 调用。

```
frontend/
├─ templates/           # Jinja2 HTML模板
│   ├─ base.html       # 基础模板（导航栏、页脚）
│   ├─ index.html      # 首页
│   ├─ questions.html  # 问题列表页
│   ├─ detail.html     # 问题详情页
│   ├─ new_question.html    # 新建问题表单
│   ├─ edit_question.html   # 编辑问题表单
│   └─ admin_login.html     # 管理员登录页
├─ static/
│   └─ css/
│       └─ style.css   # 全局样式（CSS变量定义）
└─ README.md
```

### 10.1 frontend/templates/ 页面

|| 模板 | 对应URL |
|------|---------|
| `index.html` | `/` |
| `questions.html` | `/questions` |
| `detail.html` | `/question/<code>` |
| `new_question.html` | `/question/new` |
| `edit_question.html` | `/question/<code>/edit` |
| `admin_login.html` | `/admin/login` |

---

## 11. tests/ 目录

**作用：** 存放测试代码和测试数据。

```
tests/
├─ backend/       # 后端逻辑测试
├─ frontend/      # 前端页面/组件测试
├─ database/      # 数据库层测试
└─ fixtures/       # 测试用示例数据
```

---

## 12. assets/ 目录

**作用：** 存放项目级静态资源，如 logo、图标、页面示意图、原型图等。

```
assets/
├─ icons/         # 图标
├─ images/         # 图片
└─ mockups/        # 原型图
```

---

## 13. 文件命名原则

### 13.1 文档文件

统一使用大写英文单词加下划线，或清晰的英文命名：
- `README.md`
- `AGENTS.md`
- `TASKS.md`
- `CONTENT_SPEC.md`

### 13.2 SQL 文件

建议加编号和明确作用：
- `001_create_core_tables.sql`
- `002_create_relation_tables.sql`
- `003_create_indexes.sql`
- `001_seed_dicts.sql`

### 13.3 数据文件

建议按用途命名，不要只叫 `data1.csv`、`temp.json`。

---

## 14. 当前阶段已创建的文件

### 根目录文档

- [x] `README.md`
- [x] `AGENTS.md`
- [x] `TASKS.md`
- [x] `CONTENT_SPEC.md`
- [x] `PROJECT_STRUCTURE.md`
- [x] `.gitignore`
- [x] `.env.example`

### database/

- [x] `database/schema/001_create_core_tables.sql`
- [x] `database/schema/002_create_relation_tables.sql`
- [x] `database/schema/003_create_indexes.sql`
- [x] `database/seed/001_seed_dicts.sql`
- [x] `database/seed/002_seed_sample_data.sql`
- [x] `database/README.md`
- [x] `database/queries/README.md`

### 前端骨架

- [x] `frontend/README.md`
- [x] `frontend/templates/base.html`
- [x] `frontend/templates/index.html`
- [x] `frontend/templates/questions.html`
- [x] `frontend/templates/detail.html`
- [x] `frontend/templates/new_question.html`
- [x] `frontend/templates/edit_question.html`
- [x] `frontend/templates/admin_login.html`
- [x] `frontend/static/css/style.css`

### 后端骨架

- [x] `backend/README.md`
- [x] `backend/app.py`
- [x] `backend/config.py`
- [x] `backend/routes/questions.py`
- [x] `backend/routes/search.py`
- [x] `backend/routes/tags.py`
- [x] `backend/services/question_service.py`

### 脚本骨架

- [x] `scripts/db/init_db.sh`
- [x] `scripts/README.md`

---

## 15. 目录结构完成标准

如果满足以下条件，可以认为项目结构初步合格：

- [x] 核心文档都在根目录
- [x] 数据库脚本集中在 `database/`
- [x] 前端页面和组件在 `frontend/`
- [x] 脚本不与页面代码混放
- [x] 数据模板和导入导出文件有专门位置
- [x] 项目未来扩展方向有明确容器目录

---

## 16. 最终原则提醒

项目目录的目标不是"看起来专业"，而是：

1. 让人容易找到文件
2. 让 agent 不容易放错内容
3. 让开发顺序清楚
4. 让后续扩展不混乱
5. 让知识库建设和网站开发能长期共存

**一句话原则：文档有文档的位置，数据库有数据库的位置，页面有页面的位置，脚本有脚本的位置，内容有内容的位置。**
