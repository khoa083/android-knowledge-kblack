/* View track J: sơ đồ node cho model rời rạc (tab phụ; tab chính là hình ở views/visuals.js). */
(function () {
  'use strict';
  var K = 'track.cleancode.';
  var N = function (m, id, x, y, icon, tok) { return { id: id, x: x, y: y, icon: icon, tok: tok, labelKey: K + 'm.' + m + '.n.' + id }; };
  var E = function (id, f, t) { return { id: id, from: f, to: t }; };
  var T = function (m, id) { return { id: id, labelKey: K + 'm.' + m + '.met.' + id }; };
  function V(m, cfg) {
    var v = { titleKey: K + 'm.' + m + '.diagramTitle', descKey: K + 'm.' + m + '.diagramDesc', captionKey: K + 'cap.' + m, subjectKey: K + 'col.subject',
      stateFamilies: { surprise: 'fail' }, famKeys: { done: K + 'fam.done', fail: K + 'fam.fail', idle: K + 'fam.none' } };
    for (var k in cfg) v[k] = cfg[k];
    ADE.registerView('cleancode.' + m, v);
  }
  /* J1: mã → bộ nhớ làm việc; yêu cầu mới → mã; mã → hẹn nhắc */
  V('fits', { layout: 'pipeline', nodes: [N('fits', 'code', 0, 1.5, 'list', 'job'), N('fits', 'head', 4, 0, 'chip', 'state'), N('fits', 'change', 0, 3.5, 'source', 'ui'), N('fits', 'remind', 8, 1.5, 'clock', 'runtime')],
    edges: [E('e1', 'code', 'head'), E('e2', 'change', 'code'), E('e3', 'code', 'remind')],
    metrics: [T('fits', 'paths'), T('fits', 'vars'), T('fits', 'skipped')] });
  /* J2: chữ ký → tên → cài đặt → màn hình gọi */
  V('names', { layout: 'pipeline', nodes: [N('names', 'sig', 0, 1, 'eye', 'ui'), N('names', 'name', 3, 1, 'source', 'state'), N('names', 'impl', 6, 1, 'list', 'job'), N('names', 'screen', 9, 1, 'screen', 'runtime')],
    edges: [E('e1', 'sig', 'name'), E('e2', 'name', 'impl'), E('e3', 'impl', 'screen')],
    metrics: [T('names', 'right'), T('names', 'both'), T('names', 'second')] });
  /* J3: màn hình → ranh giới → kho dữ liệu → gửi SMS */
  V('parse', { layout: 'pipeline', nodes: [N('parse', 'screen', 0, 1, 'screen', 'ui'), N('parse', 'boundary', 3, 1, 'target', 'state'), N('parse', 'repo', 6, 1, 'store', 'job'), N('parse', 'sms', 9, 1, 'phone', 'runtime')],
    edges: [E('e1', 'screen', 'boundary'), E('e2', 'boundary', 'repo'), E('e3', 'repo', 'sms')],
    metrics: [T('parse', 'checks'), T('parse', 'form'), T('parse', 'late')] });
  /* J4: danh sách ví dụ → test → mã → bệnh nhân */
  V('tdd', { layout: 'pipeline', nodes: [N('tdd', 'list', 0, 1, 'list', 'state'), N('tdd', 'test', 3, 1, 'check', 'ui'), N('tdd', 'code', 6, 1, 'source', 'job'), N('tdd', 'patient', 9, 1, 'phone', 'runtime')],
    edges: [E('e1', 'list', 'test'), E('e2', 'test', 'code'), E('e3', 'code', 'patient')],
    metrics: [T('tdd', 'tests'), T('tdd', 'red'), T('tdd', 'wrong')] });
  /* J5: test → book() → chi tiết bên trong; thay đổi đi vào chi tiết */
  V('testDesign', { layout: 'pipeline', nodes: [N('testDesign', 'tests', 0, 1, 'check', 'ui'), N('testDesign', 'api', 3, 1, 'target', 'state'), N('testDesign', 'detail', 6, 1, 'layers', 'job'), N('testDesign', 'change', 9, 1, 'source', 'runtime')],
    edges: [E('e1', 'tests', 'api'), E('e2', 'api', 'detail'), E('e3', 'change', 'detail')],
    metrics: [T('testDesign', 'edges'), T('testDesign', 'broken'), T('testDesign', 'caught')] });
  /* J6: thay đổi → biên dịch → test → commit */
  V('refactor', { layout: 'pipeline', nodes: [N('refactor', 'edit', 0, 1, 'source', 'ui'), N('refactor', 'build', 3, 1, 'chip', 'job'), N('refactor', 'test', 6, 1, 'check', 'state'), N('refactor', 'commit', 9, 1, 'store', 'runtime')],
    edges: [E('e1', 'edit', 'build'), E('e2', 'build', 'test'), E('e3', 'test', 'commit')],
    metrics: [T('refactor', 'suspects'), T('refactor', 'lost'), T('refactor', 'release')] });
  /* J7: báo lỗi → test tái hiện → chọn commit → tốt hay xấu */
  V('bisect', { layout: 'pipeline', nodes: [N('bisect', 'report', 0, 1, 'phone', 'ui'), N('bisect', 'test', 3, 1, 'check', 'state'), N('bisect', 'pick', 6, 1, 'list', 'job'), N('bisect', 'verdict', 9, 1, 'target', 'runtime')],
    edges: [E('e1', 'report', 'test'), E('e2', 'test', 'pick'), E('e3', 'pick', 'verdict')],
    metrics: [T('bisect', 'probes'), T('bisect', 'left'), T('bisect', 'minutes')] });
  /* J8: nghiệp vụ → (giao diện ← chi tiết) → SDK */
  V('solid', { layout: 'pipeline', nodes: [N('solid', 'booking', 0, 1.5, 'job', 'ui'), N('solid', 'port', 4, 0, 'target', 'state'), N('solid', 'adapter', 4, 3, 'layers', 'job'), N('solid', 'sdk', 8, 1.5, 'store', 'runtime')],
    edges: [E('e1', 'booking', 'sdk'), E('e2', 'booking', 'port'), E('e3', 'adapter', 'port'), E('e4', 'adapter', 'sdk')],
    metrics: [T('solid', 'files'), T('solid', 'crash'), T('solid', 'detail')] });
  /* J9: đồ thị module → đếm Ca, Ce → tính I → chi phí build lại */
  V('components', { layout: 'pipeline', nodes: [N('components', 'graph', 0, 1, 'layers', 'ui'), N('components', 'count', 3, 1, 'list', 'state'), N('components', 'metric', 6, 1, 'target', 'job'), N('components', 'cost', 9, 1, 'clock', 'runtime')],
    edges: [E('e1', 'graph', 'count'), E('e2', 'count', 'metric'), E('e3', 'metric', 'cost')],
    metrics: [T('components', 'violations'), T('components', 'hot'), T('components', 'rebuilds')] });
})();
