#!/usr/bin/env python3
"""Full-library policy review round 1.

Every policy_basis row receives a review disposition. This is not a blanket
"passed" flag: rows without a stable official source are explicitly marked as
source_pending/manual_local_review so they cannot be mistaken for verified
launch content.
"""

import sqlite3
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"
REPORT_PATH = PROJECT_ROOT / "data" / "reports" / "full_policy_review_round1_20260423.md"
TODAY = datetime.now().strftime("%Y-%m-%d")


def item(codes, url, org, status, current_status, note, expiry_date=None):
    return {
        "codes": codes,
        "url": url,
        "org": org,
        "status": status,
        "current_status": current_status,
        "note": note,
        "expiry_date": expiry_date,
    }


REVIEWED = [
    item(
        ["GOV-VAT-001", "POL-VAT-001", "GOV-VAT-002", "SAT-VAT-001", "TAX-POL-008"],
        "https://www.npc.gov.cn/npc/c2/c30834/202412/t20241225_442015.html",
        "中国人大网",
        "needs_update",
        "pol_replaced",
        "《中华人民共和国增值税法》自2026-01-01施行，原《中华人民共和国增值税暂行条例》同时废止；仍引用暂行条例、实施细则或视同销售旧条款的问题必须按新法重核。",
        "2025-12-31",
    ),
    item(
        ["SAT-VAT-004", "POL-VAT-007"],
        "https://shanghai.chinatax.gov.cn/zcfw/zcfgk/zzs/202602/t479295.html",
        "国家税务总局/上海市税务局转载",
        "needs_update",
        "pol_partial",
        "国家税务总局公告2026年第6号调整增值税纳税申报事项；旧申报表、旧申报口径类答案需按2026年公告复核。",
    ),
    item(
        ["GOV-Tax-001", "TAX-POL-001"],
        "https://www.gov.cn/banshi/2005-08/19/content_24823.htm",
        "中国政府网",
        "source_found",
        "pol_effective",
        "已找到税收征收管理法官方来源；答案级复核仍需逐条核验引用条款、滞纳金和处罚适用边界。",
    ),
    item(
        ["GOV-Tax-002", "SAT-TAX-001", "GOV-REG-001", "GOV-REG-002", "GOV-REG-003", "GOV-REG-004", "POL-SUS-001", "CLEAR-POL-001", "TAX-POL-005"],
        "https://www.gov.cn/gongbao/content/2015/content_2975893.htm",
        "国务院公报",
        "source_found",
        "pol_effective",
        "已找到税务登记管理办法官方来源；登记、停复业、注销章节相关问题仍需结合后续优化征管服务文件复核。",
    ),
    item(
        ["SAT-2024-033"],
        "https://guangdong.chinatax.gov.cn/gdsw/yjsw_yhssyshj2024_zcwj_yhggfw/2024-07/24/content_0ab816531e5a41b1be1339837324b124.shtml",
        "国家税务总局/广东省税务局转载",
        "source_found",
        "pol_effective",
        "已找到优化若干税收征管服务事项官方转载来源；需继续核验库内文号“2024年第33号”是否准确，疑似与税总征科发〔2024〕33号混写。",
    ),
    item(
        ["GOV-CIT-001", "POL-CIT-001", "POL-WHT-001", "TAX-POL-006", "TAX-POL-007"],
        "https://www.gov.cn/flfg/2007-03/19/content_554243.htm",
        "中国政府网",
        "source_found",
        "pol_effective",
        "已找到企业所得税法官方来源；涉及非居民预提、汇算清缴、免税收入等问题需补最新修正文本并逐条核验。",
    ),
    item(
        ["SAT-CIT-001"],
        "https://www.gov.cn/gongbao/content/2018/content_5326376.htm",
        "国务院公报",
        "source_found",
        "pol_effective",
        "已找到企业所得税税前扣除凭证管理办法官方来源；发票/非发票扣除问题需按具体凭证类型复核。",
    ),
    item(
        ["GOV-CIT-002"],
        "https://www.gov.cn/zwgk/2009-05/08/content_1308132.htm",
        "中国政府网",
        "source_found",
        "pol_effective",
        "已找到企业清算业务企业所得税处理若干问题通知官方来源；注销清算类问题需复核清算所得、股东分配和亏损处理边界。",
    ),
    item(
        ["POL-CIT-002", "SAT-FEE-001"],
        "https://www.chinatax.gov.cn/chinatax/n810341/n810765/n812156/201103/c1187231/content.html",
        "国家税务总局",
        "source_found",
        "pol_effective",
        "已找到国家税务总局公告2011年第25号官方来源；资产损失和费用扣除问题需核验是否存在条款废止或资料留存口径变化。",
    ),
    item(
        ["POL-INV-001"],
        "https://www.gov.cn/flfg/2010-12/27/content_1773544.htm",
        "中国政府网",
        "source_found",
        "pol_effective",
        "已找到发票管理办法官方来源；数电票、电子发票和红字发票问题需另挂更新公告。",
    ),
    item(
        ["SAT-INV-001", "SAT-INV-002"],
        "https://shenzhen.chinatax.gov.cn/sztax/zcwj/zcfgk/zjzcfgk/zzszj/201607/2f1c6fc957ba49dabac505269bc58989.shtml",
        "国家税务总局/深圳市税务局转载",
        "source_found",
        "pol_effective",
        "已找到国家税务总局公告2016年第47号官方转载来源；红字发票类问题需继续核验数电票红字确认单新流程。",
    ),
    item(
        ["POL-INV-003"],
        "https://shenzhen.chinatax.gov.cn/sztax/zcwj/zcfgk/zjzcfgk/zzszj/201607/2f1c6fc957ba49dabac505269bc58989.shtml",
        "国家税务总局/深圳市税务局转载",
        "needs_update",
        "pol_replaced",
        "库内记录为2014年第73号红字发票旧依据；已找到2016年第47号后续公告，应按新公告替换或合并该依据。",
    ),
    item(
        ["POL-SSF-001"],
        "https://www.gov.cn/banshi/2005-08/04/content_20250.htm",
        "中国政府网",
        "source_found",
        "pol_effective",
        "已找到社会保险费征缴暂行条例官方来源；社保费征管职责和电子申报流程需结合税务部门征收现行口径复核。",
    ),
    item(
        ["SSF-POL-001"],
        "https://www.gov.cn/flfg/2010-10/28/content_1732964.htm",
        "中国政府网",
        "source_found",
        "pol_effective",
        "已找到社会保险法官方来源；社保登记问题需结合地方人社/税务协同办理口径复核。",
    ),
    item(
        ["SSF-POL-002"],
        "https://www.gov.cn/ziliao/flfg/2007-06/29/content_669394.htm",
        "中国政府网",
        "source_found",
        "pol_effective",
        "已找到劳动合同法官方来源；停业、注销、用工终止类问题需核验与社保减员、工资个税扣缴的衔接。",
    ),
    item(
        ["GOV-PEN-001"],
        "https://www.npc.gov.cn/npc/c2/c30834/202101/t20210122_309857.html",
        "中国人大网",
        "source_found",
        "pol_effective",
        "已找到2021年修订行政处罚法官方来源；税务处罚问题需同步核验税务稽查和首违不罚专项规定。",
    ),
    item(
        ["POL-DEC-002"],
        "https://www.gov.cn/gongbao/content/2021/content_5637950.htm",
        "中国政府网/国务院公报",
        "source_found",
        "pol_effective",
        "库内名称写作税务行政处罚程序规定，但文号第52号实际对应税务稽查案件办理程序规定；需修正政策名称后再做答案级复核。",
    ),
    item(
        ["SAT-RISK-001", "SAT-RISK-002", "SAT-RISK-003"],
        "https://www.chinatax.gov.cn/chinatax/n810341/n810825/c102434/c5239133/content.html",
        "国家税务总局",
        "needs_update",
        "pol_replaced",
        "纳税信用管理办法（试行）及相关事项已进入2025年纳税缴费信用管理办法体系；风险/信用类问题必须按新规重核。",
        "2025-07-01",
    ),
    item(
        ["GOV-Tax-003", "SAT-SUS-001"],
        "https://www.gov.cn/zhengce/zhengceku/2021-09/30/content_5640426.htm",
        "中国政府网/税务总局政策库",
        "source_found",
        "pol_effective",
        "已找到重大税收违法失信主体信息公布管理办法修订公告官方来源；信用惩戒类问题需和2025信用新规交叉复核。",
    ),
    item(
        ["SAT-SUS-002"],
        "https://guizhou.chinatax.gov.cn/xwzx/zxfb/201912/t20191212_52498715.html",
        "国家税务总局/贵州省税务局转载",
        "source_found",
        "pol_effective",
        "已找到税务文书电子送达规定（试行）官方转载来源；电子税务局文书送达类问题需复核地方开通范围。",
    ),
    item(
        ["POL-WHT-002", "IIT-POL-002"],
        "https://www.chinatax.gov.cn/chinatax/n810219/n810744/n3752930/n3752974/c3959952/content.html",
        "国家税务总局",
        "source_found",
        "pol_effective",
        "已找到个人所得税法2018修正官方来源；工资薪金、综合所得和扣缴类问题需结合年度汇算与预扣预缴公告复核。",
    ),
    item(
        ["SAT-IIT-001"],
        "https://www.chinatax.gov.cn/chinatax/n810219/n810744/n3752930/n3752974/c3970353/content.html",
        "国家税务总局",
        "source_found",
        "pol_effective",
        "已找到全面实施新个人所得税法若干征管衔接事项公告官方来源；扣缴申报问题需结合后续预扣预缴公告复核。",
    ),
    item(
        ["SAT-IIT-002"],
        "https://www.gov.cn/zhengce/zhengceku/202308/content_6900701.htm",
        "中国政府网/财政部税务总局政策库",
        "source_found",
        "pol_effective",
        "已找到全年一次性奖金等个人所得税政策延续公告官方来源；奖金、补发工资类问题需核验适用期限。",
    ),
    item(
        ["SAT-IIT-003"],
        "https://www.chinatax.gov.cn/chinatax/n810341/n810755/c5156192/content.html",
        "国家税务总局",
        "source_found",
        "pol_effective",
        "已找到完善调整部分纳税人个人所得税预扣预缴方法公告官方来源；累计预扣和新入职员工问题需按该公告复核。",
    ),
    item(
        ["POL-PREF-009", "POL-DEC-001", "POL-PREF-002"],
        "https://www.gov.cn/zhengce/zhengceku/202308/content_6900147.htm",
        "中国政府网/财政部税务总局政策库",
        "needs_update",
        "pol_partial",
        "小规模纳税人增值税减免政策属于阶段性优惠，库内2023政策需要按后续延续和2026增值税法配套口径复核。",
    ),
    item(
        ["POL-PREF-005"],
        "https://www.gov.cn/zhengce/zhengceku/202303/content_5749203.htm",
        "中国政府网/财政部税务总局政策库",
        "source_found",
        "pol_effective",
        "已找到研发费用加计扣除政策官方来源；研发费用题需核验行业排除、费用归集和留存备查边界。",
    ),
    item(
        ["POL-VAT-002", "SAT-VAT-008"],
        "https://www.gov.cn/zhengce/zhengceku/2019-10/11/content_5438423.htm",
        "中国政府网/财政部税务总局海关总署政策库",
        "source_found",
        "pol_effective",
        "已找到深化增值税改革政策官方来源；税率、加计抵减和留抵相关问题需按2026增值税法配套政策继续复核。",
    ),
    item(
        ["GOV-VAT-003"],
        "https://www.gov.cn/zhengce/content/2016-03/24/content_5056665.htm",
        "中国政府网",
        "source_found",
        "pol_effective",
        "已找到全面推开营改增试点通知官方来源；营改增附件条款需按2026增值税法及后续配套规定复核。",
    ),
    item(
        ["SAT-VAT-002"],
        "https://www.gov.cn/gongbao/content/2018/content_5271313.htm",
        "中国政府网/国务院公报",
        "source_found",
        "pol_effective",
        "已找到增值税一般纳税人登记管理办法官方来源；小规模/一般纳税人边界题需结合现行销售额标准和2026配套口径复核。",
    ),
]


