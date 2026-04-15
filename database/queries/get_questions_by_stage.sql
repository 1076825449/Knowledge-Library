-- ============================================================
-- 文件：get_questions_by_stage.sql
-- 描述：按阶段查询问题列表
-- ============================================================

-- 按阶段查询（支持分页）
SELECT
    q.question_code,
    q.question_title,
    q.one_line_answer,
    q.stage_code,
    q.module_code,
    q.answer_certainty,
    q.high_frequency_flag,
    q.newbie_flag,
    q.updated_at
FROM question_master q
WHERE q.stage_code = :stage_code
  AND q.status = 'active'
ORDER BY q.high_frequency_flag DESC, q.updated_at DESC
LIMIT :limit OFFSET :offset;

-- 按阶段统计数量
SELECT COUNT(*) as total
FROM question_master
WHERE stage_code = :stage_code
  AND status = 'active';
