/* View sơ đồ cho các model rời rạc của track D. */
(function () {
  'use strict';
  var K = 'track.ux.';
  var N = function (id, x, y, icon, tok, key) { return { id: id, x: x, y: y, icon: icon, tok: tok, labelKey: key || K + 'n.' + id }; };
  var E = function (id, f, t) { return { id: id, from: f, to: t }; };
  function V(m, cfg) { var v = { titleKey: K + 'm.' + m + '.diagramTitle', descKey: K + 'm.' + m + '.diagramDesc', captionKey: K + 'cap.' + m, subjectKey: K + 'col.subject', stateFamilies: { open: 'idle', ok: 'done', broken: 'fail', blocked: 'block' }, famKeys: { done: K + 'fam.done', fail: K + 'fam.fail', block: K + 'fam.block', idle: K + 'fam.idle' } }; for (var k in cfg) v[k] = cfg[k]; ADE.registerView('ux.' + m, v); }
  /* vòng phản hồi thiết kế: màn hình → người dùng → (quan sát) → thiết kế → màn hình */
  var basic = { nodes: [N('screen', 0, 0, 'phone', 'ui'), N('user', 4, 0, 'eye', 'signal'), N('design', 4, 4, 'set', 'runtime')], edges: [E('e1', 'screen', 'user'), E('e2', 'user', 'design'), E('e3', 'design', 'screen')] };
  ['classify', 'mental', 'deceptive', 'methods', 'stakeholder', 'session', 'tone'].forEach(function (m) { V(m, { layout: 'cycle', captionKey: K + 'cap.loop', nodes: basic.nodes, edges: basic.edges, metrics: m === 'session' ? [{ id: 'issues', labelKey: K + 'm.session.met.issues' }] : [{ id: 'right', labelKey: K + 'c.metRight' }] }); });
  V('errors', { layout: 'cycle', captionKey: K + 'cap.loop', nodes: basic.nodes, edges: basic.edges, metrics: [{ id: 'right', labelKey: K + 'c.metRight' }, { id: 'before', labelKey: K + 'm.errors.met.before' }, { id: 'after', labelKey: K + 'm.errors.met.after' }] });
  V('diamond', { layout: 'pipeline', nodes: [N('discover', 0, 0, 'search', 'signal', K + 'm.diamond.ph.discover.title'), N('define', 3, 0, 'target', 'state', K + 'm.diamond.ph.define.title'), N('develop', 6, 0, 'spark', 'ui', K + 'm.diamond.ph.develop.title'), N('deliver', 9, 0, 'check', 'job', K + 'm.diamond.ph.deliver.title')],
    edges: [E('d1', 'discover', 'define'), E('d2', 'define', 'develop'), E('d3', 'develop', 'deliver'), E('back', 'deliver', 'discover')], metrics: [] });
  var ST = ['goal', 'plan', 'specify', 'perform', 'perceive', 'interpret', 'compare'];
  var pos = [[0, 0], [3, -3], [6, -3], [9, 0], [6, 3], [3, 3], [0, 3]];
  V('stages', { layout: 'cycle', nodes: ST.map(function (s, i) { return N(s, pos[i][0], pos[i][1], i <= 3 ? 'play' : 'eye', i <= 3 ? 'ui' : 'signal', K + 'm.stages.s.' + s + '.title'); }),
    edges: ST.slice(0, 6).map(function (s, i) { return E('g' + i, s, ST[i + 1]); }), metrics: [{ id: 'exec', labelKey: K + 'm.stages.met.exec' }, { id: 'eval', labelKey: K + 'm.stages.met.eval' }] });
  var CR = ['cue', 'reaction', 'evaluation', 'ability', 'timing'];
  V('create', { layout: 'pipeline', nodes: CR.map(function (s, i) { return N(s, i * 3, 0, ['bolt', 'eye', 'target', 'grid', 'clock'][i], 'signal', K + 'm.create.s.' + s + '.title'); }),
    edges: CR.slice(0, 4).map(function (s, i) { return E('c' + i, s, CR[i + 1]); }), metrics: [{ id: 'open', labelKey: K + 'm.create.met.open' }] });
  V('sprint', { layout: 'pipeline', nodes: [0, 1, 2, 3, 4].map(function (i) { return N('p' + i, i * 3, 0, ['target', 'spark', 'check', 'layers', 'eye'][i], 'ui', K + 'm.sprint.n.p' + i); }),
    edges: [0, 1, 2, 3].map(function (i) { return E('s' + i, 'p' + i, 'p' + (i + 1)); }), metrics: [] });
})();
