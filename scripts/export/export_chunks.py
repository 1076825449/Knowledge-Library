#!/usr/bin/env python3
"""
将问题拆成语义chunks，适合向量检索
每个问题生成2-4个chunk，保存到 data/exports/question_chunks.jsonl

Chunk类型:
- question_text: question_plain + keywords
- answer_core: one_line_answer + core_definition
- detailed_explanation: detailed_answer关键段落
- practical_guidance: practical_steps + risk_warning + applicable_conditions
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


def get_connection():
    return sqlite3.connect(DB_PATH)


def load_questions_with_tags(conn):
    """加载问题及标签"""
    query = """
    SELECT 
        qm.id,
        qm.question_code,
        qm.question_plain,
        qm.stage_code,
        qm.module_code,
        qm.question_type,
        qm.one_line_answer,
        qm.core_definition,
        qm.detailed_answer,
        qm.practical_steps,
        qm.risk_warning,
        qm.applicable_conditions,
        qm.keywords,
        GROUP_CONCAT(td.tag_name, ',') as tags
    FROM question_master qm
    LEFT JOIN question_tag_link qtl ON qm.id = qtl.question_id
    LEFT JOIN tag_dict td ON qtl.tag_id = td.id
    WHERE qm.status = 'active'
    GROUP BY qm.id
    ORDER BY qm.question_code
    """
    rows = conn.execute(query).fetchall()
    columns = [desc[0] for desc in conn.execute(query).description]
    return [dict(zip(columns, row)) for row in rows]


def split_text_chunks(text, chunk_size=500):
    """将长文本按指定字数分段"""
    if not text or len(text.strip()) == 0:
        return []
    
    # 按段落分割
    paragraphs = text.split("\n")
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        if len(current_chunk) + len(para) <= chunk_size:
            current_chunk += para + "\n"
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            # 如果单个段落超过chunk_size，按句子分割
            if len(para) > chunk_size:
                sentences = para.split("。")
                for sent in sentences:
                    sent = sent.strip()
                    if not sent:
                        continue
                    if len(current_chunk) + len(sent) <= chunk_size:
                        current_chunk += sent + "。"
                    else:
                        if current_chunk.strip():
                            chunks.append(current_chunk.strip())
                        current_chunk = sent + "。"
                if current_chunk.strip() and current_chunk.endswith("。"):
                    current_chunk = current_chunk[:-1]
            else:
                current_chunk = para + "\n"
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


def generate_chunks(q):
    """为一个问题生成多个chunk"""
    chunks = []
    chunk_id_prefix = f"{q['question_code']}"
    
    stage_label = STAGE_LABEL.get(q["stage_code"], q["stage_code"])
    module_label = MODULE_LABEL.get(q["module_code"], q["module_code"])
    tags = q["tags"] or ""
    
    # 1. question_text chunk
    question_text_content = f"{q['question_plain']}"
    if q["keywords"]:
        question_text_content += f"\n关键词: {q['keywords']}"
    
    chunks.append({
        "chunk_id": f"{chunk_id_prefix}-q1",
        "question_code": q["question_code"],
        "chunk_type": "question_text",
        "content": question_text_content,
        "stage_label": stage_label,
        "module_label": module_label,
        "question_type": q["question_type"],
        "tags": tags
    })
    
    # 2. answer_core chunk
    answer_core_content = f"一句话答案: {q['one_line_answer']}"
    if q["core_definition"]:
        answer_core_content += f"\n核心定义: {q['core_definition']}"
    
    chunks.append({
        "chunk_id": f"{chunk_id_prefix}-a1",
        "question_code": q["question_code"],
        "chunk_type": "answer_core",
        "content": answer_core_content,
        "stage_label": stage_label,
        "module_label": module_label,
        "question_type": q["question_type"],
        "tags": tags
    })
    
    # 3. detailed_explanation chunks
    if q["detailed_answer"]:
        detail_chunks = split_text_chunks(q["detailed_answer"], chunk_size=500)
        for i, chunk_content in enumerate(detail_chunks[:3], start=1):  # 最多3段
            chunks.append({
                "chunk_id": f"{chunk_id_prefix}-d{i}",
                "question_code": q["question_code"],
                "chunk_type": "detailed_explanation",
                "content": chunk_content,
                "stage_label": stage_label,
                "module_label": module_label,
                "question_type": q["question_type"],
                "tags": tags
            })
    
    # 4. practical_guidance chunk
    practical_parts = []
    if q["practical_steps"]:
        practical_parts.append(f"实务步骤: {q['practical_steps']}")
    if q["risk_warning"]:
        practical_parts.append(f"风险提示: {q['risk_warning']}")
    if q["applicable_conditions"]:
        practical_parts.append(f"适用条件: {q['applicable_conditions']}")
    
    if practical_parts:
        chunks.append({
            "chunk_id": f"{chunk_id_prefix}-p1",
            "question_code": q["question_code"],
            "chunk_type": "practical_guidance",
            "content": "\n".join(practical_parts),
            "stage_label": stage_label,
            "module_label": module_label,
            "question_type": q["question_type"],
            "tags": tags
        })
    
    return chunks


def main():
    print("=" * 50)
    print("问题Chunk生成脚本")
    print("=" * 50)
    
    conn = get_connection()
    
    print("\n[1/2] 加载问题数据...")
    questions = load_questions_with_tags(conn)
    print(f"    加载 {len(questions)} 条问题")
    
    conn.close()
    
    print("[2/2] 生成Chunks...")
    all_chunks = []
    chunk_count = 0
    
    for q in questions:
        chunks = generate_chunks(q)
        all_chunks.extend(chunks)
        chunk_count += len(chunks)
        print(f"    {q['question_code']}: {len(chunks)} chunks")
    
    # 写入JSONL
    output_path = OUTPUT_DIR / "question_chunks.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    
    print(f"\n导出完成: {output_path}")
    print(f"总计: {len(questions)} 条问题 -> {chunk_count} 个 chunks")


if __name__ == "__main__":
    main()
