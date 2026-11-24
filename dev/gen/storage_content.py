# Sinh tracks/storage/content.vi.js và content.en.js từ MỘT nguồn (cùng cây khoá ở hai ngôn ngữ).
# Chạy: python dev/gen/storage_content.py   (công cụ phát triển; site không cần file này)
# Mỗi chương là một module storage_v2_<id>.py: add(a) với a(k, vi, en=None); tuỳ chọn SEC_ORDER = {chương: [mục…]}.
import json, os, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
P = 'track.storage.'
E = []
def a(k, vi, en=None): E.append((P + k, vi, vi if en is None else en))

# ---------------- chung ----------------
a('title', 'Lưu dữ liệu trên Android', 'Saving Data on Android')
a('summary', 'Chọn nơi lưu theo loại dữ liệu, file riêng của app và ghi an toàn, từ SharedPreferences sang DataStore, Room (entity, DAO, Flow, quan hệ, giao dịch, migration), offline-first và đồng bộ nền bằng WorkManager, shared storage và MediaStore, sao lưu và dữ liệu nhạy cảm. Theo tài liệu chính thức của Android, đối chiếu với sách Saving Data on Android.',
  'Choosing where to store data by its kind, app-specific files and safe writes, from SharedPreferences to DataStore, Room (entities, DAOs, Flow, relations, transactions, migrations), offline-first and background sync with WorkManager, shared storage and MediaStore, backup and sensitive data. Following the official Android docs, compared with the Saving Data on Android book.')
a('preset.choose', 'Lưu dữ liệu · chọn nơi lưu theo loại dữ liệu', 'Saving data · choosing where to store by kind of data')
a('col.subject', 'Thành phần', 'Component')
for k, vi, en in [('done', 'xong', 'done'), ('surprise', 'có vấn đề', 'has a problem'), ('skipped', 'bỏ qua', 'skipped'), ('broken', 'lỗi', 'error')]:
    a('st.' + k, vi, en)
a('fam.done', 'chạy đúng', 'working'); a('fam.fail', 'có vấn đề', 'has a problem'); a('fam.none', 'chưa tới', 'not reached')
for k, vi, en in [('observe', 'quan sát', 'observe'), ('run', 'chạy', 'run'), ('write', 'ghi', 'write'), ('skip', 'bỏ qua', 'skip'), ('exception', 'ném ngoại lệ', 'exception thrown'), ('complete', 'hoàn tất', 'complete')]:
    a('kind.' + k, vi, en)

MODULES = ('storage_v2_h1', 'storage_v2_h2', 'storage_v2_h3')   # giữ dấu phẩy cuối
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
    open(os.path.join(ROOT, 'tracks', 'storage', 'content.%s.js' % lang), 'w', encoding='utf-8', newline='\n').write(
        '/* Nội dung track Lưu dữ liệu (%s). SINH TỰ ĐỘNG từ dev/gen/storage_content.py. */\nADE.addTrackStrings(\'storage\', \'%s\', {\n%s\n});\n' % (lang, lang, body))
print(len(E), 'keys')
