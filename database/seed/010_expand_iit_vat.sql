-- ============================================================
-- 010_expand_iit_vat.sql
-- IIT(+15净新增) + VAT(+10净新增) 扩容
-- 包含: question_policy_link(49条) + question_relation(20条)
-- 状态: IIT=38条, VAT=38条
-- ============================================================

-- 政策引用 (49条)
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (455, 62, 'citation', '', 0);  -- CHG-IIT-001 → IIT-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (455, 63, 'citation', '', 0);  -- CHG-IIT-001 → IIT-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (456, 63, 'citation', '', 0);  -- OPR-IIT-009 → IIT-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (456, 76, 'citation', '', 0);  -- OPR-IIT-009 → SAT-IIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (457, 63, 'citation', '', 0);  -- OPR-IIT-014 → IIT-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (457, 58, 'citation', '', 0);  -- OPR-IIT-014 → POL-WHT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (458, 63, 'citation', '', 0);  -- OPR-IIT-015 → IIT-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (459, 63, 'citation', '', 0);  -- OPR-IIT-016 → IIT-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (459, 78, 'citation', '', 0);  -- OPR-IIT-016 → SAT-IIT-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (460, 58, 'citation', '', 0);  -- OPR-IIT-017 → POL-WHT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (460, 63, 'citation', '', 0);  -- OPR-IIT-017 → IIT-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (461, 63, 'citation', '', 0);  -- OPR-IIT-018 → IIT-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (461, 38, 'citation', '', 0);  -- OPR-IIT-018 → POL-PREF-004
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (462, 63, 'citation', '', 0);  -- OPR-IIT-019 → IIT-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (463, 9, 'citation', '', 0);  -- RSK-IIT-006 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (463, 92, 'citation', '', 0);  -- RSK-IIT-006 → TAX-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (464, 9, 'citation', '', 0);  -- RSK-IIT-007 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (464, 92, 'citation', '', 0);  -- RSK-IIT-007 → TAX-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (464, 58, 'citation', '', 0);  -- RSK-IIT-007 → POL-WHT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (465, 9, 'citation', '', 0);  -- SET-IIT-003 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (465, 76, 'citation', '', 0);  -- SET-IIT-003 → SAT-IIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (466, 58, 'citation', '', 0);  -- SET-IIT-004 → POL-WHT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (466, 63, 'citation', '', 0);  -- SET-IIT-004 → IIT-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (467, 7, 'citation', '', 0);  -- SET-IIT-005 → GOV-IIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (467, 63, 'citation', '', 0);  -- SET-IIT-005 → IIT-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (468, 9, 'citation', '', 0);  -- SUS-IIT-003 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (468, 81, 'citation', '', 0);  -- SUS-IIT-003 → SAT-SUS-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (469, 7, 'citation', '', 0);  -- CLS-IIT-004 → GOV-IIT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (469, 63, 'citation', '', 0);  -- CLS-IIT-004 → IIT-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (470, 23, 'citation', '', 0);  -- OPR-VAT-011 → POL-DEC-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (470, 52, 'citation', '', 0);  -- OPR-VAT-011 → POL-VAT-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (471, 48, 'citation', '', 0);  -- OPR-VAT-012 → POL-VAT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (471, 84, 'citation', '', 0);  -- OPR-VAT-012 → SAT-VAT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (472, 48, 'citation', '', 0);  -- OPR-VAT-013 → POL-VAT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (472, 98, 'citation', '', 0);  -- OPR-VAT-013 → TAX-POL-008
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (473, 29, 'citation', '', 0);  -- OPR-VAT-014 → POL-INV-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (473, 73, 'citation', '', 0);  -- OPR-VAT-014 → SAT-INV-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (474, 56, 'citation', '', 0);  -- OPR-VAT-015 → POL-VAT-009
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (474, 54, 'citation', '', 0);  -- OPR-VAT-015 → POL-VAT-005
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (475, 5, 'citation', '', 0);  -- CHG-VAT-006 → GOV-VAT-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (475, 50, 'citation', '', 0);  -- CHG-VAT-006 → POL-VAT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (476, 56, 'citation', '', 0);  -- CLS-VAT-003 → POL-VAT-008
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (476, 5, 'citation', '', 0);  -- CLS-VAT-003 → GOV-VAT-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (477, 93, 'citation', '', 0);  -- RSK-VAT-006 → TAX-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (477, 44, 'citation', '', 0);  -- RSK-VAT-006 → POL-RISK-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (478, 74, 'citation', '', 0);  -- RSK-VAT-007 → SAT-RISK-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (478, 87, 'citation', '', 0);  -- RSK-VAT-007 → SAT-VAT-004
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (479, 4, 'citation', '', 0);  -- SET-VAT-004 → GOV-VAT-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (479, 85, 'citation', '', 0);  -- SET-VAT-004 → SAT-VAT-003

-- 关联关系 (20条)
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (455, 422, 'cross', 0);  -- CHG-IIT-001 → RSK-IIT-005
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (455, 394, 'cross', 0);  -- CHG-IIT-001 → OPR-IIT-006
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (456, 425, 'cross', 0);  -- OPR-IIT-009 → RSK-IIT-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (458, 390, 'cross', 0);  -- OPR-IIT-015 → OPR-IIT-002
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (459, 463, 'cross', 0);  -- OPR-IIT-016 → RSK-IIT-006
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (460, 425, 'cross', 0);  -- OPR-IIT-017 → RSK-IIT-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (463, 464, 'cross', 0);  -- RSK-IIT-006 → RSK-IIT-007
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (465, 426, 'cross', 0);  -- SET-IIT-003 → SET-IIT-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (466, 424, 'cross', 0);  -- SET-IIT-004 → RSK-IIT-003
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (467, 396, 'cross', 0);  -- SET-IIT-005 → OPR-IIT-007
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (468, 428, 'cross', 0);  -- SUS-IIT-003 → SUS-IIT-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (469, 380, 'cross', 0);  -- CLS-IIT-004 → CLS-IIT-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (470, 459, 'cross', 0);  -- OPR-VAT-011 → SET-VAT-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (471, 477, 'cross', 0);  -- OPR-VAT-012 → RSK-VAT-006
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (472, 432, 'cross', 0);  -- OPR-VAT-013 → CHG-VAT-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (473, 450, 'cross', 0);  -- OPR-VAT-014 → RSK-VAT-003
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (477, 478, 'cross', 0);  -- RSK-VAT-006 → RSK-VAT-007
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (479, 457, 'cross', 0);  -- SET-VAT-004 → SET-VAT-003
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (475, 441, 'cross', 0);  -- CHG-VAT-006 → CLS-VAT-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (476, 432, 'cross', 0);  -- CLS-VAT-003 → CHG-VAT-001
