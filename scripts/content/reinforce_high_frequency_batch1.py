#!/usr/bin/env python3
"""补强首批高频问题的政策依据、业务标签和关联问题。"""

import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "database" / "db" / "tax_knowledge.db"


PLAN = {
    "OPR-IIT-002": {
        "policies": [
            ("POL-WHT-003", "support_procedure", "补充代扣代缴口径"),
        ],
        "tags": ["tag_payment", "tag_withholding"],
        "relations": [
            ("OPR-IIT-005", "similar"),
            ("OPR-IIT-001", "see_also"),
        ],
    },
    "SET-IIT-001": {
        "policies": [
            ("POL-WHT-003", "support_procedure", "补充首次扣缴申报口径"),
        ],
        "tags": ["tag_first_tax", "tag_withholding"],
        "relations": [
            ("SET-IIT-003", "next_step"),
            ("OPR-IIT-001", "see_also"),
        ],
    },
    "CLS-DEC-004": {
        "policies": [
            ("GOV-CLS-001", "support_procedure", "补充注销登记程序依据"),
            ("GOV-CIT-002", "support_direct", "补充清算所得税处理依据"),
        ],
        "tags": ["tag_简易注销", "tag_一般注销", "tag_税务注销"],
        "relations": [
            ("OPR-CLEAR-003", "similar"),
            ("CLS-DEC-003", "see_also"),
        ],
    },
    "OPR-CLEAR-003": {
        "policies": [
            ("GOV-Tax-001", "support_aux", "补充税务注销的一般义务依据"),
        ],
        "tags": ["tag_简易注销", "tag_一般注销", "tag_税务注销"],
        "relations": [
            ("CLS-CLEAR-016", "similar"),
            ("CLS-DEC-004", "see_also"),
        ],
    },
    "OPR-DEC-004": {
        "policies": [
            ("POL-RISK-001", "support_risk", "补充长期零申报的风险处理依据"),
        ],
        "tags": ["tag_zero_report", "tag_risk_warning"],
        "relations": [
            ("OPR-DEC-012", "next_step"),
            ("OPR-DEC-013", "similar"),
        ],
    },
    "SET-DEC-004": {
        "policies": [
            ("SAT-VAT-002", "support_direct", "补充一般纳税人认定规则"),
        ],
        "tags": ["tag_small_scale", "tag_general_taxpayer"],
        "relations": [
            ("SET-DEC-005", "see_also"),
            ("OPR-TAX-021", "related"),
        ],
    },
    "OPR-IIT-005": {
        "policies": [
            ("POL-WHT-003", "support_procedure", "补充工资薪金扣缴口径"),
        ],
        "tags": ["tag_payment", "tag_withholding"],
        "relations": [
            ("OPR-IIT-002", "similar"),
            ("OPR-IIT-001", "see_also"),
        ],
    },
    "OPR-INV-005": {
        "policies": [
            ("POL-INV-002", "support_direct", "补充专票与普票使用规则"),
        ],
        "tags": ["tag_invoice", "tag_vat_special"],
        "relations": [
            ("OPR-INV-012", "similar"),
            ("OPR-INV-026", "see_also"),
        ],
    },
    "OPR-INV-026": {
        "policies": [
            ("POL-INV-002", "support_direct", "补充专票法律效力与使用规则"),
        ],
        "tags": ["tag_invoice", "tag_vat_special"],
        "relations": [
            ("OPR-INV-005", "similar"),
            ("OPR-INV-012", "see_also"),
        ],
    },
    "OPR-RISK-002": {
        "policies": [
            ("POL-RISK-001", "support_direct", "补充非正常户认定与解除规则"),
            ("SAT-RISK-001", "support_risk", "补充纳税信用影响口径"),
        ],
        "tags": ["tag_risk_warning", "tag_credit_rating"],
        "relations": [
            ("RSK-RISK-001", "similar"),
            ("RSK-RISK-003", "next_step"),
        ],
    },
}


def fetch_map(conn, sql):
    return {row[0]: row[1] for row in conn.execute(sql).fetchall()}


