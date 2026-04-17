#!/usr/bin/env python3
"""将 answer_summary/answer_content 格式的 JSON 转换为 import 脚本期望的格式。"""
import json
import sys

def convert(data):
    if isinstance(data, dict) and "questions" in data:
        # wrap in {"questions": [...]} already
        out = {"questions": []}
        for q in data["questions"]:
            out["questions"].append(convert_one(q))
        return out
    elif isinstance(data, list):
        out = {"questions": []}
        for q in data:
            out["questions"].append(convert_one(q))
        return out
    else:
        raise ValueError("Unknown JSON structure")

def convert_one(q):
    # 提取 answer_content 中的纯文本（去掉 markdown **）
    detailed = q.get("answer_content", "")
    # 清理 markdown 加粗
    detailed_clean = detailed.replace("**", "")

    # answer_summary 作为 one_line_answer
    one_line = q.get("answer_summary", "")

    # 处理 policy_links: 脚本用 policy_links 数组
    policy_links = []
    for pc in q.get("support_policy_codes", []):
        policy_links.append({
            "policy_code": pc,
            "support_type": "citation",
            "support_note": ""
        })

    # 处理 relations: 保留 target_code + relation_type + relation_note
    relations = []
    for rel in q.get("relations", []):
        relations.append({
            "question_code": rel.get("target_code", ""),
            "relation_type": rel.get("relation_type", "related"),
            "relation_note": rel.get("relation_note", "")
        })

    # 拆分 answer_content 为多字段（如果有结构化分隔）
    # 没有分隔符时，detailed_answer = detailed_clean
    practical_steps = ""
    core_definition = ""
    applicable_conditions = ""
    exceptions_boundary = ""
    risk_warning = ""
    scope_level = "scope_national"
    answer_certainty = "certain_clear"

    return {
        "question_code": q.get("question_code", ""),
        "question_title": q.get("question_title", ""),
        "question_plain": q.get("question_title", ""),
        "stage_code": q.get("stage_code", ""),
        "module_code": q.get("module_code", ""),
        "question_type": q.get("question_type", "type_whether"),
        "one_line_answer": one_line,
        "detailed_answer": detailed_clean,
        "core_definition": core_definition,
        "applicable_conditions": applicable_conditions,
        "exceptions_boundary": exceptions_boundary,
        "practical_steps": practical_steps,
        "risk_warning": risk_warning,
        "scope_level": scope_level,
        "answer_certainty": answer_certainty,
        "keywords": "",
        "high_frequency_flag": False,
        "newbie_flag": False,
        "policy_links": policy_links,
        "tags": q.get("tags", []),
        "relations": relations
    }

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "data/imports/questions_batch14_weak_modules.json"
    dst = sys.argv[2] if len(sys.argv) > 2 else src.replace(".json", "_importable.json")

    with open(src, encoding="utf-8") as f:
        data = json.load(f)

    converted = convert(data)

    with open(dst, "w", encoding="utf-8") as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)

    print(f"转换完成: {src} -> {dst}")
    print(f"共 {len(converted['questions'])} 条问题")
