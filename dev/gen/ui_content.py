# Sinh tracks/ui/content.vi.js và content.en.js từ MỘT nguồn. Chạy: python dev/gen/ui_content.py
import json, os, unicodedata
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = 'track.ui.'
E = []
def a(k, vi, en): E.append((P + k, vi, en))
def m(model, k, vi, en): a('m.' + model + '.' + k, vi, en)
def lab(k, vi, en): a('lab.' + k, vi, en)
def common(model, title, overview, wrapup, simp, hint, dt, dd):
    for k, v in (('title', title), ('overview', overview), ('wrapup', wrapup), ('simp.1', simp), ('ctl.hint', hint), ('diagramTitle', dt), ('diagramDesc', dd)): m(model, k, *v)

a('title', 'Giao diện Android: từ nguyên lý đến design system', 'Android UI: From Principles to Design Systems')
a('summary', 'Nguyên lý thị giác, chữ, màu, bố cục, component, pattern, design token, chuyển động và accessibility — từ ý tưởng tới `MaterialTheme` trong Compose.', 'Visual principles, type, color, layout, components, patterns, design tokens, motion and accessibility — from idea to `MaterialTheme` in Compose.')
for k, vi, en in [('crap', 'UI · sửa màn hình bằng CRAP', 'UI · fixing a screen with CRAP'), ('contrast', 'UI · kiểm tra tương phản', 'UI · contrast checker'), ('responsive', 'UI · bố cục thích ứng', 'UI · responsive lab'),
                  ('fitts', 'UI · Fitts và vùng chạm', 'UI · Fitts and touch targets'), ('tokens', 'UI · token → MaterialTheme', 'UI · tokens → MaterialTheme'), ('a11y', 'UI · kiểm tra accessibility', 'UI · accessibility audit')]:
    a('preset.' + k, vi, en)
for k, vi, en in [('col.subject', 'Đối tượng', 'Actor'), ('c.right', 'Lựa chọn của bạn khớp', 'Your choice matches'), ('c.wrong', 'Lựa chọn của bạn chưa khớp', 'Your choice does not match'), ('c.why', 'Đánh đổi', 'Trade-offs'),
                  ('c.yours', 'Bạn chọn', 'You chose'), ('c.expected', 'Gợi ý tham khảo', 'Reference suggestion'), ('n.screen', 'Màn hình (Hẹn Khám)', 'Screen (ClinicBook)'), ('n.user', 'Người dùng', 'User'), ('n.design', 'Thiết kế', 'Design')]:
    a(k, vi, en)

# ---------- E0 layers ----------
M = 'layers'
common(M, ('Năm lớp của giao diện', 'Five layers of a UI'), ('Chọn một lớp: token, component, pattern, màn hình, luồng. Xem ví dụ trong Hẹn Khám và đoạn Compose tương ứng.', 'Pick a layer: token, component, pattern, screen, flow. See the ClinicBook example and the matching Compose snippet.'),
       ('Token → component → pattern → màn hình → luồng. Material 3 là design system; Compose Material 3 là một cách triển khai nó.', 'Token → component → pattern → screen → flow. Material 3 is a design system; Compose Material 3 is one implementation of it.'),
       ('Các lớp chồng lên nhau, ranh giới giữa chúng không cứng.', 'The layers overlap; their boundaries are not rigid.'), ('Chọn lớp.', 'Pick a layer.'), ('Năm lớp', 'Five layers'), ('Từ token tới luồng.', 'From token to flow.'))
m(M, 'ctl.layer', 'Lớp', 'Layer')
for l, tv, te, wv, we, xv, xe, cv, ce in [
 ('token', 'Token', 'Token', 'Giá trị có tên theo vai trò: màu, chữ, hình khối, khoảng cách, chuyển động.', 'Role-named values: color, type, shape, spacing, motion.', 'Hẹn Khám: `primary` là màu của nút "Đặt lịch".', 'ClinicBook: `primary` is the colour of the "Book" button.', '`MaterialTheme.colorScheme.primary`', '`MaterialTheme.colorScheme.primary`'),
 ('component', 'Component', 'Component', 'Khối dựng lại được, có trạng thái và hành vi.', 'A reusable building block with states and behaviour.', 'Nút "Đặt lịch", ô số điện thoại.', 'The "Book" button, the phone field.', '`Button(onClick = …) { Text("…") }`', '`Button(onClick = …) { Text("…") }`'),
 ('pattern', 'Pattern', 'Pattern', 'Lời giải đã kiểm chứng cho một bối cảnh, ghép từ nhiều component.', 'A proven solution for a context, built from several components.', 'Form đặt lịch nhiều bước, trạng thái rỗng có nút hành động.', 'A multi-step booking form, an empty state with an action.', 'Tổ hợp `Scaffold`, `TopAppBar`, `LazyColumn`…', 'A combination of `Scaffold`, `TopAppBar`, `LazyColumn`…'),
 ('screen', 'Màn hình', 'Screen', 'Một màn cụ thể ghép các pattern cho một tác vụ.', 'A concrete screen combining patterns for a task.', 'Màn "Chọn giờ".', 'The "Choose a time" screen.', '`@Composable fun ChooseTimeScreen(…)`', '`@Composable fun ChooseTimeScreen(…)`'),
 ('flow', 'Luồng', 'Flow', 'Chuỗi màn hình đưa người dùng tới mục tiêu.', 'A sequence of screens that takes users to a goal.', 'Trang chủ → Chọn dịch vụ → Chọn giờ → Xác nhận.', 'Home → Choose a service → Choose a time → Confirm.', 'Điều hướng giữa các màn (Navigation).', 'Navigation between screens.')]:
    m(M, 'ctl.layer.' + l, tv, te); m(M, 'l.' + l + '.title', tv, te); m(M, 'l.' + l + '.what', wv, we); m(M, 'l.' + l + '.example', 'Ví dụ: ' + xv, 'Example: ' + xe); m(M, 'l.' + l + '.compose', 'Compose: ' + cv, 'Compose: ' + ce)
m(M, 's.example.title', 'Ví dụ trong Hẹn Khám', 'Example in ClinicBook'); m(M, 's.compose.title', 'Trong Compose', 'In Compose'); m(M, 'ev.example', 'ví dụ', 'example'); m(M, 'ev.compose', 'mã', 'code')
m(M, 'co.source', 'Compose Material 3 triển khai Material 3 qua `MaterialTheme`. [[src:and-m3-compose]] [[badge:ds-guideline]]', 'Compose Material 3 implements Material 3 through `MaterialTheme`. [[src:and-m3-compose]] [[badge:ds-guideline]]')

# ---------- E7 patterns ----------
M = 'patterns'
common(M, ('Chọn pattern theo bối cảnh', 'Choosing a pattern by context'), ('Tám tình huống của Hẹn Khám. Chọn pattern rồi xem khi nào dùng, khi nào không.', 'Eight ClinicBook situations. Pick a pattern, then see when to use it and when not.'),
       ('Pattern là lời giải đã kiểm chứng cho một bối cảnh; không có pattern "luôn đúng".', 'A pattern is a proven solution for one context; no pattern is "always right".'),
       ('Gợi ý tham khảo dựa trên bối cảnh nêu trong tình huống; bối cảnh khác có thể đổi lựa chọn.', 'The reference suggestion rests on the stated context; another context can change the choice.'), ('Chọn tình huống và pattern.', 'Pick a situation and a pattern.'),
       ('Tình huống và pattern', 'Situation and pattern'), ('Màn hình, người dùng và quyết định.', 'Screen, user and decision.'))
m(M, 'ctl.item', 'Tình huống', 'Situation'); m(M, 'ctl.guess', 'Pattern', 'Pattern')
for p, tv, te, sv, se, wv, we in [
 ('p1', 'Ba đích chính trên điện thoại', 'Three main destinations on a phone', 'Trang chủ, Lịch của tôi, Cài đặt; dùng thường xuyên.', 'Home, My appointments, Settings; used often.', 'Navigation bar hiển thị cho đích chính, ít đích, trên màn compact.', 'A visible navigation bar for a few main destinations on compact screens.'),
 ('p2', 'Hai danh sách cùng cấp', 'Two sibling lists', '"Sắp tới" và "Đã qua" trong Lịch của tôi.', '"Upcoming" and "Past" in My appointments.', 'Tab cho nội dung cùng cấp trong một màn.', 'Tabs for sibling content within one screen.'),
 ('p3', 'Đặt lịch qua nhiều bước phụ thuộc', 'Booking through dependent steps', 'Chọn dịch vụ rồi giờ rồi xác nhận; bước sau cần bước trước.', 'Service, then time, then confirm; each step needs the previous one.', 'Form nhiều bước (stepper) khi bước sau phụ thuộc bước trước.', 'A multi-step form (stepper) when later steps depend on earlier ones.'),
 ('p4', 'Sửa hồ sơ ngắn', 'Editing a short profile', 'Ba ô: tên, số điện thoại, email.', 'Three fields: name, phone, email.', 'Form một trang khi ít ô và không phụ thuộc nhau.', 'A single-page form when there are few independent fields.'),
 ('p5', 'Danh sách giờ trống đang tải', 'Loading the slot list', 'Thời gian tải khoảng 2–3 giây, bố cục đã biết.', 'Loading takes about 2–3 seconds; the layout is known.', 'Skeleton giữ bố cục quen thuộc trong lúc tải.', 'A skeleton keeps the familiar layout while loading.'),
 ('p6', 'Tải lên giấy tờ khám', 'Uploading medical documents', 'Tải tệp lớn, có thể hơn 10 giây.', 'A large file upload that may take over 10 seconds.', 'Thanh tiến trình có phần trăm và cách hủy cho việc dài.', 'A progress bar with percentage and a way to cancel for long tasks.'),
 ('p7', 'Chưa có lịch hẹn nào', 'No appointments yet', 'Người dùng mới mở Lịch của tôi.', 'A new user opens My appointments.', 'Trạng thái rỗng có lời giải thích và nút hành động.', 'An empty state with an explanation and an action button.'),
 ('p8', 'Hướng dẫn tính năng nhắc lịch', 'Explaining reminders', 'Cần giới thiệu tính năng cho người dùng.', 'Users need to learn about the feature.', 'Gợi ý theo ngữ cảnh đúng lúc dùng, thay vì tour dài lúc mở app.', 'A contextual tip at the moment of use, instead of a long tour at launch.')]:
    m(M, 'ctl.item.' + p, tv, te); m(M, 'i.' + p + '.title', tv, te); m(M, 'i.' + p + '.situation', sv, se); m(M, 'i.' + p + '.why', wv, we)
