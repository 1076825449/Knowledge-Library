#!/usr/bin/env python3
"""
AI检索用数据导出脚本
从 backend/config.py 读取 DB_PATH，输出:
- data/exports/questions_full.json   (完整导出)
- data/exports/questions_for_embedding.jsonl (向量检索用)
"""

import json
import sqlite3
import os
import sys
from pathlib import Path

# -------- 动态路径（与 backend/config.py 保持一致）--------
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR / "backend"))
from config import Config

DB_PATH = Config.DB_PATH
OUTPUT_DIR = ROOT_DIR / "data" / "exports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -------- 标签翻译字典（与数据库 tag_dict 实际值一致）--------
STAGE_LABEL = {
    "SET": "设立期",
    "OPR": "开业/日常经营期",
    "CHG": "变更期",
    "CLS": "注销期",
    "RSK": "风险异常期",
    "SUS": "停业期",
}

MODULE_LABEL = {
    "REG": "登记管理",
    "DEC": "申报纳税",
    "INV": "发票管理",
    "VAT": "增值税",
    "CIT": "企业所得税",
    "IIT": "个人所得税",
    "SSF": "社保费",
    "FEE": "成本费用",
    "PREF": "优惠政策",
    "RISK": "风险应对",
    "CLEAR": "清税注销",
    "ETAX": "电子税务局/系统办理",
}

CERTAINTY_LABEL = {
    "certain_clear": "明确无条件",
    "certain_conditional": "有条件",
    "certain_dispute": "有争议",
    "certain_practical": "实务做法",
}

SCOPE_LABEL = {
    "scope_national": "全国通用",
    "scope_local": "地方口径",
    "scope_mixed": "混合口径",
}


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def load_question_master(conn):
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
        result.setdefault(qid, []).append(d)
    return result


def load_tag_links(conn, question_ids):
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
        result.setdefault(qid, []).append(d)
    return result


def load_related_questions(conn, question_ids):
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
        result.setdefault(qid, []).append(d)
    return result


def translate_labels(q):
    q["stage_label"] = STAGE_LABEL.get(q["stage_code"], q["stage_code"])
    q["module_label"] = MODULE_LABEL.get(q["module_code"], q["module_code"])
    q["answer_certainty_label"] = CERTAINTY_LABEL.get(q["answer_certainty"], q["answer_certainty"])
    q["scope_level_label"] = SCOPE_LABEL.get(q["scope_level"], q["scope_level"])
    return q


def export_full_json(questions, policy_links, tag_links, related_questions):
    result = []
    for q in questions:
        qid = q["id"]
        q_translated = translate_labels(q.copy())
        del q_translated["id"]
        q_translated["policy_links"] = policy_links.get(qid, [])
        q_translated["tag_links"] = tag_links.get(qid, [])
        q_translated["related_questions"] = related_questions.get(qid, [])
        result.append(q_translated)
    output_path = OUTPUT_DIR / "questions_full.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"导出完成: {output_path} ({len(result)} 条)")


def export_embedding_jsonl(questions, policy_links, tag_links, related_questions):
    output_path = OUTPUT_DIR / "questions_for_embedding.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for q in questions:
            qid = q["id"]
            tags = tag_links.get(qid, [])
            tag_names = ",".join([t["tag_name"] for t in tags])
            related = related_questions.get(qid, [])
            related_codes = ",".join([r["question_code"] for r in related])
            policies = policy_links.get(qid, [])
            # 提取政策文号列表（用于展示）
            policy_docs = "; ".join([
                f"{p.get('document_no', '')} {p.get('article_ref', '')}"
                for p in policies
                if p.get("document_no")
            ])
            # 提取政策摘要（用于RAG）
            policy_summaries = " | ".join([
                p.get("policy_summary", "") or ""
                for p in policies
                if p.get("policy_summary")
            ])

            # 拼接检索文本：问题 → 答案 → 政策摘要 → 关键词
            retrieval_text = " | ".join(filter(None, [
                q.get("question_plain") or q.get("question_title", ""),
                q.get("one_line_answer", ""),
                policy_summaries,
                q.get("keywords", "") or "",
            ]))

            record = {
                "question_code": q["question_code"],
                "question_title": q.get("question_title", ""),
                "stage_label": STAGE_LABEL.get(q["stage_code"], q["stage_code"]),
                "module_label": MODULE_LABEL.get(q["module_code"], q["module_code"]),
                "question_type": q.get("question_type", ""),
                # 检索用全文（主要 embedding 对象）
                "retrieval_text": retrieval_text,
                # 各分段内容（供 chunk 检索）
                "question_plain": q.get("question_plain") or "",
                "one_line_answer": q.get("one_line_answer") or "",
                "detailed_answer": q.get("detailed_answer") or "",
                "core_definition": q.get("core_definition") or "",
                "practical_steps": q.get("practical_steps") or "",
                "risk_warning": q.get("risk_warning") or "",
                "keywords": q.get("keywords") or "",
                # 政策
                "policy_documents": policy_docs,
                "policy_count": len(policies),
                # 标签
                "tags": tag_names,
                "answer_certainty": q.get("answer_certainty", ""),
                "answer_certainty_label": CERTAINTY_LABEL.get(q["answer_certainty"], q["answer_certainty"]),
                "scope_level": q.get("scope_level", ""),
                "scope_level_label": SCOPE_LABEL.get(q["scope_level"], q["scope_level"]),
                # 指向信息
                "is_high_freq": bool(q.get("high_frequency_flag")),
                "is_newbie": bool(q.get("newbie_flag")),
                "related_question_codes": related_codes,
                # 版本
                "version_no": q.get("version_no", 1),
                "updated_at": q.get("updated_at", ""),
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"导出完成: {output_path}")


def main():
    print("=" * 50)
    print("AI检索数据导出脚本")
    print("=" * 50)
    print(f"\n数据库: {DB_PATH}")
    print(f"输出目录: {OUTPUT_DIR}")

    conn = get_connection()

    print("\n[1/4] 加载问题主表...")
    questions = load_question_master(conn)
    print(f"    加载 {len(questions)} 条问题")

    question_ids = [q["id"] for q in questions]

    print("[2/4] 加载政策关联...")
    policy_links = load_policy_links(conn, question_ids)
    print(f"    {sum(len(v) for v in policy_links.values())} 条政策关联")

    print("[3/4] 加载标签关联...")
    tag_links = load_tag_links(conn, question_ids)
    print(f"    {sum(len(v) for v in tag_links.values())} 条标签关联")

    print("[4/4] 加载关联问题...")
    related_questions = load_related_questions(conn, question_ids)
    print(f"    {sum(len(v) for v in related_questions.values())} 条关联问题")

    conn.close()

    print("\n[导出] 生成完整JSON...")
    export_full_json(questions, policy_links, tag_links, related_questions)

    print("[导出] 生成向量检索JSONL...")
    export_embedding_jsonl(questions, policy_links, tag_links, related_questions)

    print("\n完成!")


if __name__ == "__main__":
    main()
