#!/usr/bin/env python3
# ============================================================
# scripts/content/backfill_structured_fields_batch18.py
# 第十八批结构字段补强：补适用条件/边界/步骤/风险
# 用法: python scripts/content/backfill_structured_fields_batch18.py [--dry-run]
# ============================================================

import os
import sqlite3
import sys
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, "database", "db", "tax_knowledge.db")

UPDATES = {
    "CLS-TAX-004": {
        "applicable_conditions": "适用于企业注销时仍存在未完结税务稽查、检查或处理决定执行中的案件，需要判断能否先办工商注销及相关风险的情形。",
        "exceptions_boundary": "未完结税务稽查一般会直接影响税务注销，而工商注销与税务清税又强相关。企业不能因为工商端流程可发起，就误以为可以绕过税务案件先彻底退场。",
        "practical_steps": "步骤1：先确认税务案件当前阶段，是立案、审理、处罚还是执行中\n步骤2：核对案件涉及的补税、罚款、担保和对注销的限制条件\n步骤3：与稽查局和主管税务机关同步沟通，明确结案前能否推进其他手续\n步骤4：优先推动案件处理、缴款或依法提供担保，再安排税务注销\n步骤5：避免工商端先行完成导致税务责任和资料链断裂",
        "risk_warning": "企业注销时最大的误区是想先把营业执照退掉再说。税务案件没收完口，后面责任不会消失，只会变得更难处理。",
    },
    "OPR-ETAX-001": {
        "applicable_conditions": "适用于企业首次开通电子税务局网上申报功能，需要进行账号开通、实名认证、权限绑定和首登设置的情形。",
        "exceptions_boundary": "开通网上申报不只是注册一个账号，还包括企业主体认证、办税人员绑定和后续权限配置。不同地区电子税务局入口和认证方式会略有差异。",
        "practical_steps": "步骤1：准备营业执照、法定代表人信息、经办人身份信息和联系方式\n步骤2：通过当地电子税务局完成企业主体注册、实名认证或电子营业执照绑定\n步骤3：绑定办税人员、财务负责人或购票员等角色权限\n步骤4：首次登录后完善基本信息、税费种认定结果和消息提醒设置\n步骤5：做一次申报或查询测试，确认账号和权限已正常可用",
        "risk_warning": "电子税务局开通最容易卡住的不是注册，而是角色权限没配全。主体能登录，不代表办税员就能正常报税或领票。",
    },
    "OPR-TAX-017": {
        "applicable_conditions": "适用于企业收到税务机关《税务约谈通知书》，需要准备资料、明确应对边界并控制约谈风险的情形。",
        "exceptions_boundary": "约谈不等于正式稽查，但也不是普通提醒。企业可以客观说明业务和提供材料，但不能敷衍应对，更不能现场随意作没有证据支持的承认。",
        "practical_steps": "步骤1：先阅读约谈通知书，确认约谈原因、期间、资料要求和时间地点\n步骤2：围绕通知书关注点整理申报表、发票、合同、银行流水和说明材料\n步骤3：内部统一口径，指定熟悉业务和数据的人参加约谈\n步骤4：约谈中如实说明、围绕事实答复，不超范围随意推测\n步骤5：约谈后根据要求补充资料、主动整改或更正申报",
        "risk_warning": "税务约谈最怕的是企业准备不足、多人说法不一致。真正放大风险的，往往不是原问题，而是现场应对失控。",
    },
    "OPR-TAX-019": {
        "applicable_conditions": "适用于企业进行关联申报时，需要区分关联交易类型并理解各类交易应披露内容的情形。",
        "exceptions_boundary": "关联申报不是只填一个总金额。不同类型交易如购销、服务、融资、无形资产和股权往来，披露内容不同，遗漏关键类型会直接影响申报完整性。",
        "practical_steps": "步骤1：先识别全部关联方及其与企业之间的交易类型\n步骤2：按购销、劳务、资金、无形资产、固定资产和股权等分类汇总数据\n步骤3：对各类交易准备金额、定价依据、余额和对方信息等披露要素\n步骤4：在企业所得税汇算时完成关联业务往来报告表填报\n步骤5：同步准备同期资料和独立交易原则支持文件，防止后续抽查",
        "risk_warning": "关联申报最容易出问题的是企业只填最显眼的购销数据，漏掉资金拆借、无形资产或集团服务费这类高风险项目。",
    },
    "OPR-TAX-020": {
        "applicable_conditions": "适用于企业向境外支付服务费、特许权使用费、利息等款项，需要判断代扣代缴增值税和企业所得税以及境内预提处理的情形。",
        "exceptions_boundary": "向境外付款并不都是同一种税务口径。款项性质不同，增值税、企业所得税扣缴和协定待遇适用也不同；不能只按合同名称简单判断。",
        "practical_steps": "步骤1：先明确付款性质是服务费、特许权使用费、利息还是货款\n步骤2：分别判断是否涉及增值税代扣代缴和企业所得税源泉扣缴义务\n步骤3：如拟适用税收协定优惠，提前准备税收居民身份证明和受益所有人资料\n步骤4：在付款前完成税额测算、扣缴申报和留存资料准备\n步骤5：保留合同、付款凭证、完税资料和定性分析底稿，便于后续核查",
        "risk_warning": "跨境付款最容易被低估的是定性错误。合同一旦定性错，后面的增值税、预提所得税和协定待遇都会一起错。",
    },
    "RSK-TAX-011": {
        "applicable_conditions": "适用于企业发现自身存在虚开发票或重大涉税风险苗头，但税务机关尚未正式发现，希望主动自查和补救、争取从轻处理的情形。",
        "exceptions_boundary": "主动补救不等于一定免罚，但在税务机关正式立案前更正、补税、停止违法行为，通常比被动查处更有空间。前提是企业真整改、真补税，不是表面动作。",
        "practical_steps": "步骤1：立即锁定高风险票据、交易和相关期间，停止继续使用问题凭证\n步骤2：内部测算补税、滞纳金和可能的处罚范围，形成自查底稿\n步骤3：对已明确存在问题的事项主动更正申报、补税并提交说明\n步骤4：清理供应商、开票和审批链条，避免同类问题继续发生\n步骤5：在专业顾问帮助下准备从轻处理依据和陈述材料",
        "risk_warning": "主动补救的窗口期很短。企业一边明知有问题一边继续开票或抵扣，后面很难再主张自己是在主动纠正。",
    },
    "RSK-TAX-012": {
        "applicable_conditions": "适用于企业担心被税务稽查选案，想了解常见风险指标、选案逻辑以及被选中后通知节奏的情形。",
        "exceptions_boundary": "税务选案不会只看单一指标，而是综合税负率、发票结构、利润异常、行业对比和上下游比对等多项信息。也不存在固定‘多久一定下通知’的统一时长。",
        "practical_steps": "步骤1：定期监控企业税负率、毛利率、发票红冲率、异常票据和关联交易等指标\n步骤2：对明显偏离行业和历史水平的指标提前做经营解释和数据留痕\n步骤3：完善合同、发票、物流和资金流闭环证据，降低选案后举证难度\n步骤4：收到任何风险提示后及时自查，避免小问题滚成选案线索\n步骤5：建立内部税务风险台账，持续跟踪高风险事项处置状态",
        "risk_warning": "企业最容易误以为只要没收到通知就说明没风险。实际上，很多选案信号在正式通知前很早就已经体现在异常指标里了。",
    },
    "RSK-TAX-013": {
        "applicable_conditions": "适用于企业欠税金额较大、短期无力一次性缴清，想判断是否可申请分期缴纳及其条件的情形。",
        "exceptions_boundary": "欠税分期不是当然权利，而是特殊救济。是否获批，要看企业经营困难的真实性、还款计划可行性和税务机关审核态度；恶意拖欠通常很难获批。",
        "practical_steps": "步骤1：先核对欠税种类、金额、滞纳金和当前执行状态\n步骤2：准备经营困难证明、现金流预测、资产情况和分期还款方案\n步骤3：向主管税务机关提出书面分期申请，并说明不能一次缴清的客观原因\n步骤4：按要求提供担保、抵押或其他增信资料（如需）\n步骤5：获批后严格按计划履行，避免分期失败转入更严厉执行",
        "risk_warning": "分期缴税最容易失败的原因，不是税务机关不批，而是企业拿不出可信的现金流和履约方案。没有还款能力证明，申请通常很难通过。",
    },
    "SET-ETAX-001": {
        "applicable_conditions": "适用于新设企业第一次办理电子税务局账号注册和实名认证，需要明确开户注册、法人认证和办税员绑定流程的情形。",
        "exceptions_boundary": "电子税务局注册不只是点开网页注册账号，还涉及主体身份核验、法人实名认证和多角色授权。不同地区入口界面不同，但关键节点基本相似。",
        "practical_steps": "步骤1：准备营业执照、法定代表人身份证明、手机号和经办人资料\n步骤2：通过当地电子税务局或电子营业执照入口完成企业开户注册\n步骤3：完成法定代表人实名认证，并按需要绑定办税员和财务负责人\n步骤4：首次登录后检查税费种认定、消息提醒和功能权限是否正常\n步骤5：保留注册成功和绑定成功截图，便于后续权限排查",
        "risk_warning": "新设企业电子税务局最容易卡在法人认证和角色授权。账号注册成功不代表申报、领票和查询都能直接使用。",
    },
    "SET-TAX-004": {
        "applicable_conditions": "适用于新设企业需要确定首个纳税期限，并区分哪些税种按月申报、哪些按季申报的情形。",
        "exceptions_boundary": "第一个纳税期限不是企业自己随意决定的，而是与税费种认定、纳税人身份和征收管理规则相关。不同税种申报周期也不能混为一谈。",
        "practical_steps": "步骤1：先查看电子税务局税费种认定结果，确认各税种申报周期\n步骤2：区分增值税、企业所得税、个税、印花税等不同税种的月报或季报口径\n步骤3：根据登记月份和认定结果确定首个所属期和首个申报截止日\n步骤4：建立首年申报日历，把月度和季度节点拆开管理\n步骤5：首期申报前做一次清单式检查，避免错过任何已认定税种",
        "risk_warning": "新设企业最容易犯的错，是把所有税都按一个周期理解。首期周期一旦判断错，漏报通常从第一月就开始了。",
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
        row = conn.execute(
            """
            SELECT id, version_no
            FROM question_master
            WHERE question_code = ?
            """,
            (code,),
        ).fetchone()
        if not row:
            print(f"⚠️ 未找到问题: {code}")
            continue

        if dry_run:
            print(f"{code} -> 补 {', '.join(fields.keys())}")
            continue

        new_version = (row["version_no"] or 1) + 1
        conn.execute(
            """
            UPDATE question_master
            SET applicable_conditions = ?,
                exceptions_boundary = ?,
                practical_steps = ?,
                risk_warning = ?,
                updated_at = ?,
                version_no = ?
            WHERE id = ?
            """,
            (
                fields["applicable_conditions"],
                fields["exceptions_boundary"],
                fields["practical_steps"],
                fields["risk_warning"],
                now,
                new_version,
                row["id"],
            ),
        )
        conn.execute(
            """
            INSERT INTO question_update_log (
                question_id, version_no, update_date, update_type,
                update_reason, updated_by, reviewed_by, change_summary
            ) VALUES (?, ?, ?, 'update_revise', ?, ?, ?, ?)
            """,
            (
                row["id"],
                new_version,
                now,
                "补齐结构字段：适用条件/边界/步骤/风险",
                "system_backfill",
                "",
                f"{code} 补齐结构字段",
            ),
        )
        print(f"✅ 已补强 {code}")

    if not dry_run:
        conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
