#!/usr/bin/env python3
"""批量导入PREF税收优惠模块第四批问题（6条，冲刺20条目标）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.config import DB_PATH
import sqlite3

QUESTIONS = [
    {
        "question_code": "OPR-PREF-010",
        "question_title": "企业年度研发费用加计扣除如何归集？哪些费用可以计入？",
        "question_plain": "研发费用加计扣除归集范围哪些费用可以计入",
        "stage_code": "OPR",
        "module_code": "PREF",
        "question_type": "type_procedure",
        "one_line_answer": "研发费用包括：人员人工费用（研发人员工资社保）、直接投入费用（材料燃料动力）、折旧费用、无形资产摊销、新药临床试验费等六大类。与生产费用混同的不得计入，需单独设置研发辅助账。",
        "detailed_answer": "研发费用归集范围（依据财企〔2007〕194号等文件）：①人员人工费用：企业在职研发人员的工资、奖金、津贴、补贴、社会保险费、住房公积金等，当年逗留时间占企业正常工作时间不少于80%的研发人员；②直接投入费用：研发活动直接消耗的材料、燃料和动力费用；用于中间试验和产品试制的模具、工艺装备开发及制造费等；③折旧费用和长期待摊费用：用于研发活动的仪器、设备、厂房的折旧费；④无形资产摊销：用于研发活动的软件、专利权、非专利技术等无形资产的摊销费；⑤新产品设计费等；⑥其他相关费用：技术图书资料费、资料翻译费、专家咨询费、高新科技研发保险费等。加计扣除计算基数：自主研发项目费用=费用合计乘以(1-其他相关费用比例除以10%)；委托研发费用按80%计入基数。",
        "core_definition": "研发费用加计扣除的关键是准确归集到具体研发项目，研发辅助账必须按项目设置，与生产费用严格区分。",
        "applicable_conditions": "会计核算健全、实行查账征收的居民企业；研发活动符合创新性定义；有规范设置的研发辅助账",
        "exceptions_boundary": "与生产经营共享的设备（未单独核算）不得计入；知识产权摊销年限低于规定年限的不得全额计入；福利费工会经费职工教育经费不得计入研发费用",
        "practical_steps": "1.年初建立研发项目清单；2.每月按项目归集研发费用；3.季末核对辅助账，确保与财务账一致；4.年度汇算清缴时填报研发费用加计扣除明细表",
        "risk_warning": "未单独设研发辅助账是最大风险点；税务机关有权要求提供项目计划书、决算报告等证明材料",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_conditional",
        "keywords": "研发费用归集,研发辅助账,人员人工费用,直接投入,折旧费用",
        "high_frequency_flag": 0,
        "newbie_flag": 0,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-005", "support_type": "support_direct", "support_note": "研发费用按实际发生额100%加计扣除的归集范围和计算方式"},
        ],
    },
    {
        "question_code": "OPR-PREF-011",
        "question_title": "小规模纳税人季度销售额超过30万元免税额度，如何计算应纳税额？",
        "question_plain": "小规模纳税人季度超30万免税计算",
        "stage_code": "OPR",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "小规模纳税人季度免税额度为30万元。超过30万元的，全额按1%征收率计算应纳税额（不再仅对超出部分征税）。免税额度按未扣除不动产销售的金额判定。",
        "detailed_answer": "小规模纳税人增值税免税计算规则：适用对象：增值税小规模纳税人，以1个季度为纳税期限的；免税额度：季度销售额（未扣除不动产销售）不超过30万元；免税范围：开具普通发票和未开具发票的销售部分免税，开具增值税专用发票部分需全额缴税（因为专票购方要抵扣）。计算示例：假设季度销售额35万元（其中：开具普通发票20万元，开具专用发票15万元）：免税销售额=20万元（普通发票）；应纳税销售额=15万元（专用发票）；应纳税额=15万元乘以1%=1500元。注意：不动产销售无论金额多少均不计入免税额度，但扣除不动产后的销售额不超过10万元的，不动产以外的销售仍可享受免税。",
        "core_definition": "小规模纳税人免税是对销售额度的整体判断，超过30万后全额按优惠征收率1%缴税，而非仅就超出部分缴税。",
        "applicable_conditions": "小规模纳税人；季度销售额超过免税额度；开具的是1%征收率发票",
        "exceptions_boundary": "开具3%征收率专票的，超额后按3%全额计算而非1%；不动产销售不占用小规模免税额度",
        "practical_steps": "1.季度末统计三类销售额：普通发票、专用发票、未开票收入；2.判断是否超过30万；3.计算应纳税额=专用发票销售额乘以征收率；4.填写增值税申报表小规模纳税人适用第11行（本期应征增值税销售额）和第18行（减征额）",
        "risk_warning": "错将专票销售额填入免税栏次会导致偷税；季报数据与年度汇算数据不一致会触发风险预警",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_clear",
        "keywords": "小规模纳税人,季度免税,30万,专用发票,增值税申报",
        "high_frequency_flag": 1,
        "newbie_flag": 1,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-009", "support_type": "support_direct", "support_note": "小规模纳税人季度30万免税的判定和计算方式"},
            {"policy_code": "POL-PREF-002", "support_type": "support_aux", "support_note": "小规模纳税人免税条件的具体规定"},
        ],
    },
    {
        "question_code": "CHG-PREF-002",
        "question_title": "企业年度中间转为一般纳税人后，研发费用加计扣除还能继续享受吗？",
        "question_plain": "一般纳税人研发费用加计扣除政策",
        "stage_code": "CHG",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "可以。一般纳税人转为一般纳税人后，研发费用加计扣除政策不受纳税人身份影响，只要研发活动真实、费用归集规范即可继续享受，与增值税纳税人身份无关。",
        "detailed_answer": "研发费用加计扣除的适用条件是企业类型（居民企业）、研发活动性质（创新性）、会计核算方式（查账征收），与增值税纳税人身份无关。转为一般纳税人后：①可以继续加计扣除的研发费用：为认定为一般纳税人之前已立项的研发项目所发生的费用，只要在研发项目结束前（即研发费用发生起36个月内）均可以计入加计扣除基数；②新增研发项目：认定为一般纳税人后立项的新研发项目，费用按正常口径计入基数；③计算方式不变：制造业按研发费用的100%加计扣除，其他行业按75%至100%不等。注意事项：当年转为一般纳税人的，研发费用加计扣除与当年应税收入挂钩，若当年应税收入为0或亏损，加计扣除无法在当年全额使用，可依法向后无限期结转。",
        "core_definition": "研发费用加计扣除是企业所得税优惠政策，与增值税纳税人身份无关。一般纳税人只要有应税所得并符合研发活动标准，即可享受。",
        "applicable_conditions": "企业为居民企业；研发活动符合规定；实行查账征收；有规范的研发辅助账",
        "exceptions_boundary": "亏损企业享受加计扣除后形成更大的亏损，但该亏损可无限期向后结转",
        "practical_steps": "1.保留研发项目立项文件；2.按月归集各研发项目费用；3.年度汇算清缴时填报研发费用加计扣除明细表；4.结转的加计扣除在亏损产生年份向后抵扣",
        "risk_warning": "研发项目立项文件不完整会导致加计扣除不被认可；项目周期超过36个月部分不可计入基数",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_clear",
        "keywords": "一般纳税人,研发费用加计扣除,企业所得税优惠,亏损结转",
        "high_frequency_flag": 0,
        "newbie_flag": 0,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-005", "support_type": "support_direct", "support_note": "研发费用加计扣除的条件和计算，与纳税人身份无关"},
        ],
    },
    {
        "question_code": "OPR-PREF-012",
        "question_title": "小微企业和小型微利企业是一回事吗？分别指什么？",
        "question_plain": "小微企业和小型微利企业区别",
        "stage_code": "OPR",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "不是一回事。小微企业是增值税概念，指月销售额10万元以下或季度30万元以下的小规模纳税人；小型微利企业是企税概念，指同时满足从业人数不超过300人、资产总额不超过5000万元、年应纳税所得额不超过300万元的企业。两者分别对应不同税种的优惠政策。",
        "detailed_answer": "两个概念的区别：①小微企业（增值税概念）：增值税语境下的小微企业，是指增值税小规模纳税人中月销售额或季度销售额在规定限额内的纳税人，享受增值税免税优惠政策。判断标准：增值税应税销售额不超过规定限额（小规模纳税人免税额度）。②小型微利企业（企业所得税概念）：企税语境下的小型微利企业，是同时满足三个条件的企业：从业人数不超过300人、资产总额不超过5000万元、年应纳税所得额不超过300万元，享受企业所得税低税率优惠。判断标准：三个条件同时满足。两者关系：可以重叠（既是小规模纳税人又是小型微利企业，如初创小微企业），也可以不重叠（是一般纳税人但同时是从业人数少于300人的小型微利企业）。",
        "core_definition": "小微企业是增值税免税政策的适用主体，小型微利企业是企业所得税低税率优惠的适用主体，两者适用税种、判断标准均不同，但可重叠。",
        "applicable_conditions": "小微企业：小规模纳税人，月销售额或季度销售额在限额内；小型微利企业：同时满足三个财务指标条件的居民企业",
        "exceptions_boundary": "个体工商户可以是小微企业但不是小型微利企业（个税有单独优惠）；合伙企业不是企业所得税纳税人，不适用小型微利企业优惠",
        "practical_steps": "1.先确认纳税人身份（小规模还是一般纳税人）；2.小规模纳税人：确认季度销售额是否在30万以内；3.查账征收企业：评估三个财务指标是否同时满足；4.年度申报时根据实际情况享受对应优惠",
        "risk_warning": "混淆两个概念会导致申报表填写错误；将一般纳税人填入小微企业免税栏次会构成偷税",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_clear",
        "keywords": "小微企业,小型微利企业,增值税免税,企业所得税优惠,从业人数,资产总额",
        "high_frequency_flag": 1,
        "newbie_flag": 1,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-002", "support_type": "support_direct", "support_note": "小规模纳税人免税条件（小微企业）"},
            {"policy_code": "POL-PREF-001", "support_type": "support_direct", "support_note": "小型微利企业的三个判断标准和优惠计算方式"},
        ],
    },
    {
        "question_code": "RSK-PREF-002",
        "question_title": "企业被取消高新企业资格后，需要补缴多少税款？",
        "question_plain": "高新企业资格取消补税计算",
        "stage_code": "RSK",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "被取消高新资格的企业，需要补缴已减免的企业所得税差额。计算方式：应补缴=当期实际享受的优惠税额-(按25%法定税率计算的应纳税额-实际已缴税额)。被取消资格后年度起不再享受15%优惠税率。",
        "detailed_answer": "高新企业资格被取消后的税务处理：补税范围：被取消资格当年及后续年度（如已享受优惠）均需按25%法定税率重新计算应纳税额，不足部分需补缴。计算示例：假设某高新企业年度应纳税所得额为1000万元；按高新优惠税率15%计算：应纳税额=1000万乘以15%=150万元；按法定税率25%计算：应纳税额=1000万乘以25%=250万元；应补缴=250万-150万=100万元（不含滞纳金）。滞纳金：从滞纳之日起，按日加收万分之五滞纳金（年化约18.25%）。影响：被取消高新资格后，企业自被取消年度起连续5年内（复审合格前）不得再次申请高新认定。情节严重的，还可能被处以罚款并通报。",
        "core_definition": "高新企业被取消资格后，需要补缴15%与25%税率之间的差额，并加收滞纳金，情节严重可加处罚款。",
        "applicable_conditions": "被取消高新企业资格且在有效期内享受过优惠的所有年度",
        "exceptions_boundary": "主动补缴并提供合理解释的，可从轻或减轻处罚；被税务机关认定为恶意骗税的，除补税滞纳金外还将面临0.5至5倍罚款",
        "practical_steps": "1.收到取消资格通知后，确认被取消的年度范围；2.逐年度计算应补缴税额（按25%法定税率重新计算）；3.向主管税务机关提交更正申报；4.按时缴纳本金和滞纳金，避免进入强制执行程序",
        "risk_warning": "超过缴款期限未缴纳的，将按日加收万分之五滞纳金；抗拒不缴的，可能被强制执行或移交强制执行程序",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_clear",
        "keywords": "高新企业资格取消,补缴税款,滞纳金,15%税率,25%法定税率",
        "high_frequency_flag": 0,
        "newbie_flag": 0,
        "status": "active",
        "policies": [
            {"policy_code": "POL-PREF-006", "support_type": "support_direct", "support_note": "高新企业认定后的持续符合条件和取消资格后的处理"},
        ],
    },
    {
        "question_code": "SUS-PREF-001",
        "question_title": "企业停业期间是否还需要申报纳税？",
        "question_plain": "停业期间纳税申报义务",
        "stage_code": "SUS",
        "module_code": "PREF",
        "question_type": "type_define",
        "one_line_answer": "需要。办理停业登记的企业，在停业期间发生纳税义务的（如购置资产产生增值税进项、有租金收入等），应当向主管税务机关申报纳税。未发生纳税义务的，也应进行零申报。",
        "detailed_answer": "停业期间纳税申报规定：需要申报的情形：停业期间发生应税销售或购置资产取得发票的；取得投资收益、租金收入、特许权使用费收入的；为员工发放工资并代扣个人所得税的。申报方式：已认定税费种的企业，无论是否有收入，都应在征期内进行申报；无收入的进行零申报（填写申报表，销售额填0）；未申报将导致逾期未申报记录，影响企业纳税信用评分。停业不等于免税：停业只是税务登记状态的暂停，不等于税收义务的免除。没有收入也要按期申报，否则系统会将其标记为非正常户。复业后：持《复业单》向主管税务机关办理复业登记，领取或验旧发票，恢复正常申报状态。",
        "core_definition": "停业期间税务申报不中断。企业即使办了停业登记，仍须在征期内进行零申报或实际申报，否则影响纳税信用并可能被认定为非正常户。",
        "applicable_conditions": "已办理停业登记（定期定额征收的个体工商户）的企业；停业期间发生纳税义务的企业",
        "exceptions_boundary": "查账征收企业停业期间只要无收入即可零申报，无需办理停业登记；定期定额户不申报才会被转为非正常户",
        "practical_steps": "1.办理停业登记后，确认已认定的税费种及征期；2.每月1-15日（征期）在电子税务局进行申报；3.无收入的填写零申报；4.停业结束后及时办理复业，领取发票",
        "risk_warning": "停业期间连续三个月零申报可能触发风险预警；长期停业不申报将被转为非正常户，影响企业信用",
        "scope_level": "scope_national",
        "local_region": "",
        "answer_certainty": "certain_clear",
        "keywords": "停业登记,零申报,纳税申报,复业,非正常户",
        "high_frequency_flag": 0,
        "newbie_flag": 1,
        "status": "active",
        "policies": [
            {"policy_code": "POL-SUS-001", "support_type": "support_direct", "support_note": "定期定额户停业期间发生纳税义务应当申报纳税"},
            {"policy_code": "GOV-Tax-001", "support_type": "support_aux", "support_note": "纳税人停业期间仍需履行申报义务的法律依据"},
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
