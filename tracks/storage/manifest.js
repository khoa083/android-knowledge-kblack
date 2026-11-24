/* Track H: Lưu dữ liệu trên Android. Nội dung sinh từ dev/gen/storage_content.py (module storage_v2_<chương>.py).
   Spec: docs/tracks/H-saving-data.md (10 chương, đã duyệt 2026-11-24). Trong lúc viết: status 'draft'. */
ADE.registerTrack({
  id: 'storage', code: 'H', order: 80, domain: 'engineering',
  accent: '#4F7CA8', icon: 'store',
  titleKey: 'track.storage.title', summaryKey: 'track.storage.summary',
  level: 'intermediate', estMinutes: 300, status: 'draft',
  prerequisites: [], languages: ['vi', 'en'],
  chapters: [
    { id: 'h1', titleKey: 'track.storage.h1.title', sims: ['storage.choose'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'storage-choose', model: 'storage.choose', titleKey: 'track.storage.preset.choose' }
  ],
  logKinds: ['observe', 'run', 'write', 'skip', 'exception', 'complete'],
  labels: ['stable', 'version', 'impl', 'simplified', 'guideline'],
  glossaryNs: 'storage', misconceptionsNs: 'storage'
});
