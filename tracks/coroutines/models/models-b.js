/* Model A5 (hủy và timeout) và A6 (exception và supervision). Thuần, không DOM, không câu chữ.
   Thời gian là minh họa (mỗi đơn vị công việc 100 ms giả định), không phải benchmark. */
(function () {
  'use strict';
  var C = ADE.coro, K = C.K, step = C.step;
  var M = function (m, s) { return K + 'm.' + m + '.' + s; };

  /* ================= A5: hủy hợp tác và timeout ================= */
  (function () {
    var m = 'cancel', UNIT = 100, N = 5;
    /* Quy tắc (nguồn: coroutines-cancellation, coroutines-best-practices):
       - Hủy là hợp tác: coroutine chỉ phản ứng khi kiểm tra hủy (isActive/ensureActive) hoặc khi suspend.
       - Bắt CancellationException rồi không ném lại thì hủy không có tác dụng ở chỗ đó.
       - Khối finally chạy khi bị hủy; hàm suspend trong finally bị hủy ngay trừ khi bọc withContext(NonCancellable).
       - Với timeout, mô hình giả định mã hợp tác (coop = true); withTimeout ném TimeoutCancellationException,
         withTimeoutOrNull trả null. */
    function plan(s) {
      var coop = s.mode === 'cancel' ? s.coop : true;
      var stopAt = s.mode === 'cancel' ? (s.at - 1) * UNIT + UNIT / 2 : 250;
      return { coop: coop, stopAt: stopAt };
    }
    function steps(s) {
      var p = plan(s), out = [], t = 0, requested = false, thrown = false, units = 0;
      var P = { at: s.at, stop: p.stopAt, n: N, unit: UNIT, ms: 50 };
      var ns = function (job, caller, cleanup) { return { job: job, caller: caller || K + 'st.idle', cleanup: cleanup || K + 'st.idle' }; };
      var J = function (x) { return 'job.' + x; };
      var jobState = J('active');
      var ev = function (tt, kind, subj, key, extra) { var e = { t: tt, kind: kind, subject: subj, detailKey: M(m, 'ev.' + key), params: P }; if (extra) for (var k in extra) e[k] = extra[k]; return e; };
      var mk = function (id, type, key, tt, active, nodes, logs, extra) {
        var o = step({ id: id, type: type, titleKey: M(m, 's.' + key + '.title'), explainKey: M(m, 's.' + key + '.explain'), params: P, activeNodes: active, nodeStates: nodes, metrics: { units: units, time: tt }, logEvents: logs, codeHighlight: { snippet: 'cancel', lines: [] } });
        if (extra) extra(o); return o;
      };
      out.push(mk('launch', 'scenario', s.mode === 'cancel' ? 'launch' : 'launchTimeout', 0, ['job'], ns(jobState), [ev(0, 'launch', 'job', 'launch')], function (o) {
        o.codeHighlight.lines = s.mode === 'cancel' ? [1, 2, 3] : [1, 2];
        o.callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
        // điều khiển không có tác dụng ở cấu hình này: nói rõ lý do
        if (s.mode !== 'cancel' && !s.coop) o.callouts.push({ kind: 'mechanism', textKey: M(m, 'co.coopIgnored') });
        if (s.fin !== 'none' && (!p.coop || s.swallow)) o.callouts.push({ kind: 'mechanism', textKey: M(m, 'co.finIgnored') });
      }));
      var request = function (tt) {
        requested = true; jobState = J('cancelling');
        var key = s.mode === 'cancel' ? 'request' : 'timeoutFired';
        out.push(mk('request', 'experiment', key, tt, ['caller', 'job'], ns(jobState, K + 'st.done'), [ev(tt, 'cancel', 'caller', key, { to: 'job' })], function (o) {
          o.movingSignals = [{ edge: 'e1', tok: 'cancel' }]; o.codeHighlight.lines = s.mode === 'cancel' ? [6] : [1];
          o.changes = [{ op: 'set', textKey: M(m, 'ch.cancelling') }];
          o.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.request') }];
        }));
      };
      for (var i = 1; i <= N && !thrown; i++) {
        var end = i * UNIT;
        if (!requested && p.stopAt < end) request(p.stopAt);
        t = end; units = i;
        out.push(mk('unit' + i, 'mechanism', 'unit', t, ['job'], ns(jobState), [ev(t, 'run', 'job', 'unit', { })], function (o) { o.params = { at: s.at, stop: p.stopAt, n: N, unit: UNIT, i: units, done: units }; o.logEvents[0].params = o.params; o.codeHighlight.lines = [4]; }));
        var unitIdx = i;
        if (p.coop) {
          var req = requested;
          var key = req ? (s.swallow ? 'checkSwallow' : 'checkThrow') : 'checkOk';
          out.push(mk('check' + i, req ? 'pitfall' : 'mechanism', key, t, ['job'], ns(jobState), [ev(t, 'check', 'job', key, { })], function (o) {
            o.params = { at: s.at, stop: p.stopAt, n: N, unit: UNIT, i: unitIdx }; o.logEvents[0].params = o.params; o.codeHighlight.lines = [5];
            if (req && s.swallow) { o.callouts = [{ kind: 'pitfall', textKey: M(m, 'co.swallow') }, { kind: 'source', textKey: M(m, 'co.noswallow') }]; o.skipped = [{ whatKey: M(m, 'sk.stop.what'), whyKey: M(m, 'sk.stop.why') }]; o.changes = [{ op: 'skip', textKey: M(m, 'ch.stopSkipped') }]; }
            if (req && !s.swallow) o.changes = [{ op: 'remove', textKey: M(m, 'ch.stopped') }];
          }));
          if (req && !s.swallow) {
            thrown = true;
            // finally / cleanup
            if (s.fin !== 'none') {
              var nc = s.fin === 'nc';
              out.push(mk('cleanup', 'mechanism', nc ? 'cleanupNC' : 'cleanupPlain', t + (nc ? 50 : 0), ['job', 'cleanup'], ns(jobState, K + 'st.done', nc ? K + 'st.done' : K + 'st.blocking'),
                [ev(t + (nc ? 50 : 0), nc ? 'run' : 'cancel', 'cleanup', nc ? 'cleanupNC' : 'cleanupPlain')], function (o) {
                  o.movingSignals = [{ edge: 'e2', tok: 'state' }]; o.codeHighlight.lines = nc ? [7, 8] : [7, 8];
                  if (!nc) { o.skipped = [{ whatKey: M(m, 'sk.cleanup.what'), whyKey: M(m, 'sk.cleanup.why') }]; o.callouts = [{ kind: 'pitfall', textKey: M(m, 'co.cleanupPlain') }]; }
                  else o.callouts = [{ kind: 'mechanism', textKey: M(m, 'co.cleanupNC') }];
                }));
              t += nc ? 50 : 0;
            }
            var endKey = s.mode === 'timeout' ? 'endTimeout' : (s.mode === 'timeoutNull' ? 'endNull' : 'endCancelled');
            jobState = J('cancelled');
            out.push(mk('end', 'mechanism', endKey, t, ['job', 'caller'], ns(jobState, K + 'st.done', s.fin === 'none' ? K + 'st.idle' : K + 'st.done'),
              [ev(t, s.mode === 'timeout' ? 'exception' : 'cancel', 'job', endKey)], function (o) {
                o.codeHighlight.lines = [10]; o.changes = [{ op: 'remove', textKey: M(m, 'ch.' + endKey) }];
                if (s.mode !== 'cancel') o.callouts = [{ kind: 'source', textKey: M(m, 'co.timeout') }];
              }));
          }
        }
      }
      if (!thrown) {
        // thân hàm chạy hết (mã không hợp tác, hoặc nuốt hủy, hoặc không bị hủy)
        var cancelledEnd = requested; jobState = cancelledEnd ? J('cancelled') : J('completed');
        var k2 = cancelledEnd ? (s.swallow ? 'endSwallowed' : 'endIgnored') : 'endOk';
        out.push(mk('end', cancelledEnd ? 'pitfall' : 'mechanism', k2, t, ['job'], ns(jobState, K + 'st.done'), [ev(t, 'complete', 'job', k2)], function (o) {
          o.codeHighlight.lines = [10];
          if (cancelledEnd) { o.skipped = [{ whatKey: M(m, 'sk.stop.what'), whyKey: M(m, 'sk.stop.why') }]; o.callouts = [{ kind: 'pitfall', textKey: M(m, 'co.nocoop') }]; }
        }));
      }
      return out;
    }
    var sel = function (id, action, vals, key) {
      return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: action, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) };
    };
    ADE.registerModel('coroutines.cancel', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'cancel',
      simplificationKeys: [M(m, 'simp.1'), M(m, 'simp.2'), K + 'simp.time'], controlsHintKey: M(m, 'ctl.hint'),
      controls: [
        sel('mode', 'mode', ['cancel', 'timeout', 'timeoutNull']),
        { id: 'coop', type: 'toggle', labelKey: M(m, 'ctl.coop'), get: function (s) { return s.coop; }, action: 'coop' },
        { id: 'at', type: 'select', labelKey: M(m, 'ctl.at'), get: function (s) { return s.at; }, action: 'at', options: [1, 2, 3, 4].map(function (v) { return { value: v, labelKey: M(m, 'ctl.at.n'), params: { n: v } }; }) },
        { id: 'swallow', type: 'toggle', labelKey: M(m, 'ctl.swallow'), get: function (s) { return s.swallow; }, action: 'swallow' },
        sel('fin', 'fin', ['none', 'plain', 'nc'])
      ],
      init: function () { return { mode: 'cancel', coop: true, at: 2, swallow: false, fin: 'none' }; },
      act: function (s, a, v) {
        var n = { mode: s.mode, coop: s.coop, at: s.at, swallow: s.swallow, fin: s.fin };
        if (a === 'coop' || a === 'swallow') n[a] = !!v; else if (a === 'at') n.at = Math.max(1, Math.min(4, v | 0)); else n[a] = v;
        return n;
      },
      steps: steps,
      selfChecks: [
        { name: 'hợp tác: hủy giữa đơn vị 2 → dừng sau đơn vị 2 (t=200), job cancelled', run: function () {
          var st = ADE.models['coroutines.cancel'].steps({ mode: 'cancel', coop: true, at: 2, swallow: false, fin: 'none' }), l = st[st.length - 1];
          return l.metrics.time === 200 && l.nodeStates.job === 'job.cancelled' && l.metrics.units === 2;
        } },
        { name: 'không hợp tác: chạy hết 5 đơn vị, job vẫn cancelled', run: function () {
          var st = ADE.models['coroutines.cancel'].steps({ mode: 'cancel', coop: false, at: 2, swallow: false, fin: 'none' }), l = st[st.length - 1];
          return l.metrics.time === 500 && l.metrics.units === 5 && l.nodeStates.job === 'job.cancelled';
        } },
        { name: 'nuốt CancellationException: chạy hết, không dừng', run: function () {
          var st = ADE.models['coroutines.cancel'].steps({ mode: 'cancel', coop: true, at: 2, swallow: true, fin: 'none' }), l = st[st.length - 1];
          return l.metrics.units === 5 && l.logEvents[0].detailKey.indexOf('endSwallowed') > 0;
        } },
        { name: 'timeout 250 ms + mã hợp tác: dừng ở 300 ms', run: function () {
          var st = ADE.models['coroutines.cancel'].steps({ mode: 'timeout', coop: true, at: 2, swallow: false, fin: 'none' }), l = st[st.length - 1];
          return l.metrics.time === 300 && l.logEvents[0].kind === 'exception';
        } },
        { name: 'finally: cleanup thường bị hủy, NonCancellable chạy xong', run: function () {
          var a = ADE.models['coroutines.cancel'].steps({ mode: 'cancel', coop: true, at: 2, swallow: false, fin: 'plain' }), b = ADE.models['coroutines.cancel'].steps({ mode: 'cancel', coop: true, at: 2, swallow: false, fin: 'nc' });
          var ca = a.filter(function (x) { return x.id === 'cleanup'; })[0], cb = b.filter(function (x) { return x.id === 'cleanup'; })[0];
          return ca.logEvents[0].kind === 'cancel' && cb.logEvents[0].kind === 'run' && cb.logEvents[0].t === 250;
        } }
      ]
    });
  })();

  /* ================= A6: exception, supervision, CoroutineExceptionHandler ================= */
  (function () {
    var m = 'exception';
    /* Quy tắc (nguồn: exception-handling; mô hình giản lược, nhãn simplified):
       - launch coi exception là uncaught; async giữ exception trong Deferred và đưa ra khi await.
       - Với Job thường (coroutineScope): lỗi của con lan lên cha, cha và các con khác bị hủy; handler đặt ở coroutine CON không có tác dụng
         vì lỗi được đẩy lên cha; handler ở root (trong context của scope) nhận lỗi uncaught cuối cùng; coroutineScope ném lại lỗi cho nơi gọi.
       - supervisorScope: lỗi con không lan lên cha, không hủy con khác. Con launch xử lý lỗi bằng handler (của nó hoặc thừa kế từ context);
         con async chỉ đưa lỗi ra khi await.
       - CoroutineExceptionHandler không thể phục hồi: coroutine đã hoàn tất với exception khi handler được gọi. */
    function outcome(c) {
      var sup = c.scope === 'supervisor', fail = c.who, other = fail === 'c1' ? 'c2' : 'c1';
      var st = { root: 'job.waiting', c1: 'job.active', c2: 'job.active' }, ev = [], del = [], notes = [];
      st[fail] = 'job.failed';
      ev.push({ kind: 'exception', subject: fail, key: c.builder === 'async' ? 'throwAsync' : 'throwLaunch' });
      if (!sup) {
        st.root = 'job.failed'; st[other] = 'job.cancelled';
        ev.push({ kind: 'exception', subject: 'root', key: 'toParent' }, { kind: 'cancel', subject: other, key: 'cancelSibling' });
        if (c.builder === 'async' && c.handling === 'await') { del.push('caughtAwait'); notes.push('scopeStillFails'); }
        if (c.handling === 'scope') del.push('caughtScope');
        else if (c.ceh === 'root') del.push('handler');
        else { del.push('uncaught'); if (c.ceh === 'child') notes.push('childIgnored'); }
      } else {
        st.root = 'job.waiting';
        if (c.builder === 'launch') {
          if (c.ceh === 'child' || c.ceh === 'root') del.push('handler'); else del.push('uncaught');
          if (c.handling === 'scope') notes.push('scopeNoThrow');
        } else {
          if (c.handling === 'await') del.push('caughtAwait'); else { del.push('held'); notes.push('heldNote'); }
        }
      }
      // handler được chọn nhưng không có tác dụng ở cấu hình này: nói rõ lý do thay vì im lặng
      if (c.ceh !== 'none' && !sup && c.handling === 'scope') notes.push('cehIgnoredScope');
      if (c.ceh !== 'none' && sup && c.builder === 'async') notes.push('cehIgnoredAsync');
      return { states: st, events: ev, delivery: del, notes: notes, siblingAlive: sup };
    }
    function steps(s) {
      var o = outcome(s), out = [], P = { builder: s.builder, who: s.who === 'c1' ? 'child-1' : 'child-2', other: s.who === 'c1' ? 'child-2' : 'child-1' };
      var nsOf = function (st, sink) { return { root: st.root, c1: st.c1, c2: st.c2, sink: sink || K + 'st.idle' }; };
      var base = { root: 'job.waiting', c1: 'job.active', c2: 'job.active' };
      out.push(step({ id: 'setup', type: 'scenario', titleKey: M(m, 's.setup.title'), explainKey: s.scope === 'supervisor' ? M(m, 's.setup.explainSup') : M(m, 's.setup.explain'), params: P, activeNodes: ['root', 'c1', 'c2'], nodeStates: nsOf(base),
        codeHighlight: { snippet: 'exception', lines: s.scope === 'supervisor' ? [1, 2, 3] : [1, 2, 3] }, callouts: [{ kind: 'try', textKey: M(m, 'co.try') }],
        metrics: { state: M(m, 'val.ok') },
        logEvents: [{ t: 0, kind: 'launch', subject: 'c1', detailKey: M(m, 'ev.launch'), params: P }, { t: 0, kind: 'launch', subject: 'c2', detailKey: M(m, 'ev.launch'), params: P }] }));
      var cur = { root: 'job.waiting', c1: 'job.active', c2: 'job.active' };
      cur[s.who] = 'job.failed';
      out.push(step({ id: 'throw', type: 'mechanism', titleKey: M(m, 's.throw.title'), explainKey: s.builder === 'async' ? M(m, 's.throw.explainAsync') : M(m, 's.throw.explainLaunch'), params: P, activeNodes: [s.who], nodeStates: nsOf(cur),
        codeHighlight: { snippet: 'exception', lines: [s.who === 'c1' ? 2 : 3] }, metrics: { state: M(m, 'val.failing') },
        logEvents: [{ t: 10, kind: 'exception', subject: s.who, detailKey: M(m, 'ev.' + o.events[0].key), params: P }] }));
      if (s.scope === 'coroutine') {
        out.push(step({ id: 'propagate', type: 'pitfall', titleKey: M(m, 's.propagate.title'), explainKey: M(m, 's.propagate.explain'), params: P, activeNodes: ['root', s.who === 'c1' ? 'c2' : 'c1'], movingSignals: [{ edge: s.who === 'c1' ? 'e1' : 'e2', tok: 'error' }],
          nodeStates: nsOf(o.states), metrics: { state: M(m, 'val.failed') },
          changes: [{ op: 'remove', textKey: M(m, 'ch.sibling'), params: P }, { op: 'set', textKey: M(m, 'ch.parent') }],
          callouts: [{ kind: 'source', textKey: M(m, 'co.structured') }],
          logEvents: [{ t: 20, kind: 'exception', subject: 'root', detailKey: M(m, 'ev.toParent'), params: P }, { t: 20, kind: 'cancel', subject: s.who === 'c1' ? 'c2' : 'c1', detailKey: M(m, 'ev.cancelSibling'), params: P }] }));
      } else {
        out.push(step({ id: 'contain', type: 'mechanism', titleKey: M(m, 's.contain.title'), explainKey: M(m, 's.contain.explain'), params: P, activeNodes: ['root'], nodeStates: nsOf(o.states), metrics: { state: M(m, 'val.contained') },
          skipped: [{ whatKey: M(m, 'sk.propagate.what'), whyKey: M(m, 'sk.propagate.why') }], changes: [{ op: 'skip', textKey: M(m, 'ch.noPropagate'), params: P }],
          callouts: [{ kind: 'mechanism', textKey: M(m, 'co.supervisor') }],
          logEvents: [{ t: 20, kind: 'launch', subject: 'root', detailKey: M(m, 'ev.contained'), params: P }] }));
      }
      var sinkKey = o.delivery.indexOf('uncaught') >= 0 ? K + 'st.uncaught' : (o.delivery.indexOf('handler') >= 0 ? K + 'st.handled' : (o.delivery.indexOf('held') >= 0 ? K + 'st.held' : K + 'st.caught'));
      o.delivery.forEach(function (d, i) {
        out.push(step({ id: 'deliver' + i, type: d === 'uncaught' ? 'pitfall' : 'mechanism', titleKey: M(m, 's.deliver.' + d + '.title'), explainKey: M(m, 's.deliver.' + d + '.explain'), params: P, activeNodes: ['sink', 'root'], movingSignals: [{ edge: 'e3', tok: 'error' }],
          nodeStates: nsOf(o.states, sinkKey), metrics: { state: M(m, d === 'held' ? 'val.held' : 'val.delivered') }, codeHighlight: { snippet: 'exception', lines: d === 'caughtAwait' ? [5] : [4, 6] },
          callouts: d === 'handler' ? [{ kind: 'pitfall', textKey: M(m, 'co.nrecover') }] : [],
          logEvents: [{ t: 30 + i * 10, kind: d === 'held' ? 'suspend' : (d.indexOf('caught') === 0 ? 'complete' : 'exception'), subject: d === 'caughtAwait' ? s.who : 'sink', detailKey: M(m, 'ev.deliver.' + d), params: P }] }));
      });
      o.notes.forEach(function (n, i) {
        out.push(step({ id: 'note' + i, type: 'pitfall', titleKey: M(m, 's.note.' + n + '.title'), explainKey: M(m, 's.note.' + n + '.explain'), params: P, activeNodes: ['root'], nodeStates: nsOf(o.states, sinkKey), metrics: { state: M(m, 'val.delivered') },
          logEvents: [{ t: 50 + i * 10, kind: 'complete', subject: 'root', detailKey: M(m, 'ev.note.' + n), params: P }] }));
      });
      return out;
    }
    var S = function (id, action, vals) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: action, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
    ADE.registerModel('coroutines.exception', {
      kind: 'discrete', titleKey: M(m, 'title'), overviewKey: M(m, 'overview'), wrapupKey: M(m, 'wrapup'), codeId: 'exception',
      simplificationKeys: [M(m, 'simp.1'), M(m, 'simp.2')], controlsHintKey: M(m, 'ctl.hint'),
      controls: [S('builder', 'builder', ['launch', 'async']), S('scope', 'scope', ['coroutine', 'supervisor']), S('ceh', 'ceh', ['none', 'root', 'child']), S('handling', 'handling', ['none', 'scope', 'await']), S('who', 'who', ['c1', 'c2'])],
      init: function () { return { builder: 'launch', scope: 'coroutine', ceh: 'none', handling: 'none', who: 'c1' }; },
      act: function (s, a, v) { var n = {}; for (var k in s) n[k] = s[k]; n[a] = v; return n; },
      steps: steps,
      selfChecks: [
        { name: 'coroutineScope + launch: handler ở con không có tác dụng (uncaught), con kia bị hủy', run: function () {
          var o = outcome({ builder: 'launch', scope: 'coroutine', ceh: 'child', handling: 'none', who: 'c1' });
          return o.delivery[0] === 'uncaught' && o.states.c2 === 'job.cancelled' && o.states.root === 'job.failed' && o.notes.indexOf('childIgnored') >= 0;
        } },
        { name: 'coroutineScope + handler ở root nhận lỗi', run: function () { var o = outcome({ builder: 'launch', scope: 'coroutine', ceh: 'root', handling: 'none', who: 'c2' }); return o.delivery[0] === 'handler' && o.states.c1 === 'job.cancelled'; } },
        { name: 'supervisorScope: con kia sống, root không failed', run: function () { var o = outcome({ builder: 'launch', scope: 'supervisor', ceh: 'child', handling: 'none', who: 'c1' }); return o.states.root === 'job.waiting' && o.states.c2 === 'job.active' && o.delivery[0] === 'handler'; } },
        { name: 'async + supervisor + không await: lỗi bị giữ trong Deferred; có await thì bắt được', run: function () {
          var a = outcome({ builder: 'async', scope: 'supervisor', ceh: 'none', handling: 'none', who: 'c1' }), b = outcome({ builder: 'async', scope: 'supervisor', ceh: 'none', handling: 'await', who: 'c1' });
          return a.delivery[0] === 'held' && b.delivery[0] === 'caughtAwait';
        } },
        { name: 'async + coroutineScope + try quanh await: bắt được nhưng scope vẫn fail', run: function () { var o = outcome({ builder: 'async', scope: 'coroutine', ceh: 'none', handling: 'await', who: 'c1' }); return o.delivery.indexOf('caughtAwait') >= 0 && o.states.root === 'job.failed' && o.notes.indexOf('scopeStillFails') >= 0; } }
      ]
    });
  })();
})();