for o, nv, ne, wv, we, xv, xe in [
 ('bottomNav', 'Navigation bar', 'Navigation bar', 'Dùng khi có 3–5 đích chính trên màn compact.', 'Use with 3–5 main destinations on compact screens.', 'Không hợp khi có nhiều đích hoặc trên màn rộng (dùng rail).', 'Not for many destinations or wide screens (use a rail).'),
 ('tabs', 'Tab', 'Tabs', 'Dùng cho nội dung cùng cấp trong một màn.', 'Use for sibling content within a screen.', 'Không dùng tab làm điều hướng chính giữa các phần khác nhau.', 'Do not use tabs as primary navigation between unrelated areas.'),
 ('drawer', 'Navigation drawer / menu ẩn', 'Navigation drawer / hidden menu', 'Dùng cho nhiều đích ít dùng hoặc màn lớn.', 'Use for many rarely used destinations or large screens.', 'Ẩn đích chính làm người dùng ít khám phá.', 'Hiding main destinations reduces discovery.'),
 ('singlePage', 'Form một trang', 'Single-page form', 'Dùng khi ít ô và độc lập.', 'Use for few independent fields.', 'Không hợp khi bước sau phụ thuộc bước trước.', 'Not when later steps depend on earlier ones.'),
 ('stepper', 'Form nhiều bước', 'Multi-step form', 'Dùng khi các bước phụ thuộc nhau.', 'Use when steps depend on each other.', 'Thừa cho form ngắn; cần cho biết đang ở bước nào.', 'Overkill for short forms; must show the current step.'),
 ('skeleton', 'Skeleton', 'Skeleton', 'Dùng khi tải vài giây và biết trước bố cục.', 'Use for a few seconds of loading with a known layout.', 'Không hợp cho việc rất ngắn hoặc rất dài.', 'Not for very short or very long waits.'),
 ('spinner', 'Spinner', 'Spinner', 'Dùng cho chờ ngắn, không biết tiến độ.', 'Use for short waits with unknown progress.', 'Chờ dài thì spinner không cho biết còn bao lâu.', 'For long waits a spinner does not say how long is left.'),
 ('progressBar', 'Thanh tiến trình', 'Progress bar', 'Dùng cho việc dài, đo được tiến độ.', 'Use for long tasks with measurable progress.', 'Thừa cho việc dưới một giây.', 'Overkill for sub-second tasks.'),
 ('emptyCta', 'Trạng thái rỗng có hành động', 'Empty state with an action', 'Dùng khi chưa có dữ liệu và có bước tiếp theo rõ.', 'Use when there is no data yet and a clear next step.', 'Không chỉ ghi "Không có dữ liệu".', 'Do not just say "No data".'),
 ('contextual', 'Gợi ý theo ngữ cảnh', 'Contextual tip', 'Dùng đúng lúc người dùng cần tính năng.', 'Use when users actually need the feature.', 'Tour dài lúc mở app thường bị bỏ qua.', 'Long launch tours are often skipped.')]:
    m(M, 'ctl.guess.' + o, nv, ne); m(M, 'opt.' + o + '.when', wv, we); m(M, 'opt.' + o + '.not', 'Khi không nên: ' + xv, 'When not to: ' + xe)
m(M, 'ev.tradeoff', 'đánh đổi', 'trade-off')

# ---------- E7 form ----------
M = 'form'
common(M, ('Form clinic', 'Form clinic'), ('Form số điện thoại của Hẹn Khám. Bật lần lượt: label thật, validate inline, thông báo lỗi cụ thể.', 'ClinicBook\'s phone form. Turn on, one by one: a real label, inline validation, a specific error message.'),
       ('Label thật, phản hồi sớm và lỗi chỉ ra cách sửa giảm lỗi và bối rối.', 'A real label, early feedback and errors that show the fix reduce mistakes and confusion.'),
       ('Đếm "vấn đề" là đếm minh họa các nguyên tắc chưa áp dụng.', 'The "issues" count is an illustrative count of principles not yet applied.'), ('Bật/tắt từng nguyên tắc.', 'Toggle each principle.'), ('Form', 'Form'), ('Màn hình, người dùng và thiết kế.', 'Screen, user and design.'))
m(M, 'ctl.label', 'Label thật', 'Real label'); m(M, 'ctl.inline', 'Validate inline', 'Inline validation'); m(M, 'ctl.specific', 'Lỗi cụ thể', 'Specific error')
m(M, 's.start.title', 'Ô số điện thoại', 'The phone field'); m(M, 's.start.explain', 'Lan cần nhập số điện thoại để đặt lịch.', 'Lan needs to enter a phone number to book.'); m(M, 'ev.start', 'mở form', 'open form')
m(M, 's.label.title', 'Label', 'Label'); m(M, 's.label.on', 'Label "Số điện thoại" luôn hiện phía trên ô, kể cả khi đang gõ.', 'The "Phone number" label stays above the field, even while typing.'); m(M, 's.label.off', 'Chỉ có placeholder trong ô; gõ xong là biến mất.', 'Only a placeholder inside the field; it disappears once typing starts.'); m(M, 'ev.label', 'label', 'label')
m(M, 's.validate.title', 'Khi nào báo lỗi', 'When errors appear'); m(M, 's.validate.on', 'Báo khi rời ô, ngay cạnh ô, không đợi bấm gửi.', 'Shown on leaving the field, right next to it, without waiting for submit.'); m(M, 's.validate.off', 'Chỉ báo sau khi bấm gửi, ở đầu trang.', 'Shown only after submit, at the top of the page.'); m(M, 'ev.validate', 'validate', 'validate')
m(M, 's.message.title', 'Nội dung lỗi', 'Error text'); m(M, 's.message.on', '"Nhập 10 chữ số, ví dụ 0901234567."', '"Enter 10 digits, for example 0901234567."'); m(M, 's.message.off', '"Dữ liệu không hợp lệ."', '"Invalid input."'); m(M, 'ev.message', 'thông báo', 'message')
m(M, 'co.try', 'Bật cả ba để thấy số vấn đề về 0.', 'Turn on all three to bring the issue count to 0.')
m(M, 'co.compose', 'Compose: `OutlinedTextField(label = { Text(…) }, isError = …, supportingText = { Text(…) })` (minh họa).', 'Compose: `OutlinedTextField(label = { Text(…) }, isError = …, supportingText = { Text(…) })` (illustrative).')
m(M, 'met.issues', 'Vấn đề còn lại (minh họa)', 'Remaining issues (illustrative)')

# ---------- E7 response ----------
M = 'response'
common(M, ('Thời gian phản hồi', 'Response times'), ('Mô phỏng tải dữ liệu với độ trễ chọn được, rồi chọn chỉ báo.', 'Simulate loading with a chosen delay, then pick an indicator.'),
       ('Mốc 0,1 s, 1 s, 10 s gợi ý loại phản hồi cần có; đây là mốc kinh nghiệm, không phải ranh giới tuyệt đối.', 'The 0.1 s, 1 s and 10 s limits suggest which feedback is needed; they are rules of thumb, not absolute boundaries.'),
       ('Độ trễ chỉ là con số minh họa; site không đo mạng thật.', 'Delays are illustrative numbers; the site measures no real network.'), ('Chọn độ trễ và chỉ báo.', 'Pick a delay and an indicator.'), ('Tải dữ liệu', 'Loading'), ('Màn hình, người dùng và thiết kế.', 'Screen, user and design.'))
