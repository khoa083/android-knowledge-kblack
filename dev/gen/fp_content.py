# Sinh tracks/fp/content.vi.js và content.en.js từ MỘT nguồn (cùng cây khoá ở hai ngôn ngữ).
# Chạy: python dev/gen/fp_content.py   (công cụ phát triển; site không cần file này)
# Mỗi chương là một module fp_v2_<id>.py: add(a) với a(k, vi, en=None); tuỳ chọn SEC_ORDER = {chương: [mục…]}.
import json, os, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
P = 'track.fp.'
E = []
def a(k, vi, en=None): E.append((P + k, vi, vi if en is None else en))

# ---------------- chung ----------------
a('title', 'Lập trình hàm với Kotlin', 'Functional Programming in Kotlin')
a('summary', 'Dùng lập trình hàm để viết mã Android an toàn hơn. Mười chương: hàm thuần và referential transparency (gọi hàm có thể thay bằng kết quả của nó), bất biến và đệ quy, ghép hàm, kiểu dữ liệu đại số, lỗi là giá trị, map và flatMap, validate gom lỗi, state thuần bằng reducer, functional core và imperative shell, cập nhật state lồng sâu. Ví dụ Kotlin trên app Hẹn Khám; khi dùng Arrow (thư viện bên ngoài), luôn có bản Kotlin thuần đi trước.',
  'Using functional programming to write safer Android code. Ten chapters: pure functions and referential transparency (a call can be replaced by its result), immutability and recursion, composing functions, algebraic data types, errors as values, map and flatMap, validation that collects errors, pure state with reducers, functional core and imperative shell, updating deeply nested state. Kotlin examples on the ClinicBook app; whenever Arrow (an external library) is used, a plain Kotlin version comes first.')
a('col.subject', 'Thành phần', 'Component')
for k, vi, en in [('done', 'xong', 'done'), ('surprise', 'có vấn đề', 'has a problem'), ('skipped', 'bỏ qua', 'skipped'), ('broken', 'lỗi', 'error')]:
    a('st.' + k, vi, en)
a('fam.done', 'ổn', 'fine'); a('fam.fail', 'có vấn đề', 'has a problem'); a('fam.none', 'chưa tới', 'not reached')
for k, vi, en in [('observe', 'đọc', 'read'), ('run', 'chạy', 'run'), ('write', 'sửa', 'edit'), ('skip', 'bỏ qua', 'skip'), ('exception', 'lỗi', 'failure'), ('complete', 'hoàn tất', 'complete')]:
    a('kind.' + k, vi, en)

MODULES = ('fp_v2_p1', 'fp_v2_p2', 'fp_v2_p3', 'fp_v2_p4', 'fp_v2_p5', 'fp_v2_p6', 'fp_v2_p7', 'fp_v2_p8', 'fp_v2_p9', 'fp_v2_p10')   # giữ dấu phẩy cuối
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

# Quyết định 2026-11-24: bỏ mục "Chương này giản lược những gì" (khoá .sec.honest.) khỏi site; nguồn nằm ở docs/research.
E[:] = [e for e in E if '.sec.honest.' not in e[0]]
def norm(s): return unicodedata.normalize('NFC', s)
bad = [k for k, v, e in E if any(ord(ch) < 32 and ch != '\n' for ch in v + e)]; assert not bad, ('ký tự điều khiển (ví dụ \\b viết nhầm thành backspace)', bad)
keys = [k for k, _, _ in E]; dup = sorted(set(k for k in keys if keys.count(k) > 1)); assert not dup, dup
for lang, idx in (('vi', 1), ('en', 2)):
    body = ',\n'.join('  %s: %s' % (json.dumps(e[0]), json.dumps(norm(e[idx]), ensure_ascii=False)) for e in E)
    open(os.path.join(ROOT, 'tracks', 'fp', 'content.%s.js' % lang), 'w', encoding='utf-8', newline='\n').write(
        '/* Nội dung track Lập trình hàm với Kotlin (%s). SINH TỰ ĐỘNG từ dev/gen/fp_content.py. */\nADE.addTrackStrings(\'fp\', \'%s\', {\n%s\n});\n' % (lang, lang, body))
print(len(E), 'keys')
