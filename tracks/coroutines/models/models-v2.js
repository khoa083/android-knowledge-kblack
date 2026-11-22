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
})();
