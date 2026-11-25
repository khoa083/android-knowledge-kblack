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

  /* ================= l2: debugger: breakpoint thường, có điều kiện, chính sách All hay Thread, breakpoint chỉ ghi log =================
     Theo JetBrains IntelliJ IDEA 2026.3 Help (Breakpoints; Examine suspended program). CÀI THẬT: 500 lịch, phí = base × (100 − giảm giá) / 100;
     chỉ đơn 347 có giảm giá 120 % nên phí âm. Số lần dừng, bấm chạy tiếp, dòng log được đếm từ vòng lặp; luồng đồng bộ gửi nhịp mỗi giây,
     khoảng không nhịp dài nhất được tính từ thời gian dừng (mỗi lần dừng ngắn 1 giây, bước "xem biến" 30 giây); quá 10 giây là mất phiên.
     Danh sách lịch, mức giảm giá và hạn 10 giây là của site. */
  (function () {
    var m = 'bp', CASES = ['plain', 'cond', 'thread', 'logbp'], KS = ['s1', 's2', 's3'];
    var N = 500, BAD = 347, BASE = 200000, TIMEOUT = 10, LOOK = 30;
    var disc = function (i) { return i === BAD ? 120 : (i * 7) % 31; };
    var fee = function (i) { return BASE * (100 - disc(i)) / 100; };
    var negatives = function () { var r = []; for (var i = 0; i < N; i++) if (fee(i) < 0) r.push(i); return r; };
    // chạy vòng lặp tới bước k (0..2) với một kiểu breakpoint: chỉ số đang đứng, các lần dừng, số lần bấm chạy tiếp, số dòng log, khoảng không nhịp dài nhất
    function run(c, k) {
      var stops = [], logs = 0, at = 0, gap = 0, cond = c === 'cond' || c === 'thread', all = c !== 'thread';
      if (c === 'logbp') { logs = N; at = N - 1; }
      else if (c === 'plain') { var to = k === 0 ? 0 : BAD; for (var i = 0; i <= to; i++) stops.push(i); at = to; }
      else if (cond) { if (k === 0) at = BAD - 1; else { for (var j = 0; j < N; j++) if (fee(j) < 0) { stops.push(j); break; } at = BAD; } }
      if (c !== 'logbp' && all && stops.length) gap = k === 2 ? LOOK : 1;
      return { at: at, stops: stops.length, resumes: Math.max(0, stops.length - 1), logs: logs, filtered: c === 'logbp' && k >= 1 ? negatives().length : 0, gap: gap, expired: gap > TIMEOUT };
    }
    ADE.dbgBp = { N: N, BAD: BAD, BASE: BASE, disc: disc, fee: fee, run: run, TIMEOUT: TIMEOUT };
    var NODES = [[['report', 'bp'], 'bp', 'e1'], [['bp', 'vars'], 'vars', 'e2'], [['sync', 'server'], 'server', 'e4']];
    var HL = { plain: [[5], [5], [5]], cond: [[4, 5], [4, 5], [5]], thread: [[4, 5], [4, 5], [5]], logbp: [[5], [4, 5], [4]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var r = run(c, i), bad = (c === 'plain' && i >= 1) || r.expired, nd = NODES[i], ns = {};
        ns[nd[1]] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          metrics: { stops: r.stops, resumes: r.resumes, logs: r.logs, sync: M(m, i < 2 && c !== 'thread' && c !== 'logbp' ? 'sync.na' : (r.expired ? 'sync.expired' : 'sync.alive')) },
          codeHighlight: { snippet: 'l2.loop', lines: HL[c][i] },
          movingSignals: [{ edge: nd[2], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 2 ? 'complete' : (i === 0 ? 'observe' : 'run')), subject: nd[1] }] });
        var tryIt = i === 0 && c === 'plain';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : 'source'), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'plain' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'trong 500 lịch chỉ đơn 347 có phí âm: 200.000 × (100 − 120) / 100 = −40.000', run: function () { var n = negatives(); return n.length === 1 && n[0] === 347 && fee(347) === -40000 && fee(0) === 200000; } },
        { name: 'breakpoint thường: 348 lần dừng, 347 lần bấm chạy tiếp; có điều kiện fee < 0: đúng 1 lần dừng, ở đơn 347', run: function () {
          var a = run('plain', 1), b = run('cond', 1); return a.stops === 348 && a.resumes === 347 && b.stops === 1 && b.at === 347 && b.resumes === 0; } },
        { name: 'xem biến 30 giây: dừng mọi luồng thì luồng đồng bộ lỡ 30 nhịp > 10, mất phiên; chỉ dừng một luồng thì 0 nhịp, còn phiên', run: function () {
          return run('plain', 2).expired && run('cond', 2).expired && !run('thread', 2).expired && run('thread', 2).gap === 0 && !run('plain', 1).expired; } },
        { name: 'breakpoint chỉ ghi log: 0 lần dừng, 500 dòng log, lọc phí âm còn 1 dòng; mỗi kiểu 3 bước, dòng tô sáng trong đoạn mã', run: function () {
          var r = run('logbp', 1); return r.stops === 0 && r.logs === 500 && r.filtered === 1 &&
            CASES.every(function (c) { return steps({ case: c }).length === 3 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= 8; }); }); }); } }] });
  })();

  /* ================= l3: Logcat: lọc dần để tìm dòng lỗi; log còn lại trong bản release =================
     Theo developer.android.com/studio/debug/logcat (truy vấn key:value: cùng key OR, khác key AND, level: là mức đó trở lên, package:mine),
     tools/logcat, reference Log, privacy-and-security/risks/log-info-disclosure (R8 -assumenosideeffects xóa v, d, i; giữ w, e).
     CÀI THẬT: 16 dòng log (của site); mỗi bước là một truy vấn có cấu trúc, áp thật lên 16 dòng; bản release bỏ mọi dòng V, D, I của app. */
  (function () {
    var m = 'logcat', CASES = ['find', 'release'], KS = ['s1', 's2', 's3', 's4'];
    var LV = { V: 2, D: 3, I: 4, W: 5, E: 6, A: 7 };
    var APP = 'vn.henkham';
    // [pid, mức, tag, package, nội dung, có số điện thoại]
    var LOGS = [
      [589, 'I', 'ActivityManager', 'system_server', 'Start proc 4120:vn.henkham', 0],
      [4120, 'D', 'BookingRepo', APP, 'load bookings page=1', 0],
      [1022, 'D', 'SystemUI', 'com.android.systemui', 'status bar updated', 0],
      [2211, 'I', 'GmsCore', 'com.google.android.gms', 'heartbeat ok', 0],
      [4120, 'I', 'Sync', APP, 'sync started', 0],
      [4120, 'D', 'BookingRepo', APP, 'saving booking for phone=0912345678', 1],
      [589, 'W', 'ActivityManager', 'system_server', 'slow operation: 120ms', 0],
      [4120, 'V', 'ListAdapter', APP, 'bind row 3', 0],
      [2211, 'D', 'GmsCore', 'com.google.android.gms', 'token refresh', 0],
      [4120, 'W', 'Sync', APP, 'retry 1 for phone=0912345678', 1],
      [1022, 'I', 'SystemUI', 'com.android.systemui', 'clock tick', 0],
      [4120, 'D', 'Sync', APP, 'server responded 409', 0],
      [4120, 'E', 'BookingRepo', APP, 'save failed: SQLiteConstraintException', 0],
      [589, 'I', 'ActivityManager', 'system_server', 'Displayed vn.henkham/.MainActivity', 0],
      [2211, 'W', 'GmsCore', 'com.google.android.gms', 'location timeout', 0],
      [4120, 'I', 'Sync', APP, 'sync finished: 1 failed', 0]];
    var ERR = 12, FIXED = 'retry 1 for booking id=42';
    // truy vấn có cấu trúc: { package: [...], level: 'W', tag: [...] }; cùng key OR (mảng), khác key AND
    function match(row, q) {
      if (q.package && q.package.indexOf(row[3]) < 0) return false;
      if (q.level && LV[row[1]] < LV[q.level]) return false;
      if (q.tag && q.tag.indexOf(row[2]) < 0) return false;
      return true;
    }
    var Q = { find: [{}, { package: [APP] }, { package: [APP], level: 'W' }, { package: [APP], tag: ['BookingRepo', 'Sync'] }],
      release: [{ package: [APP] }, { package: [APP] }, { package: [APP] }, { package: [APP] }] };
    var BUILD = { find: ['debug', 'debug', 'debug', 'debug'], release: ['debug', 'release', 'release', 'release'] };
    var stripped = function (row, build) { return build === 'release' && row[3] === APP && LV[row[1]] <= LV.I; };
    function view(c, i) {
      var q = Q[c][i], b = BUILD[c][i], fixed = c === 'release' && i === 3;
      var rows = LOGS.map(function (r, k) {
        var gone = stripped(r, b), shown = !gone && match(r, q), pii = shown && r[5] === 1 && !fixed;
        return { k: k, row: r, shown: shown, gone: gone, pii: pii, msg: fixed && r[5] && r[1] === 'W' ? FIXED : r[4] };
      });
      var shown = rows.filter(function (x) { return x.shown; });
      return { q: q, build: b, rows: rows, shown: shown.length, app: shown.filter(function (x) { return x.row[3] === APP; }).length,
        pii: rows.filter(function (x) { return x.pii; }).length, found: shown.some(function (x) { return x.k === ERR; }) && shown.length <= 8 };
    }
    // chuỗi truy vấn hiển thị (giữ nguyên cú pháp Logcat, không dịch)
    function qtext(q) {
      var p = [];
      if (q.package) p.push('package:mine');
      if (q.level) p.push('level:' + { W: 'WARN', E: 'ERROR', I: 'INFO' }[q.level]);
      (q.tag || []).forEach(function (t) { p.push('tag:' + t); });
      return p.join(' ');
    }
    ADE.dbgLogcat = { view: view, qtext: qtext, LOGS: LOGS };
    var NODES = { find: [[['others', 'logd', 'view'], 'view', 'e3'], [['app', 'view'], 'view', 'e4'], [['view'], 'view', 'e4'], [['app', 'view'], 'view', 'e4']],
      release: [[['app', 'logd'], 'logd', 'e2'], [['app', 'r8'], 'r8', 'e1'], [['logd', 'view'], 'view', 'e4'], [['app', 'view'], 'view', 'e4']] };
    var HL = { find: [[5], [3, 5], [5, 8], [3, 5, 8]], release: [[3, 8], [3], [8], [9]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var v = view(c, i), bad = (c === 'find' && i === 0) || (c === 'release' && (i === 0 || i === 2)), nd = NODES[c][i], ns = {};
        ns[nd[1]] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          metrics: { shown: v.shown, app: v.app, pii: v.pii, found: M(m, v.found ? 'found.yes' : 'found.no') },
          codeHighlight: { snippet: 'l3.log', lines: HL[c][i] },
          movingSignals: [{ edge: nd[2], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : (i === 0 ? 'observe' : 'run')), subject: nd[1] }] });
        var tryIt = i === 0 && c === 'find';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : 'source'), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'find' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'không lọc 16 dòng; package:mine còn 8; thêm level:WARN còn 2 và có dòng lỗi', run: function () {
          var a = view('find', 0), b = view('find', 1), c = view('find', 2); return a.shown === 16 && b.shown === 8 && c.shown === 2 && c.found && !a.found; } },
        { name: 'tag:BookingRepo tag:Sync (cùng key nên OR) cùng package:mine còn 7 dòng', run: function () { return view('find', 3).shown === 7; } },
        { name: 'bản debug: 2 dòng lộ số điện thoại; release xóa V, D, I còn 2 dòng của app, vẫn 1 dòng lộ (Log.w); log id thì 0', run: function () {
          return view('release', 0).pii === 2 && view('release', 1).shown === 2 && view('release', 2).pii === 1 && view('release', 3).pii === 0; } },
        { name: 'mỗi cách 4 bước; dòng tô sáng nằm trong đoạn mã 9 dòng', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= 9; }); }); }); } }] });
  })();

  /* ================= l4: đọc stack trace ba tầng: sửa theo dòng đầu, hay đọc tới nguyên nhân gốc =================
     Theo Java SE 21 Throwable.printStackTrace (dòng đầu là toString; Caused by; "... n more" là n frame cuối trùng với ngoại lệ bọc ngoài) và
     developer.android.com/topic/performance/vitals/crash. CÀI THẬT: mỗi tầng có stack đầy đủ; số frame được in và số "... n more" tính bằng
     cách đếm phần đuôi giống hệt với stack của tầng bọc ngoài. Tên lớp của app và số dòng là của site. */
  (function () {
    var m = 'trace', CASES = ['top', 'root'], KS = ['s1', 's2', 's3', 's4'];
    var A = ['android.app.ActivityThread.performLaunchActivity(ActivityThread.java:4206)', 'android.app.ActivityThread.handleLaunchActivity(ActivityThread.java:4387)',
      'android.os.Handler.dispatchMessage(Handler.java:107)', 'android.os.Looper.loop(Looper.java:317)', 'android.app.ActivityThread.main(ActivityThread.java:8705)'];
    var MID = ['vn.henkham.detail.DetailViewModel.requireBooking(DetailViewModel.kt:58)', 'vn.henkham.detail.DetailActivity.onCreate(DetailActivity.kt:31)',
      'android.app.Activity.performCreate(Activity.java:9002)', 'android.app.Instrumentation.callActivityOnCreate(Instrumentation.java:1526)'].concat(A);
    var ROOT = ['java.time.format.DateTimeFormatter.createError(DateTimeFormatter.java:2108)', 'java.time.LocalDate.parse(LocalDate.java:435)',
      'vn.henkham.data.BookingMapper.toBooking(BookingMapper.kt:22)', 'vn.henkham.detail.DetailViewModel.requireBooking(DetailViewModel.kt:55)'].concat(MID.slice(1));
    var CHAIN = [
      { head: 'java.lang.RuntimeException: Unable to start activity ComponentInfo{vn.henkham/vn.henkham.DetailActivity}: java.lang.IllegalStateException: Booking not loaded', stack: A },
      { head: 'java.lang.IllegalStateException: Booking not loaded', stack: MID },
      { head: "java.time.format.DateTimeParseException: Text '2026-11-31' could not be parsed: Invalid date 'NOVEMBER 31'", stack: ROOT }];
    var isApp = function (f) { return f.indexOf('vn.henkham.') === 0; };
    function common(a, b) { var n = 0; while (n < a.length && n < b.length && a[a.length - 1 - n] === b[b.length - 1 - n]) n++; return n; }
    // các dòng in ra, đúng như printStackTrace: tầng 0 in đủ; tầng k in phần đầu, rồi "... n more"
    function lines() {
      var out = [];
      CHAIN.forEach(function (t, k) {
        var n = k ? common(t.stack, CHAIN[k - 1].stack) : 0, shown = t.stack.slice(0, t.stack.length - n);
        out.push({ kind: 'head', layer: k, text: (k ? 'Caused by: ' : '') + t.head });
        shown.forEach(function (f, j) { out.push({ kind: 'frame', layer: k, text: 'at ' + f, app: isApp(f), f: f }); });
        if (n) out.push({ kind: 'more', layer: k, n: n, hidden: t.stack.slice(t.stack.length - n) });
      });
      return out;
    }
    function firstApp(k) { var s = CHAIN[k].stack; for (var j = 0; j < s.length; j++) if (isApp(s[j])) return s[j]; return null; }
    ADE.dbgTrace = { lines: lines, CHAIN: CHAIN, firstApp: firstApp, common: common };
    var FRAME = { top: ['frame.none', 'frame.start', 'frame.vm', 'frame.vm'], root: ['frame.none', 'frame.none', 'frame.mapper', 'frame.mapper'] };
    var LAYERS = { top: [1, 1, 2, 2], root: [3, 3, 3, 3] };
    var NODES = { top: [[['outer', 'crash'], 'outer', 'e3'], [['outer'], 'outer', 'e3'], [['mid', 'outer'], 'mid', 'e2'], [['root', 'mid'], 'root', 'e1']],
      root: [[['outer', 'crash'], 'crash', 'e3'], [['root'], 'root', 'e1'], [['root', 'mid'], 'root', 'e1'], [['root'], 'root', 'e1']] };
    var HL = { top: [[1], [1], [4, 5], [2]], root: [[1], [2], [2], [2, 3]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var bad = c === 'top' && i >= 1, nd = NODES[c][i], ns = {};
        ns[nd[1]] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          metrics: { layers: LAYERS[c][i], frame: M(m, FRAME[c][i]), fixed: M(m, c === 'root' && i === 3 ? 'fixed.yes' : 'fixed.no') },
          codeHighlight: { snippet: 'l4.code', lines: HL[c][i] },
          movingSignals: [{ edge: nd[2], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : (i === 0 ? 'observe' : 'run')), subject: nd[1] }] });
        var tryIt = i === 0 && c === 'top';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : 'source'), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'top' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'tầng giữa in 4 frame rồi "... 5 more"; tầng gốc in 4 frame rồi "... 8 more" (dòng 55 và 58 khác nhau nên không tính)', run: function () {
          var mo = lines().filter(function (l) { return l.kind === 'more'; }); return mo.length === 2 && mo[0].n === 5 && mo[1].n === 8 &&
            lines().filter(function (l) { return l.kind === 'frame' && l.layer === 1; }).length === 4 && lines().filter(function (l) { return l.kind === 'frame' && l.layer === 2; }).length === 4; } },
        { name: 'tầng ngoài 0 frame của app; frame đầu của app ở tầng giữa là DetailViewModel.kt:58, ở tầng gốc là BookingMapper.kt:22', run: function () {
          return firstApp(0) === null && /DetailViewModel\.kt:58/.test(firstApp(1)) && /BookingMapper\.kt:22/.test(firstApp(2)); } },
        { name: 'phần "... n more" mở ra trùng đúng đáy của tầng bọc ngoài', run: function () {
          var mo = lines().filter(function (l) { return l.kind === 'more'; })[1]; return mo.hidden.join() === MID.slice(MID.length - 8).join(); } },
        { name: 'mỗi cách 4 bước; dòng tô sáng nằm trong đoạn mã 6 dòng', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= 6; }); }); }); } }] });
  })();

  /* ================= l5: R8 và stack trace bị làm rối: dịch bằng mapping của bản build mới nhất, hay của đúng phiên bản bị crash =================
     Theo developer.android.com build/shrink-code, studio/command-line/retrace, app-optimization/troubleshoot-the-optimization; Play Console Help 9848633.
     CÀI THẬT: hai bảng mapping (lớp rối → tên thật, hàm rối → [tên, khoảng dòng rối, dòng thật bắt đầu]); mỗi frame được tra và tính số dòng thật
     theo khoảng; frame đúng khi kết quả khớp tên thật của bản 1.6.0. Tên lớp, tên rối và số dòng là của site. */
  (function () {
    var m = 'retrace', CASES = ['latest', 'exact'], KS = ['s1', 's2', 's3', 's4'];
    var HEAD = 'java.lang.ClassNotFoundException: vn.henkham.pay.MomoPayment';
    var FRAMES = [['a.b', 'c', 4], ['a.e', 'f', 3], ['a.g', 'h', 7], null];   // null: frame của Android, không bị làm rối
    var ANDROID = 'android.view.View.performClick(View.java:7659)';
    // mapping: lớp rối → [tên thật, file, { hàm rối: [tên, dòng rối đầu, dòng rối cuối, dòng thật đầu] }]
    var MAPS = {
      exact: { 'a.b': ['vn.henkham.pay.PaymentFactory', 'PaymentFactory.kt', { c: ['create', 1, 12, 18] }], 'a.d': ['vn.henkham.pay.MomoPayment', 'MomoPayment.kt', {}],
        'a.e': ['vn.henkham.pay.PaymentViewModel', 'PaymentViewModel.kt', { f: ['pay', 1, 20, 40] }], 'a.g': ['vn.henkham.pay.PayFragment', 'PayFragment.kt', { h: ['onPayClicked', 1, 9, 70] }] },
      latest: { 'a.b': ['vn.henkham.data.BookingRepo', 'BookingRepo.kt', { c: ['save', 1, 8, 30] }], 'a.e': ['vn.henkham.pay.PaymentViewModel', 'PaymentViewModel.kt', { f: ['pay', 1, 20, 40] }],
        'a.g': ['vn.henkham.data.BookingDao', 'BookingDao.kt', { h: ['insert', 1, 9, 12] }] } };
    function tr(map, f) {
      if (!f) return { text: ANDROID, line: '—' };
      var c = map[f[0]], fn = c && c[2][f[1]];
      if (!fn || f[2] < fn[1] || f[2] > fn[2]) return { text: '?', line: '—' };
      return { text: c[0] + '.' + fn[0] + '(' + c[1] + ':' + (fn[3] + f[2] - fn[1]) + ')', line: c[0] + ' -> ' + f[0] + ' · ' + fn[1] + ':' + fn[2] + ' … -> ' + f[1] };
    }
    var obf = function (f) { return f ? f[0] + '.' + f[1] + '(Unknown Source:' + f[2] + ')' : ANDROID; };
    function rows(c, translated) {
      return FRAMES.map(function (f) { var got = translated ? tr(MAPS[c], f) : { text: '?', line: '—' }, real = tr(MAPS.exact, f);
        return { obf: obf(f), got: got.text, line: got.line, real: real.text, ok: translated && got.text === real.text, wrong: translated && got.text !== '?' && got.text !== real.text }; });
    }
    function tally(c, translated) { var r = rows(c, translated); return { ok: r.filter(function (x) { return x.ok; }).length, wrong: r.filter(function (x) { return x.wrong; }).length }; }
    ADE.dbgRetrace = { rows: rows, tally: tally, HEAD: HEAD };
    var CAUSE = { latest: ['cause.none', 'cause.none', 'cause.none', 'cause.wrong'], exact: ['cause.none', 'cause.none', 'cause.reflect', 'cause.kept'] };
    var NODES = { latest: [[['crash'], 'crash', 'e3'], [['map', 'retrace'], 'map', 'e4'], [['retrace'], 'retrace', 'e4'], [['retrace'], 'retrace', 'e4']],
      exact: [[['crash', 'map'], 'map', 'e2'], [['map', 'retrace'], 'retrace', 'e4'], [['src', 'retrace'], 'src', 'e1'], [['src', 'r8'], 'r8', 'e1']] };
    var HL = { latest: [[2], [2], [2], [2]], exact: [[2], [2], [3], [8, 9]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var t = tally(c, i >= 1), bad = c === 'latest' && i >= 2, nd = NODES[c][i], ns = {};
        ns[nd[1]] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          metrics: { ok: t.ok, wrong: i >= 2 ? t.wrong : 0, cause: M(m, CAUSE[c][i]) },
          codeHighlight: { snippet: 'l5.code', lines: HL[c][i] },
          movingSignals: [{ edge: nd[2], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : (i === 0 ? 'observe' : 'run')), subject: nd[1] }] });
        var tryIt = i === 0 && c === 'latest';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : 'source'), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'latest' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mapping đúng bản 1.6.0: cả 4 frame dịch đúng; a.b.c dòng rối 4 thành PaymentFactory.create dòng 21', run: function () {
          var r = rows('exact', true); return tally('exact', true).ok === 4 && r[0].got === 'vn.henkham.pay.PaymentFactory.create(PaymentFactory.kt:21)'; } },
        { name: 'mapping của bản mới nhất: 2 frame đúng (PaymentViewModel và frame Android), 2 frame sai mà trông hợp lý (BookingRepo, BookingDao)', run: function () {
          var t = tally('latest', true), r = rows('latest', true); return t.ok === 2 && t.wrong === 2 && /BookingRepo\.save/.test(r[0].got) && /BookingDao\.insert/.test(r[2].got); } },
        { name: 'bài tập: dòng rối 5 trong khoảng 1:12 của c ứng với dòng thật 22 (18 + 5 − 1)', run: function () { return tr(MAPS.exact, ['a.b', 'c', 5]).text === 'vn.henkham.pay.PaymentFactory.create(PaymentFactory.kt:22)'; } },
        { name: 'mỗi cách 4 bước; dòng tô sáng nằm trong đoạn mã 9 dòng', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= 9; }); }); }); } }] });
  })();

  /* ================= l6: Layout Inspector: nút bị một lớp phủ trong suốt che =================
     Theo developer.android.com studio/debug/layout-inspector và compose understand-gestures (hit test theo bounds; giữa anh em chồng nhau, chỉ cái vẽ trên
     cùng được hit; clickable tự tiêu thụ). CÀI THẬT: cây 7 thành phần theo thứ tự vẽ; thành phần nhận cú chạm là thành phần xử lý chạm vẽ sau cùng có bounds
     chứa điểm chạm; alpha không tham gia. Bố cục, kích thước và điểm chạm là của site. */
  (function () {
    var m = 'layout', CASES = ['guess', 'inspect'], KS = ['s1', 's2', 's3', 's4'];
    var TAP = [180, 624];
    // [id, tên, [x, y, w, h], alpha, xử lý chạm, độ sâu]; thứ tự = thứ tự vẽ
    var BASE = [['root', 'Box', [0, 0, 360, 800], 1, false, 0], ['col', 'Column', [0, 56, 360, 744], 1, false, 1], ['title', 'Text "Chọn giờ khám"', [16, 72, 328, 32], 1, false, 2],
      ['grid', 'SlotGrid', [16, 120, 328, 400], 1, true, 2], ['button', 'Button "Đặt lịch"', [16, 600, 328, 48], 1, true, 2],
      ['overlay', 'LoadingOverlay', [0, 0, 360, 800], 0, true, 1], ['spinner', 'CircularProgressIndicator', [156, 376, 48, 48], 0, false, 2]];
    // biến thể theo bước: nút cao 64 dp (cách đoán), hay lớp phủ bị gỡ khỏi cây (bản sửa)
    var VAR = { guess: ['base', 'base', 'tall', 'tall'], inspect: ['base', 'base', 'base', 'fixed'] };
    function tree(v) {
      return BASE.map(function (n) {
        var b = n[2].slice(); if (v === 'tall' && n[0] === 'button') b[3] = 64;
        return { id: n[0], name: n[1], b: b, alpha: n[3], click: n[4], depth: n[5], present: !(v === 'fixed' && (n[0] === 'overlay' || n[0] === 'spinner')) };
      });
    }
    var inside = function (b, p) { return p[0] >= b[0] && p[0] <= b[0] + b[2] && p[1] >= b[1] && p[1] <= b[1] + b[3]; };
    function hit(v) {
      var t = tree(v), under = t.filter(function (n) { return n.present && n.click && inside(n.b, TAP); });
      return { tree: t, under: under, hit: under.length ? under[under.length - 1].id : null };
    }
    ADE.dbgLayout = { hit: hit, VAR: VAR, TAP: TAP };
    var CAUSE = { guess: ['cause.none', 'cause.button', 'cause.button', 'cause.button'], inspect: ['cause.none', 'cause.none', 'cause.overlay', 'cause.fixed'] };
    var NODES = { guess: [[['tap', 'hit'], 'hit', 'e1'], [['button'], 'button', 'e3'], [['button'], 'button', 'e3'], [['button'], 'button', 'e3']],
      inspect: [[['inspector', 'hit'], 'inspector', 'e4'], [['inspector', 'overlay'], 'overlay', 'e4'], [['hit', 'overlay'], 'overlay', 'e2'], [['hit', 'button'], 'button', 'e3']] };
    var HL = { guess: [[5], [5], [5], [5]], inspect: [[7], [7], [2, 7], [8]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var r = hit(VAR[c][i]), ok = r.hit === 'button', bad = c === 'guess' && i >= 1, nd = NODES[c][i], ns = {};
        ns[nd[1]] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          metrics: { under: r.under.length, hit: M(m, 'hit.' + r.hit), booked: ok ? 1 : 0, cause: M(m, CAUSE[c][i]) },
          codeHighlight: { snippet: 'l6.screen', lines: HL[c][i] },
          movingSignals: [{ edge: nd[2], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : (i === 0 ? 'observe' : 'run')), subject: nd[1] }] });
        var tryIt = i === 0 && c === 'guess';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : 'source'), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'guess' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'tại (180, 624): 2 thành phần xử lý chạm (nút và lớp phủ); lớp phủ vẽ sau nên nhận cú chạm dù alpha 0', run: function () {
          var r = hit('base'); return r.under.length === 2 && r.hit === 'overlay' && r.tree.filter(function (n) { return n.id === 'overlay'; })[0].alpha === 0; } },
        { name: 'phóng nút lên 64 dp: lớp phủ vẫn nhận cú chạm', run: function () { return hit('tall').hit === 'overlay'; } },
        { name: 'gỡ lớp phủ khỏi cây: còn 1 thành phần, nút nhận cú chạm', run: function () { var r = hit('fixed'); return r.under.length === 1 && r.hit === 'button'; } },
        { name: 'mỗi cách 4 bước; dòng tô sáng nằm trong đoạn mã 8 dòng', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= 8; }); }); }); } }] });
  })();

  /* ================= l7: Database Inspector và Background Task Inspector: lịch đã lưu mà không hiện; đồng bộ kẹt =================
     Theo developer.android.com studio/inspect/database, studio/inspect/task, reference WorkInfo.State, define-work. CÀI THẬT: truy vấn áp lên các dòng
     của bảng booking; trạng thái worker tính theo luật WorkInfo.State (ràng buộc chưa thỏa: ENQUEUED; việc trước chưa SUCCEEDED: BLOCKED; FAILED,
     CANCELLED lan xuống). Dữ liệu bảng, tên worker và mạng 4G là của site. */
  (function () {
    var m = 'inspect', CASES = ['db', 'work'], KS = ['s1', 's2', 's3', 's4'];
    var ROWS = [[39, 'Phạm Thu', '20/11', 'CANCELLED'], [40, 'Trần Thị Bình', '22/11', 'COMPLETED'], [41, 'Lê Văn Cường', '24/11', 'COMPLETED'], [42, 'Nguyễn Văn An', '28/11', 'PENDING']];
    var Q = "SELECT * FROM booking WHERE status = 'CONFIRMED'";
    function table(edited) { return ROWS.map(function (r) { return r[0] === 42 && edited ? [r[0], r[1], r[2], 'CONFIRMED'] : r.slice(); }); }
    function query(rows) { return rows.filter(function (r) { return r[3] === 'CONFIRMED'; }); }
    var NET = 'METERED';   // 4G: có mạng nhưng đo lưu lượng
    var met = function (need, net) { return need === 'CONNECTED' ? net !== 'NONE' : (need === 'UNMETERED' ? net === 'UNMETERED' : true); };
    // [tên, ràng buộc, việc đi trước]; bản sửa: đồng bộ lịch hẹn không còn đứng sau việc tải ảnh
    var CHAIN = { base: [['UploadPhotos', 'UNMETERED', null], ['SyncBookings', 'CONNECTED', 'UploadPhotos'], ['NotifyUser', 'CONNECTED', 'SyncBookings']],
      fixed: [['UploadPhotos', 'UNMETERED', null], ['SyncBookings', 'CONNECTED', null], ['NotifyUser', 'CONNECTED', 'SyncBookings']] };
    function states(v, net) {
      var st = {};
      CHAIN[v].forEach(function (w) {
        var p = w[2] && st[w[2]];
        if (p === 'FAILED' || p === 'CANCELLED') st[w[0]] = p;
        else if (w[2] && p !== 'SUCCEEDED') st[w[0]] = 'BLOCKED';
        else st[w[0]] = met(w[1], net) ? 'SUCCEEDED' : 'ENQUEUED';
      });
      return st;
    }
    var finished = function (s) { return s === 'SUCCEEDED' || s === 'FAILED' || s === 'CANCELLED'; };
    function stuck(v) { var st = states(v, NET); return Object.keys(st).filter(function (k) { return !finished(st[k]); }).length; }
    ADE.dbgInspect = { table: table, query: query, Q: Q, states: states, CHAIN: CHAIN, NET: NET, stuck: stuck };
    var CAUSE = { db: ['cause.none', 'cause.none', 'cause.status', 'cause.fixed'], work: ['cause.none', 'cause.none', 'cause.wifi', 'cause.fixed'] };
    var NODES = { db: [[['app', 'db'], 'app', 'e1'], [['dbi', 'db'], 'db', 'e3'], [['dbi', 'db'], 'db', 'e3'], [['dbi', 'db', 'app'], 'app', 'e1']],
      work: [[['app', 'wm'], 'wm', 'e2'], [['bti', 'wm'], 'wm', 'e4'], [['bti', 'wm'], 'wm', 'e4'], [['app', 'wm'], 'wm', 'e2']] };
    var HL = { db: [[1, 2], [1, 2], [1], [4]], work: [[6], [6], [6], [8, 9]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var t = table(c === 'db' && i === 3), shown = c === 'db' ? query(t).length : 0, v = c === 'work' && i === 3 ? 'fixed' : 'base';
        var bad = i >= 1 && i <= 2, nd = NODES[c][i], ns = {};
        ns[nd[1]] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          metrics: { stored: c === 'db' ? t.length : 0, shown: shown, stuck: c === 'work' ? stuck(v) : 0, cause: M(m, CAUSE[c][i]) },
          codeHighlight: { snippet: 'l7.code', lines: HL[c][i] },
          movingSignals: [{ edge: nd[2], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : (i === 0 ? 'observe' : 'run')), subject: nd[1] }] });
        var tryIt = i === 0 && c === 'db';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : 'source'), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'db' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'bảng có 4 dòng, kể cả lịch 42 PENDING; truy vấn CONFIRMED trả 0 dòng; sửa 42 thành CONFIRMED thì trả đúng lịch 42', run: function () {
          var a = table(false), b = query(table(true)); return a.length === 4 && query(a).length === 0 && b.length === 1 && b[0][0] === 42; } },
        { name: 'trên 4G: UploadPhotos ENQUEUED (cần UNMETERED), hai worker sau BLOCKED; 3 worker chưa xong', run: function () {
          var s = states('base', 'METERED'); return s.UploadPhotos === 'ENQUEUED' && s.SyncBookings === 'BLOCKED' && s.NotifyUser === 'BLOCKED' && stuck('base') === 3; } },
        { name: 'tách chuỗi: SyncBookings và NotifyUser SUCCEEDED, chỉ UploadPhotos còn chờ Wi-Fi; có Wi-Fi thì cả chuỗi cũ cũng xong', run: function () {
          var s = states('fixed', 'METERED'), w = states('base', 'UNMETERED'); return s.SyncBookings === 'SUCCEEDED' && s.NotifyUser === 'SUCCEEDED' && stuck('fixed') === 1 && w.NotifyUser === 'SUCCEEDED'; } },
        { name: 'mỗi lỗi 4 bước; dòng tô sáng nằm trong đoạn mã 9 dòng', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= 9; }); }); }); } }] });
  })();

  /* ================= l8: rò rỉ bộ nhớ: listener đăng ký vào object toàn cục mà không hủy =================
     Theo developer.android.com memory-profiler (retained size, depth, references, lọc Activity rò), memory-overview (giới hạn heap, OOM), manage-app-memory,
     LeakCanary (thư viện bên ngoài). CÀI THẬT: đồ thị tham chiếu GC root → BookingEventBus → listeners → lambda → DetailActivity; sau GC, instance còn
     đường từ GC root thì ở lại. Bộ nhớ = nền + số Activity còn sống × 2,4 MB; vượt 64 MB là OOM. Các số MB là của site. */
  (function () {
    var m = 'leak', CASES = ['leak', 'fixed'], KS = ['s1', 's2', 's3', 's4'];
    var BASE = 18, PER = 2.4, LIMIT = 64, OPENS = [5, 5, 5, 20];
    var r1 = function (x) { return Math.round(x * 10) / 10; };
    // sau n lần mở rồi đóng (màn cuối còn mở), các Activity còn đường từ GC root
    function alive(c, n) {
      var reach = [];
      for (var k = 1; k <= n; k++) { var current = k === n, listened = c === 'leak' || current; if (listened || current) reach.push(k); }
      return reach;
    }
    var mem = function (c, n) { return r1(BASE + alive(c, n).length * PER); };
    function firstOom(c) { for (var n = 1; n <= 100; n++) if (mem(c, n) > LIMIT) return n; return null; }
    ADE.dbgLeak = { mem: mem, alive: alive, LIMIT: LIMIT, OPENS: OPENS, firstOom: firstOom };
    var NODES = { leak: [[['act'], 'act', 'e4'], [['act', 'lambda'], 'act', 'e4'], [['root', 'bus', 'list', 'lambda', 'act'], 'list', 'e2'], [['act'], 'act', 'e4']],
      fixed: [[['act'], 'act', 'e4'], [['act'], 'act', 'e4'], [['root', 'bus', 'list'], 'list', 'e2'], [['act'], 'act', 'e4']] };
    var HL = { leak: [[8], [8], [1, 2, 7], [8]], fixed: [[8, 9], [9], [9], [9]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var n = OPENS[i], mm = mem(c, n), inst = alive(c, n).length, bad = c === 'leak' && i >= 1, nd = NODES[c][i], ns = {};
        ns[nd[1]] = K + 'st.' + (bad ? 'surprise' : 'done');
        var oom = mm > LIMIT ? 'oom.crash' : (inst > 3 ? 'oom.slow' : 'oom.ok');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          metrics: { opens: n, mem: mm, inst: inst, oom: M(m, oom) },
          codeHighlight: { snippet: 'l8.code', lines: HL[c][i] },
          movingSignals: [{ edge: nd[2], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : (i === 0 ? 'observe' : 'run')), subject: nd[1] }] });
        var tryIt = i === 0 && c === 'leak';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : 'source'), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'leak' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'không hủy đăng ký: sau 5 lần mở còn 5 DetailActivity, 30 MB; mỗi lần thêm 2,4 MB', run: function () { return alive('leak', 5).length === 5 && mem('leak', 5) === 30 && mem('leak', 1) === 20.4; } },
        { name: 'OOM ở lần mở thứ 20: 18 + 20 × 2,4 = 66 MB > 64 MB; lần 19 là 63,6 MB', run: function () { return firstOom('leak') === 20 && mem('leak', 20) === 66 && mem('leak', 19) === 63.6; } },
        { name: 'hủy trong onDestroy: luôn 1 instance, 20,4 MB, không bao giờ OOM', run: function () { return alive('fixed', 20).length === 1 && mem('fixed', 20) === 20.4 && firstOom('fixed') === null; } },
        { name: 'mỗi cách 4 bước; dòng tô sáng nằm trong đoạn mã 10 dòng', run: function () {
          return CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= 10; }); }); }); } }] });
  })();

  /* ================= l9: khung hình giật: parse JSON trên luồng main hay trên luồng nền; 60 Hz rồi 120 Hz =================
     Theo developer.android.com vitals/render (16 ms ở 60 fps, 11 ms ở 90, 8 ms ở 120; quá hạn thì bỏ cả khung), tracing, custom-events, perfetto.dev.
     CÀI THẬT: 12 khung, mỗi khung = việc trên main + RenderThread nối tiếp; khung bắt đầu ở vsync kế tiếp sau khi khung trước xong; trễ khi dài hơn hạn,
     số vsync lỡ = ceil(thời lượng ÷ hạn) − 1. Số ms là của site. */
  (function () {
    var m = 'jank', CASES = ['main', 'bg'], KS = ['s1', 's2', 's3', 's4'];
    var N = 12, PAGE = [3, 8], RENDER = 2.5, BASE = 4, PARSE = 28, BIND = 5, HZ = [60, 60, 60, 120];
    var budget = function (hz) { return hz === 60 ? 16 : (hz === 90 ? 11 : 8); };
    function frames(c, hz) {
      var b = budget(hz), t = 0, out = [];
      for (var k = 0; k < N; k++) {
        var page = PAGE.indexOf(k) >= 0, main = page ? (c === 'main' ? BASE + PARSE : BIND) : BASE, dur = main + RENDER;
        var missed = dur > b ? Math.ceil(dur / b) - 1 : 0;
        out.push({ k: k, start: t, main: main, dur: dur, late: dur > b, missed: missed, page: page });
        t = Math.ceil((t + dur) / b) * b;
      }
      return { frames: out, total: t, budget: b };
    }
    function tally(c, hz) { var f = frames(c, hz).frames; return { late: f.filter(function (x) { return x.late; }).length, missed: f.reduce(function (s, x) { return s + x.missed; }, 0),
      longest: f.reduce(function (s, x) { return x.dur > s.dur ? x : s; }, f[0]) }; }
    ADE.dbgJank = { frames: frames, tally: tally, HZ: HZ, PARSE: PARSE, RENDER: RENDER };
    var NODES = { main: [[['vsync', 'main', 'render'], 'main', 'e1'], [['main'], 'main', 'e1'], [['main', 'screen'], 'screen', 'e3'], [['vsync', 'main'], 'vsync', 'e1']],
      bg: [[['worker', 'main'], 'worker', 'e4'], [['main', 'render'], 'main', 'e2'], [['worker'], 'worker', 'e4'], [['vsync', 'main', 'render'], 'screen', 'e3']] };
    var HL = { main: [[3], [3], [3], [3]], bg: [[8], [9], [8], [9]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var hz = HZ[i], t = tally(c, hz), bad = t.late > 0 && i >= 1, nd = NODES[c][i], ns = {};
        ns[nd[1]] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          metrics: { hz: hz, budget: budget(hz), late: t.late, missed: t.missed },
          codeHighlight: { snippet: 'l9.code', lines: HL[c][i] },
          movingSignals: [{ edge: nd[2], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : (i === 0 ? 'observe' : 'run')), subject: nd[1] }] });
        var tryIt = i === 0 && c === 'main';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : 'source'), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'main' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'parse trên main ở 60 Hz: 2 khung 34,5 ms trễ, mỗi khung lỡ 2 vsync, tổng 4; khung thường 6,5 ms', run: function () {
          var t = tally('main', 60), f = frames('main', 60).frames; return t.late === 2 && t.missed === 4 && f[3].dur === 34.5 && f[0].dur === 6.5; } },
        { name: 'ở 120 Hz (hạn 8 ms): vẫn 2 khung trễ, mỗi khung lỡ 4 vsync, tổng 8', run: function () { var t = tally('main', 120); return t.late === 2 && t.missed === 8; } },
        { name: 'parse trên luồng nền: khung nạp trang 7,5 ms; 0 khung trễ ở cả 60 và 120 Hz', run: function () {
          return tally('bg', 60).late === 0 && tally('bg', 120).late === 0 && frames('bg', 120).frames[3].dur === 7.5; } },
        { name: 'bài tập 90 Hz: 9 + 4 = 13 ms lỡ 1 vsync; 3 + 4 = 7 ms kịp; mỗi cách 4 bước, dòng tô sáng trong đoạn mã 9 dòng', run: function () {
          var b = budget(90); return b === 11 && Math.ceil(13 / b) - 1 === 1 && 7 < b &&
            CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= 9; }); }); }); } }] });
  })();

  /* ================= l10: ANR: luồng main chờ khóa do luồng sync giữ trong lúc gọi mạng; StrictMode bắt sớm =================
     Theo developer.android.com vitals/anr (5 giây cho input; chờ khóa của luồng khác), anrs/diagnose-and-fix-anrs (Blocked, held by), reference StrictMode.
     CÀI THẬT: luồng sync lấy khóa 1 giây trước khi bấm Lưu và giữ suốt lời gọi mạng; luồng main chờ phần còn lại; ANR khi chờ > 5 giây. Bản sửa gọi mạng
     ngoài khóa và chạy save trên luồng IO. Vi phạm StrictMode là các thao tác đĩa chạy trên luồng main. Thời gian mạng là của site. */
  (function () {
    var m = 'anr', CASES = ['trace', 'strict'], KS = ['s1', 's2', 's3', 's4'];
    var LEAD = 1, LIMIT = 5, NET = { wifi: 0.3, slow: 9 };
    var r1 = function (x) { return Math.round(x * 10) / 10; };
    // luồng main chờ bao lâu khi bấm Lưu ở t = 0
    function wait(net, fixed) { if (fixed) return 0; return r1(Math.max(0, NET[net] - LEAD)); }
    // các thao tác của save(); nằm trên main nếu chưa sửa
    var OPS = [['BookingRepo.save', 'DiskReadViolation'], ['BookingRepo.save', 'DiskWriteViolation']];
    function violations(onMain, enabled) { return enabled && onMain ? OPS.map(function (o) { return o[1] + ' at ' + o[0]; }) : []; }
    var PLAN = { trace: [['wifi', false], ['slow', false], ['slow', false], ['slow', true]], strict: [['wifi', false], ['wifi', false], ['wifi', false], ['wifi', true]] };
    function state(c, i) { var p = PLAN[c][i], w = wait(p[0], p[1]); return { net: p[0], netS: NET[p[0]], wait: w, anr: w > LIMIT, fixed: p[1],
      viol: c === 'strict' ? violations(!p[1], i >= 1) : [], strictOn: c === 'strict' && i >= 1 }; }
    ADE.dbgAnr = { state: state, LIMIT: LIMIT };
    var NODES = { trace: [[['tap', 'main'], 'main', 'e1'], [['main', 'lock'], 'lock', 'e2'], [['lock', 'sync'], 'sync', 'e3'], [['tap', 'main'], 'main', 'e1']],
      strict: [[['strict', 'main'], 'strict', 'e4'], [['strict', 'main'], 'main', 'e4'], [['main', 'lock'], 'lock', 'e2'], [['strict', 'main'], 'main', 'e4']] };
    var HL = { trace: [[3], [3], [4, 5], [10]], strict: [[12], [3], [3], [9]] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var st = state(c, i), bad = st.anr || st.viol.length > 0, nd = NODES[c][i], ns = {};
        ns[nd[1]] = K + 'st.' + (bad ? 'surprise' : 'done');
        var o = S(m, c + '.' + k, { type: i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism'), activeNodes: nd[0], nodeStates: ns,
          metrics: { net: st.netS, wait: st.wait, anr: M(m, st.anr ? 'anr.yes' : 'anr.no'), viol: st.viol.length },
          codeHighlight: { snippet: 'l10.code', lines: HL[c][i] },
          movingSignals: [{ edge: nd[2], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : (i === 0 ? 'observe' : 'run')), subject: nd[1] }] });
        var tryIt = i === 0 && c === 'trace';
        o.callouts = [{ kind: tryIt ? 'try' : (bad ? 'pitfall' : 'source'), textKey: tryIt ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'trace' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'Wi-Fi nhanh (0,3 giây): luồng main chờ 0 giây, không ANR', run: function () { var s = state('trace', 0); return s.wait === 0 && !s.anr; } },
        { name: '4G chậm (9 giây): luồng main chờ 8 giây > 5, ANR', run: function () { var s = state('trace', 1); return s.wait === 8 && s.anr; } },
        { name: 'gọi mạng ngoài khóa, save trên luồng IO: chờ 0 giây trên 4G chậm', run: function () { var s = state('trace', 3); return s.wait === 0 && !s.anr && s.net === 'slow'; } },
        { name: 'StrictMode: chưa bật 0 vi phạm; bật thì 2 (đọc và ghi đĩa trong save); dời save khỏi main thì 0; mỗi cách 4 bước, dòng tô sáng trong đoạn mã 12 dòng', run: function () {
          return state('strict', 0).viol.length === 0 && state('strict', 1).viol.length === 2 && state('strict', 3).viol.length === 0 &&
            CASES.every(function (c) { return steps({ case: c }).length === 4 && HL[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= 12; }); }); }); } }] });
  })();
})();
