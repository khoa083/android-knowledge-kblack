# Nghiên cứu Track C: Compose Animation (P4, 2026-11-21)

Mọi URL dưới đây đã đọc trực tiếp ngày 2026-11-21, HTTP 200, không chuyển hướng (trừ ghi chú). Phiên bản chốt: `compose.animation` / `animation-core` 1.13.0 (BOM 2026.11.01).

## Hằng số (dùng trong model; có nguồn)
| Tên | Giá trị | Nguồn |
|---|---|---|
| `Spring.DampingRatioHighBouncy` | 0.2 | reference `Spring` |
| `Spring.DampingRatioMediumBouncy` | 0.5 | reference `Spring` |
| `Spring.DampingRatioLowBouncy` | 0.75 | reference `Spring` |
| `Spring.DampingRatioNoBouncy` | 1.0 (critically damped) | reference `Spring` |
| `Spring.StiffnessMedium` | 1500 | reference `Spring` |
| `Spring.StiffnessMediumLow` | 400 (mặc định cho spring của enter/exit) | reference `Spring` |
| `Spring.StiffnessLow` | 200 | reference `Spring` |
| `Spring.StiffnessVeryLow` | 50 | reference `Spring` |
| `Spring.StiffnessHigh` | **không xác minh được** (reference chỉ ghi khai báo; không tìm thấy trong mã đã đọc) → **không dùng** | — |
| `Spring.DefaultDisplacementThreshold` | 0.01 | reference `Spring` |
| `spring()` mặc định | dampingRatio = NoBouncy, stiffness = StiffnessMedium, visibilityThreshold = null | package summary animation.core; trang customize |
| `tween()` mặc định | durationMillis = `DefaultDurationMillis`, delayMillis = 0, easing = `FastOutSlowInEasing` | package summary |
| `AnimationConstants.DefaultDurationMillis` | 300 | reference `AnimationConstants` |
| `FastOutSlowInEasing` | CubicBezierEasing(0.4, 0.0, 0.2, 1.0) | **mã nguồn** `Easing.kt`, androidx-main, đọc 2026-11-21 (reference không ghi điểm điều khiển) → nhãn `impl` |
| `LinearOutSlowInEasing` | CubicBezierEasing(0.0, 0.0, 0.2, 1.0) | `Easing.kt` (như trên) |
| `FastOutLinearInEasing` | CubicBezierEasing(0.4, 0.0, 1.0, 1.0) | `Easing.kt` (như trên) |
| `LinearEasing` | fraction → fraction | reference + `Easing.kt` |
| `exponentialDecay()` mặc định | frictionMultiplier = 1.0, absVelocityThreshold = 0.1 | reference `FloatExponentialDecaySpec`, package summary |
| Công thức exponential decay | friction = −4.2 × frictionMultiplier; v(t) = v0·e^(friction·t); x(t) = x0 − v0/friction + (v0/friction)·e^(friction·t); thời lượng = ln(threshold/|v0|)/friction | **mã nguồn** `FloatDecayAnimationSpec.kt`, androidx-main, đọc 2026-11-21 → nhãn `impl` |
| `keyframesWithSpline(init)` | thêm ở 1.6.0; overload `periodicBias` ở 1.7.0; reference không ghi experimental | package summary |

Spring trong model: dao động điều hòa tắt dần, khối lượng chuẩn hóa 1, ω0 = √stiffness, hệ số tắt c = 2ζω0; ba nghiệm giải tích (ζ<1, ζ=1, ζ>1). Đây là mô hình giảng dạy của site; không khẳng định khớp từng frame với `SpringSimulation` của Compose.

