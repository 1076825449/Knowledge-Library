#!/usr/bin/env python3
# ============================================================
# scripts/content/backfill_structured_fields_batch1.py
# 第一批结构字段补强：补适用条件/边界/步骤/风险
# 用法: python scripts/content/backfill_structured_fields_batch1.py [--dry-run]
# ============================================================

import os
import sqlite3
import sys
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'db', 'tax_knowledge.db')

UPDATES = {
    "CLS-DEC-001": {
        "applicable_conditions": "适用于企业已经进入注销、简易注销、清税注销或实质清算阶段，且名下仍存在已认定税费种、申报义务或历史欠报事项的情形。",
        "exceptions_boundary": "如果企业自设立以来一直未实际经营、未领票、未发生应税行为，部分地区可能允许在核实后按简化路径处理；但是否可以不做完整申报，仍要以主管税务机关核验结果为准，不能自行认定。",
        "practical_steps": "步骤1：登录电子税务局或到主管税务机关查询名下全部税费种和未办结事项\n步骤2：逐项补齐当期及历史所属期申报，包括增值税、附加税费、企业所得税、个人所得税、印花税等\n步骤3：核对是否存在欠税、滞纳金、罚款、非正常状态、未清票信息\n步骤4：如涉及企业所得税清算，填报清算申报表并结清税款\n步骤5：确认系统中无待申报、无欠税、无未办结事项后，再申请清税注销",
        "risk_warning": "遗漏任何一个已认定税费种的申报，都可能导致清税审核被退回；历史欠报、欠税、未清票问题未处理完就贸然申请注销，往往会重复跑流程，延长注销周期。",
    },
    "CLS-REG-001": {
        "applicable_conditions": "适用于企业已经决定终止经营，需要同步办理税务注销、发票缴销、税控设备清理和市场监管注销的情形。",
        "exceptions_boundary": "简易注销并不等于免除清税要求。即使走简易注销路径，只要仍有欠税、未申报、未缴销发票、未清理税控设备、未办结稽查或风险事项，通常仍不能直接完成注销。",
        "practical_steps": "步骤1：先核对企业名下税费申报、欠税、发票、税控设备和异常事项\n步骤2：办理清税，结清税款、滞纳金和罚款\n步骤3：缴销空白发票、完成税控设备注销或交回\n步骤4：取得清税证明或系统清税结果\n步骤5：再向市场监管部门或注销一体化平台申请工商注销",
        "risk_warning": "如果先走工商注销而税务事项未结清，往往会造成流程卡住或反复补件；发票和税控设备未清理完，也容易成为注销被退回的高频原因。",
    },
    "SUS-REG-001": {
        "applicable_conditions": "适用于企业已经依法办理停业、歇业或阶段性停业手续，且停业期间仍保留纳税人主体资格的情形。",
        "exceptions_boundary": "停业不等于税务关系终止。若停业期间实际发生销售、工资发放、代扣代缴、资产处置等事项，不能简单按零申报处理；已经进入注销、非正常户或其他特殊状态的，也要按对应规则判断。",
        "practical_steps": "步骤1：确认停业手续是否已被主管税务机关受理并在系统中生效\n步骤2：核对停业期间名下仍保留哪些税费种和申报义务\n步骤3：无经营、无应税行为时按期办理零申报\n步骤4：如发生工资发放、发票处理、资产处置等业务，按实际情况据实申报\n步骤5：定期检查电子税务局消息、待办事项和异常提醒，避免漏报",
        "risk_warning": "把停业理解成“什么都不用报”是高频误区。停业期间漏报，仍可能产生逾期申报记录、罚款、滞纳金，严重时还会引发非正常户风险。",
    },
    "SUS-PREF-001": {
        "applicable_conditions": "适用于企业原本享受即征即退、先征后退等与持续经营和实际业务发生密切相关的优惠，但在停业期间基本停止经营活动的情形。",
        "exceptions_boundary": "不同优惠政策的适用条件并不完全相同。是否在停业期间一律不能享受，还要看该优惠是否以实际销售、实际缴税、持续经营资格或专项备案为前提；地方执行口径也可能存在差异。",
        "practical_steps": "步骤1：先确认所享受的优惠类型是即征即退、先征后退还是其他减免优惠\n步骤2：查看该优惠是否要求企业处于正常经营、正常申报、持续备案状态\n步骤3：停业期间如仍发生纳税义务，先按正常规则申报并保留资料\n步骤4：恢复经营后重新核对是否仍满足优惠条件，必要时重新备案或重新申请\n步骤5：对停业期间取得的进项、退税、补贴等事项单独留痕，避免与恢复经营后的业务混同",
        "risk_warning": "在停业状态下继续按原经营期口径机械享受优惠，容易被认定为适用条件不符；一旦被追溯调整，不仅要补税，还可能影响后续优惠资格和纳税信用。",
    },
    "OPR-CIT-013": {
        "applicable_conditions": "适用于居民企业准备申请高新技术企业资格，或者已取得资格后准备继续适用15%优惠税率的情形。通常需要同时满足核心知识产权、研发投入比例、高新技术产品（服务）收入占比、科技人员占比等条件。",
        "exceptions_boundary": "高新技术企业资格不是取得一次就永久有效。资格有效期届满后需要重新认定；有效期内如果关键条件已明显不再满足，也可能被取消资格并追补税款。单纯拥有软件著作权或专利，并不当然等于能享受优惠。",
        "practical_steps": "步骤1：先核对企业所属行业是否属于国家重点支持的高新技术领域\n步骤2：梳理核心知识产权、研发项目、研发人员和研发费用归集口径\n步骤3：测算近三年研发费用占比、高新收入占比、科技人员占比是否达标\n步骤4：按认定要求准备专项审计、知识产权、成果转化、组织管理等材料\n步骤5：认定通过后，在企业所得税汇算清缴中按15%税率申报，并持续留存备查资料",
        "risk_warning": "研发费用归集不规范、高新收入口径错误、知识产权与主营业务关联性不足，都是高频风险点；如果资格取得后不再符合条件却仍按15%税率申报，可能面临补税、滞纳金和资格取消风险。",
    },
    "OPR-CIT-014": {
        "applicable_conditions": "适用于企业实际开展研发活动，并发生与研发项目直接相关的人员人工、直接投入、折旧摊销、无形资产摊销、委托研发等支出的情形。",
        "exceptions_boundary": "并非所有技术改良、日常测试、售后维护、常规升级都属于可加计扣除的研发活动。与生产经营直接混同、无法单独归集的支出，通常不能直接按研发费用加计扣除处理。委托研发、资本化研发、财政补助冲减等情形也要分别判断。",
        "practical_steps": "步骤1：先判断相关项目是否属于税法口径下的研发活动\n步骤2：建立研发项目台账，按项目归集人员、材料、折旧、设计试验等费用\n步骤3：区分费用化研发支出与资本化研发支出，核对是否符合加计扣除比例\n步骤4：准备立项资料、过程记录、费用归集底稿和辅助账\n步骤5：在企业所得税预缴或汇算清缴时填报研发费用加计扣除相关表单并留存备查",
        "risk_warning": "把普通生产成本、营销费用、售后支出混入研发费用，是最常见的风险来源；如果归集口径和辅助账不清晰，即使企业真实研发，也可能在检查时被调减加计扣除额。",
    },
    "SET-CLEAR-001": {
        "applicable_conditions": "适用于新设企业虽成立时间不长，但已经进入注销、合并分立、重大资产重组或其他需要对资产负债和所得进行清理的特殊阶段。",
        "exceptions_boundary": "新设企业并不是一定都会发生所得税清算。如果企业始终未实际经营、未发生资产处置、未形成债权债务、且符合简易注销条件，部分地区可能按简化路径办理；但是否免于实质清算，仍要以主管税务机关核实为准。",
        "practical_steps": "步骤1：先判断企业当前属于普通注销、简易注销、合并分立还是重大资产处置\n步骤2：盘点全部资产、负债、费用、损失和未履行合同事项\n步骤3：测算是否形成清算所得，以及以前年度亏损是否可以弥补\n步骤4：如需清算申报，填报企业所得税清算申报表并结清相关税款\n步骤5：完成清税后，再继续办理注销或重组后续程序",
        "risk_warning": "新设企业容易误以为“成立时间短就不用清算”。只要已经发生资产处置、债务清偿、股东收回财产等事项，就可能触发清算税务处理；忽略这一步，往往会导致注销阶段被退回重办。",
    },
    "CLS-FEE-001": {
        "applicable_conditions": "适用于企业在注销前对存货、固定资产、无形资产等进行盘点清理，确实发生报废、毁损、盘亏、无法收回等资产损失，并准备在企业所得税税前扣除的情形。",
        "exceptions_boundary": "不是所有账面减少都当然属于可税前扣除的资产损失。缺少盘点资料、审批资料、责任认定、处置记录或无法证明真实损失的，税前扣除往往会被否定；已抵扣进项税额的货物发生非正常损失时，还要同步判断是否需要做进项税额转出。",
        "practical_steps": "步骤1：对注销前的存货、固定资产、无形资产进行全面盘点，形成清单\n步骤2：区分报废、毁损、盘亏、处置损失等不同情形，测算损失金额\n步骤3：准备盘点表、报废审批、处置资料、责任说明、鉴定材料等备查文件\n步骤4：对涉及增值税进项已抵扣的资产，判断是否需要进项税额转出\n步骤5：在企业所得税申报或清算申报中按规定填报资产损失扣除信息",
        "risk_warning": "注销阶段资产损失金额往往较集中，若证据链不完整，最容易被重点关注；一旦既没有资料支撑又没有同步做增值税处理，可能同时面临企业所得税和增值税两端调整。",
    },
}


