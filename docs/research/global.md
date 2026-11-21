# Nghiên cứu toàn cục (P0)

> Ngày đối chiếu: **2026-11-20**. Mọi số liệu dưới đây lấy trực tiếp từ nguồn nêu cạnh, không lấy từ trí nhớ.
> File này là đầu ra của P0; các phase sau đọc lại thay vì tra lại.

## 1. Thư mục đích

- Đường dẫn cuối: `E:\AndroidDeepDiveExplorer`.
- Lúc bắt đầu P0, thư mục chỉ có `CLAUDE.md` (không có `docs/`) → dùng nguyên thư mục này, theo master mục 3. Không ghi đè gì.
- Thư mục prompt `E:\AndroidDeepDiveExplorer-Prompts` và thư mục sách `E:\AndroidBooks` chỉ được đọc.

## 2. Phiên bản và ngày đối chiếu

| Hạng mục | Giá trị đã chốt | Nguồn đã dùng |
|---|---|---|
| Ngày đối chiếu | 2026-11-20 | — |
| Kotlin | **2.4.21** (stable, phát hành 2026-10-08). Có `2.5.0-RC` trên Maven nhưng trang releases ghi 2.5.0 "dự kiến tháng 12/2026" nên không dùng | `repo1.maven.org` maven-metadata của `kotlin-stdlib`; trang kotlinlang.org/docs/releases.html; GitHub releases `JetBrains/kotlin` |
| kotlinx.coroutines | **1.11.0** (2026-05-08) | maven-metadata `kotlinx-coroutines-core`; GitHub releases |
| Compose BOM | **2026.11.01** (metadata cập nhật 2026-11-19) | maven-metadata `compose-bom` và file POM `compose-bom-2026.11.01.pom` |
| `compose.runtime:runtime` | **1.13.0** | POM của BOM 2026.11.01 |
| `compose.ui:ui` | **1.13.0** | POM của BOM |
| `compose.animation:animation` (và `animation-core`) | **1.13.0** | POM của BOM |
| `compose.foundation:foundation` | 1.13.0 | POM của BOM |
| `compose.material3:material3` | **1.5.0** | POM của BOM |
| `material3-adaptive` | 1.3.0 là bản stable mới nhất theo metadata (không nằm trong BOM; bản `1.4.0-alpha03` chưa dùng). **E4 xác nhận lại** | maven-metadata `material3/adaptive/adaptive` |
| Compose Compiler | Là **Gradle plugin `org.jetbrains.kotlin.plugin.compose`**, đi cùng Kotlin và dùng **cùng số phiên bản với Kotlin → 2.4.21** (từ Kotlin 2.0.0). **Không** ghi artifact cũ `androidx.compose.compiler:compiler` (1.5.x) cho Kotlin 1.x. Trang Android còn ví dụ `2.4.10`; đó chỉ là số ví dụ trong tài liệu | developer.android.com/develop/ui/compose/compiler; kotlinlang.org/docs/compose-compiler-migration-guide.html; plugin 2.4.21 tồn tại trên Maven |
| Strong skipping | **Bật mặc định từ Kotlin 2.0.20**; trước đó phải bật thủ công. Gắn nhãn `version` | developer.android.com/develop/ui/compose/performance/stability/strongskipping |
| AndroidX Lifecycle | **2.11.1** (`lifecycle-runtime-compose`, stable). Có `2.12.0-alpha06`, không dùng | maven-metadata `lifecycle-runtime-compose`; POM 2.11.1 tồn tại |
| WCAG | **2.2**, W3C Recommendation ngày **2024-12-12** | www.w3.org/TR/WCAG22/ |
| Material 3 | Đối chiếu **2026-11-20**. **Giá trị token (type scale, color roles, easing/duration) chưa đọc ở P0**; P6 đọc từ trang chính thức rồi ghi lại tại `docs/research/ui.md` | Mới kiểm URL (mục 3) |
| Android design guidance | Đối chiếu URL **2026-11-20**. Breakpoint window size class và kích thước target: đọc ở P6 | Mới kiểm URL |
| Commit AndroidX cho chi tiết nội bộ | **Chưa chốt**: việc của P3 (đọc mã nguồn hiện hành rồi ghi commit và đường dẫn) | — |

Ghi chú: `runtime/ui/animation 1.14.0-alpha01` và `material3 1.6.0-alpha01` đã có nhưng là alpha, ngoài BOM. Site chỉ trích bản trong BOM 2026.11.01.

