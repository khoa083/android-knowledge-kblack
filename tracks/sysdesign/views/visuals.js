/* Hình trực quan theo bước của track I (ADE.registerScreen với nhãn tab riêng). Sơ đồ node vẫn ở tab bên cạnh. */
(function () {
  'use strict';
  var K = 'track.sysdesign.vz.';
  var T = function (k, p) { return ADE.t(K + k, p); };
  var KS = ['s1', 's2', 's3', 's4'];
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
})();