m(M, 'ctl.delay', 'Độ trễ', 'Delay')
for d in (80, 600, 4000, 15000): m(M, 'ctl.delay.%d' % d, '%s ms' % d, '%s ms' % d)
m(M, 'ctl.indicator', 'Chỉ báo', 'Indicator')
for k, vi, en in [('none', 'không có', 'none'), ('spinner', 'spinner', 'spinner'), ('skeleton', 'skeleton', 'skeleton'), ('progress', 'thanh % tiến trình', 'percentage progress bar')]: m(M, 'ctl.indicator.' + k, vi, en)
m(M, 's.load.title', 'Tải danh sách giờ ({ms} ms)', 'Loading the slot list ({ms} ms)'); m(M, 's.load.explain', 'Lan mở màn Chọn giờ; dữ liệu mất {ms} ms để về.', 'Lan opens Choose a time; data takes {ms} ms to arrive.'); m(M, 'ev.load', 'bắt đầu tải', 'start loading')
for b, tv, te, xv, xe in [('instant', 'Dưới 0,1 s: cảm giác tức thì', 'Under 0.1 s: feels instant', 'Không cần chỉ báo; chỉ cần hiện kết quả.', 'No indicator needed; just show the result.'),
                          ('flow', 'Dưới 1 s: giữ mạch suy nghĩ', 'Under 1 s: flow of thought kept', 'Người dùng nhận ra độ trễ nhưng vẫn giữ mạch; chỉ báo nhẹ là đủ.', 'Users notice the delay but keep their flow; a light indicator is enough.'),
                          ('attention', 'Dưới 10 s: giữ được chú ý', 'Under 10 s: attention kept', 'Cần phản hồi rõ là hệ thống đang làm việc.', 'Clear feedback that the system is working is needed.'),
                          ('long', 'Trên 10 s: dễ mất chú ý', 'Over 10 s: attention is lost', 'Cần % hoàn thành và cách dừng.', 'A percent-done indicator and a way to stop are needed.')]:
    m(M, 'band.' + b + '.title', tv, te); m(M, 'band.' + b + '.explain', xv, xe)
m(M, 's.indicator.title', 'Chỉ báo bạn chọn', 'Your indicator')
for ind in ('none', 'spinner', 'skeleton', 'progress'):
    for b in ('instant', 'flow', 'attention', 'long'):
        good = {('none', 'instant'), ('spinner', 'flow'), ('skeleton', 'flow'), ('skeleton', 'attention'), ('spinner', 'attention'), ('progress', 'long'), ('progress', 'attention')}
        if (ind, b) in good: vi, en = 'Phù hợp với độ trễ này.', 'Fits this delay.'
        elif ind == 'none': vi, en = 'Không có phản hồi: người dùng không biết app có đang làm gì không.', 'No feedback: users cannot tell whether the app is working.'
        elif b == 'instant': vi, en = 'Thừa: chỉ báo nháy lên rồi biến mất gây rối mắt.', 'Overkill: an indicator that flashes and vanishes is distracting.'
        else: vi, en = 'Chưa đủ: chờ lâu cần cho biết còn bao lâu và cho phép dừng.', 'Not enough: long waits need to show how long is left and allow stopping.'
        m(M, 'ind.%s.%s' % (ind, b), vi, en)
m(M, 'co.source', 'Mốc 0,1 s / 1 s / 10 s theo Nielsen (1993, cập nhật 2014). [[src:nn-response]] [[badge:research]]', 'The 0.1 s / 1 s / 10 s limits per Nielsen (1993, updated 2014). [[src:nn-response]] [[badge:research]]')

# ---------- lab ----------
lab('pass', 'đạt', 'pass'); lab('fail', 'không đạt', 'fail')
lab('crap.title', 'Sửa màn "Xác nhận" bằng CRAP', 'Fixing the "Confirm" screen with CRAP')
lab('crap.intro', 'Bốn nguyên lý của Robin Williams (The Non-Designer\'s Design Book): Contrast, Repetition, Alignment, Proximity. Bật từng nguyên lý và đọc giải thích nhân quả; "nheo mắt" làm mờ để thấy phân cấp. [[badge:author-framework]]', 'Robin Williams\'s four principles (The Non-Designer\'s Design Book): Contrast, Repetition, Alignment, Proximity. Turn each on and read the cause and effect; "squint" blurs the screen to reveal hierarchy. [[badge:author-framework]]')
for k, vi, en in [('prox', 'Gần nhau (proximity)', 'Proximity'), ('align', 'Căn lề (alignment)', 'Alignment'), ('rep', 'Lặp lại (repetition)', 'Repetition'), ('contrast', 'Tương phản (contrast)', 'Contrast'), ('squint', 'Nheo mắt (squint test)', 'Squint test')]: lab('crap.' + k, vi, en)
lab('crap.book', 'Đặt lịch', 'Book'); lab('crap.back', 'Quay lại', 'Back')
for k, vi, en in [('prox', 'Gần nhau: nhãn và giá trị của cùng một mục sát nhau, các nhóm cách xa nhau → mắt nhóm đúng.', 'Proximity: a label and its value sit close, groups sit apart → the eye groups correctly.'),
                  ('align', 'Căn lề: mọi thứ theo một cạnh trái → mắt quét theo một đường thẳng.', 'Alignment: everything on one left edge → the eye scans along one line.'),
                  ('rep', 'Lặp lại: hai nút cùng hình dạng → biết chúng cùng loại.', 'Repetition: both buttons share a shape → they read as the same kind.'),
                  ('contrast', 'Tương phản: hành động chính nổi bật → biết bấm gì trước.', 'Contrast: the primary action stands out → you know what to tap first.'),
                  ('squint', 'Nheo mắt: làm mờ để thấy cái gì nổi lên đầu tiên — đó là phân cấp thị giác.', 'Squint: blur to see what stands out first — that is the visual hierarchy.')]:
    lab('crap.why.' + k, vi, en)
