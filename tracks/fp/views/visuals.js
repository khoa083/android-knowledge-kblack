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
})();
