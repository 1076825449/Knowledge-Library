#!/usr/bin/env python3
# ============================================================
# scripts/content/add_scope_local.py
# 历史脚本占位：原始内容已损坏，保留路径供后续人工重建
# ============================================================

import sys


def main():
    message = """
此脚本对应的历史批量内容已损坏，原文件存在无法解析的字符串与引号问题。

当前项目的地方口径建设请优先使用：
1. data/imports/ 下的结构化 JSON 批次文件
2. scripts/content/batch_import_questions.py
3. ROADMAP.md 中关于“地方口径、结构质量、录入闭环”的当前执行口径

如果需要重新导入 scope_local 内容，请基于当前数据库、枚举口径和导入格式重建新批次，
不要继续依赖这个历史脚本。
""".strip()
    print(message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
