# Sinh tracks/arch/content.vi.js và content.en.js từ MỘT nguồn (cùng cây khoá ở hai ngôn ngữ).
# Chạy: python dev/gen/arch_content.py   (công cụ phát triển; site không cần file này)
# Mỗi chương là một module arch_v2_<id>.py: add(a) với a(k, vi, en=None); tuỳ chọn SEC_ORDER = {chương: [mục…]}.
import json, os, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
P = 'track.arch.'
E = []
def a(k, vi, en=None): E.append((P + k, vi, vi if en is None else en))

# ---------------- chung ----------------
a('title', 'Kiến trúc app Android', 'Android App Architecture')
a('summary', 'Vì sao cần kiến trúc, các tầng UI, domain, data và hướng phụ thuộc, state và sự kiện, repository và offline-first, DI với Hilt, MVVM và MVI, lỗi qua các tầng, module hóa và kiểm thử. Theo hướng dẫn chính thức của Android, đối chiếu với sách Clean Architecture.',
  'Why architecture matters, the UI, domain and data layers and the direction of dependencies, state and events, repositories and offline-first, DI with Hilt, MVVM and MVI, errors across layers, modularization and testing. Following Android\'s official guide, compared with the Clean Architecture books.')
a('preset.god', 'Kiến trúc · Activity làm mọi thứ so với tách tầng', 'Architecture · an Activity doing everything versus layers')
a('col.subject', 'Tầng', 'Layer')
for k, vi, en in [('done', 'xong', 'done'), ('surprise', 'có vấn đề', 'has a problem'), ('skipped', 'không có', 'absent'), ('broken', 'lỗi', 'error')]:
    a('st.' + k, vi, en)
a('fam.done', 'làm đúng việc', 'doing its job'); a('fam.fail', 'có vấn đề', 'has a problem'); a('fam.none', 'không có tầng này', 'layer absent')
for k, vi, en in [('observe', 'quan sát', 'observe'), ('run', 'chạy', 'run'), ('write', 'sửa mã', 'edit code'), ('skip', 'bỏ qua', 'skip'), ('exception', 'ném ngoại lệ', 'exception thrown'), ('complete', 'hoàn tất', 'complete')]:
    a('kind.' + k, vi, en)

MODULES = ('arch_v2_g1', 'arch_v2_g2', 'arch_v2_g3')   # giữ dấu phẩy cuối
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
    open(os.path.join(ROOT, 'tracks', 'arch', 'content.%s.js' % lang), 'w', encoding='utf-8', newline='\n').write(
        '/* Nội dung track Kiến trúc app (%s). SINH TỰ ĐỘNG từ dev/gen/arch_content.py. */\nADE.addTrackStrings(\'arch\', \'%s\', {\n%s\n});\n' % (lang, lang, body))
print(len(E), 'keys')
