-- ============================================================
-- 文件：get_questions_by_tag.sql
-- 描述：按标签查询问题列表
-- ============================================================

-- 按标签查询（支持分页）
SELECT
    q.question_code,
    q.question_title,
    q.one_line_answer,
    q.stage_code,
    q.module_code,
    q.answer_certainty,
    q.high_frequency_flag,
    q.newbie_flag,
    q.updated_at,
    t.tag_name AS primary_tag
FROM question_master q
JOIN question_tag_link qtl ON q.id = qtl.question_id
JOIN tag_dict t ON qtl.tag_id = t.id
WHERE t.tag_code = :tag_code
  AND q.status = 'active'
  AND qtl.is_primary = 1
ORDER BY q.high_frequency_flag DESC, q.updated_at DESC
LIMIT :limit OFFSET :offset;

-- 按标签统计数量
SELECT COUNT(*) as total
FROM question_master q
JOIN question_tag_link qtl ON q.id = qtl.question_id
JOIN tag_dict t ON qtl.tag_id = t.id
WHERE t.tag_code = :tag_code
  AND q.status = 'active';
