/* View track I: sơ đồ node cho model rời rạc (tab phụ; tab chính là hình ở views/visuals.js). */
(function () {
  'use strict';
  var K = 'track.sysdesign.';
  var N = function (m, id, x, y, icon, tok) { return { id: id, x: x, y: y, icon: icon, tok: tok, labelKey: K + 'm.' + m + '.n.' + id }; };
  var E = function (id, f, t) { return { id: id, from: f, to: t }; };
  var T = function (m, id) { return { id: id, labelKey: K + 'm.' + m + '.met.' + id }; };
  function V(m, cfg) {
    var v = { titleKey: K + 'm.' + m + '.diagramTitle', descKey: K + 'm.' + m + '.diagramDesc', captionKey: K + 'cap.' + m, subjectKey: K + 'col.subject',
      stateFamilies: { surprise: 'fail' }, famKeys: { done: K + 'fam.done', fail: K + 'fam.fail', idle: K + 'fam.none' } };
    for (var k in cfg) v[k] = cfg[k];
    ADE.registerView('sysdesign.' + m, v);
  }
  /* I1: đề bài → designer, backend → kế hoạch */
  V('plan', { layout: 'pipeline', nodes: [N('plan', 'brief', 0, 1.5, 'source', 'ui'), N('plan', 'designer', 4, 0, 'eye', 'state'), N('plan', 'backend', 4, 3, 'job', 'runtime'), N('plan', 'plan', 8, 1.5, 'list', 'job')],
    edges: [E('e1', 'brief', 'designer'), E('e2', 'brief', 'backend'), E('e3', 'designer', 'plan'), E('e4', 'backend', 'plan')],
    metrics: [T('plan', 'asked'), T('plan', 'late'), T('plan', 'data')] });
})();
