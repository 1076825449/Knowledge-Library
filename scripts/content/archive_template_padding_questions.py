#!/usr/bin/env python3
"""Archive template-generated padding questions that should not stay active."""

import datetime as dt
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"
REPORT_PATH = PROJECT_ROOT / "data" / "reports" / "template_padding_archive_20260423.md"


PATTERNS = [
    "%扩展复核场景%",
    "%扩展复核第%",
    "%不能只看单一页面或单一凭证%",
]


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    where = " OR ".join(
        [
            "question_title LIKE ?",
            "one_line_answer LIKE ?",
            "detailed_answer LIKE ?",
        ]
        * len(PATTERNS)
    )
    params = []
    for pattern in PATTERNS:
        params.extend([pattern, pattern, pattern])

    rows = conn.execute(
        f"""
        SELECT id, question_code, question_title, stage_code, module_code
        FROM question_master
        WHERE status = 'active' AND ({where})
        ORDER BY question_code
        """,
        params,
    ).fetchall()

    by_combo = {}
    for row in rows:
        by_combo[(row["stage_code"], row["module_code"])] = (
            by_combo.get((row["stage_code"], row["module_code"]), 0) + 1
        )

    for row in rows:
        conn.execute(
            """
            UPDATE question_master
            SET status = 'archived', updated_at = ?
            WHERE id = ?
            """,
            (now, row["id"]),
        )
        version = conn.execute(
            "SELECT version_no FROM question_master WHERE id = ?",
            (row["id"],),
        ).fetchone()[0]
        conn.execute(
            """
            INSERT INTO question_update_log (
                question_id, version_no, update_date, update_type,
                update_reason, updated_by, reviewed_by, change_summary
            ) VALUES (?, ?, ?, 'status_change', ?, 'content_audit', 'content_audit', ?)
            """,
            (
                row["id"],
                version,
                now,
                "模板化补量内容归档",
                "标题或正文命中模板化扩展题特征，归档为非 active，避免低质量凑数内容进入正式库。",
            ),
        )

    conn.commit()

    active_after = conn.execute(
        "SELECT count(*) FROM question_master WHERE status = 'active'"
    ).fetchone()[0]
    total_after = conn.execute("SELECT count(*) FROM question_master").fetchone()[0]
    hf_after = conn.execute(
        "SELECT count(*) FROM question_master WHERE status = 'active' AND high_frequency_flag = 1"
    ).fetchone()[0]
    min_combo = conn.execute(
        """
        SELECT min(cnt)
        FROM (
            SELECT count(*) cnt
            FROM question_master
            WHERE status = 'active'
            GROUP BY stage_code, module_code
        )
        """
    ).fetchone()[0]

    lines = [
        "# 模板化补量内容归档报告",
        "",
        f"- 生成时间：{now}",
        f"- 命中并归档：{len(rows)} 条",
        f"- 归档后 active 问题数：{active_after}",
        f"- 归档后问题总记录数：{total_after}",
        f"- 归档后 active 高频问题数：{hf_after}",
        f"- 归档后阶段 × 模块最低厚度：{min_combo}",
        "",
        "## 命中规则",
        "",
        "- 标题或正文包含 `扩展复核场景`",
        "- 标题或正文包含 `扩展复核第`",
        "- 标题或正文包含 `不能只看单一页面或单一凭证`",
        "",
        "## 判断",
        "",
        "这些内容属于批量模板扩展题，字段完整但问题表达泛化、场景不够真实，不能作为正式 active 知识项保留。",
        "",
        "## 按阶段/模块归档数量",
        "",
    ]
    for (stage, module), count in sorted(by_combo.items()):
        lines.append(f"- {stage}/{module}: {count}")
    lines.extend(["", "## 样例", ""])
    for row in rows[:80]:
        lines.append(f"- `{row['question_code']}` {row['question_title']}")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    conn.close()

    print(f"archived={len(rows)}")
    print(f"active_after={active_after}")
    print(f"report={REPORT_PATH}")


if __name__ == "__main__":
    main()
