/* Track F: Kotlin — cơ chế ngôn ngữ. Nội dung sinh từ dev/gen/kotlin_content.py (module kotlin_v2_<chương>.py).
   Spec: docs/tracks/F-kotlin.md (14 chương, hai phần; chọn kiến thức cần và đủ). Trong lúc viết: status 'draft'. */
ADE.registerTrack({
  id: 'kotlin', code: 'F', order: 60, domain: 'engineering',
  accent: '#78842C', icon: 'source',
  titleKey: 'track.kotlin.title', summaryKey: 'track.kotlin.summary',
  level: 'beginner', estMinutes: 420, status: 'draft',
  prerequisites: [], languages: ['vi', 'en'],
  chapters: [
    { id: 'k1', titleKey: 'track.kotlin.k1.title', sims: ['kotlin.eval'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k2', titleKey: 'track.kotlin.k2.title', sims: ['kotlin.smartcast'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k3', titleKey: 'track.kotlin.k3.title', sims: ['kotlin.init'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k4', titleKey: 'track.kotlin.k4.title', sims: ['kotlin.hashset'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k5', titleKey: 'track.kotlin.k5.title', sims: ['kotlin.sealed'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k6', titleKey: 'track.kotlin.k6.title', sims: ['kotlin.exception'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k7', titleKey: 'track.kotlin.k7.title', sims: ['kotlin.collections'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k8', titleKey: 'track.kotlin.k8.title', sims: ['kotlin.inline'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k9', titleKey: 'track.kotlin.k9.title', sims: ['kotlin.sequence'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'kotlin-int-division', model: 'kotlin.eval', titleKey: 'track.kotlin.preset.eval' }
  ],
  logKinds: ['observe', 'check', 'run', 'write', 'skip', 'exception', 'complete'],
  labels: ['stable', 'version', 'impl', 'simplified', 'guideline'],
  glossaryNs: 'kotlin', misconceptionsNs: 'kotlin'
});
