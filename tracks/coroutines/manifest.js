/* Track A: Kotlin Coroutines Explorer. Nội dung song ngữ ở content.vi.js / content.en.js (cùng cây khoá track.coroutines.*). */
ADE.defineKind('block', { tok: 'thread', icon: 'forbidden' });   // chặn luồng (kiểu Thread.sleep), khác với suspend
ADE.defineKind('run', { tok: 'coroutine', icon: 'dot' });        // coroutine đang chạy một đơn vị công việc
ADE.defineKind('check', { tok: 'job', icon: 'eye' });            // điểm kiểm tra hủy (isActive / ensureActive)

ADE.registerTrack({
  id: 'coroutines', code: 'A', order: 10, domain: 'engineering',
  accent: '#2F83BE', icon: 'job',
  titleKey: 'track.coroutines.title', summaryKey: 'track.coroutines.summary',
  level: 'intermediate', estMinutes: 300, status: 'stable',
  prerequisites: [], languages: ['vi', 'en'],
  chapters: [
    { id: 'a0', titleKey: 'track.coroutines.a0.title', sims: ['coroutines.full'], bridges: [], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] },
    { id: 'u1', titleKey: 'track.coroutines.u1.title', sims: ['coroutines.suspend'], simAfter: 'coroutines', bridges: [], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] },   // v2 Phần 1 (Deep Dive "Why Kotlin Coroutines?")
    { id: 'u2', titleKey: 'track.coroutines.u2.title', sims: ['coroutines.seq'], simAfter: 'jump', bridges: [], goals: [{ id: 'g1', step: 5 }, { id: 'g2', step: 'end' }] },   // v2 (Deep Dive "Sequence builder")
    { id: 'u3', titleKey: 'track.coroutines.u3.title', sims: ['coroutines.cont'], simAfter: 'resume', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },   // v2 (Deep Dive "How does suspension work?")
    { id: 'u4', titleKey: 'track.coroutines.u4.title', sims: ['coroutines.sm'], simAfter: 'value', bridges: [], goals: [{ id: 'g1', step: 2 }, { id: 'g2', step: 'end' }] },   // v2 (Deep Dive "Coroutines under the hood" + "built-in support vs library")
    { id: 'a1', titleKey: 'track.coroutines.a1.title', sims: ['coroutines.suspend'], bridges: [], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] },
    { id: 'a2', titleKey: 'track.coroutines.a2.title', sims: ['coroutines.jobstate', 'coroutines.jobtree'], simAfter: 'states', bridges: ['X4'], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] },
    { id: 'a3', titleKey: 'track.coroutines.a3.title', sims: ['coroutines.builders'], simAfter: 'async', bridges: [], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] },
    { id: 'a4', titleKey: 'track.coroutines.a4.title', sims: ['coroutines.context'], simAfter: 'ctx', bridges: ['X3'], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] },
    { id: 'a5', titleKey: 'track.coroutines.a5.title', sims: ['coroutines.cancel'], simAfter: 'unstoppable', bridges: ['X4'], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] },
    { id: 'a6', titleKey: 'track.coroutines.a6.title', sims: ['coroutines.exception'], simAfter: 'ceh', bridges: [], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] },
    { id: 'sf', titleKey: 'track.coroutines.sf.title', sims: ['coroutines.builders'], simAfter: 'cs', bridges: [], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] },   // v2 (Deep Dive "Coroutine scope functions")
    { id: 'ch', titleKey: 'track.coroutines.ch.title', sims: ['coroutines.chan'], simAfter: 'types', bridges: [], goals: [{ id: 'g1', step: 3 }, { id: 'g2', step: 'end' }] },   // v2 (Deep Dive "Channel" + "Select")
    { id: 'fl', titleKey: 'track.coroutines.fl.title', sims: ['coroutines.flowcall', 'coroutines.hotcold'], simAfter: 'under', bridges: [], goals: [{ id: 'g1', step: 4 }, { id: 'g2', step: 'end' }] },   // v2 (Deep Dive "Hot and cold", "Flow introduction", "Understanding Flow")
    { id: 'a7', titleKey: 'track.coroutines.a7.title', sims: ['coroutines.flowpipe', 'coroutines.hotcold'], bridges: [], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] },
    { id: 'a8', titleKey: 'track.coroutines.a8.title', sims: ['coroutines.lifecycle', 'coroutines.effects'], simAfter: 'scopes', bridges: ['X2'], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] },
    { id: 'a9', titleKey: 'track.coroutines.a9.title', sims: ['coroutines.race', 'coroutines.vtime'], simAfter: 'lost', bridges: [], goals: [{ id: 'g1', step: 1 }, { id: 'g2', step: 'end' }] }
  ],
  presets: [
    { id: 'coroutines-full-example', model: 'coroutines.full', titleKey: 'track.coroutines.preset.full' },
    { id: 'coroutines-job-failure', model: 'coroutines.jobtree', titleKey: 'track.coroutines.preset.job' },
    { id: 'coroutines-flow-pipeline', model: 'coroutines.flowpipe', titleKey: 'track.coroutines.preset.flow' },
    { id: 'coroutines-lifecycle', model: 'coroutines.lifecycle', titleKey: 'track.coroutines.preset.lifecycle' },
    { id: 'coroutines-cancel', model: 'coroutines.cancel', titleKey: 'track.coroutines.preset.cancel' },
    { id: 'coroutines-exception', model: 'coroutines.exception', titleKey: 'track.coroutines.preset.exception' }
  ],
  logKinds: ['launch', 'suspend', 'resume', 'block', 'run', 'check', 'cancel', 'complete', 'exception', 'emit', 'collect', 'skip'],
  labels: ['stable', 'impl', 'version', 'guideline', 'simplified'],
  glossaryNs: 'coroutines', misconceptionsNs: 'coroutines'
});
