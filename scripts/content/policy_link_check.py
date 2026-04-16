#!/usr/bin/env python3
# ============================================================
# scripts/content/policy_link_check.py
# 专项检查：缺政策依据的问题
# 用法: python scripts/content/policy_link_check.py
# ============================================================

import sqlite3
import sys
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'db', 'tax_knowledge.db')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'data', 'reports')

HIGH_PRIORITY_MODULES = {'OPR'}
MEDIUM_PRIORITY_MODULES = {'SET', 'DEC'}


def connect_db():
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库文件不存在: {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def ensure_reports_dir():
    os.makedirs(REPORTS_DIR, exist_ok=True)


def get_priority(module_code):
    if module_code in HIGH_PRIORITY_MODULES:
        return "🔴 高优先级"
    elif module_code in MEDIUM_PRIORITY_MODULES:
        return "🟡 中优先级"
    else:
        return "⚪ 低优先级"


def check_missing_policy_links(conn):
    """查出所有缺少政策依据的问题，并标注优先级"""
    rows = conn.execute("""
        SELECT q.question_code, q.question_title, q.stage_code, q.module_code, q.status
        FROM question_master q
        LEFT JOIN question_policy_link p ON q.id = p.question_id
        WHERE p.id IS NULL
        ORDER BY
            CASE q.module_code
                WHEN 'OPR' THEN 1
                WHEN 'SET' THEN 2
                WHEN 'DEC' THEN 3
                ELSE 4
            END,
            q.question_code
    """).fetchall()

    return rows


def generate_report(rows):
    ensure_reports_dir()
    today = datetime.now().strftime('%Y%m%d')
    today_full = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report_path = os.path.join(REPORTS_DIR, f'missing_policy_report_{today}.txt')

    lines = []
    lines.append("=" * 70)
    lines.append("缺政策依据问题清单")
    lines.append(f"生成时间: {today_full}")
    lines.append(f"数据库: {DB_PATH}")
    lines.append("=" * 70)
    lines.append("")

    if not rows:
        lines.append("✅ 所有问题均已关联政策依据，无缺失项")
    else:
        high = [(r, get_priority(r['module_code'])) for r in rows if r['module_code'] in HIGH_PRIORITY_MODULES]
        med = [(r, get_priority(r['module_code'])) for r in rows if r['module_code'] in MEDIUM_PRIORITY_MODULES]
        low = [(r, get_priority(r['module_code'])) for r in rows if r['module_code'] not in HIGH_PRIORITY_MODULES and r['module_code'] not in MEDIUM_PRIORITY_MODULES]

        lines.append(f"总计: {len(rows)} 条问题缺少政策依据")
        lines.append(f"  🔴 高优先级 (OPR模块): {len(high)} 条")
        lines.append(f"  🟡 中优先级 (SET/DEC模块): {len(med)} 条")
        lines.append(f"  ⚪ 低优先级 (其他模块): {len(low)} 条")
        lines.append("")
        lines.append("-" * 70)

        # High priority
        if high:
            lines.append("")
            lines.append("🔴 高优先级 (OPR模块 — 无依据为高优先级):")
            lines.append("-" * 70)
            for r, _ in high:
                lines.append(f"  [{r['question_code']}]")
                lines.append(f"    标题: {r['question_title']}")
                lines.append(f"    阶段: {r['stage_code']} | 模块: {r['module_code']} | 状态: {r['status']}")
                lines.append("")

        # Medium priority
        if med:
            lines.append("")
            lines.append("🟡 中优先级 (SET/DEC模块):")
            lines.append("-" * 70)
            for r, _ in med:
                lines.append(f"  [{r['question_code']}]")
                lines.append(f"    标题: {r['question_title']}")
                lines.append(f"    阶段: {r['stage_code']} | 模块: {r['module_code']} | 状态: {r['status']}")
                lines.append("")

        # Low priority
        if low:
            lines.append("")
            lines.append("⚪ 低优先级 (其他模块):")
            lines.append("-" * 70)
            for r, _ in low:
                lines.append(f"  [{r['question_code']}]")
                lines.append(f"    标题: {r['question_title']}")
                lines.append(f"    阶段: {r['stage_code']} | 模块: {r['module_code']} | 状态: {r['status']}")
                lines.append("")

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return report_path


def main():
    print("=" * 60)
    print("缺政策依据专项检查")
    print("=" * 60)

    conn = connect_db()
    try:
        rows = check_missing_policy_links(conn)
        path = generate_report(rows)

        print(f"\n📄 报告已生成: {path}")
        print(f"\n检查结果: {len(rows)} 条问题缺少政策依据")

        if rows:
            print("\n优先级分布:")
            high = sum(1 for r in rows if r['module_code'] in HIGH_PRIORITY_MODULES)
            med = sum(1 for r in rows if r['module_code'] in MEDIUM_PRIORITY_MODULES)
            low = len(rows) - high - med
            print(f"  🔴 高优先级 (OPR): {high} 条")
            print(f"  🟡 中优先级 (SET/DEC): {med} 条")
            print(f"  ⚪ 低优先级 (其他): {low} 条")

    finally:
        conn.close()

    print("\n✅ 检查完成")


if __name__ == '__main__':
    main()
