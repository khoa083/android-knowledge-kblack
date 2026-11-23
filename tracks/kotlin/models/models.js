/* Model track F (thuần, không DOM, không câu chữ; chỉ message key). MÔ HÌNH GIẢNG DẠY (simplified).
   Nguồn: docs/research/kotlin.md (kotlinlang.org đọc ngày 2026-11-23; sách Kotlin Essentials, Effective Kotlin). */
(function () {
  'use strict';
  var K = 'track.kotlin.';
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
    ADE.registerModel('kotlin.' + m, def);
  }
  var sel = function (m, id, vals) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: id, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
  var setter = function (keys) { return function (s, a, v) { var n = {}; keys.forEach(function (k) { n[k] = s[k]; }); if (keys.indexOf(a) >= 0) n[a] = v; return n; }; };

  /* ================= K1: một biểu thức đi từ mã nguồn qua suy kiểu (lúc biên dịch) tới giá trị (lúc chạy) =================
     Bốn trường hợp theo trang Numbers và Conditions and loops: chia nguyên, chia có Double, tràn Int, when có subject.
     Giá trị là kết quả tài liệu nêu (Int.MAX_VALUE + 1 = -2147483648), không tính bằng JavaScript. */
  (function () {
    var m = 'eval', CASES = ['intdiv', 'double', 'overflow', 'when'];
    // [kiểu kết quả, giá trị (số hoặc khóa chữ), loại bước cuối, dòng mã cho 4 bước]
    var C = {
      intdiv: { type: 'Int', value: 7, last: 'pitfall', lines: [[1, 2], [2], [2], [3]] },
      double: { type: 'Double', value: 7.5, last: 'mechanism', lines: [[1, 2], [2], [2], [3]] },
      overflow: { type: 'Int', value: -2147483648, last: 'pitfall', lines: [[1, 2], [2], [2], [3, 4]] },
      when: { type: 'String', value: M(m, 'val.pass'), last: 'mechanism', lines: [[1, 2], [2, 3, 4, 5], [3, 4], [2, 6]] }
    };
    function steps(s) {
      var c = C[s.case], sn = 'eval.' + s.case, typeKey = M(m, 'type.' + c.type);
      var hl = function (i) { return { snippet: sn, lines: c.lines[i] }; };
      return [
        S(m, s.case + '.code', { type: 'scenario', activeNodes: ['src'], codeHighlight: hl(0), callouts: [{ kind: 'try', textKey: M(m, 'co.try') }],
          logEvents: [{ t: 0, kind: 'observe', subject: 'src' }] }),
        S(m, s.case + '.types', { activeNodes: ['types'], movingSignals: [{ edge: 'e1', tok: 'state' }], codeHighlight: hl(1), metrics: { type: typeKey },
          nodeStates: { types: K + 'st.done' }, stateAfter: [{ labelKey: M(m, 'met.type'), valueKey: typeKey }],
          callouts: [{ kind: 'source', textKey: M(m, 'co.' + s.case + '.types') }], logEvents: [{ t: 1, kind: 'check', subject: 'types' }] }),
        S(m, s.case + '.run', { activeNodes: ['eval'], movingSignals: [{ edge: 'e2', tok: 'signal' }], codeHighlight: hl(2), metrics: { type: typeKey, value: c.value },
          nodeStates: { types: K + 'st.done', eval: K + 'st.done' }, logEvents: [{ t: 2, kind: 'run', subject: 'eval' }] }),
        S(m, s.case + '.result', { type: c.last, activeNodes: ['out'], movingSignals: [{ edge: 'e3', tok: 'state' }], codeHighlight: hl(3), metrics: { type: typeKey, value: c.value },
          nodeStates: { types: K + 'st.done', eval: K + 'st.done', out: K + (c.last === 'pitfall' ? 'st.surprise' : 'st.done') },
          callouts: [{ kind: c.last === 'pitfall' ? 'pitfall' : 'mechanism', textKey: M(m, 'co.' + s.case + '.result') }],
          logEvents: [{ t: 3, kind: 'write', subject: 'out' }] })
      ];
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'intdiv' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi trường hợp có 4 bước; bước 2 (vị trí 2) luôn là suy kiểu', run: function () { return CASES.every(function (k) { var st = steps({ case: k }); return st.length === 4 && st[1].activeNodes[0] === 'types'; }); } },
        { name: 'chia nguyên cho 7, có Double cho 7.5; tràn Int cho -2147483648 (giá trị tài liệu)', run: function () { return C.intdiv.value === Math.trunc(15 / 2) && C.double.value === 15 / 2 && C.overflow.value === (2147483647 + 1) - 4294967296; } },
        { name: 'chia nguyên và tràn số là bẫy (bước cuối loại pitfall)', run: function () { return steps({ case: 'intdiv' })[3].type === 'pitfall' && steps({ case: 'overflow' })[3].type === 'pitfall' && steps({ case: 'double' })[3].type === 'mechanism'; } }] });
  })();
})();
