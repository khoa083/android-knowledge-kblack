# Hợp đồng lõi (P1): dành cho các phase track

> Đọc file này trước khi viết track. Lõi (`js/core`, `app.js`) **không** biết id track nào; track chỉ khai báo dữ liệu. Chi tiết quyết định ở `docs/research/global.md` mục 4.

## 1. Thứ tự file của một track (khối `<script>` trong `index.html` **và** `dev/report.html`)

```
tracks/<id>/manifest.js → content.vi.js → content.en.js → code.js → sources.js →
glossary.vi.js → glossary.en.js → misconceptions.vi.js → misconceptions.en.js → models/*.js → views/*.js
```
Mỗi khối có comment `<!-- track: <id> -->`. Thêm track = thêm khối này vào cả hai file HTML; không sửa lõi.

## 2. Chuỗi và khoá

- Nạp chuỗi bằng `ADE.addTrackStrings('<id>', 'vi'|'en', { 'track.<id>.…': '…' })`. Khoá phẳng; ngoài `track.<id>.*` bị từ chối; khoá trùng bị từ chối.
- Quy ước khoá của **chương** `c` (cơ sở `track.<id>.<c>`):
  - `.title` (= `titleKey` trong manifest), `.essence` (nhiều dòng `\n` → nhiều đoạn, bắt buộc),
  - `.goal.<gid>` (khớp `goals:[{id, step:n|'end'}]` trong manifest),
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

## 5. Route và lưu trữ

`#/<lang>/<track>/<chapter>/<pos>` · `#/<lang>/live?preset=<id>&step=<n>`. Id cấm dùng làm id track: `app track job phase step badge a11y domain shared live misconceptions glossary sources about search dev`. Bước đổi bằng `history.replaceState`. `localStorage` có tiền tố `ade.` (`lang, theme, motion, sans, diagramOnly, rail, progress, last`), luôn bọc try/catch.

## 6. Còn để lại ở P1 (xử lý sau)

- Track `hello` + khoá `domain.sandbox` trong `i18n/ui.*.js` là tạm: gỡ trước P8.
- Nguồn Android localization/app-languages/multilingual/compose-resources: nằm ở track D/E (`sources.js` của track), không ở `shared/sources.js`.
- `dev/report.html` và `index.html` có hai danh sách script riêng: giữ đồng bộ (gate ở P8).
