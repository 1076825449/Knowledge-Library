-- =====================================================================
-- 补充：标签关联（question_tag_link）+ 关联问题（question_relation）
-- 前提：003_seed_expand_content.sql 的 question_master 已写入
-- =====================================================================

-- =====================================================================
-- 标签关联
-- =====================================================================

-- SET-REG-003 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'SET-REG-003' AND t.tag_code IN ('SET', 'REG', 'type_how', 'certain_clear', 'tag_registration');

-- SET-REG-004 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'SET-REG-004' AND t.tag_code IN ('SET', 'REG', 'type_how', 'certain_clear', 'tag_registration');

-- SET-DEC-002 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'SET-DEC-002' AND t.tag_code IN ('SET', 'DEC', 'type_whether', 'certain_clear', 'tag_zero_report');

-- OPR-DEC-002 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-DEC-002' AND t.tag_code IN ('OPR', 'DEC', 'type_risk', 'certain_clear', 'tag_zero_report', 'tag_risk');

-- OPR-DEC-003 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-DEC-003' AND t.tag_code IN ('OPR', 'DEC', 'type_whether', 'certain_clear', 'tag_zero_report');

-- OPR-INV-002 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-INV-002' AND t.tag_code IN ('OPR', 'INV', 'type_how', 'certain_clear', 'tag_invoice');

-- OPR-INV-003 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-INV-003' AND t.tag_code IN ('OPR', 'INV', 'type_whether', 'certain_clear', 'tag_invoice');

-- OPR-INV-004 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-INV-004' AND t.tag_code IN ('OPR', 'INV', 'type_whether', 'certain_condition', 'tag_invoice');

-- OPR-CHG-002 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-CHG-002' AND t.tag_code IN ('OPR', 'REG', 'type_how', 'certain_clear', 'tag_change');

-- OPR-CHG-003 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-CHG-003' AND t.tag_code IN ('OPR', 'REG', 'type_whether', 'certain_clear', 'tag_change');

-- OPR-IIT-001 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-IIT-001' AND t.tag_code IN ('OPR', 'IIT', 'type_why', 'certain_clear');

-- OPR-SSF-001 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-SSF-001' AND t.tag_code IN ('OPR', 'SSF', 'type_time', 'certain_clear');

-- OPR-FEE-001 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-FEE-001' AND t.tag_code IN ('OPR', 'FEE', 'type_whether', 'certain_clear');

-- OPR-RISK-001 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-RISK-001' AND t.tag_code IN ('OPR', 'RISK', 'type_risk', 'certain_clear', 'tag_risk');

-- CLS-CLEAR-002 标签
INSERT INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'CLS-CLEAR-002' AND t.tag_code IN ('CLS', 'CLEAR', 'type_how', 'certain_clear');

-- =====================================================================
-- 关联问题
-- =====================================================================

-- SET-REG 系列关联
INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'SET-REG-001' AND r.question_code = 'SET-REG-002';

INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'SET-REG-002' AND r.question_code = 'SET-REG-003';

INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 2
FROM question_master q, question_master r
WHERE q.question_code = 'SET-REG-002' AND r.question_code = 'SET-DEC-002';

INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'SET-REG-003' AND r.question_code = 'OPR-DEC-001';

INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 2
FROM question_master q, question_master r
WHERE q.question_code = 'SET-REG-003' AND r.question_code = 'SET-REG-004';

INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'SET-DEC-002' AND r.question_code = 'OPR-DEC-001';

INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 2
FROM question_master q, question_master r
WHERE q.question_code = 'SET-DEC-002' AND r.question_code = 'OPR-DEC-002';

-- OPR-INV 系列关联
INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'OPR-INV-001' AND r.question_code = 'OPR-INV-003';

INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 2
FROM question_master q, question_master r
WHERE q.question_code = 'OPR-INV-001' AND r.question_code = 'OPR-INV-002';

-- OPR-DEC 系列关联
INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'OPR-DEC-001' AND r.question_code = 'OPR-DEC-002';

INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 2
FROM question_master q, question_master r
WHERE q.question_code = 'OPR-DEC-001' AND r.question_code = 'OPR-DEC-003';

INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'OPR-DEC-002' AND r.question_code = 'OPR-RISK-001';

-- OPR-CHG 系列关联
INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'OPR-CHG-001' AND r.question_code = 'OPR-CHG-002';

INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 2
FROM question_master q, question_master r
WHERE q.question_code = 'OPR-CHG-001' AND r.question_code = 'OPR-CHG-003';

-- CLS-CLEAR 系列关联
INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'CLS-CLEAR-001' AND r.question_code = 'CLS-CLEAR-002';