MANUAL_LOCAL_CODES = {
    "LOCAL-GX-001",
    "LOCAL-GX-002",
    "POL-LOCAL-GD-001",
    "POL-LOCAL-GD-002",
    "POL-LOCAL-GD-003",
    "POL-LOCAL-SH-001",
    "POL-LOCAL-SH-002",
}


SUSPICIOUS_CODES = {
    "POL-RISK-001": "非正常户口径疑似来自内部规范性文件或旧征管口径，需用国家税务总局现行公告/办法重新定位。",
    "POL-RISK-002": "非正常户口径疑似来自内部规范性文件或旧征管口径，需用国家税务总局现行公告/办法重新定位。",
    "POL-WHT-003": "个人所得税代扣代缴暂行办法为旧文号，需核验是否已被新个税法扣缴申报制度替代。",
    "POL-INV-002": "增值税专用发票使用规定为旧国税发文件，需核验与数电票、发票管理办法修订后的衔接。",
    "POL-INV-004": "取消发票丢失抄报税口径需查到国家税务总局2019年第8号原文后再确认。",
}


def ensure_columns(conn):
    existing = {row[1] for row in conn.execute("PRAGMA table_info(policy_basis)")}
    for name, definition in [
        ("source_url", "TEXT"),
        ("source_org", "TEXT"),
        ("source_type", "TEXT NOT NULL DEFAULT 'official'"),
        ("last_verified_at", "TEXT"),
        ("verification_status", "TEXT NOT NULL DEFAULT 'unverified'"),
        ("verification_note", "TEXT"),
    ]:
        if name not in existing:
            conn.execute(f"ALTER TABLE policy_basis ADD COLUMN {name} {definition}")


