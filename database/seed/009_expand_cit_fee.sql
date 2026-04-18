-- ============================================================
-- 009_expand_cit_fee.sql
-- CIT(+12净新增15条) + FEE(+10净新增10条) 扩容
-- 包含: question_policy_link(52条) + question_relation(24条)
-- 状态: CIT=37条, FEE=36条
-- ============================================================

-- 政策引用 (52条)
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (430, 85, 'citation', '', 0);  -- OPR-CIT-012 → SAT-TAX-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (430, 98, 'citation', '', 0);  -- OPR-CIT-012 → TAX-POL-006
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (430, 5, 'citation', '', 0);   -- OPR-CIT-012 → GOV-CIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (431, 40, 'citation', '', 0);  -- OPR-CIT-013 → POL-PREF-006
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (431, 39, 'citation', '', 0);  -- OPR-CIT-013 → POL-PREF-005
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (432, 39, 'citation', '', 0);  -- OPR-CIT-014 → POL-PREF-005
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (433, 5, 'citation', '', 0);   -- OPR-CIT-015 → GOV-CIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (433, 92, 'citation', '', 0);  -- OPR-CIT-015 → TAX-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (434, 92, 'citation', '', 0);  -- OPR-CIT-016 → TAX-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (434, 5, 'citation', '', 0);   -- OPR-CIT-016 → GOV-CIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (435, 5, 'citation', '', 0);   -- OPR-CIT-017 → GOV-CIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (435, 95, 'citation', '', 0);  -- OPR-CIT-017 → SAT-TAX-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (436, 21, 'citation', '', 0);  -- OPR-CIT-018 → POL-CIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (436, 79, 'citation', '', 0);  -- OPR-CIT-018 → SAT-FEE-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (437, 98, 'citation', '', 0);  -- OPR-CIT-019 → TAX-POL-006
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (437, 57, 'citation', '', 0);  -- OPR-CIT-019 → POL-WHT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (437, 59, 'citation', '', 0);  -- OPR-CIT-019 → POL-WHT-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (438, 21, 'citation', '', 0);  -- OPR-CIT-020 → POL-CIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (439, 21, 'citation', '', 0);  -- OPR-CIT-021 → POL-CIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (439, 5, 'citation', '', 0);   -- OPR-CIT-021 → GOV-CIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (440, 5, 'citation', '', 0);   -- OPR-CIT-022 → GOV-CIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (440, 6, 'citation', '', 0);   -- OPR-CIT-022 → GOV-CIT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (441, 58, 'citation', '', 0);  -- OPR-CIT-023 → POL-WHT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (441, 63, 'citation', '', 0);  -- OPR-CIT-023 → IIT-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (442, 92, 'citation', '', 0);  -- RSK-CIT-005 → TAX-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (442, 9, 'citation', '', 0);   -- RSK-CIT-005 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (443, 92, 'citation', '', 0);  -- RSK-CIT-006 → TAX-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (443, 9, 'citation', '', 0);   -- RSK-CIT-006 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (444, 5, 'citation', '', 0);   -- SET-CIT-003 → GOV-CIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (445, 48, 'citation', '', 0);  -- OPR-FEE-014 → POL-VAT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (445, 83, 'citation', '', 0);  -- OPR-FEE-014 → SAT-VAT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (446, 50, 'citation', '', 0);  -- OPR-FEE-015 → POL-VAT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (446, 4, 'citation', '', 0);   -- OPR-FEE-015 → GOV-VAT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (447, 48, 'citation', '', 0);  -- OPR-FEE-016 → POL-VAT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (447, 21, 'citation', '', 0);  -- OPR-FEE-016 → POL-CIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (448, 48, 'citation', '', 0);  -- OPR-FEE-017 → POL-VAT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (448, 21, 'citation', '', 0);  -- OPR-FEE-017 → POL-CIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (449, 53, 'citation', '', 0);  -- OPR-FEE-018 → POL-VAT-004
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (449, 5, 'citation', '', 0);   -- OPR-FEE-018 → GOV-VAT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (450, 44, 'citation', '', 0);  -- OPR-FEE-019 → POL-RISK-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (450, 88, 'citation', '', 0);  -- OPR-FEE-019 → SAT-VAT-006
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (451, 50, 'citation', '', 0);  -- OPR-FEE-020 → POL-VAT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (451, 4, 'citation', '', 0);   -- OPR-FEE-020 → GOV-VAT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (452, 92, 'citation', '', 0);  -- RSK-FEE-004 → TAX-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (452, 93, 'citation', '', 0);  -- RSK-FEE-004 → TAX-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (452, 27, 'citation', '', 0);  -- RSK-FEE-004 → POL-INV-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (453, 48, 'citation', '', 0);  -- RSK-FEE-005 → POL-VAT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (453, 84, 'citation', '', 0);  -- RSK-FEE-005 → SAT-VAT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (453, 44, 'citation', '', 0);  -- RSK-FEE-005 → POL-RISK-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (454, 9, 'citation', '', 0);   -- SET-FEE-005 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (454, 4, 'citation', '', 0);   -- SET-FEE-005 → GOV-VAT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (454, 87, 'citation', '', 0);  -- SET-FEE-005 → SAT-VAT-004

-- 关联关系 (24条)
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (430, 442, 'related', 0);   -- OPR-CIT-012 → RSK-CIT-005
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (430, 437, 'cross', 0);    -- OPR-CIT-012 → OPR-CIT-019
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (431, 432, 'cross', 0);    -- OPR-CIT-013 → OPR-CIT-014
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (433, 407, 'cross', 0);    -- OPR-CIT-015 → OPR-CIT-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (434, 442, 'cross', 0);  -- OPR-CIT-016 → RSK-CIT-005
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (435, 404, 'cross', 0);  -- OPR-CIT-017 → CLS-CIT-002
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (436, 411, 'cross', 0);  -- OPR-CIT-018 → OPR-CIT-009
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (440, 410, 'cross', 0);   -- OPR-CIT-022 → OPR-CIT-008
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (441, 407, 'cross', 0);  -- OPR-CIT-023 → OPR-CIT-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (442, 443, 'cross', 0);   -- RSK-CIT-005 → RSK-CIT-006
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (442, 452, 'cross', 0);  -- RSK-CIT-005 → RSK-FEE-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (444, 419, 'cross', 0);  -- SET-CIT-003 → SET-CIT-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (444, 440, 'cross', 0);  -- SET-CIT-003 → OPR-CIT-022
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (445, 448, 'cross', 0);  -- OPR-FEE-014 → OPR-FEE-017
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (446, 447, 'cross', 0);  -- OPR-FEE-015 → OPR-FEE-016
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (450, 452, 'cross', 0);  -- OPR-FEE-019 → RSK-FEE-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (450, 453, 'cross', 0);  -- OPR-FEE-019 → RSK-FEE-005
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (451, 446, 'cross', 0);  -- OPR-FEE-020 → OPR-FEE-015
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (452, 453, 'cross', 0);  -- RSK-FEE-004 → RSK-FEE-005
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (452, 414, 'cross', 0);  -- RSK-FEE-004 → OPR-FEE-007
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (452, 443, 'cross', 0);  -- RSK-FEE-004 → RSK-CIT-006
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (454, 418, 'cross', 0);  -- SET-FEE-005 → SET-FEE-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (454, 421, 'cross', 0);  -- SET-FEE-005 → SET-FEE-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (454, 412, 'cross', 0);  -- SET-FEE-005 → OPR-FEE-001
