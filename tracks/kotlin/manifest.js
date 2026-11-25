/* Track F: Kotlin — cơ chế ngôn ngữ. Nội dung sinh từ dev/gen/kotlin_content.py (module kotlin_v2_<chương>.py).
   Spec: docs/tracks/F-kotlin.md (14 chương, hai phần; chọn kiến thức cần và đủ). Đã xong 14 chương (k0 viết cuối, đặt đầu): status 'stable'. */
ADE.registerTrack({
  id: 'kotlin', code: 'F', order: 60, domain: 'engineering',
  accent: '#78842C', icon: 'source',
  titleKey: 'track.kotlin.title', summaryKey: 'track.kotlin.summary',
  level: 'beginner', estMinutes: 420, status: 'stable',
  prerequisites: [], languages: ['vi', 'en'],
  chapters: [
    { id: 'k0', titleKey: 'track.kotlin.k0.title', sims: ['kotlin.map'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k1', titleKey: 'track.kotlin.k1.title', sims: ['kotlin.eval'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k2', titleKey: 'track.kotlin.k2.title', sims: ['kotlin.smartcast'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k3', titleKey: 'track.kotlin.k3.title', sims: ['kotlin.init'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k4', titleKey: 'track.kotlin.k4.title', sims: ['kotlin.hashset'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k5', titleKey: 'track.kotlin.k5.title', sims: ['kotlin.sealed'], simAfter: 'hook', bridges: ['X24'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k6', titleKey: 'track.kotlin.k6.title', sims: ['kotlin.exception'], simAfter: 'hook', bridges: ['X14', 'X20', 'X25', 'X29'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k7', titleKey: 'track.kotlin.k7.title', sims: ['kotlin.collections'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k8', titleKey: 'track.kotlin.k8.title', sims: ['kotlin.inline'], simAfter: 'hook', bridges: ['X9', 'X32'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k9', titleKey: 'track.kotlin.k9.title', sims: ['kotlin.sequence'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k10', titleKey: 'track.kotlin.k10.title', sims: ['kotlin.variance'], simAfter: 'hook', bridges: ['X10'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k11', titleKey: 'track.kotlin.k11.title', sims: ['kotlin.delegate'], simAfter: 'hook', bridges: ['X11', 'X15'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k12', titleKey: 'track.kotlin.k12.title', sims: ['kotlin.scope'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'k13', titleKey: 'track.kotlin.k13.title', sims: ['kotlin.jvm'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'kotlin-int-division', model: 'kotlin.eval', titleKey: 'track.kotlin.preset.eval' },
    { id: 'kotlin-smart-cast', model: 'kotlin.smartcast', titleKey: 'track.kotlin.preset.smartcast' },
    { id: 'kotlin-hashset-lost', model: 'kotlin.hashset', titleKey: 'track.kotlin.preset.hashset' },
    { id: 'kotlin-foreach-return', model: 'kotlin.inline', titleKey: 'track.kotlin.preset.inline' },
    { id: 'kotlin-sequence-lazy', model: 'kotlin.sequence', titleKey: 'track.kotlin.preset.sequence' }
  ],
  logKinds: ['observe', 'check', 'run', 'write', 'skip', 'exception', 'complete'],
  labels: ['stable', 'version', 'impl', 'simplified', 'guideline'],
  glossaryNs: 'kotlin', misconceptionsNs: 'kotlin'
});
