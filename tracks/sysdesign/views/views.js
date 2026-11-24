/* View track I: sơ đồ node cho model rời rạc (tab phụ; tab chính là hình ở views/visuals.js). */
(function () {
  'use strict';
  var K = 'track.sysdesign.';
  var N = function (m, id, x, y, icon, tok) { return { id: id, x: x, y: y, icon: icon, tok: tok, labelKey: K + 'm.' + m + '.n.' + id }; };
  var E = function (id, f, t) { return { id: id, from: f, to: t }; };
  var T = function (m, id) { return { id: id, labelKey: K + 'm.' + m + '.met.' + id }; };
  function V(m, cfg) {
    var v = { titleKey: K + 'm.' + m + '.diagramTitle', descKey: K + 'm.' + m + '.diagramDesc', captionKey: K + 'cap.' + m, subjectKey: K + 'col.subject',
      stateFamilies: { surprise: 'fail' }, famKeys: { done: K + 'fam.done', fail: K + 'fam.fail', idle: K + 'fam.none' } };
    for (var k in cfg) v[k] = cfg[k];
    ADE.registerView('sysdesign.' + m, v);
  }
  /* I1: đề bài → designer, backend → kế hoạch */
  V('plan', { layout: 'pipeline', nodes: [N('plan', 'brief', 0, 1.5, 'source', 'ui'), N('plan', 'designer', 4, 0, 'eye', 'state'), N('plan', 'backend', 4, 3, 'job', 'runtime'), N('plan', 'plan', 8, 1.5, 'list', 'job')],
    edges: [E('e1', 'brief', 'designer'), E('e2', 'brief', 'backend'), E('e3', 'designer', 'plan'), E('e4', 'backend', 'plan')],
    metrics: [T('plan', 'asked'), T('plan', 'late'), T('plan', 'data')] });
  /* I2: app → Camera; Camera làm thiếu RAM → lmkd; lmkd giết app; app ↔ bản sao saved state */
  V('process', { layout: 'pipeline', nodes: [N('process', 'app', 0, 1.5, 'phone', 'ui'), N('process', 'camera', 4, 0, 'eye', 'runtime'), N('process', 'lmkd', 8, 1.5, 'cross', 'job'), N('process', 'store', 4, 3, 'store', 'state')],
    edges: [E('e1', 'app', 'camera'), E('e2', 'camera', 'lmkd'), E('e3', 'lmkd', 'app'), E('e4', 'app', 'store')],
    metrics: [T('process', 'fields'), T('process', 'free'), T('process', 'starts')] });
  /* I3: hai luồng bên trái, hai khóa bên phải */
  V('lock', { layout: 'pipeline', nodes: [N('lock', 'main', 0, 0, 'thread', 'ui'), N('lock', 'sync', 0, 3, 'thread', 'runtime'), N('lock', 'cache', 6, 0, 'list', 'state'), N('lock', 'db', 6, 3, 'store', 'job')],
    edges: [E('e1', 'main', 'cache'), E('e2', 'main', 'db'), E('e3', 'sync', 'cache'), E('e4', 'sync', 'db')],
    metrics: [T('lock', 'blocked'), T('lock', 'anr'), T('lock', 'cycle')] });
  /* I4: app ↔ server trực tiếp, hoặc server → FCM → app */
  V('channel', { layout: 'pipeline', nodes: [N('channel', 'app', 0, 1.5, 'phone', 'ui'), N('channel', 'fcm', 4, 0, 'queue', 'runtime'), N('channel', 'server', 8, 1.5, 'store', 'job')],
    edges: [E('e1', 'app', 'server'), E('e2', 'fcm', 'app'), E('e3', 'server', 'fcm')],
    metrics: [T('channel', 'reqs'), T('channel', 'latency'), T('channel', 'bg')] });
  /* I5: app → mạng → server; response đi ngược lại */
  V('retry', { layout: 'pipeline', nodes: [N('retry', 'app', 0, 1, 'phone', 'ui'), N('retry', 'net', 4, 1, 'rail', 'signal'), N('retry', 'server', 8, 1, 'store', 'job')],
    edges: [E('e1', 'app', 'net'), E('e2', 'net', 'server')],
    metrics: [T('retry', 'attempts'), T('retry', 'bookings'), T('retry', 'peak')] });
  /* I6: màn hình → bộ nhớ → đĩa → server */
  V('cache', { layout: 'pipeline', nodes: [N('cache', 'ui', 0, 1, 'screen', 'ui'), N('cache', 'mem', 3, 1, 'chip', 'state'), N('cache', 'disk', 6, 1, 'store', 'job'), N('cache', 'net', 9, 1, 'source', 'runtime')],
    edges: [E('e1', 'ui', 'mem'), E('e2', 'mem', 'disk'), E('e3', 'disk', 'net')],
    metrics: [T('cache', 'kb'), T('cache', 'right'), T('cache', 'net')] });
  /* I7: màn tin → PagingSource → server; người biên tập đổi danh sách trên server */
  V('paging', { layout: 'pipeline', nodes: [N('paging', 'ui', 0, 1, 'screen', 'ui'), N('paging', 'pager', 3, 1, 'list', 'state'), N('paging', 'server', 6, 1, 'store', 'job'), N('paging', 'editor', 9, 1, 'source', 'runtime')],
    edges: [E('e1', 'ui', 'pager'), E('e2', 'pager', 'server'), E('e3', 'editor', 'server')],
    metrics: [T('paging', 'dup'), T('paging', 'miss'), T('paging', 'gone')] });
  /* I8: máy tính bảng và điện thoại cùng ghi lên một server */
  V('conflict', { layout: 'pipeline', nodes: [N('conflict', 'tablet', 0, 0, 'screen', 'ui'), N('conflict', 'phone', 0, 3, 'phone', 'state'), N('conflict', 'server', 6, 1.5, 'store', 'job')],
    edges: [E('e1', 'tablet', 'server'), E('e2', 'phone', 'server')],
    metrics: [T('conflict', 'lost'), T('conflict', 'writes'), T('conflict', 'ask')] });
  /* I9: server phòng khám → dịch vụ đẩy → app; app tự tải lại từ server */
  V('push', { layout: 'pipeline', nodes: [N('push', 'srv', 0, 1.5, 'store', 'job'), N('push', 'push', 4, 0, 'queue', 'runtime'), N('push', 'app', 8, 1.5, 'phone', 'ui')],
    edges: [E('e1', 'srv', 'push'), E('e2', 'push', 'app'), E('e3', 'app', 'srv')],
    metrics: [T('push', 'right'), T('push', 'shown'), T('push', 'fetch')] });
})();
