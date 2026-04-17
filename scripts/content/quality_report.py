#!/usr/bin/env python3
# ============================================================
# scripts/content/quality_report.py
# 数据质量巡检脚本（增强版）
# 用法: python scripts/content/quality_report.py
# ============================================================

import sqlite3
import sys
import os
from datetime import datetime, timedelta

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'db', 'tax_knowledge.db')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'data', 'reports')

VALID_ANSWER_CERTAINTY = {'certain_clear', 'certain_conditional', 'certain_dispute', 'certain_practice'}
VALID_SCOPE_LEVEL = {'scope_national', 'scope_local', 'scope_mixed'}
VALID_QUESTION_TYPE = {'type_whether', 'type_how', 'type_define', 'type_risk',
                       'type_time', 'type_what', 'type_why',
                       # 以下为历史遗留值（已存在于DB，不应再新增）
                       'type_steps', 'type_clarify', 'type_procedure', 'type_compare'}
VALID_MODULE_CODES = {'REG', 'DEC', 'INV', 'VAT', 'CIT', 'IIT', 'SSF', 'FEE', 'PREF', 'RISK', 'CLEAR', 'ETAX'}
VALID_STAGE_CODES = {'SET', 'OPR', 'CHG', 'RSK', 'SUS', 'CLS'}
VALID_SUPPORT_TYPE = {'support_direct', 'support_aux', 'support_definition',
                      'support_procedure', 'support_risk', 'support_local',
                      # 以下为历史遗留值（已存在于DB，T4政策补强批次导入时使用）
                      'citation'}


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


def get_report_path(prefix):
    today = datetime.now().strftime('%Y%m%d')
    return os.path.join(REPORTS_DIR, f'{prefix}_{today}.txt')


def write_report(path, lines):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


# =============================================================================
# 15 项检查
# =============================================================================

def check01_fk_status(conn):
    """1. FK约束状态"""
    result = conn.execute("PRAGMA foreign_keys").fetchone()
    fk_ok = result[0] == 1
    return fk_ok, result[0]


def check02_code_consistency(conn):
    """2. 代码一致性：question_code 前缀与 module_code/stage_code 匹配"""
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
    return issues


def check03_required_fields(conn):
    """3. 必填字段完整性"""
    required = ['question_title', 'question_plain', 'one_line_answer', 'stage_code',
                'module_code', 'question_type', 'answer_certainty', 'scope_level']
    all_issues = {}
    for field in required:
        rows = conn.execute(f"""
            SELECT question_code, question_title, {field}
            FROM question_master
            WHERE {field} IS NULL OR {field} = ''
        """).fetchall()
        if rows:
            all_issues[field] = rows
    return all_issues


def check04_answer_certainty(conn):
    """4. 答案确定性合理性"""
    rows = conn.execute("""
        SELECT question_code, question_title, answer_certainty
        FROM question_master
    """).fetchall()
    invalid = [r for r in rows if r['answer_certainty'] not in VALID_ANSWER_CERTAINTY]
    return invalid


def check05_scope_level(conn):
    """5. 适用范围合理性"""
    rows = conn.execute("""
        SELECT question_code, question_title, scope_level
        FROM question_master
    """).fetchall()
    invalid = [r for r in rows if r['scope_level'] not in VALID_SCOPE_LEVEL]
    return invalid


def check06_question_type(conn):
    """6. 问题类型合理性"""
    rows = conn.execute("""
        SELECT question_code, question_title, question_type
        FROM question_master
    """).fetchall()
    invalid = [r for r in rows if r['question_type'] not in VALID_QUESTION_TYPE]
    return invalid


def check07_draft_status(conn):
    """7. 草稿状态"""
    rows = conn.execute("""
        SELECT question_code, question_title, status
        FROM question_master
        WHERE status = 'draft'
        ORDER BY question_code
    """).fetchall()
    return rows


def check08_missing_policy(conn):
    """8. 缺少政策依据"""
    rows = conn.execute("""
        SELECT q.question_code, q.question_title, q.stage_code, q.module_code, q.status
        FROM question_master q
        LEFT JOIN question_policy_link p ON q.id = p.question_id
        WHERE p.id IS NULL
    """).fetchall()
    return rows


def check09_missing_tags(conn):
    """9. 缺少业务标签"""
    rows = conn.execute("""
        SELECT q.question_code, q.question_title
        FROM question_master q
        LEFT JOIN question_tag_link t ON q.id = t.question_id
        WHERE t.id IS NULL
    """).fetchall()
    return rows


