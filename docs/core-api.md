# Hợp đồng lõi (P1): dành cho các phase track

> Đọc file này trước khi viết track. Lõi (`js/core`, `app.js`) **không** biết id track nào; track chỉ khai báo dữ liệu. Chi tiết quyết định ở `docs/research/global.md` mục 4.

## 1. Thứ tự file của một track (khối `<script>` trong `index.html` **và** `dev/report.html`)

```
tracks/<id>/manifest.js → content.vi.js → content.en.js → code.js → sources.js →
glossary.vi.js → glossary.en.js → misconceptions.vi.js → misconceptions.en.js → models/*.js → views/*.js (views.js, labs.js, screens.js)
```
Mỗi khối có comment `<!-- track: <id> -->`. Thêm track = thêm khối này vào cả hai file HTML; không sửa lõi.

## 2. Chuỗi và khoá

- Nạp chuỗi bằng `ADE.addTrackStrings('<id>', 'vi'|'en', { 'track.<id>.…': '…' })`. Khoá phẳng; ngoài `track.<id>.*` bị từ chối; khoá trùng bị từ chối.
- Quy ước khoá của **chương** `c` (cơ sở `track.<id>.<c>`):
  - `.title` (= `titleKey` trong manifest), `.essence` (nhiều dòng `\n` → nhiều đoạn, bắt buộc),
  - `.goal.<gid>` (khớp `goals:[{id, step:n|'end'}]` trong manifest). `step` là vị trí 1-based trong sim **từng bước đầu tiên** của `sims` (bỏ qua lab kiểu `compute`): chỉ tab đó hiện danh sách goal và ghi tiến độ chương; các tab khác vẫn chạy nhưng không đánh dấu goal (2026-11-23). Đổi tab thì số bước trên URL bị bỏ, tab mới mở ở trang tổng quan.
  - `.sec.<s>.title`, `.sec.<s>.p.<n>`, `.sec.<s>.badge` (các key nhãn cách nhau bằng dấu cách), `.sec.<s>.code` (id đoạn mã từ `code.js`),
  - `.quiz.<q>.q|a|why`,
  - `.sim.<modelId>` (nhãn tab khi chương có nhiều sim).
- Thứ tự các mục lấy theo thứ tự khai báo trong file `content.vi.js`.

### 2.1 Khối nội dung cho chương dài (v2, thêm 2026-11-22)

Trong một mục `…sec.<s>`, ngoài `.p.<n>` và `.code`, có thể dùng danh sách khối `.b.<n>.<trường>`. Các khối hiện xen kẽ theo thứ tự khai báo (`p`, `code` và `b` hiện theo vị trí xuất hiện đầu tiên của chúng). Trường có mặt quyết định loại khối:

| Trường | Khối | Ghi chú |
|---|---|---|
| `h` | tiêu đề con (h3) | |
| `p` | đoạn văn | `\n` tách nhiều đoạn; có markup |
| `kt` (+ `lang`) | khối mã viết thẳng | mặc định `kotlin`; chú thích trong mã được dịch theo ngôn ngữ |
| `out` | output của chương trình | |
| `note` (+ `kind`) | callout | `kind` ∈ `mechanism pitfall android source try analogy` (mặc định `mechanism`) |
| `predict` + `ans` | câu "Đoán trước" có đáp án ẩn | đặt TRƯỚC phần lộ đáp án (sim, output) |
| `ask` + `ans` | câu "Tự trả lời" (nhớ lại, tự giải thích) | |
| `bug` + `cause` + `fix` (+ `fixkt`) | thẻ bug: triệu chứng hiện, nguyên nhân và cách sửa ẩn | |
| `ex` (+ `exkt`, `hint`) + `sol` (+ `solkt`) | bài tập có gợi ý và lời giải ẩn | |

