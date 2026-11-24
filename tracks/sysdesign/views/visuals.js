/* Hình trực quan theo bước của track I (ADE.registerScreen với nhãn tab riêng). Sơ đồ node vẫn ở tab bên cạnh. */
(function () {
  'use strict';
  var K = 'track.sysdesign.vz.';
  var T = function (k, p) { return ADE.t(K + k, p); };
  var KS = ['s1', 's2', 's3', 's4'];
  var esc = function (x) { return String(x).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); };
  var uidN = 0;
  function idx(ctx) {
    if (ctx.step) return KS.indexOf(ctx.step.id.split('.').pop());
    return ctx.pos > ctx.N ? 3 : 0;
  }

  /* ---------- I1: bảng câu hỏi (hỏi ai → yêu cầu rút ra), và bảng ước lượng dữ liệu ảnh ---------- */
  ADE.registerScreen('sysdesign.plan', function (box, ctx) {
    var h = ADE.ui.h, P = ADE.sysPlan, c = ctx.state.case, i = Math.max(0, idx(ctx));
    var head = h('tr', null, ['who', 'q', 'req'].map(function (k) { return h('th', { text: T('pl.col.' + k) }); }));
    var tb = h('tbody');
    P.Q.forEach(function (q) {
      var st = P.qState(c, i, q), cur = st && ((st === 'asked' && ((q[1] === 'designer' && i === 1) || (q[1] === 'backend' && i === 2))) || (st === 'late' && i === 3));
      tb.appendChild(h('tr', null, h('td', { class: 'dim', text: T('pl.who.' + q[1]) }), h('td', { class: st ? null : 'dim', text: T('pl.q.' + q[0]) }),
        h('td', { class: cur ? (st === 'late' ? 'bad' : 'hl') : (st === 'late' ? 'bad' : (st ? 'ok' : 'dim')), text: st === 'asked' ? T('pl.r.' + q[0]) : (st === 'late' ? T('pl.late.' + q[0]) : '?') })));
    });
    var e = P.EST[c], showE = i >= 3;
    var est = h('table', { class: 'vz-table' }, h('tbody', null,
      h('tr', null, h('th', { text: T('pl.e.photos') }), h('td', { text: showE ? String(e.photos) : '?' })),
      h('tr', null, h('th', { text: T('pl.e.size') }), h('td', { class: showE ? (c === 'mockup' ? 'bad' : 'ok') : 'dim', text: showE ? T('pl.e.kb.' + c, { kb: e.kb }) : '?' })),
      h('tr', null, h('th', { text: T('pl.e.month') }), h('td', { class: showE ? (c === 'mockup' ? 'bad' : 'hl') : 'dim', text: showE ? T('pl.e.mb', { n: P.mbMonth(c) }) : '?' }))));
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('pl.cap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), tb)),
      h('p', { class: 'vz-cap', text: T('pl.ecap') }), h('div', { class: 'vz-scroll' }, est), h('div', { class: 'vz-legend', text: T('pl.legend') })));
  }, { labelKey: K + 'tab.pl', icon: 'list' });

  /* ---------- I2: dãy bậc process (chip của app tụt bậc), thanh RAM (SVG), bảng "còn lại gì" ---------- */
  ADE.registerScreen('sysdesign.process', function (box, ctx) {
    var h = ADE.ui.h, P = ADE.sysProcess, c = ctx.state.case, i = Math.max(0, idx(ctx));
    var head = h('tr', null, ['lv', 'ex', 'now'].map(function (k) { return h('th', { text: T('pr.col.' + k) }); }));
    var tb = h('tbody');
    ['fg', 'vis', 'svc', 'cached', 'gone'].forEach(function (lv) {
      var chips = [];
      if (P.LV.app[i] === lv) chips.push(h('span', { class: 'vz-chip ' + (lv === 'gone' ? 'bad' : 'hl'), text: T(i === 3 ? 'pr.chip.app2' : 'pr.chip.app') }));
      if (P.LV.cam[i] === lv) chips.push(h('span', { class: 'vz-chip', text: T('pr.chip.cam') }));
      var on = chips.length > 0;
      tb.appendChild(h('tr', null, h('th', { class: on ? null : 'dim', text: T('pr.lv.' + lv) }), h('td', { class: 'dim', text: T('pr.ex.' + lv) }), h('td', { class: on && lv === 'gone' ? 'bad' : null }, chips)));
    });
    var mem = P.MEM[i], W = 600, x = 0, cls = ['sys', 'cam', 'oth', 'our', 'free'], keys = ['sys', 'cam', 'oth', 'our', 'free'];
    var svg = '<svg class="vz-mem" viewBox="0 0 ' + W + ' 30" role="img" aria-label="' + T('pr.mem.aria', { sys: mem[0], cam: mem[1], oth: mem[2], our: mem[3], free: mem[4] }).replace(/"/g, '') + '">';
    mem.forEach(function (mb, j) { var w = mb / 4000 * W; if (w > 0) svg += '<rect class="' + cls[j] + '" x="' + x.toFixed(1) + '" y="1" width="' + w.toFixed(1) + '" height="28"/>'; x += w; });
    svg += '</svg>';
    var leg = h('div', { class: 'vz-legend' }, keys.map(function (k, j) { return h('span', null, h('i', { class: 'vz-sw ' + cls[j] }), T('pr.m.' + k, { n: mem[j] })); }));
    var sb = h('tbody');
    P.SURV[c][i].forEach(function (r) {
      var bad = P.BAD[r[2]], ok = r[2] === 'restored' || r[2] === 'refilled' || r[2] === 'attached' || r[2] === 'kept' || r[2] === 'copied';
      sb.appendChild(h('tr', null, h('th', { text: T('pr.w.' + r[0]) }), h('td', { class: r[1] === 'none' ? 'dim' : null, text: T('pr.h.' + r[1]) }),
        h('td', { class: bad ? 'bad' : (r[2] === 'na' || r[2] === 'nofile' ? 'dim' : (ok ? 'ok' : null)), text: T('pr.st.' + r[2]) })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('pr.cap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), tb)),
      h('p', { class: 'vz-cap', text: T('pr.mcap') }), h('div', { html: svg }), leg,
      h('p', { class: 'vz-cap', text: T('pr.scap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['where', 'holds', 'st'].map(function (k) { return h('th', { text: T('pr.scol.' + k) }); }))), sb)),
      h('div', { class: 'vz-legend', text: T('pr.legend') })));
  }, { labelKey: K + 'tab.pr', icon: 'layers' });

  /* ---------- I3: làn thời gian hai luồng (SVG), đồ thị chờ (SVG), bảng bốn điều kiện ---------- */
  ADE.registerScreen('sysdesign.lock', function (box, ctx) {
    var h = ADE.ui.h, P = ADE.sysLock, c = ctx.state.case, i = Math.max(0, idx(ctx)), t = P.TS[c][i];
    var X0 = 86, PX = 63, X = function (s) { return (X0 + s * PX).toFixed(1); };
    var svg = '<svg class="vz-tl" viewBox="0 0 600 124" role="img" aria-label="' + esc(T('lk.aria', { ms: P.blocked(c, i) })) + '">';
    [['main', 22], ['sync', 64]].forEach(function (ln) {
      svg += '<text class="vz-tl-n" x="4" y="' + (ln[1] + 19) + '">' + esc(T('lk.lane.' + ln[0])) + '</text><line class="vz-tl-base" x1="' + X0 + '" x2="' + X(8) + '" y1="' + (ln[1] + 15) + '" y2="' + (ln[1] + 15) + '"/>';
      P.LANES[c][ln[0]].forEach(function (g) {
        if (g[0] >= t) return;
        var e = Math.min(g[1], t), w = (e - g[0]) * PX;
        svg += '<rect class="vz-tl-' + g[2] + '" x="' + X(g[0]) + '" y="' + ln[1] + '" width="' + w.toFixed(1) + '" height="30"/>';
        var lb = g[3] ? T('lk.seg.' + g[3]) : '';
        if (lb && w > lb.length * 6.8 + 10) svg += '<text class="vz-tl-t" x="' + (+X(g[0]) + 5) + '" y="' + (ln[1] + 19) + '">' + esc(lb) + '</text>';
      });
    });
    for (var s = 0; s <= 8; s++) svg += '<line class="vz-tl-tick" x1="' + X(s) + '" x2="' + X(s) + '" y1="98" y2="103"/><text class="vz-tl-ax" x="' + X(s) + '" y="117">' + s + 's</text>';
    if (P.ANR[c] !== null && t >= P.ANR[c]) svg += '<line class="vz-tl-anr" x1="' + X(P.ANR[c]) + '" x2="' + X(P.ANR[c]) + '" y1="14" y2="100"/><text class="vz-tl-anrt" x="' + (+X(P.ANR[c]) + 4) + '" y="12">' + esc(T('lk.seg.anr')) + '</text>';
    svg += '<line class="vz-tl-cur" x1="' + X(t) + '" x2="' + X(t) + '" y1="16" y2="100"/></svg>';
    // đồ thị chờ
    var wf = P.WF[c][i], cyc = wf.length === 2 && wf[0][0] === wf[1][1], u = 'lkwf' + (++uidN);
    var g = '<svg class="vz-wf" viewBox="0 0 360 132" role="img" aria-label="' + esc(T('lk.g.aria')) + '"><defs><marker id="' + u + '" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-dg-head' + (cyc ? ' bad' : '') + '"/></marker></defs>';
    [['main', 20], ['sync', 240]].forEach(function (n) { g += '<g class="vz-dg-n' + (cyc ? ' bad' : '') + '"><rect x="' + n[1] + '" y="46" width="100" height="40" rx="4"/><text class="vz-dg-t" x="' + (n[1] + 50) + '" y="70" text-anchor="middle">' + esc(T('lk.lane.' + n[0])) + '</text></g>'; });
    wf.forEach(function (e) {
      var top = e[0] === 'main', d = top ? 'M120 54 C 165 14, 195 14, 238 54' : 'M240 78 C 195 118, 165 118, 122 78';
      g += '<path class="vz-dg-e' + (cyc ? ' bad' : '') + '" d="' + d + '" marker-end="url(#' + u + ')"/><text class="vz-dg-s" x="180" y="' + (top ? 18 : 126) + '" text-anchor="middle">' + esc(e[2]) + '</text>';
    });
    g += '</svg>';
    var k = P.conds(c, i), all = k.me && k.hw && k.np && k.cw, cb = h('tbody');
    ['me', 'hw', 'np', 'cw'].forEach(function (q) { cb.appendChild(h('tr', null, h('th', { text: T('lk.c.' + q) }), h('td', { class: k[q] ? (all ? 'bad' : 'ok') : 'dim', text: T(k[q] ? 'lk.c.yes' : 'lk.c.no') }))); });
    cb.appendChild(h('tr', null, h('th', { text: T('lk.c.verdict') }), h('td', { class: all ? 'bad' : 'ok', text: T(all ? 'lk.c.dead' : 'lk.c.alive') })));
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('lk.cap') }), h('div', { class: 'vz-scroll', html: svg }), h('div', { class: 'vz-legend', text: T('lk.legend') }),
      h('p', { class: 'vz-cap', text: T('lk.gcap') }), wf.length ? h('div', { html: g }) : h('p', { class: 'vz-cap dim', text: T('lk.g.none') }),
      h('p', { class: 'vz-cap', text: T('lk.ccap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, cb))));
  }, { labelKey: K + 'tab.lk', icon: 'thread' });
})();
