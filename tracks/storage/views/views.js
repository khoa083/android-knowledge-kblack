/* View track H: sơ đồ node cho model rời rạc (tab phụ; tab chính là hình ở views/visuals.js). */
(function () {
  'use strict';
  var K = 'track.storage.';
  var N = function (m, id, x, y, icon, tok) { return { id: id, x: x, y: y, icon: icon, tok: tok, labelKey: K + 'm.' + m + '.n.' + id }; };
  var E = function (id, f, t) { return { id: id, from: f, to: t }; };
  var T = function (m, id) { return { id: id, labelKey: K + 'm.' + m + '.met.' + id }; };
  function V(m, cfg) {
    var v = { titleKey: K + 'm.' + m + '.diagramTitle', descKey: K + 'm.' + m + '.diagramDesc', captionKey: K + 'cap.' + m, subjectKey: K + 'col.subject',
      stateFamilies: { surprise: 'fail' }, famKeys: { done: K + 'fam.done', fail: K + 'fam.fail', idle: K + 'fam.none' } };
    for (var k in cfg) v[k] = cfg[k];
    ADE.registerView('storage.' + m, v);
  }
  /* H1: loại dữ liệu → câu hỏi → nơi lưu → chương */
  V('choose', { layout: 'pipeline', nodes: [N('choose', 'data', 0, 0, 'source', 'ui'), N('choose', 'question', 3, 0, 'diamond', 'state'), N('choose', 'place', 6, 0, 'store', 'runtime'), N('choose', 'chapter', 9, 0, 'eye', 'job')],
    edges: [E('e1', 'data', 'question'), E('e2', 'question', 'place'), E('e3', 'place', 'chapter')],
    metrics: [T('choose', 'place'), T('choose', 'chapter')] });
})();
