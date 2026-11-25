/* Hình trực quan theo bước của track K (ADE.registerScreen với nhãn tab riêng). Sơ đồ node vẫn ở tab bên cạnh. */
(function () {
  'use strict';
  var K = 'track.fp.vz.';
  var T = function (k, p) { return ADE.t(K + k, p); };
  var KS = ['s1', 's2', 's3', 's4'];
  function idx(ctx) {
    if (ctx.step) return KS.indexOf(ctx.step.id.split('.').pop());
    return ctx.pos > ctx.N ? 3 : 0;
  }

  /* ---------- K1: bảng thế từng bước (mỗi hàng là chương trình sau một lần thay; hàng không thay được tô đỏ)
     + bảng phẳng "test chạy vào ngày" (thứ Hai 23 tới Chủ nhật 29/11/2026). Hàng mới hiện dần một lần; không có chuyển động lặp. ---------- */
  ADE.registerScreen('fp.pure', function (box, ctx) {
    var h = ADE.ui.h, P = ADE.fpPure, c = ctx.state.case, i = Math.max(0, idx(ctx)), v = P.view(c, i);
    var tb = h('tbody');
    v.rows.forEach(function (r, n) {
      var fresh = r[0] === i, st = r[2];
      tb.appendChild(h('tr', { 'data-k': 'pr-' + c + '-' + n },
        h('td', { class: 'c' + (fresh ? ' hl' : ''), text: String(n) }),
        h('td', { class: fresh ? 'hl' : null, translate: 'no', text: r[1] }),
        h('td', { class: 'c' + (st === 'bad' ? ' bad' : (st === 'ok' ? ' ok' : '')), text: T('pure.st.' + st) }),
        h('td', { class: st === 'bad' ? 'bad' : null, text: T('pure.why.' + r[3]) })));
    });
    var run = {}; v.runs.forEach(function (r) { run[r[0]] = r[1]; });
    var head = h('tr', null, h('th', { text: T('pure.col.run') })), body = h('tr', { 'data-k': 'pr-runs-' + c }, h('td', { text: T('pure.test.' + c) }));
    P.WEEK.forEach(function (d) {
      head.appendChild(h('th', { class: 'c', text: T('pure.day.' + d[0], { d: d[1] }) }));
      var has = Object.prototype.hasOwnProperty.call(run, d[0]);
      body.appendChild(h('td', { class: 'c ' + (!has ? 'dim' : (run[d[0]] ? 'ok' : 'bad')), 'data-k': 'pr-day-' + d[0], text: !has ? '?' : T(run[d[0]] ? 'pure.pass' : 'pure.fail') }));
    });
    box.appendChild(h('div', { class: 'vz' },
      h('p', { class: 'vz-cap', text: T('pure.cap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['n', 'expr', 'st', 'why'].map(function (k) { return h('th', { text: T('pure.col.' + k) }); }))), tb)),
      h('p', { class: 'vz-cap', text: T('pure.tcap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), h('tbody', null, body))),
      h('div', { class: 'vz-legend', text: T('pure.legend') })));
  }, { labelKey: K + 'tab.pure', icon: 'grid' });

  /* ---------- K2: (1) bảng phẳng các danh sách, mỗi nút là một ô; nút mới có viền, nút dùng chung đậm, nút bị đổi ngoài ý muốn gạch đỏ;
     (2) bảng độ sâu stack theo số phần tử đã đi qua (0 tới 50.000), mở từ bước 3. Ô giữ data-k để trượt khi đổi bước; không lặp. ---------- */
  ADE.registerScreen('fp.persist', function (box, ctx) {
    var h = ADE.ui.h, P = ADE.fpPersist, st = ctx.state, i = Math.max(0, idx(ctx)), v = P.view(st, i), L = v.list;
    var fmt = function (n) { return Number(n).toLocaleString(ADE.lang === 'vi' ? 'de-DE' : 'en-US'); };
    function chips(name, items) {
      return items.map(function (id, n) {
        var cls = 'vz-chip', sub = null;
        if (st.list === 'mutable') {
          if (name === 'booked' && id === L.added) { cls += ' bad'; sub = T('persist.chip.leak'); }
          if (name === 'selected' && id === L.added) cls += ' hl';
        } else if (name === 'selected' && n === 0) { cls += ' hl'; sub = T('persist.chip.new'); }
        else if (name !== 'booked') { cls += ' ok'; sub = T('persist.chip.shared'); }
        return h('span', { class: cls, 'data-k': 'ps-' + name + '-' + id }, h('span', { text: id }), sub ? h('small', { text: ' ' + sub }) : null);
      });
    }
    var rows = [['booked', L.booked], ['selected', L.selected]];
    if (L.rest) rows.push(['rest', L.rest]);
    var tb = h('tbody');
    rows.forEach(function (r) {
      var lostCell = st.list === 'mutable' && r[0] === 'booked' && L.lost ? [h('span', { class: 'vz-chip bad', 'data-k': 'ps-lost-' + L.lost }, h('span', { text: L.lost }), h('small', { text: ' ' + T('persist.chip.lost') }))] : [];
      tb.appendChild(h('tr', { 'data-k': 'ps-row-' + r[0] }, h('td', { text: r[0] }), h('td', { text: T('persist.ref.' + (st.list === 'mutable' && r[0] === 'selected' ? 'alias' : (r[0] === 'rest' ? 'tail' : r[0]))) }),
        h('td', null, lostCell.concat(chips(r[0], r[1])))));
    });
    var head = h('tr', null, h('th', { text: T('persist.col.seen') })), body = h('tr', { 'data-k': 'ps-depth-' + st.rec }, h('td', { text: T('persist.rec.' + st.rec) }));
    v.marks.forEach(function (x) {
      head.appendChild(h('th', { class: 'c', text: fmt(x[0]) }));
      var val = x[1], cls = 'c', txt;
      if (val === null) { cls += ' dim'; txt = '?'; }
      else if (val === 'crash') { cls += ' bad'; txt = T('persist.crash'); }
      else if (val === 'skip') { cls += ' dim'; txt = T('persist.skip'); }
      else { txt = fmt(val); if (val > P.LIMIT / 2) cls += ' bad'; else if (val === 1) cls += ' ok'; }
      body.appendChild(h('td', { class: cls, 'data-k': 'ps-m-' + x[0], text: txt }));
    });
    var result = v.crashed ? T('persist.result.crash', { n: fmt(P.LIMIT) }) : (v.total !== null ? T('persist.result.ok', { t: fmt(v.total) }) : T('persist.result.none'));
    box.appendChild(h('div', { class: 'vz' },
      h('p', { class: 'vz-cap', text: T('persist.cap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['name', 'ref', 'nodes'].map(function (k) { return h('th', { text: T('persist.col.' + k) }); }))), tb)),
      h('p', { class: 'vz-cap', text: T('persist.scap', { n: fmt(P.N), lim: fmt(P.LIMIT) }) }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), h('tbody', null, body))),
      h('p', { class: 'vz-sub' + (v.crashed ? ' bad' : ''), 'data-k': 'ps-result', text: result }),
      h('div', { class: 'vz-legend', text: T('persist.legend') })));
  }, { labelKey: K + 'tab.persist', icon: 'layers' });

  /* ---------- K3: (1) luồng dữ liệu: bốn hàm theo thứ tự chạy, kiểu vào → ra và giá trị sau mỗi hàm; cột "thứ tự đọc trong mã" lệch đỏ
     khi viết lồng nhau; (2) bảng bốn chỗ gọi: đối số (cấu hình lặp lại mờ, múi giờ sai đỏ) và chuỗi hiển thị, mở dần theo bước. ---------- */
  ADE.registerScreen('fp.compose', function (box, ctx) {
    var h = ADE.ui.h, P = ADE.fpCompose, c = ctx.state.case, i = Math.max(0, idx(ctx)), bad = c === 'nested';
    var READ = bad ? [4, 3, 2, 1] : [1, 2, 3, 4];
    var t1 = h('tbody');
    P.stages().forEach(function (x, n) {
      t1.appendChild(h('tr', { 'data-k': 'cp-st-' + x[0] }, h('td', { class: 'c', text: String(n + 1) }),
        h('td', { class: 'c' + (READ[n] !== n + 1 ? ' bad' : ' ok') + (i === 0 ? ' hl' : ''), text: String(READ[n]) }),
        h('td', { translate: 'no', text: x[0] }), h('td', { translate: 'no', text: x[1] + ' → ' + x[2] }), h('td', { translate: 'no', text: x[3] })));
    });
    var calls = P.calls(c), out = P.render(c), good = P.render('composed'), t2 = h('tbody');
    if (!bad) t2.appendChild(h('tr', { 'data-k': 'cp-site-build' }, h('td', { text: T('compose.site.build') }),
      h('td', null, ['VI', 'VND', 'CLINIC_ZONE'].map(function (a, k) { return h('span', { class: 'vz-chip' + (i < 1 ? ' dim' : (i === 3 ? ' hl' : ' ok')), 'data-k': 'cp-b-' + k, translate: 'no', text: i < 1 ? '?' : a }); })),
      h('td', { class: i < 1 ? 'dim' : '', text: i < 1 ? '?' : T('compose.build.out') })));
    calls.forEach(function (x, n) {
      var chips = x.args.map(function (a, k) {
        var cfg = k < x.config, wrong = cfg && a === 'UTC';
        var cls = 'vz-chip' + (i < 1 ? ' dim' : (wrong && i >= 2 ? ' bad' : (cfg ? (i === 3 ? ' hl' : ' dim') : ' ok')));
        return h('span', { class: cls, 'data-k': 'cp-a-' + x.site + '-' + k, translate: 'no', text: i < 1 ? '?' : a });
      });
      var res = i < 2 ? '?' : out[n], off = i >= 2 && out[n] !== good[n];
      t2.appendChild(h('tr', { 'data-k': 'cp-site-' + x.site }, h('td', { text: T('compose.site.' + x.site) }), h('td', null, chips),
        h('td', { class: (i < 2 ? 'dim' : (off ? 'bad' : '')), translate: 'no', text: res })));
    });
    var n = P.count(c), sub = i < 3 ? T('compose.edits.none') : T('compose.edits.' + c, { n: n.edits });
    box.appendChild(h('div', { class: 'vz' },
      h('p', { class: 'vz-cap', text: T('compose.cap.' + c) }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['run', 'read', 'fn', 'type', 'value'].map(function (k) { return h('th', { text: T('compose.col.' + k) }); }))), t1)),
      h('p', { class: 'vz-cap', text: T('compose.scap', { a: i >= 1 ? n.args : '?', r: i >= 1 ? n.repeated : '?' }) }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['site', 'args', 'out'].map(function (k) { return h('th', { text: T('compose.col.' + k) }); }))), t2)),
      h('p', { class: 'vz-sub', 'data-k': 'cp-edits', text: sub }),
      h('div', { class: 'vz-legend', text: T('compose.legend') })));
  }, { labelKey: K + 'tab.compose', icon: 'list' });

  /* ---------- K4: (1) bảng tính số dạng: nhân (product) hay cộng (sum); (2) ma trận mọi tổ hợp hay mọi kiểu con, nghĩa theo thiết kế màn
     và màn hình hiện gì (chạy chuỗi if hay when thật). Hàng của lỗi ở bước 3 và trạng thái mới ở bước 4 được viền; không lặp. ---------- */
  ADE.registerScreen('fp.adt', function (box, ctx) {
    var h = ADE.ui.h, A = ADE.fpAdt, c = ctx.state.case, i = Math.max(0, idx(ctx)), v = A.view(c, i), prod = c === 'product';
    var t1 = h('tbody'), parts;
    if (prod) parts = A.FIELDS.map(function (f) { return [f[0], f[0] === 'isLoading' ? 'Boolean' : (f[0] === 'error' ? 'String?' : 'List<Slot>?'), 2]; });
    else parts = v.rows.map(function (r) { return [r.v, r.v === 'Loading' ? 'data object' : 'data class', 1]; });
    parts.forEach(function (p) {
      var fresh = !prod && p[0] === 'Refreshing';
      t1.appendChild(h('tr', { 'data-k': 'adt-p-' + p[0] }, h('td', { class: fresh ? 'hl' : null, translate: 'no', text: p[0] }), h('td', { translate: 'no', text: p[1] }), h('td', { class: 'c', text: String(p[2]) })));
    });
    var expr = parts.map(function (p) { return p[2]; }).join(prod ? ' × ' : ' + ') + ' = ' + v.combos;
    t1.appendChild(h('tr', { 'data-k': 'adt-total' }, h('td', { class: prod ? 'bad' : 'ok', text: T('adt.total', { expr: expr }) }), h('td', null), h('td', { class: 'c ' + (prod ? 'bad' : 'ok'), text: String(v.combos) })));
    var t2 = h('tbody'), show = i >= 1;
    var same = function (a, b) { return a && b && a.l === b.l && a.e === b.e && a.d === b.d; };
    v.rows.forEach(function (r, n) {
      var label, mark, hit;
      if (prod) {
        label = [String(r.x.l), r.x.e ? '"…"' : 'null', r.x.d ? '[…]' : 'null'].map(function (t, k) { return h('span', { class: 'vz-chip' + (t === 'null' || t === 'false' ? ' dim' : ''), 'data-k': 'adt-v-' + n + '-' + k, translate: 'no', text: t }); });
        hit = (i === 2 && same(r.x, v.bug)) || (i === 3 && r.meaning === 'refresh');
      } else { label = [h('span', { class: 'vz-chip', translate: 'no', text: r.v })]; hit = (i === 2 && r.v === v.bug) || (i === 3 && r.v === 'Refreshing'); }
      var okMean = !!r.meaning, wrongUi = prod && r.meaning ? r.ui !== A.WANT[r.meaning] : false;
      mark = !show ? '?' : (okMean ? T('adt.mean.' + r.meaning) : T('adt.mean.none'));
      t2.appendChild(h('tr', { 'data-k': 'adt-r-' + (prod ? n : r.v) },
        h('td', { class: hit ? 'hl' : null }, label),
        h('td', { class: !show ? 'dim' : (okMean ? 'ok' : 'bad'), text: mark }),
        h('td', { class: !show ? 'dim' : ((!okMean && prod) || wrongUi || r.ui === 'crash' ? 'bad' : ''), text: !show ? '?' : T('adt.ui.' + r.ui) })));
    });
    var sub = i < 2 ? T('adt.sub.none') : (i === 2 ? T('adt.sub.bug.' + c) : T('adt.sub.v2.' + c, { n: A.SCREENS.length }));
    box.appendChild(h('div', { class: 'vz' },
      h('p', { class: 'vz-cap', text: T('adt.ccap.' + c) }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['part', 'type', 'count'].map(function (k) { return h('th', { text: T('adt.col.' + k) }); }))), t1)),
      h('p', { class: 'vz-cap', text: T('adt.mcap.' + c) }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, [prod ? 'combo' : 'variant', 'mean', 'ui'].map(function (k) { return h('th', { text: T('adt.col.' + k) }); }))), t2)),
      h('p', { class: 'vz-sub', 'data-k': 'adt-sub', text: sub }),
      h('div', { class: 'vz-legend', text: T('adt.legend') })));
  }, { labelKey: K + 'tab.adt', icon: 'grid' });

  /* ---------- K5: sơ đồ đường ray (SVG phẳng): đường thành công ở trên, đường lỗi ở dưới, bốn ga là bốn bước, màn hình ở cuối.
     Vệt màu là đường giá trị đã đi: chạy trên đường thành công, tới ga hỏng thì rẽ xuống đường lỗi và chạy thẳng tới màn hình;
     lỗi không ai bắt thì vệt dừng ở ga đó (crash). Vệt luôn có 6 điểm nên khi đổi bước nó uốn từ hình cũ sang hình mới; ga đổi lớp thì nháy. ---------- */
  var esc = function (x) { return String(x).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); };
  var fit = function (str, w) { return String(str).length * 6.4 > w ? ' textLength="' + w + '" lengthAdjust="spacingAndGlyphs"' : ''; };
  ADE.registerScreen('fp.errors', function (box, ctx) {
    var h = ADE.ui.h, P = ADE.fpErrors, c = ctx.state.case, i = Math.max(0, idx(ctx)), scen = P.SCEN[i], r = P.run(c, scen);
    var YT = 62, YE = 162, X = [118, 236, 354, 472], X0 = 22, XS = 560;
    var fn = function (st) { return st === 'parse' ? 'parsePhone' : (st === 'slot' ? 'findFreeSlot' : (st === 'quota' ? (c === 'throw' || c === 'result' ? 'checkQuota' : 'quotaLeft') : 'save')); };
    var failAt = -1, crash = false;
    r.rows.forEach(function (x, n) { if (x.rail === 'err' || x.rail === 'crash') { failAt = n; crash = x.rail === 'crash'; } });
    // 6 điểm của vệt: điểm đầu, bốn ga, điểm vào màn hình
    var pts = [[X0, YT]].concat(X.map(function (x, n) {
      if (failAt < 0 || n <= failAt) return [x, YT];
      return crash ? [X[failAt], YT] : [x, YE];
    }));
    pts.push(failAt < 0 ? [XS, YT] : (crash ? [X[failAt], YT] : [XS, YE]));
    var tok = pts[pts.length - 1], kind = failAt < 0 ? 'ok' : (crash ? 'crash' : 'err');
    var svg = '<svg class="vz-dg vz-rl" viewBox="0 0 640 212" role="img" aria-label="' + esc(T('errors.aria', { n: r.ran, s: T('errors.out.' + r.screen) })) + '">';
    svg += '<line class="vz-rl-track" x1="' + X0 + '" y1="' + YT + '" x2="' + XS + '" y2="' + YT + '"/>';
    svg += '<line class="vz-rl-track err" x1="' + X0 + '" y1="' + YE + '" x2="' + XS + '" y2="' + YE + '"/>';
    svg += '<text class="vz-rl-tl" x="' + X0 + '" y="' + (YT - 42) + '">' + esc(T('errors.col.ok')) + '</text>';
    svg += '<text class="vz-rl-tl err" x="' + X0 + '" y="' + (YE + 34) + '">' + esc(T('errors.col.err')) + '</text>';
    svg += '<polyline class="vz-rl-path ' + kind + '" data-k="er-path" points="' + pts.map(function (q) { return q[0] + ',' + q[1]; }).join(' ') + '"/>';
    r.rows.forEach(function (x, n) {
      var st = x.rail === 'ok' ? 'ok' : (x.rail === 'skip' ? 'skip' : (x.rail === 'crash' ? 'crash' : 'fail'));
      svg += '<g class="vz-rl-g ' + st + '" data-k="er-st-' + x.step + '">';
      svg += '<text class="vz-dg-t" x="' + X[n] + '" y="' + (YT - 16) + '" text-anchor="middle">' + esc(fn(x.step)) + '</text>';
      svg += '<circle class="vz-rl-st" cx="' + X[n] + '" cy="' + YT + '" r="9"/>';
      if (x.rail === 'ok') svg += '<text class="vz-dg-s" x="' + X[n] + '" y="' + (YT + 26) + '" text-anchor="middle"' + fit(x.val, 112) + '>' + esc(x.val) + '</text>';
      else if (x.rail === 'skip') svg += '<text class="vz-dg-s vz-rl-skip" x="' + X[n] + '" y="' + (YT + 26) + '" text-anchor="middle">' + esc(T('errors.skip')) + '</text>';
      else if (x.rail === 'crash') svg += '<text class="vz-dg-badt" x="' + X[n] + '" y="' + (YT + 50) + '" text-anchor="middle"' + fit(T('errors.crash', { v: x.val }), 210) + '>' + esc(T('errors.crash', { v: x.val })) + '</text>';
      svg += '</g>';
    });
    if (failAt >= 0 && !crash) {
      var ex = X[failAt] + 14, ev = r.rows[failAt].val;
      svg += '<text class="vz-rl-errv" data-k="er-errv" x="' + ex + '" y="' + (YE + 18) + '"' + fit(ev, XS - ex - 8) + '>' + esc(ev) + '</text>';
    }
    svg += '<g class="vz-rl-scr' + (r.screen === 'failed' || r.screen === 'crash' ? ' bad' : '') + '"><rect x="' + XS + '" y="' + (YT - 26) + '" width="70" height="' + (YE - YT + 52) + '" rx="6"/>' +
      '<text class="vz-dg-t" x="' + (XS + 35) + '" y="' + ((YT + YE) / 2 + 4) + '" text-anchor="middle">' + esc(T('errors.scr')) + '</text></g>';
    svg += '<circle class="vz-rl-tok ' + kind + '" data-k="er-tok" cx="' + tok[0] + '" cy="' + tok[1] + '" r="7"/>';
    svg += '</svg>';
    var bad = r.screen === 'failed' || r.screen === 'crash', wrap = h('div', { class: 'vz-scroll' });
    wrap.innerHTML = svg;
    box.appendChild(h('div', { class: 'vz' },
      h('p', { class: 'vz-cap', 'data-k': 'er-in', text: T('errors.in.' + scen) }),
      wrap,
      h('p', { class: 'vz-sub', 'data-k': 'er-sig', translate: 'no', text: 'fun book(raw: String, slotId: String): ' + P.SIG[c] }),
      h('p', { class: 'vz-sub' + (bad ? ' bad' : ''), 'data-k': 'er-screen', text: T('errors.screen', { s: T('errors.out.' + r.screen) }) }),
      h('div', { class: 'vz-legend', text: T('errors.legend') })));
  }, { labelKey: K + 'tab.errors', icon: 'rail' });

  /* ---------- K6: hộp và giá trị (SVG phẳng): hộp ban đầu bên trái, ba nhánh map(f), map(g), flatMap(g) bên phải.
     Mỗi tầng hộp là một khung; hộp trong hộp vẽ hai khung lồng (chính là khái niệm cần thấy). Nhánh mở dần theo bước;
     bước 4 thêm dòng chuỗi nhiều bước. Khung đổi lớp thì nháy; số tầng ở dòng dưới chạy số. ---------- */
  ADE.registerScreen('fp.monad', function (box, ctx) {
    var h = ADE.ui.h, P = ADE.fpMonad, c = ctx.state.case, i = Math.max(0, idx(ctx)), v = P.view(c, i), cells = v.cells;
    var BX = 14, BY = 88, BW = 170, BH = 66, RX = 330, RW = 296, RH = 58, RY = [14, 96, 178], OPS = ['map(f)', 'map(g)', 'flatMap(g)'];
    function boxes(x, y, w, hh, cell, k) {
      var s = '', d = Math.max(1, cell.depth), cls = !cell.open ? ' skip' : (d > 1 ? ' bad' : (k === i + 1 ? ' on' : ''));
      s += '<g class="vz-mn' + cls + '" data-k="mn-b-' + k + '">';
      for (var n = 0; n < d; n++) s += '<rect x="' + (x + n * 6) + '" y="' + (y + n * 6) + '" width="' + (w - n * 12) + '" height="' + (hh - n * 12) + '" rx="5"/>';
      var tx = x + 8 + (d - 1) * 6, tw = w - 16 - (d - 1) * 12;
      s += '<text class="vz-dg-s" x="' + tx + '" y="' + (y + 17 + (d - 1) * 6) + '"' + fit(cell.type, tw) + '>' + esc(cell.open ? cell.type : '') + '</text>';
      s += '<text class="vz-dg-t" x="' + tx + '" y="' + (y + hh - 13 - (d - 1) * 6) + '"' + fit(cell.open ? cell.val : '?', tw) + '>' + esc(cell.open ? cell.val : '?') + '</text>';
      return s + '</g>';
    }
    var svg = '<svg class="vz-dg vz-mnsvg" viewBox="0 0 640 252" role="img" aria-label="' + esc(T('monad.aria', { n: v.nest })) + '">';
    svg += boxes(BX, BY, BW, BH, cells[0], 0);
    RY.forEach(function (y, n) {
      var open = cells[n + 1].open, x1 = BX + BW, y1 = BY + BH / 2, x2 = RX, y2 = y + RH / 2;
      svg += '<line class="vz-dg-e' + (open ? ' up' : '') + '" data-k="mn-e-' + n + '" x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '"/>';
      svg += '<text class="vz-mn-op' + (open ? '' : ' off') + '" x="' + (x2 - 6) + '" y="' + (y2 > y1 + 20 ? y2 + 18 : y2 - 8) + '" text-anchor="end">' + OPS[n] + '</text>';
      svg += boxes(RX, y, RW, RH, cells[n + 1], n + 1);
    });
    svg += '</svg>';
    var wrap = h('div', { class: 'vz-scroll' }); wrap.innerHTML = svg;
    var ch = cells[4];
    box.appendChild(h('div', { class: 'vz' },
      h('p', { class: 'vz-cap', text: T('monad.fg.' + c) }),
      wrap,
      h('p', { class: 'vz-sub' + (v.nest > 1 ? ' bad' : ''), 'data-k': 'mn-nest', text: T('monad.nest', { n: v.nest }) }),
      h('p', { class: 'vz-sub', 'data-k': 'mn-chain', text: ch.open ? T('monad.chain.' + c) + ' → ' + ch.val + ' : ' + ch.type : T('monad.chain.none') }),
      h('div', { class: 'vz-legend', text: T('monad.legend') })));
  }, { labelKey: K + 'tab.monad', icon: 'layers' });

  /* ---------- K7: các ô của form và lỗi (bảng phẳng): mỗi hàng một ô của form đăng ký, giá trị ở lần nộp này, ô đó có được kiểm không,
     và lỗi người dùng thấy. Dừng sớm: các ô sau lỗi đầu tiên mờ "chưa kiểm". Gom lỗi: mọi ô được kiểm; bước 2 thêm dòng gộp lỗi bằng nối list.
     Hàng giữ data-k nên giá trị mới (người dùng đã sửa) nháy khi đổi bước; không lặp. ---------- */
  ADE.registerScreen('fp.validate', function (box, ctx) {
    var h = ADE.ui.h, P = ADE.fpValidate, c = ctx.state.case, i = Math.max(0, idx(ctx)), v = P.view(c, i);
    var tb = h('tbody');
    v.rows.forEach(function (r) {
      var stCls = r.st === 'err' ? 'bad' : (r.st === 'ok' ? 'ok' : 'dim');
      tb.appendChild(h('tr', { 'data-k': 'vd-' + r.f },
        h('td', { text: T('validate.f.' + r.f) }),
        h('td', { translate: 'no', 'data-k': 'vd-v-' + r.f, text: r.v === '' ? '""' : r.v }),
        h('td', { class: 'c ' + stCls, text: T('validate.st.' + r.st) }),
        h('td', { class: r.err ? 'bad' : 'dim', text: r.err ? T('validate.e.' + r.err) : '—' })));
    });
    if (c === 'acc' && i === 3) tb.appendChild(h('tr', { 'data-k': 'vd-dep' }, h('td', { text: T('validate.f.dep') }), h('td', { translate: 'no', text: v.rows[1].v }),
      h('td', { class: 'c ' + (v.extra ? 'bad' : 'ok'), text: T('validate.st.' + (v.extra ? 'err' : 'ok')) }), h('td', { class: v.extra ? 'bad' : 'dim', text: v.extra ? T('validate.e.' + v.extra) : '—' })));
    var res = v.result === 'ok' ? T('validate.res.ok') : (v.result === 'taken' ? T('validate.res.taken') : T('validate.res.err', { n: v.errs.length }));
    box.appendChild(h('div', { class: 'vz' },
      h('p', { class: 'vz-cap', 'data-k': 'vd-sub', text: T('validate.cap.' + c, { n: v.submit }) }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['field', 'value', 'checked', 'error'].map(function (k) { return h('th', { text: T('validate.col.' + k) }); }))), tb)),
      v.combine ? h('p', { class: 'vz-sub', 'data-k': 'vd-comb', translate: 'no', text: v.errs.map(function (e) { return '[' + e + ']'; }).join(' + ') + ' = [' + v.errs.join(', ') + ']' }) : null,
      h('p', { class: 'vz-sub' + (v.result === 'ok' ? '' : ' bad'), 'data-k': 'vd-res', text: res }),
      h('p', { class: 'vz-sub', 'data-k': 'vd-total', text: c === 'fast' ? T('validate.total.fast', { n: v.total }) : T('validate.total.acc', { n: v.total }) }),
      h('div', { class: 'vz-legend', text: T('validate.legend') })));
  }, { labelKey: K + 'tab.validate', icon: 'list' });
})();
