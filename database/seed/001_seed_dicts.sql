-- ============================================================
-- 文件：001_seed_dicts.sql
-- 描述：初始化字典数据（生命周期阶段、主题模块、问题类型、状态等）
-- 执行顺序：第4步（在表创建后执行）
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
('certain_conditional', '条件判断', 'answer_certainty', 2),
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

-- -------------------- 业务标签 --------------------
INSERT INTO tag_dict (tag_code, tag_name, tag_category, parent_id, display_order) VALUES
('tag_registration', '登记设立', 'business', NULL, 1),
('tag_zero_report', '零申报', 'business', NULL, 2),
('tag_invoice', '发票管理', 'business', NULL, 3),
('tag_change', '变更登记', 'business', NULL, 4),
('tag_risk', '风险警示', 'business', NULL, 5);
