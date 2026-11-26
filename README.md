# Android Deep Dive Explorer

**Học Android qua cơ chế bên dưới, bằng mô phỏng tương tác. Song ngữ Việt–Anh, chạy offline.**
*Interactive simulations of how Android, Kotlin and Compose work under the hood. Bilingual, fully offline.*

[Tiếng Việt](#tiếng-việt) · [English](#english)

---

## Tiếng Việt

### Giới thiệu

Android Deep Dive Explorer là một website học tập. Mỗi chương mở đầu bằng một lỗi thật mà lập trình viên Android hay gặp, rồi giải thích cơ chế gây ra lỗi đó qua một mô phỏng đi từng bước. Mục tiêu là hiểu *vì sao* chương trình chạy như vậy, để tự tìm và sửa được lỗi.

- **Chạy offline:** bấm đúp `index.html` là dùng được. Không cần server, mạng, cài đặt hay build.
- **Song ngữ:** mọi nội dung có bản tiếng Việt và tiếng Anh, cùng nội dung và cùng nguồn. Đổi ngôn ngữ giữ nguyên chương, bước và trạng thái mô phỏng.
- **Nhìn được cơ chế:** sơ đồ, mã nguồn và bảng sự kiện cập nhật cùng lúc ở từng bước.
- **Trung thực về độ giản lược:** mô phỏng là mô hình giảng dạy viết bằng JavaScript, không chạy Compose hay kotlinx.coroutines thật. Mỗi mô phỏng ghi rõ nó giản lược điều gì. Mỗi chương ghi nguồn và ngày đọc nguồn.

### Nội dung

| Mã | Track | Số chương | Trạng thái |
|---|---|---:|---|
| A | Kotlin Coroutines Explorer | 20 | Ổn định |
| B | Compose Runtime Explorer | 19 | Ổn định |
| C | Compose Animation Lab | 13 | Ổn định |
| F | Kotlin: cơ chế ngôn ngữ | 14 | Ổn định |
| G | Kiến trúc app Android | 12 | Ổn định |
| H | Lưu dữ liệu trên Android | 10 | Ổn định |
| I | Thiết kế hệ thống phía mobile | 14 | Ổn định |
| J | Mã sạch và kỷ luật làm nghề | 12 | Ổn định |
| K | Lập trình hàm với Kotlin | 11 | Ổn định |
| L | Gỡ lỗi và hiệu năng Android | 13 | Ổn định |
| M | Nền tảng Android: component và vòng đời | 17 (dự kiến) | Đã duyệt dàn ý, chưa viết |
| D | Thiết kế cho cách con người nghĩ (UX) | — | Tạm dừng |
| E | Giao diện Android: từ nguyên lý đến design system (UI) | — | Tạm dừng |

Mỗi track mở đầu bằng một **bản đồ triệu chứng**: gặp lỗi X thì đọc chương nào. **Cầu nối** (X1–X35) liên kết các chương có liên quan giữa các track.

Chương thường gồm các phần sau, mỗi phần kèm ví dụ mã:
1. vấn đề cần giải quyết;
2. giảng từng bước;
3. cơ chế bên dưới;
4. mô phỏng;
5. hai lỗi thật;
6. bài tập;
7. câu hỏi tự kiểm.

### Bắt đầu

1. Clone hoặc tải repo về máy.
2. Mở `index.html` bằng Chrome hoặc Edge (đường dẫn `file://`).

Không có bước nào khác.

### Cách dùng

- **Guided:** học theo chương.
  - Dùng nút Trước, Tiếp, Phát, Tạm dừng và chỉnh tốc độ.
  - Bấm `?` để xem phím tắt.
- **Live Explorer:** chọn preset của một track rồi tự thay đổi điều kiện trong mô phỏng.
- **Tìm kiếm** (`Ctrl K`): không phân biệt dấu. Gõ "tuong phan" vẫn ra "tương phản".
- **Trợ năng:**
  - tôn trọng `prefers-reduced-motion`, có nút "Giảm chuyển động";
  - có giao diện sáng và tối;
  - giao diện vẫn dùng được trên điện thoại.
- **Quyền riêng tư:**
  - `localStorage` (tiền tố `ade.`) chỉ lưu tiến độ, ngôn ngữ, giao diện và vài tùy chọn hiển thị;
  - site không gửi dữ liệu đi đâu.

### Kiến trúc

| Thành phần | Vai trò |
|---|---|
| `index.html`, `styles.css`, `app.js` | Khung site. Không chứa id của track nào |
| `js/core/` | Lõi: i18n, registry, engine mô phỏng, sơ đồ, UI, điều khiển, tìm kiếm, router |
| `i18n/` | Chuỗi giao diện chung (`ui.vi.js`, `ui.en.js`) |
| `shared/` | Nguồn, thuật ngữ, hiểu lầm thường gặp, cầu nối, lộ trình, trang giới thiệu, app mẫu "Hẹn Khám" |
| `tracks/<id>/` | Mỗi track: `manifest.js`, nội dung vi và en, mã ví dụ, nguồn, thuật ngữ, hiểu lầm, `models/`, `views/` |
| `dev/` | Trang kiểm tra (`report.html`), công cụ kiểm thử headless (`tools/`), generator nội dung (`gen/`) |
| `docs/` | Hợp đồng lõi, dàn ý và nghiên cứu từng track, tiến độ, lộ trình |
| `sources.md` | Danh sách nguồn song ngữ, sinh bằng `node dev/tools/sources-md.js` |

Các nguyên tắc thiết kế:
- **Không phụ thuộc gì cả:**
  - không có ES module, `fetch()`, CDN, webfont hay framework;
  - dữ liệu là các file `.js` thường, gắn vào `window.ADE`.
- **Track tự đăng ký:**
  - Mỗi track gọi `ADE.registerTrack` trong `manifest.js`.
  - Lõi sinh từ registry: danh mục, điều hướng, tìm kiếm, Live Explorer, thuật ngữ và trang nguồn.
  - Thêm track không phải sửa `js/core` hay `app.js`.
- **Tách model và chữ hiển thị:**
  - Model chỉ phát message key, không chứa chữ hiển thị.
  - Nội dung vi và en dùng chung một cây khóa, sinh từ một nguồn Python trong `dev/gen/`.

### Phát triển

**Thêm một track**
1. Tạo `tracks/<id>/` theo thứ tự file trong `docs/core-api.md` §1. Id không được trùng danh sách từ khóa cấm.
2. `manifest.js` gọi `ADE.registerTrack({...})`, khai báo chương, preset, loại sự kiện và nhãn.
3. Tạo `content.vi.js` và `content.en.js` với **cùng cây khóa** `track.<id>.*`. Nên sinh hai file này từ một generator trong `dev/gen/`.
4. Viết model thuần trong `models/` (`ADE.registerModel`) và view trong `views/` (`ADE.registerView`).
5. Thêm các thẻ `<script>` của track vào **cả** `index.html` và `dev/report.html`.

**Thêm một ngôn ngữ**
1. Thêm mã ngôn ngữ vào `ADE.langs` trong `js/core/i18n.js`.
2. Tạo `i18n/ui.<lang>.js`, `shared/*.<lang>.js`, `tracks/*/content.<lang>.js` (kèm thuật ngữ và hiểu lầm) với cùng cây khóa.
3. Thêm script vào hai file HTML. `dev/report.html` sẽ báo các khóa còn thiếu.

**Kiểm tra trước khi commit**

| Kiểm tra | Cách chạy | Kiểm gì |
|---|---|---|
| Báo cáo tổng | Mở `dev/report.html` (phải 0 lỗi) | Hai ngôn ngữ cùng cây khóa, Unicode NFC, markup khớp, registry, nguồn, thuật ngữ, mọi khóa model phát ra, ví dụ kiểm chứng |
| Từng track | `node dev/tools/cdp.js "<url file://>" --eval "$(cat dev/tools/track-check.js)" --pre "window.__TRACK='<id>'"` | Mọi chương, bước và hình của track |
| Điện thoại | Thêm `--w 360 --h 800 --mobile` | Bố cục ở màn hình hẹp |
| Khác | `routes-check.js`, `controls-sweep.js`, `motion-check.js`, `focus-check.js` | Điều hướng, điều khiển, chuyển động của hình, focus bàn phím |

Công cụ kiểm thử chạy Chrome headless qua giao thức DevTools và chỉ cần Node.js.

### Nguồn

Nội dung lấy từ tài liệu chính thức (developer.android.com, kotlinlang.org, mã nguồn AOSP và AndroidX có ghi phiên bản) và sách chuyên ngành. Khi có mâu thuẫn, tài liệu chính thức được ưu tiên. Danh sách đầy đủ nằm ở [`sources.md`](sources.md) và trên trang Nguồn của từng track.

Đây là dự án học tập cá nhân.

---

## English

### Overview

Android Deep Dive Explorer is a learning site. Each chapter starts from a real bug that Android developers commonly hit. It then explains the mechanism behind that bug with a step-by-step simulation. The goal is to understand *why* code behaves the way it does, so you can find and fix such bugs yourself.

- **Fully offline:** double-click `index.html`. No server, network, install or build step.
- **Bilingual:** everything exists in Vietnamese and English, with the same content and the same sources. Switching language keeps the chapter, step and simulation state.
- **The mechanism made visible:** the diagram, code and event table update together at every step.
- **Honest about simplification:** simulations are teaching models written in JavaScript; they do not run real Compose or kotlinx.coroutines. Each one states what it simplifies. Every chapter lists its sources and the date they were read.

### Contents

| Code | Track | Chapters | Status |
|---|---|---:|---|
| A | Kotlin Coroutines Explorer | 20 | Stable |
| B | Compose Runtime Explorer | 19 | Stable |
| C | Compose Animation Lab | 13 | Stable |
| F | Kotlin: How the Language Works | 14 | Stable |
| G | Android App Architecture | 12 | Stable |
| H | Saving Data on Android | 10 | Stable |
| I | Mobile System Design | 14 | Stable |
| J | Clean Code and Craft | 12 | Stable |
| K | Functional Programming in Kotlin | 11 | Stable |
| L | Android Debugging and Performance | 13 | Stable |
| M | Android Platform Fundamentals: Components and Lifecycles | 17 (planned) | Outline approved, not yet written |
| D | Designing for How People Think (UX) | — | Paused |
| E | Android UI: From Principles to Design Systems (UI) | — | Paused |

Each track opens with a **symptom map** that tells you which chapter to read for a given bug. **Bridges** (X1–X35) link related chapters across tracks.

A typical chapter has these parts, each with code examples:
1. the problem to solve;
2. a step-by-step explanation;
3. the underlying mechanism;
4. a simulation;
5. two real bugs;
6. an exercise;
7. self-check questions.

### Getting started

1. Clone or download the repository.
2. Open `index.html` in Chrome or Edge (a `file://` URL).

There are no other steps.

### Using the site

- **Where to start:** the home page has a "Where to start?" section with a six-step path for newcomers (Kotlin → Coroutines → Architecture → Storage → Compose Runtime → Compose Animation), each step with one line on why it comes next.
- **Guided:** learn chapter by chapter.
  - Use Previous, Next, Play and Pause, and adjust the speed.
  - Press `?` to see the keyboard shortcuts.
- **Live Explorer:** pick a track preset and change the conditions of the simulation yourself.
- **Search** (`Ctrl K`): ignores diacritics. "tuong phan" finds "tương phản".
- **Accessibility:**
  - respects `prefers-reduced-motion`, and has a "Reduce motion" button;
  - has light and dark themes;
  - the interface works on phones.
- **Privacy:**
  - `localStorage` (prefix `ade.`) stores only progress, language, theme and a few display options;
  - the site sends no data anywhere.

### Architecture

| Part | Role |
|---|---|
| `index.html`, `styles.css`, `app.js` | Site shell. Contains no track id |
| `js/core/` | Core: i18n, registry, simulation engine, diagrams, UI, controls, search, router |
| `i18n/` | Shared UI strings (`ui.vi.js`, `ui.en.js`) |
| `shared/` | Sources, glossary, common misconceptions, bridges, learning paths, about page, the "ClinicBook" sample app |
| `tracks/<id>/` | One folder per track: `manifest.js`, vi and en content, code samples, sources, glossary, misconceptions, `models/`, `views/` |
| `dev/` | Check page (`report.html`), headless test tools (`tools/`), content generators (`gen/`) |
| `docs/` | Core contract, per-track outlines and research, progress, roadmap |
| `sources.md` | Bilingual source list, generated by `node dev/tools/sources-md.js` |

Design principles:
- **No dependencies:**
  - no ES modules, `fetch()`, CDN, web fonts or framework;
  - data is plain `.js` files attached to `window.ADE`.
- **Tracks register themselves:**
  - Each track calls `ADE.registerTrack` in its `manifest.js`.
  - The core builds everything else from the registry: the catalog, navigation, search, Live Explorer, glossary and source pages.
  - Adding a track needs no change to `js/core` or `app.js`.
- **Models are separate from text:**
  - Models emit message keys only and hold no display text.
  - The vi and en content share one key tree, generated from a single Python source in `dev/gen/`.

### Development

**Adding a track**
1. Create `tracks/<id>/` following the file order in `docs/core-api.md` §1. The id must not be a reserved word.
2. `manifest.js` calls `ADE.registerTrack({...})` to declare chapters, presets, event kinds and labels.
3. Create `content.vi.js` and `content.en.js` with **the same key tree** `track.<id>.*`. Generate both from one generator in `dev/gen/`.
4. Write pure models in `models/` (`ADE.registerModel`) and views in `views/` (`ADE.registerView`).
5. Add the track's `<script>` tags to **both** `index.html` and `dev/report.html`.

**Adding a language**
1. Add the language code to `ADE.langs` in `js/core/i18n.js`.
2. Create `i18n/ui.<lang>.js`, `shared/*.<lang>.js` and `tracks/*/content.<lang>.js` (plus glossary and misconceptions) with the same key tree.
3. Add the scripts to both HTML files. `dev/report.html` reports any missing key.

**Checks before committing**

| Check | How to run | What it checks |
|---|---|---|
| Full report | Open `dev/report.html` (must show 0 errors) | Same key tree in both languages, Unicode NFC, matching markup, registry, sources, glossary, every key a model emits, verification examples |
| One track | `node dev/tools/cdp.js "<file:// url>" --eval "$(cat dev/tools/track-check.js)" --pre "window.__TRACK='<id>'"` | Every chapter, step and visual of the track |
| Phones | Add `--w 360 --h 800 --mobile` | Layout on narrow screens |
| Others | `routes-check.js`, `controls-sweep.js`, `motion-check.js`, `focus-check.js` | Navigation, controls, visual motion, keyboard focus |

The test tools drive headless Chrome through the DevTools protocol and need only Node.js.

### Sources

Content comes from official documentation (developer.android.com, kotlinlang.org, versioned AOSP and AndroidX source code) and technical books. When they conflict, the official documentation wins. The full list is in [`sources.md`](sources.md) and on each track's Sources page.

This is a personal learning project.