Manifest: `chapter.simAfter = '<id mục>'` đặt sim sau mục đó (mặc định ngay sau "bản chất"). `registry.validateAll` báo lỗi khi `simAfter` trỏ sai, `kind` lạ, hoặc khối hỏi–đáp thiếu trường. Cách dùng các khối theo nhịp sư phạm: `docs/chapter-template-v2.md`.
- Plural: `key.one` / `key.other` (en), `key.other` hoặc khoá thường (vi); gọi `ADE.t(key, {n})`.
- Markup: `[[term:id]]`, `[[src:id]]`, `[[badge:key]]`, `` `code` ``. Không `**đậm**`. Mọi chuỗi ở dạng NFC.
- Glossary: `ADE.addGlossary(lang, '<id>', { termId: {term, def, chapter:'<track>/<chapter>'} })`. `term` là thuật ngữ gốc tiếng Anh (cả hai ngôn ngữ). Id thuật ngữ là **toàn cục**.
- Hiểu lầm: `ADE.addMisconceptions(lang, '<id>', { id: {wrong, right, example?, chapter?} })`.
- Nguồn: `ADE.addSources([{id, title, url, org, tracks:['<id>'], label?, lang:'en', supports:{vi,en}}])`; dùng URL đích cuối (xem `global.md` mục 3). Mục phiên bản riêng của track: `ADE.versions.items.push({name, value, note?:{vi,en}})`.
- Loại sự kiện mới: `ADE.defineKind(kind, {tok, icon})`; nhãn `app.kind.<kind>` (hoặc ghi đè `track.<id>.kind.<kind>`).

## 3. Model

`ADE.registerModel(id, def)`. Model **thuần**, không DOM, không câu chữ (chỉ message key).

**Rời rạc** (`kind:'discrete'`):
```js
{ init(params)->state, act(state, action, payload)->state, steps(state)->Step[],
  titleKey, overviewKey, wrapupKey, codeId, simplificationKeys:[], controlsHintKey,
  controls:[{id, type:'toggle'|'select'|'button', labelKey, get(state), action, options?, payload?, icon?}],
  selfChecks:[{name, run()->bool}] }
Step = { id, type:'scenario|mechanism|experiment|pitfall|android', titleKey, explainKey, params,
  activeNodes:[nodeId], movingSignals:[{edge, tok}], stateBefore/After:[{labelKey, value|valueKey}], affected:[nodeId],
  skipped:[{whatKey, whyKey}], changes:[{op:'add|set|remove|skip', textKey, params}],
  callouts:[{kind:'mechanism|pitfall|android|source|try', textKey, params}], metrics:{id:value},
  codeHighlight:{snippet, lines:[n]}, typing:{node, code}, simplificationKeys:[],
  logEvents:[{t, kind, subject, to?, scope?, detailKey, params}] }
```
Session: `ADE.engine.create(modelId)` → `pos` (0 tổng quan, 1..N bước, N+1 tổng kết), `goto/next/prev/reset/act/play/pause/replayStep/setSpeed/eventsUpTo/metricsAt`. `act` tính lại `steps` từ state mới, giữ `pos` (kẹp vào N+1).

**Liên tục** (`kind:'continuous'`): `init, advance(state, dtMs), sample(state)->{t, values, done}, act`. Session có `stepFrame`, `restart`, `setFrameMs`, `samples`. (Chưa có view dựng sẵn: track C viết view riêng, xem mục 4.)

**Tính toán** (`kind:'compute'`): `compute(inputs)->{outputs, assumptionKeys, sourceIds}`, `checks:[{name, inputs, expect(result)->bool}]` (ví dụ kiểm chứng). `runChecks()` chạy tất cả.

`ADE.registerCheck(id, fn)` đăng ký kiểm chứng tuỳ ý. `dev/report.html` chạy chúng và kiểm mọi khoá mà model phát ra có đủ ở hai ngôn ngữ.

## 4. View

