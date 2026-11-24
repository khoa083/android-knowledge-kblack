/* Model track J (thuần, không DOM, không câu chữ; chỉ message key). MÔ HÌNH GIẢNG DẠY (simplified).
   Nguồn: docs/research/cleancode.md (sách của Seemann, Martin, Moskała và tài liệu chính thức, đọc từ 2026-11-24). */
(function () {
  'use strict';
  var K = 'track.cleancode.';
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
    ADE.registerModel('cleancode.' + m, def);
  }
  var sel = function (m, id, vals) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: id, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
  var setter = function (keys) { return function (s, a, v) { var n = {}; keys.forEach(function (k) { n[k] = s[k]; }); if (keys.indexOf(a) >= 0) n[a] = v; return n; }; };
  var range = function (a, b) { var r = []; for (var x = a; x <= b; x++) r.push(x); return r; };

  /* ================= J1: mã phải vừa trong đầu — một hàm dài so với ba hàm nhỏ =================
     Theo Seemann, Code That Fits in Your Head: ch.3 (trí nhớ ngắn hạn 4–7 mẩu, 7 là con số tượng trưng), ch.7 (ngưỡng; cyclomatic
     complexity: bắt đầu 1, mỗi if/for cộng 1; luật 80/24; 7.2.7 đếm biến cục bộ, tham số, field); Martin, Clean Code ch.3 (một việc,
     một mức trừu tượng, stepdown). MỘT nguồn sự thật cho mọi con số: danh sách nhánh và biến của từng hàm bên dưới; hình, chỉ số và
     selfChecks đều tính từ đây. Dòng khớp tracks/cleancode/code.js. */
  (function () {
    var m = 'fits', CASES = ['long', 'split'], KS = ['s1', 's2', 's3', 's4'], LIMIT = 7, SEEMANN_LINES = 24;
    var P = 'param', F = 'field', L = 'local';
    // mỗi hàm: đoạn mã, tên, dòng đầu–cuối, nhánh [dòng, từ khóa], biến [tên, loại, dòng xuất hiện đầu], dòng hẹn nhắc
    var FN = {
      long: { snip: 'j1.long', name: 'bookAppointment', from: 1, to: 19, remind: 17,
        br: [[2, 'if'], [4, 'if'], [6, 'if'], [8, 'if'], [9, 'if'], [10, 'for'], [12, 'if'], [16, 'if']],
        vars: [['req', P, 1], ['doctor', L, 3], ['doctors', F, 3], ['slot', L, 5], ['clock', F, 6], ['fee', L, 7], ['code', L, 10], ['v', L, 11], ['vouchers', F, 11],
          ['booking', L, 14], ['repo', F, 15], ['hours', L, 16], ['reminders', F, 17]] },
      longFree: { snip: 'j1.longFree', name: 'bookAppointment', from: 1, to: 23, remind: 21,
        br: [[2, 'if'], [4, 'if'], [6, 'if'], [8, 'if'], [9, 'if'], [10, 'for'], [12, 'if'], [14, 'if'], [20, 'if']],
        vars: [['req', P, 1], ['doctor', L, 3], ['doctors', F, 3], ['slot', L, 5], ['clock', F, 6], ['fee', L, 7], ['code', L, 10], ['v', L, 11], ['vouchers', F, 11],
          ['free', L, 15], ['booking', L, 18], ['repo', F, 19], ['hours', L, 20], ['reminders', F, 21]] },
      book: { snip: 'j1.split', name: 'bookAppointment', from: 1, to: 9, remind: 7,
        br: [[3, 'if']], vars: [['req', P, 1], ['doctor', L, 2], ['fee', L, 4], ['booking', L, 5], ['repo', F, 6], ['reminders', F, 7]] },
      validate: { snip: 'j1.split', name: 'validate', from: 11, to: 15,
        br: [[12, 'if'], [13, 'if']], vars: [['req', P, 11], ['clock', F, 13], ['doctors', F, 14]] },
      feeFor: { snip: 'j1.split', name: 'feeFor', from: 17, to: 22,
        br: [[19, 'if'], [20, 'if']], vars: [['doctor', P, 17], ['req', P, 17], ['fee', L, 18], ['vouchers', F, 21]] },
      feeFree: { snip: 'j1.splitFree', name: 'feeFor', from: 17, to: 22,
        br: [[19, 'if'], [20, 'if']], vars: [['doctor', P, 17], ['req', P, 17], ['fee', L, 18], ['vouchers', F, 21]] }
    };
    // mỗi bước: hàm đang đọc, đọc tới dòng nào, dòng tô sáng; skip: nhánh mới có bỏ qua dòng hẹn nhắc không
    var STEPS = {
      long: [{ f: 'long', upTo: 6, hl: range(2, 6) }, { f: 'long', upTo: 13, hl: range(7, 13) }, { f: 'long', upTo: 19, hl: range(14, 18) },
        { f: 'longFree', upTo: 23, hl: [14, 15, 16, 17, 21], fresh: [14], skip: true }],
      split: [{ f: 'book', upTo: 9, hl: range(2, 8) }, { f: 'validate', upTo: 15, hl: range(12, 14) }, { f: 'feeFor', upTo: 22, hl: range(18, 21) },
        { f: 'feeFree', upTo: 22, hl: [21, 7], fresh: [21], skip: false }]
    };
    function view(c, i) {
      var st = STEPS[c][i], fn = FN[st.f], prev = i > 0 && STEPS[c][i - 1].f === st.f ? STEPS[c][i - 1].upTo : fn.from - 1;
      var br = fn.br.filter(function (b) { return b[0] <= st.upTo; }), vars = fn.vars.filter(function (v) { return v[2] <= st.upTo; });
      var isNew = function (line) { return st.fresh ? st.fresh.indexOf(line) >= 0 : line > prev; };
      return { step: st, fn: fn, br: br, vars: vars, paths: 1 + br.length, nVars: vars.length, lines: fn.to - fn.from + 1, isNew: isNew,
        over: 1 + br.length > LIMIT || vars.length > LIMIT };
    }
    // bảng đếm: hàm dài đếm một hàm; bản tách cộng dồn các hàm đã đọc, mỗi hàm bắt đầu lại từ 1
    function tableFns(c, i) {
      if (c === 'long') return [STEPS.long[i].f];
      var out = [];   // feeFree là feeFor sau khi sửa: thay chỗ, không thêm hàng
      STEPS.split.slice(0, i + 1).forEach(function (s) {
        var j = s.f === 'feeFree' ? out.indexOf('feeFor') : -1;
        if (j >= 0) out[j] = s.f; else if (out.indexOf(s.f) < 0) out.push(s.f);
      });
      return out;
    }
    ADE.ccFits = { FN: FN, STEPS: STEPS, LIMIT: LIMIT, SEEMANN_LINES: SEEMANN_LINES, view: view, tableFns: tableFns };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var v = view(c, i), st = v.step, last = i === 3;
        var type = i === 0 ? 'scenario' : (last && st.skip ? 'pitfall' : 'mechanism');
        var nodes = last ? ['change', 'code', 'remind'] : ['code', 'head'];
        var ns = { code: K + 'st.done', head: K + 'st.' + (v.over ? 'surprise' : 'done') };
        if (last) { ns.change = K + 'st.done'; ns.remind = K + 'st.' + (st.skip ? 'surprise' : 'done'); }
        var o = S(m, c + '.' + k, { type: type, activeNodes: nodes, nodeStates: ns,
          metrics: { paths: v.paths, vars: v.nVars, skipped: st.skip ? 1 : 0 },
          codeHighlight: { snippet: v.fn.snip, lines: st.hl },
          movingSignals: [{ edge: last ? (st.skip ? 'e3' : 'e2') : 'e1', tok: v.over || st.skip ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: last ? (st.skip ? 'exception' : 'write') : 'observe', subject: last ? 'remind' : 'head' }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (type === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    var SNIP_LEN = { 'j1.long': 19, 'j1.longFree': 23, 'j1.split': 22, 'j1.splitFree': 22 };
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'long' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'hàm dài: 9 đường đi, 13 biến, 19 dòng (dưới 24); thêm yêu cầu mới: 10 đường đi, 14 biến, 23 dòng', run: function () {
          var a = view('long', 2), b = view('long', 3); return a.paths === 9 && a.nVars === 13 && a.lines === 19 && a.lines < SEEMANN_LINES && b.paths === 10 && b.nVars === 14 && b.lines === 23; } },
        { name: 'hàm dài vượt 7 từ bước 2; mọi hàm của bản tách không quá 7 ở cả hai cách đếm', run: function () {
          return !view('long', 0).over && view('long', 1).over && [0, 1, 2, 3].every(function (i) { var v = view('split', i); return !v.over && v.paths <= 3 && v.nVars <= 6; }); } },
        { name: 'nhánh mới của hàm dài nằm trước dòng hẹn nhắc (bị bỏ qua); bản tách giữ nguyên bookAppointment', run: function () {
          return FN.longFree.br.some(function (b) { return b[0] === 14; }) && 14 < FN.longFree.remind && STEPS.long[3].skip && !STEPS.split[3].skip && FN.book.remind === 7; } },
        { name: 'mọi dòng tô sáng và mọi dòng nhánh, biến nằm trong đoạn mã', run: function () {
          var ok = Object.keys(FN).every(function (f) { var fn = FN[f], n = SNIP_LEN[fn.snip]; return fn.to <= n && fn.br.every(function (b) { return b[0] >= fn.from && b[0] <= fn.to; }) && fn.vars.every(function (v) { return v[2] >= fn.from && v[2] <= fn.to; }); });
          return ok && CASES.every(function (c) { return steps({ case: c }).length === 4 && STEPS[c].every(function (st) { var n = SNIP_LEN[FN[st.f].snip]; return st.hl.every(function (l) { return l >= 1 && l <= n; }); }); }); } }] });
  })();
})();