## Hành vi (khẳng định có nguồn)
- `animate*AsState`: target đổi giữa chừng → bắt đầu từ current value và current velocity tới target mới; spring là spec mặc định (value-based). Spring giữ velocity liên tục khi đổi target (customize, Animatable).
- `Animatable.animateTo/animateDecay/snapTo` khi đang chạy animation khác: animation cũ bị hủy bằng `CancellationException` (hủy phần còn lại của coroutine gọi nó); `stop()` dừng tại chỗ, không nhảy tới target; sau khi kết thúc, velocity về 0; `initialVelocity` mặc định = `velocity`; `updateBounds` kẹp giá trị (reference Animatable).
- Gesture (advanced): `stop()` khi chạm mới; `snapTo` theo kéo; `VelocityTracker`; thả: `decay.calculateTargetValue`, `updateBounds`, `animateTo(0f, initialVelocity)` hoặc `animateDecay`; vị trí đặt bằng `Modifier.offset { }`.
- `AnimatedVisibility`: mặc định fade + expand/shrink; nội dung rời Composition sau khi animation kết thúc; animation ngoài Transition (animate*AsState) không được theo dõi nên nội dung có thể bị gỡ trước khi chúng xong (composables-modifiers).
- `AnimatedContent`: phải dùng tham số của content lambda (targetState) (composables-modifiers).
- `animateContentSize`: đặt **trước** các modifier kích thước như `size`, `defaultMinSize` (composables-modifiers, quick-guide).
- Hiệu năng (quick-guide): ưu tiên dạng lambda của modifier (`offset { }`), hoặc `graphicsLayer { }` (luôn ở phase draw); animation đổi layout làm re-layout và redraw. Alpha bằng `graphicsLayer` vẫn giữ composable trong composition (ảnh hưởng trợ năng); `AnimatedVisibility` gỡ nó.
- `rememberInfiniteTransition`: chạy ngay khi vào composition, không dừng trừ khi bị gỡ (value-based).
- `infiniteRepeatable` không chạy trong `ComposeTestRule`, hiển thị giá trị ban đầu (customize).
- Test: `mainClock`, `autoAdvance = false`, `advanceTimeBy` làm tròn lên bội số của frame duration (testing). `advanceTimeByFrame` xuất hiện trong ví dụ tối ưu test.
- Choose-api: cây quyết định (một thuộc tính → animate*AsState; nhiều thuộc tính bắt đầu cùng nhau → updateTransition; hiện/ẩn → AnimatedVisibility; đổi layout → AnimatedContent/Crossfade; kích thước → animateContentSize; item danh sách → animateItem(); gesture → Animatable; lặp vô hạn → rememberInfiniteTransition). Trang không tự gọi là "luật" → site trình bày như gợi ý, có chồng lấp.

## URL
- `developer.android.com/develop/ui/compose/animation` → **404** (xác nhận lại 2026-11-21); dùng `/animation/introduction` (global.md §3).
- Đã đọc: introduction, choose-api, value-based, composables-modifiers, customize, advanced, testing, quick-guide, reference Animatable, Spring, AnimationConstants, FloatExponentialDecaySpec, package summary animation.core; mã nguồn Easing.kt, FloatDecayAnimationSpec.kt (androidx-main).

## Điểm chưa xác minh / cách xử lý
- `StiffnessHigh`: không dùng.
- `Modifier.animateItem()`: trang composables-modifiers không ghi phiên bản; chỉ nhắc tên và dẫn trang choose-api, không mô phỏng.
- Easing của từng đoạn trong `keyframes` mặc định: không xác minh → model nội suy tuyến tính giữa các mốc, ghi "giản lược".
- `animateFloatAsState` default spec: reference không ghi; trang value-based nói spring là mặc định → dùng câu đó.
- Thời lượng frame: không có hằng số; khoảng frame trong lab là tham số minh họa (8/16/33 ms).

## Checklist mục 7 (Track C) — tick 2026-11-21

