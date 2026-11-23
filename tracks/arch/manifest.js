/* Track G: Kiến trúc app Android. Nội dung sinh từ dev/gen/arch_content.py (module arch_v2_<chương>.py).
   Spec: docs/tracks/G-clean-architecture.md (12 chương, đã duyệt 2026-11-23). Trong lúc viết: status 'draft'. */
ADE.registerTrack({
  id: 'arch', code: 'G', order: 70, domain: 'engineering',
  accent: '#3D7F8A', icon: 'layers',
  titleKey: 'track.arch.title', summaryKey: 'track.arch.summary',
  level: 'intermediate', estMinutes: 360, status: 'draft',
  prerequisites: [], languages: ['vi', 'en'],
  chapters: [
    { id: 'g1', titleKey: 'track.arch.g1.title', sims: ['arch.god'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'g2', titleKey: 'track.arch.g2.title', sims: ['arch.layers', 'arch.ssot'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'g3', titleKey: 'track.arch.g3.title', sims: ['arch.events'], simAfter: 'hook', bridges: ['X12'], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'g4', titleKey: 'track.arch.g4.title', sims: ['arch.offline'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'g5', titleKey: 'track.arch.g5.title', sims: ['arch.usecase'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'g6', titleKey: 'track.arch.g6.title', sims: ['arch.di'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'arch-god-activity', model: 'arch.god', titleKey: 'track.arch.preset.god' },
    { id: 'arch-layers', model: 'arch.layers', titleKey: 'track.arch.preset.layers' },
    { id: 'arch-events', model: 'arch.events', titleKey: 'track.arch.preset.events' },
    { id: 'arch-offline', model: 'arch.offline', titleKey: 'track.arch.preset.offline' },
    { id: 'arch-usecase', model: 'arch.usecase', titleKey: 'track.arch.preset.usecase' },
    { id: 'arch-di', model: 'arch.di', titleKey: 'track.arch.preset.di' }
  ],
  logKinds: ['observe', 'run', 'write', 'skip', 'exception', 'complete'],
  labels: ['stable', 'version', 'impl', 'simplified', 'guideline'],
  glossaryNs: 'arch', misconceptionsNs: 'arch'
});
