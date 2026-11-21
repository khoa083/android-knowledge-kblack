/* Tiện ích chung cho các model của track coroutines: bộ lập lịch minh họa và dựng bước từ sự kiện.
   Thuần, không DOM, không câu chữ (chỉ message key). Mọi mô hình ở đây là MÔ HÌNH GIẢNG DẠY (nhãn simplified):
   - Hàng đợi FIFO và thời gian là minh họa, không phải benchmark, không mô tả scheduler thật.
   - Số luồng của dispatcher là tham số minh họa, không phải số thật của Dispatchers.IO/Default. */
(function () {
  'use strict';
  var C = ADE.coro = {};
  var K = C.K = 'track.coroutines.';

  C.step = function (o) {
    o.type = o.type || 'mechanism';
    o.params = o.params || {};
    o.activeNodes = o.activeNodes || [];
    o.movingSignals = o.movingSignals || [];
    return o;
  };
  C.clone = function (x) { return JSON.parse(JSON.stringify(x)); };

  /* ---------- bộ lập lịch minh họa ---------- */
  // tasks: [{id, at?, segs:[{k:'run'|'block'|'delay', ms}]}]; nThreads: số luồng của dispatcher (minh họa)
  // Một task giữ luồng qua các đoạn run/block liên tiếp, và chỉ nhả luồng khi gặp 'delay' (suspend) hoặc khi xong.
  // 'block' = chặn luồng (kiểu Thread.sleep): luồng bận nên task khác không chạy được.
  C.simulate = function (tasks, nThreads) {
    var ev = [], th = [], i;
    for (i = 0; i < nThreads; i++) th.push({ until: 0, task: null });
    var S = tasks.map(function (tk) { return { tk: tk, i: 0, state: 'new', at: tk.at || 0, thread: -1, since: 0, started: false }; });
    var t = 0;
    for (var guard = 0; guard < 600; guard++) {
      // 1) đoạn đang chạy đã xong tại t
      th.forEach(function (x, j) {
        if (!x.task || x.until > t) return;
        var s = x.task; s.i++;
        if (s.i >= s.tk.segs.length) { ev.push({ t: t, kind: 'complete', task: s.tk.id, thread: j }); x.task = null; s.state = 'done'; return; }
        var seg = s.tk.segs[s.i];
        if (seg.k === 'delay') { ev.push({ t: t, kind: 'suspend', task: s.tk.id, thread: j, ms: seg.ms }); x.task = null; s.state = 'wait'; s.at = t + seg.ms; }
        else { x.until = t + seg.ms; if (seg.k === 'block') ev.push({ t: t, kind: 'block', task: s.tk.id, thread: j, ms: seg.ms }); }
      });
      // 2) task mới đến, task hết delay
      S.forEach(function (s) {
        if (s.state === 'new' && s.at <= t) { s.state = 'ready'; s.since = t; ev.push({ t: t, kind: 'launch', task: s.tk.id }); }
        else if (s.state === 'wait' && s.at <= t) {
          // hết delay: bỏ qua đoạn delay vừa xong rồi xếp hàng cho đoạn kế tiếp
          s.i++;
          if (s.i >= s.tk.segs.length) { s.state = 'done'; ev.push({ t: t, kind: 'complete', task: s.tk.id, thread: -1 }); }
          else if (s.tk.segs[s.i].k === 'delay') { s.at = t + s.tk.segs[s.i].ms; ev.push({ t: t, kind: 'suspend', task: s.tk.id, thread: -1, ms: s.tk.segs[s.i].ms }); }
          else { s.state = 'ready'; s.since = t; }
        }
      });
      // 3) gán luồng rảnh cho task sẵn sàng (FIFO theo thời điểm sẵn sàng rồi thứ tự khai báo)
      var ready = S.filter(function (s) { return s.state === 'ready'; }).sort(function (a, b) { return a.since - b.since; });
      ready.forEach(function (s) {
        for (var j = 0; j < th.length; j++) {
          if (th[j].task) continue;
          var seg = s.tk.segs[s.i];
          th[j].task = s; th[j].until = t + seg.ms; s.state = 'run'; s.thread = j;
          ev.push({ t: t, kind: 'resume', task: s.tk.id, thread: j, first: !s.started, waited: t - s.since });
          s.started = true;
          if (seg.k === 'block') ev.push({ t: t, kind: 'block', task: s.tk.id, thread: j, ms: seg.ms });
          break;
        }
      });
      // 4) nhảy tới thời điểm kế tiếp
      var next = Infinity;
      th.forEach(function (x) { if (x.task && x.until > t) next = Math.min(next, x.until); });
      S.forEach(function (s) { if ((s.state === 'new' || s.state === 'wait') && s.at > t) next = Math.min(next, s.at); });
      if (next === Infinity) break;
      t = next;
    }
    return ev;
  };

  // Dựng danh sách bước từ sự kiện của C.simulate. cfg: {tasks:[ids], threadNodes:['th0',...], threadsUsed:n, extra(stepIndex, ev)->{}}
  var KIND_KEY = { launch: 'launch', resume: 'resume', suspend: 'suspend', block: 'block', complete: 'complete' };
  C.schedSteps = function (events, cfg) {
    var ts = {}, ths = {}, steps = [], nT = cfg.threadsUsed;
    cfg.tasks.forEach(function (id) { ts[id] = null; });
    cfg.threadNodes.forEach(function (id, j) { ths[id] = j < nT ? K + 'st.free' : K + 'st.unused'; });
    var snapshot = function () {
      var o = {};
      cfg.tasks.forEach(function (id) { if (ts[id]) o[id] = ts[id]; });
      cfg.threadNodes.forEach(function (id) { o[id] = ths[id]; });
      return o;
    };
    var lastDone = 0;
    events.forEach(function (e, n) {
      var th = cfg.threadNodes[e.thread] || cfg.threadNodes[0], p = { task: String(e.task).toUpperCase(), thread: e.thread + 1, ms: e.ms, waited: e.waited, t: e.t };
      var kindKey, detailKey, titleKey, explainKey, active = [e.task], sig = [];
      if (e.kind === 'launch') { ts[e.task] = K + 'st.ready'; kindKey = 'launch'; titleKey = K + 'c.launch.title'; explainKey = K + 'c.launch.explain'; detailKey = K + 'c.ev.launch'; }
      else if (e.kind === 'resume') {
        ts[e.task] = K + 'st.running'; ths[th] = K + 'st.busy'; kindKey = 'resume'; active = [e.task, th];
        if (e.first) { titleKey = K + 'c.start.title'; explainKey = e.waited > 0 ? K + 'c.startWait.explain' : K + 'c.start.explain'; detailKey = e.waited > 0 ? K + 'c.ev.startWait' : K + 'c.ev.start'; }
        else { titleKey = K + 'c.resume.title'; explainKey = K + 'c.resume.explain'; detailKey = K + 'c.ev.resume'; }
      } else if (e.kind === 'suspend') { ts[e.task] = K + 'st.suspended'; if (e.thread >= 0) ths[th] = K + 'st.free'; kindKey = 'suspend'; titleKey = K + 'c.suspend.title'; explainKey = K + 'c.suspend.explain'; detailKey = K + 'c.ev.suspend'; active = [e.task, th]; }
      else if (e.kind === 'block') { ts[e.task] = K + 'st.blocking'; ths[th] = K + 'st.busy'; kindKey = 'block'; titleKey = K + 'c.block.title'; explainKey = K + 'c.block.explain'; detailKey = K + 'c.ev.block'; active = [e.task, th]; }
      else { ts[e.task] = K + 'st.done'; if (e.thread >= 0) ths[th] = K + 'st.free'; kindKey = 'complete'; titleKey = K + 'c.complete.title'; explainKey = K + 'c.complete.explain'; detailKey = K + 'c.ev.complete'; lastDone = e.t; active = [e.task]; }
      var st = C.step({
        id: 's' + n + '.' + e.kind + '.' + e.task, type: n === 0 ? 'scenario' : 'mechanism', titleKey: titleKey, explainKey: explainKey, params: p,
        activeNodes: active, movingSignals: sig, nodeStates: snapshot(),
        metrics: { time: e.t },
        logEvents: [{ t: e.t, kind: kindKey, subject: e.task, scope: K + 'thread.' + (e.thread != null && e.thread >= 0 ? 'th' + e.thread : 'none'), detailKey: detailKey, params: p }]
      });
      if (cfg.extra) cfg.extra(st, e, n);
      steps.push(st);
    });
    return steps;
  };
  // Tên "luồng" chỉ là ví dụ (scope trong nhật ký)
  C.threadScopeKeys = ['th0', 'th1', 'th2', 'th3', 'none'];

  /* ---------- kiểm chứng ---------- */
  ADE.registerCheck('coroutines · lập lịch: delay nhả luồng, block giữ luồng', function () {
    var mk = function (kind) { return [{ id: 'A', segs: [{ k: 'run', ms: 10 }, { k: kind, ms: 30 }, { k: 'run', ms: 10 }] }, { id: 'B', segs: [{ k: 'run', ms: 10 }] }]; };
    var done = function (ev, id) { return ev.filter(function (e) { return e.kind === 'complete' && e.task === id; })[0].t; };
    var d = C.simulate(mk('delay'), 1), b = C.simulate(mk('block'), 1);
    // delay: B chạy trong lúc A suspend → B xong sớm (t=20); block: B phải đợi A xong (t=60)
    return { pass: done(d, 'B') === 20 && done(b, 'B') === 60 && done(d, 'A') === 50 && done(b, 'A') === 50, detail: 'B(delay)=' + done(d, 'B') + ' B(block)=' + done(b, 'B') };
  });
})();
