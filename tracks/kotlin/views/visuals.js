/* Hình trực quan theo bước của track F (ADE.registerScreen với nhãn tab riêng). Dùng khi pipeline bốn khối không phải hình tự nhiên
   của nội dung: bảng bucket (K4), bảng từng phần tử (K9), ma trận gán (K10), hộp receiver lồng nhau (K12), bảng tra (K0).
   Sơ đồ node vẫn ở tab bên cạnh. Mọi số liệu lấy từ dữ liệu model (ADE.kotlin*), không tính lại theo cách khác. */
(function () {
  'use strict';
  var K = 'track.kotlin.vz.';
  var T = function (k, p) { return ADE.t(K + k, p); };
  var KS = ['start', 'first', 'next', 'end'];
  // vị trí bước: -1 = trang tổng quan, 0..3 = bước, 4 = tổng kết (giữ hình của bước cuối)
  function idx(ctx) {
    if (ctx.step) return KS.indexOf(ctx.step.id.split('.').pop());
    return ctx.pos > ctx.N ? 3 : -1;
  }
  function wrap(cap, body, legend) {
    var h = ADE.ui.h;
    return h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: cap }), h('div', { class: 'vz-scroll' }, body), legend ? h('div', { class: 'vz-legend', text: legend }) : null);
  }
  function td(text, cls) { return ADE.ui.h('td', { class: cls || null, text: text }); }

  /* ---------- K4: bảng bucket của HashSet ---------- */
  ADE.registerScreen('kotlin.hashset', function (box, ctx) {
    var h = ADE.ui.h, c = ctx.state.case, i = idx(ctx), B = ADE.kotlinBucket;
    var b1 = B('Lan|Nguyen'), b2 = B('Lan|Tran'), bp = B('P01');
    var rows = [[], [], [], []], look = null, lookOk = null, note = null;
    var chip = function (t, bad) { return h('span', { class: 'vz-chip' + (bad ? ' bad' : ''), text: t }); };
    if (c === 'mutate') {
      if (i === 1) rows[b1].push(chip('Lan Nguyen'));
      if (i >= 2) { rows[b1].push(chip('Lan Tran', true)); note = T('hash.newHash', { b: b2 }); }
      if (i === 3) { look = b2; lookOk = false; }
    } else if (c === 'copy') {
      if (i === 1) rows[b1].push(chip('Lan Nguyen'));
      if (i >= 2) { rows[b2].push(chip('Lan Tran · ' + T('hash.copy'))); note = T('hash.moved', { a: b1, b: b2 }); }
      if (i === 3) { look = b2; lookOk = true; }
    } else if (c === 'bodyProp') {
      if (i >= 1) note = T('hash.idOnly', { b: bp });
      if (i === 2) { look = bp; lookOk = true; rows[bp].push(chip('P01 (a)')); }
      if (i === 3) { rows[bp].push(chip('P01 (a)')); note = T('hash.bodyNote'); }
      if (i === 2) note = T('hash.bodyEq');
    } else {
      if (i >= 1) note = T('hash.plainNote');
      if (i === 3) { rows[0].push(chip('P01 (a)')); rows[2].push(chip('P01 (b)')); }
    }
    var tb = h('tbody');
    rows.forEach(function (r, n) {
      var cls = look === n ? (lookOk ? 'hl' : 'hl bad') : null;
      tb.appendChild(h('tr', null, td(String(n), 'c' + (cls ? ' ' + cls : '')), h('td', { class: cls }, r.length ? r : (look === n ? T('hash.empty') : '·'))));
    });
    var tbl = h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, h('th', { text: T('hash.colBucket') }), h('th', { text: T('hash.colItems') }))), tb);
    var foot = [];
    if (look !== null) foot.push(h('p', { class: 'vz-cap', text: T('hash.look', { b: look }) + ' → ' + T(lookOk ? 'hash.found' : 'hash.notFound') }));
    if (note) foot.push(h('p', { class: 'vz-cap', text: note }));
    box.appendChild(wrap(T('hash.cap'), h('div', null, tbl, foot), null));
  }, { labelKey: K + 'tab.hash', icon: 'grid' });

  /* ---------- K9: bảng từng phần tử qua filter / map / take ---------- */
  ADE.registerScreen('kotlin.sequence', function (box, ctx) {
    var h = ADE.ui.h, c = ctx.state.case, i = idx(ctx), H = ADE.kotlinSeq.HOURS;
    // ô[r] = {f: thứ tự lần chạy filter | null, fok, m: thứ tự lần chạy map | null, t: 'keep' | 'drop' | 'unread' | 'sent' | null}
    var cell = H.map(function () { return { f: null, m: null, t: null }; }), run = 0, upto;
    if (c === 'list') {
      if (i >= 1) H.forEach(function (x, r) { cell[r].f = ++run; cell[r].fok = x < 12; });
      if (i >= 2) H.forEach(function (x, r) { if (x < 12) cell[r].m = ++run; });
      if (i >= 3) { var got = 0; H.forEach(function (x, r) { if (x < 12) cell[r].t = got++ < 2 ? 'keep' : 'drop'; }); }
    } else if (c === 'sequence') {
      upto = i <= 0 ? 0 : i === 1 ? 1 : i === 2 ? 2 : 3;   // số phần tử gốc đã đọc tới bước này
      var kept = 0;
      for (var r = 0; r < H.length; r++) {
        if (r >= upto) { if (i >= 3) cell[r].t = 'unread'; continue; }
        cell[r].f = ++run; cell[r].fok = H[r] < 12;
        if (H[r] < 12) { cell[r].m = ++run; cell[r].t = kept++ < 2 ? 'keep' : null; }
      }
    } else {
      if (i >= 3) H.forEach(function (x, r) { cell[r].f = ++run; cell[r].fok = x < 12; if (x < 12) { cell[r].m = ++run; cell[r].t = 'sent'; } });
    }
    var tb = h('tbody');
    H.forEach(function (x, r) {
      var e = cell[r];
      tb.appendChild(h('tr', { class: e.t === 'unread' ? 'dim' : null },
        td(x + 'h', 'c'),
        td(e.f ? '#' + e.f + (e.fok ? ' ✓' : ' ✗') : (c === 'noTerminal' && i < 3 && i >= 1 ? T('seq.notRun') : '·'), e.f ? (e.fok ? 'c ok' : 'c dim') : 'c dim'),
        td(e.m ? '#' + e.m : '·', e.m ? 'c ok' : 'c dim'),
        td(e.t ? T('seq.' + e.t) : '·', e.t === 'keep' || e.t === 'sent' ? 'c ok' : (e.t === 'drop' ? 'c bad' : 'c dim'))));
    });
    var tbl = h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, h('th', { text: T('seq.colHour') }), h('th', { text: T('seq.colFilter') }), h('th', { text: T('seq.colMap') }), h('th', { text: T(c === 'noTerminal' ? 'seq.colEach' : 'seq.colTake') }))), tb);
    box.appendChild(wrap(T('seq.cap.' + c), tbl, T('seq.legend', { n: run })));
  }, { labelKey: K + 'tab.seq', icon: 'list' });

  /* ---------- K10: ma trận gán out / in / bất biến ---------- */
  ADE.registerScreen('kotlin.variance', function (box, ctx) {
    var h = ADE.ui.h, c = ctx.state.case, i = idx(ctx);
    var R = [['outList', 'List<out E>', 'ok', 'err', 'out'], ['invariantMutable', 'MutableList<E>', 'err', 'err', 'inv'], ['inNotifier', 'Notifier<in T>', 'err', 'ok', 'in']];
    // ô đang được kiểm ở bước hiện tại: [cột 1 = Doctor→Staff, 2 = Staff→Doctor]
    var col = i < 1 ? 0 : (c === 'inNotifier' ? (i === 3 ? 1 : 2) : 1);
    var tb = h('tbody');
    R.forEach(function (r) {
      var cur = r[0] === c;
      var cellOf = function (k, n) { var cls = 'c ' + (k === 'ok' ? 'ok' : 'bad'); if (cur && col === n) cls += ' hl'; return td(T('var.' + k), cls); };
      tb.appendChild(h('tr', null, h('td', { class: cur ? 'hl' : null }, h('code', { text: r[1] })), cellOf(r[2], 1), cellOf(r[3], 2), td(T('var.why.' + r[4]), cur ? 'hl' : null)));
    });
    var tbl = h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, h('th', { text: T('var.colType') }), h('th', { text: T('var.colUp') }), h('th', { text: T('var.colDown') }), h('th', { text: T('var.colWhy') }))), tb);
    var foot = c === 'invariantMutable' && i === 3 ? h('p', { class: 'vz-cap', text: T('var.copyNote') }) : null;
    box.appendChild(wrap(T('var.cap'), h('div', null, tbl, foot), null));
  }, { labelKey: K + 'tab.var', icon: 'grid' });

  /* ---------- K12: hộp receiver lồng nhau ---------- */
  ADE.registerScreen('kotlin.scope', function (box, ctx) {
    var h = ADE.ui.h, c = ctx.state.case, i = idx(ctx), P = 'scope.' + c + '.';
    // hit: hộp được dùng cho tên ở bước này; 'outer' | 'inner' | 'none' | null
    var hit = { nestedApply: [null, 'outer', 'outer', 'inner'], letElvis: [null, 'inner', 'outer', 'none'], dslMarker: [null, 'inner', 'outer', 'none'] }[c][Math.max(i, 0)];
    if (i < 0) hit = null;
    var bad = i === 2;
    var inner = h('div', { class: 'vz-box' + (hit === 'inner' ? ' hl' : '') }, h('div', { class: 'vz-h', text: T(P + (i === 3 ? 'innerFix' : 'inner')) }), h('div', { text: T(P + 'innerMembers') }));
    var outer = h('div', { class: 'vz-box' + (hit === 'outer' ? (bad ? ' hl bad' : ' hl') : '') }, h('div', { class: 'vz-h', text: T(P + (i === 3 ? 'outerFix' : 'outer')) }), h('div', { text: T(P + 'outerMembers') }), inner);
    var line = i >= 1 ? h('p', { class: 'vz-cap', text: T(P + 'name') + ' → ' + T(P + 'res' + i) }) : null;
    box.appendChild(wrap(T('scope.cap'), h('div', { class: 'vz' }, outer, line), T('scope.legend')));
  }, { labelKey: K + 'tab.scope', icon: 'layers' });

  /* ---------- K0: bảng tra triệu chứng → lúc lộ ra → chương ---------- */
  ADE.registerScreen('kotlin.map', function (box, ctx) {
    var h = ADE.ui.h, cur = ctx.state.symptom, i = idx(ctx), M = 'track.kotlin.m.map.';
    var tb = h('tbody');
    ADE.kotlinMap.forEach(function (r) {
      var on = r[0] === cur;
      tb.appendChild(h('tr', { class: on ? 'hl' : null },
        td(ADE.t(M + 's.' + r[0] + '.title'), on ? 'hl' : null),
        td(on && i < 1 ? '?' : ADE.t(M + 'phase.' + r[2]), (on ? 'hl ' : '') + (r[2] === 'silent' ? 'bad' : '')),
        td(on && i < 3 ? '?' : r[1].toUpperCase(), 'c' + (on ? ' hl ok' : ''))));
    });
    var tbl = h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, h('th', { text: T('map.colSym') }), h('th', { text: T('map.colPhase') }), h('th', { text: T('map.colCh') }))), tb);
    box.appendChild(wrap(T('map.cap'), tbl, null));
  }, { labelKey: K + 'tab.map', icon: 'search' });
})();