| Mục | Ở đâu |
|---|---|
| Phân biệt 7 cặp | C0 `sec.pairs.p.1` |
| Decision tree không phải luật cứng | C0 essence, `m.choose.co.notRule`, quiz q1 |
| Không cùng semantics khi ngắt; không phải API nào cũng recompose mỗi frame | C1 essence, `sec.retarget.p.2/p.3`; C7 |
| Velocity chỉ khi mô hình định nghĩa; tách bảo đảm/minh họa khi đổi target | lab: hàng Vận tốc "—" cho tween/keyframes/snap/repeat (`lab.val.noVelocity`); C1 `sec.retarget.p.2` (`simplified`); nhật ký `ev.retargetOther` ghi "minh họa" |
| `keyframesWithSpline`, `animateItem()` kèm phiên bản/nhãn | C2 `sec.more.p.1` (1.6.0/1.7.0, `version`); `animateItem()` chỉ nhắc tên, ghi rõ không mô phỏng (C0, C5) vì tài liệu đọc được không ghi phiên bản |
| Transition không buộc giống nhau; không "alpha 0 = xóa"; AnimatedContent dùng tham số lambda | model `animation.transition` (tắt child), `animation.visibility` (`co.notAlpha`, `co.lambdaWrong`), misconception `alpha-removed` |
| Thứ tự modifier có nguồn; Layout ≠ Draw | C5 `sec.sz.p.1`, `m.size.co.order`, model `animation.size` |
| Không scope detached; không suspend ngoài coroutine; pointer ≠ animation value | C6 essence, `sec.x4`; lab gesture có hai đồng hồ "Giá trị pointer" / "Giá trị animation" |
| Không "luôn tránh recomposition"; không FPS giả | C7 essence, `m.phaseread.co.measure`, `simp.2`; không có số FPS trong track |
| Test clock không điều khiển mọi thứ; `advanceTimeBy` làm tròn | C8, model `animation.testclock` (selfCheck làm tròn), `co.limits` |
| Công thức, giả định spring/tween/decay; không khớp từng frame; liệt kê phần bỏ qua | `lab.simp.1/2/3`, comment trong `models/physics.js` |
| Hằng số từ API reference, có nguồn; khoảng frame chọn được, nhãn minh họa | `physics.js` (bảng hằng số ở trên), select "Khoảng frame (minh họa)" 8/16/33 ms |
| Hiểu lầm ≥ 8, có ví dụ và nguồn | 9 mục |

Kiến trúc lab: model `kind:'compute'` + `view.mount` (lõi đã hỗ trợ), không sửa `js/core`. Trạng thái lab lưu ở `ADE.animLab.store` nên đổi ngôn ngữ giữ thời điểm/target/spec (đã kiểm). Giảm chuyển động: Phát chuyển tức thời tới trạng thái cuối.

## Animation v2: nguồn đã đối chiếu (2026-11-23)

- Mục lục *Android Animations by Tutorials*, Kunneth Ch.8, Tutorials Ch.12, Essentials Ch.39–41, 50: xem `docs/roadmap-v2.md` mục "Compose Animation v2".
- Trang `animation/choose` trả 404; trang đúng là `animation/choose-api` (cây quyết định: art-based → AnimatedVectorDrawable/Lottie; vô hạn → rememberInfiniteTransition; layout → AnimatedContent/Crossfade/Pager hoặc navigation enter/exitTransition, AnimatedVisibility/CapturedAnimatedVisibility, animateContentSize, animateItem; nhiều thuộc tính → animate*AsState / updateTransition / Animatable; target định trước → animate*AsState; gesture → Animatable; one-shot → AnimationState/animate).
- Trang `tooling/layout-inspector` của Compose trả 404 (dùng `tooling/debug`).
- Thư mục mã ở commit 296313a4: `compose/animation/{animation, animation-core, animation-graphics, …}`; danh sách file `animation-core` và `animation` đã liệt kê (xem roadmap).
- Câu trong bảng hằng số ở trên còn ghi "androidx-main, đọc 2026-11-21" cho `Easing.kt` và `FloatDecayAnimationSpec.kt`: khi viết c2 v2, đọc lại hai file ở commit ghim và sửa thành tham chiếu commit.


### C1 v2 · animate*AsState (2026-11-23)

| Claim | Nguồn | Loại |
|---|---|---|
| StateChangeDemo đổi màu đột ngột; animateColorAsState; finishedListener; colorDefaultSpring; spring(stiffness = VeryLow) | Kunneth Ch.8 | Ví dụ của sách |
| animate as state cho rotation, color, Dp | Essentials Ch.40 | Ví dụ của sách |
| Nền JoinButton animate theo state | Tutorials Ch.12 | Ví dụ của sách |
| rememberCoroutineScope; remember AnimateAsState(Animatable); SideEffect update() trừ lần đầu ("Avoid calling state.update on initial composition"); update so targetValue; restartAnimation: job?.cancel, InterruptionAwareAnimationSpec, launch(UNDISPATCHED) { animateTo; finishedListener }; KDoc: điều chỉnh về target mới, không hủy được nếu không gỡ khỏi cây | `an-aas-src` (@296313a4) | impl |
| Bài viết cũ mô tả Channel + LaunchedEffect: không khớp mã ghim | `an-aas-src` | ghi chú lệch |
| Sim `animation.aas`: 0 / 1 / 2 (1 cancel) / 0 job | Theo mã ghim | selfCheck; số giá trị minh họa |

### C2 v2 · AnimationSpec (2026-11-23)

