/* Track C: Compose Animation Lab. Nội dung song ngữ ở content.vi.js / content.en.js (sinh từ dev/gen/animation_content.py).
   Phiên bản: compose.animation 1.13.0 (BOM 2026.11.01); xem docs/research/animation.md. */
ADE.defineKind('target-change', { tok: 'state', icon: 'target' });   // target của animation đổi

ADE.registerTrack({
  id: 'animation', code: 'C', order: 30, domain: 'engineering',
  accent: '#B46D24', icon: 'motion',
  titleKey: 'track.animation.title', summaryKey: 'track.animation.summary',
  level: 'intermediate', estMinutes: 270, status: 'stable',
  prerequisites: ['runtime'], languages: ['vi', 'en'],
  chapters: [
    { id: 'c0', titleKey: 'track.animation.c0.title', sims: ['animation.choose'], bridges: ['X7'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'c1', titleKey: 'track.animation.c1.title', sims: ['animation.aas', 'animation.retarget'], simAfter: 'inside', bridges: ['X1'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },   // v2 (AnimateAsState.kt @296313a4, Kunneth Ch.8, Essentials Ch.40, Tutorials Ch.12)
    { id: 'c2', titleKey: 'track.animation.c2.title', sims: ['animation.vector', 'animation.spec'], simAfter: 'vectors', bridges: ['X7'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },   // v2 (AnimationSpec.kt, Easing.kt, VectorConverters.kt, ColorVectorConverter.kt @296313a4; Essentials Ch.39–40; Kunneth Ch.8)
    { id: 'c3', titleKey: 'track.animation.c3.title', sims: ['animation.segment', 'animation.transition'], simAfter: 'state', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },   // v2 (Transition.kt @296313a4, Kunneth Ch.8, Tutorials Ch.12)
    { id: 'c4', titleKey: 'track.animation.c4.title', sims: ['animation.exitlife', 'animation.visibility'], simAfter: 'life', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },   // v2 (AnimatedVisibility.kt @296313a4, Kunneth Ch.8, Essentials Ch.39)
    { id: 'c5', titleKey: 'track.animation.c5.title', sims: ['animation.size'], bridges: ['X1'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'c6', titleKey: 'track.animation.c6.title', sims: ['animation.gesture'], bridges: ['X4', 'X2'], goals: [{ id: 'g1', step: 0 }, { id: 'g2', step: 'end' }] },
    { id: 'c7', titleKey: 'track.animation.c7.title', sims: ['animation.phaseread'], bridges: ['X1', 'X3'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'c8', titleKey: 'track.animation.c8.title', sims: ['animation.testclock'], bridges: ['X6'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'animation-spec-lab', model: 'animation.spec', titleKey: 'track.animation.preset.spec' },
    { id: 'animation-target-interrupt', model: 'animation.retarget', titleKey: 'track.animation.preset.retarget' },
    { id: 'animation-gesture-fling', model: 'animation.gesture', titleKey: 'track.animation.preset.gesture' },
    { id: 'animation-phase-read', model: 'animation.phaseread', titleKey: 'track.animation.preset.phaseread' }
  ],
  logKinds: ['target-change', 'frame', 'interrupt', 'settle', 'observe', 'act', 'skip', 'recompose', 'layout', 'draw'],
  labels: ['stable', 'version', 'experimental', 'guideline', 'simplified', 'impl'],
  glossaryNs: 'animation', misconceptionsNs: 'animation'
});
