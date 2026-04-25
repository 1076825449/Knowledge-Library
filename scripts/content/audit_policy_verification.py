#!/usr/bin/env python3
"""Audit official-source verification coverage for active question policies."""

import sqlite3
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"
REPORT_PATH = PROJECT_ROOT / "data" / "reports" / "policy_verification_audit_20260423.md"


UNSAFE_STATUS = {
    "unverified",
    "source_found",
    "needs_update",
    "uncertain",
    "source_pending",
    "manual_local_review",
}


def ensure_columns(conn):
    existing = {row[1] for row in conn.execute("PRAGMA table_info(policy_basis)")}
    required = {"source_url", "source_org", "last_verified_at", "verification_status", "verification_note"}
    missing = required - existing
    if missing:
        raise SystemExit(
            "policy_basis 缺少核验字段，请先执行 scripts/content/verify_policy_sources_batch1.py "
            f"或数据库迁移 004。缺失: {', '.join(sorted(missing))}"
        )


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    ensure_columns(conn)

    summary = dict(
        conn.execute(
            """
            SELECT verification_status, COUNT(*) cnt
            FROM policy_basis
            GROUP BY verification_status
            """
        ).fetchall()
    )
    active_total = conn.execute("SELECT COUNT(*) FROM question_master WHERE status = 'active'").fetchone()[0]
    linked_policy_total = conn.execute(
        """
        SELECT COUNT(DISTINCT pb.id)
        FROM policy_basis pb
        JOIN question_policy_link qpl ON qpl.policy_id = pb.id
        JOIN question_master q ON q.id = qpl.question_id
        WHERE q.status = 'active'
        """
    ).fetchone()[0]
    no_url_count = conn.execute(
        """
        SELECT COUNT(DISTINCT pb.id)
        FROM policy_basis pb
        JOIN question_policy_link qpl ON qpl.policy_id = pb.id
        JOIN question_master q ON q.id = qpl.question_id
        WHERE q.status = 'active'
          AND (pb.source_url IS NULL OR trim(pb.source_url) = '')
        """
    ).fetchone()[0]

    top_unverified = conn.execute(
        """
        SELECT
            pb.policy_code,
            pb.policy_name,
            pb.document_no,
            COALESCE(pb.verification_status, 'unverified') AS verification_status,
            COALESCE(pb.current_status, '') AS current_status,
            COUNT(DISTINCT q.id) AS active_question_count,
            SUM(CASE WHEN q.high_frequency_flag = 1 THEN 1 ELSE 0 END) AS hf_link_count
        FROM policy_basis pb
        JOIN question_policy_link qpl ON qpl.policy_id = pb.id
        JOIN question_master q ON q.id = qpl.question_id
        WHERE q.status = 'active'
          AND COALESCE(pb.verification_status, 'unverified') IN ('unverified', 'source_found', 'needs_update', 'uncertain', 'source_pending', 'manual_local_review')
        GROUP BY pb.id
        ORDER BY
            CASE COALESCE(pb.verification_status, 'unverified')
                WHEN 'needs_update' THEN 1
                WHEN 'source_pending' THEN 2
                WHEN 'manual_local_review' THEN 3
                WHEN 'unverified' THEN 4
                WHEN 'source_found' THEN 5
                ELSE 4
            END,
            active_question_count DESC,
            hf_link_count DESC,
            pb.policy_code
        LIMIT 80
        """
    ).fetchall()

    exposed_questions = conn.execute(
        """
        SELECT
            q.question_code,
            q.question_title,
            q.stage_code,
            q.module_code,
            q.high_frequency_flag,
            COUNT(DISTINCT pb.id) AS policy_count,
            SUM(CASE WHEN COALESCE(pb.verification_status, 'unverified') = 'verified_current' THEN 1 ELSE 0 END) AS verified_count,
            SUM(CASE WHEN COALESCE(pb.verification_status, 'unverified') = 'needs_update' THEN 1 ELSE 0 END) AS needs_update_count
        FROM question_master q
        JOIN question_policy_link qpl ON qpl.question_id = q.id
        JOIN policy_basis pb ON pb.id = qpl.policy_id
        WHERE q.status = 'active'
        GROUP BY q.id
        HAVING verified_count = 0 OR needs_update_count > 0
        ORDER BY q.high_frequency_flag DESC, needs_update_count DESC, q.module_code, q.question_code
        LIMIT 120
        """
    ).fetchall()

    lines = [
        "# 政策依据联网核验审计报告",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 数据库：{DB_PATH}",
        f"- active 问题数：{active_total}",
        f"- active 问题引用的政策数：{linked_policy_total}",
        f"- active 引用政策中缺官方 source_url：{no_url_count}",
        "",
        "## 核验状态分布（policy_basis 全库）",
        "",
    ]
    for status in sorted(summary):
        lines.append(f"- `{status}`: {summary[status]}")

    lines.extend(
        [
            "",
            "## 优先核验政策队列",
            "",
            "排序规则：先处理 `needs_update`，再处理无官方来源/未核验，且按 active 问题引用量和高频题引用量排序。",
            "",
        ]
    )
    for row in top_unverified:
        lines.append(
            f"- `{row['policy_code']}` {row['policy_name']}（{row['document_no'] or '无文号'}）："
            f"`{row['verification_status']}` / `{row['current_status']}`，"
            f"active 引用 {row['active_question_count']}，高频引用 {row['hf_link_count']}"
        )

    lines.extend(["", "## 受影响 active 问题抽检队列", ""])
    for row in exposed_questions:
        hf = "高频" if row["high_frequency_flag"] else "普通"
        lines.append(
            f"- `{row['question_code']}` [{hf}] {row['question_title']}："
            f"{row['stage_code']}/{row['module_code']}，政策数 {row['policy_count']}，"
            f"已核验 {row['verified_count']}，需更新依据 {row['needs_update_count']}"
        )

    lines.extend(
        [
            "",
            "## 执行口径",
            "",
            "- `source_found` 只表示已找到官方来源，不等于问题答案已按现行口径复核通过。",
            "- `needs_update` 表示政策或申报口径已发现新变化，相关问题不得作为正式上线内容直接发布。",
            "- `source_pending` 表示该依据已纳入全库复核，但尚未找到稳定官方来源或现行状态。",
            "- `manual_local_review` 表示地方口径必须由对应地区官方渠道人工确认。",
            "- `verified_current` 只能在人工核对政策现行状态、条款引用、答案边界后三项均通过时使用。",
            "- 新增问题必须至少绑定一个带官方 `source_url` 的政策依据；高频问题必须完成逐条人工复核。",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"active_total={active_total}")
    print(f"linked_policy_total={linked_policy_total}")
    print(f"active_linked_policies_missing_source_url={no_url_count}")
    print(f"priority_policy_items={len(top_unverified)}")
    print(f"exposed_question_items={len(exposed_questions)}")
    print(f"report={REPORT_PATH}")


if __name__ == "__main__":
    main()
