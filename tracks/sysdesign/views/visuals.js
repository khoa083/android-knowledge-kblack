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
})();
