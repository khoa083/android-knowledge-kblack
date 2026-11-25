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
  /* l5: mã nguồn → R8 (đổi tên, ghi mapping) → stack trace rối từ người dùng → retrace dùng mapping để dịch ngược */
  V('retrace', { layout: 'pipeline', nodes: [N('retrace', 'src', 0, 0, 'source', 'ui'), N('retrace', 'r8', 3, 0, 'mechanism', 'runtime'), N('retrace', 'map', 3, 2, 'list', 'state'),
    N('retrace', 'crash', 6, 0, 'pitfall', 'signal'), N('retrace', 'retrace', 6, 2, 'search', 'job')],
    edges: [E('e1', 'src', 'r8'), E('e2', 'r8', 'map'), E('e3', 'r8', 'crash'), E('e4', 'map', 'retrace')],
    metrics: [T('retrace', 'ok'), T('retrace', 'wrong'), T('retrace', 'cause')] });
  /* l6: cú chạm → hit test → lớp phủ (vẽ trên) hay nút; Layout Inspector cho thấy cả hai */
  V('layout', { layout: 'pipeline', nodes: [N('layout', 'tap', 0, 1, 'target', 'ui'), N('layout', 'hit', 3, 1, 'search', 'runtime'), N('layout', 'overlay', 6, 0, 'layers', 'signal'),
    N('layout', 'button', 6, 2, 'check', 'state'), N('layout', 'inspector', 3, 3, 'eye', 'job')],
    edges: [E('e1', 'tap', 'hit'), E('e2', 'hit', 'overlay'), E('e3', 'hit', 'button'), E('e4', 'inspector', 'hit')],
    metrics: [T('layout', 'under'), T('layout', 'hit'), T('layout', 'booked'), T('layout', 'cause')] });
  /* l7: app ghi vào database và xếp việc vào WorkManager; hai công cụ xem trạng thái của chúng */
  V('inspect', { layout: 'pipeline', nodes: [N('inspect', 'app', 0, 1, 'android', 'ui'), N('inspect', 'db', 3, 0, 'store', 'state'), N('inspect', 'wm', 3, 2, 'job', 'job'),
    N('inspect', 'dbi', 6, 0, 'search', 'runtime'), N('inspect', 'bti', 6, 2, 'search', 'runtime')],
    edges: [E('e1', 'app', 'db'), E('e2', 'app', 'wm'), E('e3', 'dbi', 'db'), E('e4', 'bti', 'wm')],
    metrics: [T('inspect', 'stored'), T('inspect', 'shown'), T('inspect', 'stuck'), T('inspect', 'cause')] });
  /* l8: GC root → BookingEventBus → listeners → lambda → DetailActivity đã đóng */
  V('leak', { layout: 'pipeline', nodes: [N('leak', 'root', 0, 0, 'target', 'runtime'), N('leak', 'bus', 3, 0, 'store', 'state'), N('leak', 'list', 6, 0, 'list', 'state'),
    N('leak', 'lambda', 6, 2, 'mechanism', 'signal'), N('leak', 'act', 9, 2, 'screen', 'ui')],
    edges: [E('e1', 'root', 'bus'), E('e2', 'bus', 'list'), E('e3', 'list', 'lambda'), E('e4', 'lambda', 'act')],
    metrics: [T('leak', 'opens'), T('leak', 'mem'), T('leak', 'inst'), T('leak', 'oom')] });
  /* l9: vsync → luồng main → RenderThread → màn hình; luồng nền parse song song */
  V('jank', { layout: 'pipeline', nodes: [N('jank', 'vsync', 0, 1, 'clock', 'runtime'), N('jank', 'main', 3, 1, 'thread', 'ui'), N('jank', 'render', 6, 1, 'thread', 'job'),
    N('jank', 'screen', 9, 1, 'screen', 'state'), N('jank', 'worker', 3, 3, 'thread', 'signal')],
    edges: [E('e1', 'vsync', 'main'), E('e2', 'main', 'render'), E('e3', 'render', 'screen'), E('e4', 'worker', 'main')],
    metrics: [T('jank', 'hz'), T('jank', 'budget'), T('jank', 'late'), T('jank', 'missed')] });
  /* l10: bấm Lưu → luồng main → khóa của BookingRepo ← luồng sync giữ trong lúc gọi mạng; StrictMode báo việc trên main */
  V('anr', { layout: 'pipeline', nodes: [N('anr', 'tap', 0, 1, 'target', 'ui'), N('anr', 'main', 3, 1, 'thread', 'ui'), N('anr', 'lock', 6, 1, 'forbidden', 'signal'),
    N('anr', 'sync', 9, 1, 'thread', 'job'), N('anr', 'strict', 3, 3, 'eye', 'runtime')],
    edges: [E('e1', 'tap', 'main'), E('e2', 'main', 'lock'), E('e3', 'sync', 'lock'), E('e4', 'strict', 'main')],
    metrics: [T('anr', 'net'), T('anr', 'wait'), T('anr', 'anr'), T('anr', 'viol')] });
  /* l11: màn hình → nguồn dữ liệu → OkHttp → radio; Network Inspector đọc các request */
  V('net', { layout: 'pipeline', nodes: [N('net', 'ui', 0, 1, 'screen', 'ui'), N('net', 'repo', 3, 1, 'store', 'state'), N('net', 'http', 6, 1, 'mechanism', 'job'),
    N('net', 'radio', 9, 1, 'bolt', 'signal'), N('net', 'ni', 6, 3, 'search', 'runtime')],
    edges: [E('e1', 'ui', 'repo'), E('e2', 'repo', 'http'), E('e3', 'http', 'radio'), E('e4', 'ni', 'http')],
    metrics: [T('net', 'req'), T('net', 'kb'), T('net', 'high'), T('net', 'low')] });
  /* l12: bản build gần release → nhiều lần chạy → trung vị và khoảng → kết luận; nhiễu tác động lên các lần chạy */
  V('measure', { layout: 'pipeline', nodes: [N('measure', 'build', 0, 1, 'source', 'ui'), N('measure', 'runs', 3, 1, 'replay', 'job'), N('measure', 'stats', 6, 1, 'list', 'state'),
    N('measure', 'claim', 9, 1, 'check', 'runtime'), N('measure', 'noise', 3, 3, 'pitfall', 'signal')],
    edges: [E('e1', 'build', 'runs'), E('e2', 'runs', 'stats'), E('e3', 'stats', 'claim'), E('e4', 'noise', 'runs')],
    metrics: [T('measure', 'runs'), T('measure', 'claim'), T('measure', 'mb'), T('measure', 'ma')] });
  /* l0: triệu chứng → lộ ra ở đâu → công cụ → chương */
  V('map', { layout: 'pipeline', nodes: [N('map', 'symptom', 0, 0, 'eye', 'ui'), N('map', 'phase', 3, 0, 'clock', 'state'), N('map', 'cause', 6, 0, 'search', 'runtime'), N('map', 'chapter', 9, 0, 'source', 'job')],
    edges: [E('e1', 'symptom', 'phase'), E('e2', 'phase', 'cause'), E('e3', 'cause', 'chapter')],
    metrics: [T('map', 'phase'), T('map', 'chapter')] });
})();
