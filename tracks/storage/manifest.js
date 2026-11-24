/* Track H: Lưu dữ liệu trên Android. Nội dung sinh từ dev/gen/storage_content.py (module storage_v2_<chương>.py).
   Spec: docs/tracks/H-saving-data.md (10 chương, đã duyệt 2026-11-24). Trong lúc viết: status 'draft'. */
ADE.registerTrack({
  id: 'storage', code: 'H', order: 80, domain: 'engineering',
  accent: '#4F7CA8', icon: 'store',
  titleKey: 'track.storage.title', summaryKey: 'track.storage.summary',
  level: 'intermediate', estMinutes: 300, status: 'draft',
  prerequisites: [], languages: ['vi', 'en'],
  chapters: [
    { id: 'h1', titleKey: 'track.storage.h1.title', sims: ['storage.choose'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'h2', titleKey: 'track.storage.h2.title', sims: ['storage.file'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'h3', titleKey: 'track.storage.h3.title', sims: ['storage.prefs'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'h4', titleKey: 'track.storage.h4.title', sims: ['storage.room'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'storage-choose', model: 'storage.choose', titleKey: 'track.storage.preset.choose' },
    { id: 'storage-file', model: 'storage.file', titleKey: 'track.storage.preset.file' },
    { id: 'storage-prefs', model: 'storage.prefs', titleKey: 'track.storage.preset.prefs' },
    { id: 'storage-room', model: 'storage.room', titleKey: 'track.storage.preset.room' }
  ],
  logKinds: ['observe', 'run', 'write', 'skip', 'exception', 'complete'],
  labels: ['stable', 'version', 'impl', 'simplified', 'guideline'],
  glossaryNs: 'storage', misconceptionsNs: 'storage'
});
