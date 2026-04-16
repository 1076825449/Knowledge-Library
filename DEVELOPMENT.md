# 企业税务知识库 — 开发说明

## 环境准备
```bash
cd /Volumes/外接硬盘/vibe\ coding/知识库
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 启动开发服务器
```bash
source venv/bin/activate
cd backend
python app.py
# 访问 http://localhost:5000
```

## 数据库操作
```bash
# 查看数据
sqlite3 database/db/tax_knowledge.db "SELECT COUNT(*) FROM question_master"

# 备份（自动保留10份）
python scripts/ops/backup_db.py

# 数据质量巡检
python scripts/content/quality_report.py

# 导出 AI 数据
python scripts/export/export_for_ai.py
python scripts/export/export_chunks.py

# 批量导入新问题
python scripts/content/batch_import_questions.py data/imports/your_batch.json
```

## 数据库结构
- 8张表：question_master, policy_basis, tag_dict, question_policy_link, question_tag_link, question_update_log, question_relation, local_rule_note
- 所有连接启用 FK 约束（PRAGMA foreign_keys = ON）

## 内容维护
- 所有新增问题通过 batch_import_questions.py 导入
- 导入前运行 quality_report.py 检查现有数据质量
- 定期运行 backup_db.py 备份数据库