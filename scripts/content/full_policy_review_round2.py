#!/usr/bin/env python3
"""Full-library policy review round 2.

Reduce source_pending items by adding official sources found after round 1 and
separating metadata/title mismatches from simple missing-source cases.
"""

import sqlite3
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"
REPORT_PATH = PROJECT_ROOT / "data" / "reports" / "full_policy_review_round2_20260423.md"
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


UPDATES = [
    item(
        ["SAT-CLEAR-001"],
        "https://fujian.chinatax.gov.cn/npsswj/qxxxgk/wyss/zdgkjbml/tzgg_24401/202205/t20220526_460056.htm",
        "国家税务总局/福建省南平市税务局转载",
        "source_found",
        "pol_effective",
        "已找到国家税务总局公告2019年第48号官方转载来源；库内标题写作优化税务注销程序不够准确，该公告实际为税收征管若干事项，含非正常户认定解除等内容，需修正政策名称。",
    ),
    item(
        ["SAT-CLEAR-002"],
        "https://shanghai.chinatax.gov.cn/zcfw/zcfgk/swzsgl/201905/t445589.html",
        "国家税务总局/上海市税务局转载",
        "needs_update",
        "pol_partial",
        "已找到税总发〔2019〕64号官方转载来源；页面注明第一条第三项废止，参见2025年第24号公告，注销/破产清算类问题需更新。",
    ),
    item(
        ["POL-RISK-001", "POL-RISK-002"],
        "https://fujian.chinatax.gov.cn/npsswj/qxxxgk/wyss/zdgkjbml/tzgg_24401/202205/t20220526_460056.htm",
        "国家税务总局/福建省南平市税务局转载",
        "needs_update",
        "pol_replaced",
        "库内税总发〔2014〕106号非正常户口径应改挂国家税务总局公告2019年第48号；非正常户认定、解除和欠税处理需按2019年第48号重核。",
    ),
    item(
        ["POL-PREF-001"],
        "https://www.gov.cn/zhengce/zhengceku/2019-10/15/content_5440054.htm",
        "中国政府网/财政部政策库",
        "needs_update",
        "pol_expired",
        "已找到财税〔2019〕13号官方来源；该普惠性减免为阶段性政策，当前小微优惠应改按后续延续政策复核。",
    ),
    item(
        ["POL-PREF-003"],
        "https://www.gov.cn/zhengce/zhengceku/2023-03/27/content_5748507.htm",
        "中国政府网/财政部税务总局政策库",
        "needs_update",
        "pol_replaced",
        "已找到2023年小微企业和个体工商户所得税优惠政策官方来源；执行期至2024-12-31，且部分个体工商户优惠已由2023年第12号公告替代，需按现行延续政策复核。",
        "2024-12-31",
    ),
    item(
        ["POL-PREF-004"],
        "https://jdjc.mof.gov.cn/fgzd/202309/t20230904_3905379.htm",
        "财政部转载国务院文件",
        "source_found",
        "pol_effective",
        "已找到国发〔2023〕13号专项附加扣除标准提高官方来源；个税扣除类问题需结合税务总局2023年第14号执行公告复核。",
    ),
    item(
        ["POL-PREF-007"],
        "https://fgk.chinatax.gov.cn/zcfgk/c102416/c5203716/content.html",
        "国家税务总局政策法规库",
        "source_found",
        "pol_effective",
        "已找到促进残疾人就业增值税优惠政策官方政策法规库来源；具体退税限额需按地方最低工资标准动态复核。",
    ),
    item(
        ["POL-PREF-008"],
        "https://sh.mof.gov.cn/tongzhitonggao/202203/t20220331_3800284.htm",
        "财政部上海监管局转载",
        "source_found",
        "pol_effective",
        "已找到2022年第14号留抵退税政策官方系统来源；留抵退税问题需同时挂接税务总局2022年第4号征管公告。",
    ),
    item(
        ["POL-PREF-010"],
        "https://www.gov.cn/zhengce/zhengceku/2020-12/17/content_5570401.htm",
        "中国政府网/财政部政策库",
        "source_found",
        "pol_effective",
        "已找到集成电路和软件产业企业所得税政策官方来源；优惠资格问题需按清单管理和行业主管部门口径复核。",
    ),
    item(
        ["POL-TAX-001"],
        "https://www.gov.cn/zwgk/2011-09/20/content_1951515.htm",
        "中国政府网",
        "source_found",
        "pol_effective",
        "已找到专项用途财政性资金企业所得税处理官方来源；不征税收入和支出扣除问题需按资金用途、单独核算和5年转回要求复核。",
    ),
    item(
        ["SAT-VAT-003"],
        "https://shanghai.chinatax.gov.cn/zcfw/zcfgk/zzs/201910/t448187.html",
        "国家税务总局/上海市税务局转载",
        "needs_update",
        "pol_partial",
        "已找到国家税务总局公告2019年第33号官方转载来源；页面注明部分条款废止，发票管理类问题需按废止注释和后续数电票公告复核。",
    ),
    item(
        ["POL-RISK-003", "SAT-VAT-006"],
        "https://fgk.chinatax.gov.cn/zcfgk/c100012/c5194894/content.html",
        "国家税务总局政策法规库",
        "source_found",
        "pol_effective",
        "已找到国家税务总局公告2019年第38号异常增值税扣税凭证官方来源；异常凭证处理问题需结合申报表填列和信用等级差异复核。",
    ),
    item(
        ["SAT-VAT-007", "POL-VAT-005"],
        "https://www.chinatax.gov.cn/chinatax/n810341/n810760/c5162929/content.html",
        "国家税务总局",
        "source_found",
        "pol_effective",
        "已找到增值税优惠办理程序公告官方解读入口；库内文号第4号/第8号存在错配风险，需补原文链接后修正元数据。",
    ),
    item(
        ["POL-VAT-008"],
        "https://shanghai.chinatax.gov.cn/zcfw/zcfgk/zzs/202004/t453297.html",
        "财政部税务总局/上海市税务局转载",
        "needs_update",
        "pol_expired",
        "已找到二手车经销增值税政策官方转载来源；原文执行期至2023-12-31，需查后续延续政策后方可继续引用。",
        "2023-12-31",
    ),
]


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    applied = []
    for group in UPDATES:
        for code in group["codes"]:
            row = conn.execute("SELECT policy_name FROM policy_basis WHERE policy_code = ?", (code,)).fetchone()
            if not row:
                continue
            conn.execute(
                """
                UPDATE policy_basis
                SET source_url = ?,
                    source_org = ?,
                    source_type = 'official',
                    last_verified_at = ?,
                    verification_status = ?,
                    verification_note = ?,
                    current_status = ?,
                    expiry_date = COALESCE(?, expiry_date),
                    updated_at = datetime('now')
                WHERE policy_code = ?
                """,
                (
                    group["url"],
                    group["org"],
                    TODAY,
                    group["status"],
                    group["note"],
                    group["current_status"],
                    group["expiry_date"],
                    code,
                ),
            )
            applied.append((code, row["policy_name"], group["status"]))
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

    lines = [
        "# 全库政策复核 Round 2",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 本轮新增/修正官方来源：{len(applied)} 条",
        f"- active 引用政策仍缺官方 source_url：{active_missing_source}",
        "",
        "## 状态分布",
        "",
    ]
    for row in status_rows:
        lines.append(f"- `{row['verification_status']}`: {row['count']}")
    lines.extend(["", "## 本轮明细", ""])
    for code, name, status in sorted(applied):
        lines.append(f"- `{code}` {name}: `{status}`")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"updated={len(applied)}")
    print(f"active_missing_source={active_missing_source}")
    print(f"report={REPORT_PATH}")


if __name__ == "__main__":
    main()
