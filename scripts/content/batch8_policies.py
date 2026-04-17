#!/usr/bin/env python3
"""批量导入第8批政策依据（RSK/SUS/ETAX/PREF政策缺口）"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.config import DB_PATH
import sqlite3

POLICIES = [
    # RSK - 非正常户
    {
        "policy_code": "POL-RISK-002",
        "policy_name": "非正常户管理办法",
        "document_no": "税总发〔2014〕106号",
        "article_ref": "全文",
        "policy_level": "规范性文件",
        "effective_date": "2014-10-01",
        "expiry_date": "",
        "current_status": "effective",
        "policy_summary": "规范非正常户的认定、公告、解除及后续处理。非正常户是指已办理税务登记但未按规定期限申报纳税的企业。税务机关可暂停其税务登记证件、发票的使用。解除需结清税款、滞纳金、罚款，并补齐申报。",
        "raw_quote_short": "已办理税务登记的纳税人未按照规定的期限申报纳税，在税务机关责令其限期改正后，逾期不改正的，税务机关应当派员实地检查，查无下落并且无法强制其履行纳税义务的，认定为非正常户。",
        "region_scope": "national",
        "remarks": "替代LOCAL-GX-002中的非正常户章节；原有POL-RISK-001保留",
    },
    # RSK - 纳税信用
    {
        "policy_code": "SAT-RISK-002",
        "policy_name": "纳税信用管理办法（试行）",
        "document_no": "国家税务总局公告2014年第40号",
        "article_ref": "第一章至第四章",
        "policy_level": "部门规章",
        "effective_date": "2014-10-01",
        "expiry_date": "",
        "current_status": "effective",
        "policy_summary": "建立纳税人纳税信用评价制度，按A/B/M/C/D五级管理。年度评价指标1000分，D级纳税人发票领用、出口退税等受严格限制。信用修复机制：纳税人对评价有异议可申请补评、复评。",
        "raw_quote_short": "纳税信用评价采取年度评价指标得分和直接判级相结合的方式。年度评价指标得分采取扣分方式。纳税信用评价周期为一个纳税年度。",
        "region_scope": "national",
        "remarks": "SAT-RISK-001为此公告，现统一引用",
    },
    # RSK - 异常凭证
    {
        "policy_code": "POL-RISK-003",
        "policy_name": "关于异常增值税扣税凭证处理有关问题的公告",
        "document_no": "国家税务总局公告2019年第38号",
        "article_ref": "全文",
        "policy_level": "规范性文件",
        "effective_date": "2019-04-01",
        "expiry_date": "",
        "current_status": "effective",
        "policy_summary": "规范异常增值税扣税凭证的范围及处理方式。异常凭证包括：增值税发票税率开错、非正常户开具的发票、等。取得异常凭证的纳税人，尚未申报抵扣的，暂不抵扣；已申报抵扣的，须进项税额转出。",
        "raw_quote_short": "符合下列情形之一的增值税专用发票，列入异常凭证范围：（一）纳税人丢失、被盗税控专用设备中未开具的增值税专用发票；（二）非正常户纳税人未向税务机关申报或未按规定缴纳税款的增值税专用发票。",
        "region_scope": "national",
        "remarks": "补充RSK异常凭证处理路径",
    },
    # SUS - 停业税务处理
    {
        "policy_code": "POL-SUS-001",
        "policy_name": "税务登记管理办法（停业复业章节）",
        "document_no": "国家税务总局令第7号",
        "article_ref": "第五章（停业、复业登记）",
        "policy_level": "行政规章",
        "effective_date": "2004-02-01",
        "expiry_date": "",
        "current_status": "effective",
        "policy_summary": "实行定期定额征收的个体工商户需要停业的，应在停业前向税务机关申报办理停业登记。纳税人的停业期限不得超过一年。停业期间，税务机关应封存其税务登记证件、发票领购簿、未使用发票等。",
        "raw_quote_short": "实行定期定额征收方式的纳税人需要停业的，应当向税务机关申报办理停业登记。纳税人停业期间发生纳税义务，应当向主管税务机关申报纳税。",
        "region_scope": "national",
        "remarks": "注意：仅定期定额户需办理停业登记；查账征收企业不需办理停业登记，但应按规定申报",
    },
    # ETAX - 税费种认定
    {
        "policy_code": "SAT-DEC-006",
        "policy_name": "关于进一步推进税费种认定便利化的公告",
        "document_no": "国家税务总局公告2019年第34号",
        "article_ref": "全文",
        "policy_level": "部门规章",
        "effective_date": "2019-07-01",
        "expiry_date": "",
        "current_status": "effective",
        "policy_summary": "推进税费种认定信息电子化，纳税人可通过电子税务局查询已认定的税费种信息。主管税务机关根据纳税人经营情况认定税种，纳税人如发现认定有误可申请调整。",
        "raw_quote_short": "税务机关应当通过电子税务局等渠道，将税费种认定信息告知纳税人。纳税人经营情况发生变化，需要调整税种认定的，应当向税务机关申请办理。",
        "region_scope": "national",
        "remarks": "税费种认定查询和变更的电子化依据",
    },
    # ETAX - 纳税信用评价
    {
        "policy_code": "SAT-RISK-003",
        "policy_name": "纳税信用管理有关问题的公告",
        "document_no": "国家税务总局公告2020年第33号",
        "article_ref": "全文",
        "policy_level": "部门规章",
        "effective_date": "2020-07-01",
        "expiry_date": "",
        "current_status": "effective",
        "policy_summary": "明确纳税信用修复机制，纳税人可在规定期限内申请信用修复。纳入严重失信主体名单的企业，实施联合惩戒措施。",
        "raw_quote_short": "纳税人对纳税信用评价结果有异议的，可在评价年度当年的12月31日前，向主管税务机关申请纳税信用补评或复评。",
        "region_scope": "national",
        "remarks": "企业可通过电子税务局查询信用等级和信用状态",
    },
    # PREF - 小微优惠总纲
    {
        "policy_code": "POL-PREF-001",
        "policy_name": "关于实施小微企业普惠性税收减免政策的通知",
        "document_no": "财税〔2019〕13号",
        "article_ref": "全文",
        "policy_level": "规范性文件",
        "effective_date": "2019-01-01",
        "expiry_date": "",
        "current_status": "effective",
        "policy_summary": "对小型微利企业年应纳税所得额不超过100万元的部分，减按25%计入应纳税所得额，按20%的税率缴纳企业所得税（实际税负5%）。超过100万元但不超过300万元的部分，减按50%计入应纳税所得额。",
        "raw_quote_short": "对小型微利企业年应纳税所得额不超过100万元的部分，减按25%计入应纳税所得额，按20%的税率缴纳企业所得税；对年应纳税所得额超过100万元但不超过300万元的部分，减按50%计入应纳税所得额，按20%的税率缴纳企业所得税。",
        "region_scope": "national",
        "remarks": "小微企业所得税优惠的纲领性文件，后有延续政策",
    },
    # PREF - 增值税小规模免税
    {
        "policy_code": "POL-PREF-002",
        "policy_name": "关于进一步支持小微企业的增值税政策的公告",
        "document_no": "国家税务总局公告2023年第1号",
        "article_ref": "全文",
        "policy_level": "规范性文件",
        "effective_date": "2023-01-01",
        "expiry_date": "",
        "current_status": "effective",
        "policy_summary": "对月销售额10万元以下（含10万元）的增值税小规模纳税人，免征增值税。适用3%征收率的应税销售收入，减按1%征收率征收增值税。",
        "raw_quote_short": "对月销售额10万元以下（含本数）的增值税小规模纳税人，免征增值税。增值税小规模纳税人适用3%征收率的应税销售收入，减按1%征收率计算缴纳增值税。",
        "region_scope": "national",
        "remarks": "小规模纳税人增值税优惠的核心依据，有效期延续中",
    },
    # PREF - 小微所得税优惠延续
    {
        "policy_code": "POL-PREF-003",
        "policy_name": "关于小微企业和个体工商户所得税优惠政策的公告",
        "document_no": "财税〔2023〕12号",
        "article_ref": "全文",
        "policy_level": "规范性文件",
        "effective_date": "2023-01-01",
        "expiry_date": "",
        "current_status": "effective",
        "policy_summary": "对小型微利企业年应纳税所得额不超过100万元的部分，在已优惠基础上再减半征收企业所得税（实际税负约2.5%）。执行至2027年12月31日。",
        "raw_quote_short": "对小型微利企业年应纳税所得额不超过100万元的部分，减按25%计入应纳税所得额，按20%的税率缴纳企业所得税，在此基础上，再减半征收企业所得税。",
        "region_scope": "national",
        "remarks": "实际税负约2.5%，延续至2027年",
    },
    # PREF - 个税专项附加扣除
    {
        "policy_code": "POL-PREF-004",
        "policy_name": "个人所得税专项附加扣除标准提高",
        "document_no": "国发〔2023〕13号",
        "article_ref": "全文",
        "policy_level": "行政法规",
        "effective_date": "2023-01-01",
        "expiry_date": "",
        "current_status": "effective",
        "policy_summary": "提高3岁以下婴幼儿照护、子女教育、赡养老人、住房贷款利息、住房租金、大病医疗等六项个人所得税专项附加扣除标准。例如子女教育从每个子女每月1000元提高至2000元。",
        "raw_quote_short": "3岁以下婴幼儿照护、子女教育、赡养老人专项附加扣除标准，分别提高至每个子女每月2000元、2000元（学历教育）、3000元（独生子女）或1500元（分摊）。",
        "region_scope": "national",
        "remarks": "2023年标准提高后的政策，适用于员工个人所得税汇算",
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
            print(f"  ~ {p['policy_code']} 已存在，跳过: {e}")
    conn.commit()
    total = cur.execute("SELECT COUNT(*) FROM policy_basis").fetchone()[0]
    print(f"\n完成：新增 {added} 条，跳过 {skipped} 条，政策库共 {total} 条")
    conn.close()

if __name__ == "__main__":
    main()
