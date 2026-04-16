#!/usr/bin/env python3
"""
AI检索用数据导出脚本
读取SQLite数据库，输出:
- data/exports/questions_full.json (完整导出)
- data/exports/questions_for_embedding.jsonl (向量检索用)
"""

import json
import sqlite3
from pathlib import Path

# 配置路径
DB_PATH = "/Volumes/外接硬盘/vibe coding/知识库/database/db/tax_knowledge.db"
BASE_DIR = Path("/Volumes/外接硬盘/vibe coding/知识库")
OUTPUT_DIR = BASE_DIR / "data" / "exports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 标签翻译字典
STAGE_LABEL = {
    "setup": "设立",
    "operation": "经营",
    "change": "变更",
    "dissolution": "注销",
    "cross_border": "跨境"
}

MODULE_LABEL = {
    "SSF": "财税处理",
    "OPR": "运营管理",
    "TAX": "税务申报",
    "INV": "投资融资",
    "SET": "设立合规",
    "RISK": "风险管控",
    "CIT": "企业所得税",
    "CLS": "涉税争议",
    "POLICY": "政策法规",
    "ACCT": "会计核算",
    "DEC": "税费优惠",
    "IIT": "个人所得税",
    "REG": "税务登记",
    "CHG": "变更事项",
    "FEE": "发票管理",
    "CLEAR": "涉税争议"
}

CERTAINTY_LABEL = {
    "certain_clear": "明确无条件",
    "certain_condition": "有条件",
    "certain_dispute": "有争议",
    "certain_practice": "实务做法"
}

SCOPE_LABEL = {
    "scope_national": "全国通用",
    "scope_provincial": "省级口径",
    "scope_local": "地方口径"
}


def get_connection():
    return sqlite3.connect(DB_PATH)


def load_question_master(conn):
    """加载问题主表"""
    query = """
    SELECT 
        id, question_code, question_title, question_plain,
        stage_code, module_code, question_type,
        one_line_answer, detailed_answer, core_definition,
        applicable_conditions, exceptions_boundary,
        practical_steps, risk_warning,
        scope_level, local_region,
        answer_certainty, keywords,
        high_frequency_flag, newbie_flag,
        status, version_no, created_at, updated_at
    FROM question_master
    WHERE status = 'active'
    ORDER BY question_code
    """
    rows = conn.execute(query).fetchall()
    columns = [desc[0] for desc in conn.execute(query).description]
    return [dict(zip(columns, row)) for row in rows]


def load_policy_links(conn, question_ids):
    """加载政策关联"""
    if not question_ids:
        return {}
    
    placeholders = ",".join("?" * len(question_ids))
    query = f"""
    SELECT 
        qpl.question_id,
        pb.id as policy_id,
        pb.policy_code,
        pb.policy_name,
        pb.document_no,
        pb.article_ref,
        pb.policy_level,
        pb.effective_date,
        pb.expiry_date,
        pb.current_status,
        pb.policy_summary,
        pb.raw_quote_short,
        pb.region_scope,
        qpl.support_type,
        qpl.support_note,
        qpl.display_order
    FROM question_policy_link qpl
    JOIN policy_basis pb ON qpl.policy_id = pb.id
    WHERE qpl.question_id IN ({placeholders})
    ORDER BY qpl.question_id, qpl.display_order
    """
    
    rows = conn.execute(query, question_ids).fetchall()
    columns = [desc[0] for desc in conn.execute(query, question_ids).description]
    
    result = {}
    for row in rows:
        d = dict(zip(columns, row))
        qid = d.pop("question_id")
        if qid not in result:
            result[qid] = []
        result[qid].append(d)
    return result


def load_tag_links(conn, question_ids):
    """加载标签关联"""
    if not question_ids:
        return {}
    
    placeholders = ",".join("?" * len(question_ids))
    query = f"""
    SELECT 
        qtl.question_id,
        td.id as tag_id,
        td.tag_code,
        td.tag_name,
        td.tag_category,
        qtl.is_primary,
        qtl.display_order
    FROM question_tag_link qtl
    JOIN tag_dict td ON qtl.tag_id = td.id
    WHERE qtl.question_id IN ({placeholders})
    ORDER BY qtl.question_id, qtl.display_order
    """
    
    rows = conn.execute(query, question_ids).fetchall()
    columns = [desc[0] for desc in conn.execute(query, question_ids).description]
    
    result = {}
    for row in rows:
        d = dict(zip(columns, row))
        qid = d.pop("question_id")
        if qid not in result:
            result[qid] = []
        result[qid].append(d)
    return result