def check10_orphan_policy_links(conn):
    """10. 孤立政策关联（policy_link 但 policy_dict 里无此 code）"""
    # Get all valid policy_codes from policy_basis
    valid_codes = {r['policy_code'] for r in conn.execute("SELECT policy_code FROM policy_basis").fetchall()}

    rows = conn.execute("""
        SELECT q.question_code, q.question_title,
               pb.policy_code, pb.policy_name, qpl.policy_id
        FROM question_policy_link qpl
        JOIN question_master q ON qpl.question_id = q.id
        JOIN policy_basis pb ON qpl.policy_id = pb.id
    """).fetchall()

    orphan = [r for r in rows if r['policy_code'] not in valid_codes]
    return orphan


def check11_orphan_tag_links(conn):
    """11. 孤立标签关联（tag_link 但 tag_dict 里无此 code）"""
    valid_codes = {r['tag_code'] for r in conn.execute("SELECT tag_code FROM tag_dict").fetchall()}

    rows = conn.execute("""
        SELECT q.question_code, q.question_title,
               td.tag_code, td.tag_name, qtl.tag_id
        FROM question_tag_link qtl
        JOIN question_master q ON qtl.question_id = q.id
        JOIN tag_dict td ON qtl.tag_id = td.id
    """).fetchall()

    orphan = [r for r in rows if r['tag_code'] not in valid_codes]
    return orphan


def check12_duplicate_codes(conn):
    """12. 重复问题代码"""
    rows = conn.execute("""
        SELECT question_code, COUNT(*) as cnt
        FROM question_master
        GROUP BY question_code
        HAVING cnt > 1
    """).fetchall()
    return rows


def check13_type_distribution(conn):
    """13. 类型分布统计"""
    rows = conn.execute("""
        SELECT question_type, COUNT(*) as cnt
        FROM question_master
        GROUP BY question_type
        ORDER BY cnt DESC
    """).fetchall()
    return rows


def check14_stage_module_matrix(conn):
    """14. 阶段×模块覆盖矩阵"""
    rows = conn.execute("""
        SELECT stage_code, module_code, COUNT(*) as cnt
        FROM question_master
        GROUP BY stage_code, module_code
        ORDER BY stage_code, module_code
    """).fetchall()

    all_stages = sorted({r['stage_code'] for r in rows})
    all_modules = sorted({r['module_code'] for r in rows})
    matrix = {}
    for r in rows:
        matrix[(r['stage_code'], r['module_code'])] = r['cnt']

    return rows, all_stages, all_modules, matrix


def check15_stale_content(conn):
    """15. 更新记录缺失（updated_at 为空或 created_at == updated_at）"""
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    rows = conn.execute("""
        SELECT question_code, question_title, created_at, updated_at, status
        FROM question_master
        WHERE updated_at IS NULL
           OR updated_at = ''
           OR updated_at = created_at
           OR updated_at < ?
        ORDER BY updated_at
    """, (one_year_ago,)).fetchall()
    return rows


def check16_support_type(conn):
    """16. support_type 枚举值合法性"""
    rows = conn.execute("""
        SELECT q.question_code, q.question_title, qpl.support_type, qpl.support_note
        FROM question_policy_link qpl
        JOIN question_master q ON q.id = qpl.question_id
    """).fetchall()
    invalid = [r for r in rows if r['support_type'] not in VALID_SUPPORT_TYPE]
    return invalid


def check17_stage_module_domain(conn):
    """17. stage_code / module_code 字典域合法性"""
    # 从 tag_dict 动态获取合法值（而非硬编码）
    valid_stages = {r['tag_code'] for r in conn.execute(
        "SELECT tag_code FROM tag_dict WHERE tag_category='stage'").fetchall()}
    valid_modules = {r['tag_code'] for r in conn.execute(
        "SELECT tag_code FROM tag_dict WHERE tag_category='module'").fetchall()}

    rows = conn.execute("""
        SELECT question_code, stage_code, module_code
        FROM question_master
    """).fetchall()

    bad_stage = [r for r in rows if r['stage_code'] not in valid_stages]
    bad_module = [r for r in rows if r['module_code'] not in valid_modules]
    return bad_stage, bad_module, valid_stages, valid_modules