def connect_db():
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库文件不存在: {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def main():
    dry_run = "--dry-run" in sys.argv
    conn = connect_db()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for code, fields in UPDATES.items():
        row = conn.execute("""
            SELECT id, version_no
            FROM question_master
            WHERE question_code = ?
        """, (code,)).fetchone()
        if not row:
            print(f"⚠️ 未找到问题: {code}")
            continue

        if dry_run:
            print(f"{code} -> 补 {', '.join(fields.keys())}")
            continue

        new_version = (row["version_no"] or 1) + 1
        conn.execute("""
            UPDATE question_master
            SET applicable_conditions = ?,
                exceptions_boundary = ?,
                practical_steps = ?,
                risk_warning = ?,
                updated_at = ?,
                version_no = ?
            WHERE id = ?
        """, (
            fields["applicable_conditions"],
            fields["exceptions_boundary"],
            fields["practical_steps"],
            fields["risk_warning"],
            now,
            new_version,
            row["id"],
        ))
        conn.execute("""
            INSERT INTO question_update_log (
                question_id, version_no, update_date, update_type,
                update_reason, updated_by, reviewed_by, change_summary
            ) VALUES (?, ?, ?, 'update_revise', ?, ?, ?, ?)
        """, (
            row["id"],
            new_version,
            now,
            "补齐结构字段：适用条件/边界/步骤/风险",
            "system_backfill",
            "",
            f"{code} 补齐结构字段",
        ))
        print(f"✅ 已补强 {code}")

    if not dry_run:
        conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