def load_related_questions(conn, question_ids):
    """加载关联问题"""
    if not question_ids:
        return {}
    
    placeholders = ",".join("?" * len(question_ids))
    query = f"""
    SELECT 
        qr.question_id,
        qm.question_code,
        qm.question_title,
        qr.relation_type,
        qr.display_order
    FROM question_relation qr
    JOIN question_master qm ON qr.related_id = qm.id
    WHERE qr.question_id IN ({placeholders})
    ORDER BY qr.question_id, qr.display_order
    """
    
    rows = conn.execute(query, question_ids).fetchall()
    columns = [desc[0] for desc in conn.execute(query, question_ids).description]
    
    result = {}
    for row in rows:
        d = dict(zip(columns, row))
        qid = d.pop("question_id")
        if qid not in result:
            result[qid] = []
        result[qid].append(d)
    return result


def translate_labels(q):
    """翻译标签字段"""
    q["stage_label"] = STAGE_LABEL.get(q["stage_code"], q["stage_code"])
    q["module_label"] = MODULE_LABEL.get(q["module_code"], q["module_code"])
    q["answer_certainty_label"] = CERTAINTY_LABEL.get(q["answer_certainty"], q["answer_certainty"])
    q["scope_level_label"] = SCOPE_LABEL.get(q["scope_level"], q["scope_level"])
    return q


def export_full_json(questions, policy_links, tag_links, related_questions):
    """导出完整JSON"""
    result = []
    for q in questions:
        qid = q["id"]
        q_translated = translate_labels(q.copy())
        
        # 移除id，添加关联数据
        del q_translated["id"]
        q_translated["policy_links"] = policy_links.get(qid, [])
        q_translated["tag_links"] = tag_links.get(qid, [])
        q_translated["related_questions"] = related_questions.get(qid, [])
        
        result.append(q_translated)
    
    output_path = OUTPUT_DIR / "questions_full.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"导出完成: {output_path} ({len(result)} 条记录)")


def export_embedding_jsonl(questions, tag_links, related_questions):
    """导出向量检索用JSONL"""
    output_path = OUTPUT_DIR / "questions_for_embedding.jsonl"
    
    with open(output_path, "w", encoding="utf-8") as f:
        for q in questions:
            qid = q["id"]
            
            # 处理标签
            tags = tag_links.get(qid, [])
            tag_names = ",".join([t["tag_name"] for t in tags])
            
            # 处理关联问题
            related = related_questions.get(qid, [])
            related_codes = ",".join([r["question_code"] for r in related])
            
            record = {
                "question_code": q["question_code"],
                "stage_label": STAGE_LABEL.get(q["stage_code"], q["stage_code"]),
                "module_label": MODULE_LABEL.get(q["module_code"], q["module_code"]),
                "question_type": q["question_type"],
                "question_plain": q["question_plain"],
                "one_line_answer": q["one_line_answer"],
                "keywords": q["keywords"] or "",
                "tags": tag_names,
                "answer_certainty_label": CERTAINTY_LABEL.get(q["answer_certainty"], q["answer_certainty"]),
                "is_high_freq": bool(q["high_frequency_flag"]),
                "is_newbie": bool(q["newbie_flag"]),
                "scope_level": q["scope_level"],
                "related_question_codes": related_codes
            }
            
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    print(f"导出完成: {output_path}")


def main():
    print("=" * 50)
    print("AI检索数据导出脚本")
    print("=" * 50)
    
    conn = get_connection()
    
    print("\n[1/4] 加载问题主表...")
    questions = load_question_master(conn)
    print(f"    加载 {len(questions)} 条问题")
    
    question_ids = [q["id"] for q in questions]
    
    print("[2/4] 加载政策关联...")
    policy_links = load_policy_links(conn, question_ids)
    print(f"    加载 {sum(len(v) for v in policy_links.values())} 条政策关联")
    
    print("[3/4] 加载标签关联...")
    tag_links = load_tag_links(conn, question_ids)
    print(f"    加载 {sum(len(v) for v in tag_links.values())} 条标签关联")
    
    print("[4/4] 加载关联问题...")
    related_questions = load_related_questions(conn, question_ids)
    print(f"    加载 {sum(len(v) for v in related_questions.values())} 条关联问题")
    
    conn.close()
    
    print("\n[导出] 生成完整JSON...")
    export_full_json(questions, policy_links, tag_links, related_questions)
    
    print("[导出] 生成向量检索JSONL...")
    export_embedding_jsonl(questions, tag_links, related_questions)
    
    print("\n导出完成!")


if __name__ == "__main__":
    main()