`ADE.registerView(modelId, cfg)`:
```js
{ titleKey, descKey,                                   // <title> và <desc> của SVG
  nodes:[{id, x, y, w?, d?, h?, icon, tok, labelKey}], // x,y: toạ độ lưới isometric; icon: tên trong ADE.diagram.ICONS; tok: tên token ngữ nghĩa
  edges:[{id, from, to, labelKey?}],
  metrics:[{id, labelKey}],                            // dải chỉ số điền dần ('?' tới khi step.metrics có giá trị)
  subjectKey?, scopeKey?,                              // tên cột "Thành phần" và cột phụ (scope) của bảng log
  mount?(container, {trackId, modelId, def}) }         // chỉ cho model compute hoặc view tự vẽ: trả {destroy, refresh?}
```
Lõi tự vẽ sơ đồ isometric, zoom vào `activeNodes`, token chạy dọc `movingSignals`, timeline, bảng log, panel và điều khiển.

### 4.1 Dạng bố cục (`layout`) — thêm 2026-11-21

Mỗi view chọn dạng hình hợp với bản chất khái niệm; **đừng dùng một cảnh chung cho mọi model**.

| `layout` | Dùng khi | Dữ liệu |
|---|---|---|
| `'iso'` (mặc định) | bản đồ kiến trúc nhiều thành phần (A0/B0 kiểu "map") | `nodes[].x,y` là toạ độ lưới isometric |
| `'tree'` | quan hệ cha–con (cây Job, composition, lan lỗi) | cha suy từ `edges` (from = cha), hoặc khai báo `node.parent` (khi đó mọi node dùng `parent`; `null` = gốc riêng) |
| `'pipeline'` | dòng dữ liệu trái → phải, các giai đoạn | hạng = đường dài nhất theo `edges` (cạnh quay lui vẽ vòng phía dưới); ghi đè bằng `node.col`, `node.row` |
| `'cycle'` | vòng lặp (bấm → state → render, quy trình lặp) | node xếp trên vòng theo thứ tự khai báo |
| `'lanes'` | ai chiếm tài nguyên lúc nào; thứ tự theo thời gian | `lanes(events, step, opts) → {rows:[{id, labelKey, group?}], bars:[{row, from, to, kind:'run'\|'block'\|'wait'\|'ready', label?, cur?, ghost?}], marks:[{row, t, label?, cur?}], tMax, now, axisKey?}`; `opts = {pos, steps, prev}`; `events` = `S.eventsUpTo()`. `barKeys` đổi nhãn chú giải (`run/block/wait/ready/mark`) |

Lõi làm chung cho mọi dạng:
- **Dòng "Bạn đang xem"** phía trên hình: `captionKey` (nên có: nói hình biểu diễn gì và nên thử gì), nếu thiếu thì dùng `descKey`.
- **Họ trạng thái**: đoạn cuối của khoá trong `step.nodeStates` → `run, wait, block, cancel, fail, done, idle` (bảng `FAM_WORDS` trong `diagram.js`; ghi đè bằng `view.stateFamilies:{đoạn: họ}`). Mỗi họ có glyph + kiểu viền riêng (không chỉ màu). Chú giải hình dạng tự sinh từ các họ có trong mô phỏng; nhãn chung `app.fam.<họ>`, track đổi nhãn bằng `view.famKeys:{họ: key}` (ví dụ coroutines: "suspend (không giữ luồng)").
- **"Điều vừa đổi"**: node có `nodeStates` khác bước trước được viền nhấn + nhịp một lần; chú thích trên hình ghi tiêu đề bước và `nhãn: trước → sau`.
- `movingSignals[].label` hiện số/giá trị trên token. Zoom camera: `iso` luôn; dạng phẳng chỉ khi > 6 node (hoặc `view.zoom: true`). Mọi chuyển động tắt khi reduced-motion hoặc "Chỉ sơ đồ".


Icon mới: thêm vào `ADE.diagram.ICONS` (nét 24×24, `currentColor`). Khung điện thoại mẫu: `ADE.ui.mockFrame(node)`. Đoạn mã: `ADE.addCode(trackId, id, {lang, illustrative?, lines:[string | {vi,en}]})`.

