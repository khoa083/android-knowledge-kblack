# Sinh tracks/animation/content.vi.js và content.en.js từ MỘT nguồn (cùng cây khoá ở hai ngôn ngữ).
# Chạy: python dev/gen/animation_content.py
import json, os, unicodedata
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = 'track.animation.'
E = []
def a(k, vi, en): E.append((P + k, vi, en))
def m(model, k, vi, en): a('m.' + model + '.' + k, vi, en)
def steps(model, rows):
    # rows: (id, title_vi, title_en, explain_vi, explain_en, ev_vi, ev_en) ; None = bỏ
    for r in rows:
        sid, tv, te, xv, xe, ev, ee = r
        if tv: m(model, 's.' + sid + '.title', tv, te)
        if xv: m(model, 's.' + sid + '.explain', xv, xe)
        if ev: m(model, 'ev.' + sid, ev, ee)
def common(model, title, overview, wrapup, simp, hint, dtitle, ddesc):
    m(model, 'title', *title); m(model, 'overview', *overview); m(model, 'wrapup', *wrapup); m(model, 'simp.1', *simp)
    m(model, 'ctl.hint', *hint); m(model, 'diagramTitle', *dtitle); m(model, 'diagramDesc', *ddesc)

# ---------- chung ----------
a('title', 'Compose Animation Lab', 'Compose Animation Lab')
a('summary', 'Từ target state đến giá trị theo từng frame: chọn API, AnimationSpec, gesture và các phase của Compose.', 'From target state to per-frame values: choosing APIs, AnimationSpec, gestures, and Compose phases.')
a('preset.spec', 'Animation · phòng thí nghiệm AnimationSpec', 'Animation · AnimationSpec lab')
a('preset.retarget', 'Animation · đổi target giữa chừng', 'Animation · changing the target mid-way')
a('preset.gesture', 'Animation · kéo, fling và quay về', 'Animation · drag, fling and return')
a('preset.phaseread', 'Animation · đọc giá trị ở phase nào', 'Animation · which phase reads the value')
a('kind.target-change', 'đổi target', 'target change')
a('col.subject', 'Thành phần', 'Component')
for k, vi, en in [('target', 'target mới', 'new target'), ('running', 'đang chạy', 'running'), ('animating', 'đang animate', 'animating'), ('snapped', 'nhảy thẳng', 'jumps'),
                  ('settled', 'đã ổn định', 'settled'), ('inComp', 'trong Composition', 'in Composition'), ('outComp', 'ngoài Composition', 'out of Composition'),
                  ('exiting', 'đang exit', 'exiting'), ('entering', 'đang enter', 'entering'), ('rerun', 'chạy', 'runs'),
                  ('skipped', 'bỏ qua', 'skipped'), ('moved', 'bị đẩy theo', 'pushed along'), ('overlap', 'có thể bị chồng', 'may overlap')]:
    a('st.' + k, vi, en)

# ---------- lab ----------
L = lambda k, vi, en: a('lab.' + k, vi, en)
L('title.retarget', 'Lab: target và current', 'Lab: target and current')
L('title.spec', 'Lab: AnimationSpec', 'Lab: AnimationSpec')
L('title.gesture', 'Lab: kéo, fling, quay về', 'Lab: drag, fling, return')
L('preview', 'Xem trước', 'Preview'); L('puck', 'Vật thể đang animate', 'The animated object')
L('values', 'Giá trị', 'Values'); L('graph', 'Giá trị theo thời gian', 'Value over time')
L('graphDesc', 'Đường liền: giá trị đã chạy; đường đứt: đường đi dự kiến từ thời điểm hiện tại; vạch ngang: target.', 'Solid line: values so far; dashed line: the expected path from now; horizontal mark: the target.')
for k, vi, en in [('time', 'Thời gian', 'Time'), ('current', 'Hiện tại (current)', 'Current'), ('target', 'Target', 'Target'), ('velocity', 'Vận tốc', 'Velocity'), ('frame', 'Khoảng frame', 'Frame interval'), ('pointer', 'Pointer', 'Pointer')]:
    L('row.' + k, vi, en)
L('ctl.play', 'Phát', 'Play'); L('ctl.pause', 'Tạm dừng', 'Pause'); L('ctl.step', 'Tiến 1 frame', 'Step frame'); L('ctl.restart', 'Chạy lại', 'Restart')
L('ctl.retarget', 'Đổi target giữa chừng', 'Change target mid-way'); L('ctl.reverse', 'Đảo target', 'Reverse target'); L('ctl.reset', 'Đặt lại', 'Reset')
L('ctl.frame', 'Khoảng frame (minh họa)', 'Frame interval (illustrative)'); L('ctl.frameN', '{n} ms', '{n} ms')
L('ctl.slider', 'Target mới', 'New target')
L('ctl.drag', 'Kéo sang phải', 'Drag right'); L('ctl.touch', 'Chạm (dừng animation)', 'Touch (stop the animation)'); L('ctl.release', 'Thả (fling)', 'Release (fling)')
L('ctl.flingV', 'Vận tốc khi thả', 'Release velocity')
L('hint.gesture', 'Kéo vật thể bằng chuột hoặc ngón tay, hoặc dùng các nút; khi vật thể có focus, phím mũi tên kéo và Enter thả.', 'Drag the object with a mouse or finger, or use the buttons; with the object focused, arrow keys drag and Enter releases.')
L('spec.type', 'Spec', 'Spec')
for k, vi, en in [('spring', 'spring', 'spring'), ('tween', 'tween', 'tween'), ('keyframes', 'keyframes', 'keyframes'), ('repeat', 'repeatable', 'repeatable'), ('infinite', 'infiniteRepeatable', 'infiniteRepeatable'), ('snap', 'snap', 'snap'), ('decay', 'exponentialDecay', 'exponentialDecay')]:
    L('spec.type.' + k, vi, en)
L('spec.damping', 'dampingRatio', 'dampingRatio'); L('spec.damping.n', '{name} ({v})', '{name} ({v})')
L('spec.stiffness', 'stiffness', 'stiffness'); L('spec.stiffness.n', 'Stiffness{name} ({v})', 'Stiffness{name} ({v})')
L('spec.duration', 'durationMillis', 'durationMillis'); L('spec.durationN', '{n} ms', '{n} ms'); L('spec.durationDefault', '{n} ms (mặc định)', '{n} ms (default)')
L('spec.easing', 'easing', 'easing'); L('spec.mode', 'repeatMode', 'repeatMode'); L('spec.iterations', 'iterations', 'iterations')
L('spec.delay', 'delayMillis', 'delayMillis'); L('spec.multiplier', 'frictionMultiplier', 'frictionMultiplier'); L('spec.v0', 'Vận tốc ban đầu', 'Initial velocity'); L('spec.v0N', '{n} /s', '{n} /s')
L('unit.ms', '{n} ms', '{n} ms'); L('unit.perS', '{n} /s', '{n} /s')
L('val.dismissed', 'đã bị loại (dismissed)', 'dismissed'); L('val.dragging', 'đang kéo (pointer điều khiển)', 'dragging (pointer in control)')
L('val.noVelocity', '— (mô hình không định nghĩa vận tốc cho spec này)', '— (the model does not define velocity for this spec)')
L('val.paused', 'dừng (stop)', 'stopped')
L('clock.pointer', 'Giá trị pointer', 'Pointer value'); L('clock.anim', 'Giá trị animation', 'Animation value')
L('log', 'Nhật ký sự kiện', 'Event log'); L('log.empty', 'Chưa có sự kiện. Bấm Phát hoặc Tiến 1 frame.', 'No events yet. Press Play or Step frame.')
L('code', 'Mã Kotlin tương ứng', 'Matching Kotlin code')
L('simp.title', 'Mô phỏng đang giản lược điều gì', 'What this simulation simplifies')
L('simp.1', 'Bỏ qua density, layout thật, frame scheduler, vector converter và chi tiết interruption của Compose; kết quả không khớp từng frame với Compose.', 'It leaves out density, real layout, the frame scheduler, vector converters and Compose interruption details; results do not match Compose frame by frame.')
L('simp.2', 'Spring là dao động điều hòa tắt dần với khối lượng 1: ω0 = √stiffness, hệ số tắt 2·ζ·ω0, ba nghiệm cho ζ < 1, ζ = 1, ζ > 1. Tween dùng cubic-bezier; keyframes nội suy tuyến tính giữa các mốc. Decay theo công thức của `FloatExponentialDecaySpec` (androidx-main, đọc 2026-11-21). [[badge:simplified]] [[src:an-decay-src]]', 'Spring is a damped harmonic oscillator with mass 1: ω0 = √stiffness, damping coefficient 2·ζ·ω0, three solutions for ζ < 1, ζ = 1, ζ > 1. Tween uses cubic-bezier; keyframes interpolate linearly between marks. Decay follows the `FloatExponentialDecaySpec` formula (androidx-main, read 2026-11-21). [[badge:simplified]] [[src:an-decay-src]]')
L('simp.3', 'Khoảng frame 8/16/33 ms chỉ là minh họa, không phải tần số màn hình hay số đo. Vận tốc chỉ hiện với spring và decay, nơi mô hình định nghĩa được nó.', 'The 8/16/33 ms frame intervals are illustrative, not a display rate or a measurement. Velocity is shown only for spring and decay, where the model can define it.')
for k, vi, en in [('ev.start', 'bắt đầu {from} → {to}', 'start {from} → {to}'),
                  ('ev.retargetSpring', 'target {from} → {to}; giữ vận tốc {v} /s', 'target {from} → {to}; velocity {v} /s kept'),
                  ('ev.retargetOther', 'target {from} → {to}; chạy tiếp từ giá trị hiện tại (minh họa)', 'target {from} → {to}; continues from the current value (illustrative)'),
                  ('ev.settle', 'ổn định ở {v} sau {t} ms', 'settled at {v} after {t} ms'),
                  ('ev.stop', 'stop() tại {v}: animation cũ bị hủy (CancellationException)', 'stop() at {v}: the running animation is cancelled (CancellationException)'),
                  ('ev.snap', 'snapTo({v})', 'snapTo({v})'),
                  ('ev.back', 'thả với {v} /s; decay dự đoán {p}, trong biên → animateTo(0, initialVelocity)', 'released at {v} /s; decay predicts {p}, within bounds → animateTo(0, initialVelocity)'),
                  ('ev.fling', 'thả với {v} /s; decay dự đoán {p}, ngoài biên → animateDecay', 'released at {v} /s; decay predicts {p}, out of bounds → animateDecay'),
                  ('ev.dismissed', 'decay dừng ở {v}: vật thể bị loại', 'decay stopped at {v}: the object is dismissed')]:
    L(k, vi, en)
