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
  ['retarget', 'spec', 'gesture'].forEach(function (id) {
    ADE.registerView('animation.' + id, { titleKey: K + 'lab.title.' + id, descKey: K + 'lab.graphDesc', nodes: [], edges: [],
      mount: function (container, ctx) { return ADE.animLab.mount(container, id, ctx.modelId); } });
  });
})();
