/* Hình trực quan theo bước của track B (ADE.registerScreen với nhãn tab riêng). Sơ đồ node vẫn ở tab bên cạnh.
   B3 runtime.structure: SlotTable là một dãy group, nên vẽ thành dãy ô thẳng hàng thay cho các khối nối nhau.
   Dữ liệu lấy nguyên từ stateAfter của model; hàng vừa đổi ở bước này có viền. */
(function () {
  'use strict';
  var K = 'track.runtime.vz.';
  ADE.registerScreen('runtime.structure', function (box, ctx) {
    var h = ADE.ui.h, steps = ctx.steps, i = ctx.step ? steps.indexOf(ctx.step) : (ctx.pos > ctx.N ? steps.length - 1 : 0);
    var cur = steps[i] || steps[0], prev = i > 0 ? steps[i - 1] : null;
    var val = function (st, k) { var r = (st.stateAfter || []).filter(function (x) { return x.labelKey.split('.').pop() === k; })[0]; return r ? String(r.value) : '—'; };
    var tb = h('tbody');
    ['old', 'seq', 'pending', 'ops', 'nodes'].forEach(function (k) {
      var v = val(cur, k), changed = prev && val(prev, k) !== v;
      var parts = v === '—' ? [] : v.split(' · ');
      var cell = h('td', { class: changed ? 'hl' : null }, parts.length ? parts.map(function (p) { return h('span', { class: 'vz-chip' + (/✗/.test(p) ? ' bad' : ''), text: p }); }) : '—');
      tb.appendChild(h('tr', null, h('th', { text: ADE.t('track.runtime.m.structure.st.' + k) }), cell));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: ADE.t(K + 'slots.cap') }), h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, tb))));
  }, { labelKey: K + 'tab.slots', icon: 'list' });

  /* MD runtime.chain: đối chiếu chuỗi modifier cũ và mới theo vị trí; hành động trên node hiện dần theo tổng số đo của bước
     (reused + updated + inserted + removed), theo thứ tự hàng. Hàng lấy từ chú thích của model (giữ/cập nhật/chèn/gỡ). */
  var ROWS = {
    equal: [['padding', 'padding', 'reuse'], ['clip', 'clip', 'reuse'], ['background(Red)', 'background(Red)', 'reuse'], ['size', 'size', 'reuse']],
    update: [['padding', 'padding', 'reuse'], ['clip', 'clip', 'reuse'], ['background(Red)', 'background(Blue)', 'update'], ['size', 'size', 'reuse']],
    insert: [['padding', 'padding', 'reuse'], ['—', 'border', 'insert'], ['background', 'background', 'reuse'], ['size', 'size', 'reuse']],
    replace: [['padding', 'padding', 'reuse'], ['shadow', '—', 'remove'], ['—', 'border', 'insert'], ['background', 'background', 'reuse'], ['size', 'size', 'reuse']]
  };
  ADE.registerScreen('runtime.chain', function (box, ctx) {
    var h = ADE.ui.h, sc = ROWS[ctx.state.which] ? ctx.state.which : 'equal', steps = ctx.steps;
    var st = ctx.step || (ctx.pos > ctx.N ? steps[steps.length - 1] : null), mt = (st && st.metrics) || {};
    var done = (mt.reused || 0) + (mt.updated || 0) + (mt.inserted || 0) + (mt.removed || 0);
    var tb = h('tbody');
    ROWS[sc].forEach(function (r, i) {
      var shown = i < done, cur = i === done - 1;
      tb.appendChild(h('tr', null, h('td', { class: 'c', text: String(i + 1) }), h('td', { text: r[0] }), h('td', { text: r[1] }),
        h('td', { class: (shown ? (r[2] === 'reuse' ? 'ok' : r[2] === 'remove' ? 'bad' : '') : 'dim') + (cur ? ' hl' : ''), text: shown ? ADE.t(K + 'chain.' + r[2]) : '·' })));
    });
    var th = function (k) { return h('th', { text: ADE.t(K + 'chain.' + k) }); };
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: ADE.t(K + 'chain.cap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, h('th', { text: '#' }), th('colOld'), th('colNew'), th('colAct'))), tb))));
  }, { labelKey: K + 'tab.chain', icon: 'list' });
})();
