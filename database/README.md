# database/ 目录说明

## 目录结构

```
database/
├── README.md           # 本文件
├── schema/             # 建表 SQL
│   ├── 001_create_core_tables.sql      # 核心表（问题主表、政策依据表、标签字典表）
│   ├── 002_create_relation_tables.sql  # 关联表（政策关联、标签关联、更新记录、关联问题、地方口径）
│   └── 003_create_indexes.sql          # 索引
├── seed/               # 初始化数据
│   ├── 001_seed_dicts.sql              # 字典数据（生命周期阶段、主题模块、问题类型等）
│   └── 002_seed_sample_data.sql        # 示例数据（问题、政策依据、关联数据）
├── migrations/         # 迁移脚本（后续扩展）
├── queries/            # 常用查询示例
│   └── README.md
└── db/                 # 数据库文件（SQLite）
    └── README.md
```

## 初始化顺序

执行以下 SQL 文件（按顺序）：

```bash
# 1. 创建核心表
sqlite3 tax_knowledge.db < schema/001_create_core_tables.sql

# 2. 创建关联表
sqlite3 tax_knowledge.db < schema/002_create_relation_tables.sql

# 3. 创建索引
sqlite3 tax_knowledge.db < schema/003_create_indexes.sql

# 4. 初始化字典数据
sqlite3 tax_knowledge.db < seed/001_seed_dicts.sql

# 5. 插入示例数据
sqlite3 tax_knowledge.db < seed/002_seed_sample_data.sql
```

## 或使用完整脚本

```bash
# 一次性执行所有 schema + seed
sqlite3 tax_knowledge.db < ../schema_tax_knowledge_base.sql
```

## 数据库文件

SQLite 数据库文件建议存放在 `database/db/` 目录，文件名如 `tax_knowledge.db`。

**注意：** `.gitignore` 已忽略 `*.db` 文件，如需提交空库模板，请使用 `.gitkeep` 占位。
