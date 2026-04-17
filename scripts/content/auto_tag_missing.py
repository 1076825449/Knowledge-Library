#!/usr/bin/env python3
# ============================================================
# scripts/content/auto_tag_missing.py
# 自动为缺标签的问题补充业务标签
# 用法: python scripts/content/auto_tag_missing.py [--dry-run]
# ============================================================

import sqlite3
import os
import sys
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'db', 'tax_knowledge.db')


# ── 标签推荐规则 ──────────────────────────────────────────────

# module → 基础业务标签
MODULE_TAG_MAP = {
    'REG':   ['tag_register', 'tag_tax_registration'],
    'DEC':   ['tag_declaration', 'tag_period'],
    'INV':   ['tag_invoice', 'tag_invoice_issue'],
    'VAT':   ['tag_invoice', 'tag_vat_special'],
    'CIT':   ['tag_invoice', 'tag_credit_rating'],
    'IIT':   ['tag_withholding'],
    'SSF':   ['tag_ssf'],
    'FEE':   ['tag_invoice', 'tag_payment'],
    'PREF':  ['tag_policy_benefit'],
    'RISK':  ['tag_risk_warning', 'tag_risk_control'],
    'CLEAR': ['tag_注销清算', 'tag_清税', 'tag_税务注销'],
    'ETAX':  ['tag_ca_cert', 'tag_tax_control'],
    'TAX':   ['tag_risk_control'],
}

# stage → 基础业务标签
STAGE_TAG_MAP = {
    'SET': ['tag_setup', 'tag_first_tax'],
    'OPR': ['tag_setup'],
    'CHG': ['tag_change', 'tag_business_scope'],
    'RSK': ['tag_risk_warning'],
    'SUS': ['tag_risk_warning'],
    'CLS': ['tag_注销清算'],
}

# 关键词 → 业务标签
KEYWORD_TAG_MAP = [
    (re.compile(r'零申报|零收入|没收入|未经营'), 'tag_zero_report'),
    (re.compile(r'发票'), 'tag_invoice'),
    (re.compile(r'红字|红冲|开具红字'), 'tag_red_invoice'),
    (re.compile(r'失控|异常凭证|失控发票'), 'tag_runaway_invoice'),
    (re.compile(r'欠税|欠缴|滞纳金'), 'tag_overdue'),
    (re.compile(r'非正常户|走逃|失联'), 'tag_runaway'),
    (re.compile(r'首违不罚|首违|不予处罚'), 'tag_penalty_first'),
    (re.compile(r'纳税信用|信用等级|信用评价'), 'tag_credit_rating'),
    (re.compile(r'跨省|跨区|异地|跨地区'), 'tag_cross_region'),
    (re.compile(r'出口|退税|免抵退'), 'tag_export'),
    (re.compile(r'小规模|小微'), 'tag_small_scale'),
    (re.compile(r'一般纳税人|一般计税'), 'tag_general_taxpayer'),
    (re.compile(r'注销|清税|清算'), 'tag_注销清算'),
    (re.compile(r'简易注销'), 'tag_简易注销'),
    (re.compile(r'一般注销'), 'tag_一般注销'),
    (re.compile(r'分支机构|分公司|子公司'), 'tag_business_scope'),
    (re.compile(r'注册资本|实缴|认缴|资本'), 'tag_capital_increase'),
    (re.compile(r'加成|扣除|调增调减|税前扣除'), 'tag_capital_reserve'),
    (re.compile(r'社保|失业保险|工伤保险|生育保险|养老保险'), 'tag_ssf'),
    (re.compile(r'专项附加扣除|附加扣除'), 'tag_withholding'),
    (re.compile(r'代扣代缴|扣缴'), 'tag_withholding'),
    (re.compile(r'个人所得税|个税'), 'tag_withholding'),
    (re.compile(r'企业所得税|所得税'), 'tag_credit_rating'),
    (re.compile(r'增值税'), 'tag_vat_special'),
    (re.compile(r'年报|年度申报|汇算清缴'), 'tag_declaration'),
    (re.compile(r'三证合一|多证合一|统一社会信用代码'), 'tag_three_in_one'),
    (re.compile(r'CA证书|电子税务局|电子申报'), 'tag_ca_cert'),
    (re.compile(r'税控设备|税控盘|金税盘'), 'tag_tax_control'),
    (re.compile(r'变更登记|地址变更|经营范围变更|变更'), 'tag_change'),
    (re.compile(r'新办|设立登记|开业'), 'tag_registration'),
    (re.compile(r'重大违法|税收违法|黑名单'), 'tag_major_violation'),
    (re.compile(r'善意取得|虚开发票'), 'tag_good_faith'),
    (re.compile(r'银行贷款|融资'), 'tag_credit_loan'),
    (re.compile(r'免税|减税|免税收入|税收优惠'), 'tag_audit_free'),
    (re.compile(r'资本公积|转增资本|转增股本'), 'tag_capital_reserve'),
    (re.compile(r'收购|合并|分立|资产重组'), 'tag_business_scope'),
    (re.compile(r'发票领用|领用发票|领票'), 'tag_invoice_apply'),
    (re.compile(r'发票认证|认证|勾选抵扣'), 'tag_invoice_certification'),
    (re.compile(r'作废|发票作废'), 'tag_invoice_void'),
    (re.compile(r'风险纳税人|风险等级|重大风险'), 'tag_risk_control'),
    (re.compile(r'自查|纳税自查|自检'), 'tag_self_check'),
]