Đọc lại ở commit ghim 296313a4: `AnimationSpec.kt`, `Easing.kt`, `FloatDecayAnimationSpec.kt`, `SpringSimulation.kt`, `VectorConverters.kt`, `ColorVectorConverter.kt`. URL `an-easing-src`, `an-decay-src` chuyển từ `refs/heads/androidx-main` sang commit ghim (giá trị không đổi: cubic-bezier (0.4, 0, 0.2, 1)…, `ExponentialDecayFriction = -4.2f`, frictionMultiplier 1, absVelocityThreshold 0.1).

| Claim | Nguồn | Loại |
|---|---|---|
| AnimationSpec chỉ có vectorize(converter); FiniteAnimationSpec; tween 300/0/FastOutSlowIn; spring NoBouncy/StiffnessMedium; keyframes LinearEasing mặc định, ArcMode | `an-spec-src` | impl |
| Converter: Float/Int/Dp 1D, Offset/Size/DpOffset 2D, Rect 4D | `an-vectorconv-src` | impl |
| Màu → Oklab, AnimationVector4D(alpha, L, a, b), kẹp khi đổi ngược | `an-colorconv-src` | impl |
| Oklab của đỏ ≈ (.628, .225, .126), trắng (1, 0, 0); FastOutSlowIn(0.5) ≈ 0.776 | Tính bằng công thức chuẩn (site tự tính) | ghi rõ trong simp |
| Spec/easing, spring, keyframes trong ví dụ | Essentials Ch.39–40, Kunneth Ch.8 | Ví dụ của sách |

### C3 v2 · updateTransition (2026-11-23)

| Claim | Nguồn | Loại |
|---|---|---|
| updateTransition = remember Transition + animateTo(target) mỗi lần chạy + DisposableEffect; con mặc định spring, chỉ FiniteAnimationSpec; currentState là initialState tới khi xong; adjust course khi target đổi; chạy lại nếu đích của con đổi; MutableTransitionState cho state đầu khác target, phải remember | `an-transition-src` (@296313a4) | impl |
| JoinButton bốn thuộc tính, updateTransition + animateColor(tween(600)) | Tutorials Ch.12 | Ví dụ của sách |
| borderWidth/degrees; isRunning, segment, currentState | Kunneth Ch.8 | Ví dụ của sách |
| Sim `animation.segment`: currentState đổi ở 400 ms; đổi ý thì không bao giờ là Expanded; Mutable chạy ngay | Theo KDoc | selfCheck; mốc thời gian minh họa |

### C4 v2 · AnimatedVisibility, AnimatedContent (2026-11-23)

| Claim | Nguồn | Loại |
|---|---|---|
| Mặc định fadeIn+expandIn / fadeOut+shrinkOut; kết hợp bằng + chạy cùng lúc; chờ mọi animation enter/exit (kể cả tùy biến trên scope.transition); gỡ và dispose sau exit; Layout riêng lấy kích thước lớn nhất; Row/Column có mặc định riêng; MutableTransitionState để làm việc sau exit | `an-av-src` (@296313a4) | impl |
| Animation ngoài Transition không được theo dõi; AnimatedContent phải dùng tham số lambda | `an-composables` | stable |
| AnimatedVisibility, slide, Crossfade | Kunneth Ch.8 | Ví dụ của sách |
| animateEnterExit cho con, auto-start | Essentials Ch.39 | Ví dụ của sách |
| Sim `animation.exitlife`: gỡ ở 300 / 500 ms; bản "outside" bị cắt ở 300 ms | Theo KDoc và tài liệu | selfCheck; mốc minh họa |

### C5 v2 · animateContentSize, animateItem (2026-11-23)

Đọc ở commit ghim 296313a4: `compose/animation/animation/.../AnimationModifier.kt`; `compose/foundation/foundation/.../lazy/LazyItemScope.kt`, `lazy/layout/LazyLayoutItemAnimation.kt`, `lazy/LazyListMeasuredItem.kt`.

