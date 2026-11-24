# Sinh tracks/sysdesign/content.vi.js và content.en.js từ MỘT nguồn (cùng cây khoá ở hai ngôn ngữ).
# Chạy: python dev/gen/sysdesign_content.py   (công cụ phát triển; site không cần file này)
# Mỗi chương là một module sysdesign_v2_<id>.py: add(a) với a(k, vi, en=None); tuỳ chọn SEC_ORDER = {chương: [mục…]}.
import json, os, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
P = 'track.sysdesign.'
E = []
def a(k, vi, en=None): E.append((P + k, vi, vi if en is None else en))

# ---------------- chung ----------------
a('title', 'Thiết kế hệ thống phía mobile', 'Mobile System Design')
a('summary', 'Nhìn từ phía app Android: từ đề bài tới kế hoạch, process và bộ nhớ, luồng và khóa, chọn kênh giao tiếp, mạng không tin cậy, cache, phân trang, nhiều thiết bị và xung đột, thông báo đẩy, ảnh và tệp lớn, khởi động và pin, phát hành an toàn, và một bài mẫu app nhắn tin. Theo tài liệu chính thức của Android và Firebase, đối chiếu sách system design.',
  'Seen from the Android app: from a brief to a plan, processes and memory, threads and locks, choosing a channel, unreliable networks, caching, paging, multiple devices and conflicts, push notifications, images and large files, startup and battery, safe releases, and a worked messaging app. Following the official Android and Firebase docs, compared with system design books.')
a('col.subject', 'Thành phần', 'Component')
for k, vi, en in [('done', 'xong', 'done'), ('surprise', 'có vấn đề', 'has a problem'), ('skipped', 'bỏ qua', 'skipped'), ('broken', 'lỗi', 'error')]:
    a('st.' + k, vi, en)
a('fam.done', 'chạy đúng', 'working'); a('fam.fail', 'có vấn đề', 'has a problem'); a('fam.none', 'chưa tới', 'not reached')
for k, vi, en in [('observe', 'quan sát', 'observe'), ('run', 'chạy', 'run'), ('write', 'ghi', 'write'), ('skip', 'bỏ qua', 'skip'), ('exception', 'ném ngoại lệ', 'exception thrown'), ('complete', 'hoàn tất', 'complete')]:
    a('kind.' + k, vi, en)

MODULES = ('sysdesign_v2_i1', 'sysdesign_v2_i2', 'sysdesign_v2_i3', 'sysdesign_v2_i4', 'sysdesign_v2_i5', 'sysdesign_v2_i6', 'sysdesign_v2_i7', 'sysdesign_v2_i8')   # giữ dấu phẩy cuối
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
for lang, idx in (('vi', 1), ('en', 2)):
    body = ',\n'.join('  %s: %s' % (json.dumps(e[0]), json.dumps(norm(e[idx]), ensure_ascii=False)) for e in E)
    open(os.path.join(ROOT, 'tracks', 'sysdesign', 'content.%s.js' % lang), 'w', encoding='utf-8', newline='\n').write(
        '/* Nội dung track Thiết kế hệ thống phía mobile (%s). SINH TỰ ĐỘNG từ dev/gen/sysdesign_content.py. */\nADE.addTrackStrings(\'sysdesign\', \'%s\', {\n%s\n});\n' % (lang, lang, body))
print(len(E), 'keys')
