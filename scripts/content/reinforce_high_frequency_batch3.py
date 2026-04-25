#!/usr/bin/env python3
"""补强第三批高频问题：继续压政策缺口并清最后 1 条关联缺口。"""

import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "database" / "db" / "tax_knowledge.db"


POLICY_PLAN = {
    "OPR-IIT-025": [("SAT-IIT-001", "support_procedure", "补充个税汇算申报规则")],
    "OPR-IIT-028": [("SAT-IIT-002", "support_direct", "补充全年一次性奖金计税规则")],
    "OPR-INV-001": [("POL-INV-003", "support_direct", "补充退款冲红的发票处理规则")],
    "OPR-INV-003": [("POL-INV-003", "support_direct", "补充红字发票开具规则")],
    "OPR-INV-004": [("POL-INV-002", "support_direct", "补充专用发票使用规则")],
    "OPR-INV-006": [("POL-INV-003", "support_direct", "补充已认证专票红冲规则")],
    "OPR-INV-007": [("POL-INV-004", "support_procedure", "补充专票认证与丢失处理规则")],
    "OPR-INV-011": [("POL-INV-002", "support_procedure", "补充专票领用与开具资格规则")],
    "OPR-INV-012": [("POL-INV-002", "support_direct", "补充普票与专票使用规则")],
    "OPR-INV-013": [("POL-INV-003", "support_definition", "补充红字发票适用情形")],
    "OPR-INV-014": [("POL-INV-003", "support_direct", "补充作废与红冲处理规则")],
    "OPR-INV-027": [("POL-INV-003", "support_direct", "补充作废与红冲的边界规则")],
    "OPR-RISK-001": [("POL-RISK-001", "support_risk", "补充非正常户认定与后果依据")],
    "OPR-RISK-008": [("POL-INV-003", "support_procedure", "补充发票红冲处理规则")],
    "OPR-SSF-001": [("POL-SSF-001", "support_direct", "补充社保费征缴与登记义务")],
    "OPR-SSF-002": [("GOV-PEN-001", "support_risk", "补充未履行法定义务的处罚风险")],
    "OPR-SSF-004": [("POL-SSF-001", "support_direct", "补充社保缴费基数的一般规则")],
    "OPR-SSF-022": [("POL-SSF-001", "support_procedure", "补充社保费申报征收规则")],
    "RSK-RISK-016": [("POL-WHT-003", "support_direct", "补充个税代扣代缴义务依据")],
    "RSK-RISK-017": [("POL-SSF-001", "support_direct", "补充社保费欠缴责任依据")],
}

RELATION_PLAN = {
    "SET-INV-001": [("SET-INV-004", "next_step")],
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
    version_map = fetch_map(conn, "SELECT question_code, version_no FROM question_master")

    touched = set()
    policy_changes = 0
    relation_changes = 0

    try:
        for question_code, items in POLICY_PLAN.items():
            question_id = question_map[question_code]
            for policy_code, support_type, note in items:
                if ensure_policy_link(conn, question_id, policy_map[policy_code], support_type, note):
                    policy_changes += 1
                    touched.add(question_code)

        for question_code, items in RELATION_PLAN.items():
            question_id = question_map[question_code]
            for related_code, relation_type in items:
                if ensure_relation(conn, question_id, question_map[related_code], relation_type):
                    relation_changes += 1
                    touched.add(question_code)

        for question_code in sorted(touched):
            question_id = question_map[question_code]
            conn.execute(
                "UPDATE question_master SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (question_id,),
            )
            add_update_log(
                conn,
                question_id,
                version_map[question_code],
                "高频问题补强：继续补政策依据并打通发票/社保/个税链路",
            )

        conn.commit()
    finally:
        conn.close()

    print("high_frequency_batch3")
    print(f"policy_changes={policy_changes}")
    print(f"relation_changes={relation_changes}")
    print(f"question_changes={len(touched)}")


if __name__ == "__main__":
    main()
