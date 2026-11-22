/* Track B: Compose Runtime Explorer. Nội dung song ngữ ở content.vi.js / content.en.js (cùng cây khoá track.runtime.*).
   Phiên bản: Compose BOM 2026.11.01 (runtime/ui 1.13.0), Kotlin 2.4.21; xem docs/research/runtime.md. */
ADE.registerTrack({
  id: 'runtime', code: 'B', order: 20, domain: 'engineering',
  accent: '#946BC4', icon: 'layers',
  titleKey: 'track.runtime.title', summaryKey: 'track.runtime.summary',
  level: 'advanced', estMinutes: 300, status: 'stable',
  prerequisites: ['coroutines'], languages: ['vi', 'en'],
  chapters: [
    { id: 'b0', titleKey: 'track.runtime.b0.title', sims: ['runtime.map'], bridges: ['X5'], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] },
    { id: 'dc', titleKey: 'track.runtime.dc.title', sims: ['runtime.runs'], simAfter: 'rules', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },   // v2 (Kunneth Ch.2–3, Thinking in Compose)
    { id: 'b1', titleKey: 'track.runtime.b1.title', sims: ['runtime.setcontent'], bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'b2', titleKey: 'track.runtime.b2.title', sims: ['runtime.groups', 'runtime.compiler'], simAfter: 'restart', bridges: [], goals: [{ id: 'g1', step: 5 }, { id: 'g2', step: 'end' }] },   // v2 (how-compose-works.md @296313a4)
    { id: 'b3', titleKey: 'track.runtime.b3.title', sims: ['runtime.structure', 'runtime.keys'], simAfter: 'identity', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },   // v2 (how-compose-works.md @296313a4, Lifecycle of composables)
    { id: 'b4', titleKey: 'track.runtime.b4.title', sims: ['runtime.snapshot'], bridges: ['X2'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'b5', titleKey: 'track.runtime.b5.title', sims: ['runtime.recomposer'], bridges: ['X3'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'b6', titleKey: 'track.runtime.b6.title', sims: ['runtime.applier'], bridges: [], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] },
    { id: 'b7', titleKey: 'track.runtime.b7.title', sims: ['runtime.phases'], bridges: ['X1'], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] },
    { id: 'b8', titleKey: 'track.runtime.b8.title', sims: ['runtime.skip'], bridges: ['X2'], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'b9', titleKey: 'track.runtime.b9.title', sims: ['runtime.semantics'], bridges: ['X6'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'b10', titleKey: 'track.runtime.b10.title', sims: ['runtime.counter'], bridges: ['X1'], goals: [{ id: 'g1', step: 4 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'runtime-counter', model: 'runtime.counter', titleKey: 'track.runtime.preset.counter' },
    { id: 'runtime-list-key', model: 'runtime.keys', titleKey: 'track.runtime.preset.keys' },
    { id: 'runtime-phase-read', model: 'runtime.phases', titleKey: 'track.runtime.preset.phases' }
  ],
  logKinds: ['write', 'invalidate', 'schedule', 'recompose', 'skip', 'apply', 'layout', 'draw', 'frame', 'observe', 'act', 'resume'],
  labels: ['stable', 'impl', 'android-impl', 'version', 'simplified', 'guideline'],
  glossaryNs: 'runtime', misconceptionsNs: 'runtime'
});
