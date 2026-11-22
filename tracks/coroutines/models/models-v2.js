/* Model cho các chương v2 (Phần 1, theo Kotlin Coroutines: Deep Dive). Thuần, không DOM, không câu chữ (chỉ message key).
   Mọi mô hình là MÔ HÌNH GIẢNG DẠY (simplified); nguồn và giới hạn ở docs/research/coroutines.md. */
(function () {
  'use strict';
  var C = ADE.coro, K = C.K, step = C.step;
  var M = function (m, s) { return K + 'm.' + m + '.' + s; };

  /* ================= U2: sequence builder: luồng thực thi nhảy giữa main và khối sequence =================
     Một luồng duy nhất. Mỗi lần main gọi next(), luồng chạy vào khối sequence tới yield kế tiếp rồi quay lại main.
     Trạng thái mỗi hàng sau từng sự kiện nằm ở params: m (main), g (khối sequence) ∈ run | call | wait | idle | done.
     So sánh: chế độ "List" (buildList) chạy HẾT khối ngay từ đầu, không nhảy qua lại. */
  (function () {
    var m = 'seq';
    function steps(s) {
      var out = [], t = 0, last = '?', printed = 0;
      var push = function (id, o) {
        t += 10;
        var ps = o.ps || {};
        var ns = { main: M(m, 'st.' + ps.m), gen: M(m, 'st.' + ps.g), th: M(m, 'st.th' + (ps.m === 'run' ? 'Main' : ps.g === 'run' ? 'Gen' : 'Free')) };
        if (o.val != null) last = o.val;
        if (o.out) printed += o.out;
        var ev = (o.ev || []).map(function (e) { e.t = t; e.scope = M(m, 'scope'); e.params = e.params || {}; e.params.m = ps.m; e.params.g = ps.g; return e; });
        out.push(step({ id: id, type: o.type || 'mechanism', titleKey: M(m, 's.' + id + '.title'), explainKey: M(m, 's.' + id + '.explain'), params: o.params || {},
          activeNodes: [ps.m === 'run' ? 'main' : 'gen'], nodeStates: ns,
          metrics: { time: t, val: last, out: printed }, codeHighlight: { snippet: s.eager ? 'seqList' : 'seq', lines: o.lines },
          callouts: o.co ? [{ kind: o.co[0], textKey: M(m, 'co.' + o.co[1]) }] : [], logEvents: ev }));
      };
      var E = function (kind, subject, key, params) { var p = {}; for (var k in (params || {})) p[k] = params[k]; return { kind: kind, subject: subject, detailKey: M(m, 'ev.' + key), params: p }; };
      if (s.eager) {
        push('eBuild', { ps: { m: 'call', g: 'run' }, lines: [2, 3, 4, 5, 6, 7, 8, 9], out: 4, type: 'experiment', co: ['pitfall', 'eager'],
          ev: [E('run', 'gen', 'eBuild')] });
        push('eDone', { ps: { m: 'run', g: 'done' }, lines: [10], ev: [E('complete', 'gen', 'eDone')] });
        push('eStart', { ps: { m: 'run', g: 'done' }, lines: [11, 12], out: 1, ev: [E('run', 'main', 'start')] });
        push('eFirst', { ps: { m: 'run', g: 'done' }, lines: [13], val: 1, out: 1, params: { v: 1 }, ev: [E('collect', 'main', 'eRead', { v: 1 })] });
        push('eSecond', { ps: { m: 'run', g: 'done' }, lines: [14], val: 2, out: 1, params: { v: 2 }, ev: [E('collect', 'main', 'eRead', { v: 2 })] });
        return out;
      }
      push('start', { ps: { m: 'run', g: 'idle' }, lines: [12, 13], out: 1, co: ['try', 'start'], ev: [E('run', 'main', 'start')] });
      var words = ['first', 'second', 'third'];
      var n = s.all ? 3 : 2;
      for (var i = 0; i < n; i++) {
        var v = i + 1, P = { v: v, w: words[i] };
        push('next' + v, { ps: { m: 'call', g: 'run' }, lines: [14 + 2 * i, 2 + 2 * i], out: 1, params: P, co: i === 0 ? ['mechanism', 'enter'] : i === 1 ? ['mechanism', 'resume'] : null,
          ev: [E(i === 0 ? 'launch' : 'resume', 'gen', i === 0 ? 'enter' : 'resume', P)] });
        push('yield' + v, { ps: { m: 'run', g: 'wait' }, lines: [3 + 2 * i, 14 + 2 * i], val: v, params: P, co: i === 0 ? ['mechanism', 'yield'] : null,
          ev: [E('suspend', 'gen', 'yield', P), E('collect', 'main', 'got', P)] });
        push('print' + v, { ps: { m: 'run', g: 'wait' }, lines: [15 + 2 * i], out: 1, params: P, ev: [E('run', 'main', 'print', P)] });
      }
      if (s.all) {
        push('end', { ps: { m: 'call', g: 'run' }, lines: [20, 8, 9], out: 1, co: ['mechanism', 'end'], ev: [E('resume', 'gen', 'end')] });
        push('finish', { ps: { m: 'run', g: 'done' }, lines: [20, 21], out: 1, ev: [E('complete', 'gen', 'finish'), E('complete', 'main', 'mainDone')] });
      } else {
        push('pause', { ps: { m: 'done', g: 'wait' }, lines: [21], type: 'pitfall', co: ['mechanism', 'pause'], ev: [E('complete', 'main', 'mainDone')] });
      }
      return out;
    }
    ADE.registerModel('coroutines.seq', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'seq',
      simplificationKeys: [M(m, 'simp.1'), M(m, 'simp.2')], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        { id: 'all', type: 'toggle', labelKey: M(m, 'ctl.all'), get: function (s) { return s.all; }, action: 'all' },
        { id: 'eager', type: 'toggle', labelKey: M(m, 'ctl.eager'), get: function (s) { return s.eager; }, action: 'eager' }
      ],
      init: function () { return { all: false, eager: false }; },
      act: function (s, a, v) { var n = { all: s.all, eager: s.eager }; n[a] = !!v; return n; },
      steps: steps,
      selfChecks: [
        { name: 'lazy 2 lần next: 8 bước, khối sequence dừng ở yield(2); đi hết: có Done; List: khối chạy hết trước Starting', run: function () {
          var d = ADE.models['coroutines.seq'], a = d.steps({ all: false, eager: false }), b = d.steps({ all: true, eager: false }), c = d.steps({ all: false, eager: true });
          var lastG = function (st) { return st[st.length - 1].logEvents[0].params.g; };
          return a.length === 8 && lastG(a) === 'wait' && b[b.length - 1].id === 'finish' && c[0].id === 'eBuild' && c[2].id === 'eStart';
        } }
      ]
    });
  })();

  /* ================= U3: suspendCoroutine, Continuation và các cách resume =================
     Năm chế độ (control 'how'): never (không ai resume → treo), now (resume ngay trong lambda → không suspend thật),
     thread (luồng mới ngủ 1000 ms rồi resume → phần sau chạy TRÊN luồng đó), sched (scheduler hẹn giờ = delay tự viết),
     exc (resumeWithException → exception ném ra tại điểm suspension). Thời gian là minh hoạ (1000 ms trong mã vẽ thành 100).
     params của sự kiện: co ∈ run|wait|done; on ∈ th0|th1|'' (luồng đang chạy coroutine); t1 ∈ run|block|timer|''. */
  (function () {
    var m = 'cont';
    var SN = { never: 'contNever', now: 'contNow', thread: 'contThread', sched: 'contSched', exc: 'contExc' };
    function steps(s) {
      var out = [], how = s.how;
      var push = function (id, from, to, o) {
        var ps = o.ps;
        var ev = [{ t: from, kind: o.kind || 'run', subject: o.subject || 'co', scope: M(m, 'scope.' + (ps.on || 'none')), detailKey: M(m, 'ev.' + (o.ev || id)),
          params: { co: ps.co, on: ps.on || '', t1: ps.t1 || '', to: to } }];
        out.push(step({ id: id, type: o.type || 'mechanism', titleKey: M(m, 's.' + id + '.title'), explainKey: M(m, 's.' + id + '.explain'),
          activeNodes: [o.subject === 'th1' ? 'th1' : 'co'],
          nodeStates: { co: M(m, 'st.' + ps.co), th0: M(m, 'st.' + (ps.on === 'th0' ? 'busy' : 'free')), th1: M(m, 'st.' + (ps.on === 'th1' ? 'busy' : ps.t1 === 'block' ? 'blocked' : ps.t1 === 'timer' ? 'timer' : 'free')) },
          metrics: { time: to, out: M(m, 'o.' + (o.out || 'none')), on: M(m, 'thr.' + (ps.on || 'none')) }, codeHighlight: { snippet: SN[how], lines: o.lines },
          callouts: o.co ? [{ kind: o.co[0], textKey: M(m, 'co.' + o.co[1]) }] : [], logEvents: ev }));
      };
      if (how === 'exc') {
        push('excLambda', 0, 10, { ps: { co: 'run', on: 'th0' }, lines: [5, 6] });
        push('excThrow', 10, 20, { ps: { co: 'run', on: 'th0' }, lines: [6, 8], kind: 'exception', co: ['mechanism', 'exc'] });
        push('excCatch', 20, 30, { ps: { co: 'run', on: 'th0' }, lines: [9], out: 'caught' });
        push('done', 30, 40, { ps: { co: 'done', on: '' }, lines: [11], kind: 'complete' });
        return out;
      }
      if (how === 'sched') {
        push('before', 0, 10, { ps: { co: 'run', on: 'th0' }, lines: [11], out: 'before' });
        push('schedule', 10, 20, { ps: { co: 'run', on: 'th0', t1: 'timer' }, lines: [12, 6, 7], co: ['mechanism', 'schedule'] });
        push('suspended', 20, 120, { ps: { co: 'wait', on: '', t1: 'timer' }, lines: [12], kind: 'suspend', co: ['mechanism', 'free'] });
        push('fire', 120, 130, { ps: { co: 'run', on: 'th1' }, lines: [7, 13], kind: 'resume', out: 'after', co: ['pitfall', 'onSched'] });
        push('done', 130, 140, { ps: { co: 'done', on: '' }, lines: [14], kind: 'complete' });
        return out;
      }
      push('before', 0, 10, { ps: { co: 'run', on: 'th0' }, lines: [2], out: 'before' });
      if (how === 'never') {
        push('lambda', 10, 20, { ps: { co: 'run', on: 'th0' }, lines: [3, 4], out: 'beforeToo', co: ['mechanism', 'lambda'] });
        push('suspended', 20, 120, { ps: { co: 'wait', on: '' }, lines: [3], kind: 'suspend', co: ['mechanism', 'free'] });
        push('hang', 120, 130, { ps: { co: 'wait', on: '' }, lines: [6], type: 'pitfall', kind: 'skip', co: ['pitfall', 'hang'] });
        return out;
      }
      if (how === 'now') {
        push('lambdaNow', 10, 20, { ps: { co: 'run', on: 'th0' }, lines: [3, 4], kind: 'resume', co: ['mechanism', 'noSuspend'] });
        push('after', 20, 30, { ps: { co: 'run', on: 'th0' }, lines: [6], out: 'after' });
        push('done', 30, 40, { ps: { co: 'done', on: '' }, lines: [7], kind: 'complete' });
        return out;
      }
      // thread
      push('lambdaThread', 10, 20, { ps: { co: 'run', on: 'th0', t1: 'run' }, lines: [3, 4], subject: 'th1', kind: 'launch' });
      push('suspended', 20, 30, { ps: { co: 'wait', on: '', t1: 'run' }, lines: [3, 5], kind: 'suspend', out: 'suspended', co: ['mechanism', 'free'] });
      push('sleep', 30, 120, { ps: { co: 'wait', on: '', t1: 'block' }, lines: [6], kind: 'block', subject: 'th1', co: ['pitfall', 'sleepCost'] });
      push('resumeThread', 120, 130, { ps: { co: 'run', on: 'th1' }, lines: [7, 11], kind: 'resume', out: 'after', co: ['pitfall', 'onThread'] });
      push('resumed', 130, 140, { ps: { co: 'done', on: '', t1: 'run' }, lines: [8], subject: 'th1', out: 'resumed', co: ['mechanism', 'order'] });
      return out;
    }
    ADE.registerModel('coroutines.cont', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'contThread',
      simplificationKeys: [M(m, 'simp.1'), M(m, 'simp.2'), K + 'simp.time'], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        { id: 'how', type: 'select', labelKey: M(m, 'ctl.how'), get: function (s) { return s.how; }, action: 'how',
          options: ['thread', 'never', 'now', 'sched', 'exc'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.how.' + v) }; }) }
      ],
      init: function () { return { how: 'thread' }; },
      act: function (s, a, v) { return { how: ['never', 'now', 'thread', 'sched', 'exc'].indexOf(v) >= 0 ? v : 'thread' }; },
      steps: steps,
      selfChecks: [
        { name: 'thread: "After" chạy trên luồng phụ trước "Resumed"; never: không có "After"; now: không có bước suspend', run: function () {
          var d = ADE.models['coroutines.cont'];
          var th = d.steps({ how: 'thread' }), nv = d.steps({ how: 'never' }), nw = d.steps({ how: 'now' });
          var ia = -1, ir = -1; th.forEach(function (x, i) { if (x.metrics.out === M(m, 'o.after')) ia = i; if (x.metrics.out === M(m, 'o.resumed')) ir = i; });
          return ia >= 0 && ir > ia && th[ia].metrics.on === M(m, 'thr.th1') &&
            !nv.some(function (x) { return x.metrics.out === M(m, 'o.after'); }) && !nw.some(function (x) { return x.logEvents[0].kind === 'suspend'; });
        } }
      ]
    });
  })();

  /* ================= U4: hàm suspend sau khi biên dịch là một state machine =================
     printUser(token) có hai điểm suspend (getUserId, getUserName) → ba trạng thái label 0, 1, 2.
     Trường của PrintUserContinuation hiện ở dải chỉ số: label, userId, result; cùng giá trị printUser trả về và trạng thái luồng.
     mode: 'suspend' (cả hai lời gọi suspend), 'now' (getUserId có kết quả ngay → không trả COROUTINE_SUSPENDED),
     'fail' (getUserName resume bằng exception → getOrThrow ném ra → completion nhận Result.failure). */
  (function () {
    var m = 'sm';
    var V = function (k) { return M(m, 'v.' + k); };
    function steps(s) {
      var out = [], f = { label: 0, userId: V('none'), result: V('none'), ret: V('none'), th: V('busy') };
      var push = function (id, o) {
        for (var k in o.f || {}) f[k] = o.f[k];
        var ns = { call: M(m, 'st.' + (o.call || 'waiting')), l0: M(m, 'st.' + (o.l0 || 'idle')), l1: M(m, 'st.' + (o.l1 || 'idle')), l2: M(m, 'st.' + (o.l2 || 'idle')), cont: M(m, 'st.label' + f.label) };
        out.push(step({ id: id, type: o.type || 'mechanism', titleKey: M(m, 's.' + id + '.title'), explainKey: M(m, 's.' + id + '.explain'),
          activeNodes: o.active, movingSignals: o.sig ? [{ edge: o.sig, tok: 'coroutine' }] : [], nodeStates: ns,
          metrics: { label: f.label, userId: f.userId, result: f.result, ret: f.ret, th: f.th }, codeHighlight: { snippet: 'smUser', lines: o.lines },
          callouts: o.co ? [{ kind: o.co[0], textKey: M(m, 'co.' + o.co[1]) }] : [],
          logEvents: [{ t: out.length + 1, kind: o.kind || 'run', subject: o.subject || 'printUser', scope: M(m, 'scope.' + (f.th === V('free') ? 'free' : 'busy')), detailKey: M(m, 'ev.' + id) }] }));
      };
      push('call', { active: ['call', 'cont'], sig: 'e1', lines: [1, 2, 3], kind: 'launch', call: 'waiting', co: ['mechanism', 'wrap'] });
      push('l0', { active: ['l0'], lines: [6, 7, 8, 9], l0: 'running', f: { label: 1 }, co: ['mechanism', 'labelFirst'] });
      if (s.mode === 'now') {
        push('l0now', { active: ['l0', 'l1'], sig: 'e2', lines: [9, 11], l0: 'done', l1: 'running', f: { result: V('okId'), ret: V('none') }, kind: 'resume', co: ['mechanism', 'fallThrough'] });
      } else {
        push('susp1', { active: ['l0', 'call'], lines: [10], l0: 'suspended', kind: 'suspend', subject: 'getUserId', f: { ret: V('susp'), th: V('free') }, co: ['mechanism', 'unwind'] });
        push('resume1', { active: ['cont', 'l1'], sig: 'e2', lines: [2, 4, 5, 13, 14], l0: 'done', l1: 'running', kind: 'resume', f: { result: V('okId'), ret: V('none'), th: V('busy') }, co: ['mechanism', 'reuse'] });
      }
      push('l1', { active: ['l1'], lines: [14, 15, 16, 17, 18], l0: 'done', l1: 'running', f: { label: 2, userId: V('id') }, co: ['mechanism', 'store'] });
      push('susp2', { active: ['l1', 'call'], lines: [19], l0: 'done', l1: 'suspended', kind: 'suspend', subject: 'getUserName', f: { ret: V('susp'), th: V('free') } });
      if (s.mode === 'fail') {
        push('resumeFail', { active: ['cont', 'l2'], sig: 'e3', lines: [2, 4, 5, 22, 23], l0: 'done', l1: 'done', l2: 'failed', kind: 'exception', f: { result: V('fail'), ret: V('none'), th: V('busy') }, co: ['pitfall', 'throwHere'] });
        push('completeFail', { active: ['call'], sig: 'e4', lines: [23], l0: 'done', l1: 'done', l2: 'failed', call: 'failed', kind: 'exception', subject: 'completion', f: { ret: V('thrown') }, co: ['mechanism', 'failUp'] });
        return out;
      }
      push('resume2', { active: ['cont', 'l2'], sig: 'e3', lines: [2, 4, 5, 22, 23, 24, 25], l0: 'done', l1: 'done', l2: 'running', kind: 'resume', f: { result: V('okName'), ret: V('none'), th: V('busy') } });
      push('ret', { active: ['call'], sig: 'e4', lines: [26], l0: 'done', l1: 'done', l2: 'done', call: 'resumed', kind: 'complete', subject: 'completion', f: { ret: V('unit') }, co: ['mechanism', 'completion'] });
      return out;
    }
    ADE.registerModel('coroutines.sm', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'smUser',
      simplificationKeys: [M(m, 'simp.1'), M(m, 'simp.2')], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        { id: 'mode', type: 'select', labelKey: M(m, 'ctl.mode'), get: function (s) { return s.mode; }, action: 'mode',
          options: ['suspend', 'now', 'fail'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.mode.' + v) }; }) }
      ],
      init: function () { return { mode: 'suspend' }; },
      act: function (s, a, v) { return { mode: ['suspend', 'now', 'fail'].indexOf(v) >= 0 ? v : 'suspend' }; },
      steps: steps,
      selfChecks: [
        { name: 'suspend: 2 lần trả COROUTINE_SUSPENDED, label 0→1→2, kết thúc Unit; now: chỉ 1 lần suspend; fail: completion nhận failure', run: function () {
          var d = ADE.models['coroutines.sm'];
          var cnt = function (st) { return st.filter(function (x) { return x.metrics.ret === M(m, 'v.susp'); }).length; };
          var a = d.steps({ mode: 'suspend' }), b = d.steps({ mode: 'now' }), c = d.steps({ mode: 'fail' });
          return cnt(a) === 2 && cnt(b) === 1 && a[a.length - 1].metrics.ret === M(m, 'v.unit') && a[a.length - 1].metrics.label === 2 &&
            c[c.length - 1].metrics.ret === M(m, 'v.thrown');
        } }
      ]
    });
  })();

  /* ================= A2: vòng đời của Job (New → Active → Completing → Completed; Cancelling → Cancelled) =================
     Một coroutine cha có một con. lazy: bắt đầu ở New, phải start(). cancelAt: 'none' | 'active' (hủy khi đang chạy thân)
     | 'completing' (hủy khi thân đã xong, đang chờ con). Dải chỉ số: isActive, isCompleted, isCancelled, số con đang chạy.
     Bảng cờ theo tài liệu Job của kotlinx.coroutines. */
  (function () {
    var m = 'jobstate';
    var FLAGS = { new: [0, 0, 0], active: [1, 0, 0], completing: [1, 0, 0], cancelling: [0, 0, 1], cancelled: [0, 1, 1], completed: [0, 1, 0] };
    var STATES = ['new', 'active', 'completing', 'completed', 'cancelling', 'cancelled'];
    function steps(s) {
      var out = [], seen = {}, kids = 0;
      var B = function (x) { return M(m, 'v.' + (x ? 'yes' : 'no')); };
      var push = function (id, state, o) {
        o = o || {};
        if (o.kids != null) kids = o.kids;
        seen[state] = 1;
        var ns = {};
        STATES.forEach(function (st) {
          ns[st] = M(m, 'st.' + (st === state ? (st === 'completed' ? 'completed' : st === 'cancelled' ? 'cancelled' : st === 'cancelling' ? 'cancelling' : 'running') : seen[st] ? 'done' : 'idle'));
        });
        var f = FLAGS[state];
        out.push(step({ id: id, type: o.type || 'mechanism', titleKey: M(m, 's.' + id + '.title'), explainKey: M(m, 's.' + id + '.explain'),
          activeNodes: [state], movingSignals: o.edge ? [{ edge: o.edge, tok: 'job' }] : [], nodeStates: ns,
          metrics: { isActive: B(f[0]), isCompleted: B(f[1]), isCancelled: B(f[2]), kids: kids },
          codeHighlight: { snippet: 'jobState', lines: o.lines || [] },
          callouts: o.co ? [{ kind: o.co[0], textKey: M(m, 'co.' + o.co[1]) }] : [],
          logEvents: [{ t: (out.length + 1) * 10, kind: o.kind || 'run', subject: o.subject || 'parent', scope: M(m, 'state.' + state), detailKey: M(m, 'ev.' + id) }] }));
      };
      if (s.lazy) {
        push('createdLazy', 'new', { lines: [1], kind: 'launch', co: ['mechanism', 'lazy'] });
        push('start', 'active', { lines: [8], edge: 'e1', kind: 'resume' });
      } else {
        push('created', 'active', { lines: [1], kind: 'launch' });
      }
      push('child', 'active', { lines: [2, 3], kids: 1, kind: 'launch', subject: 'child' });
      if (s.cancelAt === 'active') {
        push('cancelActive', 'cancelling', { lines: [9], edge: 'e4', kind: 'cancel', type: 'experiment', co: ['mechanism', 'cancelling'] });
        push('cleanup', 'cancelling', { lines: [4], kids: 0, kind: 'cancel', subject: 'child', co: ['android', 'finally'] });
        push('cancelled', 'cancelled', { lines: [9, 10], edge: 'e6', kind: 'complete' });
        return out;
      }
      push('bodyDone', 'completing', { lines: [6], edge: 'e2', kind: 'suspend', co: ['mechanism', 'completing'] });
      if (s.cancelAt === 'completing') {
        push('cancelCompleting', 'cancelling', { lines: [9], edge: 'e5', kind: 'cancel', type: 'experiment' });
        push('cleanup', 'cancelling', { lines: [4], kids: 0, kind: 'cancel', subject: 'child', co: ['android', 'finally'] });
        push('cancelled', 'cancelled', { lines: [9, 10], edge: 'e6', kind: 'complete' });
        return out;
      }
      push('childDone', 'completing', { lines: [3], kids: 0, kind: 'complete', subject: 'child' });
      push('completed', 'completed', { lines: [10], edge: 'e3', kind: 'complete', co: ['mechanism', 'join'] });
      return out;
    }
    ADE.registerModel('coroutines.jobstate', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'jobState',
      simplificationKeys: [M(m, 'simp.1')], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        { id: 'lazy', type: 'toggle', labelKey: M(m, 'ctl.lazy'), get: function (s) { return s.lazy; }, action: 'lazy' },
        { id: 'cancelAt', type: 'select', labelKey: M(m, 'ctl.cancelAt'), get: function (s) { return s.cancelAt; }, action: 'cancelAt',
          options: ['none', 'active', 'completing'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.cancelAt.' + v) }; }) }
      ],
      init: function () { return { lazy: false, cancelAt: 'none' }; },
      act: function (s, a, v) { var n = { lazy: s.lazy, cancelAt: s.cancelAt }; if (a === 'lazy') n.lazy = !!v; else n.cancelAt = ['none', 'active', 'completing'].indexOf(v) >= 0 ? v : 'none'; return n; },
      steps: steps,
      selfChecks: [
        { name: 'kết thúc Completed (F,T,F) khi không hủy; Cancelled (F,T,T) khi hủy; lazy bắt đầu ở New (F,F,F)', run: function () {
          var d = ADE.models['coroutines.jobstate'], Y = M(m, 'v.yes'), N = M(m, 'v.no');
          var last = function (st) { return st[st.length - 1].metrics; };
          var a = last(d.steps({ lazy: false, cancelAt: 'none' })), b = last(d.steps({ lazy: false, cancelAt: 'active' })), c = d.steps({ lazy: true, cancelAt: 'completing' });
          return a.isActive === N && a.isCompleted === Y && a.isCancelled === N && b.isCompleted === Y && b.isCancelled === Y &&
            c[0].metrics.isActive === N && c[0].metrics.isCompleted === N && last(c).isCancelled === Y;
        } }
      ]
    });
  })();

  /* ================= FL: Flow dưới mui xe: collect → map → flowOf → emit → lambda của collect =================
     flowOf("A","B","C").map { it.lowercase() }.collect { println(it) }. Ba hàng: terminal (collect), map, builder (flowOf).
     Trạng thái mỗi hàng: run (đang chạy mã của nó) | call (đang chờ một lời gọi lồng trả về) | idle | done. twice: collect lần 2 chạy lại từ đầu (flow lạnh). */
  (function () {
    var m = 'flowcall';
    function steps(s) {
      var out = [], st = { t: 'idle', m: 'idle', b: 'idle' }, printed = 0, t = 0, round = 0;
      var push = function (id, ns, o) {
        o = o || {};
        for (var k in ns) st[k] = ns[k];
        t += 10;
        out.push(step({ id: id + round, type: o.type || 'mechanism', titleKey: M(m, 's.' + id + '.title'), explainKey: M(m, 's.' + id + '.explain'), params: o.p || {},
          activeNodes: [o.who || 't'], nodeStates: {}, metrics: { time: t, out: printed, depth: (st.t === 'call' ? 1 : 0) + (st.m === 'call' ? 1 : 0) + (st.b !== 'idle' && st.b !== 'done' ? 1 : 0) },
          codeHighlight: { snippet: 'flowCall', lines: o.lines || [] }, callouts: o.co ? [{ kind: o.co[0], textKey: M(m, 'co.' + o.co[1]) }] : [],
          logEvents: [{ t: t, kind: o.kind || 'run', subject: o.who || 't', scope: M(m, 'scope'), detailKey: M(m, 'ev.' + id), params: { v: (o.p || {}).v, T: st.t, Mm: st.m, Bb: st.b } }] }));
      };
      var once = function () {
        push('collect', { t: 'run', m: 'idle', b: 'idle' }, { who: 't', lines: [10, 11], kind: 'launch', co: round === 0 ? ['mechanism', 'collect'] : ['mechanism', 'again'] });
        push('mapStart', { t: 'call', m: 'run' }, { who: 'm', lines: [5, 6], co: round === 0 ? ['mechanism', 'mapIs'] : null });
        push('builderStart', { m: 'call', b: 'run' }, { who: 'b', lines: [1, 2], kind: 'resume' });
        ['A', 'B', 'C'].forEach(function (v, i) {
          push('emit', { b: 'call', m: 'run' }, { who: 'm', lines: [2, 6, 7], kind: 'emit', p: { v: v }, co: i === 0 && round === 0 ? ['mechanism', 'emitCalls'] : null });
          push('mapEmit', { m: 'call', t: 'run' }, { who: 't', lines: [7, 11], kind: 'emit', p: { v: v.toLowerCase() } });
          printed++;
          push('print', {}, { who: 't', lines: [11], kind: 'collect', p: { v: v.toLowerCase() } });
          push('back', { t: 'call', m: 'call', b: 'run' }, { who: 'b', lines: [2], kind: 'resume', p: { v: v }, co: i === 0 && round === 0 ? ['mechanism', 'sync'] : null });
        });
        push('builderEnd', { b: 'done', m: 'run' }, { who: 'b', lines: [3], kind: 'complete' });
        push('mapEnd', { m: 'done', t: 'run' }, { who: 'm', lines: [8], kind: 'complete' });
        push('collectEnd', { t: 'done' }, { who: 't', lines: [12], kind: 'complete' });
      };
      once();
      if (s.twice) { round = 1; st = { t: 'idle', m: 'idle', b: 'idle' }; once(); }
      return out;
    }
    ADE.registerModel('coroutines.flowcall', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'flowCall',
      simplificationKeys: [M(m, 'simp.1')], controlsHintKey: M(m, 'ctl.hint'),
      controls: [{ id: 'twice', type: 'toggle', labelKey: M(m, 'ctl.twice'), get: function (s) { return s.twice; }, action: 'twice' }],
      init: function () { return { twice: false }; },
      act: function (s, a, v) { return { twice: !!v }; },
      steps: steps,
      selfChecks: [
        { name: 'một lần collect: 3 lần in, builder chạy 1 lần; collect 2 lần: builder chạy lại (6 lần in)', run: function () {
          var d = ADE.models['coroutines.flowcall'], a = d.steps({ twice: false }), b = d.steps({ twice: true });
          var cnt = function (st, pre) { return st.filter(function (x) { return x.id.indexOf(pre) === 0; }).length; };
          return a[a.length - 1].metrics.out === 3 && cnt(a, 'builderStart') === 1 && b[b.length - 1].metrics.out === 6 && cnt(b, 'builderStart') === 2;
        } }
      ]
    });
  })();

  /* ================= FB: flow (lười) và channelFlow (tải trước) cho dữ liệu phân trang =================
     Ví dụ của Deep Dive: FakeUserApi 3 user/trang, takePage mất 1000 ms; first { kiểm 1000 ms; tìm User3 }.
     flow: trang kế chỉ tải khi cần → xong ở 6000 ms, 2 lần gọi mạng. channelFlow: producer chạy song song, tải tiếp
     trong lúc consumer kiểm → xong ở 5000 ms, 5 lần gọi mạng. params: p (prod: fetch|wait|idle|cancel), c (cons: check|wait|done). */
  (function () {
    var m = 'paging';
    function events(mode) {
      var ev = [], pages = 0, checked = 0;
      var E = function (t, key, p, c, o) { o = o || {}; if (o.page != null) pages = o.page + 1; if (o.u != null) checked = o.u + 1; ev.push({ t: t, key: key, p: p, c: c, page: o.page, u: o.u, pages: pages, checked: checked }); };
      if (mode === 'flow') {
        E(0, 'fetch', 'fetch', 'wait', { page: 0 });
        E(1000, 'check', 'wait', 'check', { u: 0 });
        E(2000, 'check', 'wait', 'check', { u: 1 });
        E(3000, 'check', 'wait', 'check', { u: 2 });
        E(4000, 'fetchLazy', 'fetch', 'wait', { page: 1 });
        E(5000, 'check', 'wait', 'check', { u: 3 });
        E(6000, 'found', 'cancel', 'done');
      } else {
        E(0, 'fetch', 'fetch', 'wait', { page: 0 });
        for (var i = 0; i < 4; i++) { E(1000 * (i + 1), 'check', 'fetch', 'check', { u: i }); E(1000 * (i + 1), 'prefetch', 'fetch', 'check', { page: i + 1 }); }
        E(5000, 'found', 'cancel', 'done');
      }
      return ev;
    }
    function steps(s) {
      return events(s.mode).map(function (e, i) {
        var co = null;
        if (e.key === 'fetchLazy') co = ['mechanism', 'lazy'];
        if (e.key === 'prefetch' && e.page === 1) co = ['mechanism', 'prefetch'];
        if (e.key === 'found') co = [s.mode === 'flow' ? 'mechanism' : 'pitfall', s.mode === 'flow' ? 'foundFlow' : 'foundCh'];
        return step({ id: e.key + i, type: e.key === 'found' ? 'experiment' : 'mechanism', titleKey: M(m, 's.' + e.key + '.title'), explainKey: M(m, 's.' + e.key + '.explain'),
          params: { page: e.page, u: e.u, t: e.t }, activeNodes: [e.key === 'check' ? 'cons' : 'prod'], nodeStates: {},
          metrics: { time: e.t, pages: e.pages, checked: e.checked }, codeHighlight: { snippet: s.mode === 'flow' ? 'pagingFlow' : 'pagingCh', lines: e.key === 'check' ? [9, 10] : e.key === 'found' ? [11] : [3, 4, 5] },
          callouts: co ? [{ kind: co[0], textKey: M(m, 'co.' + co[1]) }] : [],
          logEvents: [{ t: e.t, kind: e.key === 'check' ? 'collect' : e.key === 'found' ? 'complete' : 'emit', subject: e.key === 'check' || e.key === 'found' ? 'cons' : 'prod', scope: M(m, 'scope.' + s.mode), detailKey: M(m, 'ev.' + e.key), params: { page: e.page, u: e.u, p: e.p, c: e.c } }] });
      });
    }
    ADE.registerModel('coroutines.paging', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'pagingFlow',
      simplificationKeys: [M(m, 'simp.1'), K + 'simp.time'], controlsHintKey: M(m, 'ctl.hint'),
      controls: [{ id: 'mode', type: 'select', labelKey: M(m, 'ctl.mode'), get: function (s) { return s.mode; }, action: 'mode',
        options: ['flow', 'channelFlow'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.mode.' + v) }; }) }],
      init: function () { return { mode: 'flow' }; },
      act: function (s, a, v) { return { mode: v === 'channelFlow' ? 'channelFlow' : 'flow' }; },
      steps: steps,
      selfChecks: [
        { name: 'flow: xong 6000 ms, 2 trang; channelFlow: xong 5000 ms, 5 trang (khớp output của sách)', run: function () {
          var a = events('flow'), b = events('channelFlow'), la = a[a.length - 1], lb = b[b.length - 1];
          return la.t === 6000 && la.pages === 2 && lb.t === 5000 && lb.pages === 5;
        } }
      ]
    });
  })();

  /* ================= CH: Channel và sức chứa (theo chương "Channel" của Deep Dive) =================
     Producer: repeat(5) { send(index * 2); delay(100); println("Sent") } rồi đóng (produce). Consumer: delay(1000); với mỗi phần tử: println; delay(1000).
     mode: rendezvous (0) | buffered (3) | unlimited | conflated (1, thay phần tử cũ) | dropOldest (2, bỏ phần tử cũ nhất).
     Mô phỏng sự kiện rời rạc theo ms (thời gian của mã, minh hoạ); thứ tự xử lý trong cùng một mốc: producer trước, consumer sau. */
  (function () {
    var m = 'chan';
    var CAP = { rendezvous: 0, buffered: 3, unlimited: 1e9, conflated: 1, dropOldest: 2 };
    function simulate(mode) {
      var cap = CAP[mode], buf = [], ev = [], t = 0, closed = false, sent = 0, recv = 0, dropped = 0;
      var P = { i: 0, at: 0, st: 'ready', pending: null }, Cn = { at: 1000, st: 'delay' };
      var E = function (kind, who, key, v) { ev.push({ t: t, kind: kind, who: who, key: key, v: v, n: buf.length, p: P.st, c: Cn.st, sent: sent, recv: recv, dropped: dropped }); };
      var got = function (v) { recv++; Cn.st = 'delay'; Cn.at = t + 1000; E('collect', 'cons', 'got', v); };
      var trySend = function (v) {
        if (Cn.st === 'waiting' && buf.length === 0) { sent++; P.st = 'delay'; P.at = t + 100; got(v); return; }
        if (mode === 'conflated' && buf.length >= 1) { dropped++; E('skip', 'chan', 'replaced', buf[0]); buf = []; }
        if (mode === 'dropOldest' && buf.length >= cap) { dropped++; E('skip', 'chan', 'droppedOld', buf.shift()); }
        if (buf.length < cap) { buf.push(v); sent++; P.st = 'delay'; P.at = t + 100; E('emit', 'prod', 'buffered', v); }
        else { P.st = 'suspended'; P.pending = v; E('suspend', 'prod', 'full', v); }
      };
      var tryReceive = function () {
        if (buf.length) {
          var v = buf.shift(); got(v);
          if (P.st === 'suspended') { buf.push(P.pending); sent++; var pv = P.pending; P.st = 'delay'; P.at = t + 100; E('resume', 'prod', 'resumed', pv); }
          return;
        }
        if (P.st === 'suspended') { var w = P.pending; sent++; P.st = 'delay'; P.at = t + 100; E('resume', 'prod', 'handover', w); got(w); return; }
        if (closed) { Cn.st = 'done'; E('complete', 'cons', 'end'); return; }
        E('run', 'cons', 'waiting');
      };
      for (var guard = 0; guard < 400; guard++) {
        var times = [];
        if (P.st === 'ready' || P.st === 'delay') times.push(P.at);
        if (Cn.st === 'delay') times.push(Cn.at);
        if (!times.length) break;
        t = Math.min.apply(null, times);
        if (P.st === 'delay' && P.at === t) {
          E('run', 'prod', 'sentLine'); P.i++;
          if (P.i >= 5) { P.st = 'done'; closed = true; E('complete', 'prod', 'closed'); if (Cn.st === 'waiting' && !buf.length) { Cn.st = 'done'; E('complete', 'cons', 'end'); } }
          else P.st = 'ready';
        }
        if (P.st === 'ready' && P.at <= t) trySend(P.i * 2);
        if (Cn.st === 'delay' && Cn.at === t) { Cn.st = 'waiting'; tryReceive(); }
      }
      return ev;
    }
    var LINES = { buffered: [4], full: [4], resumed: [4], handover: [4], sentLine: [6], closed: [8], got: [10, 11], waiting: [10], end: [10], replaced: [2, 4], droppedOld: [2, 4] };
    function steps(s) {
      return simulate(s.mode).map(function (e, i) {
        var co = null;
        if (e.key === 'full') co = ['mechanism', s.mode === 'rendezvous' ? 'rendezvous' : 'full'];
        if (e.key === 'replaced') co = ['pitfall', 'conflated'];
        if (e.key === 'droppedOld') co = ['pitfall', 'dropOldest'];
        if (e.key === 'closed') co = ['mechanism', 'produce'];
        return step({ id: e.key + i, type: e.kind === 'skip' ? 'pitfall' : 'mechanism', titleKey: M(m, 's.' + e.key + '.title'), explainKey: M(m, 's.' + e.key + '.explain'), params: { v: e.v, n: e.n, t: e.t },
          activeNodes: [e.who], nodeStates: {}, metrics: { time: e.t, n: e.n, sent: e.sent, recv: e.recv, dropped: e.dropped },
          codeHighlight: { snippet: 'chanCap', lines: LINES[e.key] || [] }, callouts: co ? [{ kind: co[0], textKey: M(m, 'co.' + co[1]) }] : [],
          logEvents: [{ t: e.t, kind: e.kind, subject: e.who, scope: M(m, 'scope.' + s.mode), detailKey: M(m, 'ev.' + e.key), params: { v: e.v, n: e.n, p: e.p, c: e.c } }] });
      });
    }
    ADE.registerModel('coroutines.chan', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'chanCap',
      simplificationKeys: [M(m, 'simp.1'), K + 'simp.time'], controlsHintKey: M(m, 'ctl.hint'),
      controls: [{ id: 'mode', type: 'select', labelKey: M(m, 'ctl.mode'), get: function (s) { return s.mode; }, action: 'mode',
        options: ['rendezvous', 'buffered', 'unlimited', 'conflated', 'dropOldest'].map(function (v) { return { value: v, labelKey: M(m, 'ctl.mode.' + v) }; }) }],
      init: function () { return { mode: 'rendezvous' }; },
      act: function (s, a, v) { return { mode: CAP[v] !== undefined ? v : 'rendezvous' }; },
      steps: steps,
      selfChecks: [
        { name: 'nhận đúng theo sách: rendezvous 0,2,4,6,8; conflated chỉ 8; dropOldest 6,8; buffered có 3 lần Sent trước khi nhận 0', run: function () {
          var got = function (mode) { return simulate(mode).filter(function (e) { return e.key === 'got'; }).map(function (e) { return e.v; }).join(','); };
          var b = simulate('buffered'), firstGot = 0, sentBefore = 0;
          b.some(function (e, i) { if (e.key === 'got') { firstGot = i; return true; } return false; });
          b.slice(0, firstGot).forEach(function (e) { if (e.key === 'sentLine') sentBefore++; });
          return got('rendezvous') === '0,2,4,6,8' && got('unlimited') === '0,2,4,6,8' && got('conflated') === '8' && got('dropOldest') === '6,8' && sentBefore === 3;
        } }
      ]
    });
  })();
})();