Mẫu để dán vào `sources.md` ở P7:

```
## Phiên bản đã đối chiếu
- Ngày đối chiếu: 2026-11-20
- Kotlin: 2.4.21
- kotlinx.coroutines: 1.11.0
- Compose BOM: 2026.11.01  (runtime 1.13.0, ui 1.13.0, animation 1.13.0, material3 1.5.0)
- Compose Compiler: plugin org.jetbrains.kotlin.plugin.compose, đi kèm Kotlin 2.4.21 (strong skipping bật mặc định từ Kotlin 2.0.20)
- AndroidX Lifecycle: 2.11.1
- Commit AndroidX tham khảo cho chi tiết nội bộ: (điền ở P3)
- WCAG: 2.2 (W3C Recommendation 2024-12-12)
- Material 3: đối chiếu ngày 2026-11-20 (điền các token đã dùng ở P6)
- Android design guidance: đối chiếu ngày 2026-11-20 (điền ở P6)
```

## 3. Kiểm tra URL

Phương pháp: trích mọi URL xuất hiện trong `SOURCES.md`, `tracks/*.md`, master, style, i18n, template và `phases/*.md` → **189 URL duy nhất**. Mỗi URL được tải bằng HTTP GET, theo redirect, đọc status cuối và thẻ `<title>`.

Kết quả: **188 trả 200** (sau redirect), **1 trả 404**. Dù vậy, 200 chưa phải "đúng nội dung". Phát hiện thêm:

### 3.1 Phải thay (đưa URL thay thế vào `sources.js`, không dùng URL cũ)

| URL trong spec | Vấn đề | URL thay thế (đã tải, 200, kiểm tiêu đề) |
|---|---|---|
| `https://developer.android.com/develop/ui/compose/animation` | **404** ("Page Not Found") dù spec ghi đã kiểm 200 | `https://developer.android.com/develop/ui/compose/animation/introduction` (tiêu đề "Animations in Compose"). Dùng cho C0 |
| `https://kotlinlang.org/docs/flow.html` | Trả 200 nhưng chỉ là **trang chuyển hướng** (`meta refresh`, tiêu đề "You will be redirected shortly") | `https://kotlinlang.org/docs/coroutines-flow.html` (tiêu đề "Flows"). Dùng cho A7 |
| `https://kotlinlang.org/docs/cancellation-and-timeouts.html` | Trang chuyển hướng bằng `meta refresh` + JS, không có tiêu đề | `https://kotlinlang.org/docs/coroutines-cancellation.html` (tiêu đề "Cancellation and timeouts"). Dùng cho A5 |

Bài học: một URL có thể trả 200 nhưng chỉ là stub, và stub có thể biến mất. Site **luôn dùng URL đích cuối cùng**.

### 3.2 Redirect HTTP (đổi sang URL đích trong `sources.js`)

| URL trong spec | URL đích |
|---|---|
| `https://developer.android.com/develop/ui/compose/layouts/adaptive` | `.../layouts/adaptive/get-started-with-adaptive-apps` |
| `https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/lang` | `https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/lang` |
| `https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion` | `https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion` |
| `https://m3.material.io/styles/motion/overview` | `https://m3.material.io/styles/motion/overview/how-it-works` |
| `https://www.designcouncil.org.uk/our-resources/the-double-diamond/` | `https://www.designcouncil.org.uk/resources/the-double-diamond/` |
| `https://www.designcouncil.org.uk/our-resources/framework-for-innovation/` | `https://www.designcouncil.org.uk/resources/framework-for-innovation/` |

### 3.3 Material 3: status có ý nghĩa, nội dung chưa xác nhận

- `m3.material.io` là ứng dụng một trang (SPA). Đã thử một đường dẫn vô nghĩa (`/this/path/does-not-exist-xyz`) và một URL spec đã đánh dấu 404 (`/styles/shape/overview`): cả hai trả **404 thật**. Vậy status 200 ở các trang M3 còn lại **có phân biệt được** trang tồn tại.
- Tuy vậy `<title>` ban đầu của SPA chung chung, nên **chưa xác nhận nội dung**:
  - `.../styles/color/static/baseline` và `.../styles/color/dynamic/user-generated-source` cùng hiện tiêu đề "Dynamic color";
  - `.../foundations/accessible-design/overview` chỉ hiện "Material Design";
  - `.../foundations/designing/color-contrast` hiện "Accessibility designing".
