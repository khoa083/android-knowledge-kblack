/* Track K: Lập trình hàm với Kotlin. Nội dung sinh từ dev/gen/fp_content.py (module fp_v2_<chương>.py).
   Spec: docs/tracks/K-functional-kotlin.md (11 chương, đã duyệt 2026-11-24). Xong P0–P10 ngày 2026-11-25: status 'stable'. */
ADE.registerTrack({
  id: 'fp', code: 'K', order: 110, domain: 'engineering',
  accent: '#8C6D1F', icon: 'mechanism',
  titleKey: 'track.fp.title', summaryKey: 'track.fp.summary',
  level: 'advanced', estMinutes: 345, status: 'stable',
  prerequisites: [], languages: ['vi', 'en'],
  chapters: [
    { id: 'p0', titleKey: 'track.fp.p0.title', sims: ['fp.map'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'p1', titleKey: 'track.fp.p1.title', sims: ['fp.pure'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'p2', titleKey: 'track.fp.p2.title', sims: ['fp.persist'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'p3', titleKey: 'track.fp.p3.title', sims: ['fp.compose'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'p4', titleKey: 'track.fp.p4.title', sims: ['fp.adt'], simAfter: 'hook', bridges: ['X24'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'p5', titleKey: 'track.fp.p5.title', sims: ['fp.errors'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'p6', titleKey: 'track.fp.p6.title', sims: ['fp.monad'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'p7', titleKey: 'track.fp.p7.title', sims: ['fp.validate'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'p8', titleKey: 'track.fp.p8.title', sims: ['fp.reducer'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'p9', titleKey: 'track.fp.p9.title', sims: ['fp.core'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'p10', titleKey: 'track.fp.p10.title', sims: ['fp.optics'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'fp-map', model: 'fp.map', titleKey: 'track.fp.preset.map' },
    { id: 'fp-pure', model: 'fp.pure', titleKey: 'track.fp.preset.pure' },
    { id: 'fp-persist', model: 'fp.persist', titleKey: 'track.fp.preset.persist' },
    { id: 'fp-compose', model: 'fp.compose', titleKey: 'track.fp.preset.compose' },
    { id: 'fp-adt', model: 'fp.adt', titleKey: 'track.fp.preset.adt' },
    { id: 'fp-errors', model: 'fp.errors', titleKey: 'track.fp.preset.errors' },
    { id: 'fp-monad', model: 'fp.monad', titleKey: 'track.fp.preset.monad' },
    { id: 'fp-validate', model: 'fp.validate', titleKey: 'track.fp.preset.validate' },
    { id: 'fp-reducer', model: 'fp.reducer', titleKey: 'track.fp.preset.reducer' },
    { id: 'fp-core', model: 'fp.core', titleKey: 'track.fp.preset.core' },
    { id: 'fp-optics', model: 'fp.optics', titleKey: 'track.fp.preset.optics' }
  ],
  logKinds: ['observe', 'run', 'write', 'skip', 'exception', 'complete'],
  labels: ['stable', 'version', 'impl', 'simplified', 'guideline'],
  glossaryNs: 'fp', misconceptionsNs: 'fp'
});
