#!/usr/bin/env python3
"""补强第四批高频问题：清空高频问题第二条政策缺口。"""

import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "database" / "db" / "tax_knowledge.db"


POLICY_PLAN = {
    "OPR-INV-003": ("POL-INV-001", "support_definition", "补充发票管理的一般规则"),
    "OPR-INV-004": ("POL-VAT-001", "support_direct", "补充小规模纳税人开具专票的增值税依据"),
    "OPR-RISK-010": ("GOV-Tax-001", "support_risk", "补充税务风险管理的一般义务"),
    "OPR-SSF-001": ("GOV-Tax-001", "support_aux", "补充依法申报缴费的一般义务"),
    "OPR-SSF-004": ("GOV-Tax-001", "support_aux", "补充依法缴费与征收的一般义务"),
    "OPR-SSF-023": ("GOV-Tax-001", "support_procedure", "补充日常申报缴费的一般程序义务"),
    "OPR-VAT-007": ("POL-INV-004", "support_procedure", "补充专票丢失处理规则"),
    "OPR-VAT-017": ("POL-PREF-009", "support_direct", "补充小规模纳税人免税政策"),
    "OPR-VAT-018": ("POL-VAT-003", "support_direct", "补充出口退税相关增值税优惠口径"),
    "RSK-RISK-017": ("GOV-PEN-001", "support_risk", "补充逾期不缴的处罚规则"),
    "RSK-RISK-025": ("GOV-PEN-001", "support_aux", "补充执法程序与权利救济规则"),
    "RSK-VAT-001": ("POL-RISK-003", "support_direct", "补充异常扣税凭证处理规则"),
    "RSK-VAT-002": ("GOV-PEN-001", "support_risk", "补充欠税强制执行的处罚程序"),
    "SET-DEC-002": ("SAT-VAT-004", "support_procedure", "补充首次申报的申报规则"),
    "SET-DEC-003": ("POL-CIT-001", "support_direct", "补充企业所得税申报义务"),
    "SET-DEC-005": ("POL-PREF-009", "support_aux", "补充小规模纳税人优惠比较口径"),
    "SET-DEC-006": ("GOV-Tax-001", "support_procedure", "补充首次申报的一般义务"),
    "SET-INV-001": ("POL-INV-001", "support_direct", "补充首次领票与发票管理规则"),
    "SET-INV-002": ("GOV-Tax-002", "support_procedure", "补充首次领票资料与登记流程"),
    "SET-REG-003": ("SAT-2024-033", "support_procedure", "补充新办企业税务办理优化流程"),
    "SET-REG-004": ("SAT-2024-033", "support_procedure", "补充新办企业信息报告与后续办理流程"),
    "SET-REG-005": ("SAT-DEC-006", "support_procedure", "补充税费种认定便利化规则"),
    "SET-REG-007": ("SAT-2024-033", "support_procedure", "补充营业执照后涉税事项办理流程"),
    "SET-REG-008": ("GOV-Tax-001", "support_risk", "补充逾期办理登记申报责任"),
    "SET-REG-009": ("SAT-2024-033", "support_definition", "补充三证合一后的税务登记衔接规则"),
    "SET-REG-010": ("SAT-DEC-006", "support_procedure", "补充税费种认定操作规则"),
    "SET-REG-014": ("SAT-2024-033", "support_definition", "补充设立登记与变更登记衔接规则"),
    "SET-VAT-002": ("SAT-VAT-002", "support_procedure", "补充一般纳税人申请认定规则"),
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
    changes = 0

    try:
        for question_code, (policy_code, support_type, note) in POLICY_PLAN.items():
            if ensure_policy_link(
                conn,
                question_map[question_code],
                policy_map[policy_code],
                support_type,
                note,
            ):
                changes += 1
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
                "高频问题补强：补齐第二条政策依据",
            )

        conn.commit()
    finally:
        conn.close()

    print("high_frequency_batch4")
    print(f"policy_changes={changes}")
    print(f"question_changes={len(touched)}")


if __name__ == "__main__":
    main()