def update_policy(conn, code, status, current_status, note, url=None, org=None, expiry_date=None):
    conn.execute(
        """
        UPDATE policy_basis
        SET source_url = COALESCE(?, source_url),
            source_org = COALESCE(?, source_org),
            source_type = CASE WHEN ? IS NULL THEN source_type ELSE 'official' END,
            last_verified_at = ?,
            verification_status = ?,
            verification_note = ?,
            current_status = ?,
            expiry_date = COALESCE(?, expiry_date),
            updated_at = datetime('now')
        WHERE policy_code = ?
        """,
        (url, org, url, TODAY, status, note, current_status, expiry_date, code),
    )


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    ensure_columns(conn)

    applied = []
    not_found = []
    for group in REVIEWED:
        for code in group["codes"]:
            row = conn.execute("SELECT policy_name FROM policy_basis WHERE policy_code = ?", (code,)).fetchone()
            if not row:
                not_found.append(code)
                continue
            update_policy(
                conn,
                code,
                group["status"],
                group["current_status"],
                group["note"],
                group["url"],
                group["org"],
                group["expiry_date"],
            )
            applied.append((code, row["policy_name"], group["status"]))

    for code in MANUAL_LOCAL_CODES:
        row = conn.execute("SELECT policy_name FROM policy_basis WHERE policy_code = ?", (code,)).fetchone()
        if row:
            update_policy(
                conn,
                code,
                "manual_local_review",
                "pol_uncertain",
                "地方口径政策已纳入全库复核，但本轮未确认稳定官方全文或适用地区现行状态；上线前必须由对应地方税务/财政/人大官网逐条确认。",
            )
            applied.append((code, row["policy_name"], "manual_local_review"))

    for code, note in SUSPICIOUS_CODES.items():
        row = conn.execute("SELECT policy_name FROM policy_basis WHERE policy_code = ?", (code,)).fetchone()
        if row:
            update_policy(conn, code, "source_pending", "pol_uncertain", note)
            applied.append((code, row["policy_name"], "source_pending"))

    remaining = conn.execute(
        """
        SELECT policy_code, policy_name
        FROM policy_basis
        WHERE COALESCE(verification_status, 'unverified') = 'unverified'
        ORDER BY id
        """
    ).fetchall()
    for row in remaining:
        update_policy(
            conn,
            row["policy_code"],
            "source_pending",
            "pol_uncertain",
            "全库复核第一轮已覆盖该政策，但本轮未确认稳定官方来源、现行状态或替代关系；不得作为已复核依据使用。",
        )
        applied.append((row["policy_code"], row["policy_name"], "source_pending"))

    conn.commit()

    status_rows = conn.execute(
        "SELECT verification_status, COUNT(*) AS count FROM policy_basis GROUP BY verification_status ORDER BY verification_status"
    ).fetchall()
    active_missing_source = conn.execute(
        """
        SELECT COUNT(DISTINCT pb.id)
        FROM policy_basis pb
        JOIN question_policy_link qpl ON qpl.policy_id = pb.id
        JOIN question_master q ON q.id = qpl.question_id
        WHERE q.status='active'
          AND (pb.source_url IS NULL OR trim(pb.source_url) = '')
        """
    ).fetchone()[0]
    affected_needs_update = conn.execute(
        """
        SELECT COUNT(DISTINCT q.id)
        FROM question_master q
        JOIN question_policy_link qpl ON qpl.question_id = q.id
        JOIN policy_basis pb ON pb.id = qpl.policy_id
        WHERE q.status='active' AND pb.verification_status = 'needs_update'
        """
    ).fetchone()[0]

    lines = [
        "# 全库政策复核 Round 1",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 数据库：{DB_PATH}",
        f"- policy_basis 总数：{conn.execute('SELECT COUNT(*) FROM policy_basis').fetchone()[0]}",
        f"- 本轮写入复核结论：{len(applied)} 条记录",
        f"- active 引用政策仍缺官方 source_url：{active_missing_source}",
        f"- 受 `needs_update` 政策影响的 active 问题：{affected_needs_update}",
        "",
        "## 状态分布",
        "",
    ]
    for row in status_rows:
        lines.append(f"- `{row['verification_status']}`: {row['count']}")
    lines.extend(["", "## 口径说明", ""])
    lines.append("- `source_found`：已找到官方或税务机关转载来源，但答案尚未逐条签收。")
    lines.append("- `needs_update`：已发现废止、替代或重大口径变化，相关问题必须修订。")
    lines.append("- `source_pending`：已纳入全库复核，但本轮未确认稳定官方来源或现行状态。")
    lines.append("- `manual_local_review`：地方口径必须由对应地区官方渠道二次确认。")
    lines.extend(["", "## 本轮明细", ""])
    for code, name, status in sorted(applied):
        lines.append(f"- `{code}` {name}: `{status}`")
    if not_found:
        lines.extend(["", "## 脚本中配置但库内不存在", ""])
        for code in not_found:
            lines.append(f"- `{code}`")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"updated={len(applied)}")
    print(f"active_missing_source={active_missing_source}")
    print(f"affected_needs_update_questions={affected_needs_update}")
    print(f"report={REPORT_PATH}")


if __name__ == "__main__":
    main()
