#!/usr/bin/env python3
# ============================================================
# scripts/content/backfill_missing_relations.py
# 为缺少关联问题的条目补充低风险同模块关联
# 用法: python scripts/content/backfill_missing_relations.py [--dry-run]
# ============================================================

import os
import re
import sqlite3
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'db', 'tax_knowledge.db')


def connect_db():
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库文件不存在: {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def tokenize_keywords(row):
    raw = " ".join(filter(None, [
        row["keywords"] or "",
        row["question_title"] or "",
        row["question_plain"] or "",
    ]))
    parts = re.split(r"[\s,，、；;|/（）()]+", raw)
    return {p.strip() for p in parts if len(p.strip()) >= 2}


def candidate_score(source, target):
    score = 0
    if source["module_code"] == target["module_code"]:
        score += 5
    if source["stage_code"] == target["stage_code"]:
        score += 3
    if source["question_type"] == target["question_type"]:
        score += 2

    src_tokens = source["_tokens"]
    tgt_tokens = target["_tokens"]
    overlap = src_tokens & tgt_tokens
    score += min(len(overlap), 4)

    if source["high_frequency_flag"] and target["high_frequency_flag"]:
        score += 1

    return score, overlap


def main():
    dry_run = "--dry-run" in sys.argv
    conn = connect_db()

    all_questions = conn.execute("""
        SELECT id, question_code, question_title, question_plain, keywords,
               stage_code, module_code, question_type,
               high_frequency_flag, newbie_flag
        FROM question_master
        WHERE status = 'active'
    """).fetchall()

    question_map = []
    for row in all_questions:
        item = dict(row)
        item["_tokens"] = tokenize_keywords(row)
        question_map.append(item)

    missing_rows = conn.execute("""
        SELECT q.id, q.question_code, q.question_title, q.question_plain, q.keywords,
               q.stage_code, q.module_code, q.question_type,
               q.high_frequency_flag, q.newbie_flag
        FROM question_master q
        LEFT JOIN question_relation r ON q.id = r.question_id
        WHERE q.status = 'active' AND r.id IS NULL
        ORDER BY q.module_code, q.question_code
    """).fetchall()

    if not missing_rows:
        print("✅ 所有 active 问题均已有关联问题")
        conn.close()
        return

    inserted = 0
    covered_questions = 0

    for row in missing_rows:
        source = dict(row)
        source["_tokens"] = tokenize_keywords(row)

        candidates = []
        for target in question_map:
            if target["id"] == source["id"]:
                continue
            if target["module_code"] != source["module_code"]:
                continue

            score, overlap = candidate_score(source, target)
            if score < 8:
                continue
            candidates.append((score, len(overlap), target))

        candidates.sort(key=lambda item: (-item[0], -item[1], item[2]["question_code"]))
        selected = []
        seen_codes = set()
        for _, _, target in candidates:
            if target["question_code"] in seen_codes:
                continue
            selected.append(target)
            seen_codes.add(target["question_code"])
            if len(selected) >= 3:
                break

        if not selected:
            continue

        covered_questions += 1
        if dry_run:
            print(f"{source['question_code']} -> {', '.join(t['question_code'] for t in selected)}")
            continue

        for idx, target in enumerate(selected, start=1):
            conn.execute("""
                INSERT OR IGNORE INTO question_relation
                    (question_id, related_id, relation_type, display_order)
                VALUES (?, ?, 'related', ?)
            """, (source["id"], target["id"], idx))
            conn.execute("""
                INSERT OR IGNORE INTO question_relation
                    (question_id, related_id, relation_type, display_order)
                VALUES (?, ?, 'related', ?)
            """, (target["id"], source["id"], 99))
            inserted += 1

    if not dry_run:
        conn.commit()
        print(f"✅ 已为 {covered_questions} 条问题补充关联")
        print(f"✅ 新增 question_relation 记录: {inserted}")
        remaining = conn.execute("""
            SELECT COUNT(*) FROM question_master q
            LEFT JOIN question_relation r ON q.id = r.question_id
            WHERE q.status = 'active' AND r.id IS NULL
        """).fetchone()[0]
        print(f"📋 剩余缺关联问题: {remaining} 条")
    else:
        print(f"🔍 [Dry Run] 可覆盖缺关联问题: {covered_questions} 条")

    conn.close()


if __name__ == "__main__":
    main()