**Tô màu cú pháp (thêm 2026-11-23):** `ADE.ui.codeBlock` tự tô màu khi `lang` là `kotlin`, `kt` hoặc `kts` (mặc định `kotlin`); ngôn ngữ khác (ví dụ khối "Kết quả") để chữ thuần. Lõi là `ADE.syntax.tokenize(lines, lang)`, trả về `[[{c, t}]]` (mỗi dòng một mảng token; `c` thuộc `kw str esc num com ann type fn` hoặc `null`). Tokenizer dùng regex, giữ trạng thái qua dòng cho `/* … */` và raw string `"""`, có cache theo nội dung. Nó chỉ bọc `<span class="t-…">` quanh chữ gốc nên `textContent` không đổi. `dev/tools/syntax-check.js` (chạy bằng `cdp.js --eval`) tokenize mọi snippet và mọi khối `kt/exkt/fixkt/solkt` ở cả vi và en, rồi báo dòng nào ghép lại khác chữ gốc. Đây là phép tô màu theo heuristic, không phải parser Kotlin: ví dụ `Channel<Int>()` được tô như lời gọi hàm.

### 4.2 Hình trực quan theo bước: màn hình mẫu, bảng, ma trận (thêm 2026-11-23)

`ADE.registerScreen(modelId, fn)` (đặt trong `tracks/<id>/views/screens.js`, nạp sau `views.js`). `fn(container, ctx)` vẽ giao diện mẫu của bước hiện tại; `ctx = {step, pos, N, state, steps, reduced, viewState, redraw}` (`step` là `null` ở trang tổng quan và trang tổng kết). Sim có màn hình thì vùng sơ đồ có thêm tab "Màn hình", mở mặc định ở lần đầu; sơ đồ node và Timeline vẫn còn ở hai tab bên cạnh. Lỗi trong `fn` được bắt và ghi vào `ADE.err`, không làm hỏng sim.

Thành phần dùng chung trong `styles.css`: khung `ADE.ui.mockFrame`; lớp `mk-*` (bên trong `.mf-screen`, luôn nền sáng như ứng dụng mẫu: `mk-grid`, `mk-slot` + `free-pop`/`full-dim`/`tap`, `mk-card`, `mk-unseen`, `mk-row`, `mk-note`, `mk-snack` + `mk-timer`, `mk-chat-h`, `mk-bubble`, `mk-input`, `mk-btn`, `mk-dot` cho chấm số thứ tự mắt dừng); lớp `scr-*` (bên ngoài điện thoại: `scr-tools`, `scr-cap`, `scr-out`, `scr-mem`, `scr-attn` làm mờ và bỏ màu màn hình). Hiệu ứng (chấm hiện dần, vòng chạm, thanh đếm ngược) đặt trạng thái cuối là trạng thái mặc định nên khi giảm chuyển động vẫn đọc được.

**Hình trực quan cho mọi track (cập nhật 2026-11-23, quyết định của người dùng):** với mọi chủ đề trừ UI/UX (đang tạm dừng), chọn kiểu hình dễ học nhất mà không cần hỏi trước. `ADE.registerScreen(modelId, fn, opts)` nhận thêm `opts = { labelKey, icon }` để đặt nhãn và icon cho tab (mặc định "Màn hình" và icon điện thoại). CSS dùng chung `.vz` (khung), `.vz-cap`, `.vz-scroll`, `.vz-table` (ô `.c` căn giữa, `.hl` viền tập trung, `.bad` gạch chéo đỏ, `.ok`, `.dim`), `.vz-chip`, `.vz-box` (lồng nhau được), `.vz-legend`. Sơ đồ node vẫn ở tab bên cạnh. Ví dụ: `tracks/kotlin/views/visuals.js` (bảng bucket K4, bảng từng phần tử K9, ma trận gán K10, hộp receiver K12, bảng tra K0). Sim đầu tiên dùng màn hình mẫu: `ux.glance` (D1).

### 4.3 Trạng thái track `soon` (thêm 2026-11-23)

