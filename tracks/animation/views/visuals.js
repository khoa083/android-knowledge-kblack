/* Hình trực quan theo bước của track C (ADE.registerScreen với nhãn tab riêng). Sơ đồ node vẫn ở tab bên cạnh.
   C0 animation.tree: trang choose-api là một CÂY quyết định, nên vẽ thành cây có nhánh Có/Không thay cho chuỗi khối.
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
  ADE.registerScreen('animation.tree', function (box, ctx) {
    var h = ADE.ui.h, T = ADE.animTree, sc = ctx.state.which, path = T.PATHS[sc] || [];
    var last = ctx.steps.length - 1, i = ctx.step ? ctx.steps.indexOf(ctx.step) : (ctx.pos > ctx.N ? last : 0);
    var depth = Math.min(i, path.length), atApi = i >= last;
    function render(node, level, onPath) {
      if (node.leaf) {
        var hit = onPath && node.leaf === sc && atApi;
        return h('div', { class: 'vz-box' + (hit ? ' hl' : '') }, h('div', { class: 'vz-h', text: T.API[node.leaf] }), h('div', { class: hit ? null : 'dim', text: ADE.t(K + 'tree.chapter', { ch: T.CH[node.leaf].toUpperCase() }) }));
      }
      var answered = onPath && level < depth, isCur = onPath && level === depth - 1;
      var kids = ['yes', 'no'].filter(function (s) { return node[s]; }).map(function (s) {
        var taken = answered && (path[level][1] ? 'yes' : 'no') === s;
        return h('div', null, h('div', { class: 'vz-cap', text: (taken ? '▸ ' : '') + ADE.t(K + 'tree.' + s) }), render(node[s], level + 1, taken));
      });
      return h('div', { class: 'vz-box' + (isCur ? ' hl' : '') }, h('div', { class: 'vz-h', text: ADE.t(M + 's.q.' + node.q + '.title') }), kids);
    }
    box.appendChild(h('div', { class: 'vz' }, h('p', { class: 'vz-cap', text: ADE.t(K + 'tree.cap') }), h('div', { class: 'vz-scroll' }, render(build(), 0, true))));
  }, { labelKey: K + 'tab.tree', icon: 'diamond' });
})();