lab('crap.note', 'Gestalt (gần nhau, giống nhau) và phân cấp thị giác là nền nghiên cứu cho các nguyên lý này. Đẹp hơn không tự động dễ dùng hơn. (Đọc thêm) [[src:nn-gestalt]] [[src:nn-aesthetic]]', 'Gestalt (proximity, similarity) and visual hierarchy are the research basis for these principles. Prettier is not automatically more usable. (Further reading) [[src:nn-gestalt]] [[src:nn-aesthetic]]')
lab('type.title', 'Type scale playground', 'Type scale playground')
lab('type.intro', 'Vai trò chữ theo token M3 (cỡ/line height, đọc từ m3.material.io ngày 2026-11-21). Đổi mẫu vi/en, line height, độ rộng cột; thử cỡ chữ hệ thống 200%. [[src:m3-type]] [[badge:ds-guideline]]', 'Type roles from M3 tokens (size/line height, read from m3.material.io on 2026-11-21). Switch the vi/en sample, line height and column width; try 200% system font size. [[src:m3-type]] [[badge:ds-guideline]]')
lab('type.role', 'Vai trò', 'Role'); lab('type.sample', 'Mẫu chữ', 'Sample'); lab('type.sample.vi', 'Tiếng Việt', 'Vietnamese'); lab('type.sample.en', 'Tiếng Anh', 'English')
lab('type.lh', 'Line height', 'Line height'); lab('type.lhToken', 'theo token', 'token value'); lab('type.width', 'Độ rộng cột', 'Column width'); lab('type.zoom', 'Cỡ chữ hệ thống 200%', '200% system font size')
lab('type.text.vi', 'Lịch khám tổng quát của bạn vào thứ Năm lúc 9 giờ sáng. Hãy đến sớm mười lăm phút để làm thủ tục.', 'Lịch khám tổng quát của bạn vào thứ Năm lúc 9 giờ sáng. Hãy đến sớm mười lăm phút để làm thủ tục.')
lab('type.text.en', 'Your general check-up is on Thursday at 9 a.m. Please arrive fifteen minutes early to check in.', 'Your general check-up is on Thursday at 9 a.m. Please arrive fifteen minutes early to check in.')
lab('type.read', '{role}: cỡ {size}, line height {lh} (tỉ lệ {r}).', '{role}: size {size}, line height {lh} (ratio {r}).')
lab('type.warnVi', 'Tiếng Việt có dấu chồng (ví dụ "ặ", "ổ"): line height thấp hơn khoảng 1,2 lần cỡ chữ dễ làm dấu chạm dòng trên. Đây là ngưỡng kinh nghiệm của site, không phải chuẩn.', 'Vietnamese stacks diacritics (for example "ặ", "ổ"): a line height below about 1.2× the font size makes marks touch the line above. This is the site\'s rule of thumb, not a standard.')
lab('type.note', 'Trên Android dùng `sp` để chữ theo cài đặt cỡ chữ; WCAG 1.4.4 yêu cầu phóng to 200% không mất nội dung. Compose: `MaterialTheme.typography.bodyLarge`, `TextStyle(lineHeight = …)`. [[src:wcag22]]', 'On Android use `sp` so text follows the font-size setting; WCAG 1.4.4 requires 200% resizing without loss of content. Compose: `MaterialTheme.typography.bodyLarge`, `TextStyle(lineHeight = …)`. [[src:wcag22]]')
lab('contrast.title', 'Kiểm tra tương phản', 'Contrast checker')
lab('contrast.intro', 'Chọn màu chữ và màu nền; tỉ lệ tính theo relative luminance của WCAG 2.2 (ngưỡng 0.04045). Kiểm chứng: đen/trắng = 21:1, cùng màu = 1:1. [[src:wcag22]] [[badge:normative]] [[badge:quant-model]]', 'Pick text and background colours; the ratio uses WCAG 2.2 relative luminance (0.04045 threshold). Checks: black/white = 21:1, same colour = 1:1. [[src:wcag22]] [[badge:normative]] [[badge:quant-model]]')
lab('contrast.fg', 'Màu chữ', 'Text colour'); lab('contrast.bg', 'Màu nền', 'Background'); lab('contrast.example', 'Ví dụ đen/trắng', 'Black/white example')
lab('contrast.small', 'Chữ thường 14px: Lịch khám thứ Năm', 'Normal 14px text: Thursday appointment'); lab('contrast.large', 'Chữ lớn 24px', 'Large 24px text')
lab('contrast.ratio', 'Tỉ lệ tương phản: {r}:1', 'Contrast ratio: {r}:1')
for k, vi, en in [('aaText', 'chữ thường ≥ 4.5:1', 'normal text ≥ 4.5:1'), ('aaLarge', 'chữ lớn ≥ 3:1', 'large text ≥ 3:1'), ('aaaText', 'chữ thường ≥ 7:1', 'normal text ≥ 7:1'), ('aaaLarge', 'chữ lớn ≥ 4.5:1', 'large text ≥ 4.5:1'), ('nonText', 'thành phần không phải chữ ≥ 3:1', 'non-text components ≥ 3:1')]: lab('contrast.c.' + k, vi, en)
lab('contrast.note', 'Chữ lớn: ≥ 18 pt, hoặc ≥ 14 pt đậm. Đạt tương phản không có nghĩa là đủ accessible; WCAG là chuẩn kỹ thuật, việc nó có là luật hay không tùy từng nơi.', 'Large text: ≥ 18 pt, or ≥ 14 pt bold. Passing contrast does not mean accessible enough; WCAG is a technical standard, and whether it is law depends on the jurisdiction.')
lab('roles.title', 'Color roles trên Hẹn Khám (mô hình giản lược)', 'Color roles on ClinicBook (simplified model)')
lab('roles.intro', 'Chọn một màu nguồn; mô hình giữ sắc độ và đặt độ sáng cố định cho từng vai trò. Đây KHÔNG phải thuật toán HCT/dynamic color của Material. [[badge:simplified]] [[src:mdc-color]]', 'Pick a source colour; the model keeps its hue and sets a fixed lightness for each role. This is NOT Material\'s HCT/dynamic color algorithm. [[badge:simplified]] [[src:mdc-color]]')
lab('roles.src', 'Màu nguồn', 'Source colour'); lab('roles.dark', 'Dark', 'Dark'); lab('roles.shift', 'Độ sáng primary', 'Primary lightness')
lab('roles.shift.0', 'theo mô hình', 'model default'); lab('roles.shift.up', 'sáng hơn (+0,25)', 'lighter (+0.25)'); lab('roles.shift.down', 'tối hơn (−0,2)', 'darker (−0.2)')
lab('roles.colorOnly', 'Lỗi chỉ báo bằng màu', 'Error shown by colour only'); lab('roles.cvd', 'Bộ lọc mù màu (giản lược)', 'Colour-blindness filter (simplified)')
for k, vi, en in [('none', 'không', 'none'), ('protan', 'protan (giản lược)', 'protan (simplified)'), ('deutan', 'deutan (giản lược)', 'deutan (simplified)'), ('gray', 'thang xám', 'greyscale')]: lab('roles.cvd.' + k, vi, en)
lab('roles.errText', 'Nhập 10 chữ số', 'Enter 10 digits'); lab('roles.book', 'Đặt lịch', 'Book'); lab('roles.pair', 'Cặp vai trò', 'Role pair'); lab('roles.ratio', 'Tỉ lệ', 'Ratio')
lab('roles.onlyWarn', 'Lỗi chỉ thể hiện bằng viền đỏ: vi phạm WCAG 1.4.1 (Use of Color, mức A). Thêm icon và chữ.', 'The error is shown only by a red border: it fails WCAG 1.4.1 (Use of Color, level A). Add an icon and text.')
lab('roles.cvdNote', 'Bộ lọc là ma trận tuyến tính đơn giản để minh họa, không mô phỏng chính xác thị giác của người mù màu.', 'The filter is a simple linear matrix for illustration; it does not accurately simulate colour-blind vision.')
lab('roles.note', 'Mỗi cặp "on-" phải đọc được trên nền tương ứng. Light và dark là hai bảng màu khác nhau, không phải đảo màu. Dynamic color có từ Android 12 (`dynamicLightColorScheme(context)`). [[src:and-m3-compose]]', 'Each "on-" pair must be readable on its background. Light and dark are two different palettes, not inversions. Dynamic color exists from Android 12 (`dynamicLightColorScheme(context)`). [[src:and-m3-compose]]')
lab('responsive.title', 'Responsive lab', 'Responsive lab')
lab('responsive.intro', 'Kéo độ rộng cửa sổ (dp); breakpoint theo tài liệu Android, đọc 2026-11-21. Màn "Lịch của tôi" đổi cấu trúc. [[src:and-wsc]] [[badge:stable]]', 'Drag the window width (dp); breakpoints from the Android documentation, read 2026-11-21. "My appointments" changes structure. [[src:and-wsc]] [[badge:stable]]')
lab('responsive.width', 'Độ rộng cửa sổ (dp)', 'Window width (dp)'); lab('responsive.read', 'Độ rộng {w} dp → {cls}', 'Width {w} dp → {cls}')
for k, vi, en in [('compact', 'Compact (< 600)', 'Compact (< 600)'), ('medium', 'Medium (600–839)', 'Medium (600–839)'), ('expanded', 'Expanded (840–1199)', 'Expanded (840–1199)'), ('large', 'Large (1200–1599)', 'Large (1200–1599)'), ('xlarge', 'Extra-large (≥ 1600)', 'Extra-large (≥ 1600)')]: lab('responsive.cls.' + k, vi, en)
lab('responsive.detail', 'Chi tiết lịch hẹn', 'Appointment detail')
lab('responsive.layout.bar', 'Compact: một cột danh sách, navigation bar ở dưới.', 'Compact: a single list column, navigation bar at the bottom.')
lab('responsive.layout.rail', 'Medium: navigation rail bên trái, vẫn một danh sách.', 'Medium: a navigation rail on the left, still one list.')
lab('responsive.layout.twoPane', 'Expanded trở lên: list-detail hai cột, navigation rail. Cấu trúc đổi, không chỉ co giãn.', 'Expanded and up: two-pane list-detail with a rail. The structure changes, not just the size.')
lab('responsive.note', 'Compose: `currentWindowAdaptiveInfo().windowSizeClass`; `ListDetailPaneScaffold` cho list-detail (material3-adaptive). Large/Extra-large cần `supportLargeAndXLargeWidth = true`. Mô hình chọn bar/rail đơn giản hóa từ hướng dẫn. [[src:and-canonical]] [[src:and-m3-compose]] [[badge:version]]', 'Compose: `currentWindowAdaptiveInfo().windowSizeClass`; `ListDetailPaneScaffold` for list-detail (material3-adaptive). Large/Extra-large need `supportLargeAndXLargeWidth = true`. The bar/rail choice is simplified from the guidance. [[src:and-canonical]] [[src:and-m3-compose]] [[badge:version]]')
lab('fitts.title', 'Fitts playground', 'Fitts playground')
lab('fitts.intro', 'MT = a + b·log2(D/W + 1) (dạng Shannon; NN/g trình bày dạng log2(2D/W)). a, b là hệ số minh họa, chỉnh được. Bấm "Bắt đầu" rồi chạm mục tiêu. [[src:nn-fitts]] [[badge:quant-model]]', 'MT = a + b·log2(D/W + 1) (Shannon form; NN/g presents log2(2D/W)). a and b are illustrative coefficients you can change. Press "Start", then hit the target. [[src:nn-fitts]] [[badge:quant-model]]')
lab('fitts.privacy', 'Minh họa cá nhân: thời gian và số lần trượt của bạn chỉ nằm trong bộ nhớ trang, không lưu, không gửi đi.', 'Personal illustration: your times and misses stay only in page memory; not saved, not sent.')
lab('fitts.size', 'Kích thước mục tiêu (CSS px)', 'Target size (CSS px)'); lab('fitts.dist', 'Khoảng cách', 'Distance'); lab('fitts.expand', 'Vùng chạm mở rộng (≥ 48)', 'Expanded touch area (≥ 48)')
lab('fitts.start', 'Bắt đầu', 'Start'); lab('fitts.go', 'Chạm mục tiêu!', 'Hit the target!'); lab('fitts.target', 'Mục tiêu', 'Target')
lab('fitts.read', 'Dự đoán (minh họa): {pred} ms; độ khó {id} bit. Của bạn ở cấu hình này: {n} lần, trung bình {avg} ms; trượt {miss}.', 'Predicted (illustrative): {pred} ms; difficulty {id} bits. Yours for this setup: {n} tries, mean {avg} ms; misses {miss}.')
lab('fitts.note', 'Ba mốc khác nhau, không gộp: Android khuyến nghị target ≥ 48 dp; WCAG 2.5.8 (AA) ≥ 24×24 CSS px hoặc đủ khoảng cách; 2.5.5 (AAA) ≥ 44×44 CSS px. Lab giả định 1 dp ≈ 1 CSS px để minh họa. Compose: `Modifier.minimumInteractiveComponentSize()`. [[src:and-design-a11y]] [[src:and-a11y-defaults]] [[src:wcag22]]', 'Three different marks, not merged: Android recommends targets ≥ 48 dp; WCAG 2.5.8 (AA) ≥ 24×24 CSS px or enough spacing; 2.5.5 (AAA) ≥ 44×44 CSS px. The lab assumes 1 dp ≈ 1 CSS px for illustration. Compose: `Modifier.minimumInteractiveComponentSize()`. [[src:and-design-a11y]] [[src:and-a11y-defaults]] [[src:wcag22]]')
lab('states.title', 'Trạng thái component và state layer', 'Component states and state layers')
lab('states.intro', 'Chọn component và trạng thái; lớp phủ dùng độ mờ của M3 (hover 8%, focus 10%, press 10%, drag 16%; đọc 2026-11-21). [[src:m3-states]] [[badge:ds-guideline]]', 'Pick a component and a state; the overlay uses M3 opacities (hover 8%, focus 10%, press 10%, drag 16%; read 2026-11-21). [[src:m3-states]] [[badge:ds-guideline]]')
lab('states.comp', 'Component', 'Component')
for k, vi, en in [('button', 'Button', 'Button'), ('textfield', 'TextField', 'TextField'), ('navitem', 'Mục navigation bar', 'Navigation bar item')]: lab('states.comp.' + k, vi, en)
lab('states.state', 'Trạng thái', 'State')
for k, vi, en in [('enabled', 'enabled', 'enabled'), ('hover', 'hovered', 'hovered'), ('focus', 'focused', 'focused'), ('pressed', 'pressed', 'pressed'), ('dragged', 'dragged', 'dragged'), ('disabled', 'disabled', 'disabled')]: lab('states.state.' + k, vi, en)
lab('states.label.button', 'Đặt lịch', 'Book'); lab('states.label.nav', 'Trang chủ', 'Home')
lab('states.read', 'Trạng thái {state}: lớp phủ {op}% màu nội dung.', 'State {state}: a {op}% overlay of the content colour.')
lab('states.disabled', 'Disabled: nội dung mờ đi; site không ghi số vì chưa xác minh giá trị.', 'Disabled: the content is faded; the site gives no number because the value is unverified.')
lab('states.note', 'Focus phải nhìn thấy được (WCAG 2.4.7, AA): ở đây là viền focus, không chỉ lớp phủ. Compose: `Button`, `OutlinedTextField(isError, supportingText)`, `NavigationBar`. [[src:wcag22]]', 'Focus must be visible (WCAG 2.4.7, AA): here a focus ring, not just an overlay. Compose: `Button`, `OutlinedTextField(isError, supportingText)`, `NavigationBar`. [[src:wcag22]]')
lab('tokens.title', 'Token editor → MaterialTheme', 'Token editor → MaterialTheme')
lab('tokens.intro', 'Sửa token (màu nguồn, góc bo, tỉ lệ chữ, mật độ) và xem Hẹn Khám cập nhật cùng đoạn `MaterialTheme` sinh ra. Màu dùng mô hình giản lược của E3. [[badge:simplified]]', 'Edit tokens (source colour, corner radius, type scale, density) and see ClinicBook update together with the generated `MaterialTheme` snippet. Colours use E3\'s simplified model. [[badge:simplified]]')
lab('tokens.src', 'Màu nguồn', 'Source colour'); lab('tokens.radius', 'Góc bo (dp)', 'Corner radius (dp)'); lab('tokens.scale', 'Tỉ lệ chữ', 'Type scale'); lab('tokens.dense', 'Mật độ cao', 'Compact density')
lab('tokens.warn', 'Cặp không đạt 4.5:1: {pairs}', 'Pairs below 4.5:1: {pairs}')
lab('tokens.note', 'Đoạn mã minh họa, kiểm tra API hiện hành trước khi dùng. `MaterialTheme` cung cấp giá trị qua `CompositionLocal`; đổi theme là đổi state nên nơi đọc giá trị sẽ recompose (B0, B4). [[src:and-m3-compose]]', 'Illustrative snippet; check the current API before using it. `MaterialTheme` provides values through `CompositionLocal`; changing the theme changes state, so places reading those values recompose (B0, B4). [[src:and-m3-compose]]')
lab('motion.title', 'Motion purpose lab', 'Motion purpose lab')
lab('motion.intro', 'Cùng một chuyển cảnh (mở chi tiết lịch hẹn) với token easing/duration của M3 (đọc 2026-11-21). [[src:m3-motion]] [[badge:ds-guideline]]', 'The same transition (opening an appointment) with M3 easing/duration tokens (read 2026-11-21). [[src:m3-motion]] [[badge:ds-guideline]]')
lab('motion.easing', 'Easing', 'Easing'); lab('motion.dur', 'Duration', 'Duration'); lab('motion.reduce', 'Giảm chuyển động (trong lab)', 'Reduce motion (in the lab)')
lab('motion.detail', 'Khám tổng quát · Bác sĩ Minh · Phòng 203. Mang theo thẻ bảo hiểm.', 'General check-up · Dr Minh · Room 203. Bring your insurance card.')
lab('motion.open', 'Mở chi tiết', 'Open details'); lab('motion.close', 'Đóng chi tiết', 'Close details')
lab('motion.reduced', 'Giảm chuyển động đang bật: thẻ đổi kích thước tức thì.', 'Reduced motion is on: the card resizes instantly.')
lab('motion.read', 'Easing {e}, {d} ms.', 'Easing {e}, {d} ms.')
lab('motion.note', 'Cơ chế frame của chuyển động trong Compose: C2 (spec, easing) và C7 (frame clock, phase). Site tôn trọng `prefers-reduced-motion` và có nút tắt chuyển động. [[src:wcag22]]', 'How motion advances per frame in Compose: C2 (specs, easing) and C7 (frame clock, phases). The site respects `prefers-reduced-motion` and has a motion toggle. [[src:wcag22]]')
lab('a11y.title', 'Kiểm tra accessibility Hẹn Khám', 'ClinicBook accessibility audit')
lab('a11y.intro', 'Bật/tắt các vấn đề cài sẵn; bảng liệt kê tiêu chí WCAG 2.2 (mã và mức) và cách sửa trong Compose. [[src:wcag22]] [[badge:normative]]', 'Toggle planted issues; the table lists WCAG 2.2 criteria (code and level) and the Compose fix. [[src:wcag22]] [[badge:normative]]')
for k, vi, en in [('icon', 'Icon không nhãn', 'Unlabeled icon'), ('contrast', 'Tương phản thấp', 'Low contrast'), ('target', 'Target nhỏ', 'Small target'), ('order', 'Thứ tự focus sai', 'Wrong focus order'), ('colorOnly', 'Lỗi form chỉ bằng màu', 'Form error by colour only'), ('fixedText', 'Chữ cỡ cố định', 'Fixed-size text')]: lab('a11y.i.' + k, vi, en)
for k, vi, en in [('icon', '`Icon(contentDescription = "Cài đặt")` hoặc `Modifier.semantics { contentDescription = … }`', '`Icon(contentDescription = "Settings")` or `Modifier.semantics { contentDescription = … }`'),
                  ('contrast', 'Dùng cặp "on-" đạt ≥ 4.5:1', 'Use an "on-" pair reaching ≥ 4.5:1'), ('target', '`Modifier.minimumInteractiveComponentSize()` (48 dp)', '`Modifier.minimumInteractiveComponentSize()` (48 dp)'),
                  ('order', 'Sắp lại thứ tự bố cục; `Modifier.semantics { traversalIndex = … }` khi cần (minh họa)', 'Reorder the layout; `Modifier.semantics { traversalIndex = … }` when needed (illustrative)'),
                  ('colorOnly', '`supportingText` + icon lỗi, không chỉ màu viền', '`supportingText` + an error icon, not just the border colour'), ('fixedText', 'Dùng `sp` và cho layout co giãn', 'Use `sp` and let the layout grow')]: lab('a11y.fix.' + k, vi, en)
