import io, re, sys, glob, os
sys.stdout.reconfigure(encoding='utf-8')
# dùng: terms.py <track> <chapter-prefix> <model-prefix> [<vz-prefix>]
# in lần xuất hiện ĐẦU TIÊN (theo thứ tự trang: essence, hook, mô phỏng, các mục) của từng thuật ngữ đã từng cần giải thích
TERMS = ['PERT', 'TDD', 'OTP', 'cam kết ngầm', 'implied commitment', 'PR', 'LGTM', 'diff', 'squash', 'review', 'checklist', 'nhánh', 'branch', 'Room', 'module', 'Gradle', 'ABI', 'DI', 'data class', 'bắc cầu', 'transitively', 'thành phần', 'component', 'Ca', 'Ce', 'build lại', 'rebuild', 'SOLID', 'SRP', 'OCP', 'DIP', 'giao diện', 'commit', 'refactor', 'mock', 'fake', 'stub', 'spy', 'TDD', 'build', 'HEAD', 'UTC', 'cache', 'interface', 'constructor', 'getter',
         'side effect', 'debugger', 'tag', 'git reset', 'bisect', 'regression', 'hồi quy', 'assertion', 'coverage', 'độ phủ', 'invariant', 'immutable', 'bất biến',
         'DTO', 'SDK', 'null', 'typealias', 'value class', 'IDE', 'API', 'JVM', 'suspend', 'coroutine', 'ViewModel', 'Compose', 'Flow', 'Room', 'DAO',
         'transaction', 'rollback', 'index', 'schema', 'migration', 'cache', 'latency', 'throughput', 'idempotent', 'retry', 'backoff', 'sealed', 'Result', 'Either']
track, ch, model = sys.argv[1], sys.argv[2], sys.argv[3]
vz = sys.argv[4] if len(sys.argv) > 4 else ''
rows = {}
for lang in ('vi', 'en'):
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tracks', track, 'content.%s.js' % lang)
    for line in io.open(f, encoding='utf-8'):
        m = re.match(r'\s*"([^"]+)"\s*:\s*(.*)', line)
        if not m:
            continue
        k, v = m.group(1), m.group(2).rstrip(',').strip('"')
        v = v.replace('\\n', ' ')
        rows.setdefault(lang, []).append((k.replace('track.' + track + '.', ''), v))


def order(k):
    if k.endswith(ch + '.essence'):
        return 0
    if '.sec.hook.' in k and k.startswith(ch + '.'):
        return 1
    if k.startswith('m.' + model + '.') and not k.startswith('m.' + model + '.co.'):
        return 2
    if k.startswith('m.' + model + '.co.'):
        return 3
    if k.startswith('vz.' + vz + '.') if vz else False:
        return 4
    if k.startswith(ch + '.sec.'):
        return 5
    if k.startswith(ch + '.quiz'):
        return 6
    return None


for lang in ('vi', 'en'):
    items = [(order(k), i, k, v) for i, (k, v) in enumerate(rows[lang]) if order(k) is not None]
    items.sort(key=lambda t: (t[0], t[1]))
    print('=== ' + lang)
    seen = set()
    for t in TERMS:
        if t in seen:
            continue
        rx = re.compile(r'(?<![A-Za-z])' + re.escape(t) + r'(?![A-Za-z])', re.I if t.islower() else 0)
        for o, i, k, v in items:
            mm = rx.search(v)
            if mm:
                seen.add(t)
                snip = v[max(0, mm.start() - 25): mm.end() + 70].replace('\\n', ' ')
                glossed = '(' in v[mm.end(): mm.end() + 3] or ' (' in v[mm.end(): mm.end() + 2]
                print('%-12s %s %-34s ..%s..' % (t, 'G' if glossed else '-', k[:34], snip))
                break