m('retarget', 'title', 'Target và current: đổi target giữa chừng', 'Target and current: changing the target mid-way')
m('spec', 'title', 'Cùng start và target, khác spec', 'Same start and target, different spec')
m('gesture', 'title', 'Animatable và cử chỉ kéo', 'Animatable and drag gestures')

# ---------- C0 choose ----------
M = 'choose'
common(M, ('Chọn API theo nhu cầu', 'Choosing an API by need'), ('Chọn một nhu cầu; mô hình gợi ý API, lý do và chỗ chồng lấp.', 'Pick a need; the model suggests an API, the reason and where APIs overlap.'),
       ('Cây quyết định giúp bắt đầu nhanh, nhưng các API chồng lấp nhau; chọn theo việc bạn cần điều khiển: target, nhiều thuộc tính, sự có mặt trong Composition hay cử chỉ.', 'The decision tree helps you start quickly, but APIs overlap; choose by what you need to control: a target, several properties, presence in the Composition or a gesture.'),
       ('Chỉ giữ các nhánh chính của cây trong tài liệu; bỏ qua AnimatedVectorDrawable, Lottie và Navigation.', 'Only the main branches of the documented tree are kept; AnimatedVectorDrawable, Lottie and Navigation are left out.'),
       ('Chọn nhu cầu.', 'Pick a need.'), ('Từ nhu cầu tới API', 'From need to API'), ('Nhu cầu, API gợi ý và lựa chọn thay thế.', 'The need, the suggested API and an alternative.'))
m(M, 'ctl.need', 'Nhu cầu', 'Need')
NEEDS = {
 'one': ('một giá trị đi theo target', 'one value following a target', 'animate*AsState', 'Một thuộc tính độc lập, target do state quyết định.', 'One independent property whose target is decided by state.', 'Nếu cần dừng, snap hay chạy tuần tự, `Animatable` hợp hơn.', 'If you need to stop, snap or run in sequence, `Animatable` fits better.'),
 'many': ('nhiều thuộc tính cùng một state', 'several properties for one state', 'updateTransition', 'Nhiều thuộc tính cần bắt đầu cùng nhau theo một state.', 'Several properties must start together for one state.', 'Thuộc tính độc lập nhau thì vài `animate*AsState` cũng được.', 'If the properties are independent, a few `animate*AsState` calls also work.'),
 'visibility': ('hiện/ẩn', 'showing/hiding', 'AnimatedVisibility', 'Hiện/ẩn và rời Composition sau khi exit kết thúc.', 'Show/hide, leaving the Composition after the exit finishes.', '`animateFloatAsState` với `Modifier.alpha()` cũng làm mờ được, nhưng nội dung vẫn ở trong Composition.', '`animateFloatAsState` with `Modifier.alpha()` can fade too, but the content stays in the Composition.'),
 'content': ('đổi nội dung', 'switching content', 'AnimatedContent / Crossfade', 'Đổi giữa các layout theo một target state.', 'Switch between layouts by a target state.', '`Crossfade` đơn giản hơn; `AnimatedContent` cho chỉnh `ContentTransform` và `SizeTransform`.', '`Crossfade` is simpler; `AnimatedContent` lets you tune `ContentTransform` and `SizeTransform`.'),
 'size': ('kích thước nội dung', 'content size', 'Modifier.animateContentSize', 'Kích thước của nội dung thay đổi.', 'The size of the content changes.', 'Nếu chỉ cần hiệu ứng lúc vẽ, `graphicsLayer` scale không đổi layout (C5).', 'If you only need a draw-time effect, `graphicsLayer` scale does not change layout (C5).'),
 'list': ('item trong danh sách', 'list items', 'Modifier.animateItem()', 'Item trong lazy list được thêm, xóa, đổi chỗ.', 'Items in a lazy list are added, removed or reordered.', 'Site chỉ nhắc tên API này, không mô phỏng; xem trang danh sách của tài liệu.', 'The site only names this API and does not simulate it; see the lists page of the documentation.'),
 'gesture': ('cử chỉ, fling', 'gestures, flings', 'Animatable', 'Giá trị do cử chỉ điều khiển, cần stop, snapTo, animateDecay.', 'A gesture-driven value that needs stop, snapTo and animateDecay.', 'Một số trường hợp có component dựng sẵn; tài liệu gợi ý `Animatable` khi có một nguồn sự thật cho giá trị.', 'Some cases have ready-made components; the documentation suggests `Animatable` when the value has a single source of truth.'),
 'infinite': ('lặp vô hạn', 'infinite repetition', 'rememberInfiniteTransition', 'Animation lặp mãi khi composable còn trong Composition.', 'An animation that repeats while the composable stays in the Composition.', '`infiniteRepeatable` là spec dùng được trong các API khác.', '`infiniteRepeatable` is a spec usable in other APIs.'),
 'lowlevel': ('điều khiển mức thấp', 'low-level control', 'Animation / TargetBasedAnimation / AnimationState', 'Khi có lý do cụ thể, ví dụ tự quản lý thời gian chơi.', 'When there is a specific reason, such as managing play time yourself.', 'Phần lớn ứng dụng không cần mức này.', 'Most apps do not need this level.'),
}
for n, (lv, le, api, wv, we, av, ae) in NEEDS.items():
    m(M, 'ctl.need.' + n, lv, le); m(M, 'need.' + n, 'Nhu cầu: ' + lv + '.', 'Need: ' + le + '.')
    m(M, 'apiName.' + n, api, api); m(M, 'api.' + n, 'Gợi ý: `' + api.split(' / ')[0] + '`. ' + wv, 'Suggested: `' + api.split(' / ')[0] + '`. ' + we)
    m(M, 'alt.' + n, av, ae)
for k, vi, en in [('need', 'Nhu cầu', 'Need'), ('api', 'API gợi ý', 'Suggested API'), ('alt', 'Chồng lấp / thay thế', 'Overlap / alternative')]:
    m(M, 'n.' + k, vi, en)
steps(M, [('need', 'Bạn cần gì?', 'What do you need?', None, None, None, None), ('api', 'API gợi ý', 'Suggested API', None, None, None, None),
          ('alt', 'Chỗ chồng lấp', 'Where APIs overlap', None, None, 'lựa chọn thay thế', 'alternative')])
m(M, 'st.api', 'API', 'API')
m(M, 'co.try', 'Đổi "Nhu cầu" để xem các nhánh khác.', 'Change "Need" to see other branches.')
m(M, 'co.source', 'Theo cây quyết định của trang "Choose an animation API". [[src:an-choose]]', 'Following the decision tree on the "Choose an animation API" page. [[src:an-choose]]')
m(M, 'co.notRule', 'Đây là gợi ý để bắt đầu, không phải luật cứng.', 'This is a starting suggestion, not a hard rule.')

# ---------- C3 transition ----------
M = 'transition'
common(M, ('Một state, nhiều thuộc tính', 'One state, several properties'), ('Card chuyển giữa Collapsed và Expanded; màu, chiều cao, alpha là ba child animation của cùng một Transition. Tắt từng child để thấy chúng độc lập.', 'A card moves between Collapsed and Expanded; color, height and alpha are three child animations of one Transition. Turn each child off to see that they are independent.'),
       ('Transition gom các child theo một state, nhưng mỗi child có spec riêng và có thể không animate; Transition chỉ ổn định khi mọi child đã xong.', 'A Transition groups children under one state, but each child has its own spec and may not animate at all; the Transition settles only when every child is done.'),
       ('Thời lượng là con số minh họa; mô hình không vẽ giá trị từng frame của từng child.', 'Durations are illustrative numbers; the model does not draw per-frame values of each child.'),
       ('Đổi hướng hoặc tắt child.', 'Change direction or turn children off.'), ('Transition và các child', 'The Transition and its children'), ('State đổi; Transition điều khiển ba child.', 'The state changes; the Transition drives three children.'))
m(M, 'ctl.dir', 'Hướng', 'Direction'); m(M, 'ctl.dir.expand', 'Collapsed → Expanded', 'Collapsed → Expanded'); m(M, 'ctl.dir.collapse', 'Expanded → Collapsed', 'Expanded → Collapsed')
m(M, 'ctl.color', 'Animate màu', 'Animate color'); m(M, 'ctl.size', 'Animate chiều cao', 'Animate height'); m(M, 'ctl.alpha', 'Animate alpha', 'Animate alpha')
for k, vi, en in [('state', 'cardState', 'cardState'), ('transition', 'Transition', 'Transition'), ('color', 'color', 'color'), ('size', 'height', 'height'), ('alpha', 'alpha', 'alpha')]:
    m(M, 'n.' + k, vi, en)
m(M, 'met.children', 'Child đang animate', 'Animating children'); m(M, 'met.ms', 'Thời lượng (ms, minh họa)', 'Duration (ms, illustrative)')
m(M, 's.target.title', 'targetState: {from} → {to}', 'targetState: {from} → {to}')
m(M, 's.target.explain', '`updateTransition(cardState)` nhận target mới; currentState vẫn là {from} cho tới khi mọi child xong.', '`updateTransition(cardState)` receives a new target; currentState stays {from} until every child is done.')
m(M, 'ev.target', 'targetState = {to}', 'targetState = {to}')
m(M, 'st.current', 'currentState', 'currentState'); m(M, 'st.targetS', 'targetState', 'targetState')
m(M, 'co.try', 'Tắt "Animate chiều cao" rồi đi lại: chiều cao nhảy thẳng, màu và alpha vẫn animate.', 'Turn off "Animate height" and walk through again: height jumps, color and alpha still animate.')
for p, vi, en in [('color', 'Child: màu', 'Child: color'), ('size', 'Child: chiều cao', 'Child: height'), ('alpha', 'Child: alpha', 'Child: alpha')]:
    m(M, 's.prop.' + p + '.title', vi, en)
