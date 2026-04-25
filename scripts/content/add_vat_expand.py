#!/usr/bin/env python3
# ============================================================
# scripts/content/add_vat_expand.py
# 历史脚本占位：原始内容已损坏，保留路径供后续人工重建
# ============================================================

import sys


def main():
    message = """
此脚本原用于向历史 JSON 批次追加 VAT 问题，但原始文件已损坏，无法安全执行。

后续如需补充 VAT 模块内容，请改用：
1. data/imports/ 下的现行批次 JSON
2. scripts/content/batch_import_questions.py
3. scripts/content/priority_reinforce.py 生成的最新补强清单

保留本文件仅为兼容旧路径，避免语法错误继续影响仓库维护。
""".strip()
    print(message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
