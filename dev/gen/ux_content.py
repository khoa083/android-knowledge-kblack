# Sinh tracks/ux/content.vi.js và content.en.js từ MỘT nguồn. Chạy: python dev/gen/ux_content.py
import json, os, unicodedata
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = 'track.ux.'
E = []
def a(k, vi, en): E.append((P + k, vi, en))
def m(model, k, vi, en): a('m.' + model + '.' + k, vi, en)
def lab(k, vi, en): a('lab.' + k, vi, en)
def common(model, title, overview, wrapup, simp, hint, dt, dd):
    for k, v in (('title', title), ('overview', overview), ('wrapup', wrapup), ('simp.1', simp), ('ctl.hint', hint), ('diagramTitle', dt), ('diagramDesc', dd)): m(model, k, *v)
def choice(model, items, guesses, item_label, guess_label, src=None, try_=None):
    m(model, 'ctl.item', *item_label); m(model, 'ctl.guess', *guess_label)
    for g, gv, ge in guesses: m(model, 'ctl.guess.' + g, gv, ge)
    for iid, tv, te, sv, se, wv, we in items:
        m(model, 'ctl.item.' + iid, tv, te); m(model, 'i.' + iid + '.title', tv, te); m(model, 'i.' + iid + '.situation', sv, se); m(model, 'i.' + iid + '.why', wv, we)
    m(model, 'ev.why', 'giải thích', 'explanation')
    m(model, 'co.try', *(try_ or ('Đổi tình huống hoặc câu trả lời của bạn rồi đi lại các bước.', 'Change the situation or your answer, then walk the steps again.')))
    if src: m(model, 'co.source', *src)

# ---------- chung ----------
a('title', 'Thiết kế cho cách con người nghĩ', 'Designing for How People Think')
a('summary', 'Con người nhìn, nhớ, hành động, mắc lỗi và quyết định thế nào — và cách nghiên cứu, đo lường, viết chữ để sản phẩm Android hợp với họ.', 'How people see, remember, act, err and decide — and how to research, measure and write so Android products fit them.')
for k, vi, en in [('stages', 'UX · bảy giai đoạn hành động', 'UX · the seven stages of action'), ('errors', 'UX · phòng thí nghiệm lỗi', 'UX · error lab'), ('heuristic', 'UX · workbench đánh giá heuristic', 'UX · heuristic evaluation workbench'),
                  ('curve', 'UX · đường cong phát hiện vấn đề', 'UX · problem discovery curve'), ('sus', 'UX · máy tính SUS', 'UX · SUS calculator'), ('microcopy', 'UX · biên tập microcopy', 'UX · microcopy editor')]:
    a('preset.' + k, vi, en)
a('col.subject', 'Đối tượng', 'Actor')
for k, vi, en in [('c.right', 'Câu trả lời của bạn khớp', 'Your answer matches'), ('c.wrong', 'Câu trả lời của bạn chưa khớp', 'Your answer does not match'), ('c.why', 'Vì sao', 'Why'),
                  ('c.yours', 'Bạn chọn', 'You chose'), ('c.expected', 'Đáp án tham khảo', 'Reference answer'), ('c.metRight', 'Khớp đáp án', 'Matches the answer'),
                  ('st.broken', 'lỗi thiết kế', 'design flaw'), ('st.ok', 'ổn', 'fine'), ('st.open', 'thông', 'open'), ('st.blocked', 'nghẽn', 'blocked'),
                  ('n.screen', 'Màn hình (Hẹn Khám)', 'Screen (ClinicBook)'), ('n.user', 'Người dùng', 'User'), ('n.design', 'Thiết kế', 'Design')]:
    a(k, vi, en)

# ---------- D0 classify ----------
M = 'classify'
common(M, ('UX hay UI?', 'UX or UI?'), ('Tám tình huống của Hẹn Khám. Chọn tình huống, đoán đó là vấn đề UX, UI hay cả hai, rồi xem giải thích.', 'Eight ClinicBook situations. Pick one, guess whether it is a UX problem, a UI problem or both, then read the explanation.'),
       ('UI là bề mặt tương tác; UX là toàn bộ trải nghiệm, kể cả dịch vụ phía sau; usability là thuộc tính đo được của UI.', 'UI is the interaction surface; UX is the whole experience, including the service behind it; usability is a measurable attribute of the UI.'),
       ('Phân loại là để tập nhìn; nhiều vấn đề thật nằm ở cả hai.', 'The classification is practice in seeing; many real problems sit in both.'), ('Chọn tình huống và câu trả lời.', 'Pick a situation and an answer.'),
       ('Tình huống, người dùng, thiết kế', 'Situation, user, design'), ('Màn hình, người dùng và quyết định thiết kế.', 'The screen, the user and the design decision.'))
choice(M, [
 ('c1', 'Phòng khám không nhận lịch đã đặt', 'The clinic never gets the booking', 'Đặt lịch thành công trên app nhưng tới nơi thì phòng khám không có tên.', 'Booking succeeds in the app, but at the clinic there is no record.', 'Giao diện có thể hoàn hảo; vấn đề nằm ở dịch vụ phía sau. Đó là UX, không phải UI.', 'The interface may be perfect; the problem is the service behind it. That is UX, not UI.'),
 ('c2', 'Chữ trên nút "Tiếp" quá nhỏ', 'The "Next" label is too small', 'Nút "Tiếp" ở màn Chọn giờ dùng chữ 10 px, khó đọc.', 'The "Next" button on Choose a time uses 10 px text that is hard to read.', 'Đây là vấn đề của bề mặt giao diện (kích thước chữ).', 'This is a problem of the interface surface (text size).'),
 ('c3', 'Không biết bấm đâu để đổi giờ', 'No idea where to change the time', 'Người dùng muốn đổi giờ hẹn nhưng chữ "Sửa" trông như chữ thường.', 'The user wants to change the time but "Edit" looks like plain text.', 'Signifier yếu là vấn đề UI, và nó làm người dùng bỏ cuộc: ảnh hưởng tới trải nghiệm.', 'A weak signifier is a UI problem, and it makes people give up: it affects the experience.'),
 ('c4', 'Nhắc lịch tới quá muộn', 'The reminder arrives too late', 'Tin nhắc lịch tới 10 phút trước giờ hẹn, không kịp đi.', 'The reminder arrives 10 minutes before the appointment, too late to travel.', 'Thời điểm nhắc là quyết định về dịch vụ và hành trình người dùng.', 'Reminder timing is a decision about the service and the user journey.'),
 ('c5', 'Màu nút chính và phụ giống nhau', 'Primary and secondary buttons look alike', '"Xác nhận" và "Hủy" cùng màu, cùng kiểu.', '"Confirm" and "Cancel" share the same colour and style.', 'Phân cấp thị giác là việc của UI.', 'Visual hierarchy is a UI matter.'),
 ('c6', 'Phải nhập lại số điện thoại mỗi lần', 'Re-entering the phone number every time', 'Mỗi lần đặt lịch đều phải gõ lại số điện thoại.', 'Every booking asks for the phone number again.', 'Vừa là luồng (không nhớ dữ liệu) vừa là màn hình (ô nhập không tự điền).', 'It is both the flow (data not remembered) and the screen (the field is not prefilled).'),
 ('c7', 'Không thể đặt lịch cho người nhà', 'Cannot book for a family member', 'App chỉ cho đặt lịch cho chính chủ tài khoản.', 'The app only lets the account owner book for themselves.', 'Thiếu nhu cầu trong mô hình dịch vụ: UX.', 'A need missing from the service model: UX.'),
 ('c8', 'Icon điều hướng không có nhãn', 'Navigation icons without labels', 'Thanh điều hướng chỉ có icon.', 'The navigation bar has icons only.', 'Vấn đề hiển thị trên giao diện.', 'A display problem on the interface.')],
 [('ux', 'Vấn đề UX', 'A UX problem'), ('ui', 'Vấn đề UI', 'A UI problem'), ('both', 'Cả hai', 'Both')], ('Tình huống', 'Situation'), ('Bạn nghĩ đây là', 'You think this is'),
 ('UX bao trùm mọi tương tác với công ty, dịch vụ và sản phẩm; UI là một phần quan trọng của nó. [[src:nn-ux-def]] [[badge:research]]', 'UX covers every interaction with the company, its services and products; the UI is an important part of it. [[src:nn-ux-def]] [[badge:research]]'))

# ---------- D0 diamond ----------
M = 'diamond'
common(M, ('Double Diamond', 'The Double Diamond'), ('Bốn pha của Double Diamond (Design Council). Chọn pha; bật "vòng lặp" để thấy quy trình quay lại.', 'The four phases of the Double Diamond (Design Council). Pick a phase; turn on "loop" to see the process go back.'),
       ('Hai viên kim cương mở rộng rồi thu hẹp hai lần: hiểu vấn đề, rồi tìm giải pháp. Quy trình là lời mời, không phải sổ tay, và thường quay lại đầu.', 'Two diamonds widen and narrow twice: understand the problem, then find a solution. A process is an invitation, not a manual, and often returns to the start.'),
       ('Mỗi pha chỉ nêu câu hỏi, phương pháp và đầu ra tiêu biểu.', 'Each phase lists only a typical question, methods and output.'), ('Chọn pha hoặc bật vòng lặp.', 'Pick a phase or turn on the loop.'),
       ('Bốn pha', 'Four phases'), ('Discover, Define, Develop, Deliver và mũi tên quay lại.', 'Discover, Define, Develop, Deliver and an arrow going back.'))
m(M, 'ctl.phase', 'Pha', 'Phase'); m(M, 'ctl.loop', 'Vòng lặp', 'Loop')
for p, tv, te, qv, qe, mv, me, ov, oe in [
 ('discover', 'Discover', 'Discover', 'Vấn đề thật là gì với người đặt lịch khám?', 'What is the real problem for people booking appointments?', 'Nói chuyện và dành thời gian với người bị ảnh hưởng thay vì giả định: phỏng vấn, quan sát.', 'Talk to and spend time with the people affected instead of assuming: interviews, observation.', 'Hiểu biết về người dùng và bối cảnh.', 'Insight into users and context.'),
 ('define', 'Define', 'Define', 'Ta nên giải quyết vấn đề nào?', 'Which problem should we solve?', 'Tổng hợp phát hiện, đặt lại câu hỏi thiết kế.', 'Synthesise findings, reframe the design question.', 'Một phát biểu vấn đề rõ ràng.', 'A clear problem statement.'),
 ('develop', 'Develop', 'Develop', 'Có những cách giải nào?', 'What are the possible answers?', 'Tạo nhiều phương án, lấy cảm hứng bên ngoài, đồng thiết kế.', 'Generate many options, draw on outside inspiration, co-design.', 'Các phương án để thử.', 'Options to try.'),
 ('deliver', 'Deliver', 'Deliver', 'Phương án nào hiệu quả?', 'Which option works?', 'Thử ở quy mô nhỏ, bỏ cái không hiệu quả, cải tiến cái hiệu quả.', 'Test at small scale, drop what fails, improve what works.', 'Giải pháp đã được kiểm chứng ban đầu.', 'A solution with initial evidence.')]:
    m(M, 'ctl.phase.' + p, tv, te); m(M, 'ph.' + p + '.title', tv, te); m(M, 'ph.' + p + '.q', 'Câu hỏi chính: ' + qv, 'Key question: ' + qe); m(M, 'ph.' + p + '.methods', mv, me); m(M, 'ph.' + p + '.output', 'Đầu ra: ' + ov, 'Output: ' + oe)
m(M, 's.methods.title', 'Phương pháp', 'Methods'); m(M, 's.output.title', 'Đầu ra', 'Output'); m(M, 'ev.methods', 'phương pháp', 'methods'); m(M, 'ev.output', 'đầu ra', 'output')
m(M, 's.loop.title', 'Quay lại Discover', 'Back to Discover'); m(M, 's.loop.explain', 'Học được điều mới thì quay lại đầu: quy trình không tuyến tính.', 'Learning something new sends you back to the start: the process is not linear.'); m(M, 'ev.loop', 'quay lại', 'loop back')
m(M, 'co.source', 'Double Diamond là framework của Design Council. [[src:dc-diamond]] [[badge:author-framework]]', 'The Double Diamond is the Design Council\'s framework. [[src:dc-diamond]] [[badge:author-framework]]')

# ---------- D1 mental ----------
M = 'mental'
common(M, ('Mô hình tư duy: "Lưu tự động"', 'Mental model: "Auto-save"'), ('Màn Cài đặt có công tắc "Lưu tự động". Bạn dự đoán điều gì xảy ra với lịch đang soạn khi thoát màn hình?', 'Settings has an "Auto-save" switch. What do you predict happens to a draft booking when you leave the screen?'),
       ('Mô hình tư duy của người dùng có thể khác mô hình của hệ thống; chỗ lệch là nơi sinh ra lỗi và bất ngờ.', 'Users\' mental models can differ from the system\'s model; the gap is where errors and surprises come from.'),
       ('Hành vi "hệ thống" ở đây là giả định cho bài tập, không phải hành vi của app có thật.', 'The "system" behaviour here is assumed for the exercise, not the behaviour of a real app.'), ('Chọn trạng thái công tắc và dự đoán.', 'Pick the switch state and a prediction.'),
       ('Người dùng và hệ thống', 'User and system'), ('Dự đoán của người dùng so với điều hệ thống làm.', 'The user\'s prediction compared with what the system does.'))
choice(M, [('on', 'Công tắc BẬT', 'Switch ON', 'Lưu tự động đang bật; bạn thoát màn hình Chọn giờ giữa chừng.', 'Auto-save is on; you leave Choose a time half-way.', 'Hệ thống giữ bản nháp lịch hẹn; lần sau mở lại ở đúng bước.', 'The system keeps the draft; next time it reopens at the same step.'),
           ('off', 'Công tắc TẮT', 'Switch OFF', 'Lưu tự động đang tắt; bạn thoát màn hình Chọn giờ giữa chừng.', 'Auto-save is off; you leave Choose a time half-way.', 'Hệ thống bỏ bản nháp mà không hỏi.', 'The system discards the draft without asking.')],
       [('saved', 'Bản nháp được giữ', 'The draft is kept'), ('lost', 'Bản nháp mất', 'The draft is lost'), ('asked', 'App sẽ hỏi trước', 'The app will ask first')], ('Trạng thái', 'State'), ('Bạn dự đoán', 'You predict'))
