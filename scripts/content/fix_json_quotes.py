#!/usr/bin/env python3
"""修复JSON文件中未转义的引号和反斜杠问题"""
import json, re, sys

def fix_content(text):
    """对JSON字符串值内容进行转义处理"""
    if not text:
        return text
    # 替换反斜杠（除了已有转义的）
    # 替换中文/英文引号为转义的ASCII引号
    result = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        # 处理反斜杠：如果是未转义的反斜杠（不是\\或\/），改为\\
        if c == '\\' and i + 1 < n:
            next_c = text[i+1]
            if next_c not in ('\\', '/', 'n', 'r', 't', '"', 'u'):
                # 未转义的反斜杠
                result.append('\\\\')
                i += 1
                continue
        # 处理引号：中文左引号、"、"改为转义引号
        if c in ('\u201c', '\u201d', '"'):  # " " "
            result.append('\\"')
        else:
            result.append(c)
        i += 1
    return ''.join(result)

def fix_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()

    # 简单粗暴方法：把所有未在JSON语法位置的中文引号替换
    # 策略：把"和"替换为'"'（对JSON安全的表示）
    # 但更好的方式：直接用json模块重新编码

    # 尝试解析现有内容，找出问题字段
    # 替换所有 \" 为 "  (反斜杠引号)检查
    lines = raw.split('\n')
    fixed_lines = []

    for line in lines:
        # 跳过空行和结构行（只有冒号的行）
        colon_pos = line.find('": "')
        if colon_pos == -1:
            fixed_lines.append(line)
            continue

        # 找到冒号后面的内容区域
        content_start = colon_pos + 3  # '": "'
        # 找到行尾的 '",' 或 '"'
        if line.rstrip().endswith(','):
            content_end = len(line) - 2  # 去掉 '",'
            trailing = '",'
        elif line.rstrip().endswith('"'):
            content_end = len(line) - 1  # 去掉 '"'
            trailing = '"'
        else:
            fixed_lines.append(line)
            continue

        # 提取字段名和内容
        field_part = line[:content_start]
        content_raw = line[content_start:content_end]

        # 修复内容中的转义问题
        fixed_content = fix_content(content_raw)

        fixed_lines.append(field_part + fixed_content + trailing)

    fixed_raw = '\n'.join(fixed_lines)

    # 用json模块验证
    try:
        data = json.loads(fixed_raw)
        print(f"JSON解析成功！共 {len(data.get('questions', []))} 条问题")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"已重写文件: {filepath}")
        return True
    except json.JSONDecodeError as e:
        print(f"仍无法解析: {e}")
        print(f"问题行附近: {repr(fixed_raw[max(0,e.pos-50):e.pos+50])}")
        return False

if __name__ == '__main__':
    for f in sys.argv[1:]:
        print(f"处理: {f}")
        fix_json_file(f)