def ensure_policy_link(conn, question_id, policy_id, support_type, support_note):
    exists = conn.execute(
        """
        SELECT id FROM question_policy_link
        WHERE question_id = ? AND policy_id = ? AND support_type = ?
        """,
        (question_id, policy_id, support_type),
    ).fetchone()
    if exists:
        return False

    next_order = conn.execute(
        "SELECT COALESCE(MAX(display_order), 0) + 1 FROM question_policy_link WHERE question_id = ?",
        (question_id,),
    ).fetchone()[0]
    conn.execute(
        """
        INSERT INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order)
        VALUES (?, ?, ?, ?, ?)
        """,
        (question_id, policy_id, support_type, support_note, next_order),
    )
    return True


def ensure_tag_link(conn, question_id, tag_id):
    exists = conn.execute(
        "SELECT id FROM question_tag_link WHERE question_id = ? AND tag_id = ?",
        (question_id, tag_id),
    ).fetchone()
    if exists:
        return False

    next_order = conn.execute(
        "SELECT COALESCE(MAX(display_order), 0) + 1 FROM question_tag_link WHERE question_id = ?",
        (question_id,),
    ).fetchone()[0]
    conn.execute(
        """
        INSERT INTO question_tag_link (question_id, tag_id, is_primary, display_order)
        VALUES (?, ?, 0, ?)
        """,
        (question_id, tag_id, next_order),
    )
    return True


def ensure_relation(conn, question_id, related_id, relation_type):
    exists = conn.execute(
        """
        SELECT id FROM question_relation
        WHERE question_id = ? AND related_id = ?
        """,
        (question_id, related_id),
    ).fetchone()
    if exists:
        return False

    next_order = conn.execute(
        "SELECT COALESCE(MAX(display_order), 0) + 1 FROM question_relation WHERE question_id = ?",
        (question_id,),
    ).fetchone()[0]
    conn.execute(
        """
        INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
        VALUES (?, ?, ?, ?)
        """,
        (question_id, related_id, relation_type, next_order),
    )
    return True


def add_update_log(conn, question_id, version_no, summary):
    conn.execute(
        """
        INSERT INTO question_update_log (
            question_id, version_no, update_date, update_type,
            update_reason, updated_by, change_summary
        ) VALUES (?, ?, CURRENT_TIMESTAMP, 'update_revise', ?, 'system_reinforce', ?)
        """,
        (question_id, version_no, summary, summary),
    )


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    question_map = fetch_map(conn, "SELECT question_code, id FROM question_master")
    tag_map = fetch_map(conn, "SELECT tag_code, id FROM tag_dict")
    policy_map = fetch_map(conn, "SELECT policy_code, id FROM policy_basis")
    version_map = fetch_map(conn, "SELECT question_code, version_no FROM question_master")

    changes = {"policy": 0, "tag": 0, "relation": 0, "question": 0}

    try:
        for question_code, spec in PLAN.items():
            question_id = question_map[question_code]
            question_changed = False

            for policy_code, support_type, note in spec["policies"]:
                if ensure_policy_link(conn, question_id, policy_map[policy_code], support_type, note):
                    changes["policy"] += 1
                    question_changed = True

            for tag_code in spec["tags"]:
                if ensure_tag_link(conn, question_id, tag_map[tag_code]):
                    changes["tag"] += 1
                    question_changed = True

            for related_code, relation_type in spec["relations"]:
                if ensure_relation(conn, question_id, question_map[related_code], relation_type):
                    changes["relation"] += 1
                    question_changed = True

            if question_changed:
                conn.execute(
                    "UPDATE question_master SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (question_id,),
                )
                add_update_log(
                    conn,
                    question_id,
                    version_map[question_code],
                    "高频问题补强：补充政策依据、业务标签和关联问题",
                )
                changes["question"] += 1

        conn.commit()
    finally:
        conn.close()

    print("high_frequency_batch1")
    for key, value in changes.items():
        print(f"{key}_changes={value}")


if __name__ == "__main__":
    main()
