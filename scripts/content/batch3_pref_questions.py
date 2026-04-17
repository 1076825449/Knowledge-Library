#!/usr/bin/env python3
"""批量导入PREF税收优惠模块第三批问题（5条）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.config import DB_PATH
import sqlite3

QUESTIONS = [
    {
        "question_code": "CHG-PREF-001",
        "question_title": "小微企业享受优惠后，企业所得税年度申报如何填报？",
        "question_plain": "小微企业所得税优惠年度申报表填报",
        "stage_code": "CHG",
        "module_code": "PREF",
        "question_type": "type_procedure",
        "one_line_answer": "小微企业在年度汇算清缴时，通过填写企税年度申报表中的资产总额、从业人数和应纳税所得额，系统自动计算减免税额，无需单独申请。",
        "detailed_answer": "小微企业所得税优惠采用自行判别、申报享受、留存备查的方式。年度汇算清缴时填报主表和减免所得税优惠明细表，系统自动计算减免税额。留存备查资料包括：从业人数和资产总额相关季度波动说明、工资发放凭证、社保缴纳记录等。",
        "core_definition": "小微企业所得税优惠在年度汇算清缴时通过申报表自动计算享受，不需要前置审批，但需要留存备查资料。",
        "applicable_conditions": "同时满足从业人数不超过300人、资产总额不超过5000万元、年应纳税所得额不超过300万元的条件；查账征收企业",
        "exceptions_boundary": "核定征收企业需先转为查账征收才能享受；超过人数或资产总额限制则全年不得享受优惠",
        "practical_steps": "1.年底统计全年平均从业人数和资产总额；2.次年5月31日前完成年度汇算清缴；3.填报企业所得税年度纳税申报表相关行次；4.留存从业人数、资产、社保等备查资料",
        "risk_warning": "年度中间不符合条件（如中间扩招超过300人），当年全年不得享受优惠，需进行更正申报",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_clear",
        "keywords": "小微企业所得税,年度汇算清缴,申报表填报,减免所得税",
        "high_frequency_flag": 1,
        "newbie_flag": 1,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-001", "support_type": "support_direct", "support_note": "小微企业所得税优惠的计算方式和条件"},
            {"policy_code": "POL-PREF-003", "support_type": "support_direct", "support_note": "不超过100万部分再减半，执行至2027年"},
        ],
    },
    {
        "question_code": "OPR-PREF-008",
        "question_title": "企业同时符合高新技术企业和软件企业优惠条件，能否叠加享受？",
        "question_plain": "高新企业和软件企业优惠能否叠加",
        "stage_code": "OPR",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "不可以叠加享受。高新企业15%优惠税率和软件企业两免三减半属于同税种的同类优惠，企业须在年度汇算清缴时择一适用，但研发费用加计扣除可叠加使用。",
        "detailed_answer": "税收优惠政策叠加规则：同一税种、同一性质（税率式减免）的优惠不可叠加，但不同类型的优惠可以叠加。不可叠加：高新产品（服务）收入占企业总收入不低于60%的企业所得税15%税率优惠，与软件企业两免三减半不可同时享受。可以叠加：研发费用加计扣除（属于税基式减免）与税率式优惠不冲突。企业决策建议：如果企业处于初创期且预计未来几年盈利有限，优先选择两免三减半；如果企业已处于稳定盈利期，选择高新15%优惠更稳定。",
        "core_definition": "企业所得税优惠分为税基式减免（税前加计扣除）和税率式减免（低税率优惠），同类型不可叠加，不同类型可叠加。",
        "applicable_conditions": "同时符合高新企业和软件企业认定条件的企业；在年度汇算清缴前做出选择并填报相应申报表",
        "exceptions_boundary": "软件企业即征即退增值税与高新企业增值税优惠性质不同，可以同时享受",
        "practical_steps": "1.评估企业预期盈利情况；2.在年度汇算清缴前确定适用哪种优惠；3.在相应优惠明细表中二选一填报；4.研发费用加计扣除可叠加填报",
        "risk_warning": "未做选择而填报两种优惠的，税务机关有权要求更正申报；被取消高新或软件企业资格后需补缴优惠差额",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_conditional",
        "keywords": "高新企业优惠,软件企业优惠,企业所得税,叠加享受",
        "high_frequency_flag": 0,
        "newbie_flag": 0,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-006", "support_type": "support_direct", "support_note": "高新企业享受15%优惠税率的条件和认定程序"},
            {"policy_code": "POL-PREF-010", "support_type": "support_direct", "support_note": "软件企业两免三减半优惠条件"},
            {"policy_code": "POL-PREF-005", "support_type": "support_aux", "support_note": "研发费用加计扣除可与税率式优惠叠加"},
        ],
    },
    {
        "question_code": "RSK-PREF-001",
        "question_title": "企业享受税收优惠后被税务机关检查，主要查什么？",
        "question_plain": "税收优惠后续检查主要内容",
        "stage_code": "RSK",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "税务机关核查税收优惠主要关注三点：企业是否符合优惠条件；申报数据与留存备查资料是否一致；是否存在骗取优惠的违法行为。",
        "detailed_answer": "优惠后续管理的主要检查内容：小微企业所得税优惠核查从业人数和资产总额是否全年均符合条件；高新企业优惠核查研发费用占比是否持续达标、高新收入占比是否持续不低于60%、科技人员占比是否持续不低于10%；研发费用加计扣除核查研发费用与生产费用是否混同、辅助账是否按项目分别设置；软件企业优惠核查收入结构是否达标、认定证书是否有效。常见风险点：季报数据与年度汇算数据不一致导致系统预警；辅助账设置不规范导致无法证明研发费用真实性。",
        "core_definition": "税收优惠不是免死金牌，享受优惠后仍需接受后续管理，核心是持续符合优惠条件并保留完整证据链。",
        "applicable_conditions": "所有享受税收优惠的企业均可能被列入检查范围，其中高新、软件、研发费加计扣除为重点关注对象",
        "exceptions_boundary": "主动申请复核或更正申报可降低处罚风险；留存备查资料完整是应对检查的关键",
        "practical_steps": "1.建立优惠享受台账，记录每年享受优惠的金额和条件；2.按年度整理并归档所有留存备查资料；3.收到检查通知后60日内准备资料；4.如有指标波动，提前准备说明材料",
        "risk_warning": "检查发现不符合条件但已享受优惠的，除补缴税款和滞纳金外，还可能处以0.5至5倍罚款；骗税构成犯罪的移交司法机关",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_clear",
        "keywords": "税收优惠检查,后续管理,高新企业检查,留存备查资料",
        "high_frequency_flag": 0,
        "newbie_flag": 0,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-006", "support_type": "support_direct", "support_note": "高新企业认定后的持续符合条件义务和抽查机制"},
            {"policy_code": "POL-PREF-001", "support_type": "support_direct", "support_note": "小微企业所得税优惠的条件核查标准"},
        ],
    },
    {
        "question_code": "OPR-PREF-009",
        "question_title": "个体工商户可以享受哪些增值税和个人所得税优惠？",
        "question_plain": "个体工商户增值税个人所得税优惠",
        "stage_code": "OPR",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "个体工商户可享受的增值税优惠与公司一致（月销售额不超过10万元免征，3%减按1%）；个人所得税方面：2023年1月1日至2027年12月31日，年应纳税所得额不超过200万元的部分，减半征收个人所得税。",
        "detailed_answer": "个体工商户税收优惠分两类：增值税优惠与公司制企业相同：月销售额不超过10万元（季度不超过30万元）免征增值税；3%征收率减按1%征收（执行至2027年）。个人所得税优惠：2023至2027年，年应纳税所得额不超过200万元的部分，减半征收个人所得税，适用5%至35%超额累进税率（经营所得）。计算方式：应税所得乘以适用税率减去速算扣除数后再减半。申报方式：个人所得税经营所得申报表，按季度预缴，年度汇算清缴。",
        "core_definition": "个体工商户在增值税上视同小规模纳税人，在个人所得税上享受单独的减半优惠（200万以内年应税所得额减半）。",
        "applicable_conditions": "增值税：小规模纳税人条件与公司制企业相同；个人所得税：个体工商户业主、个人独资企业投资人、合伙企业个人合伙人",
        "exceptions_boundary": "个体工商户转为一般纳税人后不再享受小规模纳税人增值税优惠；但个人所得税优惠不受纳税人身份影响",
        "practical_steps": "1.确认自身增值税纳税人身份；2.按月或季度申报增值税；3.个人所得税经营所得按季度预缴（5月、7月、10月、12月15日前），次年3月31日前完成年度汇算清缴",
        "risk_warning": "个体工商户与投资人个人账户资金往来需有合法依据，否则可能被认定为偷税",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_clear",
        "keywords": "个体工商户,增值税优惠,个人所得税优惠,经营所得",
        "high_frequency_flag": 1,
        "newbie_flag": 1,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-009", "support_type": "support_direct", "support_note": "小规模纳税人月销售10万以下免征增值税，个体工商户适用"},
            {"policy_code": "POL-PREF-003", "support_type": "support_direct", "support_note": "个体工商户年应纳税所得额不超过200万部分减半征收个税，执行至2027年"},
        ],
    },
    {
        "question_code": "SET-PREF-003",
        "question_title": "初创期企业如何利用好各项税收优惠政策降低税负？",
        "question_plain": "初创企业税收筹划优惠政策利用",
        "stage_code": "SET",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "初创企业税筹核心三步：首年申请为小规模纳税人（自动享受增值税免税）；有盈利后优先申请软件企业两免三减半（比高新更优惠）；同步规划高新认定路径（3年后接续15%税率）。",
        "detailed_answer": "初创企业税务规划时间轴：设立第1年：确认为小规模纳税人，月销售额不超过10万自动免增值税；3%减按1%优惠（执行至2027年）。第2至3年（如果开始盈利）：如果符合软件企业条件，优先选择两免三减半（前2年免税，后3年12.5%）；同时规划研发项目立项，为研发费加计扣除打基础。第3至5年：申请高新企业认定（认定周期6至12个月），接续软件企业优惠；研发费按100%加计扣除（制造业）。重要原则：初创期企业往往收入不高但支出大，重点用好加计扣除减少应税所得；有盈利后重点关注低税率优惠。",
        "core_definition": "初创企业税筹关键是时间轴规划，在不同发展阶段选择最适合当前情况的优惠政策，形成接力式优惠结构。",
        "applicable_conditions": "各发展阶段有不同侧重：初创无收入阶段用好增值税优惠；开始盈利阶段用好软件或高新低税率；持续投入研发阶段用好研发费加计扣除",
        "exceptions_boundary": "优惠政策均有明确条件限制，不可为了享受优惠而虚构条件；部分优惠需要前置认定，需提前6至12个月布局",
        "practical_steps": "1.设立首月：确认税种认定；2.第1年：建立研发辅助账（即使当期无收入，为未来加计扣除打基础）；3.第2年：评估软件或高新认定可行性；4.每年：季报关注免税额度使用情况",
        "risk_warning": "初创企业常见风险：过早认定一般纳税人丧失免税资格；虚列研发费用骗取加计扣除；未留存备查资料导致优惠被追缴",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_conditional",
        "keywords": "初创企业,税收筹划,小规模纳税人,软件企业,高新企业",
        "high_frequency_flag": 0,
        "newbie_flag": 1,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-002", "support_type": "support_direct", "support_note": "小规模纳税人增值税免税条件，初创企业首年即适用"},
            {"policy_code": "POL-PREF-010", "support_type": "support_direct", "support_note": "软件企业两免三减半，初创企业盈利后首选"},
            {"policy_code": "POL-PREF-006", "support_type": "support_direct", "support_note": "高新企业15%税率，中长期优惠接续方案"},
            {"policy_code": "POL-PREF-005", "support_type": "support_aux", "support_note": "研发费用加计扣除贯穿全程"},
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
    print(f"完成：新增 {q_added} 条，跳过 {q_skipped} 条；问题库共 {total_q} 条，PREF模块 {pref_q} 条，政策库 {total_p} 条")
    conn.close()

if __name__ == "__main__":
    main()