lab('a11y.err', 'Nhập 10 chữ số', 'Enter 10 digits'); lab('a11y.col.issue', 'Vấn đề', 'Issue'); lab('a11y.col.fix', 'Cách sửa (Compose)', 'Fix (Compose)')
lab('a11y.unlabeled', '(không có nhãn)', '(unlabeled)'); lab('a11y.settings', 'Cài đặt', 'Settings'); lab('a11y.order', 'Thứ tự đọc tuyến tính', 'Linear reading order')
for k, vi, en in [('heading', 'tiêu đề', 'heading'), ('button', 'nút', 'button'), ('text', 'văn bản', 'text'), ('edit', 'ô nhập', 'edit field')]: lab('a11y.role.' + k, vi, en)
lab('a11y.notTalkback', 'Mô phỏng giản lược từ một mô hình semantics nhỏ, không phải TalkBack thật.', 'A simplified simulation from a small semantics model, not real TalkBack.')
lab('a11y.note', 'Semantics tree phục vụ trợ năng và kiểm thử (B9). Compose: `Modifier.semantics { heading() }`, `clearAndSetSemantics`, `Role.Button`, `stateDescription`. [[src:and-design-a11y]]', 'The semantics tree serves accessibility and testing (B9). Compose: `Modifier.semantics { heading() }`, `clearAndSetSemantics`, `Role.Button`, `stateDescription`. [[src:and-design-a11y]]')
for k, vi, en in [('crap', 'CRAP', 'CRAP'), ('type', 'Type scale', 'Type scale'), ('contrast', 'Tương phản', 'Contrast'), ('roles', 'Color roles', 'Color roles'), ('responsive', 'Responsive', 'Responsive'), ('fitts', 'Fitts', 'Fitts'), ('states', 'Trạng thái', 'States'), ('tokens', 'Token', 'Tokens'), ('motion', 'Chuyển động', 'Motion'), ('a11y', 'Accessibility', 'Accessibility')]:
    pass

