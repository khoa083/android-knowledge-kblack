/* Track J: Mã sạch và kỷ luật làm nghề. Nội dung sinh từ dev/gen/cleancode_content.py (module cleancode_v2_<chương>.py).
   Spec: docs/tracks/J-clean-code.md (12 chương, đã duyệt 2026-11-24). Trong lúc viết: status 'draft'. */
ADE.registerTrack({
  id: 'cleancode', code: 'J', order: 100, domain: 'engineering',
  accent: '#5B6B7F', icon: 'list',
  titleKey: 'track.cleancode.title', summaryKey: 'track.cleancode.summary',
  level: 'intermediate', estMinutes: 360, status: 'draft',
  prerequisites: [], languages: ['vi', 'en'],
  chapters: [
    { id: 'j1', titleKey: 'track.cleancode.j1.title', sims: ['cleancode.fits'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'j2', titleKey: 'track.cleancode.j2.title', sims: ['cleancode.names'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'j3', titleKey: 'track.cleancode.j3.title', sims: ['cleancode.parse'], simAfter: 'hook', bridges: ['X20'], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'j4', titleKey: 'track.cleancode.j4.title', sims: ['cleancode.tdd'], simAfter: 'hook', bridges: ['X21'], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'j5', titleKey: 'track.cleancode.j5.title', sims: ['cleancode.testDesign'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'j6', titleKey: 'track.cleancode.j6.title', sims: ['cleancode.refactor'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'j7', titleKey: 'track.cleancode.j7.title', sims: ['cleancode.bisect'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'cleancode-fits', model: 'cleancode.fits', titleKey: 'track.cleancode.preset.fits' },
    { id: 'cleancode-names', model: 'cleancode.names', titleKey: 'track.cleancode.preset.names' },
    { id: 'cleancode-parse', model: 'cleancode.parse', titleKey: 'track.cleancode.preset.parse' },
    { id: 'cleancode-tdd', model: 'cleancode.tdd', titleKey: 'track.cleancode.preset.tdd' },
    { id: 'cleancode-testDesign', model: 'cleancode.testDesign', titleKey: 'track.cleancode.preset.testDesign' },
    { id: 'cleancode-refactor', model: 'cleancode.refactor', titleKey: 'track.cleancode.preset.refactor' },
    { id: 'cleancode-bisect', model: 'cleancode.bisect', titleKey: 'track.cleancode.preset.bisect' }
  ],
  logKinds: ['observe', 'run', 'write', 'skip', 'exception', 'complete'],
  labels: ['stable', 'version', 'impl', 'simplified', 'guideline'],
  glossaryNs: 'cleancode', misconceptionsNs: 'cleancode'
});
