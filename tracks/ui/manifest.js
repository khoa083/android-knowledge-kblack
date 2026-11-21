/* Track E: Giao diện Android — từ nguyên lý đến design system. Nội dung sinh từ dev/gen/ui_content.py. Mock app dùng chung: shared/mock-app/. */
ADE.registerTrack({
  id: 'ui', code: 'E', order: 50, domain: 'design',
  accent: '#398D62', icon: 'grid',
  titleKey: 'track.ui.title', summaryKey: 'track.ui.summary',
  level: 'beginner', estMinutes: 360, status: 'stable',
  prerequisites: ['ux'], languages: ['vi', 'en'],
  chapters: [
    { id: 'e0', titleKey: 'track.ui.e0.title', sims: ['ui.layers'], bridges: ['X5'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'e1', titleKey: 'track.ui.e1.title', sims: ['ui.crap'], bridges: [], goals: [{ id: 'g1', step: 0 }, { id: 'g2', step: 'end' }] },
    { id: 'e2', titleKey: 'track.ui.e2.title', sims: ['ui.type'], bridges: ['X5'], goals: [{ id: 'g1', step: 0 }, { id: 'g2', step: 'end' }] },
    { id: 'e3', titleKey: 'track.ui.e3.title', sims: ['ui.contrast', 'ui.roles'], bridges: ['X5'], goals: [{ id: 'g1', step: 0 }, { id: 'g2', step: 'end' }] },
    { id: 'e4', titleKey: 'track.ui.e4.title', sims: ['ui.responsive'], bridges: [], goals: [{ id: 'g1', step: 0 }, { id: 'g2', step: 'end' }] },
    { id: 'e5', titleKey: 'track.ui.e5.title', sims: ['ui.fitts'], bridges: [], goals: [{ id: 'g1', step: 0 }, { id: 'g2', step: 'end' }] },
    { id: 'e6', titleKey: 'track.ui.e6.title', sims: ['ui.states'], bridges: [], goals: [{ id: 'g1', step: 0 }, { id: 'g2', step: 'end' }] },
    { id: 'e7', titleKey: 'track.ui.e7.title', sims: ['ui.patterns', 'ui.form', 'ui.response'], bridges: ['X8'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'e8', titleKey: 'track.ui.e8.title', sims: ['ui.tokens'], bridges: ['X5'], goals: [{ id: 'g1', step: 0 }, { id: 'g2', step: 'end' }] },
    { id: 'e9', titleKey: 'track.ui.e9.title', sims: ['ui.motion'], bridges: ['X7', 'X1'], goals: [{ id: 'g1', step: 0 }, { id: 'g2', step: 'end' }] },
    { id: 'e10', titleKey: 'track.ui.e10.title', sims: ['ui.a11y'], bridges: ['X6'], goals: [{ id: 'g1', step: 0 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'ui-crap-fix', model: 'ui.crap', titleKey: 'track.ui.preset.crap' },
    { id: 'ui-contrast-checker', model: 'ui.contrast', titleKey: 'track.ui.preset.contrast' },
    { id: 'ui-responsive-lab', model: 'ui.responsive', titleKey: 'track.ui.preset.responsive' },
    { id: 'ui-fitts-playground', model: 'ui.fitts', titleKey: 'track.ui.preset.fitts' },
    { id: 'ui-token-editor', model: 'ui.tokens', titleKey: 'track.ui.preset.tokens' },
    { id: 'ui-a11y-audit', model: 'ui.a11y', titleKey: 'track.ui.preset.a11y' }
  ],
  logKinds: ['observe', 'act', 'feedback', 'measure', 'error', 'decide'],
  labels: ['normative', 'research', 'ds-guideline', 'author-framework', 'quant-model', 'stable', 'version', 'guideline', 'simplified'],
  glossaryNs: 'ui', misconceptionsNs: 'ui'
});