m(M, 's.gap.title', 'Chỗ lệch giữa hai mô hình', 'The gap between the two models'); m(M, 'ev.gap', 'so sánh mô hình', 'compare models')
for it in ('on', 'off'):
    for g in ('saved', 'lost', 'asked'):
        ok = (it == 'on' and g == 'saved') or (it == 'off' and g == 'lost')
        if ok: vi, en = 'Hai mô hình khớp ở tình huống này: không có bất ngờ.', 'Both models match here: no surprise.'
        elif g == 'asked': vi, en = 'Bạn chờ một câu hỏi xác nhận mà hệ thống không đưa ra. Gợi ý thiết kế: cho biết trạng thái lưu ngay trên màn hình.', 'You expect a confirmation the system never shows. Design hint: show the save state right on the screen.'
        else: vi, en = 'Mô hình của bạn ngược với hệ thống: đây là nơi người dùng mất dữ liệu hoặc bối rối. Gợi ý: nhãn công tắc nói rõ hệ quả.', 'Your model is the opposite of the system: this is where users lose data or get confused. Hint: make the switch label state the consequence.'
        m(M, 'gap.' + it + '.' + g, vi, en)

# ---------- D2 stages ----------
M = 'stages'
common(M, ('Bảy giai đoạn: đổi giờ hẹn', 'Seven stages: changing an appointment time'), ('Tác vụ "đổi giờ hẹn" đi qua bảy giai đoạn hành động. Bật các lỗi thiết kế để thấy vực nào bị mở rộng.', 'The "change the appointment time" task goes through seven stages of action. Turn on design flaws to see which gulf widens.'),
       ('Signifier giúp vượt vực thực thi (làm gì, ở đâu); feedback giúp vượt vực đánh giá (đã xảy ra gì).', 'Signifiers help cross the gulf of execution (what to do, where); feedback helps cross the gulf of evaluation (what happened).'),
       ('Bảy giai đoạn và hai vực là mô hình của Norman (The Design of Everyday Things), dùng làm khung đọc; độ rộng vực trong mô phỏng chỉ là đếm minh họa.', 'The seven stages and two gulfs are Norman\'s model (The Design of Everyday Things), used as a reading frame; the gulf width in the simulation is an illustrative count.'),
       ('Bật/tắt từng lỗi thiết kế.', 'Toggle each design flaw.'), ('Bảy giai đoạn hành động', 'Seven stages of action'), ('Bốn giai đoạn thực thi rồi ba giai đoạn đánh giá.', 'Four execution stages, then three evaluation stages.'))
m(M, 'ctl.noSignifier', 'Bỏ signifier của nút Sửa', 'Remove the Edit signifier'); m(M, 'ctl.noFeedback', 'Bỏ feedback sau khi lưu', 'Remove feedback after saving'); m(M, 'ctl.vague', 'Thông báo mơ hồ', 'Vague message')
for st, tv, te, xv, xe in [('goal', 'Mục tiêu', 'Goal', 'Lan muốn dời lịch khám sang buổi chiều.', 'Lan wants to move her appointment to the afternoon.'),
                           ('plan', 'Lập kế hoạch', 'Plan', 'Lan nghĩ: vào "Lịch của tôi", tìm chỗ sửa.', 'Lan thinks: open "My appointments", find where to edit.'),
                           ('specify', 'Xác định hành động', 'Specify', 'Cô thấy chữ "Sửa" có chevron, biết bấm vào đó.', 'She sees "Edit" with a chevron and knows to tap it.'),
                           ('perform', 'Thực hiện', 'Perform', 'Cô chọn 14:00 và bấm "Lưu giờ mới".', 'She picks 14:00 and taps "Save new time".'),
                           ('perceive', 'Cảm nhận', 'Perceive', 'Snackbar hiện "Đã dời sang 14:00" kèm "Hoàn tác".', 'A snackbar shows "Moved to 14:00" with "Undo".'),
                           ('interpret', 'Diễn giải', 'Interpret', 'Cô hiểu lịch đã đổi thành công.', 'She understands the change succeeded.'),
                           ('compare', 'So sánh', 'Compare', 'Kết quả khớp mục tiêu: xong.', 'The result matches the goal: done.')]:
    m(M, 's.' + st + '.title', tv, te); m(M, 's.' + st + '.explain', xv, xe)
for k, vi, en in [('plan.broken.noSignifier', '"Sửa" trông như chữ thường: Lan không biết nên bắt đầu ở đâu.', '"Edit" looks like plain text: Lan does not know where to start.'),
                  ('specify.broken.noSignifier', 'Không có dấu hiệu bấm được: cô thử chạm thẻ, nhấn giữ, vuốt.', 'No sign that it is tappable: she tries tapping the card, long-pressing, swiping.'),
                  ('perceive.broken.noFeedback', 'Bấm lưu xong màn hình không đổi gì.', 'After tapping save, nothing on the screen changes.'),
                  ('interpret.broken.noFeedback', 'Không có tín hiệu nên cô không biết đã lưu chưa, bấm thêm lần nữa.', 'With no signal she cannot tell whether it saved, so she taps again.'),
                  ('interpret.broken.vague', 'Thông báo "Đã xử lý" không nói xử lý gì.', 'The message "Processed" does not say what was processed.'),
                  ('compare.broken.vague', 'Cô phải mở lại lịch để kiểm tra giờ mới.', 'She has to reopen the appointment to check the new time.')]:
    m(M, 's.' + k, vi, en)
m(M, 'ev.ok', 'ổn', 'fine'); m(M, 'ev.broken', 'vực bị mở rộng', 'gulf widens')
m(M, 'co.noSignifier', 'Vực thực thi mở rộng: người dùng không thấy cách làm. [[src:nn-heuristics]]', 'The gulf of execution widens: users cannot see how to act. [[src:nn-heuristics]]')
m(M, 'co.noFeedback', 'Vực đánh giá mở rộng: vi phạm heuristic #1 "Hiển thị trạng thái hệ thống". [[src:nn-heuristics]]', 'The gulf of evaluation widens: it breaks heuristic #1 "Visibility of system status". [[src:nn-heuristics]]')
m(M, 'co.vague', 'Thông báo cần nói chính xác điều đã xảy ra. [[src:nn-errmsg]]', 'Messages need to say precisely what happened. [[src:nn-errmsg]]')
m(M, 'co.try', 'Bật "Bỏ feedback sau khi lưu" rồi xem các bước cảm nhận và diễn giải. Trong Compose, nút cần `Role.Button` và nhãn semantics (cầu nối X6).', 'Turn on "Remove feedback after saving" and look at the perceive and interpret steps. In Compose, a button needs `Role.Button` and a semantics label (bridge X6).')
m(M, 'met.exec', 'Vực thực thi (minh họa)', 'Gulf of execution (illustrative)'); m(M, 'met.eval', 'Vực đánh giá (minh họa)', 'Gulf of evaluation (illustrative)')

# ---------- D3 errors ----------
M = 'errors'
common(M, ('Phòng thí nghiệm lỗi', 'Error lab'), ('Sáu tình huống lỗi ở Hẹn Khám. Phân loại slip hay mistake, chọn một biện pháp, xem số lỗi trước và sau trong mô hình minh họa.', 'Six error situations in ClinicBook. Classify slip or mistake, pick one remedy, and see errors before and after in an illustrative model.'),
       ('Slip cần constraint, định dạng dễ dãi, undo; mistake cần nhãn rõ, xem trước kết quả và khớp mô hình tư duy. Trước hết xem lại thiết kế, đừng trách người dùng.', 'Slips need constraints, forgiving formats and undo; mistakes need clear labels, previews and matching mental models. Look at the design first; do not blame users.'),
       ('Số lỗi "trước 4, sau 1 hoặc 3" là con số minh họa của mô hình, không phải dữ liệu đo.', 'The "before 4, after 1 or 3" counts are illustrative model numbers, not measured data.'),
       ('Chọn tình huống, phân loại và biện pháp.', 'Pick a situation, a classification and a remedy.'), ('Tình huống lỗi', 'Error situation'), ('Màn hình, người dùng và thiết kế.', 'Screen, user and design.'))
choice(M, [
 ('e1', 'Bấm nhầm giờ', 'Tapping the wrong time', 'Hai nút 09:00 và 09:30 sát nhau; Lan định chọn 09:30 nhưng chạm vào 09:00.', 'The 09:00 and 09:30 buttons are close together; Lan means 09:30 but taps 09:00.', 'Ý định đúng, thao tác sai: slip.', 'Right intention, wrong action: a slip.'),
 ('e2', '"Hủy" là hủy gì?', 'What does "Cancel" cancel?', 'Ở màn Xác nhận, Lan bấm "Hủy" để quay lại, nhưng app hủy luôn lịch hẹn.', 'On Confirm, Lan taps "Cancel" to go back, but the app cancels the appointment.', 'Kế hoạch dựa trên hiểu sai nhãn: mistake.', 'The plan rests on misreading the label: a mistake.'),
 ('e3', 'Số điện thoại sai định dạng', 'Phone number in the "wrong" format', 'Lan gõ "0901-234-567" và bị báo lỗi vì có dấu gạch.', 'Lan types "0901-234-567" and gets an error because of the dashes.', 'Định nhập đúng số, chỉ khác định dạng: slip (và lỗi của form quá khắt khe).', 'She meant the right number, only the format differs: a slip (and an overly strict form).'),
 ('e4', 'Chọn nhầm dịch vụ', 'Picking the wrong service', '"Khám tổng quát" và "Khám sức khỏe" nghe như nhau; Lan chọn sai loại.', '"General check-up" and "Health screening" sound alike; Lan picks the wrong one.', 'Mục tiêu sai do mô hình tư duy lệch: mistake.', 'The wrong goal from a mismatched mental model: a mistake.'),
 ('e5', 'Xóa nhầm lịch', 'Deleting the wrong appointment', 'Vuốt để xóa trên danh sách; ngón tay trượt sang thẻ bên cạnh.', 'Swipe-to-delete on the list; the finger slides onto the next card.', 'Ý định đúng, thao tác trượt: slip.', 'Right intention, the action slips: a slip.'),
 ('e6', 'Tưởng đã đặt xong', 'Thinking the booking is done', 'Lan dừng ở màn Chọn giờ vì tưởng chọn giờ là xong, chưa bấm Xác nhận.', 'Lan stops at Choose a time, thinking picking a time finished the booking.', 'Hiểu sai luồng: mistake.', 'Misunderstanding the flow: a mistake.')],
 [('slip', 'Slip', 'Slip'), ('mistake', 'Mistake', 'Mistake')], ('Tình huống', 'Situation'), ('Bạn phân loại là', 'You classify it as'),
 ('Slip và mistake theo NN/g; thiết kế chịu trách nhiệm trước. [[src:nn-slips]] [[src:nn-mistakes]] [[badge:research]]', 'Slips and mistakes per NN/g; the design is responsible first. [[src:nn-slips]] [[src:nn-mistakes]] [[badge:research]]'))
m(M, 'ctl.remedy', 'Biện pháp', 'Remedy')
for k, vi, en in [('constraint', 'thêm khoảng cách / constraint', 'spacing / a constraint'), ('confirm', 'xác nhận có trọng tâm', 'a focused confirmation'), ('forgiving', 'định dạng dễ dãi', 'a forgiving format'),
                  ('plainLabel', 'nhãn rõ nghĩa', 'a clear label'), ('preview', 'xem trước kết quả', 'a preview of the result'), ('undo', 'hoàn tác (Snackbar "Hoàn tác")', 'undo (a Snackbar with "Undo")')]:
    m(M, 'ctl.remedy.' + k, vi, en)
for e, gv, ge, wv, we in [
 ('e1', 'Khoảng cách và vùng chạm lớn hơn làm khó bấm nhầm; xác nhận giờ đã chọn giúp phát hiện sớm.', 'More spacing and larger touch targets make mis-taps harder; confirming the chosen time catches it early.', 'Biện pháp này không chặn được cú chạm trượt.', 'This remedy does not stop the slipped tap.'),
 ('e2', 'Nhãn "Quay lại" và "Hủy lịch hẹn" tách bạch xóa chỗ mơ hồ.', 'Separate labels "Back" and "Cancel appointment" remove the ambiguity.', 'Gốc vấn đề là nhãn mơ hồ; biện pháp này không sửa nó.', 'The root is the vague label; this remedy does not fix it.'),
 ('e3', 'Chấp nhận mọi định dạng rồi tự chuẩn hóa; `TextField(isError = …, supportingText = …)` chỉ dùng khi thật sự sai.', 'Accept any format and normalise it; use `TextField(isError = …, supportingText = …)` only when it is truly wrong.', 'Người dùng vẫn bị chặn vì dấu gạch.', 'The user is still blocked by the dashes.'),
 ('e4', 'Mô tả ngắn và xem trước nội dung dịch vụ giúp chọn đúng.', 'A short description and a preview of each service help pick correctly.', 'Không giúp người dùng phân biệt hai dịch vụ.', 'It does not help users tell the two services apart.'),
 ('e5', 'Snackbar có "Hoàn tác" cho phép sửa ngay sau khi lỡ tay.', 'A Snackbar with "Undo" lets users fix a slip right away.', 'Lỗi vẫn xảy ra và khó khôi phục.', 'The error still happens and is hard to recover from.'),
 ('e6', 'Xem trước "Lịch chưa được đặt — bấm Xác nhận để hoàn tất" làm rõ trạng thái.', 'A preview "Not booked yet — tap Confirm to finish" makes the state clear.', 'Không nói cho người dùng biết họ chưa xong.', 'It does not tell users they are not done.')]:
    m(M, 'i.' + e + '.r.good', gv + ' Số lỗi (minh họa): {before} → {after}.', ge + ' Errors (illustrative): {before} → {after}.')
    m(M, 'i.' + e + '.r.weak', wv + ' Số lỗi (minh họa): {before} → {after}.', we + ' Errors (illustrative): {before} → {after}.')
m(M, 's.remedy.title', 'Áp dụng biện pháp', 'Applying the remedy'); m(M, 'st.errors', 'Lỗi trên 10 lần thử (minh họa)', 'Errors per 10 tries (illustrative)')
m(M, 'co.illustrative', 'Con số chỉ để so sánh trong mô hình, không phải dữ liệu nghiên cứu. [[badge:simplified]]', 'The numbers only compare within the model; they are not research data. [[badge:simplified]]')
m(M, 'met.before', 'Lỗi trước', 'Errors before'); m(M, 'met.after', 'Lỗi sau', 'Errors after')

