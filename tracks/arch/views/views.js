/* View track G: sơ đồ node cho model rời rạc. Bốn tầng xếp từ màn hình tới nguồn dữ liệu. */
(function () {
  'use strict';
  var K = 'track.arch.';
  var N = function (m, id, x, y, icon, tok) { return { id: id, x: x, y: y, icon: icon, tok: tok, labelKey: K + 'm.' + m + '.n.' + id }; };
  var E = function (id, f, t) { return { id: id, from: f, to: t }; };
  var T = function (m, id) { return { id: id, labelKey: K + 'm.' + m + '.met.' + id }; };
  function V(m, cfg) {
    var v = { titleKey: K + 'm.' + m + '.diagramTitle', descKey: K + 'm.' + m + '.diagramDesc', captionKey: K + 'cap.' + m, subjectKey: K + 'col.subject',
      stateFamilies: { surprise: 'fail' }, famKeys: { done: K + 'fam.done', fail: K + 'fam.fail', idle: K + 'fam.none' } };
    for (var k in cfg) v[k] = cfg[k];
    ADE.registerView('arch.' + m, v);
  }
  /* G1: màn hình → state holder (ViewModel) → repository → nguồn dữ liệu */
  V('god', { layout: 'pipeline', nodes: [N('god', 'ui', 0, 0, 'screen', 'ui'), N('god', 'vm', 3, 0, 'layers', 'state'), N('god', 'repo', 6, 0, 'store', 'runtime'), N('god', 'source', 9, 0, 'source', 'job')],
    edges: [E('e1', 'ui', 'vm'), E('e2', 'vm', 'repo'), E('e3', 'repo', 'source')], metrics: [T('god', 'keep'), T('god', 'files'), T('god', 'test')] });
})();
