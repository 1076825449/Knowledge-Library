#!/usr/bin/env python3
"""批量补充增值税申报抵扣相关政策 — batch10_vat_policies.py"""
import sqlite3

DB_PATH = "/Volumes/外接硬盘/vibe coding/网站/知识库/database/db/tax_knowledge.db"

POLICIES = [
    {
        "policy_code": "POL-VAT-002",
        "policy_name": "关于深化增值税改革有关政策的公告",
        "document_no": "财政部 税务总局 海关总署公告2019年第39号",
        "article_ref": "第七条",
        "policy_level": "level_bulletin",
        "effective_date": "2019-04-01",
        "expiry_date": None,
        "current_status": "active",
        "policy_summary": "明确旅客运输服务进项税额抵扣规则，增值税改革核心文件",
        "raw_quote_short": "纳税人购进国内旅客运输服务，其进项税额允许从销项税额中抵扣",
        "region_scope": "scope_national",
        "remarks": "增值税改革减税降费核心政策"
    },
    {
        "policy_code": "POL-VAT-003",
        "policy_name": "关于继续执行的部分增值税税收优惠政策",
        "document_no": "财政部 税务总局公告2019年第98号",
        "article_ref": "第一条",
        "policy_level": "level_bulletin",
        "effective_date": "2019-01-01",
        "expiry_date": None,
        "current_status": "active",
        "policy_summary": "延续部分增值税优惠政策，明确免税销售额标准",
        "raw_quote_short": "小规模纳税人月销售额未超过10万元的，免征增值税",
        "region_scope": "scope_national",
        "remarks": "免税销售额标准延续"
    },
    {
        "policy_code": "POL-VAT-004",
        "policy_name": "关于明确农产品增值税进项税额核定扣除有关事项的公告",
        "document_no": "财政部 税务总局公告2013年第66号",
        "article_ref": "第二条",
        "policy_level": "level_bulletin",
        "effective_date": "2013-09-01",
        "expiry_date": None,
        "current_status": "active",
        "policy_summary": "农产品增值税进项税额核定扣除办法，适用于以农产品为原料的生产企业",
        "raw_quote_short": "以农产品为原料生产销售货物的纳税人，农产品进项税额按核定扣除办法执行",
        "region_scope": "scope_national",
        "remarks": "核定扣除进项税额"
    },
    {
        "policy_code": "POL-VAT-005",
        "policy_name": "关于进一步优化增值税优惠政策办理程序的公告",
        "document_no": "国家税务总局公告2021年第8号",
        "article_ref": "第二条",
        "policy_level": "level_bulletin",
        "effective_date": "2021-04-01",
        "expiry_date": None,
        "current_status": "active",
        "policy_summary": "优化增值税优惠政策备案程序，简化纳税人申请流程",
        "raw_quote_short": "符合增值税优惠条件的纳税人，可直接在电子税务局办理备案",
        "region_scope": "scope_national",
        "remarks": "优惠办理便利化"
    },
    {
        "policy_code": "POL-VAT-006",
        "policy_name": "增值税发票管理等有关事项的公告",
        "document_no": "国家税务总局公告2020年第5号",
        "article_ref": "第一/二条",
        "policy_level": "level_bulletin",
        "effective_date": "2020-02-01",
        "expiry_date": None,
        "current_status": "active",
        "policy_summary": "明确增值税发票勾选认证、异常扣税凭证处理等重要规定",
        "raw_quote_short": "取消增值税发票抄报税，改为纳税人对发票进行用途确认",
        "region_scope": "scope_national",
        "remarks": "发票管理改革"
    },
    {
        "policy_code": "POL-VAT-007",
        "policy_name": "关于全面推开营业税改征增值税试点后增值税纳税申报有关事项的公告",
        "document_no": "国家税务总局公告2016年第23号",
        "article_ref": "附件1/2",
        "policy_level": "level_bulletin",
        "effective_date": "2016-06-01",
        "expiry_date": None,
        "current_status": "active",
        "policy_summary": "营改增后增值税纳税申报表格式及填报要求，适用于所有增值税纳税人",
        "raw_quote_short": "增值税一般纳税人申报表及附列资料格式，明确填报口径",
        "region_scope": "scope_national",
        "remarks": "申报表格式"
    },
    {
        "policy_code": "POL-VAT-008",
        "policy_name": "关于二手车经销企业减征增值税等政策的公告",
        "document_no": "财政部 税务总局公告2020年第17号",
        "article_ref": "第一条",
        "policy_level": "level_bulletin",
        "effective_date": "2020-05-01",
        "expiry_date": None,
        "current_status": "active",
        "policy_summary": "明确二手车经销企业减征增值税政策，利好汽车流通行业",
        "raw_quote_short": "从事二手车经销的纳税人，按0.5%征收率征收增值税",
        "region_scope": "scope_national",
        "remarks": "减征增值税"
    },
    {
        "policy_code": "POL-VAT-009",
        "policy_name": "关于增值税即征即退政策的公告",
        "document_no": "财政部 税务总局公告2011年第100号",
        "article_ref": "第一条",
        "policy_level": "level_bulletin",
        "effective_date": "2011-01-01",
        "expiry_date": None,
        "current_status": "active",
        "policy_summary": "明确软件产品、增值税即征即退的申请条件、计算方法和后续管理",
        "raw_quote_short": "增值税一般纳税人销售其自行开发生产的软件产品，按13%税率征收后，实际税负超过3%的部分实行即征即退",
        "region_scope": "scope_national",
        "remarks": "即征即退政策"
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