# ---------- D5 create ----------
M = 'create'
common(M, ('Phễu CREATE: bật nhắc lịch hẹn', 'The CREATE funnel: turning on reminders'), ('Hành động mục tiêu: người dùng bật "Nhắc lịch hẹn". Bật các can thiệp để gỡ điểm nghẽn ở từng giai đoạn.', 'Target action: users turn on "Appointment reminders". Turn on interventions to clear the bottleneck at each stage.'),
       ('Trong mô hình này, hành động chỉ xảy ra khi cả năm giai đoạn thông; can thiệp nên minh bạch và vì lợi ích người dùng.', 'In this model, the action happens only when all five stages are open; interventions should be transparent and in the user\'s interest.'),
       ('Mô hình minh họa, không có số liệu thật: mỗi giai đoạn chỉ là "thông" hoặc "nghẽn".', 'An illustrative model with no real data: each stage is only "open" or "blocked".'), ('Bật/tắt can thiệp.', 'Toggle interventions.'),
       ('Năm giai đoạn CREATE', 'The five CREATE stages'), ('Cue, Reaction, Evaluation, Ability, Timing.', 'Cue, Reaction, Evaluation, Ability, Timing.'))
for k, vi, en in [('cueAction', 'Gợi ý xuất hiện ở màn Xác nhận', 'A prompt on the Confirm screen'), ('reassure', 'Nói rõ không gửi quảng cáo', 'Say clearly there are no ads'), ('benefit', 'Giải thích lợi ích', 'Explain the benefit'),
                  ('fewerSteps', 'Bật bằng một chạm', 'Turn on with one tap'), ('timely', 'Hỏi ngay sau khi đặt lịch', 'Ask right after booking')]:
    m(M, 'ctl.' + k, vi, en)
m(M, 's.target.title', 'Hành động mục tiêu', 'Target action'); m(M, 's.target.explain', 'Bật "Nhắc lịch hẹn" trong Hẹn Khám.', 'Turn on "Appointment reminders" in ClinicBook.'); m(M, 'ev.target', 'hành động mục tiêu', 'target action')
m(M, 'co.noData', 'CREATE là framework của Stephen Wendel (Designing for Behavior Change). Phễu ở đây là khái niệm, không có số liệu thật. [[badge:author-framework]]', 'CREATE is Stephen Wendel\'s framework (Designing for Behavior Change). The funnel here is conceptual, with no real data. [[badge:author-framework]]')
for st, tv, te, ov, oe, bv, be in [
 ('cue', 'Cue', 'Cue', 'Người dùng thấy gợi ý đúng chỗ.', 'Users see the prompt in the right place.', 'Không có gì nhắc người dùng nghĩ tới tính năng.', 'Nothing makes users think of the feature.'),
 ('reaction', 'Reaction', 'Reaction', 'Phản ứng đầu tiên là tin tưởng.', 'The first reaction is trust.', 'Người dùng nghi đây là quảng cáo.', 'Users suspect it is advertising.'),
 ('evaluation', 'Evaluation', 'Evaluation', 'Người dùng thấy lợi ích rõ: không quên lịch.', 'Users see a clear benefit: not forgetting the appointment.', 'Không rõ được gì, nên bỏ qua.', 'The benefit is unclear, so they skip it.'),
 ('ability', 'Ability', 'Ability', 'Một chạm là xong.', 'One tap and it is done.', 'Phải vào Cài đặt qua ba màn.', 'It takes three screens through Settings.'),
 ('timing', 'Timing', 'Timing', 'Hỏi lúc người dùng vừa đặt lịch, khi nhu cầu rõ nhất.', 'Asked right after booking, when the need is clearest.', 'Hỏi lúc mở app lần đầu, khi chưa có lịch nào.', 'Asked on first launch, before any booking exists.')]:
    m(M, 's.' + st + '.title', tv, te); m(M, 's.' + st + '.open', ov, oe); m(M, 's.' + st + '.blocked', bv, be)
m(M, 'ev.open', 'thông', 'open'); m(M, 'ev.blocked', 'nghẽn', 'blocked'); m(M, 'met.open', 'Giai đoạn thông', 'Open stages')

# ---------- D5 deceptive ----------
M = 'deceptive'
common(M, ('Nhận diện deceptive pattern', 'Recognising deceptive patterns'), ('Sáu màn mẫu có deceptive pattern. Gắn nhãn loại pattern, xem tác hại và cách làm trung thực.', 'Six sample screens with deceptive patterns. Label the pattern type, see the harm and the honest alternative.'),
       ('Deceptive pattern đẩy người dùng tới lựa chọn có lợi cho công ty bằng cách lừa, đánh lạc hướng hoặc cản trở. Học để nhận diện và tránh.', 'Deceptive patterns push users towards choices that benefit the company by deceiving, misdirecting or obstructing. Learn them to recognise and avoid them.'),
       ('Mỗi màn chỉ có một pattern chính; màn thật có thể chồng nhiều pattern.', 'Each screen has one main pattern; real screens can stack several.'), ('Chọn màn và loại pattern.', 'Pick a screen and a pattern type.'),
       ('Màn mẫu', 'Sample screen'), ('Màn hình, người dùng và thiết kế.', 'Screen, user and design.'))
choice(M, [
 ('p1', 'Ô tick sẵn', 'Pre-ticked box', 'Màn Xác nhận có ô "Nhận tin khuyến mãi" đã tick sẵn, chữ xám nhỏ.', 'Confirm has a pre-ticked "Send me promotions" box in small grey text.', 'Lựa chọn được làm sẵn và giấu đi: sneaking/preselection.', 'The choice is pre-made and hidden: sneaking/preselection.'),
 ('p2', 'Nút từ chối làm người dùng xấu hổ', 'A shaming decline button', 'Hộp thoại nhắc lịch có nút "Không, tôi thích lỡ hẹn".', 'The reminder dialog has a "No, I like missing appointments" button.', 'Dùng cảm giác xấu hổ để ép đồng ý: confirmshaming.', 'Using shame to force agreement: confirmshaming.'),
 ('p3', 'Đồng hồ đếm ngược giả', 'Fake countdown', '"Giờ này chỉ giữ trong 02:00!" dù lịch không hề bị giữ.', '"This slot is held for 02:00 only!" although nothing is held.', 'Tạo khẩn cấp giả: false urgency (một dạng lừa bằng chữ/hình).', 'Fake urgency: false urgency (a kind of visual/wording trick).'),
 ('p4', 'Hủy lịch nhiều bước', 'Multi-step cancellation', 'Đặt lịch một chạm, nhưng hủy phải qua năm màn và gọi điện.', 'Booking takes one tap, but cancelling takes five screens and a phone call.', 'Cản trở lựa chọn ít lợi nhuận: obstruction.', 'Obstructing the less profitable choice: obstruction.'),
 ('p5', 'Nút từ chối bị làm mờ', 'Faded decline button', '"Bỏ qua" màu xám nhạt cạnh "Đồng ý" nổi bật.', '"Skip" in faint grey next to a bold "Agree".', 'Đánh lạc hướng bằng hình thức: visual trick.', 'Misdirection through visuals: a visual trick.'),
 ('p6', 'Hỏi đi hỏi lại', 'Asking again and again', 'Mỗi lần mở app đều hiện hộp thoại bật thông báo, không có "Đừng hỏi nữa".', 'Every launch shows the notifications dialog, with no "Don\'t ask again".', 'Làm phiền tới khi người dùng đồng ý: nagging.', 'Pestering until users agree: nagging.')],
 [('sneaking', 'Sneaking / preselection', 'Sneaking / preselection'), ('confirmshaming', 'Confirmshaming', 'Confirmshaming'), ('falseUrgency', 'Khẩn cấp giả', 'False urgency'),
  ('obstruction', 'Obstruction', 'Obstruction'), ('visualTrick', 'Mẹo hình thức', 'Visual trick'), ('nagging', 'Nagging', 'Nagging')], ('Màn mẫu', 'Sample screen'), ('Loại pattern', 'Pattern type'),
 ('Định nghĩa và các loại theo NN/g; thuật ngữ do Harry Brignull đặt (2010). [[src:nn-deceptive]] [[badge:research]]', 'Definition and types per NN/g; the term was coined by Harry Brignull (2010). [[src:nn-deceptive]] [[badge:research]]'))
for p, vi, en in [('p1', 'Để ô trống, chữ rõ ràng; hỏi khi người dùng có lý do.', 'Leave the box unticked, in clear text; ask when users have a reason.'), ('p2', 'Hai lựa chọn trung tính: "Bật nhắc" / "Không, cảm ơn".', 'Two neutral options: "Turn on" / "No thanks".'),
               ('p3', 'Chỉ báo hạn chót khi có thật, nói rõ điều gì xảy ra khi hết giờ.', 'Show a deadline only when it is real, and say what happens when it ends.'), ('p4', 'Hủy dễ như đặt: một màn xác nhận có trọng tâm.', 'Make cancelling as easy as booking: one focused confirmation.'),
               ('p5', 'Hai nút cùng mức dễ thấy; nhấn mạnh hành động an toàn hơn.', 'Make both buttons equally visible; emphasise the safer action.'), ('p6', 'Hỏi một lần, nhớ câu trả lời, cho đổi trong Cài đặt.', 'Ask once, remember the answer, allow changes in Settings.')]:
    m(M, 'i.' + p + '.honest', vi, en)
m(M, 's.honest.title', 'Cách làm trung thực', 'The honest alternative'); m(M, 'ev.honest', 'thiết kế lại', 'redesign')
m(M, 'co.ethics', 'Site chỉ trình bày để nhận diện và tránh, không hướng dẫn áp dụng.', 'The site presents these only to recognise and avoid them, not as instructions.')

# ---------- D6 methods ----------
M = 'methods'
common(M, ('Chọn phương pháp nghiên cứu', 'Choosing a research method'), ('Sáu câu hỏi nghiên cứu về Hẹn Khám. Chọn phương pháp bạn nghĩ hợp nhất, rồi xem nó nằm ở đâu trên các trục.', 'Six research questions about ClinicBook. Pick the method you think fits best, then see where it sits on the axes.'),
       ('Chọn phương pháp theo câu hỏi: thái độ hay hành vi, định tính hay định lượng, bối cảnh sử dụng.', 'Choose the method by the question: attitudes or behaviour, qualitative or quantitative, context of use.'),
       ('Mỗi câu hỏi có một vài phương án hợp lý; đáp án tham khảo không loại trừ cách khác.', 'Each question has a few reasonable options; the reference answer does not rule out others.'), ('Chọn câu hỏi và phương pháp.', 'Pick a question and a method.'),
       ('Câu hỏi và phương pháp', 'Question and method'), ('Màn hình, người dùng và quyết định nghiên cứu.', 'Screen, user and research decision.'))
choice(M, [
 ('q1', 'Vì sao người dùng bỏ ở bước chọn giờ?', 'Why do users drop off at Choose a time?', 'Câu hỏi "vì sao" về hành vi trong bối cảnh thật.', 'A "why" question about behaviour in real context.', 'Cần quan sát và hỏi trong bối cảnh: field study hoặc phỏng vấn kết hợp quan sát.', 'It needs observation and questions in context: a field study or interviews with observation.'),
 ('q2', 'Bao nhiêu % hoàn tất đặt lịch?', 'What % complete a booking?', 'Câu hỏi "bao nhiêu" về hành vi thật.', 'A "how many" question about real behaviour.', 'Analytics đo hành vi tự nhiên với số lượng lớn.', 'Analytics measures natural behaviour at scale.'),
 ('q3', 'Người dùng có tìm được nút đổi giờ?', 'Can users find the change-time button?', 'Câu hỏi về khả năng làm một tác vụ cụ thể.', 'A question about completing a specific task.', 'Usability test cho thấy người dùng làm được hay không và vấp ở đâu.', 'A usability test shows whether users can do it and where they stumble.'),
 ('q4', 'Người dùng đánh giá thế nào về độ dễ dùng?', 'How do users rate ease of use?', 'Câu hỏi về thái độ, cần con số.', 'An attitude question that needs numbers.', 'Khảo sát (ví dụ SUS) đo thái độ tự báo cáo.', 'A survey (for example SUS) measures self-reported attitudes.'),
 ('q5', 'Người dùng nhóm các dịch vụ thế nào?', 'How do users group the services?', 'Câu hỏi về mô hình tư duy khi phân loại.', 'A question about mental models when categorising.', 'Card sorting cho thấy cách người dùng nhóm nội dung.', 'Card sorting shows how users group content.'),
 ('q6', 'Đặt lịch khám diễn ra thế nào trong đời sống gia đình?', 'How does booking fit into family life?', 'Câu hỏi khám phá về nhu cầu và bối cảnh.', 'An exploratory question about needs and context.', 'Phỏng vấn sâu hoặc contextual inquiry.', 'In-depth interviews or contextual inquiry.')],
 [('interview', 'Phỏng vấn', 'Interviews'), ('fieldStudy', 'Field study / contextual inquiry', 'Field study / contextual inquiry'), ('usability', 'Usability test', 'Usability test'),
  ('survey', 'Khảo sát', 'Survey'), ('analytics', 'Analytics', 'Analytics'), ('cardSort', 'Card sorting', 'Card sorting')], ('Câu hỏi', 'Question'), ('Bạn chọn phương pháp', 'Your method'),
 ('Ba trục theo NN/g: thái độ↔hành vi, định tính↔định lượng, bối cảnh sử dụng. [[src:nn-methods]] [[badge:research]]', 'Three axes per NN/g: attitudinal↔behavioural, qualitative↔quantitative, context of use. [[src:nn-methods]] [[badge:research]]'))
for q, vi, en in [('q1', 'Hành vi · định tính · bối cảnh tự nhiên.', 'Behavioural · qualitative · natural context.'), ('q2', 'Hành vi · định lượng · bối cảnh tự nhiên.', 'Behavioural · quantitative · natural context.'),
                  ('q3', 'Gần hành vi · định tính · có kịch bản.', 'Leaning behavioural · qualitative · scripted.'), ('q4', 'Thái độ · định lượng.', 'Attitudinal · quantitative.'),
                  ('q5', 'Thái độ · có thể định tính hoặc định lượng · dùng hạn chế.', 'Attitudinal · qualitative or quantitative · limited use.'), ('q6', 'Thái độ và hành vi · định tính · bối cảnh tự nhiên.', 'Attitudes and behaviour · qualitative · natural context.')]:
    m(M, 'i.' + q + '.axes', 'Trên bản đồ: ' + vi, 'On the map: ' + en)
m(M, 's.axes.title', 'Vị trí trên các trục', 'Position on the axes'); m(M, 'ev.axes', 'xếp lên bản đồ', 'place on the map')