m(M, 's.prop.color.tween', 'Màu animate bằng spec mặc định của child (ở đây là tween minh họa).', 'Color animates with the child\'s spec (an illustrative tween here).')
m(M, 's.prop.alpha.tween', 'Alpha animate bằng tween minh họa.', 'Alpha animates with an illustrative tween.')
m(M, 's.prop.size.spring', 'Khi mở rộng, chiều cao dùng `spring()` qua `transitionSpec`: spec có thể khác theo hướng chuyển.', 'When expanding, height uses `spring()` through `transitionSpec`: the spec can differ by direction.')
m(M, 's.prop.size.tween', 'Khi thu gọn, chiều cao dùng tween minh họa.', 'When collapsing, height uses an illustrative tween.')
m(M, 's.prop.off', 'Child này đã tắt trong sandbox: giá trị nhảy thẳng tới đích. Transition không buộc mọi thuộc tính phải animate giống nhau.', 'This child is turned off in the sandbox: its value jumps straight to the target. A Transition does not force every property to animate the same way.')
for p, vi, en in [('color', 'màu', 'color'), ('size', 'chiều cao', 'height'), ('alpha', 'alpha', 'alpha')]:
    m(M, 'ch.' + p, vi + ' đi dần tới giá trị của target', en + ' moves towards the target value')
    m(M, 'ch.' + p + '.snap', vi + ' nhảy thẳng tới giá trị của target', en + ' jumps to the target value')
m(M, 'ev.anim.tween', 'tween ~{ms} ms', 'tween ~{ms} ms'); m(M, 'ev.anim.spring', 'spring ~{ms} ms (minh họa)', 'spring ~{ms} ms (illustrative)'); m(M, 'ev.snap', 'không animate', 'not animated')
m(M, 'sk.anim', 'Animation của child', 'The child animation'); m(M, 'sk.off', 'đã tắt trong sandbox', 'turned off in the sandbox')
m(M, 's.settle.title', 'Transition ổn định ở {to}', 'The Transition settles at {to}')
m(M, 's.settle.explain', 'Khi child chậm nhất xong (~{ms} ms trong mô hình), currentState bằng targetState.', 'When the slowest child is done (~{ms} ms in the model), currentState equals targetState.')
m(M, 'ev.settle', 'currentState = targetState', 'currentState = targetState')
m(M, 'co.settle', '`Transition.currentState` bằng `targetState` khi đã ổn định. [[src:an-value]]', '`Transition.currentState` equals `targetState` once settled. [[src:an-value]]')

# ---------- C4 visibility ----------
M = 'visibility'
common(M, ('Ai còn trong Composition?', 'Who is still in the Composition?'), ('Bật/tắt banner bằng AnimatedVisibility, hoặc đổi nội dung A → B bằng AnimatedContent/Crossfade; theo dõi nội dung nào còn trong Composition.', 'Toggle a banner with AnimatedVisibility, or switch content A → B with AnimatedContent/Crossfade; track which content is still in the Composition.'),
       ('Nội dung rời Composition khi animation của API đó kết thúc, không phải lúc alpha bắt đầu giảm; trong lúc đổi nội dung, cũ và mới cùng có mặt.', 'Content leaves the Composition when that API\'s animation finishes, not when alpha starts to drop; while content switches, old and new are both present.'),
       ('Thời lượng 300 ms là minh họa; mô hình không vẽ enter/exit từng frame.', 'The 300 ms duration is illustrative; the model does not draw enter/exit frame by frame.'),
       ('Chọn API và thao tác.', 'Pick an API and an action.'), ('Trigger, transition và nội dung', 'Trigger, transition and content'), ('Trigger đổi target; transition điều khiển nội dung A và B.', 'The trigger changes the target; the transition drives content A and B.'))
m(M, 'ctl.api', 'API', 'API'); m(M, 'ctl.api.visibility', 'AnimatedVisibility', 'AnimatedVisibility'); m(M, 'ctl.api.content', 'AnimatedContent', 'AnimatedContent'); m(M, 'ctl.api.crossfade', 'Crossfade', 'Crossfade')
m(M, 'ctl.action', 'Thao tác (AnimatedVisibility)', 'Action (AnimatedVisibility)'); m(M, 'ctl.action.hide', 'ẩn banner', 'hide the banner'); m(M, 'ctl.action.show', 'hiện banner', 'show the banner')
m(M, 'ctl.outside', 'Thêm animate*AsState ngoài Transition', 'Add animate*AsState outside the Transition')
m(M, 'ctl.lambda', 'Dùng tham số của content lambda', 'Use the content lambda parameter')
for k, vi, en in [('trigger', 'Trigger', 'Trigger'), ('transition', 'Transition', 'Transition'), ('a', 'Nội dung A / banner', 'Content A / banner'), ('b', 'Nội dung B', 'Content B')]:
    m(M, 'n.' + k, vi, en)
m(M, 's.vtrigger.title', 'visible đổi', 'visible changes')
m(M, 's.vtrigger.hide', '`visible` thành false: exit transition bắt đầu.', '`visible` becomes false: the exit transition starts.')
m(M, 's.vtrigger.show', '`visible` thành true: nội dung vào Composition và enter transition bắt đầu.', '`visible` becomes true: the content enters the Composition and the enter transition starts.')
m(M, 'ev.vtrigger', 'visible đổi', 'visible changes')
steps(M, [('exit', 'Exit đang chạy', 'The exit is running', 'Mặc định là fade + shrink. Banner mờ dần nhưng vẫn còn trong Composition.', 'The default is fade + shrink. The banner fades but is still in the Composition.', 'exit: fadeOut + shrinkVertically', 'exit: fadeOut + shrinkVertically'),
          ('outside', 'Animation ngoài Transition', 'An animation outside the Transition', 'Một `animate*AsState` riêng cho alpha không thuộc Transition của AnimatedVisibility.', 'A separate `animate*AsState` for alpha does not belong to the AnimatedVisibility Transition.', 'animate*AsState không được theo dõi', 'animate*AsState not tracked'),
          ('removed', 'Banner rời Composition', 'The banner leaves the Composition', 'Khi exit của Transition kết thúc, AnimatedVisibility gỡ nội dung khỏi Composition.', 'When the Transition exit finishes, AnimatedVisibility removes the content from the Composition.', 'gỡ khỏi Composition', 'removed from the Composition'),
          ('enter', 'Enter đang chạy', 'The enter is running', 'Nội dung đã ở trong Composition ngay từ đầu enter; mặc định fade + expand.', 'The content is in the Composition from the start of the enter; the default is fade + expand.', 'enter: fadeIn + expandVertically', 'enter: fadeIn + expandVertically'),
          ('shown', 'Banner hiện đầy đủ', 'The banner is fully shown', 'Enter kết thúc.', 'The enter finishes.', 'enter xong', 'enter finished')])
m(M, 'st.inComp', 'Trong Composition', 'In Composition'); m(M, 'val.yes', 'có', 'yes'); m(M, 'val.no', 'không', 'no')
m(M, 'co.outside', 'Animation tạo bằng `animate*AsState` ngoài Transition không được AnimatedVisibility theo dõi, nên nội dung có thể bị gỡ trước khi animation đó xong. [[src:an-composables]]', 'Animations created with `animate*AsState` outside the Transition are not tracked by AnimatedVisibility, so the content can be removed before they finish. [[src:an-composables]]')
m(M, 'ch.removed', 'Banner bị gỡ khỏi Composition', 'The banner is removed from the Composition'); m(M, 'ch.added', 'Banner được thêm vào Composition', 'The banner is added to the Composition')
m(M, 'co.notAlpha', 'Không rút gọn thành "alpha = 0 là bị xóa ngay": thời điểm rời Composition tùy API và transition. [[src:an-composables]]', 'Do not reduce this to "alpha = 0 means removed at once": when content leaves depends on the API and the transition. [[src:an-composables]]')
m(M, 's.ctrigger.title', 'targetState đổi A → B', 'targetState changes A → B')
m(M, 's.ctrigger.content', '`AnimatedContent(targetState = page)` nhận target mới.', '`AnimatedContent(targetState = page)` receives a new target.')
m(M, 's.ctrigger.crossfade', '`Crossfade(targetState = page)` nhận target mới.', '`Crossfade(targetState = page)` receives a new target.')
m(M, 'ev.ctrigger', 'page = B', 'page = B')
m(M, 's.both.title', 'A và B cùng có mặt', 'A and B are both present')
m(M, 's.both.content', 'Trong lúc chuyển, A đang exit và B đang enter; mặc định là fade-through. Content lambda được gọi cho từng state với tham số riêng.', 'During the switch, A exits while B enters; the default is a fade-through. The content lambda is called for each state with its own parameter.')
m(M, 's.both.crossfade', 'Crossfade làm mờ A và hiện B cùng lúc.', 'Crossfade fades A out and B in at the same time.')
m(M, 'ev.both', 'A exit, B enter', 'A exits, B enters'); m(M, 'st.present', 'Đang có mặt', 'Present')
m(M, 'ch.bAdded', 'B được thêm vào Composition', 'B is added to the Composition')
m(M, 'co.lambdaOk', 'Content lambda dùng tham số `target`, nên phần đang exit vẫn hiển thị A. [[src:an-composables]]', 'The content lambda uses its `target` parameter, so the exiting part still shows A. [[src:an-composables]]')
m(M, 'co.lambdaWrong', 'Content lambda đọc `page` từ bên ngoài thay vì tham số: phần đang exit cũng hiện B. Tài liệu yêu cầu luôn dùng tham số của lambda. [[src:an-composables]]', 'The content lambda reads `page` from outside instead of its parameter: the exiting part shows B too. The documentation says to always use the lambda parameter. [[src:an-composables]]')
m(M, 's.swap.title', 'A rời Composition', 'A leaves the Composition')
m(M, 's.swap.explain', 'Chuyển xong, chỉ còn B.', 'The switch is done; only B remains.')
m(M, 's.swap.wrong', 'Chuyển xong, chỉ còn B; nhưng trong lúc chuyển, phần exit đã hiện sai nội dung.', 'The switch is done; only B remains, but during the switch the exiting part showed the wrong content.')
m(M, 'ev.swap', 'gỡ A', 'remove A'); m(M, 'ch.aRemoved', 'A bị gỡ khỏi Composition', 'A is removed from the Composition')
m(M, 'co.try', 'Thử "ẩn banner" rồi bật "Thêm animate*AsState ngoài Transition".', 'Try "hide the banner", then turn on "Add animate*AsState outside the Transition".')
m(M, 'co.actionVisOnly', 'Thao tác ẩn/hiện chỉ áp dụng cho AnimatedVisibility.', 'The hide/show action applies only to AnimatedVisibility.')
m(M, 'co.outsideVisOnly', 'Animation ngoài Transition chỉ áp dụng cho AnimatedVisibility.', 'The outside animation applies only to AnimatedVisibility.')
m(M, 'co.contentOnly', '"Dùng tham số của content lambda" chỉ áp dụng cho AnimatedContent.', '"Use the content lambda parameter" applies only to AnimatedContent.')
m(M, 'co.hideOnly', 'Animation ngoài Transition chỉ gây vấn đề khi ẩn (exit).', 'The outside animation only matters when hiding (exit).')

