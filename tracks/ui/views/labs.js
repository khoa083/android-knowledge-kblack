/* Lab của track E (model kind 'compute', gắn qua view.mount). Trạng thái giữ trong ADE.uiLab.store (bộ nhớ trang): đổi ngôn ngữ
   không mất; KHÔNG lưu, KHÔNG gửi. Màu trong khung mẫu là nội dung minh họa, không phải token của site (master 5.4c). Chữ: track.ui.lab.* */
(function () {
  'use strict';
  var Q = ADE.uiQuant, K = 'track.ui.lab.', L = ADE.uiLab = { store: {} };
  var T = function (k, p) { return ADE.t(K + k, p); };
  var h = function () { return ADE.ui.h.apply(null, arguments); };
  var CSS = '.uil{display:grid;gap:12px;min-width:0}.uil>*{min-width:0}.uil .row{display:flex;flex-wrap:wrap;gap:8px;align-items:flex-end}' +
    '.uil-two{display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);gap:16px}@media(max-width:760px){.uil-two{grid-template-columns:minmax(0,1fr)}}' +
    '.uil table{border-collapse:collapse;font:12px var(--mono);width:100%}.uil th,.uil td{border-bottom:1px solid var(--line);padding:4px 6px;text-align:left}' +
    '.uil .ok{color:var(--tok-job)}.uil .bad{color:var(--tok-error)}.uil .warn{border-left:3px solid var(--tok-state);padding:6px 10px}.uil .scroll{overflow-x:auto;max-width:100%}' +
    '.uil input[type=text]{font:13px var(--mono);border:1px solid var(--line-strong);border-radius:var(--radius);padding:6px;background:var(--paper);color:var(--ink);width:8em}' +
    '.uil .sw{display:inline-block;width:14px;height:14px;border:1px solid #777;vertical-align:middle;margin-right:4px}' +
    '.mk{font:14px system-ui,sans-serif;color:#1b1b1b;display:flex;flex-direction:column;gap:8px}.mk .card{border-radius:12px;padding:10px;border:1px solid #c9c9c9}' +
    '.mk .btn2{border-radius:20px;padding:9px 14px;text-align:center;font-weight:600;border:1px solid #1b1b1b;background:#fff;position:relative;overflow:hidden}' +
    '.mk .layer{position:absolute;inset:0;background:currentColor;pointer-events:none}.mk .muted{color:#555;font-size:12px}' +
    '.uil .demo{border:1px solid var(--line);border-radius:var(--radius);padding:10px;overflow:hidden;background:#fff;color:#1b1b1b}' +
    '.uil .fitts{position:relative;height:260px;border:1px solid var(--line);border-radius:var(--radius);background:var(--paper);overflow:hidden;touch-action:manipulation}' +
    '.uil .tgt{position:absolute;border-radius:50%;background:#0b776d;border:none;padding:0;cursor:pointer}.uil .tgt .hit{position:absolute;border-radius:50%;outline:1px dashed #b0287a}';
  function style() { if (document.getElementById('uil-style')) return; var s = document.createElement('style'); s.id = 'uil-style'; s.textContent = CSS; document.head.appendChild(s); }
  function shell(c, kind, badge) { style(); var r = h('div', { class: 'uil panel pad' }); r.appendChild(h('header', { class: 'panel-h' }, h('h2', { class: 'caps', text: T(kind + '.title') }), h('span', { class: 'badge', text: ADE.t('badge.' + (badge || 'simplified')) }))); r.appendChild(h('p', { class: 'prose', html: ADE.markup(T(kind + '.intro')) })); c.appendChild(r); return r; }
  function sel(fk, label, opts, val, on) { var id = 'uil-' + fk, s = h('select', { id: id, class: 'sel', 'data-fk': fk }); opts.forEach(function (o) { s.appendChild(h('option', { value: String(o[0]), text: o[1], selected: String(o[0]) === String(val) ? true : null })); }); s.addEventListener('change', function () { ADE.ui.withFocus(function () { on(s.value); }); }); return h('label', { class: 'field', for: id }, h('span', { text: label }), s); }
  function tog(fk, label, val, on) { var id = 'uil-' + fk, c = h('input', { type: 'checkbox', id: id, 'data-fk': fk, checked: val ? true : null }); c.addEventListener('change', function () { ADE.ui.withFocus(function () { on(c.checked); }); }); return h('label', { class: 'field inline', for: id }, c, h('span', { text: label })); }
  function color(fk, label, val, on) {
    var id = 'uil-' + fk, c = h('input', { type: 'color', id: id, 'data-fk': fk, value: val }), t = h('input', { type: 'text', value: val, 'aria-label': label + ' (hex)', 'data-fk': fk + '-hex' });
    c.addEventListener('input', function () { t.value = c.value; on(c.value); });
    t.addEventListener('change', function () { if (/^#?[0-9a-f]{6}$/i.test(t.value)) { var v = '#' + t.value.replace('#', ''); c.value = v; ADE.ui.withFocus(function () { on(v); }); } });
    return h('label', { class: 'field', for: id }, h('span', { text: label }), h('span', { class: 'row' }, c, t));
  }
  var yes = function (ok) { return h('span', { class: ok ? 'ok' : 'bad', text: (ok ? '✓ ' : '✗ ') + T(ok ? 'pass' : 'fail') }); };
  var r2 = function (x) { return ADE.num(Math.round(x * 100) / 100); };
  function mount(id, fn, badge) { return function (c) { var root = shell(c, id, badge), st = L.store[id] || (L.store[id] = fn.init()), box = h('div'); root.appendChild(box); var api = { root: root, box: box, st: st, rerender: function () { box.innerHTML = ''; fn.render(api); } }; api.rerender(); return { destroy: function () { if (fn.destroy) fn.destroy(api); root.remove(); } }; }; }

  /* ================= E1: CRAP + squint test ================= */
  L.crap = mount('crap', { init: function () { return { prox: false, align: false, rep: false, contrast: false, squint: false }; }, render: function (a) {
    var s = a.st, box = a.box;
    box.appendChild(h('div', { class: 'row' }, ['prox', 'align', 'rep', 'contrast', 'squint'].map(function (k) { return tog('crap-' + k, T('crap.' + k), s[k], function (v) { s[k] = v; a.rerender(); }); })));
    var scr = h('div', { class: 'mk', style: (s.squint ? 'filter:blur(3px);' : '') + 'text-align:' + (s.align ? 'left' : 'center') });
    var g = s.prox ? '4px' : '14px', groupGap = s.prox ? '18px' : '14px';
    var grp = function (title, line) { return h('div', { style: 'display:flex;flex-direction:column;gap:' + g + ';margin-bottom:' + groupGap }, h('b', { text: title, style: s.align ? '' : 'margin-left:' + (title.length % 3) * 8 + 'px' }), h('span', { class: 'muted', text: line })); };
    scr.appendChild(h('div', { style: 'font-size:18px;font-weight:700', text: ADE.t('shared.mock.confirm.title') }));
    scr.appendChild(grp(ADE.t('shared.mock.svc.general'), ADE.t('shared.mock.home.nextWhen')));
    scr.appendChild(grp(ADE.t('shared.mock.confirm.phone'), '0901 234 567'));
    var bs = s.rep ? 'border-radius:20px;border:1px solid #1b1b1b' : '', pri = s.contrast ? 'background:#0b776d;color:#fff;border-color:#0b776d' : 'background:#e8e8e8;color:#666';
    scr.appendChild(h('div', { class: 'row', style: 'justify-content:' + (s.align ? 'flex-start' : 'center') },
      h('span', { class: 'btn2', style: bs + ';' + pri, text: T('crap.book') }), h('span', { class: 'btn2', style: s.rep ? bs : 'border-radius:4px;border:2px dotted #888', text: T('crap.back') })));
    var two = h('div', { class: 'uil-two' }); two.appendChild(ADE.ui.mockFrame(scr));
    var ex = h('div'); ['prox', 'align', 'rep', 'contrast', 'squint'].forEach(function (k) { ex.appendChild(h('p', { class: 'prose', text: (s[k] ? '✓ ' : '○ ') + T('crap.why.' + k) })); });
    ex.appendChild(h('p', { class: 'hint', html: ADE.markup(T('crap.note')) })); two.appendChild(ex); box.appendChild(two);
  } }, 'author-framework');

  /* ================= E2: type scale playground ================= */
  L.type = mount('type', { init: function () { return { role: 'bodyLarge', sample: 'vi', lh: 1, width: 320, zoom: false }; }, render: function (a) {
    var s = a.st, box = a.box, t = Q.TYPE[s.role];
    box.appendChild(h('div', { class: 'row' },
      sel('type-role', T('type.role'), Object.keys(Q.TYPE).map(function (k) { return [k, k + ' · ' + Q.TYPE[k][0] + '/' + Q.TYPE[k][1]]; }), s.role, function (v) { s.role = v; a.rerender(); }),
      sel('type-sample', T('type.sample'), [['vi', T('type.sample.vi')], ['en', T('type.sample.en')]], s.sample, function (v) { s.sample = v; a.rerender(); }),
      sel('type-lh', T('type.lh'), [[0.8, '0.8×'], [1, T('type.lhToken')], [1.2, '1.2×']], s.lh, function (v) { s.lh = +v; a.rerender(); }),
      sel('type-width', T('type.width'), [[220, '220 px'], [320, '320 px'], [480, '480 px']], s.width, function (v) { s.width = +v; a.rerender(); }),
      tog('type-zoom', T('type.zoom'), s.zoom, function (v) { s.zoom = v; a.rerender(); })));
    var size = t[0] * (s.zoom ? 2 : 1), lh = t[1] * s.lh * (s.zoom ? 2 : 1);
    var demo = h('div', { class: 'demo', lang: s.sample, style: 'max-width:' + s.width + 'px;font-size:' + size + 'px;line-height:' + lh + 'px;font-family:system-ui,sans-serif' }, T('type.text.' + s.sample));
    box.appendChild(demo);
    var ratio = lh / size, warn = s.sample === 'vi' && ratio < 1.2;
    box.appendChild(h('p', { 'aria-live': 'polite', text: T('type.read', { role: s.role, size: size, lh: Math.round(lh), r: r2(ratio) }) }));
    if (warn) box.appendChild(h('p', { class: 'warn', text: T('type.warnVi') }));
    box.appendChild(h('p', { class: 'hint', html: ADE.markup(T('type.note')) }));
  } }, 'ds-guideline');

  /* ================= E3: contrast checker ================= */
  L.contrast = mount('contrast', { init: function () { return { fg: '#767676', bg: '#ffffff' }; }, render: function (a) {
    var s = a.st, box = a.box, r = Q.contrast(s.fg, s.bg), v = Q.verdict(r);
    box.appendChild(h('div', { class: 'row' }, color('ct-fg', T('contrast.fg'), s.fg, function (x) { s.fg = x; upd(); }), color('ct-bg', T('contrast.bg'), s.bg, function (x) { s.bg = x; upd(); }),
      h('button', { type: 'button', class: 'btn', 'data-fk': 'ct-bw', text: T('contrast.example'), onclick: function () { ADE.ui.withFocus(function () { s.fg = '#000000'; s.bg = '#ffffff'; a.rerender(); }); } })));
    var out = h('div', { 'aria-live': 'polite' }); box.appendChild(out);
    function upd() {
      r = Q.contrast(s.fg, s.bg); v = Q.verdict(r); out.innerHTML = '';
      out.appendChild(h('div', { class: 'demo', style: 'background:' + s.bg + ';color:' + s.fg }, h('p', { style: 'font-size:14px;margin:0', text: T('contrast.small') }), h('p', { style: 'font-size:24px;margin:4px 0', text: T('contrast.large') }), h('span', { style: 'display:inline-block;width:40px;height:20px;border:3px solid ' + s.fg })));
      out.appendChild(h('p', null, h('b', { text: T('contrast.ratio', { r: r2(r) }) })));
      var tb = h('table'); [['aaText', '1.4.3 AA', 'contrast.c.aaText'], ['aaLarge', '1.4.3 AA', 'contrast.c.aaLarge'], ['aaaText', '1.4.6 AAA', 'contrast.c.aaaText'], ['aaaLarge', '1.4.6 AAA', 'contrast.c.aaaLarge'], ['nonText', '1.4.11 AA', 'contrast.c.nonText']].forEach(function (x) { tb.appendChild(h('tr', null, h('td', { text: x[1] }), h('td', { text: T(x[2].replace('contrast.', 'contrast.')) }), h('td', null, yes(v[x[0]])))); });
      out.appendChild(tb);
      out.appendChild(h('p', { class: 'hint', html: ADE.markup(T('contrast.note')) }));
    }
    upd();
  } }, 'normative');

  /* ================= E3: color roles (giản lược) + chỉ dùng màu + bộ lọc mù màu ================= */
  L.roles = mount('roles', { init: function () { return { src: '#3a7bd5', dark: false, shift: 0, colorOnly: true, cvd: 'none' }; }, render: function (a) {
    var s = a.st, box = a.box, R = Q.roles(s.src, s.dark, s.shift), f = function (c) { return s.cvd === 'none' ? c : Q.simulate(c, s.cvd); };
    box.appendChild(h('div', { class: 'row' }, color('rl-src', T('roles.src'), s.src, function (x) { s.src = x; a.rerender(); }), tog('rl-dark', T('roles.dark'), s.dark, function (x) { s.dark = x; a.rerender(); }),
      sel('rl-shift', T('roles.shift'), [[0, T('roles.shift.0')], [0.25, T('roles.shift.up')], [-0.2, T('roles.shift.down')]], s.shift, function (x) { s.shift = +x; a.rerender(); }),
      tog('rl-only', T('roles.colorOnly'), s.colorOnly, function (x) { s.colorOnly = x; a.rerender(); }),
      sel('rl-cvd', T('roles.cvd'), ['none', 'protan', 'deutan', 'gray'].map(function (k) { return [k, T('roles.cvd.' + k)]; }), s.cvd, function (x) { s.cvd = x; a.rerender(); })));
    var scr = h('div', { class: 'mk', style: 'background:' + f(R.surface) + ';color:' + f(R.onSurface) + ';padding:10px;border-radius:8px' },
      h('div', { style: 'background:' + f(R.primary) + ';color:' + f(R.onPrimary) + ';padding:10px;border-radius:8px;font-weight:700', text: ADE.t('shared.mock.app') + ' · primary / onPrimary' }),
      h('div', { class: 'card', style: 'background:' + f(R.primaryContainer) + ';color:' + f(R.onPrimaryContainer) + ';border-color:' + f(R.outline) }, ADE.t('shared.mock.home.nextWhen') + ' · primaryContainer'),
      h('label', { style: 'display:flex;flex-direction:column;gap:2px' }, h('span', { text: ADE.t('shared.mock.confirm.phone') }),
        h('span', { style: 'border:2px solid ' + f(R.error) + ';border-radius:6px;padding:6px;background:' + f(R.surface), text: '0901-234-567' }),
        h('span', { style: 'color:' + f(R.error) + ';font-size:12px', text: s.colorOnly ? '' : '⚠ ' + T('roles.errText') })),
      h('span', { class: 'btn2', style: 'background:' + f(R.primary) + ';color:' + f(R.onPrimary) + ';border-color:' + f(R.primary), text: T('roles.book') }));
    var two = h('div', { class: 'uil-two' }); two.appendChild(ADE.ui.mockFrame(scr));
    var side = h('div'), tb = h('table');
    tb.appendChild(h('tr', null, h('th', { text: T('roles.pair') }), h('th', { text: T('roles.ratio') }), h('th', { text: '1.4.3 AA' })));
    Q.rolePairs(R).forEach(function (p) { tb.appendChild(h('tr', null, h('td', null, h('span', { class: 'sw', style: 'background:' + R[p.fg] }), h('span', { class: 'sw', style: 'background:' + R[p.bg] }), p.fg + ' / ' + p.bg), h('td', { text: r2(p.ratio) + ':1' }), h('td', null, yes(p.ok)))); });
    side.appendChild(h('div', { class: 'scroll' }, tb));
    if (s.colorOnly) side.appendChild(h('p', { class: 'warn', text: T('roles.onlyWarn') }));
    if (s.cvd !== 'none') side.appendChild(h('p', { class: 'hint', text: T('roles.cvdNote') }));
    side.appendChild(h('p', { class: 'hint', html: ADE.markup(T('roles.note')) }));
    two.appendChild(side); box.appendChild(two);
  } }, 'simplified');

  /* ================= E4: responsive lab ================= */
  L.responsive = mount('responsive', { init: function () { return { w: 412 }; }, render: function (a) {
    var s = a.st, box = a.box, cls = Q.widthClass(s.w);
    var rg = h('input', { type: 'range', min: '320', max: '1700', step: '10', value: String(s.w), id: 'uil-w', 'data-fk': 'rs-w' });
    var out = h('div', { 'aria-live': 'polite' });
    rg.addEventListener('input', function () { s.w = +rg.value; draw(); });
    box.appendChild(h('label', { class: 'field', for: 'uil-w' }, h('span', { text: T('responsive.width') }), rg)); box.appendChild(out);
    function draw() {
      cls = Q.widthClass(s.w); out.innerHTML = '';
      out.appendChild(h('p', null, h('b', { text: T('responsive.read', { w: s.w, cls: T('responsive.cls.' + cls) }) })));
      var nav = cls === 'compact' ? 'bar' : cls === 'medium' ? 'rail' : 'rail', twoPane = cls !== 'compact' && cls !== 'medium';
      var scale = Math.min(1, 640 / s.w), W = s.w * scale;
      var frame = h('div', { style: 'width:' + W + 'px;max-width:100%;height:200px;border:2px solid #444;border-radius:10px;display:flex;flex-direction:' + (nav === 'bar' ? 'column' : 'row') + ';overflow:hidden;background:#fff;color:#1b1b1b;font:12px system-ui' });
      var list = h('div', { style: 'flex:1;padding:6px;display:flex;flex-direction:column;gap:4px;min-width:0' }, [1, 2, 3].map(function (i) { return h('div', { style: 'border:1px solid #bbb;border-radius:6px;padding:4px', text: ADE.t('shared.mock.home.next') + ' ' + i }); }));
      var detail = h('div', { style: 'flex:1.4;padding:6px;border-left:1px solid #bbb;min-width:0', text: T('responsive.detail') });
      var navEl = h('div', { style: nav === 'bar' ? 'height:34px;border-top:1px solid #bbb;display:flex;justify-content:space-around;align-items:center' : 'width:44px;border-right:1px solid #bbb;display:flex;flex-direction:column;gap:8px;align-items:center;padding-top:8px' }, ['⌂', '☰', '⚙'].map(function (x) { return h('span', { 'aria-hidden': 'true', text: x }); }));
      if (nav === 'bar') { var main = h('div', { style: 'flex:1;display:flex;min-height:0' }, list); frame.appendChild(main); frame.appendChild(navEl); }
      else { frame.appendChild(navEl); frame.appendChild(list); if (twoPane) frame.appendChild(detail); }
      out.appendChild(h('div', { class: 'scroll' }, frame));
      out.appendChild(h('p', { text: T('responsive.layout.' + (twoPane ? 'twoPane' : nav)) }));
      out.appendChild(h('p', { class: 'hint', html: ADE.markup(T('responsive.note')) }));
    }
    draw();
  } }, 'stable');

  /* ================= E5: Fitts playground (đo cá nhân, chỉ trong bộ nhớ trang) ================= */
  L.fitts = mount('fitts', { init: function () { return { size: 48, dist: 200, expand: false, a: 100, b: 150, trials: [], waiting: false, t0: 0, misses: 0 }; }, render: function (a) {
    var s = a.st, box = a.box;
    box.appendChild(h('p', { class: 'warn', role: 'note', text: T('fitts.privacy') }));
    box.appendChild(h('div', { class: 'row' },
      sel('ft-size', T('fitts.size'), [[24, '24 px'], [48, '48 px'], [72, '72 px']], s.size, function (v) { s.size = +v; a.rerender(); }),
      sel('ft-dist', T('fitts.dist'), [[100, '100 px'], [200, '200 px'], [320, '320 px']], s.dist, function (v) { s.dist = +v; a.rerender(); }),
      tog('ft-expand', T('fitts.expand'), s.expand, function (v) { s.expand = v; a.rerender(); }),
      sel('ft-a', 'a (ms)', [[50, '50'], [100, '100'], [200, '200']], s.a, function (v) { s.a = +v; a.rerender(); }),
      sel('ft-b', 'b (ms/bit)', [[100, '100'], [150, '150'], [250, '250']], s.b, function (v) { s.b = +v; a.rerender(); })));
    var field = h('div', { class: 'fitts', 'data-fk': 'ft-field' }), W = s.size, hitW = s.expand ? Math.max(48, W) : W;
    var start = h('button', { type: 'button', class: 'btn', 'data-fk': 'ft-start', style: 'position:absolute;left:8px;top:110px', text: T('fitts.start') });
    var tgt = h('button', { type: 'button', class: 'tgt', 'data-fk': 'ft-target', 'aria-label': T('fitts.target'), style: 'left:' + (120 + s.dist - hitW / 2) + 'px;top:' + (130 - hitW / 2) + 'px;width:' + hitW + 'px;height:' + hitW + 'px;background:transparent' });
    tgt.appendChild(h('span', { style: 'position:absolute;left:' + (hitW - W) / 2 + 'px;top:' + (hitW - W) / 2 + 'px;width:' + W + 'px;height:' + W + 'px;border-radius:50%;background:#0b776d' }));
    if (s.expand) tgt.appendChild(h('span', { class: 'hit', style: 'inset:0' }));
    start.addEventListener('click', function () { s.waiting = true; s.t0 = performance.now(); start.textContent = T('fitts.go'); });
    tgt.addEventListener('click', function (e) { e.stopPropagation(); if (!s.waiting) return; s.trials.push({ ms: Math.round(performance.now() - s.t0), D: s.dist, W: hitW }); s.waiting = false; a.rerender(); });
    field.addEventListener('click', function (e) { if (s.waiting && e.target === field) s.misses++; });
    field.appendChild(start); field.appendChild(tgt); box.appendChild(field);
    var pred = Q.fitts(s.dist, hitW, s.a, s.b), mine = s.trials.filter(function (t) { return t.D === s.dist && t.W === hitW; });
    var avg = mine.length ? Math.round(mine.reduce(function (x, t) { return x + t.ms; }, 0) / mine.length) : null;
    box.appendChild(h('p', { 'aria-live': 'polite', text: T('fitts.read', { pred: Math.round(pred), id: r2(Math.log(s.dist / hitW + 1) / Math.LN2), n: mine.length, avg: avg == null ? '—' : avg, miss: s.misses }) }));
    box.appendChild(h('div', { class: 'row' }, h('button', { type: 'button', class: 'btn', 'data-fk': 'ft-reset', text: ADE.t('track.ux.lab.reset'), onclick: function () { ADE.ui.withFocus(function () { s.trials = []; s.misses = 0; a.rerender(); }); } })));
    box.appendChild(h('p', { class: 'hint', html: ADE.markup(T('fitts.note')) }));
  } }, 'quant-model');

  /* ================= E6: component states + state layer ================= */
  L.states = mount('states', { init: function () { return { comp: 'button', state: 'pressed' }; }, render: function (a) {
    var s = a.st, box = a.box, op = Q.STATE_LAYER[s.state] || 0;
    box.appendChild(h('div', { class: 'row' }, sel('st-comp', T('states.comp'), ['button', 'textfield', 'navitem'].map(function (k) { return [k, T('states.comp.' + k)]; }), s.comp, function (v) { s.comp = v; a.rerender(); }),
      sel('st-state', T('states.state'), ['enabled', 'hover', 'focus', 'pressed', 'dragged', 'disabled'].map(function (k) { return [k, T('states.state.' + k)]; }), s.state, function (v) { s.state = v; a.rerender(); })));
    var layer = h('span', { class: 'layer', style: 'opacity:' + op });
    var focusRing = s.state === 'focus' ? ';outline:3px solid #1b1b1b;outline-offset:2px' : '', dis = s.state === 'disabled';
    var el = s.comp === 'button' ? h('span', { class: 'btn2', style: 'background:#0b776d;color:#fff;border-color:#0b776d' + focusRing + (dis ? ';background:#ddd;color:#777;border-color:#ddd' : '') }, layer, T('states.label.button'))
      : s.comp === 'textfield' ? h('span', { class: 'btn2', style: 'border-radius:6px;text-align:left;color:#1b1b1b' + focusRing + (dis ? ';color:#999;border-color:#ccc' : '') }, layer, ADE.t('shared.mock.confirm.phone'))
        : h('span', { class: 'btn2', style: 'border:none;color:#0b776d' + focusRing + (dis ? ';color:#999' : '') }, layer, '⌂ ' + T('states.label.nav'));
    box.appendChild(h('div', { class: 'demo' }, el));
    box.appendChild(h('p', { 'aria-live': 'polite', text: dis ? T('states.disabled') : T('states.read', { state: T('states.state.' + s.state), op: Math.round(op * 100) }) }));
    box.appendChild(h('p', { class: 'hint', html: ADE.markup(T('states.note')) }));
  } }, 'ds-guideline');

  /* ================= E8: token editor → MaterialTheme ================= */
  L.tokens = mount('tokens', { init: function () { return { src: '#3a7bd5', radius: 12, scale: 1, dense: false, dark: false }; }, render: function (a) {
    var s = a.st, box = a.box, R = Q.roles(s.src, s.dark, 0);
    box.appendChild(h('div', { class: 'row' }, color('tk-src', T('tokens.src'), s.src, function (x) { s.src = x; a.rerender(); }),
      sel('tk-radius', T('tokens.radius'), [[0, '0'], [8, '8'], [12, '12'], [28, '28']], s.radius, function (x) { s.radius = +x; a.rerender(); }),
      sel('tk-scale', T('tokens.scale'), [[0.9, '0.9×'], [1, '1×'], [1.15, '1.15×']], s.scale, function (x) { s.scale = +x; a.rerender(); }),
      tog('tk-dense', T('tokens.dense'), s.dense, function (x) { s.dense = x; a.rerender(); }), tog('tk-dark', T('roles.dark'), s.dark, function (x) { s.dark = x; a.rerender(); })));
    var pad = s.dense ? 6 : 12, fs = Math.round(16 * s.scale);
    var scr = h('div', { class: 'mk', style: 'background:' + R.surface + ';color:' + R.onSurface + ';padding:' + pad + 'px;gap:' + pad + 'px;font-size:' + fs + 'px;border-radius:8px' },
      h('div', { style: 'font-size:' + Math.round(22 * s.scale) + 'px;font-weight:600', text: ADE.t('shared.mock.services.title') }),
      ['general', 'dental'].map(function (k) { return h('div', { class: 'card', style: 'border-radius:' + s.radius + 'px;padding:' + pad + 'px;background:' + R.primaryContainer + ';color:' + R.onPrimaryContainer + ';border-color:' + R.outline, text: ADE.t('shared.mock.svc.' + k) }); }),
      h('span', { class: 'btn2', style: 'border-radius:' + s.radius + 'px;background:' + R.primary + ';color:' + R.onPrimary + ';border-color:' + R.primary, text: T('roles.book') }));
    var two = h('div', { class: 'uil-two' }); two.appendChild(ADE.ui.mockFrame(scr));
    var side = h('div'), bad = Q.rolePairs(R).filter(function (p) { return !p.ok; });
    if (bad.length) side.appendChild(h('p', { class: 'warn', text: T('tokens.warn', { pairs: bad.map(function (p) { return p.fg + '/' + p.bg + ' ' + r2(p.ratio) + ':1'; }).join(', ') }) }));
    var code = { lang: 'kotlin', illustrative: true, lines: [
      'MaterialTheme(',
      '  colorScheme = ' + (s.dark ? 'darkColorScheme' : 'lightColorScheme') + '(',
      '    primary = Color(0xFF' + R.primary.slice(1).toUpperCase() + '), onPrimary = Color(0xFF' + R.onPrimary.slice(1).toUpperCase() + '),',
      '    primaryContainer = Color(0xFF' + R.primaryContainer.slice(1).toUpperCase() + '), surface = Color(0xFF' + R.surface.slice(1).toUpperCase() + ')',
      '  ),',
      '  typography = Typography(bodyLarge = TextStyle(fontSize = ' + fs + '.sp, lineHeight = ' + Math.round(24 * s.scale) + '.sp)),',
      '  shapes = Shapes(medium = RoundedCornerShape(' + s.radius + '.dp))',
      ') { HenKhamApp() }'] };
    side.appendChild(ADE.ui.codeBlock(code, []));
    side.appendChild(h('p', { class: 'hint', html: ADE.markup(T('tokens.note')) }));
    two.appendChild(side); box.appendChild(two);
  } }, 'simplified');

  /* ================= E9: motion purpose lab ================= */
  L.motion = mount('motion', { init: function () { return { easing: 'emphasizedDecelerate', dur: 'medium4', reduce: false, open: false }; }, render: function (a) {
    var s = a.st, box = a.box, e = Q.EASING[s.easing], d = Q.DURATION[s.dur], reduce = s.reduce || ADE.motionReduced();
    box.appendChild(h('div', { class: 'row' }, sel('mo-easing', T('motion.easing'), Object.keys(Q.EASING).map(function (k) { return [k, k + ' (' + Q.EASING[k].join(', ') + ')']; }), s.easing, function (v) { s.easing = v; a.rerender(); }),
      sel('mo-dur', T('motion.dur'), Object.keys(Q.DURATION).map(function (k) { return [k, k + ' · ' + Q.DURATION[k] + ' ms']; }), s.dur, function (v) { s.dur = v; a.rerender(); }),
      tog('mo-reduce', T('motion.reduce'), s.reduce, function (v) { s.reduce = v; a.rerender(); })));
    var card = h('div', { class: 'card', style: 'background:#e6f2ef;border-color:#0b776d;overflow:hidden;height:' + (s.open ? 150 : 48) + 'px;transition:' + (reduce ? 'none' : 'height ' + d + 'ms cubic-bezier(' + e.join(',') + ')') + ';color:#1b1b1b' },
      h('b', { text: ADE.t('shared.mock.home.next') + ' · ' + ADE.t('shared.mock.home.nextWhen') }), h('p', { class: 'muted', text: T('motion.detail') }));
    var btn = h('button', { type: 'button', class: 'btn primary', 'data-fk': 'mo-play', text: T(s.open ? 'motion.close' : 'motion.open') });
    btn.addEventListener('click', function () { s.open = !s.open; card.style.height = (s.open ? 150 : 48) + 'px'; btn.textContent = T(s.open ? 'motion.close' : 'motion.open'); });
    box.appendChild(h('div', { class: 'demo' }, card)); box.appendChild(btn);
    box.appendChild(h('p', { 'aria-live': 'polite', text: reduce ? T('motion.reduced') : T('motion.read', { e: s.easing, d: d }) }));
    box.appendChild(h('p', { class: 'hint', html: ADE.markup(T('motion.note')) }));
  } }, 'ds-guideline');

  /* ================= E10: a11y audit + thứ tự đọc giản lược ================= */
  var ISSUES = ['icon', 'contrast', 'target', 'order', 'colorOnly', 'fixedText'];
  var SC = { icon: '1.1.1 A · 4.1.2 A', contrast: '1.4.3 AA', target: '2.5.8 AA', order: '2.4.3 A', colorOnly: '1.4.1 A', fixedText: '1.4.4 AA' };
  L.a11y = mount('a11y', { init: function () { var o = {}; ISSUES.forEach(function (k) { o[k] = true; }); return o; }, render: function (a) {
    var s = a.st, box = a.box;
    box.appendChild(h('div', { class: 'row' }, ISSUES.map(function (k) { return tog('ay-' + k, T('a11y.i.' + k), s[k], function (v) { s[k] = v; a.rerender(); }); })));
    var scr = h('div', { class: 'mk', style: s.fixedText ? 'font-size:13px' : 'font-size:1em' },
      h('div', { class: 'row', style: 'justify-content:space-between' }, h('b', { text: ADE.t('shared.mock.mine.title') }), h('span', { style: 'display:inline-flex;width:' + (s.target ? 24 : 48) + 'px;height:' + (s.target ? 24 : 48) + 'px;align-items:center;justify-content:center;border:1px solid #bbb;border-radius:50%', text: '⚙' })),
      h('div', { class: 'card' }, h('span', { style: 'color:' + (s.contrast ? '#b0b0b0' : '#555'), text: ADE.t('shared.mock.home.nextWhen') })),
      h('span', { style: 'border:2px solid #b3261e;border-radius:6px;padding:6px', text: '0901-234-567' }), h('span', { style: 'color:#b3261e;font-size:12px', text: s.colorOnly ? '' : '⚠ ' + T('a11y.err') }));
    var two = h('div', { class: 'uil-two' }); two.appendChild(ADE.ui.mockFrame(scr));
    var side = h('div'), tb = h('table');
    tb.appendChild(h('tr', null, h('th', { text: T('a11y.col.issue') }), h('th', { text: 'WCAG 2.2' }), h('th', { text: T('a11y.col.fix') })));
    ISSUES.filter(function (k) { return s[k]; }).forEach(function (k) { tb.appendChild(h('tr', null, h('td', { text: T('a11y.i.' + k) }), h('td', { text: SC[k] }), h('td', { text: T('a11y.fix.' + k) }))); });
    side.appendChild(h('div', { class: 'scroll' }, tb));
    // thứ tự đọc (mô hình semantics giản lược)
    var items = [['heading', ADE.t('shared.mock.mine.title'), true], ['button', s.icon ? T('a11y.unlabeled') : T('a11y.settings'), false], ['text', ADE.t('shared.mock.home.nextWhen'), false], ['edit', ADE.t('shared.mock.confirm.phone') + (s.colorOnly ? '' : ', ' + T('a11y.err')), false]];
    if (s.order) items = [items[2], items[0], items[3], items[1]];
    var ol = h('ol'); items.forEach(function (it) { ol.appendChild(h('li', { text: it[1] + ' — ' + T('a11y.role.' + it[0]) })); });
    side.appendChild(h('h3', { class: 'caps sub', text: T('a11y.order') })); side.appendChild(ol);
    side.appendChild(h('p', { class: 'warn', text: T('a11y.notTalkback') }));
    side.appendChild(h('p', { class: 'hint', html: ADE.markup(T('a11y.note')) }));
    two.appendChild(side); box.appendChild(two);
  } }, 'normative');

  /* ---------- đăng ký ---------- */
  ['crap', 'type', 'contrast', 'roles', 'responsive', 'fitts', 'states', 'tokens', 'motion', 'a11y'].forEach(function (id) {
    ADE.registerModel('ui.' + id, { kind: 'compute', titleKey: K + id + '.title', compute: function (i) { return { outputs: i, assumptionKeys: [], sourceIds: [] }; }, checks: id === 'contrast' ? [{ name: 'kiểm tra tương phản: đen/trắng đạt mọi mức', inputs: {}, expect: function () { var v = Q.verdict(Q.contrast('#000', '#fff')); return v.aaaText && v.nonText; } }] : [] });
    ADE.registerView('ui.' + id, { titleKey: K + id + '.title', descKey: K + id + '.intro', nodes: [], edges: [], mount: function (c) { return L[id](c); } });
  });
})();
