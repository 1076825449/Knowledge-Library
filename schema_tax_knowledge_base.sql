-- ============================================================
-- 企业全生命周期税务问题知识库 - 数据库 Schema
-- 目标：中小型知识库，稳定、清晰、可维护、可扩展
-- 创建时间：2026-04-15
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
    scope_level     TEXT NOT NULL DEFAULT 'national',
    local_region    TEXT,

    -- 确定性
    answer_certainty TEXT NOT NULL DEFAULT 'clear',

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

-- 索引：常用查询字段
CREATE INDEX IF NOT EXISTS idx_qm_stage_code    ON question_master(stage_code);
CREATE INDEX IF NOT EXISTS idx_qm_module_code   ON question_master(module_code);
CREATE INDEX IF NOT EXISTS idx_qm_question_type ON question_master(question_type);
CREATE INDEX IF NOT EXISTS idx_qm_status        ON question_master(status);
CREATE INDEX IF NOT EXISTS idx_qm_scope_level   ON question_master(scope_level);
CREATE INDEX IF NOT EXISTS idx_qm_high_freq      ON question_master(high_frequency_flag);
CREATE INDEX IF NOT EXISTS idx_qm_newbie         ON question_master(newbie_flag);
CREATE INDEX IF NOT EXISTS idx_qm_updated_at    ON question_master(updated_at);

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

-- 索引
CREATE INDEX IF NOT EXISTS idx_pb_policy_level   ON policy_basis(policy_level);
CREATE INDEX IF NOT EXISTS idx_pb_current_status ON policy_basis(current_status);
CREATE INDEX IF NOT EXISTS idx_pb_region_scope   ON policy_basis(region_scope);
CREATE INDEX IF NOT EXISTS idx_pb_policy_code    ON policy_basis(policy_code);

-- -------------------- 3. 问题-政策关联表 --------------------
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

-- 索引：唯一约束防止重复关联
CREATE UNIQUE INDEX IF NOT EXISTS idx_qpl_unique     ON question_policy_link(question_id, policy_id, support_type);
CREATE INDEX IF NOT EXISTS idx_qpl_question_id      ON question_policy_link(question_id);
CREATE INDEX IF NOT EXISTS idx_qpl_policy_id        ON question_policy_link(policy_id);

-- -------------------- 4. 标签字典表 --------------------
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

-- 索引
CREATE INDEX IF NOT EXISTS idx_td_tag_category ON tag_dict(tag_category);
CREATE INDEX IF NOT EXISTS idx_td_parent_id     ON tag_dict(parent_id);

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

-- 唯一约束防止重复关联
CREATE UNIQUE INDEX IF NOT EXISTS idx_qtl_unique ON question_tag_link(question_id, tag_id);
CREATE INDEX IF NOT EXISTS idx_qtl_question_id   ON question_tag_link(question_id);
CREATE INDEX IF NOT EXISTS idx_qtl_tag_id        ON question_tag_link(tag_id);

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

-- 索引
CREATE INDEX IF NOT EXISTS idx_qul_question_id ON question_update_log(question_id);
CREATE INDEX IF NOT EXISTS idx_qul_update_date ON question_update_log(update_date);

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

-- 唯一约束防止重复关联
CREATE UNIQUE INDEX IF NOT EXISTS idx_qr_unique ON question_relation(question_id, related_id, relation_type);
CREATE INDEX IF NOT EXISTS idx_qr_question_id   ON question_relation(question_id);
CREATE INDEX IF NOT EXISTS idx_qr_related_id    ON question_relation(related_id);

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

-- 索引
CREATE INDEX IF NOT EXISTS idx_lrn_question_id ON local_rule_note(question_id);
CREATE INDEX IF NOT EXISTS idx_lrn_region_code ON local_rule_note(region_code);

-- ============================================================
-- 字典数据初始化
-- ============================================================

