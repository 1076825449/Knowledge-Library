#!/usr/bin/env python3
"""Fail deployment/readiness when active content uses unsafe policy basis."""

import sqlite3
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"
BLOCKING_STATUSES = ("needs_update", "source_pending", "manual_local_review", "unverified")


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT
            q.question_code,
            q.question_title,
            q.high_frequency_flag,
            GROUP_CONCAT(DISTINCT pb.policy_code || ':' || COALESCE(pb.verification_status, 'unverified')) AS policies
        FROM question_master q
        JOIN question_policy_link qpl ON qpl.question_id = q.id
        JOIN policy_basis pb ON pb.id = qpl.policy_id
        WHERE q.status = 'active'
          AND COALESCE(pb.verification_status, 'unverified') IN (
              'needs_update', 'source_pending', 'manual_local_review', 'unverified'
          )
        GROUP BY q.id
        ORDER BY q.high_frequency_flag DESC, q.question_code
        """
    ).fetchall()
    if not rows:
        print("policy_launch_gate=PASS")
        return 0

    hf_count = sum(1 for row in rows if row["high_frequency_flag"])
    print("policy_launch_gate=FAIL")
    print(f"blocking_statuses={','.join(BLOCKING_STATUSES)}")
    print(f"blocked_active_questions={len(rows)}")
    print(f"blocked_high_frequency_questions={hf_count}")
    print("examples:")
    for row in rows[:20]:
        print(f"- {row['question_code']} {row['question_title']} -> {row['policies']}")
    if len(rows) > 20:
        print(f"... {len(rows) - 20} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())
