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
})();
