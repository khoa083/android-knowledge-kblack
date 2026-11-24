/* Track I: Thiết kế hệ thống phía mobile. Nội dung sinh từ dev/gen/sysdesign_content.py (module sysdesign_v2_<chương>.py).
   Spec: docs/tracks/I-mobile-system-design.md (14 chương, đã duyệt 2026-11-24). Trong lúc viết: status 'draft'. */
ADE.registerTrack({
  id: 'sysdesign', code: 'I', order: 90, domain: 'engineering',
  accent: '#7A6FB0', icon: 'job',
  titleKey: 'track.sysdesign.title', summaryKey: 'track.sysdesign.summary',
  level: 'advanced', estMinutes: 400, status: 'draft',
  prerequisites: [], languages: ['vi', 'en'],
  chapters: [
    { id: 'i1', titleKey: 'track.sysdesign.i1.title', sims: ['sysdesign.plan'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'i2', titleKey: 'track.sysdesign.i2.title', sims: ['sysdesign.process'], simAfter: 'hook', bridges: ['X17'], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'i3', titleKey: 'track.sysdesign.i3.title', sims: ['sysdesign.lock'], simAfter: 'hook', bridges: ['X18'], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'i4', titleKey: 'track.sysdesign.i4.title', sims: ['sysdesign.channel'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'i5', titleKey: 'track.sysdesign.i5.title', sims: ['sysdesign.retry'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'i6', titleKey: 'track.sysdesign.i6.title', sims: ['sysdesign.cache'], simAfter: 'hook', bridges: ['X19'], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'i7', titleKey: 'track.sysdesign.i7.title', sims: ['sysdesign.paging'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'i8', titleKey: 'track.sysdesign.i8.title', sims: ['sysdesign.conflict'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'sysdesign-plan', model: 'sysdesign.plan', titleKey: 'track.sysdesign.preset.plan' },
    { id: 'sysdesign-process', model: 'sysdesign.process', titleKey: 'track.sysdesign.preset.process' },
    { id: 'sysdesign-lock', model: 'sysdesign.lock', titleKey: 'track.sysdesign.preset.lock' },
    { id: 'sysdesign-channel', model: 'sysdesign.channel', titleKey: 'track.sysdesign.preset.channel' },
    { id: 'sysdesign-retry', model: 'sysdesign.retry', titleKey: 'track.sysdesign.preset.retry' },
    { id: 'sysdesign-cache', model: 'sysdesign.cache', titleKey: 'track.sysdesign.preset.cache' },
    { id: 'sysdesign-paging', model: 'sysdesign.paging', titleKey: 'track.sysdesign.preset.paging' },
    { id: 'sysdesign-conflict', model: 'sysdesign.conflict', titleKey: 'track.sysdesign.preset.conflict' }
  ],
  logKinds: ['observe', 'run', 'write', 'skip', 'exception', 'complete'],
  labels: ['stable', 'version', 'impl', 'simplified', 'guideline'],
  glossaryNs: 'sysdesign', misconceptionsNs: 'sysdesign'
});
