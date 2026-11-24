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

  /* ================= I2: tiến trình, bộ nhớ và cái chết của process — form trong ViewModel so với saved state =================
     Theo developer.android.com: Processes and app lifecycle (bậc foreground, visible, service, cached; giết cached trước),
     Activity lifecycle (hệ thống giết process, không giết Activity), Save UI states (ViewModel mất khi process bị giết; saved state
     lưu lúc onStop, bản sao ngoài process), Get a result from an activity (camera: process gần như chắc chắn bị hủy),
     ComponentCallbacks2 (từ API 34 chỉ còn UI_HIDDEN, BACKGROUND); source.android.com lmkd. Số MB là minh họa (RAM 4 GB). */
  (function () {
    var m = 'process', CASES = ['vm', 'saved'], KS = ['s1', 's2', 's3', 's4'];
    // bậc của app và Camera ở mỗi bước ('' = không có process)
    var LV = { app: ['fg', 'cached', 'gone', 'fg'], cam: ['', 'fg', 'fg', 'cached'] };
    // RAM (MB): hệ thống, Camera, app khác ở nền, Hẹn Khám, trống — tổng 4000
    var MEM = [[1500, 0, 1400, 300, 800], [1500, 900, 1000, 300, 300], [1500, 1500, 600, 0, 400], [1500, 1500, 600, 300, 100]];
    // còn lại gì: [hàng, đang giữ, trạng thái] theo cách và bước
    var SURV = {
      vm: [[['vm', 'form', 'live'], ['saved', 'none', 'na'], ['disk', 'photo', 'nofile']],
           [['vm', 'form', 'live'], ['saved', 'none', 'na'], ['disk', 'photo', 'writing']],
           [['vm', 'form', 'lost'], ['saved', 'none', 'na'], ['disk', 'photo', 'kept']],
           [['vm', 'form', 'empty'], ['saved', 'none', 'na'], ['disk', 'photo', 'orphan']]],
      saved: [[['vm', 'form', 'live'], ['saved', 'ids', 'live'], ['disk', 'photo', 'nofile']],
              [['vm', 'form', 'live'], ['saved', 'ids', 'copied'], ['disk', 'photo', 'writing']],
              [['vm', 'form', 'lost'], ['saved', 'ids', 'kept'], ['disk', 'photo', 'pending']],
              [['vm', 'form', 'refilled'], ['saved', 'ids', 'restored'], ['disk', 'photo', 'attached']]]
    };
    var BAD = { lost: 1, empty: 1, orphan: 1 };
    function fields(c, i) { if (i === 3) return c === 'vm' ? 0 : 3; return i === 2 ? (c === 'vm' ? 0 : 2) : 2; }
    ADE.sysProcess = { LV: LV, MEM: MEM, SURV: SURV, BAD: BAD };
    var LINES = { vm: [[2, 3], [6, 7], [8], [4, 9]], saved: [[2, 3], [4, 6], [7], [8, 9]] };
    var NODES = [['app'], ['app', 'camera'], ['lmkd', 'app'], ['app', 'store']];
    var EDGE = ['', 'e1', 'e3', 'e4'];
    function steps(s) {
      return KS.map(function (k, i) {
        var bad = s.case === 'vm' && i === 3, type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism');
        var ns = { app: K + 'st.' + (i === 2 ? 'broken' : (bad ? 'surprise' : 'done')) };
        if (i >= 1) ns.camera = K + 'st.done';
        if (i >= 2) ns.lmkd = K + 'st.done';
        ns.store = K + 'st.' + (s.case === 'vm' ? 'skipped' : 'done');
        var o = S(m, s.case + '.' + k, { type: type, activeNodes: NODES[i], nodeStates: ns,
          metrics: { fields: fields(s.case, i), free: MEM[i][4], starts: i === 3 ? 2 : 1 },
          codeHighlight: { snippet: 'i2.' + s.case, lines: LINES[s.case][i] },
          movingSignals: EDGE[i] ? [{ edge: EDGE[i], tok: i === 2 || bad ? 'signal' : 'state' }] : [],
          logEvents: [{ t: i, kind: i === 2 ? 'exception' : (bad ? 'exception' : (i === 3 ? 'complete' : (i === 0 ? 'write' : 'observe'))), subject: NODES[i][0] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'vm' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'RAM mỗi bước cộng lại đúng 4000 MB', run: function () { return MEM.every(function (r) { return r.reduce(function (x, y) { return x + y; }, 0) === 4000; }); } },
        { name: 'process bị giết ở bước 3: không còn RAM của app, ViewModel mất ở cả hai cách', run: function () { return MEM[2][3] === 0 && LV.app[2] === 'gone' && CASES.every(function (c) { return SURV[c][2][0][2] === 'lost'; }); } },
        { name: 'quay lại: chỉ ViewModel thì form rỗng và ảnh mồ côi; saved state thì đủ 3 ô', run: function () { return fields('vm', 3) === 0 && SURV.vm[3][2][2] === 'orphan' && fields('saved', 3) === 3 && SURV.saved[3][1][2] === 'restored'; } },
        { name: 'mỗi cách có 4 bước, dòng mã nằm trong đoạn mã', run: function () { return CASES.every(function (c) { return steps({ case: c }).length === 4 && LINES[c].every(function (l) { return l.every(function (n) { return n >= 1 && n <= (c === 'vm' ? 9 : 10); }); }); }); } }] });
  })();

  /* ================= I3: luồng, khóa, ANR và deadlock — giữ khóa lâu, hai khóa ngược thứ tự, một thứ tự chung =================
     Theo developer.android.com ANRs (sự kiện nhập 5 giây; main thread chờ khóa; deadlock; Mutex.withLock), Processes and threads
     overview (đừng chặn UI thread); kotlinx.coroutines Mutex; OS Concepts bản 10 ch.8 (bốn điều kiện, đồ thị chờ, thứ tự khóa).
     Mốc thời gian là minh họa: chạm ở giây 1, ANR ở giây 6. */
  (function () {
    var m = 'lock', CASES = ['hold', 'cycle', 'order'], KS = ['s1', 's2', 's3', 's4'];
    // làn thời gian: [bắt đầu, kết thúc (giây), loại, nhãn]
    var LANES = {
      hold: { main: [[1, 7, 'wait', 'waitC'], [7, 8, 'run', 'draw']], sync: [[0, 7, 'hold', 'holdC']] },
      cycle: { main: [[1, 2, 'run', 'ui'], [2, 3, 'hold', 'holdC2'], [3, 8, 'wait', 'waitD']], sync: [[0, 3, 'hold', 'holdD'], [3, 8, 'wait', 'waitC']] },
      order: { main: [[1.1, 1.3, 'wait', ''], [1.3, 1.4, 'hold', ''], [1.4, 2, 'run', 'draw']], sync: [[1, 1.3, 'hold', 'copy'], [1.3, 7, 'run', 'write']] }
    };
    var TS = { hold: [1, 3, 6, 8], cycle: [1, 2, 3, 8], order: [1.1, 1.3, 2, 8] };
    var ANR = { hold: 6, cycle: 6, order: null };
    var WF = { hold: [[], [['main', 'sync', 'cacheLock']], [['main', 'sync', 'cacheLock']], []],
      cycle: [[], [], [['main', 'sync', 'dbLock'], ['sync', 'main', 'cacheLock']], [['main', 'sync', 'dbLock'], ['sync', 'main', 'cacheLock']]],
      order: [[], [['main', 'sync', 'cacheLock']], [], []] };
    function blocked(c, i) { var t = TS[c][i]; return Math.round(LANES[c].main.reduce(function (acc, g) { return g[2] === 'wait' && g[0] < t ? acc + Math.min(g[1], t) - g[0] : acc; }, 0) * 1000); }
    function anr(c, i) { return ANR[c] !== null && TS[c][i] >= ANR[c] ? 1 : 0; }
    function cyc(c, i) { var e = WF[c][i]; return e.some(function (a) { return e.some(function (b) { return a[0] === b[1] && a[1] === b[0]; }); }) ? 1 : 0; }
    // bốn điều kiện tại bước: loại trừ, giữ và chờ, không tước, chờ vòng
    function conds(c, i) { var w = cyc(c, i) === 1; return { me: true, hw: c === 'cycle' && i >= 2, np: true, cw: w }; }
    ADE.sysLock = { LANES: LANES, TS: TS, ANR: ANR, WF: WF, blocked: blocked, conds: conds };
    var LINES = { hold: [[2, 3], [6], [6], [4, 7]], cycle: [[2], [6], [3, 7], [3, 7]], order: [[1, 2], [5], [3, 6], [7]] };
    var NODES = { hold: [['sync', 'cache'], ['main', 'cache'], ['main'], ['main', 'sync']], cycle: [['sync', 'db'], ['main', 'cache'], ['main', 'sync', 'cache', 'db'], ['main', 'sync']], order: [['sync', 'cache', 'db'], ['main', 'cache'], ['main', 'sync'], ['sync', 'db']] };
    var EDGE = { hold: ['e3', 'e1', 'e1', 'e1'], cycle: ['e4', 'e1', 'e2', 'e2'], order: ['e3', 'e1', 'e1', 'e4'] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var bad = anr(c, i) === 1 || cyc(c, i) === 1, type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism');
        var ns = {}; NODES[c][i].forEach(function (n) { ns[n] = K + 'st.' + (bad && (n === 'main' || n === 'sync') ? 'surprise' : 'done'); });
        var o = S(m, c + '.' + k, { type: type, activeNodes: NODES[c][i], nodeStates: ns,
          metrics: { blocked: blocked(c, i), anr: anr(c, i), cycle: cyc(c, i) },
          codeHighlight: { snippet: 'i3.' + c, lines: LINES[c][i] },
          movingSignals: [{ edge: EDGE[c][i], tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : 'run'), subject: NODES[c][i][0] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'hold' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'giữ khóa lâu: ANR nhưng không có vòng chờ; main bị chặn 6 giây', run: function () { return anr('hold', 3) === 1 && [0, 1, 2, 3].every(function (i) { return cyc('hold', i) === 0; }) && blocked('hold', 3) === 6000; } },
        { name: 'ngược thứ tự: vòng chờ từ bước 3, đủ bốn điều kiện, rồi ANR', run: function () { var k = conds('cycle', 2); return cyc('cycle', 2) === 1 && k.me && k.hw && k.np && k.cw && anr('cycle', 3) === 1; } },
        { name: 'một thứ tự chung: không vòng, không ANR, main chờ dưới 1 giây', run: function () { return [0, 1, 2, 3].every(function (i) { return cyc('order', i) === 0 && anr('order', i) === 0 && blocked('order', i) < 1000; }); } },
        { name: 'mỗi cách 4 bước; dòng mã nằm trong đoạn mã', run: function () { var n = { hold: 8, cycle: 8, order: 7 }; return CASES.every(function (c) { return steps({ case: c }).length === 4 && LINES[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= n[c]; }); }); }); } }] });
  })();

  /* ================= I4: chọn kênh giao tiếp — polling, long polling, WebSocket, FCM cho cùng một tin =================
     Theo Alex Xu tập 1 ch.12; developer.android.com (Optimize network access: radio ~18 giây sau mỗi lần truyền; Doze tạm dừng mạng);
     Firebase (FCM overview, priority, collapsible); MDN (SSE, WebSocket). Tin tới server ở giây 7; chu kỳ 5 giây, hạn chờ 30 giây là minh họa. */
  (function () {
    var m = 'channel', CASES = ['poll', 'long', 'ws', 'push'], KS = ['s1', 's2', 's3', 's4'];
    var PARTS = { poll: ['app', 'server'], long: ['app', 'server'], ws: ['app', 'server'], push: ['app', 'fcm', 'server'] };
    // tin mỗi bước: [từ, tới, nhãn, 1 nếu phí hay không tới]
    var MSGS = {
      poll: [[['app', 'server', 'q0', 0], ['server', 'app', 'none', 1]], [['app', 'server', 'q5', 0], ['server', 'app', 'none', 1]],
             [['server', 'server', 'arrive', 0], ['app', 'server', 'q10', 0], ['server', 'app', 'one', 0]], [['app', 'server', 'more', 0], ['server', 'app', 'none4', 1]]],
      long: [[['app', 'server', 'lq0', 0]], [['server', 'server', 'hold', 0]], [['server', 'server', 'arrive', 0], ['server', 'app', 'lone', 0], ['app', 'server', 'lq7', 0]], [['server', 'app', 'ltimeout', 1], ['app', 'server', 'lq37', 0]]],
      ws: [[['app', 'server', 'up', 0], ['server', 'app', 'ok', 0]], [['app', 'server', 'send', 0]], [['server', 'server', 'arrive', 0], ['server', 'app', 'wpush', 0]], [['app', 'app', 'doze', 1], ['server', 'app', 'lost', 1]]],
      push: [[['app', 'fcm', 'token', 0], ['app', 'server', 'reg', 0]], [['app', 'app', 'idle', 0]], [['server', 'server', 'arrive', 0], ['server', 'fcm', 'fsend', 0], ['fcm', 'app', 'fdeliver', 0]], [['app', 'app', 'notify', 0], ['app', 'server', 'fetch', 0]]]
    };
    var REQS = { poll: [1, 2, 3, 7], long: [1, 1, 2, 3], ws: [1, 1, 1, 1], push: [1, 1, 1, 2] };
    var LAT = { poll: 3, long: 0, ws: 0, push: 0 };
    var BG = { poll: 0, long: 0, ws: 0, push: 1 };
    ADE.sysChannel = { PARTS: PARTS, MSGS: MSGS, ROWS: ['poll', 'long', 'sse', 'ws', 'push'] };
    var LINES = { poll: [[2], [4], [2, 3], [1, 4]], long: [[2], [2], [3], [2]], ws: [[1], [5], [2], [3, 6]], push: [[1], [2], [3, 4], [5]] };
    var NODES = { poll: ['app', 'server'], long: ['app', 'server'], ws: ['app', 'server'], push: ['app', 'fcm', 'server'] };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var bad = MSGS[c][i].some(function (x) { return x[3] === 1; }), type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism');
        var ns = {}; NODES[c].forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        if (c !== 'push') ns.fcm = K + 'st.skipped';
        var first = MSGS[c][i][0], edge = c === 'push' ? (first[1] === 'fcm' || first[0] === 'fcm' ? (first[0] === 'server' ? 'e3' : 'e2') : 'e1') : 'e1';
        var o = S(m, c + '.' + k, { type: type, activeNodes: NODES[c], nodeStates: ns,
          metrics: { reqs: REQS[c][i], latency: i >= 2 ? LAT[c] : 0, bg: BG[c] },
          codeHighlight: { snippet: 'i4.' + c, lines: LINES[c][i] },
          movingSignals: [{ edge: edge, tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'skip' : (i === 3 ? 'complete' : 'run'), subject: first[0] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'poll' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'polling: 7 lượt hỏi trong 30 giây (0, 5, …, 30), tin trễ 3 giây', run: function () { return REQS.poll[3] === 7 && LAT.poll === 3; } },
        { name: 'chỉ FCM nhận được khi app ở nền; WebSocket mất tin khi Doze', run: function () { return BG.push === 1 && BG.ws === 0 && MSGS.ws[3].every(function (x) { return x[3] === 1; }); } },
        { name: 'tin của mọi kênh chỉ dùng các bên của kênh đó', run: function () { return CASES.every(function (c) { return MSGS[c].every(function (r) { return r.every(function (x) { return PARTS[c].indexOf(x[0]) >= 0 && PARTS[c].indexOf(x[1]) >= 0; }); }); }); } },
        { name: 'mỗi kênh 4 bước; dòng mã nằm trong đoạn mã', run: function () { var n = { poll: 5, long: 4, ws: 6, push: 6 }; return CASES.every(function (c) { return steps({ case: c }).length === 4 && LINES[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= n[c]; }); }); }); } }] });
  })();

  /* ================= I5: mạng không tin cậy — request mất, response mất, Idempotency-Key, bão thử lại =================
     Theo DDIA bản 2 (ch.9 không phân biệt được; ch.12 idempotence; ch.2 retry storm, backoff), RFC 9110, bản nháp IETF Idempotency-Key 09,
     WorkManager define-work. Thời hạn chờ, khoảng thử và giá trị jitter là minh họa (jitter cố định để mô phỏng tất định). */
  (function () {
    var m = 'retry', CASES = ['reqlost', 'resplost', 'key', 'storm'], KS = ['s1', 's2', 's3', 's4'];
    var MSGS = {
      reqlost: [[['app', 'mid', 'book', 1], ['mid', 'mid', 'lostreq', 1]], [['app', 'app', 'timeout', 0]], [['app', 'server', 'retry', 0], ['server', 'server', 'c41', 0], ['server', 'app', 'r41', 0]], [['server', 'server', 'one', 0]]],
      resplost: [[['app', 'server', 'book', 0], ['server', 'server', 'c41', 0]], [['server', 'mid', 'lost41', 1], ['app', 'app', 'timeout', 0]], [['app', 'server', 'retry', 0], ['server', 'server', 'c42', 1], ['server', 'app', 'r42', 0]], [['server', 'server', 'two', 1]]],
      key: [[['app', 'app', 'genkey', 0], ['app', 'server', 'bookk', 0], ['server', 'server', 'c41k', 0]], [['server', 'mid', 'lost41', 1], ['app', 'app', 'timeout', 0]], [['app', 'server', 'retryk', 0], ['server', 'server', 'seen', 0], ['server', 'app', 'same', 0]], [['server', 'server', 'one', 0]]],
      storm: [[], [], [], []]
    };
    // lịch trên server sau mỗi bước: [id, key, trùng]
    var BOOK = {
      reqlost: [[], [], [['#41', '', 0]], [['#41', '', 0]]],
      resplost: [[['#41', '', 0]], [['#41', '', 0]], [['#41', '', 0], ['#42', '', 1]], [['#41', '', 0], ['#42', '', 1]]],
      key: [[['#41', 'k-7f3a', 0]], [['#41', 'k-7f3a', 0]], [['#41', 'k-7f3a', 0]], [['#41', 'k-7f3a', 0]]],
      storm: [[], [], [], []]
    };
    var ATT = { reqlost: [1, 1, 2, 2], resplost: [1, 1, 2, 2], key: [1, 1, 2, 2] };
    // bão thử lại: thời điểm gửi (giây) của 5 máy theo từng cách; 0 là lần gửi đầu cùng thất bại
    var EVERY2 = [2, 4, 6, 8, 10, 12, 14, 16], EXP = [1, 3, 7, 15];
    var JIT = [[0.1, 1.2, 3.9, 9.6], [0.3, 2.1, 4.6, 11.2], [0.55, 1.6, 5.3, 8.4], [0.7, 2.6, 3.1, 10.5], [0.95, 1.9, 5.6, 10.1]];
    var SCHED = { fail: [[], [], [], [], []], fixed: [EVERY2, EVERY2, EVERY2, EVERY2, EVERY2], exp: [EXP, EXP, EXP, EXP, EXP], jitter: JIT };
    var STORM_KIND = ['fail', 'fixed', 'exp', 'jitter'];
    function peak(kind) { var b = {}; SCHED[kind].forEach(function (ph) { ph.forEach(function (t) { var k = Math.floor(t * 2); b[k] = (b[k] || 0) + 1; }); }); var mx = 0; for (var k in b) if (b[k] > mx) mx = b[k]; return kind === 'fail' ? 5 : mx; }
    function sends(kind) { return 5 + SCHED[kind].reduce(function (a, ph) { return a + ph.length; }, 0); }
    ADE.sysRetry = { MSGS: MSGS, BOOK: BOOK, SCHED: SCHED, STORM_KIND: STORM_KIND, peak: peak };
    var LINES = { reqlost: [[3], [4], [2, 3], [3]], resplost: [[3], [4], [3], [2]], key: [[1, 3], [4], [3, 6], [6]], storm: [[1], [1, 2], [3, 4], [5]] };
    var SNIP = { reqlost: 'i5.nokey', resplost: 'i5.nokey', key: 'i5.key', storm: 'i5.storm' };
    function steps(s) {
      var c = s.case;
      return KS.map(function (k, i) {
        var bad = c === 'storm' ? (i >= 1 && peak(STORM_KIND[i]) >= 4) : (MSGS[c][i].some(function (x) { return x[3] === 1; }) || BOOK[c][i].some(function (b) { return b[2] === 1; }));
        if (c === 'storm' && i === 0) bad = false;
        var type = i === 0 ? 'scenario' : (bad ? 'pitfall' : 'mechanism');
        var nodes = c === 'storm' ? ['app', 'server'] : (i === 1 ? ['app', 'net'] : ['app', 'net', 'server']);
        var ns = {}; nodes.forEach(function (n) { ns[n] = K + 'st.' + (bad ? 'surprise' : 'done'); });
        var met = c === 'storm' ? { attempts: sends(STORM_KIND[i]), bookings: 0, peak: peak(STORM_KIND[i]) } : { attempts: ATT[c][i], bookings: BOOK[c][i].length, peak: 1 };
        var o = S(m, c + '.' + k, { type: type, activeNodes: nodes, nodeStates: ns, metrics: met,
          codeHighlight: { snippet: SNIP[c], lines: LINES[c][i] },
          movingSignals: [{ edge: i === 1 && c !== 'storm' ? 'e2' : 'e1', tok: bad ? 'signal' : 'state' }],
          logEvents: [{ t: i, kind: bad ? 'exception' : (i === 3 ? 'complete' : 'run'), subject: nodes[0] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (bad ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + c + '.' + k) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'resplost' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'response mất + thử lại không key: hai lịch; có key: một lịch', run: function () { return BOOK.resplost[3].length === 2 && BOOK.key[3].length === 1 && BOOK.reqlost[3].length === 1; } },
        { name: 'bão thử lại: cố định và exponential đỉnh 5, có jitter đỉnh 3', run: function () { return peak('fixed') === 5 && peak('exp') === 5 && peak('jitter') === 3; } },
        { name: 'jitter đầy đủ: mỗi khoảng chờ nằm trong [0, 2^n) giây', run: function () { return JIT.every(function (ph) { var prev = 0; return ph.every(function (t, n) { var d = t - prev; prev = t; return d >= 0 && d < Math.pow(2, n); }); }); } },
        { name: 'mỗi tình huống 4 bước; dòng mã nằm trong đoạn mã', run: function () { var n = { reqlost: 7, resplost: 7, key: 6, storm: 5 }; return CASES.every(function (c) { return steps({ case: c }).length === 4 && LINES[c].every(function (l) { return l.every(function (x) { return x >= 1 && x <= n[c]; }); }); }); } }] });
  })();
})();
