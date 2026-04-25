#!/usr/bin/env python3
"""Report active questions affected by policies marked needs_update."""

import sqlite3
from collections import defaultdict
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"
REPORT_PATH = PROJECT_ROOT / "data" / "reports" / "questions_affected_by_policy_updates_20260423.md"


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT
            q.question_code,
            q.question_title,
            q.stage_code,
            q.module_code,
            q.high_frequency_flag,
            pb.policy_code,
            pb.policy_name,
            pb.document_no,
            pb.current_status,
            pb.verification_note
        FROM question_master q
        JOIN question_policy_link qpl ON qpl.question_id = q.id
        JOIN policy_basis pb ON pb.id = qpl.policy_id
        WHERE q.status = 'active'
          AND pb.verification_status = 'needs_update'
        ORDER BY q.high_frequency_flag DESC, q.module_code, q.question_code, pb.policy_code
        """
    ).fetchall()

    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["question_code"], row["question_title"], row["stage_code"], row["module_code"], row["high_frequency_flag"])].append(row)

    by_policy = conn.execute(
        """
        SELECT
            pb.policy_code,
            pb.policy_name,
            pb.document_no,
            pb.current_status,
            COUNT(DISTINCT q.id) AS question_count,
            SUM(CASE WHEN q.high_frequency_flag = 1 THEN 1 ELSE 0 END) AS hf_count
        FROM policy_basis pb
        JOIN question_policy_link qpl ON qpl.policy_id = pb.id
        JOIN question_master q ON q.id = qpl.question_id
        WHERE q.status = 'active'
          AND pb.verification_status = 'needs_update'
        GROUP BY pb.id
        ORDER BY question_count DESC, hf_count DESC, pb.policy_code
        """
    ).fetchall()

    lines = [
        "# 受过时/需更新政策影响的 active 问题清单",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 数据库：{DB_PATH}",
        f"- 受影响 active 问题数：{len(grouped)}",
        f"- 受影响明细关联数：{len(rows)}",
        "",
        "## 按政策汇总",
        "",
    ]
    for row in by_policy:
        lines.append(
            f"- `{row['policy_code']}` {row['policy_name']}（{row['document_no'] or '无文号'}，{row['current_status']}）："
            f"影响 active 问题 {row['question_count']} 条，高频引用 {row['hf_count'] or 0} 条"
        )

    lines.extend(["", "## 按问题清单", ""])
    for (code, title, stage, module, hf), policies in grouped.items():
        flag = "高频" if hf else "普通"
        policy_bits = "；".join(
            f"{p['policy_code']}({p['current_status']})" for p in policies
        )
        lines.append(f"- `{code}` [{flag}] {stage}/{module} {title} -> {policy_bits}")

    lines.extend(
        [
            "",
            "## 处理规则",
            "",
            "- 这些问题不得作为正式上线签收内容直接发布。",
            "- 优先处理高频问题和 `VAT`、`DEC`、`PREF`、`RISK` 模块。",
            "- 每条问题需先替换或补充现行政策依据，再重写结论、适用条件、例外边界和风险提示。",
            "- 完成问题级复核后，才能把相关政策从 `needs_update` 或 `source_found` 提升到 `verified_current`。",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"affected_questions={len(grouped)}")
    print(f"affected_links={len(rows)}")
    print(f"report={REPORT_PATH}")


if __name__ == "__main__":
    main()