# ---------- D7 session ----------
M = 'session'
common(M, ('Phiên think-aloud (mô phỏng)', 'A think-aloud session (simulated)'), ('Một người tham gia hư cấu đặt lịch trên Hẹn Khám. Xem phiên qua ống kính "làm" hoặc "nói", và bật ghi chú vấn đề.', 'A fictional participant books on ClinicBook. View the session through the "do" or "say" lens, and turn on issue notes.'),
       ('Người tham gia nói một đằng, làm một nẻo: ghi lại cả hai, và ưu tiên điều họ làm khi phát hiện vấn đề.', 'Participants may say one thing and do another: record both, and give priority to what they do when spotting problems.'),
       ('Kịch bản tự soạn, người tham gia hư cấu; danh sách vấn đề tham chiếu có ba mục.', 'A self-written script with a fictional participant; the reference issue list has three items.'), ('Đổi ống kính hoặc bật ghi chú.', 'Change the lens or turn on notes.'),
       ('Phiên test', 'Test session'), ('Người tham gia, màn hình và người quan sát.', 'Participant, screen and observer.'))
m(M, 'ctl.lens', 'Ống kính', 'Lens'); m(M, 'ctl.lens.do', 'điều người tham gia làm', 'what the participant does'); m(M, 'ctl.lens.say', 'điều người tham gia nói', 'what the participant says'); m(M, 'ctl.notes', 'Ghi chú vấn đề', 'Note issues')
for l, tv, te, dv, de, sv, se in [
 ('l1', 'Mở app', 'Opening the app', 'Mở app, bấm "Đặt lịch mới" ngay.', 'Opens the app and taps "Book a new appointment" right away.', '"Ồ, dễ thấy đấy."', '"Oh, that\'s easy to spot."'),
 ('l2', 'Chọn giờ', 'Choosing a time', 'Lướt danh sách giờ hai lần, dừng 20 giây ở "Không còn chỗ".', 'Scrolls the time list twice, pauses 20 seconds on "No slots left".', '"Chắc không sao, tôi chọn đại."', '"Probably fine, I\'ll just pick one."'),
 ('l3', 'Chọn được giờ', 'Picks a time', 'Chọn 09:00.', 'Picks 09:00.', '"Được rồi."', '"Okay."'),
 ('l4', 'Nhập số điện thoại', 'Entering the phone number', 'Gõ số có dấu gạch, gặp "Lỗi 422", xóa đi gõ lại ba lần.', 'Types the number with dashes, gets "Error 422", deletes and retypes three times.', '"Hơi khó chịu nhưng ổn."', '"A bit annoying but fine."'),
 ('l5', 'Xác nhận', 'Confirming', 'Do dự giữa "OK" và "Hủy", bấm "OK" sau 8 giây.', 'Hesitates between "OK" and "Cancel", taps "OK" after 8 seconds.', '"Cũng rõ thôi."', '"It\'s clear enough."'),
 ('l6', 'Kết thúc', 'Wrapping up', 'Mở "Lịch của tôi" để kiểm tra lại.', 'Opens "My appointments" to double-check.', '"Tôi sẽ cho 8 điểm."', '"I\'d give it an 8."')]:
    m(M, 's.' + l + '.title', tv, te); m(M, 's.' + l + '.do', 'Làm: ' + dv, 'Does: ' + de); m(M, 's.' + l + '.say', 'Nói: ' + sv, 'Says: ' + se)
    m(M, 'ev.' + l + '.do', dv, de); m(M, 'ev.' + l + '.say', sv, se)
for k, vi, en in [('time', 'Vấn đề: màn Chọn giờ không gợi ý giờ khác khi hết chỗ.', 'Issue: Choose a time offers no alternative when slots are full.'), ('phone', 'Vấn đề: ô số điện thoại quá khắt khe và lỗi khó hiểu.', 'Issue: the phone field is too strict and its error is unclear.'),
                  ('cancel', 'Vấn đề: nhãn "OK"/"Hủy" mơ hồ ở màn Xác nhận.', 'Issue: vague "OK"/"Cancel" labels on Confirm.')]:
    m(M, 'note.' + k, vi, en)
m(M, 'met.issues', 'Vấn đề đã ghi', 'Issues noted')

# ---------- D9 tone ----------
M = 'tone'
common(M, ('Voice và tone', 'Voice and tone'), ('Chọn voice cho Hẹn Khám và một bối cảnh; xem cùng thông điệp "lịch hẹn" được viết thế nào.', 'Pick a voice for ClinicBook and a context; see how the same "appointment" message is written.'),
       ('Voice giữ nguyên cá tính; tone điều chỉnh theo bối cảnh và cảm xúc của người đọc.', 'Voice keeps the personality; tone adjusts to context and the reader\'s feelings.'),
       ('Hai voice và ba bối cảnh tự soạn; voice chart đầy đủ của Podmajersky có nhiều cột hơn.', 'Two voices and three contexts, self-written; Podmajersky\'s full voice chart has more columns.'), ('Chọn voice và bối cảnh.', 'Pick a voice and a context.'),
       ('Voice, thông điệp, người đọc', 'Voice, message, reader'), ('Thiết kế chọn voice; màn hình hiện thông điệp; người đọc phản ứng.', 'Design picks a voice; the screen shows the message; the reader responds.'))
m(M, 'ctl.voice', 'Voice', 'Voice'); m(M, 'ctl.voice.warm', 'ấm áp, rõ ràng, đáng tin', 'warm, clear, trustworthy'); m(M, 'ctl.voice.plain', 'trung tính, ngắn gọn, chính xác', 'neutral, concise, precise')
m(M, 'ctl.ctx', 'Bối cảnh', 'Context')
for c, vi, en in [('normal', 'bình thường', 'normal'), ('urgent', 'khẩn cấp', 'urgent'), ('error', 'lỗi', 'error')]: m(M, 'ctl.ctx.' + c, vi, en); m(M, 'ctx.' + c + '.title', 'Bối cảnh: ' + vi, 'Context: ' + en)
m(M, 's.voice.title', 'Voice đã chọn', 'The chosen voice'); m(M, 'voice.warm', 'Hẹn Khám nói như một lễ tân tận tâm: ấm áp nhưng không suồng sã.', 'ClinicBook speaks like a caring receptionist: warm but not overly casual.'); m(M, 'voice.plain', 'Hẹn Khám nói như một tấm biển chỉ dẫn tốt: ngắn, chính xác.', 'ClinicBook speaks like a good signpost: short and precise.'); m(M, 'ev.voice', 'chọn voice', 'pick a voice')
for v in ('warm', 'plain'):
    for c, vi, en in {'warm': [('normal', '"Hẹn bạn 9:00 sáng thứ Năm nhé. Chúng tôi sẽ nhắc trước một ngày."', '"See you Thursday at 9:00. We\'ll remind you a day before."'), ('urgent', '"Phòng khám đổi lịch: buổi hẹn 9:00 của bạn cần chọn giờ mới hôm nay."', '"The clinic changed its schedule: please pick a new time for your 9:00 visit today."'), ('error', '"Chưa lưu được lịch vì mất kết nối. Thông tin của bạn vẫn còn — thử lại nhé."', '"We couldn\'t save the booking because the connection dropped. Your details are still here — try again."')],
                      'plain': [('normal', '"Lịch hẹn: Thứ Năm 09:00. Nhắc trước 1 ngày."', '"Appointment: Thursday 09:00. Reminder 1 day before."'), ('urgent', '"Lịch 09:00 bị hủy bởi phòng khám. Chọn giờ mới."', '"Your 09:00 was cancelled by the clinic. Choose a new time."'), ('error', '"Chưa lưu: mất kết nối. Dữ liệu vẫn giữ. Thử lại."', '"Not saved: connection lost. Your data is kept. Try again."')]}[v]:
        m(M, 'msg.' + v + '.' + c, vi, en)
m(M, 's.why.title', 'Vì sao tone đổi', 'Why the tone changes')
for c, vi, en in [('normal', 'Bình thường: thông tin chính trước, giọng thân thiện vừa phải.', 'Normal: key information first, moderately friendly.'), ('urgent', 'Khẩn cấp: nói việc cần làm ngay, bớt trang trí.', 'Urgent: say what to do now, drop the decoration.'), ('error', 'Lỗi: nói chuyện gì xảy ra, dữ liệu có mất không, làm gì tiếp; không đổ lỗi.', 'Error: say what happened, whether data is lost and what to do next; no blame.')]:
    m(M, 'why.' + c, vi, en)
m(M, 'ev.why', 'điều chỉnh tone', 'adjust tone')
m(M, 'co.source', 'Bốn chiều của tone theo NN/g: trang trọng↔thân mật, nghiêm túc↔hài hước, tôn trọng↔bất kính, trung tính↔nhiệt tình. Voice chart là framework của Torrey Podmajersky. [[src:nn-tone]] [[badge:author-framework]]', 'NN/g\'s four tone dimensions: formal↔casual, serious↔funny, respectful↔irreverent, matter-of-fact↔enthusiastic. The voice chart is Torrey Podmajersky\'s framework. [[src:nn-tone]] [[badge:author-framework]]')

# ---------- D10 sprint ----------
M = 'sprint'
common(M, ('Kế hoạch design sprint', 'Planning a design sprint'), ('Hai biến thể sprint với cùng mục tiêu: cải thiện màn Chọn giờ. Thử bỏ pha test để thấy đầu ra nào bị thiếu.', 'Two sprint variants with the same goal: improving Choose a time. Try skipping the test phase to see which output goes missing.'),
       ('Sprint là công cụ, không phải nghi lễ: mỗi pha có đầu ra, và bỏ pha test là bỏ bằng chứng.', 'A sprint is a tool, not a ritual: each phase has an output, and skipping the test drops the evidence.'),
       ('Hai biến thể được rút gọn còn năm pha; mỗi nguồn có chi tiết riêng.', 'Both variants are shortened to five phases; each source has its own details.'), ('Chọn biến thể; bật/tắt bỏ pha test.', 'Pick a variant; toggle skipping the test.'),
       ('Năm pha', 'Five phases'), ('Các pha của sprint theo thứ tự.', 'The sprint phases in order.'))
m(M, 'ctl.variant', 'Biến thể', 'Variant'); m(M, 'ctl.variant.gv', 'GV (5 ngày)', 'GV (5 days)'); m(M, 'ctl.variant.banfield', 'Banfield và cộng sự', 'Banfield et al.'); m(M, 'ctl.skipTest', 'Bỏ pha test', 'Skip the test phase')
for i in range(5): m(M, 'n.p%d' % i, 'Pha %d' % (i + 1), 'Phase %d' % (i + 1))
for p, tv, te, xv, xe in [('mon', 'Thứ Hai: map', 'Monday: map', 'Vẽ bản đồ vấn đề, chọn mục tiêu dài hạn và điểm tập trung.', 'Map the problem, set a long-term goal and pick a target.'),
                          ('tue', 'Thứ Ba: sketch', 'Tuesday: sketch', 'Xem lại ý tưởng có sẵn, mỗi người phác giải pháp.', 'Review existing ideas; everyone sketches solutions.'),
                          ('wed', 'Thứ Tư: decide', 'Wednesday: decide', 'Phê bình, quyết định, viết storyboard.', 'Critique, decide and storyboard.'),
                          ('thu', 'Thứ Năm: prototype', 'Thursday: prototype', 'Dựng bản mẫu trông như thật.', 'Build a realistic-looking prototype.'),
                          ('fri', 'Thứ Sáu: test', 'Friday: test', 'Phỏng vấn khách hàng và quan sát họ dùng bản mẫu.', 'Interview customers and watch them use the prototype.'),
                          ('understand', 'Understand', 'Understand', 'Thống nhất hiểu biết về vấn đề và người dùng.', 'Build a shared understanding of the problem and users.'),
                          ('diverge', 'Diverge', 'Diverge', 'Tạo nhiều ý tưởng.', 'Generate many ideas.'),
                          ('converge', 'Converge', 'Converge', 'Chọn ý tưởng để làm.', 'Choose the ideas to build.'),
                          ('prototype', 'Prototype', 'Prototype', 'Dựng bản mẫu.', 'Build the prototype.'),
                          ('test', 'Test', 'Test', 'Kiểm tra với người dùng.', 'Test with users.')]:
    m(M, 's.' + p + '.title', tv, te); m(M, 's.' + p + '.explain', xv, xe); m(M, 'ev.' + p, tv, te)
m(M, 's.fri.skipped', 'Bỏ ngày test: nhóm có bản mẫu nhưng không có bằng chứng người dùng dùng được nó.', 'Skipping test day: the team has a prototype but no evidence that users can use it.')
m(M, 's.test.skipped', 'Bỏ pha test: không có bằng chứng từ người dùng.', 'Skipping the test phase: no evidence from users.')
m(M, 'sk.test', 'Kiểm tra với người dùng', 'Testing with users'); m(M, 'sk.why', 'pha bị bỏ trong kế hoạch', 'the phase was dropped from the plan')
m(M, 'co.gv', 'Năm ngày của GV: map, sketch, decide, prototype, test. [[src:gv-sprint]] [[badge:author-framework]]', 'GV\'s five days: map, sketch, decide, prototype, test. [[src:gv-sprint]] [[badge:author-framework]]')
m(M, 'co.banfield', 'Biến thể của Richard Banfield, C. Todd Lombardo và Trace Wax (sách Design Sprint): Understand, Diverge, Converge, Prototype, Test. [[badge:author-framework]]', 'The variant by Richard Banfield, C. Todd Lombardo and Trace Wax (the Design Sprint book): Understand, Diverge, Converge, Prototype, Test. [[badge:author-framework]]')

# ---------- D10 stakeholder ----------
M = 'stakeholder'
common(M, ('Phản hồi stakeholder', 'Responding to stakeholders'), ('Năm phản hồi giả định về Hẹn Khám. Chọn cách trả lời, rồi xem phân tích.', 'Five hypothetical pieces of feedback about ClinicBook. Pick how to respond, then read the analysis.'),
       ('Trả lời bằng mục tiêu, dữ liệu và giới hạn; đồng ý ngay hay bác bỏ ngay đều bỏ lỡ cuộc trao đổi.', 'Respond with goals, data and constraints; agreeing or rejecting immediately both skip the conversation.'),
       ('Ý tưởng lấy từ Tom Greever (Articulating Design Decisions), diễn đạt lại; phản hồi là giả định.', 'The idea comes from Tom Greever (Articulating Design Decisions), rephrased; the feedback is hypothetical.'), ('Chọn phản hồi và cách trả lời.', 'Pick the feedback and a response.'),
       ('Phản hồi và cách trả lời', 'Feedback and response'), ('Màn hình, stakeholder và thiết kế.', 'Screen, stakeholder and design.'))
