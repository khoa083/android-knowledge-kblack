# Android Deep Dive Explorer

*Tiếng Việt ở trên · English below*

---

## Tiếng Việt

Website học tập tương tác, song ngữ Việt–Anh, chạy **offline**. Các track:

| Mã | Track | Lĩnh vực | Trạng thái |
|---|---|---|---|
| A | Kotlin Coroutines Explorer | Engineering | có |
| B | Compose Runtime Explorer | Engineering | có |
| C | Compose Animation Lab | Engineering | có |
| D | Thiết kế cho cách con người nghĩ (UX) | Design | sắp ra mắt |
| E | Giao diện Android: từ nguyên lý đến design system (UI) | Design | sắp ra mắt |
| F | Kotlin: cơ chế ngôn ngữ | Engineering | có |
| G | Kiến trúc app Android | Engineering | đang viết |
| H–K | Lưu dữ liệu; Thiết kế hệ thống phía mobile; Mã sạch; Lập trình hàm với Kotlin | Engineering | dàn ý chờ duyệt (`docs/tracks/`) |

Mô phỏng là **mô hình giảng dạy** viết bằng JavaScript: không chạy Compose hay kotlinx.coroutines thật, không phải công cụ nghiên cứu người dùng hay kiểm định accessibility. Mỗi mô phỏng nêu rõ phần giản lược.

### Cách mở
Bấm đúp `index.html`. Không cần server, internet, cài đặt hay build. Đã kiểm bằng Chrome và Edge qua `file://`.

### Cách dùng
- **Guided**: đi theo chương; mỗi bước cập nhật sơ đồ, mã và nhật ký sự kiện cùng lúc. Nút Trước/Tiếp, Phát/Tạm dừng, tốc độ; phím tắt xem bằng `?`.
- **Live Explorer**: chọn preset của từng track, tự do tác động sandbox.
- Lab (Animation, UX, UI) có điều khiển riêng: Step frame, Đổi target, đo cá nhân… Số đo cá nhân chỉ nằm trong bộ nhớ trang, **không lưu, không gửi đi**.
- Đổi ngôn ngữ (VI/EN) giữ nguyên chương, bước và trạng thái mô phỏng. `localStorage` (tiền tố `ade.`) chỉ lưu tiến độ, ngôn ngữ, theme và vài tuỳ chọn hiển thị.
- Tôn trọng `prefers-reduced-motion`; có nút "Giảm chuyển động".
- Tìm kiếm (Ctrl K) không phân biệt dấu: chuỗi được chuẩn hóa NFD, bỏ dấu kết hợp, đổi đ→d và về chữ thường, nên gõ "tuong phan" vẫn tìm thấy "tương phản".

### Cấu trúc
```
index.html, styles.css, app.js     khung site (không chứa id track nào)
js/core/                           lõi: i18n, registry, engine, diagram, ui, controls, search, router
i18n/ui.vi.js, ui.en.js            chuỗi giao diện chung (khoá app.*)
shared/                            nguồn chung, glossary, cầu nối X1–X8, lộ trình, trang Về site, mock app "Hẹn Khám"
tracks/<id>/                       manifest, content.vi/en, code, sources, glossary, misconceptions, models/, views/
dev/report.html                    báo cáo kiểm tra (song ngữ, registry, nguồn, ví dụ kiểm chứng)
dev/tools/                         công cụ kiểm thử (Chrome headless qua CDP), sinh sources.md
dev/gen/                           script sinh content.vi/en.js của các track từ một nguồn (công cụ phát triển, site không cần)
docs/                              tiến độ, hợp đồng lõi, nghiên cứu từng track, checklist
sources.md                         danh sách nguồn song ngữ (sinh bằng node dev/tools/sources-md.js)
```

### Thêm một track
1. Tạo `tracks/<id>/` theo thứ tự file trong `docs/core-api.md` mục 1; id không trùng danh sách cấm.
2. `manifest.js` gọi `ADE.registerTrack({...})` (chương, preset, logKinds, nhãn).
3. `content.vi.js` và `content.en.js` **cùng cây khoá** `track.<id>.*` (nên sinh từ một nguồn như `dev/gen/*.py`).
4. Model thuần trong `models/` (`ADE.registerModel`, chỉ phát message key), view trong `views/` (`ADE.registerView`).
5. Thêm khối `<script>` của track vào **cả** `index.html` và `dev/report.html`.
6. Mở `dev/report.html`: phải 0 lỗi; chạy `node dev/tools/cdp.js` với `track-check.js`, `routes-check.js`, `controls-sweep.js`.
Không cần sửa `js/core` hay `app.js`: catalog, điều hướng, tìm kiếm, Live Explorer, glossary, hiểu lầm, nguồn tự sinh từ registry.

