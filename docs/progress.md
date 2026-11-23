# Tiến độ triển khai: Android Deep Dive Explorer

Thư mục đích: `E:\AndroidDeepDiveExplorer` (lúc bắt đầu chỉ có `CLAUDE.md`, dùng nguyên thư mục, không ghi đè gì).
Đặc tả: `E:\AndroidDeepDiveExplorer-Prompts` (chỉ đọc). Quy trình: mỗi phase xong thì tự kiểm, cập nhật file này, báo người dùng rồi **chờ xác nhận** trước khi sang phase kế tiếp.

Trạng thái: `chưa / đang / xong`.

| Phase | Nội dung | Trạng thái | Ghi chú |
|---|---|---|---|
| P0 | Chuẩn bị toàn cục: phiên bản, URL, kiến trúc, design tokens | **xong** (2026-11-20) | Đầu ra: `docs/research/global.md`, `docs/design-principles.md`. Chờ người dùng xác nhận để sang P1. Chưa kiểm font ở trình duyệt (làm ở P1) |
| P1 | Khung site, i18n, registry, engine, `dev/report.html`, track "hello" | **xong** (2026-11-20) | Người dùng yêu cầu làm tiếp bằng lịch 2h sáng nên P2 bắt đầu ở lần chạy đó. Hợp đồng lõi: `docs/core-api.md`. Track hello là tạm, gỡ trước P8 |
| P2 | Track A: Kotlin Coroutines | **xong** (2026-11-21) | Report 0 lỗi; checklist A ở `docs/research/coroutines.md` cuối file |
| P3 | Track B: Compose Runtime | **xong** (2026-11-21) | Report 0 lỗi; checklist B cuối `docs/research/runtime.md`. Chi tiết nội bộ ghi nhánh androidx-main + ngày đọc (không có commit hash) |
| P4 | Track C: Compose Animation | **xong** (2026-11-21) | Report 0 lỗi; checklist C cuối `docs/research/animation.md` |
| P5 | Track D: UX | **xong** (2026-11-21) | Report 0 lỗi; checklist D cuối `docs/research/ux.md` |
| P6 | Track E: UI | **xong** (2026-11-21) | Report 0 lỗi; checklist E cuối `docs/research/ui.md` |
| P7 | Tích hợp trang chung (cầu nối X1–X8, catalog, lộ trình, tìm kiếm, nguồn, README) | **xong** (2026-11-21) | README.md, sources.md, bản đồ cầu nối SVG, gỡ track hello |
| P8 | QA nghiệm thu; gỡ track "hello" | **xong** (2026-11-21) | Chrome + Edge đạt; Firefox/Safari chưa xác minh (không có trên máy) |

## Nhật ký

### P0 — 2026-11-20
- Đã đọc: master, STYLE-REFERENCE, I18N-STYLE-GUIDE, CONSTRAINTS-CHECKLIST, SOURCES, REFERENCE-BOOKS, P0, P1, và track A–E (A, D, E đọc đủ; B, C đọc phần đầu, phần còn lại đọc ở phase của chúng).
- **Phiên bản chốt:** Kotlin 2.4.21; kotlinx.coroutines 1.11.0; Compose BOM 2026.11.01 (runtime/ui/animation 1.13.0, material3 1.5.0); Compose Compiler là plugin `org.jetbrains.kotlin.plugin.compose` đi cùng Kotlin 2.4.21, strong skipping mặc định từ Kotlin 2.0.20; AndroidX Lifecycle 2.11.1; WCAG 2.2 (Recommendation 2024-12-12); Material 3 đối chiếu 2026-11-20 (token chưa đọc, làm ở P6).
- **URL:** 189 URL duy nhất được kiểm; 188 trả 200, 1 trả 404. Phải thay 3 URL (animation overview 404; hai trang kotlinlang chỉ là stub chuyển hướng: flow, cancellation). 6 URL redirect đổi sang URL đích. Chi tiết ở `global.md` mục 3.
- **Tương phản:** chỉnh 7 màu (light: ink-3, state, ui, flow, cancel, job; dark: ink-3); thêm token `--line-strong` và `--row-active`; quy tắc chip dùng chữ `--ink`; accent track chỉ non-text. Chi tiết ở `global.md` mục 5.
- **Kiến trúc:** thứ tự script, namespace `ADE`, khóa chuỗi phẳng + `addStrings` có chặn trùng và chặn ghi sai vùng, validate hai giai đoạn (`registerTrack` rồi `validateAll()`), tiền tố `ade.` cho `localStorage`, quy tắc NFC. Chi tiết ở `global.md` mục 4.

## Việc cần xác minh ở phase sau
- P1: kiểm chuỗi tiếng Việt viết hoa trong trình duyệt (Windows: Consolas, Cascadia Mono nếu có) ở light và dark; ghi vào `design-principles.md` mục 4. Android (Roboto Mono/Noto Sans Mono) chưa kiểm được.
- P3: chốt commit AndroidX.
- P6: nội dung trang M3, `material3-adaptive` stable.
- Spec còn lệch thực tế: `SOURCES.md` ghi mọi URL đã kiểm 200 ngày 2026-11-20 nhưng có 1 URL 404 và 2 stub; không sửa spec (thư mục chỉ đọc), site dùng URL đã thay.

### P1 — 2026-11-20
- **Đã dựng:** `index.html`, `styles.css`, `app.js`; `js/core/{i18n,registry,engine,diagram,ui,controls,search,router}.js`; `i18n/ui.{vi,en}.js` (≈400 khoá); `shared/` (nguồn + phiên bản, glossary, hiểu lầm, cầu nối X1–X8, lộ trình, trang Về site); `dev/report.{html,js}`; track tạm `tracks/hello/`.
- **Kiểm bằng Chrome headless qua `file://`** (điều khiển bằng CDP, vì khung xem trước tích hợp chỉ render ảnh tĩnh): không lỗi console ở mọi route (16 route, vi/en); catalog, nav, rail, drawer, tìm kiếm (Ctrl K), Live Explorer, nguồn, glossary, hiểu lầm đều tự nhận track hello; Back/Forward hoạt động; đổi ngôn ngữ giữa chừng giữ route, bước và cấu hình sandbox; `?` mở bảng phím tắt; phím tắt bị bỏ qua khi focus ở nút; giảm chuyển động tắt zoom, token và gõ chữ, Play thành từng bước; bật lại thì zoom hoạt động; 360px không cuộn ngang (16/16 route); chạy được khi `localStorage` và `history.replaceState` bị chặn.
- **`dev/report.html`:** sạch (0 lỗi); 1 cảnh báo là các tham chiếu của cầu nối, lộ trình tới track chưa đăng ký (bình thường). Có kiểm khoá model phát ra, NFC, markup khớp hai ngôn ngữ, id bị cấm, URL đã thay, ví dụ kiểm chứng engine.
- **Gate tĩnh:** không `fetch`/XHR/`import`/`export`/`type="module"`/webfont/CDN trong `app.js`, `js/core`, `index.html`, `styles.css`; không `trackId ===` hay `case '<id>'` trong lõi.
- **Quyết định thêm so với P0:** id route cũng bị cấm làm id track; `pos` của session (0 tổng quan, 1..N bước, N+1 tổng kết) là số trong URL; view config sinh sơ đồ, timeline, bảng log (track không tự vẽ trừ model compute/liên tục); bước đổi bằng `replaceState`.
- **Chưa làm / chưa kiểm:** font Cascadia Mono và Android (Roboto Mono, Noto Sans Mono) vẫn chưa kiểm; chưa kiểm bằng Firefox/Edge/Safari (chỉ Chrome); view dựng sẵn cho model liên tục (Animation) để P4; khối "Tự kiểm tra" chỉ là hiện/ẩn đáp án; mock app "Hẹn Khám" để P5; README, bản đồ cầu nối đầy đủ, `sources.md` ở P7.
- **Sửa sau rà soát (cùng ngày):** (1) focus không còn rơi về `<body>` sau khi dựng lại DOM: `ADE.ui.withFocus` + thuộc tính `data-fk` cho mọi phần tử tương tác được dựng lại (nút Trước/Tiếp, mục bước, dòng log, tab, sandbox, header, drawer, bộ lọc); kiểm bằng `dev/tools/focus-check.js` (mọi mục đều giữ focus). (2) Nhãn node bị làm mờ 70% chỉ còn 4.163:1 ở light → chỉ làm mờ khối và icon, giữ nhãn đậm. (3) Cài `.i18n-missing` (ký tự vô hình + `ADE.markMissing`, viền cảnh báo khi `?dev=1`; đã thử xoá khoá en rồi dựng lại). (4) `document.title` ở trang chủ. (5) `aria-live` có nội dung sau mỗi bước.
- **Trình duyệt đã kiểm:** Chrome và Edge (headless, `file://`): 16 route không lỗi console, không cuộn ngang ở 360px, kiểm focus đạt, `dev/report.html` sạch. Firefox, Safari chưa kiểm.
- **Công cụ kiểm thử trong dự án:** `dev/tools/cdp.js` (Chrome/Edge headless qua CDP; `BROWSER_EXE` để đổi trình duyệt), `routes-check.js`, `focus-check.js`.
- **Lịch tự động:** tác vụ `android-deep-dive-continue` chạy MỘT LẦN lúc 02:00 thứ Bảy 2026-11-21 (giờ máy, +07:00, khi hạn mức được đặt lại), làm lần lượt các phase còn lại từ P2, tự kiểm và cập nhật file này sau mỗi phase. Chỉ chạy khi ứng dụng Claude đang mở (đóng thì chạy ở lần mở kế tiếp).
- **Việc dọn sau:** gỡ `tracks/hello`, khối script của nó (2 file HTML) và khoá `domain.sandbox` trước P8.

### P2 — 2026-11-20 (dừng giữa chừng vì hết hạn mức sử dụng)
- **Đã có:** `docs/research/coroutines.md` (nguồn đã đọc, URL thay, điểm chưa xác minh: `flatMap*`, `lifecycleScope`); `tracks/coroutines/` gồm manifest (10 chương A0–A9, 6 preset, kind mới block/run/check), 16 nguồn, code.js, 13 model (`models/common.js`, `models-a/b/c.js`), views, content.vi/en (983 khoá sinh từ cùng một nguồn nên cùng cây khoá), glossary 25 mục, hiểu lầm 11 mục; khối script đã thêm vào `index.html` và `dev/report.html`. Lõi: thêm `step.nodeStates` (hiện trạng thái dưới nhãn node), select hỗ trợ giá trị chuỗi, report quét tích Descartes cấu hình.
- **Script sinh nội dung** nằm trong thư mục tạm của phiên (`scratchpad/gen/p1–p5.py`, `build.py`) và có thể đã mất; nếu mất thì sửa trực tiếp `content.*.js` (giữ cùng khoá ở vi và en).
- **Kết quả `dev/report.html` lần cuối:** 2 lỗi, 13 cảnh báo, không lỗi console. Hai lỗi là ví dụ kiểm chứng: (1) `coroutines · lập lịch` (đo được B(delay)=20, B(block)=60: xem lại điều kiện `done(d,'A') === 50`; B chạy 20 ms nên kỳ vọng B(delay)=20 là đúng, chỉ cần kiểm lại giá trị của A); (2) `coroutines.hotcold` (xem lại kết quả B cho từng loại nguồn; bước channel đã đổi sang khoá `recvOnlyB`).
- **P2 — việc còn lại:** sửa 2 ví dụ trên; chạy lại report tới 0 lỗi (khoá thiếu nếu có); mở từng chương bằng `dev/tools/cdp.js` (không lỗi console, sơ đồ không chồng nhau, 360px, focus, đổi ngôn ngữ giữ bước, reduced-motion); thêm các route A vào `routes-check.js`; rà câu tuyệt đối vi/en; tick mục A trong CONSTRAINTS-CHECKLIST; viết nội dung đầy đủ cầu nối X2 (A8) vào `shared/bridges.*.js` nếu cần; đặt P2 = xong.