choice(M, [
 ('f1', '"Làm logo to hơn."', '"Make the logo bigger."', 'Giám đốc muốn logo chiếm nửa màn Trang chủ.', 'The director wants the logo to fill half the Home screen.', 'Đưa về mục tiêu: người dùng mở app để xem lịch sắp tới; logo lớn đẩy thông tin đó xuống.', 'Go back to the goal: users open the app to see their next appointment; a big logo pushes it down.'),
 ('f2', '"Sao không làm giống app X?"', '"Why not copy app X?"', 'Một stakeholder muốn sao chép luồng của app khác.', 'A stakeholder wants to copy another app\'s flow.', 'Dùng dữ liệu: kết quả test của chính người dùng Hẹn Khám cho biết điều gì hiệu quả.', 'Use data: test results with ClinicBook\'s own users show what works.'),
 ('f3', '"Thêm 5 bước xác minh."', '"Add 5 verification steps."', 'Bộ phận pháp lý muốn thêm nhiều bước khi đặt lịch.', 'Legal wants many extra steps when booking.', 'Nêu giới hạn và đánh đổi: yêu cầu nào bắt buộc, yêu cầu nào có thể gộp.', 'State constraints and trade-offs: which requirements are mandatory and which can be merged.'),
 ('f4', '"Màu xanh này buồn quá."', '"This blue is too sad."', 'Ý kiến cá nhân về màu.', 'A personal opinion on colour.', 'Quay về mục tiêu thương hiệu và khả năng đọc (tương phản), không tranh cãi sở thích.', 'Return to brand goals and readability (contrast) rather than arguing about taste.'),
 ('f5', '"Người dùng không đọc đâu, bỏ hết chữ đi."', '"Users don\'t read, remove all text."', 'Một stakeholder muốn chỉ dùng icon.', 'A stakeholder wants icons only.', 'Dẫn dữ liệu về cách người dùng quét chữ và vấn đề icon không nhãn đã thấy trong test.', 'Cite data on how users scan text and the unlabeled-icon problem seen in testing.')],
 [('goal', 'Đưa về mục tiêu', 'Tie it to the goal'), ('data', 'Dẫn dữ liệu', 'Bring data'), ('constraint', 'Nêu giới hạn và đánh đổi', 'State constraints and trade-offs'), ('comply', 'Làm theo ngay', 'Just comply')],
 ('Phản hồi', 'Feedback'), ('Bạn trả lời bằng', 'You respond with'))

# ---------- lab ----------
lab('reset', 'Đặt lại', 'Reset'); lab('ms', '{n} ms', '{n} ms')
lab('recall.title', 'Nhận ra hay nhớ lại (đo của bạn)', 'Recognition or recall (yours)')
lab('recall.intro', 'Cùng tác vụ "chọn lại dịch vụ đã đặt lần trước" theo hai cách: (a) gõ lại tên, (b) chọn từ "Gần đây".', 'The same task "pick the service you booked last time" two ways: (a) type the name, (b) pick from "Recent".')
lab('recall.privacy', 'Minh họa cá nhân, không phải dữ liệu nghiên cứu: thời gian và số thao tác chỉ nằm trong bộ nhớ của trang này, không được lưu và không được gửi đi đâu.', 'Personal illustration, not research data: time and action counts stay only in this page\'s memory; they are not saved or sent anywhere.')
lab('recall.inputLabel', 'Tên dịch vụ', 'Service name'); lab('recall.placeholder', 'Gõ tên dịch vụ lần trước…', 'Type last time\'s service…')
lab('recall.answer', 'Khám tổng quát', 'General check-up'); lab('recall.recentChip', 'Gần đây: Khám tổng quát', 'Recent: General check-up')
lab('recall.task.a', 'Cách (a): gõ lại tên dịch vụ bạn đặt lần trước (gợi ý: khám tổng quát).', 'Way (a): type the service you booked last time (hint: general check-up).')
lab('recall.task.b', 'Cách (b): chọn từ "Gần đây".', 'Way (b): pick from "Recent".')
lab('recall.pick', 'Chọn một cách để bắt đầu; đồng hồ chạy từ thao tác đầu tiên.', 'Pick a way to start; the timer starts at your first action.')
lab('recall.startA', 'Bắt đầu cách (a)', 'Start way (a)'); lab('recall.startB', 'Bắt đầu cách (b)', 'Start way (b)')
lab('recall.col.task', 'Cách', 'Way'); lab('recall.col.time', 'Thời gian', 'Time'); lab('recall.col.actions', 'Thao tác', 'Actions'); lab('recall.row.a', '(a) nhớ lại', '(a) recall'); lab('recall.row.b', '(b) nhận ra', '(b) recognition')
lab('recall.note', 'Một lần đo của một người không chứng minh gì; nó chỉ giúp bạn cảm nhận khác biệt. Nhận ra dễ hơn nhớ lại vì có nhiều gợi ý truy xuất (NN/g).', 'One measurement of one person proves nothing; it only lets you feel the difference. Recognition is easier than recall because it offers more retrieval cues (NN/g).')
lab('heuristic.title', 'Workbench đánh giá heuristic', 'Heuristic evaluation workbench')
lab('heuristic.intro', 'Luồng Hẹn Khám có 12 vấn đề cài sẵn và vài mồi nhử. Chọn vùng nghi ngờ trên màn hình, gắn heuristic và severity, rồi bấm "Chấm".', 'The ClinicBook flow has 12 planted issues and a few decoys. Select a suspicious area on the screen, assign a heuristic and a severity, then press "Grade".')
lab('heuristic.screen', 'Màn hình', 'Screen'); lab('heuristic.pick', 'Chọn một vùng (khung có viền) trên màn hình bên trái.', 'Select an area (outlined) on the screen on the left.')
lab('heuristic.area', 'Vùng {id}', 'Area {id}'); lab('heuristic.isIssue', 'Đây là vấn đề', 'This is an issue'); lab('heuristic.heur', 'Heuristic', 'Heuristic'); lab('heuristic.sev', 'Severity', 'Severity')
lab('heuristic.grade', 'Chấm', 'Grade'); lab('heuristic.threeOn', 'Chế độ ba người đánh giá', 'Three-evaluator mode'); lab('heuristic.threeOff', 'Tắt chế độ ba người', 'Turn off three evaluators')
lab('heuristic.threeText', 'Mô phỏng: người 1 tìm {a}, người 2 tìm {b}, người 3 tìm {c} vấn đề; gộp lại được {u}/{n}. Đó là lý do nên có 3–5 người đánh giá độc lập (mô hình giản lược).', 'Simulation: evaluator 1 finds {a}, evaluator 2 finds {b}, evaluator 3 finds {c} issues; together {u}/{n}. That is why 3–5 independent evaluators are recommended (simplified model).')
lab('heuristic.summary', 'Tìm đúng {hit}, bỏ sót {miss}, báo nhầm {fp}; heuristic khớp {hok}; severity lệch ≤ 1 bậc: {sok}.', 'Found {hit}, missed {miss}, false alarms {fp}; heuristic matched {hok}; severity within 1 level: {sok}.')
lab('heuristic.col.area', 'Vùng', 'Area'); lab('heuristic.col.result', 'Kết quả', 'Result'); lab('heuristic.col.answer', 'Đáp án và giải thích', 'Answer and explanation')
for k, vi, en in [('hit', 'tìm đúng', 'found'), ('miss', 'bỏ sót', 'missed'), ('fp', 'báo nhầm', 'false alarm'), ('okDecoy', 'mồi nhử, bỏ qua đúng', 'decoy, correctly ignored')]: lab('heuristic.res.' + k, vi, en)
lab('heuristic.ans', '{h} · {sev}', '{h} · {sev}'); lab('heuristic.decoy', 'Không phải vấn đề', 'Not an issue')
lab('heuristic.note', 'Heuristic là quy tắc kinh nghiệm, không phải định luật; đánh giá chuyên gia không thay test với người dùng. Severity: thang 0–4 của NN/g. [[src:nn-heuristics]] [[src:nn-severity]] [[src:nn-heur-eval]]', 'Heuristics are rules of thumb, not laws; expert review does not replace testing with users. Severity: NN/g\'s 0–4 scale. [[src:nn-heuristics]] [[src:nn-severity]] [[src:nn-heur-eval]]')
for i, vi, en in [(1, 'Hiển thị trạng thái hệ thống (Visibility of system status)', 'Visibility of system status'), (2, 'Khớp hệ thống với thế giới thật (Match between system and the real world)', 'Match between system and the real world'),
                  (3, 'Người dùng kiểm soát và tự do (User control and freedom)', 'User control and freedom'), (4, 'Nhất quán và theo chuẩn (Consistency and standards)', 'Consistency and standards'),
                  (5, 'Phòng ngừa lỗi (Error prevention)', 'Error prevention'), (6, 'Nhận ra thay vì nhớ lại (Recognition rather than recall)', 'Recognition rather than recall'),
                  (7, 'Linh hoạt và hiệu quả (Flexibility and efficiency of use)', 'Flexibility and efficiency of use'), (8, 'Thẩm mỹ và tối giản (Aesthetic and minimalist design)', 'Aesthetic and minimalist design'),
                  (9, 'Giúp nhận ra, chẩn đoán, phục hồi lỗi (Help users recognize, diagnose, and recover from errors)', 'Help users recognize, diagnose, and recover from errors'), (10, 'Trợ giúp và tài liệu (Help and documentation)', 'Help and documentation')]:
    lab('h.%d' % i, '#%d %s' % (i, vi), '#%d %s' % (i, en))
for i, vi, en in [(0, '0 – không phải vấn đề', '0 – not a problem'), (1, '1 – thẩm mỹ', '1 – cosmetic'), (2, '2 – nhỏ', '2 – minor'), (3, '3 – lớn', '3 – major'), (4, '4 – thảm họa', '4 – catastrophe')]: lab('sev.%d' % i, vi, en)
for k, vi, en in [('h1', 'Thẻ lịch sắp tới không có cách đổi giờ ngay tại đây.', 'The upcoming appointment card offers no way to change the time right here.'), ('h2', 'Nút chính rõ ràng, đúng việc.', 'A clear primary button for the main task.'),
                  ('h3', 'Thanh điều hướng chỉ có icon, phải nhớ nghĩa.', 'The navigation bar is icon-only; users must remember meanings.'), ('s1', 'Danh sách dịch vụ có tên và thời lượng rõ.', 'The service list shows clear names and durations.'),
                  ('s2', 'Không có lối tắt cho dịch vụ đã đặt trước đây.', 'No shortcut to previously booked services.'), ('t1', 'Ô giờ nhỏ, sát nhau; giờ đã chọn chỉ khác bằng viền.', 'Time chips are small and close; the selection differs only by an outline.'),
                  ('t2', '"Không còn chỗ" không gợi ý ngày hay giờ khác.', '"No slots left" suggests no other day or time.'), ('t3', '"Tiếp" không được nhấn mạnh như hành động chính.', '"Next" is not emphasised as the primary action.'),
                  ('c1', 'Tóm tắt lịch hẹn đầy đủ trước khi xác nhận.', 'A full summary before confirming.'), ('c2', 'Ô số điện thoại không gợi ý định dạng, không chấp nhận dấu gạch.', 'The phone field gives no format hint and rejects dashes.'),
                  ('c3', '"Lỗi 422" là mã kỹ thuật, không nói cách sửa.', '"Error 422" is a technical code with no fix.'), ('c4', '"OK" và "Hủy" không nói kết quả; "Hủy" mơ hồ.', '"OK" and "Cancel" do not state the outcome; "Cancel" is ambiguous.'),
                  ('m1', '"Sửa" trông như chữ thường, không giống nút.', '"Edit" looks like plain text, not a button.'), ('m2', 'Trạng thái rỗng không gợi ý bước tiếp theo.', 'The empty state suggests no next step.'),
                  ('m3', 'Hủy lịch hẹn không có hoàn tác.', 'Cancelling an appointment has no undo.')]:
    lab('why.' + k, vi, en)