| Claim | Nguồn | Loại |
|---|---|---|
| animateContentSize = clipToBounds() then SizeAnimationModifierElement; hai overload (có/không alignment, mặc định TopStart); spec mặc định spring(StiffnessMediumLow, IntSize.VisibilityThreshold) | `an-acs-src` | impl |
| measure: đo con → animateTo(kích thước con) trả anim.value → constraints.constrain → đặt con theo alignment; lần đầu tạo Animatable(targetSize) nên không animate; đích đổi thì startSize = giá trị hiện tại và launch animateTo; listener chỉ khi Finished; onReset xóa animData; dùng lookahead size làm đích | `an-acs-src` | impl |
| Đặt trước size/defaultMinSize; tham số animationSpec, alignment, finishedListener | `an-composables` | stable |
| Kunneth ghi mặc định `spring()` (sách viết cho phiên bản cũ); ở commit ghim là spring(StiffnessMediumLow); không khẳng định phiên bản nào đã đổi | Kunneth Ch.8 vs `an-acs-src` | ghi rõ trong bài |
| `.height(h).animateContentSize()` nhảy (constraints cố định); animation vô hình vẫn làm đo lại mỗi frame | Suy ra từ mã (`constrain`, state đọc trong measure) | ghi rõ "suy ra, không phải số đo" |
| animateItem: fade in/out + placement (kể cả arrangement/alignment), null tắt, mặc định spring(StiffnessMediumLow), cần key; animateItemWithTransitions còn internal | `an-lazyscope-src`, `cp-lists` | impl / stable |
| Item đặt ở targetOffset + placementDelta bằng placeWithLayer; placementDelta animate về 0; alpha của GraphicsLayer cho fade; độ lệch do cuộn không animate | `an-lazyanim-src` (+ LazyListMeasuredItem.kt) | impl |
| SizeChangeAnimationDemo (Slider → maxLines), snap(1000) | Kunneth Ch.8 | Ví dụ của sách |
| Overview READ MORE với Column.animateContentSize | AAT Ch.10 | Ví dụ của sách |
| notifyItemRemoved/Inserted, DefaultItemAnimator, bốn hàm của ItemAnimator | AAT Ch.7 | Ví dụ của sách (hệ View) |
| Sim `animation.acs`: 40/160 px, giá trị từng frame 85/128/152/160 | Minh họa | selfCheck; ghi trong simp |

### IF v2 (chương mới) · repeatable, infiniteRepeatable, InfiniteTransition (2026-11-23)

Đọc ở commit ghim 296313a4: `animation-core/.../AnimationSpec.kt` (RepeatableSpec, InfiniteRepeatableSpec, RepeatMode, StartOffset), `InfiniteTransition.kt`, `SuspendAnimation.kt`; `ui/ui/.../platform/InfiniteAnimationPolicy.kt` (đường dẫn tìm bằng `?format=JSON`).

| Claim | Nguồn | Loại |
|---|---|---|
| repeatable/infiniteRepeatable chỉ nhận DurationBasedAnimationSpec; TODO "Consider supporting repeating spring specs"; Reverse nên dùng số lượt lẻ, nếu không có thể nhảy tới giá trị cuối; initialStartOffset không lặp, delay trong spec thì lặp; StartOffsetType Delay/FastForward; InfiniteRepeatableSpec ném IllegalArgumentException khi thời lượng 0; không bao giờ tự xong, dừng khi composable bị gỡ | `an-spec-src` | impl |
| rememberInfiniteTransition = remember + run(); LaunchedEffect lặp withInfiniteAnimationFrameNanos; play time / durationScale; scale = 0 → skipToEnd + snapshotFlow chờ > 0; đổi scale → reset từ 0; con: TransitionAnimationState, DisposableEffect thêm/gỡ, SideEffect tạo lại khi initial/target đổi (không giữ liên tục) | `an-inftrans-src` | impl |
| callWithFrameNanos: isInfinite → withInfiniteAnimationFrameNanos, ngược lại withFrameNanos | `an-suspend-src` | impl |
| InfiniteAnimationPolicy: áp cho animation lấy frame qua withInfiniteAnimationFrameNanos/Millis; mặc định không cài, trừ ComposeTestRule | `ui-infpolicy-src` | impl |
| ComposeTestRule không chạy infiniteRepeatable, vẽ bằng giá trị ban đầu | `an-customize` (đã dùng ở C8) | stable |
| repeatable(10, tween(2000), Reverse) cho fadeIn (số chẵn: chính là trường hợp KDoc cảnh báo) | Essentials 39.5 vs `an-spec-src` | Ví dụ của sách, ghi rõ trong bài |
| InfiniteRepeatableDemo (rotate, keyframes 0→359, Reverse + khoảng nghỉ); progress indicator dùng InfiniteRepeatableSpec | Kunneth Ch.8 | Ví dụ của sách; ghi chú rotate đọc ở composition |
| Sim `animation.repeat`: 300 ms Linear mỗi lượt; bước "nhảy tới giá trị cuối" theo câu chữ KDoc | Minh họa | selfCheck; ghi trong simp |