- **Quy ước:** mọi URL `m3.material.io` ghi là "200, nội dung chưa xác nhận". P6 mở bằng trình duyệt thật, đọc nội dung và xác nhận trước khi dùng làm nguồn cho một khẳng định.

### 3.4 Đã khớp

- 71 bài NN/g: tiêu đề khớp chủ đề đã khai (ví dụ `measuring-perceived-usability` = "Beyond NPS: SUS, NASA-TLX, and the Single Ease Question", đủ để đối chiếu SUS ở D8). Mới đối chiếu tiêu đề; nội dung từng bài đọc ở P5 và P6.
- 18 trang WCAG Understanding và `TR/WCAG22`: tiêu đề khớp mã tiêu chí (ví dụ 2.5.8 = Target Size (Minimum), 2.5.5 = Target Size (Enhanced), 1.4.11 = Non-text Contrast).
- Các trang Android Developers, kotlinlang (trừ hai stub), How Composition Works, Grokking Android, GV, Design Council, Laws of UX: tiêu đề khớp.
- `designed-to-scale.vercel.app` và `protocol-explorer-alpha.vercel.app` còn truy cập được; chỉ liệt kê ở trang Nguồn với vai trò "cảm hứng UX".
- Các URL 404 đã liệt kê trong `tracks/D-ux.md` và `tracks/E-ui.md` **không** xuất hiện trong bộ URL đã kiểm; không dùng chúng.

## 4. Quyết định kiến trúc

### 4.1 Thứ tự thẻ `<script>`

Chỉ dùng `<script src defer>` cổ điển. Thuộc tính `defer` giữ đúng thứ tự trong tài liệu và chạy trước `DOMContentLoaded`, nên thứ tự dưới đây là xác định. Mỗi file bọc trong IIFE, bắt đầu bằng `window.ADE = window.ADE || {}`. Không ES module, không `fetch`.

```
index.html
1. js/core/i18n.js            // tạo ADE, ADE.t, ADE.addStrings, Intl, markup
2. js/core/registry.js        // ADE.registerTrack, nguồn, lộ trình, cầu nối, model registry
3. js/core/engine.js          // SimEngine
4. js/core/diagram.js         // helper SVG isometric, icon tự vẽ
5. js/core/ui.js              // panel, tab, badge, callout, mock-frame
6. js/core/controls.js        // thanh điều khiển, phím tắt
7. js/core/search.js
8. js/core/router.js
9. i18n/ui.vi.js, i18n/ui.en.js
10. shared/sources.js, shared/glossary.{vi,en}.js, shared/misconceptions.{vi,en}.js,
    shared/bridges.{vi,en}.js, shared/paths.js, shared/mock-app/*
11. <!-- TRACK: <id> --> khối riêng cho mỗi track, đúng thứ tự:
    tracks/<id>/manifest.js → content.vi.js → content.en.js → code.js → sources.js →
    glossary.*.js → misconceptions.*.js → models/*.js → views/*.js
12. app.js                    // bootstrap: ADE.boot() = validateAll() + router + render
```

`dev/report.html` nạp đúng chuỗi 1–11 rồi chạy kiểm tra thay cho `app.js`.

### 4.2 Namespace `window.ADE`

| Thành viên | Vai trò |
|---|---|
| `ADE.t(key, params)` | Tra chuỗi + thay tham số + plural |
| `ADE.addStrings(lang, obj, prefixGuard)` | Nạp chuỗi (xem 4.3) |
| `ADE.setLang(lang)`, `ADE.lang`, `ADE.langs` | Ngôn ngữ hiện tại và danh sách hỗ trợ (`['vi','en']`) |
| `ADE.renderMarkup(str)` | Chuyển `[[term:]]`, `[[src:]]`, `[[badge:]]`, backtick thành DOM |
| `ADE.registerTrack(manifest)` | Kiểm tra cấu trúc rồi lưu (xem 4.6) |
| `ADE.registerModel(id, factory)` | Đăng ký model mô phỏng; manifest chỉ trỏ tới id |
| `ADE.addSources(list)`, `ADE.addGlossary(...)`, `ADE.addMisconceptions(...)`, `ADE.addBridges(list)`, `ADE.addPaths(list)` | Kho dữ liệu dùng chung, mỗi file gọi một lần |
| `ADE.tracks`, `ADE.getTrack(id)`, `ADE.domains()` | Truy vấn từ registry; lõi **không** biết tên track |
| `ADE.validateAll()` | Kiểm tra chéo sau khi mọi script đã nạp (xem 4.6) |
| `ADE.engine`, `ADE.diagram`, `ADE.ui`, `ADE.controls`, `ADE.search`, `ADE.router` | Các mô-đun lõi |
| `ADE.store` | Bọc `localStorage` (try/catch) |
| `ADE.dev` | Cờ `?dev=1` |

