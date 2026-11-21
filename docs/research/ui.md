# Nghiên cứu Track E: UI (P6, 2026-11-21)

Ngày đối chiếu mọi giá trị: **2026-11-21**. Trang m3.material.io là SPA: công cụ đọc thường chỉ thấy tiêu đề, nên đã mở bằng Chrome headless (`dev/tools/cdp.js`, render JS) và đọc chữ đã render.

## WCAG 2.2 (W3C Recommendation 2024-12-12) — `normative`
- Relative luminance: kênh sRGB c = C8/255; c ≤ **0.04045** → c/12.92, ngược lại ((c + 0.055)/1.055)^2.4; L = 0.2126R + 0.7152G + 0.0722B. (Trước 05/2021 hằng là 0.03928; W3C ghi không ảnh hưởng thực tế.)
- Contrast ratio = (L1 + 0.05)/(L2 + 0.05), L1 sáng hơn; khoảng 1–21. Kiểm chứng: đen/trắng = 21; cùng màu = 1.
- Large-scale text: ≥ 18 pt, hoặc ≥ 14 pt đậm.
- 1.4.3 Contrast (Minimum) AA: 4.5:1, chữ lớn 3:1 · 1.4.6 Contrast (Enhanced) AAA: 7:1, chữ lớn 4.5:1 · 1.4.11 Non-text Contrast AA: 3:1 · 1.4.1 Use of Color A · 1.4.4 Resize Text AA (200%) · 2.2.2 Pause, Stop, Hide A · 2.3.3 Animation from Interactions AAA · 2.4.7 Focus Visible AA · 2.5.8 Target Size (Minimum) AA: 24×24 CSS px (có ngoại lệ khoảng cách) · 2.5.5 Target Size (Enhanced) AAA: 44×44 CSS px.
- Bốn nguyên tắc: Perceivable, Operable, Understandable, Robust (WAI accessibility-principles; trang không dùng chữ "POUR").
- Một số câu chữ SC (2.3.3, 2.4.7, 2.5.5, 2.5.8) do công cụ tóm tắt, chưa xác nhận nguyên văn; giá trị số khớp nhau giữa các lần đọc.

## Android / Compose — `stable` / `ds-guideline`
- Window size class (width): Compact < 600dp; Medium 600–<840; Expanded 840–<1200; Large 1200–<1600; Extra-large ≥ 1600 (Large/XL cần `supportLargeAndXLargeWidth = true`). Height: Compact < 480; Medium 480–<900; Expanded ≥ 900. API `currentWindowAdaptiveInfo().windowSizeClass` (material3-adaptive). (use-window-size-classes)
- Canonical layouts: list-detail (`ListDetailPaneScaffold`), supporting pane (`SupportingPaneScaffold`), feed (`LazyVerticalGrid`). NavigationBar cho compact, NavigationRail cho tablet nhỏ/ngang, NavigationDrawer cho tablet lớn (trang Material 3 in Compose).
- Target: "ít nhất 48 dp" (design accessibility); `minimumInteractiveComponentSize` giữ ≥ 48 dp không gian layout mỗi chiều; Checkbox, RadioButton, Switch, Slider, Surface dùng nội bộ (api-defaults). Tương phản chữ ≥ 4.5:1, thành phần không phải chữ ≥ 3:1; chữ thân ≥ 12 sp.
- Dynamic color: Android 12+ (`Build.VERSION.SDK_INT >= Build.VERSION_CODES.S`), `dynamicLightColorScheme(context)` / `dynamicDarkColorScheme(context)`; `lightColorScheme`/`darkColorScheme`; `MaterialTheme(colorScheme, typography, shapes)` (designsystems/material3).

## Material 3 (m3.material.io, đọc bằng trình duyệt 2026-11-21) — `ds-guideline`
- Type scale (trang type-scale-tokens; bộ **emphasized** đọc được đủ size/line height/tracking; cỡ chữ bộ baseline trùng — đối chiếu MDC-Android Typography.md): displayLarge 57/64 (−0.25) · displayMedium 45/52 · displaySmall 36/44 · headlineLarge 32/40 · headlineMedium 28/36 · headlineSmall 24/32 · titleLarge 22/28 · titleMedium 16/24 (0.15) · titleSmall 14/20 (0.1) · bodyLarge 16/24 (0.5) · bodyMedium 14/20 (0.25) · bodySmall 12/16 (0.4) · labelLarge 14/20 (0.1) · labelMedium 12/16 (0.5) · labelSmall 11/16 (0.5). Trang ghi đơn vị pt; trên Android dùng sp. Line height của bộ baseline lấy theo bộ emphasized (cùng cỡ) — ghi chú trên site.
- Motion (easing-and-duration/tokens-specs): standard cubic-bezier(0.2, 0, 0, 1); standard decelerate (0, 0, 0, 1); standard accelerate (0.3, 0, 1, 1); emphasized decelerate (0.05, 0.7, 0.1, 1); emphasized accelerate (0.3, 0, 0.8, 0.15); emphasized: không có dạng CSS cubic (dùng standard làm dự phòng). Duration: short1–4 = 50/100/150/200 ms; medium1–4 = 250/300/350/400; long1–4 = 450/500/550/600; extra-long1–4 = 700/800/900/1000.
- State layers (foundations/interaction/states/state-layers): hover +8%, focus +10%, press +10%, drag +16% opacity.
- Color roles: primary/onPrimary, primaryContainer/onPrimaryContainer, secondary…, tertiary…, error/onError, errorContainer/onErrorContainer, surface/onSurface, surfaceVariant/onSurfaceVariant, outline/outlineVariant, inverse… (MDC-Android Color.md; trang m3 roles không đọc được bảng). Site KHÔNG tái tạo thuật toán HCT/dynamic color: lab dùng mô hình ánh xạ giản lược theo độ sáng HSL.

