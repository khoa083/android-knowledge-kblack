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
    { id: 'j2', titleKey: 'track.cleancode.j2.title', sims: ['cleancode.names'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'cleancode-fits', model: 'cleancode.fits', titleKey: 'track.cleancode.preset.fits' },
    { id: 'cleancode-names', model: 'cleancode.names', titleKey: 'track.cleancode.preset.names' }
  ],
  logKinds: ['observe', 'run', 'write', 'skip', 'exception', 'complete'],
  labels: ['stable', 'version', 'impl', 'simplified', 'guideline'],
  glossaryNs: 'cleancode', misconceptionsNs: 'cleancode'
});