### 4.3 Message key và lưu chuỗi

- **Chuỗi lưu phẳng theo khóa chấm** (`'track.runtime.b10.step3.explain': '...'`), không lồng object. Lý do: so sánh "cùng cây key" giữa vi và en chỉ là so hai tập khóa.
- Nạp bằng `ADE.addStrings(lang, obj)`:
  - **Từ chối khóa trùng** (ném lỗi, báo ở report);
  - **Từ chối khóa ngoài vùng cho phép**: file của track `<id>` chỉ được ghi vào `track.<id>.*`; `i18n/ui.*.js` chỉ ghi vào `app.*`, `job.*`, `phase.*`, `step.*`, `badge.*`, `a11y.*`, `domain.*`; `shared/*` chỉ ghi vào `shared.*`.
- Namespace:

| Vùng | Tiền tố | Nơi nạp |
|---|---|---|
| Giao diện chung | `app.` (ví dụ `app.play`, `app.next`) | `i18n/ui.<lang>.js` |
| Tên cố định dùng chung | `job.`, `phase.`, `step.`, `badge.`, `a11y.`, `domain.` | `i18n/ui.<lang>.js` |
| Nội dung track | `track.<id>.` (ví dụ `track.ux.d4.title`, `track.runtime.b10.step3.explain`) | `tracks/<id>/content.<lang>.js` và các file glossary/hiểu lầm của track |
| Dùng chung giữa track | `shared.` (`shared.glossary.*`, `shared.mis.*`, `shared.bridge.*`, `shared.path.*`, `shared.src.*`) | `shared/*` |

- **Id track bị cấm** (reserved): `app, track, job, phase, step, badge, a11y, domain, shared`. `registerTrack` từ chối.
- **Mục glossary và hiểu lầm của track** là khóa dưới `track.<id>.glossary.<termId>.{term,def}` và `track.<id>.mis.<n>.{wrong,right,example}`; `glossaryNs`/`misconceptionsNs` trong manifest chính là `<id>` hoặc một nhóm con.
- Thiếu khóa ở ngôn ngữ hiện tại → hiện bản `vi`, gắn class `.i18n-missing`; `console.warn` **chỉ khi** `?dev=1`.
- **Mọi chuỗi lưu ở dạng Unicode NFC.** Phép kiểm tra của report: `s === s.normalize('NFC')`. Lý do: dấu tổ hợp rời (NFD) hiển thị xấu hơn trong font monospace và làm hỏng so khớp tìm kiếm.
- Số dùng `Intl.NumberFormat(lang)`, plural dùng `Intl.PluralRules`; trong mã và công thức luôn dấu chấm.

### 4.4 Markup nội dung

Bốn dạng, không chèn HTML tùy ý:

| Cú pháp | Kết quả |
|---|---|
| `[[term:<id>]]` | Link glossary; khi trang ở `vi` bọc `lang="en"` |
| `[[src:<id>]]` | Icon trích nguồn, trỏ tới mục nguồn |
| `[[badge:<key>]]` | Nhãn phân loại (bảng 7.3 master) |
| `` `code` `` | Mã nội dòng, thêm `translate="no"` |

Renderer tự escape mọi ký tự còn lại. Mọi `<` và `&` trong chuỗi là văn bản thường.

### 4.5 Manifest

Theo master 6.4: `id, code, order, domain, accent, icon, titleKey, summaryKey, level, estMinutes, status, prerequisites, languages, chapters[{id,titleKey,sims,bridges}], presets[{id,model,titleKey}], logKinds, labels, glossaryNs, misconceptionsNs`.

- `accent`: một hex duy nhất, theo quy tắc ở mục 5.4 (chỉ non-text).
- `chapters[].sims` và `presets[].model` là **id model** (đăng ký bằng `ADE.registerModel`).
- `logKinds` do track khai; renderer sinh chip chú giải từ danh sách này.

### 4.6 Kiểm tra hai giai đoạn

