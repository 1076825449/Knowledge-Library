# database/queries/ 说明

本目录存放常用查询示例，供调试和参考使用。

## 查询示例

| 文件 | 说明 |
|------|------|
| `get_question_detail.sql` | 查询问题详情及政策依据 |
| `get_questions_by_stage.sql` | 按生命周期阶段查询问题 |
| `get_questions_by_tag.sql` | 按标签查询问题 |
| `get_recent_updates.sql` | 查询最近更新的问题 |
| `search_questions.sql` | 关键词搜索问题 |

## 使用方式

```bash
sqlite3 tax_knowledge.db < get_question_detail.sql
```

或在 SQLite 交互界面：

```sql
.read get_question_detail.sql
```
