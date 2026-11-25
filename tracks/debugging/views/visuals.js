/* Hình trực quan theo bước của track L (ADE.registerScreen với nhãn tab riêng). Sơ đồ node vẫn ở tab bên cạnh. */
(function () {
  'use strict';
  var K = 'track.debugging.vz.';
  var T = function (k, p) { return ADE.t(K + k, p); };
  var KS = ['s1', 's2', 's3', 's4'];
  function idx(ctx) {
    if (ctx.step) return KS.indexOf(ctx.step.id.split('.').pop());
    return ctx.pos > ctx.N ? 3 : 0;
  }
  var esc = function (x) { return String(x).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); };
  var fit = function (str, w) { return String(str).length * 6.4 > w ? ' textLength="' + w + '" lengthAdjust="spacingAndGlyphs"' : ''; };

  /* ---------- l1: vòng gỡ lỗi (SVG phẳng: bốn trạm, cạnh quay lại, lối ra "sửa và khóa"; cách đoán là một đường tắt không qua trạm nào)
     và bảng 8 kịch bản: kết quả mỗi kịch bản tính từ bản sửa đang áp dụng (đỏ crash, vàng màn trống). Ô đổi lớp thì nháy; không lặp. ---------- */
  ADE.registerScreen('debugging.loop', function (box, ctx) {
    var h = ADE.ui.h, L = ADE.dbgLoop, c = ctx.state.case, i = Math.max(0, idx(ctx)), patch = L.PATCH[c][i], t = L.tally(patch);
    var nl = function (id) { return ADE.t('track.debugging.m.loop.n.' + id); };
    var W = 140, HH = 30;
    var ST = { repro: [10, 14], narrow: [170, 14], hypo: [330, 14], check: [330, 92], lock: [490, 92] };
    // trạm đã qua và trạm đang đứng theo bước (cách có phương pháp)
    var REACH = [['repro'], ['repro', 'narrow'], ['repro', 'narrow', 'hypo', 'check'], ['repro', 'narrow', 'hypo', 'check', 'lock']][i];
    var CUR = [['repro'], ['narrow'], ['hypo', 'check'], ['lock']][i];
    function cls(id) {
      if (c === 'guess') return id === 'lock' ? 'bad' : 'skip';
      return CUR.indexOf(id) >= 0 ? 'on' : (REACH.indexOf(id) >= 0 ? 'ok' : '');
    }
    var E = [['e1', [[150, 29], [170, 29]], ['repro', 'narrow']], ['e2', [[310, 29], [330, 29]], ['narrow', 'hypo']], ['e3', [[400, 44], [400, 92]], ['hypo', 'check']],
      ['e4', [[330, 112], [80, 112], [80, 44]], ['check', 'repro']], ['e5', [[470, 107], [490, 107]], ['check', 'lock']]];
    var svg = '<svg class="vz-dg vz-loop" viewBox="0 0 640 190" role="img" aria-label="' + esc(T('loop.aria', { c: t.crash, b: t.blank })) + '">';
    E.forEach(function (e) {
      var on = c === 'method' && REACH.indexOf(e[2][0]) >= 0 && REACH.indexOf(e[2][1]) >= 0 && e[0] !== 'e4';
      svg += '<polyline class="vz-dg-e' + (on ? ' up' : '') + '" data-k="lp-' + e[0] + '" fill="none" points="' + e[1].map(function (p) { return p.join(','); }).join(' ') + '"/>';
    });
    Object.keys(ST).forEach(function (id) {
      var p = ST[id], k = cls(id), lb = nl(id);
      svg += '<g class="vz-dg-n' + (k ? ' ' + k : '') + '" data-k="lp-' + id + '"><rect x="' + p[0] + '" y="' + p[1] + '" width="' + W + '" height="' + HH + '" rx="4"/>' +
        '<text class="vz-dg-s" x="' + (p[0] + 8) + '" y="' + (p[1] + 19) + '"' + fit(lb, W - 16) + '>' + esc(lb) + '</text></g>';
    });
    // đường tắt của cách đoán: báo lỗi → đoán rồi sửa → phát hành, không qua trạm nào
    if (c === 'guess') {
      var gl = T('loop.guess');
      svg += '<polyline class="vz-dg-e bad" data-k="lp-short" fill="none" points="150,163 560,163 560,122"/>' +
        '<g class="vz-dg-n bad" data-k="lp-guess"><rect x="10" y="148" width="' + W + '" height="' + HH + '" rx="4"/><text class="vz-dg-s" x="18" y="167"' + fit(gl, W - 16) + '>' + esc(gl) + '</text></g>';
    }
    svg += '</svg>';
    var wrap = h('div', { class: 'vz-scroll' }); wrap.innerHTML = svg;
    var tb = h('tbody');
    L.SC.forEach(function (sc, n) {
      var o = L.outcome(sc, patch), re = sc[1] === null ? 'no' : (L.recreated(sc, patch) ? 'yes' : 'hidden');
      tb.appendChild(h('tr', { 'data-k': 'lp-sc-' + sc[0] }, h('td', { class: 'c', text: String(n + 1) }), h('td', { text: T('loop.sc.' + sc[0]) }),
        h('td', { class: re === 'yes' ? 'hl' : null, text: T('loop.re.' + re) }),
        h('td', { class: o === 'crash' ? 'bad' : (o === 'blank' ? 'warn' : 'ok'), text: T('loop.out.' + o) })));
    });
    box.appendChild(h('div', { class: 'vz' },
      h('p', { class: 'vz-cap', text: T('loop.cap.' + c) }),
      wrap,
      h('p', { class: 'vz-sub', 'data-k': 'lp-patch', text: T('loop.patch', { p: T('loop.p.' + patch) }) }),
      h('p', { class: 'vz-sub' + (c === 'guess' && i >= 2 ? ' bad' : ''), 'data-k': 'lp-rel-' + i, text: T('loop.rel.' + c + '.' + i) }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['n', 'sc', 're', 'out'].map(function (k) { return h('th', { text: T('loop.col.' + k) }); }))), tb)),
      h('div', { class: 'vz-legend', text: T('loop.legend') })));
  }, { labelKey: K + 'tab.loop', icon: 'replay' });
})();
