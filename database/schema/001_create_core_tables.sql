-- ============================================================
-- 文件：001_create_core_tables.sql
-- 描述：创建核心数据表（问题主表、政策依据表、标签字典表）
-- 执行顺序：第1步
-- ============================================================

-- -------------------- 1. 问题主表 --------------------
CREATE TABLE IF NOT EXISTS question_master (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    question_code   TEXT NOT NULL UNIQUE,
    question_title  TEXT NOT NULL,
    question_plain  TEXT NOT NULL,

    -- 分类
    stage_code      TEXT NOT NULL,
    module_code     TEXT NOT NULL,
    question_type   TEXT NOT NULL,

    -- 答案
    one_line_answer TEXT NOT NULL,
    detailed_answer TEXT,
    core_definition TEXT,

    -- 条件与边界
    applicable_conditions TEXT,
    exceptions_boundary   TEXT,

    -- 实务
    practical_steps TEXT,
    risk_warning    TEXT,

    -- 适用范围
    scope_level     TEXT NOT NULL DEFAULT 'scope_national',
    local_region    TEXT,

    -- 确定性
    answer_certainty TEXT NOT NULL DEFAULT 'certain_clear',

    -- 元数据
    keywords        TEXT,
    high_frequency_flag INTEGER NOT NULL DEFAULT 0,
    newbie_flag     INTEGER NOT NULL DEFAULT 0,

    -- 版本管理
    status          TEXT NOT NULL DEFAULT 'draft',
    version_no      INTEGER NOT NULL DEFAULT 1,

    -- 审计字段
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- -------------------- 2. 政策依据表 --------------------
CREATE TABLE IF NOT EXISTS policy_basis (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_code     TEXT NOT NULL UNIQUE,
    policy_name     TEXT NOT NULL,
    document_no     TEXT,
    article_ref     TEXT,

    -- 政策层级
    policy_level    TEXT NOT NULL,

    -- 有效期
    effective_date  TEXT,
    expiry_date     TEXT,
    current_status  TEXT NOT NULL DEFAULT 'effective',

    -- 内容摘要
    policy_summary  TEXT,
    raw_quote_short TEXT,

    -- 适用范围
    region_scope    TEXT DEFAULT 'national',

    -- 备注
    remarks         TEXT,

    -- 审计字段
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- -------------------- 3. 标签字典表 --------------------
CREATE TABLE IF NOT EXISTS tag_dict (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_code        TEXT NOT NULL UNIQUE,
    tag_name        TEXT NOT NULL,
    tag_category    TEXT,
    parent_id       INTEGER,
    display_order   INTEGER NOT NULL DEFAULT 1,
    status          TEXT NOT NULL DEFAULT 'active',

    FOREIGN KEY (parent_id) REFERENCES tag_dict(id) ON DELETE SET NULL
);
