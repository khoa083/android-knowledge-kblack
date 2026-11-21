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
