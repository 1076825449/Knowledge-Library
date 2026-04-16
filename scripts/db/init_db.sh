#!/bin/bash
# ============================================================
# 文件：scripts/db/init_db.sh
# 用途：从零初始化税务知识库数据库
# 用法：bash scripts/db/init_db.sh
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
DB_DIR="$ROOT_DIR/database/db"
DB_FILE="$DB_DIR/tax_knowledge.db"

echo "==> 初始化数据库: $DB_FILE"

# 如果数据库已存在，先备份
if [ -f "$DB_FILE" ]; then
    BACKUP_FILE="$DB_FILE.backup_$(date +%Y%m%d_%H%M%S)"
    echo "==> 发现已有数据库，备份至: $BACKUP_FILE"
    cp "$DB_FILE" "$BACKUP_FILE"
    rm "$DB_FILE"
fi

# 执行建表
echo "==> 第1步：创建核心表..."
sqlite3 "$DB_FILE" < "$ROOT_DIR/database/schema/001_create_core_tables.sql"

echo "==> 第2步：创建关联表..."
sqlite3 "$DB_FILE" < "$ROOT_DIR/database/schema/002_create_relation_tables.sql"

echo "==> 第3步：创建索引..."
sqlite3 "$DB_FILE" < "$ROOT_DIR/database/schema/003_create_indexes.sql"

echo "==> 第4步：初始化字典数据..."
sqlite3 "$DB_FILE" < "$ROOT_DIR/database/seed/001_seed_dicts.sql"

echo "==> 第5步：插入示例数据..."
sqlite3 "$DB_FILE" < "$ROOT_DIR/database/seed/002_seed_sample_data.sql"

echo "==> 第6步：插入扩展问题内容（SET/OPR/CLS阶段）..."
sqlite3 "$DB_FILE" < "$ROOT_DIR/database/seed/003_seed_expand_content.sql"

echo "==> 第7步：插入标签关联与问题关系..."
sqlite3 "$DB_FILE" < "$ROOT_DIR/database/seed/003b_seed_tags_and_relations.sql"

# 验证
echo ""
echo "==> 验证数据..."
QUESTION_COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM question_master;")
POLICY_COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM policy_basis;")
TAG_COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM tag_dict;")
LINK_COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM question_policy_link;")
echo "    问题:   $QUESTION_COUNT 条"
echo "    政策:   $POLICY_COUNT 条"
echo "    字典:   $TAG_COUNT 条"
echo "    关联:   $LINK_COUNT 条"

echo ""
echo "==> 数据库初始化完成！"
