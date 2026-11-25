/* View track L: sơ đồ node cho model rời rạc (tab phụ; tab chính là hình ở views/visuals.js). */
(function () {
  'use strict';
  var K = 'track.debugging.';
  var N = function (m, id, x, y, icon, tok) { return { id: id, x: x, y: y, icon: icon, tok: tok, labelKey: K + 'm.' + m + '.n.' + id }; };
  var E = function (id, f, t) { return { id: id, from: f, to: t }; };
  var T = function (m, id) { return { id: id, labelKey: K + 'm.' + m + '.met.' + id }; };
  function V(m, cfg) {
    var v = { titleKey: K + 'm.' + m + '.diagramTitle', descKey: K + 'm.' + m + '.diagramDesc', captionKey: K + 'cap.' + m, subjectKey: K + 'col.subject',
      stateFamilies: { surprise: 'fail' }, famKeys: { done: K + 'fam.done', fail: K + 'fam.fail', idle: K + 'fam.none' } };
    for (var k in cfg) v[k] = cfg[k];
    ADE.registerView('debugging.' + m, v);
  }
  /* l1: vòng tái hiện → thu hẹp → giả thuyết → kiểm (sai thì quay lại tái hiện); đúng thì sửa và khóa bằng test */
  V('loop', { layout: 'pipeline', nodes: [N('loop', 'repro', 0, 0, 'replay', 'ui'), N('loop', 'narrow', 3, 0, 'search', 'state'), N('loop', 'hypo', 6, 0, 'target', 'runtime'),
    N('loop', 'check', 6, 2, 'check', 'job'), N('loop', 'lock', 9, 2, 'source', 'state')],
    edges: [E('e1', 'repro', 'narrow'), E('e2', 'narrow', 'hypo'), E('e3', 'hypo', 'check'), E('e4', 'check', 'repro'), E('e5', 'check', 'lock')],
    metrics: [T('loop', 'crash'), T('loop', 'blank'), T('loop', 'releases'), T('loop', 'known')] });
  /* l2: luồng báo cáo → breakpoint → bảng biến; luồng đồng bộ → máy chủ (bị dừng theo hay không tùy chính sách) */
  V('bp', { layout: 'pipeline', nodes: [N('bp', 'report', 0, 0, 'thread', 'job'), N('bp', 'bp', 3, 0, 'pause', 'signal'), N('bp', 'vars', 6, 0, 'list', 'state'),
    N('bp', 'sync', 0, 2, 'thread', 'job'), N('bp', 'server', 6, 2, 'source', 'runtime')],
    edges: [E('e1', 'report', 'bp'), E('e2', 'bp', 'vars'), E('e3', 'bp', 'sync'), E('e4', 'sync', 'server')],
    metrics: [T('bp', 'stops'), T('bp', 'resumes'), T('bp', 'logs'), T('bp', 'sync')] });
  /* l3: lời gọi Log trong app (R8 có thể xóa lúc build) → buffer của logd ← hệ thống và app khác; Logcat đọc và lọc */
  V('logcat', { layout: 'pipeline', nodes: [N('logcat', 'app', 0, 0, 'source', 'ui'), N('logcat', 'r8', 0, 2, 'cross', 'signal'), N('logcat', 'logd', 3, 1, 'list', 'state'),
    N('logcat', 'others', 3, 3, 'layers', 'runtime'), N('logcat', 'view', 6, 1, 'search', 'job')],
    edges: [E('e1', 'r8', 'app'), E('e2', 'app', 'logd'), E('e3', 'others', 'logd'), E('e4', 'logd', 'view')],
    metrics: [T('logcat', 'shown'), T('logcat', 'app'), T('logcat', 'pii'), T('logcat', 'found')] });
  /* l4: tầng gốc → bọc thành tầng giữa → bọc thành tầng ngoài → crash */
  V('trace', { layout: 'pipeline', nodes: [N('trace', 'root', 0, 0, 'pitfall', 'signal'), N('trace', 'mid', 3, 0, 'layers', 'state'), N('trace', 'outer', 6, 0, 'layers', 'runtime'), N('trace', 'crash', 9, 0, 'cross', 'job')],
    edges: [E('e1', 'root', 'mid'), E('e2', 'mid', 'outer'), E('e3', 'outer', 'crash')],
    metrics: [T('trace', 'layers'), T('trace', 'frame'), T('trace', 'fixed')] });
})();
