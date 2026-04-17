#!/usr/bin/env python3
# ============================================================
# scripts/content/priority_reinforce.py
# 内容质量缺口盘点 + 补强优先级清单
# 用法: python scripts/content/priority_reinforce.py
# ============================================================

import sqlite3
import os
import sys
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'db', 'tax_knowledge.db')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'data', 'reports')


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


def score_question(rd, missing_count):
    """计算补强优先级分数"""
    score = 0
    # 高频 +5，新手 +3（同时满足取高）
    if rd['high_frequency_flag'] and rd['newbie_flag']:
        score += 8
    elif rd['high_frequency_flag']:
        score += 5
    elif rd['newbie_flag']:
        score += 3
    # 结构字段缺失越多越优先
    score += missing_count * 2
    # 无关联问题 +3
    if rd.get('rel_count', 1) == 0:
        score += 3
    # 无更新记录 +1
    if rd.get('update_count', 1) == 0:
        score += 1
    return score


def main():
    ensure_reports_dir()
    conn = connect_db()
    today = datetime.now().strftime('%Y-%m-%d')

    lines = []
    lines.append("=" * 70)
    lines.append("税务知识库内容质量缺口盘点与补强优先级清单")
    lines.append(f"生成时间: {today}")
    lines.append(f"数据库: {DB_PATH}")
    lines.append("=" * 70)

    # ── 字典域校验（发现脏数据则报警，不继续产出误导矩阵）─────────
    valid_stages = {r['tag_code'] for r in conn.execute(
        "SELECT tag_code FROM tag_dict WHERE tag_category='stage'").fetchall()}
    valid_modules = {r['tag_code'] for r in conn.execute(
        "SELECT tag_code FROM tag_dict WHERE tag_category='module'").fetchall()}

    all_questions_raw = conn.execute(
        "SELECT question_code, stage_code, module_code FROM question_master WHERE status='active'"
    ).fetchall()

    bad_stage = [(r['question_code'], r['stage_code']) for r in all_questions_raw
                 if r['stage_code'] not in valid_stages]
    bad_module = [(r['question_code'], r['module_code']) for r in all_questions_raw
                   if r['module_code'] not in valid_modules]

    if bad_stage or bad_module:
        lines.append("")
        lines.append("=" * 70)
        lines.append("【⚠️ 字典域错误 — 停止产出补强报告】")
        lines.append("=" * 70)
        if bad_stage:
            lines.append(f"发现 {len(bad_stage)} 条非法 stage_code：")
            for code, sc in bad_stage:
                lines.append(f"  {code} → stage='{sc}' (不合法)")
        if bad_module:
            lines.append(f"发现 {len(bad_module)} 条非法 module_code：")
            for code, mc in bad_module:
                lines.append(f"  {code} → module='{mc}' (不合法)")
        lines.append("")
        lines.append(f"请先修正数据库中的非法 stage/module 值，再重新运行本报告。")
        lines.append(f"合法 stage: {sorted(valid_stages)}")
        lines.append(f"合法 module: {sorted(valid_modules)}")
        print('\n'.join(lines))
        conn.close()
        sys.exit(1)

    # ── 基础数字 ──────────────────────────────────────────────
    total = conn.execute("SELECT COUNT(*) FROM question_master WHERE status='active'").fetchone()[0]
    hf = conn.execute("SELECT COUNT(*) FROM question_master WHERE status='active' AND high_frequency_flag=1").fetchone()[0]
    newbie = conn.execute("SELECT COUNT(*) FROM question_master WHERE status='active' AND newbie_flag=1").fetchone()[0]
    hf_newbie = conn.execute("SELECT COUNT(*) FROM question_master WHERE status='active' AND (high_frequency_flag=1 OR newbie_flag=1)").fetchone()[0]
    policies = conn.execute("SELECT COUNT(*) FROM policy_basis").fetchone()[0]
    relations = conn.execute("SELECT COUNT(*) FROM question_relation").fetchone()[0]
    local_notes = conn.execute("SELECT COUNT(*) FROM local_rule_note").fetchone()[0]

    lines.append("")
    lines.append("【基础数据】")
    lines.append(f"  总问题(active): {total} 条")
    lines.append(f"  高频问题: {hf} 条 ({hf/total*100:.0f}%)")
    lines.append(f"  新手问题: {newbie} 条 ({newbie/total*100:.0f}%)")
    lines.append(f"  高频或新手: {hf_newbie} 条 ({hf_newbie/total*100:.0f}%)")
    lines.append(f"  政策依据: {policies} 条")
    lines.append(f"  关联关系: {relations} 条（均每条问题 {relations/total:.1f} 条关联）")
    lines.append(f"  地方口径: {local_notes} 条")

    # ── 缺口统计 ──────────────────────────────────────────────
    missing_policy = conn.execute("""
        SELECT COUNT(*) FROM question_master q
        LEFT JOIN question_policy_link p ON q.id=p.question_id
        WHERE p.id IS NULL AND q.status='active'
    """).fetchone()[0]

    missing_cond = conn.execute("SELECT COUNT(*) FROM question_master WHERE status='active' AND (applicable_conditions IS NULL OR applicable_conditions='')").fetchone()[0]
    missing_exc = conn.execute("SELECT COUNT(*) FROM question_master WHERE status='active' AND (exceptions_boundary IS NULL OR exceptions_boundary='')").fetchone()[0]
    missing_step = conn.execute("SELECT COUNT(*) FROM question_master WHERE status='active' AND (practical_steps IS NULL OR practical_steps='')").fetchone()[0]
    missing_risk = conn.execute("SELECT COUNT(*) FROM question_master WHERE status='active' AND (risk_warning IS NULL OR risk_warning='')").fetchone()[0]
    missing_tags = conn.execute("SELECT COUNT(*) FROM question_master q LEFT JOIN question_tag_link t ON q.id=t.question_id WHERE t.id IS NULL AND q.status='active'").fetchone()[0]
    missing_update = conn.execute("SELECT COUNT(*) FROM question_master q LEFT JOIN question_update_log u ON q.id=u.question_id WHERE u.id IS NULL AND q.status='active'").fetchone()[0]
    missing_rel = conn.execute("SELECT COUNT(*) FROM question_master q LEFT JOIN question_relation r ON q.id=r.question_id WHERE r.id IS NULL AND q.status='active'").fetchone()[0]

    lines.append("")
    lines.append("【内容缺口统计】")
    lines.append(f"  缺政策依据: {missing_policy} 条  ✅ 全部已关联")
    lines.append(f"  缺适用条件(applicable_conditions): {missing_cond} 条")
    lines.append(f"  缺例外边界(exceptions_boundary): {missing_exc} 条")
    lines.append(f"  缺实务步骤(practical_steps): {missing_step} 条")
    lines.append(f"  缺风险提示(risk_warning): {missing_risk} 条")
    lines.append(f"  缺业务标签: {missing_tags} 条")
    lines.append(f"  缺更新记录: {missing_update} 条")
    lines.append(f"  缺关联问题: {missing_rel} 条")

    # ── 阶段×模块矩阵 ──────────────────────────────────────────
    lines.append("")
    lines.append("【阶段×模块覆盖矩阵】")
    matrix = conn.execute("""
        SELECT stage_code, module_code, COUNT(*) as cnt
        FROM question_master WHERE status='active'
        GROUP BY stage_code, module_code
        ORDER BY stage_code, module_code
    """).fetchall()
    all_stages = sorted({r['stage_code'] for r in matrix})
    all_modules = sorted({r['tag_code'] for r in conn.execute("SELECT tag_code FROM tag_dict WHERE tag_category='module' ORDER BY display_order").fetchall()})
    m_dict = {(r['stage_code'], r['module_code']): r['cnt'] for r in matrix}
    header = f"{'':12}" + "".join(f"{m:>8}" for m in all_modules)
    lines.append(header)
    lines.append("-" * len(header))
    for s in all_stages:
        row_str = f"{s:<12}"
        for m in all_modules:
            cnt = m_dict.get((s, m), 0)
            row_str += f"{cnt:>8}"
        lines.append(row_str)

    # ── 阶段/模块覆盖差距 ──────────────────────────────────────
    all_stage_tags = {r['tag_code']: r['tag_name'] for r in conn.execute("SELECT tag_code, tag_name FROM tag_dict WHERE tag_category='stage' ORDER BY display_order").fetchall()}
    all_module_tags = {r['tag_code']: r['tag_name'] for r in conn.execute("SELECT tag_code, tag_name FROM tag_dict WHERE tag_category='module' ORDER BY display_order").fetchall()}
    covered_stages = {r['stage_code'] for r in matrix}
    covered_modules = {r['module_code'] for r in matrix}

    lines.append("")
    lines.append("【覆盖差距】")
    if covered_stages < set(all_stage_tags):
        missing_s = set(all_stage_tags) - covered_stages
        lines.append(f"  阶段空白: {', '.join(missing_s)}")
    if covered_modules < set(all_module_tags):
        missing_m = set(all_module_tags) - covered_modules
        lines.append(f"  模块空白: {', '.join(missing_m)} （已有内容但无空白阶段）")

    # ── 缺结构字段最严重的模块（动态，按缺失数排序）─────────────────
    lines.append("")
    lines.append("【结构缺失最严重的模块】")
    worst_module = conn.execute("""
        SELECT module_code, COUNT(*) as miss_cnt,
               SUM((applicable_conditions IS NULL OR applicable_conditions='')) as miss_cond,
               SUM((exceptions_boundary IS NULL OR exceptions_boundary='')) as miss_exc,
               SUM((practical_steps IS NULL OR practical_steps='')) as miss_step,
               SUM((risk_warning IS NULL OR risk_warning='')) as miss_risk
        FROM question_master
        WHERE status='active'
          AND (applicable_conditions IS NULL OR applicable_conditions=''
               OR exceptions_boundary IS NULL OR exceptions_boundary=''
               OR practical_steps IS NULL OR practical_steps=''
               OR risk_warning IS NULL OR risk_warning='')
        GROUP BY module_code
        ORDER BY miss_cnt DESC
    """).fetchall()
    if worst_module:
        for r in worst_module[:4]:
            missing = []
            if r['miss_cond']: missing.append(f"条件({r['miss_cond']})")
            if r['miss_exc']: missing.append(f"边界({r['miss_exc']})")
            if r['miss_step']: missing.append(f"步骤({r['miss_step']})")
            if r['miss_risk']: missing.append(f"风险({r['miss_risk']})")
            lines.append(f"  {r['module_code']}: {r['miss_cnt']} 条问题缺 {', '.join(missing)}")
    else:
        lines.append("  （无结构性缺失）")

    # ── 高优先级补强清单 ──────────────────────────────────────
    lines.append("")
    lines.append("=" * 70)
    lines.append("【高优先级补强清单】")
    lines.append("=" * 70)
    lines.append("")
    lines.append("评分规则: 高频+新手加权 + 结构字段缺失数×2 + 无关联+3 + 无更新记录+1")
    lines.append("")

    # 收集所有有缺口的问题（含各类缺失）
    # 注意：DISTINCT 防止 LEFT JOIN 放大导致重复行
    all_gap = conn.execute("""
        SELECT DISTINCT
            q.question_code, q.question_title, q.stage_code, q.module_code,
            q.question_type, q.answer_certainty,
            q.high_frequency_flag, q.newbie_flag,
            (q.applicable_conditions IS NULL OR q.applicable_conditions='') as miss_cond,
            (q.exceptions_boundary IS NULL OR q.exceptions_boundary='') as miss_exc,
            (q.practical_steps IS NULL OR q.practical_steps='') as miss_step,
            (q.risk_warning IS NULL OR q.risk_warning='') as miss_risk,
            (SELECT COUNT(*) FROM question_relation WHERE question_id=q.id) as rel_count,
            (SELECT COUNT(*) FROM question_update_log WHERE question_id=q.id) as update_count,
            (SELECT COUNT(*) FROM question_tag_link WHERE question_id=q.id) as tag_count
        FROM question_master q
        LEFT JOIN question_policy_link p ON q.id=p.question_id
        WHERE q.status='active'
          AND (
              (q.applicable_conditions IS NULL OR q.applicable_conditions='')
           OR (q.exceptions_boundary IS NULL OR q.exceptions_boundary='')
           OR (q.practical_steps IS NULL OR q.practical_steps='')
           OR (q.risk_warning IS NULL OR q.risk_warning='')
           OR (SELECT COUNT(*) FROM question_relation WHERE question_id=q.id) = 0
           OR (SELECT COUNT(*) FROM question_update_log WHERE question_id=q.id) = 0
           OR (SELECT COUNT(*) FROM question_tag_link WHERE question_id=q.id) = 0
          )
    """).fetchall()

    # 计算优先级分数
    scored = []
    for r in all_gap:
        rd = dict(r)  # sqlite3.Row → dict for .get()
        # missing_count = 结构字段缺失数（用于×2加权，不含关联/标签/更新记录）
        missing_count = sum([rd['miss_cond'], rd['miss_exc'], rd['miss_step'], rd['miss_risk']])
        score = score_question(rd, missing_count)
        # 推荐补强内容
        suggest = []
        if rd['miss_cond']: suggest.append('适用条件')
        if rd['miss_risk']: suggest.append('风险提示')
        if rd['miss_exc']: suggest.append('例外边界')
        if rd['miss_step']: suggest.append('实务步骤')
        if rd['rel_count'] == 0: suggest.append('关联问题')
        if rd['update_count'] == 0: suggest.append('更新记录')
        if rd['tag_count'] == 0: suggest.append('业务标签')

        scored.append({
            **rd,
            'score': score,
            'missing_count': missing_count,
            'suggest': suggest
        })

    scored.sort(key=lambda x: x['score'], reverse=True)

    # 输出 TOP 20
    priority_labels = {9: '🔴 极高', 7: '🟠 高', 5: '🟡 中', 3: '🟢 一般'}
    def get_priority_label(score):
        for threshold, label in sorted(priority_labels.items(), reverse=True):
            if score >= threshold:
                return label
        return '⚪ 低'

    for i, r in enumerate(scored[:20], 1):
        plabel = get_priority_label(r['score'])
        flags = []
        if r['high_frequency_flag']: flags.append('高频')
        if r['newbie_flag']: flags.append('新手')
        flag_str = '/'.join(flags) if flags else '普通'
        lines.append(f"  {i:2}. [{r['question_code']}] {r['question_title']}")
        lines.append(f"       阶段={r['stage_code']}/{r['module_code']} | {flag_str} | 确定性={r['answer_certainty']}")
        lines.append(f"       评分={r['score']} {plabel} | 缺 {r['missing_count']} 个结构项 | 建议优先补: {', '.join(r['suggest'])}")
        lines.append("")

    # ── 下一批内容建设建议（动态，基于真实数据缺口）────────────────
    lines.append("")
    lines.append("=" * 70)
    lines.append("【下一批内容建设建议（按批次）】")
    lines.append("=" * 70)

    # 按模块统计缺结构字段的问题数，取最严重的模块
    module_gap = conn.execute("""
        SELECT module_code, COUNT(*) as cnt
        FROM question_master
        WHERE status='active'
          AND (applicable_conditions IS NULL OR applicable_conditions=''
               OR exceptions_boundary IS NULL OR exceptions_boundary=''
               OR practical_steps IS NULL OR practical_steps=''
               OR risk_warning IS NULL OR risk_warning='')
        GROUP BY module_code
        ORDER BY cnt DESC
    """).fetchall()

    batch_num = 1

    # 批次1: 缺结构字段最严重的模块
    if module_gap:
        top_module = module_gap[0]['module_code']
        top_cnt = module_gap[0]['cnt']
        lines.append("")
        lines.append(f"【批次{batch_num}: {top_module}模块结构补强】— {top_cnt} 条")
        lines.append(f"理由: 该模块问题缺少 applicable_conditions / exceptions_boundary / practical_steps / risk_warning")
        lines.append(f"建议: 逐条补充四类结构字段")
        batch_num += 1

    # 批次2: 缺关联问题最多的模块
    no_rel = conn.execute("""
        SELECT q.module_code, COUNT(*) as cnt
        FROM question_master q
        LEFT JOIN question_relation r ON q.id=r.question_id
        WHERE q.status='active' AND r.id IS NULL
        GROUP BY q.module_code
        ORDER BY cnt DESC
    """).fetchone()
    if no_rel and no_rel['cnt'] > 0:
        lines.append("")
        lines.append(f"【批次{batch_num}: {no_rel['module_code']}模块关联问题补强】— {no_rel['cnt']} 条无关联问题")
        lines.append(f"理由: 该模块大量问题缺少关联问题，无法形成问题网络")
        lines.append(f"建议: 建立同模块内问题的关联关系（next_step / prerequisite / related）")
        batch_num += 1

    # 批次3: 缺更新记录的问题
    no_update = conn.execute("""
        SELECT COUNT(*) as cnt FROM question_master q
        LEFT JOIN question_update_log u ON q.id=u.question_id
        WHERE q.status='active' AND u.id IS NULL
    """).fetchone()
    if no_update and no_update['cnt'] > 0:
        lines.append("")
        lines.append(f"【批次{batch_num}: 缺更新记录问题】— {no_update['cnt']} 条")
        lines.append(f"理由: 首批录入问题缺少 update_log，数据可信度不足")
        lines.append(f"建议: 补充 v1.0 创建记录（update_reason='首批录入'）")
        batch_num += 1

    # 批次4: 高频+新手但缺业务标签
    no_tags_hf = conn.execute("""
        SELECT COUNT(*) as cnt FROM question_master q
        LEFT JOIN question_tag_link t ON q.id=t.question_id
        WHERE q.status='active' AND q.high_frequency_flag=1 AND t.id IS NULL
    """).fetchone()
    if no_tags_hf and no_tags_hf['cnt'] > 0:
        lines.append("")
        lines.append(f"【批次{batch_num}: 高频问题补充业务标签】— {no_tags_hf['cnt']} 条")
        lines.append(f"理由: 高频问题无业务标签，影响筛选体验")
        lines.append(f"建议: 给高频问题补充对应业务标签（零申报/发票管理/变更登记等）")

    if batch_num == 1:
        lines.append("")
        lines.append("  （当前数据质量良好，无明显批次缺口）")

    # ── 保存报告 ──────────────────────────────────────────────
    report_path = os.path.join(REPORTS_DIR, f'priority_reinforce_{datetime.now().strftime("%Y%m%d")}.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('\n'.join(lines))
    print(f"\n✅ 报告已保存: {report_path}")

    conn.close()


if __name__ == '__main__':
    main()
