#!/usr/bin/env python3
"""补强第二批高频问题：补第二条政策、清标签缺口和关联缺口。"""

import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "database" / "db" / "tax_knowledge.db"


POLICY_PLAN = {
    "OPR-CIT-002": [("SAT-SSF-001", "support_direct", "补充境外支付源泉扣缴规则")],
    "OPR-CIT-003": [("SAT-SSF-001", "support_direct", "补充非居民企业源泉扣缴规则")],
    "OPR-CIT-008": [("POL-CIT-001", "support_direct", "补充企业所得税年度申报义务")],
    "OPR-CIT-027": [("POL-CIT-001", "support_direct", "补充亏损弥补基本规则")],
    "OPR-CIT-033": [("POL-CIT-001", "support_direct", "补充亏损弥补基本规则")],
    "OPR-DEC-001": [("SAT-VAT-004", "support_procedure", "补充零申报的申报口径")],
    "OPR-DEC-003": [("SAT-VAT-004", "support_procedure", "补充按月按季申报口径")],
    "OPR-DEC-005": [("POL-PREF-009", "support_direct", "补充小规模纳税人免税额度规则")],
    "OPR-DEC-011": [("GOV-Tax-001", "support_definition", "补充申报义务的一般规则")],
    "OPR-DEC-012": [("GOV-Tax-001", "support_procedure", "补充零申报的一般申报依据")],
    "OPR-DEC-013": [("POL-RISK-001", "support_risk", "补充长期零申报的风险处理依据")],
    "OPR-FEE-001": [("SAT-CIT-001", "support_direct", "补充税前扣除凭证规则")],
    "OPR-FEE-002": [("SAT-CIT-001", "support_direct", "补充外部凭证税前扣除规则")],
    "OPR-FEE-003": [("SAT-CIT-001", "support_direct", "补充报销与税前扣除凭证规则")],
    "OPR-FEE-021": [("POL-CIT-001", "support_direct", "补充业务招待费税前扣除限制")],
    "OPR-FEE-027": [("POL-CIT-001", "support_direct", "补充业务招待费税前扣除限制")],
    "OPR-IIT-001": [("POL-WHT-003", "support_procedure", "补充工资薪金扣缴规则")],
    "OPR-IIT-004": [("SAT-IIT-002", "support_direct", "补充全年一次性奖金计税规则")],
    "OPR-IIT-020": [("SAT-IIT-001", "support_procedure", "补充个税汇算申报规则")],
    "OPR-IIT-023": [("SAT-IIT-002", "support_direct", "补充全年一次性奖金计税规则")],
}

TAG_PLAN = {
    "OPR-CIT-004": ["tag_withholding", "tag_payment"],
    "RSK-RISK-029": ["tag_invoice"],
}

RELATION_PLAN = {
    "OPR-PREF-005": [("OPR-ETAX-002", "next_step")],
    "OPR-PREF-011": [("OPR-DEC-005", "similar")],
    "OPR-SSF-002": [("OPR-SSF-015", "see_also")],
    "RSK-RISK-015": [("RSK-TAX-009", "related")],
    "RSK-RISK-016": [("OPR-IIT-001", "prerequisite")],
    "RSK-RISK-017": [("OPR-SSF-015", "prerequisite")],
    "RSK-RISK-027": [("RSK-TAX-009", "similar")],
    "RSK-VAT-001": [("RSK-INV-002", "similar")],
    "RSK-VAT-002": [("OPR-RISK-012", "related")],
    "SET-INV-001": [("OPR-INV-002", "next_step")],
    "SET-REG-004": [("SET-REG-005", "next_step")],
    "SUS-VAT-001": [("SUS-DEC-001", "similar")],
}


def fetch_map(conn, sql):
    return {row[0]: row[1] for row in conn.execute(sql).fetchall()}