lab('curve.title', 'Đường cong phát hiện vấn đề', 'Problem discovery curve')
lab('curve.intro', 'found(n) = 1 − (1 − L)^n, với L là tỉ lệ vấn đề một người tham gia tìm ra. Mặc định L = 31% (Nielsen, "trung bình trên nhiều dự án") — đây là giả định, bạn chỉnh được. [[src:nn-5users]] [[badge:quant-model]]', 'found(n) = 1 − (1 − L)^n, where L is the share of problems one participant uncovers. Default L = 31% (Nielsen, "averaged across many projects") — an assumption you can change. [[src:nn-5users]] [[badge:quant-model]]')
lab('curve.L', 'L (tỉ lệ một người tìm ra)', 'L (share found by one user)'); lab('curve.n', 'n (số người tham gia)', 'n (participants)')
lab('curve.read', 'Với n = {n}, L = {L}: mô hình dự đoán tìm được {f} vấn đề.', 'With n = {n}, L = {L}: the model predicts {f} of the problems found.')
lab('curve.desc', 'Đường cong tỉ lệ vấn đề tìm được theo số người tham gia.', 'A curve of the share of problems found against the number of participants.')
lab('curve.compare', 'Theo đúng công thức, 1 vòng × 15 người ({one}) và 3 vòng × 5 người ({three}) cho độ phủ gần bằng nhau. Lợi ích của nhiều vòng nhỏ nằm ở chỗ công thức không mô tả: sửa giữa các vòng, kiểm lại bản sửa, và lộ ra vấn đề trước bị che (Nielsen khuyên chia ngân sách thành nhiều vòng).', 'By the formula itself, 1 round × 15 users ({one}) and 3 rounds × 5 users ({three}) give nearly the same coverage. The benefit of several small rounds lies where the formula is silent: fixing between rounds, checking the fixes, and uncovering problems that were masked (Nielsen advises splitting the budget into several rounds).')
lab('curve.assume', 'Giả định: người dùng tương đồng, dùng sản phẩm theo cách tương tự; vấn đề độc lập, L đồng đều. Vấn đề hiếm cần nhiều người hơn; nhiều nhóm người dùng khác nhau cần test riêng từng nhóm; câu hỏi định lượng cần ≥ 20 người. [[src:nn-howmany]]', 'Assumptions: similar users using the product in similar ways; independent problems with a uniform L. Rare problems need more users; distinct user groups need separate tests; quantitative questions need ≥ 20 users. [[src:nn-howmany]]')
lab('sus.title', 'Máy tính SUS', 'SUS calculator')
lab('sus.intro', 'Nhập câu trả lời 1–5 cho 10 câu SUS của từng người tham gia (dữ liệu giả định để học). [[badge:quant-model]]', 'Enter 1–5 answers to the 10 SUS items for each participant (hypothetical data for learning). [[badge:quant-model]]')
lab('sus.col.p', 'Người', 'Participant'); lab('sus.col.score', 'Điểm', 'Score'); lab('sus.participant', 'P{n}', 'P{n}'); lab('sus.cell', 'Người {p}, câu {q}', 'Participant {p}, item {q}')
for i in range(1, 11): lab('sus.q%d' % i, 'Câu %d của SUS (lẻ: tích cực, chẵn: tiêu cực)' % i, 'SUS item %d (odd: positive, even: negative)' % i)
lab('sus.add', 'Thêm người', 'Add participant'); lab('sus.remove', 'Bớt người', 'Remove participant')
lab('sus.mean', 'Trung bình: {m} trên {n} người (mức trung bình tham chiếu của SUS là {avg}).', 'Mean: {m} over {n} participants (the SUS reference average is {avg}).')
lab('sus.warn', 'SUS không phải phần trăm: 70 không có nghĩa "70% hài lòng". Với vài người, trung bình rất bất định; so sánh định lượng cần khoảng 20–30 người trở lên. [[src:mu-sus]] [[src:nn-perceived]]', 'SUS is not a percentage: 70 does not mean "70% satisfied". With a few people the mean is very uncertain; quantitative comparisons need roughly 20–30 people or more. [[src:mu-sus]] [[src:nn-perceived]]')
lab('sus.formula', 'Công thức (Sauro): câu lẻ lấy điểm − 1, câu chẵn lấy 5 − điểm, cộng lại rồi nhân 2,5. Kiểm chứng: mọi câu bằng 3 → 50.', 'Formula (Sauro): odd items score − 1, even items 5 − score, sum and multiply by 2.5. Check: all items at 3 → 50.')
lab('success.title', 'Task success và khoảng tin cậy', 'Task success and confidence intervals')
lab('success.intro', 'Nhập số người thành công trên tổng số cho hai thiết kế; khoảng tin cậy 95% theo adjusted Wald. [[badge:quant-model]]', 'Enter successes out of total for two designs; 95% confidence intervals by adjusted Wald. [[badge:quant-model]]')
lab('success.design.a', 'Thiết kế A', 'Design A'); lab('success.design.b', 'Thiết kế B', 'Design B'); lab('success.x', 'Thành công', 'Successes'); lab('success.n', 'Tổng', 'Total')
lab('success.chart', 'Khoảng tin cậy của hai thiết kế', 'Confidence intervals of the two designs'); lab('success.desc', 'Hai đoạn thẳng là khoảng tin cậy 95%; chấm là tỉ lệ quan sát.', 'The two segments are 95% intervals; the dots are the observed rates.')
lab('success.ci', '{d}: {x}/{n} = {p}; khoảng tin cậy 95%: {lo} – {hi}.', '{d}: {x}/{n} = {p}; 95% interval: {lo} – {hi}.')
lab('success.overlap', 'Hai khoảng chồng nhau: chưa đủ để kết luận thiết kế nào tốt hơn.', 'The intervals overlap: not enough to conclude which design is better.')
lab('success.noOverlap', 'Hai khoảng không chồng nhau: khác biệt đáng chú ý trong giả định của mô hình; vẫn cần xem cách lấy mẫu.', 'The intervals do not overlap: a notable difference under the model\'s assumptions; still check how the sample was drawn.')
lab('success.formula', 'p̃ = (x + z²/2)/(n + z²), khoảng p̃ ± z·√(p̃(1 − p̃)/(n + z²)), z = 1,96. Kiểm chứng: 20/100 → 13–29% (ví dụ của NN/g). [[src:mu-wald]] [[src:wiki-binom]] [[src:nn-success]]', 'p̃ = (x + z²/2)/(n + z²), interval p̃ ± z·√(p̃(1 − p̃)/(n + z²)), z = 1.96. Check: 20/100 → 13–29% (NN/g\'s example). [[src:mu-wald]] [[src:wiki-binom]] [[src:nn-success]]')
lab('microcopy.title', 'Biên tập microcopy', 'Microcopy editor')
lab('microcopy.intro', 'Tám chuỗi của Hẹn Khám. Sửa từng chuỗi; checklist tự soạn (dựa trên hướng dẫn thông báo lỗi của NN/g) chấm ngay trên trang.', 'Eight ClinicBook strings. Edit each; a self-written checklist (based on NN/g\'s error-message guidelines) grades it on the page.')
lab('mc.item', 'Chuỗi', 'String'); lab('mc.context', 'Bối cảnh', 'Context'); lab('mc.orig', 'Bản gốc', 'Original'); lab('mc.yours', 'Bản của bạn', 'Your version'); lab('mc.suggest', 'Xem bản đề xuất', 'See a suggested version')
lab('mc.note', 'Checklist là công cụ tập luyện, không phải bộ chấm chuẩn; chữ tốt còn phụ thuộc bối cảnh. Giữ một chuỗi trọn câu trong tài nguyên (strings.xml, plurals) thay vì ghép mảnh — cầu nối X8. [[src:nn-errmsg]]', 'The checklist is a practice tool, not a standard grader; good copy also depends on context. Keep each sentence whole in resources (strings.xml, plurals) instead of concatenating pieces — bridge X8. [[src:nn-errmsg]]')
for k, vi, en in [('notEmpty', 'Không để trống', 'Not empty'), ('length', 'Độ dài hợp mobile (nút ≤ 24, câu ≤ 90 ký tự)', 'Mobile-friendly length (buttons ≤ 24, sentences ≤ 90 characters)'),
                  ('noCode', 'Không có mã lỗi kỹ thuật', 'No technical error codes'), ('noVague', 'Không dùng từ mơ hồ (OK, Gửi, Xử lý…)', 'No vague words (OK, Submit, Process…)'), ('noBlame', 'Không đổ lỗi cho người dùng', 'No blaming the user')]:
    lab('mc.rule.' + k, vi, en)
lab('mc.vagueWords', 'ok|gửi|xử lý|đồng ý|có|không', 'ok|submit|process|yes|no|continue')
lab('mc.blameWords', 'bạn đã sai|bạn nhập sai|không hợp lệ|bạn quên', 'you entered|invalid|you forgot|your mistake|illegal')
MC = [
 ('btnConfirm', 'Nút ở màn Xác nhận', 'Button on Confirm', 'Nút chính hoàn tất việc đặt lịch.', 'The primary button that completes the booking.', 'OK', 'OK', 'Đặt lịch', 'Book appointment', 'Động từ nói đúng kết quả của việc bấm.', 'A verb that states the result of tapping.'),
 ('btnCancel', 'Nút phụ ở màn Xác nhận', 'Secondary button on Confirm', 'Người dùng muốn quay lại sửa giờ, không phải hủy lịch.', 'The user wants to go back and change the time, not cancel the appointment.', 'Hủy', 'Cancel', 'Quay lại sửa', 'Go back and edit', 'Tách "quay lại" khỏi "hủy lịch hẹn" để tránh mistake.', 'Separate "go back" from "cancel appointment" to avoid mistakes.'),
 ('errPhone', 'Lỗi số điện thoại', 'Phone number error', 'Người dùng gõ số có dấu gạch.', 'The user typed the number with dashes.', 'Số điện thoại không hợp lệ.', 'Invalid phone number.', 'Nhập 10 chữ số, ví dụ 0901234567.', 'Enter 10 digits, for example 0901234567.', 'Nói cách sửa thay vì phán xét; tốt hơn nữa là tự chấp nhận dấu gạch.', 'Say how to fix it instead of judging; better still, accept dashes automatically.'),
 ('errServer', 'Lỗi máy chủ', 'Server error', 'Lưu lịch thất bại vì mạng.', 'Saving failed because of the network.', 'Lỗi 422', 'Error 422', 'Chưa lưu được lịch. Kiểm tra kết nối rồi thử lại — thông tin bạn nhập vẫn còn.', 'Couldn\'t save the booking. Check your connection and try again — your details are still here.', 'Nói chuyện gì xảy ra, dữ liệu còn không, làm gì tiếp; ẩn mã kỹ thuật.', 'Say what happened, whether data is kept and what to do; hide the technical code.'),
 ('empty', 'Trạng thái rỗng', 'Empty state', 'Người dùng chưa có lịch hẹn nào.', 'The user has no appointments yet.', 'Không có dữ liệu', 'No data', 'Chưa có lịch hẹn. Đặt lịch khám đầu tiên của bạn.', 'No appointments yet. Book your first visit.', 'Trạng thái rỗng nên chỉ ra bước tiếp theo.', 'An empty state should point to the next step.'),
 ('cancelDialog', 'Hộp thoại hủy lịch', 'Cancel dialog', 'Xác nhận trước khi hủy một lịch hẹn.', 'Confirm before cancelling an appointment.', 'Bạn có chắc không?', 'Are you sure?', 'Hủy lịch khám Thứ Năm 09:00? Bạn có thể đặt lại sau.', 'Cancel your Thursday 09:00 visit? You can book again later.', 'Xác nhận có trọng tâm nói rõ cái gì sẽ mất.', 'A focused confirmation says exactly what will be lost.'),
 ('reminder', 'Thông báo nhắc lịch', 'Reminder notification', 'Nhắc trước một ngày.', 'A reminder one day before.', 'Thông báo: bạn có sự kiện.', 'Notification: you have an event.', 'Mai 09:00 bạn có lịch Khám tổng quát.', 'Tomorrow at 09:00: General check-up.', 'Thông tin quan trọng nhất đứng đầu, ngắn gọn.', 'The most important information first, briefly.'),
 ('saved', 'Phản hồi sau khi lưu', 'Feedback after saving', 'Snackbar sau khi đổi giờ.', 'A snackbar after changing the time.', 'Thành công', 'Success', 'Đã dời sang 14:00. Hoàn tác', 'Moved to 14:00. Undo', 'Nói chính xác điều đã xảy ra và cho hoàn tác.', 'Say exactly what happened and offer undo.')]
for k, lv, le, cv, ce, ov, oe, bv, be, wv, we in MC:
    lab('mc.i.' + k + '.label', lv, le); lab('mc.i.' + k + '.ctx', cv, ce); lab('mc.i.' + k + '.orig', ov, oe); lab('mc.i.' + k + '.better', bv, be); lab('mc.i.' + k + '.why', wv, we)

# ---------- chương ----------
def ch(c, title, essence, g1, g2, secs, quiz, sims=None):
    a(c + '.title', *title); a(c + '.essence', *essence); a(c + '.goal.g1', *g1); a(c + '.goal.g2', *g2)
    for sid, stitle, badge, paras in secs:
        a(c + '.sec.' + sid + '.title', *stitle); a(c + '.sec.' + sid + '.badge', badge, badge)
        for i, p in enumerate(paras): a(c + '.sec.' + sid + '.p.' + str(i + 1), *p)
    for i, (q, ans, why) in enumerate(quiz):
        a(c + '.quiz.q%d.q' % (i + 1), *q); a(c + '.quiz.q%d.a' % (i + 1), *ans); a(c + '.quiz.q%d.why' % (i + 1), *why)
    for sid, vi, en in (sims or []): a(c + '.sim.' + sid, vi, en)

ch('d0', ('Bản đồ UX', 'The UX map'),
   ('UX bao trùm mọi tương tác với sản phẩm và dịch vụ; usability là thuộc tính đo được; UI là bề mặt tương tác.\nThiết kế lấy con người làm trung tâm là vòng lặp: quan sát, ý tưởng, bản mẫu, kiểm tra.\nTrack này dùng ứng dụng hư cấu "Hẹn Khám" để luyện tập.', 'UX covers every interaction with products and services; usability is a measurable attribute; UI is the interaction surface.\nHuman-centred design is a loop: observe, ideate, prototype, test.\nThis track uses the fictional "ClinicBook" app for practice.'),
   ('Đã phân loại một tình huống', 'Classified one situation'), ('Đã xem Double Diamond', 'Looked at the Double Diamond'),
   [('def', ('UX, UI, usability', 'UX, UI, usability'), 'research', [
      ('UX bao trùm mọi khía cạnh tương tác của người dùng với công ty, dịch vụ và sản phẩm; giao diện là phần rất quan trọng nhưng không phải tất cả. Usability là thuộc tính chất lượng của UI. [[src:nn-ux-def]]', 'UX covers every aspect of the user\'s interaction with the company, its services and products; the interface is very important but not everything. Usability is a quality attribute of the UI. [[src:nn-ux-def]]'),
      ('Năm thành phần của usability: dễ học, hiệu quả, dễ nhớ, ít lỗi, hài lòng; tầm quan trọng của từng phần tùy sản phẩm. [[src:nn-usability101]]', 'The five components of usability: learnability, efficiency, memorability, errors, satisfaction; their relative importance depends on the product. [[src:nn-usability101]]'),
      ('Double Diamond của Design Council: Discover, Define, Develop, Deliver; quy trình là lời mời, và tổ chức thường quay lại đầu khi học được điều mới. Bản đồ UI tương ứng ở chương E0. [[src:dc-diamond]] [[badge:author-framework]]', 'The Design Council\'s Double Diamond: Discover, Define, Develop, Deliver; the process is an invitation, and organisations often return to the start when they learn something new. The matching UI map is in chapter E0. [[src:dc-diamond]] [[badge:author-framework]]')])],
   [(('UI tốt có bảo đảm UX tốt?', 'Does a good UI guarantee good UX?'), ('Không.', 'No.'), ('Dịch vụ phía sau có thể làm hỏng trải nghiệm dù giao diện hoàn hảo.', 'The service behind it can ruin the experience even with a perfect interface.')),
    (('Usability gồm những gì?', 'What does usability include?'), ('Dễ học, hiệu quả, dễ nhớ, ít lỗi, hài lòng.', 'Learnability, efficiency, memorability, errors, satisfaction.'), ('Theo NN/g Usability 101.', 'Per NN/g Usability 101.'))],
   [('ux.classify', 'UX hay UI?', 'UX or UI?'), ('ux.diamond', 'Double Diamond', 'Double Diamond')])

