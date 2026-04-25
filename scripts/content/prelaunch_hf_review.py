"""
上线前高频问题复核脚本

作用：
1. 统一高频问题中的旧稳定度枚举 certain_conditional -> certain_condition
2. 合并已识别的高频重复题，保留 canonical 题号，归档重复题
3. 迁移关联问题引用，减少前台重复入口
4. 生成复核报告，便于后续人工复核接手
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "database" / "db" / "tax_knowledge.db"
REPORT_PATH = ROOT / "data" / "reports" / "hf_prelaunch_review_20260422.md"

REVIEWER = "codex-prelaunch-review"
REVIEW_DATE = "2026-04-22"

DEDUP_MAP = {
    "OPR-CIT-031": "OPR-CIT-025",
    "OPR-CIT-032": "OPR-CIT-026",
    "OPR-CIT-033": "OPR-CIT-027",
    "OPR-IIT-025": "OPR-IIT-020",
    "OPR-IIT-028": "OPR-IIT-023",
    "OPR-FEE-027": "OPR-FEE-021",
}


def fetchone(cur: sqlite3.Cursor, sql: str, params=()):
    row = cur.execute(sql, params).fetchone()
    if row is None:
        raise ValueError(f"missing row for query: {sql} {params}")
    return row


def add_log(cur: sqlite3.Cursor, question_id: int, update_type: str, reason: str, summary: str):
    version_no = fetchone(
        cur,
        "SELECT COALESCE(MAX(version_no), 0) + 1 FROM question_update_log WHERE question_id = ?",
        (question_id,),
    )[0]
    cur.execute(
        """
        INSERT INTO question_update_log (
            question_id, version_no, update_date, update_type,
            update_reason, updated_by, reviewed_by, change_summary
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            question_id,
            version_no,
            REVIEW_DATE,
            update_type,
            reason,
            REVIEWER,
            REVIEWER,
            summary,
        ),
    )


def ensure_relation(cur: sqlite3.Cursor, question_id: int, related_id: int, relation_type: str, display_order: int):
    exists = cur.execute(
        """
        SELECT 1 FROM question_relation
        WHERE question_id = ? AND related_id = ? AND relation_type = ?
        """,
        (question_id, related_id, relation_type),
    ).fetchone()
    if not exists:
        cur.execute(
            """
            INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
            VALUES (?, ?, ?, ?)
            """,
            (question_id, related_id, relation_type, display_order),
        )


def merge_duplicate(cur: sqlite3.Cursor, duplicate_code: str, canonical_code: str, actions: list[str]):
    dup = fetchone(
        cur,
        "SELECT id, question_title FROM question_master WHERE question_code = ?",
        (duplicate_code,),
    )
    canonical = fetchone(
        cur,
        "SELECT id, question_title FROM question_master WHERE question_code = ?",
        (canonical_code,),
    )
    dup_id = dup[0]
    canonical_id = canonical[0]

    # 迁移外部指向 duplicate 的关联问题
    incoming_rows = cur.execute(
        """
        SELECT question_id, relation_type, display_order
        FROM question_relation
        WHERE related_id = ?
        """,
        (dup_id,),
    ).fetchall()
    for question_id, relation_type, display_order in incoming_rows:
        if question_id == canonical_id:
            continue
        ensure_relation(cur, question_id, canonical_id, relation_type, display_order)
    cur.execute("DELETE FROM question_relation WHERE related_id = ?", (dup_id,))

    # 清理 duplicate 自己发出的关联
    cur.execute("DELETE FROM question_relation WHERE question_id = ?", (dup_id,))

    # 归档 duplicate
    cur.execute(
        """
        UPDATE question_master
        SET status = 'archived',
            high_frequency_flag = 0,
            newbie_flag = 0,
            updated_at = datetime('now')
        WHERE id = ?
        """,
        (dup_id,),
    )

    add_log(
        cur,
        dup_id,
        "update_status",
        "上线前高频复核去重归档",
        f"与 {canonical_code} 内容重复，归档并将关联入口合并到 canonical 题号。",
    )
    add_log(
        cur,
        canonical_id,
        "update_revise",
        "上线前高频复核去重收口",
        f"合并重复入口 {duplicate_code}，保留 {canonical_code} 作为唯一高频入口。",
    )
    actions.append(f"- 归档重复高频题 `{duplicate_code}`，合并到 `{canonical_code}`")


