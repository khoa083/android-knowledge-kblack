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

  /* ---------- l3: bảng log kiểu bắt gói tin; dòng truy vấn ở trên; hàng bị lọc thì mờ, hàng bị R8 xóa thì mờ kèm ghi chú;
     hàng lỗi cần tìm và hàng lộ số điện thoại tô đỏ. Tính từ ADE.dbgLogcat; ô đổi lớp thì nháy. ---------- */
  ADE.registerScreen('debugging.logcat', function (box, ctx) {
    var h = ADE.ui.h, L = ADE.dbgLogcat, c = ctx.state.case, i = Math.max(0, idx(ctx)), v = L.view(c, i), q = L.qtext(v.q);
    var tb = h('tbody');
    v.rows.forEach(function (x) {
      var r = x.row, hot = x.shown && (x.pii || (c === 'find' && x.k === 12 && i >= 2));
      var cl = !x.shown ? null : (hot ? 'bad' : null);
      tb.appendChild(h('tr', { 'data-k': 'lc-' + x.k, class: x.shown ? null : 'fade' },
        h('td', { class: cl, text: String(r[0]) }), h('td', { class: cl ? 'c ' + cl : 'c', text: r[1] }), h('td', { class: cl, text: r[2] }),
        h('td', { class: cl, text: x.gone ? T('lc.removed') : x.msg })));
    });
    box.appendChild(h('div', { class: 'vz' },
      h('p', { class: 'vz-sub', 'data-k': 'lc-q-' + c + i, text: T('lc.query', { q: q || T('lc.none') }) }),
      h('p', { class: 'vz-sub', 'data-k': 'lc-b-' + v.build, text: T('lc.build.' + v.build) }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['pid', 'lvl', 'tag', 'msg'].map(function (k) { return h('th', { text: T('lc.col.' + k) }); }))), tb)),
      h('p', { class: 'vz-sub' + (v.pii ? ' bad' : ''), 'data-k': 'lc-n', text: T('lc.count', { n: v.shown, p: v.pii }) }),
      h('div', { class: 'vz-legend', text: T('lc.legend') })));
  }, { labelKey: K + 'tab.logcat', icon: 'list' });

  /* ---------- l4: stack trace từng dòng (bảng phẳng, thụt lề theo tầng, không hộp lồng): frame của app in đậm; hàng đang đọc có viền,
     hàng đặt bản sửa tô đỏ; ở bước 3 của cách đọc tới gốc, dòng "... 8 more" mở ra thành các frame trùng (mờ). Tính từ ADE.dbgTrace. ---------- */
  ADE.registerScreen('debugging.trace', function (box, ctx) {
    var h = ADE.ui.h, D = ADE.dbgTrace, c = ctx.state.case, i = Math.max(0, idx(ctx)), L = D.lines();
    var nCaused = L.filter(function (l) { return l.kind === 'head' && l.layer > 0; }).length;
    function state(l) {
      if (c === 'top') {
        if (i === 0) return l.layer === 0 && l.kind !== 'more' ? 'hl' : null;
        if (i === 2 || i === 3) { if (l.kind === 'frame' && l.layer === 1 && /DetailViewModel\.kt:58/.test(l.text)) return 'bad'; }
        if (i === 3 && l.layer === 2 && l.kind === 'head') return 'hl';
        return null;
      }
      if (i === 0) return l.kind === 'head' ? 'hl' : null;
      if (i === 1) return l.kind === 'head' && l.layer === 2 ? 'hl' : null;
      if (l.kind === 'frame' && l.layer === 2 && /BookingMapper\.kt:22/.test(l.text)) return i === 3 ? 'bad' : 'hl';
      return null;
    }
    var tb = h('tbody'), expand = c === 'root' && i >= 2;
    L.forEach(function (l, n) {
      var st = state(l), pad = 'padding-left:' + (8 + l.layer * 16 + (l.kind === 'head' ? 0 : 14)) + 'px';
      var txt = l.kind === 'more' ? T('tr.more', { n: l.n }) : l.text;
      var cls = st || (l.kind === 'frame' && !l.app ? 'dim' : null);
      tb.appendChild(h('tr', { 'data-k': 'tr-' + n + (st ? '-' + st : '') }, h('td', { class: cls, style: pad, text: txt })));
      if (l.kind === 'more' && l.layer === 2 && expand) l.hidden.forEach(function (f, j) {
        tb.appendChild(h('tr', { 'data-k': 'tr-x-' + j, class: 'fade' }, h('td', { style: 'padding-left:' + (8 + l.layer * 16 + 28) + 'px', text: 'at ' + f })));
      });
    });
    var key = 'tr.focus.' + c + '.' + i, f = D.firstApp(2).replace(/^.*\(|\)$/g, '');
    box.appendChild(h('div', { class: 'vz' },
      h('p', { class: 'vz-sub' + (c === 'top' && i >= 1 ? ' bad' : ''), 'data-k': 'tr-f-' + c + i, text: T(key, { n: nCaused, f: f }) }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table vz-trace' }, tb)),
      h('div', { class: 'vz-legend', text: T('tr.legend') })));
  }, { labelKey: K + 'tab.trace', icon: 'layers' });

  /* ---------- l5: bảng đối chiếu frame (rối, dịch ra, thật, dòng mapping đã dùng); cột "thật" hiện từ bước 3; ô dịch sai tô đỏ.
     Tính từ ADE.dbgRetrace; ô đổi lớp thì nháy. ---------- */
  ADE.registerScreen('debugging.retrace', function (box, ctx) {
    var h = ADE.ui.h, D = ADE.dbgRetrace, c = ctx.state.case, i = Math.max(0, idx(ctx)), rs = D.rows(c, i >= 1), t = D.tally(c, i >= 1), showReal = i >= 2;
    var tb = h('tbody'), sh = function (x) { return String(x).replace(/vn\.henkham\./g, ''); };
    rs.forEach(function (r, n) {
      r = { obf: r.obf, got: sh(r.got), real: sh(r.real), line: sh(r.line), ok: r.ok, wrong: r.wrong };
      tb.appendChild(h('tr', { 'data-k': 'rt-' + n },
        h('td', { text: r.obf }),
        h('td', { class: showReal && r.wrong ? 'bad' : (r.got === '?' ? 'dim' : (showReal && r.ok ? 'ok' : null)), text: r.got === '?' ? T('rt.q') : r.got }),
        h('td', { class: showReal ? null : 'dim', text: showReal ? r.real : T('rt.q') }),
        h('td', { class: 'dim', text: r.line })));
    });
    box.appendChild(h('div', { class: 'vz' },
      h('p', { class: 'vz-sub', 'data-k': 'rt-map-' + c, text: T('rt.map', { f: T('rt.map.' + c) }) }),
      h('p', { class: 'vz-sub' + (c === 'exact' && i >= 2 ? ' bad' : ''), 'data-k': 'rt-head-' + (c === 'exact' && i >= 2 ? 1 : 0), text: T('rt.head', { h: D.HEAD }) }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table vz-trace' }, h('thead', null, h('tr', null, ['obf', 'got', 'real', 'line'].map(function (k) { return h('th', { text: T('rt.col.' + k) }); }))), tb)),
      h('p', { class: 'vz-sub' + (showReal && t.wrong ? ' bad' : ''), 'data-k': 'rt-n-' + i, text: T('rt.count', { ok: t.ok, w: showReal ? t.wrong : 0 }) }),
      h('div', { class: 'vz-legend', text: T('rt.legend') })));
  }, { labelKey: K + 'tab.retrace', icon: 'search' });

  /* ---------- l6: màn hình thu nhỏ (SVG phẳng) với bounds của từng thành phần, chấm đỏ ở điểm chạm; thành phần nhận cú chạm tô đỏ (lớp phủ)
     hay xanh (nút); lớp trong suốt vẽ nét đứt. Dưới là bảng cây thành phần theo thứ tự vẽ; ở cách xem cây, hàng dưới điểm chạm có viền. ---------- */
  ADE.registerScreen('debugging.layout', function (box, ctx) {
    var h = ADE.ui.h, D = ADE.dbgLayout, c = ctx.state.case, i = Math.max(0, idx(ctx)), r = D.hit(D.VAR[c][i]), sc = 0.28, ox = 6, oy = 6;
    var look = c === 'inspect';
    var hn = r.hit === 'button' ? ADE.t('track.debugging.m.layout.hit.button') : ADE.t('track.debugging.m.layout.hit.overlay');
    var svg = '<svg class="vz-dg vz-phone" width="130" height="269" style="width:130px;height:auto" viewBox="0 0 114 236" role="img" aria-label="' + esc(T('ly.aria', { h: hn })) + '">';
    r.tree.forEach(function (n) {
      if (!n.present || n.id === 'root') return;
      var b = n.b, k = n.id === r.hit ? (n.id === 'button' ? 'ok' : 'bad') : (look && i >= 1 && n.id === 'overlay' ? 'bad' : '');
      svg += '<g class="vz-dg-n' + (k ? ' ' + k : '') + (n.alpha === 0 && !k ? ' skip' : '') + '" data-k="ly-' + n.id + '-' + (k || 'n') + '"><rect x="' + (ox + b[0] * sc).toFixed(1) + '" y="' + (oy + b[1] * sc).toFixed(1) +
        '" width="' + (b[2] * sc).toFixed(1) + '" height="' + ((n.id === 'button' ? 48 : b[3]) * sc).toFixed(1) + '" rx="1.5"' + (n.alpha === 0 ? ' stroke-dasharray="3 2"' : '') + '/></g>';
    });
    svg += '<circle class="vz-tap" cx="' + (ox + D.TAP[0] * sc).toFixed(1) + '" cy="' + (oy + D.TAP[1] * sc).toFixed(1) + '" r="3.2"/></svg>';
    var wrap = h('div', { class: 'vz-phone-wrap' }); wrap.innerHTML = svg;
    var underIds = r.under.map(function (n) { return n.id; });
    var tb = h('tbody');
    r.tree.forEach(function (n) {
      var on = look && underIds.indexOf(n.id) >= 0, bad = look && i >= 1 && n.id === 'overlay' && n.present;
      var cl = bad ? 'bad' : (on ? 'hl' : null);
      tb.appendChild(h('tr', { 'data-k': 'ly-r-' + n.id + '-' + (cl || 'n') + '-' + n.b[3] + (n.present ? '' : '-gone'), class: n.present ? null : 'fade' },
        h('td', { class: cl, style: 'padding-left:' + (8 + n.depth * 14) + 'px', text: n.present ? n.name : n.name + ' ' + T('ly.gone') }),
        h('td', { class: cl, text: n.b.join(', ') }), h('td', { class: cl ? 'c ' + cl : 'c', text: String(n.alpha) }), h('td', { class: cl ? 'c ' + cl : 'c', text: T(n.click ? 'ly.yes' : 'ly.no') })));
    });
    var btn = r.tree.filter(function (n) { return n.id === 'button'; })[0];
    box.appendChild(h('div', { class: 'vz' },
      h('div', { class: 'vz-row' }, wrap, h('div', null,
        h('p', { class: 'vz-sub' + (r.hit === 'button' ? '' : ' bad'), 'data-k': 'ly-sub-' + r.hit + '-' + r.under.length, text: T('ly.sub', { n: r.under.length, h: hn }) }),
        h('p', { class: 'vz-sub', 'data-k': 'ly-note-' + c + i, text: T('ly.note.' + c + '.' + i) }))),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table vz-trace' }, h('thead', null, h('tr', null, ['name', 'bounds', 'alpha', 'click'].map(function (k) { return h('th', { text: T('ly.col.' + k) }); }))), tb)),
      h('div', { class: 'vz-legend', text: T('ly.legend') })));
  }, { labelKey: K + 'tab.layout', icon: 'layers' });

  /* ---------- l7: lỗi database: dòng truy vấn và bảng booking thật (hàng khớp truy vấn có viền, ô status làm dòng bị loại tô đỏ);
     lỗi việc nền: chuỗi worker (SVG phẳng, ô và mũi tên), mỗi ô ghi trạng thái và ràng buộc; worker kẹt tô đỏ, đã xong tô xanh. ---------- */
  ADE.registerScreen('debugging.inspect', function (box, ctx) {
    var h = ADE.ui.h, D = ADE.dbgInspect, c = ctx.state.case, i = Math.max(0, idx(ctx)), kids = [];
    if (c === 'db') {
      var t = D.table(i === 3), res = D.query(t), ids = res.map(function (r) { return r[0]; });
      kids.push(h('p', { class: 'vz-sub', 'data-k': 'in-q-' + (i >= 2 ? 1 : 0), text: i >= 2 ? T('in.query', { q: D.Q }) : T('in.noquery') }));
      kids.push(h('p', { class: 'vz-cap', text: T('in.table', { n: t.length }) }));
      var tb = h('tbody');
      t.forEach(function (r) {
        var hit = i >= 2 && ids.indexOf(r[0]) >= 0, badCell = i >= 2 && r[0] === 42 && r[3] !== 'CONFIRMED', hidden = i === 0;
        tb.appendChild(h('tr', { 'data-k': 'in-r-' + r[0] + '-' + r[3] + (hit ? '-hit' : ''), class: hidden ? 'fade' : null },
          h('td', { class: hit ? 'hl' : null, text: String(r[0]) }), h('td', { class: hit ? 'hl' : null, text: r[1] }), h('td', { class: hit ? 'hl' : null, text: r[2] }),
          h('td', { class: badCell ? 'bad' : (hit ? 'hl' : null), text: r[3] })));
      });
      kids.push(h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['id', 'patient', 'day', 'status'].map(function (k) { return h('th', { text: T('in.col.' + k) }); }))), tb)));
      kids.push(h('p', { class: 'vz-sub' + (res.length ? '' : ' bad'), 'data-k': 'in-res-' + res.length + '-' + i, text: T('in.result', { n: res.length, ids: ids.length ? ids.join(', ') : '—' }) }));
    } else {
      var v = i === 3 ? 'fixed' : 'base', st = D.states(v, D.NET), ch = D.CHAIN[v], W = 170, GAP = 26;
      var svg = '<svg class="vz-dg" viewBox="0 0 ' + (3 * W + 2 * GAP + 8) + ' 92" role="img" aria-label="' + esc(T('in.chains', { n: D.stuck(v) })) + '">';
      ch.forEach(function (w, n) {
        var x = 4 + n * (W + GAP), s = i === 0 ? '?' : st[w[0]], cl = i === 0 ? '' : (s === 'SUCCEEDED' ? 'ok' : (s === 'ENQUEUED' || s === 'BLOCKED' ? 'bad' : ''));
        if (n > 0) svg += '<line class="vz-dg-e' + (w[2] ? '' : ' bad') + '" data-k="in-e-' + n + '-' + (w[2] ? 1 : 0) + '" x1="' + (x - GAP) + '" y1="34" x2="' + x + '" y2="34"/>';
        svg += '<g class="vz-dg-n' + (cl ? ' ' + cl : '') + '" data-k="in-w-' + w[0] + '-' + s + '"><rect x="' + x + '" y="10" width="' + W + '" height="48" rx="4"/>' +
          '<text class="vz-dg-t" x="' + (x + 8) + '" y="28">' + esc(w[0]) + '</text><text class="vz-dg-s" x="' + (x + 8) + '" y="48">' + esc(s) + '</text></g>';
        svg += '<text class="vz-dg-s" data-k="in-c-' + w[0] + '-' + (i >= 2 ? 1 : 0) + '" x="' + (x + 8) + '" y="80">' + (i >= 2 || n === 0 ? esc(T('in.need', { c: w[1] })) : '') + '</text>';
      });
      svg += '</svg>';
      var wrap = h('div', { class: 'vz-scroll' }); wrap.innerHTML = svg;
      kids.push(h('p', { class: 'vz-sub', 'data-k': 'in-net', text: T('in.net', { n: T('in.net.metered') }) }));
      kids.push(wrap);
      kids.push(h('p', { class: 'vz-sub' + (D.stuck(v) > 1 ? ' bad' : ''), 'data-k': 'in-stuck-' + i, text: T('in.chains', { n: i === 0 ? '?' : D.stuck(v) }) }));
    }
    kids.push(h('div', { class: 'vz-legend', text: T('in.legend') }));
    box.appendChild(h('div', { class: 'vz' }, kids));
  }, { labelKey: K + 'tab.inspect', icon: 'list' });

  /* ---------- l8: đường tham chiếu (SVG phẳng, 5 ô một hàng) và các cột bộ nhớ sau GC theo từng lần mở, vạch ngang giới hạn 64 MB.
     Ô đỏ: mắt xích giữ Activity đã đóng (từ bước 3 của cách rò); cách sửa có mắt xích list → lambda bị cắt. Tính từ ADE.dbgLeak. ---------- */
  ADE.registerScreen('debugging.leak', function (box, ctx) {
    var h = ADE.ui.h, D = ADE.dbgLeak, c = ctx.state.case, i = Math.max(0, idx(ctx)), n = D.OPENS[i], mm = D.mem(c, n), inst = D.alive(c, n).length;
    var ids = ['root', 'bus', 'list', 'lambda', 'act'], W = 112, G = 14, showPath = i >= 2;
    var svg = '<svg class="vz-dg" viewBox="0 0 ' + (5 * W + 4 * G + 8) + ' 210" role="img" aria-label="' + esc(T('lk.aria', { n: n, m: mm })) + '">';
    ids.forEach(function (id, k) {
      var x = 4 + k * (W + G), lb = ADE.t('track.debugging.m.leak.n.' + id), cut = c === 'fixed' && k === 3;
      var cl = showPath && c === 'leak' ? 'bad' : (cut ? 'skip' : (showPath ? 'ok' : ''));
      if (k > 0) svg += '<line class="vz-dg-e' + (showPath && c === 'leak' ? ' bad' : '') + '" data-k="lk-e-' + k + '-' + (c === 'fixed' && k >= 3 ? 'cut' : 'on') + '"' + (c === 'fixed' && k >= 3 ? ' stroke-dasharray="4 4"' : '') +
        ' x1="' + (x - G) + '" y1="26" x2="' + x + '" y2="26"/>';
      svg += '<g class="vz-dg-n' + (cl ? ' ' + cl : '') + '" data-k="lk-n-' + id + '-' + (cl || 'n') + '"><rect x="' + x + '" y="8" width="' + W + '" height="36" rx="4"/>' +
        '<text class="vz-dg-s" x="' + (x + 6) + '" y="30"' + fit(lb, W - 12) + '>' + esc(lb) + '</text></g>';
    });
    // cột bộ nhớ sau GC cho mỗi lần mở; trục 0..70 MB, vạch giới hạn 64 MB
    var X0 = 40, BW = (5 * W + 4 * G - X0) / 20, Y1 = 200, HMB = 2.0, ly = Y1 - D.LIMIT * HMB;
    svg += '<line class="vz-dg-e bad" data-k="lk-limit" x1="' + X0 + '" y1="' + ly + '" x2="' + (5 * W + 4 * G) + '" y2="' + ly + '"/><text class="vz-dg-s" x="4" y="' + (ly + 4) + '">64</text>';
    for (var j = 1; j <= n; j++) {
      var v = D.mem(c, j), hgt = Math.min(v, 70) * HMB, over = v > D.LIMIT;
      svg += '<g class="vz-dg-n' + (over ? ' bad' : (c === 'leak' && j > 1 ? '' : ' ok')) + '" data-k="lk-b-' + j + '-' + (over ? 'x' : 'o') + '"><rect x="' + (X0 + (j - 1) * BW + 2).toFixed(1) + '" y="' + (Y1 - hgt).toFixed(1) + '" width="' + (BW - 4).toFixed(1) + '" height="' + hgt.toFixed(1) + '" rx="1"/></g>';
    }
    svg += '<text class="vz-dg-s" x="4" y="' + Y1 + '">0</text></svg>';
    var wrap = h('div', { class: 'vz-scroll' }); wrap.innerHTML = svg;
    box.appendChild(h('div', { class: 'vz' },
      wrap,
      h('p', { class: 'vz-sub' + (c === 'leak' && i >= 1 ? ' bad' : ''), 'data-k': 'lk-sub-' + c + i, text: T('lk.sub', { n: n, m: mm, k: inst }) + (c === 'fixed' && i >= 2 ? ' ' + T('lk.cut') : '') }),
      h('div', { class: 'vz-legend', text: T('lk.legend') })));
  }, { labelKey: K + 'tab.leak', icon: 'layers' });

  /* ---------- l9: dòng thời gian (SVG phẳng): vạch vsync theo hạn của tần số đang xét; làn main có một khối cho mỗi khung (rộng theo ms), khối trễ tô đỏ;
     từ bước 2 hiện đoạn parseJson (vàng nhạt) trên main hay trên làn luồng nền; làn RenderThread. Tính từ ADE.dbgJank; ô đổi lớp thì nháy. ---------- */
  ADE.registerScreen('debugging.jank', function (box, ctx) {
    var h = ADE.ui.h, D = ADE.dbgJank, c = ctx.state.case, i = Math.max(0, idx(ctx)), hz = D.HZ[i], F = D.frames(c, hz), t = D.tally(c, hz);
    var X0 = 124, W = 500, sc = W / F.total, showSec = i >= 1;
    var svg = '<svg class="vz-dg vz-lanes" viewBox="0 0 ' + (X0 + W + 8) + ' ' + (c === 'bg' ? 112 : 84) + '" role="img" aria-label="' + esc(T('jk.aria', { n: F.frames.length, hz: hz, l: t.late, m: t.missed })) + '">';
    svg += '<text class="vz-dg-s" x="4" y="26">' + esc(T('jk.lane.main')) + '</text><text class="vz-dg-s" x="4" y="56">' + esc(T('jk.lane.render')) + '</text>';
    if (c === 'bg') svg += '<text class="vz-dg-s" x="4" y="90">' + esc(T('jk.lane.worker')) + '</text>';
    for (var v = 0; v <= F.total + 0.01; v += F.budget) svg += '<line class="vz-vsync" data-k="jk-v-' + hz + '-' + v + '" x1="' + (X0 + v * sc).toFixed(1) + '" y1="6" x2="' + (X0 + v * sc).toFixed(1) + '" y2="' + (c === 'bg' ? 104 : 72) + '"/>';
    F.frames.forEach(function (f) {
      var x = X0 + f.start * sc;
      svg += '<g class="vz-dg-n' + (f.late ? ' bad' : ' ok') + '" data-k="jk-f-' + f.k + '-' + (f.late ? 'l' : 'o') + '"><rect x="' + x.toFixed(1) + '" y="14" width="' + (f.main * sc).toFixed(1) + '" height="18" rx="2"/></g>';
      svg += '<g class="vz-dg-n" data-k="jk-r-' + f.k + '"><rect x="' + (x + f.main * sc).toFixed(1) + '" y="44" width="' + (D.RENDER * sc).toFixed(1) + '" height="16" rx="2"/></g>';
      if (f.page && showSec) {
        if (c === 'main') svg += '<rect class="vz-sec" data-k="jk-s-' + f.k + '" x="' + (x + 4 * sc).toFixed(1) + '" y="17" width="' + (D.PARSE * sc).toFixed(1) + '" height="12" rx="1"/>';
        else svg += '<rect class="vz-sec" data-k="jk-w-' + f.k + '" x="' + Math.max(X0, x - D.PARSE * sc - 4).toFixed(1) + '" y="80" width="' + (D.PARSE * sc).toFixed(1) + '" height="14" rx="1"/>';
      }
    });
    svg += '</svg>';
    var wrap = h('div', { class: 'vz-scroll' }); wrap.innerHTML = svg;
    var L = t.longest;
    box.appendChild(h('div', { class: 'vz' },
      wrap,
      h('p', { class: 'vz-sub' + (t.late ? ' bad' : ''), 'data-k': 'jk-sub-' + c + '-' + hz, text: T('jk.sub', { hz: hz, b: F.budget, l: t.late, m: t.missed }) }),
      h('p', { class: 'vz-sub', 'data-k': 'jk-focus-' + c + i, text: T('jk.focus', { t: L.dur, mm: L.main, r: D.RENDER }) }),
      h('div', { class: 'vz-legend', text: T('jk.legend') })));
  }, { labelKey: K + 'tab.jank', icon: 'clock' });

  /* ---------- l10: cách đọc trace: bảng các luồng (tên, trạng thái, đang chờ, đang giữ, đang ở); hàng main và hàng giữ khóa có viền, ô chờ/giữ gây ANR tô đỏ.
     Cách StrictMode: các dòng vi phạm trong Logcat. Dưới cùng là thanh thời gian chờ của luồng main (0–10 giây) với vạch hạn 5 giây. Tính từ ADE.dbgAnr. ---------- */
  ADE.registerScreen('debugging.anr', function (box, ctx) {
    var h = ADE.ui.h, D = ADE.dbgAnr, c = ctx.state.case, i = Math.max(0, idx(ctx)), st = D.state(c, i), kids = [];
    kids.push(h('p', { class: 'vz-sub', 'data-k': 'an-net-' + st.net, text: T('an.net', { n: T('an.net.' + st.net) }) }));
    if (c === 'trace') {
      var blocked = st.wait > 0, look = i >= 1, deep = i >= 2;
      var rows = [
        ['main (tid 1)', blocked ? 'Blocked' : 'Native', blocked ? '<0x0a1b> (tid 24)' : '—', '—', st.fixed ? 'EditViewModel.onSave → Dispatchers.IO' : 'BookingRepo.save'],
        ['SyncWorker (tid 24)', 'Native', '—', blocked ? '<0x0a1b>' : '—', st.fixed ? 'api.fetchAll() ' + T('an.outside') : 'socketRead0 ← BookingRepo.sync'],
        ['RenderThread (tid 8)', 'Native', '—', '—', 'nativePollOnce'],
        ['BG Thread #0 (tid 26)', 'Waiting', '—', '—', 'Unsafe.park']];
      var tb = h('tbody');
      rows.forEach(function (r, n) {
        var hl = look && (n === 0 || (deep && n === 1)), redW = look && blocked && n === 0, redH = deep && blocked && n === 1;
        tb.appendChild(h('tr', { 'data-k': 'an-t-' + n + '-' + r[1] + (hl ? '-hl' : '') + (blocked ? '-b' : '') },
          h('td', { class: hl ? 'hl' : null, text: r[0] }), h('td', { class: redW ? 'bad' : (hl ? 'hl' : null), text: r[1] }),
          h('td', { class: redW ? 'bad' : (hl ? 'hl' : null), text: r[2] }), h('td', { class: redH ? 'bad' : (hl ? 'hl' : null), text: r[3] }), h('td', { class: hl ? 'hl' : null, text: r[4] })));
      });
      kids.push(h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table vz-trace' }, h('thead', null, h('tr', null, ['name', 'state', 'wait', 'hold', 'at'].map(function (k) { return h('th', { text: T('an.col.' + k) }); }))), tb)));
    } else {
      kids.push(h('p', { class: 'vz-cap', text: T('an.viol.title') }));
      var lb = h('tbody');
      var lines = !st.strictOn ? [T('an.viol.none')] : (st.viol.length ? st.viol.map(function (v) { return 'D/StrictMode: StrictMode policy violation: android.os.strictmode.' + v; }) : [T('an.viol.zero')]);
      lines.forEach(function (l, n) { lb.appendChild(h('tr', { 'data-k': 'an-v-' + i + '-' + n }, h('td', { class: st.viol.length ? 'bad' : 'dim', text: l }))); });
      kids.push(h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table vz-trace' }, lb)));
    }
    var X0 = 8, W = 500, sc = W / 10, ww = Math.min(st.wait, 10) * sc;
    var svg = '<svg class="vz-dg vz-lanes" viewBox="0 0 520 52" role="img" aria-label="' + esc(T('an.bar', { w: st.wait })) + '">' +
      '<line class="vz-dg-e" x1="' + X0 + '" y1="20" x2="' + (X0 + W) + '" y2="20"/>' +
      (ww > 0 ? '<g class="vz-dg-n' + (st.anr ? ' bad' : '') + '" data-k="an-w-' + st.wait + '"><rect x="' + X0 + '" y="10" width="' + ww.toFixed(1) + '" height="20" rx="2"/></g>' : '') +
      '<line class="vz-dg-e bad" data-k="an-lim" x1="' + (X0 + D.LIMIT * sc) + '" y1="4" x2="' + (X0 + D.LIMIT * sc) + '" y2="36"/>' +
      '<text class="vz-dg-s" x="' + (X0 + D.LIMIT * sc + 8) + '" y="46">5 s</text><text class="vz-dg-s" x="' + X0 + '" y="44">0</text><text class="vz-dg-s" x="' + (X0 + W - 20) + '" y="44">10 s</text></svg>';
    var wrap = h('div', { class: 'vz-scroll' }); wrap.innerHTML = svg;
    kids.push(wrap);
    kids.push(h('p', { class: 'vz-sub' + (st.anr ? ' bad' : ''), 'data-k': 'an-sub-' + c + i, text: T('an.bar', { w: st.wait }) }));
    kids.push(h('div', { class: 'vz-legend', text: T('an.legend') }));
    box.appendChild(h('div', { class: 'vz' }, kids));
  }, { labelKey: K + 'tab.anr', icon: 'thread' });
})();
