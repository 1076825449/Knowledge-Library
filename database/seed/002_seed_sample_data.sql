-- ============================================================
-- 文件：002_seed_sample_data.sql
-- 描述：示例问题、政策依据、关联数据
-- 执行顺序：第5步（在字典数据插入后执行）
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

-- -------------------- 问题-标签关联表示例 --------------------
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
