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
    { id: 'h4', titleKey: 'track.storage.h4.title', sims: ['storage.room'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'h5', titleKey: 'track.storage.h5.title', sims: ['storage.rel'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'h6', titleKey: 'track.storage.h6.title', sims: ['storage.mig'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'h7', titleKey: 'track.storage.h7.title', sims: ['storage.sync'], simAfter: 'hook', bridges: ['X16'], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'h8', titleKey: 'track.storage.h8.title', sims: ['storage.media'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'h9', titleKey: 'track.storage.h9.title', sims: ['storage.backup'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'storage-choose', model: 'storage.choose', titleKey: 'track.storage.preset.choose' },
    { id: 'storage-file', model: 'storage.file', titleKey: 'track.storage.preset.file' },
    { id: 'storage-prefs', model: 'storage.prefs', titleKey: 'track.storage.preset.prefs' },
    { id: 'storage-room', model: 'storage.room', titleKey: 'track.storage.preset.room' },
    { id: 'storage-rel', model: 'storage.rel', titleKey: 'track.storage.preset.rel' },
    { id: 'storage-mig', model: 'storage.mig', titleKey: 'track.storage.preset.mig' },
    { id: 'storage-sync', model: 'storage.sync', titleKey: 'track.storage.preset.sync' },
    { id: 'storage-media', model: 'storage.media', titleKey: 'track.storage.preset.media' },
    { id: 'storage-backup', model: 'storage.backup', titleKey: 'track.storage.preset.backup' }
  ],
  logKinds: ['observe', 'run', 'write', 'skip', 'exception', 'complete'],
  labels: ['stable', 'version', 'impl', 'simplified', 'guideline'],
  glossaryNs: 'storage', misconceptionsNs: 'storage'
});
