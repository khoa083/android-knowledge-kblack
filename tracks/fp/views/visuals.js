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

  /* ---------- K5: đường ray: mỗi hàng là một bước của luồng đặt lịch, hai cột là đường thành công và đường lỗi.
     Bước hỏng đặt giá trị lỗi sang cột lỗi; các bước sau mờ "bỏ qua"; lỗi không ai bắt tô đỏ "crash".
     Dưới bảng: chữ ký hàm của cách viết đang chọn và điều màn hình hiện. Ô giữ data-k để trượt và nháy khi đổi bước; không lặp. ---------- */
  ADE.registerScreen('fp.errors', function (box, ctx) {
    var h = ADE.ui.h, P = ADE.fpErrors, c = ctx.state.case, i = Math.max(0, idx(ctx)), scen = P.SCEN[i], r = P.run(c, scen);
    var tb = h('tbody');
    r.rows.forEach(function (x, n) {
      var okCell, errCell;
      if (x.rail === 'ok') { okCell = h('span', { class: 'vz-chip ok', 'data-k': 'er-v-' + x.step, translate: 'no', text: x.val }); errCell = null; }
      else if (x.rail === 'skip') { okCell = h('span', { class: 'vz-chip dim', 'data-k': 'er-v-' + x.step, text: T('errors.skip') }); errCell = h('span', { class: 'vz-chip dim', text: T('errors.skip') }); }
      else { okCell = null; errCell = h('span', { class: 'vz-chip ' + (x.rail === 'crash' ? 'bad' : 'hl'), 'data-k': 'er-v-' + x.step, translate: 'no', text: x.rail === 'crash' ? T('errors.crash', { v: x.val }) : x.val }); }
      tb.appendChild(h('tr', { 'data-k': 'er-row-' + x.step },
        h('td', { class: 'c', text: String(n + 1) }),
        h('td', { translate: 'no', text: x.step === 'parse' ? 'parsePhone' : (x.step === 'slot' ? 'findFreeSlot' : (x.step === 'quota' ? (c === 'throw' || c === 'result' ? 'checkQuota' : 'quotaLeft') : 'save')) }),
        h('td', { class: x.rail === 'ok' ? 'ok' : (x.rail === 'skip' ? 'dim' : '') }, okCell),
        h('td', { class: x.rail === 'crash' ? 'bad' : (x.rail === 'skip' ? 'dim' : '') }, errCell)));
    });
    var bad = r.screen === 'failed' || r.screen === 'crash';
    box.appendChild(h('div', { class: 'vz' },
      h('p', { class: 'vz-cap', 'data-k': 'er-in', text: T('errors.in.' + scen) }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['n', 'fn', 'ok', 'err'].map(function (k) { return h('th', { text: T('errors.col.' + k) }); }))), tb)),
      h('p', { class: 'vz-sub', 'data-k': 'er-sig', translate: 'no', text: 'fun book(raw: String, slotId: String): ' + P.SIG[c] }),
      h('p', { class: 'vz-sub' + (bad ? ' bad' : ''), 'data-k': 'er-screen', text: T('errors.screen', { s: T('errors.out.' + r.screen) }) }),
      h('div', { class: 'vz-legend', text: T('errors.legend') })));
  }, { labelKey: K + 'tab.errors', icon: 'rail' });
})();
