-- ============================================================
-- 文件：002_create_relation_tables.sql
-- 描述：创建关联表（问题-政策、问题-标签、更新记录、关联问题、地方口径）
-- 执行顺序：第2步
-- ============================================================

-- -------------------- 4. 问题-政策关联表 --------------------
CREATE TABLE IF NOT EXISTS question_policy_link (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id     INTEGER NOT NULL,
    policy_id       INTEGER NOT NULL,
    support_type    TEXT NOT NULL,
    support_note    TEXT,
    display_order   INTEGER NOT NULL DEFAULT 1,

    FOREIGN KEY (question_id) REFERENCES question_master(id) ON DELETE CASCADE,
    FOREIGN KEY (policy_id)   REFERENCES policy_basis(id)    ON DELETE CASCADE
);

-- -------------------- 5. 问题-标签关联表 --------------------
CREATE TABLE IF NOT EXISTS question_tag_link (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id     INTEGER NOT NULL,
    tag_id          INTEGER NOT NULL,
    is_primary      INTEGER NOT NULL DEFAULT 0,
    display_order   INTEGER NOT NULL DEFAULT 1,

    FOREIGN KEY (question_id) REFERENCES question_master(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id)      REFERENCES tag_dict(id)       ON DELETE CASCADE
);

-- -------------------- 6. 问题更新记录表 --------------------
CREATE TABLE IF NOT EXISTS question_update_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id     INTEGER NOT NULL,
    version_no      INTEGER NOT NULL,
    update_date     TEXT NOT NULL DEFAULT (datetime('now')),
    update_type     TEXT NOT NULL,
    update_reason   TEXT,
    updated_by      TEXT,
    reviewed_by     TEXT,
    change_summary  TEXT,

    FOREIGN KEY (question_id) REFERENCES question_master(id) ON DELETE CASCADE
);

-- -------------------- 7. 关联问题表 --------------------
CREATE TABLE IF NOT EXISTS question_relation (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id     INTEGER NOT NULL,
    related_id      INTEGER NOT NULL,
    relation_type   TEXT NOT NULL,
    display_order   INTEGER NOT NULL DEFAULT 1,

    FOREIGN KEY (question_id) REFERENCES question_master(id) ON DELETE CASCADE,
    FOREIGN KEY (related_id)  REFERENCES question_master(id) ON DELETE CASCADE
);

-- -------------------- 8. 地方口径表 --------------------
CREATE TABLE IF NOT EXISTS local_rule_note (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id     INTEGER NOT NULL,
    region_code     TEXT NOT NULL,
    region_name     TEXT NOT NULL,
    local_content   TEXT NOT NULL,
    authority_name  TEXT,
    effective_date  TEXT,
    expiry_date     TEXT,
    source_url      TEXT,
    remarks         TEXT,

    FOREIGN KEY (question_id) REFERENCES question_master(id) ON DELETE CASCADE
);