### P2 — 2026-11-21 (lần chạy tự động, hoàn tất)
- **Sửa 2 ví dụ kiểm chứng (lỗi thật trong model, không phải kỳ vọng sai):** (1) `ADE.coro.simulate`: hết `delay` thì task chạy lại cả đoạn delay (A xong ở 80 thay vì 50) → khi hết chờ bỏ qua đoạn delay rồi xếp hàng đoạn kế; xử lý delay ở cuối hoặc hai delay liền nhau; sự kiện không có luồng (`thread: -1`) không còn đổi trạng thái luồng. (2) `coroutines.hotcold`: `cache.slice(-0)` trả cả mảng nên SharedFlow replay=0 phát lại mọi giá trị → `replay > 0 ? slice(-replay) : []`.
- **Nội dung thêm:** A0 mục "Chín cặp khái niệm dễ nhầm"; A7 đoạn `flowOn`/`catch` chỉ tác động upstream; A8 mục "Cầu nối X2" (nội dung đầy đủ, chương chủ sở hữu); badge A1 `impl simplified`. Cùng khoá ở vi và en.
- **Sơ đồ:** sửa toạ độ `jobtree` (gốc và grandchild chồng lên child-2), `race` và `vtime` (node chung đè nhãn). Đã chụp và xem lại.
- **CSS:** `.field` thêm `min-width:0; max-width:100%` (select có option dài làm A8 tiếng Việt tràn 383px ở 360px). Không sửa `js/core`.
- **Công cụ:** thêm `dev/tools/track-check.js` (mỗi chương/tab sim: đi hết các bước, thử mọi điều khiển ở mức model và DOM, lộ khoá, cuộn ngang, focus sau Tiếp, đổi ngôn ngữ giữ route, preset). `routes-check.js` giờ sinh route từ registry (track, chương, preset, glossary, nguồn) nên không phải sửa khi thêm track.
- **Kết quả kiểm (file://, Chrome headless):** `dev/report.html` 0 lỗi, 13 cảnh báo (12 "nghi chưa dịch" là tên mã/API giống nhau ở hai ngôn ngữ, 1 là tham chiếu tới track chưa đăng ký); không lỗi console; 13 tab sim ở 10 chương đều đi hết bước; mọi điều khiển đổi danh sách bước (trừ "Bỏ thao tác cuối"/"Xóa hết" khi chưa có thao tác, đúng ý đồ); không lộ khoá; đổi ngôn ngữ giữ route và bước; focus không rơi về BODY; 36 route ở 360px không cuộn ngang; reduced-motion gắn class `reduced-motion`. Edge: report sạch.
- **Rà câu tuyệt đối:** đã đọc các câu có always/never/every/only và luôn/không bao giờ/mọi/chỉ; đều là phát biểu từ tài liệu chính thức hoặc đã có điều kiện.
- **Chưa xác minh:** Firefox, Safari; font Android; `flatMap*` (đã ghi rõ là không mô phỏng); kiểm tương phản tự động chỉ ở mức token (P0), chưa đo từng màu node mới.

### P3 — 2026-11-21 (lần chạy tự động)
- **Nghiên cứu:** đọc trực tiếp 13 trang (phases, lifecycle, mental-model, stability, strong skipping, side-effects, semantics, how-compose-works.md, reference Snapshot/Applier/MonotonicFrameClock/ComposeView/Recomposer), đều HTTP 200, không chuyển hướng. Ghi ở `docs/research/runtime.md`. how-compose-works.md không hiện commit hash → ghi "androidx-main, đọc 2026-11-21", gắn `impl`; `$changed` chỉ nhắc tên.
- **Đã dựng `tracks/runtime/`:** manifest (11 chương B0–B10, 3 preset `runtime-counter`, `runtime-list-key`, `runtime-phase-read`), 11 model trong `models/models.js` (map, setcontent, compiler, keys, snapshot, recomposer, applier, phases, skip, semantics, counter) với selfCheck, `views/views.js` (sơ đồ runtime 11 node dùng lại cho 7 model + 4 sơ đồ riêng), `code.js` (10 đoạn, minh họa), 14 nguồn, glossary 15 mục, hiểu lầm 9 mục. Nội dung 748 khoá/ngôn ngữ sinh từ `dev/gen/runtime_content.py` (một nguồn → cùng cây khoá vi/en; sửa ở đó rồi chạy lại). Khối script đã thêm vào `index.html` và `dev/report.html`.
- **Cầu nối:** B7 sở hữu X1 (`b7.sec.x1`), B5 sở hữu X3 (`b5.sec.x3`); B0 tóm tắt X5, B4/B8 tóm tắt X2, B9 trỏ X6.
- **Kiểm (file://, Chrome headless):** report 0 lỗi (cảnh báo: "nghi chưa dịch" cho tên API/mã, tham chiếu tới track chưa có); track-check desktop và 360px: 0 vấn đề (mọi điều khiển đổi danh sách bước ở mức model, không lộ khoá, đổi ngôn ngữ giữ route, focus không rơi về BODY); routes-check 51 route ở 360px không cuộn ngang; đã chụp và xem B0, B3, B7, B9, B10 (sửa: bố cục lưới bản đồ cho bớt cạnh cắt qua node, callout B3 thiếu tham số, dải chỉ số điền dần).
- **Lệch spec:** node sơ đồ B0 chưa bấm được trực tiếp; thay bằng ô chọn "Thành phần" (cần thay đổi lõi để hỗ trợ bấm node; để P7/P8 cân nhắc).
- **Chưa xác minh:** commit hash cho how-compose-works.md; Firefox/Safari.
- **Sửa sau rà soát (cùng ngày, P2+P3):**
  - Thử thêm vào lõi "node bấm được" + nhãn cố định cho node: **bị chặn** (quy tắc chỉ sửa `js/core` khi có lỗi lõi; công cụ cũng từ chối). Lõi KHÔNG đổi. B0 giữ ô chọn "Thành phần"; nhãn `android-impl` đưa vào chính tên node (`ComposeView ‹android-impl›`, `LayoutNode ‹android-impl›`) nên hiện ở mọi model dùng sơ đồ chung. Nếu người dùng đồng ý sửa lõi: thêm `node.action` (role=button, Enter/Space, `data-fk`) và `node.badgeKey` trong `js/core/diagram.js`, nối `scene.onNode` trong `js/core/ui.js`.
  - Thêm `dev/tools/controls-sweep.js` (quét mọi tổ hợp điều khiển). Tìm ra 4 chỗ điều khiển không đổi gì: `coroutines.cancel` coop ở chế độ timeout, fin khi không bị hủy; `coroutines.exception` ceh khi lỗi đã bị bắt quanh scope hoặc con là async trong supervisor; `runtime.setcontent` eager khi gọi createComposition() trước. Cả 4 đúng ngữ nghĩa → model giờ hiện ghi chú "vì sao điều khiển không có tác dụng" (khoá mới ở vi và en). Quét lại: không còn điều khiển chết.
  - Track B: bổ sung state trước/sau, thành phần bị ảnh hưởng, thay đổi cho map, applier, semantics, recomposer; sửa trích dẫn B4 (`and-effects` → `and-state` cho `collectAsStateWithLifecycle`).
  - Thêm `docs/checklist.md`: checklist chung §0–4, §10, §11 với vị trí và trạng thái.
  - Kiểm lại: report 0 lỗi; track-check A và B (chỉ còn "undo/clear từ trạng thái đầu", đúng ý đồ); routes-check 51 route 0 vấn đề; focus-check đạt.

### P4 — kế hoạch ban đầu (đã làm xong, giữ để tham khảo)
1. Nghiên cứu: đọc `tracks/C-compose-animation.md`, P4 phase; đọc nguồn thật (animation/introduction, reference AnimationSpec/spring/tween/Easing, Animatable, Transition, AnimatedVisibility, animate*AsState) và ghi hằng số có nguồn (spring stiffness/damping, tween mặc định) pin animation 1.13.0 → `docs/research/animation.md`.
2. Ưu tiên model rời rạc cho khái niệm theo bước (AnimatedVisibility/Transition, ngắt, hủy Animatable — C6 sở hữu X4); chỉ dùng model liên tục cho đường cong/spring. Lưu ý: `app.js mountStage` chỉ gọi `view.mount` cho model `compute` → model liên tục chưa có chỗ gắn view (cần sửa lõi; nếu không được phép thì dùng model compute có view tự vẽ cho biểu đồ đường cong).
3. Manifest, nội dung (sinh từ `dev/gen/animation_content.py`), code, model, view, glossary (không định nghĩa lại `frame-clock`, `launched-effect`), hiểu lầm, nguồn; khối script trong cả hai HTML; kiểm như P3.

### P4 — 2026-11-21 (lần chạy tự động)
- **Nghiên cứu:** đọc 13 trang chính thức + 2 file mã nguồn AndroidX (Easing.kt, FloatDecayAnimationSpec.kt, androidx-main). Hằng số ghi ở `docs/research/animation.md`. `Spring.StiffnessHigh` không xác minh được → không dùng. URL `/compose/animation` xác nhận 404 → dùng `/animation/introduction`.
- **Đã dựng `tracks/animation/`:** manifest (9 chương C0–C8, 4 preset đúng spec), `models/physics.js` (spring 3 chế độ dạng giải tích, tween cubic-bezier, keyframes, repeatable/infinite, snap, decay theo công thức nguồn; 6 ví dụ kiểm chứng), `models/models.js` (6 model rời rạc: choose, transition, visibility, size, phaseread, testclock + 3 model compute cho lab), `views/lab.js` (lab dùng chung: preview, đồ thị value-over-time, bảng current/target/velocity, Play/Pause/Step frame/Restart/Đổi target/Reset, khoảng frame minh họa, kéo-fling bằng chuột/cảm ứng/bàn phím, hai đồng hồ pointer/animation, panel mã, nhật ký, giản lược), `views/views.js`, `code.js`, 15 nguồn, glossary 13 mục (dùng lại `frame-clock`, `launched-effect`), hiểu lầm 9 mục. Nội dung 551 khoá/ngôn ngữ sinh từ `dev/gen/animation_content.py`. Khối script thêm vào cả hai HTML. Không sửa `js/core`.
- **Cầu nối:** C6 sở hữu X4 (`c6.sec.x4`); C0/C2 dẫn X7; C1/C5/C7 dẫn X1; C7 dẫn X3; C8 dẫn X6.
- **Kiểm:** report 0 lỗi (Chrome và Edge), mọi ví dụ kiểm chứng PASS; track-check A/B/C (C: 0 vấn đề desktop và 360px, gồm thử mọi nút/select của lab); controls-sweep: không điều khiển chết (C4 có ghi chú khi điều khiển không áp dụng); routes-check 65 route ở 360px: 0 vấn đề; đổi ngôn ngữ giữa chừng giữ trạng thái lab (đã kiểm C1); Play thật bằng rAF trong headless chạy tới "ổn định"; chụp C1, C2, C4, C6. Sửa trong lúc kiểm: tràn ngang do `sr-only` trong khối mã của lab, chữ đồ thị phóng to (viewBox theo bề rộng thật), tham số nhật ký lưu số thô để đổi ngôn ngữ định dạng lại, id hiểu lầm trùng `whole-tree` → `anim-whole-tree`.
- **Chưa xác minh:** Firefox/Safari; kéo bằng cảm ứng thật (chỉ thử bằng nút và mô phỏng sự kiện); `keyframes` easing từng đoạn (mô hình tuyến tính, đã ghi giản lược).

### P5 — kế hoạch ban đầu (đã làm, giữ để tham khảo)
1. Nghiên cứu: xác nhận nội dung các trang NN/g chính (heuristics, severity, how-many-test-users → p, slips/mistakes, deceptive patterns, research methods, success rate), Design Council, GV; công thức SUS + adjusted Wald có nguồn → `docs/research/ux.md`.
2. Mock app "Hẹn Khám / ClinicBook" ở `shared/mock-app/` (dùng `ADE.ui.mockFrame`), đổi ngôn ngữ theo site.
3. Model: quant (SUS, adjusted Wald, discovery curve) + rời rạc (D0 phân loại, D1, D2 bảy giai đoạn, D3 lab lỗi, D4 workbench, D5 CREATE + deceptive, D6, D7, D9 microcopy, D10).
4. Nội dung sinh từ `dev/gen/ux_content.py`; nguồn, glossary, ≥10 hiểu lầm; khối script hai HTML; kiểm như P4.

### P5 — 2026-11-21 (lần chạy tự động)
- **Nghiên cứu:** đọc nội dung 20+ trang (NN/g: heuristics, severity, heuristic evaluation, usability 101, UX definition, slips, mistakes, error messages, deceptive patterns, success rate, perceived usability, how many test users, why 5 users, research methods, recognition/recall, short-term memory, simplicity vs choice, progressive disclosure, tone dimensions; MeasuringU SUS và Wald; Wikipedia Agresti–Coull; Design Council; GV; lawsofux Hick; Android app-languages). Ghi `docs/research/ux.md`.
- **Mock app dùng chung** `shared/mock-app/` (mock-app.js + chuỗi vi/en `shared.mock.*`): 6 màn Hẹn Khám/ClinicBook, đổi ngôn ngữ theo site, có "vùng" đánh dấu cho workbench; palette cố định vì màn mẫu luôn nền sáng (tương phản đã tính trong comment). Khối script thêm vào cả hai HTML (phần shared).
- **Track `tracks/ux/`:** 11 chương D0–D10, 20 sim: 14 model rời rạc (khuôn "tình huống → lựa chọn → giải thích" cho classify, mental, errors, deceptive, methods, stakeholder; cộng diamond, stages, create, session, tone, sprint) và 6 lab compute (`views/labs.js`: đo cá nhân recall, workbench heuristic 12 vấn đề + 3 mồi nhử + chế độ ba người, đường cong phát hiện, máy tính SUS, task success + adjusted Wald so hai thiết kế, microcopy editor với checklist tự soạn). Model định lượng thuần `models/quant.js` với 3 ví dụ kiểm chứng (SUS 50/100/0; 20/100 → 13–29% khớp NN/g; L 0.31, n 5 → 84.4%). 6 preset đúng spec. Nguồn 33 mục (6 mục "đọc thêm" ghi rõ chưa dùng cho khẳng định), glossary 17, hiểu lầm 11. Nội dung 878 khoá/ngôn ngữ sinh từ `dev/gen/ux_content.py`.
- **Cầu nối:** D9 sở hữu X8 (`d9.sec.x8`, dùng chính site song ngữ làm ví dụ); D2, D9 dẫn X6; D1 dẫn X7.
- **Kiểm:** report 0 lỗi; mọi ví dụ kiểm chứng PASS; track-check D desktop và 360px 0 vấn đề; controls-sweep không điều khiển chết; routes-check 83 route ở 360px 0 vấn đề; chụp D1 (lab đo cá nhân), D4 (workbench, chấm bài). Sửa trong lúc kiểm: màu mock app trên nền sáng ở theme tối; câu CREATE thêm "trong mô hình này".
- **Chưa làm / chưa xác minh:** chưa đọc epub sách (chỉ nêu tên framework); journey map kéo thả (D6 sandbox 2) và câu hỏi phỏng vấn (D6 sandbox 3), voice chart chọn 3 thuộc tính (D9) được rút gọn: D6 chỉ có bộ chọn phương pháp, D9 có voice/tone với 2 voice × 3 bối cảnh; A/B test chỉ trình bày khái niệm. Nội dung m3.material.io content design chưa dùng (chờ P6).

### P6 — 2026-11-21 (lần chạy tự động)
- **Nghiên cứu:** WCAG 2.2 (luminance ngưỡng 0.04045, ngưỡng 1.4.3/1.4.6/1.4.11/2.5.5/2.5.8…), WAI principles, Android (window size class, canonical layouts, target 48 dp, `minimumInteractiveComponentSize`, dynamic color Android 12+), NN/g Fitts và thời gian phản hồi. m3.material.io là SPA: mở bằng `dev/tools/cdp.js` (Chrome headless render JS) để đọc type scale (size/line height/tracking), motion tokens (easing + duration) và state layer opacities. Ghi `docs/research/ui.md`.
- **Track `tracks/ui/`:** 11 chương E0–E10; 14 sim: 4 model rời rạc (layers, patterns, form, response) + 10 lab compute (`views/labs.js`: CRAP + squint, type scale + cảnh báo dấu tiếng Việt + 200%, contrast checker, color roles giản lược + "chỉ màu" + bộ lọc mù màu, responsive lab, Fitts playground đo cá nhân, component states + state layer, token editor sinh `MaterialTheme`, motion lab theo token, a11y audit + thứ tự đọc giản lược). `models/quant.js` với 5 ví dụ kiểm chứng (21:1/1:1, #767676 ≈ 4.54, breakpoint, Fitts, light ≠ đảo màu). 6 preset đúng spec. Nguồn 23 (10 mục "đọc thêm"), glossary 14, hiểu lầm 11. Nội dung 510 khoá/ngôn ngữ sinh từ `dev/gen/ui_content.py`.
- **Cầu nối:** E8 sở hữu X5, E9 sở hữu X7, E10 sở hữu X6 (nội dung đầy đủ); E7 dẫn X8; E9 dẫn X1. Cả 5 track đã đăng ký: report không còn tham chiếu treo.
- **Kiểm:** report 0 lỗi; track-check E (desktop, 360px) 0 vấn đề; controls-sweep toàn site không điều khiển chết; routes-check 101 route ở 360px 0 vấn đề; chụp E3 (roles dark) và E4 (list-detail ở 900 dp). `dev/tools/track-check.js` giờ bấm cả button/select/checkbox trong lab D và E.
- **Chưa xác minh:** line height của bộ type baseline (lấy theo bộ emphasized cùng cỡ, đã ghi trên site); opacity trạng thái disabled; sách UI chưa đọc; các trang NN/g "đọc thêm".

### P7 — 2026-11-21 (lần chạy tự động)
- **Cầu nối X1–X8:** nội dung đầy đủ ở chương chủ sở hữu (X1 B7, X2 A8, X3 B5, X4 C6, X5 E8, X6 E10, X7 E9, X8 D9); nơi dẫn chỉ có tóm tắt `shared/bridges.*` + chip link. Kiểm hai chiều bằng script trong trình duyệt: tìm ra C6 thiếu X2 → đã thêm; giờ mọi chương chủ sở hữu và chương dẫn đều khai báo cầu nối.
- **Trang chủ:** thêm bản đồ cầu nối dạng SVG line-art (khối isometric cho mỗi track, đường + nhãn mã cầu nối, khối là link, sinh từ registry — không id track cứng) trong `app.js` (`bridgeSvg`), CSS ở `styles.css`. Không sửa `js/core`.
- **Gỡ track tạm "hello":** xoá khối script ở `index.html` và `dev/report.html`, xoá `tracks/hello/`, xoá khoá `domain.sandbox` ở `i18n/ui.*.js`; `dev/tools/focus-check.js` chuyển sang chương A1. Registry chạy với đúng 5 track thật.
- **`sources.md`** song ngữ sinh từ registry bằng `node dev/tools/sources-md.js` (110 nguồn, mục phiên bản, ghi chú chính thức/thứ cấp, sách chỉ tên + tác giả, hai trang mẫu là "cảm hứng UX"); không có đường dẫn file sách.
- **`README.md`** song ngữ: cách mở, cách dùng, cấu trúc, thêm track, thêm ngôn ngữ, kiểm tra, cách chuẩn hóa tìm kiếm không dấu.
- **Đã có từ P1, kiểm lại:** catalog nhóm theo domain + bộ lọc, lộ trình (`shared/paths.js`), Live Explorer theo preset (`?preset=&step=`), hiểu lầm và glossary gom theo track, tìm kiếm không dấu ("tuong phan" → "tương phản"), trang Về site có mục quyền riêng tư.
- **Kiểm:** report 0 lỗi; track-check cả 5 track (chỉ còn undo/clear của A, đúng ý đồ); routes-check 98 route ở 360px 0 vấn đề.

### P8 — QA nghiệm thu, 2026-11-21 (lần chạy tự động)
- **`dev/report.html`:** 0 lỗi trên Chrome và Edge; 89 ví dụ kiểm chứng PASS, 0 FAIL; mọi khoá model phát ra có ở vi và en; 88 cảnh báo đều là "nghi chưa dịch" cho tên API/mã/thuật ngữ giữ nguyên tiếng Anh (ví dụ "Compose Runtime Explorer", "Strong skipping", "recompose Child").
- **Gate tĩnh:** 0 kết quả cho `type="module"`, `fetch(`, `XMLHttpRequest`, `import`/`export` đầu dòng trong `app.js`, `js/`, `tracks/*/models`, `tracks/*/views`, `shared/mock-app`; không `http` trong `src=`/stylesheet; không `@font-face`/Google Fonts; không TODO/Lorem/Coming soon; các `case '` trong `app.js` là tên trang, không có nhánh theo id track; không còn khoá `ui.*`. Cờ dev mặc định tắt (`ADE.dev=false`).
- **Route:** 98 route sinh từ registry ở 360px và 768px (Chrome) và 360px (Edge): không cuộn ngang, không lộ khoá, không lỗi console. Back/Forward đúng; URL theo bước mở đúng bước.
- **Sandbox/preset:** track-check cả 5 track (đi hết bước, thử mọi điều khiển ở mức model và DOM, lab bấm mọi button/select/checkbox, preset Live Explorer, đổi ngôn ngữ giữ route và bước, focus không rơi về BODY): chỉ còn "undo/clear từ trạng thái đầu" của A (đúng ý đồ). controls-sweep: không điều khiển chết ở mọi tổ hợp.
- **Truy cập:** focus-check đạt; reduced-motion gắn class và lab chuyển tức thời; chữ hoa chỉ cho tiêu đề ≤ 40 ký tự (đã sửa 2 chỗ); theme sáng và tối đã chụp kiểm (D8 sáng, nhiều lab tối); màn mẫu dùng bảng màu cố định có tương phản tính trước.
- **Nhận diện:** sơ đồ isometric, icon, logo, mock app "Hẹn Khám" tự vẽ; không asset/CSS/câu chữ của trang mẫu; hai trang mẫu chỉ ở trang Nguồn với vai trò cảm hứng UX.
- **Chưa xác minh / không áp dụng:** Firefox và Safari (không có trên máy); font Android; `originals/01–06` không có trong thư mục đặc tả nên đối chiếu theo `tracks/*.md`; sách tham khảo chưa đọc epub (chỉ nêu tên framework + tác giả); vài trang NN/g/M3 chỉ là "đọc thêm".
- **Việc còn lại đề xuất (không chặn bàn giao):** ~~cho node sơ đồ B0 bấm được~~ (đã làm 2026-11-21, xem mục cuối); journey map kéo thả (D6) và inspector bốn tab (E) đang ở dạng rút gọn; kiểm Firefox/Safari và trên thiết bị Android thật.

### Làm rõ và đa dạng hoá hình minh hoạ, animation — 2026-11-21 (phiên chính, theo phản hồi người dùng: "hình và animation cứ giống nhau, hơi khó hiểu")
- **Lõi (`js/core/diagram.js`, `ui.js`, `styles.css`, `i18n/ui.*.js`)**: thêm `view.layout` = `iso | tree | pipeline | cycle | lanes` (mặc định `iso`, view cũ không đổi); thẻ phẳng có độ dày (giữ chất "bản vẽ"); họ trạng thái có glyph + kiểu viền (chạy/chờ/chặn/hủy/lỗi/xong/rảnh) và chú giải tự sinh; node vừa đổi trạng thái được nhấn + chú thích trên hình "nhãn: trước → sau"; dòng "Bạn đang xem" (`captionKey`); token mang nhãn giá trị; lanes = hàng × thời gian (thanh chạy / chặn gạch chéo / suspend viền đứt / chờ luồng chấm, phần dự kiến mờ, vạch "bây giờ", mốc ◆). Sửa zoom cắt nhãn (hộp bao gồm icon + 2 dòng chữ); marker mũi tên có id riêng mỗi scene. Hợp đồng ở `docs/core-api.md` §4.1.
- **Track A**: A0 vòng (cycle); A1 suspend, A3 builders, A4 context, A5 cancel, A7a flowpipe, A9a race, A9b vtime → lanes; A2 jobtree, A6 exception, A8b effects → tree; A7b hotcold, A8a lifecycle → pipeline. 13 caption mới + nhãn mốc (vi/en). Đổi tên luồng ví dụ "Luồng A/B" → "Luồng 1/2" (tránh trùng tên coroutine A/B); tiêu đề bước dùng "luồng {n}".
- **Công cụ**: `cdp.js --el <selector>` (chụp một phần tử); `dev/tools/shots.js` (chụp nhiều route, chọn tab sim bằng `@n`).
- **Kiểm**: report 0 lỗi; track-check A desktop + 360px như trước (chỉ undo/clear ở trạng thái đầu); đã xem ảnh A0, A1, A2, A3, A5, A6, A7a/b, A8b, A9a/b (sáng, tối, 360px).
- **Track B**: B0 giữ bản đồ iso 11 khối (toàn cảnh); B1 setcontent (đường ống gập hai hàng), B2 compiler, B5 recomposer, B6 applier, B7 phases, B9 semantics → pipeline; B4 snapshot, B10 counter → cycle; B3 keys, B8 skip → tree. View dạng phẳng lấy tập con của bản đồ (giữ id node, model không đổi).
- **Track C** (model rời rạc): choose, transition, visibility, phaseread, testclock → pipeline; size → tree. Ba lab (retarget, spec, gesture) vẫn tự vẽ đồ thị.
- **Track D/E**: 10 model "tình huống → lựa chọn" (classify, mental, errors, deceptive, methods, stakeholder, session, tone; patterns, form, response) → vòng phản hồi Thiết kế → Màn hình → Người dùng (thêm cạnh design → screen) với caption chung `cap.loop`; stages → cycle (7 giai đoạn Norman); diamond, create, sprint, layers → pipeline. Nhãn họ trạng thái riêng cho UX (ổn / hỏng / bị chặn / chưa xét) và Runtime qua `view.famKeys`.
- **Caption** B–E thêm vào `dev/gen/*_content.py` (khối "caption sơ đồ", chạy lại script; đã kiểm script tái tạo đúng từng byte trước khi thêm).
- **Kiểm (Chrome headless, file://)**: report 0 lỗi (Chrome và Edge); track-check 5 track desktop + 360px: 0 vấn đề mới (A vẫn chỉ "undo/clear từ trạng thái đầu", đúng ý đồ); routes-check 98 route ở 360px: 0 vấn đề; focus-check đạt; reduced-motion: scene có class `still`, không có thanh `grow`, không token chạy. Đã xem ảnh B1, B4, B6, B7 (tối), B10, C3, D0, D2, D3, E0.
- **Chưa làm / chưa xác minh**: tương phản của màu mới chỉ dùng token sẵn có (chữ `--ink`/`--ink-2`, nét `--focus`), chưa đo tự động từng tổ hợp; Firefox/Safari; trên 360px các sơ đồ phẳng và lanes có độ rộng tối thiểu và cuộn ngang trong khung sơ đồ (trang không cuộn ngang).
- **Sau rà soát (cùng ngày)**: khôi phục zoom cho dạng phẳng (đẩy camera nhẹ vào thẻ vừa đổi + hàng xóm nối trực tiếp + chỗ chú thích; giữ ≥ 68% toàn cảnh nên không cắt; lanes không zoom); thanh "dự kiến" của lanes dùng nét đứt `--line-strong` (không dùng opacity, giữ ≥ 3:1); khung sơ đồ nhận focus (`tabindex=0`, `role=region`) để cuộn ngang bằng bàn phím trên màn hẹp; rà câu tuyệt đối trong chuỗi mới (C3 "luôn khớp" → "cùng nhịp"; A5 thêm "trong mô hình này" và nói điểm suspend của kotlinx cũng kiểm tra hủy; C7 "every frame" → "on each animation frame"; B0 caption khớp nhãn điều khiển "Thành phần"/"Component").
- **Việc còn lại của P8 đã xử lý**: node sơ đồ B0 bấm được (`view.nodeAction` trong lõi: chuột, Enter, Space, `aria-pressed`, `data-fk` giữ focus sau khi vẽ lại); đã kiểm bằng CDP (bấm snapshot → ô chọn = snapshot; Enter trên applier → bước đổi, focus vẫn ở node).

- **Dừng 2026-11-21 (hạn mức tuần 96%)**: chưa làm các lệch spec còn lại vì mỗi việc cần đọc nguồn và viết nội dung song ngữ, không đủ hạn mức để làm trọn: (1) D9 sandbox 2: model `ux.tone` hiện cho chọn 2 voice dựng sẵn (mỗi voice 3 thuộc tính) × 3 bối cảnh; spec muốn người đọc tự chọn 3 thuộc tính (cần câu mẫu cho từng tổ hợp, nguồn: tone-of-voice-dimensions, Podmajersky). (2) D6: journey map kéo thả và bộ câu hỏi phỏng vấn (đọc journey-mapping-101, user-interviews trước). (3) E: inspector 4 tab (Giải thích / Mã Compose / Token / Kiểm tra a11y). Kiểm thêm Firefox/Safari, thiết bị Android thật.

- **2026-11-21 (cuối):** người dùng thấy nội dung quá rút gọn → lộ trình v2 ở `docs/roadmap-v2.md` (viết lại Coroutines theo Deep Dive trước, rồi 6 track mới). Đã `git init` + commit.

## Coroutines v2 (bắt đầu 2026-11-22)

- Dàn chương trong `docs/roadmap-v2.md` đã khớp với mục lục thật của Deep Dive.
- **Generator:**
  - `dev/gen/coroutines_content.py` nạp `coroutines_base.json` (nội dung v1) cùng các file `coroutines_v2_*.py`;
  - đã kiểm: chỉ với base, generator tái tạo đúng từng byte (chỉ khác dòng chú thích đầu file).
- **Lõi (chung cho mọi track):**
  - khối nội dung v2 `.sec.<s>.b.<n>.<trường>`: tiêu đề con, đoạn, mã, output, callout (thêm `analogy`), đoán trước, tự trả lời, bug, bài tập; xem `docs/core-api.md` §2.1;
  - `chapter.simAfter`;
  - `registry` kiểm các khối này;
  - report bỏ cảnh báo "chưa dịch" cho các trường mã.
- **Khung sư phạm:** `docs/chapter-template-v2.md`.
- **U1 "Vì sao cần coroutine?" xong:**
  - nội dung gồm 10 mục: vấn đề, 4 cách giải, song song bằng async, chi phí luồng, 4 bug, 3 bài tập, tự trả lời, quiz 3 câu;
  - dùng lại sim `coroutines.suspend` (đặt sau mục "Cách 4" để câu đoán đứng trước sim);
  - thêm 4 nguồn;
  - bảng nguồn ở `docs/research/coroutines.md`.
- **Kiểm U1:**
  - report: 0 lỗi;
  - track-check 1280 và 360: chỉ còn 4 vấn đề cũ, cố ý;
  - routes-check: 99 route, 0 vấn đề;
  - focus-check: đạt;
  - đã xem ảnh mục bug (tối).
- **Chưa làm ở U1:**
  - xem ảnh trang ở nền sáng;
  - mở lại các URL nguồn mới;
  - đọc phần tương ứng trong *Coroutines by Tutorials*;
  - tìm thêm cách giảng trên mạng.
- **Tiếp theo:**
  - U2 Sequence builder (Deep Dive tr. 27–32);
  - U3 How does suspension work? (tr. 33–44);
  - U4 Coroutines under the hood (tr. 45–62): cần sim mới cho state machine/continuation;
  - sau đó Phần 2 (viết sâu lại A1–A9 theo các chương tr. 65–233).
- **U2 "Sequence builder" xong (2026-11-22):**
  - nội dung gồm: ôn chương trước, sequence là gì, theo dõi từng bước nhảy, vì sao cần suspension (có ghi chú impl), dùng thật, giới hạn `@RestrictsSuspension` (2 bug), 3 bài tập, tự trả lời, quiz 3 câu;
  - sim mới `coroutines.seq` (`tracks/coroutines/models/models-v2.js`, view lanes, đoạn mã `seq` và `seqList`), đặt sau mục "jump";
  - thêm 2 nguồn.
- **Kiểm U2:** report 0 lỗi; track-check 1280 và 360 không thêm vấn đề; routes-check 100 route, 0 vấn đề; đã xem ảnh sim ở bước 5.
- **Nội dung:**
  - viết trong `dev/gen/coroutines_v2_part1.py` (U1) và `coroutines_v2_u2.py` (U2);
  - mỗi chương mới nên là một file `coroutines_v2_<id>.py`, thêm tên vào danh sách `mod` trong `coroutines_content.py`.
- **U3 "Suspension hoạt động thế nào" xong (2026-11-22):**
  - nội dung gồm: ôn chương trước, ví von lưu game (khớp/không khớp), `suspendCoroutine`, resume và luồng, tự viết `delay`, resume với giá trị (gói callback), resume với exception, "suspend coroutine chứ không phải hàm", 4 bug, 3 bài tập, tự trả lời, quiz 3 câu;
  - sim mới `coroutines.cont` có 5 chế độ resume, đặt sau mục "resume";
  - thêm 4 nguồn; đã kiểm 10 URL bằng curl (200).
- **Kiểm U3:** report 0 lỗi, cả hai selfCheck đạt; track-check 1280 và 360 không thêm vấn đề; routes-check 101 route, 0 vấn đề; focus-check đạt; đã xem ảnh sim ở bước 5 (chế độ thread).
- **Tiếp theo:**
  - U4 "Coroutines under the hood" (Deep Dive tr. 45–62): CPS, state machine với `label`, continuation lồng nhau như call stack; cần sim mới (bước qua `label`, `COROUTINE_SUSPENDED`);
  - U5 "built-in support vs library" (tr. 63–64), có thể gộp vào U4.
- **U4 "Coroutine dưới mui xe" xong (2026-11-22):**
  - nội dung gồm: ôn chương trước, ba ý chính, CPS, hàm đơn giản (label, `COROUTINE_SUSPENDED`), biến cục bộ, `printUser`, chuỗi continuation (bài 13 Tick), mã thật và chi phí, ngôn ngữ so với thư viện, 3 bug (bộ nhớ giữ qua điểm suspend, "optimized out", stack trace), 3 bài tập, tự trả lời, quiz 3 câu;
  - sim mới `coroutines.sm` (state machine, 3 tình huống), đặt sau mục "value";
  - thêm 2 nguồn; URL đã kiểm (200).
- **Phần 1 của Coroutines v2 (U1–U4) xong.** Tiếp theo là Phần 2: viết sâu lại A1–A9 theo các chương Deep Dive tr. 65–233.
- **Chuyển cảnh và chuyển động (2026-11-22, theo phản hồi người dùng "không thấy animation, thiếu sinh động"):**
  - nguyên nhân: quy tắc cũ "chuyển động chỉ để giải thích, không trang trí" nên chỉ có vài hiệu ứng nhỏ trong sơ đồ; cài đặt animation của Windows ở mặc định (bật);
  - đã thêm vào lõi: vào trang (trượt lên lần lượt), mục chương hiện dần khi cuộn, panel trượt theo hướng khi đổi bước, chỉ số đổi thì nháy, dòng log mới trượt vào, ô mở trượt xuống, nút có phản hồi, thẻ sơ đồ bật rõ hơn;
  - quy tắc mới ở `docs/design-principles.md` §5.1;
  - reduced-motion tắt hết, đã kiểm bằng `--reduce` (rv=0, animation none);
  - chưa xem bằng mắt trên trình duyệt thật (headless chỉ kiểm class/animationName).
- **Sơ đồ lanes chuyển động liên tục (2026-11-22, người dùng: "sơ đồ chỉ nhảy giữa các trạng thái"):** `Scene._laneTween` nhớ vị trí và độ dài từng thanh, mốc, vạch "bây giờ"; bước sau chạy từ hình cũ sang mới (Web Animations, 560 ms ÷ tốc độ). Đã kiểm bằng CDP: 7 animation chạy ở một lần đổi bước của U3. Mục tiêu (goal) của U1–U4 đổi câu chữ cho đúng ở mọi chế độ sim. `next-prompt.md` cập nhật: §5.1 thắng hướng dẫn bổ trợ; bắt buộc nghiên cứu nguồn trước mỗi chương.
- **Đối chiếu nguồn U1–U4 (2026-11-22):** đã tải mã nguồn stdlib/kotlinx và tài liệu thật. Sửa chi tiết `SequenceBuilderIterator`, chế độ debug, `-Xdebug` (kèm cảnh báo không dùng cho production); bỏ trích dẫn nguyên văn thông báo lỗi chưa xác minh.
- **Phần 2 bắt đầu: A3 v2 "Coroutine builders" (2026-11-22):**
  - viết sâu thêm vào A3, gồm 12 mục: ôn tập, cầu nối, launch, runBlocking, async, when (v1), structured concurrency, bức tranh lớn, coroutineScope, 3 bug, 3 bài tập, tự trả lời; sim đặt sau "async";
  - thêm 4 nguồn API;
  - generator có thêm `override` (ghi đè chuỗi v1) và `SEC_ORDER` (sắp lại thứ tự mục).
- **Kiểm A3 v2:** report 0 lỗi; track-check 1280 và 360 không thêm vấn đề; routes-check 102 route, 0 vấn đề.
- **Tiếp theo trong Phần 2:** Context (tr. 82–93) → A4; Job và chờ con (tr. 94–106) → A2; Hủy (tr. 107–121) → A5; Exception (tr. 122–132) → A6; Scope functions (tr. 133–152); Dispatchers (tr. 153–172) → A4; Tự dựng scope (tr. 173–182); Shared state (tr. 183–197) và Testing (tr. 198–233) → A9.
- **A4 v2 "Coroutine context" (2026-11-22):** viết sâu thêm vào A4, gồm 12 mục: ôn tập, context là gì, tra phần tử, ghép bằng +, minusKey/fold, thừa hưởng và ghi đè, đọc trong hàm suspend, tự tạo phần tử, ctx (v1, dispatcher), 3 bug (`Job()` phá cây, phần tử dùng chung bị race, `ThreadLocal`), 3 bài tập, tự trả lời. Sim đặt sau "ctx". Thêm nguồn `kx-asctx`. Report 0 lỗi; track-check không thêm vấn đề. Phần Dispatchers (tr. 153–172) sẽ thêm vào A4 sau.
- **A2 v2 "Job, vòng đời và chờ con" (2026-11-22):**
  - nội dung gồm: ôn tập, vì sao Job quan trọng, máy trạng thái và bảng cờ, Job không được thừa hưởng, join/children, `Job()`/`CompletableJob`, tree (v1), 3 bug, 2 bài tập, tự trả lời;
  - sim mới `coroutines.jobstate` (tab "Vòng đời Job", cùng tab "Cây Job" cũ);
  - thêm 2 nguồn API.
- **Kiểm A2 v2:** report 0 lỗi; track-check không thêm vấn đề; routes-check 0 vấn đề.
- **A5 v2 "Hủy" (2026-11-22):**
  - nội dung gồm: ôn tập, ba hiệu ứng của `cancel`, `join`/`cancelAndJoin`/hủy nhóm, cơ chế `CancellationException` + `finally` (ví von khớp/không khớp), Cancelling + `NonCancellable`, `invokeOnCompletion`, dừng mã không suspend (`yield`/`isActive`/`ensureActive`), rules (v1), `suspendCancellableCoroutine`, 4 bug, 3 bài tập, tự trả lời;
  - sim `coroutines.cancel` đặt sau mục "unstoppable" với câu đoán trước;
  - thêm nguồn `kx-noncancellable`.
- **Kiểm A5 v2:** report 0 lỗi; track-check không thêm vấn đề; routes-check 0 vấn đề.
- **A6 v2 "Exception" (2026-11-22):**
  - nội dung gồm: ôn tập, lan truyền hai chiều, `try/catch` quanh `launch` vô dụng (ví von dây leo núi), `SupervisorJob` (lỗi hay gặp với một con), `supervisorScope` và bẫy `withContext(SupervisorJob())`, `async`/`await`, `CancellationException` không lan lên cha, CEH, rules (v1), 3 bug, 3 bài tập (bài 3 dùng sim), tự trả lời;
  - sim đặt sau mục "ceh";
  - thêm 3 nguồn API.
- **Kiểm A6 v2:** report 0 lỗi; track-check không thêm vấn đề; routes-check 0 vấn đề.
- **SF "Scope functions" (chương mới, 2026-11-22):**
  - nội dung gồm: ôn tập, ba cách chưa ổn (`GlobalScope`, truyền scope, ví dụ Twitter), `coroutineScope`, họ scope function so với builder, `withContext`, `supervisorScope`, `withTimeout`/`withTimeoutOrNull`, việc phụ trên scope riêng, 2 bug, 3 bài tập, tự trả lời, quiz 3 câu;
  - dùng lại sim `coroutines.builders`;
  - thêm 2 nguồn API.
- **Kiểm SF:** report 0 lỗi; track-check không thêm vấn đề; routes-check 103 route, 0 vấn đề.
- **Phần 2 còn lại:** Dispatchers (tr. 153–172) → A4; Tự dựng scope (tr. 173–182); Shared state (tr. 183–197) và Testing (tr. 198–233) → A9. Sau đó Phần 3 (Channel, Flow → A7) và Phần 4 (→ A8).
- **A4 v2 phần Dispatchers (2026-11-22):**
  - 10 mục mới (Default, Main, IO dùng chung pool, `IO.limitedParallelism`, một luồng, Unconfined, `Main.immediate`, `ContinuationInterceptor`, chọn theo loại việc) + 3 bug + 2 bài tập;
  - `SEC_ORDER` ghép với phần Context;
  - thêm 3 nguồn (`kx-dispatchers`, `kt-interceptor`, `ax-vmscope`: mã nguồn AndroidX cho `viewModelScope` dùng `Main.immediate`).
- **Sửa CSS:** tiêu đề ô hỏi–đáp có mã dài làm tràn ở 360px.
- **Kiểm:** report 0 lỗi; routes-check 103 route, 0 vấn đề; track-check coroutines (4 cũ), runtime 0, animation 0.
- **A8 v2 phần 1 "Tự dựng scope" (2026-11-22):**
  - nội dung gồm: ôn tập, không hiện thực `CoroutineScope`, hàm `CoroutineScope()`, dựng scope ViewModel 4 bước, `viewModelScope`/`lifecycleScope` (bản sách 2.4.0 và bản androidx-main), scope việc phụ và backend, 3 bug, 2 bài tập, tự trả lời;
  - sim A8 đặt sau mục "scopes" (v1);
  - thêm nguồn `kx-scopefn`.
- **Kiểm:** report 0 lỗi; track-check và routes-check như trên.
- **A9 v2 phần 1 "Trạng thái chung" (2026-11-22):**
  - nội dung gồm: ôn tập, `UserDownloader`, vì sao mất cập nhật, `synchronized`, atomic, giới hạn một luồng thô/mịn, `Mutex` (ví von, 2 nguy hiểm), `Semaphore`, race (v1), 3 bug, 2 bài tập; mục v1 "test" để cuối, chờ chương Testing;
  - sim đặt sau mục "lost";
  - thêm 2 nguồn.
- **Kiểm:** report 0 lỗi; track-check không thêm vấn đề; routes-check 0 vấn đề.
- **Còn lại của Phần 2:** Testing (Deep Dive tr. 198–233, 36 trang) → A9 phần 2.
- **A9 v2 phần 2 "Kiểm thử" (2026-11-22):**
  - 12 mục mới (kiểm thử cơ bản, thời gian, scheduler/dispatcher/`TestScope`, `runTest`, `backgroundScope`, kiểm structured concurrency, `UnconfinedTestDispatcher`, inject dispatcher, kiểm giữa chừng, inject `TestScope`, `setMain` + rule), 3 bug, 3 bài tập, tự trả lời;
  - đổi tiêu đề và phần "bản chất" của A9;
  - thêm nguồn `kx-test`.
- **Kiểm:** report 0 lỗi; track-check không thêm vấn đề; routes-check 103 route, 0 vấn đề.
- **PHẦN 2 HOÀN TẤT.** Tiếp theo là Phần 3 (Deep Dive tr. 234–375: Channel, Select, Hot/cold, Flow intro, Understanding Flow, Flow building, Flow lifecycle, Flow processing, SharedFlow/StateFlow, Testing flow) → viết sâu A7 (có thể tách thành nhiều chương: Channel, Flow cơ bản, toán tử, SharedFlow/StateFlow). Sau đó Phần 4 (tr. 376–449) → A8.


- **CH "Channel và select" (chương mới, 2026-11-22):** đọc Deep Dive tr. 235–262; sim mới `coroutines.chan` (5 loại sức chứa, kết quả khớp output của sách, selfCheck đạt); 3 nguồn API; 3 bug, 2 bài tập. Report 0 lỗi.
- **Chuyển động cho MỌI sơ đồ (2026-11-22, người dùng: "chưa có hoạt cảnh, phải áp dụng cho tất cả sơ đồ và mọi bài"):**
  - lõi (`js/core/diagram.js`, `styles.css`) tự thêm cho mọi sơ đồ dạng thẻ/isometric của 5 track (và track tương lai):
    - token tự chạy giữa node cũ và node mới ở mỗi bước (dọc cạnh, ngược chiều, hoặc bay vòng cung), kể cả khi model không khai báo `movingSignals`;
    - quầng viền chạy vòng quanh node đang xử lý;
    - cạnh kề chảy nét đứt;
  - lanes: thanh đang chạy có viền chạy, vạch "bây giờ" nhịp sáng, token bay giữa các hàng.
- **Kiểm (CDP):**
  - sau một bước, sơ đồ B6/D2/A2/C3/E7/B0 có 4–7 animation chạy, token di chuyển (tọa độ đổi theo thời gian);
  - lanes U2/U3/CH/A1 có 2–4 viền chạy + vạch "bây giờ";
  - reduced-motion: không còn animation;
  - report 0 lỗi; track-check: coroutines 4 vấn đề cũ, runtime/animation/ux 0.
- **Chưa phủ:** các "lab" tự vẽ (Animation C-labs, UX/UI labs như SUS, contrast, Fitts) dùng hình riêng, không qua lõi sơ đồ; chưa thêm chuyển động liên tục cho chúng.
- **FL "Flow từ gốc" (chương mới, 2026-11-22):**
  - nội dung gồm: nóng/lạnh, vì sao cần Flow, đặc điểm và tên gọi, tự dựng Flow từ lambda qua 5 bước, toán tử là `flow { collect { … } }`, trạng thái chung, 3 bug, 2 bài tập, tự trả lời, quiz 3 câu;
  - sim mới `coroutines.flowcall` (lanes ba tầng collect/map/builder, có toggle "collect 2 lần"), cộng tab `hotcold` cũ.
- **Kiểm:** report 0 lỗi; track-check và routes như trên.
- **FB "Tạo flow và vòng đời" (chương mới, 2026-11-22):**
  - nội dung gồm: flowOf/asFlow/Reactive Streams, `flow` và `channelFlow` (lười và tải trước), `callbackFlow` + `awaitClose`, vòng đời (onEach/onStart/onCompletion/onEmpty), `catch` phía trên, `flowOn`/`launchIn` + mẫu Android, 3 bug, 2 bài tập, tự trả lời, quiz 3 câu;
  - sim mới `coroutines.paging` (lanes producer/consumer, chọn `flow` hoặc `channelFlow`; khớp output sách 6000 ms/2 trang và 5000 ms/5 trang);
  - 3 nguồn API mới: `kx-channelflow`, `kx-callbackflow`, `kx-flowon`.
- **Kiểm:** report 0 lỗi; track-check (1280, 360) coroutines vẫn 4 vấn đề cũ (a2#1, a8 undo/clear); routes-check 106 route, 0 vấn đề.
- **Tiếp theo:** chương "Flow processing" (Deep Dive tr. 318–344).
- **FP "Xử lý flow" (chương mới, 2026-11-22):**
  - nội dung gồm: map/filter/take/drop và hiện thực; lần theo chuỗi lambda 1–8; fold/scan (reducer); merge/zip/combine; flatMapConcat/Merge/Latest + `concurrency`; retry/retryWhen (phát lại phần tử đầu); distinctUntilChanged + terminal; 3 bug, 2 bài tập, tự trả lời, quiz 3 câu;
  - 2 sim mới:
    - `coroutines.flatmap`: concat, merge, merge2, latest; khớp output của sách;
    - `coroutines.combine`: merge, zip, combine. Thời điểm của zip suy từ mã `zipImpl`: flow1 đứng "chờ cặp".
  - helper `stLanes` trong `views.js` vẽ hàng từ `params.st`/`params.mk`, dùng lại được cho sim lanes sau;
  - 7 nguồn mới.
- **Kiểm:** report 0 lỗi (2 selfCheck mới PASS); track-check (1280, 360) vẫn 4 vấn đề cũ; routes-check 107 route, 0 vấn đề.
- **Nhắc (người dùng, 2026-11-22):** trước khi viết mỗi track mới, đọc mục lục thật (`tools/epub_toc.py` cho epub, trang đầu cho pdf) rồi sửa dàn chương nháp trong `roadmap-v2.md`.
- **Tiếp theo:** SharedFlow/StateFlow (Deep Dive tr. PDF 345–358), rồi Testing flow (tr. PDF 359–375).
- **A7 viết lại thành "SharedFlow, StateFlow, shareIn và stateIn" (2026-11-22, giữ id `a7`):**
  - module `coroutines_v2_a7.py`: thêm `add()` + `override()` + `SEC_ORDER`;
  - mục mới: recap, shared, sharein, stateflow, statein, bugs (3), exercises (2), recall, quiz q4–q5;
  - hai mục v1 được giữ nhưng đổi tiêu đề và câu chữ: `hot` (người đến muộn, dẫn sang CH) và `ops` (buffer/conflate; bỏ câu cũ "site không mô phỏng flatMap", vì FP đã có);
  - sim mới `coroutines.sharein` (Eagerly / Lazily / WhileSubscribed() / WhileSubscribed(5000)), đứng đầu ba tab; selfCheck chạy lại ví dụ WhileSubscribed của sách;
  - `stLanes` nhận thêm tham số `noOut`.
- **Lõi:** bước tick trục lanes thêm 2000/2500/5000/10000 (trục 15 s trước đây bị dính nhãn).
- **Sửa FB:** câu hỏi dự đoán `onCompletion` thiếu `.collect { println(it) }`.
- **Kiểm:** report 0 lỗi; track-check (1280, 360) vẫn 4 vấn đề cũ; routes-check 107 route, 0 vấn đề.
- **Tiếp theo:** Testing flow (Deep Dive tr. PDF 359–375), mở rộng phần testing của A9 (module `a9t`), không tạo chương mới.
- **A9 thêm phần kiểm thử flow (2026-11-22, module `coroutines_v2_a9f.py`, không tạo chương mới):**
  - mục mới: `tflow` (toList, currentTime, retry), `tinf` (flow vô hạn: 4 cách), `tconn` (đếm kết nối), `tvm` (ViewModel với MutableSharedFlow), `tfbugs` (2 bug), `tfex` (bài tập debounce + flatMapLatest), quiz q3–q4;
  - ghi chú bổ sung điều kiện ngầm mà sách bỏ qua (thay Main, đăng ký trước khi emit).
- **Kiểm:** report 0 lỗi; A9 ở 360px không cuộn ngang.
- **Phần 3 của Coroutines v2 hoàn tất:** CH, FL, FB, FP, A7 (viết lại), kiểm thử flow trong A9.
- **Tiếp theo:** Phần 4 (Deep Dive tr. PDF 376–449) → A8.
- **PR "Coroutines trong thực tế" (chương mới, cuối track, 2026-11-22):**
  - nội dung gồm: tầng dữ liệu (callback, hàm chặn, IO/limitedParallelism, Flow); tầng domain (song song, độc lập, timeout); tầng trình bày (CoroutineWorker, scope tự tạo, runBlocking, collect Flow); launch hay suspend; recipes (sửa 3 lỗi in trong sách); Java interop; 15 best practices có lý do; 3 bug, 2 bài tập, tự trả lời, quiz 3 câu;
  - sim mới `coroutines.launchsusp`: 2 kiểu hàm × 3 sự cố, selfCheck.
- **Sửa A9:** chú thích `app.cash.turbine` bị routes-check coi là lộ khoá; đổi thành "thư viện của Cash App".
- **Kiểm:** report 0 lỗi; track-check (1280, 360) vẫn 4 vấn đề cũ; routes-check 108 route, 0 vấn đề.
- **Coroutines v2 đã phủ toàn bộ sách Deep Dive (Phần 1–4).**
- **Tiếp theo theo `roadmap-v2.md`:** Compose Runtime/Animation v2, rồi UX/UI v2, rồi các track mới. Với mỗi track mới, đọc mục lục thật trước rồi sửa dàn chương nháp.
- **Sửa sau review (2026-11-22):**
  - PR/sim `launchsusp`: hai snippet có `CoroutineExceptionHandler`; lời giải thích nêu rõ khi thiếu handler: JVM → `Thread.uncaughtExceptionHandler`, Android → crash app (nguồn `kx-ceh`, `and-crash` mới). Trước đó câu chữ theo cách viết cho backend của sách ("in ra rồi bỏ qua").
  - Ghi chú lỗi in: chỉ các ví dụ retry cho hàm suspend dùng biến `attempt` sai; ở ví dụ Flow, `attempt` hợp lệ.
  - Soát khẳng định v1 lỗi thời:
    - `a4.sec.ctx.p.1` nói "không có số luồng nào được tài liệu bảo đảm", nay sửa theo tài liệu Dispatchers: Default = số nhân (ít nhất 2), IO = 64;
    - đã kiểm misconceptions (nhãn điều khiển vẫn khớp), A0 (tham chiếu chương vẫn đúng), câu cũ về flatMap ở A7 (đã sửa trước đó);
    - `estMinutes` của track: 300 → 900 (nội dung khoảng 66 nghìn từ, khoảng 440 phút chỉ để đọc).
- **Còn nợ (người dùng đã yêu cầu chuyển động cho toàn bộ bài học):** 6 lab tự vẽ (Animation C-labs, UX/UI labs) chưa có chuyển động liên tục. Làm như việc đầu tiên khi viết Animation/UX/UI v2, hoặc sớm hơn nếu người dùng muốn.
- **Chuyển động cho mọi lab tự vẽ (2026-11-22, theo yêu cầu "toàn bộ bài học"):**
  - lõi thêm `ui.labMotion(root)` (js/core/ui.js); `app.js` gắn nó cho mọi model `compute` khi mount, nên lab hiện có (Animation, UX, UI) và lab sau này tự có;
  - cơ chế: MutationObserver chạy so cấu trúc trước/sau: số chạy dần, SVG nội suy, phần mới hiện dần, phần vừa đổi giữ `.mo-live` (liên tục) tới lần đổi sau; lab tự cập nhật theo frame thì bỏ qua;
  - CSS: `.mo-chg`, `.mo-live` (tắt khi giảm chuyển động và "Chỉ sơ đồ");
  - `docs/design-principles.md` §5.1 thêm dòng "Lab tự vẽ".
- **Kiểm:**
  - SUS: số 76,1 → 77,5 chạy dần;
  - discovery curve: path nội suy, các phần vừa đổi có `.mo-live`;
  - Play của lab Animation: giá trị tăng đều, không bị đè;
  - `--reduce`: 0 animation;
  - track-check UX/UI/Animation 0 vấn đề, 0 lỗi console; routes-check 108 route 0 vấn đề; report 0 lỗi.
- **Runtime v2 bắt đầu (2026-11-22):**
  - **Dàn chương** đã đối chiếu mục lục thật của 3 sách (Kunneth, Compose by Tutorials, Essentials), ghi ở `roadmap-v2.md`. Không có sách về nội bộ Compose, nên cơ chế lấy từ tài liệu chính thức, `how-compose-works.md` và mã AndroidX, ghim commit `296313a4`.
  - **Generator:** `runtime_content.py` có hook module v2 (`runtime_v2_*.py`, cùng khuôn với Coroutines); tái tạo đúng từng byte khi chưa có module.
  - **Chương mới DC "Tư duy khai báo"** (Kunneth Ch.2–3, Thinking in Compose):
    - nội dung: hệ View, khai báo, emit node, năm điều về thân composable, nơi đặt side effect, 3 bug, 2 bài tập, tự trả lời, quiz;
    - sim `runtime.runs`: đếm số lần bấm, số lần thân chạy, số lần side effect chạy; side effect đặt trong thân hoặc trong callback, có hoặc không có animation; có một lượt bị hủy;
    - 3 nguồn sách mới.
  - **Kiểm:** report 0 lỗi (selfCheck PASS); track-check Runtime (1280, 360) 0 vấn đề; routes-check 109 route, 0 vấn đề.
  - **Tiếp theo:** b2 (compiler: `$composer`, group, `changed`, restart group), dựa trên `how-compose-works.md` @296313a4.
- **Đổi tên site, tác giả, git (2026-11-22):**
  - Tên site là **MOBILE DEEP DIVE**, câu tagline "Hiểu Mobile (Android…) từ bên trong". Có favicon riêng (`favicon.svg`, nhúng data URI để chạy được qua `file://`).
  - Tác giả **Kblack**, có link GitHub ở footer và mục "Tác giả" trong trang Về site này.
  - Lịch sử git đã viết lại sang danh tính của người dùng và bỏ dòng ghi công Claude. Mỗi commit đều push lên `origin main` (quy tắc ghi trong `CLAUDE.md`).
- **Tô màu cú pháp cho mọi khối mã (2026-11-23):**
  - Thêm `ADE.syntax.tokenize` (regex, Kotlin) trong `js/core/ui.js`; `ui.codeBlock` tự tô màu. Tác động: chương, sim, lab, bài tập và lời giải. Khối "Kết quả" vẫn để chữ thuần.
  - Bảng màu theo sắc độ One Light / One Dark, chỉnh độ sáng cho ≥ 4.6:1 trên nền khối và trên dòng đang highlight. Bảng đo ở `design-principles.md` §3.1; script `dev/tools/syn_palette.py`.
  - **Kiểm:**
    - `dev/tools/syntax-check.js`: 566 khối (vi + en), 0 dòng sai lệch chữ;
    - đã xem ảnh khối Channel (ch) và mã sim runtime-counter có dòng highlight, ở light và dark;
    - report 0 lỗi; track-check ở 1280 và 360: Runtime, Animation, UX, UI 0 vấn đề, Coroutines chỉ còn 4 mục cũ đã biết (a2#1 undo/clear, a8 undo); 0 lỗi console; routes-check 109 route, 0 vấn đề, không cuộn ngang ở 360;
    - labMotion: khi đổi màu trong lab token editor, chỉ các literal hex bị đổi mới nhấp nháy (trước đây cả dòng); lab Animation không có token nào bị đánh dấu.
  - **Tiếp theo:** b2 (compiler).
- **Runtime v2 · B2 viết lại (2026-11-23):**
  - Nội dung (`runtime_v2_b2.py`): vì sao cần compiler plugin (liên hệ `suspend`/CPS ở U4), nhớ theo vị trí, group và hai luật slot, skip (getter `skipping` thật), vì sao `changed()` phải chạy mọi lượt (`||` của Kotlin có short-circuit, `or` thì không), restart (scope bị invalidate thì không skip; cha skip vẫn restart con), mã thật khác mã giả (tên API ở commit ghim, `$changed`, `$default`, `sourceInformation`, scope trong slot, GapComposer/LinkComposer), 3 bug, 3 bài tập, tự trả lời, quiz 4 câu.
  - Sim mới `runtime.groups`: B(person) → A(…); 4 kịch bản giữa hai lượt (không đổi, Person mới, field là `mutableStateOf`, `var` thường sửa tại chỗ → UI cũ), cùng biến thể mã giả định (`changed()` trong điều kiện short-circuit). Sim cũ `runtime.compiler` giữ làm tab thứ hai.
  - Nguồn mới: `rt-composer-src`, `rt-gapcomposer`, `kt-boolean-or`; `rt-how` trỏ tới commit ghim.
  - Sửa lõi nhỏ: khối đoạn văn v2 có lớp `blk-p` và khoảng cách giữa các khối liền nhau (trước đó các đoạn dính nhau ở mọi chương v2).
  - **Tiếp theo:** b3 (SlotTable, identity, `key()`; phần "Detecting Structural Changes" của `how-compose-works.md`).
- **Runtime v2 · B3 viết lại (2026-11-23):**
  - Nội dung (`runtime_v2_b3.py`): SlotTable (5 số nguyên mỗi group, không con trỏ con, số slot), đọc/ghi và gap buffer, chuỗi group, xóa/chèn/di chuyển qua Pending và insert table, flow-control group, key trùng theo thứ tự, danh sách với `key()`/`items(key)`; 3 bug, 3 bài tập, tự trả lời, quiz 4 câu.
  - Sim mới `runtime.structure` (5 kịch bản theo tài liệu); sim `runtime.keys` giữ làm tab thứ hai.
  - **Kiểm:** report 0 lỗi (selfCheck PASS); track-check Runtime 1280/360 0 vấn đề; routes-check; đã xem ảnh sim.
  - **Tiếp theo:** b4 (State và Snapshot).
- **Runtime v2 · B4 viết lại (2026-11-23):**
  - Nội dung (`runtime_v2_b4.py`): State/MutableState/remember (Kunneth Ch.5), đường đi từ một lần ghi tới recomposition (read/write observer, global write observer, GlobalSnapshotManager trên Android), snapshot và record (quy tắc readable ở commit ghim), policy (equivalent, merge, counterPolicy), derivedStateOf (dùng đúng/sai, cơ chế isInvalidFor), collection không quan sát được, collectAsState/snapshotFlow; 3 bug, 3 bài tập, tự trả lời, quiz 4 câu.
  - Sim mới `runtime.records` (A/B snapshot, apply, xung đột, merge); sim `runtime.snapshot` giữ làm tab thứ hai. 5 nguồn mới.
  - **Kiểm:** report 0 lỗi, 123 cảnh báo (bằng mốc cũ); selfCheck PASS; track-check Runtime 1280/360 0 vấn đề; đã xem ảnh sim.
  - **Tiếp theo:** sh (quản lý state: stateless/stateful, hoisting, rememberSaveable, ViewModel), dựa trên Kunneth Ch.5, Ch.7; Tutorials Ch.7; Essentials Ch.42.
  - **Rà sau B4 (2026-11-23):** goal g1 của b4 sửa thành bước 5 (`applyA`); bug 2 của B2 bỏ hệ quả cụ thể không có nguồn (giờ ghi "không xác định"); goal g1 của B3 viết trung tính (đúng cho cả kịch bản Counters và tab `runtime.keys`); ghi chú ghim commit trong `docs/research/runtime.md` và đầu `models.js` được cập nhật.
  - **Còn nợ (làm khi viết lại từng chương):** chữ "androidx-main, đọc 2026-11-21" trong nội dung v1 của B0, B5, B6; một dòng trong overview của tab `runtime.compiler` (B2) nói tab đó dùng tên API thật ở commit ghim; rà glossary của track cho các thuật ngữ mới (group, slot, restart scope, Pending, insert table, flow-control group, state record, mutation policy, derived state) ở cả hai ngôn ngữ.
- **Runtime v2 · SH chương mới (2026-11-23):**
  - Nội dung (`runtime_v2_sh.py`): vòng cập nhật UI và UDF (Tutorials Ch.7, Essentials Ch.20), stateful/stateless (Kunneth Ch.5), ba luật hoist, ai giữ state (composable, plain state holder, ViewModel; caveat MonotonicFrameClock), sống qua đổi cấu hình/process death (rememberSaveable, Saver, giới hạn Bundle, SavedStateHandle); 3 bug, 3 bài tập, tự trả lời, quiz 4 câu. Ví dụ LiveData của sách được ghi là phiên bản sách.
  - Sim mới `runtime.survive` (5 nơi giữ × 4 sự kiện). Nguồn mới `cp-hoisting`, `cp-saving`.
  - **Kiểm:** report 0 lỗi, 121 cảnh báo; selfCheck PASS; track-check Runtime 1280/360 0 vấn đề; đã xem ảnh sim.
  - **Tiếp theo:** b5 (Recomposer và frame clock).
- **Runtime v2 · B5 viết lại (2026-11-23):**
  - Nội dung (`runtime_v2_b5.py`): Recomposer làm gì, vòng lặp chính theo mã ở commit ghim (chờ việc, xin frame, thứ tự animation → recompose → apply), frame clock trên Android (Choreographer, broadcast frame clock cho effect, viewModelScope không có clock), tạm dừng theo lifecycle; 2 bug, 2 bài tập, tự trả lời, quiz 4 câu. Giữ mục cầu nối X3.
  - Sim mới `runtime.frame` (một lần ghi, animation, vào nền giữa animation); sim `runtime.recomposer` giữ làm tab thứ hai. 3 nguồn mới.
  - **Kiểm:** report 0 lỗi, 121 cảnh báo; selfCheck PASS; track-check Runtime 1280/360 0 vấn đề; đã xem ảnh sim.
  - **Tiếp theo:** ef (side effects và vòng đời: LaunchedEffect, DisposableEffect, SideEffect, rememberUpdatedState, produceState, rememberCoroutineScope), dựa trên Kunneth Ch.7, Tutorials Ch.11, Essentials Ch.33 và trang side-effects.
- **Runtime v2 · EF chương mới (2026-11-23):**
  - Nội dung (`runtime_v2_ef.py`): effect là gì, LaunchedEffect (ví dụ Kunneth, cơ chế remember + RememberObserver ở commit ghim), rememberCoroutineScope, key và rememberUpdatedState, DisposableEffect, SideEffect, produceState, ghi chú lịch sử onActive/onCommit (Tutorials Ch.11); 3 bug, 3 bài tập, tự trả lời, quiz 4 câu.
  - Sim mới `runtime.effects` (bộ đếm Start/Restart/Stop; hẹn giờ có/không rememberUpdatedState). Nguồn mới `rt-effects-src`, `rt-remember-observer`.
  - **Kiểm:** report 0 lỗi, 121 cảnh báo; selfCheck PASS; track-check Runtime 1280/360 0 vấn đề; đã xem ảnh sim.
  - **Tiếp theo:** cl (CompositionLocal), rồi b6, b7, lo, md, lz, b8, b9, pf, b10, b0 theo `roadmap-v2.md`.
- **Runtime v2 · CL chương mới (2026-11-23):**
  - Nội dung (`runtime_v2_cl.py`): vì sao có CompositionLocal (Essentials Ch.21), cung cấp và đọc, compositionLocalOf vs static (KDoc ở commit ghim; ghi rõ chỗ sách dùng static cho màu), khi nào nên/không, slot API (Essentials Ch.22); 2 bug, 2 bài tập, tự trả lời, quiz 4 câu.
  - Sim mới `runtime.locals` (cây C1–C8, dynamic vs static). Nguồn mới `cp-compositionlocal`, `rt-local-src`.
  - **Kiểm:** report 0 lỗi, 121 cảnh báo; selfCheck PASS; track-check Runtime 1280/360 0 vấn đề; đã xem ảnh sim (sửa chú thích hướng cây).
  - **Tiếp theo:** b6 (Composer ghi nhận, Applier áp dụng), rồi b7, lo, md, lz, b8, b9, pf, b10, b0.
- **Runtime v2 · B6 viết lại (2026-11-23):**
  - Nội dung (`runtime_v2_b6.py`): tính và áp thay đổi là hai bước, ComposeNode và Updater, giao diện Applier, insertTopDown vs insertBottomUp (ví dụ trong KDoc), UiApplier trên Android; đối chiếu chuỗi Text → … → ReusableComposeNode của Kunneth với commit ghim (đã hứa ở DC); 2 bug, 2 bài tập, tự trả lời, quiz 4 câu.
  - Sim mới `runtime.insert` (thứ tự chèn × kiểu thông báo); sim `runtime.applier` giữ làm tab thứ hai. 4 nguồn mới.
  - **Kiểm:** report 0 lỗi, 121 cảnh báo; selfCheck PASS; track-check Runtime 1280/360 0 vấn đề; đã xem ảnh sim.
  - **Tiếp theo:** b7 (Composition, Layout, Drawing: ba phase và đọc state theo phase), rồi lo, md, lz, b8, b9, pf, b10, b0.
- **Runtime v2 · B7 viết lại (2026-11-23):**
  - Nội dung (`runtime_v2_b7.py`): ba phase, layout một lượt, đọc state theo phase, hoãn lần đọc (Modifier.offset { }, drawBehind), vòng lặp onSizeChanged; giữ cầu nối X1; 2 bug, 2 bài tập, tự trả lời, quiz 4 câu.
  - Sim mới `runtime.scroll` (đọc ở composition/placement/draw qua 3 frame; vòng lặp hai frame); sim `runtime.phases` giữ làm tab thứ hai.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Runtime 1280/360 0 vấn đề; đã xem ảnh sim.
  - **Tiếp theo:** lo (layout tùy chỉnh và modifier), rồi md, lz, b8, b9, pf, b10, b0.
- **Dọn nợ Runtime v2 (2026-11-23):** glossary Runtime thêm 10 thuật ngữ song ngữ (group, slot, nhớ theo vị trí, insert table, flow-control group, state record, mutation policy, derived state, state hoisting, side effect; `frame-clock` đã có ở Coroutines nên không thêm), `composition-local` trỏ sang chương CL; overview tab `runtime.compiler` (B2) ghi rõ dùng tên API thật ở commit ghim. Report 0 lỗi, 120 cảnh báo; routes-check 112 route 0 vấn đề.
  - **Còn nợ:** chữ "androidx-main, đọc 2026-11-21" trong v1 của B0 (sẽ sửa khi viết lại B0).
- **Runtime v2 · LO chương mới (2026-11-23):**
  - Nội dung (`runtime_v2_lo.py`): mô hình layout một lượt ba bước (Layout basics, Custom layouts, Kunneth Ch.4), Constraints (bốn giá trị, Infinity, bốn loại, KDoc "không thương lượng"), `Modifier.layout` (firstBaselineToTop, exampleLayout của Essentials), `Layout` (MyBasicColumn, SimpleFlexBox của Kunneth), luật đo một lần và thông điệp lỗi ở commit ghim, intrinsic (TwoTexts, định nghĩa KDoc, cài đặt mặc định, override), SubcomposeLayout và BoxWithConstraints; 3 bug, 3 bài tập, tự trả lời, quiz 4 câu.
  - Sim mới `runtime.measure` (cột, đo hai lần, Row không/có IntrinsicSize.Min). 8 nguồn mới (`cp-layout-custom`, `cp-layout-basics`, `cp-intrinsics`, `cp-constraints-mod`, `ui-measurepolicy-src`, `ui-measure-once`, `ui-subcompose-src`, `ui-constraints-src`), đều HTTP 200.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Runtime 1280/360 0 vấn đề, console 0; routes-check 113 route 0 vấn đề; quét chữ chương vi/en không lộ khoá; đã xem ảnh sim (desktop light, 360 dark).
  - **Tiếp theo:** md (Modifier: chuỗi, thứ tự, Modifier.Node; trang constraints-modifiers đã đọc), rồi lz, b8 (kèm annotation runtime), b9, pf, b10, b0.
- **Runtime v2 · MD chương mới (2026-11-23):**
  - Nội dung (`runtime_v2_md.py`): modifier là gì và quy ước tham số (KDoc, Essentials Ch.24, `modifier` vs `Modifier` của Tutorials Ch.6), thứ tự (clip/background, border/padding, clickable/padding, không có margin, mô hình lớp bọc của LO), kích thước/offset/modifier theo scope, trích và dùng lại (then, cấp phát mỗi frame), dưới mui xe (element vs node, `NodeChain.updateFrom`, `actionForModifiers`), ba cách tự viết modifier và Modifier.Node; 3 bug, 3 bài tập, tự trả lời, quiz 4 câu.
  - Sim mới `runtime.chain` (không đổi, đổi màu, thêm border có điều kiện, border/shadow khác lớp). 6 nguồn mới (`cp-modifiers`, `cp-custom-modifiers`, `cp-modifiers-node`, `ui-modifier-src`, `ui-nodechain-src`, `ui-mne-src`), đều HTTP 200.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Runtime 1280/360 0 vấn đề (sửa một câu quiz có inline code quá dài làm tràn ngang ở 360); routes-check 114 route 0 vấn đề; quét chữ vi/en sạch; đã xem ảnh sim.
  - **Tiếp theo:** lz (lazy list bên trong: SubcomposeLayout, key, contentType, tái sử dụng; Tutorials Ch.4, Essentials Ch.34–37, lists docs), rồi b8 (kèm annotation runtime), b9, pf, b10, b0.
- **Runtime v2 · LZ chương mới (2026-11-23):**
  - Nội dung (`runtime_v2_lz.py`): Column hay LazyColumn (Essentials Ch.34, Tutorials Ch.4), DSL LazyListScope và stickyHeader, bên trong (LazyLayout = SubcomposeLayout, cache lambda theo key, SaveableStateProvider), dùng lại slot và contentType (đối chiếu "without needing to recycle"/"destroyed" của sách với pool 7 slot mỗi loại ở mã ghim), key, đọc vị trí cuộn bằng derivedStateOf (sửa cách của Essentials Ch.37), mẹo của tài liệu; 3 bug, 3 bài tập, tự trả lời, quiz 4 câu.
  - Sim mới `runtime.lazy` (cùng contentType, khác contentType, Column + verticalScroll). 4 nguồn mới (`cp-lists`, `fd-lazylayout-src`, `fd-lazycontent-src`, `fd-scrollcheck-src`), đều HTTP 200.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Runtime 1280/360 0 vấn đề; routes-check 115 route 0 vấn đề; quét chữ vi/en sạch; đã xem ảnh sim (sửa chú thích hình cho đúng bố cục ngang).
  - **Chưa xác minh:** phần Tips của trang Lists chỉ đọc qua bản tóm tắt (site có ghi rõ).
  - **Tiếp theo:** b8 (skip, stability, strong skipping, compiler report, và các annotation của runtime theo yêu cầu 2026-11-23), rồi b9, pf, b10, b0.
- **Runtime v2 · B8 viết lại (2026-11-23):**
  - Nội dung (`runtime_v2_b8.py`, override + SEC_ORDER, giữ mục v1 `stability`, `correct`): nhắc lại restartable/skippable và luật `shouldBeRestartable` của compiler, suy luận stability, strong skipping (so ===, lambda tự remember, điều kiện không memoize), compiler report và Layout Inspector, thứ tự sửa stability và file cấu hình, **các annotation của runtime** (yêu cầu 2026-11-23): đã liệt kê thư mục `runtime` và `runtime-annotation` ở commit ghim; dạy `@StableMarker`, `@Stable`, `@Immutable`, `@NonSkippableComposable`, `@NonRestartableComposable`, `@ReadOnlyComposable`, `@ExplicitGroupsComposable`, `@DontMemoize`, `@DisallowComposableCalls`, `@ComposableTarget`/`@ComposableTargetMarker`/`@ComposableOpenTarget`/`@ComposableInferredTarget`, `@ComposeCompilerApi`, `@NoLiveLiterals`, và ba annotation cho lint (`@FrequentlyChangingValue`, `@RememberInComposition`, `@DoNotRetain`); bảng tóm tắt; `@Composable` trỏ về DC/B2. 3 bug, 3 bài tập, tự trả lời, quiz thêm q3, q4.
  - Phát hiện: Compose compiler đã chuyển sang repo JetBrains/kotlin; mã compiler ghim theo tag `v2.4.21` (khớp phiên bản Kotlin của site).
  - Sim mới `runtime.annot` (không annotation, @NonSkippableComposable, @NonRestartableComposable); sim `runtime.skip` giữ làm tab thứ hai. 8 nguồn mới, đều HTTP 200.
  - Glossary Runtime thêm 9 thuật ngữ song ngữ: constraints, đo một lượt, intrinsic measurement, SubcomposeLayout, Modifier.Node, contentType, restartable/skippable, @Stable/@Immutable, compiler report.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Runtime 1280/360 0 vấn đề; routes-check 115 route 0 vấn đề; quét chữ vi/en sạch; đã xem ảnh sim (sửa chú thích hình cho đúng bố cục cây).
  - **Tiếp theo:** b9 (host, semantics, test, accessibility: Kunneth Ch.10, Tutorials Ch.14–15), rồi pf, b10, b0.
  - **Rà sau B8 (2026-11-23):** goal g1 của B8 viết trung tính (đúng cho cả tab `runtime.annot` và `runtime.skip`); bỏ khẳng định "nơi gọi hàm @ReadOnlyComposable không có group" (mã compiler chỉ cho thấy cờ `withGroups` của phạm vi gọi, chưa đủ để khẳng định); bổ sung luật lambda vào đoạn `shouldBeRestartable`.
  - **Còn nợ:** goal g1 của B2, B4, B5, B6, B7 mô tả bước của tab thứ nhất; kiểm lại xem có đúng ở tab thứ hai không (B3 đã làm trung tính). Một số giá trị `stateAfter` của LZ/MD là từ tiếng Anh ngắn (`new ×4`, `reuse`, `insert`), nên đổi sang ký hiệu hoặc tên API khi sửa các file này.
- **Runtime v2 · B9 viết lại (2026-11-23):**
  - Nội dung (`runtime_v2_b9.py`, override + SEC_ORDER, giữ mục v1 `sem`): cây semantics, gộp và luật "con tự gộp đứng riêng", xóa/ghi đè/ẩn semantics, accessibility thực hành theo Tutorials Ch.15, kiểm thử UI theo Kunneth Ch.10 (rule, finder/action/assertion, testTag, thuộc tính semantics riêng), đồng bộ và đồng hồ ảo của test, debug (Layout Inspector, ghi chú phần InspectorInfo của sách dựa trên composed đã cũ); 3 bug, 3 bài tập, tự trả lời, quiz thêm q3, q4.
  - Sim mới `runtime.focus` (Row thường, Row.clickable, clickable + customActions); sim `runtime.semantics` giữ làm tab thứ hai. 4 nguồn mới, đều HTTP 200.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Runtime 1280/360 0 vấn đề; routes-check 115 route 0 vấn đề; quét chữ vi/en sạch; đã xem ảnh sim.
  - **Chưa dùng:** *Android Accessibility by Tutorials* (PDF) cho B9; có thể bổ sung khi làm lại track UI (E10).
  - **Tiếp theo:** pf (hiệu năng và debug: đếm recomposition, Layout Inspector, composition tracing, baseline profile), rồi b10, b0.
- **Runtime v2 · PF chương mới (2026-11-23):**
  - Nội dung (`runtime_v2_pf.py`): đo cho đúng (release, R8, Baseline Profile ~30%), remember phép tính đắt và luật key/contentType chi tiết, derivedStateOf và computedStateOf (Compose 1.13), hoãn lần đọc (ví dụ Jetsnack ba bước), không ghi ngược, công cụ (Layout Inspector đếm recompose/skip, composition tracing, recomposition tracing, Macrobenchmark) và quy trình gợi ý; 3 bug, 2 bài tập, tự trả lời, quiz 4 câu. Manifest đặt PF giữa b9 và b10.
  - Sim mới `runtime.perf` (đọc thẳng, derivedStateOf, ghi ngược). 5 nguồn mới, đều HTTP 200.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Runtime 1280/360 0 vấn đề; routes-check 116 route 0 vấn đề; quét chữ vi/en sạch; đã xem ảnh sim (sửa chú thích bố cục).
  - **Chưa xác minh:** cơ chế bên trong của `computedStateOf` (chưa đọc `ComputedState.kt`).
  - **Tiếp theo:** b10 (Live: luồng +1, cập nhật tham chiếu tới các chương mới), rồi b0 (bản đồ; sửa câu "androidx-main, đọc 2026-11-21").
- **Runtime v2 · B10 viết lại (2026-11-23):**
  - Nội dung (`runtime_v2_b10.py`, override + SEC_ORDER, giữ mục v1 `flow` và sim `runtime.counter` theo lộ trình): tám bước, mỗi bước nối với chương và tên API thật (setter MutableState, GlobalSnapshotManager, restart scope, Recomposer/frame clock, Composer/SlotTable, skip/strong skipping, UiApplier, phase, semantics), hai biến thể của sim, những gì tám bước bỏ qua (gom ghi, bỏ lượt, tạm dừng, lazy, NodeChain, effect), 3 bug định vị theo bước, 2 bài tập, tự trả lời, quiz thêm q3, q4. Không có sim mới (lộ trình ghi "giữ").
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; track-check Runtime 1280/360 0 vấn đề; routes-check 116 route 0 vấn đề; quét chữ vi/en sạch.
  - **Tiếp theo:** b0 (bản đồ toàn cảnh, viết cuối; sửa câu "androidx-main, đọc 2026-11-21").
- **Runtime v2 · B0 viết lại (2026-11-23), RUNTIME V2 XONG:**
  - Nội dung (`runtime_v2_b0.py`, override + SEC_ORDER, giữ mục v1 `roles`, `theme` và sim `runtime.map`): đoán trước, thứ tự đọc cả track (DC → … → B10, gồm các chương mới SH, EF, CL, LO, MD, LZ, PF), chỉ mục "triệu chứng → chương", mục "site nói thật tới đâu" (commit ghim, tag compiler Kotlin, ngày đọc tài liệu, sách là nguồn chính và chỗ lệch được ghi), quiz thêm q3. `simAfter: roles`.
  - Đã xử lý nợ: hai câu "androidx-main, đọc 2026-11-21" (callout `m.compiler.co.impl`, `m.applier.co.coalesce`) nay ghi "ghim androidx-main commit 296313a4"; grep `content.*.js` không còn "đọc 2026-11-21"/"read 2026-11-21".
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; track-check Runtime 1280/360 0 vấn đề; routes-check 116 route 0 vấn đề; quét chữ vi/en sạch.
  - **Tiếp theo:** Compose Animation v2 theo bước 5 của nhiệm vụ định kỳ: (a) đọc mục lục thật của Android Animations by Tutorials (PDF), chương animation trong Kunneth, Tutorials Ch.12, Essentials, tài liệu animation và mã compose/animation ở commit ghim; (b) đọc spec track C và chương hiện có; (c) viết dàn chương Animation v2 vào roadmap-v2.md, tạo docs/research/animation.md, commit riêng; (d) viết chương.
- **Compose Animation v2 · dàn chương (2026-11-23):** đã đọc mục lục thật của *Android Animations by Tutorials* (PDF), Kunneth Ch.8, Tutorials Ch.12, Essentials Ch.39–41, 50, danh mục trang animation của developer.android.com và thư mục `compose/animation` ở commit ghim; spec track C. Dàn 13 chương (giữ c0–c8, thêm vm, if, se, cv) ghi vào `roadmap-v2.md`; ghi chú nguồn vào `docs/research/animation.md`.
  - **Tiếp theo:** thêm cơ chế module v2 vào `dev/gen/animation_content.py`, rồi viết c1 (animate*AsState) theo thứ tự trong roadmap.
- **Animation v2 · C1 viết lại (2026-11-23):**
  - Kỹ thuật: `dev/gen/animation_content.py` có cơ chế module v2 (`for mod in (...)`, add/override/SEC_ORDER), giống Runtime.
  - Nội dung (`animation_v2_c1.py`, giữ mục v1 `retarget` và lab `animation.retarget` làm tab thứ hai): vấn đề đổi state đột ngột (Kunneth Ch.8), API animate*AsState (Kunneth, Essentials Ch.40, Tutorials Ch.12), bên trong ở commit ghim (remember, SideEffect, restartAnimation, UNDISPATCHED; ghi chú bài viết cũ dùng Channel không còn đúng), giới hạn và khi nào cần Animatable; 3 bug, 2 bài tập, tự trả lời, quiz thêm q3, q4.
  - Sim mới `animation.aas` (lần đầu, đổi target, đổi giữa chừng, target không đổi). Nguồn mới `an-aas-src` (HTTP 200).
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Animation 1280/360 0 vấn đề; routes-check 116 route 0 vấn đề; quét chữ vi/en sạch; đã xem ảnh sim.
  - **Tiếp theo:** c2 (AnimationSpec; đọc lại `Easing.kt`, `FloatDecayAnimationSpec.kt`, `SpringSimulation.kt` ở commit ghim, sửa ghi chú "đọc 2026-11-21" trong research).
- **Animation v2 · C2 viết lại (2026-11-23):**
  - Nội dung (`animation_v2_c2.py`, giữ mục v1 `spring`, `more` và lab `animation.spec`): spec là gì (Kunneth, Essentials), easing là cubic-bezier (cách tính fraction), dưới mui xe AnimationVector/TwoWayConverter/vectorize, màu trong Oklab; 2 bug, 2 bài tập, tự trả lời, quiz thêm q3, q4. Sửa hai chỗ "androidx-main, đọc 2026-11-21" (c2 spring.p.2, lab.simp.2) thành tham chiếu commit ghim; URL nguồn easing/decay giờ ghim commit.
  - Sim mới `animation.vector` (Dp/tween, Offset/spring, Color/Oklab, Float/keyframes). 3 nguồn mới, đều HTTP 200.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Animation 1280/360 0 vấn đề; routes-check 116 route 0 vấn đề; quét chữ sạch; đã xem ảnh sim.
  - **Tiếp theo:** c3 (updateTransition; Kunneth Ch.8 multiple values, Tutorials Ch.12 transition, `Transition.kt`).
- **Animation v2 · C3 viết lại (2026-11-23):**
  - Nội dung (`animation_v2_c3.py`, giữ mục v1 `t` và sim `animation.transition`): vì sao cần Transition (JoinButton của Tutorials Ch.12, Kunneth Ch.8), dưới mui xe ở commit ghim (animateTo, currentState, isRunning, chạy lại khi đích con đổi), transitionSpec theo hướng (isTransitioningTo, chỉ FiniteAnimationSpec), MutableTransitionState; 2 bug, 2 bài tập, tự trả lời, quiz thêm q3, q4.
  - Sim mới `animation.segment` (mở rộng, đổi ý giữa chừng, MutableTransitionState). Nguồn mới `an-transition-src` (HTTP 200).
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Animation 1280/360 0 vấn đề; routes-check 116 route 0 vấn đề; quét chữ sạch; đã xem ảnh sim.
  - **Tiếp theo:** c4 (AnimatedVisibility, animateEnterExit, AnimatedContent, Crossfade; Kunneth Ch.8, Essentials Ch.39, AAT Ch.10, `AnimatedVisibility.kt`, `AnimatedContent.kt`), rồi c5, if, c6, se, cv, vm, c7, c8, c0 theo `roadmap-v2.md`.
  - **Còn nợ (Animation):** goal g1 của c1/c2/c3 ở bước 2 chỉ đúng với tab sim mới; tab lab (compute) không có bước nên goal đó chỉ đạt qua tab đầu.
- **Animation v2 · C4 viết lại (2026-11-23):**
  - Nội dung (`animation_v2_c4.py`, giữ mục v1 `vis` và sim `animation.visibility`): ẩn không phải gỡ ngay (KDoc ở commit ghim: chờ mọi animation enter/exit, gỡ và dispose sau exit, kết hợp chạy cùng lúc), animateEnterExit và auto-start (Essentials Ch.39), AnimatedContent/Crossfade và luật dùng tham số lambda; 2 bug, 1 bài tập, tự trả lời, quiz thêm q3. Bản gọn hơn các chương trước vì hạn mức sắp hết.
  - Sim mới `animation.exitlife` (hiệu ứng có sẵn, animation tùy biến trên transition, animateFloatAsState ngoài transition). Nguồn mới `an-av-src` (HTTP 200).
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Animation 1280/360 0 vấn đề; routes-check 116 route 0 vấn đề; quét chữ sạch; đã xem ảnh sim.
  - **Tiếp theo:** c5 (animateContentSize, animateItem, layout vs graphicsLayer; Kunneth Ch.8, AAT Ch.10 và Ch.7, `AnimationModifier.kt`), rồi if, c6, se, cv, vm, c7, c8, c0. Có thể bổ sung sâu thêm cho c4 (AnimatedContent: ContentTransform, SizeTransform, z-order; `AnimatedContent.kt`).
- **Glossary Animation (2026-11-23):** thêm 4 thuật ngữ song ngữ (AnimationVector, TwoWayConverter, MutableTransitionState, currentState của Transition). Report 0 lỗi, 120 cảnh báo.
- **Dừng phiên định kỳ 2026-11-23 ở 92% hạn mức 5 giờ.** Tiếp theo: Animation v2 c5 theo `roadmap-v2.md`.
- **Animation v2 · C5 viết lại (2026-11-23):**
  - Nội dung (`animation_v2_c5.py`, giữ mục v1 `sz` và sim `animation.size` làm tab thứ hai): animateContentSize trong Kunneth Ch.8 và AAT Ch.10; thứ tự modifier theo tài liệu; bên trong ở commit ghim (clipToBounds + SizeAnimationModifierNode, bốn bước của measure, lần đầu không animate, ngắt giữa chừng và finishedListener, chỉ layout chạy lại mỗi frame, onReset, lookahead); item trong list: ItemAnimator của RecyclerView (AAT Ch.7) đối chiếu `Modifier.animateItem()`, cần key, bên trong là placementDelta + GraphicsLayer; 3 bug, 2 bài tập, tự trả lời 3 câu, quiz thêm q3, q4.
  - Sim mới `animation.acs` (trước height, sau height, đổi ý giữa chừng). 4 nguồn mới (`an-acs-src`, `an-lazyscope-src`, `an-lazyanim-src`, `book-aat`), đều HTTP 200. Sửa hai mô tả nguồn en còn ghi "read 2026-11-21".
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Animation 1280/360 0 vấn đề; routes-check 116 route 0 vấn đề; quét chữ vi/en sạch; đã xem ảnh sim.
  - **Tiếp theo:** if (lặp và vô hạn: repeatable, infiniteRepeatable, rememberInfiniteTransition, InfiniteAnimationPolicy; Essentials 39.5, `InfiniteTransition.kt`, `InfiniteAnimationPolicy.kt`), rồi c6, se, cv, vm, c7, c8, c0.
- **Animation v2 · C5 sửa độ chính xác (2026-11-23):** goal g1 trung tính (đúng với cả ba cách viết); câu về mặc định `spring()` của Kunneth viết lại trung tính (sách viết cho phiên bản cũ, không khẳng định phiên bản nào đổi); trích đúng nguyên văn ghi chú TODO.
- **Animation v2 · IF chương mới (2026-11-23):**
  - Nội dung (`animation_v2_if.py`, thêm vào manifest giữa c5 và c6): repeatable (Essentials 39.5, customize; chỉ DurationBased, số lượt lẻ với Reverse, StartOffset), infiniteRepeatable và rememberInfiniteTransition (Kunneth Ch.8, value-based; ghi chú rotate đọc ở composition → graphicsLayer), bên trong InfiniteTransition ở commit ghim (LaunchedEffect + withInfiniteAnimationFrameNanos, durationScale, SideEffect/DisposableEffect, không giữ liên tục), InfiniteAnimationPolicy và kiểm thử (nối C8); 3 bug, 2 bài tập, tự trả lời 3 câu, quiz 4 câu.
  - Sim mới `animation.repeat` (Restart 3, Reverse 3, Reverse 2, vô hạn với durationScale 0 và rời composition). 3 nguồn mới (`an-inftrans-src`, `an-suspend-src`, `ui-infpolicy-src`), đều HTTP 200.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Animation 1280/360 0 vấn đề; routes-check 117 route 0 vấn đề; quét chữ vi/en sạch; đã xem ảnh sim.
  - **Tiếp theo:** c6 (Animatable và gesture: animateTo/snapTo/animateDecay/stop, mutex, VelocityTracker, fling; advanced docs, Essentials Ch.50, AAT Ch.9, `Animatable.kt`, `DecayAnimationSpec.kt`), rồi se, cv, vm, c7, c8, c0.
- **Animation v2 · C6 viết lại (2026-11-23):**
  - Nội dung (`animation_v2_c6.py`, giữ mục v1 `x4` và lab `animation.gesture` làm tab thứ hai): khi nào cần Animatable (Essentials Ch.50 kéo không có đà → cần Animatable; so với animate*AsState; ví dụ tap → animateTo), bên trong ở commit ghim (runAnimation trong MutatorMutex, hủy bằng MutationInterruptedException, liên tục giá trị/vận tốc, initialVelocity, AnimationResult, bounds, snapTo kẹp, @RememberInComposition, InterruptionAwareAnimationSpec), swipe-to-dismiss từng bước theo tài liệu (ghi chú composed → Modifier.Node); 3 bug, 1 bài tập, tự trả lời 3 câu, quiz thêm q3, q4.
  - Sim mới `animation.mutex` (đổi đích giữa chừng, thả chậm trượt về, hất mạnh chạm biên). 2 nguồn mới (`an-animatable-src`, `an-mutex-src`), đều HTTP 200.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Animation 1280/360 0 vấn đề; routes-check 117 route 0 vấn đề; quét chữ vi/en sạch; đã xem ảnh sim.
  - **Tiếp theo:** se (shared element: SharedTransitionLayout, sharedElement/sharedBounds, navigation; shared-elements docs, AAT Ch.4–6, `SharedTransitionScope.kt`), rồi cv, vm, c7, c8, c0.
- **Animation v2 · SE chương mới (2026-11-23):**
  - Nội dung (`animation_v2_se.py`, thêm vào manifest giữa c6 và c7): trước Compose (AAT Ch.6: transitionName, addSharedElement, ChangeBounds) và đối chiếu; ba API chính, sharedElement vs sharedBounds, key data class; bên trong ở commit ghim (LookaheadScope, overlay, khớp key trong một scope, isTransitionActive, isMatchFound; ghi chú phiên bản về opt-in thử nghiệm); thứ tự modifier và resizeMode; navigation và predictive back, giới hạn; 3 bug, 1 bài tập, tự trả lời 2 câu, quiz 4 câu.
  - Sim mới `animation.shared` (cùng key, khác key, clip trước sharedElement). 4 nguồn mới (`an-shared`, `an-shared-custom`, `an-shared-nav`, `an-shared-src`), đều HTTP 200.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Animation 1280/360 0 vấn đề; routes-check 118 route 0 vấn đề; quét chữ vi/en sạch; đã xem ảnh sim.
  - **Tiếp theo:** cv (vẽ và vector động: Canvas + animation, AnimatedVectorDrawable; Essentials Ch.41, vectors docs, AAT Ch.2), rồi vm, c7, c8, c0.
- **Animation v2 · CV chương mới (2026-11-23):**
  - Nội dung (`animation_v2_cv.py`, thêm vào manifest giữa se và c7): hệ View (AAT Ch.2 FavoriteButton, Ch.10 làm lại bằng Compose) và cách nghĩ theo phase; Canvas và DrawScope (Essentials Ch.41) với giá trị animate đọc trong lambda vẽ, drawBehind cho màu (quick guide); AVD trong Compose và bên trong ở commit ghim (updateTransition(atEnd), animator XML → keyframes, spec đảo ngược, VectorPainter có Composition riêng với VectorApplier); 2 bug, 1 bài tập, tự trả lời 2 câu, quiz 4 câu.
  - Sim mới `animation.avd` (Canvas, AVD tới cuối, AVD về đầu). 5 nguồn mới (`an-vectors`, `an-avdpainter-src`, `an-animator-src`, `an-aiv-src`, `ui-vectorpainter-src`), đều HTTP 200.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Animation 1280/360 0 vấn đề; routes-check 119 route 0 vấn đề; quét chữ vi/en sạch; đã xem ảnh sim.
  - **Tiếp theo:** vm (trước Compose: ValueAnimator, ObjectAnimator, interpolator, Transition framework, shared element View; AAT Ch.1–6), rồi c7, c8, c0.
- **Animation v2 · VM chương mới (2026-11-23):**
  - Nội dung (`animation_v2_vm.py`, đặt sau c0 trong manifest đúng dàn chương): ValueAnimator, ObjectAnimator, interpolator (AAT Ch.1), chuỗi tính mỗi frame theo tài liệu Property Animation, XML anim vs animator và cảnh báo view animation (AAT Ch.3), chuyển màn hình và Transition framework (AAT Ch.4–5), bảng đối chiếu View → Compose (gắn nhãn ánh xạ ý niệm); 2 bug, 1 bài tập (AnimatorSet → rememberTransition), tự trả lời 2 câu, quiz 4 câu.
  - Sim mới `animation.vframe` (ObjectAnimator, TranslateAnimation, Compose; ví dụ 40 ms của tài liệu). 1 nguồn mới (`views-prop`, HTTP 200).
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Animation 1280/360 0 vấn đề; routes-check 120 route 0 vấn đề; quét chữ vi/en sạch; đã xem ảnh sim.
  - **Tiếp theo:** c7 (frame clock và phase, giữ X1, X3; Runtime B5, B7, quick-guide), rồi c8, c0.
- **Animation v2 · C7 viết lại (2026-11-23):**
  - Nội dung (`animation_v2_c7.py`, giữ mục v1 `defer` và sim `animation.phaseread` làm tab thứ hai): một frame từ Choreographer tới màn hình (AndroidUiFrameClock, thứ tự trong frame của Recomposer: animation trước, rồi thông báo, recompose, apply; giữ X3), tỉ lệ thời lượng của máy (MotionDurationScale từ ANIMATOR_DURATION_SCALE, tỉ lệ 0 nhảy tới cuối ở frame đầu); 2 bug, 1 bài tập, tự trả lời 2 câu, quiz thêm q3, q4.
  - Sim mới `animation.frameorder` (đọc trong thân, đọc trong graphicsLayer, tỉ lệ 0). Không thêm nguồn mới (dùng lại nguồn Runtime B5 và `an-suspend-src`).
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Animation 1280/360 0 vấn đề; routes-check 120 route 0 vấn đề; quét chữ vi/en sạch; đã xem ảnh sim.
  - **Tiếp theo:** c8 (kiểm thử, công cụ, giảm chuyển động: testing, tooling, Essentials 40.10, Runtime B9), rồi c0 cuối cùng.
- **Animation v2 · C8 viết lại (2026-11-23):**
  - Nội dung (`animation_v2_c8.py`, giữ mục v1 `test` và lab `animation.testclock`): đồng hồ test điều khiển gì theo KDoc của MainTestClock ở commit ghim (2 frame khởi động, làm tròn, ignoreFrameDuration, autoAdvance, vẽ trên Android không theo đồng hồ), viết test theo trang Test animations (runWithoutImplicitWait có nhãn phiên bản), công cụ (Animation Inspector của Essentials so với Animation Preview hiện tại), giảm chuyển động (phần Compose tự làm và phần người viết phải làm); 3 bug, 1 bài tập, tự trả lời 2 câu, quiz thêm q3, q4. Sửa ghi chú v1 "16 ms là minh họa" thành có nguồn.
  - Sim mới `animation.clockstart` (tự tiến, bỏ làm tròn, autoAdvance). 2 nguồn mới (`ui-testclock-src`, `an-tooling`), đều HTTP 200.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck PASS; track-check Animation 1280/360 0 vấn đề; routes-check 120 route 0 vấn đề; quét chữ vi/en sạch; đã xem ảnh sim.
  - **Tiếp theo:** c0 (chọn API theo cây quyết định choose-api; viết cuối cùng), rồi sang UX v2 / UI v2 (đọc mục lục sách trước).
- **Animation v2 · C0 viết lại (2026-11-23), Animation v2 hoàn tất 13 chương:**
  - Nội dung (`animation_v2_c0.py`, giữ mục v1 `pairs` và sim `animation.choose` làm tab thứ hai): bản đồ track và thứ tự đọc, cây quyết định chọn API theo trang choose-api (cấu trúc lồng nhau đọc từ HTML; ghi chú CapturedAnimatedVisibility và TextMotion.Animated chưa giảng), chỉ mục triệu chứng → chương, ghi chú trung thực; tự trả lời 2 câu, quiz thêm q3, q4.
  - Sim mới `animation.tree` (6 nhu cầu đi theo cây tới API và chương).
- **Lõi: goal và tiến độ chương gắn với sim từng bước đầu tiên (2026-11-23, người dùng hỏi về điểm nợ goal của C1–C3):**
  - Kiểm lại: điểm nợ cũ vô hại (tab lab kiểu compute không hiện goal, không ghi tiến độ). Lỗi thật: chương có HAI tab từng bước (đếm trong trang: 32 chương có ≥ 2 sim, trong đó 24 chương có ≥ 2 tab từng bước: coroutines a2, fl, fp, a7, a8, a9; runtime b2–b9; animation c0, c3, c4, c5, c7, c8; ux d0, d5, d10; ui e7) thì tab thứ hai cũng ghi `progress.max/done` chung và hiện danh sách goal viết cho tab đầu, nên goal có thể bị đánh dấu nhầm.
  - Sửa `app.js` (`mountStage`): chỉ sim từng bước ĐẦU TIÊN trong `chapter.sims` hiện goal và gọi `saveProg`; các chương UX có tab đầu là lab (d1, d7, d9) dùng sim từng bước kế tiếp. Đổi tab thì bỏ số bước trên URL để tab mới không nhảy theo bước của tab cũ.
  - Kiểm bằng script trong trang: tab 2 của c3 không hiện goal, đi 3 bước ở tab 2 không ghi tiến độ, tab 1 ghi đúng.
- **UX v2 · dàn chương (2026-11-23):** đọc mục lục thật của Norman, Krug, Whalen, Albert & Tullis, Podmajersky, Metts & Welfle, Greever, Wendel, Design Sprint, Design Thinking Playbook; ghi dàn 15 chương vào `roadmap-v2.md` (giữ d0–d10, thêm sm, kr, wx, ad). Chưa viết chương nào.
  - **Tiếp theo:** kiểm cơ chế module v2 của generator UX, rồi viết d1 theo thứ tự trong roadmap.
- **UI v2 · dàn chương (2026-11-23):** đọc mục lục thật của Tidwell, Neil, MacDonald, Williams, App Design Apprentice; ghi dàn 14 chương vào `roadmap-v2.md` (giữ e0–e10, thêm ia, dv, ap). Mục lục Lupton chưa trích được, ghi rõ phải đọc trước E2.
  - **Tiếp theo (thứ tự đề nghị):** UX v2 d1 (kiểm cơ chế module v2 của `dev/gen/ux_content.py` trước), rồi theo thứ tự UX trong roadmap; UI v2 sau UX.

- **UX v2 · D1 viết lại (2026-11-23):**
  - Nội dung (`ux_v2_d1.py`, module UX v2 đầu tiên; loader nay báo lỗi nếu thiếu file module): sáu "bộ óc" của Whalen (framework của tác giả), thị giác và chú ý (hai kiểu xử lý, saccade, mẫu chữ F ghi rõ là số đo trên máy tính, popout, vùng nhìn nét ~2°, "chỗ không ai nhìn", icon), ba "sự thật" của Krug, kiến thức trong đầu và trong thế giới (Norman Ch.3, Bảng 3.1), Snackbar ở commit ghim (Short 4000 ms dưới TODO, có action thì Indefinite, thời gian khuyến nghị trợ năng từ API 29), mô hình tư duy và system image (Whalen Ch.4, Norman Ch.1), áp vào Hẹn Khám; 3 bug, 1 bài tập, tự trả lời 3 câu, quiz thêm q3, q4. Mục v1 `mem` giữ lại, sửa để đặt hai con số trí nhớ ngắn hạn (NN/g, Norman) cạnh nhau.
  - Sim mới `ux.glance` (ô trống nổi bật / không nổi bật / lưu ý trong thẻ giống khuyến mãi / mã chỉ có trong Snackbar), đứng đầu chương nên goal theo nó (g1 = bước 2 "mắt dừng ở đâu", giống nhau ở cả bốn biến thể). Thứ tự tab: glance, mental, recall; `simAfter: 'hook'`. `reg()` của UX nhận thêm `simpExtra`. Thêm nhãn `impl`, `stable` vào danh sách nhãn của manifest UX.
  - 6 nguồn mới: `book-whalen`, `book-norman`, `book-krug`, `m3-snackbar-src`, `ui-a11ymgr-src`, `and-a11ymgr`. O'Reilly và sensible.com chặn curl (403/406) nhưng mở được trong trình duyệt; ghi trong `docs/research/ux.md`.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck `ux.glance` 3/3 PASS; track-check UX 1280/360 0 vấn đề; routes-check 120 route 0 vấn đề; đã xem ảnh sim (1280, 360); quét chữ vi/en 186 khóa mới sạch; hai URL googlesource mới HTTP 200.
  - **Sửa sau commit đầu (cùng ngày):** goal g1 của d1 ban đầu đặt `step: 1`, nhưng `progress.max` đếm từ 1 (vị trí 0 là trang tổng quan), nên g1 bị đánh dấu ngay ở bước giới thiệu; đổi thành `step: 2` và kiểm trong trang (sau bước 1: chưa xong; sau bước 2: g1 xong; tab Mô hình tư duy không ghi tiến độ; đổi tab bỏ số bước trên URL). Hai chỗ chữ: "phần lớn người" → "nhiều người" cho đúng câu của Whalen; câu về thông báo nhắc lịch của Hẹn Khám ghi rõ là suy ra của site, tách khỏi trích dẫn Norman.
  - **Tiếp theo:** sm (sáu "bộ óc" còn lại của Whalen: Ch.3, Ch.5–7, Part II Ch.9–14, Ch.15–16), rồi d2.
- **UX/UI: màn hình mẫu theo bước thay cho sơ đồ hộp (2026-11-23, người dùng hỏi sơ đồ hộp có hợp với UX/UI không):**
  - Đánh giá: sơ đồ node hợp với track kỹ thuật (chủ thể là các khối như Recomposer, coroutine), nhưng với UX/UI chủ thể là màn hình và con người; sim `ux.glance` vẽ bốn hộp mà không vẽ lưới ô giờ, mắt dò ô, thẻ bị bỏ qua hay Snackbar biến mất. Người dùng chọn làm màn hình mẫu.
  - **Lõi:** `ADE.registerScreen(modelId, fn)`; `mountSim` thêm tab "Màn hình" (mặc định ở lần đầu) khi sim có màn hình, sơ đồ và Timeline giữ ở hai tab bên cạnh. Sim không đăng ký thì không đổi gì. Chuỗi `app.screen`, `app.screenView`. CSS dùng chung `mk-*` (trong điện thoại) và `scr-*` (bên ngoài). Tài liệu: `docs/core-api.md` §4.2.
  - **UX:** `tracks/ux/views/screens.js` vẽ màn hình Hẹn Khám cho `ux.glance` ở cả bốn biến thể: lưới 12/24 ô giờ, chấm số thứ tự mắt dừng (theo số đo của bước), thẻ "0 lần nhìn", màn Xác nhận có lưu ý nhịn ăn, Snackbar có thanh đếm ngược 4 s, màn tin nhắn, hàng "Trong đầu Lan" với các chữ số vượt mức 3–5 của Norman; nút "Nhìn như hệ chú ý" làm mờ và bỏ màu màn hình (mẹo của Whalen). Sửa biến thể lưu ý cho khớp giờ hẹn 14:00 (nhịn ăn từ 06:00, Lan ăn trưa).
  - **Quyết định của người dùng:** CHỈ track UI/UX dùng màn hình mẫu; track cũ và track mới giữ sơ đồ node; thấy track nào cần đổi kiểu sơ đồ thì báo người dùng, không tự đổi.
- **UI/UX tạm dừng, hiển thị "Sắp ra mắt" (2026-11-23, quyết định của người dùng):**
  - Lõi: trạng thái track mới `soon` (`STATUSES` trong registry) và `ADE.trackOpen(t)`. Track `soon` vẫn hiện trên trang chủ, thanh chip và danh mục với nhãn "Sắp ra mắt / Coming soon", nhưng trang track chỉ có khung "Sắp ra mắt"; đường dẫn chương chuyển về trang track; không có cột chương, thanh tiến độ, preset trong Live Explorer, hay kết quả tìm kiếm chương/preset. Nội dung vẫn nạp nên report vẫn kiểm đủ (`resolveRef`, `allPresets` giữ nguyên). Thuật ngữ và hiểu lầm của UX/UI vẫn xem được ở trang chung. Bộ lọc trạng thái trên trang chủ có thêm "Sắp ra mắt".
  - `tracks/ux/manifest.js`, `tracks/ui/manifest.js`: `status: 'soon'`. Muốn mở lại: đổi về `'stable'`.
  - Phần SM đang viết dở (model `ux.minds` và view) cất trong `git stash` ("UX v2 SM chapter WIP …"); chưa có nội dung chương. D1 v2 (đã xong) và cơ chế màn hình mẫu giữ nguyên trong mã.
  - Track-check: từ giờ chỉ chạy cho track đang mở (Coroutines, Runtime, Animation); UX/UI đóng nên không có chương để bấm.
  - **Tiếp theo:** track mới Kotlin (ưu tiên 4 trong roadmap). Theo yêu cầu mới của người dùng: tự chọn phần kiến thức cần và đủ, không bám từng chương sách.
- **P-NEW: track F Kotlin · khung + K1 (2026-11-23, người dùng duyệt dàn ý 14 chương):**
  - Khung track: `tracks/kotlin/` (manifest `status: 'draft'` trong lúc viết, `order: 60`, màu `#78842C` đạt ≥ 3,44 trên cả sáu nền; logKinds dùng lại loại có sẵn trong lõi), generator mới `dev/gen/kotlin_content.py` (module `kotlin_v2_<id>.py`, báo lỗi nếu thiếu module), khối `<script>` trong `index.html` và `dev/report.html`. Không sửa lõi.
  - K1 (`kotlin_v2_k1.py`, 8 mục, mục cơ chế ≤ 4 khối): val/var và suy kiểu (val không bất biến), số (chia nguyên, chuyển kiểu tường minh, tràn số, boxing và cache -128..127), if/when là biểu thức và hàm với tham số mặc định; 2 bug (thanh tiến độ 0%, === trên Int?), bài tập dựa trên "Pretty time display", tự trả lời 2 câu, quiz 4 câu. 7 nguồn, 4 thuật ngữ, 3 hiểu lầm.
  - Sim `kotlin.eval` (chia nguyên, chia cho 2.0, tràn Int, when): mã nguồn → suy kiểu → tính giá trị → biến; goal g1 = bước 2 (suy kiểu).
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck 3/3 PASS; track-check Kotlin 1280/360 0 vấn đề; routes-check 123 route 0 vấn đề (sửa một lỗi lộ khóa `app.kind.check` bằng nhãn loại sự kiện của track); goal kiểm trong trang; đã xem ảnh sim.
  - **Tiếp theo:** K2 (null safety, smart cast, platform type).
- **Kotlin · K2 (2026-11-23):** null safety, smart cast, platform type (`kotlin_v2_k2.py`, 8 mục): kiểu nullable và 5 cách làm việc với nó, nguồn gây NPE theo tài liệu, bảng điều kiện smart cast, platform type T! và chú thích nullability (có Android, JSpecify); 2 bug (!! để qua lỗi smart cast; NPE xa chỗ gọi Java), bài tập dựa trên "Person details display", tự trả lời 2 câu, quiz 4 câu. Sim `kotlin.smartcast` (val cục bộ, var property, property open, var bị lambda sửa, platform type). 3 nguồn mới, 3 thuật ngữ, 2 hiểu lầm.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck 6/6 PASS (cả track); track-check Kotlin 1280/360 0 vấn đề; routes-check 124 route 0 vấn đề; đã xem ảnh sim.
  - **Tiếp theo:** K3 (class, interface, object, thứ tự khởi tạo).
- **Kotlin · K3 (2026-11-23):** class, interface, object và thứ tự khởi tạo (`kotlin_v2_k3.py`, 8 mục): class và property (setter không chạy lúc khởi tạo), final mặc định, interface không giữ trạng thái; hai luật thứ tự khởi tạo và cảnh báo thành viên open; lateinit; object/companion/object expression và thời điểm khởi tạo; 2 bug (setupUi trong init, lateinit binding), bài tập VaccineStock (dựa trên "Implementing the Product class"), tự trả lời 2 câu, quiz 4 câu. Sim `kotlin.init` (lớp cha/con, gọi open trong init, object, lateinit). 5 nguồn mới, 2 thuật ngữ, 2 hiểu lầm.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck 9/9 PASS (cả track); track-check Kotlin 1280/360 0 vấn đề; routes-check 125 route 0 vấn đề; đã xem ảnh sim.
  - **Tiếp theo:** K4 (data class, equals/hashCode, copy).
- **Kotlin · K4 (2026-11-23):** data class và bằng nhau (`kotlin_v2_k4.py`, 8 mục): những gì data class sinh ra (chỉ từ constructor chính), copy nông, == và ===, bảng băm và hợp đồng hashCode, hạn chế mutability (val + copy, UiState trên Android); 2 bug (bỏ chọn không được sau khi sửa họ; hai bệnh nhân bị gộp do note trong thân), bài tập dựa trên "Data class practice", tự trả lời 2 câu, quiz 4 câu. Sim `kotlin.hashset` (sửa sau khi thêm, val + copy, property trong thân, class thường), bucket minh họa. 2 nguồn mới, 2 thuật ngữ, 2 hiểu lầm.
  - **Kiểm:** report 0 lỗi, 120 cảnh báo; selfCheck 12/12 PASS (cả track); track-check Kotlin 1280/360 0 vấn đề; routes-check 126 route 0 vấn đề; đã xem ảnh sim (sửa loại sự kiện tra cứu từ "kiểm kiểu" sang "chạy").
  - **Báo người dùng (không tự làm):** bucket của HashSet có thể dễ hình dung hơn nếu vẽ thành bảng các bucket thay vì sơ đồ node.
  - **Tiếp theo:** K5 (enum, sealed, when).
