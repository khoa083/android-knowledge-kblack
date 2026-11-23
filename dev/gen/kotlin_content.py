# Sinh tracks/kotlin/content.vi.js và content.en.js từ MỘT nguồn (cùng cây khoá ở hai ngôn ngữ).
# Chạy: python dev/gen/kotlin_content.py   (công cụ phát triển; site không cần file này)
# Mỗi chương là một module kotlin_v2_<id>.py: add(a) với a(k, vi, en=None); tuỳ chọn SEC_ORDER = {chương: [mục…]}.
import json, os, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
P = 'track.kotlin.'
E = []
def a(k, vi, en=None): E.append((P + k, vi, vi if en is None else en))

# ---------------- chung ----------------
a('title', 'Kotlin: cơ chế ngôn ngữ', 'Kotlin: How the Language Works')
a('summary', 'Từ val, kiểu và hàm cho người mới, tới những cơ chế hay gây bug trên Android: null và platform type, equals/hashCode, sealed, thứ tự khởi tạo, lambda và inline, sequence, variance, delegate.',
  'From val, types and functions for beginners to the mechanisms behind real Android bugs: null and platform types, equals/hashCode, sealed, initialization order, lambdas and inline, sequences, variance, delegates.')
a('preset.eval', 'Kotlin · chia nguyên, tràn số và when', 'Kotlin · integer division, overflow and when')
a('col.subject', 'Giai đoạn', 'Stage')
a('st.done', 'xong', 'done')
a('st.surprise', 'kết quả bất ngờ', 'surprising result')
a('fam.done', 'xong', 'done')
a('fam.surprise', 'kết quả bất ngờ (không có lỗi)', 'surprising result (no error)')
a('st.broken', 'không được', 'not allowed')
a('st.skipped', 'không áp dụng', 'not applicable')
a('st.crashed', 'ngoại lệ lúc chạy', 'exception at runtime')
a('st.running', 'đang khởi tạo', 'initialising')
a('fam.running', 'đang chạy', 'running')
a('fam.fail', 'lỗi (biên dịch hoặc lúc chạy)', 'error (compile time or runtime)')
a('fam.na', 'không áp dụng', 'not applicable')
for k, vi, en in [('observe', 'đọc mã', 'read code'), ('check', 'kiểm kiểu (biên dịch)', 'type check (compile)'), ('run', 'chạy', 'run'), ('write', 'gán', 'assign'), ('skip', 'bỏ qua', 'skip')]:
    a('kind.' + k, vi, en)

MODULES = ('kotlin_v2_k1', 'kotlin_v2_k2', 'kotlin_v2_k3')   # giữ dấu phẩy cuối
for mod in MODULES:
    assert os.path.exists(os.path.join(HERE, mod + '.py')), 'thiếu module ' + mod
    mm = __import__(mod)
    mm.add(a)
    for chap, order in getattr(mm, 'SEC_ORDER', {}).items():
        pre = P + chap + '.sec.'
        idx = [i for i, e in enumerate(E) if e[0].startswith(pre)]
        items = [E[i] for i in idx]
        items.sort(key=lambda e: order.index(e[0][len(pre):].split('.')[0]) if e[0][len(pre):].split('.')[0] in order else len(order))
        first = idx[0]; sidx = set(idx)
        E[:] = [e for i, e in enumerate(E) if i not in sidx]
        E[first:first] = items

def norm(s): return unicodedata.normalize('NFC', s)
keys = [k for k, _, _ in E]; dup = sorted(set(k for k in keys if keys.count(k) > 1)); assert not dup, dup
same = [k for k, vi, en in E if vi == en and len(vi) > 40 and not k.endswith('.kt') and '.badge' not in k]
for lang, idx in (('vi', 1), ('en', 2)):
    body = ',\n'.join('  %s: %s' % (json.dumps(e[0]), json.dumps(norm(e[idx]), ensure_ascii=False)) for e in E)
    open(os.path.join(ROOT, 'tracks', 'kotlin', 'content.%s.js' % lang), 'w', encoding='utf-8', newline='\n').write(
        '/* Nội dung track Kotlin (%s). SINH TỰ ĐỘNG từ dev/gen/kotlin_content.py. */\nADE.addTrackStrings(\'kotlin\', \'%s\', {\n%s\n});\n' % (lang, lang, body))
print(len(E), 'keys', ('| vi=en check: ' + ', '.join(same)) if same else '')
