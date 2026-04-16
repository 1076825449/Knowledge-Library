#!/usr/bin/env python3
# ============================================================
# scripts/content/audit_data.py
# 数据审计脚本 - 检查知识库数据质量问题
# 用法: python scripts/content/audit_data.py
# ============================================================

import sqlite3
import sys
import os
from datetime import datetime

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'db', 'tax_knowledge.db')


def connect_db():
    """连接数据库"""
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库文件不存在: {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def check_foreign_keys(conn):
    """检查1: 外键启用状态"""
    print("\n" + "=" * 60)
    print("【检查1】外键启用状态")
    print("=" * 60)
    result = conn.execute("PRAGMA foreign_keys").fetchone()
    fk_enabled = result[0] == 1
    if fk_enabled:
        print("✅ 外键约束已启用")
    else:
        print("❌ 外键约束未启用（PRAGMA foreign_keys = 0）")
    return fk_enabled


def check_code_consistency(conn):
    """检查2: 问题编码与 stage/module 一致性"""
    print("\n" + "=" * 60)
    print("【检查2】问题编码与 stage/module 分类一致性")
    print("=" * 60)
    rows = conn.execute("""
        SELECT question_code, stage_code, module_code
        FROM question_master
        ORDER BY question_code
    """).fetchall()

    issues = []
    for r in rows:
        expected_prefix = f"{r['stage_code']}-{r['module_code']}-"
        if not r['question_code'].startswith(expected_prefix):
            issues.append({
                'code': r['question_code'],
                'stage': r['stage_code'],
                'module': r['module_code'],
                'expected': expected_prefix
            })

    if not issues:
        print(f"✅ 所有 {len(rows)} 条问题编码与分类一致")
    else:
        print(f"❌ 发现 {len(issues)} 条编码不一致：")
        for i in issues:
            print(f"   {i['code']} → stage={i['stage']}, module={i['module']}, 编码应为 {i['expected']}***")
    return issues


def check_missing_one_line_answer(conn):
    """检查3: 缺失一句话结论"""
    print("\n" + "=" * 60)
    print("【检查3】缺失 one_line_answer 的问题")
    print("=" * 60)
    rows = conn.execute("""
        SELECT question_code, question_title, one_line_answer
        FROM question_master
        WHERE one_line_answer IS NULL OR one_line_answer = ''
    """).fetchall()

    if not rows:
        print("✅ 所有问题均有一句话结论")
    else:
        print(f"❌ 发现 {len(rows)} 条缺失 one_line_answer：")
        for r in rows:
            print(f"   [{r['question_code']}] {r['question_title'][:40]}")
    return rows


def check_missing_policy_links(conn):
    """检查4: 缺少政策依据的问题"""
    print("\n" + "=" * 60)
    print("【检查4】缺少政策依据的问题")
    print("=" * 60)
    rows = conn.execute("""
        SELECT q.question_code, q.question_title, q.status
        FROM question_master q
        LEFT JOIN question_policy_link p ON q.id = p.question_id
        WHERE p.id IS NULL
    """).fetchall()

    if not rows:
        print("✅ 所有问题均已关联政策依据")
    else:
        print(f"⚠️  发现 {len(rows)} 条问题缺少政策依据：")
        for r in rows:
            print(f"   [{r['question_code']}] {r['question_title'][:40]} (status={r['status']})")
    return rows


def check_missing_tags(conn):
    """检查5: 缺少标签的问题"""
    print("\n" + "=" * 60)
    print("【检查5】缺少标签的问题")
    print("=" * 60)
    rows = conn.execute("""
        SELECT q.question_code, q.question_title
        FROM question_master q
        LEFT JOIN question_tag_link t ON q.id = t.question_id
        WHERE t.id IS NULL
    """).fetchall()

    if not rows:
        print("✅ 所有问题均已关联标签")
    else:
        print(f"❌ 发现 {len(rows)} 条问题缺少标签：")
        for r in rows:
            print(f"   [{r['question_code']}] {r['question_title'][:40]}")
    return rows


def check_draft_questions(conn):
    """检查6: 非 active 状态的问题"""
    print("\n" + "=" * 60)
    print("【检查6】非 active 状态的问题")
    print("=" * 60)
    rows = conn.execute("""
        SELECT question_code, question_title, status
        FROM question_master
        WHERE status != 'active'
        ORDER BY status
    """).fetchall()

    if not rows:
        print("✅ 所有问题均为 active 状态")
    else:
        print(f"⚠️  发现 {len(rows)} 条非 active 状态：")
        for r in rows:
            print(f"   [{r['question_code']}] status={r['status']} | {r['question_title'][:40]}")
    return rows


def check_empty_key_fields(conn):
    """检查7: 核心字段为空的问题"""
    print("\n" + "=" * 60)
    print("【检查7】核心字段为空的问题")
    print("=" * 60)
    fields = [
        ('detailed_answer', '详细解答'),
        ('core_definition', '核心定义'),
        ('applicable_conditions', '适用条件'),
        ('exceptions_boundary', '例外与边界'),
        ('practical_steps', '实务步骤'),
        ('risk_warning', '风险提示'),
    ]

    all_issues = {}
    for field, label in fields:
        rows = conn.execute(f"""
            SELECT question_code, question_title
            FROM question_master
            WHERE {field} IS NULL OR {field} = ''
        """).fetchall()
        if rows:
            all_issues[field] = (label, rows)

    if not all_issues:
        print("✅ 所有问题核心字段均已填写")
    else:
        total = sum(len(v[1]) for v in all_issues.values())
        print(f"⚠️  发现 {total} 条问题存在空字段：")
        for field, (label, rows) in all_issues.items():
            print(f"\n   [{label}] {len(rows)} 条问题缺失：")
            for r in rows[:3]:
                print(f"      [{r['question_code']}] {r['question_title'][:35]}")
            if len(rows) > 3:
                print(f"      ... 还有 {len(rows) - 3} 条")
    return all_issues


def check_scope_level_distribution(conn):
    """检查8: scope_level 分布"""
    print("\n" + "=" * 60)
    print("【检查8】scope_level 适用范围分布")
    print("=" * 60)
    rows = conn.execute("""
        SELECT scope_level, COUNT(*) as cnt
        FROM question_master
        GROUP BY scope_level
        ORDER BY cnt DESC
    """).fetchall()

    total = sum(r['cnt'] for r in rows)
    for r in rows:
        pct = r['cnt'] / total * 100 if total > 0 else 0
        print(f"   {r['scope_level']}: {r['cnt']} 条 ({pct:.1f}%)")

    national_only = all(r['scope_level'] == 'scope_national' for r in rows)
    if national_only:
        print("⚠️  所有问题均为全国性，缺少地方性数据（scope_local / scope_mixed）")
    return rows


def check_answer_certainty_distribution(conn):
    """检查9: 结论稳定度分布"""
    print("\n" + "=" * 60)
    print("【检查9】结论稳定度分布")
    print("=" * 60)
    rows = conn.execute("""
        SELECT answer_certainty, COUNT(*) as cnt
        FROM question_master
        GROUP BY answer_certainty
        ORDER BY cnt DESC
    """).fetchall()

    total = sum(r['cnt'] for r in rows)
    for r in rows:
        pct = r['cnt'] / total * 100 if total > 0 else 0
        print(f"   {r['answer_certainty']}: {r['cnt']} 条 ({pct:.1f}%)")
    return rows


def check_question_type_distribution(conn):
    """检查10: 问题类型分布"""
    print("\n" + "=" * 60)
    print("【检查10】问题类型分布")
    print("=" * 60)
    rows = conn.execute("""
        SELECT question_type, COUNT(*) as cnt
        FROM question_master
        GROUP BY question_type
        ORDER BY cnt DESC
    """).fetchall()

    total = sum(r['cnt'] for r in rows)
    for r in rows:
        pct = r['cnt'] / total * 100 if total > 0 else 0
        print(f"   {r['question_type']}: {r['cnt']} 条 ({pct:.1f}%)")

    # 检查是否有未定义类型
    valid_types = {'type_whether', 'type_how', 'type_define', 'type_risk', 'type_time'}
    found_types = {r['question_type'] for r in rows}
    unknown = found_types - valid_types
    if unknown:
        print(f"⚠️  存在未定义的问题类型: {unknown}")
    return rows


def check_lifecycle_coverage(conn):
    """检查11: 生命周期阶段覆盖"""
    print("\n" + "=" * 60)
    print("【检查11】生命周期阶段覆盖")
    print("=" * 60)
    rows = conn.execute("""
        SELECT q.stage_code, t.tag_name, COUNT(*) as cnt
        FROM question_master q
        JOIN tag_dict t ON q.stage_code = t.tag_code AND t.tag_category = 'stage'
        GROUP BY q.stage_code
        ORDER BY t.display_order
    """).fetchall()

    all_stages = conn.execute("""
        SELECT tag_code FROM tag_dict WHERE tag_category = 'stage' ORDER BY display_order
    """).fetchall()
    all_stage_codes = {r['tag_code'] for r in all_stages}
    covered = {r['stage_code'] for r in rows}

    for r in rows:
        print(f"   {r['stage_code']} ({r['tag_name']}): {r['cnt']} 条")

    missing = all_stage_codes - covered
    if missing:
        print(f"⚠️  缺少以下阶段: {missing}")
    return rows, missing


def check_module_coverage(conn):
    """检查12: 主题模块覆盖"""
    print("\n" + "=" * 60)
    print("【检查12】主题模块覆盖")
    print("=" * 60)
    rows = conn.execute("""
        SELECT q.module_code, t.tag_name, COUNT(*) as cnt
        FROM question_master q
        JOIN tag_dict t ON q.module_code = t.tag_code AND t.tag_category = 'module'
        GROUP BY q.module_code
        ORDER BY t.display_order
    """).fetchall()

    all_modules = conn.execute("""
        SELECT tag_code FROM tag_dict WHERE tag_category = 'module' ORDER BY display_order
    """).fetchall()
    all_module_codes = {r['tag_code'] for r in all_modules}
    covered = {r['module_code'] for r in rows}

    for r in rows:
        print(f"   {r['module_code']} ({r['tag_name']}): {r['cnt']} 条")

    missing = all_module_codes - covered
    if missing:
        print(f"⚠️  缺少以下模块: {missing}")
    return rows, missing


def check_orphan_relations(conn):
    """检查13: 孤儿关联问题（关联了不存在的问题）"""
    print("\n" + "=" * 60)
    print("【检查13】孤儿关联问题")
    print("=" * 60)
    rows = conn.execute("""
        SELECT qr.id, qr.question_id, qr.related_id
        FROM question_relation qr
        LEFT JOIN question_master q1 ON qr.question_id = q1.id
        LEFT JOIN question_master q2 ON qr.related_id = q2.id
        WHERE q1.id IS NULL OR q2.id IS NULL
    """).fetchall()

    if not rows:
        print("✅ 所有关联问题均有效")
    else:
        print(f"❌ 发现 {len(rows)} 条孤儿关联：")
        for r in rows:
            print(f"   id={r['id']}, question_id={r['question_id']}, related_id={r['related_id']}")
    return rows


def check_orphan_policy_links(conn):
    """检查14: 孤儿政策关联"""
    print("\n" + "=" * 60)
    print("【检查14】孤儿政策关联")
    print("=" * 60)
    rows = conn.execute("""
        SELECT qpl.id, qpl.question_id, qpl.policy_id
        FROM question_policy_link qpl
        LEFT JOIN question_master q ON qpl.question_id = q.id
        LEFT JOIN policy_basis p ON qpl.policy_id = p.id
        WHERE q.id IS NULL OR p.id IS NULL
    """).fetchall()

    if not rows:
        print("✅ 所有政策关联均有效")
    else:
        print(f"❌ 发现 {len(rows)} 条孤儿政策关联：")
        for r in rows:
            print(f"   id={r['id']}, question_id={r['question_id']}, policy_id={r['policy_id']}")
    return rows


def print_summary(all_results):
    """打印汇总"""
    print("\n" + "=" * 60)
    print("【汇总】数据质量报告")
    print("=" * 60)

    total_questions = all_results.get('total_questions', 0)
    issues_count = (
        len(all_results.get('code_issues', [])) +
        len(all_results.get('missing_policies', [])) +
        len(all_results.get('missing_tags', [])) +
        sum(len(v[1]) for v in all_results.get('empty_fields', {}).values())
    )

    print(f"问题总数：{total_questions}")
    print(f"数据质量异常项：{issues_count}")
    print()
    print("优先级 P0（必须修复）：")
    if all_results.get('code_issues'):
        print(f"  ❌ 编码不一致: {len(all_results['code_issues'])} 条")
    if not all_results.get('foreign_keys'):
        print(f"  ❌ 外键未启用")
    if all_results.get('orphan_relations'):
        print(f"  ❌ 孤儿关联: {len(all_results['orphan_relations'])} 条")
    if all_results.get('orphan_policies'):
        print(f"  ❌ 孤儿政策关联: {len(all_results['orphan_policies'])} 条")

    print()
    print("优先级 P1（应该修复）：")
    if all_results.get('missing_policies'):
        print(f"  ⚠️  缺政策依据: {len(all_results['missing_policies'])} 条")
    if all_results.get('draft_questions'):
        print(f"  ⚠️  非active状态: {len(all_results['draft_questions'])} 条")
    if all_results.get('missing_tags'):
        print(f"  ⚠️  缺标签: {len(all_results['missing_tags'])} 条")

    print()
    print("优先级 P2（改进项）：")
    if all_results.get('empty_fields'):
        empty_total = sum(len(v[1]) for v in all_results['empty_fields'].values())
        print(f"  ⚠️  核心字段为空: {empty_total} 处")


def main():
    print("=" * 60)
    print(f"税务知识库数据审计报告")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"数据库: {DB_PATH}")
    print("=" * 60)

    conn = connect_db()

    all_results = {}

    # 总问题数
    total = conn.execute("SELECT COUNT(*) FROM question_master").fetchone()[0]
    all_results['total_questions'] = total
    print(f"\n总问题数: {total} 条")

    # 执行各项检查
    all_results['foreign_keys'] = check_foreign_keys(conn)
    all_results['code_issues'] = check_code_consistency(conn)
    all_results['missing_one_line'] = check_missing_one_line_answer(conn)
    all_results['missing_policies'] = check_missing_policy_links(conn)
    all_results['missing_tags'] = check_missing_tags(conn)
    all_results['draft_questions'] = check_draft_questions(conn)
    all_results['empty_fields'] = check_empty_key_fields(conn)
    all_results['scope_dist'] = check_scope_level_distribution(conn)
    all_results['certainty_dist'] = check_answer_certainty_distribution(conn)
    all_results['type_dist'] = check_question_type_distribution(conn)
    lc, missing_lc = check_lifecycle_coverage(conn)
    all_results['lifecycle'] = lc
    all_results['lifecycle_missing'] = missing_lc
    mod, missing_mod = check_module_coverage(conn)
    all_results['module'] = mod
    all_results['module_missing'] = missing_mod
    all_results['orphan_relations'] = check_orphan_relations(conn)
    all_results['orphan_policies'] = check_orphan_policy_links(conn)

    print_summary(all_results)

    conn.close()
    print("\n✅ 审计完成")


if __name__ == '__main__':
    main()
