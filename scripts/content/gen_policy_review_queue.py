#!/usr/bin/env python3
"""生成政策核验优先级队列报告。"""
import sqlite3, os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"
conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()

report_lines = []
report_lines.append('# 政策依据核验队列报告')
report_lines.append('> 生成时间: 2026-04-25')
report_lines.append('> 用途: 按优先级处理阻断政策，人工核验后更新 policy_basis 表')
report_lines.append('')
report_lines.append('## 阻断统计')
report_lines.append('')

statuses = [('needs_update', 'P0: 需联网核查最新政策'), ('source_pending', 'P1: 需补充官方来源'), ('manual_local_review', 'P2: 需地方/人工确认')]
for status, label in statuses:
    count = cur.execute('SELECT COUNT(*) FROM policy_basis WHERE verification_status = ?', (status,)).fetchone()[0]
    total_active_refs = cur.execute('''
        SELECT COUNT(DISTINCT q.question_id)
        FROM policy_basis p
        JOIN question_policy_link q ON p.id = q.policy_id
        JOIN question_master m ON q.question_id = m.id
        WHERE p.verification_status = ? AND m.status = 'active' AND q.support_type = 'citation'
    ''', (status,)).fetchone()[0]
    no_url_count = cur.execute('''
        SELECT COUNT(*) FROM policy_basis
        WHERE verification_status = ? AND (source_url IS NULL OR source_url = '')
    ''', (status,)).fetchone()[0]
    report_lines.append(f'- **{status}** ({count}条政策, {total_active_refs}条active问题引用, {no_url_count}条缺source_url)')
    print(f'{status}: {count} policies, {total_active_refs} active refs, {no_url_count} no url')

report_lines.append('')
report_lines.append('## 优先级处理队列')
report_lines.append('')

for status, label in statuses:
    report_lines.append(f'### {label}')
    report_lines.append('')
    report_lines.append('| policy_code | policy_name | active引用 | source_url | 处理建议 |')
    report_lines.append('|---|---|---|---|---|')

    rows = cur.execute('''
        SELECT p.policy_code, p.policy_name, p.source_url, p.expiry_date,
               COUNT(DISTINCT CASE WHEN m.status = 'active' THEN m.id END) as active_refs
        FROM policy_basis p
        LEFT JOIN question_policy_link q ON p.id = q.policy_id AND q.support_type = 'citation'
        LEFT JOIN question_master m ON q.question_id = m.id
        WHERE p.verification_status = ?
        GROUP BY p.id
        ORDER BY active_refs DESC
    ''', (status,)).fetchall()
    for r in rows:
        code, name, url, expiry, refs = r
        url_str = f'[{url}]({url})' if url else '`无`'
        name_esc = name.replace('|', '\\|')
        if status == 'needs_update':
            suggestion = '联网核查2024-2025新政策是否已替代'
        elif status == 'source_pending':
            suggestion = '补充官方来源或标注地方官网'
        else:
            suggestion = '查询广西/柳州主管税务机关口径'
        report_lines.append(f'| {code} | {name_esc} | {refs} | {url_str} | {suggestion} |')
    report_lines.append('')

conn.close()

os.makedirs("data/reports", exist_ok=True)
report_path = "data/reports/policy_review_queue_20260425.md"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))
print(f'\n报告已生成: {report_path}')
print(f'行数: {len(report_lines)}')
