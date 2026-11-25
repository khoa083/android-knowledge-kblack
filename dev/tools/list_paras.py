"""Liệt kê các đoạn lời giảng (p, note) của một module chương, kèm tên mục và chuỗi tiếng Việt, để chuẩn bị viết lại.
Dùng: python dev/tools/list_paras.py dev/gen/coroutines_v2_a3.py [độ dài tối đa]"""
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
L = io.open(sys.argv[1], encoding='utf-8').read().split('\n')
width = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
sec = None
for i, line in enumerate(L):
    m = re.match(r"    S_? = '([a-z0-9]+)'", line)
    if m:
        sec = m.group(1)
    m2 = re.match(r"    B\(C, S_?, (\d+), '(p|note)',(.*)", line)
    if m2:
        rest = m2.group(3).strip()
        vi = rest if rest else L[i + 1].strip()
        print('==', sec, m2.group(1), m2.group(2), '|', vi[:width])
    m3 = re.match(r"    m\('(overview|wrapup)', (.*)", line)
    if m3:
        print('==', m3.group(1), '|', m3.group(2)[:width])