-- -------------------- 生命周期阶段 --------------------
INSERT INTO tag_dict (tag_code, tag_name, tag_category, display_order) VALUES
('SET', '设立期', 'stage', 1),
('OPR', '开业/日常经营期', 'stage', 2),
('CHG', '变更期', 'stage', 3),
('RSK', '风险异常期', 'stage', 4),
('SUS', '停业期', 'stage', 5),
('CLS', '注销期', 'stage', 6);

-- -------------------- 主题模块 --------------------
INSERT INTO tag_dict (tag_code, tag_name, tag_category, display_order) VALUES
('REG', '登记管理', 'module', 1),
('DEC', '申报纳税', 'module', 2),
('INV', '发票管理', 'module', 3),
('VAT', '增值税', 'module', 4),
('CIT', '企业所得税', 'module', 5),
('IIT', '个人所得税', 'module', 6),
('SSF', '社保费', 'module', 7),
('FEE', '成本费用', 'module', 8),
('PREF', '优惠政策', 'module', 9),
('RISK', '风险应对', 'module', 10),
('CLEAR', '清税注销', 'module', 11),
('ETAX', '电子税务局/系统办理', 'module', 12);

-- -------------------- 问题类型 --------------------
INSERT INTO tag_dict (tag_code, tag_name, tag_category, display_order) VALUES
('type_whether', '是否类', 'question_type', 1),
('type_how', '怎么办类', 'question_type', 2),
('type_define', '定义类', 'question_type', 3),
('type_risk', '风险类', 'question_type', 4),
('type_time', '时限类', 'question_type', 5);

-- -------------------- 答案确定性 --------------------
INSERT INTO tag_dict (tag_code, tag_name, tag_category, display_order) VALUES
('certain_clear', '明确', 'answer_certainty', 1),
('certain_condition', '条件判断', 'answer_certainty', 2),
('certain_dispute', '存在争议', 'answer_certainty', 3),
('certain_practice', '以实务口径为准', 'answer_certainty', 4);

-- -------------------- 记录状态 --------------------
INSERT INTO tag_dict (tag_code, tag_name, tag_category, display_order) VALUES
('status_draft', '草稿', 'status', 1),
('status_pending', '待复核', 'status', 2),
('status_active', '启用', 'status', 3),
('status_obsolete', '过时', 'status', 4),
('status_archived', '归档', 'status', 5);

-- -------------------- 政策层级 --------------------
INSERT INTO tag_dict (tag_code, tag_name, tag_category, display_order) VALUES
('level_law', '法律', 'policy_level', 1),
('level_admin', '行政法规', 'policy_level', 2),
('level_department', '部门规章', 'policy_level', 3),
('level_bulletin', '公告', 'policy_level', 4),
('level_notice', '通知', 'policy_level', 5),
('level_local', '地方规范', 'policy_level', 6),
('level_reply', '复函/批复', 'policy_level', 7);

-- -------------------- 政策效力状态 --------------------
INSERT INTO tag_dict (tag_code, tag_name, tag_category, display_order) VALUES
('pol_effective', '有效', 'policy_status', 1),
('pol_partial', '部分有效', 'policy_status', 2),
('pol_expired', '已废止', 'policy_status', 3),
('pol_replaced', '被替代', 'policy_status', 4),
('pol_uncertain', '不确定', 'policy_status', 5);

-- -------------------- 支撑类型 --------------------
INSERT INTO tag_dict (tag_code, tag_name, tag_category, display_order) VALUES
('support_direct', '直接依据', 'support_type', 1),
('support_aux', '辅助依据', 'support_type', 2),
('support_definition', '定义依据', 'support_type', 3),
('support_procedure', '办理依据', 'support_type', 4),
('support_risk', '风险依据', 'support_type', 5),
('support_local', '地方执行依据', 'support_type', 6);

-- -------------------- 更新类型 --------------------
INSERT INTO tag_dict (tag_code, tag_name, tag_category, display_order) VALUES
('update_new', '新增', 'update_type', 1),
('update_revise', '修订', 'update_type', 2),
('update_policy', '政策更新', 'update_type', 3),
('update_boundary', '补充边界', 'update_type', 4),
('update_local', '增加地方口径', 'update_type', 5),
('update_status', '状态调整', 'update_type', 6);

