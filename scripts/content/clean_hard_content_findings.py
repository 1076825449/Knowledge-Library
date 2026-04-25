#!/usr/bin/env python3
"""Clean hard content findings: duplicate active titles and truncated titles."""

import datetime as dt
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"
REPORT_PATH = PROJECT_ROOT / "data" / "reports" / "hard_content_findings_cleaned_20260423.md"


DUPLICATE_ARCHIVE_CODES = [
    "OPR-CIT-034",
    "OPR-CIT-035",
    "OPR-CIT-036",
    "OPR-DEC-013",
    "OPR-FEE-028",
    "OPR-FEE-029",
    "OPR-FEE-030",
    "OPR-FEE-031",
    "OPR-FEE-032",
    "OPR-IIT-026",
    "OPR-IIT-027",
    "OPR-IIT-029",
]


TITLE_FIXES = {
    "CLS-FEE-001": "注销时发生的资产损失（包括存货报废、固定资产盘亏等），税务上如何处理？",
    "CLS-PREF-001": "注销前已备案的税收优惠资格（如小型微利企业、高新技术企业等）还要收口吗？",
    "RSK-TAX-005": "企业被税务机关稽查补税后，须在规定时限内缴纳税款吗？",
    "CLS-DEC-001": "注销前须完成当期所有税种申报，包括增值税、企业所得税和个税吗？",
    "CLS-REG-003": "分支机构注销是否必须先于母公司完成？流程与普通注销相同吗？",
    "SET-RISK-002": "新设企业预防涉税风险的核心动作有哪些？",
}


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# 硬性内容问题清理报告",
        "",
        f"- 生成时间：{now}",
        "",
    ]

    archived = []
    for code in DUPLICATE_ARCHIVE_CODES:
        row = conn.execute(
            "SELECT id, question_title, version_no FROM question_master WHERE question_code = ? AND status = 'active'",
            (code,),
        ).fetchone()
        if not row:
            continue
        conn.execute(
            "UPDATE question_master SET status = 'archived', updated_at = ? WHERE id = ?",
            (now, row["id"]),
        )
        conn.execute(
            """
            INSERT INTO question_update_log (
                question_id, version_no, update_date, update_type,
                update_reason, updated_by, reviewed_by, change_summary
            ) VALUES (?, ?, ?, 'status_change', ?, 'content_audit', 'content_audit', ?)
            """,
            (
                row["id"],
                row["version_no"],
                now,
                "重复题名归档",
                "归档后导入的重复问题，保留较早的 canonical active 版本。",
            ),
        )
        archived.append((code, row["question_title"]))

    fixed = []
    for code, new_title in TITLE_FIXES.items():
        row = conn.execute(
            "SELECT id, question_title, version_no FROM question_master WHERE question_code = ? AND status = 'active'",
            (code,),
        ).fetchone()
        if not row:
            continue
        old_title = row["question_title"]
        conn.execute(
            """
            UPDATE question_master
            SET question_title = ?, question_plain = ?, version_no = version_no + 1, updated_at = ?
            WHERE id = ?
            """,
            (new_title, new_title, now, row["id"]),
        )
        conn.execute(
            """
            INSERT INTO question_update_log (
                question_id, version_no, update_date, update_type,
                update_reason, updated_by, reviewed_by, change_summary
            ) VALUES (?, ?, ?, 'revise', ?, 'content_audit', 'content_audit', ?)
            """,
            (
                row["id"],
                row["version_no"] + 1,
                now,
                "标题截断修正",
                f"标题由“{old_title}”修正为“{new_title}”。",
            ),
        )
        fixed.append((code, old_title, new_title))

    conn.commit()
    active_after = conn.execute(
        "SELECT count(*) FROM question_master WHERE status = 'active'"
    ).fetchone()[0]
    conn.close()

    lines.append(f"- 归档重复题：{len(archived)} 条")
    lines.append(f"- 修正截断标题：{len(fixed)} 条")
    lines.append(f"- 清理后 active 问题数：{active_after}")
    lines.append("")
    lines.append("## 已归档重复题")
    lines.append("")
    for code, title in archived:
        lines.append(f"- `{code}` {title}")
    lines.append("")
    lines.append("## 已修正标题")
    lines.append("")
    for code, old, new in fixed:
        lines.append(f"- `{code}` `{old}` -> `{new}`")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"archived_duplicates={len(archived)}")
    print(f"fixed_titles={len(fixed)}")
    print(f"active_after={active_after}")
    print(f"report={REPORT_PATH}")


if __name__ == "__main__":
    main()
