/* Model track I (thuần, không DOM, không câu chữ; chỉ message key). MÔ HÌNH GIẢNG DẠY (simplified).
   Nguồn: docs/research/sysdesign.md (tài liệu chính thức và sách system design, đọc từ 2026-11-24). */
(function () {
  'use strict';
  var K = 'track.sysdesign.';
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
    ADE.registerModel('sysdesign.' + m, def);
  }
  var sel = function (m, id, vals) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: id, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
  var setter = function (keys) { return function (s, a, v) { var n = {}; keys.forEach(function (k) { n[k] = s[k]; }); if (keys.indexOf(a) >= 0) n[a] = v; return n; }; };
  var nsOf = function (o) { var n = {}; Object.keys(o).forEach(function (k) { n[k] = K + 'st.' + o[k]; }); return n; };


  /* ================= I1: từ đề bài tới kế hoạch — làm theo bản thiết kế so với hỏi trước rồi mới làm =================
     Theo Tjeerd in 't Veen, Mobile System Design ch.2 (tìm yêu cầu phụ trước khi mở IDE; xin bản thiết kế với nội dung xấu nhất;
     bàn về lỗi sớm, ưu tiên lỗi không chặn màn hình; thống nhất với backend về phiên, token, timeout, mã lỗi, thông báo đẩy theo
     ngôn ngữ) và Alex Xu, System Design Interview tập 1 ch.2–3 (ước lượng nhanh bằng số tròn, ghi giả định và đơn vị; khung bốn
     bước, hỏi trước khi trả lời). Câu hỏi về mất mạng và trạng thái rỗng là bổ sung của site. Mọi con số là giả định minh họa. */
  (function () {
    var m = 'plan', CASES = ['mockup', 'asked'], KS = ['s1', 's2', 's3', 's4'];
    var Q = [['d1', 'designer'], ['d2', 'designer'], ['d3', 'designer'], ['b1', 'backend'], ['b2', 'backend'], ['b3', 'backend']];
    // trạng thái từng câu hỏi sau mỗi bước: '' chưa | 'asked' đã hỏi, có yêu cầu | 'late' lộ ra sau khi phát hành
    function qState(c, i, q) {
      if (c === 'asked') { if (q[1] === 'designer') return i >= 1 ? 'asked' : ''; return i >= 2 ? 'asked' : ''; }
      return i >= 3 ? 'late' : '';
    }
    // ước lượng dữ liệu di động: [ảnh mỗi ngày, KB mỗi ảnh] → MB mỗi tháng (30 ngày, làm tròn)
    var EST = { mockup: { photos: 2, kb: 4000 }, asked: { photos: 2, kb: 300 } };
    function mbMonth(c) { return Math.round(EST[c].photos * 30 * EST[c].kb / 1000); }
    ADE.sysPlan = { Q: Q, qState: qState, EST: EST, mbMonth: mbMonth };
    var TYPE = { mockup: ['scenario', 'mechanism', 'mechanism', 'pitfall'], asked: ['scenario', 'mechanism', 'mechanism', 'mechanism'] };
    var NODES = [['brief'], ['brief', 'designer'], ['brief', 'backend'], ['plan']];
    function steps(s) {
      return KS.map(function (k, i) {
        var type = TYPE[s.case][i], bad = type === 'pitfall';
        var asked = Q.filter(function (q) { return qState(s.case, i, q) === 'asked'; }).length, late = Q.filter(function (q) { return qState(s.case, i, q) === 'late'; }).length;
        var nodes = s.case === 'mockup' && (i === 1 || i === 2) ? ['brief', 'plan'] : NODES[i];
        var ns = {}; nodes.forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        if (s.case === 'mockup' && i >= 1) { ns.designer = K + 'st.skipped'; ns.backend = K + 'st.skipped'; }
        var o = S(m, s.case + '.' + k, { type: type, activeNodes: nodes, nodeStates: ns,
          metrics: { asked: asked, late: late, data: i === 3 ? mbMonth(s.case) : 0 },
          movingSignals: [], logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : 'observe'), subject: nodes[nodes.length - 1] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'mockup' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'hỏi trước: mọi câu hỏi có yêu cầu trước khi viết mã; làm theo bản thiết kế: mọi câu lộ ra sau khi phát hành', run: function () { return Q.every(function (q) { return qState('asked', 2, q) === 'asked' && qState('mockup', 3, q) === 'late'; }); } },
        { name: 'ước lượng: thu nhỏ ảnh trước khi gửi làm dữ liệu mỗi tháng giảm hơn 10 lần', run: function () { return mbMonth('mockup') > 10 * mbMonth('asked'); } },
        { name: 'mỗi cách có 4 bước', run: function () { return CASES.every(function (c) { return steps({ case: c }).length === 4; }); } }] });
  })();
})();
