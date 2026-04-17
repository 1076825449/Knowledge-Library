#!/usr/bin/env python3
"""批量导入第9批政策依据：PREF税收优惠模块扩容（+6条）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.config import DB_PATH
import sqlite3

POLICIES = [
    # PREF-005 研发费用加计扣除
    {
        "policy_code": "POL-PREF-005",
        "policy_name": "关于进一步完善研发费用税前加计扣除政策的公告",
        "document_no": "财税〔2023〕7号",
        "article_ref": "全文",
        "policy_level": "规范性文件",
        "effective_date": "2023-01-01",
        "expiry_date": "2027-12-31",
        "current_status": "effective",
        "policy_summary": "企业开展研发活动中实际发生的研发费用，未形成无形资产计入当期损益的，在按规定据实扣除的基础上，再按实际发生额的100%在税前加计扣除；形成无形资产的，按无形资产成本的200%在税前摊销。委托境外研发费用不超过境内符合条件的研发费用三分之二的部分，可以按规定适用加计扣除。",
        "raw_quote_short": "企业开展研发活动中实际发生的研发费用，未形成无形资产计入当期损益的，在按规定据实扣除的基础上，再按实际发生额的100%在税前加计扣除。",
        "region_scope": "national",
        "remarks": "适用所有行业，只要符合研发活动定义；制造业扣除比例已提升至100%",
    },
    # PREF-006 高新技术企业优惠
    {
        "policy_code": "POL-PREF-006",
        "policy_name": "高新技术企业认定管理办法",
        "document_no": "国科发火〔2023〕209号",
        "article_ref": "全文",
        "policy_level": "行政规章",
        "effective_date": "2023-12-01",
        "expiry_date": "",
        "current_status": "effective",
        "policy_summary": "高新技术企业是指在《国家重点支持的高新技术领域》内，持续进行研究开发与技术成果转化，形成企业核心自主知识产权，并以此为基础开展经营活动的居民企业。认定为高新技术企业后，可享受15%的优惠税率（比法定税率25%降低10个百分点）。",
        "raw_quote_short": "高新技术企业是指在国家重点支持的高新技术领域内，持续进行研究开发与技术成果转化，形成企业核心自主知识产权，并以此为基础开展经营活动，在中国境内（不包括港澳台地区）注册的居民企业。",
        "region_scope": "national",
        "remarks": "认定条件：注册满一年、自主知识产权、领域符合、技术收入占比、高新收入占比、研发费占比、科技人员占比",
    },
    # PREF-007 残疾人就业优惠
    {
        "policy_code": "POL-PREF-007",
        "policy_name": "关于促进残疾人就业增值税优惠政策的通知",
        "document_no": "财税〔2016〕52号",
        "article_ref": "全文",
        "policy_level": "规范性文件",
        "effective_date": "2016-05-01",
        "expiry_date": "",
        "current_status": "effective",
        "policy_summary": "对安置残疾人的单位和个体工商户，按安置残疾人的人数，最高可享受每人每月最低工资4倍增值税即征即退。对月销售额不足3万元的小规模纳税人免税优惠与即征即退政策不可同时享受。",
        "raw_quote_short": "对安置残疾人的单位和个体工商户（以下称纳税人），根据纳税人安置残疾人的人数，限额即征即退增值税。每月可退还的增值税具体限额，由县级以上税务机关根据纳税人所在区县适用的月最低工资标准的4倍确定。",
        "region_scope": "national",
        "remarks": "残疾人就业增值税即征即退的完整政策依据；需在申报时提交残联核定表",
    },
    # PREF-008 增量留抵退税
    {
        "policy_code": "POL-PREF-008",
        "policy_name": "关于进一步加大增值税期末留抵退税政策实施力度的公告",
        "document_no": "财政部 税务总局公告2022年第14号",
        "article_ref": "全文",
        "policy_level": "规范性文件",
        "effective_date": "2022-04-01",
        "expiry_date": "",
        "current_status": "effective",
        "policy_summary": "加大小微企业增值税期末留抵退税政策力度，将先进制造业按月全额退还增值税增量留抵税额政策范围扩大至符合条件的小微企业（含个体工商户），并一次性退还小微企业存量留抵税额。微型企业存量留抵税额于2022年4月起集中退还，大型企业于2022年6月前退还。",
        "raw_quote_short": "加大小微企业增值税期末留抵退税政策力度，将先进制造业按月全额退还增值税增量留抵税额政策范围扩大至符合条件的小微企业（含个体工商户），并一次性退还小微企业存量留抵税额。",
        "region_scope": "national",
        "remarks": "留抵退税是增值税申报的重要风险点，企业应关注增量留抵与存量留抵的区别及申请条件",
    },
    # PREF-009 小规模纳税人免税升级优惠（季度30万/45万）
    {
        "policy_code": "POL-PREF-009",
        "policy_name": "关于小规模纳税人免征增值税政策的公告",
        "document_no": "财政部 税务总局公告2023年第19号",
        "article_ref": "全文",
        "policy_level": "规范性文件",
        "effective_date": "2023-01-01",
        "expiry_date": "2027-12-31",
        "current_status": "effective",
        "policy_summary": "对月销售额10万元以下（含10万元）的增值税小规模纳税人，免征增值税。适用3%征收率的应税销售收入，减按1%征收率征收增值税。合计月销售额超过10万元，但扣除本期发生的销售不动产后未超过10万元的，其销售货物、劳务、服务、无形资产取得的销售额免征增值税。",
        "raw_quote_short": "对月销售额10万元以下（含10万元）的增值税小规模纳税人，免征增值税。增值税小规模纳税人适用3%征收率的应税销售收入，减按1%征收率征收增值税。",
        "region_scope": "national",
        "remarks": "小规模免税的核心政策延续至2027年；注意销售额判定是按差额前金额还是扣除不动产后的金额",
    },
    # PREF-010 软件企业和集成电路优惠
    {
        "policy_code": "POL-PREF-010",
        "policy_name": "关于促进集成电路产业和软件产业高质量发展企业所得税政策的公告",
        "document_no": "财政部 税务总局 发展改革委 工业和信息化部公告2020年第45号",
        "article_ref": "全文",
        "policy_level": "规范性文件",
        "effective_date": "2020-01-01",
        "expiry_date": "",
        "current_status": "effective",
        "policy_summary": "国家鼓励的集成电路生产企业或项目，第一年至第二年免征企业所得税，第三年至第五年按照25%的法定税率减半征收企业所得税（两免三减半）。国家鼓励的软件企业，自盈利年度起享受两免三减半优惠。",
        "raw_quote_short": "国家鼓励的集成电路生产企业或项目，第一年至第二年免征企业所得税，第三年至第五年按照25%的法定税率减半征收企业所得税。",
        "region_scope": "national",
        "remarks": "两免三减半政策需在认定后才能享受；软件企业认定条件包括收入占比、人员占比等",
    },
]

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    added = 0
    skipped = 0
    for p in POLICIES:
        try:
            cur.execute("""
                INSERT INTO policy_basis (policy_code, policy_name, document_no, article_ref,
                    policy_level, effective_date, expiry_date, current_status,
                    policy_summary, raw_quote_short, region_scope, remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p["policy_code"], p["policy_name"], p["document_no"], p["article_ref"],
                p["policy_level"], p["effective_date"], p["expiry_date"], p["current_status"],
                p["policy_summary"], p["raw_quote_short"], p["region_scope"], p["remarks"]
            ))
            added += 1
            print(f"  + {p['policy_code']}  {p['policy_name']}")
        except sqlite3.IntegrityError as e:
            skipped += 1
            print(f"  ~ {p['policy_code']} 已存在，跳过")
    conn.commit()
    total = cur.execute("SELECT COUNT(*) FROM policy_basis").fetchone()[0]
    print(f"\n完成：新增 {added} 条，跳过 {skipped} 条，政策库共 {total} 条")
    conn.close()

if __name__ == "__main__":
    main()
