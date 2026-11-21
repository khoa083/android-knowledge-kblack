/* View sơ đồ cho các model rời rạc của track E. */
(function () {
  'use strict';
  var K = 'track.ui.';
  var N = function (id, x, y, icon, tok, key) { return { id: id, x: x, y: y, icon: icon, tok: tok, labelKey: key || K + 'n.' + id }; };
  var E = function (id, f, t) { return { id: id, from: f, to: t }; };
  function V(m, cfg) { var v = { titleKey: K + 'm.' + m + '.diagramTitle', descKey: K + 'm.' + m + '.diagramDesc', captionKey: K + 'cap.' + m, subjectKey: K + 'col.subject' }; for (var k in cfg) v[k] = cfg[k]; ADE.registerView('ui.' + m, v); }
  var L = ['token', 'component', 'pattern', 'screen', 'flow'];
  V('layers', { layout: 'pipeline', nodes: L.map(function (l, i) { return N(l, i * 3, 0, ['spark', 'square', 'grid', 'phone', 'layers'][i], 'ui', K + 'm.layers.l.' + l + '.title'); }), edges: L.slice(0, 4).map(function (l, i) { return E('l' + i, l, L[i + 1]); }), metrics: [] });
  /* vòng phản hồi thiết kế: màn hình → người dùng → (quan sát) → thiết kế → màn hình */
  var basic = { nodes: [N('screen', 0, 0, 'phone', 'ui'), N('user', 4, 0, 'eye', 'signal'), N('design', 4, 4, 'set', 'runtime')], edges: [E('e1', 'screen', 'user'), E('e2', 'user', 'design'), E('e3', 'design', 'screen')] };
  V('patterns', { layout: 'cycle', captionKey: K + 'cap.loop', nodes: basic.nodes, edges: basic.edges, metrics: [] });
  V('form', { layout: 'cycle', captionKey: K + 'cap.loop', nodes: basic.nodes, edges: basic.edges, metrics: [{ id: 'issues', labelKey: K + 'm.form.met.issues' }] });
  V('response', { layout: 'cycle', captionKey: K + 'cap.loop', nodes: basic.nodes, edges: basic.edges, metrics: [] });
})();