Manifest được nạp **trước** content và model, nên `registerTrack` chỉ kiểm tra được cấu trúc:

1. **Khi gọi `registerTrack`** (cấu trúc): trường bắt buộc, kiểu dữ liệu, id trùng, id thuộc danh sách cấm, `domain` là chuỗi, `accent` là hex hợp lệ.
2. **`ADE.validateAll()`** chạy một lần ở `ADE.boot()` và ở `dev/report.html`, **sau khi mọi script đã nạp**: chapter có đủ khóa content, preset trỏ tới model tồn tại, cầu nối trỏ tới chương tồn tại, `prerequisites` trỏ tới track tồn tại, `sims` trỏ tới model tồn tại.

Lỗi gom vào `ADE.errors`, hiển thị ở `dev/report.html`, không làm hỏng giao diện chính.

### 4.7 Route và lưu trữ

- Route: `#/<lang>/` (trang chủ), `#/<lang>/<trackId>/<chapterId>[/<step>]`, `#/<lang>/live?preset=<id>&step=<n>`, `#/<lang>/misconceptions`, `#/<lang>/glossary`, `#/<lang>/sources`, `#/<lang>/about`, `#/<lang>/search?q=`. Thiếu `<lang>` → chuyển sang ngôn ngữ đã lưu, mặc định `vi`.
- `localStorage`: mọi khóa có **tiền tố `ade.`** vì các trang `file://` có thể dùng chung origin. Tập khóa: `ade.lang`, `ade.theme`, `ade.motion`, `ade.sans`, `ade.diagramOnly`, `ade.rail`, `ade.progress`. Mọi đọc/ghi bọc try/catch; giao diện phải chạy đúng khi storage không dùng được. Chỉ lưu tiến độ, ngôn ngữ và lựa chọn giao diện; không lưu dữ liệu đo cá nhân.

### 4.8 Bộ kiểm tra của `dev/report.html`

1. **Song ngữ:** khóa có ở `vi` mà thiếu ở `en` và ngược lại; chuỗi rỗng; chuỗi giống hệt giữa hai ngôn ngữ (loại trừ tên riêng, mã); **chuỗi không ở dạng NFC**.
2. **Registry:** lỗi manifest (giai đoạn 1 và 2 của mục 4.6); chapter/preset/cầu nối trỏ tới key hay model không tồn tại.
3. **Nguồn:** `[[src:id]]` không có trong registry; nguồn khai báo nhưng không dùng; nguồn thiếu ghi chú ở một ngôn ngữ; URL nằm trong danh sách "đã thay" (mục 3.1).
4. **Glossary:** `[[term:x]]` không có mục ở ngôn ngữ hiện tại.
5. **Model tính toán:** chạy các ví dụ kiểm chứng (`runChecks()`), báo PASS/FAIL.
6. **Ngoài report, gate ở P8:** tìm `trackId ===`/`case '<id>'` trong `js/core` và `app.js`; tìm `import`/`export`/`fetch(`/`type="module"`; tìm URL ngoài `file://`.

## 5. Design tokens: tính tương phản

**Công thức** (WCAG 2.2, Understanding 1.4.3): `L = 0.2126·R + 0.7152·G + 0.0722·B` với `c ≤ 0.03928 ? c/12.92 : ((c+0.055)/1.055)^2.4`; tỷ lệ `(L1 + 0.05)/(L2 + 0.05)` với `L1 ≥ L2`.
**Kiểm chứng:** đen/trắng = **21.000:1**; hai màu giống nhau = **1.000:1**. (Script chạy ra đúng.)

**Ngưỡng:**
- chữ thường: ≥ 4.5:1 (1.4.3, AA);
- thành phần không phải chữ và nét đồ họa có nghĩa: ≥ 3:1 (1.4.11, AA).

**Biên an toàn nội bộ:** ≥ **4.55:1** cho chữ và ≥ **3.10:1** cho non-text, để làm tròn không che mất vi phạm. Mọi tỷ lệ dưới đây in 3 chữ số thập phân.

Nền đối chiếu: `paper` = nền trang, `paper2` = nền panel, `paper3` = nền tô nhạt / dòng đang chọn. Chữ và token đều phải đạt trên cả ba.

### 5.1 Giá trị cuối cùng (đưa vào `styles.css` ở P1)

**Light**