def get_recommended_tags(module_code, stage_code, title):
    """根据模块、阶段、标题推荐标签"""
    tags = set()

    # module 基础标签
    for tag in MODULE_TAG_MAP.get(module_code, []):
        tags.add(tag)

    # stage 基础标签
    for tag in STAGE_TAG_MAP.get(stage_code, []):
        tags.add(tag)

    # 标题关键词匹配
    title_lower = title  # 中文标题，不需要 lowercase
    for pattern, tag in KEYWORD_TAG_MAP:
        if pattern.search(title):
            tags.add(tag)

    return tags


def connect_db():
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库文件不存在: {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def get_tag_id_map(conn):
    """返回 tag_code → id 的映射"""
    rows = conn.execute("SELECT id, tag_code FROM tag_dict").fetchall()
    return {r['tag_code']: r['id'] for r in rows}


def main():
    dry_run = '--dry-run' in sys.argv
    if dry_run:
        print("🔍 [Dry Run 模式] 仅显示将要添加的标签，不写入数据库")

    conn = connect_db()
    tag_map = get_tag_id_map(conn)

    # 找出所有缺标签的问题
    rows = conn.execute("""
        SELECT q.id, q.question_code, q.question_title,
               q.module_code, q.stage_code
        FROM question_master q
        LEFT JOIN question_tag_link t ON q.id = t.question_id
        WHERE t.id IS NULL
        ORDER BY q.module_code, q.question_code
    """).fetchall()

    if not rows:
        print("✅ 所有问题均已有标签，无需补充")
        conn.close()
        return

    print(f"📋 共有 {len(rows)} 条问题缺标签，开始补充...\n")

    total_added = 0
    tag_added_by_module = {}

    for r in rows:
        qid = r['id']
        qcode = r['question_code']
        title = r['question_title']
        module = r['module_code']
        stage = r['stage_code']

        recommended = get_recommended_tags(module, stage, title)

        # 过滤：只保留存在的标签
        valid_tags = [t for t in recommended if t in tag_map]
        # 去重：查询现有标签
        existing = {t['tag_code'] for t in conn.execute(
            "SELECT td.tag_code FROM question_tag_link qtl JOIN tag_dict td ON qtl.tag_id=td.id WHERE qtl.question_id=?",
            (qid,)).fetchall()}
        to_add = [t for t in valid_tags if t not in existing]

        if not to_add:
            continue

        if dry_run:
            print(f"  {qcode} ({module}) → 添加: {', '.join(to_add)}")
        else:
            for tag_name in to_add:
                tag_id = tag_map[tag_name]
                conn.execute(
                    "INSERT INTO question_tag_link (question_id, tag_id, is_primary, display_order) VALUES (?, ?, 0, 0)",
                    (qid, tag_id)
                )
            print(f"  ✅ {qcode} → 添加 {len(to_add)} 个标签: {', '.join(to_add)}")

        total_added += len(to_add)
        tag_added_by_module[module] = tag_added_by_module.get(module, 0) + len(to_add)

    if not dry_run:
        conn.commit()
        print(f"\n✅ 写入完成，共添加 {total_added} 个标签关联")
    else:
        print(f"\n🔍 [Dry Run] 共需添加 {total_added} 个标签关联")

    print("\n📊 各模块补充统计：")
    for mod, cnt in sorted(tag_added_by_module.items(), key=lambda x: -x[1]):
        print(f"  {mod}: +{cnt} 条")

    # 验证剩余缺标签数
    remaining = conn.execute("""
        SELECT COUNT(*) FROM question_master q
        LEFT JOIN question_tag_link t ON q.id = t.question_id
        WHERE t.id IS NULL
    """).fetchone()[0]
    print(f"\n📋 剩余缺标签问题: {remaining} 条")

    conn.close()


if __name__ == '__main__':
    main()
