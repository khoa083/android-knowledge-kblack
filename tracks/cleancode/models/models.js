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

  /* ================= J2: che tên, đoán đọc hay ghi — bản trộn so với bản tách command và query =================
     Theo Seemann 8.1.5 (X out names: đoán từ kiểu), 8.1.6 (CQS: command không trả dữ liệu, query không có side effect), 8.1.7;
     Martin, Clean Code ch.2–3 (tên lộ ý định, side effect là lời nói dối, set trả Boolean, tham số cờ); Moskała, Effective Kotlin
     Item 15 (property là trạng thái, không phải hành vi). Bảng ROWS là nguồn sự thật; số "đoán đúng" tính từ đó. */
  (function () {
    var m = 'names', CASES = ['mixed', 'cqs'], KS = ['s1', 's2', 's3', 's4'];
    var READ_GUESS = ['query', 'ask', 'state', 'lookup'];   // đoán là chỉ đọc; còn lại (command, unknown) là đoán có ghi
    // [khóa, chữ ký với tên che, đoán, tên thật, việc thật, loại thật r|w|rw|slow, dòng chữ ký, dòng cài đặt]
    var ROWS = {
      mixed: [['getAll', 'fun xxx(): List<Appointment>', 'query', 'getAppointments()', 'getAll', 'rw', 2, [3, 4, 5]],
        ['save', 'fun xxx(Appointment): Boolean', 'ask', 'save(a)', 'save', 'rw', 7, [8]],
        ['process', 'fun xxx(String, Boolean)', 'unknown', 'process(data2, flag)', 'process', 'w', 9, [10]],
        ['nextFree', 'val xxx: Slot', 'state', 'nextFree', 'nextFree', 'slow', 12, [13]]],
      cqs: [['appointments', 'fun xxx(): List<Appointment>', 'query', 'appointments()', 'appointments', 'r', 2, [2]],
        ['clear', 'fun xxx()', 'unknown', 'clearExpiredCache()', 'clear', 'w', 3, [3]],
        ['add', 'fun xxx(Appointment)', 'command', 'add(a)', 'add', 'w', 4, [4]],
        ['cancel', 'fun xxx(AppointmentId)', 'command', 'cancel(id)', 'cancel', 'w', 5, [5]],
        ['reschedule', 'fun xxx(AppointmentId, Slot)', 'command', 'reschedule(id, to)', 'reschedule', 'w', 6, [6]],
        ['find', 'suspend fun xxx(DoctorId): Slot?', 'lookup', 'findNextFreeSlot(doctor)', 'find', 'r', 7, [7]]]
    };
    function right(r) { var rd = READ_GUESS.indexOf(r[2]) >= 0; return rd ? r[5] === 'r' : r[5] === 'w'; }
    // màn hình gọi hai lần khi mất mạng: [trả về, cache sau đó] cho mỗi lần gọi; cache ban đầu 3 lịch hẹn
    var CALLS = { mixed: [[3, 0], [0, 0]], cqs: [[3, 3], [3, 3]] };
    var SNIP = { mixed: 'j2.mixed', cqs: 'j2.cqs' };
    function hlLines(c, i) {
      if (i === 3) return c === 'mixed' ? [3, 4, 5] : [2];
      return ROWS[c].reduce(function (acc, r) { return acc.concat(i < 2 ? [r[6]] : r[7]); }, []);
    }
    ADE.ccNames = { ROWS: ROWS, CALLS: CALLS, right: right };
    function steps(s) {
      var c = s.case, rows = ROWS[c];
      var nRight = rows.filter(right).length, nBoth = rows.filter(function (r) { return r[5] === 'rw'; }).length;
      return KS.map(function (k, i) {
        var bad = (i === 2 && nRight < rows.length) || (i === 3 && CALLS[c][1][0] === 0);
        var node = ['sig', 'name', 'impl', 'screen'][i];
        var ns = {}; ns[node] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: i === 0 ? ['sig'] : [['sig', 'name'], ['name', 'impl'], ['impl', 'screen']][i - 1], nodeStates: ns,
          metrics: { right: i >= 2 ? nRight : 0, both: i >= 2 ? nBoth : 0, second: i === 3 ? CALLS[c][1][0] : 0 },
          codeHighlight: { snippet: SNIP[c], lines: hlLines(c, i) },
          movingSignals: i === 0 ? [] : [{ edge: 'e' + i, tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'run' : 'observe'), subject: node }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    var LEN = { 'j2.mixed': 14, 'j2.cqs': 8 };
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'mixed' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'bản trộn: đoán đúng 1/4, hai hàm vừa đọc vừa ghi; bản CQS: đoán đúng 6/6, không hàm nào vừa đọc vừa ghi', run: function () {
          return ROWS.mixed.filter(right).length === 1 && ROWS.mixed.filter(function (r) { return r[5] === 'rw'; }).length === 2 && ROWS.cqs.filter(right).length === 6 && ROWS.cqs.every(function (r) { return r[5] !== 'rw'; }); } },
        { name: 'bản CQS: chữ ký có kiểu trả về thì là query (chỉ đọc), không có thì là command (ghi)', run: function () {
          return ROWS.cqs.every(function (r) { var ret = /\)\s*:/.test(r[1]); return ret ? r[5] === 'r' : r[5] === 'w'; }); } },
        { name: 'gọi hai lần khi mất mạng: bản trộn lần hai trả 0, bản CQS trả 3 cả hai lần', run: function () { return CALLS.mixed[1][0] === 0 && CALLS.cqs[0][0] === 3 && CALLS.cqs[1][0] === 3; } },
        { name: 'mỗi bản 4 bước; mọi dòng tô sáng nằm trong đoạn mã', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && [0, 1, 2, 3].every(function (i) { return hlLines(c, i).every(function (l) { return l >= 1 && l <= LEN[SNIP[c]]; }); }); }); } }] });
  })();

  /* ================= J3: kiểm rải rác so với parse một lần ở ranh giới =================
     Theo Seemann 5.2.4 (Postel: dễ dãi đầu vào, fail fast), 5.3 (hiểu biết mất sau khi kiểm), 5.3.1 (luôn hợp lệ, kiểm ở constructor),
     7.2.5 (parse, don't validate); Kotlin docs inline value classes (init + require; khác typealias). Các luật dưới đây được CÀI THẬT
     bằng JS: kết quả từng ô của hình tính từ chúng, không gõ tay. Luật số di động là minh họa của site. */
  (function () {
    var m = 'parse', CASES = ['validate', 'parse'], KS = ['s1', 's2', 's3', 's4'];
    var RULE = {   // ba luật rải rác của ba màn hình (cố ý khác nhau) và luật thứ tư ở bộ gửi SMS
      booking: function (s) { return s.replace(/ /g, '').length === 10; },
      profile: function (s) { return s.indexOf('+84') === 0 || s.indexOf('0') === 0; },
      reminder: function (s) { return s.length >= 9; }
    };
    function smsOk(s) { return /^0\d{9}$/.test(s.replace(/ /g, '')); }
    function parsePhone(raw) { var d = raw.replace(/\D/g, ''), local = d.indexOf('84') === 0 ? '0' + d.slice(2) : d; return /^0[35789]\d{8}$/.test(local) ? local : null; }
    var INPUTS = [['booking', '0912 345 678'], ['profile', '+84 912 345 678'], ['reminder', '091234567']];
    // một hàng của hình: giá trị ở từng chặng và nó có phải số sai đang đi tiếp không
    function row(c, x) {
      var from = x[0], raw = x[1], p = parsePhone(raw);
      if (c === 'validate') { var pass = RULE[from](raw), ok = pass && smsOk(raw); return { from: from, raw: raw, edge: pass ? 'pass.' + from : 'rejected', inside: pass ? 'string' : 'stopped', sms: !pass ? 'none' : (ok ? 'sent' : 'failed'), badLeak: pass && !p, value: null }; }
      return { from: from, raw: raw, edge: p ? 'parsed' : 'rejected', inside: p ? 'typed' : 'stopped', sms: p ? 'sent' : 'none', badLeak: false, value: p };
    }
    function rows(c) { return INPUTS.map(function (x) { return row(c, x); }); }
    function tally(c) { var r = rows(c); return { checks: c === 'validate' ? 4 : 1, form: r.filter(function (x) { return x.edge === 'rejected'; }).length, late: r.filter(function (x) { return x.sms === 'failed'; }).length }; }
    var HL = { validate: [[1], [2, 3, 4], [7], [11, 12]], parse: [[7], [8, 9, 10], [2, 3, 13], [14]] };
    ADE.ccParse = { rows: rows, tally: tally };
    function steps(s) {
      var c = s.case, t = tally(c);
      return KS.map(function (k, i) {
        var bad = c === 'validate' && (i === 3 || i === 2), node = ['screen', 'boundary', 'repo', 'sms'][i];
        var ns = {}; ns[node] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: i === 0 ? ['screen'] : [['screen', 'boundary'], ['boundary', 'repo'], ['repo', 'sms']][i - 1], nodeStates: ns,
          metrics: { checks: i === 0 ? 0 : (c === 'validate' && i < 3 ? 3 : t.checks), form: i >= 1 ? t.form : 0, late: i === 3 ? t.late : 0 },
          codeHighlight: { snippet: 'j3.' + c, lines: HL[c][i] },
          movingSignals: i === 0 ? [] : [{ edge: 'e' + i, tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : 'run'), subject: node }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        if (c === 'validate' && i === 1) o.callouts[0].kind = 'pitfall';
        return o;
      });
    }
    var LEN = { 'j3.validate': 15, 'j3.parse': 14 };
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'validate' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'kiểm rải rác: cả ba số qua kiểm ở màn hình, một số sai thật lọt vào trong, hai SMS hỏng lúc gửi (một do số sai, một do luật thứ tư khác)', run: function () {
          var r = rows('validate'); return r.every(function (x) { return x.edge !== 'rejected'; }) && r.filter(function (x) { return x.badLeak; }).length === 1 && tally('validate').late === 2; } },
        { name: 'parse: +84 chuẩn hóa thành 0912345678, số thiếu chữ số bị từ chối tại form, không SMS nào hỏng', run: function () {
          var r = rows('parse'); return r[0].value === '0912345678' && r[1].value === '0912345678' && r[2].edge === 'rejected' && tally('parse').late === 0 && tally('parse').form === 1; } },
        { name: 'số +84 hợp lệ nhưng luật thứ tư của bản rải rác vẫn từ chối (luật khác nhau, không phải số sai)', run: function () { return parsePhone('+84 912 345 678') !== null && !smsOk('+84 912 345 678'); } },
        { name: 'mỗi cách 4 bước; mọi dòng tô sáng nằm trong đoạn mã', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= LEN['j3.' + c]; }); }); }); } }] });
  })();

  /* ================= J4: viết mã trước so với TDD cho hàm phí khám =================
     Theo Martin, Clean Craftsmanship ch.2 (ba luật, luật thứ tư refactor), Clean Code ch.9; Seemann 5.2.2 (Red Green Refactor), 6.2.2
     (Devil's Advocate, tam giác hóa), 11.2 (đừng tin test chưa thấy đỏ). Năm phiên bản hàm phí được CÀI THẬT dưới đây; trạng thái
     từng test (đỏ, xanh, đã thấy đỏ) tính bằng cách chạy chúng, không gõ tay. Phí tính theo nghìn đồng. */
  (function () {
    var m = 'tdd', CASES = ['after', 'tdd'], KS = ['s1', 's2', 's3', 's4'];
    // ví dụ: [khóa, thứ trong tuần (1 = thứ hai … 7 = chủ nhật), là ngày lễ, phí mong đợi]; ngày đã kiểm thứ trong lịch 2026
    var EX = [['mon', 1, false, 200], ['sat', 6, false, 300], ['sun', 7, false, 300], ['hol', 3, true, 400]];
    var weekend = function (d) { return d === 6 || d === 7; };
    var V = {
      after: function (d) { return weekend(d) ? 300 : 200; },
      t1: function () { return 200; },
      t2: function (d) { return d === 6 ? 300 : 200; },
      t3: function (d) { return weekend(d) ? 300 : 200; },
      t4: function (d, hol) { return hol ? 400 : (weekend(d) ? 300 : 200); }
    };
    var run = function (ver, ex) { return V[ver](ex[1], ex[2]); };
    // mỗi bước: phiên bản mã, các test đã viết, pha đã đi trong bước, dòng tô sáng
    var PLAN = {
      after: [{ ver: 'after', tests: [], walk: ['code'], hl: [1, 2, 3] }, { ver: 'after', tests: ['mon', 'sat'], walk: ['green'], hl: [4] },
        { ver: 'after', tests: ['mon', 'sat'], walk: ['green'], hl: [4] }, { ver: 'after', tests: ['mon', 'sat'], walk: ['prod'], hl: [3], prod: 'hol' }],
      tdd: [{ ver: 't1', prev: null, tests: ['mon'], walk: ['red', 'green'], hl: [2] }, { ver: 't2', prev: 't1', tests: ['mon', 'sat'], walk: ['red', 'green'], hl: [2, 3] },
        { ver: 't3', prev: 't2', tests: ['mon', 'sat', 'sun'], walk: ['red', 'green', 'refactor'], hl: [2, 4, 5] }, { ver: 't4', prev: 't3', tests: ['mon', 'sat', 'sun', 'hol'], walk: ['red', 'green', 'refactor'], hl: [1, 3, 4, 5, 6] }]
    };
    var exOf = function (k) { return EX.filter(function (e) { return e[0] === k; })[0]; };
    // một test đã từng đỏ? Với TDD: test mới phải đỏ với phiên bản trước (hoặc chưa có hàm) — tính bằng cách chạy
    function seenRed(c, i, k) {
      if (c !== 'tdd') return false;
      for (var j = 0; j <= i; j++) { var p = PLAN.tdd[j]; if (p.tests.indexOf(k) >= 0) { return p.prev === null || run(p.prev, exOf(k)) !== exOf(k)[3]; } }
      return false;
    }
    function rows(c, i) {
      var p = PLAN[c][i];
      return EX.map(function (e) {
        var written = p.tests.indexOf(e[0]) >= 0, got = run(p.ver, e), fresh = c === 'tdd' ? p.tests[p.tests.length - 1] === e[0] : (i === 1 && written) || p.prod === e[0];
        return { k: e[0], want: e[3], written: written, pass: got === e[3], got: got, seen: written && seenRed(c, i, e[0]), prod: p.prod === e[0], fresh: fresh };
      });
    }
    function wrongDays(c, i) { return PLAN[c][i].prod ? rows(c, i).filter(function (r) { return r.prod && !r.pass; }).length : 0; }
    ADE.ccTdd = { PLAN: PLAN, rows: rows };
    var SNIP = function (c, i) { return 'j4.' + PLAN[c][i].ver; };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var r = rows(c, i), bad = wrongDays(c, i) > 0, nodes = c === 'tdd' ? ['list', 'test', 'code'] : [['code'], ['code', 'test'], ['test'], ['code', 'patient']][i];
        var ns = {}; nodes.forEach(function (n) { ns[n] = K + 'st.done'; }); if (bad) ns.patient = K + 'st.surprise';
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nodes, nodeStates: ns,
          metrics: { tests: r.filter(function (x) { return x.written; }).length, red: r.filter(function (x) { return x.seen; }).length, wrong: wrongDays(c, i) },
          codeHighlight: { snippet: SNIP(c, i), lines: PLAN[c][i].hl },
          movingSignals: [{ edge: bad ? 'e3' : (c === 'tdd' ? 'e2' : 'e1'), tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (PLAN[c][i].walk.indexOf('refactor') >= 0 ? 'write' : 'run'), subject: bad ? 'patient' : nodes[nodes.length - 1] }] });
        o.callouts = [{ kind: i === 0 && c === 'after' ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 && c === 'after' ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        if (c === 'after' && i === 2) o.callouts[0].kind = 'pitfall';
        return o;
      });
    }
    var LEN = { 'j4.after': 4, 'j4.t1': 2, 'j4.t2': 3, 'j4.t3': 5, 'j4.t4': 10 };
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'after' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'TDD: mỗi test mới đỏ với phiên bản trước và xanh với phiên bản sau; cuối cùng 4/4 xanh, 4/4 đã thấy đỏ', run: function () {
          var ok = PLAN.tdd.every(function (p) { var k = p.tests[p.tests.length - 1], e = exOf(k); return (p.prev === null || run(p.prev, e) !== e[3]) && run(p.ver, e) === e[3]; });
          var last = rows('tdd', 3); return ok && last.every(function (x) { return x.pass && x.seen; }); } },
        { name: 'tam giác hóa: bản chỉ kiểm thứ bảy (t2) qua test thứ hai và thứ bảy nhưng sai chủ nhật', run: function () { return run('t2', exOf('mon')) === 200 && run('t2', exOf('sat')) === 300 && run('t2', exOf('sun')) !== 300; } },
        { name: 'viết mã trước: hai test xanh ngay, không test nào từng đỏ; ngày lễ 2/9 tính 200 thay vì 400', run: function () {
          var r = rows('after', 3); return r.filter(function (x) { return x.written && x.pass; }).length === 2 && r.every(function (x) { return !x.seen; }) && run('after', exOf('hol')) === 200 && wrongDays('after', 3) === 1; } },
        { name: 'mỗi cách 4 bước; mọi dòng tô sáng nằm trong đoạn mã', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && [0, 1, 2, 3].every(function (i) { return PLAN[c][i].hl.every(function (l) { return l >= 1 && l <= LEN[SNIP(c, i)]; }); }); }); } }] });
  })();

  /* ================= J5: test mock từng lời gọi so với test kiểm kết quả với fake =================
     Theo Martin, Clean Craftsmanship ch.3 (test double theo Meszaros; mock là spy biết kỳ vọng; spy, mock làm test dễ vỡ; London/Chicago),
     ch.4 (fragile test là vấn đề thiết kế; Rule 12); Seemann 4.2.2 (AAA), 11.1. Danh sách cạnh EDGES là nguồn sự thật:
     số cạnh, test vỡ sau mỗi refactor (test có cạnh vào thứ vừa đổi) và test bắt được lỗi đều tính từ đó. */
  (function () {
    var m = 'testDesign', CASES = ['mock', 'behavior'], KS = ['s1', 's2', 's3', 's4'];
    var TESTS = ['t1', 't2', 't3', 't4'];
    var NODES = [['book', 'pub'], ['validate', 'int'], ['feeFor', 'int'], ['save', 'int'], ['schedule', 'int'], ['FakeRepo', 'fake'], ['FakeReminders', 'fake']];
    var EDGES = {
      mock: { t1: ['book', 'validate', 'feeFor', 'save'], t2: ['book', 'feeFor', 'save'], t3: ['book', 'schedule', 'save'], t4: ['book', 'validate', 'save'] },
      behavior: { t1: ['book', 'FakeRepo'], t2: ['book', 'FakeRepo'], t3: ['book', 'FakeReminders'], t4: ['book', 'FakeRepo'] }
    };
    // mỗi bước: những gì đổi (refactor A, refactor B, lỗi phí); refactor không đổi hành vi
    var CHANGE = [[], ['validate', 'feeFor'], ['save', 'schedule', 'FakeRepo'], ['feeFor']];   // giao diện Repo đổi ở B: FakeRepo sửa một chỗ
    var BUG_STEP = 3, CHECKS_FEE = 't2';   // chỉ test t2 khẳng định con số phí
    var kindOf = function (n) { return NODES.filter(function (x) { return x[0] === n; })[0][1]; };
    function edgeCount(c) { return TESTS.reduce(function (s, t) { return s + EDGES[c][t].length; }, 0); }
    // refactor: test vỡ nếu nó chạm vào chi tiết bên trong vừa đổi (fake đổi thì sửa fake một chỗ, test không đổi)
    function brokenAt(c, i) { if (i === 0 || i === BUG_STEP) return []; return TESTS.filter(function (t) { return EDGES[c][t].some(function (n) { return CHANGE[i].indexOf(n) >= 0 && kindOf(n) === 'int'; }); }); }
    // lỗi phí: test bắt được nếu nó khẳng định con số phí VÀ mã tính phí thật chạy trong test (không bị mock)
    function caught(c) { var t = CHECKS_FEE; return EDGES[c][t].indexOf('feeFor') < 0 ? [t] : []; }
    function fakeEdits(c, i) { return c === 'behavior' && i === 2 ? 1 : 0; }
    ADE.ccTestDesign = { TESTS: TESTS, NODES: NODES, EDGES: EDGES, CHANGE: CHANGE, BUG_STEP: BUG_STEP, brokenAt: brokenAt, caught: caught, edgeCount: edgeCount, fakeEdits: fakeEdits };
    var HL = { mock: [[2, 3, 4], [3, 6], [7], [3]], behavior: [[2, 3, 5, 7], [5], [2], [7]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var br = brokenAt(c, i).length, miss = i === BUG_STEP && caught(c).length === 0, bad = br > 0 || miss;
        var nodes = i === 0 ? ['tests', 'api'] : ['change', 'detail', 'tests'];
        var ns = {}; nodes.forEach(function (n) { ns[n] = K + 'st.done'; }); if (bad) ns.tests = K + 'st.surprise';
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nodes, nodeStates: ns,
          metrics: { edges: edgeCount(c), broken: br, caught: i === BUG_STEP ? caught(c).length : 0 },
          codeHighlight: { snippet: 'j5.' + c, lines: HL[c][i] },
          movingSignals: [{ edge: i === 0 ? 'e1' : 'e3', tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 0 ? 'observe' : 'write'), subject: i === 0 ? 'tests' : 'detail' }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 && c === 'mock' ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        if (c === 'behavior' && i === 2) o.callouts[0].kind = 'source';
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'mock' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mock từng lời gọi: 13 cạnh; refactor A vỡ 3/4, refactor B vỡ 4/4; lỗi phí: 0 test bắt được', run: function () {
          return edgeCount('mock') === 13 && brokenAt('mock', 1).length === 3 && brokenAt('mock', 2).length === 4 && caught('mock').length === 0; } },
        { name: 'kiểm kết quả với fake: 8 cạnh, không cạnh nào vào chi tiết bên trong; refactor không vỡ test nào; lỗi phí: test phí cuối tuần bắt được', run: function () {
          var noInt = TESTS.every(function (t) { return EDGES.behavior[t].every(function (n) { return kindOf(n) !== 'int'; }); });
          return edgeCount('behavior') === 8 && noInt && brokenAt('behavior', 1).length === 0 && brokenAt('behavior', 2).length === 0 && caught('behavior')[0] === 't2'; } },
        { name: 'mỗi cách 4 bước; mọi dòng tô sáng nằm trong đoạn mã (8 dòng)', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= 8; }); }); }); } }] });
  })();

  /* ================= J6: đổi tại chỗ một lần so với song song từng bước nhỏ (strangler) =================
     Theo Martin, Clean Craftsmanship ch.5 (chuỗi thay đổi nhỏ, test xanh sau MỖI thay đổi; nhỏ tới mức không gỡ lỗi; không để test đỏ quá vài
     phút; cấu trúc mới song song rồi chuyển dần; chừa đường lui) và Seemann 10.2, A.24 (strangler). Bảng CELLS là nguồn sự thật: số thay đổi
     bị nghi = số ô đang "nghi" hay ô đỏ ở bước đó; phút bỏ đi tính từ ô hoàn tác. Thời gian và số lỗi là minh họa. */
  (function () {
    var m = 'refactor', CASES = ['big', 'small'], KS = ['s1', 's2', 's3', 's4'], STEP_MIN = 15, DAY_MIN = 300;
    var COLS = { big: ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8'], small: ['c1', 'c2', 'c3', 'c4', 'c4b', 'c5', 'c6', 'c7', 'c8'] };
    // trạng thái [test, commit] của từng cột sau mỗi bước (null = chưa làm)
    var CELLS = {
      big: [
        { c1: ['nobuild', 'no'], c2: ['nobuild', 'no'], c3: ['nobuild', 'no'], c4: ['nobuild', 'no'] },
        { c1: ['nobuild', 'no'], c2: ['nobuild', 'no'], c3: ['nobuild', 'no'], c4: ['nobuild', 'no'], c5: ['nobuild', 'no'], c6: ['nobuild', 'no'], c7: ['nobuild', 'no'], c8: ['nobuild', 'no'] },
        { c1: ['sus', 'no'], c2: ['sus', 'no'], c3: ['sus', 'no'], c4: ['sus', 'no'], c5: ['sus', 'no'], c6: ['sus', 'no'], c7: ['sus', 'no'], c8: ['sus', 'no'] },
        { c1: ['gone', 'no'], c2: ['gone', 'no'], c3: ['gone', 'no'], c4: ['gone', 'no'], c5: ['gone', 'no'], c6: ['gone', 'no'], c7: ['gone', 'no'], c8: ['gone', 'no'] }],
      small: [
        { c1: ['green', 'yes'], c2: ['green', 'yes'] },
        { c1: ['green', 'yes'], c2: ['green', 'yes'], c3: ['green', 'yes'], c4: ['red', 'undo'] },
        { c1: ['green', 'yes'], c2: ['green', 'yes'], c3: ['green', 'yes'], c4: ['red', 'undo'], c4b: ['green', 'yes'], c5: ['green', 'yes'], c6: ['green', 'yes'] },
        { c1: ['green', 'yes'], c2: ['green', 'yes'], c3: ['green', 'yes'], c4: ['red', 'undo'], c4b: ['green', 'yes'], c5: ['green', 'yes'], c6: ['green', 'yes'], c7: ['green', 'yes'], c8: ['green', 'yes'] }]
    };
    var BUILD = { big: [17, 40, 0, 0], small: [0, 0, 0, 0] }, RED = { big: [null, null, 3, 0], small: [0, 1, 0, 0] };
    function fresh(c, i) { var now = CELLS[c][i], prev = i > 0 ? CELLS[c][i - 1] : {}; return COLS[c].filter(function (k) { return now[k] && (!prev[k] || prev[k][0] !== now[k][0]); }); }
    function suspects(c, i) { var now = CELLS[c][i]; if (c === 'big') return COLS.big.filter(function (k) { return now[k] && (now[k][0] === 'sus' || now[k][0] === 'gone'); }).length;
      return fresh(c, i).filter(function (k) { return now[k][0] === 'red'; }).length; }
    function lost(c, i) { var now = CELLS[c][i]; if (c === 'big') return now.c1 && now.c1[0] === 'gone' ? DAY_MIN : 0; return COLS.small.filter(function (k) { return now[k] && now[k][1] === 'undo'; }).length * STEP_MIN; }
    function releasable(c, i) { var now = CELLS[c][i]; return COLS[c].every(function (k) { return !now[k] || now[k][0] === 'green' || now[k][1] === 'undo' || now[k][0] === 'gone'; }) ? 1 : 0; }
    ADE.ccRefactor = { COLS: COLS, CELLS: CELLS, BUILD: BUILD, RED: RED, fresh: fresh, suspects: suspects };
    var HL = { big: [[2, 4], [5], [6], [7]], small: [[2, 3, 5], [6, 7], [8, 6], [9, 2]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var sus = suspects(c, i), bad = BUILD[c][i] > 0 || sus > 0 || lost(c, i) >= DAY_MIN, node = BUILD[c][i] > 0 ? 'build' : (sus ? 'test' : 'commit');
        var ns = { edit: K + 'st.done' }; ns[node] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: ['edit', node], nodeStates: ns,
          metrics: { suspects: sus, lost: lost(c, i), release: releasable(c, i) },
          codeHighlight: { snippet: 'j6.' + c, lines: HL[c][i] },
          movingSignals: [{ edge: node === 'build' ? 'e1' : (node === 'test' ? 'e2' : 'e3'), tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (node === 'commit' ? 'complete' : 'run'), subject: node }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 && c === 'big' ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        if (c === 'small' && i === 1) o.callouts[0].kind = 'source';
        return o;
      });
    }
    var LEN = { 'j6.big': 7, 'j6.small': 9 };
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'big' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'đổi tại chỗ: 2 bước không biên dịch được, 8 thay đổi bị nghi khi 3 test đỏ, bỏ 300 phút', run: function () {
          return BUILD.big[0] > 0 && BUILD.big[1] > 0 && suspects('big', 2) === 8 && RED.big[2] === 3 && lost('big', 3) === 300; } },
        { name: 'song song: mọi commit xanh trừ một bước đỏ được hoàn tác; lúc đỏ chỉ 1 thay đổi bị nghi; bỏ 15 phút; luôn phát hành được', run: function () {
          var last = CELLS.small[3], reds = COLS.small.filter(function (k) { return last[k][0] === 'red'; });
          return reds.length === 1 && last[reds[0]][1] === 'undo' && suspects('small', 1) === 1 && lost('small', 3) === 15 && [0, 1, 2, 3].every(function (i) { return releasable('small', i) === 1; }); } },
        { name: 'mỗi cách 4 bước; mọi dòng tô sáng nằm trong đoạn mã', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= LEN['j6.' + c]; }); }); }); } }] });
  })();

  /* ================= J7: lùi từng commit so với chia đôi (git bisect run) =================
     Theo Seemann ch.12 (tái hiện lỗi thành test; chia đôi; git bisect) và tài liệu git-bisect (tìm kiếm nhị phân; mã thoát của bisect run).
     Hai chiến lược được CÀI THẬT: danh sách lần thử, khoảng nghi ngờ và số phút đều tính bằng cách chạy chúng với commit lỗi đầu tiên = 137.
     Lịch sử thẳng; git bisect thật chọn theo đồ thị commit. */
  (function () {
    var m = 'bisect', CASES = ['linear', 'bisect'], KS = ['s1', 's2', 's3', 's4'], N = 200, CULPRIT = 137, MIN_PER = 3;
    var isBad = function (c) { return c >= CULPRIT; };
    // mỗi lần thử: [commit, xấu?, lo (tốt cao nhất đã biết), hi (xấu thấp nhất đã biết)]
    function run(c) {
      var lo = 0, hi = N, out = [];
      if (c === 'linear') { for (var k = N - 1; k > lo && hi - lo > 1; k--) { var b = isBad(k); if (b) hi = k; else lo = k; out.push([k, b, lo, hi]); } return out; }
      while (hi - lo > 1) { var mid = Math.floor((lo + hi) / 2), bb = isBad(mid); if (bb) hi = mid; else lo = mid; out.push([mid, bb, lo, hi]); }
      return out;
    }
    var RUNS = { linear: run('linear'), bisect: run('bisect') };
    var UPTO = { linear: [0, 10, 30, RUNS.linear.length], bisect: [0, 2, 5, RUNS.bisect.length] };   // số lần thử đã xong sau mỗi bước
    function state(c, i) {
      var n = UPTO[c][i], last = n ? RUNS[c][n - 1] : [null, null, 0, N], prev = i ? UPTO[c][i - 1] : 0;
      return { probes: n, lo: last[2], hi: last[3], left: last[3] - last[2], found: last[3] - last[2] === 1 ? last[3] : null, fresh: RUNS[c].slice(prev, n), minutes: n * MIN_PER, all: RUNS[c].slice(0, n) };
    }
    ADE.ccBisect = { N: N, state: state };
    var HL = { linear: [[1], [2, 3], [2, 3, 4], [4]], bisect: [[1, 2, 3], [4], [4, 5], [6, 7]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var st = state(c, i), slow = c === 'linear' && i >= 2, nodes = i === 0 ? ['report', 'test'] : ['pick', 'verdict'];
        var ns = {}; nodes.forEach(function (n) { ns[n] = K + 'st.done'; }); if (slow) ns.verdict = K + 'st.surprise';
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (slow ? 'pitfall' : 'mechanism'), activeNodes: nodes, nodeStates: ns,
          metrics: { probes: st.probes, left: i === 0 ? N : (st.found ? 1 : st.left), minutes: st.minutes },
          codeHighlight: { snippet: 'j7.' + c, lines: HL[c][i] },
          movingSignals: [{ edge: i === 0 ? 'e1' : 'e3', tok: slow ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: st.found ? 'complete' : (i === 0 ? 'observe' : 'run'), subject: nodes[nodes.length - 1] }] });
        o.callouts = [{ kind: i === 0 && c === 'linear' ? 'try' : (slow ? 'pitfall' : 'source'), textKey: i === 0 && c === 'linear' ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        if (c === 'linear' && i === 1) o.callouts[0].kind = 'pitfall';
        return o;
      });
    }
    var LEN = { 'j7.linear': 4, 'j7.bisect': 7 };
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'linear' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'chia đôi: 8 lần thử (= ⌈log2 200⌉), lần lượt 100, 150, 125, 137, 131, 134, 135, 136; tìm ra 137', run: function () {
          var r = RUNS.bisect; return r.length === Math.ceil(Math.log(N) / Math.LN2) && r.map(function (x) { return x[0]; }).join() === '100,150,125,137,131,134,135,136' && state('bisect', 3).found === CULPRIT; } },
        { name: 'lùi từng commit: 64 lần (199 tới 136), 192 phút; sau 10 lần còn 190, sau 30 lần còn 170 commit bị nghi', run: function () {
          return RUNS.linear.length === 64 && state('linear', 3).minutes === 192 && state('linear', 1).left === 190 && state('linear', 2).left === 170 && state('linear', 3).found === CULPRIT; } },
        { name: 'chia đôi: sau 2 lần còn 50, sau 5 lần còn 6 commit bị nghi', run: function () { return state('bisect', 1).left === 50 && state('bisect', 2).left === 6; } },
        { name: 'mỗi cách 4 bước; mọi dòng tô sáng nằm trong đoạn mã', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= LEN['j7.' + c]; }); }); }); } }] });
  })();

  /* ================= J8: simple design và SOLID — when theo chuỗi so với thiết kế SOLID =================
     Theo Martin, Clean Architecture ch.7–11 (SRP theo actor; OCP; LSP của Liskov; ISP; DIP với trừu tượng ổn định), Clean Code ch.6, ch.12,
     Clean Craftsmanship ch.6; Effective Kotlin Item 36. Mỗi bước mở một (hay hai) hàng nguyên lý; số file phải sửa để thêm MoMo đếm từ danh
     sách nơi dùng when theo chuỗi; đồ thị phụ thuộc là danh sách cạnh. */
  (function () {
    var m = 'solid', CASES = ['switch', 'solid'], KS = ['s1', 's2', 's3', 's4'];
    var ROWS = ['srp', 'ocp', 'lsp', 'isp', 'dip'], STEP_ROWS = [['srp'], ['ocp'], ['lsp', 'isp'], ['dip']];
    var WHEN_SITES = { switch: ['fee', 'pay', 'receipt', 'refund', 'analytics'], solid: [] };   // nơi rẽ nhánh theo cách thanh toán
    var MOMO_FILES = function (c) { return c === 'switch' ? WHEN_SITES.switch.length : 1; };    // SOLID: thêm đúng một file MoMo
    var REFUND_CRASH = { switch: 1, solid: 0 };
    // đồ thị phụ thuộc mã nguồn: [từ, tới] nghĩa là "từ" import "tới"
    var EDGES = { switch: [['booking', 'sdk']], solid: [['booking', 'port'], ['adapter', 'port'], ['adapter', 'sdk']] };
    var POLICY = ['booking', 'port'], DETAIL = ['adapter', 'sdk'];
    function policyOnDetail(c) { return EDGES[c].filter(function (e) { return POLICY.indexOf(e[0]) >= 0 && DETAIL.indexOf(e[1]) >= 0; }).length; }
    function openRows(i) { return STEP_ROWS.slice(0, i + 1).reduce(function (a, r) { return a.concat(r); }, []); }
    ADE.ccSolid = { ROWS: ROWS, STEP_ROWS: STEP_ROWS, EDGES: EDGES, POLICY: POLICY, openRows: openRows, policyOnDetail: policyOnDetail };
    var HL = { switch: [[1], [2, 5, 7], [9, 10], [12]], solid: [[1, 2, 3], [4, 5], [6, 7], [8, 9, 10]] };
    function steps(s) {
      var c = s.case, bad = c === 'switch';
      return KS.map(function (k, i) {
        var nodes = i === 3 ? (bad ? ['booking', 'sdk'] : ['booking', 'port', 'adapter']) : ['booking'];
        var ns = {}; nodes.forEach(function (n) { ns[n] = K + 'st.' + (bad && i > 0 ? 'surprise' : 'done'); });
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nodes, nodeStates: ns,
          metrics: { files: i >= 1 ? MOMO_FILES(c) : 0, crash: i >= 2 ? REFUND_CRASH[c] : 0, detail: i >= 3 ? policyOnDetail(c) : 0 },
          codeHighlight: { snippet: 'j8.' + c, lines: HL[c][i] },
          movingSignals: [{ edge: bad ? 'e1' : (i === 3 ? 'e3' : 'e2'), tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad && i > 0 ? 'exception' : 'observe', subject: nodes[nodes.length - 1] }] });
        o.callouts = [{ kind: i === 0 && bad ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 && bad ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    var LEN = { 'j8.switch': 12, 'j8.solid': 10 };
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'switch' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'thêm MoMo: when theo chuỗi sửa 5 file, SOLID thêm 1 file; hoàn tiền: 1 chỗ crash so với 0', run: function () { return MOMO_FILES('switch') === 5 && MOMO_FILES('solid') === 1 && REFUND_CRASH.switch === 1 && REFUND_CRASH.solid === 0; } },
        { name: 'DIP: bản when có 1 cạnh nghiệp vụ → chi tiết; bản SOLID có 0, và chi tiết trỏ vào giao diện của nghiệp vụ', run: function () {
          return policyOnDetail('switch') === 1 && policyOnDetail('solid') === 0 && EDGES.solid.some(function (e) { return e[0] === 'adapter' && e[1] === 'port'; }); } },
        { name: 'bốn bước mở đủ năm nguyên lý, mỗi nguyên lý đúng một lần', run: function () { var r = openRows(3); return r.length === 5 && ROWS.every(function (x) { return r.indexOf(x) >= 0; }); } },
        { name: 'mỗi thiết kế 4 bước; mọi dòng tô sáng nằm trong đoạn mã', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= LEN['j8.' + c]; }); }); }); } }] });
  })();

  /* ================= J9: nguyên lý thành phần — một :core:common so với chia theo lý do thay đổi =================
     Theo Martin, Clean Architecture ch.13 (REP, CCP, CRP), ch.14 (ADP, SDP, Fan-in, Fan-out, I = Fan-out/(Fan-in + Fan-out), SAP). Danh sách cạnh
     EDGES là nguồn sự thật: Ca, Ce, I, mũi tên vi phạm SDP, số module phụ thuộc bắc cầu và tổng lần build đều tính từ đó. Đếm theo MODULE
     (Martin đếm theo lớp); tần suất đổi là minh họa. */
  (function () {
    var m = 'components', CASES = ['common', 'split'], KS = ['s1', 's2', 's3', 's4'];
    var MODS = {
      common: ['app', 'booking', 'profile', 'reminder', 'data', 'analytics', 'common', 'network', 'prefs'],
      split: ['app', 'booking', 'profile', 'reminder', 'data', 'analytics', 'model', 'network', 'prefs']
    };
    var EDGES = {
      common: [['app', 'booking'], ['app', 'profile'], ['app', 'reminder'], ['app', 'common'], ['booking', 'common'], ['booking', 'data'], ['profile', 'common'], ['profile', 'data'],
        ['reminder', 'common'], ['reminder', 'data'], ['data', 'common'], ['common', 'analytics'], ['analytics', 'network'], ['analytics', 'prefs']],
      split: [['app', 'booking'], ['app', 'profile'], ['app', 'reminder'], ['app', 'analytics'], ['booking', 'model'], ['booking', 'data'], ['profile', 'model'], ['profile', 'data'],
        ['reminder', 'model'], ['reminder', 'data'], ['data', 'model'], ['analytics', 'model'], ['analytics', 'network'], ['analytics', 'prefs']]
    };
    var CHANGES = {   // số lần đổi mỗi tháng (minh họa); tổng xấp xỉ nhau để so công bằng
      common: { app: 2, booking: 4, profile: 4, reminder: 4, data: 3, analytics: 6, common: 12, network: 1, prefs: 1 },
      split: { app: 2, booking: 8, profile: 8, reminder: 8, data: 3, analytics: 6, model: 1, network: 1, prefs: 1 }
    };
    var HOT_I = 0.25, HOT_CHG = 6;   // "ổn định mà hay đổi": I ≤ 0,25 và đổi ≥ 6 lần mỗi tháng
    function ca(c, x) { return EDGES[c].filter(function (e) { return e[1] === x; }).length; }
    function ce(c, x) { return EDGES[c].filter(function (e) { return e[0] === x; }).length; }
    function inst(c, x) { var a = ca(c, x), e = ce(c, x); return a + e ? e / (a + e) : 0; }
    function dependents(c, x) {   // module phụ thuộc bắc cầu vào x
      var seen = {}, q = [x];
      while (q.length) { var y = q.shift(); EDGES[c].forEach(function (e) { if (e[1] === y && !seen[e[0]]) { seen[e[0]] = true; q.push(e[0]); } }); }
      return Object.keys(seen).length;
    }
    function rebuilds(c, x) { return 1 + dependents(c, x); }
    function violations(c) { return EDGES[c].filter(function (e) { return inst(c, e[0]) < inst(c, e[1]); }); }
    function hot(c) { return MODS[c].filter(function (x) { return inst(c, x) <= HOT_I && CHANGES[c][x] >= HOT_CHG; }); }
    function total(c) { return MODS[c].reduce(function (s, x) { return s + CHANGES[c][x] * rebuilds(c, x); }, 0); }
    function changesTotal(c) { return MODS[c].reduce(function (s, x) { return s + CHANGES[c][x]; }, 0); }
    ADE.ccComponents = { MODS: MODS, EDGES: EDGES, CHANGES: CHANGES, ca: ca, ce: ce, inst: inst, rebuilds: rebuilds, violations: violations, hot: hot, total: total };
    var HL = { common: [[1, 6], [2, 3], [1], [3, 5, 6]], split: [[1, 2], [5, 6, 8], [3], [8]] };
    function steps(s) {
      var c = s.case, bad = c === 'common';
      return KS.map(function (k, i) {
        var node = ['graph', 'count', 'metric', 'cost'][i], warn = bad && i >= 1;
        var ns = {}; ns[node] = K + 'st.' + (warn ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (warn ? 'pitfall' : 'mechanism'), activeNodes: i === 0 ? ['graph', 'count'] : [['count', 'metric'], ['metric', 'cost'], ['cost']][i - 1], nodeStates: ns,
          metrics: { violations: i >= 1 ? violations(c).length : 0, hot: i >= 2 ? hot(c).length : 0, rebuilds: i >= 3 ? total(c) : 0 },
          codeHighlight: { snippet: 'j9.' + c, lines: HL[c][i] },
          movingSignals: [{ edge: 'e' + Math.max(1, i), tok: warn ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: warn ? 'exception' : (i === 3 ? 'complete' : 'run'), subject: node }] });
        o.callouts = [{ kind: i === 0 && bad ? 'try' : (warn ? 'pitfall' : 'source'), textKey: i === 0 && bad ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    var LEN = { 'j9.common': 6, 'j9.split': 8 };
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'common' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'common: Ca 5, Ce 1, I = 1/6; analytics I = 2/3; đúng một mũi tên vi phạm SDP (common → analytics); common là module ổn định mà hay đổi', run: function () {
          var v = violations('common'); return ca('common', 'common') === 5 && ce('common', 'common') === 1 && Math.abs(inst('common', 'common') - 1 / 6) < 1e-9 && Math.abs(inst('common', 'analytics') - 2 / 3) < 1e-9 &&
            v.length === 1 && v[0][0] === 'common' && v[0][1] === 'analytics' && hot('common').join() === 'common'; } },
        { name: 'chia lại: model I = 0, analytics I = 3/4; không vi phạm SDP; không module ổn định mà hay đổi', run: function () {
          return inst('split', 'model') === 0 && inst('split', 'analytics') === 0.75 && violations('split').length === 0 && hot('split').length === 0; } },
        { name: 'build lại mỗi tháng: 171 so với 90, với tổng lần đổi gần bằng nhau (37 và 38); common kéo theo 6 module mỗi lần đổi', run: function () {
          return total('common') === 171 && total('split') === 90 && changesTotal('common') === 37 && changesTotal('split') === 38 && rebuilds('common', 'common') === 6; } },
        { name: 'không có vòng phụ thuộc ở cả hai cách chia (ADP)', run: function () { return CASES.every(function (c) { return MODS[c].every(function (x) { var seen = {}, q = [x], cyc = false;
          while (q.length && !cyc) { var y = q.shift(); EDGES[c].forEach(function (e) { if (e[0] === y) { if (e[1] === x) cyc = true; if (!seen[e[1]]) { seen[e[1]] = true; q.push(e[1]); } } }); } return !cyc; }); }); } },
        { name: 'mỗi cách 4 bước; mọi dòng tô sáng nằm trong đoạn mã', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= LEN['j9.' + c]; }); }); }); } }] });
  })();
})();
