/* Hình trực quan theo bước của track I (ADE.registerScreen với nhãn tab riêng). Sơ đồ node vẫn ở tab bên cạnh. */
(function () {
  'use strict';
  var K = 'track.sysdesign.vz.';
  var T = function (k, p) { return ADE.t(K + k, p); };
  var KS = ['s1', 's2', 's3', 's4'];
  var esc = function (x) { return String(x).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); };
  var uidN = 0;
  function fitText(str, w) { return String(str).length * 6.6 > w ? ' textLength="' + w + '" lengthAdjust="spacingAndGlyphs"' : ''; }
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

  /* ---------- I4: sơ đồ tuần tự (cột là các bên, hàng là tin), và bảng so sánh các kênh ---------- */
  ADE.registerScreen('sysdesign.channel', function (box, ctx) {
    var h = ADE.ui.h, Y = ADE.sysChannel, c = ctx.state.case, i = Math.max(0, idx(ctx)), parts = Y.PARTS[c];
    var COL = parts.length === 3 ? { app: 90, fcm: 300, server: 510 } : { app: 120, server: 480 }, ROW = 34, TOP = 52, W = 600;
    var rows = []; for (var k = 0; k <= i; k++) Y.MSGS[c][k].forEach(function (x) { rows.push({ x: x, cur: k === i }); });
    var H = TOP + rows.length * ROW + 16, u = 'chsq' + (++uidN);
    var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="vz-dg vz-sq" role="img" aria-label="' + esc(T('ch.cap')) + '"><defs>' +
      ['n', 'c', 'b'].map(function (t) { return '<marker id="' + u + t + '" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-sq-head ' + t + '"/></marker>'; }).join('') + '</defs>';
    parts.forEach(function (p) {
      var x = COL[p];
      svg += '<line class="vz-sq-life" x1="' + x + '" y1="' + (TOP - 8) + '" x2="' + x + '" y2="' + (H - 6) + '"/><rect class="vz-sq-part" x="' + (x - 66) + '" y="6" width="132" height="30" rx="4"/><text class="vz-dg-t" x="' + x + '" y="26" text-anchor="middle">' + esc(T('ch.p.' + p)) + '</text>';
    });
    rows.forEach(function (r, n) {
      var y = TOP + n * ROW + 20, a = COL[r.x[0]], b = COL[r.x[1]], bad = r.x[3] === 1, cl = 'vz-sq-m' + (bad ? ' bad' : '') + (r.cur ? ' cur' : '');
      var mk = 'url(#' + u + (bad ? 'b' : (r.cur ? 'c' : 'n')) + ')', lb = T('ch.m.' + r.x[2]);
      if (a === b) {
        var right = a < 300, tx = right ? a + 28 : a - 28;
        svg += '<path class="' + cl + '" d="M' + a + ' ' + (y - 10) + ' h ' + (right ? 22 : -22) + ' v 14 h ' + (right ? -20 : 20) + '" marker-end="' + mk + '"/><text class="vz-sq-l' + (bad ? ' bad' : '') + '" x="' + tx + '" y="' + (y + 1) + '"' + (right ? '' : ' text-anchor="end"') + fitText(lb, right ? 300 : a - 40) + '>' + esc(lb) + '</text>';
      } else {
        var dir = b > a ? 1 : -1;
        svg += '<line class="' + cl + '" x1="' + (a + dir * 4) + '" y1="' + y + '" x2="' + (b - dir * 6) + '" y2="' + y + '" marker-end="' + mk + '"/><text class="vz-sq-l' + (bad ? ' bad' : '') + '" x="' + ((a + b) / 2) + '" y="' + (y - 6) + '" text-anchor="middle"' + fitText(lb, Math.abs(b - a) - 16) + '>' + esc(lb) + '</text>';
      }
    });
    svg += '</svg>';
    var cols = ['dir', 'lat', 'cost', 'bg'];
    var tb = h('tbody');
    Y.ROWS.forEach(function (r) {
      var on = r === c;
      tb.appendChild(h('tr', null, h('th', { class: on ? 'hl' : (r === 'sse' ? 'dim' : null), text: T('ch.r.' + r + '.name') }), cols.map(function (k) {
        return h('td', { class: k === 'bg' ? (r === 'push' ? 'ok' : (on ? 'bad' : 'dim')) : (on ? 'hl' : null), text: T('ch.r.' + r + '.' + k) });
      })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('ch.cap') }), h('div', { class: 'vz-scroll', html: svg }),
      h('p', { class: 'vz-cap', text: T('ch.tcap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, h('th', { text: T('ch.col.ch') }), cols.map(function (k) { return h('th', { text: T('ch.col.' + k) }); }))), tb)),
      h('div', { class: 'vz-legend', text: T('ch.legend') })));
  }, { labelKey: K + 'tab.ch', icon: 'queue' });

  /* ---------- I5: sơ đồ tuần tự app, mạng, server (tin mất dừng ở giữa) + bảng lịch; tình huống bão: làn thử lại của 5 máy ---------- */
  ADE.registerScreen('sysdesign.retry', function (box, ctx) {
    var h = ADE.ui.h, Y = ADE.sysRetry, c = ctx.state.case, i = Math.max(0, idx(ctx));
    if (c === 'storm') {
      var kind = Y.STORM_KIND[i], X0 = 70, PX = 32, X = function (t) { return (X0 + t * PX).toFixed(1); }, pk = Y.peak(kind);
      var sv = '<svg class="vz-tl" viewBox="0 0 600 236" role="img" aria-label="' + esc(T('rt.s.aria', { n: pk })) + '">';
      for (var n = 0; n < 5; n++) {
        var y = 20 + n * 36;
        sv += '<text class="vz-tl-n" x="4" y="' + (y + 4) + '">' + esc(T('rt.s.phone', { n: n + 1 })) + '</text><line class="vz-tl-base" x1="' + X0 + '" x2="' + X(16) + '" y1="' + y + '" y2="' + y + '"/>';
        sv += '<circle class="vz-rt-fail" cx="' + X(0) + '" cy="' + y + '" r="6"/>';
        Y.SCHED[kind][n].forEach(function (t) { sv += '<circle class="vz-rt-dot" cx="' + X(t) + '" cy="' + y + '" r="6"/>'; });
      }
      for (var s = 0; s <= 16; s += 2) sv += '<line class="vz-tl-tick" x1="' + X(s) + '" x2="' + X(s) + '" y1="194" y2="200"/><text class="vz-tl-ax" x="' + X(s) + '" y="214">' + s + 's</text>';
      sv += '<text class="' + (pk >= 4 ? 'vz-tl-anrt' : 'vz-tl-t') + '" x="' + X0 + '" y="232">' + esc(T('rt.s.' + kind) + ' · ' + T('rt.s.peak', { n: pk })) + '</text></svg>';
      box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('rt.scap') }), h('div', { class: 'vz-scroll', html: sv })));
      return;
    }
    var COL = { app: 90, mid: 300, server: 510 }, ROW = 34, TOP = 52, W = 600;
    var rows = []; for (var k = 0; k <= i; k++) Y.MSGS[c][k].forEach(function (x) { rows.push({ x: x, cur: k === i }); });
    var H = TOP + rows.length * ROW + 16, u = 'rtsq' + (++uidN);
    var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="vz-dg vz-sq" role="img" aria-label="' + esc(T('rt.cap')) + '"><defs>' +
      ['n', 'c', 'b'].map(function (t) { return '<marker id="' + u + t + '" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-sq-head ' + t + '"/></marker>'; }).join('') + '</defs>';
    ['app', 'server'].forEach(function (p) {
      var x = COL[p];
      svg += '<line class="vz-sq-life" x1="' + x + '" y1="' + (TOP - 8) + '" x2="' + x + '" y2="' + (H - 6) + '"/><rect class="vz-sq-part" x="' + (x - 66) + '" y="6" width="132" height="30" rx="4"/><text class="vz-dg-t" x="' + x + '" y="26" text-anchor="middle">' + esc(T('rt.p.' + p)) + '</text>';
    });
    rows.forEach(function (r, n) {
      var y = TOP + n * ROW + 20, a = COL[r.x[0]], b = COL[r.x[1]], bad = r.x[3] === 1, cl = 'vz-sq-m' + (bad ? ' bad' : '') + (r.cur ? ' cur' : '');
      var mk = 'url(#' + u + (bad ? 'b' : (r.cur ? 'c' : 'n')) + ')', lb = T('rt.m.' + r.x[2]);
      if (r.x[0] === 'mid') { svg += '<text class="vz-sq-l bad" x="' + a + '" y="' + (y + 1) + '" text-anchor="middle">' + esc(lb) + '</text>'; return; }
      if (a === b) {
        var right = a < 300, tx = right ? a + 28 : a - 28;
        svg += '<path class="' + cl + '" d="M' + a + ' ' + (y - 10) + ' h ' + (right ? 22 : -22) + ' v 14 h ' + (right ? -20 : 20) + '" marker-end="' + mk + '"/><text class="vz-sq-l' + (bad ? ' bad' : '') + '" x="' + tx + '" y="' + (y + 1) + '"' + (right ? '' : ' text-anchor="end"') + fitText(lb, right ? 300 : a - 40) + '>' + esc(lb) + '</text>';
      } else {
        var dir = b > a ? 1 : -1, end = b === COL.mid ? b : b - dir * 6;
        svg += '<line class="' + cl + '" x1="' + (a + dir * 4) + '" y1="' + y + '" x2="' + end + '" y2="' + y + '"' + (b === COL.mid ? '' : ' marker-end="' + mk + '"') + '/>' + (b === COL.mid ? '<text class="vz-sq-l bad" x="' + (b + dir * 10) + '" y="' + (y + 4) + '"' + (dir < 0 ? ' text-anchor="end"' : '') + '>✕</text>' : '') +
          '<text class="vz-sq-l' + (bad ? ' bad' : '') + '" x="' + ((a + b) / 2) + '" y="' + (y - 6) + '" text-anchor="middle"' + fitText(lb, Math.abs(b - a) - 16) + '>' + esc(lb) + '</text>';
      }
    });
    svg += '</svg>';
    var bk = Y.BOOK[c][i], tb = h('tbody');
    if (!bk.length) tb.appendChild(h('tr', null, h('td', { class: 'dim', colspan: '2', text: T('rt.t.none') })));
    bk.forEach(function (b) { tb.appendChild(h('tr', null, h('td', { class: b[2] ? 'bad' : 'ok', text: b[0] + (b[2] ? ' · ' + T('rt.t.dup') : '') }), h('td', { class: b[1] ? null : 'dim', text: b[1] || T('rt.t.nokey') }))); });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('rt.cap') }), h('div', { class: 'vz-scroll', html: svg }),
      h('p', { class: 'vz-cap', text: T('rt.tcap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, h('th', { text: T('rt.t.id') }), h('th', { text: T('rt.t.key') }))), tb)),
      h('div', { class: 'vz-legend', text: T('rt.legend') })));
  }, { labelKey: K + 'tab.rt', icon: 'replay' });

  /* ---------- I6: bảng ba tầng cache (tầng trả lời có viền) + giá hiển thị so với server; bảng header → hành vi ---------- */
  ADE.registerScreen('sysdesign.cache', function (box, ctx) {
    var h = ADE.ui.h, Y = ADE.sysCache, c = ctx.state.case, i = Math.max(0, idx(ctx)), p = Y.P[c][i];
    var tb = h('tbody');
    ['mem', 'disk', 'net'].forEach(function (t, j) {
      var r = p[0][j], ans = p[1] === t, waste = t === 'net' && Y.WASTE[c][i] === 1, old = r === 'hitold';
      tb.appendChild(h('tr', null, h('th', { class: ans ? 'hl' : null, text: T('ca.t.' + t) }),
        h('td', { class: old || waste ? 'bad' : (ans ? 'hl' : (r === 'off' || r === 'skip' ? 'dim' : null)), text: T('ca.r.' + r) }),
        h('td', { class: 'c' + (t === 'net' && p[2] ? '' : ' dim'), text: t === 'net' ? String(p[2]) : '0' })));
    });
    var ok = Y.right(c, i) === 1, fee = function (n) { return T(n ? 'ca.fee.new' : 'ca.fee.old'); };
    tb.appendChild(h('tr', null, h('th', { text: T('ca.shown') }), h('td', { class: ok ? 'ok' : 'bad', colspan: '2', text: fee(p[3]) })));
    tb.appendChild(h('tr', null, h('th', { text: T('ca.server') }), h('td', { class: 'dim', colspan: '2', text: fee(Y.SERVER_NEW[i]) })));
    var hb = h('tbody');
    ['maxage', 'nocache', 'nostore', 'mustrev', 'private', 'etag', 'n304'].forEach(function (k) {
      var on = Y.HDR[c].indexOf(k) >= 0;
      hb.appendChild(h('tr', null, h('th', { class: on ? 'hl' : null, text: Y.HNAMES[k] }), h('td', { class: on ? 'hl' : null, text: T('ca.h.' + k + '.what') })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('ca.cap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['tier', 'res', 'kb'].map(function (k) { return h('th', { text: T('ca.col.' + k) }); }))), tb)),
      h('p', { class: 'vz-cap', text: T('ca.hcap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, hb)),
      h('div', { class: 'vz-legend', text: T('ca.legend') })));
  }, { labelKey: K + 'tab.ca', icon: 'layers' });

  /* ---------- I7: hai dãy ô đặt cạnh nhau: danh sách trên server lúc này và danh sách app đã tải theo trang ---------- */
  ADE.registerScreen('sysdesign.paging', function (box, ctx) {
    var h = ADE.ui.h, P = ADE.sysPaging, c = ctx.state.case, i = Math.max(0, idx(ctx)), k = P.marks(c, i), ps = P.pages(c, i);
    var pageOf = [], fresh = [];
    ps.forEach(function (p) { p[2].forEach(function (x, j) { pageOf.push(j === 0 ? T('pg.page.' + p[1]) : ''); fresh.push(p[0] === i); }); });
    var tb = h('tbody'), n = Math.max(k.srv.length, k.app.length);
    for (var r = 0; r < n; r++) {
      var sm = k.srvMk[r], am = k.appMk[r], sx = k.srv[r], ax = k.app[r];
      tb.appendChild(h('tr', null, h('td', { class: 'c dim', text: String(r + 1) }),
        h('td', { class: sx === undefined ? 'dim' : (sm === 'miss' ? 'bad' : (sm === 'new' ? 'hl' : null)), text: sx === undefined ? '' : T('pg.post', { n: sx }) + (sm ? ' · ' + T('pg.mk.' + sm) : '') }),
        h('td', { class: ax === undefined ? 'dim' : (am === 'dup' ? 'bad' : (am === 'gone' ? 'dim' : (fresh[r] ? 'hl' : null))), text: ax === undefined ? '' : T('pg.post', { n: ax }) + (am ? ' · ' + T('pg.mk.' + am) : '') }),
        h('td', { class: 'dim', text: ax === undefined ? '' : pageOf[r] })));
    }
    var req = P.REQ[c][i], ev = P.EV[c];
    var top = h('div', { class: 'vz-box' + (i === 1 ? ' hl' : '') }, h('div', { class: 'vz-h', text: T(i === 1 ? 'pg.evh' : 'pg.reqh') }),
      h('div', { text: i === 1 ? [ev.ins ? T('pg.ev.ins') : '', ev.del ? T('pg.ev.del') : ''].filter(Boolean).join(' ') : (req || T('pg.req.none')) }));
    var kids = [h('p', { class: 'vz-cap', text: T('pg.cap') }), top,
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['pos', 'srv', 'app', 'page'].map(function (q) { return h('th', { text: T('pg.col.' + q) }); }))), tb))];
    if (P.CRASH[c][i]) kids.push(h('div', { class: 'vz-box bad' }, h('div', { class: 'vz-h', text: T('pg.crashh') }), h('div', { text: 'Key "17" was already used. If you are using LazyColumn/Row please make sure you provide a unique key for each item.' })));
    kids.push(h('div', { class: 'vz-legend', text: T('pg.legend') }));
    box.appendChild(h('div', { class: 'vz' }, kids));
  }, { labelKey: K + 'tab.pg', icon: 'list' });
})();