## NN/g — `research`
- Fitts: T = a + b·log2(2D/W) (NN/g fitts-law, Budiu 2022); a, b phụ thuộc thiết bị trỏ. Spec site yêu cầu biến thể Shannon `a + b·log2(D/W + 1)`: dùng dạng Shannon (MacKenzie) và ghi rõ NN/g trình bày dạng log2(2D/W). a, b trong lab là minh họa.
- Thời gian phản hồi: 0,1 s (cảm giác tức thì), 1 s (giữ mạch suy nghĩ), 10 s (giữ chú ý; cần % hoàn thành và cách dừng) (response-times-3-important-limits).

## Chưa xác minh / xử lý
- Các trang NN/g khác trong spec (gestalt, aesthetic-usability, dark-mode, form placeholders, …): chưa đọc nội dung lần này → nêu ý ở mức chung, không gán số; liệt kê là "đọc thêm".
- Opacity của trạng thái disabled: không đọc được → không ghi số.
- Bộ lọc mù màu: ma trận mô phỏng đơn giản hóa (không theo một nghiên cứu cụ thể) → nhãn `simplified`.
- Sách UI (Williams, Tidwell, Neil…): chưa đọc epub; chỉ nêu tên framework (CRAP – Robin Williams, atomic design – Brad Frost).

## Checklist mục 9 (Track E) — tick 2026-11-21

| Mục | Ở đâu |
|---|---|
| M3 `ds-guideline` + ngày; WCAG `normative` + mã + mức | mọi giá trị M3 ghi "đọc 2026-11-21" (`lab.type.intro`, `lab.states.intro`, `lab.motion.intro`, E9 `sec.x7`); WCAG có mã + mức (E3 `sec.c`, lab contrast, lab a11y bảng) |
| Không "đạt tương phản là đủ"; WCAG không phải luật ở mọi nơi | `lab.contrast.note`, E10 `sec.x6.p.1`, misconception `contrast-enough` |
| Đẹp ≠ dễ dùng | E1 essence, quiz q2, `lab.crap.note`, misconception `pretty-usable` |
| Pattern có bối cảnh, khi nào không, thay thế | model `ui.patterns` (`opt.*.when`, `opt.*.not`), misconception `hamburger-best` |
| Công thức tương phản đúng, kiểm chứng 21:1, 1:1; ngưỡng có nguồn | `models/quant.js` (ngưỡng 0.04045) + registerCheck 21:1/1:1 và #767676 ≈ 4.54 |
| Fitts có nguồn, a/b minh họa; tách Android 48 dp, WCAG 2.5.8, 2.5.5 | `lab.fitts.intro`, `lab.fitts.note`, E5 essence |
| Color roles giản lược; mù màu giản lược | `lab.roles.intro` ("KHÔNG phải HCT/dynamic color"), `lab.roles.cvdNote`, badge `simplified` |
| Token từ trang chính thức + ngày | type scale, motion, state layer, breakpoint (bảng ở trên) |
| Light ≠ đảo màu | registerCheck "light và dark là hai bảng khác nhau", `lab.roles.note`, misconception `dark-invert` |
| Thứ tự đọc giản lược, không phải TalkBack | `lab.a11y.notTalkback` |
| Không tái tạo UI/logo có thật | mock Hẹn Khám hư cấu, tự vẽ |
| Hiểu lầm ≥ 10 | 11 mục |

Lệch spec có chủ ý (ghi lại): inspector bốn tab "Giải thích/Mã Compose/Token/Kiểm tra a11y" được thay bằng các khối trong từng lab (giải thích, đoạn mã, bảng kiểm tra); bộ chọn component trạng thái có 3 component (Button, TextField, mục navigation bar) thay vì 5; "pattern picker" 8 tình huống, form clinic, thời gian phản hồi là model rời rạc với sơ đồ isometric thay vì mock.
