-- fix_opr_stage_naming.sql
-- 修复6个 STAGE-MODULE-003 → STAGE-MODULE-XXX 命名错误
-- 命名规范：STAGE代码-MODULE代码-序号，但 MODULE-OPR-003 用了 MODULE 作为前缀
--
-- 运行前已验证所有目标代码均不存在，源代码均存在，policy_links 自然保留

BEGIN;

UPDATE question_master SET question_code='OPR-VAT-016'    WHERE question_code='VAT-OPR-003';
UPDATE question_master SET question_code='OPR-REG-023'    WHERE question_code='REG-OPR-003';
UPDATE question_master SET question_code='OPR-PREF-021'   WHERE question_code='PREF-OPR-003';
UPDATE question_master SET question_code='OPR-SSF-022'     WHERE question_code='SSF-OPR-003';
UPDATE question_master SET question_code='OPR-DEC-044'     WHERE question_code='DEC-OPR-003';
UPDATE question_master SET question_code='OPR-CLEAR-029'  WHERE question_code='CLEAR-OPR-003';

COMMIT;