def ensure_policy_link(conn, question_id, policy_id, support_type, support_note):
    exists = conn.execute(
        """
        SELECT 1 FROM question_policy_link
        WHERE question_id = ? AND policy_id = ? AND support_type = ?
        """,
        (question_id, policy_id, support_type),
    ).fetchone()
    if exists:
        return False

    display_order = conn.execute(
        "SELECT COALESCE(MAX(display_order), 0) + 1 FROM question_policy_link WHERE question_id = ?",
        (question_id,),
    ).fetchone()[0]
    conn.execute(
        """
        INSERT INTO question_policy_link (question_id, policy_id, support_type, support_note, display_order)
        VALUES (?, ?, ?, ?, ?)
        """,
        (question_id, policy_id, support_type, support_note, display_order),
    )
    return True


def ensure_tag_link(conn, question_id, tag_id):
    exists = conn.execute(
        "SELECT 1 FROM question_tag_link WHERE question_id = ? AND tag_id = ?",
        (question_id, tag_id),
    ).fetchone()
    if exists:
        return False

    display_order = conn.execute(
        "SELECT COALESCE(MAX(display_order), 0) + 1 FROM question_tag_link WHERE question_id = ?",
        (question_id,),
    ).fetchone()[0]
    conn.execute(
        """
        INSERT INTO question_tag_link (question_id, tag_id, is_primary, display_order)
        VALUES (?, ?, 0, ?)
        """,
        (question_id, tag_id, display_order),
    )
    return True


def ensure_relation(conn, question_id, related_id, relation_type):
    exists = conn.execute(
        "SELECT 1 FROM question_relation WHERE question_id = ? AND related_id = ?",
        (question_id, related_id),
    ).fetchone()
    if exists:
        return False

    display_order = conn.execute(
        "SELECT COALESCE(MAX(display_order), 0) + 1 FROM question_relation WHERE question_id = ?",
        (question_id,),
    ).fetchone()[0]
    conn.execute(
        """
        INSERT INTO question_relation (question_id, related_id, relation_type, display_order)
        VALUES (?, ?, ?, ?)
        """,
        (question_id, related_id, relation_type, display_order),
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
    policy_map = fetch_map(conn, "SELECT policy_code, id FROM policy_basis")
    tag_map = fetch_map(conn, "SELECT tag_code, id FROM tag_dict")
    version_map = fetch_map(conn, "SELECT question_code, version_no FROM question_master")

    question_touched = set()
    changes = {"policy": 0, "tag": 0, "relation": 0}

    try:
        for question_code, items in POLICY_PLAN.items():
            question_id = question_map[question_code]
            for policy_code, support_type, note in items:
                if ensure_policy_link(conn, question_id, policy_map[policy_code], support_type, note):
                    changes["policy"] += 1
                    question_touched.add(question_code)

        for question_code, tag_codes in TAG_PLAN.items():
            question_id = question_map[question_code]
            for tag_code in tag_codes:
                if ensure_tag_link(conn, question_id, tag_map[tag_code]):
                    changes["tag"] += 1
                    question_touched.add(question_code)

        for question_code, items in RELATION_PLAN.items():
            question_id = question_map[question_code]
            for related_code, relation_type in items:
                if ensure_relation(conn, question_id, question_map[related_code], relation_type):
                    changes["relation"] += 1
                    question_touched.add(question_code)

        for question_code in sorted(question_touched):
            question_id = question_map[question_code]
            conn.execute(
                "UPDATE question_master SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (question_id,),
            )
            add_update_log(
                conn,
                question_id,
                version_map[question_code],
                "高频问题补强：补第二条政策、清标签缺口并补关联问题",
            )

        conn.commit()
    finally:
        conn.close()

    print("high_frequency_batch2")
    print(f"policy_changes={changes['policy']}")
    print(f"tag_changes={changes['tag']}")
    print(f"relation_changes={changes['relation']}")
    print(f"question_changes={len(question_touched)}")


if __name__ == "__main__":
    main()
