/* View track K: sơ đồ node cho model rời rạc (tab phụ; tab chính là hình ở views/visuals.js). */
(function () {
  'use strict';
  var K = 'track.fp.';
  var N = function (m, id, x, y, icon, tok) { return { id: id, x: x, y: y, icon: icon, tok: tok, labelKey: K + 'm.' + m + '.n.' + id }; };
  var E = function (id, f, t) { return { id: id, from: f, to: t }; };
  var T = function (m, id) { return { id: id, labelKey: K + 'm.' + m + '.met.' + id }; };
  function V(m, cfg) {
    var v = { titleKey: K + 'm.' + m + '.diagramTitle', descKey: K + 'm.' + m + '.diagramDesc', captionKey: K + 'cap.' + m, subjectKey: K + 'col.subject',
      stateFamilies: { surprise: 'fail' }, famKeys: { done: K + 'fam.done', fail: K + 'fam.fail', idle: K + 'fam.none' } };
    for (var k in cfg) v[k] = cfg[k];
    ADE.registerView('fp.' + m, v);
  }
  /* K1: thế giới bên ngoài (đồng hồ, biến đếm) → lời gọi → giá trị → test */
  V('pure', { layout: 'pipeline', nodes: [N('pure', 'world', 0, 1, 'clock', 'runtime'), N('pure', 'call', 3, 1, 'mechanism', 'ui'), N('pure', 'value', 6, 1, 'target', 'state'), N('pure', 'test', 9, 1, 'check', 'job')],
    edges: [E('e1', 'world', 'call'), E('e2', 'call', 'value'), E('e3', 'value', 'test')],
    metrics: [T('pure', 'subst'), T('pure', 'opaque'), T('pure', 'red')] });
})();
