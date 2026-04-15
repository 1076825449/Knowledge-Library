-- ============================================================
-- 文件：get_question_detail.sql
-- 描述：查询问题详情与政策依据
-- ============================================================

-- 问题详情（含所有字段）
SELECT
    q.id,
    q.question_code,
    q.question_title,
    q.question_plain,
    q.stage_code,
    q.module_code,
    q.question_type,
    q.one_line_answer,
    q.detailed_answer,
    q.core_definition,
    q.applicable_conditions,
    q.exceptions_boundary,
    q.practical_steps,
    q.risk_warning,
    q.scope_level,
    q.local_region,
    q.answer_certainty,
    q.keywords,
    q.high_frequency_flag,
    q.newbie_flag,
    q.status,
    q.version_no,
    q.created_at,
    q.updated_at
FROM question_master q
WHERE q.question_code = :question_code;

-- 政策依据列表
SELECT
    p.id AS policy_id,
    p.policy_code,
    p.policy_name,
    p.document_no,
    p.article_ref,
    p.policy_level,
    p.effective_date,
    p.current_status,
    p.policy_summary,
    p.raw_quote_short,
    qpl.support_type,
    qpl.support_note
FROM question_master q
JOIN question_policy_link qpl ON q.id = qpl.question_id
JOIN policy_basis p ON qpl.policy_id = p.id
WHERE q.question_code = :question_code
ORDER BY qpl.display_order;

-- 标签列表
SELECT
    t.tag_code,
    t.tag_name,
    t.tag_category,
    qtl.is_primary
FROM question_master q
JOIN question_tag_link qtl ON q.id = qtl.question_id
JOIN tag_dict t ON qtl.tag_id = t.id
WHERE q.question_code = :question_code
ORDER BY qtl.is_primary DESC, qtl.display_order;

-- 关联问题
SELECT
    qr.related_id,
    q2.question_code,
    q2.question_title,
    q2.one_line_answer,
    qr.relation_type
FROM question_master q
JOIN question_relation qr ON q.id = qr.question_id
JOIN question_master q2 ON qr.related_id = q2.id
WHERE q.question_code = :question_code
ORDER BY qr.display_order;

-- 更新记录
SELECT
    qul.version_no,
    qul.update_date,
    qul.update_type,
    qul.update_reason,
    qul.updated_by,
    qul.reviewed_by,
    qul.change_summary
FROM question_master q
JOIN question_update_log qul ON q.id = qul.question_id
WHERE q.question_code = :question_code
ORDER BY qul.version_no DESC;

-- 地方口径
SELECT
    lrn.region_code,
    lrn.region_name,
    lrn.local_content,
    lrn.authority_name,
    lrn.effective_date,
    lrn.source_url
FROM question_master q
JOIN local_rule_note lrn ON q.id = lrn.question_id
WHERE q.question_code = :question_code;