# ---------- C5 size ----------
M = 'size'
common(M, ('Đổi kích thước thật hay chỉ lúc vẽ', 'Real size change or draw-time only'), ('Card mở rộng theo ba cách: `animateContentSize`, `graphicsLayer` scale, hoặc `offset {}`. Xem phase nào chạy mỗi frame và card bên cạnh ra sao.', 'A card grows in three ways: `animateContentSize`, `graphicsLayer` scale, or `offset {}`. See which phase runs each frame and what happens to the card next to it.'),
       ('Đổi kích thước thật đi qua Layout nên phần tử khác được đẩy theo; transform lúc vẽ không đổi layout nên có thể chồng lên phần tử khác.', 'A real size change goes through Layout, so other elements move along; a draw-time transform does not change layout, so it can overlap other elements.'),
       ('Mô hình giả định mỗi frame đều đổi giá trị; số frame là minh họa.', 'The model assumes the value changes every frame; the frame count is illustrative.'),
       ('Chọn cách animate và số frame.', 'Pick the approach and the frame count.'), ('Card, phase và phần tử bên cạnh', 'The card, the phases and its neighbour'), ('Card đổi qua Layout hoặc chỉ qua Draw; phần tử bên cạnh phản ứng theo.', 'The card changes through Layout or only Draw; its neighbour reacts.'))
m(M, 'simp.2', '`offset {}` đọc giá trị ở bước đặt vị trí của Layout (không đo lại); mô hình gộp nó vào nhóm "không đổi kích thước layout".', '`offset {}` reads the value in the placement step of Layout (no re-measure); the model groups it with "no layout size change".')
m(M, 'ctl.how', 'Cách animate', 'Approach'); m(M, 'ctl.how.contentSize', 'animateContentSize()', 'animateContentSize()'); m(M, 'ctl.how.scale', 'graphicsLayer { scaleY }', 'graphicsLayer { scaleY }'); m(M, 'ctl.how.offset', 'offset { }', 'offset { }')
m(M, 'ctl.frames', 'Số frame', 'Frames'); m(M, 'ctl.frames.3', '3', '3'); m(M, 'ctl.frames.5', '5', '5')
for k, vi, en in [('card', 'Card', 'Card'), ('layout', 'Layout (đo, đặt)', 'Layout (measure, place)'), ('draw', 'Draw', 'Draw'), ('sibling', 'Card bên cạnh', 'Neighbouring card')]:
    m(M, 'n.' + k, vi, en)
m(M, 'met.layouts', 'Lượt layout', 'Layout passes'); m(M, 'met.draws', 'Lượt draw', 'Draw passes')
m(M, 's.toggle.title', 'Mở rộng card', 'Expand the card')
m(M, 's.toggle.contentSize', '`animateContentSize()` đặt trước `height(...)`: kích thước đổi dần và được báo cho layout.', '`animateContentSize()` placed before `height(...)`: the size changes gradually and is reported to layout.')
m(M, 's.toggle.scale', '`graphicsLayer { scaleY = s }`: chỉ phóng to lúc vẽ; kích thước layout vẫn là 72.dp.', '`graphicsLayer { scaleY = s }`: scaled only when drawing; the layout size stays 72.dp.')
m(M, 's.toggle.offset', '`offset { }`: dời vị trí ở bước đặt; cha không đặt lại các con khác.', '`offset { }`: moves the position in the placement step; the parent does not re-place the other children.')
m(M, 'ev.toggle', 'expanded = true', 'expanded = true')
m(M, 'co.try', 'So "animateContentSize()" với "graphicsLayer": nhìn đèn Layout và card bên cạnh.', 'Compare "animateContentSize()" with "graphicsLayer": watch the Layout light and the neighbouring card.')
m(M, 's.frame.title', 'Frame {n}', 'Frame {n}')
m(M, 's.frame.layout', 'Kích thước mới được đo và đặt; card bên cạnh bị đẩy theo, rồi vẽ.', 'The new size is measured and placed; the neighbouring card is pushed along, then drawn.')
m(M, 's.frame.draw', 'Không đo lại; chỉ vẽ với transform mới.', 'No re-measure; only drawn with the new transform.')
for f in range(1, 6): m(M, 'ev.f%d' % f, 'đo và đặt lại', 'measure and place again')
m(M, 'ev.noLayout', 'layout không đổi', 'layout unchanged'); m(M, 'ev.draw', 'vẽ', 'draw')
m(M, 'sk.layout', 'Đo và đặt lại', 'Re-measure and re-place'); m(M, 'sk.drawOnly', 'giá trị chỉ được đọc lúc vẽ hoặc lúc đặt vị trí', 'the value is read only when drawing or placing')
m(M, 's.result.title', 'Kết quả với phần tử bên cạnh', 'The result for the neighbour')
m(M, 's.result.layout', 'Card bên cạnh dời xuống theo kích thước mới.', 'The neighbouring card moves down with the new size.')
m(M, 's.result.draw', 'Card bên cạnh đứng yên; card đang animate có thể vẽ chồng lên nó.', 'The neighbouring card stays put; the animating card may draw over it.')
m(M, 'ev.result', 'xong', 'done')
m(M, 'co.order', 'Đặt `animateContentSize()` trước các modifier kích thước như `size`, `defaultMinSize` để giá trị animation được báo cho layout. [[src:an-composables]] [[src:an-quick]]', 'Place `animateContentSize()` before size modifiers such as `size` and `defaultMinSize` so the animated value is reported to layout. [[src:an-composables]] [[src:an-quick]]')
m(M, 'co.overlap', '`offset {}` không đổi cách cha đặt con nên các phần tử có thể chồng nhau; `Modifier.layout {}` thì truyền thay đổi lên cha. [[src:an-quick]]', '`offset {}` does not change how the parent places the child, so elements may overlap; `Modifier.layout {}` propagates the change to the parent. [[src:an-quick]]')

# ---------- C7 phaseread ----------
M = 'phaseread'
common(M, ('Đọc giá trị animation ở đâu', 'Where the animated value is read'), ('Cùng một giá trị `x` từ `animateFloatAsState`, đọc ở ba chỗ. Đếm phase chạy mỗi frame.', 'The same `x` value from `animateFloatAsState`, read in three places. Count the phases run each frame.'),
       ('Đọc trong thân composable: có thể recompose mỗi frame. Đọc trong `offset {}`: chỉ layout (đặt vị trí) và draw. Đọc trong `graphicsLayer {}`: chỉ draw. Chọn phase phù hợp và đo trước khi tối ưu.', 'Read in the composable body: it can recompose every frame. Read in `offset {}`: only layout (placement) and draw. Read in `graphicsLayer {}`: draw only. Pick the right phase and measure before optimising.'),
       ('Bộ đếm là minh họa cho ví dụ này, không phải số đo hiệu năng.', 'The counters are illustrative for this example, not performance measurements.'),
       ('Chọn nơi đọc và số frame.', 'Pick the read site and the frame count.'), ('Giá trị animation và ba phase', 'The animated value and three phases'), ('Giá trị animation đi tới Composition, Layout hoặc Draw tùy nơi đọc.', 'The animated value reaches Composition, Layout or Draw depending on where it is read.'))
m(M, 'simp.2', 'Không có số FPS hay thời gian: chỉ đếm phase nào chạy.', 'No FPS or timings: only which phases run is counted.')
m(M, 'ctl.where', 'Đọc x ở', 'Read x in'); m(M, 'ctl.where.composition', 'composition: Modifier.offset(x.dp)', 'composition: Modifier.offset(x.dp)'); m(M, 'ctl.where.layout', 'layout: Modifier.offset { }', 'layout: Modifier.offset { }'); m(M, 'ctl.where.draw', 'draw: graphicsLayer { }', 'draw: graphicsLayer { }')
m(M, 'ctl.frames', 'Số frame', 'Frames'); m(M, 'ctl.frames.3', '3', '3'); m(M, 'ctl.frames.5', '5', '5')
for k, vi, en in [('anim', 'x (animation)', 'x (animation)'), ('comp', 'Composition', 'Composition'), ('layout', 'Layout', 'Layout'), ('draw', 'Draw', 'Draw')]:
    m(M, 'n.' + k, vi, en)
m(M, 'met.comp', 'Recomposition', 'Recompositions'); m(M, 'met.layout', 'Layout', 'Layouts'); m(M, 'met.draw', 'Draw', 'Draws')
m(M, 's.where.title', 'x được đọc ở đâu?', 'Where is x read?')
m(M, 's.where.composition', '`Modifier.offset(x = x.dp)` đọc `x` ngay trong thân composable, tức là trong Composition.', '`Modifier.offset(x = x.dp)` reads `x` in the composable body, that is, during Composition.')
m(M, 's.where.layout', '`Modifier.offset { }` đọc `x` trong lambda chạy ở bước đặt vị trí của Layout.', '`Modifier.offset { }` reads `x` in a lambda that runs in the placement step of Layout.')
m(M, 's.where.draw', '`graphicsLayer { translationX = x }` đọc `x` trong lambda chạy ở phase draw.', '`graphicsLayer { translationX = x }` reads `x` in a lambda that runs in the draw phase.')
for k, vi, en in [('composition', 'đọc trong composition', 'read in composition'), ('layout', 'đọc trong layout', 'read in layout'), ('draw', 'đọc trong draw', 'read in draw')]:
    m(M, 'ev.where.' + k, vi, en)