### Thêm một ngôn ngữ
1. Thêm mã ngôn ngữ vào `ADE.langs` (`js/core/i18n.js`).
2. Tạo `i18n/ui.<lang>.js`, `shared/*.<lang>.js`, `tracks/*/content.<lang>.js` (và glossary, misconceptions) cùng cây khoá.
3. Thêm script tương ứng vào hai file HTML; `dev/report.html` sẽ báo khoá thiếu.

### Kiểm tra
- `dev/report.html`: song ngữ (cùng cây khoá, NFC, markup khớp), registry, nguồn, glossary, mọi khoá model phát ra, ví dụ kiểm chứng.
- `node dev/tools/cdp.js "<url file://>" --eval "$(cat dev/tools/track-check.js)" --pre "window.__TRACK='<id>'"` (thêm `--w 360 --h 800 --mobile` cho điện thoại).

---

## English

An interactive, bilingual (Vietnamese–English) learning site that runs **offline**. Tracks:

| Code | Track | Domain | Status |
|---|---|---|---|
| A | Kotlin Coroutines Explorer | Engineering | available |
| B | Compose Runtime Explorer | Engineering | available |
| C | Compose Animation Lab | Engineering | available |
| D | Designing for How People Think (UX) | Design | coming soon |
| E | Android UI: From Principles to Design Systems (UI) | Design | coming soon |
| F | Kotlin: How the Language Works | Engineering | available |
| G | Android App Architecture | Engineering | in progress |
| H–K | Saving Data; Mobile System Design; Clean Code and Craft; Functional Programming in Kotlin | Engineering | outlines awaiting approval (`docs/tracks/`) |

The simulations are **teaching models** written in JavaScript: they do not run real Compose or kotlinx.coroutines, and they are not a user-research or accessibility-audit tool. Every simulation states what it simplifies.

### Opening
Double-click `index.html`. No server, internet, install or build. Tested in Chrome and Edge over `file://`.

### Using it
- **Guided**: follow a chapter; each step updates the diagram, code and event log together. Previous/Next, Play/Pause, speed; press `?` for shortcuts.
- **Live Explorer**: pick a preset per track and play freely with the sandbox.
- Labs (Animation, UX, UI) have their own controls: step frame, change target, personal measurements… Personal measurements stay in page memory only — **never saved or sent**.
- Switching language (VI/EN) keeps the chapter, step and simulation state. `localStorage` (prefix `ade.`) stores only progress, language, theme and a few display options.
- Respects `prefers-reduced-motion`; there is also a "Reduce motion" button.
- Search (Ctrl K) ignores diacritics: text is NFD-normalised, combining marks are removed, đ→d, lower-cased, so "tuong phan" finds "tương phản".

### Structure
See the tree above. The core (`js/core`, `app.js`) contains no track id; every track registers itself through its `manifest.js`.

### Adding a track
1. Create `tracks/<id>/` following the file order in `docs/core-api.md` §1; the id must not be a reserved word.
2. `manifest.js` calls `ADE.registerTrack({...})` (chapters, presets, log kinds, labels).
3. `content.vi.js` and `content.en.js` share **the same key tree** `track.<id>.*` (best generated from one source, like `dev/gen/*.py`).
4. Pure models in `models/` (`ADE.registerModel`, message keys only), views in `views/` (`ADE.registerView`).
5. Add the track's `<script>` block to **both** `index.html` and `dev/report.html`.
6. Open `dev/report.html`: it must show 0 errors; run `node dev/tools/cdp.js` with `track-check.js`, `routes-check.js`, `controls-sweep.js`.
No change to `js/core` or `app.js` is needed: the catalog, navigation, search, Live Explorer, glossary, misconceptions and sources are generated from the registry.

### Adding a language
1. Add the language code to `ADE.langs` (`js/core/i18n.js`).
2. Create `i18n/ui.<lang>.js`, `shared/*.<lang>.js`, `tracks/*/content.<lang>.js` (plus glossary and misconceptions) with the same key tree.
3. Add the scripts to both HTML files; `dev/report.html` reports any missing key.

### Checks
- `dev/report.html`: bilingual parity (same keys, NFC, matching markup), registry, sources, glossary, every key a model emits, verification examples.
- `node dev/tools/cdp.js "<file:// url>" --eval "$(cat dev/tools/track-check.js)" --pre "window.__TRACK='<id>'"` (add `--w 360 --h 800 --mobile` for phones).
