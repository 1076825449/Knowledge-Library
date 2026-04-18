-- add_type_why_policy_links.sql
-- 为 7 条 type_why 问题补充政策依据
-- 运行前已验证：7条问题均无任何 policy_link

BEGIN;

-- REG-OPR-003: 企业为什么要按税务部门要求设置账簿凭证？
-- 依据：征管法（账簿设置义务）+ 税务登记管理办法
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES
(561, 1,  'support_direct', '《税收征收管理法》第十九条：纳税人、扣缴义务人按照有关法律、行政法规和国务院财政、税务主管部门的规定设置账簿', 1),
(561, 18, 'support_direct', '《税务登记管理办法》对账簿设置的具体要求', 2);

-- VAT-OPR-003: 增值税为什么要实行抵扣链机制？
-- 依据：增值税暂行条例及实施细则
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES
(562, 40, 'support_direct', '《增值税暂行条例》第八条：纳税人购进货物或者接受应税劳务支付的增值税额，为进项税额', 1),
(562, 4,  'support_definition', '《增值税暂行条例实施细则》对抵扣机制的细化规定', 2);

-- PREF-OPR-003: 小微企业为什么要主动申请税收优惠？
-- 依据：小微企业所得税优惠、增值税优惠
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES
(563, 51, 'support_direct', '《关于实施小微企业普惠性税收减免政策的通知》：符合条件的应主动申报', 1),
(563, 53, 'support_direct', '《关于小微企业和个体工商户所得税优惠政策的公告》：优惠需经纳税评估后适用', 2);

-- SSF-OPR-003: 社保费为什么要和工资一起申报？
-- 依据：社会保险费征缴暂行条例
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES
(564, 39, 'support_direct', '《社会保险费征缴暂行条例》：缴费单位应当按时足额缴纳社会保险费，与工资薪金同步申报', 1);

-- DEC-OPR-003: 企业为什么要按月或按季申报？
-- 依据：税收征收管理法
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES
(565, 1,  'support_direct', '《税收征收管理法》第二十五条：纳税人必须依照规定申报纳税期限办理纳税申报', 1),
(565, 2,  'support_procedure', '《税务登记管理办法》纳税申报期限的具体规定', 2);

-- CLEAR-OPR-003: 企业注销时为什么要进行清算所得税处理？
-- 依据：企业所得税法清算条款 + 企业清算所得税处理通知
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES
(566, 24, 'support_direct', '《关于企业清算业务企业所得税处理若干问题的通知》：注销前应进行清算所得税处理', 1),
(566, 22, 'support_procedure', '《公司注销登记管理办法》与税务注销的程序衔接', 2);

-- TAX-OPR-005: 企业为什么要进行纳税信用评价？
-- 依据：税收征收管理法 + 重大税收违法失信主体信息公布管理办法
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES
(567, 1,  'support_definition', '《税收征收管理法》建立纳税信用管理制度的法律基础', 1),
(567, 12, 'support_direct', '《重大税收违法失信主体信息公布管理办法》：信用等级影响企业信用评价和联合惩戒范围', 2);

COMMIT;
