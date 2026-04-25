#!/usr/bin/env python3
"""Seed official-source verification metadata for high-impact policies.

This script is intentionally conservative: it only writes official source
links and verification flags that were manually checked. It does not claim the
whole policy library is current.
"""

import sqlite3
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"
REPORT_PATH = PROJECT_ROOT / "data" / "reports" / "policy_source_verification_batch1_20260423.md"


VERIFIED_POLICIES = [
    {
        "policy_codes": ["GOV-VAT-001", "POL-VAT-001", "GOV-VAT-002", "SAT-VAT-001"],
        "source_url": "https://www.npc.gov.cn/npc/c2/c30834/202412/t20241225_442015.html",
        "source_org": "中国人大网",
        "verification_status": "needs_update",
        "current_status": "pol_replaced",
        "expiry_date": "2025-12-31",
        "note": "《中华人民共和国增值税法》自2026-01-01施行，原《中华人民共和国增值税暂行条例》同时废止；仍引用暂行条例或实施细则的问题需要按新法口径复核。",
    },
    {
        "policy_codes": ["SAT-VAT-004"],
        "source_url": "https://shanghai.chinatax.gov.cn/zcfw/zcfgk/zzs/202602/t479295.html",
        "source_org": "国家税务总局/上海市税务局转载",
        "verification_status": "needs_update",
        "current_status": "pol_partial",
        "expiry_date": None,
        "note": "国家税务总局公告2026年第6号调整增值税纳税申报有关事项；涉及申报表、申报口径的问题需要按2026年公告复核。",
    },
    {
        "policy_codes": ["SAT-CIT-001"],
        "source_url": "https://www.gov.cn/gongbao/content/2018/content_5326376.htm",
        "source_org": "国务院公报",
        "verification_status": "source_found",
        "current_status": "pol_effective",
        "expiry_date": None,
        "note": "已找到《企业所得税税前扣除凭证管理办法》（国家税务总局公告2018年第28号）官方来源；仍需逐条核验具体问题是否正确引用条款。",
    },
    {
        "policy_codes": ["GOV-CIT-001", "POL-CIT-001"],
        "source_url": "https://www.gov.cn/flfg/2007-03/19/content_554243.htm",
        "source_org": "中国政府网",
        "verification_status": "source_found",
        "current_status": "pol_effective",
        "expiry_date": None,
        "note": "已找到《中华人民共和国企业所得税法》官方来源；后续应补充最新修正版本来源并核验具体条款。",
    },
    {
        "policy_codes": ["POL-INV-001"],
        "source_url": "https://www.gov.cn/flfg/2010-12/27/content_1773544.htm",
        "source_org": "中国政府网",
        "verification_status": "source_found",
        "current_status": "pol_effective",
        "expiry_date": None,
        "note": "已找到《中华人民共和国发票管理办法》官方来源；发票电子化和数电票问题仍需继续挂接更新公告。",
    },
    {
        "policy_codes": ["GOV-Tax-001", "TAX-POL-001"],
        "source_url": "https://www.gov.cn/banshi/2005-08/19/content_24823.htm",
        "source_org": "中国政府网",
        "verification_status": "source_found",
        "current_status": "pol_effective",
        "expiry_date": None,
        "note": "已找到《中华人民共和国税收征收管理法》官方来源；后续应补充最新有效文本来源并核验滞纳金、处罚等具体条款。",
    },
    {
        "policy_codes": ["GOV-REG-001", "SAT-TAX-001", "GOV-Tax-002"],
        "source_url": "https://www.gov.cn/gongbao/content/2015/content_2975893.htm",
        "source_org": "国务院公报",
        "verification_status": "source_found",
        "current_status": "pol_effective",
        "expiry_date": None,
        "note": "已找到《税务登记管理办法》官方来源；登记实名、电子税务局和一照一码相关问题仍需继续核验后续公告。",
    },
]


def ensure_columns(conn):
    existing = {row[1] for row in conn.execute("PRAGMA table_info(policy_basis)")}
    columns = [
        ("source_url", "TEXT"),
        ("source_org", "TEXT"),
        ("source_type", "TEXT NOT NULL DEFAULT 'official'"),
        ("last_verified_at", "TEXT"),
        ("verification_status", "TEXT NOT NULL DEFAULT 'unverified'"),
        ("verification_note", "TEXT"),
    ]
    for name, definition in columns:
        if name not in existing:
            conn.execute(f"ALTER TABLE policy_basis ADD COLUMN {name} {definition}")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_pb_verification_status ON policy_basis(verification_status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_pb_last_verified_at ON policy_basis(last_verified_at)")


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    ensure_columns(conn)

    touched = []
    missing = []
    for item in VERIFIED_POLICIES:
        for code in item["policy_codes"]:
            row = conn.execute(
                "SELECT id, policy_name FROM policy_basis WHERE policy_code = ?",
                (code,),
            ).fetchone()
            if not row:
                missing.append(code)
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
                    item["source_url"],
                    item["source_org"],
                    today,
                    item["verification_status"],
                    item["note"],
                    item["current_status"],
                    item["expiry_date"],
                    code,
                ),
            )
            touched.append((code, row["policy_name"], item["verification_status"], item["note"]))

    conn.commit()

    total = conn.execute("SELECT COUNT(*) FROM policy_basis").fetchone()[0]
    active_linked = conn.execute(
        """
        SELECT COUNT(DISTINCT pb.id)
        FROM policy_basis pb
        JOIN question_policy_link qpl ON qpl.policy_id = pb.id
        JOIN question_master q ON q.id = qpl.question_id
        WHERE q.status = 'active'
        """
    ).fetchone()[0]
    by_status = conn.execute(
        """
        SELECT verification_status, COUNT(*)
        FROM policy_basis
        GROUP BY verification_status
        ORDER BY COUNT(*) DESC
        """
    ).fetchall()

    lines = [
        "# 政策官方来源核验 Batch 1",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 数据库：{DB_PATH}",
        f"- policy_basis 总数：{total}",
        f"- active 问题正在引用的政策数：{active_linked}",
        f"- 本批写入官方来源/核验标记：{len(touched)} 条政策记录",
        "",
        "## 核验状态分布",
        "",
    ]
    for status, count in by_status:
        lines.append(f"- `{status}`: {count}")
    lines.extend(["", "## 本批处理记录", ""])
    for code, name, status, note in touched:
        lines.append(f"- `{code}` {name}：`{status}`；{note}")
    if missing:
        lines.extend(["", "## 未在库中找到的 policy_code", ""])
        for code in missing:
            lines.append(f"- `{code}`")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"updated={len(touched)}")
    print(f"missing={len(missing)}")
    print(f"report={REPORT_PATH}")


if __name__ == "__main__":
    main()