ch('d1', ('Bộ óc người dùng', 'The user\'s mind'),
   ('Thị giác và sự chú ý có giới hạn; người dùng quét chứ không đọc từng chữ.\nNhận ra dễ hơn nhớ lại; tải nhận thức càng thấp càng ít lỗi.\nMô hình tư duy của người dùng có thể khác mô hình của hệ thống.', 'Vision and attention are limited; users scan rather than read every word.\nRecognition is easier than recall; lower cognitive load means fewer errors.\nUsers\' mental models can differ from the system\'s model.'),
   ('Đã thử cả hai cách trong lab', 'Tried both ways in the lab'), ('Đã so dự đoán với hệ thống', 'Compared a prediction with the system'),
   [('mem', ('Trí nhớ và "7±2"', 'Memory and "7±2"'), 'research', [
      ('Nhận ra dễ hơn nhớ lại vì có nhiều gợi ý truy xuất; giao diện nên làm lựa chọn hiện ra. [[src:nn-recall]]', 'Recognition is easier than recall because it offers more retrieval cues; interfaces should make options visible. [[src:nn-recall]]'),
      ('Trí nhớ ngắn hạn giữ khoảng 7 chunk và phai trong khoảng 20 giây. Điều đó không có nghĩa menu tối đa 7 mục: menu dùng recognition. [[src:nn-stm]] [[badge:research]]', 'Short-term memory holds about 7 chunks that fade in about 20 seconds. That does not mean menus must have at most 7 items: menus rely on recognition. [[src:nn-stm]] [[badge:research]]'),
      ('Six Minds (John Whalen) — thị giác/chú ý, định hướng, trí nhớ, ngôn ngữ, ra quyết định, cảm xúc — là một khung đọc của tác giả, không phải chuẩn. Chuyển động thu hút chú ý: cầu nối X7 (E9). [[badge:author-framework]]', 'Six Minds (John Whalen) — vision/attention, wayfinding, memory, language, decision-making, emotion — is an author\'s reading frame, not a standard. Motion draws attention: bridge X7 (E9). [[badge:author-framework]]')])],
   [(('7±2 có nghĩa menu tối đa 7 mục?', 'Does 7±2 mean menus of at most 7 items?'), ('Không.', 'No.'), ('Menu dựa vào recognition, không phải trí nhớ ngắn hạn.', 'Menus rely on recognition, not short-term memory.')),
    (('Số đo của bạn trong lab có phải dữ liệu nghiên cứu?', 'Is your lab measurement research data?'), ('Không.', 'No.'), ('Đó là minh họa cá nhân, không lưu, không gửi.', 'It is a personal illustration, not saved or sent.'))],
   [('ux.recall', 'Nhận ra / nhớ lại', 'Recognition / recall'), ('ux.mental', 'Mô hình tư duy', 'Mental model')])

ch('d2', ('Nguyên lý tương tác', 'Interaction principles'),
   ('Bảy giai đoạn hành động và hai vực: vực thực thi (làm sao để làm) và vực đánh giá (đã xong chưa).\nSignifier cho biết làm gì, ở đâu; feedback cho biết điều gì đã xảy ra.\nMô hình bảy giai đoạn là của Don Norman (The Design of Everyday Things).', 'Seven stages of action and two gulfs: execution (how do I do it) and evaluation (is it done).\nSignifiers say what and where; feedback says what happened.\nThe seven-stage model is Don Norman\'s (The Design of Everyday Things).'),
   ('Đã tới giai đoạn thực hiện', 'Reached the perform stage'), ('Đã bật một lỗi thiết kế', 'Turned on a design flaw'),
   [('st', ('Signifier và feedback trên Android', 'Signifiers and feedback on Android'), 'research author-framework', [
      ('Heuristic #1 "Hiển thị trạng thái hệ thống": luôn cho người dùng biết chuyện gì đang diễn ra. [[src:nn-heuristics]]', 'Heuristic #1 "Visibility of system status": keep users informed about what is going on. [[src:nn-heuristics]]'),
      ('Trong Compose, phần tử bấm được nên có `Modifier.clickable` với `role = Role.Button` và nhãn semantics để trình đọc màn hình hiểu; phần trợ năng đầy đủ ở cầu nối X6.', 'In Compose, a tappable element should use `Modifier.clickable` with `role = Role.Button` and a semantics label so screen readers understand it; full accessibility is in bridge X6.')])],
   [(('Bỏ feedback sau khi lưu mở rộng vực nào?', 'Removing feedback after saving widens which gulf?'), ('Vực đánh giá.', 'The gulf of evaluation.'), ('Người dùng không biết đã lưu chưa.', 'Users cannot tell whether it saved.')),
    (('Signifier giúp vực nào?', 'Which gulf do signifiers help?'), ('Vực thực thi.', 'The gulf of execution.'), ('Chúng cho biết làm gì và ở đâu.', 'They show what to do and where.'))])

ch('d3', ('Lỗi người dùng', 'User errors'),
   ('Slip: định làm đúng nhưng thao tác sai. Mistake: mục tiêu hoặc kế hoạch sai, thường do mô hình tư duy lệch.\nChiến lược: phòng ngừa, phát hiện sớm, phục hồi (undo, thông báo chỉ cách sửa).\nKhi người dùng sai, trước hết xem lại thiết kế, nhưng không phủ nhận vi phạm có chủ ý.', 'Slip: the intention is right but the action is wrong. Mistake: the goal or plan is wrong, often from a mismatched mental model.\nStrategy: prevent, detect early, recover (undo, messages that show the fix).\nWhen users err, look at the design first, without denying deliberate violations.'),
   ('Đã phân loại một lỗi', 'Classified one error'), ('Đã thử một biện pháp', 'Tried a remedy'),
   [('err', ('Phòng và chữa lỗi', 'Preventing and fixing errors'), 'research', [
      ('Slip: dùng constraint, gợi ý, mặc định tốt, định dạng dễ dãi; lỗi là của thiết kế. Mistake: tìm chỗ lệch mô hình tư duy, theo quy ước, signifier rõ, xem trước kết quả. Chung: bớt gánh nhớ, xác nhận trước thao tác phá hủy (quá nhiều thì người dùng bấm qua), undo. [[src:nn-slips]] [[src:nn-mistakes]]', 'Slips: use constraints, suggestions, good defaults, forgiving formats; the fault is the design\'s. Mistakes: find mental-model gaps, follow conventions, clear signifiers, preview results. For both: reduce memory load, confirm destructive actions (too many and users click through), undo. [[src:nn-slips]] [[src:nn-mistakes]]'),
      ('Thông báo lỗi: gần nguồn, không chỉ dựa vào màu, ngôn ngữ dễ hiểu, chính xác, gợi ý cách sửa, không đổ lỗi, giữ dữ liệu đã nhập. Trong Compose: `TextField(isError = …, supportingText = …)` và `Snackbar` có hành động "Hoàn tác". [[src:nn-errmsg]]', 'Error messages: near the source, not colour alone, plain language, precise, constructive, no blame, keep the user\'s input. In Compose: `TextField(isError = …, supportingText = …)` and a `Snackbar` with an "Undo" action. [[src:nn-errmsg]]')])],
   [(('Gõ số điện thoại có dấu gạch rồi bị báo lỗi là slip hay mistake?', 'Typing a phone number with dashes and getting an error: slip or mistake?'), ('Slip — và form quá khắt khe.', 'A slip — and an overly strict form.'), ('Định nhập đúng số, chỉ khác định dạng.', 'The intended number was right; only the format differed.')),
    (('Có nên xác nhận mọi thao tác?', 'Should every action be confirmed?'), ('Không.', 'No.'), ('Quá nhiều xác nhận khiến người dùng bấm qua mà không đọc.', 'Too many confirmations make users click through without reading.'))])

ch('d4', ('Heuristic evaluation và severity', 'Heuristic evaluation and severity'),
   ('10 heuristic của Nielsen là quy tắc kinh nghiệm rộng, không phải định luật.\nĐánh giá do 3–5 người làm độc lập rồi gộp; severity chấm theo thang 0–4.\nĐánh giá chuyên gia không thay test với người dùng.', 'Nielsen\'s 10 heuristics are broad rules of thumb, not laws.\n3–5 people evaluate independently, then consolidate; severity uses a 0–4 scale.\nExpert review does not replace testing with users.'),
   ('Đã mở workbench', 'Opened the workbench'), ('Đã chấm bài', 'Graded your review'),
   [('he', ('Cách làm', 'How to do it'), 'research', [
      ('Mỗi người đánh giá làm riêng khoảng 1–2 giờ, không xem bài người khác, rồi cả nhóm gộp và thảo luận. [[src:nn-heur-eval]]', 'Each evaluator works alone for about 1–2 hours without seeing others\' results, then the team consolidates and discusses. [[src:nn-heur-eval]]'),
      ('Severity kết hợp tần suất, tác động và độ dai dẳng; tác động thị trường xét riêng. Điểm của một người không đủ tin cậy; lấy trung bình khoảng ba người. [[src:nn-severity]]', 'Severity combines frequency, impact and persistence; market impact is assessed separately. One person\'s ratings are not reliable enough; average about three. [[src:nn-severity]]')])],
   [(('Heuristic có phải định luật?', 'Are heuristics laws?'), ('Không.', 'No.'), ('Chúng là quy tắc kinh nghiệm rộng.', 'They are broad rules of thumb.')),
    (('Vì sao cần nhiều người đánh giá?', 'Why use several evaluators?'), ('Mỗi người tìm được một tập con khác nhau.', 'Each finds a different subset.'), ('Gộp lại phủ được nhiều vấn đề hơn.', 'Together they cover more problems.'))])

ch('d5', ('Quyết định, hành vi và đạo đức', 'Decisions, behaviour and ethics'),
   ('Người dùng quyết định bằng cả trực giác lẫn cân nhắc; số lựa chọn, cách trình bày và thời điểm đều ảnh hưởng.\nThiết kế thay đổi hành vi phải minh bạch và vì lợi ích người dùng.\nDeceptive pattern chỉ học để nhận diện và tránh.', 'Users decide by both intuition and deliberation; the number of options, presentation and timing all matter.\nDesign that changes behaviour must be transparent and in the user\'s interest.\nDeceptive patterns are studied only to recognise and avoid them.'),
   ('Đã gỡ một điểm nghẽn CREATE', 'Cleared a CREATE bottleneck'), ('Đã nhận diện một pattern', 'Recognised a pattern'),
   [('hick', ('Hick\'s law và quá tải lựa chọn', 'Hick\'s law and choice overload'), 'research', [
      ('Thời gian quyết định tăng theo số và độ phức tạp của lựa chọn trong điều kiện nhất định (nghiên cứu của Hick và Hyman, 1952). Nguồn ở đây là lawsofux.com — nguồn thứ cấp — nên site chỉ trình bày định tính. [[src:lawsofux-hick]]', 'Decision time grows with the number and complexity of choices under certain conditions (Hick and Hyman\'s 1952 study). The source here is lawsofux.com — a secondary source — so the site presents it only qualitatively. [[src:lawsofux-hick]]'),
      ('Không suy ra "ít lựa chọn luôn tốt": NN/g ủng hộ đơn giản hóa nhưng cũng cảnh báo progressive disclosure quá 2 tầng thường kém, và quá đơn giản thành trừu tượng. [[src:nn-simplicity]] [[src:nn-progressive]]', 'Do not conclude "fewer options are always better": NN/g favours simplicity but also warns that progressive disclosure beyond 2 levels tends to be poor, and oversimplifying becomes abstract. [[src:nn-simplicity]] [[src:nn-progressive]]'),
      ('Deceptive pattern: obstruction, mẹo hình thức hoặc chữ, nagging, confirmshaming, sneaking/preselection. Thiết kế thuyết phục trung thực (ví dụ bằng chứng xã hội có thật) khác thiết kế lừa dối. [[src:nn-deceptive]]', 'Deceptive patterns: obstruction, visual or wording tricks, nagging, confirmshaming, sneaking/preselection. Honest persuasion (for example real social proof) differs from deception. [[src:nn-deceptive]]')])],
   [(('Hick\'s law có nghĩa càng ít lựa chọn càng tốt?', 'Does Hick\'s law mean fewer choices are always better?'), ('Không.', 'No.'), ('Nó mô tả thời gian quyết định trong điều kiện nhất định; quá đơn giản lại gây khó.', 'It describes decision time under certain conditions; oversimplifying creates other problems.')),
    (('Ô tick sẵn bằng chữ mờ là pattern gì?', 'A pre-ticked box in faint text is which pattern?'), ('Sneaking / preselection.', 'Sneaking / preselection.'), ('Lựa chọn được làm sẵn và giấu đi.', 'The choice is pre-made and hidden.'))],
   [('ux.create', 'Phễu CREATE', 'CREATE funnel'), ('ux.deceptive', 'Deceptive pattern', 'Deceptive patterns')])

ch('d6', ('Nghiên cứu người dùng', 'User research'),
   ('Chọn phương pháp theo câu hỏi: thái độ ↔ hành vi, định tính ↔ định lượng, bối cảnh sử dụng.\nPhỏng vấn và contextual inquiry để hiểu nhu cầu; persona và journey map là công cụ tổng hợp, không thay dữ liệu.\nĐiều người dùng nói khác điều họ làm.', 'Choose the method by the question: attitudinal ↔ behavioural, qualitative ↔ quantitative, context of use.\nInterviews and contextual inquiry to understand needs; personas and journey maps are synthesis tools, not data.\nWhat users say differs from what they do.'),
   ('Đã chọn phương pháp cho một câu hỏi', 'Picked a method for one question'), ('Đã xem vị trí trên các trục', 'Saw the position on the axes'),
   [('ax', ('Ba trục', 'Three axes'), 'research', [
      ('Thái độ là "người dùng nói gì" (khảo sát, card sorting); hành vi là "người dùng làm gì" (A/B test, eyetracking); usability test và field study nằm giữa, nghiêng về hành vi. Định tính trả lời "vì sao, sửa thế nào"; định lượng trả lời "bao nhiêu". [[src:nn-methods]]', 'Attitudinal is "what people say" (surveys, card sorting); behavioural is "what people do" (A/B tests, eyetracking); usability studies and field studies sit between, leaning behavioural. Qualitative answers "why and how to fix"; quantitative answers "how many". [[src:nn-methods]]'),
      ('Journey map và persona trong site là bản mẫu để thực hành, dữ liệu giả định cho mục đích học. Đọc thêm: [[src:nn-journey]] [[src:nn-persona]] [[src:nn-interviews]]', 'Journey maps and personas on this site are practice templates with assumed data for learning. Further reading: [[src:nn-journey]] [[src:nn-persona]] [[src:nn-interviews]]')])],
   [(('"Bao nhiêu % hoàn tất đặt lịch?" hợp phương pháp nào?', '"What % complete a booking?" fits which method?'), ('Analytics.', 'Analytics.'), ('Câu hỏi định lượng về hành vi thật.', 'A quantitative question about real behaviour.')),
    (('Persona có thay được dữ liệu?', 'Can personas replace data?'), ('Không.', 'No.'), ('Chúng tổng hợp dữ liệu nghiên cứu.', 'They synthesise research data.'))])