`status` của manifest thuộc `stable | draft | soon`. `ADE.trackOpen(t)` trả `false` cho track `soon`. Giao diện của track đóng: vẫn có thẻ trên trang chủ, chip trên thanh track và mục trong danh mục (nhãn "Sắp ra mắt / Coming soon", chip viền chấm), nhưng trang track chỉ có khung "Sắp ra mắt" (`data-fk="soon"`); đường dẫn chương chuyển sang trang track; không có cột chương, thanh tiến độ, chương trong danh mục, preset trong Live Explorer, hay chương/preset trong tìm kiếm. `resolveRef` và `allPresets` KHÔNG lọc, để `dev/report.html` vẫn kiểm đủ nội dung của track đóng. Thuật ngữ và hiểu lầm của track đóng vẫn hiện ở trang chung. Track-check chỉ chạy cho track đang mở. Đang dùng cho UX và UI (người dùng tạm dừng ngày 2026-11-23).

### 4.4 Đồ thị kiểu graph view (thêm 2026-11-24)

`js/core/graph.js` cung cấp `ADE.graph.create(opts)` và trả về `{ el, destroy }`. App gắn nó vào `cur.mounts` để hủy khi đổi trang.

**`opts`:**
- `data()`: trả `{ nodes, edges }`.
  - **Node:** `{ id, kind: 'hub' | 'leaf' | 'term', label, title, href, color, short }`.
  - **Cạnh:** `{ a, b, kind: 'member' | 'bridge' | 'path' | 'term', label }`.
- `height`: chiều cao khung đồ thị.
- `labels: 'all'`: luôn hiện nhãn mọi node.
- `legendKinds`: các loại hiện trong chú giải.
- `toggles`: `[{ id, labelKey, get, set }]`. Đổi toggle thì dựng lại dữ liệu và giữ vị trí của node cũ.

**Tương tác:**
- Mô phỏng lực, không dùng thư viện; vị trí ban đầu tất định.
- Kéo node để sắp lại; kéo nền để di chuyển.
- Phóng to bằng Ctrl/⌘ + cuộn hoặc nút + −. Cuộn thường vẫn cuộn trang.
- Rê chuột hay focus vào node thì làm nổi các node lân cận và ghi tên chúng vào dòng `aria-live`.
- Chỉ hub vào được bằng Tab. Mọi chương vẫn có trong danh sách văn bản bên dưới.
- Giảm chuyển động: tính xong bố cục ngay, không chạy hoạt ảnh.
- Dừng mô phỏng khi tab bị ẩn.

**Lõi không biết id track nào.** `app.js` dựng dữ liệu từ registry:
- **trang chủ:** mọi track, các chương có cầu nối hay nằm trong lộ trình học; có toggle "Hiện mọi chương" và "Hiện lộ trình học";
- **trang track:** chương của track và các chương nối cầu với nó; chỉ hiện khi track có cầu nối;
- **glossary:** thuật ngữ → chương định nghĩa → track, dựng khi mở mục `<details>`.

Chương của track `soon` không hiện riêng; tham chiếu tới nó nối vào hub của track.

## 5. Route và lưu trữ

`#/<lang>/<track>/<chapter>/<pos>` · `#/<lang>/live?preset=<id>&step=<n>`. Id cấm dùng làm id track: `app track job phase step badge a11y domain shared live misconceptions glossary sources about search dev`. Bước đổi bằng `history.replaceState`. `localStorage` có tiền tố `ade.` (`lang, theme, motion, sans, diagramOnly, rail, progress, last`), luôn bọc try/catch.

## 6. Còn để lại ở P1 (xử lý sau)

- Track `hello` + khoá `domain.sandbox` trong `i18n/ui.*.js` là tạm: gỡ trước P8.
- Nguồn Android localization/app-languages/multilingual/compose-resources: nằm ở track D/E (`sources.js` của track), không ở `shared/sources.js`.
- `dev/report.html` và `index.html` có hai danh sách script riêng: giữ đồng bộ (gate ở P8).
