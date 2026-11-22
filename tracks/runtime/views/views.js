/* View track B. Mỗi model chọn dạng hình hợp bản chất:
   - iso: bản đồ 11 thành phần (B0, Live Explorer) — nhìn toàn cảnh kiến trúc
   - pipeline: chuỗi xử lý trái → phải (setContent, compiler, recomposer, applier, phases, semantics)
   - cycle: vòng đọc–ghi state (snapshot) và vòng một lần bấm (counter)
   - tree: quan hệ cha–con (keys, skip)
   Lõi vẽ; ở đây chỉ khai báo node, cạnh, dải chỉ số (mọi nhãn là message key). Id node giữ nguyên id của bản đồ để model không đổi. */
(function () {
  'use strict';
  var K = 'track.runtime.';
  var T = function (m, id) { return { id: id, labelKey: K + 'm.' + m + '.met.' + id }; };
  var MAPN = [
    ['host', 0, 0, 'phone', 'ui'], ['composition', 4, 0, 'layers', 'runtime'], ['recomposer', 8, 0, 'clock', 'runtime'],
    ['compiler', 0, 4, 'chip', 'runtime'], ['composer', 4, 4, 'grid', 'runtime'], ['snapshot', 8, 4, 'frame', 'state'],
    ['slots', 0, 8, 'store', 'runtime'], ['applier', 4, 8, 'set', 'runtime'], ['uitree', 8, 8, 'list', 'ui'],
    ['phases', 4, 12, 'layers', 'ui'], ['semantics', 8, 12, 'eye', 'ui']
  ].map(function (a) { return { id: a[0], x: a[1], y: a[2], icon: a[3], tok: a[4], labelKey: K + 'n.' + a[0] }; });
  var E = function (id, f, t) { return { id: id, from: f, to: t }; };
  var MAPE = [E('e0', 'host', 'composition'), E('e1', 'recomposer', 'composition'), E('e2', 'composition', 'compiler'), E('e3', 'compiler', 'composer'),
    E('e4', 'composer', 'slots'), E('e5', 'snapshot', 'recomposer'), E('e6', 'composer', 'applier'), E('e7', 'applier', 'uitree'),
    E('e8', 'uitree', 'phases'), E('e9', 'uitree', 'snapshot'), E('e10', 'uitree', 'semantics')];
  var EX = [E('e11', 'composition', 'composer'), E('e12', 'composer', 'snapshot')];   // cạnh chỉ dùng ở các dạng phẳng
  // lấy một tập con của bản đồ (giữ id, nhãn, icon) cho dạng phẳng; extra: thuộc tính thêm theo id (col/row)
  function pick(ids, edgeIds, extra) {
    var nodes = ids.map(function (id) { var n = MAPN.filter(function (x) { return x.id === id; })[0], o = {}; for (var k in n) o[k] = n[k]; if (extra && extra[id]) for (var j in extra[id]) o[j] = extra[id][j]; return o; });
    var edges = MAPE.concat(EX).filter(function (e) { return edgeIds.indexOf(e.id) >= 0; });
    return { nodes: nodes, edges: edges };
  }
  function V(m, cfg) {
    var v = { titleKey: K + 'm.' + m + '.diagramTitle', descKey: K + 'm.' + m + '.diagramDesc', captionKey: K + 'cap.' + m, subjectKey: K + 'col.subject', famKeys: { idle: K + 'fam.idle', run: K + 'fam.run', done: K + 'fam.done' } };
    for (var k in cfg) v[k] = cfg[k];
    ADE.registerView('runtime.' + m, v);
  }
  var mix = function (a, b) { for (var k in b) a[k] = b[k]; return a; };
  V('map', { nodes: MAPN, edges: MAPE, metrics: [], nodeAction: 'focus' });   // bấm khối = chọn thành phần (giống ô "Thành phần")
  V('setcontent', mix({ layout: 'pipeline' }, pick(['host', 'composition', 'compiler', 'composer', 'slots', 'applier', 'uitree', 'phases'], ['e0', 'e2', 'e3', 'e4', 'e6', 'e7', 'e8'], { host: { col: 0, row: 0 }, composition: { col: 1, row: 0 }, compiler: { col: 2, row: 0 }, composer: { col: 3, row: 0 }, slots: { col: 4, row: 0 }, applier: { col: 3, row: 1 }, uitree: { col: 2, row: 1 }, phases: { col: 1, row: 1 } }), { metrics: [] }));
  V('compiler', mix({ layout: 'pipeline' }, pick(['composition', 'compiler', 'composer', 'slots'], ['e2', 'e3', 'e4']), { metrics: [] }));
  V('snapshot', mix({ layout: 'cycle' }, pick(['snapshot', 'recomposer', 'composition', 'composer'], ['e5', 'e1', 'e11', 'e12']), { metrics: [] }));
  V('recomposer', mix({ layout: 'pipeline' }, pick(['snapshot', 'recomposer', 'composition', 'composer', 'applier'], ['e5', 'e1', 'e11', 'e6']), { metrics: [T('recomposer', 'writes'), T('recomposer', 'passes')] }));
  V('applier', mix({ layout: 'pipeline' }, pick(['composer', 'slots', 'applier', 'uitree'], ['e4', 'e6', 'e7'], { slots: { col: 1, row: 0 }, applier: { col: 1, row: 1 }, uitree: { col: 2, row: 1 }, composer: { row: 0.5 } }), { metrics: [T('applier', 'calls')] }));
  V('counter', mix({ layout: 'cycle', zoom: false }, pick(['uitree', 'snapshot', 'recomposer', 'composition', 'composer', 'slots', 'applier', 'phases'], ['e9', 'e5', 'e1', 'e11', 'e4', 'e6', 'e7', 'e8']), { metrics: [T('counter', 'count'), T('counter', 'recomposed'), T('counter', 'skipped')] }));
  var N = function (m, id, x, y, icon, tok) { return { id: id, x: x, y: y, icon: icon, tok: tok, labelKey: K + 'm.' + m + '.n.' + id }; };
  /* DC (v2): người dùng bấm → state → Recomposer → thân composable → màn hình; side effect đi từ thân hoặc từ callback. */
  V('runs', {
    layout: 'cycle', zoom: false,
    nodes: [N('runs', 'tap', 0, 0, 'phone', 'ui'), N('runs', 'state', 4, 0, 'frame', 'state'), N('runs', 'recomposer', 8, 0, 'clock', 'runtime'),
      N('runs', 'body', 8, 4, 'chip', 'runtime'), N('runs', 'screen', 4, 4, 'screen', 'ui'), N('runs', 'effect', 0, 4, 'store', 'error')],
    edges: [E('e0', 'tap', 'state'), E('e1', 'state', 'recomposer'), E('e2', 'recomposer', 'body'), E('e3', 'body', 'screen'), E('e4', 'body', 'effect'), E('e5', 'tap', 'effect')],
    metrics: [T('runs', 'taps'), T('runs', 'runs'), T('runs', 'effects'), T('runs', 'shown')]
  });
  V('keys', {
    layout: 'tree',
    nodes: [N('keys', 'list', 0, 0, 'list', 'state'), N('keys', 'p0', 5, -3, 'square', 'runtime'), N('keys', 'p1', 5, 1, 'square', 'runtime'), N('keys', 'p2', 5, 5, 'square', 'runtime'), N('keys', 'p3', 5, 9, 'square', 'runtime')],
    edges: [E('e0', 'list', 'p0'), E('e1', 'list', 'p1'), E('e2', 'list', 'p2'), E('e3', 'list', 'p3')],
    metrics: [T('keys', 'kept'), T('keys', 'recomposed'), T('keys', 'created'), T('keys', 'removed')]
  });
  V('phases', {
    layout: 'pipeline',
    nodes: [N('phases', 'state', 0, 0, 'frame', 'state'), N('phases', 'comp', 4, 0, 'layers', 'runtime'), N('phases', 'layout', 4, 4, 'grid', 'ui'), N('phases', 'draw', 4, 8, 'spark', 'ui')],
    edges: [E('e1', 'state', 'comp'), E('e2', 'state', 'layout'), E('e3', 'state', 'draw')],
    metrics: [T('phases', 'comp'), T('phases', 'layout'), T('phases', 'draw'), T('phases', 'frames')]
  });
  V('skip', {
    layout: 'tree',
    nodes: [N('skip', 'parent', 0, 0, 'layers', 'runtime'), N('skip', 'child', 0, 5, 'square', 'runtime')],
    edges: [E('e1', 'parent', 'child')], metrics: [T('skip', 'child')]
  });
  V('semantics', {
    layout: 'pipeline',
    nodes: [N('semantics', 'ui', 0, 0, 'list', 'ui'), N('semantics', 'sem', 4, 0, 'eye', 'ui'), N('semantics', 'a11y', 8, -2, 'phone', 'signal'), N('semantics', 'test', 8, 4, 'check', 'job')],
    edges: [E('e1', 'ui', 'sem'), E('e2', 'sem', 'a11y'), E('e3', 'sem', 'test')], metrics: [T('semantics', 'nodes')]
  });
})();