### C6 v2 · Animatable và gesture (2026-11-23)

Đọc ở commit ghim 296313a4: `animation-core/.../Animatable.kt`, `InternalMutatorMutex.kt`, `AnimationSpec.kt` (InterruptionAwareAnimationSpec), `SuspendAnimation.kt`.

| Claim | Nguồn | Loại |
|---|---|---|
| Loại trừ nhau: runAnimation trong mutatorMutex.mutate; lời gọi mới (animateTo/animateDecay/snapTo/stop) hủy cũ bằng CancellationException, phần sau trong coroutine gọi cũng bị hủy | `an-animatable-src`, `an-mutex-src` (MutationInterruptedException) | impl |
| animateTo đi từ value hiện tại, initialVelocity mặc định = velocity; chỉ nên đặt sau fling; spring cho vận tốc liên tục | `an-animatable-src` (KDoc) | impl |
| endAnimation đặt vận tốc 0, isRunning false; AnimationResult Finished/BoundReached; bounds theo từng chiều; snapTo kẹp; stop dừng tại chỗ | `an-animatable-src` | impl |
| Hàm tạo có @RememberInComposition; animateTo nhận InterruptionAwareAnimationSpec (mới ở commit ghim, bảo người đọc kiểm bản phát hành) | `an-animatable-src`, `an-spec-src` | impl / version |
| Tap → animateTo; swipeToDismiss: stop, snapTo + VelocityTracker, splineBasedDecay.calculateTargetValue, updateBounds, animateTo(0, v) / animateDecay + onDismissed; bọc trong Modifier.composed | `an-advanced` | stable (ví dụ chính thức) |
| draggable + rememberDraggableState, detectDragGestures cộng dồn offset | Essentials Ch.50.5–50.6 | Ví dụ của sách |
| Sim `animation.mutex`: 40 px / 250 px/s, đích decay 190 và 900, biên 300 | Minh họa | selfCheck; ghi trong simp |

### SE v2 (chương mới) · Shared element (2026-11-23)

Đọc ở commit ghim 296313a4: `animation/animation/.../SharedTransitionScope.kt` (thư mục còn SharedElement.kt, SharedContentNode.kt, SharedTransitionStateMachine.kt, ExperimentalSharedTransitionApi.kt). Tài liệu: shared-elements, /customize, /navigation (đọc 2026-11-23, HTTP 200).

| Claim | Nguồn | Loại |
|---|---|---|
| SharedTransitionLayout = SharedTransitionScope { Box(modifier.then(m)) }; SharedTransitionScope bắt đầu bằng LookaheadScope | `an-shared-src` | impl |
| Scope: không gian tọa độ; overlay vẽ shared element trong lúc chuyển tới khi isTransitionActive = false; khớp key không qua scope khác; isMatchFound chỉ true sau khi phần tử mới được compose (lazy: trong lượt đo) | `an-shared-src` (KDoc) | impl |
| Clip/fade phải đặt sau modifier shared; zIndexInOverlay, clipInOverlayDuringTransition, placeholderSize (AnimatedSize đo lại cha mỗi frame); DefaultSpring StiffnessMediumLow | `an-shared-src` | impl |
| Tại commit ghim, SharedTransitionScope.kt không mang @ExperimentalSharedTransitionApi; không khẳng định thời điểm ổn định | `an-shared-src` (grep 0 lần) | version |
| sharedElement vs sharedBounds, Text dùng sharedBounds, key data class, thứ tự modifier, requiredSize, giới hạn | `an-shared` | stable |
| scaleToBounds vs RemeasureToBounds, boundsTransform keyframes ArcMode | `an-shared-custom` | stable |
| Navigation 3/2, predictive back theo API level, enableOnBackInvokedCallback | `an-shared-nav` | version |
| transitionName, addSharedElement, sharedElementEnterTransition, ChangeBounds/ChangeTransform; tên trùng trong RecyclerView | AAT Ch.6 | Ví dụ của sách (hệ View) |
| Sim `animation.shared`: 64×64 → 360×240, khung trung gian | Minh họa | selfCheck; ghi trong simp |
