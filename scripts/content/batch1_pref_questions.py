#!/usr/bin/env python3
"""批量导入PREF税收优惠模块第一批问题（5条）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.config import DB_PATH
import sqlite3

QUESTIONS = [
    {
        "question_code": "OPR-PREF-001",
        "question_title": "小规模纳税人免税政策适用条件是什么？",
        "question_plain": "小规模纳税人免税政策适用条件是什么",
        "stage_code": "OPR",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "月销售额≤10万元（季度≤30万元）的增值税小规模纳税人，免征增值税；3%征收率的销售，减按1%征收。",
        "detailed_answer": "免税条件按月或按季度判定，以1个月或1个季度为纳税期限的小规模纳税人，月销售额未超过10万元（季度未超过30万元）的，免征增值税。注意：若扣除本期发生的销售不动产后的月销售额不超过10万元，则不动产以外的销售仍可享受免税。适用3%征收率的销售收入，减按1%征收率计算缴纳增值税。",
        "core_definition": "小规模纳税人免税是增值税优惠政策，按月判定月销售额是否≤10万元，或按季度判定是否≤30万元。免税适用于所有行业的小规模纳税人。",
        "applicable_conditions": "增值税小规模纳税人；月销售额≤10万元或季度≤30万元；取得的是增值税应税收入",
        "exceptions_boundary": "扣除销售不动产后的金额才超过10万元的，不影响免税资格；超出免税限额的全额缴税，而非仅就超出部分缴税",
        "practical_steps": "1.确认是否为小规模纳税人（年应征增值税销售额≤500万元）；2.按月或季度统计销售额；3.在电子税务局填写增值税申报表时自动享受免税",
        "risk_warning": "季度中间超标准（如季度中途转一般纳税人）需按实际销售天数分段计算免税额度",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_clear",
        "keywords": "小规模纳税人,免税,月销售额10万,季度30万,增值税优惠",
        "high_frequency_flag": 1,
        "newbie_flag": 1,
        "status": "active",
        # 政策链接
        "policies": [
            {"policy_code": "POL-PREF-009", "support_type": "support_direct", "support_note": "月销售额10万元以下免征增值税，减按1%征收率"},
            {"policy_code": "POL-PREF-002", "support_type": "support_aux", "support_note": "小规模纳税人月销售额10万以下免征增值税"},
        ],
    },
    {
        "question_code": "OPR-PREF-002",
        "question_title": "小微企业所得税优惠的适用条件是什么？",
        "question_plain": "小微企业所得税优惠适用条件",
        "stage_code": "OPR",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "同时满足：从业人数≤300人、资产总额≤5000万元、年应纳税所得额≤300万元的企业，减按20%税率征税；≤100万元部分再减半，实际税负2.5%。",
        "detailed_answer": "小型微利企业需同时满足三个条件：①从业人数不超过300人（从业人数，包括与企业建立劳动关系的职工人数和企业接受的劳务派遣用工人数）；②资产总额不超过5000万元；③年应纳税所得额不超过300万元。优惠计算方式：年应纳税所得额≤100万元部分，减按25%计入应税所得，税率20%（税负2.5%）；100万~300万元部分，减按50%计入，税率20%（税负10%）。",
        "core_definition": "小型微利企业是同时满足人数、资产、所得三个条件的企业，可享受低税率优惠。",
        "applicable_conditions": "从业人数≤300人；资产总额≤5000万元；年应纳税所得额≤300万元；从事国家非限制和禁止行业",
        "exceptions_boundary": "非居民企业不适用；机关事业单位等不在经营范围内的主体不适用；查账征收企业才可享受，定额征收企业需先转为查账征收",
        "practical_steps": "1.每年季度预缴时在电子税务局填报从业人数和资产总额；2.年度汇算清缴时确认三项指标均符合条件；3.系统自动计算优惠税额",
        "risk_warning": "从业人数和资产总额按季度平均值计算，季中途变化需加权平均；超标准后当年不能享受优惠",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_conditional",
        "keywords": "小型微利企业,企业所得税优惠,从业人数,资产总额,年应纳税所得额300万",
        "high_frequency_flag": 1,
        "newbie_flag": 1,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-001", "support_type": "support_direct", "support_note": "小型微利企业年应纳税所得额≤100万减按25%，税率20%；超过100万不超过300万减按50%"},
            {"policy_code": "POL-PREF-003", "support_type": "support_direct", "support_note": "≤100万部分再减半，实际税负约2.5%，执行至2027年"},
        ],
    },
    {
        "question_code": "SET-PREF-001",
        "question_title": "新设立企业可以享受哪些税收优惠？",
        "question_plain": "新公司设立税收优惠有哪些",
        "stage_code": "SET",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "新设企业常见优惠：小规模纳税人月销售额≤10万元免增值税；小微企税优惠（需满足条件后次年开始享受）；部分行业（高新/软件/集成电路）可申请认定后享受优惠税率。",
        "detailed_answer": "新设企业在设立初期可享受的优惠分三类：①增值税优惠：新设首月即为小规模纳税人，月销售额≤10万元免征增值税，3%征收率减按1%征收（2027年前）；②企业所得税优惠：需先有应税所得，小型微利企业满足条件后（从业人数≤300人、资产≤5000万、所得≤300万）享受优惠税率；③行业性优惠：高新技术企业和软件企业可在盈利年度起享受15%优惠税率或两免三减半，需要提前向科技部门申请认定。",
        "core_definition": "新设企业税收优惠主要分为普惠性（小规模免税+小微优惠，需满足条件）和行业性（高新/软件，需认定）两类。",
        "applicable_conditions": "小规模纳税人免税无行业限制；小微企业所得税优惠需满足三项条件；高新/软件企业优惠需经认定",
        "exceptions_boundary": "新设企业首年若为小规模纳税人即自动享受增值税优惠，无需申请；企业所得优惠需等有盈利后才能享受；高新认定需投入一定研发费用并满足人员比例要求",
        "practical_steps": "1.设立首月确认税种认定（小规模还是一般纳税人）；2.季报时关注销售额是否在免税额度内；3.如有研发计划，提前规划高新认定路径",
        "risk_warning": "小规模纳税人转为一般纳税人后，当年即不可再享受小规模免税政策；高新/软件认定周期通常需要6~12个月",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_conditional",
        "keywords": "新设企业,税收优惠,小规模纳税人,小微优惠,高新企业,软件企业",
        "high_frequency_flag": 1,
        "newbie_flag": 1,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-002", "support_type": "support_direct", "support_note": "小规模纳税人月销售10万以下免增值税"},
            {"policy_code": "POL-PREF-001", "support_type": "support_direct", "support_note": "小微企业所得税优惠条件与计算方式"},
            {"policy_code": "POL-PREF-006", "support_type": "support_aux", "support_note": "高新企业认定后可享受15%优惠税率"},
            {"policy_code": "POL-PREF-010", "support_type": "support_aux", "support_note": "软件企业盈利年度起享受两免三减半"},
        ],
    },
    {
        "question_code": "OPR-PREF-003",
        "question_title": "研发费用加计扣除的适用范围是什么？",
        "question_plain": "研发费用加计扣除适用范围条件",
        "stage_code": "OPR",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "企业为获得科学与技术新知识或改进生产工艺而进行的研发活动，所产生的费用可按实际发生额的100%在税前加计扣除（制造业已提升至100%，其他行业维持100%）。",
        "detailed_answer": "研发费用加计扣除适用于企业开展的研发活动，判定标准是：①有明确创新目标（获得新知识/改进质量/新技术/新服务）；②有系统性（属于公司核心业务，非零散项目）；③结果不确定性（无法预先判断最终是否成功）。适用主体：在中国境内注册的居民企业（不包括个人独资和合伙企业）。扣除比例：制造业企业按研发费用的100%加计扣除（2023年起）；其他行业按75%~100%执行（分年度政策延续）。可加计扣除的费用包括：人员人工、直接投入、折旧费用、无形资产摊销、新药临床试验等。",
        "core_definition": "研发费用加计扣除是对企业真实研发活动的成本加成优惠，按费用发生额的固定比例在税前扣除，减少企业应纳税所得额。",
        "applicable_conditions": "研发活动符合创新性定义；企业为居民企业（非个人独资/合伙）；企业为查账征收；已建立研发辅助账或专账管理",
        "exceptions_boundary": "委托境外研发（可扣三分之二）；不适用税前加计扣除：烟酒制造、房地产、批发零售等行业；已形成无形资产的摊销不重复加计扣除；财政部和国家税务总局规定的其他行业不适用",
        "practical_steps": "1.年初规划研发项目，设立研发辅助账；2.季末归集符合条件的研发费用；3.年度汇算清缴时填报研发费用加计扣除明细表；4.留存研发项目立项文件、辅助账、决算报告备查",
        "risk_warning": "未按规定设辅助账或项目无法证明创新性，税务机关有权要求补税；研发费用与生产费用混同也会导致无法加计扣除",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_conditional",
        "keywords": "研发费用,加计扣除,研发活动,制造业,科技型中小企业",
        "high_frequency_flag": 0,
        "newbie_flag": 0,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-005", "support_type": "support_direct", "support_note": "研发费用按实际发生额100%加计扣除，制造业比例提升"},
        ],
    },
    {
        "question_code": "CHG-PREF-001",
        "question_title": "企业转为一般纳税人后，还能享受之前的小规模免税优惠吗？",
        "question_plain": "一般纳税人还能享受小规模免税吗",
        "stage_code": "CHG",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "转为一般纳税人的当月起，不再适用小规模纳税人免税政策；但经营期间（如季度中途转一般纳税人）原季度免税额度可按实际经营天数分段计算。",
        "detailed_answer": "小规模纳税人免税政策仅适用于小规模纳税人。一旦企业被认定为一般纳税人（或逾期未申请继续作为小规模纳税人），从认定生效当月起，所有增值税应税收入均按一般纳税人税率计算，不再享受月10万元免税额度。特殊情况：如果企业在季度中间申请转为一般纳税人，该季度仍可按小规模纳税人身份享受季度30万元的免税额度，超出部分按实际天数分段计算应纳税额。",
        "core_definition": "纳税人身份决定适用的增值税政策。小规模纳税人身份一旦变更为一般纳税人，原有免税政策从变更生效当月起失效。",
        "applicable_conditions": "季度中途申请转一般纳税人：可分段计算该季度免税额度；全年申请转一般纳税人：从次年起执行一般纳税人规则",
        "exceptions_boundary": "一般纳税人转回小规模纳税人：需满足连续12个月销售额≤500万元的条件，且每个一般纳税人只有一次机会转回",
        "practical_steps": "1.确认转一般纳税人的生效时间（通常次月生效）；2.若季度中途转，准备好各月销售额台账；3.转一般纳税人后及时调整发票类型（专票/普票）和申报方式",
        "risk_warning": "未及时了解转一般纳税人时间节点，可能导致当月销售额被全额计税；转一般纳税人前的进项税额若未及时认证，将无法抵扣",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_clear",
        "keywords": "一般纳税人,小规模纳税人,转一般纳税人,免税政策失效,身份变更",
        "high_frequency_flag": 0,
        "newbie_flag": 1,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-009", "support_type": "support_direct", "support_note": "小规模纳税人免税条件及适用身份限制"},
            {"policy_code": "SAT-VAT-002", "support_type": "support_aux", "support_note": "一般纳税人登记的时间条件和生效规则"},
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
                    print(f"    -> 链接 {pol['policy_code']} ({pol['support_type']})")
            q_added += 1
            print(f"  + {q['question_code']}  {q['question_title']}")
        except sqlite3.IntegrityError as e:
            q_skipped += 1
            print(f"  ~ {q['question_code']} 已存在，跳过")
    conn.commit()
    total_q = cur.execute("SELECT COUNT(*) FROM question_master WHERE status='active'").fetchone()[0]
    total_p = cur.execute("SELECT COUNT(*) FROM policy_basis").fetchone()[0]
    print(f"\n完成：新增 {q_added} 条问题，跳过 {q_skipped} 条；问题库共 {total_q} 条，政策库 {total_p} 条")
    conn.close()

if __name__ == "__main__":
    main()