| Token | Hex | | Token | Hex |
|---|---|---|---|---|
| `--ink` | `#0B4F45` | | `--tok-state` | `#925F00` |
| `--ink-2` | `#2F6E63` | | `--tok-signal` | `#B0287A` |
| `--ink-3` | `#4C716A` | | `--tok-runtime` | `#6236C9` |
| `--paper` | `#FBFCFB` | | `--tok-ui` | `#0B776D` |
| `--paper-2` | `#F1F6F4` | | `--tok-coroutine` | `#1D5FD1` |
| `--paper-3` | `#E3EEEA` | | `--tok-job` | `#1F793A` |
| `--line` (trang trí) | `#B9D3CB` | | `--tok-thread` | `#5B6878` |
| `--line-strong` (mới) | `#638D81` | | `--tok-flow` | `#587300` |
| `--brand` | `#0B4F45` | | `--tok-cancel` | `#AC4E0C` |
| `--focus` | `#C25E00` | | `--tok-error` | `#C42B32` |
| `--row-active` (mới) | `#E3EEEA` (= paper-3) | | `--tok-anim` | `#0B4F45` |

**Dark**

| Token | Hex | | Token | Hex |
|---|---|---|---|---|
| `--ink` | `#BFE3D6` | | `--tok-state` | `#F2B84B` |
| `--ink-2` | `#8FBFB1` | | `--tok-signal` | `#F472B6` |
| `--ink-3` | `#6C9C8F` | | `--tok-runtime` | `#A78BFA` |
| `--paper` | `#0A1512` | | `--tok-ui` | `#2DD4BF` |
| `--paper-2` | `#10201B` | | `--tok-coroutine` | `#60A5FA` |
| `--paper-3` | `#173029` | | `--tok-job` | `#4ADE80` |
| `--line` (trang trí) | `#2A4A41` | | `--tok-thread` | `#94A3B8` |
| `--line-strong` (mới) | `#4F8073` | | `--tok-flow` | `#BEF264` |
| `--brand` | `#5FD3A8` | | `--tok-cancel` | `#FB923C` |
| `--focus` | `#FFC24D` | | `--tok-error` | `#F87171` |
| `--row-active` (mới) | `#173029` (= paper-3) | | `--tok-anim` | `#E2E8F0` |

**Accent track** (một giá trị dùng cho cả hai theme; xem quy tắc 5.4):
`coroutines #2F83BE` · `runtime #946BC4` · `animation #B46D24` · `ux #C75976` · `ui #398D62`.

### 5.2 Cặp phải chỉnh (so với gợi ý trong `STYLE-REFERENCE.md` mục 5)

| Theme | Token | Gợi ý ban đầu | Giá trị cuối | Lý do (tỷ lệ gần ngưỡng nhất trước khi chỉnh) |
|---|---|---|---|---|
| light | `--ink-3` | `#5E8C83` | `#4C716A` | 3.676 trên paper, 3.178 trên paper-3: **không đạt** chữ |
| light | `--tok-state` | `#9A6400` | `#925F00` | 4.209 trên paper-3 (tô nhạt) |
| light | `--tok-ui` | `#0B7A70` | `#0B776D` | 4.394 trên paper-3 |
| light | `--tok-flow` | `#5E7A00` | `#587300` | 4.152 trên paper-3 |
| light | `--tok-cancel` | `#B4520C` | `#AC4E0C` | 4.264 trên paper-3 |
| light | `--tok-job` | `#1F7A3A` | `#1F793A` | 4.53 trên paper-3: đạt, chỉnh nhẹ để có biên an toàn 4.55 |
| dark | `--ink-3` | `#6A9A8D` | `#6C9C8F` | 4.440 trên paper-3 |

Tổng: **7 màu** được chỉnh (6 light, 1 dark), mỗi màu giữ nguyên hue, chỉ đổi độ sáng. **Thêm 2 token mới:** `--line-strong` (light và dark) và `--row-active`. Các màu còn lại giữ nguyên gợi ý.

### 5.3 Bảng tương phản đầy đủ (3 chữ số thập phân; cột = paper / paper-2 / paper-3)

**A. Chữ**

