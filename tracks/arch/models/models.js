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
  /* ================= G2a: hướng phụ thuộc giữa các tầng (đồ thị "A biết về B") =================
     Theo Guide to app architecture (mũi tên trong hướng dẫn là phụ thuộc giữa các lớp; domain phụ thuộc data), Domain layer
     (use case phụ thuộc repository), Modularization và Common modularization patterns (internal ẩn khai báo khỏi module khác;
     giao tiếp hai chiều trực tiếp giữa hai module là không thể vì phụ thuộc vòng), Kotlin Visibility modifiers (module là tập file
     biên dịch cùng nhau), Boudjnah ch1–2 (Dependency Rule: mũi tên hướng vào domain; đảo phụ thuộc bằng interface repository đặt
     cạnh use case). Cạnh của từng bước nằm ở ADE.archLayers để hình đồ thị (views/visuals.js) và model dùng chung một dữ liệu. */
  (function () {
    var m = 'layers', CASES = ['google', 'wrong', 'modules', 'inverted'], KS = ['s1', 's2', 's3', 's4'];
    var BASE = [['ui', 'vm'], ['vm', 'uc'], ['uc', 'repo'], ['repo', 'api'], ['repo', 'dao']];
    var NOUC = [['ui', 'vm'], ['vm', 'repo'], ['repo', 'api'], ['repo', 'dao']];
    var INV = [['ui', 'vm'], ['vm', 'uc'], ['repo', 'uc'], ['repo', 'api'], ['repo', 'dao']];
    var BAD = BASE.concat([['repo', 'ui']]);
    var MODS = [['feature', ['ui', 'vm']], ['domain', ['uc']], ['data', ['repo', 'api', 'dao']]];
    var ok = { ui: 'done', vm: 'done', uc: 'done', repo: 'done', api: 'done', dao: 'done' };
    var st = function (o) { var n = {}, k; for (k in ok) n[k] = ok[k]; for (k in o) n[k] = o[k]; return n; };
    // mỗi bước: [cạnh, nhóm module (null = một module), kết quả build, node sáng, trạng thái node, số đo {wrong, caught, test}, loại bước, dòng mã, loại log, chủ thể, dữ liệu đi ngược lên]
    var P = {
      google: [
        [BASE, null, 'na', ['ui', 'vm', 'uc', 'repo'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'scenario', [1, 2, 3, 4, 5, 6, 7], 'observe', 'ui', false],
        [BASE, null, 'na', ['dao', 'repo', 'uc', 'vm', 'ui'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'mechanism', [7, 8], 'run', 'repo', true],
        [NOUC, null, 'na', ['vm', 'repo'], st({ uc: 'skipped' }), { wrong: 0, caught: 'na', test: 'jvm' }, 'mechanism', [3, 5], 'write', 'vm', false],
        [BASE, null, 'na', ['repo', 'api', 'dao'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'mechanism', [10, 11], 'complete', 'repo', false]],
      wrong: [
        [BASE, null, 'na', ['repo'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'scenario', [3, 4, 5, 6], 'observe', 'repo', false],
        [BAD, null, 'na', ['repo', 'ui'], st({ repo: 'surprise' }), { wrong: 1, caught: 'na', test: 'jvm' }, 'pitfall', [1, 2, 3, 4, 5], 'write', 'repo', false],
        [BAD, null, 'pass', ['repo', 'ui'], st({ repo: 'surprise' }), { wrong: 1, caught: 'none', test: 'jvm' }, 'pitfall', [7], 'run', 'repo', false],
        [BAD, null, 'pass', ['ui', 'vm', 'uc', 'repo'], st({ repo: 'surprise', ui: 'surprise' }), { wrong: 1, caught: 'none', test: 'device' }, 'pitfall', [3, 8], 'observe', 'repo', false]],
      modules: [
        [BASE, MODS, 'na', ['ui', 'vm', 'uc', 'repo'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'scenario', [1, 2], 'observe', 'repo', false],
        [BAD, MODS, 'unresolved', ['repo', 'ui'], st({ repo: 'broken' }), { wrong: 1, caught: 'compiler', test: 'jvm' }, 'mechanism', [3, 4], 'exception', 'repo', false],
        [BAD, MODS, 'cycle', ['repo', 'ui', 'vm', 'uc'], st({ repo: 'broken', ui: 'broken' }), { wrong: 1, caught: 'gradle', test: 'jvm' }, 'pitfall', [5, 6, 7], 'exception', 'repo', false],
        [BASE, MODS, 'pass', ['vm', 'repo'], ok, { wrong: 0, caught: 'gradle', test: 'jvm' }, 'mechanism', [8, 9], 'complete', 'vm', false]],
      inverted: [
        [BASE, null, 'na', ['uc', 'repo'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'scenario', [1, 2, 3], 'observe', 'uc', false],
        [INV, null, 'na', ['uc', 'repo'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'mechanism', [1, 2, 4, 5], 'write', 'repo', false],
        [INV, null, 'na', ['uc'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'mechanism', [1, 2, 3], 'run', 'uc', false],
        [INV, null, 'pass', ['repo', 'uc'], ok, { wrong: 0, caught: 'na', test: 'jvm' }, 'mechanism', [6, 7], 'complete', 'repo', false]]
    };
    ADE.archLayers = {
      CASES: CASES,
      at: function (c, i) {
        var p = P[c][i];
        return { edges: p[0].map(function (x) { return { from: x[0], to: x[1], bad: x[0] === 'repo' && x[1] === 'ui' }; }), mods: p[1], build: p[2], dataUp: p[10], noUc: p[0] === NOUC };
      }
    };
    var EDGE = { 'ui>vm': 'e1', 'vm>uc': 'e2', 'uc>repo': 'e3', 'repo>api': 'e4', 'repo>dao': 'e5' };
    function steps(s) {
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[4]).forEach(function (n) { ns[n] = K + 'st.' + p[4][n]; });
        var met = { wrong: p[5].wrong, caught: M(m, 'caught.' + p[5].caught), test: M(m, 'test.' + p[5].test) };
        var sig;
        if (p[10]) sig = [{ edge: 'e5', tok: 'state', reverse: true }, { edge: 'e3', tok: 'state', reverse: true }, { edge: 'e2', tok: 'state', reverse: true }, { edge: 'e1', tok: 'state', reverse: true }];
        else if (s.case === 'inverted' && i >= 1) sig = [{ edge: 'e3', tok: 'state', reverse: true }];
        else sig = [{ edge: EDGE[p[3][0] + '>' + p[3][1]] || 'e1', tok: p[6] === 'pitfall' ? 'signal' : 'state' }];
        var o = S(m, s.case + '.' + KS[i], { type: p[6], activeNodes: p[3], nodeStates: ns, metrics: met, codeHighlight: { snippet: 'g2.' + s.case, lines: p[7] },
          movingSignals: sig, logEvents: [{ t: i, kind: p[8], subject: p[9] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (p[6] === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'google' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'một module: phụ thuộc sai vẫn biên dịch qua, không ai bắt', run: function () { var a = ADE.archLayers.at('wrong', 2); return a.build === 'pass' && a.edges.some(function (x) { return x.bad; }) && steps({ case: 'wrong' })[2].metrics.caught === M(m, 'caught.none'); } },
        { name: 'tách module: trình biên dịch bắt import sai, Gradle chặn vòng phụ thuộc', run: function () { return ADE.archLayers.at('modules', 1).build === 'unresolved' && ADE.archLayers.at('modules', 2).build === 'cycle'; } },
        { name: 'đảo phụ thuộc: repository trỏ vào domain, domain không trỏ ra ngoài', run: function () { var ed = ADE.archLayers.at('inverted', 3).edges; return ed.some(function (x) { return x.from === 'repo' && x.to === 'uc'; }) && !ed.some(function (x) { return x.from === 'uc'; }); } }] });
  })();

  /* ================= G2b: một nguồn sự thật (SSOT) và luồng dữ liệu một chiều (UDF) =================
     Theo Guide to app architecture (SSOT là chủ của dữ liệu, chỉ SSOT được sửa, lộ ra kiểu bất biến; UDF: state đi xuống,
     sự kiện đi lên tới SSOT), Data layer (mỗi repository định nghĩa một SSOT; dữ liệu lộ ra phải bất biến), UI layer (vòng UDF). */
  (function () {
    var m = 'ssot', CASES = ['twowriters', 'ssot'], KS = ['s1', 's2', 's3', 's4'];
    // mỗi bước: [node sáng, trạng thái node, số đo {copies, writers, agree}, loại bước, dòng mã, loại log, chủ thể, tín hiệu]
    var P = {
      twowriters: [
        [['choose'], { choose: 'done', mine: 'done', repo: 'done' }, { copies: 2, writers: 2, agree: 'na' }, 'scenario', [2, 3], 'write', 'choose', [{ edge: 'e1', tok: 'signal' }]],
        [['mine'], { choose: 'done', mine: 'surprise', repo: 'done' }, { copies: 3, writers: 2, agree: 'no' }, 'pitfall', [4], 'observe', 'mine', [{ edge: 'e4', tok: 'state' }]],
        [['mine', 'repo'], { choose: 'done', mine: 'surprise', repo: 'surprise' }, { copies: 3, writers: 3, agree: 'no' }, 'pitfall', [5], 'write', 'mine', [{ edge: 'e3', tok: 'signal' }]],
        [['choose', 'mine', 'repo'], { choose: 'surprise', mine: 'surprise', repo: 'surprise' }, { copies: 3, writers: 3, agree: 'no' }, 'pitfall', [1, 2, 4], 'observe', 'choose', [{ edge: 'e2', tok: 'state' }]]],
      ssot: [
        [['choose', 'repo'], { choose: 'done', mine: 'done', repo: 'done' }, { copies: 1, writers: 1, agree: 'na' }, 'scenario', [3, 6], 'write', 'choose', [{ edge: 'e1', tok: 'signal' }]],
        [['repo'], { choose: 'done', mine: 'done', repo: 'done' }, { copies: 1, writers: 1, agree: 'na' }, 'mechanism', [1, 2, 3], 'run', 'repo', [{ edge: 'e1', tok: 'signal' }]],
        [['repo', 'choose', 'mine'], { choose: 'done', mine: 'done', repo: 'done' }, { copies: 1, writers: 1, agree: 'yes' }, 'mechanism', [2, 7, 8], 'observe', 'repo', [{ edge: 'e2', tok: 'state' }, { edge: 'e4', tok: 'state' }]],
        [['mine', 'repo', 'choose'], { choose: 'done', mine: 'done', repo: 'done' }, { copies: 1, writers: 1, agree: 'yes' }, 'mechanism', [4, 8], 'complete', 'mine', [{ edge: 'e3', tok: 'signal' }, { edge: 'e2', tok: 'state' }]]]
    };
    function steps(s) {
      return P[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var met = { copies: p[2].copies, writers: p[2].writers, agree: M(m, 'agree.' + p[2].agree) };
        var o = S(m, s.case + '.' + KS[i], { type: p[3], activeNodes: p[0], nodeStates: ns, metrics: met, codeHighlight: { snippet: 'g2.' + s.case, lines: p[4] },
          movingSignals: p[7], logEvents: [{ t: i, kind: p[5], subject: p[6] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (p[3] === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'twowriters' }; }, act: setter(['case']), steps: steps,
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'nhiều nơi giữ và sửa dữ liệu: hai màn hình lệch nhau', run: function () { var x = steps({ case: 'twowriters' })[3].metrics; return x.copies > 1 && x.writers > 1 && x.agree === M(m, 'agree.no'); } },
        { name: 'một nguồn sự thật: một bản, một chỗ sửa, hai màn hình khớp', run: function () { var x = steps({ case: 'ssot' })[3].metrics; return x.copies === 1 && x.writers === 1 && x.agree === M(m, 'agree.yes'); } }] });
  })();
  /* ================= G3: thông báo "Đã đặt lịch" qua một lần xoay màn hình =================
     Theo UI events (ViewModel event phải thành cập nhật UI state; UI báo lại khi đã hiện thông báo; Channel và stream khác
     không bảo đảm giao khi ViewModel sống lâu hơn UI), State holders (ViewModel sống qua tái tạo Activity), kotlinx.coroutines
     1.11.0 API: StateFlow phát lại giá trị mới nhất cho subscriber mới; MutableSharedFlow() không replay, emit trả về ngay khi
     không có subscriber (giá trị bị bỏ). Bốn cột của hình "Làn thời gian" lấy từ ADE.archEvents. */
  (function () {
    var m = 'events', CASES = ['sticky', 'shared', 'state'], KS = ['s1', 's2', 's3', 's4'];
    // mỗi ô: [mã chuỗi, kiểu ô] — kiểu: '' bình thường, 'hl' đang xảy ra, 'bad' lỗi, 'dim' không còn/không có
    // hàng: a1 = Activity lần 1, a2 = Activity lần 2 (sau xoay), vm = ViewModel, user = người dùng thấy
    var LANES = ['a1', 'vm', 'a2', 'user'];
    var G = {
      sticky: [
        { a1: ['tap', 'hl'], vm: ['setMsg', 'hl'], a2: ['none', 'dim'], user: ['toast1', ''] },
        { a1: ['destroyed', 'dim'], vm: ['keepMsg', 'bad'], a2: ['created', 'hl'], user: ['nothing', 'dim'] },
        { a1: ['destroyed', 'dim'], vm: ['replay', 'bad'], a2: ['collect', 'hl'], user: ['toast2', 'bad'] },
        { a1: ['destroyed', 'dim'], vm: ['keepMsg', 'bad'], a2: ['rotateAgain', 'hl'], user: ['toast3', 'bad'] }],
      shared: [
        { a1: ['tap', 'hl'], vm: ['request', 'hl'], a2: ['none', 'dim'], user: ['waiting', ''] },
        { a1: ['destroyed', 'dim'], vm: ['request', ''], a2: ['notYet', 'dim'], user: ['nothing', 'dim'] },
        { a1: ['destroyed', 'dim'], vm: ['emitNoSub', 'bad'], a2: ['notYet', 'dim'], user: ['nothing', 'dim'] },
        { a1: ['destroyed', 'dim'], vm: ['emptyFlow', 'bad'], a2: ['collectNothing', 'hl'], user: ['bookAgain', 'bad'] }],
      state: [
        { a1: ['tap', 'hl'], vm: ['setMsg', 'hl'], a2: ['none', 'dim'], user: ['toast1', ''] },
        { a1: ['shownCall', 'hl'], vm: ['cleared', 'hl'], a2: ['none', 'dim'], user: ['toast1', 'dim'] },
        { a1: ['destroyed', 'dim'], vm: ['noMsg', ''], a2: ['collectClean', 'hl'], user: ['nothing', ''] },
        { a1: ['destroyed', 'dim'], vm: ['pendingMsg', 'hl'], a2: ['collectPending', 'hl'], user: ['toastOnce', ''] }]
    };
    // số đo theo bước: {shown, lost, truth}
    var MET = {
      sticky: [{ shown: 1, lost: 'no', truth: 'flag' }, { shown: 1, lost: 'no', truth: 'flag' }, { shown: 2, lost: 'no', truth: 'flag' }, { shown: 3, lost: 'no', truth: 'flag' }],
      shared: [{ shown: 0, lost: 'na', truth: 'stream' }, { shown: 0, lost: 'na', truth: 'stream' }, { shown: 0, lost: 'yes', truth: 'stream' }, { shown: 0, lost: 'yes', truth: 'stream' }],
      state: [{ shown: 1, lost: 'no', truth: 'state' }, { shown: 1, lost: 'no', truth: 'state' }, { shown: 1, lost: 'no', truth: 'state' }, { shown: 1, lost: 'no', truth: 'state' }]
    };
    var STEP = {   // [node sáng, trạng thái node, loại bước, dòng mã, loại log, chủ thể, tín hiệu]
      sticky: [[['act', 'vm', 'flow', 'toast'], { act: 'done', vm: 'done', flow: 'done', toast: 'done' }, 'scenario', [2, 3, 6], 'write', 'vm', [{ edge: 'e1', tok: 'signal' }, { edge: 'e2', tok: 'state' }]],
        [['act', 'vm'], { act: 'skipped', vm: 'done', flow: 'done', toast: 'skipped' }, 'mechanism', [1, 2], 'observe', 'act', []],
        [['flow', 'act', 'toast'], { act: 'done', vm: 'done', flow: 'surprise', toast: 'surprise' }, 'pitfall', [5, 6], 'observe', 'act', [{ edge: 'e2', tok: 'state' }, { edge: 'e3', tok: 'signal' }]],
        [['flow', 'toast'], { act: 'done', vm: 'done', flow: 'surprise', toast: 'surprise' }, 'pitfall', [5, 6], 'observe', 'toast', [{ edge: 'e3', tok: 'signal' }]]],
      shared: [[['act', 'vm'], { act: 'done', vm: 'done', flow: 'done', toast: 'skipped' }, 'scenario', [2, 3], 'write', 'vm', [{ edge: 'e1', tok: 'signal' }]],
        [['act'], { act: 'skipped', vm: 'done', flow: 'done', toast: 'skipped' }, 'mechanism', [1], 'observe', 'act', []],
        [['vm', 'flow'], { act: 'skipped', vm: 'done', flow: 'surprise', toast: 'skipped' }, 'pitfall', [3, 4], 'skip', 'flow', []],
        [['act', 'flow', 'toast'], { act: 'done', vm: 'done', flow: 'surprise', toast: 'surprise' }, 'pitfall', [7], 'observe', 'toast', [{ edge: 'e2', tok: 'state' }]]],
      state: [[['act', 'vm', 'flow', 'toast'], { act: 'done', vm: 'done', flow: 'done', toast: 'done' }, 'scenario', [3, 5, 7], 'write', 'vm', [{ edge: 'e1', tok: 'signal' }, { edge: 'e2', tok: 'state' }]],
        [['toast', 'act', 'vm'], { act: 'done', vm: 'done', flow: 'done', toast: 'done' }, 'mechanism', [4, 8], 'write', 'act', [{ edge: 'e1', tok: 'signal' }]],
        [['flow', 'act'], { act: 'done', vm: 'done', flow: 'done', toast: 'done' }, 'mechanism', [1, 3], 'observe', 'act', [{ edge: 'e2', tok: 'state' }]],
        [['flow', 'act', 'toast'], { act: 'done', vm: 'done', flow: 'done', toast: 'done' }, 'mechanism', [7, 8], 'complete', 'toast', [{ edge: 'e2', tok: 'state' }, { edge: 'e3', tok: 'signal' }]]]
    };
    ADE.archEvents = { LANES: LANES, at: function (c, i) { return G[c][i]; } };
    function steps(s) {
      return STEP[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var x = MET[s.case][i];
        var o = S(m, s.case + '.' + KS[i], { type: p[2], activeNodes: p[0], nodeStates: ns,
          metrics: { shown: x.shown, lost: M(m, 'lost.' + x.lost), truth: M(m, 'truth.' + x.truth) },
          codeHighlight: { snippet: 'g3.' + s.case, lines: p[3] }, movingSignals: p[6], logEvents: [{ t: i, kind: p[4], subject: p[5] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (p[2] === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'sticky' }; }, act: setter(['case']), steps: steps,
      simpExtra: [M(m, 'simp.2')],
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'cờ trong StateFlow không xóa: thông báo hiện lại sau mỗi lần xoay', run: function () { var a = steps({ case: 'sticky' }); return a[3].metrics.shown > a[0].metrics.shown; } },
        { name: 'SharedFlow không replay, phát lúc không có subscriber: thông báo mất', run: function () { var x = steps({ case: 'shared' })[3].metrics; return x.shown === 0 && x.lost === M(m, 'lost.yes'); } },
        { name: 'thông báo là UI state, UI báo đã hiện: đúng một lần, không mất', run: function () { return steps({ case: 'state' }).every(function (s) { return s.metrics.shown === 1 && s.metrics.lost === M(m, 'lost.no'); }); } }] });
  })();
  /* ================= G4: data layer offline-first: database là nguồn sự thật =================
     Theo Build an offline-first app (đọc chỉ từ nguồn cục bộ, là nguồn sự thật chuẩn; ghi cập nhật vào nguồn cục bộ trước để nó
     báo cho người đọc; đọc qua Flow; ghi qua suspend; ba chiến lược ghi: chỉ online, hàng đợi, ghi lười với WorkManager),
     Data layer (mỗi repository một SSOT). Hàng của hình "Làn thời gian" lấy từ ADE.archOffline. */
  (function () {
    var m = 'offline', CASES = ['mixed', 'ssot', 'lazy'], KS = ['s1', 's2', 's3', 's4'];
    var LANES = ['net', 'db', 'repo', 'ui'];
    var G = {
      mixed: [
        { net: ['idle', 'dim'], db: ['oldList', ''], repo: ['readDb', 'hl'], ui: ['showOld', ''] },
        { net: ['returnsNew', 'hl'], db: ['stillOld', 'bad'], repo: ['passThrough', 'bad'], ui: ['showNew', 'hl'] },
        { net: ['idle', 'dim'], db: ['stillOld', 'bad'], repo: ['readDb', ''], ui: ['showOldAgain', 'bad'] },
        { net: ['offline', 'dim'], db: ['stillOld', 'bad'], repo: ['readDb', ''], ui: ['showOldOffline', 'bad'] }],
      ssot: [
        { net: ['idle', 'dim'], db: ['oldList', ''], repo: ['readDb', 'hl'], ui: ['showOld', ''] },
        { net: ['returnsNew', 'hl'], db: ['written', 'hl'], repo: ['writeDb', 'hl'], ui: ['showOld', 'dim'] },
        { net: ['idle', 'dim'], db: ['emits', 'hl'], repo: ['flowEmits', ''], ui: ['showNew', 'hl'] },
        { net: ['offline', 'dim'], db: ['keepNew', ''], repo: ['refreshFail', 'hl'], ui: ['showNewOffline', 'hl'] }],
      lazy: [
        { net: ['offline', 'dim'], db: ['markPending', 'hl'], repo: ['writeLocalFirst', 'hl'], ui: ['tapCancel', ''] },
        { net: ['offline', 'dim'], db: ['emitsPending', ''], repo: ['flowEmits', ''], ui: ['showPending', 'hl'] },
        { net: ['offline', 'dim'], db: ['pending', ''], repo: ['queued', 'hl'], ui: ['showPending', ''] },
        { net: ['receivesCancel', 'hl'], db: ['clearPending', 'hl'], repo: ['workerRuns', 'hl'], ui: ['showSynced', 'hl'] }]
    };
    var MET = {   // {src, ui, db}: UI đọc từ đâu, UI có bản mới nhất không, DB có bản mới nhất không
      mixed: [{ src: 'db', ui: 'no', db: 'no' }, { src: 'net', ui: 'yes', db: 'no' }, { src: 'db', ui: 'no', db: 'no' }, { src: 'db', ui: 'no', db: 'no' }],
      ssot: [{ src: 'db', ui: 'no', db: 'no' }, { src: 'db', ui: 'no', db: 'yes' }, { src: 'db', ui: 'yes', db: 'yes' }, { src: 'db', ui: 'yes', db: 'yes' }],
      lazy: [{ src: 'db', ui: 'no', db: 'yes' }, { src: 'db', ui: 'yes', db: 'yes' }, { src: 'db', ui: 'yes', db: 'yes' }, { src: 'db', ui: 'yes', db: 'yes' }]
    };
    var STEP = {   // [node sáng, trạng thái node, loại bước, dòng mã, loại log, chủ thể, tín hiệu]
      mixed: [[['ui', 'repo', 'db'], { ui: 'done', repo: 'done', db: 'done', net: 'skipped' }, 'scenario', [1, 2], 'observe', 'ui', [{ edge: 'e2', tok: 'state', reverse: true }]],
        [['repo', 'net', 'ui'], { ui: 'done', repo: 'surprise', db: 'surprise', net: 'done' }, 'pitfall', [3, 6], 'run', 'repo', [{ edge: 'e3', tok: 'state', reverse: true }, { edge: 'e1', tok: 'state', reverse: true }]],
        [['ui', 'db'], { ui: 'surprise', repo: 'done', db: 'surprise', net: 'skipped' }, 'pitfall', [2, 7], 'observe', 'ui', [{ edge: 'e2', tok: 'state', reverse: true }]],
        [['ui', 'db'], { ui: 'surprise', repo: 'done', db: 'surprise', net: 'broken' }, 'pitfall', [2], 'observe', 'ui', [{ edge: 'e2', tok: 'state', reverse: true }]]],
      ssot: [[['ui', 'repo', 'db'], { ui: 'done', repo: 'done', db: 'done', net: 'skipped' }, 'scenario', [2, 8], 'observe', 'ui', [{ edge: 'e2', tok: 'state', reverse: true }]],
        [['repo', 'net', 'db'], { ui: 'done', repo: 'done', db: 'done', net: 'done' }, 'mechanism', [3, 4, 5], 'write', 'repo', [{ edge: 'e3', tok: 'state', reverse: true }, { edge: 'e2', tok: 'signal' }]],
        [['db', 'repo', 'ui'], { ui: 'done', repo: 'done', db: 'done', net: 'done' }, 'mechanism', [5, 8], 'observe', 'db', [{ edge: 'e2', tok: 'state', reverse: true }, { edge: 'e1', tok: 'state', reverse: true }]],
        [['repo', 'net', 'ui'], { ui: 'done', repo: 'done', db: 'done', net: 'broken' }, 'mechanism', [2, 4], 'exception', 'net', [{ edge: 'e2', tok: 'state', reverse: true }]]],
      lazy: [[['ui', 'repo', 'db'], { ui: 'done', repo: 'done', db: 'done', net: 'broken' }, 'scenario', [1, 2], 'write', 'ui', [{ edge: 'e1', tok: 'signal' }, { edge: 'e2', tok: 'signal' }]],
        [['db', 'ui'], { ui: 'done', repo: 'done', db: 'done', net: 'broken' }, 'mechanism', [2], 'observe', 'ui', [{ edge: 'e2', tok: 'state', reverse: true }, { edge: 'e1', tok: 'state', reverse: true }]],
        [['repo'], { ui: 'done', repo: 'done', db: 'done', net: 'broken' }, 'mechanism', [3, 4, 5], 'skip', 'repo', []],
        [['repo', 'net', 'db', 'ui'], { ui: 'done', repo: 'done', db: 'done', net: 'done' }, 'mechanism', [7], 'complete', 'net', [{ edge: 'e3', tok: 'signal' }, { edge: 'e2', tok: 'signal' }]]]
    };
    ADE.archOffline = { LANES: LANES, at: function (c, i) { return G[c][i]; } };
    function steps(s) {
      return STEP[s.case].map(function (p, i) {
        var ns = {}; Object.keys(p[1]).forEach(function (n) { ns[n] = K + 'st.' + p[1][n]; });
        var x = MET[s.case][i];
        var o = S(m, s.case + '.' + KS[i], { type: p[2], activeNodes: p[0], nodeStates: ns,
          metrics: { src: M(m, 'src.' + x.src), ui: M(m, 'fresh.' + x.ui), db: M(m, 'fresh.' + x.db) },
          codeHighlight: { snippet: 'g4.' + s.case, lines: p[3] }, movingSignals: p[6], logEvents: [{ t: i, kind: p[4], subject: p[5] }] });
        o.callouts = [{ kind: i === 0 ? 'try' : (p[2] === 'pitfall' ? 'pitfall' : 'source'), textKey: i === 0 ? M(m, 'co.try') : M(m, 'co.' + s.case + '.' + KS[i]) }];
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'case', CASES)], init: function () { return { case: 'mixed' }; }, act: setter(['case']), steps: steps,
      selfChecks: [
        { name: 'mỗi tình huống có 4 bước', run: function () { return CASES.every(function (k) { return steps({ case: k }).length === 4; }); } },
        { name: 'trả thẳng kết quả mạng cho UI: DB vẫn cũ, mở lại màn thấy bản cũ', run: function () { var x = steps({ case: 'mixed' }); return x[1].metrics.ui === M(m, 'fresh.yes') && x[2].metrics.ui === M(m, 'fresh.no') && x[2].metrics.db === M(m, 'fresh.no'); } },
        { name: 'DB là nguồn sự thật: UI chỉ đọc DB và có bản mới sau khi DB được ghi', run: function () { var x = steps({ case: 'ssot' }); return x.every(function (s) { return s.metrics.src === M(m, 'src.db'); }) && x[2].metrics.ui === M(m, 'fresh.yes'); } },
        { name: 'ghi lười: UI thấy thay đổi ngay cả khi mất mạng', run: function () { return ADE.archOffline.at('lazy', 1).net[0] === 'offline' && steps({ case: 'lazy' })[1].metrics.ui === M(m, 'fresh.yes'); } }] });
  })();
})();
