# 企业全生命周期税务问题知识库

## 项目概述

本项目用于建设一个"企业全生命周期税务问题知识库"，特点是以"实际问题—答案"的形式组织内容，而非按文件罗列。

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

## 文件说明

- `schema_tax_knowledge_base.sql` - 完整建表语句 + 字典数据 + 示例数据

## 使用方式

```bash
# 在 SQLite 中执行
sqlite3 tax_knowledge.db < schema_tax_knowledge_base.sql

# 或进入 SQLite 交互界面
sqlite3 tax_knowledge.db
.read schema_tax_knowledge_base.sql
```

## 设计原则

1. **问题卡片为核心** - 一个问题就是一个独立知识单元
2. **内容与依据分离** - 问题内容不与政策依据混在一起
3. **结构稳定可扩展** - 新增问题通过新增记录实现，不破坏整体结构
4. **便于后续扩展** - 支持网站展示、AI检索、向量化的结构化清洗

## 创建时间

2026-04-15
