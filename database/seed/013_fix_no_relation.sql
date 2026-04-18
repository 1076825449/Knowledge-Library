-- ============================================================
-- 013_fix_no_relation.sql
-- 修复48条无关联问题，补全73条cross relations
-- 状态: 0条无关联问题
-- ============================================================

-- 关联关系 (73条)

INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (435, 49, 'cross', 0);  -- OPR-CIT-019 → OPR-CIT-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (435, 440, 'cross', 0);  -- OPR-CIT-019 → RSK-CIT-005
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (436, 434, 'cross', 0);  -- OPR-CIT-020 → OPR-CIT-018
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (436, 440, 'cross', 0);  -- OPR-CIT-020 → RSK-CIT-005
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (437, 434, 'cross', 0);  -- OPR-CIT-021 → OPR-CIT-018
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (437, 440, 'cross', 0);  -- OPR-CIT-021 → RSK-CIT-005
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (441, 450, 'cross', 0);  -- RSK-CIT-006 → RSK-FEE-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (441, 484, 'cross', 0);  -- RSK-CIT-006 → RSK-INV-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (445, 446, 'cross', 0);  -- OPR-FEE-016 → OPR-FEE-017
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (445, 434, 'cross', 0);  -- OPR-FEE-016 → OPR-CIT-018
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (446, 450, 'cross', 0);  -- OPR-FEE-017 → RSK-FEE-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (447, 255, 'cross', 0);  -- OPR-FEE-018 → OPR-FEE-005
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (447, 450, 'cross', 0);  -- OPR-FEE-018 → RSK-FEE-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (451, 485, 'cross', 0);  -- RSK-FEE-005 → RSK-INV-002
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (451, 71, 'cross', 0);  -- RSK-FEE-005 → OPR-FEE-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (455, 461, 'cross', 0);  -- OPR-IIT-014 → RSK-IIT-006
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (455, 57, 'cross', 0);  -- OPR-IIT-014 → OPR-IIT-002
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (459, 434, 'cross', 0);  -- OPR-IIT-018 → OPR-CIT-018
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (459, 461, 'cross', 0);  -- OPR-IIT-018 → RSK-IIT-006
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (460, 461, 'cross', 0);  -- OPR-IIT-019 → RSK-IIT-006
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (460, 467, 'cross', 0);  -- OPR-IIT-019 → CLS-IIT-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (462, 273, 'cross', 0);  -- RSK-IIT-007 → RSK-IIT-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (462, 461, 'cross', 0);  -- RSK-IIT-007 → RSK-IIT-006
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (490, 381, 'cross', 0);  -- CLS-INV-005 → CLS-INV-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (479, 3, 'cross', 0);  -- OPR-INV-021 → OPR-INV-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (480, 486, 'cross', 0);  -- OPR-INV-022 → RSK-INV-003
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (481, 469, 'cross', 0);  -- OPR-INV-023 → OPR-VAT-012
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (481, 485, 'cross', 0);  -- OPR-INV-023 → RSK-INV-002
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (483, 252, 'cross', 0);  -- OPR-INV-025 → RSK-FEE-003
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (483, 14, 'cross', 0);  -- OPR-INV-025 → OPR-INV-003
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (485, 475, 'cross', 0);  -- RSK-INV-002 → RSK-VAT-006
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (485, 450, 'cross', 0);  -- RSK-INV-002 → RSK-FEE-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (486, 450, 'cross', 0);  -- RSK-INV-003 → RSK-FEE-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (491, 136, 'cross', 0);  -- SUS-INV-003 → SUS-INV-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (492, 136, 'cross', 0);  -- SUS-INV-004 → SUS-INV-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (492, 203, 'cross', 0);  -- SUS-INV-004 → SUS-VAT-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (500, 474, 'cross', 0);  -- CLS-PREF-004 → CLS-VAT-003
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (500, 473, 'cross', 0);  -- CLS-PREF-004 → CHG-VAT-006
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (497, 178, 'cross', 0);  -- OPR-PREF-016 → OPR-PREF-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (497, 498, 'cross', 0);  -- OPR-PREF-016 → RSK-PREF-003
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (499, 498, 'cross', 0);  -- RSK-PREF-004 → RSK-PREF-003
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (501, 192, 'cross', 0);  -- SUS-PREF-003 → SUS-PREF-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (503, 221, 'cross', 0);  -- CHG-SSF-008 → CHG-SSF-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (512, 360, 'cross', 0);  -- CHG-SSF-009 → CLS-SSF-002
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (504, 359, 'cross', 0);  -- CLS-SSF-005 → CLS-SSF-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (505, 66, 'cross', 0);  -- OPR-SSF-015 → OPR-SSF-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (505, 509, 'cross', 0);  -- OPR-SSF-015 → RSK-SSF-005
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (506, 298, 'cross', 0);  -- OPR-SSF-016 → OPR-SSF-008
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (507, 66, 'cross', 0);  -- OPR-SSF-017 → OPR-SSF-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (508, 66, 'cross', 0);  -- OPR-SSF-018 → OPR-SSF-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (513, 46, 'cross', 0);  -- OPR-SSF-019 → OPR-SSF-003
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (514, 68, 'cross', 0);  -- OPR-SSF-020 → OPR-SSF-006
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (515, 66, 'cross', 0);  -- OPR-SSF-021 → OPR-SSF-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (509, 310, 'cross', 0);  -- RSK-SSF-005 → RSK-SSF-004
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (510, 311, 'cross', 0);  -- SET-SSF-003 → SET-SSF-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (511, 375, 'cross', 0);  -- SUS-SSF-002 → SUS-SSF-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (519, 525, 'cross', 0);  -- OPR-TAX-018 → SET-TAX-003
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (520, 258, 'cross', 0);  -- OPR-TAX-019 → OPR-TAX-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (521, 435, 'cross', 0);  -- OPR-TAX-020 → OPR-CIT-019
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (522, 429, 'cross', 0);  -- RSK-TAX-011 → RSK-TAX-010
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (522, 428, 'cross', 0);  -- RSK-TAX-011 → RSK-TAX-009
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (523, 428, 'cross', 0);  -- RSK-TAX-012 → RSK-TAX-009
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (523, 391, 'cross', 0);  -- RSK-TAX-012 → RSK-TAX-005
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (524, 391, 'cross', 0);  -- RSK-TAX-013 → RSK-TAX-005
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (524, 392, 'cross', 0);  -- RSK-TAX-013 → RSK-TAX-006
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (525, 262, 'cross', 0);  -- SET-TAX-003 → SET-TAX-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (526, 262, 'cross', 0);  -- SET-TAX-004 → SET-TAX-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (526, 315, 'cross', 0);  -- SET-TAX-004 → OPR-TAX-011
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (527, 266, 'cross', 0);  -- CLS-TAX-004 → CLS-TAX-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (527, 523, 'cross', 0);  -- CLS-TAX-004 → RSK-TAX-012
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (472, 468, 'cross', 0);  -- OPR-VAT-015 → OPR-VAT-011
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (472, 476, 'cross', 0);  -- OPR-VAT-015 → RSK-VAT-007
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (476, 198, 'cross', 0);  -- RSK-VAT-007 → RSK-VAT-001
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (476, 373, 'cross', 0);  -- RSK-VAT-007 → RSK-VAT-004