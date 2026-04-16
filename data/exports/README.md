# AI检索数据导出说明

## 概述

本目录由 `scripts/export/export_for_ai.py` 自动生成，包含知识库全部内容，用于：
1. **文本向量化**（embedding）：将问题文本转为向量存入向量数据库
2. **RAG检索**：根据用户问题召回最相关的问题和答案片段
3. **知识图谱构建**：基于政策关联和标签关系构建结构化知识网络

## 生成方式

```bash
cd /path/to/知识库
python scripts/export/export_for_ai.py
```

生成三个文件：
- `questions_full.json` — 完整知识库（113条，含所有字段和关联）
- `questions_for_embedding.jsonl` — 向量检索用（113条，每行一个JSON对象）
- `question_chunks.jsonl` — 语义chunk（~500条，每行一个chunk）

## 文件格式

### questions_for_embedding.jsonl（主要向量检索文件）

每行一个JSON对象，字段说明：

| 字段 | 类型 | 说明 |
|------|------|------|
| `question_code` | string | 唯一编码，如 `SET-DEC-001` |
| `question_title` | string | 问题标题（中文） |
| `stage_label` | string | 生命周期阶段，如 `设立期` |
| `module_label` | string | 税务模块，如 `申报纳税` |
| `question_type` | string | 问题类型，如 `type_whether` |
| `retrieval_text` | string | **主要检索文本**：问题+答案+政策摘要拼接 |
| `question_plain` | string | 问题原文（口语化） |
| `one_line_answer` | string | 一句话结论 |
| `detailed_answer` | string | 详细解答（长文本） |
| `core_definition` | string | 核心定义 |
| `practical_steps` | string | 实务步骤 |
| `risk_warning` | string | 风险提示 |
| `keywords` | string | 关键词（逗号分隔） |
| `policy_documents` | string | 政策文号列表（分号分隔） |
| `policy_count` | int | 关联政策数量 |
| `tags` | string | 标签名列表（逗号分隔） |
| `answer_certainty` | string | 结论稳定度代码 |
| `answer_certainty_label` | string | 结论稳定度中文 |
| `scope_level` | string | 适用范围代码 |
| `scope_level_label` | string | 适用范围中文 |
| `is_high_freq` | bool | 是否高频问题 |
| `is_newbie` | bool | 是否新手必看 |
| `related_question_codes` | string | 关联问题编码（逗号分隔） |
| `version_no` | int | 版本号 |
| `updated_at` | string | 最后更新时间 |

**推荐 embedding 策略：**

```
检索字段优先级：
1. retrieval_text  → 整体语义匹配（主要向量维度）
2. question_plain  → 问题理解
3. one_line_answer → 答案匹配
4. practical_steps → 实务指引匹配
```

**推荐RAG策略：**

```
用户问题 → embedding(retrieval_text) → top-k 召回
→ 提取 related_question_codes 扩展召回
→ 补充 policy_documents 原文引用
→ 组装答案（问题 + 结论 + 政策依据 + 实务步骤）
```

### question_chunks.jsonl（语义分段文件）

每个问题拆分为 2~5 个 chunk：

| chunk_type | 内容来源 | 用途 |
|------------|----------|------|
| `question_text` | question_plain + keywords | 问题语义 |
| `answer_core` | one_line_answer + core_definition | 核心结论 |
| `detailed_explanation` | detailed_answer 段落（最多3段） | 详细解读 |
| `practical_guidance` | practical_steps + risk_warning + applicable_conditions | 实务操作 |

字段：
```
chunk_id, question_code, chunk_type, content, stage_label, module_label, question_type, tags
```

### questions_full.json（完整知识库）

完整数据库 dump，含所有字段和政策/标签/关联问题的完整对象。用于构建知识图谱或完整备份。

## 向量数据库推荐配置

| 参数 | 推荐值 |
|------|--------|
| embedding 模型 | `text-embedding-3-small` 或 `bge-m3` |
| 向量维度 | 1536（text-embedding-3-small）或 1024（bge-m3） |
| 召回数量 top-k | 5~10 |
| 相似度阈值 | 0.5~0.65 |
| rerank | 推荐使用 `cohere/rerank` 对 top-20 rerank |

## 版本管理

- 每次内容更新后重新运行导出脚本
- 文件名不含版本号，CI/CD 环境建议使用时间戳备份：
  ```bash
  cp questions_for_embedding.jsonl "questions_for_embedding_$(date +%Y%m%d_%H%M%S).jsonl"
  ```
- 建议配合 `scripts/ops/backup_db.py` 每次备份数据库快照

## 字段覆盖度（2026-04-16）

| 字段 | 填充率 |
|------|--------|
| one_line_answer | 100% |
| detailed_answer | ~95% |
| policy_links | 100%（每题至少1条） |
| tag_links | 100%（每题至少1个） |
| related_questions | ~54%（61/113条有至少1个关联） |
| core_definition | ~95% |
| applicable_conditions | ~95% |
| practical_steps | ~95% |
| risk_warning | ~95% |

## 下一步

1. 将 `questions_for_embedding.jsonl` 上传至向量数据库
2. 配置 RAG 检索流程（召回 → rerank → 组装）
3. （可选）使用 `question_chunks.jsonl` 构建更细粒度的 chunk 索引
4. （可选）使用 `questions_full.json` 构建知识图谱（Neo4j）

---
生成时间：`date +%Y-%m-%d\ %H:%M:%S`
数据库：`<项目根目录>/database/db/tax_knowledge.db`
