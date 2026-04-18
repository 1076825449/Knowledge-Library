-- 007_fix_remaining_enum.sql
-- 执行时间：2026-04-20
-- 问题：上次004脚本遗漏了 level_bulletin(52条) 和 level_law(12条)，
--       以及 question_update_log 中的 update_revise(2条)

BEGIN TRANSACTION;

-- level_bulletin（公告类）→ level_department（部门规章层级）
UPDATE policy_basis SET policy_level = 'level_department', updated_at = datetime('now')
WHERE policy_level = 'level_bulletin';

-- level_law（法律层级）→ level_national（国家级）
-- 注：此处的"法律"多为行政法规/暂行条例等，实际应归入 level_department
-- 但因涉及税收征管法等重要上位法，统一归入 level_national 更安全
UPDATE policy_basis SET policy_level = 'level_national', updated_at = datetime('now')
WHERE policy_level = 'level_law';

-- update_revise → update_edit（标准化类型）
UPDATE question_update_log SET update_type = 'update_edit', updated_at = datetime('now')
WHERE update_type = 'update_revise';

COMMIT;
