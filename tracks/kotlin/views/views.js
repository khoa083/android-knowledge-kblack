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
  /* K3: điểm kích hoạt → khởi tạo lớp cha → khởi tạo lớp con / object → dùng */
  V('init', { layout: 'pipeline', famKeys: { done: K + 'fam.done', fail: K + 'fam.fail', idle: K + 'fam.na', run: K + 'fam.running' },
    nodes: [N('init', 'trigger', 0, 0, 'play', 'ui'), N('init', 'parent', 3, 0, 'layers', 'state'), N('init', 'child', 6, 0, 'square', 'runtime'), N('init', 'use', 9, 0, 'target', 'job')],
    edges: [E('e1', 'trigger', 'parent'), E('e2', 'parent', 'child'), E('e3', 'child', 'use')], metrics: [T('init', 'inits')] });
  /* K4: object → hashCode → bucket trong HashSet → tra cứu (contains / ==) */
  V('hashset', { layout: 'pipeline', famKeys: { done: K + 'fam.done', fail: K + 'fam.hashFail' },
    nodes: [N('hashset', 'obj', 0, 0, 'square', 'ui'), N('hashset', 'hash', 3, 0, 'grid', 'state'), N('hashset', 'bucket', 6, 0, 'layers', 'runtime'), N('hashset', 'lookup', 9, 0, 'search', 'job')],
    edges: [E('e1', 'obj', 'hash'), E('e2', 'hash', 'bucket'), E('e3', 'bucket', 'lookup')], metrics: [T('hashset', 'bucket'), T('hashset', 'size'), T('hashset', 'found')] });
  /* K5: khai báo kiểu → when / chuyển đổi → trình biên dịch kiểm → kết quả lúc chạy */
  V('sealed', { layout: 'pipeline', famKeys: { done: K + 'fam.done', fail: K + 'fam.fail', run: K + 'fam.running' },
    nodes: [N('sealed', 'def', 0, 0, 'layers', 'state'), N('sealed', 'when', 3, 0, 'diamond', 'ui'), N('sealed', 'compiler', 6, 0, 'target', 'runtime'), N('sealed', 'screen', 9, 0, 'phone', 'job')],
    edges: [E('e1', 'def', 'when'), E('e2', 'when', 'compiler'), E('e3', 'compiler', 'screen')], metrics: [T('sealed', 'covered'), T('sealed', 'total')] });
  /* K6: nơi gọi → hàm trong chuỗi gọi (ném) → try/catch khớp → finally / close */
  V('exception', { layout: 'pipeline', famKeys: { done: K + 'fam.done', fail: K + 'fam.excFail', idle: K + 'fam.na' },
    nodes: [N('exception', 'call', 0, 0, 'play', 'ui'), N('exception', 'fn', 3, 0, 'layers', 'state'), N('exception', 'handler', 6, 0, 'diamond', 'runtime'), N('exception', 'cleanup', 9, 0, 'store', 'job')],
    edges: [E('e1', 'call', 'fn'), E('e2', 'fn', 'handler'), E('e3', 'handler', 'cleanup')], metrics: [T('exception', 'exc'), T('exception', 'skipped'), T('exception', 'closed')] });
  /* K7: collection gốc → tham chiếu / ép kiểu → thao tác → bên đọc thấy gì */
  V('collections', { layout: 'pipeline', famKeys: { done: K + 'fam.done', fail: K + 'fam.collFail' },
    nodes: [N('collections', 'source', 0, 0, 'store', 'state'), N('collections', 'ref', 3, 0, 'layers', 'ui'), N('collections', 'op', 6, 0, 'play', 'runtime'), N('collections', 'result', 9, 0, 'search', 'job')],
    edges: [E('e1', 'source', 'ref'), E('e2', 'ref', 'op'), E('e3', 'op', 'result')], metrics: [T('collections', 'size'), T('collections', 'seen'), T('collections', 'type')] });
  /* K8: chỗ gọi → trình biên dịch (inline hay object hàm) → thân lambda chạy → kết quả (return thoát đâu, ai giữ lambda) */
  V('inline', { layout: 'pipeline', famKeys: { done: K + 'fam.done', fail: K + 'fam.collFail' },
    nodes: [N('inline', 'call', 0, 0, 'source', 'ui'), N('inline', 'compile', 3, 0, 'target', 'state'), N('inline', 'lambda', 6, 0, 'play', 'runtime'), N('inline', 'exit', 9, 0, 'square', 'job')],
    edges: [E('e1', 'call', 'compile'), E('e2', 'compile', 'lambda'), E('e3', 'lambda', 'exit')], metrics: [T('inline', 'objects'), T('inline', 'exit'), T('inline', 'captured')] });
  /* K9: danh sách gốc → filter → map → take / thao tác cuối */
  V('sequence', { layout: 'pipeline', famKeys: { done: K + 'fam.done', fail: K + 'fam.collFail', wait: K + 'fam.waiting', idle: K + 'fam.unused', run: K + 'fam.running' },
    nodes: [N('sequence', 'source', 0, 0, 'store', 'state'), N('sequence', 'filter', 3, 0, 'diamond', 'ui'), N('sequence', 'map', 6, 0, 'play', 'runtime'), N('sequence', 'terminal', 9, 0, 'target', 'job')],
    edges: [E('e1', 'source', 'filter'), E('e2', 'filter', 'map'), E('e3', 'map', 'terminal')], metrics: [T('sequence', 'ops'), T('sequence', 'inter'), T('sequence', 'touched')] });
  /* K10: khai báo kiểu (out / in / bất biến) → phép gán → trình biên dịch kiểm → gọi hàm qua biến */
  V('variance', { layout: 'pipeline', famKeys: { done: K + 'fam.done', fail: K + 'fam.fail' },
    nodes: [N('variance', 'decl', 0, 0, 'layers', 'state'), N('variance', 'assign', 3, 0, 'source', 'ui'), N('variance', 'compiler', 6, 0, 'target', 'runtime'), N('variance', 'call', 9, 0, 'play', 'job')],
    edges: [E('e1', 'decl', 'assign'), E('e2', 'assign', 'compiler'), E('e3', 'compiler', 'call')], metrics: [T('variance', 'variance'), T('variance', 'assign'), T('variance', 'safe')] });
  /* K2: mã → kiểm null → luật smart cast của trình biên dịch → chỗ dùng */
  V('smartcast', { layout: 'pipeline', famKeys: { done: K + 'fam.done', fail: K + 'fam.fail', idle: K + 'fam.na' },
    nodes: [N('smartcast', 'src', 0, 0, 'source', 'ui'), N('smartcast', 'check', 3, 0, 'diamond', 'state'), N('smartcast', 'rule', 6, 0, 'target', 'runtime'), N('smartcast', 'use', 9, 0, 'play', 'job')],
    edges: [E('e1', 'src', 'check'), E('e2', 'check', 'rule'), E('e3', 'rule', 'use')], metrics: [T('smartcast', 'smart'), T('smartcast', 'fail')] });
})();