| Theme | Màu | Hex | paper | paper-2 | paper-3 |
|---|---|---|---|---|---|
| light | ink | `#0B4F45` | 9.204 | 8.667 | 7.971 |
| light | ink-2 | `#2F6E63` | 5.782 | 5.445 | 5.008 |
| light | ink-3 | `#4C716A` | 5.266 | 4.959 | 4.561 |
| dark | ink | `#BFE3D6` | 13.441 | 12.193 | 10.175 |
| dark | ink-2 | `#8FBFB1` | 9.084 | 8.241 | 6.877 |
| dark | ink-3 | `#6C9C8F` | 6.014 | 5.456 | 4.553 |

`--brand` làm chữ: light 9.204 / 8.667 / 7.971; dark `#5FD3A8` 10.071 / 9.136 / 7.624.

**B. Token ngữ nghĩa trên nền** (đạt ≥ 4.55, dùng được làm chữ và nét)

| Token | Light (paper / paper-2 / paper-3) | Dark (paper / paper-2 / paper-3) |
|---|---|---|
| state | 5.291 / 4.983 / 4.582 | 10.393 / 9.428 / 7.868 |
| signal | 5.952 / 5.605 / 5.155 | 7.024 / 6.371 / 5.317 |
| runtime | 7.064 / 6.653 / 6.118 | 6.835 / 6.201 / 5.175 |
| ui | 5.271 / 4.964 / 4.565 | 9.993 / 9.065 / 7.565 |
| coroutine | 5.657 / 5.327 / 4.899 | 7.317 / 6.637 / 5.539 |
| job | 5.298 / 4.989 / 4.588 | 10.675 / 9.684 / 8.081 |
| thread | 5.524 / 5.202 / 4.784 | 7.255 / 6.581 / 5.492 |
| flow | 5.280 / 4.972 / 4.573 | 14.239 / 12.917 / 10.779 |
| cancel | 5.305 / 4.996 / 4.594 | 8.219 / 7.456 / 6.222 |
| error | 5.461 / 5.143 / 4.730 | 6.725 / 6.100 / 5.091 |
| anim | 9.204 / 8.667 / 7.971 | 15.090 / 13.688 / 11.423 |

**C. Chip, tô nhạt (16% token trộn với paper)**

| Token | Light: token trên tint | Light: ink trên tint | Dark: token trên tint | Dark: ink trên tint |
|---|---|---|---|---|
| state | 4.257 | 7.404 | 7.603 | 9.832 |
| signal | 4.618 | 7.140 | 5.625 | 10.765 |
| runtime | 5.466 | 7.121 | 5.396 | 10.610 |
| ui | 4.228 | 7.383 | 7.266 | 9.773 |
| coroutine | 4.483 | 7.295 | 5.680 | 10.434 |
| job | 4.251 | 7.385 | 7.703 | 9.699 |
| thread | 4.448 | 7.411 | 5.611 | 10.396 |
| flow | 4.256 | 7.420 | 9.615 | 9.077 |
| cancel | 4.224 | 7.328 | 6.347 | 10.380 |
| error | 4.261 | 7.181 | 5.423 | 10.839 |
| anim | 7.007 | 7.007 | 9.954 | 8.867 |

→ **Quy tắc:** ở theme **light**, chữ màu token trên tint của chính nó có thể chỉ đạt ~4.2–4.6, **dưới biên an toàn**. Vì vậy chip và chú giải log **luôn dùng chữ `--ink` (≥ 7.0 trên mọi tint)**, còn màu token chỉ ở **icon, viền trái, đường nét** (non-text, ≥ 4.2 ≥ 3.1). Màu token không bao giờ là cách duy nhất phân biệt loại sự kiện (kèm icon và nhãn).

**D. Nút đảo màu:** chữ `--paper` trên nền `--brand`: light 9.204, dark 10.071 (đạt). Chữ `--paper` trên nền `--ink`: light 9.204, dark 13.441.

**E. Non-text**

| Theme | Màu | Hex | paper | paper-2 | paper-3 | Vai trò |
|---|---|---|---|---|---|---|
| light | line-strong | `#638D81` | 3.609 | 3.399 | 3.126 | Viền control, nét sơ đồ có nghĩa |
| light | focus | `#C25E00` | 4.171 | 3.928 | 3.613 | Focus ring |
| light | line | `#B9D3CB` | 1.542 | 1.452 | 1.335 | **Chỉ trang trí** |
| dark | line-strong | `#4F8073` | 4.135 | 3.751 | 3.130 | Như trên |
| dark | focus | `#FFC24D` | 11.583 | 10.507 | 8.769 | Focus ring |
| dark | line | `#2A4A41` | 1.908 | 1.731 | 1.445 | **Chỉ trang trí** |

