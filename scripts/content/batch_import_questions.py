#!/usr/bin/env python3
"""
批量导入问题到税务知识库。

用法:
  python scripts/content/batch_import_questions.py data/questions_batch1.json

JSON 格式:
{
  "questions": [
    {
      "question_title": "...",
      "question_plain": "...",
      "stage_code": "SET",
      "module_code": "DEC",
      "question_type": "type_whether",
      "one_line_answer": "...",
      "detailed_answer": "...",
      "core_definition": "...",
      "applicable_conditions": "...",
      "exceptions_boundary": "...",
      "practical_steps": "...",
      "risk_warning": "...",
      "scope_level": "scope_national",
      "answer_certainty": "certain_clear",
      "keywords": "...",
      "high_frequency_flag": true,
      "newbie_flag": false,
      "policy_links": [
        {
          "policy_code": "GOV-Tax-001",
          "support_type": "support_direct",
          "support_note": "第25条，支撑申报义务"
        }
      ],
      "tags": ["零申报", "新手"],
      "relations": [
        {"question_code": "SET-DEC-001", "relation_type": "related"}
      ]
    }
  ]
}
"""

import json
import sqlite3
import datetime
import sys
import re
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"


def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_code(conn, stage_code, module_code):
    """生成下一个问题编码"""
    prefix = f"{stage_code}-{module_code}-"
    cur = conn.cursor()
    cur.execute(
        "SELECT question_code FROM question_master WHERE question_code LIKE ? ORDER BY question_code DESC LIMIT 1",
        (f"{prefix}%",)
    )
    row = cur.fetchone()
    if not row:
        return f"{prefix}001"
    last = row[0]
    num = int(last.split("-")[-1]) + 1
    return f"{prefix}{num:03d}"


def resolve_tag_ids(conn, tag_names_or_codes):
    """tag_names_or_codes 可以是 tag_name 或 tag_code，返回 id 列表"""
    if not tag_names_or_codes:
        return []
    cur = conn.cursor()
    ids = []
    for t in tag_names_or_codes:
        # 先按 code 查
        cur.execute("SELECT id FROM tag_dict WHERE tag_code = ?", (t,))
        row = cur.fetchone()
        if not row:
            # 再按 name 查
            cur.execute("SELECT id FROM tag_dict WHERE tag_name = ?", (t,))
            row = cur.fetchone()
        if row:
            ids.append(row[0])
    return ids


def resolve_policy_id(conn, policy_code):
    cur = conn.cursor()
    cur.execute("SELECT id FROM policy_basis WHERE policy_code = ?", (policy_code,))
    row = cur.fetchone()
    return row[0] if row else None


def resolve_question_id(conn, question_code):
    cur = conn.cursor()
    cur.execute("SELECT id FROM question_master WHERE question_code = ?", (question_code,))
    row = cur.fetchone()
    return row[0] if row else None