m(M, 'co.try', 'Đổi "Đọc x ở" và so bộ đếm Recomposition.', 'Change "Read x in" and compare the Recompositions counter.')
m(M, 's.frame.title', 'Frame {n}', 'Frame {n}')
m(M, 's.frame.composition', 'Giá trị mới làm scope đọc nó recompose, rồi layout và draw.', 'The new value recomposes the scope that reads it, then layout and draw run.')
m(M, 's.frame.layout', 'Không recompose; chỉ đặt lại vị trí rồi vẽ.', 'No recompose; only re-place and draw.')
m(M, 's.frame.draw', 'Không recompose, không layout; chỉ vẽ lại với translation mới.', 'No recompose, no layout; only redraw with the new translation.')
m(M, 'ev.frame', 'frame {n}', 'frame {n}'); m(M, 'ev.run', 'chạy', 'runs'); m(M, 'ev.skip', 'bỏ qua', 'skipped')
m(M, 'sk.comp', 'Recomposition', 'Recomposition'); m(M, 'sk.notRead', 'không đọc x trong Composition', 'x is not read during Composition')
m(M, 's.measure.title', 'Chọn phase, rồi đo', 'Pick the phase, then measure')
m(M, 's.measure.explain', 'Hoãn việc đọc sang `offset {}` hay `graphicsLayer {}` thường giảm việc mỗi frame, nhưng không phải mọi recomposition đều cần tránh.', 'Deferring the read to `offset {}` or `graphicsLayer {}` usually reduces work per frame, but not every recomposition needs to be avoided.')
m(M, 'ev.measure', 'kết thúc', 'end')
m(M, 'co.measure', 'Không có mẹo "luôn tránh recomposition": đo để xác nhận bottleneck trước khi đổi mã. [[src:an-quick]] [[badge:guideline]]', 'There is no "always avoid recomposition" rule: measure to confirm the bottleneck before changing code. [[src:an-quick]] [[badge:guideline]]')
m(M, 'co.x3', 'Animation tiến theo frame clock (cầu nối X3, chương B5); `withFrameNanos` là API low-level, phần lớn ứng dụng dùng API high-level. [[src:rt-frameclock]]', 'Animations advance with the frame clock (bridge X3, chapter B5); `withFrameNanos` is a low-level API and most apps use high-level APIs. [[src:rt-frameclock]]')

# ---------- C8 testclock ----------
M = 'testclock'
common(M, ('Đồng hồ test và giá trị trung gian', 'The test clock and intermediate values'), ('Một tween 300 ms (FastOutSlowInEasing) từ 0 tới 100 trong test. Tắt autoAdvance và nhảy tới 0/25/50/75/100% thời lượng.', 'A 300 ms tween (FastOutSlowInEasing) from 0 to 100 in a test. Turn off autoAdvance and jump to 0/25/50/75/100% of the duration.'),
       ('`mainClock` cho test kiểm soát thời gian animation; `advanceTimeBy` làm tròn lên bội số của frame duration. Đồng hồ test không điều khiển mọi thứ của Android host.', '`mainClock` lets a test control animation time; `advanceTimeBy` rounds up to a multiple of the frame duration. The test clock does not control everything on the Android host.'),
       ('Frame duration 16 ms trong mô hình là minh họa; tài liệu không nêu con số.', 'The 16 ms frame duration in the model is illustrative; the documentation does not give a number.'),
       ('Bật/tắt autoAdvance và chọn mốc thời gian.', 'Toggle autoAdvance and pick a time mark.'), ('Test, đồng hồ và animation', 'The test, the clock and the animation'), ('Test điều khiển mainClock; mainClock điều khiển animation.', 'The test drives mainClock; mainClock drives the animation.'))
m(M, 'simp.2', 'Giá trị trung gian tính bằng mô hình tween của site, không phải chạy Compose thật.', 'Intermediate values come from the site\'s tween model, not from running Compose.')
m(M, 'ctl.auto', 'autoAdvance', 'autoAdvance'); m(M, 'ctl.at', 'Nhảy tới', 'Jump to')
for v in [0, 25, 50, 75, 100]: m(M, 'ctl.at.%d' % v, '%d%% (%d ms)' % (v, 3 * v), '%d%% (%d ms)' % (v, 3 * v))
for k, vi, en in [('test', 'Test', 'Test'), ('clock', 'mainClock', 'mainClock'), ('anim', 'Animation', 'Animation')]:
    m(M, 'n.' + k, vi, en)
m(M, 'met.value', 'Giá trị đọc được', 'Value read'); m(M, 'met.clock', 'Đồng hồ (ms)', 'Clock (ms)')
steps(M, [('start', 'Test bắt đầu animation', 'The test starts the animation', 'Composable được dựng trong `createComposeRule()`; animation bắt đầu.', 'The composable is set up in `createComposeRule()`; the animation starts.', 'bắt đầu', 'start'),
          ('auto', 'autoAdvance: đồng hồ tự chạy', 'autoAdvance: the clock runs by itself', 'Với autoAdvance bật (mặc định), test đồng bộ cho tới khi animation xong; lúc kiểm tra, giá trị đã là 100.', 'With autoAdvance on (the default), the test synchronises until the animation is done; when asserting, the value is already 100.', 'đồng hồ tự tiến tới khi xong', 'the clock advances until done'),
          ('paused', 'autoAdvance = false', 'autoAdvance = false', 'Đồng hồ đứng yên; animation dừng ở giá trị ban đầu tới khi test tự tiến thời gian.', 'The clock stands still; the animation stays at its initial value until the test advances time.', 'đồng hồ dừng', 'clock paused'),
          ('advance', 'advanceTimeBy({req})', 'advanceTimeBy({req})', 'Yêu cầu {req} ms; đồng hồ thực sự tiến {real} ms. Giá trị lúc đó là {v}.', 'Requested {req} ms; the clock actually moves {real} ms. The value at that moment is {v}.', 'đồng hồ = {real} ms', 'clock = {real} ms'),
          ('assert', 'Kiểm tra giá trị trung gian', 'Assert the intermediate value', 'Test so giá trị {v} với kỳ vọng tính cho {real} ms, không phải cho {req} ms.', 'The test compares the value {v} with the expectation for {real} ms, not {req} ms.', 'assert ở {real} ms', 'assert at {real} ms'),
          ('limits', 'Đồng hồ test kiểm soát gì', 'What the test clock controls', 'Nó điều khiển thời gian của animation trong Compose test; không điều khiển mọi thứ của host Android. `infiniteRepeatable` không chạy trong ComposeTestRule.', 'It controls animation time inside the Compose test; it does not control everything on the Android host. `infiniteRepeatable` does not run in ComposeTestRule.', 'giới hạn', 'limits')])
m(M, 'st.value', 'Giá trị', 'Value'); m(M, 'st.req', 'Yêu cầu', 'Requested'); m(M, 'st.real', 'Đồng hồ thực tiến', 'Clock actually moved')
m(M, 'co.try', 'Tắt autoAdvance rồi chọn 25%: 75 ms được làm tròn lên.', 'Turn off autoAdvance, then pick 25%: 75 ms is rounded up.')
m(M, 'co.round', '`advanceTimeBy` không tiến đúng số ms yêu cầu mà làm tròn lên bội số gần nhất của frame duration. [[src:an-testing]]', '`advanceTimeBy` does not move by exactly the requested amount; it rounds up to the nearest multiple of the frame duration. [[src:an-testing]]')
m(M, 'co.limits', 'Infinite animation không chạy trong ComposeTestRule và hiển thị giá trị ban đầu. [[src:an-customize]]', 'Infinite animations do not run in ComposeTestRule and render their initial value. [[src:an-customize]]')
m(M, 'co.x6', 'Giảm chuyển động cho người dùng là chuyện của ứng dụng (cầu nối X6: WCAG 2.3.3 "Animation from Interactions", chương E10); site này cũng có nút "Giảm chuyển động".', 'Reducing motion for users is the app\'s job (bridge X6: WCAG 2.3.3 "Animation from Interactions", chapter E10); this site also has a "Reduce motion" button.')
m(M, 'co.atIgnored', 'Với autoAdvance bật, mốc "Nhảy tới" không có tác dụng: đồng hồ tự chạy tới khi animation xong.', 'With autoAdvance on, the "Jump to" mark has no effect: the clock runs until the animation is done.')

# ---------- chương ----------
def ch(c, title, essence, g1, g2, secs, quiz):
    a(c + '.title', *title); a(c + '.essence', *essence); a(c + '.goal.g1', *g1); a(c + '.goal.g2', *g2)
    for sid, stitle, badge, paras in secs:
        a(c + '.sec.' + sid + '.title', *stitle); a(c + '.sec.' + sid + '.badge', badge, badge)
        for i, p in enumerate(paras): a(c + '.sec.' + sid + '.p.' + str(i + 1), *p)
    for i, (q, ans, why) in enumerate(quiz):
        a(c + '.quiz.q%d.q' % (i + 1), *q); a(c + '.quiz.q%d.a' % (i + 1), *ans); a(c + '.quiz.q%d.why' % (i + 1), *why)

ch('c0', ('Chọn API trong 30 giây', 'Choosing an API in 30 seconds'),
   ('UI state hoặc target đổi → API animation xác định điểm bắt đầu và đích → AnimationSpec quy định cách tính theo thời gian → animation sinh current value theo từng frame → composable, modifier, layout hoặc draw dùng giá trị đó → Compose cập nhật các phase cần thiết.\nCây quyết định trong tài liệu giúp chọn API nhanh; các API chồng lấp nhau, nên đó là gợi ý, không phải luật cứng.',
    'UI state or a target changes → the animation API sets a start and an end → the AnimationSpec defines how to compute over time → the animation produces a current value each frame → a composable, modifier, layout or draw uses that value → Compose updates the needed phases.\nThe decision tree in the documentation helps pick an API quickly; APIs overlap, so it is a suggestion, not a hard rule.'),
   ('Đã xem API gợi ý cho một nhu cầu', 'Looked at the suggested API for one need'), ('Đã xem chỗ chồng lấp', 'Looked at where APIs overlap'),
   [('pairs', ('Bảy cặp cần phân biệt', 'Seven pairs to tell apart'), 'stable', [
      ('model state ↔ animated value; target ↔ current; spec (cách tính) ↔ state holder (giữ giá trị, như `Animatable`); Transition ↔ từng thuộc tính; animation layout ↔ transform lúc vẽ; animation do state ↔ animation do cử chỉ; đối tượng tính giá trị ↔ API quản lý vòng đời (như `AnimatedVisibility`). [[src:an-intro]] [[src:an-value]]',
       'model state ↔ animated value; target ↔ current; spec (how to compute) ↔ state holder (holding the value, such as `Animatable`); Transition ↔ each property; layout animation ↔ draw-time transform; state-driven ↔ gesture-driven animation; the object that computes values ↔ the API that manages lifecycle (such as `AnimatedVisibility`). [[src:an-intro]] [[src:an-value]]'),
      ('Cây quyết định: một thuộc tính theo target → `animate*AsState`; nhiều thuộc tính bắt đầu cùng nhau → `updateTransition`; hiện/ẩn → `AnimatedVisibility`; đổi layout → `AnimatedContent`/`Crossfade`; kích thước → `animateContentSize`; item danh sách → `animateItem()`; cử chỉ → `Animatable`; lặp vô hạn → `rememberInfiniteTransition`. [[src:an-choose]]',
       'The decision tree: one property following a target → `animate*AsState`; several properties starting together → `updateTransition`; show/hide → `AnimatedVisibility`; switching layouts → `AnimatedContent`/`Crossfade`; size → `animateContentSize`; list items → `animateItem()`; gestures → `Animatable`; infinite repetition → `rememberInfiniteTransition`. [[src:an-choose]]'),
      ('Cầu nối X7: chuyển động nên có mục đích; nguyên tắc chuyển động của Material nằm ở chương E9.', 'Bridge X7: motion should have a purpose; Material motion principles live in chapter E9.')])],
   [(('Cây quyết định có phải luật bắt buộc?', 'Is the decision tree a mandatory rule?'), ('Không.', 'No.'), ('Các API chồng lấp; ví dụ mờ dần có thể dùng `AnimatedVisibility` hoặc `animateFloatAsState` + alpha, với hệ quả khác nhau.', 'APIs overlap; fading, for example, can use `AnimatedVisibility` or `animateFloatAsState` + alpha, with different consequences.')),
    (('Cử chỉ kéo và fling nên dùng gì?', 'What fits drag and fling gestures?'), ('`Animatable`.', '`Animatable`.'), ('Nó có `stop`, `snapTo`, `animateDecay` điều khiển bằng suspend API.', 'It has `stop`, `snapTo` and `animateDecay`, driven by suspend APIs.'))])