ch('d7', ('Usability testing và "5 người dùng"', 'Usability testing and "5 users"'),
   ('Vòng test nhỏ lặp lại thường hiệu quả hơn một lần test lớn cho mục tiêu phát hiện vấn đề (định tính).\nKết luận về tỉ lệ cần mẫu lớn hơn.\nThink-aloud là công cụ cốt lõi.', 'Small repeated test rounds usually beat one big test for finding problems (qualitative).\nConclusions about rates need bigger samples.\nThink-aloud is the core tool.'),
   ('Đã chỉnh L hoặc n', 'Adjusted L or n'), ('Đã xem phiên think-aloud', 'Watched the think-aloud session'),
   [('five', ('"5 người" và giới hạn của nó', '"5 users" and its limits'), 'quant-model research', [
      ('Nielsen: số vấn đề tìm được với n người là N(1 − (1 − L)^n), L điển hình 31%; với 5 người khoảng 85%. Công thức chỉ đúng với người dùng tương đồng dùng sản phẩm theo cách tương tự. [[src:nn-5users]]', 'Nielsen: problems found with n users is N(1 − (1 − L)^n), with a typical L of 31%; with 5 users about 85%. The formula holds only for similar users using the product in similar ways. [[src:nn-5users]]'),
      ('Nghiên cứu định lượng cần ít nhất 20 người; nhiều nhóm người dùng khác biệt cần khoảng 5 (hoặc 3–4) mỗi nhóm; nên chia ngân sách thành nhiều vòng nhỏ. [[src:nn-howmany]] Đọc thêm về think-aloud: [[src:nn-thinkaloud]]', 'Quantitative studies need at least 20 users; distinct user groups need about 5 (or 3–4) each; split the budget into several small rounds. [[src:nn-howmany]] Further reading on think-aloud: [[src:nn-thinkaloud]]')])],
   [(('5 người có đủ để biết bao nhiêu % hoàn tất?', 'Are 5 users enough to know what % complete?'), ('Không.', 'No.'), ('Câu hỏi định lượng cần ≥ 20 người.', 'Quantitative questions need ≥ 20 users.')),
    (('L = 31% là gì?', 'What is L = 31%?'), ('Một giả định trung bình từ nhiều dự án.', 'An average assumption across many projects.'), ('Sản phẩm của bạn có thể khác; hãy chỉnh L.', 'Your product may differ; adjust L.'))],
   [('ux.curve', 'Đường cong phát hiện', 'Discovery curve'), ('ux.session', 'Phiên think-aloud', 'Think-aloud session')])

ch('d8', ('Đo lường UX', 'Measuring UX'),
   ('Chỉ số hiệu năng: task success, thời gian, lỗi, khả năng học; chỉ số tự báo cáo: SUS, đánh giá sau tác vụ.\nMẫu nhỏ thì phải kèm khoảng tin cậy, không chỉ báo một con số.\nSUS là thang 0–100, không phải phần trăm.', 'Performance metrics: task success, time, errors, learnability; self-reported metrics: SUS, post-task ratings.\nSmall samples must come with confidence intervals, not a single number.\nSUS is a 0–100 scale, not a percentage.'),
   ('Đã tính một điểm SUS', 'Calculated a SUS score'), ('Đã so khoảng tin cậy hai thiết kế', 'Compared the two designs\' intervals'),
   [('m', ('Con số và giới hạn', 'Numbers and their limits'), 'quant-model research', [
      ('SUS: câu lẻ điểm − 1, câu chẵn 5 − điểm, tổng × 2,5; trung bình khoảng 68; không phải phần trăm. [[src:mu-sus]] [[src:nn-perceived]]', 'SUS: odd items score − 1, even items 5 − score, sum × 2.5; average about 68; not a percentage. [[src:mu-sus]] [[src:nn-perceived]]'),
      ('Mọi tỉ lệ cần khoảng tin cậy; adjusted Wald hợp mẫu nhỏ. Partial success là thứ bậc: báo từng mức, không lấy trung bình nhãn số. [[src:nn-success]] [[src:mu-wald]]', 'Every percentage needs a confidence interval; adjusted Wald suits small samples. Partial success is ordinal: report each level, do not average numeric labels. [[src:nn-success]] [[src:mu-wald]]'),
      ('A/B test (khái niệm): so hai phương án trên người dùng thật; dừng sớm khi thấy kết quả "đẹp" làm tăng rủi ro kết luận sai. Site không mô phỏng số liệu A/B giả như kết quả thật.', 'A/B testing (concept): compare two options with real users; stopping early when results look "good" raises the risk of wrong conclusions. The site does not simulate fake A/B data as if it were real.')])],
   [(('SUS 70 có phải "70% hài lòng"?', 'Does SUS 70 mean "70% satisfied"?'), ('Không.', 'No.'), ('SUS không phải phần trăm.', 'SUS is not a percentage.')),
    (('Hai khoảng tin cậy chồng nhau thì sao?', 'What if the two intervals overlap?'), ('Chưa đủ để kết luận.', 'Not enough to conclude.'), ('Khác biệt có thể do ngẫu nhiên.', 'The difference may be chance.'))],
   [('ux.sus', 'SUS', 'SUS'), ('ux.success', 'Task success', 'Task success')])

ch('d9', ('UX writing và content design', 'UX writing and content design'),
   ('Chữ là thiết kế: nhãn nút, tiêu đề, trạng thái rỗng, lỗi, xác nhận dẫn người dùng đi tiếp.\nVoice là cá tính nhất quán; tone đổi theo bối cảnh.\nChữ phải sống được qua nhiều ngôn ngữ (cầu nối X8).', 'Words are design: button labels, titles, empty states, errors and confirmations move users forward.\nVoice is a consistent personality; tone changes with context.\nCopy must survive several languages (bridge X8).'),
   ('Đã sửa một chuỗi', 'Edited one string'), ('Đã thử voice và tone', 'Tried voice and tone'),
   [('x8', ('Cầu nối X8: UX writing và bản địa hóa', 'Bridge X8: UX writing and localization'), 'research stable', [
      ('Chuỗi dài ngắn khác nhau theo ngôn ngữ; ngữ pháp và số nhiều khác nhau. Ví dụ ngay trên site này: cùng một nút "Tiến 1 frame" / "Step frame" có độ dài khác nhau, và câu "{n} lần ghi" / "{n} writes" dùng tham số thay vì ghép chữ.', 'String lengths differ by language; grammar and plurals differ. An example on this very site: the same button "Tiến 1 frame" / "Step frame" has different lengths, and "{n} lần ghi" / "{n} writes" uses a parameter instead of concatenation.'),
      ('Không ghép câu từ nhiều mảnh: giữ trọn câu trong `strings.xml`, dùng `plurals` cho số nhiều và tham số cho giá trị. Từ Android 13 (API 33) người dùng chọn ngôn ngữ riêng cho từng app (`LocaleManager.setApplicationLocales`); bản cũ hơn dùng `AppCompatDelegate.setApplicationLocales` (AppCompat ≥ 1.6.0). [[src:and-app-languages]] [[src:and-localization]]', 'Do not build sentences from pieces: keep whole sentences in `strings.xml`, use `plurals` for plural forms and parameters for values. Since Android 13 (API 33) users can pick a language per app (`LocaleManager.setApplicationLocales`); older versions use `AppCompatDelegate.setApplicationLocales` (AppCompat ≥ 1.6.0). [[src:and-app-languages]] [[src:and-localization]]'),
      ('Quy trình biên tập của Torrey Podmajersky (Strategic Writing for UX): mục đích → ngắn gọn → hội thoại → rõ ràng; voice/tone theo Metts và Welfle (Writing Is Designing). Trợ năng trong chữ: link nói rõ đích, không chỉ "bấm vào đây", alt text — cầu nối X6. [[badge:author-framework]] Đọc thêm: [[src:nn-uxwriting]]', 'Torrey Podmajersky\'s editing process (Strategic Writing for UX): purpose → concise → conversational → clear; voice/tone per Metts and Welfle (Writing Is Designing). Accessibility in copy: links that state the destination, not just "click here", alt text — bridge X6. [[badge:author-framework]] Further reading: [[src:nn-uxwriting]]')])],
   [(('Ghép "Bạn có " + n + " lịch hẹn" có ổn?', 'Is concatenating "You have " + n + " appointments" fine?'), ('Không.', 'No.'), ('Ngữ pháp và số nhiều khác nhau theo ngôn ngữ; dùng chuỗi có tham số và plurals.', 'Grammar and plurals differ by language; use parameterised strings and plurals.')),
    (('Voice và tone khác nhau thế nào?', 'How do voice and tone differ?'), ('Voice giữ nguyên, tone đổi theo bối cảnh.', 'Voice stays, tone changes with context.'), ('Cùng một sản phẩm nói khác khi báo lỗi và khi chào.', 'The same product speaks differently in an error and in a greeting.'))],
   [('ux.microcopy', 'Microcopy', 'Microcopy'), ('ux.tone', 'Voice và tone', 'Voice and tone')])

ch('d10', ('Quy trình và cộng tác', 'Process and collaboration'),
   ('Quy trình là công cụ, không phải nghi lễ.\nDesign thinking và design sprint có nhiều biến thể; ghi rõ tác giả của từng biến thể.\nTrình bày quyết định thiết kế cho stakeholder là một kỹ năng thiết kế.', 'Process is a tool, not a ritual.\nDesign thinking and design sprints have many variants; credit the author of each.\nPresenting design decisions to stakeholders is a design skill.'),
   ('Đã xem một biến thể sprint', 'Looked at one sprint variant'), ('Đã trả lời một phản hồi', 'Responded to one piece of feedback'),
   [('sp', ('Các biến thể sprint', 'Sprint variants'), 'author-framework', [
      ('GV: năm ngày — map, sketch, decide, prototype, test với khách hàng thật. [[src:gv-sprint]] Banfield, Lombardo và Wax (sách Design Sprint): Understand, Diverge, Converge, Prototype, Test.', 'GV: five days — map, sketch, decide, prototype, test with real customers. [[src:gv-sprint]] Banfield, Lombardo and Wax (the Design Sprint book): Understand, Diverge, Converge, Prototype, Test.'),
      ('Trả lời stakeholder bằng mục tiêu, dữ liệu và giới hạn là ý tưởng của Tom Greever (Articulating Design Decisions), được diễn đạt lại. Đọc thêm: [[src:nn-designthinking]]', 'Answering stakeholders with goals, data and constraints is Tom Greever\'s idea (Articulating Design Decisions), rephrased. Further reading: [[src:nn-designthinking]]')])],
   [(('Bỏ ngày test để kịp tiến độ thì mất gì?', 'What do you lose by skipping test day to save time?'), ('Bằng chứng từ người dùng.', 'Evidence from users.'), ('Bản mẫu chưa được kiểm chứng.', 'The prototype stays unverified.')),
    (('Design thinking có phải quy trình tuyến tính?', 'Is design thinking a linear process?'), ('Không.', 'No.'), ('Các nhóm thường quay lại pha trước khi học được điều mới.', 'Teams often loop back when they learn something new.'))],
   [('ux.sprint', 'Sprint', 'Sprint'), ('ux.stakeholder', 'Stakeholder', 'Stakeholder')])

def norm(s): return unicodedata.normalize('NFC', s)
# ---- caption sơ đồ ("Bạn đang xem") và nhãn chú giải, thêm 2026-11-21 ----
a('cap.loop', 'Vòng phản hồi của thiết kế: thiết kế tạo ra màn hình, người dùng dùng màn hình, những gì quan sát được quay về sửa thiết kế. Thẻ được nhấn là phần bước này đang xét; câu hỏi và lựa chọn nằm ở bảng bên phải.', 'The design feedback loop: the design produces a screen, people use the screen, what you observe goes back into the design. The highlighted card is the part this step is about; the question and choices are in the panel on the right.')
a('cap.diamond', 'Bốn giai đoạn Double Diamond từ trái sang phải; mũi tên quay lại phía dưới nghĩa là có thể quay về khám phá khi học được điều mới.', 'The four Double Diamond stages from left to right; the arrow looping back underneath means you can return to discovery when you learn something new.')
a('cap.stages', 'Bảy giai đoạn hành động của Norman xếp thành vòng: nửa đầu là thực hiện (mục tiêu → làm), nửa sau là đánh giá (nhận biết → so với mục tiêu). Thẻ viền đỏ là giai đoạn bị hỏng.', "Norman's seven stages of action as a loop: the first half is execution (goal → act), the second half is evaluation (perceive → compare with the goal). A red-bordered card is a broken stage.")
a('cap.create', 'Năm bước CREATE (Stephen Wendel) từ tín hiệu tới đúng lúc hành động; bước bị chặn là chỗ người dùng rơi khỏi luồng.', 'The five CREATE steps (Stephen Wendel) from cue to the right timing; a blocked step is where people drop out.')
a('cap.sprint', 'Năm ngày của design sprint (GV) từ trái sang phải; thẻ nhấn là ngày đang xét.', 'The five days of the design sprint (GV) from left to right; the highlighted card is the day being discussed.')
a('fam.done', 'ổn', 'works')
a('fam.fail', 'hỏng', 'broken')
a('fam.block', 'bị chặn', 'blocked')
a('fam.idle', 'chưa xét', 'not checked yet')

keys = [k for k, _, _ in E]; dup = sorted(set(k for k in keys if keys.count(k) > 1)); assert not dup, dup
for lang, idx in (('vi', 1), ('en', 2)):
    body = ',\n'.join('  %s: %s' % (json.dumps(e[0]), json.dumps(norm(e[idx]), ensure_ascii=False)) for e in E)
    open(os.path.join(ROOT, 'tracks', 'ux', 'content.%s.js' % lang), 'w', encoding='utf-8', newline='\n').write('/* Nội dung track UX (%s). SINH TỰ ĐỘNG từ dev/gen/ux_content.py. */\nADE.addTrackStrings(\'ux\', \'%s\', {\n%s\n});\n' % (lang, lang, body))
print(len(E), 'keys')
