-- fix_malformed_codes.sql
-- 修复两批次非法代码格式：
--   1. RISK-RISK-XXX → RSK-RISK-0(28~31)  (stage_code前缀错误)
--   2. TAX-TAX-001  → OPR-TAX-022        (TAX非法作为stage_code)
-- 运行前已验证：所有目标代码均不存在，源代码均存在

BEGIN;

-- 1. RISK-RISK-001~004 → RSK-RISK-028~031
-- 语义不同的4个问题，保留id/policy_links等关联，修改question_code
UPDATE question_master SET question_code='RSK-RISK-028' WHERE question_code='RISK-RISK-001';
UPDATE question_master SET question_code='RSK-RISK-029' WHERE question_code='RISK-RISK-002';
UPDATE question_master SET question_code='RSK-RISK-030' WHERE question_code='RISK-RISK-003';
UPDATE question_master SET question_code='RSK-RISK-031' WHERE question_code='RISK-RISK-004';

-- 2. TAX-TAX-001 → OPR-TAX-022
-- TAX-TAX-001: "企业所得税自行申报与源泉扣缴有何不同？" module=TAX stage=OPR type=type_compare
-- OPR-TAX-022: 空缺，语义匹配（运营阶段 TAX模块 对比类问题）
UPDATE question_master SET question_code='OPR-TAX-022' WHERE question_code='TAX-TAX-001';

COMMIT;
