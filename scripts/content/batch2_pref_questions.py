#!/usr/bin/env python3
"""批量导入PREF税收优惠模块第二批问题（5条）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.config import DB_PATH
import sqlite3

QUESTIONS = [
    {
        "question_code": "OPR-PREF-004",
        "question_title": "高新企业认定需要满足哪些条件？如何申请？",
        "question_plain": "高新企业认定条件申请流程",
        "stage_code": "OPR",
        "module_code": "PREF",
        "question_type": "type_procedure",
        "one_line_answer": "高新企业认定需满足：注册满一年、自主知识产权、领域符合、研发费占比>=5%/4%/2%（按收入分档）、高新收入占比>=60%、科技人员占比>=10%。认定在高新技术企业认定管理工作网在线申报，每年受理一次。",
        "detailed_answer": "高新技术企业认定采用评分制，满分100分，需达到70分以上：知识产权<=30分，拥有核心自主知识产权；科技成果转化<=30分；研发管理<=20分；成长性<=20分。申请流程：注册高企工作网→在线填写申报材料→专家评审→认定报备→公示10个工作日→颁发证书（有效期3年，期满需重新认定）。",
        "core_definition": "高新企业认定是对企业科技创新能力的官方认证，认证后可享受15%优惠税率（较25%法定税率低10个百分点）。",
        "applicable_conditions": "注册满一年的居民企业；拥有核心自主知识产权；研发费用占比达标；高新技术产品收入占比>=60%；科技人员占比>=10%；申请前无重大安全质量事故或环境违法行为",
        "exceptions_boundary": "知识产权仅购买或转让的不可计分；认定后抽查不合格将取消资格并追缴税款",
        "practical_steps": "1.初步自评（在线评分表）；2.整理知识产权；3.建立研发辅助账；4.在高企工作网在线提交材料；5.等待评审结果",
        "risk_warning": "认定后需每年报送年度发展情况报表；抽查发现不达标将被取消资格并追缴已减税",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_conditional",
        "keywords": "高新企业认定,自主知识产权,研发费用占比,高新技术产品收入",
        "high_frequency_flag": 0,
        "newbie_flag": 0,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-006", "support_type": "support_direct", "support_note": "高新企业认定管理办法全文，明确认定条件和程序"},
        ],
    },
    {
        "question_code": "OPR-PREF-005",
        "question_title": "增值税留抵退税的申请条件是什么？如何操作？",
        "question_plain": "留抵退税申请条件操作流程",
        "stage_code": "OPR",
        "module_code": "PREF",
        "question_type": "type_procedure",
        "one_line_answer": "符合条件的小微企业和制造业等行业企业，可申请增量或存量留抵退税。条件：纳税信用等级为A级或B级；申请前36个月无骗取留抵退税记录；2019年4月起未享受即征即退。",
        "detailed_answer": "留抵退税分两类：增量留抵退税与2019年3月底相比，当期增量留抵税额>0即可申请；存量留抵退税小微企业和制造业等行业企业可一次性退还。计算公式：退还增量=当期增量留抵税额 x 进项构成比例。申请时间：征期内（每月1-15日）在电子税务局提交申请，审核通过后税款自动退至企业账户。",
        "core_definition": "留抵退税是将企业进项税额大于销项税额的差额以现金形式退还给企业，缓解资金压力。",
        "applicable_conditions": "小规模纳税人转登记纳税人、小微企业和制造业等行业企业；增量留抵与2019年3月底相比为正；纳税信用等级A级或B级；近36个月无骗税记录",
        "exceptions_boundary": "存在稽查未结案件的企业暂不允许申请；非独立核算分公司分别判断",
        "practical_steps": "1.登录电子税务局查询当前留抵税额和信用等级；2.确认进项构成比例；3.填写申请表；4.提交后5-10个工作日内审核",
        "risk_warning": "骗取留抵退税属严重违法行为，追缴税款+滞纳金+0.5-5倍罚款并信用降级",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_conditional",
        "keywords": "留抵退税,增量留抵,存量留抵,进项税额,增值税退税",
        "high_frequency_flag": 1,
        "newbie_flag": 0,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-008", "support_type": "support_direct", "support_note": "小微企业和制造业等行业企业可申请增量留抵退税和存量留抵退税"},
        ],
    },
    {
        "question_code": "OPR-PREF-006",
        "question_title": "软件企业两免三减半优惠如何申请？适用条件是什么？",
        "question_plain": "软件企业两免三减半优惠申请条件",
        "stage_code": "OPR",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "国家鼓励的软件企业，自盈利年度起，第一年至第二年免征企业所得税，第三年至第五年减按25%的税率减半征收（实际税负约12.5%）。需先在工信部门备案并取得软件企业认定证书，再向主管税务机关备案。",
        "detailed_answer": "软件企业两免三减半优惠前提条件：符合国家鼓励的软件企业条件；拥有核心关键技术；当年软件产品开发销售收入占企业收入总额>=50%；研究开发费用占企业收入总额>=7%。备案流程：企业自查符合条件→在工信部软件和信息服务业网填报备案→取得软件企业认定证书→向主管税务机关提交备案资料→主管税务机关受理后生效。优惠周期从企业开始获利年度起算。",
        "core_definition": "软件企业两免三减半是企业所得税优惠，获利年度起算，前两年免征，后三年减半，按25%法定税率减半约12.5%税负。",
        "applicable_conditions": "取得软件企业认定证书；年应纳税所得额>0；有盈利；收入结构符合软件企业比例要求；在有效期内向税务机关完成备案",
        "exceptions_boundary": "外购软件作为商品销售不享受优惠；两免三减半与高新优惠不可叠加，企业需择一适用",
        "practical_steps": "1.自查是否符合条件；2.向工信部门申请软件企业认定；3.取得证书后向主管税务机关提交备案材料；4.年度汇算清缴时填报优惠明细表",
        "risk_warning": "软件企业认定证书有效期1年，逾期需重新认定；需每年向主管税务机关提交年度报告",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_conditional",
        "keywords": "软件企业,两免三减半,企业所得税优惠,软件企业认定",
        "high_frequency_flag": 0,
        "newbie_flag": 0,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-010", "support_type": "support_direct", "support_note": "国家鼓励的软件企业自盈利年度起享受两免三减半"},
        ],
    },
    {
        "question_code": "SET-PREF-002",
        "question_title": "残疾人就业优惠企业可以享受哪些政策？如何申请？",
        "question_plain": "残疾人就业优惠企业申请条件",
        "stage_code": "SET",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "安置残疾人的企业，可按安置人数享受增值税即征即退：每人每月最低工资4倍退还增值税；同时可享受企业所得税加计扣除。需先向主管税务机关申请成为残疾人就业单位。",
        "detailed_answer": "残疾人就业优惠包含三个层面：增值税即征即退：企业安置残疾人的，在职职工总数中残疾人占比>=25%（或10人以上企业占比>=1.5%），按安置人数 x 当地月最低工资标准 x 4倍退还增值税。企业所得税：残疾人员工工资在计算应纳税所得额时可加计100%扣除。残保金减免：达到规定比例（1.5%）的企业无需缴纳残疾人就业保障金。",
        "core_definition": "残疾人就业优惠通过增值税退税+企业所得税加计扣除+残保金减免三个渠道为企业减负。",
        "applicable_conditions": "与残疾人依法签订一年以上劳动合同；实际支付的工资不低于当地最低工资标准；为残疾人足额缴纳社会保险；按规定完成残疾人就业申报",
        "exceptions_boundary": "享受增值税即征即退后，同一笔工资支出不可再重复享受企税加计以外的优惠",
        "practical_steps": "1.与符合条件的残疾人签订劳动合同并缴纳社保；2.向当地残联申报残疾人就业情况；3.持残联出具的核定表，向主管税务机关申请增值税即征即退备案；4.季度预缴和年度汇算时分别填报企税加计扣除",
        "risk_warning": "虚报残疾人就业人数骗取退税将被追缴税款、处以罚款并加收滞纳金，情节严重追究刑事责任",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_conditional",
        "keywords": "残疾人就业优惠,增值税即征即退,残保金,企税加计扣除",
        "high_frequency_flag": 0,
        "newbie_flag": 0,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-007", "support_type": "support_direct", "support_note": "安置残疾人可享受每人每月最低工资4倍的增值税即征即退"},
        ],
    },
    {
        "question_code": "OPR-PREF-007",
        "question_title": "小规模纳税人3%征收率减按1%征收的政策如何适用？",
        "question_plain": "小规模纳税人3%减按1%政策适用",
        "stage_code": "OPR",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "增值税小规模纳税人适用3%征收率的应税销售收入，在2027年12月31日前减按1%征收率计算缴纳增值税。申报时将销售额填入减征栏次，系统自动计算税额。",
        "detailed_answer": "3%减按1%是针对小规模纳税人的阶段性优惠政策：适用主体所有增值税小规模纳税人；适用项目为适用3%征收率的应税销售收入；征收率正常3%，目前延续至2027年12月31日。申报表填写：在增值税申报表（小规模纳税人适用）第18栏本期应纳税额减征额=销售额x2%，在第22栏本期应补退税额=销售额x1%-已预缴税额。发票开具：开具1%征收率的增值税发票，受票方可按1%抵扣进项（普票不可抵）。",
        "core_definition": "3%减按1%是征收率优惠，小规模纳税人申报时自动适用，不需额外申请。",
        "applicable_conditions": "小规模纳税人；征收品目为3%征收率；属于应税销售收入；开票征收率为1%",
        "exceptions_boundary": "5%征收率的项目不适用1%优惠；已开具3%税率发票需作废重开为1%才能享受优惠",
        "practical_steps": "1.确认开票项目属于3%征收率范围；2.开具1%征收率的发票；3.申报时在第18栏填入减征额（销售额x2%）；4.季度汇总申报，销售额合计仍享受月10万/季度30万免税政策",
        "risk_warning": "开票税率与申报表填写必须一致；如开具3%税率发票则不能享受1%优惠，需作废或红字冲销后重新开具",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_clear",
        "keywords": "小规模纳税人,3%减按1%,征收率优惠,增值税申报",
        "high_frequency_flag": 1,
        "newbie_flag": 1,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-009", "support_type": "support_direct", "support_note": "小规模纳税人3%征收率减按1%征收，执行至2027年"},
            {"policy_code": "POL-PREF-002", "support_type": "support_aux", "support_note": "小规模纳税人免税条件与3%减按1%优惠可同时适用"},
        ],
    },
]

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    q_added = 0
    q_skipped = 0
    for q in QUESTIONS:
        policies = q.pop("policies")
        try:
            cols = list(q.keys())
            vals = list(q.values())
            placeholders = ",".join(["?"] * len(cols))
            cur.execute(f"INSERT INTO question_master ({','.join(cols)}) VALUES ({placeholders})", vals)
            qid = cur.lastrowid
            for pol in policies:
                cur.execute("SELECT id FROM policy_basis WHERE policy_code=?", (pol["policy_code"],))
                pid_row = cur.fetchone()
                if pid_row:
                    cur.execute("""
                        INSERT INTO question_policy_link (question_id, policy_id, support_type, support_note)
                        VALUES (?, ?, ?, ?)
                    """, (qid, pid_row[0], pol["support_type"], pol["support_note"]))
            q_added += 1
            print(f"  + {q['question_code']}  {q['question_title']}")
        except sqlite3.IntegrityError:
            q_skipped += 1
            print(f"  ~ {q['question_code']} 已存在，跳过")
    conn.commit()
    total_q = cur.execute("SELECT COUNT(*) FROM question_master WHERE status='active'").fetchone()[0]
    total_p = cur.execute("SELECT COUNT(*) FROM policy_basis").fetchone()[0]
    pref_q = cur.execute("SELECT COUNT(*) FROM question_master WHERE status='active' AND module_code='PREF'").fetchone()[0]
    print(f"\n完成：新增 {q_added} 条，跳过 {q_skipped} 条；问题库共 {total_q} 条，PREF模块 {pref_q} 条，政策库 {total_p} 条")
    conn.close()

if __name__ == "__main__":
    main()