def import_questions(data):
    conn = get_connection()
    cur = conn.cursor()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    results = {"imported": [], "skipped": [], "errors": []}

    questions_raw = data.get("questions", [])
    if not isinstance(questions_raw, list):
        results["errors"].append("JSON 根目录必须有 'questions' 数组")
        return results

    for i, q in enumerate(questions_raw):
        try:
            # 必填字段校验
            required = ["question_title", "stage_code", "module_code", "one_line_answer"]
            missing = [f for f in required if not str(q.get(f, "")).strip()]
            if missing:
                results["errors"].append(
                    f"[{i}] 缺少必填字段: {', '.join(missing)}"
                )
                continue

            stage = q["stage_code"].strip().upper()
            module = q["module_code"].strip().upper()
            code = generate_code(conn, stage, module)

            cur.execute(
                """
                INSERT INTO question_master (
                    question_code, question_title, question_plain,
                    stage_code, module_code, question_type,
                    one_line_answer, detailed_answer, core_definition,
                    applicable_conditions, exceptions_boundary,
                    practical_steps, risk_warning,
                    scope_level, local_region,
                    answer_certainty, keywords,
                    high_frequency_flag, newbie_flag,
                    status, version_no, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', 1, ?, ?)
                """,
                (
                    code,
                    q["question_title"].strip(),
                    q.get("question_plain", q["question_title"].strip()),
                    stage,
                    module,
                    q.get("question_type", "type_whether"),
                    q["one_line_answer"].strip(),
                    q.get("detailed_answer", ""),
                    q.get("core_definition", ""),
                    q.get("applicable_conditions", ""),
                    q.get("exceptions_boundary", ""),
                    q.get("practical_steps", ""),
                    q.get("risk_warning", ""),
                    q.get("scope_level", "scope_national"),
                    q.get("local_region", ""),
                    q.get("answer_certainty", "certain_clear"),
                    q.get("keywords", ""),
                    1 if q.get("high_frequency_flag") else 0,
                    1 if q.get("newbie_flag") else 0,
                    now,
                    now,
                ),
            )
            question_id = cur.lastrowid

            # 更新记录
            cur.execute(
                """
                INSERT INTO question_update_log (
                    question_id, version_no, update_date, update_type,
                    update_reason, updated_by, reviewed_by, change_summary
                ) VALUES (?, 1, ?, 'create', ?, 'batch_import', ?, ?)
                """,
                (
                    question_id,
                    now,
                    "批量导入",
                    "batch_import",
                    f'创建问题 {code}',
                ),
            )

            # 标签：支持 tags 和 business_tags 两种字段名
            tag_ids = resolve_tag_ids(conn, q.get("tags", []) + q.get("business_tags", []))
            for idx, tag_id in enumerate(tag_ids):
                cur.execute(
                    """
                    INSERT OR IGNORE INTO question_tag_link
                    (question_id, tag_id, is_primary, display_order)
                    VALUES (?, ?, ?, ?)
                    """,
                    (question_id, tag_id, 1 if idx == 0 else 0, idx + 1),
                )

            # 政策依据
            for pl in q.get("policy_links", []):
                policy_id = resolve_policy_id(conn, pl.get("policy_code", ""))
                if policy_id:
                    cur.execute(
                        """
                        INSERT OR IGNORE INTO question_policy_link
                        (question_id, policy_id, support_type, support_note, display_order)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            question_id,
                            policy_id,
                            pl.get("support_type", "support_direct"),
                            pl.get("support_note", ""),
                            1,
                        ),
                    )

            results["imported"].append(code)

        except Exception as e:
            results["errors"].append(f"[{i}] 导入失败: {str(e)}")
            continue

    # 第二轮：建立关联（等所有问题都有了 ID）
    # 重新查询所有新导入问题的 ID
    new_codes = results["imported"]
    for code in new_codes:
        # 在原始 JSON 中找到这条
        for q in questions_raw:
            s, m = q["stage_code"].strip().upper(), q["module_code"].strip().upper()
            prefix = f"{s}-{m}-"
            if not code.startswith(prefix):
                continue

            question_id = resolve_question_id(conn, code)
            if not question_id:
                continue

            for rel in q.get("relations", []):
                rel_id = resolve_question_id(conn, rel.get("question_code", ""))
                if rel_id:
                    cur.execute(
                        """
                        INSERT OR IGNORE INTO question_relation
                        (question_id, related_id, relation_type, display_order)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            question_id,
                            rel_id,
                            rel.get("relation_type", "related"),
                            1,
                        ),
                    )
                    # 双向关联：目标也指向回来
                    cur.execute(
                        """
                        INSERT OR IGNORE INTO question_relation
                        (question_id, related_id, relation_type, display_order)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            rel_id,
                            question_id,
                            rel.get("relation_type", "related"),
                            1,
                        ),
                    )

    conn.commit()
    conn.close()
    return results


def main():
    if len(sys.argv) < 2:
        print("用法: python batch_import_questions.py <questions.json>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.exists():
        print(f"文件不存在: {json_path}")
        sys.exit(1)

    print(f"读取: {json_path}")
    data = load_json(json_path)
    questions_count = len(data.get("questions", []))
    print(f"共 {questions_count} 条问题待导入")

    results = import_questions(data)

    print(f"\n=== 导入结果 ===")
    print(f"成功: {len(results['imported'])} 条")
    for code in results["imported"]:
        print(f"  + {code}")

    if results["skipped"]:
        print(f"\n跳过: {len(results['skipped'])} 条")
        for s in results["skipped"]:
            print(f"  - {s}")

    if results["errors"]:
        print(f"\n错误: {len(results['errors'])} 条")
        for e in results["errors"]:
            print(f"  ! {e}")

    print(f"\n数据库: {DB_PATH}")


if __name__ == "__main__":
    main()