`--line` (≈ 1.3–1.9:1) chỉ dùng cho đường kẻ trang trí giữa các vùng, lưới isometric mờ. **Biên của control** (nút, ô nhập, thẻ bấm được) **và nét sơ đồ có nghĩa** phải dùng `--line-strong`.

**F. Dòng đang chọn trong bảng log:** nền `--row-active` (đúng bằng paper-3 nên mọi cặp trong bảng A và B trên paper-3 áp dụng nguyên) **cộng** vạch trái 3px màu `--brand` và dấu ▶ (không chỉ dựa vào màu nền).

### 5.4 Quy tắc accent của track

- Accent là **non-text only**: vạch, viền thẻ, icon, chấm nhận diện. **Chữ trên thẻ track luôn là `--ink`**, không tô màu accent.
- Mỗi accent được chọn độ sáng để đạt ≥ 3.10:1 trên cả ba nền ở **cả hai theme** (số đo: coroutines light 3.460 / dark 3.427; runtime 3.428 / 3.460; animation 3.431 / 3.456; ux 3.455 / 3.433; ui 3.427 / 3.460, là giá trị nhỏ nhất trong ba nền).
- Một số accent cùng họ màu với token ngữ nghĩa (tím ~ runtime, xanh dương ~ coroutine, hồng ~ signal). **Vì thế accent không bao giờ xuất hiện bên trong canvas sơ đồ, bảng log hay chú giải loại sự kiện.** Chỉ xuất hiện ở catalog, nav, tiêu đề, thanh tiến độ.
- Mock UI (khung "Giao diện mẫu") được miễn token ngữ nghĩa (master 5.4c); khung có viền `--line-strong` và nhãn.

### 5.5 Nhận xét còn lại

- `--tok-anim` ở light **trùng hex với `--ink`** (`#0B4F45`), đúng theo `STYLE-REFERENCE`. Phân biệt bằng **nét** (current value dùng nét đặc và dấu tròn đầy; velocity dùng nét đứt) và nhãn, không bằng màu.
- Tỷ lệ chỉ đo chữ/nền phẳng. Chữ đè lên lưới isometric (`--grid-iso`, alpha ≤ .07) không đổi kết luận đáng kể; P1 vẫn kiểm bằng mắt.

## 6. Font và dấu tiếng Việt

Stack (từ `STYLE-REFERENCE` 4.1): `ui-monospace, "Cascadia Mono", "Cascadia Code", Consolas, "SF Mono", "Roboto Mono", "Noto Sans Mono", monospace`.

| Kiểm tra | Kết quả |
|---|---|
| Consolas (Windows): phủ glyph dạng dựng sẵn của toàn bộ chữ cái tiếng Việt, hoa và thường (đọc bảng `cmap` của `consola.ttf`) | **Đạt**: không thiếu glyph nào |
| Courier New (`cour.ttf`) | **Đạt**: không thiếu glyph nào |
| Cascadia Mono / Cascadia Code | **Chưa kiểm**: không cài trên máy này |
| Roboto Mono / Noto Sans Mono trên Android | **Chưa kiểm**: không có thiết bị |
| Chuỗi mẫu "TIẾNG VIỆT · ỨNG DỤNG · ĐỒNG THỜI · HỦY BỎ · CẬP NHẬT · NHẬT KÝ SỰ KIỆN" khi `text-transform: uppercase`, ở light và dark, `line-height ≥ 1.3`, xem dấu có bị cắt hoặc lệch | **Chưa kiểm**: cần trình duyệt và CSS; **làm ở P1** rồi ghi kết quả vào `docs/design-principles.md` |

Phép kiểm `cmap` chỉ bao phủ glyph dựng sẵn (NFC). Vì thế có quy tắc NFC ở mục 4.3.

## 7. Điều cần theo dõi ở phase sau

- **P1:** kiểm chuỗi hoa tiếng Việt trong trình duyệt; xác nhận `ui-monospace` không chọn font thiếu dấu.
- **P3:** chốt commit AndroidX cho SlotTable/group/`$changed`.
- **P6:** đọc nội dung các trang `m3.material.io` (mục 3.3) trước khi dùng làm nguồn; lấy giá trị token; xác nhận `material3-adaptive` stable.
- **P7:** dán đúng URL đích (mục 3.1 và 3.2) vào `shared/sources.js`; điền mục "Phiên bản đã đối chiếu".
