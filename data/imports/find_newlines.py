"""直接看 fixed text 在报错位置的字节级内容"""
with open('questions_batch13_pref_etax.json', 'rb') as f:
    raw = f.read()

result = []
i = 0
in_string = False

while i < len(raw):
    b = raw[i]
    if b == 0x22:
        in_string = not in_string
        result.append(b)
        i += 1
    elif b == 0x0a:
        if in_string:
            result.extend(b'\\n')
        else:
            result.append(b)
        i += 1
    else:
        result.append(b)
        i += 1

text = bytes(result).decode('utf-8')

# Error is at pos 1554 (1-indexed from json.loads perspective, 0-indexed from string)
# json.JSONDecodeError.pos is 0-indexed character offset
# The error is: Expecting ',' delimiter at pos 1554
# So char[1554] is the problem
print(f"Character at 1554: {repr(text[1554])}")
print(f"Chars 1540-1570: {repr(text[1540:1570])}")
print()

# Find all unescaped newlines in the fixed text
print("=== All newlines in fixed text ===")
for i, c in enumerate(text):
    if c == '\n':
        ctx = text[max(0,i-30):i+30]
        print(f"  pos {i}: {repr(ctx)}")
        if i > 1600:
            print("  ... (stopping)")
            break