ch('c1', ('Từ target đến animation value', 'From target to animation value'),
   ('`animate*AsState` nhận target và trả về giá trị animation; target là đích, current là giá trị đang hiển thị.\nKhi target đổi giữa chừng, `animate*AsState` chạy tiếp từ current value và current velocity; với spring, vận tốc liên tục.\nKhông phải API nào cũng có cùng ngữ nghĩa khi bị ngắt, và không phải API nào cũng buộc recomposition mỗi frame (X1).',
    '`animate*AsState` takes a target and returns an animated value; the target is the destination, current is what is on screen.\nWhen the target changes mid-way, `animate*AsState` continues from the current value and velocity; with a spring, velocity stays continuous.\nNot every API has the same interruption semantics, and not every API forces recomposition every frame (X1).'),
   ('Đã mở lab', 'Opened the lab'), ('Đã đổi target trong lúc animation đang chạy', 'Changed the target while the animation was running'),
   [('retarget', ('Đổi target giữa chừng', 'Changing the target mid-way'), 'stable', [
      ('Theo trang value-based, nếu target đổi khi đang chạy, `animate*AsState` bắt đầu từ giá trị và vận tốc hiện tại tới target mới; bạn không phải tự xử lý việc ngắt. Spring là spec mặc định. [[src:an-value]]',
       'According to the value-based page, if the target changes while running, `animate*AsState` starts from the current value and velocity towards the new target; you do not handle the interruption yourself. Spring is the default spec. [[src:an-value]]'),
      ('Trong lab, chọn tween rồi đổi target: mô hình chạy tween mới từ giá trị hiện tại với vận tốc 0. Đó là minh họa; tài liệu chỉ bảo đảm việc tiếp tục từ current value và velocity, không mô tả đường đi từng frame cho mọi spec. [[badge:simplified]]',
       'In the lab, pick tween and change the target: the model runs a new tween from the current value with zero velocity. That is illustrative; the documentation only guarantees continuing from the current value and velocity, not the per-frame path for every spec. [[badge:simplified]]'),
      ('So với `Animatable`: khi cần snap, stop, decay hay chạy tuần tự, `Animatable` cho điều khiển trực tiếp (C6). Giá trị đọc trong `offset { }` không làm recompose mỗi frame (C7, cầu nối X1).',
       'Compared with `Animatable`: when you need snap, stop, decay or sequences, `Animatable` gives direct control (C6). A value read in `offset { }` does not recompose every frame (C7, bridge X1).')])],
   [(('Target có phải giá trị đang hiển thị?', 'Is the target the value on screen?'), ('Không.', 'No.'), ('Target là đích; current đi dần về target theo spec.', 'The target is the destination; current moves towards it following the spec.')),
    (('Đổi target giữa chừng với spring: vận tốc có bị đặt về 0?', 'Changing the target mid-way with a spring: is velocity reset to 0?'), ('Không.', 'No.'), ('Spring giữ vận tốc liên tục khi đổi target.', 'A spring keeps velocity continuous when the target changes.'))])

ch('c2', ('AnimationSpec và đường cong', 'AnimationSpec and curves'),
   ('Giữ nguyên start và target, chỉ đổi spec: spring (damping, stiffness), tween (duration, easing), keyframes, repeatable/infiniteRepeatable, snap, decay.\nHằng số trong lab lấy từ API reference của animation-core (pin 1.13.0); điểm điều khiển của easing và công thức decay lấy từ mã nguồn AndroidX, gắn nhãn implementation.\nVận tốc chỉ hiện khi mô hình định nghĩa được nó (spring, decay).',
    'Keep start and target, change only the spec: spring (damping, stiffness), tween (duration, easing), keyframes, repeatable/infiniteRepeatable, snap, decay.\nConstants in the lab come from the animation-core API reference (pinned to 1.13.0); easing control points and the decay formula come from the AndroidX source and are labelled implementation.\nVelocity is shown only where the model can define it (spring, decay).'),
   ('Đã mở lab', 'Opened the lab'), ('Đã so ít nhất hai spec', 'Compared at least two specs'),
   [('spring', ('spring và tween: giá trị mặc định', 'spring and tween: default values'), 'stable', [
      ('`spring()` mặc định dùng `Spring.DampingRatioNoBouncy` (1.0, critically damped) và `Spring.StiffnessMedium` (1500). Các hằng có tên khác: damping 0.2 (HighBouncy), 0.5 (MediumBouncy), 0.75 (LowBouncy); stiffness 400 (MediumLow), 200 (Low), 50 (VeryLow). [[src:an-spring]] [[src:an-pkg]]',
       '`spring()` defaults to `Spring.DampingRatioNoBouncy` (1.0, critically damped) and `Spring.StiffnessMedium` (1500). Other named constants: damping 0.2 (HighBouncy), 0.5 (MediumBouncy), 0.75 (LowBouncy); stiffness 400 (MediumLow), 200 (Low), 50 (VeryLow). [[src:an-spring]] [[src:an-pkg]]'),
      ('`tween()` mặc định: `DefaultDurationMillis` = 300 ms, không delay, `FastOutSlowInEasing`. [[src:an-constants]] [[src:an-pkg]] Theo mã nguồn (androidx-main, đọc 2026-11-21), `FastOutSlowInEasing` là cubic-bezier (0.4, 0, 0.2, 1), `LinearOutSlowInEasing` (0, 0, 0.2, 1), `FastOutLinearInEasing` (0.4, 0, 1, 1). [[badge:impl]] [[src:an-easing-src]]',
       '`tween()` defaults: `DefaultDurationMillis` = 300 ms, no delay, `FastOutSlowInEasing`. [[src:an-constants]] [[src:an-pkg]] According to the source (androidx-main, read 2026-11-21), `FastOutSlowInEasing` is cubic-bezier (0.4, 0, 0.2, 1), `LinearOutSlowInEasing` (0, 0, 0.2, 1), `FastOutLinearInEasing` (0.4, 0, 1, 1). [[badge:impl]] [[src:an-easing-src]]'),
      ('Spring không "tốt hơn" tween trong mọi trường hợp: spring hợp khi target có thể đổi giữa chừng; tween cho thời lượng xác định, có thể khớp token thời lượng và easing của design system (cầu nối X7, E9). [[src:an-customize]]',
       'Spring is not "better" than tween in every case: spring suits targets that may change mid-way; tween gives a fixed duration that can match the design system\'s duration and easing tokens (bridge X7, E9). [[src:an-customize]]')]),
    ('more', ('keyframes, lặp, snap, decay', 'keyframes, repetition, snap, decay'), 'stable version', [
      ('`keyframes` nội suy giữa các mốc thời gian; `keyframesWithSpline` làm mượt giữa các mốc, có từ animation-core 1.6.0 (overload `periodicBias` từ 1.7.0). Lab nội suy tuyến tính giữa các mốc và không mô phỏng spline. [[src:an-customize]] [[src:an-pkg]] [[badge:version]]',
       '`keyframes` interpolates between time marks; `keyframesWithSpline` smooths between marks and exists since animation-core 1.6.0 (the `periodicBias` overload since 1.7.0). The lab interpolates linearly between marks and does not simulate splines. [[src:an-customize]] [[src:an-pkg]] [[badge:version]]'),
      ('`repeatable(iterations, …, RepeatMode.Restart | Reverse)`; `infiniteRepeatable` lặp mãi; `snap(delayMillis)` nhảy tới đích sau delay. `exponentialDecay()` mặc định frictionMultiplier 1.0 và ngưỡng vận tốc 0.1; mã nguồn dùng friction −4.2 × multiplier và vận tốc giảm theo hàm mũ. [[src:an-decayspec]] [[src:an-decay-src]] [[badge:impl]]',
       '`repeatable(iterations, …, RepeatMode.Restart | Reverse)`; `infiniteRepeatable` repeats forever; `snap(delayMillis)` jumps to the end after a delay. `exponentialDecay()` defaults to frictionMultiplier 1.0 and a velocity threshold of 0.1; the source uses friction −4.2 × multiplier and velocity decays exponentially. [[src:an-decayspec]] [[src:an-decay-src]] [[badge:impl]]'),
      ('Nâng cao: giá trị được đổi sang `AnimationVector` (1D–4D) qua `TwoWayConverter`, mỗi chiều có vận tốc riêng; lab chỉ dùng một chiều. [[src:an-customize]]',
       'Advanced: values are converted to an `AnimationVector` (1D–4D) through a `TwoWayConverter`, each dimension with its own velocity; the lab uses one dimension only. [[src:an-customize]]')])],
   [(('Giá trị mặc định của `tween()`?', 'What are the defaults of `tween()`?'), ('300 ms, không delay, `FastOutSlowInEasing`.', '300 ms, no delay, `FastOutSlowInEasing`.'), ('Theo package summary và `AnimationConstants`.', 'According to the package summary and `AnimationConstants`.')),
    (('Vì sao lab không hiện vận tốc cho tween?', 'Why does the lab not show velocity for tween?'), ('Mô hình không định nghĩa vận tốc cho spec đó.', 'The model does not define velocity for that spec.'), ('Chỉ hiện số khi mô hình giải thích đúng được.', 'Numbers are shown only when the model can explain them correctly.'))])

