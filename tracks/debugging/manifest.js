/* Track L: Gỡ lỗi và hiệu năng Android. Nội dung sinh từ dev/gen/debugging_content.py (module debugging_v2_<chương>.py).
   Spec: docs/tracks/L-debugging-performance.md (13 chương, đã duyệt 2026-11-24). Trong lúc viết: status 'draft'.
   num: số hiển thị của chương (khớp id l1…l12; l0 bản đồ viết cuối, đặt đầu). Dạy câu hỏi mà công cụ trả lời, không dạy nút bấm của IDE. */
ADE.registerTrack({
  id: 'debugging', code: 'L', order: 120, domain: 'engineering',
  accent: '#A0523C', icon: 'search',
  titleKey: 'track.debugging.title', summaryKey: 'track.debugging.summary',
  level: 'intermediate', estMinutes: 360, status: 'draft',
  prerequisites: [], languages: ['vi', 'en'],
  chapters: [
    { id: 'l1', num: 1, titleKey: 'track.debugging.l1.title', sims: ['debugging.loop'], simAfter: 'hook', bridges: ['X28'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'l2', num: 2, titleKey: 'track.debugging.l2.title', sims: ['debugging.bp'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'l3', num: 3, titleKey: 'track.debugging.l3.title', sims: ['debugging.logcat'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'l4', num: 4, titleKey: 'track.debugging.l4.title', sims: ['debugging.trace'], simAfter: 'hook', bridges: ['X29'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'l5', num: 5, titleKey: 'track.debugging.l5.title', sims: ['debugging.retrace'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },
    { id: 'l6', num: 6, titleKey: 'track.debugging.l6.title', sims: ['debugging.layout'], simAfter: 'hook', bridges: ['X30'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'l7', num: 7, titleKey: 'track.debugging.l7.title', sims: ['debugging.inspect'], simAfter: 'hook', bridges: ['X31'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'l8', num: 8, titleKey: 'track.debugging.l8.title', sims: ['debugging.leak'], simAfter: 'hook', bridges: ['X32'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'l9', num: 9, titleKey: 'track.debugging.l9.title', sims: ['debugging.jank'], simAfter: 'hook', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'l10', num: 10, titleKey: 'track.debugging.l10.title', sims: ['debugging.anr'], simAfter: 'hook', bridges: ['X33'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'l11', num: 11, titleKey: 'track.debugging.l11.title', sims: ['debugging.net'], simAfter: 'hook', bridges: ['X34'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },
    { id: 'l12', num: 12, titleKey: 'track.debugging.l12.title', sims: ['debugging.measure'], simAfter: 'hook', bridges: ['X35'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'debugging-loop', model: 'debugging.loop', titleKey: 'track.debugging.preset.loop' },
    { id: 'debugging-bp', model: 'debugging.bp', titleKey: 'track.debugging.preset.bp' },
    { id: 'debugging-logcat', model: 'debugging.logcat', titleKey: 'track.debugging.preset.logcat' },
    { id: 'debugging-trace', model: 'debugging.trace', titleKey: 'track.debugging.preset.trace' },
    { id: 'debugging-retrace', model: 'debugging.retrace', titleKey: 'track.debugging.preset.retrace' },
    { id: 'debugging-layout', model: 'debugging.layout', titleKey: 'track.debugging.preset.layout' },
    { id: 'debugging-inspect', model: 'debugging.inspect', titleKey: 'track.debugging.preset.inspect' },
    { id: 'debugging-leak', model: 'debugging.leak', titleKey: 'track.debugging.preset.leak' },
    { id: 'debugging-jank', model: 'debugging.jank', titleKey: 'track.debugging.preset.jank' },
    { id: 'debugging-anr', model: 'debugging.anr', titleKey: 'track.debugging.preset.anr' },
    { id: 'debugging-net', model: 'debugging.net', titleKey: 'track.debugging.preset.net' },
    { id: 'debugging-measure', model: 'debugging.measure', titleKey: 'track.debugging.preset.measure' }
  ],
  logKinds: ['observe', 'run', 'write', 'skip', 'exception', 'complete'],
  labels: ['stable', 'version', 'impl', 'simplified', 'guideline'],
  glossaryNs: 'debugging', misconceptionsNs: 'debugging'
});
