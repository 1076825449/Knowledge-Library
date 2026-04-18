-- fix_scope_local_policy_links.sql
-- 为10条新增的scope_local问题添加政策链接
-- 每条至少1条政策链接，确保详情页显示"政策依据"区域

BEGIN;

-- OPR-REG-024: 跨区域涉税事项报告
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order)
SELECT q.id, p.id, 'citation', '《税务登记管理办法》及跨区域涉税事项报告规定', 1
FROM question_master q, policy_basis p
WHERE q.question_code = 'OPR-REG-024' AND p.policy_code = 'GOV-Tax-001';

-- RSK-RISK-032: 非正常户解除
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order)
SELECT q.id, p.id, 'citation', '《税务登记管理办法》：非正常户解除须补申报、缴清欠税及滞纳金', 1
FROM question_master q, policy_basis p
WHERE q.question_code = 'RSK-RISK-032' AND p.policy_code = 'GOV-Tax-001';

-- OPR-PREF-022: 北部湾经济区优惠
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order)
SELECT q.id, p.id, 'citation', '《西部地区鼓励类产业目录》及广西北部湾经济区专项政策', 1
FROM question_master q, policy_basis p
WHERE q.question_code = 'OPR-PREF-022' AND p.policy_code = 'POL-PREF-006';

-- SET-REG-016: 新办纳税人套餐
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order)
SELECT q.id, p.id, 'citation', '《纳税服务工作规范》：新办纳税人套餐一次性办理税务报告', 1
FROM question_master q, policy_basis p
WHERE q.question_code = 'SET-REG-016' AND p.policy_code = 'GOV-Tax-001';

-- OPR-VAT-019: 区块链电子发票
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order)
SELECT q.id, p.id, 'citation', '《关于推行区块链电子发票的通知》及增值税电子发票相关规定', 1
FROM question_master q, policy_basis p
WHERE q.question_code = 'OPR-VAT-019' AND p.policy_code = 'POL-VAT-001';

-- SUS-CLEAR-005: 税务注销清税
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order)
SELECT q.id, p.id, 'citation', '《税务注销管理办法》：清税须结清税款、缴销发票、完成汇算清缴', 1
FROM question_master q, policy_basis p
WHERE q.question_code = 'SUS-CLEAR-005' AND p.policy_code = 'GOV-Tax-001';

-- OPR-TAX-023: 银税互动
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order)
SELECT q.id, p.id, 'citation', '《纳税信用评价管理办法》：银税互动机制，A/B/M级纳税人可享信用贷款', 1
FROM question_master q, policy_basis p
WHERE q.question_code = 'OPR-TAX-023' AND p.policy_code = 'GOV-Tax-001';

-- OPR-SSF-023: 社保费日常申报
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order)
SELECT q.id, p.id, 'citation', '《社会保险法》及社保费征缴相关规定', 1
FROM question_master q, policy_basis p
WHERE q.question_code = 'OPR-SSF-023' AND p.policy_code = 'POL-SSF-001';

-- OPR-IIT-030: 股息红利代扣代缴
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order)
SELECT q.id, p.id, 'citation', '《个人所得税法》及预提所得税源泉扣缴规定', 1
FROM question_master q, policy_basis p
WHERE q.question_code = 'OPR-IIT-030' AND p.policy_code = 'GOV-Tax-001';

-- OPR-INV-029: 农产品收购发票
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order)
SELECT q.id, p.id, 'citation', '《增值税暂行条例》及农产品收购发票进项税额抵扣规定', 1
FROM question_master q, policy_basis p
WHERE q.question_code = 'OPR-INV-029' AND p.policy_code = 'POL-VAT-001';

COMMIT;
