# 企业税务知识库 — 开发说明

## 环境准备

```bash
# 克隆或进入项目目录
cd /path/to/知识库

# 创建虚拟环境（Python 3.11+）
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 验证环境
python scripts/ops/check_env.py
```

## 目录结构

```
知识库/
├── backend/                # Flask 应用
│   ├── app.py               # 主入口（localhost:5000）
│   ├── config.py            # 数据库路径配置
│   ├── routes/              # 路由（questions, search, tags）
│   ├── services/            # 业务逻辑（QuestionService）
│   └── static/              # 静态资源
├── frontend/                # 模板和样式
├── database/
│   ├── db/                  # SQLite 数据库文件（不提交到 Git）
│   │   └── tax_knowledge.db
│   └── schema/               # 建表 SQL 脚本
│       ├── 001_create_core_tables.sql
│       ├── 002_create_relation_tables.sql
│       └── 003_create_indexes.sql
├── scripts/
│   ├── content/             # 内容管理
│   │   ├── batch_import_questions.py    # 批量导入（INSERT 模式）
│   │   ├── audit_data.py               # 数据审计（14项检查）
│   │   └── quality_report.py            # 质量报告
│   ├── export/              # AI 检索导出
│   │   ├── export_for_ai.py             # 导出 JSON/JSONL
│   │   └── export_chunks.py             # 导出语义 chunk
│   └── ops/                 # 运维脚本
│       ├── backup_db.py                 # 数据库备份（保留10份）
│       └── check_env.py                 # 环境检查
├── data/
│   ├── imports/             # 批量导入 JSON 文件
│   │   └── questions_batch*.json
│   └── exports/             # AI 导出数据（每次运行重新生成）
├── tests/                   # 测试套件
│   ├── backend/
│   │   └── test_question_service.py     # 服务层测试
│   └── database/
│       └── test_schema.py               # 数据库结构测试
├── requirements.txt         # Python 依赖
└── .gitignore              # 已配置：*.db, data/exports/, venv/
```

## 日常开发命令

```bash
# 启动开发服务器（热重载）
source venv/bin/activate
cd backend
python app.py
# → http://localhost:5000

# 运行测试
cd /path/to/知识库
pytest tests/ -v

# 数据审计
python scripts/content/audit_data.py

# 质量报告
python scripts/content/quality_report.py

# 导出 AI 数据（每次内容更新后运行）
python scripts/export/export_for_ai.py
python scripts/export/export_chunks.py

# 数据库备份
python scripts/ops/backup_db.py
```

## 数据库说明

**8张表：**

| 表名 | 用途 | 关键列 |
|------|------|--------|
| `question_master` | 问题主体 | id, question_code, stage_code, module_code, answer_certainty, scope_level |
| `tag_dict` | 标签字典 | id, tag_code, tag_name, tag_category（module/stage/question_type/business_tag） |
| `policy_basis` | 政策库 | id, policy_code, document_no, article_ref, policy_level, effective_date |
| `question_policy_link` | 问题↔政策 | question_id, policy_id, support_type |
| `question_tag_link` | 问题↔标签 | question_id, tag_id, is_primary, display_order |
| `question_relation` | 关联问题 | question_id, related_id, relation_type |
| `question_update_log` | 更新记录 | question_id, update_type, old_value, new_value |
| `local_rule_note` | 地方口径 | id, region_scope, rule_summary, effective_date |

**枚举值约定（统一小写下划线格式）：**

| 字段 | 有效值 |
|------|--------|
| `stage_code` | SET, OPR, CHG, CLS, RSK, SUS |
| `module_code` | REG, DEC, INV, VAT, CIT, IIT, SSF, FEE, PREF, RISK, CLEAR, ETAX |
| `answer_certainty` | certain_clear, certain_conditional, certain_dispute, certain_practical |
| `scope_level` | scope_national, scope_local |
| `question_type` | type_whether, type_how, type_define, type_risk, type_time, type_what, type_why |

**连接数据库时必须启用 FK：**
```python
conn.execute("PRAGMA foreign_keys = ON")
```

## 代码规范

- Python 3.11+，无重型框架依赖
- Flask 路由 → services → database 分层
- 枚举值统一小写下划线（Python侧常量用全大写，DB存储用小写下划线）
- 批量导入必须通过 `batch_import_questions.py`，不得直接 SQL INSERT
- 导出脚本独立运行，不修改数据库

## Git 工作流

```bash
# 1. 开发前从 main 拉最新
git checkout main && git pull origin main

# 2. 创建功能分支
git checkout -b feat/content-batch7

# 3. 开发 + 测试

# 4. 提交（数据文件只提交 .json 源文件，不提交 .db）
git add database/db/tax_knowledge.db  # 仅 .db 文件（内容变更）
git add data/imports/questions_batch*.json  # 导入源文件
git add scripts/ backend/ tests/    # 代码变更
git commit -m "feat: ..."

# 5. 推送
git push origin feat/content-batch7
# → 创建 PR → review → merge to main
```

## 内容扩容流程

```bash
# 1. 写 JSON 批导入文件（参考 data/imports/questions_batch5_set.json）
# 字段名：question_title, question_plain, stage_code, module_code,
#         one_line_answer, detailed_answer, policy_basis, business_tags ...

# 2. 导入前审计现有数据
python scripts/content/audit_data.py

# 3. 执行导入
python scripts/content/batch_import_questions.py data/imports/your_batch.json

# 4. 验证
python scripts/content/audit_data.py

# 5. 重新导出 AI 数据
python scripts/export/export_for_ai.py
python scripts/export/export_chunks.py

# 6. 提交
git add database/db/tax_knowledge.db data/imports/your_batch.json
git commit -m "feat: 内容扩容 N 条"
git push origin main
```
