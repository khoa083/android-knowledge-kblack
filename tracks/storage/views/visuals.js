/* Hình trực quan theo bước của track H (ADE.registerScreen với nhãn tab riêng). Sơ đồ node vẫn ở tab bên cạnh.
   H1: CÂY QUYẾT ĐỊNH dạng bậc thang (mỗi câu "có" rẽ sang một lá, "không" đi xuống câu tiếp), kèm bảng thuộc tính năm nơi lưu.
   Câu hỏi, câu trả lời và thuộc tính lấy từ ADE.storageChoose (models.js), không tính lại ở đây. */
(function () {
  'use strict';
  var K = 'track.storage.vz.', MC = 'track.storage.m.choose.';
  var T = function (k, p) { return ADE.t(K + k, p); };
  // vị trí bước của H1, tính từ id bước (<loại>.start | <loại>.<câu hỏi> | <loại>.leaf); số bước thay đổi theo tình huống
  function chooseIdx(ctx, C, ans) {
    if (!ctx.step) return ctx.pos > ctx.N ? ans.length + 1 : 0;
    var k = ctx.step.id.split('.').pop();
    return k === 'start' ? 0 : k === 'leaf' ? ans.length + 1 : C.Q.indexOf(k) + 1;
  }

  /* ---------- H1: cây quyết định chọn nơi lưu ---------- */
  ADE.registerScreen('storage.choose', function (box, ctx) {
    var h = ADE.ui.h, C = ADE.storageChoose, c = ctx.state.data, ans = C.ANS[c], leaf = C.leafOf(ans);
    var i = chooseIdx(ctx, C, ans), last = ans.length + 1, answered = Math.min(i, ans.length), done = i >= last;
    var leafBox = function (p, on) {
      return h('div', { class: 'vz-box vz-dt-leaf' + (on ? ' hl' : '') }, h('div', { class: 'vz-h', text: ADE.t(MC + 'place.' + p) }),
        h('div', { class: on ? null : 'dim', text: T('dt.chapter', { ch: C.CH[p].toUpperCase() }) }));
    };
    var rows = [];
    C.Q.forEach(function (q, k) {
      var asked = k < answered, cur = k === answered - 1 && !done, yes = asked && ans[k] === 1, no = asked && ans[k] === 0;
      var past = k >= ans.length;   // câu hỏi sau lá đã chọn: không đi tới
      rows.push(h('div', { class: 'vz-dt-row' + (past && done ? ' off' : '') },
        h('div', { class: 'vz-box' + (cur ? ' hl' : '') }, h('div', { class: 'vz-h', text: T('dt.q', { n: k + 1 }) }), h('div', { text: ADE.t(MC + 'q.' + q) })),
        h('div', { class: 'vz-dt-arr' + (yes ? ' on' : ''), text: (yes ? '▸ ' : '') + T('dt.yes') + ' →' }),
        leafBox(C.YES[q], yes && done)));
      rows.push(h('div', { class: 'vz-dt-no' + (no ? ' on' : ''), text: (no ? '▾ ' : '↓ ') + T('dt.no') }));
    });
    rows.push(h('div', { class: 'vz-dt-row' + (done && leaf !== C.LAST ? ' off' : '') }, h('div', { class: 'vz-dt-end', text: T('dt.end') }), h('div', { class: 'vz-dt-arr' + (leaf === C.LAST && done ? ' on' : ''), text: '→' }),
      leafBox(C.LAST, leaf === C.LAST && done)));
    // bảng thuộc tính năm nơi lưu (theo bảng so sánh của trang Data and file storage overview)
    var head = h('tr', null, h('th', { text: T('pt.place') }), ['other', 'uninstall', 'sysdel'].map(function (k) { return h('th', { text: T('pt.' + k) }); }));
    var tb = h('tbody');
    C.PLACES.forEach(function (p) {
      var on = done && p === leaf;
      tb.appendChild(h('tr', null, h('td', { class: on ? 'hl' : null, text: ADE.t(MC + 'place.' + p) }),
        C.PROPS[p].map(function (v, k) {
          var txt = T('pt.v.' + ['other', 'uninstall', 'sysdel'][k] + '.' + v);
          return h('td', { class: on ? 'hl' : (v === 'yes' ? 'ok' : null), text: txt });
        })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: T('dt.cap') }), h('div', { class: 'vz-dt' }, rows),
      h('p', { class: 'vz-cap', text: T('pt.cap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, head), tb)),
      h('div', { class: 'vz-legend', text: T('dt.legend') })));
  }, { labelKey: K + 'tab.dt', icon: 'diamond' });
})();
