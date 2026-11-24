/* View track J: sơ đồ node cho model rời rạc (tab phụ; tab chính là hình ở views/visuals.js). */
(function () {
  'use strict';
  var K = 'track.cleancode.';
  var N = function (m, id, x, y, icon, tok) { return { id: id, x: x, y: y, icon: icon, tok: tok, labelKey: K + 'm.' + m + '.n.' + id }; };
  var E = function (id, f, t) { return { id: id, from: f, to: t }; };
  var T = function (m, id) { return { id: id, labelKey: K + 'm.' + m + '.met.' + id }; };
  function V(m, cfg) {
    var v = { titleKey: K + 'm.' + m + '.diagramTitle', descKey: K + 'm.' + m + '.diagramDesc', captionKey: K + 'cap.' + m, subjectKey: K + 'col.subject',
      stateFamilies: { surprise: 'fail' }, famKeys: { done: K + 'fam.done', fail: K + 'fam.fail', idle: K + 'fam.none' } };
    for (var k in cfg) v[k] = cfg[k];
    ADE.registerView('cleancode.' + m, v);
  }
  /* J1: mã → bộ nhớ làm việc; yêu cầu mới → mã; mã → hẹn nhắc */
  V('fits', { layout: 'pipeline', nodes: [N('fits', 'code', 0, 1.5, 'list', 'job'), N('fits', 'head', 4, 0, 'chip', 'state'), N('fits', 'change', 0, 3.5, 'source', 'ui'), N('fits', 'remind', 8, 1.5, 'clock', 'runtime')],
    edges: [E('e1', 'code', 'head'), E('e2', 'change', 'code'), E('e3', 'code', 'remind')],
    metrics: [T('fits', 'paths'), T('fits', 'vars'), T('fits', 'skipped')] });
})();
