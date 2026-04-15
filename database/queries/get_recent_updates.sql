-- ============================================================
-- 文件：get_recent_updates.sql
-- 描述：查询最近更新的问题
-- ============================================================

-- 最近更新（取每个问题的最新一条更新记录）
SELECT DISTINCT
    q.question_code,
    q.question_title,
    q.one_line_answer,
    q.stage_code,
    q.module_code,
    q.updated_at,
    qul.change_summary
FROM question_master q
JOIN (
    SELECT question_id, MAX(update_date) as max_date
    FROM question_update_log
    GROUP BY question_id
) latest ON q.id = latest.question_id
JOIN question_update_log qul ON q.id = qul.question_id AND qul.update_date = latest.max_date
WHERE q.status = 'active'
ORDER BY qul.update_date DESC
LIMIT :limit;
