/* Hình trực quan theo bước của track J (ADE.registerScreen với nhãn tab riêng). Sơ đồ node vẫn ở tab bên cạnh. */
(function () {
  'use strict';
  var K = 'track.cleancode.vz.';
  var T = function (k, p) { return ADE.t(K + k, p); };
  var KS = ['s1', 's2', 's3', 's4'];
  function idx(ctx) {
    if (ctx.step) return KS.indexOf(ctx.step.id.split('.').pop());
    return ctx.pos > ctx.N ? 3 : 0;
  }

  /* ---------- J1: hai hàng ô "bộ nhớ làm việc" (đường đi, biến) với vạch ngưỡng 7; bảng đếm cyclomatic complexity ----------
     Hàng ô phẳng, không lồng hộp. Mỗi ô có data-k: khi đổi hàm, ô cùng tên TRƯỢT tới chỗ mới (ui.labMotion, FLIP);
     ô mới hiện dần một lần; không có chuyển động lặp. */
  ADE.registerScreen('cleancode.fits', function (box, ctx) {
    var h = ADE.ui.h, J = ADE.ccFits, c = ctx.state.case, i = Math.max(0, idx(ctx)), v = J.view(c, i);
    // hàng trên: đúng 7 ô (ngưỡng); hàng dưới chỉ có khi vượt: nhãn "vượt ngưỡng 7" rồi các ô đỏ
    function chip(it, over) {
      if (!it) return h('span', { class: 'vz-chip dim vz-slot', 'aria-hidden': 'true', text: T('fits.empty') });
      return h('span', { class: 'vz-chip vz-slot' + (over ? ' bad' : '') + (it.fresh ? ' hl' : ''), 'data-k': it.k }, h('span', { text: it.text }), it.sub ? h('small', { text: it.sub }) : null);
    }
    function slotRow(label, items) {
      var inside = [], extra = items.slice(J.LIMIT);
      for (var x = 0; x < J.LIMIT; x++) inside.push(chip(items[x], false));
      return h('div', { class: 'vz-slotrow' }, h('div', { class: 'vz-slot-l' + (extra.length ? ' bad' : ''), text: label }), h('div', { class: 'vz-slots' }, inside),
        extra.length ? h('div', { class: 'vz-slots' }, [h('span', { class: 'vz-limit', text: T('fits.limit') })].concat(extra.map(function (it) { return chip(it, true); }))) : null);
    }
    var pathItems = [{ k: 'p-start', text: T('fits.start') }].concat(v.br.map(function (b) { return { k: 'p' + b[0], text: 'L' + b[0] + ' ' + b[1], fresh: v.isNew(b[0]) }; }));
    var varItems = v.vars.map(function (x) { return { k: 'v-' + x[0], text: x[0], sub: T('fits.kind.' + x[1]), fresh: v.isNew(x[2]) }; });
    var overLines = v.lines > J.SEEMANN_LINES;

    // bảng đếm: mỗi hàm bắt đầu từ 1, mỗi if/for cộng 1; hàng mới (vừa đọc) có viền
    var tb = h('tbody');
    J.tableFns(c, i).forEach(function (f) {
      var fn = J.FN[f], cur = f === v.step.f, upTo = cur ? v.step.upTo : fn.to, sum = 1;
      tb.appendChild(h('tr', { 'data-k': 'r-' + fn.name + '-start' }, h('td', { text: fn.name }), h('td', { class: 'c dim', text: String(fn.from) }), h('td', { class: 'dim', text: T('fits.what.start') }), h('td', { class: 'c', text: '1' })));
      fn.br.filter(function (b) { return b[0] <= upTo; }).forEach(function (b) {
        sum++;
        var fresh = cur && v.isNew(b[0]);
        tb.appendChild(h('tr', { 'data-k': 'r-' + fn.name + '-' + b[1] + '-' + sum }, h('td', { 'aria-label': fn.name }), h('td', { class: 'c' + (fresh ? ' hl' : ''), text: String(b[0]) }),
          h('td', { class: fresh ? 'hl' : null, text: T('fits.what.' + b[1]) }), h('td', { class: 'c' + (sum > J.LIMIT ? ' bad' : (fresh ? ' hl' : '')), text: String(sum) })));
      });
    });
    var head = h('tr', null, ['fn', 'line', 'what', 'sum'].map(function (k) { return h('th', { text: T('fits.col.' + k) }); }));

    var out = [h('p', { class: 'vz-cap', text: T('fits.cap', { fn: v.fn.name }) }),
      slotRow(T('fits.row.paths', { n: v.paths }), pathItems),
      slotRow(T('fits.row.vars', { n: v.nVars }), varItems),
      h('p', { class: 'vz-note' + (overLines ? ' bad' : ''), text: T('fits.lines', { n: v.lines, verdict: T(overLines ? 'fits.lines.over' : 'fits.lines.ok') }) })];
    if (i === 3) out.push(h('p', { class: 'vz-note ' + (v.step.skip ? 'bad' : 'ok'), text: T(v.step.skip ? 'fits.skipped' : 'fits.kept', { line: v.fn.remind || J.FN.book.remind }) }));
    out.push(h('p', { class: 'vz-cap', text: T('fits.tcap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), tb)),
      h('div', { class: 'vz-legend', text: T('fits.legend') }));
    box.appendChild(h('div', { class: 'vz' }, out));
  }, { labelKey: K + 'tab.fits', icon: 'grid' });

  /* ---------- J2: bảng đối chiếu (chữ ký che tên → đoán → tên → việc thật → đọc hay ghi), cột mở dần theo bước;
     bước 4 thêm bảng hai lần gọi khi mất mạng. Hàng có data-k; cột mới mở hiện dần một lần. ---------- */
  ADE.registerScreen('cleancode.names', function (box, ctx) {
    var h = ADE.ui.h, J = ADE.ccNames, c = ctx.state.case, i = Math.max(0, idx(ctx));
    var cols = ['sig', 'guess', 'name', 'does', 'kind'], open = [1, 1, i >= 1, i >= 2, i >= 2], fresh = [i === 0, i === 0, i === 1, i === 2, i === 2];
    var head = h('tr', null, cols.map(function (k, n) { return h('th', { class: fresh[n] && i > 0 ? 'hl' : null, text: T('nm.col.' + k) }); }));
    var tb = h('tbody');
    J.ROWS[c].forEach(function (r) {
      var ok = J.right(r), kindKey = r[5];
      var cell = function (n, text, extra) { return h('td', { class: !open[n] ? 'dim c' : (extra || (fresh[n] && i > 0 ? 'hl' : null)), text: open[n] ? text : '?' }); };
      tb.appendChild(h('tr', { 'data-k': 'nm-' + r[0] },
        h('td', null, h('code', { text: r[1] })),
        cell(1, T('nm.g.' + r[2]), i >= 2 && !ok ? 'bad' : null),
        cell(2, r[3], null),
        cell(3, T('nm.d.' + r[4]), i >= 2 && !ok ? 'bad' : null),
        cell(4, T('nm.k.' + kindKey), i >= 2 ? (ok ? 'ok' : 'bad') : null)));
    });
    var out = [h('p', { class: 'vz-cap', text: T('nm.cap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), tb))];
    if (i === 3) {
      var cb = h('tbody');
      J.CALLS[c].forEach(function (x, n) {
        cb.appendChild(h('tr', { 'data-k': 'call' + n }, h('td', { text: T('nm.call.' + (n + 1)) }), h('td', { class: 'c ' + (x[0] === 0 ? 'bad' : 'ok'), text: T('nm.ret', { n: x[0] }) }), h('td', { class: 'c' + (x[1] === 0 ? ' bad' : ''), text: T('nm.cacheN', { n: x[1] }) })));
      });
      out.push(h('p', { class: 'vz-cap', text: T('nm.tcap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['call', 'ret', 'cache'].map(function (k) { return h('th', { text: T('nm.tcol.' + k) }); }))), cb)));
    }
    out.push(h('div', { class: 'vz-legend', text: T('nm.legend') }));
    box.appendChild(h('div', { class: 'vz' }, out));
  }, { labelKey: K + 'tab.names', icon: 'list' });
})();
