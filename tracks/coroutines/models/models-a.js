/* Model A0–A4 (thuần, không DOM, không câu chữ). Mọi quy tắc là mô hình giảng dạy (simplified); nguồn ở docs/research/coroutines.md.
   Khoá chuỗi bắt đầu bằng track.coroutines. */
(function () {
  'use strict';
  var C = ADE.coro, K = C.K, step = C.step;
  var M = function (m, s) { return K + 'm.' + m + '.' + s; };

  /* ================= A0: ví dụ hoàn chỉnh UI → ViewModel → repository → StateFlow ================= */
  (function () {
    var m = 'full';
    function steps(s) {
      var out = [], ui = K + 'st.ready';
      var ns = function (vm, repo, st) { return { ui: ui, vm: vm, repo: repo, state: st }; };
      var J = function (x) { return 'job.' + x; };
      out.push(step({ id: 'click', type: 'scenario', titleKey: M(m, 's.click.title'), explainKey: M(m, 's.click.explain'), activeNodes: ['ui'], movingSignals: [{ edge: 'e1', tok: 'state' }],
        nodeStates: ns(J('active'), K + 'st.idle', M(m, 'val.idle')), metrics: { state: M(m, 'val.idle') }, codeHighlight: { snippet: 'full', lines: [1, 2] }, logEvents: [] }));
      out.push(step({ id: 'launch', titleKey: M(m, 's.launch.title'), explainKey: M(m, 's.launch.explain'), activeNodes: ['vm'], movingSignals: [],
        nodeStates: ns(J('active'), K + 'st.idle', M(m, 'val.loading')), metrics: { state: M(m, 'val.loading') }, codeHighlight: { snippet: 'full', lines: [4, 5] },
        callouts: [{ kind: 'source', textKey: M(m, 'co.vmscope') }],
        logEvents: [{ t: 10, kind: 'launch', subject: 'vm', scope: K + 'scope.main', detailKey: M(m, 'ev.launch') }] }));
      out.push(step({ id: 'call', titleKey: M(m, 's.call.title'), explainKey: s.ctx ? M(m, 's.call.explain') : M(m, 's.callMain.explain'), activeNodes: ['vm', 'repo'], movingSignals: [{ edge: 'e2', tok: 'coroutine' }],
        nodeStates: ns(J('active'), s.ctx ? K + 'st.suspended' : K + 'st.blocking', M(m, 'val.loading')), metrics: { state: M(m, 'val.loading') }, codeHighlight: { snippet: 'full', lines: [5, 8] },
        callouts: s.ctx ? [{ kind: 'mechanism', textKey: M(m, 'co.withctx') }] : [{ kind: 'pitfall', textKey: M(m, 'co.mainblock') }],
        logEvents: [s.ctx ? { t: 20, kind: 'suspend', subject: 'vm', to: 'repo', scope: K + 'scope.main', detailKey: M(m, 'ev.call') } : { t: 20, kind: 'block', subject: 'repo', scope: K + 'scope.main', detailKey: M(m, 'ev.callMain') }] }));
      out.push(step({ id: 'work', titleKey: M(m, 's.work.title'), explainKey: s.ctx ? M(m, 's.work.explain') : M(m, 's.workMain.explain'), activeNodes: ['repo'], movingSignals: [],
        nodeStates: ns(J('active'), K + 'st.running', M(m, 'val.loading')), metrics: { state: M(m, 'val.loading') }, codeHighlight: { snippet: 'full', lines: [7, 8] },
        logEvents: [{ t: 30, kind: 'resume', subject: 'repo', scope: s.ctx ? K + 'scope.io' : K + 'scope.main', detailKey: s.ctx ? M(m, 'ev.work') : M(m, 'ev.workMain') }] }));
      if (s.leave) {
        out.push(step({ id: 'leave', type: 'experiment', titleKey: M(m, 's.leave.title'), explainKey: M(m, 's.leave.explain'), activeNodes: ['ui', 'vm'], movingSignals: [],
          nodeStates: ns(J('cancelling'), K + 'st.running', M(m, 'val.loading')), metrics: { state: M(m, 'val.loading') }, codeHighlight: { snippet: 'full', lines: [4, 5] },
          changes: [{ op: 'remove', textKey: M(m, 'ch.cleared') }],
          logEvents: [{ t: 40, kind: 'cancel', subject: 'vm', scope: K + 'scope.main', detailKey: M(m, 'ev.clear') }] }));
        out.push(step({ id: 'cancelled', type: 'pitfall', titleKey: M(m, 's.cancelled.title'), explainKey: s.ctx ? M(m, 's.cancelled.explain') : M(m, 's.cancelled.explainBlock'), activeNodes: ['vm', 'repo'], movingSignals: [],
          nodeStates: ns(J('cancelled'), K + 'st.done', M(m, 'val.idle')), metrics: { state: M(m, 'val.idle') },
          skipped: [{ whatKey: M(m, 'sk.emit.what'), whyKey: M(m, 'sk.emit.why') }], changes: [{ op: 'skip', textKey: M(m, 'ch.noemit') }],
          logEvents: [{ t: 50, kind: 'cancel', subject: 'repo', scope: s.ctx ? K + 'scope.io' : K + 'scope.main', detailKey: s.ctx ? M(m, 'ev.cancel') : M(m, 'ev.cancelLate') }] }));
        return out;
      }
      out.push(step({ id: 'return', titleKey: M(m, 's.return.title'), explainKey: M(m, 's.return.explain'), activeNodes: ['vm'], movingSignals: [{ edge: 'e3', tok: 'state' }],
        nodeStates: ns(J('active'), K + 'st.done', M(m, 'val.loading')), metrics: { state: M(m, 'val.loading') }, codeHighlight: { snippet: 'full', lines: [5, 6] },
        logEvents: [{ t: 60, kind: 'resume', subject: 'vm', scope: K + 'scope.main', detailKey: M(m, 'ev.resume') }] }));
      out.push(step({ id: 'emit', titleKey: M(m, 's.emit.title'), explainKey: M(m, 's.emit.explain'), activeNodes: ['state'], movingSignals: [{ edge: 'e4', tok: 'flow' }],
        nodeStates: ns(J('completed'), K + 'st.done', M(m, 'val.ready')), metrics: { state: M(m, 'val.ready') }, codeHighlight: { snippet: 'full', lines: [6] },
        stateBefore: [{ labelKey: M(m, 'st.value'), valueKey: M(m, 'val.loading') }], stateAfter: [{ labelKey: M(m, 'st.value'), valueKey: M(m, 'val.ready') }],
        changes: [{ op: 'set', textKey: M(m, 'ch.value') }],
        logEvents: [{ t: 70, kind: 'emit', subject: 'state', scope: K + 'scope.main', detailKey: M(m, 'ev.emit') }, { t: 70, kind: 'complete', subject: 'vm', scope: K + 'scope.main', detailKey: M(m, 'ev.complete') }] }));
      out.push(step({ id: 'collect', titleKey: M(m, 's.collect.title'), explainKey: M(m, 's.collect.explain'), activeNodes: ['ui'], movingSignals: [],
        nodeStates: ns(J('completed'), K + 'st.done', M(m, 'val.ready')), metrics: { state: M(m, 'val.ready') }, codeHighlight: { snippet: 'full', lines: [10, 11] },
        callouts: [{ kind: 'android', textKey: M(m, 'co.collect') }],
        logEvents: [{ t: 80, kind: 'collect', subject: 'ui', scope: K + 'scope.main', detailKey: M(m, 'ev.collect') }] }));
      return out;
    }
    ADE.registerModel('coroutines.full', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'full',
      simplificationKeys: [M(m, 'simp.1'), M(m, 'simp.2'), K + 'simp.time'], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        { id: 'ctx', type: 'toggle', labelKey: M(m, 'ctl.ctx'), get: function (s) { return s.ctx; }, action: 'ctx' },
        { id: 'leave', type: 'toggle', labelKey: M(m, 'ctl.leave'), get: function (s) { return s.leave; }, action: 'leave' }
      ],
      init: function () { return { ctx: true, leave: false }; },
      act: function (s, a, v) { var n = { ctx: s.ctx, leave: s.leave }; n[a] = !!v; return n; },
      steps: steps,
      selfChecks: [
        { name: 'có chuyển context: 7 bước; rời màn hình: 6 bước, không emit', run: function () {
          var d = ADE.models['coroutines.full'], a = d.steps({ ctx: true, leave: false }), b = d.steps({ ctx: true, leave: true });
          return a.length === 7 && b.length === 6 && !b.some(function (x) { return x.logEvents.some(function (e) { return e.kind === 'emit'; }); });
        } }
      ]
    });
  })();

  /* ================= A1: suspend và continuation ================= */
  (function () {
    var m = 'suspend';
    function steps(s) {
      var segsA = [{ k: 'run', ms: 10 }, { k: s.block ? 'block' : 'delay', ms: 30 }, { k: 'run', ms: 10 }];
      var tasks = [{ id: 'a', segs: segsA }, { id: 'b', segs: [{ k: 'run', ms: 20 }] }];
      var ev = C.simulate(tasks, s.threads);
      return C.schedSteps(ev, { tasks: ['a', 'b'], threadNodes: ['th0', 'th1'], threadsUsed: s.threads, extra: function (st, e, n) {
        st.codeHighlight = { snippet: 'suspend', lines: e.task === 'a' ? (s.block ? [3] : [3]) : [8] };
        if (n === 0) st.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        if (e.kind === 'block') st.callouts = [{ kind: 'pitfall', textKey: M(m, 'co.block') }];
        if (e.kind === 'suspend') st.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.suspend') }];
        if (e.kind === 'resume' && e.task === 'b' && e.waited > 0) st.callouts = [{ kind: 'pitfall', textKey: M(m, 'co.wait') }];
      } });
    }
    ADE.registerModel('coroutines.suspend', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'suspend',
      simplificationKeys: [M(m, 'simp.1'), K + 'simp.sched', K + 'simp.time', K + 'simp.threads'], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        { id: 'block', type: 'toggle', labelKey: M(m, 'ctl.block'), get: function (s) { return s.block; }, action: 'block' },
        { id: 'threads', type: 'select', labelKey: M(m, 'ctl.threads'), get: function (s) { return s.threads; }, action: 'threads',
          options: [{ value: 1, labelKey: M(m, 'ctl.threads.n'), params: { n: 1 } }, { value: 2, labelKey: M(m, 'ctl.threads.n'), params: { n: 2 } }] }
      ],
      init: function () { return { block: false, threads: 1 }; },
      act: function (s, a, v) { return a === 'block' ? { block: !!v, threads: s.threads } : { block: s.block, threads: v === 2 ? 2 : 1 }; },
      steps: steps,
      selfChecks: [
        { name: '1 luồng: delay → b xong t=30; block → b xong t=70; 2 luồng + block → b xong t=20', run: function () {
          var d = ADE.models['coroutines.suspend'];
          var fin = function (s) { var st = d.steps(s), r = null; st.forEach(function (x) { x.logEvents.forEach(function (e) { if (e.kind === 'complete' && e.subject === 'b') r = e.t; }); }); return r; };
          return fin({ block: false, threads: 1 }) === 30 && fin({ block: true, threads: 1 }) === 70 && fin({ block: true, threads: 2 }) === 20;
        } }
      ]
    });
  })();

  /* ================= A2: cây Job, scope, lan truyền hủy và lỗi ================= */
  (function () {
    var m = 'jobtree';
    var TREE = { root: null, c1: 'root', c2: 'root', c3: 'root', g: 'c2' };
    var IDS = ['root', 'c1', 'c2', 'c3', 'g'];
    var kidsOf = function (id) { return IDS.filter(function (x) { return TREE[x] === id; }); };
    var descendants = function (id) { var out = []; kidsOf(id).forEach(function (k) { out.push(k); out = out.concat(descendants(k)); }); return out; };
    var isLive = function (st) { return st === 'active' || st === 'waiting'; };

    /* Quy tắc lan truyền (nguồn: exception-handling, coroutine-context-and-dispatchers, cancellation):
       1) Hủy một Job hủy đệ quy mọi con; hủy một con KHÔNG hủy cha.
       2) Lỗi (exception) của con với Job thường: con thành failed, con của nó bị hủy, rồi lỗi lan lên cha: cha failed và các con khác của cha bị hủy.
       3) supervisorScope/SupervisorJob: lỗi hoặc hủy của một con không lan lên supervisor hay con khác (chỉ các con TRỰC TIẾP của supervisor).
       Trả về danh sách chuyển trạng thái [{id, to, why}] theo thứ tự xảy ra; không sửa trạng thái đầu vào. */
    function propagate(st, act, scope) {
      var trans = [], cur = JSON.parse(JSON.stringify(st));
      var set = function (id, to, why) { if (cur[id] === to) return; cur[id] = to; trans.push({ id: id, to: to, why: why }); };
      var cancelTree = function (id, why) { descendants(id).forEach(function (d) { if (isLive(cur[d])) set(d, 'cancelled', why); }); };
      if (act.a === 'cancel') {
        if (!isLive(cur[act.n])) return { trans: trans, after: cur };
        var hasKids = descendants(act.n).some(function (d) { return isLive(cur[d]); });
        cancelTree(act.n, 'parent');
        set(act.n, hasKids ? 'cancelling' : 'cancelled', 'request');
      } else if (act.a === 'fail') {
        if (!isLive(cur[act.n])) return { trans: trans, after: cur };
        set(act.n, 'failed', 'throw'); cancelTree(act.n, 'parent');
        var node = act.n;
        while (TREE[node]) {
          var p = TREE[node];
          if (p === 'root' && scope === 'supervisor') break;      // supervisor chặn lan lên
          if (!isLive(cur[p])) break;
          set(p, 'failed', 'child'); cancelTree(p, 'sibling'); node = p;
        }
      }
      return { trans: trans, after: cur };
    }
    // Sau mọi thao tác: các Job còn sống tự hoàn tất từ lá lên; cancelling → cancelled khi con đã xong.
    function settle(st) {
      var cur = JSON.parse(JSON.stringify(st)), trans = [];
      var order = ['g', 'c1', 'c2', 'c3', 'root'];
      order.forEach(function (id) {
        if (cur[id] === 'cancelling') { cur[id] = 'cancelled'; trans.push({ id: id, to: 'cancelled', why: 'children' }); }
        else if (isLive(cur[id])) { cur[id] = 'completed'; trans.push({ id: id, to: 'completed', why: 'body' }); }
      });
      return { trans: trans, after: cur };
    }
    function counts(st) {
      var c = { active: 0, cancelled: 0, failed: 0 };
      IDS.forEach(function (id) { var v = st[id]; if (v === 'active' || v === 'waiting' || v === 'cancelling') c.active++; else if (v === 'cancelled') c.cancelled++; else if (v === 'failed') c.failed++; });
      return c;
    }
    var stateKey = function (v) { return 'job.' + v; };
    var kindOf = function (to) { return to === 'failed' ? 'exception' : (to === 'completed' ? 'complete' : 'cancel'); };
    var NAME = { root: 'root', c1: 'child-1', c2: 'child-2', c3: 'child-3', g: 'grandchild' };

    function mk(st, id, type, titleKey, explainKey, params, trans, extra) {
      var ns = {}; IDS.forEach(function (j) { ns[j] = stateKey(st[j]); });
      var c = counts(st);
      var s = step({ id: id, type: type, titleKey: titleKey, explainKey: explainKey, params: params, nodeStates: ns,
        metrics: { active: c.active, cancelled: c.cancelled, failed: c.failed }, codeHighlight: { snippet: 'jobtree', lines: [] },
        activeNodes: trans.map(function (x) { return x.id; }),
        changes: trans.map(function (x) { return { op: x.to === 'completed' ? 'set' : 'remove', textKey: M(m, 'ch.' + x.to), params: { job: NAME[x.id] } }; }),
        logEvents: trans.map(function (x, i) { return { t: 0, kind: kindOf(x.to), subject: x.id, detailKey: M(m, 'ev.' + x.to + '.' + x.why), params: { job: NAME[x.id] } }; }) });
      if (extra) extra(s);
      return s;
    }
    function steps(s) {
      var out = [], st = { root: 'waiting', c1: 'active', c2: 'active', c3: 'active', g: 'active' }, clock = 0;
      out.push(mk(st, 'create', 'scenario', M(m, 's.create.title'), s.scope === 'supervisor' ? M(m, 's.create.explainSup') : M(m, 's.create.explain'), {}, [], function (x) {
        x.logEvents = IDS.map(function (id) { return { t: 0, kind: 'launch', subject: id, detailKey: M(m, 'ev.launch'), params: { job: NAME[id] } }; });
        x.activeNodes = IDS.slice(); x.codeHighlight = { snippet: 'jobtree', lines: s.scope === 'supervisor' ? [1, 2, 3, 4] : [1, 2, 3, 4] };
        x.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
      }));
      s.acts.forEach(function (a, i) {
        var r = propagate(st, a, s.scope);
        var title = a.a === 'cancel' ? M(m, 's.cancel.title') : M(m, 's.fail.title');
        var explainKey = a.a === 'cancel' ? M(m, 's.cancel.explain') : (s.scope === 'supervisor' ? M(m, 's.fail.explainSup') : M(m, 's.fail.explain'));
        if (!r.trans.length) explainKey = M(m, 's.noop.explain');
        st = r.after; clock += 10;
        out.push(mk(st, 'act' + i, 'experiment', title, explainKey, { job: NAME[a.n] }, r.trans, function (x) {
          x.logEvents.forEach(function (e) { e.t = clock; });
          if (a.a === 'fail' && s.scope === 'coroutine' && a.n !== 'root') x.callouts = [{ kind: 'pitfall', textKey: M(m, 'co.propagate') }];
          if (a.a === 'fail' && s.scope === 'supervisor') x.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.supervisor') }];
          if (a.a === 'cancel' && a.n !== 'root') x.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.cancelChild') }];
          x.skipped = !r.trans.length ? [{ whatKey: M(m, 'sk.noop.what'), whyKey: M(m, 'sk.noop.why') }] : [];
          x.codeHighlight = { snippet: 'jobtree', lines: a.a === 'cancel' ? [6] : [7] };
        }));
        var sr = settle(st);
        if (sr.trans.some(function (x) { return x.to === 'cancelled'; }) && r.trans.some(function (x) { return x.to === 'cancelling'; })) {
          // chỉ tách bước "con xong hủy → cha cancelled" khi có cancelling
          var only = sr.trans.filter(function (x) { return x.to === 'cancelled'; });
          var st2 = JSON.parse(JSON.stringify(st)); only.forEach(function (x) { st2[x.id] = 'cancelled'; });
          clock += 5;
          out.push(mk(st2, 'wait' + i, 'mechanism', M(m, 's.children.title'), M(m, 's.children.explain'), {}, only, function (x) { x.logEvents.forEach(function (e) { e.t = clock; }); }));
          st = st2;
        }
      });
      var fin = settle(st);
      clock += 10;
      out.push(mk(fin.after, 'settle', 'mechanism', M(m, 's.settle.title'), M(m, 's.settle.explain'), {}, fin.trans, function (x) { x.logEvents.forEach(function (e) { e.t = clock; }); x.codeHighlight = { snippet: 'jobtree', lines: [8] }; }));
      return out;
    }
    var BTN = function (id, a, n, icon) { return { id: id, type: 'button', labelKey: M(m, 'ctl.' + id), action: 'add', payload: { a: a, n: n }, icon: icon }; };
    ADE.registerModel('coroutines.jobtree', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'jobtree',
      simplificationKeys: [M(m, 'simp.1'), M(m, 'simp.2')], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        { id: 'scope', type: 'select', labelKey: M(m, 'ctl.scope'), get: function (s) { return s.scope; }, action: 'scope',
          options: [{ value: 'coroutine', labelKey: M(m, 'ctl.scope.coroutine') }, { value: 'supervisor', labelKey: M(m, 'ctl.scope.supervisor') }] },
        BTN('cancelC1', 'cancel', 'c1', 'remove'), BTN('cancelC2', 'cancel', 'c2', 'remove'), BTN('cancelRoot', 'cancel', 'root', 'remove'),
        BTN('failC1', 'fail', 'c1', 'bolt'), BTN('failG', 'fail', 'g', 'bolt'),
        { id: 'undo', type: 'button', labelKey: M(m, 'ctl.undo'), action: 'undo', icon: 'prev' },
        { id: 'clear', type: 'button', labelKey: M(m, 'ctl.clear'), action: 'clear', icon: 'reset' }
      ],
      sampleStates: function () {
        var out = [], A = function (a, n) { return { a: a, n: n }; };
        var seqs = [[A('cancel', 'c1')], [A('cancel', 'c2')], [A('cancel', 'root')], [A('fail', 'c1')], [A('fail', 'g')], [A('fail', 'root')], [A('cancel', 'c2'), A('fail', 'c1')], [A('fail', 'g'), A('cancel', 'c1')], [A('cancel', 'root'), A('fail', 'c1')], [A('cancel', 'c1'), A('cancel', 'c1')]];
        ['coroutine', 'supervisor'].forEach(function (sc) { seqs.forEach(function (q) { out.push({ scope: sc, acts: q }); }); });
        return out;
      },
      init: function () { return { scope: 'coroutine', acts: [] }; },
      act: function (s, a, v) {
        var n = { scope: s.scope, acts: s.acts.slice() };
        if (a === 'scope') n.scope = v === 1 || v === 'supervisor' ? 'supervisor' : 'coroutine';
        else if (a === 'add') { if (n.acts.length < 5) n.acts.push(v); }
        else if (a === 'undo') n.acts.pop();
        else if (a === 'clear') n.acts = [];
        return n;
      },
      steps: steps,
      selfChecks: [
        { name: 'coroutineScope: con lỗi hủy con khác và cha; supervisorScope: chỉ con đó lỗi', run: function () {
          var base = { root: 'waiting', c1: 'active', c2: 'active', c3: 'active', g: 'active' };
          var a = propagate(base, { a: 'fail', n: 'c1' }, 'coroutine').after, b = propagate(base, { a: 'fail', n: 'c1' }, 'supervisor').after;
          return a.root === 'failed' && a.c2 === 'cancelled' && a.c3 === 'cancelled' && a.g === 'cancelled' && b.root === 'waiting' && b.c2 === 'active' && b.c1 === 'failed';
        } },
        { name: 'hủy một con không hủy cha; hủy cha hủy mọi con', run: function () {
          var base = { root: 'waiting', c1: 'active', c2: 'active', c3: 'active', g: 'active' };
          var a = propagate(base, { a: 'cancel', n: 'c2' }, 'coroutine').after, b = propagate(base, { a: 'cancel', n: 'root' }, 'coroutine').after;
          return a.root === 'waiting' && a.c2 === 'cancelling' && a.g === 'cancelled' && b.c1 === 'cancelled' && b.c3 === 'cancelled' && b.g === 'cancelled' && b.root === 'cancelling';
        } },
        { name: 'lỗi ở cháu lan lên con rồi tới cha (coroutineScope) nhưng dừng ở supervisor', run: function () {
          var base = { root: 'waiting', c1: 'active', c2: 'active', c3: 'active', g: 'active' };
          var a = propagate(base, { a: 'fail', n: 'g' }, 'coroutine').after, b = propagate(base, { a: 'fail', n: 'g' }, 'supervisor').after;
          return a.c2 === 'failed' && a.root === 'failed' && a.c1 === 'cancelled' && b.c2 === 'failed' && b.root === 'waiting' && b.c1 === 'active';
        } }
      ]
    });
  })();

  /* ================= A3: builders và ghép công việc ================= */
  (function () {
    var m = 'builders';
    function steps(s) {
      var out = [], P = 300, T = 200;       // thời gian giả định (ms, minh họa)
      var ns = function (p, st, pa) { return { parent: pa || 'job.active', profile: p, settings: st }; };
      var ev = function (t, kind, subject, key, params) { return { t: t, kind: kind, subject: subject, detailKey: M(m, 'ev.' + key), params: params || {} }; };
      var mkStep = function (id, type, key, active, nodeStates, time, logs, extra) {
        var o = step({ id: id, type: type, titleKey: M(m, 's.' + key + '.title'), explainKey: M(m, 's.' + key + '.explain'), params: { p: P, t: T }, activeNodes: active, nodeStates: nodeStates, metrics: { time: time }, logEvents: logs, codeHighlight: { snippet: 'builders', lines: [] } });
        if (extra) extra(o); return o;
      };
      var idle = K + 'st.idle', run = K + 'st.running', done = K + 'st.done', can = 'job.cancelled', fail = 'job.failed';
      out.push(mkStep('scope', 'scenario', s.conc ? 'scopeConc' : 'scopeSeq', ['parent'], ns(idle, idle), 0, [ev(0, 'launch', 'parent', 'scope')], function (o) { o.codeHighlight.lines = s.conc ? [1, 2, 3, 4] : [1, 2, 3]; o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }]; }));
      if (!s.conc) {
        out.push(mkStep('profile', 'mechanism', 'profile', ['profile'], ns(run, idle), 0, [ev(0, 'launch', 'profile', 'profile')], function (o) { o.codeHighlight.lines = [2]; }));
        out.push(mkStep('profileDone', 'mechanism', 'profileDone', ['profile'], ns(done, idle), P, [ev(P, 'complete', 'profile', 'profileDone')], function (o) { o.codeHighlight.lines = [2]; }));
        if (s.fail) {
          out.push(mkStep('settingsFail', 'pitfall', 'settingsFailSeq', ['settings', 'parent'], { parent: fail, profile: done, settings: fail }, P + T, [ev(P + T, 'exception', 'settings', 'settingsFail'), ev(P + T, 'exception', 'parent', 'parentFail')], function (o) { o.codeHighlight.lines = [3]; o.metrics = { time: P + T }; }));
          return out;
        }
        out.push(mkStep('settings', 'mechanism', 'settingsSeq', ['settings'], ns(done, run), P, [ev(P, 'launch', 'settings', 'settings')], function (o) { o.codeHighlight.lines = [3]; }));
        out.push(mkStep('settingsDone', 'mechanism', 'settingsDone', ['settings'], ns(done, done), P + T, [ev(P + T, 'complete', 'settings', 'settingsDone')], function (o) { o.codeHighlight.lines = [3]; }));
        out.push(mkStep('combine', 'mechanism', 'combine', ['parent'], ns(done, done, 'job.completed'), P + T, [ev(P + T, 'complete', 'parent', 'combine')], function (o) { o.codeHighlight.lines = [4]; o.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.seq') }]; }));
        return out;
      }
      out.push(mkStep('asyncBoth', 'mechanism', 'asyncBoth', ['profile', 'settings'], ns(run, run), 0, [ev(0, 'launch', 'profile', 'asyncP'), ev(0, 'launch', 'settings', 'asyncS')], function (o) { o.codeHighlight.lines = [2, 3]; o.movingSignals = [{ edge: 'e1', tok: 'coroutine' }, { edge: 'e2', tok: 'coroutine' }]; }));
      out.push(mkStep('await', 'mechanism', 'await', ['parent'], ns(run, run), 0, [ev(0, 'suspend', 'parent', 'await')], function (o) { o.codeHighlight.lines = [4]; o.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.await') }]; }));
      if (s.fail) {
        out.push(mkStep('settingsFail', 'pitfall', 'settingsFailConc', ['settings', 'parent', 'profile'], { parent: fail, profile: can, settings: fail }, T, [ev(T, 'exception', 'settings', 'settingsFail'), ev(T, 'cancel', 'profile', 'profileCancel'), ev(T, 'exception', 'parent', 'parentFail')], function (o) { o.codeHighlight.lines = [3, 4]; o.callouts = [{ kind: 'source', textKey: M(m, 'co.structured') }]; o.skipped = [{ whatKey: M(m, 'sk.profile.what'), whyKey: M(m, 'sk.profile.why') }]; o.changes = [{ op: 'remove', textKey: M(m, 'ch.profileCancelled') }]; }));
        return out;
      }
      out.push(mkStep('settingsDone', 'mechanism', 'settingsDone', ['settings'], ns(run, done), T, [ev(T, 'complete', 'settings', 'settingsDone')], function (o) { o.codeHighlight.lines = [3]; }));
      out.push(mkStep('profileDone', 'mechanism', 'profileDone', ['profile'], ns(done, done), P, [ev(P, 'complete', 'profile', 'profileDone')], function (o) { o.codeHighlight.lines = [2]; }));
      out.push(mkStep('combine', 'mechanism', 'combineConc', ['parent'], ns(done, done, 'job.completed'), P, [ev(P, 'resume', 'parent', 'resumeAwait'), ev(P, 'complete', 'parent', 'combine')], function (o) { o.codeHighlight.lines = [4]; o.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.conc') }]; }));
      return out;
    }
    ADE.registerModel('coroutines.builders', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'builders',
      simplificationKeys: [M(m, 'simp.1'), K + 'simp.time'], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        { id: 'conc', type: 'toggle', labelKey: M(m, 'ctl.conc'), get: function (s) { return s.conc; }, action: 'conc' },
        { id: 'fail', type: 'toggle', labelKey: M(m, 'ctl.fail'), get: function (s) { return s.fail; }, action: 'fail' }
      ],
      init: function () { return { conc: false, fail: false }; },
      act: function (s, a, v) { var n = { conc: s.conc, fail: s.fail }; n[a] = !!v; return n; },
      steps: steps,
      selfChecks: [
        { name: 'tuần tự 500 ms, đồng thời 300 ms (giả định 300 + 200)', run: function () {
          var d = ADE.models['coroutines.builders'], last = function (s) { var st = d.steps(s); return st[st.length - 1].metrics.time; };
          return last({ conc: false, fail: false }) === 500 && last({ conc: true, fail: false }) === 300;
        } },
        { name: 'đồng thời + lỗi: dừng ở 200 ms và hủy profile', run: function () {
          var st = ADE.models['coroutines.builders'].steps({ conc: true, fail: true }), l = st[st.length - 1];
          return l.metrics.time === 200 && l.logEvents.some(function (e) { return e.kind === 'cancel' && e.subject === 'profile'; });
        } }
      ]
    });
  })();

  /* ================= A4: CoroutineContext và Dispatcher ================= */
  (function () {
    var m = 'context';
    function steps(s) {
      var out = [], disp = s.disp === 'io' ? 'Dispatchers.IO' : 'Dispatchers.Default', w1 = 1 + (s.seed % 3), w2 = 1 + ((s.seed + 1) % 3);
      var ctxMain = [{ labelKey: M(m, 'st.job'), value: 'Job' }, { labelKey: M(m, 'st.disp'), value: 'Dispatchers.Main' }, { labelKey: M(m, 'st.name'), value: 'CoroutineName("load")' }];
      var ctxPool = [{ labelKey: M(m, 'st.job'), value: 'Job' }, { labelKey: M(m, 'st.disp'), value: disp }, { labelKey: M(m, 'st.name'), value: 'CoroutineName("load")' }];
      var P = { disp: disp, w1: w1, w2: w2 };
      var ns = function (co, main, pool) { return { co: co, main: main, pool: pool }; };
      var ev = function (t, kind, key, scope, to) { return { t: t, kind: kind, subject: 'co', to: to, scope: scope, detailKey: M(m, 'ev.' + key), params: P }; };
      out.push(step({ id: 'launch', type: 'scenario', titleKey: M(m, 's.launch.title'), explainKey: M(m, 's.launch.explain'), params: P, activeNodes: ['co', 'main'], stateAfter: ctxMain,
        nodeStates: ns(K + 'st.ready', K + 'st.busy', K + 'st.free'), codeHighlight: { snippet: 'context', lines: [1, 2] }, metrics: { time: 0 },
        callouts: [{ kind: 'mechanism', textKey: M(m, 'co.plus') }], logEvents: [ev(0, 'launch', 'launch', K + 'scope.main')] }));
      out.push(step({ id: 'run1', titleKey: M(m, 's.run1.title'), explainKey: M(m, 's.run1.explain'), params: P, activeNodes: ['co', 'main'], stateBefore: ctxMain, stateAfter: ctxMain,
        nodeStates: ns(K + 'st.running', K + 'st.busy', K + 'st.free'), codeHighlight: { snippet: 'context', lines: [3] }, metrics: { time: 10 }, logEvents: [ev(10, 'resume', 'run1', K + 'scope.main')] }));
      if (s.mainBlock) {
        out.push(step({ id: 'blockMain', type: 'pitfall', titleKey: M(m, 's.blockMain.title'), explainKey: M(m, 's.blockMain.explain'), params: P, activeNodes: ['co', 'main'], stateBefore: ctxMain, stateAfter: ctxMain,
          nodeStates: ns(K + 'st.blocking', K + 'st.busy', K + 'st.unused'), codeHighlight: { snippet: 'context', lines: [4] }, metrics: { time: 40 },
          callouts: [{ kind: 'pitfall', textKey: M(m, 'co.blockMain') }], logEvents: [ev(10, 'block', 'blockMain', K + 'scope.main')] }));
      } else {
        out.push(step({ id: 'withCtx', titleKey: M(m, 's.withCtx.title'), explainKey: M(m, 's.withCtx.explain'), params: P, activeNodes: ['co', 'pool'], movingSignals: [{ edge: 'e1', tok: 'coroutine' }], stateBefore: ctxMain, stateAfter: ctxPool,
          changes: [{ op: 'set', textKey: M(m, 'ch.disp'), params: P }], nodeStates: ns(K + 'st.suspended', K + 'st.free', K + 'st.ready'), codeHighlight: { snippet: 'context', lines: [4] }, metrics: { time: 20 },
          callouts: [{ kind: 'mechanism', textKey: M(m, 'co.withctx') }], logEvents: [ev(20, 'suspend', 'withCtx', K + 'scope.main', 'pool')] }));
        out.push(step({ id: 'work', titleKey: M(m, 's.work.title'), explainKey: M(m, 's.work.explain'), params: P, activeNodes: ['co', 'pool'], stateBefore: ctxPool, stateAfter: ctxPool,
          nodeStates: ns(K + 'st.running', K + 'st.free', K + 'st.busy'), codeHighlight: { snippet: 'context', lines: [5] }, metrics: { time: 50 },
          callouts: [{ kind: 'android', textKey: M(m, 'co.threadName') }], logEvents: [ev(30, 'resume', 'work', K + 'thread.pool1')] }));
        out.push(step({ id: 'back', titleKey: M(m, 's.back.title'), explainKey: M(m, 's.back.explain'), params: P, activeNodes: ['co', 'main'], movingSignals: [{ edge: 'e2', tok: 'coroutine' }], stateBefore: ctxPool, stateAfter: ctxMain,
          changes: [{ op: 'set', textKey: M(m, 'ch.back') }], nodeStates: ns(K + 'st.running', K + 'st.busy', K + 'st.free'), codeHighlight: { snippet: 'context', lines: [6] }, metrics: { time: 60 }, logEvents: [ev(60, 'resume', 'back', K + 'scope.main')] }));
      }
      out.push(step({ id: 'done', titleKey: M(m, 's.done.title'), explainKey: M(m, 's.done.explain'), params: P, activeNodes: ['co'], nodeStates: ns(K + 'st.done', K + 'st.free', K + 'st.free'), metrics: { time: s.mainBlock ? 50 : 70 },
        codeHighlight: { snippet: 'context', lines: [7] }, logEvents: [{ t: s.mainBlock ? 50 : 70, kind: 'complete', subject: 'co', scope: K + 'scope.main', detailKey: M(m, 'ev.done'), params: P }] }));
      return out;
    }
    ADE.registerModel('coroutines.context', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'context',
      simplificationKeys: [M(m, 'simp.1'), K + 'simp.threads', K + 'simp.sched'], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        { id: 'disp', type: 'select', labelKey: M(m, 'ctl.disp'), get: function (s) { return s.disp === 'io' ? 1 : 2; }, action: 'disp',
          options: [{ value: 1, labelKey: M(m, 'ctl.disp.io') }, { value: 2, labelKey: M(m, 'ctl.disp.default') }] },
        { id: 'mainBlock', type: 'toggle', labelKey: M(m, 'ctl.mainBlock'), get: function (s) { return s.mainBlock; }, action: 'mainBlock' },
        { id: 'seed', type: 'button', labelKey: M(m, 'ctl.seed'), action: 'seed', icon: 'refresh' }
      ],
      init: function () { return { disp: 'io', mainBlock: false, seed: 0 }; },
      act: function (s, a, v) {
        var n = { disp: s.disp, mainBlock: s.mainBlock, seed: s.seed };
        if (a === 'disp') n.disp = v === 1 ? 'io' : 'default'; else if (a === 'mainBlock') n.mainBlock = !!v; else if (a === 'seed') n.seed = s.seed + 1;
        return n;
      },
      steps: steps,
      selfChecks: [
        { name: 'đổi dispatcher không đổi số bước; chặn Main bỏ withContext', run: function () {
          var d = ADE.models['coroutines.context'];
          return d.steps({ disp: 'io', mainBlock: false, seed: 0 }).length === 6 && d.steps({ disp: 'default', mainBlock: false, seed: 5 }).length === 6 && d.steps({ disp: 'io', mainBlock: true, seed: 0 }).length === 4;
        } }
      ]
    });
  })();
})();