# ---------- chương ----------
def ch(c, title, essence, g1, g2, secs, quiz, sims=None):
    a(c + '.title', *title); a(c + '.essence', *essence); a(c + '.goal.g1', *g1); a(c + '.goal.g2', *g2)
    for sid, stitle, badge, paras in secs:
        a(c + '.sec.' + sid + '.title', *stitle); a(c + '.sec.' + sid + '.badge', badge, badge)
        for i, p in enumerate(paras): a(c + '.sec.' + sid + '.p.' + str(i + 1), *p)
    for i, (q, ans, why) in enumerate(quiz):
        a(c + '.quiz.q%d.q' % (i + 1), *q); a(c + '.quiz.q%d.a' % (i + 1), *ans); a(c + '.quiz.q%d.why' % (i + 1), *why)
    for sid, vi, en in (sims or []): a(c + '.sim.' + sid, vi, en)
Q2 = lambda q, an, w: (q, an, w)

ch('e0', ('Bản đồ UI: từ token tới màn hình', 'The UI map: from tokens to screens'),
   ('UI là các lớp xếp chồng: design token → component → pattern → màn hình → luồng.\nMaterial 3 là một design system; Compose Material 3 là cách triển khai nó.\nUX bao trùm cả trải nghiệm (D0); track này tập trung vào bề mặt giao diện.', 'A UI is stacked layers: design token → component → pattern → screen → flow.\nMaterial 3 is a design system; Compose Material 3 implements it.\nUX covers the whole experience (D0); this track focuses on the interface surface.'),
   ('Đã xem ví dụ một lớp', 'Saw one layer\'s example'), ('Đã đi hết ba bước', 'Walked all three steps'),
   [('x5', ('Cầu nối X5 (tóm tắt)', 'Bridge X5 (summary)'), 'ds-guideline', [('Token màu, chữ, hình khối của Material 3 đi vào `MaterialTheme` trong Compose; chương E8 nói đầy đủ. [[src:and-m3-compose]]', 'Material 3 colour, type and shape tokens flow into `MaterialTheme` in Compose; chapter E8 covers it fully. [[src:and-m3-compose]]')])],
   [Q2(('Compose Material 3 có phải là Material 3?', 'Is Compose Material 3 the same as Material 3?'), ('Không hẳn.', 'Not quite.'), ('Material 3 là design system; Compose Material 3 là một cách triển khai.', 'Material 3 is the design system; Compose Material 3 is one implementation.')),
    Q2(('Một nút "Đặt lịch" thuộc lớp nào?', 'Which layer is a "Book" button?'), ('Component.', 'Component.'), ('Nó dùng token màu primary.', 'It uses the primary colour token.'))])

ch('e1', ('Nguyên lý thị giác', 'Visual principles'),
   ('Mắt nhóm những thứ gần nhau và giống nhau; căn lề tạo trật tự; lặp lại tạo nhất quán.\nTương phản tạo phân cấp để người dùng biết đọc gì trước.\nĐẹp không đồng nghĩa dễ dùng: hiệu ứng thẩm mỹ–khả dụng giải thích vì sao người dùng tha thứ cho vấn đề khi giao diện đẹp.', 'The eye groups things that are close and similar; alignment creates order; repetition creates consistency.\nContrast creates hierarchy so users know what to read first.\nBeautiful is not the same as usable: the aesthetic-usability effect explains why users forgive problems in beautiful interfaces.'),
   ('Đã mở lab CRAP', 'Opened the CRAP lab'), ('Đã thử squint test', 'Tried the squint test'),
   [('p', ('CRAP và Gestalt', 'CRAP and Gestalt'), 'author-framework research', [('CRAP là bốn nguyên lý của Robin Williams (The Non-Designer\'s Design Book), dùng làm khung thực hành; Gestalt (gần nhau, giống nhau) là nền nghiên cứu. (Đọc thêm) [[src:nn-gestalt]]', 'CRAP is Robin Williams\'s four principles (The Non-Designer\'s Design Book), a practical frame; Gestalt (proximity, similarity) is the research basis. (Further reading) [[src:nn-gestalt]]')])],
   [Q2(('Squint test để làm gì?', 'What is the squint test for?'), ('Thấy phân cấp thị giác.', 'To see the visual hierarchy.'), ('Làm mờ thì chỉ còn thứ nổi bật nhất.', 'Blurring leaves only what stands out most.')),
    Q2(('Đẹp có làm giao diện dễ dùng hơn?', 'Does beauty make an interface easier to use?'), ('Không tự động.', 'Not automatically.'), ('Nó làm người dùng tha thứ cho vấn đề.', 'It makes users forgive problems.'))])

ch('e2', ('Typography và chữ tiếng Việt', 'Typography and Vietnamese text'),
   ('Type scale tạo phân cấp có hệ thống; line height và độ dài dòng ảnh hưởng độ dễ đọc.\nTiếng Việt có dấu chồng nên cần line height đủ và font hỗ trợ đầy đủ.\nNgười dùng có thể phóng to chữ: layout phải co giãn (sp trên Android, WCAG 1.4.4).', 'A type scale creates systematic hierarchy; line height and line length affect readability.\nVietnamese stacks diacritics, so it needs enough line height and full font support.\nUsers can enlarge text: layouts must grow (sp on Android, WCAG 1.4.4).'),
   ('Đã thử một vai trò chữ', 'Tried one type role'), ('Đã thử cỡ 200%', 'Tried 200% size'),
   [('t', ('Type scale của M3', 'The M3 type scale'), 'ds-guideline', [('15 vai trò từ displayLarge (57/64) tới labelSmall (11/16); đọc từ m3.material.io ngày 2026-11-21. Line height của bộ baseline lấy theo bộ emphasized cùng cỡ (trang hiển thị đủ số của bộ emphasized). [[src:m3-type]]', '15 roles from displayLarge (57/64) to labelSmall (11/16); read from m3.material.io on 2026-11-21. Baseline line heights follow the same-size emphasized set (the page shows the emphasized numbers in full). [[src:m3-type]]')])],
   [Q2(('Vì sao tiếng Việt cần line height cao hơn?', 'Why does Vietnamese need more line height?'), ('Dấu chồng (ví dụ "ặ").', 'Stacked diacritics (for example "ặ").'), ('Dấu dễ chạm dòng trên.', 'Marks can touch the line above.')),
    Q2(('Đơn vị chữ trên Android?', 'The text unit on Android?'), ('sp.', 'sp.'), ('Để theo cài đặt cỡ chữ của người dùng.', 'So it follows the user\'s font-size setting.'))])

ch('e3', ('Màu: color roles, dynamic color, tương phản', 'Colour: roles, dynamic color, contrast'),
   ('Màu theo vai trò, không theo tên màu: primary/onPrimary, primaryContainer/onPrimaryContainer, surface/onSurface, error…\nMỗi cặp "on-" phải đọc được trên nền tương ứng; light và dark là hai bảng màu khác nhau.\nTương phản tính theo WCAG; màu không được là cách duy nhất truyền thông tin (1.4.1).', 'Colour by role, not by hue: primary/onPrimary, primaryContainer/onPrimaryContainer, surface/onSurface, error…\nEach "on-" pair must be readable on its background; light and dark are two different palettes.\nContrast is computed per WCAG; colour must not be the only way to convey information (1.4.1).'),
   ('Đã tính một tỉ lệ tương phản', 'Computed one contrast ratio'), ('Đã thử bộ lọc mù màu', 'Tried the colour-blindness filter'),
   [('c', ('Ngưỡng WCAG 2.2', 'WCAG 2.2 thresholds'), 'normative', [('1.4.3 Contrast (Minimum), AA: 4.5:1, chữ lớn 3:1. 1.4.6 Contrast (Enhanced), AAA: 7:1, chữ lớn 4.5:1. 1.4.11 Non-text Contrast, AA: 3:1. 1.4.1 Use of Color, A. [[src:wcag22]]', '1.4.3 Contrast (Minimum), AA: 4.5:1, large text 3:1. 1.4.6 Contrast (Enhanced), AAA: 7:1, large text 4.5:1. 1.4.11 Non-text Contrast, AA: 3:1. 1.4.1 Use of Color, A. [[src:wcag22]]'),
     ('Compose: `lightColorScheme(...)`, `darkColorScheme(...)`, `dynamicLightColorScheme(context)` khi `Build.VERSION.SDK_INT >= Build.VERSION_CODES.S` (Android 12+). [[src:and-m3-compose]] [[badge:version]]', 'Compose: `lightColorScheme(...)`, `darkColorScheme(...)`, `dynamicLightColorScheme(context)` when `Build.VERSION.SDK_INT >= Build.VERSION_CODES.S` (Android 12+). [[src:and-m3-compose]] [[badge:version]]')])],
   [Q2(('Đen trên trắng có tỉ lệ bao nhiêu?', 'What is black on white?'), ('21:1.', '21:1.'), ('Mức cao nhất theo công thức WCAG.', 'The maximum under the WCAG formula.')),
    Q2(('Dark mode có phải đảo màu?', 'Is dark mode an inversion?'), ('Không.', 'No.'), ('Hai bảng màu khác nhau, mỗi cặp kiểm tra riêng.', 'Two different palettes, each pair checked separately.'))],
   [('ui.contrast', 'Tương phản', 'Contrast'), ('ui.roles', 'Color roles', 'Color roles')])

