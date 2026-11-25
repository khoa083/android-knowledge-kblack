/* Model track L (thuần, không DOM, không câu chữ; chỉ message key). MÔ HÌNH GIẢNG DẠY (simplified).
   Nguồn: docs/research/debugging.md (tài liệu chính thức developer.android.com, đọc từ 2026-11-25). */
(function () {
  'use strict';
  var K = 'track.debugging.';
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
    ADE.registerModel('debugging.' + m, def);
  }
  var sel = function (m, id, vals) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: id, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
  var setter = function (keys) { return function (s, a, v) { var n = {}; keys.forEach(function (k) { n[k] = s[k]; }); if (keys.indexOf(a) >= 0) n[a] = v; return n; }; };

  /* ================= l1: vòng gỡ lỗi: crash "thỉnh thoảng" ở màn chi tiết; đoán rồi sửa, hay tái hiện, thu hẹp, giả thuyết, kiểm =================
     CÀI THẬT: 8 kịch bản thao tác, mỗi cái có làm màn hình bị tạo lại không (xoay, giao diện tối, ngôn ngữ, tiến trình bị đóng rồi mở lại).
     Kết quả của một kịch bản với một bản sửa được TÍNH: không tạo lại → bình thường; tạo lại → crash, trừ khi bản sửa cố định dọc (xoay không còn
     tạo lại), phép kiểm isInitialized (thành màn trống) hay truyền id qua arguments (bình thường). Kịch bản và bản sửa là của site. */
  (function () {
    var m = 'loop', CASES = ['guess', 'method'], KS = ['s1', 's2', 's3', 's4'];
    // [id, làm màn hình bị tạo lại bằng cách nào: null | 'rotate' | 'config' | 'process']
    var SC = [['openBack', null], ['rotate', 'rotate'], ['scroll', null], ['dark', 'config'], ['home', null], ['kill', 'process'], ['lang', 'config'], ['wait', null]];
    function recreated(sc, patch) { return sc[1] !== null && !(sc[1] === 'rotate' && (patch === 'portrait' || patch === 'check')); }
    function outcome(sc, patch) {
      if (!recreated(sc, patch)) return 'ok';
      if (patch === 'args') return 'ok';
      return patch === 'check' ? 'blank' : 'crash';
    }
    var PATCH = { guess: ['portrait', 'check', 'check', 'check'], method: ['none', 'none', 'none', 'args'] };
    var RELEASES = { guess: [1, 2, 2, 3], method: [0, 0, 0, 1] };
    function tally(patch) { var c = 0, b = 0; SC.forEach(function (sc) { var o = outcome(sc, patch); if (o === 'crash') c++; if (o === 'blank') b++; }); return { crash: c, blank: b }; }
    // giả thuyết "crash khi và chỉ khi màn hình bị tạo lại" khớp mọi kịch bản khi chưa sửa
    function hypothesisHolds() { return SC.every(function (sc) { return (outcome(sc, 'none') === 'crash') === (sc[1] !== null); }); }
    ADE.dbgLoop = { SC: SC, outcome: outcome, recreated: recreated, PATCH: PATCH, tally: tally };
    var NODES = { guess: [[[], 'lock'], [[], 'lock'], [[], 'lock'], [[], 'lock']],
      method: [[['repro'], 'repro'], [['repro', 'narrow'], 'narrow'], [['hypo', 'check'], 'check'], [['check', 'lock'], 'lock']] };
    var EDGE = { method: ['e1', 'e1', 'e3', 'e5'] };
    var CODE = { guess: ['l1.guess', 'l1.guess', 'l1.guess', 'l1.guess'], method: ['l1.bug', 'l1.bug', 'l1.bug', 'l1.fix'] };
    var HL = { guess: [[1, 2], [7], [7], [2, 7]], method: [[5], [5], [3], [2, 5, 9]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var p = PATCH[c][i], t = tally(p), bad = c === 'guess', nd = NODES[c][i], ns = {};
        ns[nd[1]] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          params: { patch: p },
          metrics: { crash: t.crash, blank: t.blank, releases: RELEASES[c][i], known: M(m, c === 'method' && i >= 2 ? 'known.yes' : 'known.no') },
          codeHighlight: { snippet: CODE[c][i], lines: HL[c][i] },
          movingSignals: bad ? [] : [{ edge: EDGE.method[i], tok: 'state' }],
          logEvents: [{ t: i, kind: bad ? (t.crash ? 'exception' : 'skip') : (i === 3 ? 'complete' : (i === 0 ? 'observe' : 'run')), subject: nd[1] }] });
        var tryIt = i === 0 && c === 'guess';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : (i === 3 ? 'mechanism' : 'source')), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    var LEN = { 'l1.guess': 10, 'l1.bug': 7, 'l1.fix': 10 };
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'guess' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'chưa sửa: 4 trên 8 kịch bản crash (2, 4, 6, 7), không màn trống', run: function () { var t = tally('none'); return t.crash === 4 && t.blank === 0 && SC.length === 8 &&
          SC.map(function (sc, i) { return outcome(sc, 'none') === 'crash' ? i + 1 : 0; }).filter(Boolean).join() === '2,4,6,7'; } },
        { name: 'cố định dọc: còn 3 crash; thêm phép kiểm: 0 crash nhưng 3 màn trống; truyền id qua arguments: 0 và 0', run: function () {
          var a = tally('portrait'), b = tally('check'), c = tally('args'); return a.crash === 3 && a.blank === 0 && b.crash === 0 && b.blank === 3 && c.crash === 0 && c.blank === 0; } },
        { name: 'giả thuyết "crash khi và chỉ khi màn hình bị tạo lại" khớp cả 8 kịch bản', run: hypothesisHolds },
        { name: 'mỗi cách 4 bước; cách đoán tốn 3 bản phát hành, cách có phương pháp 1; mọi dòng tô sáng nằm trong đoạn mã', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l, i) { return l.every(function (x) { return x >= 1 && x <= LEN[CODE[c][i]]; }); }); }) &&
            RELEASES.guess[3] === 3 && RELEASES.method[3] === 1; } }] });
  })();
})();