ch('c3', ('Một giá trị, nhiều giá trị, và Transition', 'One value, many values, and Transition'),
   ('`animate*AsState` cho thuộc tính độc lập; `updateTransition` cho nhiều giá trị đi theo một state.\n`transitionSpec` có thể khác theo hướng chuyển; dùng label để debug.\nTransition không buộc mọi thuộc tính giống nhau: mỗi child có spec riêng, có thể không animate.',
    '`animate*AsState` for independent properties; `updateTransition` for several values following one state.\n`transitionSpec` can differ by direction; use labels for debugging.\nA Transition does not force every property to behave the same: each child has its own spec and may not animate.'),
   ('Đã thấy các child animate', 'Saw the children animate'), ('Đã tắt một child', 'Turned one child off'),
   [('t', ('updateTransition', 'updateTransition'), 'stable', [
      ('`updateTransition` tạo một Transition từ một giá trị state; child animation dùng `animateColor`, `animateDp`, `animateFloat`… `transitionSpec` chọn spec theo cặp state; `Transition.currentState` bằng `targetState` khi đã ổn định. [[src:an-value]]',
       '`updateTransition` creates a Transition from a state value; children use `animateColor`, `animateDp`, `animateFloat`… `transitionSpec` picks a spec per pair of states; `Transition.currentState` equals `targetState` once settled. [[src:an-value]]'),
      ('Label giúp nhận ra từng child trong công cụ debug của Android Studio (tùy phiên bản).', 'Labels help identify each child in Android Studio debugging tools (version dependent).')])],
   [(('Mọi child của một Transition có phải dùng cùng spec?', 'Must every child of a Transition use the same spec?'), ('Không.', 'No.'), ('Mỗi child có `transitionSpec` riêng, và có thể khác theo hướng chuyển.', 'Each child has its own `transitionSpec`, which can differ by direction.')),
    (('Khi nào currentState bằng targetState?', 'When does currentState equal targetState?'), ('Khi mọi child đã xong.', 'When every child is done.'), ('Transition ổn định theo child chậm nhất.', 'The Transition settles with the slowest child.'))])

ch('c4', ('Hiện/ẩn và đổi nội dung', 'Showing, hiding and switching content'),
   ('`AnimatedVisibility` animate việc hiện/ẩn và gỡ nội dung khỏi Composition sau khi exit kết thúc.\n`AnimatedContent` đổi nội dung theo targetState; phải dùng tham số của content lambda. `Crossfade` là dạng đơn giản.\nThời điểm nội dung rời Composition phụ thuộc API và transition, không phải "alpha 0 là bị xóa ngay".',
    '`AnimatedVisibility` animates showing and hiding and removes the content from the Composition after the exit finishes.\n`AnimatedContent` switches content by targetState; you must use the content lambda parameter. `Crossfade` is the simple form.\nWhen content leaves the Composition depends on the API and transition, not "alpha 0 means removed at once".'),
   ('Đã thấy nội dung còn trong Composition lúc exit', 'Saw the content still in the Composition during exit'), ('Đã thử AnimatedContent', 'Tried AnimatedContent'),
   [('vis', ('AnimatedVisibility và AnimatedContent', 'AnimatedVisibility and AnimatedContent'), 'stable', [
      ('Mặc định enter là fade + expand, exit là fade + shrink. AnimatedVisibility chờ mọi animation trong Transition của nó rồi mới gỡ nội dung; animation `animate*AsState` ngoài Transition không được theo dõi. `animateEnterExit` cho con animation riêng. [[src:an-composables]]',
       'By default enter is fade + expand and exit is fade + shrink. AnimatedVisibility waits for every animation in its Transition before removing content; `animate*AsState` animations outside the Transition are not tracked. `animateEnterExit` gives children their own animation. [[src:an-composables]]'),
      ('`AnimatedContent`: tham số của content lambda là key của nội dung đang hiển thị; `ContentTransform` tạo bằng `togetherWith`, thêm `SizeTransform` bằng `using`; mặc định là fade-through. [[src:an-composables]]',
       '`AnimatedContent`: the content lambda parameter is the key of the content being shown; `ContentTransform` is built with `togetherWith`, and `SizeTransform` is attached with `using`; the default is a fade-through. [[src:an-composables]]')])],
   [(('Alpha về 0 có nghĩa nội dung đã bị gỡ?', 'Does alpha reaching 0 mean the content was removed?'), ('Không nhất thiết.', 'Not necessarily.'), ('AnimatedVisibility gỡ sau khi exit xong; animate alpha bằng `graphicsLayer` thì vẫn còn trong Composition.', 'AnimatedVisibility removes it after the exit finishes; animating alpha with `graphicsLayer` keeps it in the Composition.')),
    (('Trong AnimatedContent nên đọc `page` hay tham số lambda?', 'In AnimatedContent, read `page` or the lambda parameter?'), ('Tham số lambda.', 'The lambda parameter.'), ('Nếu đọc `page`, phần đang exit sẽ hiện nội dung mới.', 'If you read `page`, the exiting part shows the new content.'))])

ch('c5', ('Kích thước, layout và item animation', 'Size, layout and item animation'),
   ('`animateContentSize` đổi kích thước thật, đi qua Layout; thứ tự modifier ảnh hưởng kết quả.\nTransform lúc vẽ (`graphicsLayer`) không đổi layout; `offset {}` đổi vị trí ở bước đặt mà không đổi cách cha đặt con khác.\n`animateItem()` cho item của lazy list: site chỉ nhắc tên và dẫn tài liệu.',
    '`animateContentSize` changes the real size, through Layout; modifier order affects the result.\nDraw-time transforms (`graphicsLayer`) do not change layout; `offset {}` moves in the placement step without changing how the parent places other children.\n`animateItem()` is for lazy list items: the site only names it and points to the documentation.'),
   ('Đã thấy phase chạy mỗi frame', 'Saw which phases run each frame'), ('Đã so layout với graphicsLayer', 'Compared layout with graphicsLayer'),
   [('sz', ('Layout hay Draw', 'Layout or Draw'), 'stable guideline', [
      ('Đặt `animateContentSize()` trước modifier kích thước như `size` hay `defaultMinSize` để giá trị animation được báo cho layout. [[src:an-composables]]', 'Place `animateContentSize()` before size modifiers such as `size` or `defaultMinSize` so the animated value is reported to layout. [[src:an-composables]]'),
      ('Animation đổi layout làm các composable bị ảnh hưởng đo, đặt và vẽ lại; animation ở phase draw tốn ít việc hơn. Alpha bằng `graphicsLayer` giữ composable trong Composition và layout, điều này ảnh hưởng trợ năng. [[src:an-quick]] [[badge:guideline]]', 'An animation that changes layout makes affected composables measure, place and draw again; a draw-phase animation does less work. Alpha with `graphicsLayer` keeps the composable in the Composition and laid out, which affects accessibility. [[src:an-quick]] [[badge:guideline]]'),
      ('Cầu nối X1: phase nào chạy tùy nơi state được đọc (chương B7).', 'Bridge X1: which phase runs depends on where the state is read (chapter B7).')])],
   [(('`graphicsLayer { scaleY }` có đẩy phần tử bên cạnh?', 'Does `graphicsLayer { scaleY }` push its neighbour?'), ('Không.', 'No.'), ('Nó chỉ đổi lúc vẽ; kích thước layout không đổi.', 'It changes only when drawing; the layout size is unchanged.')),
    (('Đặt `animateContentSize()` ở đâu so với `height(...)`?', 'Where does `animateContentSize()` go relative to `height(...)`?'), ('Trước.', 'Before it.'), ('Để giá trị animation được báo cho layout.', 'So the animated value is reported to layout.'))])

ch('c6', ('Animatable và gesture', 'Animatable and gestures'),
   ('`Animatable` là value holder điều khiển bằng suspend API: `animateTo`, `snapTo`, `animateDecay`, `stop`, với `initialVelocity`.\nChạy trong scope phù hợp (`LaunchedEffect` hoặc coroutine của `pointerInput`); không tạo scope detached tùy tiện, không gọi suspend API ngoài coroutine.\nAnimation mới hủy animation đang chạy; khi cử chỉ bắt đầu, dừng animation cũ.',
    '`Animatable` is a value holder driven by suspend APIs: `animateTo`, `snapTo`, `animateDecay`, `stop`, with `initialVelocity`.\nRun it in a suitable scope (`LaunchedEffect` or the `pointerInput` coroutine); do not create detached scopes at will or call suspend APIs outside a coroutine.\nA new animation cancels the running one; when a gesture starts, stop the old animation.'),
   ('Đã mở lab', 'Opened the lab'), ('Đã kéo, thả và chạm để ngắt', 'Dragged, released and touched to interrupt'),
   [('x4', ('Cầu nối X4: Animatable là suspend API', 'Bridge X4: Animatable is a suspend API'), 'stable', [
      ('Gọi `animateTo`/`animateDecay`/`snapTo` khi đang có animation sẽ hủy animation cũ bằng `CancellationException`, và phần còn lại của coroutine gọi nó cũng bị hủy; dùng try/catch nếu cần dọn dẹp. `stop()` dừng tại chỗ, không nhảy tới target. `initialVelocity` của `animateTo` mặc định là `velocity` hiện tại. [[src:an-animatable]]',
       'Calling `animateTo`/`animateDecay`/`snapTo` while an animation runs cancels the old one with a `CancellationException`, and the rest of the calling coroutine is cancelled too; use try/catch if you need cleanup. `stop()` halts in place without jumping to the target. `animateTo`\'s `initialVelocity` defaults to the current `velocity`. [[src:an-animatable]]'),
      ('Vì vậy quy tắc hủy của coroutine áp dụng nguyên vẹn (chương A5): hủy là hợp tác, `CancellationException` phải được ném lại. Chạy tuần tự: gọi nối tiếp các suspend call; chạy đồng thời: dùng coroutine con trong scope phù hợp (chương A2). Các chương A2, A5 chỉ nhắc lại phần này. [[src:an-value]]',
       'So the coroutine cancellation rules apply as-is (chapter A5): cancellation is cooperative and `CancellationException` must be rethrown. Sequential: call the suspend functions one after another; concurrent: use child coroutines in a suitable scope (chapter A2). Chapters A2 and A5 only recap this part. [[src:an-value]]'),
      ('Ví dụ cử chỉ trong tài liệu: chạm → `stop()`; kéo → `snapTo` và `VelocityTracker`; thả → dự đoán đích bằng decay; trong biên thì `animateTo(0f, initialVelocity)`, ngoài biên thì `animateDecay`. Lab theo đúng luồng này với biên ±120 (minh họa). [[src:an-advanced]]',
       'The gesture example in the documentation: touch → `stop()`; drag → `snapTo` and `VelocityTracker`; release → predict the end with decay; within bounds `animateTo(0f, initialVelocity)`, outside bounds `animateDecay`. The lab follows this flow with bounds of ±120 (illustrative). [[src:an-advanced]]')])],
   [(('Gọi `animateTo` khi animation cũ đang chạy thì sao?', 'What happens when you call `animateTo` while an old animation runs?'), ('Animation cũ bị hủy bằng `CancellationException`.', 'The old one is cancelled with a `CancellationException`.'), ('Animatable giữ các animation loại trừ nhau.', 'Animatable keeps its animations mutually exclusive.')),
    (('Pointer value và animation value có là một?', 'Are the pointer value and the animation value the same?'), ('Không.', 'No.'), ('Khi kéo, pointer điều khiển qua `snapTo`; khi thả, animation điều khiển. Lab hiện hai đồng hồ riêng.', 'While dragging, the pointer drives through `snapTo`; after release, the animation drives. The lab shows two separate clocks.'))])