ch('e4', ('Bố cục và giao diện thích ứng', 'Layout and adaptive UI'),
   ('Lưới và hệ khoảng cách tạo nhịp điệu.\nAndroid chạy trên nhiều kích thước: dùng window size class và canonical layouts (list-detail, supporting pane, feed).\nBố cục thích ứng thay đổi cấu trúc, không chỉ co giãn.', 'Grids and spacing systems create rhythm.\nAndroid runs on many sizes: use window size classes and canonical layouts (list-detail, supporting pane, feed).\nAdaptive layout changes structure, not just size.'),
   ('Đã kéo độ rộng', 'Dragged the width'), ('Đã thấy list-detail', 'Saw list-detail'),
   [('w', ('Breakpoint', 'Breakpoints'), 'stable', [('Compact < 600 dp; Medium 600–839; Expanded 840–1199; Large 1200–1599; Extra-large ≥ 1600 (đọc 2026-11-21). Độ rộng thường quan trọng hơn chiều cao. [[src:and-wsc]]', 'Compact < 600 dp; Medium 600–839; Expanded 840–1199; Large 1200–1599; Extra-large ≥ 1600 (read 2026-11-21). Width usually matters more than height. [[src:and-wsc]]')])],
   [Q2(('700 dp thuộc lớp nào?', 'Which class is 700 dp?'), ('Medium.', 'Medium.'), ('600 ≤ 700 < 840.', '600 ≤ 700 < 840.')), Q2(('Thích ứng chỉ là co giãn?', 'Is adaptive just stretching?'), ('Không.', 'No.'), ('Cấu trúc đổi, ví dụ thành list-detail.', 'The structure changes, for example to list-detail.'))])

ch('e5', ('Vùng chạm và Fitts\'s law', 'Touch targets and Fitts\'s law'),
   ('Thời gian chạm tới mục tiêu phụ thuộc khoảng cách và kích thước (Fitts).\nMục tiêu nhỏ hoặc sát nhau gây slip (D3).\nBa mốc khác nhau: khuyến nghị Android 48 dp, WCAG 2.5.8 (AA) và 2.5.5 (AAA); không gộp làm một.', 'Time to reach a target depends on distance and size (Fitts).\nSmall or crowded targets cause slips (D3).\nThree different marks: Android\'s 48 dp recommendation, WCAG 2.5.8 (AA) and 2.5.5 (AAA); do not merge them.'),
   ('Đã thử một lần chạm', 'Tried one tap'), ('Đã bật vùng chạm mở rộng', 'Turned on the expanded touch area'),
   [('f', ('Mô hình và giới hạn', 'Model and limits'), 'quant-model', [('Mô hình áp dụng cho trỏ chạm và chuột trong điều kiện thực nghiệm; không dự đoán chính xác cho từng người. a, b trong lab là minh họa. [[src:nn-fitts]]', 'The model applies to touch and mouse pointing under experimental conditions; it does not predict individuals precisely. a and b in the lab are illustrative. [[src:nn-fitts]]')])],
   [Q2(('WCAG 2.5.8 yêu cầu gì?', 'What does WCAG 2.5.8 require?'), ('≥ 24×24 CSS px hoặc đủ khoảng cách (AA).', '≥ 24×24 CSS px or enough spacing (AA).'), ('Khác với khuyến nghị 48 dp của Android.', 'Different from Android\'s 48 dp recommendation.')),
    Q2(('Icon 24 dp có vùng chạm lớn hơn được không?', 'Can a 24 dp icon have a larger touch area?'), ('Có.', 'Yes.'), ('`minimumInteractiveComponentSize` giữ 48 dp.', '`minimumInteractiveComponentSize` reserves 48 dp.'))])

ch('e6', ('Component và trạng thái tương tác', 'Components and interaction states'),
   ('Component có các trạng thái enabled, disabled, hovered, focused, pressed, dragged.\nMaterial 3 dùng state layer (lớp phủ có độ mờ theo trạng thái) để phản hồi nhất quán.\nTrạng thái focus phải nhìn thấy được (WCAG 2.4.7).', 'Components have enabled, disabled, hovered, focused, pressed and dragged states.\nMaterial 3 uses state layers (overlays with state-dependent opacity) for consistent feedback.\nFocus must be visible (WCAG 2.4.7).'),
   ('Đã chọn một trạng thái', 'Picked a state'), ('Đã xem trạng thái focus', 'Looked at the focus state'),
   [('s', ('State layer', 'State layers'), 'ds-guideline', [('Hover +8%, focus +10%, press +10%, drag +16% opacity (m3.material.io, đọc 2026-11-21). [[src:m3-states]]', 'Hover +8%, focus +10%, press +10%, drag +16% opacity (m3.material.io, read 2026-11-21). [[src:m3-states]]')])],
   [Q2(('Lớp phủ khi nhấn là bao nhiêu?', 'What is the pressed overlay?'), ('10%.', '10%.'), ('Theo trang state layers của M3.', 'Per M3\'s state layers page.')), Q2(('Chỉ lớp phủ có đủ cho focus?', 'Is an overlay alone enough for focus?'), ('Nên có chỉ báo focus nhìn rõ.', 'A clearly visible focus indicator is needed.'), ('WCAG 2.4.7.', 'WCAG 2.4.7.'))])

ch('e7', ('Pattern', 'Patterns'),
   ('Pattern là lời giải đã kiểm chứng cho một bối cảnh; anti-pattern và deceptive pattern cần tránh (D5).\nPhản hồi theo thời gian: mốc 0,1 s, 1 s, 10 s (Nielsen) — mốc kinh nghiệm có giới hạn.\nNhãn và form dài ra khi đổi ngôn ngữ: kiểm tra pattern không vỡ ở cả vi và en (X8).', 'A pattern is a proven solution for one context; anti-patterns and deceptive patterns are to be avoided (D5).\nFeedback over time: the 0.1 s, 1 s and 10 s limits (Nielsen) — rules of thumb with limits.\nLabels and forms grow when the language changes: check that patterns survive both vi and en (X8).'),
   ('Đã chọn một pattern', 'Picked one pattern'), ('Đã thử form clinic', 'Tried the form clinic'),
   [('p', ('Bối cảnh và đánh đổi', 'Context and trade-offs'), 'research', [('Mỗi pattern trong lab có "khi nào dùng" và "khi nào không"; ví dụ điều hướng ẩn làm người dùng ít khám phá. (Đọc thêm) [[src:nn-hamburger]] [[src:nn-placeholders]]', 'Each pattern in the lab has "when to use" and "when not to"; for example hidden navigation reduces discovery. (Further reading) [[src:nn-hamburger]] [[src:nn-placeholders]]')])],
   [Q2(('Tải trên 10 giây cần gì?', 'What does a wait over 10 seconds need?'), ('% hoàn thành và cách dừng.', 'Percent done and a way to stop.'), ('Theo mốc của Nielsen.', 'Per Nielsen\'s limits.')), Q2(('Placeholder thay label được không?', 'Can a placeholder replace a label?'), ('Không nên.', 'It should not.'), ('Nó biến mất khi gõ.', 'It disappears while typing.'))],
   [('ui.patterns', 'Pattern', 'Patterns'), ('ui.form', 'Form', 'Form'), ('ui.response', 'Phản hồi', 'Response time')])

ch('e8', ('Design system và token → MaterialTheme', 'Design systems and tokens → MaterialTheme'),
   ('Design system gồm token, component, hướng dẫn, quy trình và người duy trì; không chỉ là thư viện component.\nToken đặt tên theo vai trò nên thay đổi lan truyền nhất quán.\nAtomic design (Brad Frost) là một cách nghĩ về cấp độ, không phải chuẩn.', 'A design system includes tokens, components, guidelines, processes and maintainers; it is not just a component library.\nRole-named tokens make changes propagate consistently.\nAtomic design (Brad Frost) is one way to think about levels, not a standard.'),
   ('Đã sửa một token', 'Edited a token'), ('Đã xem đoạn MaterialTheme', 'Looked at the MaterialTheme snippet'),
   [('x5', ('Cầu nối X5: Material 3 theming trong Compose', 'Bridge X5: Material 3 theming in Compose'), 'ds-guideline stable', [
      ('Color roles, type scale và shapes của Material 3 trở thành `MaterialTheme(colorScheme = …, typography = Typography(…), shapes = Shapes(…))`; component đọc `MaterialTheme.colorScheme.primary`, `MaterialTheme.typography.bodyLarge`. [[src:and-m3-compose]]', 'Material 3 colour roles, type scale and shapes become `MaterialTheme(colorScheme = …, typography = Typography(…), shapes = Shapes(…))`; components read `MaterialTheme.colorScheme.primary`, `MaterialTheme.typography.bodyLarge`. [[src:and-m3-compose]]'),
      ('`MaterialTheme` cung cấp giá trị qua `CompositionLocal` (B0); đổi theme là đổi state, nên nơi đọc giá trị sẽ recompose (B4). Các chương E2, E3, B0 chỉ nhắc lại phần này. Atomic design: [[badge:author-framework]] (Đọc thêm) [[src:nn-designsystems]]', '`MaterialTheme` provides values through `CompositionLocal` (B0); changing the theme changes state, so readers recompose (B4). Chapters E2, E3 and B0 only recap this part. Atomic design: [[badge:author-framework]] (Further reading) [[src:nn-designsystems]]')])],
   [Q2(('Design system có phải chỉ là UI kit?', 'Is a design system just a UI kit?'), ('Không.', 'No.'), ('Còn hướng dẫn, quy trình, người duy trì.', 'It also has guidelines, processes and maintainers.')), Q2(('Vì sao đặt tên token theo vai trò?', 'Why name tokens by role?'), ('Để thay đổi lan truyền nhất quán.', 'So changes propagate consistently.'), ('Đổi `primary` một chỗ, mọi nơi dùng nó đổi theo.', 'Change `primary` once and every use follows.'))])

