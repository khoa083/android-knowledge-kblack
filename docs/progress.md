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