def normalize_certainty(cur: sqlite3.Cursor, actions: list[str]) -> int:
    rows = cur.execute(
        """
        SELECT id, question_code
        FROM question_master
        WHERE status = 'active'
          AND high_frequency_flag = 1
          AND answer_certainty = 'certain_conditional'
        """
    ).fetchall()
    for question_id, code in rows:
        cur.execute(
            """
            UPDATE question_master
            SET answer_certainty = 'certain_condition',
                updated_at = datetime('now')
            WHERE id = ?
            """,
            (question_id,),
        )
        add_log(
            cur,
            question_id,
            "update_revise",
            "上线前高频复核统一结论稳定度枚举",
            "将 legacy 枚举 certain_conditional 统一为 certain_condition，避免前台与后台口径不一致。",
        )
    if rows:
        actions.append(f"- 统一 {len(rows)} 条高频问题的稳定度枚举：`certain_conditional` -> `certain_condition`")
    return len(rows)


def collect_stats(cur: sqlite3.Cursor):
    return {
        "hf_total": fetchone(
            cur,
            "SELECT COUNT(*) FROM question_master WHERE status = 'active' AND high_frequency_flag = 1",
        )[0],
        "duplicate_titles": cur.execute(
            """
            SELECT question_title, COUNT(*) AS cnt
            FROM question_master
            WHERE status = 'active' AND high_frequency_flag = 1
            GROUP BY question_title
            HAVING cnt > 1
            """
        ).fetchall(),
        "legacy_certainty": fetchone(
            cur,
            """
            SELECT COUNT(*)
            FROM question_master
            WHERE status = 'active' AND high_frequency_flag = 1
              AND answer_certainty = 'certain_conditional'
            """,
        )[0],
    }


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    before = collect_stats(cur)
    actions: list[str] = []

    normalized = normalize_certainty(cur, actions)
    for duplicate_code, canonical_code in DEDUP_MAP.items():
        merge_duplicate(cur, duplicate_code, canonical_code, actions)

    after = collect_stats(cur)
    conn.commit()
    conn.close()

    REPORT_PATH.write_text(
        "\n".join(
            [
                "# 高频问题上线前复核报告",
                "",
                f"- 复核日期：{REVIEW_DATE}",
                f"- 执行人：{REVIEWER}",
                "- 复核范围：全部 active + high_frequency_flag=1 的问题",
                "",
                "## 复核前状态",
                "",
                f"- 高频问题总数：{before['hf_total']}",
                f"- 高频重复标题组数：{len(before['duplicate_titles'])}",
                f"- 高频 legacy 稳定度枚举数：{before['legacy_certainty']}",
                "",
                "## 本轮动作",
                "",
                *actions,
                "",
                "## 复核后状态",
                "",
                f"- 高频问题总数：{after['hf_total']}",
                f"- 高频重复标题组数：{len(after['duplicate_titles'])}",
                f"- 高频 legacy 稳定度枚举数：{after['legacy_certainty']}",
                "",
                "## 结论",
                "",
                "- 高频入口已完成一轮上线前 agent 复核收口。",
                "- 已消除已识别的完全重复高频题入口。",
                "- 已统一高频问题中的旧稳定度枚举口径。",
                "- 后续仍建议对高频专题做人工抽检，以完成正式上线前最后的人审签收。",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"normalized_certainty={normalized}")
    print(f"hf_total_before={before['hf_total']}")
    print(f"hf_total_after={after['hf_total']}")
    print(f"duplicate_groups_before={len(before['duplicate_titles'])}")
    print(f"duplicate_groups_after={len(after['duplicate_titles'])}")
    print(f"report={REPORT_PATH}")


if __name__ == "__main__":
    main()