-- -------------------- 适用范围层级 --------------------
INSERT INTO tag_dict (tag_code, tag_name, tag_category, display_order) VALUES
('scope_national', '全国', 'scope_level', 1),
('scope_local', '地方', 'scope_level', 2),
('scope_mixed', '混合', 'scope_level', 3);

-- ============================================================
-- 示例数据
-- ============================================================

-- -------------------- 问题主表示例 --------------------
INSERT INTO question_master (
    question_code, question_title, question_plain, stage_code, module_code, question_type,
    one_line_answer, detailed_answer, core_definition, applicable_conditions, exceptions_boundary,
    practical_steps, risk_warning, scope_level, local_region, answer_certainty,
    keywords, high_frequency_flag, newbie_flag, status, version_no
) VALUES
(
    'SET-REG-001',
    '企业没有收入，是否必须申报纳税？',
    '公司刚成立还没有收入，这个月要不要申报纳税？不申报有什么后果？',
    'SET', 'DEC', 'type_whether',
    '没有收入也要申报，属于"零申报"，长期零申报有风险',
    '企业在税务系统完成登记后，无论是否有收入，都需要按期进行纳税申报。即使当期没有应税收入，也需要办理零申报。零申报是指在纳税申报所属期内没有发生应税收入或应税行为，销售额（或营业额）为零。',
    '零申报是指在法定申报期限内，企业没有应税收入或应税行为，税务机关接受纳税人申报数据为零的申报方式。',
    '适用于所有完成税务登记的企业，无论是否领取发票、是否有业务发生。',
    '享受减免税优惠政策的企业，减免税期间也需正常申报。部分小规模纳税人季度30万免增值税政策下，符合条件可零申报但需备案。',
    '1. 登录电子税务局；2. 选择"增值税及附加税费申报"；3. 在销售额栏次填写"0"；4. 检查减免税栏次；5. 确认提交',
    '长期零申报（连续6个月以上）可能被税务机关纳入重点监控，存在偷税漏税风险；零申报不等于不用记账；连续三个月零申报可能触发税务检查。',
    'national', NULL, 'certain_clear',
    '零申报,无收入,纳税申报,设立登记,小规模纳税人', 1, 1, 'active', 1
),
(
    'OPR-CHG-001',
    '企业变更地址后，税务上还需要做什么？',
    '公司要搬家换办公地址，税务登记需要变更吗？之前的发票还能用吗？',
    'OPR', 'REG', 'type_how',
    '地址变更后15日内需到税务机关办理变更登记，发票需重新申领',
    '企业实际经营地址发生变化时，应当向主管税务机关申请办理变更税务登记。根据变更内容不同，可能涉及发票缴销重领、税费种认定调整、跨区迁移等手续。',
    '变更税务登记是指纳税人在税务登记内容发生变化时，向原税务登记机关申报办理变更登记的行为。',
    '适用于所有已办理税务登记的企业，税务登记内容发生变化时。',
    '跨区迁移（离开原主管税务机关管辖区）需要办理注销迁出流程；变更后的地址如果涉及主管税务机关变化，流程更复杂。',
    '1. 在电子税务局提交"变更税务登记"申请；2. 准备新地址证明材料；3. 缴销原发票；4. 重新领购发票（如需）；5. 确认税费种认定信息；6. 如跨区需办理迁出迁入手续',
    '未按规定办理变更登记可能面临罚款；跨区迁移可能影响企业纳税信用评级；变更期间如需开票需提前规划。',
    'national', NULL, 'certain_clear',
    '地址变更,经营地址,变更登记,发票管理,跨区迁移', 1, 0, 'active', 1
);

