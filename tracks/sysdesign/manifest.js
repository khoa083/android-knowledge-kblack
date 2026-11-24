/* Track I: Thiết kế hệ thống phía mobile. Nội dung sinh từ dev/gen/sysdesign_content.py (module sysdesign_v2_<chương>.py).
   Spec: docs/tracks/I-mobile-system-design.md (14 chương, đã duyệt 2026-11-24). Trong lúc viết: status 'draft'. */
ADE.registerTrack({
  id: 'sysdesign', code: 'I', order: 90, domain: 'engineering',
  accent: '#7A6FB0', icon: 'job',
  titleKey: 'track.sysdesign.title', summaryKey: 'track.sysdesign.summary',
  level: 'advanced', estMinutes: 400, status: 'draft',
  prerequisites: [], languages: ['vi', 'en'],
  chapters: [
    { id: 'i1', titleKey: 'track.sysdesign.i1.title', sims: ['sysdesign.plan'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'sysdesign-plan', model: 'sysdesign.plan', titleKey: 'track.sysdesign.preset.plan' }
  ],
  logKinds: ['observe', 'run', 'write', 'skip', 'exception', 'complete'],
  labels: ['stable', 'version', 'impl', 'simplified', 'guideline'],
  glossaryNs: 'sysdesign', misconceptionsNs: 'sysdesign'
});