def generate_quality_report(conn):
    """生成完整质量报告"""
    ensure_reports_dir()
    report_lines = []
    today_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    total = conn.execute("SELECT COUNT(*) FROM question_master").fetchone()[0]
    report_lines.append(f"{'='*60}")
    report_lines.append(f"税务知识库数据质量巡检报告")
    report_lines.append(f"生成时间: {today_str}")
    report_lines.append(f"数据库: {DB_PATH}")
    report_lines.append(f"总问题数: {total} 条")
    report_lines.append(f"{'='*60}")

    # 1. FK约束状态
    fk_ok, fk_val = check01_fk_status(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查1】FK约束状态")
    report_lines.append(f"{'='*60}")
    if fk_ok:
        report_lines.append(f"✅ PRAGMA foreign_keys = {fk_val} (已启用)")
    else:
        report_lines.append(f"❌ PRAGMA foreign_keys = {fk_val} (未启用)")

    # 2. 代码一致性
    code_issues = check02_code_consistency(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查2】代码一致性 (question_code 前缀匹配)")
    report_lines.append(f"{'='*60}")
    if not code_issues:
        report_lines.append(f"✅ 所有 {total} 条问题编码与 stage/module 前缀一致")
    else:
        report_lines.append(f"❌ 发现 {len(code_issues)} 条编码不一致：")
        for i in code_issues[:10]:
            report_lines.append(f"   {i['code']} → stage={i['stage']}, module={i['module']}, 期望前缀: {i['expected']}***")
        if len(code_issues) > 10:
            report_lines.append(f"   ... 还有 {len(code_issues) - 10} 条")

    # 3. 必填字段完整性
    missing_fields = check03_required_fields(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查3】必填字段完整性")
    report_lines.append(f"{'='*60}")
    if not missing_fields:
        report_lines.append(f"✅ 所有必填字段均已填写")
    else:
        total_missing = sum(len(v) for v in missing_fields.values())
        report_lines.append(f"❌ 发现 {total_missing} 处必填字段缺失：")
        for field, rows in missing_fields.items():
            report_lines.append(f"\n   [{field}] {len(rows)} 条缺失：")
            for r in rows[:3]:
                report_lines.append(f"      [{r['question_code']}] {r['question_title'][:40]}")
            if len(rows) > 3:
                report_lines.append(f"      ... 还有 {len(rows) - 3} 条")

    # 4. 答案确定性
    invalid_certainty = check04_answer_certainty(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查4】答案确定性合理性")
    report_lines.append(f"{'='*60}")
    if not invalid_certainty:
        report_lines.append(f"✅ 所有 answer_certainty 值合法")
    else:
        report_lines.append(f"❌ {len(invalid_certainty)} 条 answer_certainty 值不合法：")
        for r in invalid_certainty:
            report_lines.append(f"   [{r['question_code']}] {r['answer_certainty']}")

    # 5. 适用范围
    invalid_scope = check05_scope_level(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查5】适用范围合理性")
    report_lines.append(f"{'='*60}")
    if not invalid_scope:
        report_lines.append(f"✅ 所有 scope_level 值合法")
    else:
        report_lines.append(f"❌ {len(invalid_scope)} 条 scope_level 值不合法：")
        for r in invalid_scope:
            report_lines.append(f"   [{r['question_code']}] {r['scope_level']}")

    # 6. 问题类型
    invalid_types = check06_question_type(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查6】问题类型合理性")
    report_lines.append(f"{'='*60}")
    if not invalid_types:
        report_lines.append(f"✅ 所有 question_type 值合法")
    else:
        report_lines.append(f"❌ {len(invalid_types)} 条 question_type 值不合法：")
        for r in invalid_types:
            report_lines.append(f"   [{r['question_code']}] {r['question_type']}")

    # 7. 草稿状态
    draft_rows = check07_draft_status(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查7】草稿状态问题清单")
    report_lines.append(f"{'='*60}")
    if not draft_rows:
        report_lines.append(f"✅ 无草稿状态问题")
    else:
        report_lines.append(f"⚠️  {len(draft_rows)} 条问题处于 draft 状态：")
        for r in draft_rows:
            report_lines.append(f"   [{r['question_code']}] {r['question_title'][:45]}")

    # 8. 缺少政策依据
    missing_policy = check08_missing_policy(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查8】缺少政策依据的问题")
    report_lines.append(f"{'='*60}")
    if not missing_policy:
        report_lines.append(f"✅ 所有问题均已关联政策依据")
    else:
        report_lines.append(f"⚠️  {len(missing_policy)} 条问题缺少政策依据：")
        for r in missing_policy[:20]:
            report_lines.append(f"   [{r['question_code']}] {r['question_title'][:40]} (stage={r['stage_code']}, module={r['module_code']})")
        if len(missing_policy) > 20:
            report_lines.append(f"   ... 还有 {len(missing_policy) - 20} 条")

    # 9. 缺少业务标签
    missing_tags = check09_missing_tags(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查9】缺少业务标签的问题")
    report_lines.append(f"{'='*60}")
    if not missing_tags:
        report_lines.append(f"✅ 所有问题均已关联标签")
    else:
        report_lines.append(f"❌ {len(missing_tags)} 条问题缺少标签：")
        for r in missing_tags[:20]:
            report_lines.append(f"   [{r['question_code']}] {r['question_title'][:40]}")
        if len(missing_tags) > 20:
            report_lines.append(f"   ... 还有 {len(missing_tags) - 20} 条")

    # 10. 孤立政策关联
    orphan_policy = check10_orphan_policy_links(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查10】孤立政策关联")
    report_lines.append(f"{'='*60}")
    if not orphan_policy:
        report_lines.append(f"✅ 所有政策关联均有效")
    else:
        report_lines.append(f"❌ {len(orphan_policy)} 条政策关联无效：")
        for r in orphan_policy:
            report_lines.append(f"   question={r['question_code']}, policy_id={r['policy_id']}, policy_code={r['policy_code']}")

    # 11. 孤立标签关联
    orphan_tags = check11_orphan_tag_links(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查11】孤立标签关联")
    report_lines.append(f"{'='*60}")
    if not orphan_tags:
        report_lines.append(f"✅ 所有标签关联均有效")
    else:
        report_lines.append(f"❌ {len(orphan_tags)} 条标签关联无效：")
        for r in orphan_tags:
            report_lines.append(f"   question={r['question_code']}, tag_id={r['tag_id']}, tag_code={r['tag_code']}")

    # 12. 重复问题代码
    dup_codes = check12_duplicate_codes(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查12】重复问题代码")
    report_lines.append(f"{'='*60}")
    if not dup_codes:
        report_lines.append(f"✅ 无重复问题代码")
    else:
        report_lines.append(f"❌ {len(dup_codes)} 个问题代码重复：")
        for r in dup_codes:
            report_lines.append(f"   {r['question_code']}: {r['cnt']} 次")

    # 13. 类型分布统计
    type_dist = check13_type_distribution(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查13】问题类型分布统计")
    report_lines.append(f"{'='*60}")
    for r in type_dist:
        pct = r['cnt'] / total * 100 if total > 0 else 0
        report_lines.append(f"   {r['question_type']}: {r['cnt']} 条 ({pct:.1f}%)")

    # 14. 阶段×模块覆盖矩阵
    _, all_stages, all_modules, matrix = check14_stage_module_matrix(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查14】阶段×模块覆盖矩阵")
    report_lines.append(f"{'='*60}")

    # Header
    header = f"{'Stage/Module':<12}"
    for m in all_modules:
        header += f"{m:>8}"
    report_lines.append(header)
    report_lines.append("-" * len(header))

    for s in all_stages:
        row = f"{s:<12}"
        for m in all_modules:
            cnt = matrix.get((s, m), 0)
            row += f"{cnt:>8}"
        report_lines.append(row)

    # 15. 更新记录缺失
    stale_rows = check15_stale_content(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查15】更新记录缺失（长期未更新）")
    report_lines.append(f"{'='*60}")
    if not stale_rows:
        report_lines.append(f"✅ 所有问题均有有效更新记录")
    else:
        report_lines.append(f"⚠️  {len(stale_rows)} 条问题长期未更新（created_at == updated_at 或 updated_at > 1年前）：")
        for r in stale_rows[:20]:
            report_lines.append(f"   [{r['question_code']}] {r['question_title'][:35]} | updated={r['updated_at']}")
        if len(stale_rows) > 20:
            report_lines.append(f"   ... 还有 {len(stale_rows) - 20} 条")

    # 16. support_type 枚举合法性
    invalid_support = check16_support_type(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查16】support_type 枚举值合法性")
    report_lines.append(f"{'='*60}")
    if not invalid_support:
        report_lines.append(f"✅ 所有 policy_link 的 support_type 均为标准值")
    else:
        report_lines.append(f"❌ {len(invalid_support)} 条 support_type 为非法值：")
        for r in invalid_support[:20]:
            report_lines.append(f"   [{r['question_code']}] support_type='{r['support_type']}' note='{r['support_note']}'")
        if len(invalid_support) > 20:
            report_lines.append(f"   ... 还有 {len(invalid_support) - 20} 条")

    # 17. stage_code / module_code 字典域合法性
    bad_stage, bad_module, valid_stages, valid_modules = check17_stage_module_domain(conn)
    report_lines.append(f"\n{'='*60}")
    report_lines.append(f"【检查17】stage_code / module_code 字典域合法性")
    report_lines.append(f"{'='*60}")
    if not bad_stage and not bad_module:
        report_lines.append(f"✅ 所有 stage_code / module_code 均在合法字典内")
    else:
        if bad_stage:
            report_lines.append(f"❌ {len(bad_stage)} 条 stage_code 为非法值：")
            for r in bad_stage[:10]:
                report_lines.append(f"   [{r['question_code']}] stage='{r['stage_code']}' (合法: {sorted(valid_stages)})")
            if len(bad_stage) > 10:
                report_lines.append(f"   ... 还有 {len(bad_stage) - 10} 条")
        if bad_module:
            report_lines.append(f"❌ {len(bad_module)} 条 module_code 为非法值：")
            for r in bad_module[:10]:
                report_lines.append(f"   [{r['question_code']}] module='{r['module_code']}' (合法: {sorted(valid_modules)})")
            if len(bad_module) > 10:
                report_lines.append(f"   ... 还有 {len(bad_module) - 10} 条")

    # ---- 生成子报告 ----

    # missing_policy_report
    if missing_policy:
        mp_lines = [
            f"{'='*60}",
            f"缺政策依据问题清单",
            f"生成时间: {today_str}",
            f"总计: {len(missing_policy)} 条",
            f"{'='*60}",
        ]
        for i, r in enumerate(missing_policy, 1):
            mp_lines.append(f"{i}. [{r['question_code']}] {r['question_title']}")
            mp_lines.append(f"   stage={r['stage_code']}, module={r['module_code']}, status={r['status']}")
        write_report(get_report_path('missing_policy_report'), mp_lines)
        print(f"📄 已生成: missing_policy_report_{datetime.now().strftime('%Y%m%d')}.txt")

    # missing_tags_report
    if missing_tags:
        mt_lines = [
            f"{'='*60}",
            f"缺标签问题清单",
            f"生成时间: {today_str}",
            f"总计: {len(missing_tags)} 条",
            f"{'='*60}",
        ]
        for i, r in enumerate(missing_tags, 1):
            mt_lines.append(f"{i}. [{r['question_code']}] {r['question_title']}")
        write_report(get_report_path('missing_tags_report'), mt_lines)
        print(f"📄 已生成: missing_tags_report_{datetime.now().strftime('%Y%m%d')}.txt")

    # stale_content_report
    if stale_rows:
        sc_lines = [
            f"{'='*60}",
            f"长期未更新问题清单",
            f"生成时间: {today_str}",
            f"判定标准: updated_at 为空 / updated_at == created_at / updated_at 早于1年前",
            f"总计: {len(stale_rows)} 条",
            f"{'='*60}",
        ]
        for i, r in enumerate(stale_rows, 1):
            sc_lines.append(f"{i}. [{r['question_code']}] {r['question_title']}")
            sc_lines.append(f"   created={r['created_at']}, updated={r['updated_at']}, status={r['status']}")
        write_report(get_report_path('stale_content_report'), sc_lines)
        print(f"📄 已生成: stale_content_report_{datetime.now().strftime('%Y%m%d')}.txt")

    # 写入主报告
    write_report(get_report_path('quality_report'), report_lines)
    print(f"📄 已生成: quality_report_{datetime.now().strftime('%Y%m%d')}.txt")

    return report_lines


def main():
    print("=" * 60)
    print("税务知识库数据质量巡检")
    print("=" * 60)

    conn = connect_db()
    try:
        generate_quality_report(conn)
    finally:
        conn.close()

    print("\n✅ 巡检完成，所有报告已生成在 data/reports/ 目录")


if __name__ == '__main__':
    main()
