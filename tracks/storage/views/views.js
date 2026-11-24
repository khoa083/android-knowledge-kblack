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
  /* H2: app, hệ thống, file trên đĩa */
  V('file', { layout: 'pipeline', nodes: [N('file', 'app', 0, 0, 'phone', 'ui'), N('file', 'disk', 6, 0, 'store', 'state'), N('file', 'sys', 3, 3, 'android', 'runtime')],
    edges: [E('e1', 'app', 'disk'), E('e2', 'sys', 'app')],
    metrics: [T('file', 'file'), T('file', 'lost')] });
  /* H3: main thread, luồng IO, file trên đĩa */
  V('prefs', { layout: 'pipeline', nodes: [N('prefs', 'main', 0, 0, 'thread', 'ui'), N('prefs', 'io', 3, 3, 'thread', 'runtime'), N('prefs', 'disk', 6, 0, 'store', 'state')],
    edges: [E('e1', 'main', 'disk'), E('e2', 'io', 'disk')],
    metrics: [T('prefs', 'main'), T('prefs', 'saved')] });
  /* H4: DAO (interface) → mã Room sinh → SQLite → kết quả (Flow hay danh sách) */
  V('room', { layout: 'pipeline', nodes: [N('room', 'dao', 0, 0, 'source', 'ui'), N('room', 'impl', 3, 0, 'mechanism', 'runtime'), N('room', 'sqlite', 6, 0, 'store', 'state'), N('room', 'out', 9, 0, 'screen', 'job')],
    edges: [E('e1', 'dao', 'impl'), E('e2', 'impl', 'sqlite'), E('e3', 'sqlite', 'out')],
    metrics: [T('room', 'shown'), T('room', 'runs')] });
  /* H5: bảng doctor, bảng appointment, đồng bộ nền ghi chen vào, kết quả ghép */
  V('rel', { layout: 'pipeline', nodes: [N('rel', 'doctors', 0, 0, 'store', 'state'), N('rel', 'appts', 3, 0, 'store', 'state'), N('rel', 'result', 6, 0, 'screen', 'ui'), N('rel', 'sync', 3, 3, 'job', 'runtime')],
    edges: [E('e1', 'doctors', 'appts'), E('e2', 'appts', 'result'), E('e3', 'sync', 'appts')],
    metrics: [T('rel', 'q'), T('rel', 'dup')] });
  /* H6: app mới → Room mở database → file database của người dùng */
  V('mig', { layout: 'pipeline', nodes: [N('mig', 'app', 0, 0, 'phone', 'ui'), N('mig', 'room', 4, 0, 'mechanism', 'runtime'), N('mig', 'db', 8, 0, 'store', 'state')],
    edges: [E('e1', 'app', 'room'), E('e2', 'room', 'db')],
    metrics: [T('mig', 'ver'), T('mig', 'rows'), T('mig', 'st')] });
})();
