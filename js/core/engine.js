/* engine.js — SimEngine: ba loại model (rời rạc, liên tục, tính toán).
   Model là hàm thuần, KHÔNG chạm DOM, KHÔNG chứa câu chữ: chỉ phát message key kèm tham số.
   Mô hình rời rạc (master 6.2): model.steps(state) trả về danh sách bước tính trước:
     { id, type, titleKey, explainKey, params, activeNodes, movingSignals, stateBefore, stateAfter, affected,
       skipped:[{whatKey, whyKey}], changes:[{op:'add'|'set'|'remove'|'skip', textKey, params}],
       callouts:[{kind:'mechanism'|'pitfall'|'android'|'source'|'try', textKey, params}],
       metrics:{id:value}, codeHighlight:{snippet, lines}, typing:{node, code},
       logEvents:[{t, kind, subject, to?, scope?, detailKey, params}], simplificationKeys }
   Khi người đọc tác động: session.act(action, payload) gọi model.act(state, ...) rồi TÍNH LẠI các bước từ state mới. */
(function () {
  'use strict';
  var ADE = window.ADE = window.ADE || {};

  function Emitter() { this._l = []; }
  Emitter.prototype.on = function (fn) { var self = this; this._l.push(fn); return function () { var i = self._l.indexOf(fn); if (i >= 0) self._l.splice(i, 1); }; };
  Emitter.prototype.emit = function (type, extra) { var e = { type: type, extra: extra }; this._l.slice().forEach(function (f) { f(e); }); };

  /* ---------- rời rạc ---------- */
  function DiscreteSession(def, params) {
    Emitter.call(this);
    this.def = def; this.kind = 'discrete'; this.params = params || {};
    this.state = def.init(this.params);
    this.pos = 0;            // 0 = tổng quan, 1..N = bước, N+1 = tổng kết
    this.maxPos = 0;
    this.speed = 1;
    this.playing = false;
    this._timer = null;
    this.recompute();
  }
  DiscreteSession.prototype = Object.create(Emitter.prototype);
  DiscreteSession.prototype.recompute = function () {
    this.steps = this.def.steps(this.state) || [];
    this.N = this.steps.length;
    if (this.pos > this.N + 1) this.pos = this.N + 1;
    if (this.maxPos > this.N + 1) this.maxPos = this.N + 1;
  };
  DiscreteSession.prototype.step = function () { return this.pos >= 1 && this.pos <= this.N ? this.steps[this.pos - 1] : null; };
  DiscreteSession.prototype.goto = function (p) {
    p = Math.max(0, Math.min(this.N + 1, p | 0));
    if (p === this.pos) return;
    this.pos = p;
    if (p > this.maxPos) this.maxPos = p;
    if (p >= this.N + 1) this.pause();
    this.emit('pos');
  };
  DiscreteSession.prototype.next = function () { this.goto(this.pos + 1); };
  DiscreteSession.prototype.prev = function () { this.goto(this.pos - 1); };
  DiscreteSession.prototype.reset = function () {
    this.pause();
    this.state = this.def.init(this.params);
    this.pos = 0; this.maxPos = 0;
    this.recompute();
    this.emit('reset');
  };
  DiscreteSession.prototype.act = function (action, payload) {
    this.state = this.def.act(this.state, action, payload);
    this.recompute();
    this.emit('act', { action: action });
  };
  DiscreteSession.prototype.replayStep = function () { this.emit('replay'); };
  DiscreteSession.prototype.setSpeed = function (s) { this.speed = s; if (this.playing) { this._clear(); this._schedule(); } this.emit('speed'); };
  DiscreteSession.prototype._clear = function () { if (this._timer) { clearTimeout(this._timer); this._timer = null; } };
  DiscreteSession.prototype._schedule = function () {
    var self = this;
    this._timer = setTimeout(function () {
      if (!self.playing) return;
      self.next();
      if (self.playing) self._schedule();
    }, 1800 / self.speed);
  };
  // Giảm chuyển động: Play chạy TỪNG BƯỚC (mỗi lần bấm một bước), không tự chạy.
  DiscreteSession.prototype.play = function () {
    if (ADE.motionReduced()) { if (this.pos > this.N) this.goto(0); this.next(); return; }
    if (this.pos > this.N) this.goto(0);
    this.playing = true; this._schedule(); this.emit('play');
  };
  DiscreteSession.prototype.pause = function () { var was = this.playing; this.playing = false; this._clear(); if (was) this.emit('pause'); };
  DiscreteSession.prototype.toggle = function () { if (this.playing) this.pause(); else this.play(); };
  DiscreteSession.prototype.destroy = function () { this.pause(); this._l = []; };

  // Sự kiện nhật ký cộng dồn tới vị trí hiện tại; mỗi sự kiện kèm chỉ số bước (1-based).
  DiscreteSession.prototype.eventsUpTo = function (pos) {
    var out = [], upto = Math.min(pos == null ? this.pos : pos, this.N);
    for (var i = 0; i < upto; i++) {
      (this.steps[i].logEvents || []).forEach(function (e) { out.push({ e: e, step: i + 1 }); });
    }
    return out;
  };
  // Dải chỉ số điền dần: giá trị mới nhất của từng metric tới bước hiện tại; chưa có → undefined ("?").
  DiscreteSession.prototype.metricsAt = function (pos) {
    var out = {}, upto = Math.min(pos == null ? this.pos : pos, this.N);
    for (var i = 0; i < upto; i++) { var m = this.steps[i].metrics; if (m) Object.keys(m).forEach(function (k) { out[k] = m[k]; }); }
    return out;
  };

  /* ---------- liên tục ---------- */
  // def: init(params)->state; advance(state, dtMs)->state; sample(state)->{t, values, done}; act(state, action, payload)->state
  function ContinuousSession(def, params) {
    Emitter.call(this);
    this.def = def; this.kind = 'continuous'; this.params = params || {};
    this.frameMs = 16;          // khoảng frame minh hoạ, người đọc chọn được (không hard-code là quy luật)
    this.speed = 1; this.playing = false;
    this._raf = 0; this._acc = 0; this._last = 0;
    this.restart(true);
  }
  ContinuousSession.prototype = Object.create(Emitter.prototype);
  ContinuousSession.prototype.restart = function (silent) {
    this.pause();
    this.state = this.def.init(this.params);
    this.samples = [this.def.sample(this.state)];
    this.frame = 0;
    if (!silent) this.emit('reset');
  };
  ContinuousSession.prototype.reset = function () { this.restart(); };
  ContinuousSession.prototype.last = function () { return this.samples[this.samples.length - 1]; };
  ContinuousSession.prototype.stepFrame = function () {
    this.state = this.def.advance(this.state, this.frameMs);
    this.samples.push(this.def.sample(this.state));
    this.frame++;
    this.emit('frame');
  };
  ContinuousSession.prototype.act = function (action, payload) {
    this.state = this.def.act(this.state, action, payload);
    this.emit('act', { action: action });
  };
  ContinuousSession.prototype.setFrameMs = function (ms) { this.frameMs = ms; this.emit('speed'); };
  ContinuousSession.prototype.setSpeed = function (s) { this.speed = s; this.emit('speed'); };
  ContinuousSession.prototype.play = function () {
    if (ADE.motionReduced()) { this.stepFrame(); return; }
    var self = this;
    if (this.playing) return;
    this.playing = true; this._last = 0; this._acc = 0;
    var loop = function (now) {
      if (!self.playing) return;
      if (self._last) {
        self._acc += (now - self._last) * self.speed;
        var guard = 0;
        while (self._acc >= self.frameMs && guard++ < 240) { self._acc -= self.frameMs; self.stepFrame(); }
        if (self.last().done) { self.pause(); return; }
      }
      self._last = now;
      self._raf = requestAnimationFrame(loop);
    };
    this._raf = requestAnimationFrame(loop);
    this.emit('play');
  };
  ContinuousSession.prototype.pause = function () { var was = this.playing; this.playing = false; if (this._raf) cancelAnimationFrame(this._raf); this._raf = 0; if (was) this.emit('pause'); };
  ContinuousSession.prototype.toggle = function () { if (this.playing) this.pause(); else this.play(); };
  ContinuousSession.prototype.destroy = function () { this.pause(); this._l = []; };

  /* ---------- tính toán ---------- */
  // def.compute(inputs)->{outputs, assumptionKeys, sourceIds}; def.checks:[{name, inputs, expect:function(result)->bool}]
  function run(modelOrId, params) {
    var def = typeof modelOrId === 'string' ? ADE.models[modelOrId] : modelOrId;
    if (!def) throw new Error('Không có model: ' + modelOrId);
    if (def.kind === 'discrete') return new DiscreteSession(def, params);
    if (def.kind === 'continuous') return new ContinuousSession(def, params);
    throw new Error('Model tính toán không có session: ' + def.id);
  }

  // Gom mọi message key mà một bước phát ra (cho dev/report kiểm tra thiếu khoá).
  function collectKeys(step) {
    var out = [];
    var add = function (k) { if (k) out.push(k); };
    add(step.titleKey); add(step.explainKey);
    (step.simplificationKeys || []).forEach(add);
    (step.skipped || []).forEach(function (s) { add(s.whatKey); add(s.whyKey); });
    (step.changes || []).forEach(function (c) { add(c.textKey); });
    (step.callouts || []).forEach(function (c) { add(c.textKey); });
    (step.logEvents || []).forEach(function (e) { add(e.detailKey); });
    ['stateBefore', 'stateAfter'].forEach(function (f) { (step[f] || []).forEach(function (s) { add(s.labelKey); add(s.valueKey); }); });
    return out;
  }
  // Mô hình không được phát câu chữ: mọi trường *Key phải trông như khoá (có dấu chấm, không khoảng trắng).
  function looksLikeKey(s) { return typeof s === 'string' && /^[A-Za-z0-9_.\-]+$/.test(s) && s.indexOf('.') > 0; }

  /* ---------- kiểm chứng ---------- */
  var checks = [];
  ADE.registerCheck = function (id, fn) { checks.push({ id: id, fn: fn }); };
  function runChecks() {
    var results = [];
    checks.forEach(function (c) {
      try { var r = c.fn(); results.push({ id: c.id, pass: !!(r === true || (r && r.pass)), detail: r && r.detail ? r.detail : '' }); }
      catch (e) { results.push({ id: c.id, pass: false, detail: String(e) }); }
    });
    Object.keys(ADE.models).forEach(function (id) {
      var def = ADE.models[id];
      (def.checks || []).forEach(function (c) {
        try {
          var r = def.compute(c.inputs);
          results.push({ id: id + ' · ' + c.name, pass: !!c.expect(r), detail: JSON.stringify(r.outputs || r).slice(0, 120) });
        } catch (e) { results.push({ id: id + ' · ' + c.name, pass: false, detail: String(e) }); }
      });
      (def.selfChecks || []).forEach(function (c) {
        try { var r = c.run(); results.push({ id: id + ' · ' + c.name, pass: !!(r === true || (r && r.pass)), detail: r && r.detail ? r.detail : '' }); }
        catch (e) { results.push({ id: id + ' · ' + c.name, pass: false, detail: String(e) }); }
      });
    });
    return results;
  }

  ADE.engine = { create: run, collectKeys: collectKeys, looksLikeKey: looksLikeKey, runChecks: runChecks, Discrete: DiscreteSession, Continuous: ContinuousSession };

  // Kiểm chứng của chính engine, bằng model giả (không đăng ký vào registry).
  ADE.registerCheck('engine · rời rạc: tính lại bước khi act, giữ chỉ số', function () {
    var def = {
      kind: 'discrete',
      init: function () { return { n: 2 }; },
      steps: function (s) { var a = []; for (var i = 0; i < s.n; i++) a.push({ id: 's' + i, titleKey: 'x.t', explainKey: 'x.e', logEvents: [{ t: i, kind: 'act', subject: 'a', detailKey: 'x.d' }] }); return a; },
      act: function (s, a, p) { return { n: p }; }
    };
    var s = new DiscreteSession(def);
    s.goto(2);
    s.act('set', 4);
    var ok1 = s.N === 4 && s.pos === 2 && s.eventsUpTo().length === 2;
    s.goto(5); s.act('set', 1);
    var ok2 = s.N === 1 && s.pos === 2;      // kẹp vào "tổng kết" (N+1)
    s.reset();
    var ok3 = s.N === 2 && s.pos === 0;
    s.destroy();
    return { pass: ok1 && ok2 && ok3, detail: [ok1, ok2, ok3].join('/') };
  });
  ADE.registerCheck('engine · liên tục: step frame tích luỹ thời gian', function () {
    var def = {
      kind: 'continuous',
      init: function () { return { t: 0, v: 0 }; },
      advance: function (s, dt) { return { t: s.t + dt, v: s.v + dt * 0.01 }; },
      sample: function (s) { return { t: s.t, values: { v: s.v }, done: s.t >= 100 }; },
      act: function (s) { return s; }
    };
    var s = new ContinuousSession(def);
    s.setFrameMs(10);
    for (var i = 0; i < 5; i++) s.stepFrame();
    var ok = Math.abs(s.last().t - 50) < 1e-9 && s.samples.length === 6;
    s.restart();
    return { pass: ok && s.last().t === 0, detail: 't=50' };
  });
})();
