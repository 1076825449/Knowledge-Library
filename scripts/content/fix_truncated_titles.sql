-- fix_truncated_titles.sql
-- 修复 5 条 IIT/SUS/SSF 模块截断标题问题
-- 标题从 25 字符截断恢复为完整内容

BEGIN;

-- CLS-IIT-001: 注销时自然人股东取得清算分配款，企业须先代扣20%股息红利个税
UPDATE question_master SET
    question_title = '企业注销时向自然人股东分配清算款项，如何代扣代缴个人所得税？',
    question_plain = '公司注销时，清算组在还清税款和职工工资后还有剩余财产要分配给自然人股东。这种情况下企业需要代扣代缴个人所得税吗？具体要扣多少？怎么申报？'
WHERE question_code = 'CLS-IIT-001';

-- CLS-IIT-003: 注销前资本公积转增注册资本，自然人股东须代扣20%个税
UPDATE question_master SET
    question_title = '注销前资本公积转增注册资本，自然人股东须缴纳多少个人所得税？',
    question_plain = '公司在注销前，股东会决议用资本公积转增注册资本。自然人股东需要缴纳个人所得税吗？税率是多少？企业需要履行什么扣缴义务？'
WHERE question_code = 'CLS-IIT-003';

-- SUS-IIT-001: 停业期间个人所得税代扣代缴义务仍然存在
UPDATE question_master SET
    question_title = '停业期间企业是否仍有个人所得税代扣代缴义务？具体要如何处理？',
    question_plain = '公司目前处于停业状态，没有开展业务，员工都已离职在家。停业期间如果没有任何个人所得，还要不要申报个人所得税？如果有个人所得（比如发放生活费），要怎么处理？'
WHERE question_code = 'SUS-IIT-001';

-- SUS-IIT-002: 停业期间向个人股东分红仍须代扣20%个税
UPDATE question_master SET
    question_title = '停业期间向个人股东分红，是否仍须代扣代缴个人所得税？',
    question_plain = '公司目前停业中，但股东会决定分配一部分未分配利润。请问停业期间分红，个人所得税还要不要扣？停业状态能否作为免税理由？'
WHERE question_code = 'SUS-IIT-002';

-- SUS-SSF-001: 停业期间社保缴纳以劳动关系为准，员工未减员则须继续缴纳
UPDATE question_master SET
    question_title = '停业期间社保是否仍须缴纳？员工全部离职后是否就可以暂停缴纳？',
    question_plain = '公司停业了，员工都已经离职并办理了社保减员。请问这种情况下，社保是不是就可以暂停缴纳了？如果部分员工还在（待岗状态），要怎么处理？'
WHERE question_code = 'SUS-SSF-001';

COMMIT;
