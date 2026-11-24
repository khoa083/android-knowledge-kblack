/* Track K: Lập trình hàm với Kotlin. Nội dung sinh từ dev/gen/fp_content.py (module fp_v2_<chương>.py).
   Spec: docs/tracks/K-functional-kotlin.md (11 chương, đã duyệt 2026-11-24). Trong lúc viết: status 'draft'. */
ADE.registerTrack({
  id: 'fp', code: 'K', order: 110, domain: 'engineering',
  accent: '#8C6D1F', icon: 'mechanism',
  titleKey: 'track.fp.title', summaryKey: 'track.fp.summary',
  level: 'advanced', estMinutes: 330, status: 'draft',
  prerequisites: [], languages: ['vi', 'en'],
  chapters: [
    { id: 'p1', titleKey: 'track.fp.p1.title', sims: ['fp.pure'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'p2', titleKey: 'track.fp.p2.title', sims: ['fp.persist'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'fp-pure', model: 'fp.pure', titleKey: 'track.fp.preset.pure' },
    { id: 'fp-persist', model: 'fp.persist', titleKey: 'track.fp.preset.persist' }
  ],
  logKinds: ['observe', 'run', 'write', 'skip', 'exception', 'complete'],
  labels: ['stable', 'version', 'impl', 'simplified', 'guideline'],
  glossaryNs: 'fp', misconceptionsNs: 'fp'
});
