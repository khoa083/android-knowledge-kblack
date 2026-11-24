# Sinh tracks/cleancode/content.vi.js và content.en.js từ MỘT nguồn (cùng cây khoá ở hai ngôn ngữ).
# Chạy: python dev/gen/cleancode_content.py   (công cụ phát triển; site không cần file này)
# Mỗi chương là một module cleancode_v2_<id>.py: add(a) với a(k, vi, en=None); tuỳ chọn SEC_ORDER = {chương: [mục…]}.
import json, os, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
P = 'track.cleancode.'
E = []
def a(k, vi, en=None): E.append((P + k, vi, vi if en is None else en))

# ---------------- chung ----------------
a('title', 'Mã sạch và kỷ luật làm nghề', 'Clean Code and Craft')
a('summary', 'Viết mã mà người sau đọc và sửa được: mã vừa trong đầu, đặt tên và tách hàm, đóng gói và parse một lần, TDD và thiết kế test, refactor từng bước nhỏ, gỡ lỗi có phương pháp, SOLID và nguyên lý thành phần, làm việc nhóm và tính chuyên nghiệp. Ví dụ bằng Kotlin trên app Hẹn Khám; mọi quy tắc là heuristic có ghi tên tác giả (Seemann, Martin, Moskała).',
  'Writing code the next person can read and change: code that fits in your head, naming and splitting functions, encapsulation and parsing once, TDD and test design, refactoring in small steps, methodical debugging, SOLID and component principles, teamwork and professionalism. Examples in Kotlin on the ClinicBook app; every rule is a heuristic credited to its author (Seemann, Martin, Moskała).')
a('col.subject', 'Thành phần', 'Component')
for k, vi, en in [('done', 'xong', 'done'), ('surprise', 'có vấn đề', 'has a problem'), ('skipped', 'bỏ qua', 'skipped'), ('broken', 'lỗi', 'error')]:
    a('st.' + k, vi, en)
a('fam.done', 'ổn', 'fine'); a('fam.fail', 'có vấn đề', 'has a problem'); a('fam.none', 'chưa tới', 'not reached')
for k, vi, en in [('observe', 'đọc', 'read'), ('run', 'chạy', 'run'), ('write', 'sửa', 'edit'), ('skip', 'bỏ qua', 'skip'), ('exception', 'lỗi', 'failure'), ('complete', 'hoàn tất', 'complete')]:
    a('kind.' + k, vi, en)

MODULES = ('cleancode_v2_j1', 'cleancode_v2_j2', 'cleancode_v2_j3', 'cleancode_v2_j4', 'cleancode_v2_j5', 'cleancode_v2_j6', 'cleancode_v2_j7', 'cleancode_v2_j8', 'cleancode_v2_j9', 'cleancode_v2_j10', 'cleancode_v2_j11')   # giữ dấu phẩy cuối
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
bad = [k for k, v, e in E if any(ord(ch) < 32 and ch != '\n' for ch in v + e)]; assert not bad, ('ký tự điều khiển (ví dụ \\b viết nhầm thành backspace)', bad)
keys = [k for k, _, _ in E]; dup = sorted(set(k for k in keys if keys.count(k) > 1)); assert not dup, dup
for lang, idx in (('vi', 1), ('en', 2)):
    body = ',\n'.join('  %s: %s' % (json.dumps(e[0]), json.dumps(norm(e[idx]), ensure_ascii=False)) for e in E)
    open(os.path.join(ROOT, 'tracks', 'cleancode', 'content.%s.js' % lang), 'w', encoding='utf-8', newline='\n').write(
        '/* Nội dung track Mã sạch và kỷ luật làm nghề (%s). SINH TỰ ĐỘNG từ dev/gen/cleancode_content.py. */\nADE.addTrackStrings(\'cleancode\', \'%s\', {\n%s\n});\n' % (lang, lang, body))
print(len(E), 'keys')