ch('c7', ('Animation, frame clock và phases', 'Animation, the frame clock and phases'),
   ('Animation tiến theo frame; `withFrameNanos` là API low-level, phần lớn ứng dụng dùng API high-level (X3).\nĐọc animated state trong thân composable có thể gây recomposition mỗi lần cập nhật; có thể hoãn việc đọc sang `graphicsLayer {}`, `offset {}` hoặc draw lambda (X1).\nKhông có quy tắc "luôn tránh mọi recomposition": chọn đúng phase và đo để xác nhận bottleneck.',
    'Animations advance frame by frame; `withFrameNanos` is a low-level API and most apps use high-level APIs (X3).\nReading animated state in the composable body can recompose on every update; you can defer the read to `graphicsLayer {}`, `offset {}` or a draw lambda (X1).\nThere is no rule to "always avoid every recomposition": pick the right phase and measure to confirm the bottleneck.'),
   ('Đã chạy vài frame', 'Ran a few frames'), ('Đã so ba nơi đọc', 'Compared the three read sites'),
   [('defer', ('Hoãn việc đọc', 'Deferring the read'), 'stable guideline', [
      ('Ưu tiên dạng lambda của modifier khi có thể: nó bỏ qua recomposition và chạy animation ngoài composition; nếu không, dùng `graphicsLayer { }`, luôn chạy ở phase draw. [[src:an-quick]] [[src:cp-phases]]', 'Prefer the lambda form of a modifier where possible: it skips recomposition and runs the animation outside composition; otherwise use `graphicsLayer { }`, which always runs in the draw phase. [[src:an-quick]] [[src:cp-phases]]'),
      ('Transform ở Draw khác thay đổi constraints hay kích thước ở Layout (C5). Bộ đếm trong mô phỏng là minh họa, không phải số đo hiệu năng.', 'A Draw transform differs from changing constraints or size in Layout (C5). The counters in the simulation are illustrative, not performance measurements.')])],
   [(('Đọc `x` trong `graphicsLayer {}` thì có recompose mỗi frame?', 'Does reading `x` in `graphicsLayer {}` recompose every frame?'), ('Không.', 'No.'), ('Giá trị chỉ được đọc ở phase draw.', 'The value is read only in the draw phase.')),
    (('Có nên tự dùng `withFrameNanos` cho mọi animation?', 'Should you use `withFrameNanos` for every animation?'), ('Không.', 'No.'), ('Đó là API low-level; API high-level đã lo nhịp frame.', 'It is a low-level API; high-level APIs already handle frame timing.'))])

ch('c8', ('Kiểm thử, debug và giảm chuyển động', 'Testing, debugging and reduced motion'),
   ('`ComposeTestRule.mainClock` cho test kiểm soát thời gian; tắt `autoAdvance` để tự tiến bằng `advanceTimeBy`.\n`advanceTimeBy` làm tròn lên bội số của frame duration; infinite animation không chạy trong ComposeTestRule.\nĐồng hồ test không điều khiển mọi thứ của Android host. Debug bằng label và công cụ của Android Studio (tùy phiên bản).',
    '`ComposeTestRule.mainClock` lets a test control time; turn off `autoAdvance` to move it yourself with `advanceTimeBy`.\n`advanceTimeBy` rounds up to a multiple of the frame duration; infinite animations do not run in ComposeTestRule.\nThe test clock does not control everything on the Android host. Debug with labels and Android Studio tools (version dependent).'),
   ('Đã tắt autoAdvance', 'Turned off autoAdvance'), ('Đã thấy việc làm tròn thời gian', 'Saw the time rounding'),
   [('test', ('mainClock', 'mainClock'), 'stable', [
      ('Theo trang Test animations: `mainClock` cho kiểm thử xác định; `autoAdvance = false` tạm dừng animation; `advanceTimeBy` làm tròn lên bội số gần nhất của frame duration. Ví dụ tối ưu test dùng `advanceTimeByFrame()`. [[src:an-testing]]',
       'According to the Test animations page: `mainClock` gives deterministic tests; `autoAdvance = false` pauses animations; `advanceTimeBy` rounds up to the nearest multiple of the frame duration. The test optimisation example uses `advanceTimeByFrame()`. [[src:an-testing]]'),
      ('Cầu nối X6: WCAG 2.3.3 "Animation from Interactions" và thiết kế bao hàm nằm ở chương E10; site này có nút "Giảm chuyển động" và tôn trọng `prefers-reduced-motion`.', 'Bridge X6: WCAG 2.3.3 "Animation from Interactions" and inclusive design live in chapter E10; this site has a "Reduce motion" button and respects `prefers-reduced-motion`.')])],
   [(('`advanceTimeBy(75)` có tiến đúng 75 ms?', 'Does `advanceTimeBy(75)` move exactly 75 ms?'), ('Không nhất thiết.', 'Not necessarily.'), ('Nó làm tròn lên bội số của frame duration.', 'It rounds up to a multiple of the frame duration.')),
    (('`infiniteRepeatable` có chạy trong ComposeTestRule?', 'Does `infiniteRepeatable` run in ComposeTestRule?'), ('Không.', 'No.'), ('Nó hiển thị giá trị ban đầu.', 'It renders its initial value.'))])

def norm(s): return unicodedata.normalize('NFC', s)
# ---- caption sơ đồ ("Bạn đang xem") và nhãn chú giải, thêm 2026-11-21 ----
a('cap.choose', 'Từ trái sang phải: nhu cầu chuyển động → API gợi ý → API chồng lấp hoặc thay thế.', 'Left to right: the motion need → the suggested API → an overlapping or alternative API.')
a('cap.transition', 'Một state (trái) điều khiển một Transition; Transition dẫn các giá trị con (màu, chiều cao, alpha) cùng lúc, nên chúng chuyển động cùng nhịp.', 'One state (left) drives a Transition; the Transition drives its child values (colour, height, alpha) together, so they stay in step.')
a('cap.visibility', 'Trigger đổi visible → AnimatedVisibility chạy hiệu ứng vào hoặc ra cho nội dung bên phải.', 'A trigger changes visible → AnimatedVisibility runs the enter or exit effect for the content on the right.')
a('cap.size', 'Thẻ cha ở trên; đổi kích thước ảnh hưởng tới layout và vẽ (ở dưới), và có thể đẩy phần tử bên cạnh.', 'The parent card on top; a size change affects layout and drawing (below), and can push the neighbouring item.')
a('cap.phaseread', 'Giá trị animation bên trái; ba phase bên phải. Đọc giá trị ở phase nào thì mỗi frame phase đó chạy lại (thẻ nhấn).', 'The animated value on the left; the three phases on the right. Whichever phase reads the value runs again on each animation frame (highlighted card).')
a('cap.testclock', 'Bài test điều khiển đồng hồ; đồng hồ quyết định animation tiến tới frame nào.', 'The test drives the clock; the clock decides which frame the animation reaches.')

# ---------------- v2 (2026-11-23): module chương dài, cùng khuôn với dev/gen/runtime_content.py ----------------
# Mỗi module: add(a) (a(k, vi, en=None)), tuỳ chọn override(o) và SEC_ORDER = {chương: [mục…]}.
import sys
_here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, _here)
def a2(k, vi, en=None): E.append((P + k, vi, vi if en is None else en))
def o2(k, vi, en=None):
    k = P + k
    for i, e in enumerate(E):
        if e[0] == k: E[i] = (k, vi, vi if en is None else en); return
    raise KeyError(k)
for mod in ('animation_v2_c1', 'animation_v2_c2', 'animation_v2_c3', 'animation_v2_c4'):   # thêm module mới vào đây
    if os.path.exists(os.path.join(_here, mod + '.py')):
        mm = __import__(mod)
        mm.add(a2)
        if hasattr(mm, 'override'): mm.override(o2)
        for chap, order in getattr(mm, 'SEC_ORDER', {}).items():
            pre = P + chap + '.sec.'
            idx = [i for i, e in enumerate(E) if e[0].startswith(pre)]
            items = [E[i] for i in idx]
            rank = lambda e: order.index(e[0][len(pre):].split('.')[0]) if e[0][len(pre):].split('.')[0] in order else len(order)
            items.sort(key=rank)
            first = idx[0]; sidx = set(idx)
            E[:] = [e for i, e in enumerate(E) if i not in sidx]
            E[first:first] = items

keys = [k for k, _, _ in E]; dup = [k for k in set(keys) if keys.count(k) > 1]; assert not dup, dup
for lang, idx in (('vi', 1), ('en', 2)):
    body = ',\n'.join('  %s: %s' % (json.dumps(e[0]), json.dumps(norm(e[idx]), ensure_ascii=False)) for e in E)
    txt = '/* Nội dung track Compose Animation (%s). SINH TỰ ĐỘNG từ dev/gen/animation_content.py. */\nADE.addTrackStrings(\'animation\', \'%s\', {\n%s\n});\n' % (lang, lang, body)
    open(os.path.join(ROOT, 'tracks', 'animation', 'content.%s.js' % lang), 'w', encoding='utf-8', newline='\n').write(txt)
print(len(E), 'keys')
