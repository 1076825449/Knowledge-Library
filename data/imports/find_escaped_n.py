"""精确分析：找出所有 \\n (0x5c 0x6e) 出现的位置和上下文"""
with open('questions_batch13_pref_etax.json', 'rb') as f:
    raw = f.read()

# Find all \n (0x5c 0x6e) in original
print("All \\n (0x5c 0x6e) in original file:")
for i in range(len(raw) - 1):
    if raw[i] == 0x5c and raw[i+1] == 0x6e:
        # What's before and after?
        before = raw[max(0,i-10):i]
        after = raw[i+2:min(len(raw), i+12)]
        before_str = before.decode('utf-8', errors='replace')
        after_str = after.decode('utf-8', errors='replace')
        print(f"  pos {i}: ...{repr(before_str)}\\n{repr(after_str)}...")
