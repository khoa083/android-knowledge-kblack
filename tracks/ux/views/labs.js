/* Lab tương tác của track D (model kind 'compute', gắn qua view.mount). Trạng thái giữ trong ADE.uxLab.store (bộ nhớ trang)
   nên đổi ngôn ngữ không mất dữ liệu; KHÔNG lưu localStorage, KHÔNG gửi đi đâu. Mọi chữ là message key track.ux.lab.* */
(function () {
  'use strict';
  var Q = ADE.uxQuant, K = 'track.ux.lab.', L = ADE.uxLab = { store: {} };
  var T = function (k, p) { return ADE.t(K + k, p); };
  var CSS = '.uxl{display:grid;gap:12px;min-width:0}.uxl>*{min-width:0}.uxl .row{display:flex;flex-wrap:wrap;gap:8px;align-items:flex-end}' +
    '.uxl-two{display:grid;grid-template-columns:minmax(0,320px) minmax(0,1fr);gap:16px}@media(max-width:760px){.uxl-two{grid-template-columns:minmax(0,1fr)}}' +
    '.uxl table{border-collapse:collapse;font:12px var(--mono);width:100%}.uxl th,.uxl td{border-bottom:1px solid var(--line);padding:4px 6px;text-align:left}.uxl td.num{text-align:right}' +
    '.uxl .scroll{overflow-x:auto;max-width:100%}.uxl .warn{border-left:3px solid var(--tok-state);padding:6px 10px;background:var(--paper)}' +
    '.uxl .ok{color:var(--tok-job)}.uxl .bad{color:var(--tok-error)}.uxl textarea,.uxl input[type=text],.uxl input[type=number]{font:13px var(--mono);border:1px solid var(--line-strong);border-radius:var(--radius);padding:6px;background:var(--paper);color:var(--ink);max-width:100%;box-sizing:border-box}' +
    '.uxl textarea{width:100%;min-height:52px}.uxl svg{width:100%;height:auto;border:1px solid var(--line);border-radius:var(--radius);background:var(--paper)}.uxl svg text{font:11px var(--mono);fill:var(--ink-2)}' +
    '.uxl .curve{fill:none;stroke:var(--tok-signal);stroke-width:2.5}.uxl .ax{stroke:var(--line-strong)}.uxl .bar{fill:var(--tok-ui)}.uxl .ci{stroke:var(--ink);stroke-width:2}' +
    '.uxl .chk li{list-style:none;padding:2px 0}.uxl ul.chk{margin:0;padding:0}';
  function style() { if (document.getElementById('uxl-style')) return; var s = document.createElement('style'); s.id = 'uxl-style'; s.textContent = CSS; document.head.appendChild(s); }
  function shell(container, kind) {
    style(); var h = ADE.ui.h, root = h('div', { class: 'uxl panel pad' });
    root.appendChild(h('header', { class: 'panel-h' }, h('h2', { class: 'caps', text: T(kind + '.title') }), h('span', { class: 'badge badge-quant-model', text: ADE.t('badge.' + (kind === 'recall' || kind === 'heuristic' || kind === 'microcopy' ? 'simplified' : 'quant-model')) })));
    root.appendChild(h('p', { class: 'prose', html: ADE.markup(T(kind + '.intro')) }));
    container.appendChild(root); return root;
  }
  var pct = function (v) { return ADE.num(Math.round(v * 1000) / 10) + '%'; };
  function sel(fk, label, opts, val, on) {
    var h = ADE.ui.h, id = 'uxl-' + fk, s = h('select', { id: id, class: 'sel', 'data-fk': fk });
    opts.forEach(function (o) { s.appendChild(h('option', { value: String(o[0]), text: o[1], selected: String(o[0]) === String(val) ? true : null })); });
    s.addEventListener('change', function () { on(s.value); });
    return h('label', { class: 'field', for: id }, h('span', { text: label }), s);
  }
  function btn(fk, label, on, pri) { var b = ADE.ui.h('button', { type: 'button', class: 'btn' + (pri ? ' primary' : ''), 'data-fk': fk, text: label }); b.addEventListener('click', function () { ADE.ui.withFocus(on); }); return b; }

  /* ================= D1: recognition vs recall — đo của chính người đọc (minh họa cá nhân, chỉ trong bộ nhớ trang) ================= */
  L.recall = function (container) {
    var h = ADE.ui.h, st = L.store.recall || (L.store.recall = { a: null, b: null, cur: null }), root = shell(container, 'recall');
    root.appendChild(h('p', { class: 'warn', role: 'note', text: T('recall.privacy') }));
    var two = h('div', { class: 'uxl-two' }), left = h('div'), right = h('div'); two.appendChild(left); two.appendChild(right); root.appendChild(two);
    function norm(s) { return String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd').toLowerCase(); }
    function start(mode) { st.cur = { mode: mode, t0: null, actions: 0 }; render(); }
    function hit() { if (!st.cur) return; if (st.cur.t0 == null) st.cur.t0 = performance.now(); st.cur.actions++; }
    function done() { var c = st.cur; st[c.mode] = { ms: Math.round(performance.now() - (c.t0 || performance.now())), actions: c.actions }; st.cur = null; render(); }
    function render() {
      left.innerHTML = ''; right.innerHTML = '';
      var c = st.cur, screen = ADE.mockApp.screen('services', { variant: { recent: c && c.mode === 'b' } });
      if (c && c.mode === 'a') {
        var inp = h('input', { type: 'text', class: 'ma-in', 'data-fk': 'recall-input', 'aria-label': T('recall.inputLabel'), placeholder: T('recall.placeholder') });
        inp.addEventListener('keydown', function () { hit(); });
        inp.addEventListener('input', function () { if (norm(inp.value).indexOf(norm(T('recall.answer'))) >= 0) done(); });
        screen.insertBefore(inp, screen.children[1]);
        setTimeout(function () { try { inp.focus(); } catch (e) { } }, 0);
      }
      if (c && c.mode === 'b') {
        var chip = h('button', { type: 'button', class: 'btn', 'data-fk': 'recall-recent', text: T('recall.recentChip') });
        chip.addEventListener('click', function () { hit(); done(); });
        screen.insertBefore(chip, screen.children[1]);
      }
      left.appendChild(ADE.ui.mockFrame(screen));
      right.appendChild(h('p', { text: c ? T('recall.task.' + c.mode) : T('recall.pick') }));
      right.appendChild(h('div', { class: 'row' }, btn('recall-a', T('recall.startA'), function () { start('a'); }), btn('recall-b', T('recall.startB'), function () { start('b'); }), btn('recall-reset', T('reset'), function () { st.a = st.b = st.cur = null; render(); })));
      var tb = h('table'); tb.appendChild(h('tr', null, h('th', { text: T('recall.col.task') }), h('th', { text: T('recall.col.time') }), h('th', { text: T('recall.col.actions') })));
      ['a', 'b'].forEach(function (k) { var r = st[k]; tb.appendChild(h('tr', null, h('td', { text: T('recall.row.' + k) }), h('td', { class: 'num', text: r ? T('ms', { n: r.ms }) : '—' }), h('td', { class: 'num', text: r ? String(r.actions) : '—' }))); });
      right.appendChild(tb);
      right.appendChild(h('p', { class: 'hint', text: T('recall.note') }));
    }
    render(); return { destroy: function () { st.cur = null; root.remove(); } };
  };

  /* ================= D4: Heuristic Evaluation Workbench (12 vấn đề cài sẵn + 3 mồi nhử) ================= */
  var ANS = L.HEUR_ANSWER = {
    h1: { issue: true, h: [7, 3], sev: 2 }, h2: { issue: false }, h3: { issue: true, h: [6], sev: 2 },
    s1: { issue: false }, s2: { issue: true, h: [7, 6], sev: 2 },
    t1: { issue: true, h: [5], sev: 3 }, t2: { issue: true, h: [9, 3], sev: 3 }, t3: { issue: true, h: [4], sev: 1 },
    c1: { issue: false }, c2: { issue: true, h: [5], sev: 2 }, c3: { issue: true, h: [9], sev: 3 }, c4: { issue: true, h: [2, 4], sev: 3 },
    m1: { issue: true, h: [4, 6], sev: 2 }, m2: { issue: true, h: [10, 9], sev: 1 }, m3: { issue: true, h: [3], sev: 3 }
  };
  var SCREEN_OF = { h: 'home', s: 'services', t: 'time', c: 'confirm', m: 'mine' };
  var EVAL3 = [['h3', 't2', 'c3', 'c4', 'm3'], ['t1', 'c2', 'c3', 's2', 'h1'], ['t3', 'm1', 'm2', 'c4', 't2']];   // tập con cố định (minh họa)
  L.heuristic = function (container) {
    var h = ADE.ui.h, st = L.store.heuristic || (L.store.heuristic = { screen: 'confirm', marks: {}, cur: null, graded: false, three: false }), root = shell(container, 'heuristic');
    var two = h('div', { class: 'uxl-two' }), left = h('div'), right = h('div'); two.appendChild(left); two.appendChild(right); root.appendChild(two);
    var out = h('div'); root.appendChild(out);
    function render() {
      left.innerHTML = ''; right.innerHTML = ''; out.innerHTML = '';
      left.appendChild(sel('heur-screen', T('heuristic.screen'), Object.keys(SCREEN_OF).map(function (k) { return [SCREEN_OF[k], ADE.t('shared.mock.' + (SCREEN_OF[k] === 'home' ? 'app' : SCREEN_OF[k] + '.title'))]; }), st.screen, function (v) { st.screen = v; st.cur = null; render(); }));
      var spots = {}; Object.keys(st.marks).forEach(function (k) { if (st.marks[k].issue) spots[k] = true; }); if (st.cur) spots[st.cur] = true;
      left.appendChild(ADE.ui.mockFrame(ADE.mockApp.screen(st.screen, { spots: spots, onSpot: function (id) { st.cur = id; st.marks[id] = st.marks[id] || { issue: true, h: 1, sev: 2 }; render(); } })));
      if (!st.cur) right.appendChild(h('p', { text: T('heuristic.pick') }));
      else {
        var mk = st.marks[st.cur];
        right.appendChild(h('h3', { class: 'caps sub', text: T('heuristic.area', { id: st.cur.toUpperCase() }) }));
        var cb = h('input', { type: 'checkbox', id: 'uxl-issue', 'data-fk': 'heur-issue', checked: mk.issue ? true : null }); cb.addEventListener('change', function () { mk.issue = cb.checked; render(); });
        right.appendChild(h('label', { class: 'field inline', for: 'uxl-issue' }, cb, h('span', { text: T('heuristic.isIssue') })));
        right.appendChild(sel('heur-h', T('heuristic.heur'), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(function (i) { return [i, T('h.' + i)]; }), mk.h, function (v) { mk.h = +v; }));
        right.appendChild(sel('heur-sev', T('heuristic.sev'), [0, 1, 2, 3, 4].map(function (i) { return [i, T('sev.' + i)]; }), mk.sev, function (v) { mk.sev = +v; }));
      }
      right.appendChild(h('div', { class: 'row' }, btn('heur-grade', T('heuristic.grade'), function () { st.graded = true; render(); }, true), btn('heur-three', T(st.three ? 'heuristic.threeOff' : 'heuristic.threeOn'), function () { st.three = !st.three; render(); }), btn('heur-reset', T('reset'), function () { st.marks = {}; st.cur = null; st.graded = false; render(); })));
      if (st.three) {
        var u = Q.union(EVAL3);
        out.appendChild(h('p', { class: 'warn', text: T('heuristic.threeText', { a: EVAL3[0].length, b: EVAL3[1].length, c: EVAL3[2].length, u: u.length, n: 12 }) }));
      }
      if (st.graded) {
        var g = Q.grade(ANS, st.marks);
        out.appendChild(h('p', { text: T('heuristic.summary', { hit: g.hit.length, miss: g.miss.length, fp: g.falsePos.length, hok: g.heurOk, sok: g.sevClose }) }));
        var tb = h('table'); tb.appendChild(h('tr', null, h('th', { text: T('heuristic.col.area') }), h('th', { text: T('heuristic.col.result') }), h('th', { text: T('heuristic.col.answer') })));
        Object.keys(ANS).forEach(function (k) {
          var a = ANS[k], res = g.hit.indexOf(k) >= 0 ? 'hit' : g.miss.indexOf(k) >= 0 ? 'miss' : g.falsePos.indexOf(k) >= 0 ? 'fp' : 'okDecoy';
          tb.appendChild(h('tr', null, h('td', { text: k.toUpperCase() }), h('td', { class: res === 'hit' || res === 'okDecoy' ? 'ok' : 'bad', text: T('heuristic.res.' + res) }),
            h('td', { text: a.issue ? T('heuristic.ans', { h: T('h.' + a.h[0]), sev: T('sev.' + a.sev) }) + ' — ' + T('why.' + k) : T('heuristic.decoy') + ' — ' + T('why.' + k) })));
        });
        out.appendChild(h('div', { class: 'scroll' }, tb));
      }
      out.appendChild(h('p', { class: 'hint', html: ADE.markup(T('heuristic.note')) }));
    }
    render(); return { destroy: function () { root.remove(); } };
  };

  /* ================= D7: đường cong phát hiện 1 − (1 − L)^n ================= */
  L.curve = function (container) {
    var h = ADE.ui.h, st = L.store.curve || (L.store.curve = { L: Q.L_DEFAULT, n: 5 }), root = shell(container, 'curve');
    var ctl = h('div', { class: 'row' }); root.appendChild(ctl);
    var mk = function (fk, label, min, max, step, key) {
      var i = h('input', { type: 'range', min: String(min), max: String(max), step: String(step), value: String(st[key]), 'data-fk': fk, id: 'uxl-' + fk });
      i.addEventListener('input', function () { st[key] = +i.value; draw(); });
      return h('label', { class: 'field', for: 'uxl-' + fk }, h('span', { text: label }), i);
    };
    ctl.appendChild(mk('curve-L', T('curve.L'), 0.05, 0.6, 0.01, 'L')); ctl.appendChild(mk('curve-n', T('curve.n'), 1, 20, 1, 'n'));
    var read = h('p', { 'aria-live': 'polite' }); root.appendChild(read);
    var NS = 'http://www.w3.org/2000/svg', svg = document.createElementNS(NS, 'svg'); svg.setAttribute('viewBox', '0 0 600 220'); svg.setAttribute('role', 'img'); root.appendChild(svg);
    var cmp = h('p', { class: 'warn' }); root.appendChild(cmp);
    root.appendChild(h('p', { class: 'hint', html: ADE.markup(T('curve.assume')) }));
    function draw() {
      var f = Q.found(st.n, st.L), x = function (n) { return 40 + (n - 1) / 19 * 540; }, y = function (v) { return 200 - v * 180; }, d = '';
      for (var n = 1; n <= 20; n++) d += (n === 1 ? 'M' : 'L') + x(n).toFixed(1) + ' ' + y(Q.found(n, st.L)).toFixed(1);
      svg.innerHTML = '<title>' + ADE.esc(T('curve.title')) + '</title><desc>' + ADE.esc(T('curve.desc')) + '</desc><line class="ax" x1="40" y1="200" x2="590" y2="200"/><line class="ax" x1="40" y1="20" x2="40" y2="200"/>' +
        '<text x="2" y="24">100%</text><text x="10" y="204">0%</text><text x="560" y="216">n=20</text><path class="curve" d="' + d + '"/>' +
        '<circle cx="' + x(st.n).toFixed(1) + '" cy="' + y(f).toFixed(1) + '" r="5" fill="var(--ink)"/>';
      read.textContent = T('curve.read', { n: st.n, L: pct(st.L), f: pct(f) });
      var one = Q.found(15, st.L), three = 1 - Math.pow(1 - Q.found(5, st.L), 3);
      cmp.textContent = T('curve.compare', { one: pct(one), three: pct(three) });
    }
    draw(); return { destroy: function () { root.remove(); } };
  };

  /* ================= D8: máy tính SUS ================= */
  L.sus = function (container) {
    var h = ADE.ui.h, st = L.store.sus || (L.store.sus = { rows: [[4, 2, 4, 2, 4, 2, 4, 2, 4, 2], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [5, 1, 4, 2, 5, 2, 4, 1, 5, 2]] }), root = shell(container, 'sus');
    var box = h('div'); root.appendChild(box);
    function render() {
      box.innerHTML = '';
      var tb = h('table'), head = h('tr', null, h('th', { text: T('sus.col.p') }));
      for (var q = 1; q <= 10; q++) head.appendChild(h('th', { text: 'Q' + q, title: T('sus.q' + q) }));
      head.appendChild(h('th', { text: T('sus.col.score') })); tb.appendChild(head);
      var scores = [];
      st.rows.forEach(function (r, i) {
        var tr = h('tr', null, h('td', { text: T('sus.participant', { n: i + 1 }) }));
        r.forEach(function (v, j) {
          var s = h('select', { class: 'sel', 'data-fk': 'sus-' + i + '-' + j, 'aria-label': T('sus.cell', { p: i + 1, q: j + 1 }) });
          [1, 2, 3, 4, 5].forEach(function (k) { s.appendChild(h('option', { value: String(k), text: String(k), selected: k === v ? true : null })); });
          s.addEventListener('change', function () { r[j] = +s.value; ADE.ui.withFocus(render); });
          tr.appendChild(h('td', null, s));
        });
        var sc = Q.sus(r); scores.push(sc); tr.appendChild(h('td', { class: 'num', text: ADE.num(sc) })); tb.appendChild(tr);
      });
      box.appendChild(h('div', { class: 'scroll' }, tb));
      var mean = scores.reduce(function (a, b) { return a + b; }, 0) / scores.length;
      box.appendChild(h('div', { class: 'row' }, btn('sus-add', T('sus.add'), function () { if (st.rows.length < 8) st.rows.push([3, 3, 3, 3, 3, 3, 3, 3, 3, 3]); render(); }), btn('sus-remove', T('sus.remove'), function () { if (st.rows.length > 1) st.rows.pop(); render(); }), btn('sus-reset', T('reset'), function () { delete L.store.sus; root.remove(); L.sus(container); })));
      box.appendChild(h('p', { 'aria-live': 'polite', text: T('sus.mean', { m: Math.round(mean * 10) / 10, n: scores.length, avg: Q.SUS_AVERAGE }) }));
      box.appendChild(h('p', { class: 'warn', html: ADE.markup(T('sus.warn')) }));
      box.appendChild(h('p', { class: 'hint', html: ADE.markup(T('sus.formula')) }));
    }
    render(); return { destroy: function () { root.remove(); } };
  };

  /* ================= D8: task success + khoảng tin cậy adjusted Wald, so sánh hai thiết kế ================= */
  L.success = function (container) {
    var h = ADE.ui.h, st = L.store.success || (L.store.success = { a: [7, 10], b: [9, 10] }), root = shell(container, 'success');
    var box = h('div'); root.appendChild(box);
    var NS = 'http://www.w3.org/2000/svg';
    function num(fk, label, val, on) { var id = 'uxl-' + fk, i = h('input', { type: 'number', min: '0', max: '500', id: id, 'data-fk': fk, value: String(val) }); i.addEventListener('change', function () { on(Math.max(0, Math.round(+i.value || 0))); ADE.ui.withFocus(render); }); return h('label', { class: 'field', for: id }, h('span', { text: label }), i); }
    function render() {
      box.innerHTML = '';
      ['a', 'b'].forEach(function (k) {
        var v = st[k];
        box.appendChild(h('div', { class: 'row' }, h('b', { text: T('success.design.' + k) }), num('succ-' + k + 'x', T('success.x'), v[0], function (x) { v[0] = Math.min(x, v[1]); }), num('succ-' + k + 'n', T('success.n'), v[1], function (n) { v[1] = Math.max(1, n); v[0] = Math.min(v[0], v[1]); })));
      });
      var ra = Q.adjWald(st.a[0], st.a[1]), rb = Q.adjWald(st.b[0], st.b[1]);
      var svg = document.createElementNS(NS, 'svg'); svg.setAttribute('viewBox', '0 0 600 120'); svg.setAttribute('role', 'img');
      var x = function (p) { return 60 + p * 520; }, bar = function (r, y, lab) { return '<text x="2" y="' + (y + 4) + '">' + ADE.esc(lab) + '</text><line class="ci" x1="' + x(r.lo) + '" x2="' + x(r.hi) + '" y1="' + y + '" y2="' + y + '"/><circle cx="' + x(r.p) + '" cy="' + y + '" r="5" fill="var(--tok-ui)"/>'; };
      svg.innerHTML = '<title>' + ADE.esc(T('success.chart')) + '</title><desc>' + ADE.esc(T('success.desc')) + '</desc><line class="ax" x1="60" x2="580" y1="100" y2="100"/><text x="52" y="116">0%</text><text x="560" y="116">100%</text>' + bar(ra, 35, 'A') + bar(rb, 70, 'B');
      box.appendChild(svg);
      [['a', ra, st.a], ['b', rb, st.b]].forEach(function (z) { box.appendChild(h('p', { text: T('success.ci', { d: T('success.design.' + z[0]), x: z[2][0], n: z[2][1], p: pct(z[1].p), lo: pct(z[1].lo), hi: pct(z[1].hi) }) })); });
      box.appendChild(h('p', { class: 'warn', 'aria-live': 'polite', text: T(Q.overlap(ra, rb) ? 'success.overlap' : 'success.noOverlap') }));
      box.appendChild(h('p', { class: 'hint', html: ADE.markup(T('success.formula')) }));
    }
    render(); return { destroy: function () { root.remove(); } };
  };

  /* ================= D9: Microcopy Editor — checklist tự soạn, chấm cục bộ ================= */
  var ITEMS = ['btnConfirm', 'btnCancel', 'errPhone', 'errServer', 'empty', 'cancelDialog', 'reminder', 'saved'];
  L.microcopy = function (container) {
    var h = ADE.ui.h, st = L.store.microcopy || (L.store.microcopy = { item: 'errServer', text: {} }), root = shell(container, 'microcopy');
    var box = h('div'); root.appendChild(box);
    function checks(item, txt) {
      var t = String(txt || '').trim(), low = t.toLowerCase(), isBtn = item.indexOf('btn') === 0;
      var vague = T('mc.vagueWords').split('|'), blame = T('mc.blameWords').split('|');
      return {
        notEmpty: t.length > 0,
        length: t.length > 0 && t.length <= (isBtn ? 24 : 90),
        noCode: !/\d{3,}/.test(t) && !/error|exception|null|lỗi \d/i.test(t),
        noVague: !vague.some(function (w) { return w && new RegExp('(^|\\s)' + w + '($|\\s|[.!?,])', 'i').test(low); }),
        noBlame: !blame.some(function (w) { return w && low.indexOf(w) >= 0; })
      };
    }
    function render() {
      box.innerHTML = '';
      box.appendChild(sel('mc-item', T('mc.item'), ITEMS.map(function (i) { return [i, T('mc.i.' + i + '.label')]; }), st.item, function (v) { st.item = v; ADE.ui.withFocus(render); }));
      var it = st.item, cur = st.text[it] != null ? st.text[it] : T('mc.i.' + it + '.orig');
      box.appendChild(h('p', null, h('b', { text: T('mc.context') + ': ' }), h('span', { text: T('mc.i.' + it + '.ctx') })));
      box.appendChild(h('p', null, h('b', { text: T('mc.orig') + ': ' }), h('code', { translate: 'no', text: T('mc.i.' + it + '.orig') })));
      var ta = h('textarea', { 'data-fk': 'mc-text', id: 'uxl-mc', 'aria-label': T('mc.yours') }); ta.value = cur;
      var list = h('ul', { class: 'chk', 'aria-live': 'polite' });
      var upd = function () { st.text[it] = ta.value; var c = checks(it, ta.value); list.innerHTML = ''; Object.keys(c).forEach(function (k) { list.appendChild(h('li', { class: c[k] ? 'ok' : 'bad', text: (c[k] ? '✓ ' : '✗ ') + T('mc.rule.' + k) })); }); };
      ta.addEventListener('input', upd);
      box.appendChild(h('label', { class: 'field', for: 'uxl-mc', style: 'display:flex' }, h('span', { text: T('mc.yours') }), ta));
      box.appendChild(list); upd();
      var det = h('details', { class: 'acc' }, h('summary', { text: T('mc.suggest') }), h('p', null, h('code', { translate: 'no', text: T('mc.i.' + it + '.better') })), h('p', { class: 'prose', text: T('mc.i.' + it + '.why') }));
      box.appendChild(det);
      box.appendChild(h('p', { class: 'hint', html: ADE.markup(T('mc.note')) }));
    }
    render(); return { destroy: function () { root.remove(); } };
  };

  /* ---------- đăng ký model compute + view ---------- */
  var reg = function (id, checks) {
    ADE.registerModel('ux.' + id, { kind: 'compute', titleKey: K + id + '.title', compute: function (inp) { return { outputs: inp, assumptionKeys: [], sourceIds: [] }; }, checks: checks || [] });
    ADE.registerView('ux.' + id, { titleKey: K + id + '.title', descKey: K + id + '.intro', nodes: [], edges: [], mount: function (c) { return L[id](c); } });
  };
  reg('recall'); reg('heuristic', [{ name: 'đáp án workbench: 12 vấn đề và 3 mồi nhử', inputs: {}, expect: function () { var k = Object.keys(ANS); return k.filter(function (x) { return ANS[x].issue; }).length === 12 && k.length === 15; } }]);
  reg('curve'); reg('sus'); reg('success'); reg('microcopy');
})();
