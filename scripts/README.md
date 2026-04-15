# scripts/ 辅助脚本目录

## 目录结构

```
scripts/
├── README.md      # 本文件
├── db/            # 数据库脚本
├── import/        # 导入脚本
├── export/        # 导出脚本
├── content/       # 内容辅助脚本
└── dev/           # 开发辅助脚本
```

## db/ 数据库脚本

| 脚本 | 说明 |
|------|------|
| `init_db.sh` | 初始化数据库 |
| `reset_db.sh` | 重置数据库 |
| `backup_db.sh` | 备份数据库 |

## import/ 导入脚本

| 脚本 | 说明 |
|------|------|
| `import_questions.py` | 批量导入问题 |
| `import_policies.py` | 批量导入政策依据 |
| `import_tags.py` | 批量导入标签 |

## export/ 导出脚本

| 脚本 | 说明 |
|------|------|
| `export_questions_to_json.py` | 导出问题为 JSON |
| `export_for_search.py` | 导出用于搜索索引的数据 |
| `export_for_ai_chunks.py` | 导出用于 AI 切片的数据 |

## content/ 内容辅助脚本

| 脚本 | 说明 |
|------|------|
| `validate_question_fields.py` | 校验问题字段完整性 |
| `check_missing_policy_links.py` | 检查未关联政策的问题 |
| `generate_question_template.py` | 生成问题模板 |

## dev/ 开发辅助脚本

| 脚本 | 说明 |
|------|------|
| `start_dev.sh` | 启动本地开发环境 |
| `lint.sh` | 代码检查 |
| `format.sh` | 代码格式化 |
