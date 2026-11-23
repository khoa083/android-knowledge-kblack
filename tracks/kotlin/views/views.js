/* View track F: sơ đồ node cho model rời rạc (track kỹ thuật giữ sơ đồ node; chỉ UI/UX dùng màn hình mẫu). */
(function () {
  'use strict';
  var K = 'track.kotlin.';
  var N = function (m, id, x, y, icon, tok) { return { id: id, x: x, y: y, icon: icon, tok: tok, labelKey: K + 'm.' + m + '.n.' + id }; };
  var E = function (id, f, t) { return { id: id, from: f, to: t }; };
  var T = function (m, id) { return { id: id, labelKey: K + 'm.' + m + '.met.' + id }; };
  function V(m, cfg) {
    var v = { titleKey: K + 'm.' + m + '.diagramTitle', descKey: K + 'm.' + m + '.diagramDesc', captionKey: K + 'cap.' + m, subjectKey: K + 'col.subject',
      stateFamilies: { surprise: 'fail' }, famKeys: { done: K + 'fam.done', fail: K + 'fam.surprise' } };
    for (var k in cfg) v[k] = cfg[k];
    ADE.registerView('kotlin.' + m, v);
  }
  /* K1: mã nguồn → suy kiểu (biên dịch) → tính giá trị (chạy) → biến nhận kết quả */
  V('eval', { layout: 'pipeline', nodes: [N('eval', 'src', 0, 0, 'source', 'ui'), N('eval', 'types', 3, 0, 'target', 'state'), N('eval', 'eval', 6, 0, 'play', 'runtime'), N('eval', 'out', 9, 0, 'store', 'job')],
    edges: [E('e1', 'src', 'types'), E('e2', 'types', 'eval'), E('e3', 'eval', 'out')], metrics: [T('eval', 'type'), T('eval', 'value')] });
  /* K2: mã → kiểm null → luật smart cast của trình biên dịch → chỗ dùng */
  V('smartcast', { layout: 'pipeline', famKeys: { done: K + 'fam.done', fail: K + 'fam.fail', idle: K + 'fam.na' },
    nodes: [N('smartcast', 'src', 0, 0, 'source', 'ui'), N('smartcast', 'check', 3, 0, 'diamond', 'state'), N('smartcast', 'rule', 6, 0, 'target', 'runtime'), N('smartcast', 'use', 9, 0, 'play', 'job')],
    edges: [E('e1', 'src', 'check'), E('e2', 'check', 'rule'), E('e3', 'rule', 'use')], metrics: [T('smartcast', 'smart'), T('smartcast', 'fail')] });
})();
