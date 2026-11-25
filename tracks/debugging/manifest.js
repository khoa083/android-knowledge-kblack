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
    { id: 'l4', num: 4, titleKey: 'track.debugging.l4.title', sims: ['debugging.trace'], simAfter: 'hook', bridges: ['X29'], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'debugging-loop', model: 'debugging.loop', titleKey: 'track.debugging.preset.loop' },
    { id: 'debugging-bp', model: 'debugging.bp', titleKey: 'track.debugging.preset.bp' },
    { id: 'debugging-logcat', model: 'debugging.logcat', titleKey: 'track.debugging.preset.logcat' },
    { id: 'debugging-trace', model: 'debugging.trace', titleKey: 'track.debugging.preset.trace' }
  ],
  logKinds: ['observe', 'run', 'write', 'skip', 'exception', 'complete'],
  labels: ['stable', 'version', 'impl', 'simplified', 'guideline'],
  glossaryNs: 'debugging', misconceptionsNs: 'debugging'
});
