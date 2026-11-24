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
      // nhãn bài có data-k: khi bài mới chèn lên đầu, các bài cũ TRƯỢT xuống một hàng (ui.labMotion, FLIP)
      var occ = {}; for (var q = 0; q < r; q++) if (k.app[q] === ax) occ[ax] = (occ[ax] || 0) + 1;
      tb.appendChild(h('tr', null, h('td', { class: 'c dim', text: String(r + 1) }),
        h('td', { class: sx === undefined ? 'dim' : (sm === 'miss' ? 'bad' : (sm === 'new' ? 'hl' : null)) }, sx === undefined ? null : h('span', { class: 'vz-item', 'data-k': 's' + sx, text: T('pg.post', { n: sx }) + (sm ? ' · ' + T('pg.mk.' + sm) : '') })),
        h('td', { class: ax === undefined ? 'dim' : (am === 'dup' ? 'bad' : (am === 'gone' ? 'dim' : (fresh[r] ? 'hl' : null))) }, ax === undefined ? null : h('span', { class: 'vz-item', 'data-k': 'a' + ax + '-' + (occ[ax] || 0), text: T('pg.post', { n: ax }) + (am ? ' · ' + T('pg.mk.' + am) : '') })),
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

  /* ---------- I8: làn thời gian ba cột (máy tính bảng | server | điện thoại) theo từng mốc; bảng gộp từng trường của bản ghi ---------- */
  ADE.registerScreen('sysdesign.conflict', function (box, ctx) {
    var h = ADE.ui.h, Y = ADE.sysConflict, c = ctx.state.case, i = Math.max(0, idx(ctx)), st = Y.states(c), cur = st[i];
    var tl = h('tbody');
    Y.ACT[c].forEach(function (row, r) {
      var on = r === i, future = r > i, lostRow = Y.lost(c, r) > 0;
      tl.appendChild(h('tr', null, h('th', { class: on ? 'hl' : (future ? 'dim' : null), text: T('cf.t.' + r) }),
        row.map(function (a, j) {
          var bad = !future && ((lostRow && ((j === 1 && a === 'lwwTake') || a === 'pullLost')) || a === 'conflict');
          return h('td', { class: future ? 'dim' : (bad ? 'bad' : (on && a !== 'idle' ? 'hl' : null)), text: future ? '' : T('cf.a.' + a) + (j === 1 && !future ? ' (v' + st[r][3] + ')' : '') });
        })));
    });
    var te = Y.ed(c, 'tab'), pe = Y.ed(c, 'phn'), fb = h('tbody');
    Y.F.forEach(function (f) {
      var val = function (v) { return T('cf.v.' + v); };
      var tch = cur[0][f] !== Y.BASE[f], pch = cur[2][f] !== Y.BASE[f], conf = cur[4].indexOf(f) >= 0;
      var want = [te, pe].filter(function (e) { return e[0] === f; }).map(function (e) { return e[1]; });
      var srvBad = i >= 2 && want.length && want.indexOf(cur[1][f]) < 0 && cur[1][f] !== 'both' && !(c === 'ifmatch' && i === 2);
      fb.appendChild(h('tr', null, h('th', { text: T('cf.f.' + f) }), h('td', { class: 'dim', text: val(Y.BASE[f]) }),
        h('td', { class: tch ? 'hl' : null, text: val(cur[0][f]) }), h('td', { class: pch ? 'hl' : null, text: val(cur[2][f]) }),
        h('td', { class: conf || srvBad ? 'bad' : (cur[1][f] !== Y.BASE[f] ? 'ok' : null), text: conf ? val(cur[0][f]) + ' | ' + val(cur[2][f]) + ' · ' + T('cf.mk.conflict') : val(cur[1][f]) + (srvBad ? ' · ' + T('cf.mk.lost') : '') })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('cf.cap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['time', 'tab', 'srv', 'phn'].map(function (k) { return h('th', { text: T('cf.col.' + k) }); }))), tl)),
      h('p', { class: 'vz-cap', text: T('cf.fcap', { v: cur[3] }) }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['field', 'base', 'tab', 'phn', 'srv'].map(function (k) { return h('th', { text: T('cf.fcol.' + k) }); }))), fb)),
      h('div', { class: 'vz-legend', text: T('cf.legend') })));
  }, { labelKey: K + 'tab.cf', icon: 'list' });

  /* ---------- I9: sơ đồ tuần tự server, dịch vụ đẩy, app; bảng "dịch vụ đẩy bảo đảm gì → thiết kế đáp lại" ---------- */
  ADE.registerScreen('sysdesign.push', function (box, ctx) {
    var h = ADE.ui.h, Y = ADE.sysPush, c = ctx.state.case, i = Math.max(0, idx(ctx));
    var COL = { srv: 90, push: 300, app: 510 }, ROW = 34, TOP = 52, W = 600;
    var rows = []; for (var k = 0; k <= i; k++) Y.MSGS[c][k].forEach(function (x) { rows.push({ x: x, cur: k === i }); });
    var H = TOP + rows.length * ROW + 16, u = 'pusq' + (++uidN);
    var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="vz-dg vz-sq" role="img" aria-label="' + esc(T('pu.cap')) + '"><defs>' +
      ['n', 'c', 'b'].map(function (t) { return '<marker id="' + u + t + '" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-sq-head ' + t + '"/></marker>'; }).join('') + '</defs>';
    Y.PARTS.forEach(function (p) {
      var x = COL[p];
      svg += '<line class="vz-sq-life" x1="' + x + '" y1="' + (TOP - 8) + '" x2="' + x + '" y2="' + (H - 6) + '"/><rect class="vz-sq-part" x="' + (x - 66) + '" y="6" width="132" height="30" rx="4"/><text class="vz-dg-t" x="' + x + '" y="26" text-anchor="middle"' + fitText(T('pu.p.' + p), 124) + '>' + esc(T('pu.p.' + p)) + '</text>';
    });
    rows.forEach(function (r, n) {
      var y = TOP + n * ROW + 20, a = COL[r.x[0]], b = COL[r.x[1]], bd = r.x[3] === 1, cl = 'vz-sq-m' + (bd ? ' bad' : '') + (r.cur ? ' cur' : '');
      var mk = 'url(#' + u + (bd ? 'b' : (r.cur ? 'c' : 'n')) + ')', lb = T('pu.m.' + r.x[2]);
      if (a === b) {
        var right = a < 400, tx = right ? a + 28 : a - 28;
        svg += '<path class="' + cl + '" d="M' + a + ' ' + (y - 10) + ' h ' + (right ? 22 : -22) + ' v 14 h ' + (right ? -20 : 20) + '" marker-end="' + mk + '"/><text class="vz-sq-l' + (bd ? ' bad' : '') + '" x="' + tx + '" y="' + (y + 1) + '"' + (right ? '' : ' text-anchor="end"') + fitText(lb, right ? W - tx - 8 : a - 40) + '>' + esc(lb) + '</text>';
      } else {
        var dir = b > a ? 1 : -1;
        svg += '<line class="' + cl + '" x1="' + (a + dir * 4) + '" y1="' + y + '" x2="' + (b - dir * 6) + '" y2="' + y + '" marker-end="' + mk + '"/><text class="vz-sq-l' + (bd ? ' bad' : '') + '" x="' + ((a + b) / 2) + '" y="' + (y - 6) + '" text-anchor="middle"' + fitText(lb, Math.abs(b - a) - 16) + '>' + esc(lb) + '</text>';
      }
    });
    svg += '</svg>';
    var tb = h('tbody'), f = Y.FOCUS[c];
    Y.ROWS.forEach(function (r) {
      var on = r === f;
      tb.appendChild(h('tr', null, h('th', { class: on ? 'hl' : null, text: T('pu.g.' + r) }), h('td', { class: on ? 'hl' : 'dim', text: T('pu.g.' + r + '.no') }), h('td', { class: on ? 'ok' : null, text: T('pu.g.' + r + '.do') })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('pu.cap') }), h('div', { class: 'vz-scroll', html: svg }),
      h('p', { class: 'vz-cap', text: T('pu.gcap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['what', 'no', 'do'].map(function (k) { return h('th', { text: T('pu.gcol.' + k) }); }))), tb)),
      h('div', { class: 'vz-legend', text: T('pu.legend') })));
  }, { labelKey: K + 'tab.pu', icon: 'queue' });

  /* ---------- I10a: bảng tính bộ nhớ bitmap theo từng bước; bảng vòng lặp calculateInSampleSize ---------- */
  ADE.registerScreen('sysdesign.bitmap', function (box, ctx) {
    var h = ADE.ui.h, Y = ADE.sysBitmap, c = ctx.state.case, i = Math.max(0, idx(ctx)), k = Y.calc(c);
    var f1 = function (x) { return T('bm.mib', { n: String(Math.round(x * 100) / 100).replace('.', ADE.lang === 'vi' ? ',' : '.') }); };
    var R = [['src', 0, Y.W + ' × ' + Y.H + ' px'], ['need', 0, Y.REQ + ' × ' + Y.REQ + ' px'], ['s', 1, String(k.s)], ['dec', 2, k.dw + ' × ' + k.dh + ' px'], ['bpp', 2, T('bm.bppv')],
      ['one', 2, f1(k.one)], ['n', 3, String(Y.N)], ['total', 3, f1(k.total)], ['heap', 3, f1(Y.HEAP)]];
    var tb = h('tbody');
    R.forEach(function (r) {
      var shown = i >= r[1], cur = i === r[1], bad = shown && k.oom && r[0] === 'total';
      tb.appendChild(h('tr', null, h('th', { class: cur ? 'hl' : null, text: T('bm.r.' + r[0]) }), h('td', { class: !shown ? 'dim' : (bad ? 'bad' : (cur ? 'hl' : null)), text: shown ? r[2] + (bad ? ' · ' + T('bm.oom') : '') : '?' })));
    });
    var kids = [h('p', { class: 'vz-cap', text: T('bm.cap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, h('th', { text: T('bm.col.what') }), h('th', { text: T('bm.col.val') }))), tb))];
    if (c === 'sampled' && i >= 1) {
      var lb = h('tbody');
      Y.loop().forEach(function (r) {
        lb.appendChild(h('tr', null, h('td', { class: 'c', text: String(r[0]) }), h('td', { class: 'c', text: r[1] + ' × ' + r[2] }), h('td', { class: r[3] ? 'ok' : 'hl', text: T(r[3] ? 'bm.l.go' : 'bm.l.stop') })));
      });
      kids.push(h('p', { class: 'vz-cap', text: T('bm.lcap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['s', 'half', 'go'].map(function (q) { return h('th', { text: T('bm.lcol.' + q) }); }))), lb)));
    }
    kids.push(h('div', { class: 'vz-legend', text: T('bm.legend') }));
    box.appendChild(h('div', { class: 'vz' }, kids));
  }, { labelKey: K + 'tab.bm', icon: 'list' });

  /* ---------- I10b: dãy ô các khúc upload theo từng request; ô HTTP của bước ---------- */
  ADE.registerScreen('sysdesign.upload', function (box, ctx) {
    var h = ADE.ui.h, Y = ADE.sysUpload, c = ctx.state.case, i = Math.max(0, idx(ctx));
    var tb = h('tbody');
    Y.rowsOf(c, i).forEach(function (row) {
      // mỗi lần gửi chia hai hàng 10 khúc để vừa màn hẹp; số trong ô là số thứ tự khúc, màu là trạng thái
      [0, 10].forEach(function (off) {
        var cells = row[1].slice(off, off + 10).map(function (st, n) { return h('td', { class: 'c' + (st === 'ok' ? ' ok' : (st === 'lost' || st === 'part' ? ' bad' : (st === 'sent' ? ' hl' : ' dim'))), title: T('up.st.' + (st || 'none')), text: String(off + n + 1) + (st === 'part' ? '½' : '') }); });
        tb.appendChild(h('tr', null, [h('th', { text: off ? '' : T('up.row.' + row[0]) })].concat(cells)));
      });
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('up.cap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table vz-cells' }, tb)),
      h('div', { class: 'vz-box' + (i === 1 ? ' bad' : '') }, [h('div', { class: 'vz-h', text: T('up.httph') })].concat(Y.HTTP[c][i].map(function (l) { return h('div', { text: l }); }))),
      h('div', { class: 'vz-legend', text: T('up.legend') })));
  }, { labelKey: K + 'tab.up', icon: 'rail' });

  /* ---------- I11: làn thời gian khởi động (luồng chính, luồng nền) với vạch TTID, TTFD; bảng các việc ---------- */
  ADE.registerScreen('sysdesign.startup', function (box, ctx) {
    var h = ADE.ui.h, Y = ADE.sysStartup, c = ctx.state.case, i = Math.max(0, idx(ctx)), its = Y.IT[c].filter(function (x) { return x[4] <= i; });
    var X0 = 96, PW = 488, W = 600, X = function (t) { return (X0 + t * PW / Y.MAX).toFixed(1); }, LY = { main: 34, bg: 74 }, BH = 24, H = 140;
    var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="vz-dg vz-tl" role="img" aria-label="' + esc(T('st.cap')) + '">';
    ['main', 'bg'].forEach(function (l) { svg += '<text class="vz-tl-n" x="4" y="' + (LY[l] + 16) + '"' + fitText(T('st.lane.' + l), 88) + '>' + esc(T('st.lane.' + l)) + '</text><line class="vz-tl-base" x1="' + X0 + '" y1="' + (LY[l] + BH) + '" x2="' + (X0 + PW) + '" y2="' + (LY[l] + BH) + '"/>'; });
    for (var t = 0; t <= Y.MAX; t += 1000) svg += '<line class="vz-tl-tick" x1="' + X(t) + '" y1="' + (LY.bg + BH) + '" x2="' + X(t) + '" y2="' + (LY.bg + BH + 5) + '"/><text class="vz-tl-t" x="' + X(t) + '" y="' + (H - 18) + '" text-anchor="middle">' + (t / 1000) + ' s</text>';
    its.forEach(function (x) {
      var x1 = +X(x[2]), w = Math.max(2, +X(x[2] + x[3]) - x1), init = x[1] === 'main' && ['crash', 'analytics', 'ads', 'chat', 'img', 'db'].indexOf(x[0]) >= 0;
      var cl = (init && c === 'heavy' && x[0] !== 'crash' ? 'vz-tl-wait' : 'vz-tl-run') + (x[4] === i ? ' vz-tl-cur' : '');
      svg += '<rect class="' + cl + '" x="' + x1 + '" y="' + LY[x[1]] + '" width="' + w.toFixed(1) + '" height="' + BH + '" rx="2"/>';
      var lb = T('st.k.' + x[0]); if (lb.length * 6.6 < w - 6) svg += '<text class="vz-tl-t" x="' + (x1 + w / 2).toFixed(1) + '" y="' + (LY[x[1]] + 16) + '" text-anchor="middle">' + esc(lb) + '</text>';
    });
    [['ttid', 2], ['ttfd', 3]].forEach(function (mk) {
      if (i < mk[1]) return; var tx = +X((mk[0] === 'ttid' ? Y.TTID : Y.TTFD)[c]);
      svg += '<line class="vz-tl-anr" x1="' + tx + '" y1="' + (LY.main - 8) + '" x2="' + tx + '" y2="' + (LY.bg + BH + 4) + '"/><text class="vz-tl-anrt" x="' + (tx + 3) + '" y="' + (mk[0] === 'ttid' ? LY.main - 10 : LY.bg + BH + 16) + '"' + (tx > X0 + PW - 70 ? ' text-anchor="end"' : '') + '>' + esc(T('st.m.' + mk[0])) + '</text>';
    });
    svg += '</svg>';
    var tb = h('tbody');
    its.forEach(function (x) {
      var init = x[1] === 'main' && ['crash', 'analytics', 'ads', 'chat', 'img', 'db'].indexOf(x[0]) >= 0, bad = init && c === 'heavy' && x[0] !== 'crash';
      tb.appendChild(h('tr', null, h('th', { class: x[4] === i ? 'hl' : null, text: T('st.k.' + x[0]) }), h('td', { class: bad ? 'bad' : null, text: T('st.lane.' + x[1]) }),
        h('td', { class: 'c', text: String(x[3]) }), h('td', { class: 'dim', text: T('st.w.' + c + '.' + x[0]) })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('st.cap') }), h('div', { class: 'vz-scroll', html: svg }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['job', 'lane', 'ms', 'why'].map(function (k) { return h('th', { text: T('st.col.' + k) }); }))), tb)),
      h('div', { class: 'vz-legend', text: T('st.legend') })));
  }, { labelKey: K + 'tab.st', icon: 'rail' });

  /* ---------- I12a: dãy ô theo ngày: đang phát gì, bao nhiêu người chạy mã lỗi, bao nhiêu người gặp crash ---------- */
  ADE.registerScreen('sysdesign.rollout', function (box, ctx) {
    var h = ADE.ui.h, Y = ADE.sysRollout, c = ctx.state.case, i = Math.max(0, idx(ctx)), shown = Y.STEP_DAYS[i][Y.STEP_DAYS[i].length - 1], now = Y.STEP_DAYS[i];
    var fmt = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ADE.lang === 'vi' ? '.' : ','); };
    var head = h('tr', null, [h('th', { text: T('ro.col.day') })].concat(Y.D[c].map(function (_, d) { return h('th', { class: 'c' + (now.indexOf(d) >= 0 ? ' hl' : ''), text: String(d + 1) }); })));
    var rows = [['offer', function (d) { return T('ro.o.' + Y.D[c][d][0]); }, function () { return null; }],
      ['bad', function (d) { return fmt(Math.round(Y.D[c][d][1] * 1000)); }, function (d) { return Y.D[c][d][1] > 0 ? 'bad' : 'ok'; }],
      ['crash', function (d) { return fmt(Y.crashOf(c, d)); }, function (d) { return Y.crashOf(c, d) > 0 ? 'bad' : 'ok'; }]];
    var tb = h('tbody');
    rows.forEach(function (r) {
      tb.appendChild(h('tr', null, [h('th', { text: T('ro.r.' + r[0]) })].concat(Y.D[c].map(function (_, d) { return h('td', { class: 'c' + (d > shown ? ' dim' : (r[2](d) ? ' ' + r[2](d) : '')), text: d > shown ? '' : r[1](d) }); }))));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('ro.cap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table vz-cells' }, h('thead', null, head), tb)),
      h('div', { class: 'vz-box' }, h('div', { class: 'vz-h', text: T('ro.vh') }), h('div', { text: T('ro.vitals') })),
      h('div', { class: 'vz-legend', text: T('ro.legend') })));
  }, { labelKey: K + 'tab.ro', icon: 'rail' });

  /* ---------- I12b: ma trận phiên bản app × API (trước, sau thay đổi, /v2) ---------- */
  ADE.registerScreen('sysdesign.compat', function (box, ctx) {
    var h = ADE.ui.h, Y = ADE.sysCompat, c = ctx.state.case, i = Math.max(0, idx(ctx));
    var cols = ['before', 'after', 'v2'], tb = h('tbody');
    Y.APPS.forEach(function (a) {
      var r = Y.result(c, a);
      var cell = function (col) {
        if (col === 'before') return a[2] === 'new' ? ['dim', T('cp.r.na')] : ['ok', T('cp.r.ok')];
        if (i < 1) return ['dim', '?'];
        if (col === 'v2') return c === 'versioned' && a[2] === 'new' ? (i >= 2 ? ['ok', T('cp.r.ok')] : ['dim', '?']) : ['dim', T('cp.r.na')];
        if (c === 'versioned') return a[2] === 'new' ? ['dim', T('cp.r.na')] : (i >= 2 ? ['ok', T('cp.r.same')] : ['dim', '?']);
        if (i < 2) return ['dim', '?'];
        return r === 'crash' ? ['bad', T('cp.r.crash')] : (r === 'update' ? ['hl', T('cp.r.update')] : ['ok', T('cp.r.ok')]);
      };
      tb.appendChild(h('tr', null, [h('th', { text: T('cp.app.' + a[0]) }), h('td', { class: 'c dim', text: a[1] + '%' })].concat(cols.map(function (col) { var x = cell(col); return h('td', { class: x[0], text: x[1] }); }))));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('cp.cap') }), h('div', { class: 'vz-box' + (i >= 1 ? ' hl' : '') }, h('div', { class: 'vz-h', text: T('cp.changeh') }), h('div', { text: i >= 1 ? T('cp.change.' + c) : T('cp.change.none') })),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['app', 'share', 'before', 'after', 'v2'].map(function (k) { return h('th', { text: T('cp.col.' + k) }); }))), tb)),
      h('div', { class: 'vz-legend', text: T('cp.legend') })));
  }, { labelKey: K + 'tab.cp', icon: 'list' });

  /* ---------- I13: đồ thị thành phần của app (thành phần sáng theo bước) + sơ đồ tuần tự của tin nhắn ---------- */
  ADE.registerScreen('sysdesign.chat', function (box, ctx) {
    var h = ADE.ui.h, Y = ADE.sysChat, c = ctx.state.case, i = Math.max(0, idx(ctx)), p = Y.P[c][i], u = 'chg' + (++uidN), BW = 108, BH = 34;
    var g = '<svg viewBox="0 0 660 248" class="vz-dg" role="img" aria-label="' + esc(T('ct.gcap')) + '"><defs><marker id="' + u + 'a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-dg-head"/></marker><marker id="' + u + 'b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-dg-head bad"/></marker></defs>';
    g += '<rect class="vz-dg-mod" x="8" y="8" width="520" height="232" rx="6"/><text class="vz-dg-modt" x="16" y="234">' + esc(T('ct.app')) + '</text>';
    Y.EDGES.forEach(function (e, k) {
      var a = Y.COMP[e[0]], b = Y.COMP[e[1]], on = p[1].indexOf(k) >= 0, bd = p[2].indexOf(k) >= 0;
      // điểm đầu, cuối nằm trên viền hộp: co vector nối tâm theo nửa kích thước hộp
      var dx = b[0] - a[0], dy = b[1] - a[1], tt = Math.min(dx ? (BW / 2 + 3) / Math.abs(dx) : 1e9, dy ? (BH / 2 + 3) / Math.abs(dy) : 1e9);
      var sx = a[0] + dx * tt, sy = a[1] + dy * tt, tx = b[0] - dx * tt, ty = b[1] - dy * tt;
      g += '<line class="vz-dg-e' + (bd ? ' bad' : (on ? ' up' : '')) + '" x1="' + sx.toFixed(1) + '" y1="' + sy.toFixed(1) + '" x2="' + tx.toFixed(1) + '" y2="' + ty.toFixed(1) + '" marker-end="url(#' + u + (bd ? 'b' : 'a') + ')"/>';
    });
    Object.keys(Y.COMP).forEach(function (k) {
      var q = Y.COMP[k], on = p[0].indexOf(k) >= 0, lb = T('ct.c.' + k);
      g += '<g class="vz-dg-n' + (on ? ' on' : ' skip') + '"><rect x="' + (q[0] - BW / 2) + '" y="' + (q[1] - BH / 2) + '" width="' + BW + '" height="' + BH + '" rx="4"/><text class="vz-dg-t" x="' + q[0] + '" y="' + (q[1] + 5) + '" text-anchor="middle"' + fitText(lb, BW - 10) + '>' + esc(lb) + '</text></g>';
    });
    g += '</svg>';
    // sơ đồ tuần tự: máy người gửi, máy thứ hai của người gửi, server, máy người nhận; hiện các bước tới bước hiện tại
    var COL = { a: 70, a2: 230, srv: 390, b: 560 }, ROW = 30, TOP = 50, W = 640, rows = [];
    for (var s = 0; s <= i; s++) Y.P[c][s][3].forEach(function (x) { rows.push({ x: x, cur: s === i }); });
    var H = TOP + rows.length * ROW + 14, v = 'chsq' + (++uidN);
    var sq = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="vz-dg vz-sq" role="img" aria-label="' + esc(T('ct.scap')) + '"><defs>' + ['n', 'c', 'b'].map(function (t) { return '<marker id="' + v + t + '" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.5L9 5 1 8.5z" class="vz-sq-head ' + t + '"/></marker>'; }).join('') + '</defs>';
    Y.PARTS.forEach(function (pt) { var x = COL[pt]; sq += '<line class="vz-sq-life" x1="' + x + '" y1="' + (TOP - 8) + '" x2="' + x + '" y2="' + (H - 6) + '"/><rect class="vz-sq-part" x="' + (x - 64) + '" y="6" width="128" height="30" rx="4"/><text class="vz-dg-t" x="' + x + '" y="26" text-anchor="middle"' + fitText(T('ct.p.' + pt), 120) + '>' + esc(T('ct.p.' + pt)) + '</text>'; });
    rows.forEach(function (r, n) {
      var y = TOP + n * ROW + 18, a = COL[r.x[0]], b = COL[r.x[1]], bd = r.x[3] === 1, cl = 'vz-sq-m' + (bd ? ' bad' : '') + (r.cur ? ' cur' : ''), mk = 'url(#' + v + (bd ? 'b' : (r.cur ? 'c' : 'n')) + ')', lb = T('ct.m.' + r.x[2]);
      if (a === b) { var right = a < 400, tx = right ? a + 28 : a - 28; sq += '<path class="' + cl + '" d="M' + a + ' ' + (y - 10) + ' h ' + (right ? 22 : -22) + ' v 14 h ' + (right ? -20 : 20) + '" marker-end="' + mk + '"/><text class="vz-sq-l' + (bd ? ' bad' : '') + '" x="' + tx + '" y="' + (y + 1) + '"' + (right ? '' : ' text-anchor="end"') + fitText(lb, right ? W - tx - 8 : a - 40) + '>' + esc(lb) + '</text>'; }
      else { var dir = b > a ? 1 : -1; sq += '<line class="' + cl + '" x1="' + (a + dir * 4) + '" y1="' + y + '" x2="' + (b - dir * 6) + '" y2="' + y + '" marker-end="' + mk + '"/><text class="vz-sq-l' + (bd ? ' bad' : '') + '" x="' + ((a + b) / 2) + '" y="' + (y - 6) + '" text-anchor="middle"' + fitText(lb, Math.abs(b - a) - 16) + '>' + esc(lb) + '</text>'; }
    });
    sq += '</svg>';
    var tick = h('div', { class: 'vz-box' + (i === Y.P[c].length - 1 ? ' hl' : '') }, h('div', { class: 'vz-h', text: T('ct.tickh') }), h('div', { text: T('ct.tick.' + p[4]) }));
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('ct.gcap') }), h('div', { class: 'vz-scroll', html: g }), tick,
      h('p', { class: 'vz-cap', text: T('ct.scap') }), h('div', { class: 'vz-scroll', html: sq }), h('div', { class: 'vz-legend', text: T('ct.legend') })));
  }, { labelKey: K + 'tab.ct', icon: 'layers' });

  /* ---------- I0: bảng tra mọi triệu chứng; hàng đang chọn có viền, ô "?" mở dần theo bước ---------- */
  ADE.registerScreen('sysdesign.map', function (box, ctx) {
    var h = ADE.ui.h, cur = ctx.state.symptom, i = ctx.step ? ['start', 'first', 'next', 'end'].indexOf(ctx.step.id.split('.').pop()) : (ctx.pos > ctx.N ? 3 : -1);
    var tb = h('tbody');
    ADE.sysMap.forEach(function (r) {
      var on = r[0] === cur;
      tb.appendChild(h('tr', null, h('td', { class: on ? 'hl' : null, text: ADE.t('track.sysdesign.m.map.s.' + r[0] + '.title') }),
        h('td', { class: on && i < 1 ? 'dim' : (on ? 'hl' : null), text: on && i < 1 ? '?' : ADE.t('track.sysdesign.m.map.phase.' + r[2]) }),
        h('td', { class: 'c ' + (on && i < 3 ? 'dim' : (on ? 'hl' : '')), text: on && i < 3 ? '?' : r[1].toUpperCase() })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('map.cap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['sym', 'phase', 'ch'].map(function (k) { return h('th', { text: T('map.col.' + k) }); }))), tb)),
      h('div', { class: 'vz-legend', text: T('map.legend') })));
  }, { labelKey: K + 'tab.map', icon: 'grid' });
})();
