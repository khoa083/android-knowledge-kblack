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
  /* K2: danh sách đã chọn → danh sách gốc (dùng chung); hàm cộng phí → stack */
  V('persist', { layout: 'pipeline', nodes: [N('persist', 'selected', 0, 0, 'list', 'ui'), N('persist', 'booked', 4, 0, 'store', 'state'), N('persist', 'fold', 0, 2, 'mechanism', 'job'), N('persist', 'stack', 4, 2, 'layers', 'runtime')],
    edges: [E('e1', 'selected', 'booked'), E('e2', 'booked', 'fold'), E('e3', 'fold', 'stack')],
    metrics: [T('persist', 'touched'), T('persist', 'nodes'), T('persist', 'depth')] });
  /* K3: chuỗi đầu vào → các hàm ghép → bốn màn hình; cấu hình phòng khám → bốn màn hình */
  V('compose', { layout: 'pipeline', nodes: [N('compose', 'raw', 0, 0, 'source', 'ui'), N('compose', 'pipe', 3, 0, 'mechanism', 'job'), N('compose', 'screens', 6, 1, 'screen', 'state'), N('compose', 'config', 3, 2, 'list', 'runtime')],
    edges: [E('e1', 'raw', 'pipe'), E('e2', 'pipe', 'screens'), E('e3', 'config', 'screens')],
    metrics: [T('compose', 'args'), T('compose', 'repeated'), T('compose', 'wrong'), T('compose', 'edits')] });
  /* K4: kiểu → các trạng thái biểu diễn được → màn hình; khối catch ghi vào state */
  V('adt', { layout: 'pipeline', nodes: [N('adt', 'type', 0, 0, 'layers', 'ui'), N('adt', 'states', 3, 0, 'grid', 'state'), N('adt', 'screen', 6, 0, 'screen', 'job'), N('adt', 'catch', 3, 2, 'mechanism', 'runtime')],
    edges: [E('e1', 'type', 'states'), E('e2', 'states', 'screen'), E('e3', 'catch', 'states')],
    metrics: [T('adt', 'combos'), T('adt', 'invalid'), T('adt', 'silent'), T('adt', 'flagged')] });
})();
