-- ============================================================
-- 012_expand_ssf_tax.sql
-- SSF(+15净新增) + TAX(+10净新增) 扩容
-- 包含: question_policy_link(48条) + question_relation(3条已验证)
-- 状态: SSF=46条, TAX=44条
-- ============================================================

-- 政策引用 (48条)

INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (503, 95, 'citation', '', 0);  -- CHG-SSF-008 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (503, 96, 'citation', '', 0);  -- CHG-SSF-008 → SSF-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (504, 95, 'citation', '', 0);  -- CLS-SSF-005 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (504, 96, 'citation', '', 0);  -- CLS-SSF-005 → SSF-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (505, 95, 'citation', '', 0);  -- OPR-SSF-015 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (505, 39, 'citation', '', 0);  -- OPR-SSF-015 → POL-SSF-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (506, 95, 'citation', '', 0);  -- OPR-SSF-016 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (506, 96, 'citation', '', 0);  -- OPR-SSF-016 → SSF-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (507, 95, 'citation', '', 0);  -- OPR-SSF-017 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (508, 95, 'citation', '', 0);  -- OPR-SSF-018 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (508, 39, 'citation', '', 0);  -- OPR-SSF-018 → POL-SSF-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (509, 95, 'citation', '', 0);  -- RSK-SSF-005 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (509, 90, 'citation', '', 0);  -- RSK-SSF-005 → TAX-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (510, 95, 'citation', '', 0);  -- SET-SSF-003 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (510, 39, 'citation', '', 0);  -- SET-SSF-003 → POL-SSF-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (511, 95, 'citation', '', 0);  -- SUS-SSF-002 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (511, 39, 'citation', '', 0);  -- SUS-SSF-002 → POL-SSF-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (512, 96, 'citation', '', 0);  -- CHG-SSF-009 → SSF-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (512, 95, 'citation', '', 0);  -- CHG-SSF-009 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (513, 95, 'citation', '', 0);  -- OPR-SSF-019 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (513, 96, 'citation', '', 0);  -- OPR-SSF-019 → SSF-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (514, 95, 'citation', '', 0);  -- OPR-SSF-020 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (514, 96, 'citation', '', 0);  -- OPR-SSF-020 → SSF-POL-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (515, 95, 'citation', '', 0);  -- OPR-SSF-021 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (516, 95, 'citation', '', 0);  -- RSK-SSF-006 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (516, 90, 'citation', '', 0);  -- RSK-SSF-006 → TAX-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (517, 95, 'citation', '', 0);  -- SUS-SSF-003 → SSF-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (517, 39, 'citation', '', 0);  -- SUS-SSF-003 → POL-SSF-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (518, 1, 'citation', '', 0);  -- OPR-TAX-017 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (518, 90, 'citation', '', 0);  -- OPR-TAX-017 → TAX-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (519, 1, 'citation', '', 0);  -- OPR-TAX-018 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (519, 2, 'citation', '', 0);  -- OPR-TAX-018 → GOV-Tax-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (520, 85, 'citation', '', 0);  -- OPR-TAX-019 → SAT-TAX-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (520, 97, 'citation', '', 0);  -- OPR-TAX-019 → TAX-POL-006
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (521, 97, 'citation', '', 0);  -- OPR-TAX-020 → TAX-POL-006
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (521, 1, 'citation', '', 0);  -- OPR-TAX-020 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (522, 1, 'citation', '', 0);  -- RSK-TAX-011 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (522, 90, 'citation', '', 0);  -- RSK-TAX-011 → TAX-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (523, 92, 'citation', '', 0);  -- RSK-TAX-012 → TAX-POL-003
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (523, 1, 'citation', '', 0);  -- RSK-TAX-012 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (524, 90, 'citation', '', 0);  -- RSK-TAX-013 → TAX-POL-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (524, 1, 'citation', '', 0);  -- RSK-TAX-013 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (525, 1, 'citation', '', 0);  -- SET-TAX-003 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (525, 2, 'citation', '', 0);  -- SET-TAX-003 → GOV-Tax-002
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (526, 1, 'citation', '', 0);  -- SET-TAX-004 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (526, 10, 'citation', '', 0);  -- SET-TAX-004 → SAT-TAX-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (527, 1, 'citation', '', 0);  -- CLS-TAX-004 → GOV-Tax-001
INSERT OR IGNORE INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order) VALUES (527, 83, 'citation', '', 0);  -- CLS-TAX-004 → SAT-CLEAR-001

-- 关联关系 (仅验证通过者，未验证者见注释)

-- SKIP (target may not exist): CHG-SSF-008 → CHG-SSF-001
-- SKIP (target may not exist): CLS-SSF-005 → CLS-SSF-001
-- SKIP (target may not exist): RSK-SSF-005 → RSK-SSF-004
-- SKIP (target may not exist): SET-SSF-003 → SET-SSF-001
-- SKIP (target may not exist): SUS-SSF-002 → SUS-SSF-001
-- SKIP (target may not exist): CHG-SSF-009 → CLS-SSF-002
-- SKIP (target may not exist): OPR-SSF-019 → OPR-SSF-003
-- SKIP (target may not exist): OPR-SSF-020 → OPR-SSF-006
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (516, 509, 'cross', 0);  -- RSK-SSF-006 → RSK-SSF-005 [VERIFIED]
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (517, 511, 'cross', 0);  -- SUS-SSF-003 → SUS-SSF-002 [VERIFIED]
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order) VALUES (518, 523, 'cross', 0);  -- OPR-TAX-017 → RSK-TAX-012 [VERIFIED]
-- SKIP (target may not exist): OPR-TAX-018 → SET-TAX-001
-- SKIP (target may not exist): OPR-TAX-019 → OPR-TAX-001
-- SKIP (target may not exist): RSK-TAX-011 → RSK-TAX-010
-- SKIP (target may not exist): RSK-TAX-012 → RSK-TAX-009
-- SKIP (target may not exist): SET-TAX-003 → SET-TAX-001
-- SKIP (target may not exist): SET-TAX-004 → OPR-TAX-011
-- SKIP (target may not exist): CLS-TAX-004 → CLS-TAX-001