-- -------------------- 政策依据表示例 --------------------
INSERT INTO policy_basis (
    policy_code, policy_name, document_no, article_ref, policy_level,
    effective_date, current_status, policy_summary, raw_quote_short, region_scope
) VALUES
(
    'GOV-Tax-001',
    '中华人民共和国税收征收管理法',
    '主席令第49号',
    '第十六条',
    'level_law',
    '2001-05-01', 'pol_effective',
    '规定了税务登记、纳税申报、税款征收等基本征纳制度',
    '从事生产、经营的纳税人，税务登记内容发生变化的，应当自向工商行政管理机关或者其他机关办理变更登记之日起三十日内，持有关证件向税务机关申报办理变更税务登记。',
    'national'
),
(
    'GOV-Tax-002',
    '税务登记管理办法',
    '国家税务总局令第7号',
    '第十七条',
    'level_department',
    '2004-02-01', 'pol_effective',
    '细化了税务登记的具体办理流程和材料要求',
    '纳税人税务登记内容发生变化，应当自发生变化之日起30日内，向主管税务机关申报办理变更税务登记。',
    'national'
),
(
    'SAT-2024-033',
    '关于优化税务登记管理有关问题的公告',
    '国家税务总局公告2024年第33号',
    '第一条、第二条',
    'level_bulletin',
    '2024-06-01', 'pol_effective',
    '进一步简化变更登记流程，推进智能化办理',
    '纳税人申请变更税务登记，可通过电子税务局全程网上办理，无需上门报送纸质材料。变更内容涉及发票管理的，系统自动触发发票缴销流程。',
    'national'
);

-- -------------------- 问题-政策关联表示例 --------------------
INSERT INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES
(1, 1, 'support_direct', '明确了纳税人申报义务的基本要求', 1),
(1, 2, 'support_procedure', '规定了变更登记的具体时限和流程', 2),
(2, 1, 'support_direct', '规定了变更登记的基本时限要求', 1),
(2, 2, 'support_procedure', '细化变更登记办理流程', 2),
(2, 3, 'support_direct', '明确优化后的办理方式', 3);

-- -------------------- 标签及其关联数据 --------------------
INSERT INTO tag_dict (tag_code, tag_name, tag_category, parent_id, display_order) VALUES
('tag_registration', '登记设立', 'business', NULL, 1),
('tag_zero_report', '零申报', 'business', NULL, 2),
('tag_invoice', '发票管理', 'business', NULL, 3),
('tag_change', '变更登记', 'business', NULL, 4),
('tag_risk', '风险警示', 'business', NULL, 5);

INSERT INTO question_tag_link (question_id, tag_id, is_primary, display_order) VALUES
(1, 1, 1, 1),
(1, 2, 1, 2),
(1, 5, 0, 3),
(2, 1, 1, 1),
(2, 3, 1, 2),
(2, 4, 0, 3);

-- -------------------- 更新记录示例 --------------------
INSERT INTO question_update_log (question_id, version_no, update_type, update_reason, updated_by, reviewed_by, change_summary) VALUES
(1, 1, 'update_new', '新增问题', '系统管理员', '税务专家', '初始创建问题卡片，涵盖零申报基本要求和风险提示');

INSERT INTO question_update_log (question_id, version_no, update_type, update_reason, updated_by, reviewed_by, change_summary) VALUES
(2, 1, 'update_new', '新增问题', '系统管理员', '税务专家', '初始创建问题卡片，涵盖地址变更的完整流程和风险点');

-- -------------------- 关联问题示例 --------------------
INSERT INTO question_relation (question_id, related_id, relation_type, display_order) VALUES
(1, 2, 'related', 1);

-- -------------------- 地方口径表示例 --------------------
INSERT INTO local_rule_note (
    question_id, region_code, region_name, local_content, authority_name, effective_date, source_url
) VALUES
(1, 'SH', '上海市', '上海市小规模纳税人季度销售额未超过30万元的，可享受免税政策，但需正常申报。', '国家税务总局上海市税务局', '2023-01-01', 'https://shanghai.tax.gov.cn');