ch('e9', ('Chuyển động có mục đích', 'Purposeful motion'),
   ('Chuyển động dùng để hướng chú ý, thể hiện quan hệ không gian, phản hồi hành động và che độ trễ.\nChuyển động trang trí có thể gây xao nhãng, thậm chí khó chịu cho người nhạy cảm với chuyển động.\nMaterial định nghĩa token easing và duration.', 'Motion is for directing attention, showing spatial relationships, giving feedback and covering latency.\nDecorative motion can distract and even harm people sensitive to motion.\nMaterial defines easing and duration tokens.'),
   ('Đã mở lab', 'Opened the lab'), ('Đã thử giảm chuyển động', 'Tried reduced motion'),
   [('x7', ('Cầu nối X7: Material motion và Compose Animation', 'Bridge X7: Material motion and Compose Animation'), 'ds-guideline normative', [
      ('Token M3 (đọc 2026-11-21): standard cubic-bezier(0.2, 0, 0, 1), standard decelerate (0, 0, 0, 1), standard accelerate (0.3, 0, 1, 1), emphasized decelerate (0.05, 0.7, 0.1, 1), emphasized accelerate (0.3, 0, 0.8, 0.15); duration short1–4 50–200 ms, medium1–4 250–400 ms, long1–4 450–600 ms, extra-long1–4 700–1000 ms. [[src:m3-motion]]', 'M3 tokens (read 2026-11-21): standard cubic-bezier(0.2, 0, 0, 1), standard decelerate (0, 0, 0, 1), standard accelerate (0.3, 0, 1, 1), emphasized decelerate (0.05, 0.7, 0.1, 1), emphasized accelerate (0.3, 0, 0.8, 0.15); durations short1–4 50–200 ms, medium1–4 250–400 ms, long1–4 450–600 ms, extra-long1–4 700–1000 ms. [[src:m3-motion]]'),
      ('Trong Compose, token thành `tween(durationMillis, easing = CubicBezierEasing(…))` (C2); animation tiến theo frame clock và phase đọc giá trị quyết định công việc mỗi frame (C7, X1). Chương C0, C2, D1 chỉ nhắc lại phần này.', 'In Compose, tokens become `tween(durationMillis, easing = CubicBezierEasing(…))` (C2); animations advance with the frame clock, and the phase that reads the value decides the per-frame work (C7, X1). Chapters C0, C2 and D1 only recap this part.'),
      ('WCAG 2.3.3 Animation from Interactions (AAA): chuyển động do tương tác có thể tắt được trừ khi thiết yếu; 2.2.2 Pause, Stop, Hide (A) cho nội dung tự chuyển động. [[src:wcag22]]', 'WCAG 2.3.3 Animation from Interactions (AAA): interaction-triggered motion can be disabled unless essential; 2.2.2 Pause, Stop, Hide (A) for auto-moving content. [[src:wcag22]]')])],
   [Q2(('Chuyển động nên dùng khi nào?', 'When should motion be used?'), ('Khi có mục đích: chú ý, quan hệ, phản hồi, che trễ.', 'When it has a purpose: attention, relationships, feedback, latency.'), ('Trang trí thì dễ gây xao nhãng.', 'Decoration tends to distract.')), Q2(('medium4 là bao nhiêu ms?', 'How many ms is medium4?'), ('400 ms.', '400 ms.'), ('Theo token M3.', 'Per the M3 tokens.'))])

ch('e10', ('Accessibility trong UI Compose', 'Accessibility in Compose UI'),
   ('WCAG xoay quanh bốn nguyên tắc: perceivable, operable, understandable, robust.\nTrên Android, Compose cung cấp semantics cho TalkBack và kiểm thử (B9).\nAccessibility là thiết kế bao hàm cho nhiều người, không phải checklist cuối dự án.', 'WCAG rests on four principles: perceivable, operable, understandable, robust.\nOn Android, Compose provides semantics for TalkBack and testing (B9).\nAccessibility is inclusive design for many people, not an end-of-project checklist.'),
   ('Đã tắt một vấn đề', 'Turned off one issue'), ('Đã xem thứ tự đọc', 'Looked at the reading order'),
   [('x6', ('Cầu nối X6: WCAG, semantics và thiết kế bao hàm', 'Bridge X6: WCAG, semantics and inclusive design'), 'normative stable', [
      ('Bốn nguyên tắc của WAI: perceivable, operable, understandable, robust. WCAG là chuẩn kỹ thuật của W3C (2.2, 12/2024); việc nó có là nghĩa vụ pháp lý hay không tùy nơi. Đạt tương phản chưa phải là đủ accessible. [[src:wai-principles]] [[src:wcag22]]', 'WAI\'s four principles: perceivable, operable, understandable, robust. WCAG is a W3C technical standard (2.2, Dec 2024); whether it is a legal duty depends on the place. Passing contrast is not the same as being accessible. [[src:wai-principles]] [[src:wcag22]]'),
      ('Compose: `Modifier.semantics { contentDescription = …; heading() }`, `clearAndSetSemantics`, `Role.Button`, `stateDescription`; target ≥ 48 dp với `minimumInteractiveComponentSize`; chữ dùng `sp`. Semantics tree là cây song song phục vụ trợ năng và kiểm thử (B9). [[src:and-design-a11y]] [[src:and-a11y-defaults]]', 'Compose: `Modifier.semantics { contentDescription = …; heading() }`, `clearAndSetSemantics`, `Role.Button`, `stateDescription`; targets ≥ 48 dp with `minimumInteractiveComponentSize`; text in `sp`. The semantics tree is a parallel tree serving accessibility and testing (B9). [[src:and-design-a11y]] [[src:and-a11y-defaults]]'),
      ('Chữ cũng là trợ năng: link nói rõ đích, alt text, thông báo lỗi chỉ cách sửa (D9, D3). Các chương B9, D2, D9 chỉ nhắc lại phần này.', 'Words are accessibility too: links that state the destination, alt text, errors that show the fix (D9, D3). Chapters B9, D2 and D9 only recap this part.')])],
   [Q2(('Đạt tương phản là đủ accessible?', 'Is passing contrast enough for accessibility?'), ('Không.', 'No.'), ('Còn nhãn, thứ tự focus, target, cỡ chữ…', 'Labels, focus order, targets, text size and more also matter.')), Q2(('Mô phỏng thứ tự đọc có phải TalkBack?', 'Is the reading-order simulation TalkBack?'), ('Không.', 'No.'), ('Đó là mô hình semantics giản lược.', 'It is a simplified semantics model.'))])

def norm(s): return unicodedata.normalize('NFC', s)
# ---- caption sơ đồ ("Bạn đang xem") và nhãn chú giải, thêm 2026-11-21 ----
a('cap.loop', 'Vòng phản hồi của thiết kế: thiết kế tạo ra màn hình, người dùng dùng màn hình, những gì quan sát được quay về sửa thiết kế. Thẻ được nhấn là phần bước này đang xét; câu hỏi và lựa chọn nằm ở bảng bên phải.', 'The design feedback loop: the design produces a screen, people use the screen, what you observe goes back into the design. The highlighted card is the part this step is about; the question and choices are in the panel on the right.')
a('cap.layers', 'Từ token tới luồng màn hình, trái sang phải: mỗi lớp được ghép từ lớp bên trái.', 'From tokens to screen flows, left to right: each layer is built from the one to its left.')

keys = [k for k, _, _ in E]; dup = sorted(set(k for k in keys if keys.count(k) > 1)); assert not dup, dup
for lang, idx in (('vi', 1), ('en', 2)):
    body = ',\n'.join('  %s: %s' % (json.dumps(e[0]), json.dumps(norm(e[idx]), ensure_ascii=False)) for e in E)
    open(os.path.join(ROOT, 'tracks', 'ui', 'content.%s.js' % lang), 'w', encoding='utf-8', newline='\n').write('/* Nội dung track UI (%s). SINH TỰ ĐỘNG từ dev/gen/ui_content.py. */\nADE.addTrackStrings(\'ui\', \'%s\', {\n%s\n});\n' % (lang, lang, body))
print(len(E), 'keys')
