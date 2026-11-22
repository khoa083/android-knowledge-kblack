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
  /* B2 (v2): mã đã biến đổi gọi Composer; Composer ghi group và slot, giữ restart scope, phát node ra màn hình. */
  V('groups', {
    layout: 'pipeline', zoom: false,
    nodes: [N('groups', 'caller', 0, 0, 'clock', 'runtime'), N('groups', 'code', 4, 0, 'chip', 'runtime'), N('groups', 'composer', 8, 0, 'grid', 'runtime'),
      N('groups', 'scope', 0, 4, 'refresh', 'state'), N('groups', 'groups', 4, 4, 'list', 'runtime'), N('groups', 'slots', 8, 4, 'store', 'state'),
      N('groups', 'screen', 8, 8, 'screen', 'ui')],
    edges: [E('e0', 'caller', 'code'), E('e1', 'code', 'composer'), E('e2', 'composer', 'groups'), E('e3', 'composer', 'slots'), E('e4', 'composer', 'scope'),
      E('e5', 'scope', 'caller'), E('e6', 'composer', 'screen')],
    metrics: [T('groups', 'groups'), T('groups', 'slots'), T('groups', 'runs'), T('groups', 'skipped'), T('groups', 'shown')]
  });
  /* B3 (v2): chuỗi group mới so với bảng cũ; lệch thì Pending (bảng băm theo key), chèn qua insert table, rồi danh sách thay đổi tới Applier. */
  V('structure', {
    layout: 'pipeline', zoom: false,
    nodes: [N('structure', 'code', 0, 0, 'chip', 'runtime'), N('structure', 'composer', 4, 0, 'grid', 'runtime'), N('structure', 'old', 8, 0, 'list', 'runtime'),
      N('structure', 'pending', 4, 4, 'store', 'state'), N('structure', 'insert', 8, 4, 'add', 'runtime'), N('structure', 'changes', 4, 8, 'queue', 'runtime'),
      N('structure', 'nodes', 8, 8, 'screen', 'ui')],
    edges: [E('e1', 'code', 'composer'), E('e2', 'composer', 'old'), E('e3', 'composer', 'pending'), E('e4', 'composer', 'insert'), E('e5', 'composer', 'changes'), E('e6', 'changes', 'nodes')],
    metrics: [T('structure', 'matched'), T('structure', 'moved'), T('structure', 'inserted'), T('structure', 'deleted'), T('structure', 'applier')]
  });
  /* B4 (v2): global snapshot, hai mutable snapshot A và B, chuỗi state record, policy khi apply, và apply observer (Recomposer). */
  V('records', {
    layout: 'pipeline', zoom: false,
    nodes: [N('records', 'global', 0, 4, 'layers', 'state'), N('records', 'snapA', 4, 0, 'frame', 'state'), N('records', 'snapB', 4, 8, 'frame', 'state'),
      N('records', 'records', 8, 4, 'list', 'runtime'), N('records', 'policy', 8, 8, 'diamond', 'runtime'), N('records', 'observers', 0, 0, 'clock', 'runtime')],
    edges: [E('e1', 'global', 'snapA'), E('e2', 'global', 'snapB'), E('e3', 'snapA', 'records'), E('e4', 'snapB', 'records'), E('e5', 'snapA', 'global'),
      E('e6', 'snapB', 'policy'), E('e7', 'global', 'observers')],
    metrics: [T('records', 'global'), T('records', 'applied'), T('records', 'conflicts'), T('records', 'records')]
  });
  /* SH (v2): màn hình và năm nơi giữ state: Composition, Bundle (saved instance state), ViewModelStore, process, lưu trữ bền. */
  V('survive', {
    layout: 'pipeline', zoom: false,
    nodes: [N('survive', 'ui', 0, 4, 'phone', 'ui'), N('survive', 'composition', 4, 0, 'layers', 'runtime'), N('survive', 'bundle', 4, 4, 'store', 'state'),
      N('survive', 'vm', 4, 8, 'chip', 'state'), N('survive', 'disk', 8, 8, 'store', 'job'), N('survive', 'process', 8, 0, 'thread', 'error')],
    edges: [E('e1', 'ui', 'composition'), E('e2', 'ui', 'bundle'), E('e3', 'ui', 'vm'), E('e4', 'vm', 'bundle'), E('e5', 'vm', 'disk')],
    metrics: [T('survive', 'kept'), T('survive', 'lost'), T('survive', 'checked')]
  });
  /* B5 (v2): Choreographer → frame clock → Recomposer; awaiter của frame clock (animation) chạy trước, rồi recompose và apply; lifecycle tạm dừng clock. */
  V('frame', {
    layout: 'pipeline', zoom: false,
    nodes: [N('frame', 'choreographer', 0, 0, 'clock', 'signal'), N('frame', 'clock', 4, 0, 'frame', 'signal'), N('frame', 'recomposer', 8, 0, 'clock', 'runtime'),
      N('frame', 'awaiters', 8, 4, 'motion', 'anim'), N('frame', 'composition', 12, 0, 'layers', 'runtime'), N('frame', 'applier', 12, 4, 'set', 'ui'),
      N('frame', 'lifecycle', 4, 4, 'phone', 'ui')],
    edges: [E('e0', 'clock', 'choreographer'), E('e0r', 'choreographer', 'recomposer'), E('e1', 'recomposer', 'clock'), E('e2', 'recomposer', 'awaiters'), E('e2r', 'awaiters', 'recomposer'),
      E('e3', 'recomposer', 'composition'), E('e4', 'composition', 'applier'), E('e5', 'lifecycle', 'recomposer'), E('e6', 'lifecycle', 'clock')],
    metrics: [T('frame', 'frames'), T('frame', 'recomps'), T('frame', 'animFrames')]
  });
  /* EF (v2): cú bấm/cha → composition → object được remember (LaunchedEffectImpl, DisposableEffect) → coroutine; SideEffect sau mỗi lượt. */
  V('effects', {
    layout: 'pipeline', zoom: false,
    nodes: [N('effects', 'tap', 0, 0, 'phone', 'ui'), N('effects', 'composition', 4, 0, 'layers', 'runtime'), N('effects', 'remembered', 8, 0, 'store', 'runtime'),
      N('effects', 'job', 12, 0, 'job', 'coroutine'), N('effects', 'side', 8, 4, 'spark', 'signal')],
    edges: [E('e1', 'tap', 'composition'), E('e2', 'composition', 'remembered'), E('e3', 'remembered', 'job'), E('e4', 'composition', 'side'), E('e5', 'job', 'composition')],
    metrics: [T('effects', 'launched'), T('effects', 'cancelled'), T('effects', 'disposed'), T('effects', 'side')]
  });
  /* CL (v2): cây composable của ví dụ Essentials Ch.21 với một CompositionLocalProvider. */
  V('locals', {
    layout: 'tree',
    nodes: [N('locals', 'c1', 0, 2, 'layers', 'runtime'), N('locals', 'c2', 4, -2, 'square', 'runtime'), N('locals', 'c4', 8, -2, 'square', 'runtime'), N('locals', 'c6', 12, -2, 'square', 'ui'),
      N('locals', 'prov', 4, 5, 'store', 'state'), N('locals', 'c3', 8, 5, 'square', 'ui'), N('locals', 'c5', 12, 5, 'square', 'runtime'), N('locals', 'c7', 16, 3, 'square', 'runtime'), N('locals', 'c8', 16, 7, 'square', 'ui')],
    edges: [E('e0', 'c1', 'c2'), E('e0b', 'c2', 'c4'), E('e0c', 'c4', 'c6'), E('e1', 'c1', 'prov'), E('e2', 'prov', 'c3'), E('e3', 'c3', 'c5'), E('e4', 'c5', 'c7'), E('e5', 'c5', 'c8')],
    metrics: [T('locals', 'recomposed'), T('locals', 'readers'), T('locals', 'provided')]
  });
  /* B6 (v2): cây R → B → (A, C) của ví dụ trong KDoc Applier. */
  V('insert', {
    layout: 'tree',
    nodes: [N('insert', 'r', 0, 0, 'layers', 'ui'), N('insert', 'b', 0, 4, 'square', 'ui'), N('insert', 'a', -3, 8, 'square', 'ui'), N('insert', 'c', 3, 8, 'square', 'ui')],
    edges: [E('e1', 'r', 'b'), E('e2', 'b', 'a'), E('e3', 'b', 'c')],
    metrics: [T('insert', 'notifications'), T('insert', 'inserts')]
  });
  /* B7 (v2): một state cuộn được đọc ở composition, layout (placement) hoặc draw; phase nào đọc thì phase đó chạy lại, rồi các phase sau. */
  V('scroll', {
    layout: 'pipeline', zoom: false,
    nodes: [N('scroll', 'state', 0, 4, 'frame', 'state'), N('scroll', 'comp', 4, 0, 'layers', 'runtime'), N('scroll', 'layout', 8, 4, 'grid', 'ui'), N('scroll', 'draw', 12, 8, 'spark', 'ui')],
    edges: [E('e1', 'state', 'comp'), E('e2', 'state', 'layout'), E('e3', 'state', 'draw'), E('e4', 'comp', 'layout'), E('e5', 'layout', 'draw'), E('e6', 'layout', 'state')],
    metrics: [T('scroll', 'comp'), T('scroll', 'layout'), T('scroll', 'draw'), T('scroll', 'frames')]
  });
  /* LO (v2): một Layout cha và ba con; cạnh là lời gọi measure/intrinsic từ cha xuống con. */
  V('measure', {
    layout: 'tree',
    nodes: [N('measure', 'parent', 0, 0, 'grid', 'ui'), N('measure', 'k1', -4, 5, 'square', 'ui'), N('measure', 'k2', 0, 5, 'square', 'ui'), N('measure', 'k3', 4, 5, 'square', 'ui')],
    edges: [E('e1', 'parent', 'k1'), E('e2', 'parent', 'k2'), E('e3', 'parent', 'k3')],
    metrics: [T('measure', 'measured'), T('measure', 'queries'), T('measure', 'height')]
  });
  /* MD (v2): chuỗi node modifier từ ngoài vào trong, kết thúc ở LayoutNode. */
  V('chain', {
    layout: 'pipeline', zoom: false,
    nodes: [N('chain', 'm1', 0, 0, 'square', 'runtime'), N('chain', 'm2', 4, 0, 'square', 'runtime'), N('chain', 'm3', 8, 0, 'square', 'runtime'), N('chain', 'm4', 12, 0, 'square', 'runtime'), N('chain', 'layout', 16, 0, 'grid', 'ui')],
    edges: [E('e1', 'm1', 'm2'), E('e2', 'm2', 'm3'), E('e3', 'm3', 'm4'), E('e4', 'm4', 'layout')],
    metrics: [T('chain', 'reused'), T('chain', 'updated'), T('chain', 'inserted'), T('chain', 'removed')]
  });
  /* LZ (v2): dữ liệu → khối đo của LazyLayout (SubcomposeLayout) → slot đang hiện; slot rời màn hình vào pool để dùng lại. */
  V('lazy', {
    layout: 'pipeline', zoom: false,
    nodes: [N('lazy', 'data', 0, 0, 'list', 'state'), N('lazy', 'measure', 4, 0, 'grid', 'runtime'), N('lazy', 'active', 8, -2, 'layers', 'ui'), N('lazy', 'pool', 8, 4, 'store', 'runtime')],
    edges: [E('e1', 'data', 'measure'), E('e2', 'measure', 'active'), E('e3', 'pool', 'active'), E('e4', 'active', 'pool')],
    metrics: [T('lazy', 'composed'), T('lazy', 'fresh'), T('lazy', 'reused'), T('lazy', 'pool')]
  });
  /* B8 (v2): Screen gọi Badge; blinkState được Badge đọc, nhưng thuộc scope nào tùy annotation. */
  V('annot', {
    layout: 'tree',
    nodes: [N('annot', 'screen', 0, 0, 'layers', 'runtime'), N('annot', 'badge', 0, 5, 'square', 'ui'), N('annot', 'state', 5, 5, 'frame', 'state')],
    edges: [E('e1', 'screen', 'badge'), E('e2', 'state', 'badge'), E('e3', 'state', 'screen')],
    metrics: [T('annot', 'screen'), T('annot', 'badge'), T('annot', 'changed')]
  });
  /* B9 (v2): cây UI → cây semantics → TalkBack và framework kiểm thử. */
  V('focus', {
    layout: 'pipeline', zoom: false,
    nodes: [N('focus', 'ui', 0, 0, 'list', 'ui'), N('focus', 'sem', 4, 0, 'eye', 'ui'), N('focus', 'a11y', 8, -2, 'phone', 'signal'), N('focus', 'test', 8, 4, 'check', 'job')],
    edges: [E('e1', 'ui', 'sem'), E('e2', 'sem', 'a11y'), E('e3', 'sem', 'test')],
    metrics: [T('focus', 'nodes'), T('focus', 'stops'), T('focus', 'actions')]
  });
  /* PF (v2): state cuộn/count → màn hình; derivedStateOf đứng giữa lọc thay đổi; mũi tên ngược là ghi ngược. */
  V('perf', {
    layout: 'pipeline', zoom: false,
    nodes: [N('perf', 'state', 0, 0, 'frame', 'state'), N('perf', 'derived', 4, 4, 'set', 'runtime'), N('perf', 'screen', 8, 0, 'layers', 'runtime')],
    edges: [E('e1', 'state', 'screen'), E('e2', 'screen', 'state'), E('e3', 'state', 'derived'), E('e4', 'derived', 'screen')],
    metrics: [T('perf', 'recomposed'), T('perf', 'value')]
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
