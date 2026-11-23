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
  /* G2a: đồ thị phụ thuộc giữa các tầng (tab phụ; tab chính là hình đồ thị ở views/visuals.js) */
  V('layers', { layout: 'pipeline', nodes: [N('layers', 'ui', 0, 0, 'screen', 'ui'), N('layers', 'vm', 3, 0, 'layers', 'state'), N('layers', 'uc', 6, 0, 'mechanism', 'runtime'),
      N('layers', 'repo', 9, 0, 'store', 'runtime'), N('layers', 'api', 12, 0, 'source', 'job'), N('layers', 'dao', 12, 3, 'store', 'job')],
    edges: [E('e1', 'ui', 'vm'), E('e2', 'vm', 'uc'), E('e3', 'uc', 'repo'), E('e4', 'repo', 'api'), E('e5', 'repo', 'dao')],
    metrics: [T('layers', 'wrong'), T('layers', 'caught'), T('layers', 'test')] });
  /* G2b: vòng UDF: sự kiện đi lên nguồn sự thật, state đi xuống hai màn hình */
  V('ssot', { layout: 'cycle', nodes: [N('ssot', 'choose', 0, 3, 'screen', 'ui'), N('ssot', 'repo', 4, 0, 'store', 'state'), N('ssot', 'mine', 8, 3, 'screen', 'ui')],
    edges: [E('e1', 'choose', 'repo'), E('e2', 'repo', 'choose'), E('e3', 'mine', 'repo'), E('e4', 'repo', 'mine')],
    metrics: [T('ssot', 'copies'), T('ssot', 'writers'), T('ssot', 'agree')] });
  /* G3: Activity gửi sự kiện lên ViewModel; state hay sự kiện đi qua một kênh (StateFlow / SharedFlow) về Activity; Activity hiện thông báo */
  V('events', { layout: 'cycle', nodes: [N('events', 'act', 0, 3, 'screen', 'ui'), N('events', 'vm', 4, 0, 'layers', 'state'), N('events', 'flow', 8, 3, 'queue', 'state'), N('events', 'toast', 4, 6, 'phone', 'ui')],
    edges: [E('e1', 'act', 'vm'), E('e4', 'vm', 'flow'), E('e2', 'flow', 'act'), E('e3', 'act', 'toast')],
    metrics: [T('events', 'shown'), T('events', 'lost'), T('events', 'truth')] });
  /* G4: UI hỏi repository; repository đọc và ghi database, gọi mạng; dữ liệu đi ngược lên */
  V('offline', { layout: 'pipeline', nodes: [N('offline', 'ui', 0, 0, 'screen', 'ui'), N('offline', 'repo', 3, 0, 'store', 'runtime'), N('offline', 'db', 6, 0, 'store', 'state'), N('offline', 'net', 6, 3, 'source', 'job')],
    edges: [E('e1', 'ui', 'repo'), E('e2', 'repo', 'db'), E('e3', 'repo', 'net')],
    metrics: [T('offline', 'src'), T('offline', 'ui'), T('offline', 'db')] });
  /* G5: hai ViewModel, một use case, repository */
  V('usecase', { layout: 'pipeline', nodes: [N('usecase', 'choose', 0, 0, 'layers', 'state'), N('usecase', 'resched', 0, 3, 'layers', 'state'), N('usecase', 'uc', 4, 1.5, 'mechanism', 'runtime'), N('usecase', 'repo', 8, 1.5, 'store', 'job')],
    edges: [E('e1', 'choose', 'uc'), E('e2', 'resched', 'uc'), E('e3', 'uc', 'repo'), E('e4', 'choose', 'repo'), E('e5', 'resched', 'repo')],
    metrics: [T('usecase', 'copies'), T('usecase', 'agree'), T('usecase', 'extra')] });
  /* G6: Activity, ViewModel, repository, database theo chiều "ai giữ ai" */
  V('di', { layout: 'pipeline', nodes: [N('di', 'act', 0, 0, 'screen', 'ui'), N('di', 'vm', 3, 0, 'layers', 'state'), N('di', 'repo', 6, 0, 'store', 'runtime'), N('di', 'db', 9, 0, 'store', 'job')],
    edges: [E('e1', 'act', 'vm'), E('e2', 'vm', 'repo'), E('e3', 'repo', 'db'), E('e4', 'act', 'repo')],
    metrics: [T('di', 'inst'), T('di', 'hold'), T('di', 'when')] });
  /* G7: vòng màn hình → ViewModel (reducer) → state → màn hình */
  V('mvi', { layout: 'cycle', nodes: [N('mvi', 'ui', 0, 3, 'screen', 'ui'), N('mvi', 'vm', 4, 0, 'layers', 'runtime'), N('mvi', 'state', 8, 3, 'store', 'state')],
    edges: [E('e1', 'ui', 'vm'), E('e2', 'vm', 'state'), E('e3', 'state', 'ui')],
    metrics: [T('mvi', 'streams'), T('mvi', 'bad'), T('mvi', 'repr')] });
})();
