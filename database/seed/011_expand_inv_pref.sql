-- ============================================================
-- 011_expand_inv_pref.sql
-- INV(+15净新增) + PREF(+10净新增) 扩容
-- 包含: question_policy_link(49条) + question_relation(13条)
-- 状态: INV=44条, PREF=39条
-- ============================================================

-- 政策引用 (49条)

INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (478, 33, 'citation', '', 0);  -- OPR-INV-020 → POL-INV-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (478, 8, 'citation', '', 0);  -- OPR-INV-020 → SAT-VAT-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (479, 33, 'citation', '', 0);  -- OPR-INV-021 → POL-INV-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (480, 36, 'citation', '', 0);  -- OPR-INV-022 → POL-INV-004
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (480, 1, 'citation', '', 0);  -- OPR-INV-022 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (481, 33, 'citation', '', 0);  -- OPR-INV-023 → POL-INV-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (481, 5, 'citation', '', 0);  -- OPR-INV-023 → SAT-INV-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (482, 33, 'citation', '', 0);  -- OPR-INV-024 → POL-INV-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (482, 74, 'citation', '', 0);  -- OPR-INV-024 → SAT-VAT-006
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (483, 33, 'citation', '', 0);  -- OPR-INV-025 → POL-INV-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (483, 41, 'citation', '', 0);  -- OPR-INV-025 → POL-CIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (484, 91, 'citation', '', 0);  -- RSK-INV-001 → TAX-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (484, 33, 'citation', '', 0);  -- RSK-INV-001 → POL-INV-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (485, 47, 'citation', '', 0);  -- RSK-INV-002 → POL-RISK-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (485, 74, 'citation', '', 0);  -- RSK-INV-002 → SAT-VAT-006
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (486, 91, 'citation', '', 0);  -- RSK-INV-003 → TAX-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (486, 33, 'citation', '', 0);  -- RSK-INV-003 → POL-INV-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (487, 7, 'citation', '', 0);  -- SET-INV-004 → SAT-VAT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (487, 8, 'citation', '', 0);  -- SET-INV-004 → SAT-VAT-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (488, 7, 'citation', '', 0);  -- SET-INV-005 → SAT-VAT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (488, 1, 'citation', '', 0);  -- SET-INV-005 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (489, 18, 'citation', '', 0);  -- CLS-INV-004 → GOV-REG-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (489, 33, 'citation', '', 0);  -- CLS-INV-004 → POL-INV-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (490, 33, 'citation', '', 0);  -- CLS-INV-005 → POL-INV-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (490, 1, 'citation', '', 0);  -- CLS-INV-005 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (491, 48, 'citation', '', 0);  -- SUS-INV-003 → POL-SUS-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (491, 7, 'citation', '', 0);  -- SUS-INV-003 → SAT-VAT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (492, 48, 'citation', '', 0);  -- SUS-INV-004 → POL-SUS-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (492, 74, 'citation', '', 0);  -- SUS-INV-004 → SAT-VAT-006
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (493, 53, 'citation', '', 0);  -- CHG-PREF-007 → POL-PREF-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (493, 52, 'citation', '', 0);  -- CHG-PREF-007 → POL-PREF-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (494, 60, 'citation', '', 0);  -- OPR-PREF-013 → POL-PREF-010
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (494, 52, 'citation', '', 0);  -- OPR-PREF-013 → POL-PREF-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (495, 55, 'citation', '', 0);  -- OPR-PREF-014 → POL-PREF-005
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (495, 41, 'citation', '', 0);  -- OPR-PREF-014 → POL-CIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (496, 60, 'citation', '', 0);  -- OPR-PREF-015 → POL-PREF-010
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (496, 52, 'citation', '', 0);  -- OPR-PREF-015 → POL-PREF-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (497, 57, 'citation', '', 0);  -- OPR-PREF-016 → POL-PREF-007
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (497, 55, 'citation', '', 0);  -- OPR-PREF-016 → POL-PREF-005
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (498, 55, 'citation', '', 0);  -- RSK-PREF-003 → POL-PREF-005
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (498, 1, 'citation', '', 0);  -- RSK-PREF-003 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (499, 56, 'citation', '', 0);  -- RSK-PREF-004 → POL-PREF-006
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (499, 90, 'citation', '', 0);  -- RSK-PREF-004 → TAX-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (500, 58, 'citation', '', 0);  -- CLS-PREF-004 → POL-PREF-008
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (500, 26, 'citation', '', 0);  -- CLS-PREF-004 → GOV-VAT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (501, 52, 'citation', '', 0);  -- SUS-PREF-003 → POL-PREF-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (501, 53, 'citation', '', 0);  -- SUS-PREF-003 → POL-PREF-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (502, 52, 'citation', '', 0);  -- SET-PREF-005 → POL-PREF-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (502, 53, 'citation', '', 0);  -- SET-PREF-005 → POL-PREF-003

-- 关联关系 (13条)

INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (480, 486, 'cross', 0);  -- OPR-INV-022 → RSK-INV-003
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (482, 485, 'cross', 0);  -- OPR-INV-024 → RSK-INV-002
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (484, 486, 'cross', 0);  -- RSK-INV-001 → RSK-INV-003
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (495, 498, 'cross', 0);  -- OPR-PREF-014 → RSK-PREF-003
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (498, 499, 'cross', 0);  -- RSK-PREF-003 → RSK-PREF-004