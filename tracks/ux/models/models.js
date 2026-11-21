/* Model rời rạc track D (thuần, không DOM, không câu chữ). Mọi con số là MINH HỌA (simplified) trừ khi ghi nguồn.
   Ứng dụng mẫu "Hẹn Khám / ClinicBook" là hư cấu. */
(function () {
  'use strict';
  var K = 'track.ux.';
  var M = function (m, s) { return K + 'm.' + m + '.' + s; };
  function S(m, id, o) {
    o.id = id; o.type = o.type || 'mechanism'; o.titleKey = o.titleKey || M(m, 's.' + id + '.title'); o.explainKey = o.explainKey || M(m, 's.' + id + '.explain');
    o.params = o.params || {}; o.activeNodes = o.activeNodes || []; o.movingSignals = o.movingSignals || [];
    (o.logEvents || []).forEach(function (e) { if (!e.detailKey) e.detailKey = M(m, 'ev.' + id); if (!e.params) e.params = o.params; });
    return o;
  }
  function reg(m, def) {
    def.kind = 'discrete'; def.titleKey = M(m, 'title'); def.overviewKey = M(m, 'overview'); def.wrapupKey = M(m, 'wrapup');
    def.codeId = def.codeId || null; def.controlsHintKey = M(m, 'ctl.hint'); def.simplificationKeys = [M(m, 'simp.1')];
    ADE.registerModel('ux.' + m, def);
  }
  var sel = function (m, id, vals) { return { id: id, type: 'select', labelKey: M(m, 'ctl.' + id), get: function (s) { return s[id]; }, action: id, options: vals.map(function (v) { return { value: v, labelKey: M(m, 'ctl.' + id + '.' + v) }; }) }; };
  var tog = function (m, id) { return { id: id, type: 'toggle', labelKey: M(m, 'ctl.' + id), get: function (s) { return !!s[id]; }, action: id }; };
  var setter = function (keys) { return function (s, a, v) { var n = {}; keys.forEach(function (k) { n[k] = s[k]; }); if (keys.indexOf(a) >= 0) n[a] = typeof s[a] === 'boolean' ? !!v : v; return n; }; };

  /* ---------- khuôn "chọn tình huống → đoán → giải thích" ----------
     items: {id: correctAnswer}; guesses: danh sách đáp án. Bước: tình huống, đáp án của bạn (đúng/sai), giải thích (+ bước thêm qua cfg.extra). */
  function choice(m, items, guesses, cfg) {
    cfg = cfg || {};
    var ids = Object.keys(items);
    function steps(s) {
      var it = s.item, ok = (items[it] === s.guess) || (Array.isArray(items[it]) && items[it].indexOf(s.guess) >= 0), P = { guess: '' };
      var out = [
        S(m, 'situation', { type: 'scenario', titleKey: M(m, 'i.' + it + '.title'), explainKey: M(m, 'i.' + it + '.situation'), activeNodes: ['screen'],
          callouts: [{ kind: 'try', textKey: M(m, 'co.try') }], logEvents: [{ t: 0, kind: 'observe', subject: 'screen', detailKey: M(m, 'i.' + it + '.title') }] }),
        S(m, 'answer', { type: ok ? 'mechanism' : 'pitfall', titleKey: K + (ok ? 'c.right' : 'c.wrong'), explainKey: M(m, 'ctl.guess.' + s.guess), activeNodes: ['user'],
          movingSignals: [{ edge: 'e1', tok: 'signal' }], stateAfter: [{ labelKey: K + 'c.yours', valueKey: M(m, 'ctl.guess.' + s.guess) }, { labelKey: K + 'c.expected', valueKey: M(m, 'ctl.guess.' + (Array.isArray(items[it]) ? items[it][0] : items[it])) }],
          logEvents: [{ t: 1, kind: 'decide', subject: 'user', detailKey: M(m, 'ctl.guess.' + s.guess) }] }),
        S(m, 'why', { titleKey: K + 'c.why', explainKey: M(m, 'i.' + it + '.why'), activeNodes: ['design'], movingSignals: [{ edge: 'e2', tok: 'state' }],
          callouts: cfg.source ? [{ kind: 'source', textKey: M(m, 'co.source') }] : [], logEvents: [{ t: 2, kind: 'feedback', subject: 'design' }], detailKey: null })
      ];
      out[2].logEvents[0].detailKey = M(m, 'ev.why');
      if (cfg.extra) cfg.extra(out, s, ok);
      out[out.length - 1].metrics = { right: ok ? 1 : 0 };
      return out;
    }
    return { steps: steps, controls: [sel(m, 'item', ids), sel(m, 'guess', guesses)].concat(cfg.controls || []),
      init: function () { var o = { item: ids[0], guess: guesses[0] }; (cfg.initExtra || function () { })(o); return o; },
      act: setter(['item', 'guess'].concat(cfg.extraKeys || [])),
      selfChecks: [{ name: 'mỗi tình huống có ít nhất 3 bước; đáp án đúng cho kết quả "đúng"', run: function () {
        return ids.every(function (i) { var g = Array.isArray(items[i]) ? items[i][0] : items[i], st = steps(Object.assign({ item: i, guess: g }, cfg.base || {})); return st.length >= 3 && st[1].titleKey === K + 'c.right'; });
      } }] };
  }
  function regChoice(m, items, guesses, cfg) { var c = choice(m, items, guesses, cfg); reg(m, { controls: c.controls, init: c.init, act: c.act, steps: c.steps, selfChecks: c.selfChecks }); }

  /* D0: UX hay UI? (8 tình huống của Hẹn Khám) */
  regChoice('classify', { c1: 'ux', c2: 'ui', c3: 'both', c4: 'ux', c5: 'ui', c6: 'both', c7: 'ux', c8: 'ui' }, ['ux', 'ui', 'both'], { source: true });

  /* D0: Double Diamond (Design Council) — chọn pha; bật "vòng lặp" để quay lại đầu */
  (function () {
    var m = 'diamond', PH = ['discover', 'define', 'develop', 'deliver'];
    function steps(s) {
      var out = [S(m, 'phase', { type: 'scenario', titleKey: M(m, 'ph.' + s.phase + '.title'), explainKey: M(m, 'ph.' + s.phase + '.q'), activeNodes: [s.phase], logEvents: [{ t: 0, kind: 'observe', subject: s.phase, detailKey: M(m, 'ph.' + s.phase + '.title') }] }),
        S(m, 'methods', { explainKey: M(m, 'ph.' + s.phase + '.methods'), activeNodes: [s.phase], logEvents: [{ t: 1, kind: 'act', subject: s.phase }] }),
        S(m, 'output', { explainKey: M(m, 'ph.' + s.phase + '.output'), activeNodes: [s.phase], callouts: [{ kind: 'source', textKey: M(m, 'co.source') }], logEvents: [{ t: 2, kind: 'measure', subject: s.phase }] })];
      if (s.loop) out.push(S(m, 'loop', { type: 'experiment', activeNodes: ['discover', s.phase], movingSignals: [{ edge: 'back', tok: 'signal' }], logEvents: [{ t: 3, kind: 'recover', subject: 'discover' }] }));
      return out;
    }
    reg(m, { controls: [sel(m, 'phase', PH), tog(m, 'loop')], init: function () { return { phase: 'discover', loop: false }; }, act: setter(['phase', 'loop']), steps: steps,
      selfChecks: [{ name: 'mỗi pha có 3 bước; vòng lặp thêm 1 bước', run: function () { return PH.every(function (p) { return steps({ phase: p, loop: false }).length === 3 && steps({ phase: p, loop: true }).length === 4; }); } }] });
  })();

  /* D1: mô hình tư duy — công tắc "Lưu tự động" */
  regChoice('mental', { on: 'saved', off: 'lost' }, ['saved', 'lost', 'asked'], {
    extra: function (out, s) { out.push(S('mental', 'gap', { explainKey: M('mental', 'gap.' + s.item + '.' + s.guess), activeNodes: ['user', 'design'], logEvents: [{ t: 3, kind: 'observe', subject: 'design' }] })); }
  });

  /* D2: bảy giai đoạn hành động (Norman, DOET — author-framework) với công tắc lỗi thiết kế */
  var STAGES = ['goal', 'plan', 'specify', 'perform', 'perceive', 'interpret', 'compare'];
  var BREAK = { noSignifier: ['plan', 'specify'], noFeedback: ['perceive', 'interpret'], vague: ['interpret', 'compare'] };
  var U = ADE.uxStages = {};
  U.gulfs = function (s) {
    var exec = 0, evalg = 0;
    Object.keys(BREAK).forEach(function (f) { if (!s[f]) return; BREAK[f].forEach(function (st) { if (STAGES.indexOf(st) <= 3) exec++; else evalg++; }); });
    return { exec: exec, eval: evalg };
  };
  (function () {
    var m = 'stages';
    function steps(s) {
      var g = U.gulfs(s), out = [];
      STAGES.forEach(function (st, i) {
        var broken = Object.keys(BREAK).filter(function (f) { return s[f] && BREAK[f].indexOf(st) >= 0; });
        var o = S(m, st, { type: i === 0 ? 'scenario' : broken.length ? 'pitfall' : 'mechanism', explainKey: M(m, 's.' + st + (broken.length ? '.broken.' + broken[0] : '.explain')), activeNodes: [st],
          nodeStates: (function () { var ns = {}; STAGES.forEach(function (x, j) { if (j <= i) ns[x] = K + (Object.keys(BREAK).some(function (f) { return s[f] && BREAK[f].indexOf(x) >= 0; }) ? 'st.broken' : 'st.ok'); }); return ns; })(),
          logEvents: [{ t: i, kind: broken.length ? 'error' : (i <= 3 ? 'act' : 'observe'), subject: st, detailKey: M(m, broken.length ? 'ev.broken' : 'ev.ok') }] });
        if (broken.length) o.callouts = [{ kind: 'pitfall', textKey: M(m, 'co.' + broken[0]) }];
        if (i === 3) o.metrics = { exec: g.exec };
        if (i === 6) o.metrics = { exec: g.exec, eval: g.eval };
        out.push(o);
      });
      out[0].callouts = [{ kind: 'try', textKey: M(m, 'co.try') }];
      return out;
    }
    reg(m, { controls: [tog(m, 'noSignifier'), tog(m, 'noFeedback'), tog(m, 'vague')], init: function () { return { noSignifier: false, noFeedback: false, vague: false }; },
      act: setter(['noSignifier', 'noFeedback', 'vague']), steps: steps,
      selfChecks: [{ name: 'bỏ signifier mở rộng vực thực thi; bỏ feedback mở rộng vực đánh giá', run: function () { return U.gulfs({ noSignifier: true }).exec === 2 && U.gulfs({ noFeedback: true }).eval === 2 && U.gulfs({}).exec === 0; } }] });
  })();

  /* D3: phòng thí nghiệm lỗi — phân loại slip/mistake, chọn biện pháp; số lỗi trước/sau là MINH HỌA */
  var ERR = { e1: { type: 'slip', good: ['constraint', 'confirm'] }, e2: { type: 'mistake', good: ['plainLabel'] }, e3: { type: 'slip', good: ['forgiving'] },
    e4: { type: 'mistake', good: ['plainLabel', 'preview'] }, e5: { type: 'slip', good: ['undo'] }, e6: { type: 'mistake', good: ['preview'] } };
  var REMEDY = ['constraint', 'confirm', 'forgiving', 'plainLabel', 'preview', 'undo'];
  ADE.uxErrors = { ERR: ERR, after: function (item, remedy) { return ERR[item].good.indexOf(remedy) >= 0 ? 1 : 3; }, BEFORE: 4 };
  regChoice('errors', (function () { var o = {}; Object.keys(ERR).forEach(function (k) { o[k] = ERR[k].type; }); return o; })(), ['slip', 'mistake'], {
    source: true, controls: [sel('errors', 'remedy', REMEDY)], extraKeys: ['remedy'], initExtra: function (o) { o.remedy = 'constraint'; }, base: { remedy: 'constraint' },
    extra: function (out, s) {
      var after = ADE.uxErrors.after(s.item, s.remedy), good = after === 1;
      out.push(S('errors', 'remedy', { type: good ? 'mechanism' : 'pitfall', explainKey: M('errors', 'i.' + s.item + '.r.' + (good ? 'good' : 'weak')), params: { before: ADE.uxErrors.BEFORE, after: after },
        activeNodes: ['design', 'screen'], stateBefore: [{ labelKey: M('errors', 'st.errors'), value: String(ADE.uxErrors.BEFORE) }], stateAfter: [{ labelKey: M('errors', 'st.errors'), value: String(after) }],
        changes: [{ op: 'set', textKey: M('errors', 'ctl.remedy.' + s.remedy) }], callouts: [{ kind: 'mechanism', textKey: M('errors', 'co.illustrative') }],
        logEvents: [{ t: 3, kind: good ? 'recover' : 'error', subject: 'design', detailKey: M('errors', 'ctl.remedy.' + s.remedy) }] }));
      out[out.length - 1].metrics = { before: ADE.uxErrors.BEFORE, after: after };
    }
  });

  /* D5: phễu CREATE (Wendel — author-framework). Không có số liệu thật: mỗi giai đoạn chỉ là "thông" hoặc "nghẽn". */
  var CREATE = ['cue', 'reaction', 'evaluation', 'ability', 'timing'];
  var FIX = { cue: 'cueAction', reaction: 'reassure', evaluation: 'benefit', ability: 'fewerSteps', timing: 'timely' };
  (function () {
    var m = 'create';
    function steps(s) {
      var out = [S(m, 'target', { type: 'scenario', activeNodes: ['cue'], callouts: [{ kind: 'mechanism', textKey: M(m, 'co.noData') }], logEvents: [{ t: 0, kind: 'observe', subject: 'cue' }] })], open = 0;
      CREATE.forEach(function (st, i) {
        var ok = !!s[FIX[st]]; if (ok) open++;
        var o = S(m, st, { type: ok ? 'mechanism' : 'pitfall', explainKey: M(m, 's.' + st + (ok ? '.open' : '.blocked')), activeNodes: [st],
          nodeStates: { }, logEvents: [{ t: i + 1, kind: ok ? 'act' : 'error', subject: st, detailKey: M(m, ok ? 'ev.open' : 'ev.blocked') }] });
        o.nodeStates[st] = K + (ok ? 'st.open' : 'st.blocked');
        out.push(o);
      });
      out[out.length - 1].metrics = { open: open };
      return out;
    }
    var ctl = CREATE.map(function (st) { return tog(m, FIX[st]); });
    reg(m, { controls: ctl, init: function () { return { cueAction: true, reassure: true, benefit: false, fewerSteps: false, timely: false }; }, act: setter(CREATE.map(function (st) { return FIX[st]; })), steps: steps,
      selfChecks: [{ name: 'không can thiệp nào có số liệu; bật cả năm thì mọi giai đoạn thông', run: function () { var st = steps({ cueAction: true, reassure: true, benefit: true, fewerSteps: true, timely: true }); return st[st.length - 1].metrics.open === 5; } }] });
  })();

  /* D5: nhận diện deceptive pattern (chỉ để nhận diện và tránh) */
  regChoice('deceptive', { p1: 'sneaking', p2: 'confirmshaming', p3: 'falseUrgency', p4: 'obstruction', p5: 'visualTrick', p6: 'nagging' },
    ['sneaking', 'confirmshaming', 'falseUrgency', 'obstruction', 'visualTrick', 'nagging'], { source: true,
      extra: function (out, s) { out.push(S('deceptive', 'honest', { explainKey: M('deceptive', 'i.' + s.item + '.honest'), activeNodes: ['design'], callouts: [{ kind: 'pitfall', textKey: M('deceptive', 'co.ethics') }], logEvents: [{ t: 3, kind: 'recover', subject: 'design' }] })); } });

  /* D6: bộ chọn phương pháp nghiên cứu (NN/g which-ux-research-methods) */
  regChoice('methods', { q1: ['fieldStudy', 'interview'], q2: ['analytics'], q3: ['usability'], q4: ['survey'], q5: ['cardSort'], q6: ['interview', 'fieldStudy'] },
    ['interview', 'fieldStudy', 'usability', 'survey', 'analytics', 'cardSort'], { source: true,
      extra: function (out, s) { out.push(S('methods', 'axes', { explainKey: M('methods', 'i.' + s.item + '.axes'), activeNodes: ['design'], logEvents: [{ t: 3, kind: 'measure', subject: 'design' }] })); } });

  /* D7: phiên think-aloud mô phỏng — ống kính "nói" (thái độ) và "làm" (hành vi) */
  (function () {
    var m = 'session', LINES = ['l1', 'l2', 'l3', 'l4', 'l5', 'l6'], ISSUE = { l2: 'time', l4: 'phone', l5: 'cancel' };
    function steps(s) {
      return LINES.map(function (l, i) {
        var o = S(m, l, { type: i === 0 ? 'scenario' : ISSUE[l] ? 'pitfall' : 'mechanism', explainKey: M(m, 's.' + l + '.' + s.lens), activeNodes: [s.lens === 'say' ? 'user' : 'screen'],
          logEvents: [{ t: i, kind: s.lens === 'say' ? 'observe' : (ISSUE[l] ? 'error' : 'act'), subject: s.lens === 'say' ? 'user' : 'screen', detailKey: M(m, 'ev.' + l + '.' + s.lens) }] });
        if (ISSUE[l] && s.notes) o.changes = [{ op: 'add', textKey: M(m, 'note.' + ISSUE[l]) }];
        if (i === 5) o.metrics = { issues: s.notes ? 3 : 0 };
        return o;
      });
    }
    reg(m, { controls: [sel(m, 'lens', ['do', 'say']), tog(m, 'notes')], init: function () { return { lens: 'do', notes: true }; }, act: setter(['lens', 'notes']), steps: steps,
      selfChecks: [{ name: 'sáu dòng; ba vấn đề tham chiếu', run: function () { return steps({ lens: 'do', notes: true }).length === 6 && Object.keys(ISSUE).length === 3; } }] });
  })();

  /* D9: voice và tone — cùng một thông điệp ở các bối cảnh */
  (function () {
    var m = 'tone', CTX = ['normal', 'urgent', 'error'];
    function steps(s) {
      return [S(m, 'voice', { type: 'scenario', explainKey: M(m, 'voice.' + s.voice), activeNodes: ['design'], logEvents: [{ t: 0, kind: 'observe', subject: 'design' }] }),
        S(m, 'msg', { titleKey: M(m, 'ctx.' + s.ctx + '.title'), explainKey: M(m, 'msg.' + s.voice + '.' + s.ctx), activeNodes: ['screen'], movingSignals: [{ edge: 'e1', tok: 'signal' }], logEvents: [{ t: 1, kind: 'feedback', subject: 'screen', detailKey: M(m, 'ctx.' + s.ctx + '.title') }] }),
        S(m, 'why', { explainKey: M(m, 'why.' + s.ctx), activeNodes: ['user'], callouts: [{ kind: 'source', textKey: M(m, 'co.source') }], logEvents: [{ t: 2, kind: 'decide', subject: 'user' }] })];
    }
    reg(m, { controls: [sel(m, 'voice', ['warm', 'plain']), sel(m, 'ctx', CTX)], init: function () { return { voice: 'warm', ctx: 'normal' }; }, act: setter(['voice', 'ctx']), steps: steps,
      selfChecks: [{ name: 'mỗi bối cảnh có 3 bước', run: function () { return CTX.every(function (c) { return steps({ voice: 'warm', ctx: c }).length === 3; }); } }] });
  })();

  /* D10: kế hoạch sprint — hai biến thể (GV; Banfield et al.), có thể bỏ ngày test để thấy đầu ra bị thiếu */
  (function () {
    var m = 'sprint', V = { gv: ['mon', 'tue', 'wed', 'thu', 'fri'], banfield: ['understand', 'diverge', 'converge', 'prototype', 'test'] };
    function steps(s) {
      var ph = V[s.variant], out = [];
      ph.forEach(function (p, i) {
        var skip = s.skipTest && i === 4;
        var o = S(m, p, { type: i === 0 ? 'scenario' : skip ? 'pitfall' : 'mechanism', explainKey: M(m, 's.' + p + (skip ? '.skipped' : '.explain')), activeNodes: ['p' + i],
          logEvents: [{ t: i, kind: skip ? 'error' : 'act', subject: 'p' + i, detailKey: M(m, 'ev.' + p) }] });
        if (skip) o.skipped = [{ whatKey: M(m, 'sk.test'), whyKey: M(m, 'sk.why') }];
        out.push(o);
      });
      out[0].callouts = [{ kind: 'source', textKey: M(m, 'co.' + s.variant) }];
      return out;
    }
    reg(m, { controls: [sel(m, 'variant', ['gv', 'banfield']), tog(m, 'skipTest')], init: function () { return { variant: 'gv', skipTest: false }; }, act: setter(['variant', 'skipTest']), steps: steps,
      selfChecks: [{ name: 'hai biến thể đều 5 pha', run: function () { return steps({ variant: 'gv' }).length === 5 && steps({ variant: 'banfield' }).length === 5; } }] });
  })();

  /* D10: phản hồi stakeholder (ý tưởng từ Greever, Articulating Design Decisions — author-framework) */
  regChoice('stakeholder', { f1: 'goal', f2: 'data', f3: 'constraint', f4: 'goal', f5: 'data' }, ['goal', 'data', 'constraint', 'comply']);
})();
