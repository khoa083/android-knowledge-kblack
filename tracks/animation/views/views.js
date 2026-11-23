/* View track C: sơ đồ isometric cho model rời rạc; ba lab (retarget, spec, gesture) tự vẽ qua ADE.animLab.mount. */
(function () {
  'use strict';
  var K = 'track.animation.';
  var N = function (m, id, x, y, icon, tok) { return { id: id, x: x, y: y, icon: icon, tok: tok, labelKey: K + 'm.' + m + '.n.' + id }; };
  var E = function (id, f, t) { return { id: id, from: f, to: t }; };
  var T = function (m, id) { return { id: id, labelKey: K + 'm.' + m + '.met.' + id }; };
  function V(m, cfg) { var v = { titleKey: K + 'm.' + m + '.diagramTitle', descKey: K + 'm.' + m + '.diagramDesc', captionKey: K + 'cap.' + m, subjectKey: K + 'col.subject' }; for (var k in cfg) v[k] = cfg[k]; ADE.registerView('animation.' + m, v); }
  V('choose', { layout: 'pipeline', nodes: [N('choose', 'need', 0, 0, 'target', 'state'), N('choose', 'api', 4, 0, 'motion', 'anim'), N('choose', 'alt', 4, 4, 'layers', 'runtime')], edges: [E('e1', 'need', 'api'), E('e2', 'api', 'alt')], metrics: [] });
  V('transition', {
    layout: 'pipeline',
    nodes: [N('transition', 'state', 0, 0, 'frame', 'state'), N('transition', 'transition', 4, 0, 'motion', 'anim'), N('transition', 'color', 8, -4, 'spark', 'anim'), N('transition', 'size', 8, 0, 'grid', 'anim'), N('transition', 'alpha', 8, 4, 'eye', 'anim')],
    edges: [E('e0', 'state', 'transition'), E('e1', 'transition', 'color'), E('e2', 'transition', 'size'), E('e3', 'transition', 'alpha')], metrics: [T('transition', 'children'), T('transition', 'ms')]
  });
  V('visibility', {
    layout: 'pipeline',
    nodes: [N('visibility', 'trigger', 0, 0, 'target', 'state'), N('visibility', 'transition', 4, 0, 'motion', 'anim'), N('visibility', 'a', 8, -2, 'square', 'ui'), N('visibility', 'b', 8, 3, 'square', 'ui')],
    edges: [E('e0', 'trigger', 'transition'), E('e1', 'transition', 'a'), E('e2', 'transition', 'b')], metrics: []
  });
  V('size', {
    layout: 'tree',
    nodes: [N('size', 'card', 0, 0, 'phone', 'ui'), N('size', 'layout', 4, -2, 'grid', 'ui'), N('size', 'draw', 4, 3, 'spark', 'ui'), N('size', 'sibling', 8, 0, 'square', 'runtime')],
    edges: [E('e1', 'card', 'layout'), E('e2', 'card', 'draw'), E('e3', 'layout', 'sibling')], metrics: [T('size', 'layouts'), T('size', 'draws')]
  });
  V('phaseread', {
    layout: 'pipeline',
    nodes: [N('phaseread', 'anim', 0, 0, 'motion', 'anim'), N('phaseread', 'comp', 4, -4, 'layers', 'runtime'), N('phaseread', 'layout', 4, 0, 'grid', 'ui'), N('phaseread', 'draw', 4, 4, 'spark', 'ui')],
    edges: [E('e1', 'anim', 'comp'), E('e2', 'anim', 'layout'), E('e3', 'anim', 'draw')], metrics: [T('phaseread', 'comp'), T('phaseread', 'layout'), T('phaseread', 'draw')]
  });
  V('testclock', {
    layout: 'pipeline',
    nodes: [N('testclock', 'test', 0, 0, 'check', 'job'), N('testclock', 'clock', 4, 0, 'clock', 'state'), N('testclock', 'anim', 4, 4, 'motion', 'anim')],
    edges: [E('e0', 'test', 'clock'), E('e1', 'clock', 'anim')], metrics: [T('testclock', 'value'), T('testclock', 'clock')]
  });
  /* C1 (v2): composable → AnimateAsState (remember) → job (coroutine) → Animatable; giá trị quay về composable mỗi frame. */
  V('aas', {
    layout: 'pipeline', zoom: false,
    nodes: [N('aas', 'comp', 0, 0, 'layers', 'runtime'), N('aas', 'state', 4, 0, 'store', 'state'), N('aas', 'job', 8, 0, 'job', 'job'), N('aas', 'anim', 12, 0, 'motion', 'anim')],
    edges: [E('e1', 'comp', 'state'), E('e2', 'state', 'job'), E('e3', 'job', 'anim'), E('e4', 'anim', 'comp')],
    metrics: [T('aas', 'launched'), T('aas', 'cancelled'), T('aas', 'value')]
  });
  /* C2 (v2): giá trị → converter → AnimationVector ← VectorizedAnimationSpec; rồi quay lại kiểu giá trị. */
  V('vector', {
    layout: 'pipeline', zoom: false,
    nodes: [N('vector', 'value', 0, 0, 'target', 'state'), N('vector', 'conv', 4, 0, 'set', 'runtime'), N('vector', 'vec', 8, 0, 'grid', 'anim'), N('vector', 'spec', 12, 0, 'motion', 'anim')],
    edges: [E('e1', 'value', 'conv'), E('e2', 'conv', 'vec'), E('e3', 'spec', 'vec'), E('e4', 'vec', 'value')],
    metrics: [T('vector', 'dim')]
  });
  /* C3 (v2): state → Transition → ba con (alpha, color, height), mỗi con có spec riêng. */
  V('segment', {
    layout: 'pipeline', zoom: false,
    nodes: [N('segment', 'state', 0, 0, 'frame', 'state'), N('segment', 'transition', 4, 0, 'motion', 'anim'), N('segment', 'alpha', 8, -4, 'eye', 'anim'), N('segment', 'color', 8, 0, 'spark', 'anim'), N('segment', 'height', 8, 4, 'grid', 'anim')],
    edges: [E('e0', 'state', 'transition'), E('e1', 'transition', 'alpha'), E('e2', 'transition', 'color'), E('e3', 'transition', 'height')],
    metrics: [T('segment', 'running'), T('segment', 'ms')]
  });
  /* C4 (v2): cờ visible → AnimatedVisibility → nội dung trong composition → bị gỡ. */
  V('exitlife', {
    layout: 'pipeline', zoom: false,
    nodes: [N('exitlife', 'flag', 0, 0, 'target', 'state'), N('exitlife', 'av', 4, 0, 'motion', 'anim'), N('exitlife', 'content', 8, -2, 'square', 'ui'), N('exitlife', 'gone', 8, 3, 'remove', 'runtime')],
    edges: [E('e1', 'flag', 'av'), E('e2', 'av', 'content'), E('e3', 'av', 'gone')],
    metrics: [T('exitlife', 'ms'), T('exitlife', 'inComp')]
  });
  /* C5 (v2): state → con (height) → node animateContentSize → cha và phần tử bên cạnh. */
  V('acs', {
    layout: 'pipeline', zoom: false,
    nodes: [N('acs', 'state', 0, 0, 'target', 'state'), N('acs', 'child', 4, -3, 'square', 'ui'), N('acs', 'node', 8, 0, 'grid', 'anim'), N('acs', 'parent', 12, 3, 'layers', 'runtime')],
    edges: [E('e1', 'state', 'child'), E('e2', 'child', 'node'), E('e3', 'node', 'parent')],
    metrics: [T('acs', 'comp'), T('acs', 'layout'), T('acs', 'child'), T('acs', 'reported')]
  });
  /* IF (v2): đồng hồ frame → spec lặp → giá trị; tỉ lệ thời lượng / chính sách can thiệp vào đồng hồ. */
  V('repeat', {
    layout: 'pipeline', zoom: false,
    nodes: [N('repeat', 'clock', 0, 0, 'frame', 'runtime'), N('repeat', 'spec', 4, 0, 'layers', 'anim'), N('repeat', 'value', 8, 0, 'spark', 'ui'), N('repeat', 'policy', 0, 4, 'target', 'state')],
    edges: [E('e1', 'clock', 'spec'), E('e2', 'spec', 'value'), E('e3', 'policy', 'clock')],
    metrics: [T('repeat', 'ms'), T('repeat', 'iter'), T('repeat', 'value')]
  });
  ['retarget', 'spec', 'gesture'].forEach(function (id) {
    ADE.registerView('animation.' + id, { titleKey: K + 'lab.title.' + id, descKey: K + 'lab.graphDesc', nodes: [], edges: [],
      mount: function (container, ctx) { return ADE.animLab.mount(container, id, ctx.modelId); } });
  });
})();
