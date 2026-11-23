/* Track D: Thiết kế cho cách con người nghĩ (UX). Nội dung sinh từ dev/gen/ux_content.py. Ứng dụng mẫu hư cấu: shared/mock-app/. */
ADE.registerTrack({
  id: 'ux', code: 'D', order: 40, domain: 'design',
  accent: '#C75976', icon: 'eye',
  titleKey: 'track.ux.title', summaryKey: 'track.ux.summary',
  level: 'beginner', estMinutes: 360, status: 'stable',
  prerequisites: [], languages: ['vi', 'en'],
  chapters: [
    { id: 'd0', titleKey: 'track.ux.d0.title', sims: ['ux.classify', 'ux.diamond'], bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'd1', titleKey: 'track.ux.d1.title', sims: ['ux.glance', 'ux.mental', 'ux.recall'], simAfter: 'hook', bridges: ['X7'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'd2', titleKey: 'track.ux.d2.title', sims: ['ux.stages'], bridges: ['X6'], goals: [{ id: 'g1', step: 4 }, { id: 'g2', step: 'end' }] },
    { id: 'd3', titleKey: 'track.ux.d3.title', sims: ['ux.errors'], bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'd4', titleKey: 'track.ux.d4.title', sims: ['ux.heuristic'], bridges: [], goals: [{ id: 'g1', step: 0 }, { id: 'g2', step: 'end' }] },
    { id: 'd5', titleKey: 'track.ux.d5.title', sims: ['ux.create', 'ux.deceptive'], bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'd6', titleKey: 'track.ux.d6.title', sims: ['ux.methods'], bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'd7', titleKey: 'track.ux.d7.title', sims: ['ux.curve', 'ux.session'], bridges: [], goals: [{ id: 'g1', step: 0 }, { id: 'g2', step: 'end' }] },
    { id: 'd8', titleKey: 'track.ux.d8.title', sims: ['ux.sus', 'ux.success'], bridges: [], goals: [{ id: 'g1', step: 0 }, { id: 'g2', step: 'end' }] },
    { id: 'd9', titleKey: 'track.ux.d9.title', sims: ['ux.microcopy', 'ux.tone'], bridges: ['X8', 'X6'], goals: [{ id: 'g1', step: 0 }, { id: 'g2', step: 'end' }] },
    { id: 'd10', titleKey: 'track.ux.d10.title', sims: ['ux.sprint', 'ux.stakeholder'], bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'ux-seven-stages', model: 'ux.stages', titleKey: 'track.ux.preset.stages' },
    { id: 'ux-error-lab', model: 'ux.errors', titleKey: 'track.ux.preset.errors' },
    { id: 'ux-heuristic-eval', model: 'ux.heuristic', titleKey: 'track.ux.preset.heuristic' },
    { id: 'ux-discovery-curve', model: 'ux.curve', titleKey: 'track.ux.preset.curve' },
    { id: 'ux-sus-calculator', model: 'ux.sus', titleKey: 'track.ux.preset.sus' },
    { id: 'ux-microcopy', model: 'ux.microcopy', titleKey: 'track.ux.preset.microcopy' }
  ],
  logKinds: ['observe', 'act', 'error', 'feedback', 'decide', 'measure', 'recover'],
  labels: ['normative', 'research', 'ds-guideline', 'author-framework', 'quant-model', 'guideline', 'simplified', 'impl', 'stable'],
  glossaryNs: 'ux', misconceptionsNs: 'ux'
});
