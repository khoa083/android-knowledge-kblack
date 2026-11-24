import io, re, sys, glob, collections, os
sys.stdout.reconfigure(encoding='utf-8')
# dùng: lint.py [track|*] [tiền tố] [dump|list]
#   không tham số: cả site, đếm theo track
#   có tiền tố: in từng chỗ khớp; thêm "dump": in toàn bộ giá trị (vi rồi en) theo thứ tự khóa
track = sys.argv[1] if len(sys.argv) > 1 else '*'
prefix = sys.argv[2] if len(sys.argv) > 2 else ''
mode = sys.argv[3] if len(sys.argv) > 3 else ''
PATS = [
    r'(mục|section|in|ở|chương|chapter|ch\.)\s*[0-9]+\.[0-9]+(\.[0-9]+)?\b(?!\s*(s|giây|ms|%|px|đ|dòng|lines|GB|MB|KB))',
    r'\bItem\s*[0-9]',
    r'\bch\.\s*[0-9]+',
    r'(\bIn|\bỞ),?\s+(he|she|his|ông|bà)\b',
    r'The Clean Coder|Clean Agile|Software Craftsman',
    r'Clean Craftsmanship|Clean Coder|xUnit Test Patterns|Effective Kotlin|Clean Architecture',
    r'\b(Rule|Quy tắc)\s*[0-9]+(?![0-9/])',
    r'\(\s*[0-9]+\.[0-9]+(\.[0-9]+)?\s*\)',
    r'\((Clean Code|Effective Kotlin|Clean Architecture)\)',
    r'(?-i:Code That Fits)',
    r'(?-i:Clean Code)',
    r'\sin and\s',
    r'theo của',
    r'(Exercise|Bài tập)\s*[0-9]+\.[0-9]',
    r'\b(DDIA|AAT)\b',
    r'(Martin|Moskała|Seemann|Kleppmann|Carli|Vermeulen):\s',
]
rx = [re.compile(p, re.I) for p in PATS]
tot = collections.Counter()
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tracks', track, 'content.*.js'))):
    f = f.replace('\\', '/')
    tname = f.split('/')[-2]
    lang = f.split('.')[-2]
    t = io.open(f, encoding='utf-8').read()
    for line in t.split('\n'):
        m = re.match(r'\s*"([^"]+)"\s*:\s*(.*)', line)
        if not m:
            continue
        k, v = m.group(1), m.group(2)
        if prefix and ('.' + prefix + '.') not in k and not k.endswith('.' + prefix) and not k.startswith(prefix):
            continue
        if mode == 'prose':
            if ('.vz.' in k and ('.vz.' + prefix + '.') not in k and not k.endswith('.' + prefix)) or ('.m.map.' in k and prefix != 'map'):
                continue
            if re.search(r'\.(badge|kt|exkt|solkt|kind)"?$', k) or k.endswith('.kt') or '.vz.' in k and False:
                continue
            print('[%s] %s: %s' % (lang, k.replace('track.' + tname + '.', ''), v.rstrip(',').strip('"').replace('\n', ' / ').replace('\\"', '"')))
            continue
        if mode == 'dump':
            print('[%s] %s\n    %s' % (lang, k, v.rstrip(',').strip('"').replace('\\n', '\n    ')))
            continue
        for r in rx:
            mm = r.search(v)
            if mm:
                tot[tname + ' | ' + r.pattern[:18]] += 1
                if prefix:
                    print(lang, k, '|', v[max(0, mm.start() - 30):mm.end() + 30])
if mode not in ('dump','prose'):
    for k, v in sorted(tot.items()):
        print(k, v)
    print('total', sum(tot.values()))
