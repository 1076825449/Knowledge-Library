-- ============================================================
-- database/seed/004_fix_enum_dirty_data.sql
-- 修复枚举脏数据（由批量导入历史遗留）
-- 执行时间：2026-04-20
-- 影响：policy_basis(14+48条) + question_update_log(100条)
-- ============================================================

-- 1. policy_basis.policy_level：中文值和 level_regulation 统一为标准前缀
UPDATE policy_basis SET policy_level = 'level_department' WHERE policy_level = '规范性文件';  -- 5条
UPDATE policy_basis SET policy_level = 'level_admin'      WHERE policy_level = '行政规章';    -- 1条
UPDATE policy_basis SET policy_level = 'level_local'      WHERE policy_level = 'local';        -- 5条
UPDATE policy_basis SET policy_level = 'level_department' WHERE policy_level = 'level_regulation'; -- 3条

-- 2. policy_basis.current_status：effective/active 统一为 pol_effective
UPDATE policy_basis SET current_status = 'pol_effective' WHERE current_status IN ('effective', 'active');  -- 48条

-- 3. question_update_log.update_type：create 统一为 update_new
UPDATE question_update_log SET update_type = 'update_new' WHERE update_type = 'create';  -- 100条

-- 验证查询（执行后运行以下 SQL 确认）
-- SELECT DISTINCT policy_level FROM policy_basis;
-- SELECT DISTINCT current_status FROM policy_basis;
-- SELECT DISTINCT update_type FROM question_update_log;
