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

  /* ---------- l2: hai làn luồng (SVG phẳng): làn trên là luồng báo cáo đi qua 500 lịch (vạch đỏ là chỗ dừng; nhiều lần dừng thành dải đỏ),
     làn dưới là luồng đồng bộ (chấm là nhịp; đoạn đỏ là lúc bị dừng theo quá hạn). Dưới là bảng biến tại chỗ dừng, hoặc log của breakpoint.
     Giá trị tính từ ADE.dbgBp; ô đổi lớp thì nháy. ---------- */
  ADE.registerScreen('debugging.bp', function (box, ctx) {
    var h = ADE.ui.h, P = ADE.dbgBp, c = ctx.state.case, i = Math.max(0, idx(ctx)), r = P.run(c, i);
    var X0 = 120, W = 480, x = function (n) { return X0 + n * W / (P.N - 1); };
    var svg = '<svg class="vz-dg vz-lanes" viewBox="0 0 620 130" role="img" aria-label="' + esc(T('bp.aria', { s: r.stops, m: r.gap })) + '">';
    svg += '<text class="vz-dg-s" x="4" y="38">' + esc(T('bp.lane.report')) + '</text><text class="vz-dg-s" x="4" y="98">' + esc(T('bp.lane.sync')) + '</text>';
    svg += '<line class="vz-dg-e" x1="' + X0 + '" y1="34" x2="' + (X0 + W) + '" y2="34"/><line class="vz-dg-e" x1="' + X0 + '" y1="94" x2="' + (X0 + W) + '" y2="94"/>';
    svg += '<line class="vz-dg-e up" data-k="bp-prog" x1="' + X0 + '" y1="34" x2="' + x(r.at).toFixed(1) + '" y2="34"/>';
    if (r.stops > 1) svg += '<g class="vz-dg-n bad" data-k="bp-band"><rect x="' + X0 + '" y="24" width="' + (x(P.BAD) - X0).toFixed(1) + '" height="20" rx="2"/></g>';
    else if (r.stops === 1) svg += '<g class="vz-dg-n bad" data-k="bp-stop"><rect x="' + (x(r.at) - 3).toFixed(1) + '" y="22" width="6" height="24" rx="1"/></g>';
    if (r.stops) svg += '<text class="vz-dg-s" data-k="bp-at" x="' + (x(r.at) - 30).toFixed(1) + '" y="16">' + esc(r.at === P.BAD ? T('bp.hit') : 'i = ' + r.at) + '</text>';
    // nhịp của luồng đồng bộ: mỗi 24 px một chấm; khi bị dừng theo quá hạn, một đoạn đỏ thay cho các chấm sau chỗ dừng
    var cut = r.expired ? x(r.at) : -1;
    for (var px = X0 + 6; px < X0 + W; px += 24) {
      if (cut >= 0 && px > cut && px < cut + 90) continue;
      svg += '<circle class="vz-dot" cx="' + px + '" cy="94" r="3.5"/>';
    }
    if (cut >= 0) svg += '<g class="vz-dg-n bad" data-k="bp-gap"><rect x="' + cut.toFixed(1) + '" y="86" width="90" height="16" rx="2"/></g>';
    svg += '<text class="vz-dg-s" x="' + X0 + '" y="124">' + esc(T('bp.axis')) + '</text></svg>';
    var wrap = h('div', { class: 'vz-scroll' }); wrap.innerHTML = svg;
    var sub1 = c === 'logbp' ? T('bp.sub.logs', { n: r.logs, k: r.filtered }) : T('bp.sub.stops', { s: r.stops, r: r.resumes });
    var sub2 = T('bp.sub.sync', { m: r.gap, st: T('bp.st.' + (r.expired ? 'expired' : 'alive')) });
    var tb = h('tbody'), title;
    if (c === 'logbp') {
      title = T('bp.log.title');
      for (var n = P.BAD - 2; n <= P.BAD + 2; n++) {
        var neg = P.fee(n) < 0, on = neg && i >= 1;
        tb.appendChild(h('tr', { 'data-k': 'bp-log-' + n }, h('td', { class: on ? 'bad' : null, text: 'i=' + n + ' fee=' + P.fee(n) }), h('td', { class: on ? 'bad' : 'dim', text: i >= 1 ? (neg ? '← fee < 0' : '') : '' })));
      }
    } else {
      title = T('bp.vars.title');
      var at = r.stops ? r.at : null;
      var rows = at === null ? [['i', '—'], ['b.discountPercent', '—'], ['fee', '—']] :
        [['i', String(at)], ['b.id', String(1001 + at)], ['b.base', String(P.BASE)], ['b.discountPercent', String(P.disc(at))], ['fee', String(P.fee(at))]];
      rows.forEach(function (rw) {
        var badCell = at !== null && P.fee(at) < 0 && (rw[0] === 'fee' || rw[0] === 'b.discountPercent');
        tb.appendChild(h('tr', { 'data-k': 'bp-v-' + rw[0] }, h('td', { text: rw[0] }), h('td', { class: badCell ? 'bad' : null, text: rw[1] })));
      });
    }
    box.appendChild(h('div', { class: 'vz' },
      wrap,
      h('p', { class: 'vz-sub' + (c === 'plain' && i >= 1 ? ' bad' : ''), 'data-k': 'bp-sub1', text: sub1 }),
      h('p', { class: 'vz-sub' + (r.expired ? ' bad' : ''), 'data-k': 'bp-sub2', text: sub2 }),
      h('p', { class: 'vz-cap', text: title }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, h('th', { text: T('bp.col.name') }), h('th', { text: T('bp.col.val') }))), tb)),
      h('div', { class: 'vz-legend', text: T('bp.legend') })));
  }, { labelKey: K + 'tab.bp', icon: 'thread' });
})();
