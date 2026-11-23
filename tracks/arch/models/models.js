/* Model track G (thuần, không DOM, không câu chữ; chỉ message key). MÔ HÌNH GIẢNG DẠY (simplified).
   Nguồn: docs/research/arch.md (developer.android.com đọc ngày 2026-11-23; sách Dumbravan, Boudjnah). */
(function () {
  'use strict';
  var K = 'track.arch.';
  var M = function (m, s) { return K + 'm.' + m + '.' + s; };
  function S(m, id, o) {
    o.id = id; o.type = o.type || 'mechanism';
    o.titleKey = o.titleKey || M(m, 's.' + id + '.title');
    o.explainKey = o.explainKey || M(m, 's.' + id + '.explain');
    o.params = o.params || {}; o.activeNodes = o.activeNodes || []; o.movingSignals = o.movingSignals || [];
    (o.logEvents || []).forEach(function (e) { if (!e.detailKey) e.detailKey = M(m, 'ev.' + id); if (!e.params) e.params = o.params; });
    return o;
  }
  function reg(m, def) {
    def.kind = 'discrete'; def.titleKey = M(m, 'title'); def.overviewKey = M(m, 'overview'); def.wrapupKey = M(m, 'wrapup');
    def.codeId = def.codeId || null; def.controlsHintKey = M(m, 'ctl.hint'); def.simplificationKeys = [M(m, 'simp.1')].concat(def.simpExtra || []);
    ADE.registerModel('arch.' + m, def);
  }
  var sel = function (m, id, vals) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: id, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
  var setter = function (keys) { return function (s, a, v) { var n = {}; keys.forEach(function (k) { n[k] = s[k]; }); if (keys.indexOf(a) >= 0) n[a] = v; return n; }; };

  /* ================= G1: Activity làm mọi thứ so với tách tầng — bốn phép thử: bấm, xoay màn hình, đổi API, kiểm thử =================
     Theo Guide to app architecture (component có thể bị hủy bất cứ lúc nào; tách mối quan tâm), Handle configuration changes
     (Activity bị hủy và tạo lại), ViewModel overview (giữ state qua thay đổi cấu hình), Testing fundamentals (local và instrumented).
     Số file phải sửa là đếm trong app mẫu Hẹn Khám (ba màn hình cùng gọi API giờ trống), chỉ để minh họa. */
  (function () {
    var m = 'god', CASES = ['god', 'layered'];
    var NODES = ['ui', 'vm', 'repo', 'source'];
    // mỗi bước: [node sáng, trạng thái node, số đo {keep, files, test}, loại bước, dòng mã, loại log, chủ thể]
    var P = {
      god: [[['ui'], { ui: 'done', vm: 'skipped', repo: 'skipped', source: 'skipped' }, { keep: 'na', files: 0, test: 'na' }, 'scenario', [1, 2, 3, 4, 5, 6, 7], 'run', 'ui'],
        [['ui'], { ui: 'surprise', vm: 'skipped', repo: 'skipped', source: 'skipped' }, { keep: 'no', files: 0, test: 'na' }, 'pitfall', [1, 2], 'observe', 'ui'],
        [['ui'], { ui: 'surprise', vm: 'skipped', repo: 'skipped', source: 'skipped' }, { keep: 'no', files: 3, test: 'na' }, 'pitfall', [4, 5], 'write', 'ui'],
        [['ui'], { ui: 'surprise', vm: 'skipped', repo: 'skipped', source: 'skipped' }, { keep: 'no', files: 3, test: 'device' }, 'pitfall', [3, 4, 5, 6], 'observe', 'ui']],
      layered: [[['ui', 'vm', 'repo', 'source'], { ui: 'done', vm: 'done', repo: 'done', source: 'done' }, { keep: 'na', files: 0, test: 'na' }, 'scenario', [1, 2, 3, 4, 5, 6, 7, 8], 'run', 'vm'],
        [['ui', 'vm'], { ui: 'done', vm: 'done', repo: 'done', source: 'done' }, { keep: 'yes', files: 0, test: 'na' }, 'mechanism', [2, 5, 6], 'observe', 'vm'],
        [['repo', 'source'], { ui: 'done', vm: 'done', repo: 'done', source: 'done' }, { keep: 'yes', files: 1, test: 'na' }, 'mechanism', [8, 9], 'write', 'source'],
        [['vm', 'repo'], { ui: 'done', vm: 'done', repo: 'done', source: 'done' }, { keep: 'yes', files: 1, test: 'local' }, 'mechanism', [10, 11, 12], 'complete', 'vm']]
    };
    ADE.archGod = P;
    var EDGE = { ui: null, vm: 'e1', repo: 'e2', source: 'e3' };
    function steps(s) {
      var K4 = ['tap', 'rotate', 'api', 'test'];
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var met = { keep: M(m, 'keep.' + p[2].keep), files: p[2].files, test: M(m, 'test.' + p[2].test) };
        var e = EDGE[p[0][0]] || EDGE[p[0][1]], bad = p[3] === 'pitfall';
        var o = S(m, s.case + '.' + K4[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: met, codeHighlight: { snippet: 'g1.' + s.case, lines: p[4] },
          movingSignals: e ? [{ edge: e, tok: bad ? 'signal' : 'state' }] : [], logEvents: [{ t: i, kind: p[5], subject: p[6] }] });
        if (i === 0) o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (i >= 1) o.callouts = [{ kind: bad ? 'pitfall' : 'source', textKey: M(m, 'co.' + s.case + '.' + K4[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'god' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi cách có 4 bước: bấm, xoay màn hình, đổi API, kiểm thử', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'Activity làm mọi thứ: mất dữ liệu khi xoay, phải sửa nhiều file, chỉ test được trên thiết bị', run: function () { var g = steps({ case: 'god' })[3].metrics; return g.keep === M(m, 'keep.no') && g.files > 1 && g.test === M(m, 'test.device'); } },
        { name: 'tách tầng: giữ dữ liệu qua xoay, sửa 1 file, test được trên máy (local)', run: function () { var l = steps({ case: 'layered' })[3].metrics; return l.keep === M(m, 'keep.yes') && l.files === 1 && l.test === M(m, 'test.local'); } }] });
  })();
})();
