/* Hình trực quan theo bước của track C (ADE.registerScreen với nhãn tab riêng). Sơ đồ node vẫn ở tab bên cạnh.
   C0 animation.tree: trang choose-api là một CÂY quyết định; hình vẽ đường đi của tình huống đang chọn (câu hỏi, câu trả lời,
   nhánh còn lại dẫn tới đâu) và một bảng tra cho cả sáu tình huống. Bản cũ lồng hộp nhiều tầng khó đọc (người dùng góp ý 2026-11-24).
   Cây được ghép từ các đường đi trong model (ADE.animTree.PATHS); chỉ gồm những nhánh mà sáu tình huống mẫu đi qua. */
(function () {
  'use strict';
  var K = 'track.animation.vz.', M = 'track.animation.m.tree.';
  function build() {
    var T = ADE.animTree, root = null;
    Object.keys(T.PATHS).forEach(function (sc) {
      var path = T.PATHS[sc], ref = { node: root }, holder = function (v) { root = v; };
      var cur = root, set = holder;
      path.forEach(function (qa) {
        if (!cur) { cur = { q: qa[0], yes: null, no: null }; set(cur); }
        var side = qa[1] ? 'yes' : 'no', parent = cur;
        set = function (v) { parent[side] = v; };
        cur = parent[side];
      });
      set({ leaf: sc });
    });
    return root;
  }
  /* Vẽ thành ĐƯỜNG ĐI dọc của tình huống đang chọn (dễ dò hơn cây lồng nhiều tầng): mỗi hàng một câu hỏi có số thứ tự,
     câu trả lời đã chọn, và nhánh còn lại dẫn tới đâu; câu hỏi hiện dần theo bước, cuối cùng là thẻ API.
     Bên dưới: bảng tra sáu nhu cầu → API → chương, hàng của tình huống đang xem được tô. */
  ADE.registerScreen('animation.tree', function (box, ctx) {
    var h = ADE.ui.h, T = ADE.animTree, sc = ctx.state.which, path = T.PATHS[sc] || [];
    var last = ctx.steps.length - 1, i = ctx.step ? ctx.steps.indexOf(ctx.step) : (ctx.pos > ctx.N ? last : 0);
    var depth = Math.min(i, path.length), atApi = i >= last, root = build();
    var yn = function (v) { return ADE.t(K + 'tree.' + (v ? 'yes' : 'no')); };
    var flow = h('ol', { class: 'dpath' }), node = root;
    path.forEach(function (qa, k) {
      if (!node || node.leaf) return;
      var shown = k <= depth, answered = k < depth, cur = k === depth && !atApi, side = qa[1] ? 'yes' : 'no', other = node[qa[1] ? 'no' : 'yes'];
      var otherTxt = !other ? '' : (other.leaf ? ADE.t(K + 'tree.else', { ans: yn(!qa[1]), api: T.API[other.leaf] }) : ADE.t(K + 'tree.elseQ', { ans: yn(!qa[1]) }));
      flow.appendChild(h('li', { class: 'dpath-q' + (cur ? ' cur' : '') + (shown ? '' : ' later') },
        h('span', { class: 'dpath-n', text: String(k + 1) }),
        h('div', { class: 'dpath-body' },
          h('div', { class: 'dpath-t', text: shown ? ADE.t(M + 's.q.' + qa[0] + '.title') : '?' }),
          shown ? h('div', { class: 'dpath-a' },
            h('span', { class: 'dpath-pick' + (answered ? ' on' : ' wait'), text: answered ? yn(qa[1]) + ' ✓' : ADE.t(K + 'tree.thinking') }),
            answered && otherTxt ? h('span', { class: 'dpath-else', text: otherTxt }) : null) : null)));
      node = node[side];
    });
    flow.appendChild(h('li', { class: 'dpath-api' + (atApi ? ' on' : ' later') },
      h('span', { class: 'dpath-n', text: '→' }),
      h('div', { class: 'dpath-body' }, h('div', { class: 'dpath-t', text: atApi ? T.API[sc] : '?' }),
        atApi ? h('div', { class: 'dpath-a', text: ADE.t(K + 'tree.chapter', { ch: T.CH[sc].toUpperCase() }) }) : null)));
    var tb = h('tbody');
    Object.keys(T.PATHS).forEach(function (k) {
      var me = k === sc;
      tb.appendChild(h('tr', null, h('th', { class: me ? 'hl' : null, text: ADE.t(M + 'ctl.which.' + k) }), h('td', { class: me && atApi ? 'ok' : (me ? null : 'dim'), text: T.API[k] }),
        h('td', { class: 'c dim', text: T.CH[k].toUpperCase() }), h('td', { class: 'c dim', text: String(T.PATHS[k].length) })));
    });
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: ADE.t(K + 'tree.cap') }), flow,
      h('p', { class: 'vz-cap', text: ADE.t(K + 'tree.tcap') }),
      h('div', { class: 'vz-scroll' }, h('table', { class: 'vz-table' }, h('thead', null, h('tr', null, ['need', 'api', 'ch', 'qs'].map(function (q) { return h('th', { text: ADE.t(K + 'tree.col.' + q) }); }))), tb))));
  }, { labelKey: K + 'tab.tree', icon: 'diamond' });
})();
