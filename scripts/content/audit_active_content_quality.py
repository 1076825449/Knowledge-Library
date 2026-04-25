#!/usr/bin/env python3
"""Heuristic quality audit for active question cards."""

import re
import sqlite3
from collections import defaultdict
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"
REPORT_PATH = PROJECT_ROOT / "data" / "reports" / "active_content_quality_audit_20260423.md"


GENERIC_PATTERNS = [
    "扩展复核",
    "不能只看单一页面或单一凭证",
    "这类问题看起来只是一个",
    "不应只看单一页面或单一凭证",
]


def text_len(value):
    return len((value or "").strip())


def normalize_title(title):
    title = re.sub(r"[？?。！!，,、：:；;\s]+", "", title or "")
    title = title.replace("企业", "").replace("公司", "")
    return title


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT *
        FROM question_master
        WHERE status = 'active'
        ORDER BY question_code
        """
    ).fetchall()

    policy_counts = {
        row["question_id"]: row["cnt"]
        for row in conn.execute(
            """
            SELECT question_id, count(*) cnt
            FROM question_policy_link
            GROUP BY question_id
            """
        )
    }
    tag_counts = {
        row["question_id"]: row["cnt"]
        for row in conn.execute(
            """
            SELECT question_id, count(*) cnt
            FROM question_tag_link
            GROUP BY question_id
            """
        )
    }
    relation_counts = {
        row["question_id"]: row["cnt"]
        for row in conn.execute(
            """
            SELECT question_id, count(*) cnt
            FROM question_relation
            GROUP BY question_id
            """
        )
    }

    findings = defaultdict(list)
    normalized = defaultdict(list)
    for row in rows:
        code = row["question_code"]
        title = row["question_title"] or ""
        combined = "\n".join(
            str(row[k] or "")
            for k in [
                "question_title",
                "question_plain",
                "one_line_answer",
                "detailed_answer",
                "core_definition",
                "applicable_conditions",
                "exceptions_boundary",
                "practical_steps",
                "risk_warning",
            ]
        )

        normalized[normalize_title(title)].append((code, title))

        if any(pattern in combined for pattern in GENERIC_PATTERNS):
            findings["模板化或泛化表述残留"].append((code, title))
        if "扩展复核" in title:
            findings["标题含扩展复核"].append((code, title))
        if ("（" in title and "）" not in title) or ("(" in title and ")" not in title):
            findings["标题疑似截断或括号未闭合"].append((code, title))
        if title.endswith(("、", "，", "：", "专", "所", "等")):
            findings["标题结尾疑似截断"].append((code, title))
        if text_len(row["detailed_answer"]) < 80:
            findings["详细解答过短"].append((code, title))
        if text_len(row["applicable_conditions"]) < 20:
            findings["适用条件过短"].append((code, title))
        if text_len(row["exceptions_boundary"]) < 20:
            findings["例外边界过短"].append((code, title))
        if text_len(row["practical_steps"]) < 30:
            findings["实务步骤过短"].append((code, title))
        if text_len(row["risk_warning"]) < 30:
            findings["风险提示过短"].append((code, title))
        if policy_counts.get(row["id"], 0) < 1:
            findings["缺政策依据"].append((code, title))
        elif policy_counts.get(row["id"], 0) < 2 and row["high_frequency_flag"]:
            findings["高频题政策依据少于2条"].append((code, title))
        if tag_counts.get(row["id"], 0) < 1:
            findings["缺标签"].append((code, title))
        if relation_counts.get(row["id"], 0) < 1:
            findings["缺关联问题"].append((code, title))

    for key, items in normalized.items():
        if key and len(items) > 1:
            findings["疑似重复题名"].extend(items)

    lines = [
        "# Active 内容质量审计报告",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- active 问题数：{len(rows)}",
        f"- 审计维度：模板化残留、标题截断、字段长度、政策依据、标签、关联、疑似重复",
        "",
        "## 汇总",
        "",
    ]
    if not findings:
        lines.append("- 未发现启发式质量问题。")
    else:
        for name in sorted(findings):
            lines.append(f"- {name}: {len(findings[name])}")
    lines.append("")

    for name in sorted(findings):
        lines.append(f"## {name}")
        lines.append("")
        for code, title in findings[name][:120]:
            lines.append(f"- `{code}` {title}")
        if len(findings[name]) > 120:
            lines.append(f"- ... 还有 {len(findings[name]) - 120} 条")
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"active_total={len(rows)}")
    for name in sorted(findings):
        print(f"{name}: {len(findings[name])}")
    print(f"report={REPORT_PATH}")


if __name__ == "__main__":
    main()
