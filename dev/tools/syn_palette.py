"""Fit One Light / One Dark token hues to >= 4.6:1 contrast against the site's code backgrounds (both normal and highlighted line)."""
import colorsys

def hex2rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
def rgb2hex(c): return '#' + ''.join('%02X' % round(max(0, min(1, x)) * 255) for x in c)
def lum(c):
    f = lambda x: x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = map(f, c); return 0.2126 * r + 0.7152 * g + 0.0722 * b
def cr(a, b):
    la, lb = lum(hex2rgb(a)), lum(hex2rgb(b)); hi, lo = max(la, lb), min(la, lb); return (hi + 0.05) / (lo + 0.05)

def fit(col, bgs, dark, target=4.6):
    h, l, s = colorsys.rgb_to_hls(*hex2rgb(col))
    c = col
    while min(cr(c, b) for b in bgs) < target:
        l = l + 0.01 if dark else l - 0.01
        if l < 0 or l > 1: break
        c = rgb2hex(colorsys.hls_to_rgb(h, l, s))
    return c

THEMES = {
    'light': {'dark': False, 'bg': '#F4F8F6', 'hl': '#DFEBE6', 'src': {
        'fg': '#383A42', 'kw': '#A626A4', 'str': '#50A14F', 'esc': '#0184BC', 'num': '#986801',
        'com': '#A0A1A7', 'ann': '#E45649', 'type': '#0B776D',  # type: xanh-lục site (vàng One Light trùng màu số sau khi làm tối)
        'fn': '#4078F2', 'ln': '#9DA5A2'}},
    'dark': {'dark': True, 'bg': '#13211D', 'hl': '#1F362F', 'src': {
        'fg': '#ABB2BF', 'kw': '#C678DD', 'str': '#98C379', 'esc': '#56B6C2', 'num': '#D19A66',
        'com': '#5C6370', 'ann': '#E06C75', 'type': '#E5C07B', 'fn': '#61AFEF', 'ln': '#4B5263'}},
}
for name, t in THEMES.items():
    print('==', name, 'bg', t['bg'], 'hl', t['hl'])
    for k, v in t['src'].items():
        target = 3.0 if k == 'ln' else 4.6   # số dòng là chữ phụ, aria-hidden, nhưng vẫn giữ >= 3:1
        o = fit(v, [t['bg'], t['hl']], t['dark'], target)
        print('  --syn-%-5s %s  (from %s)  bg %.2f  hl %.2f' % (k, o, v, cr(o, t['bg']), cr(o, t['hl'])))
