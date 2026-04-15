-- ============================================================
-- 文件：search_questions.sql
-- 描述：关键词搜索问题
-- ============================================================

-- 基础搜索（标题 + 关键词字段）
SELECT
    q.question_code,
    q.question_title,
    q.one_line_answer,
    q.stage_code,
    q.module_code,
    q.answer_certainty,
    q.high_frequency_flag,
    q.newbie_flag,
    q.keywords
FROM question_master q
WHERE q.status = 'active'
  AND (
    q.question_title LIKE '%' || :keyword || '%'
    OR q.keywords LIKE '%' || :keyword || '%'
    OR q.one_line_answer LIKE '%' || :keyword || '%'
  )
ORDER BY
    CASE WHEN q.question_title LIKE '%' || :keyword || '%' THEN 0 ELSE 1 END,
    q.high_frequency_flag DESC,
    q.updated_at DESC
LIMIT :limit OFFSET :offset;

-- 搜索结果数量
SELECT COUNT(*) as total
FROM question_master q
WHERE q.status = 'active'
  AND (
    q.question_title LIKE '%' || :keyword || '%'
    OR q.keywords LIKE '%' || :keyword || '%'
    OR q.one_line_answer LIKE '%' || :keyword || '%'
  );

-- 高频问题（首页用）
SELECT
    q.question_code,
    q.question_title,
    q.one_line_answer,
    q.stage_code
FROM question_master q
WHERE q.status = 'active'
  AND q.high_frequency_flag = 1
ORDER BY q.updated_at DESC
LIMIT :limit;

-- 新手必看（首页用）
SELECT
    q.question_code,
    q.question_title,
    q.one_line_answer,
    q.stage_code
FROM question_master q
WHERE q.status = 'active'
  AND q.newbie_flag = 1
ORDER BY q.updated_at DESC
LIMIT :limit;
