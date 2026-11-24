# Thiết kế hệ thống phía mobile · I9: thông báo đẩy (Phần 2)
# Người dùng (2026-11-24): dịch vụ bên thứ ba như FCM chỉ làm nhẹ, dạy tư duy; tài liệu của chúng đổi liên tục nên không đi sâu API.
# Nguồn: Alex Xu tập 1 ch.10 (bảng thiết bị, không mất phía server, không đúng một lần, khử trùng, opt-out); FCM (overview 4096 byte,
# collapsible: không bảo đảm thứ tự, gộp, quá 100 message chờ thì bỏ; priority: callback vài giây; manage registrations: cũ sau một tháng)
# chỉ làm ví dụ; Android: quyền POST_NOTIFICATIONS. Đọc 2026-11-24.

SEC_ORDER = {'i9': ['hook', 'signal', 'guarantees', 'devices', 'permission', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.push', 'Thiết kế hệ thống · thông báo đổi giờ khám', 'System design · visit time change notifications')
    m = lambda k, vi, en=None: a('m.push.' + k, vi, en)
    m('title', 'Push mang nội dung, hay push chỉ là tín hiệu', 'A push that carries content, or a push that is only a signal')
    m('overview', 'Phòng khám đổi giờ khám của một lịch hẹn hai lần: 9:00 thành 10:00, rồi đổi lại thành 9:30. Điện thoại đang ngủ sâu nên nhận muộn. Bốn tình huống: push mang cả nội dung; push chỉ báo "lịch b42 vừa đổi" để app tự tải bản mới; push bị mất hẳn; push tới hai lần vì server gửi lại sau timeout. Dịch vụ đẩy ở đây nói chung; trên Android thường là FCM.',
      'The clinic changes a booking\'s time twice: 9:00 to 10:00, then back to 9:30. The phone is in deep sleep and receives late. Four situations: the push carries the whole content; the push only says "booking b42 changed" and the app fetches the latest itself; the push is lost entirely; the push arrives twice because the server resent it after a timeout. The push service here is generic; on Android it is usually FCM.')
    m('wrapup', 'Dịch vụ đẩy không bảo đảm thứ tự, không bảo đảm đúng một lần, và không bảo đảm tới. Vì vậy push nên là một tín hiệu đánh thức ("có gì đó đổi, hãy đồng bộ") chứ không phải nơi chứa sự thật. App tải bản mới nhất từ server, khử trùng theo id sự kiện, và đồng bộ cả khi được mở, để push mất hay tới sai thứ tự cũng không làm màn hình sai.',
      'A push service guarantees neither order, nor exactly-once, nor delivery. So a push should be a wake-up signal ("something changed, sync") rather than the place truth lives. The app fetches the latest from the server, dedupes by event ID, and also syncs when opened, so a lost or reordered push cannot make the screen wrong.')
    m('simp.1', 'Các mốc giờ, id lịch b42, id sự kiện e17 và việc push B tới trước push A là minh họa. Chương dùng một dịch vụ đẩy chung; chi tiết API của FCM đổi theo thời gian và cố ý không đi sâu.', 'The times, booking id b42, event id e17 and push B arriving before push A are illustrative. The chapter uses a generic push service; FCM\'s API details change over time and are deliberately not covered in depth.')
    m('simp.2', 'Không mất phía server, không đúng một lần, khử trùng theo id sự kiện, bảng thiết bị theo Alex Xu tập 1; không bảo đảm thứ tự, message gộp, callback chỉ có vài giây theo tài liệu FCM; quyền thông báo theo tài liệu Android. Đọc ngày 2026-11-24.', 'Never losing on the server side, no exactly-once, deduping by event ID and the device table follow Alex Xu vol. 1; no ordering, collapsible messages and the few-second callback follow the FCM docs; the notification permission follows the Android docs. Read on 2026-11-24.')
    m('ctl.hint', 'Đổi tình huống rồi đi lại; so giờ hiện ở bước 4 với giờ thật (9:30).', 'Switch the situation and walk again; compare the time shown at step 4 with the real one (9:30).')
    m('ctl.case', 'Tình huống', 'Situation')
    for k, vi, en in [('payload', 'push mang cả nội dung', 'push carries the content'), ('tickle', 'push chỉ báo có thay đổi', 'push only signals a change'), ('lost', 'push bị mất', 'push is lost'), ('dup', 'push tới hai lần', 'push arrives twice')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Server, dịch vụ đẩy, app', 'Server, push service, app')
    m('diagramDesc', 'Server gửi qua dịch vụ đẩy tới app; app tự tải lại từ server', 'The server sends through the push service to the app; the app fetches from the server itself')
    for k, vi, en in [('srv', 'Server phòng khám', 'Clinic server'), ('push', 'Dịch vụ đẩy (FCM)', 'Push service (FCM)'), ('app', 'App trên điện thoại', 'App on the phone')]:
        m('n.' + k, vi, en)
    m('met.right', 'Giờ hiện đúng 9:30', 'Shows the right time, 9:30'); m('met.shown', 'Thông báo đã hiện', 'Notifications shown'); m('met.fetch', 'Lần app tải từ server', 'App fetches from the server')
    a('cap.push', 'Server bên trái gửi qua dịch vụ đẩy ở giữa tới app bên phải; mũi tên dưới là app tự tải lại.', 'The server on the left sends through the push service in the middle to the app on the right; the lower arrow is the app fetching itself.')
    S = [
        ('payload', 's1', 'Server gửi push A: "Lịch khám đổi sang 10:00"', 'The server sends push A: "Your visit moved to 10:00"', 'Cả nội dung nằm trong push. Điện thoại đang ngủ sâu, chưa nhận.', 'The whole content is in the push. The phone is in deep sleep and has not received it.'),
        ('payload', 's2', 'Server gửi push B: "Lịch khám đổi sang 9:30"; cả hai chờ ở dịch vụ đẩy', 'The server sends push B: "Your visit moved to 9:30"; both wait at the push service', 'Mỗi lần đổi giờ là một push riêng.', 'Each time change is a separate push.'),
        ('payload', 's3', 'Điện thoại thức dậy: nhận B rồi mới nhận A', 'The phone wakes up: receives B, then A', 'Dịch vụ đẩy không bảo đảm thứ tự giao.', 'The push service does not guarantee delivery order.'),
        ('payload', 's4', 'Thông báo cuối cùng ghi 10:00; giờ thật là 9:30', 'The last notification says 10:00; the real time is 9:30', 'App tin vào chữ trong push theo thứ tự tới. Người dùng đến muộn nửa tiếng.', 'The app trusts the push text in arrival order. The patient arrives half an hour late.'),
        ('tickle', 's1', 'Server gửi push: "lịch b42 vừa đổi", không kèm giờ', 'The server sends a push: "booking b42 changed", without the time', 'Push chỉ là tín hiệu, có khóa gộp theo lịch.', 'The push is only a signal, with a collapse key per booking.'),
        ('tickle', 's2', 'Lần đổi thứ hai: push cùng khóa gộp thay push cũ chưa giao', 'Second change: a push with the same collapse key replaces the undelivered one', 'Chỉ còn một push đang chờ.', 'Only one push is left waiting.'),
        ('tickle', 's3', 'Điện thoại nhận một push; app hỏi server bản mới nhất của b42', 'The phone receives one push; the app asks the server for the latest b42', 'Việc tải giao cho WorkManager, vì callback nhận push chỉ có vài giây.', 'The fetch goes to WorkManager, since the push callback only has a few seconds.'),
        ('tickle', 's4', 'Server trả 9:30; app hiện một thông báo đúng', 'The server returns 9:30; the app shows one correct notification', 'Thứ tự push không còn quan trọng, vì sự thật nằm ở server.', 'Push order no longer matters, because the truth lives on the server.'),
        ('lost', 's1', 'Server gửi push: "lịch b42 vừa đổi"', 'The server sends a push: "booking b42 changed"', 'Như cách trên.', 'As before.'),
        ('lost', 's2', 'Push bị bỏ: máy tắt quá lâu, hay quá nhiều push đang chờ', 'The push is dropped: the phone was off too long, or too many pushes were pending', 'Không có gì tới điện thoại, và app không biết.', 'Nothing reaches the phone, and the app does not know.'),
        ('lost', 's3', 'Người dùng tự mở app; app đồng bộ lịch hẹn với server', 'The user opens the app; it syncs bookings with the server', 'Đồng bộ khi mở app là con đường thứ hai, không phụ thuộc push.', 'Syncing on open is a second path that does not depend on push.'),
        ('lost', 's4', 'Màn hình hiện 9:30', 'The screen shows 9:30', 'Không có thông báo, nhưng màn hình không sai. Với lời nhắc quan trọng, server có thể gửi thêm kênh khác (SMS).', 'No notification, but the screen is not wrong. For critical reminders the server can add another channel (SMS).'),
        ('dup', 's1', 'Server gửi push sự kiện e17: "nhắc khám lúc 9:30"', 'The server sends push for event e17: "visit at 9:30"', 'Push có id sự kiện.', 'The push carries an event ID.'),
        ('dup', 's2', 'Server không nhận được xác nhận (timeout) nên gửi lại e17', 'The server gets no acknowledgement (timeout), so it resends e17', 'Giống chương I5: không biết request mất hay response mất.', 'Like chapter I5: it cannot tell a lost request from a lost response.'),
        ('dup', 's3', 'Điện thoại nhận e17 hai lần', 'The phone receives e17 twice', 'Lần gửi đầu thật ra đã tới.', 'The first send had in fact arrived.'),
        ('dup', 's4', 'App thấy e17 đã có trong database: bỏ lần hai, chỉ hiện một thông báo', 'The app finds e17 already in its database: drops the second, shows one notification', 'Khử trùng phải sống qua process bị giết, nên lưu trong database chứ không trong bộ nhớ.', 'Deduplication must survive process death, so it lives in the database, not in memory.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi tình huống; ở bước 4 so giờ hiện với 9:30, và xem hàng được tô ở bảng dưới.', 'Walk all four steps of each situation; at step 4 compare the time shown with 9:30, and see which row is highlighted in the lower table.'),
        ('payload.s2', 'Alex Xu (tập 1): thông báo có thể trễ hay đảo thứ tự, nhưng không được mất; phía server lưu lại và thử lại. [[src:book-xu1]]', 'Alex Xu: notifications may be delayed or reordered, but never lost; the server persists and retries. [[src:book-xu1]]'),
        ('payload.s3', 'Tài liệu FCM nói rõ không bảo đảm thứ tự giao message. [[src:fcm-collapsible]]', 'The FCM docs state that message delivery order is not guaranteed. [[src:fcm-collapsible]]'),
        ('payload.s4', 'Push còn giới hạn kích thước (với FCM là 4096 byte), thêm một lý do để không đặt dữ liệu thật vào đó. [[src:fcm-overview]]', 'Pushes also have a size limit (4096 bytes for FCM), one more reason not to put real data there. [[src:fcm-overview]]'),
        ('tickle.s2', 'FCM: message gộp được thay message cũ cùng khóa chưa giao; hợp với tín hiệu "có thay đổi". [[src:fcm-collapsible]]', 'FCM: a collapsible message replaces an undelivered older one with the same key; a good fit for "something changed" signals. [[src:fcm-collapsible]]'),
        ('tickle.s3', 'FCM: callback nhận message chỉ có vài giây; việc lâu hơn giao cho WorkManager. [[src:fcm-priority]]', 'FCM: the message callback only has a few seconds; longer work goes to WorkManager. [[src:fcm-priority]]'),
        ('tickle.s4', 'Cùng ý với chương I6 và track Kiến trúc (G4): server, rồi database của app, là nguồn sự thật; push chỉ báo lúc nên đồng bộ.', 'Same idea as chapter I6 and the Architecture track (G4): the server, then the app\'s database, is the source of truth; a push only says when to sync.'),
        ('lost.s2', 'FCM: trên Android, quá nhiều message không gộp được đang chờ thì bỏ hết và app phải đồng bộ lại toàn bộ. [[src:fcm-collapsible]]', 'FCM: on Android, too many pending non-collapsible messages are all discarded and the app must do a full resync. [[src:fcm-collapsible]]'),
        ('lost.s3', 'Mở app là lúc chắc chắn có mạng và người dùng đang nhìn: luôn đồng bộ ở đây, đừng chỉ dựa vào push.', 'Opening the app is when there is a network and the user is looking: always sync there, do not rely on push alone.'),
        ('lost.s4', 'Alex Xu (tập 1) thiết kế hệ thống thông báo nhiều kênh: push, SMS, email; mỗi kênh có thể hỏng riêng. [[src:book-xu1]]', 'Alex Xu designs a multi-channel notification system: push, SMS, email; each can fail on its own. [[src:book-xu1]]'),
        ('dup.s2', 'Gửi lại sau timeout là đúng (không được mất), nhưng có giá: phía nhận có thể thấy hai lần.', 'Resending after a timeout is right (never lose), but it has a price: the receiver may see it twice.'),
        ('dup.s3', 'Alex Xu (tập 1): thông báo không bảo đảm đúng một lần; phần lớn chỉ tới một lần, nhưng hệ phân tán có thể tạo bản trùng. [[src:book-xu1]]', 'Alex Xu: notifications are not exactly-once; most arrive once, but a distributed system can create duplicates. [[src:book-xu1]]'),
        ('dup.s4', 'Alex Xu (tập 1): khử trùng bằng id sự kiện, đã thấy thì bỏ. Đây là cùng ý với idempotency key ở chương I5, áp ở phía nhận. [[src:book-xu1]]', 'Alex Xu: dedupe by event ID, drop it if seen. The same idea as the idempotency key in chapter I5, applied on the receiving side. [[src:book-xu1]]')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.pu', 'Sơ đồ tuần tự và các bảo đảm', 'Sequence and guarantees')
    z('pu.cap', 'Sơ đồ tuần tự: mỗi hàng là một tin theo thời gian, từ trên xuống. Mũi tên đậm: bước hiện tại. Mũi tên đỏ đứt: chỗ thông tin sai.', 'Sequence diagram: each row is one message in time, top to bottom. Bold arrows: the current step. Red dashed arrow: where the information goes wrong.')
    for k, vi, en in [('srv', 'Server phòng khám', 'Clinic server'), ('push', 'Dịch vụ đẩy', 'Push service')]:
        z('pu.p.' + k, vi, en)
    z('pu.p.app', 'App trên máy', 'App')
    for k, vi, en in [
        ('sendA', 'push A: "đổi sang 10:00"', 'push A: "moved to 10:00"'), ('sendB', 'push B: "đổi sang 9:30"', 'push B: "moved to 9:30"'), ('hold', 'máy ngủ: giữ cả hai', 'phone asleep: holds both'),
        ('gotB', 'B tới trước', 'B arrives first'), ('gotA', 'A tới sau', 'A arrives second'), ('showA', 'hiện "10:00" (sai)', 'shows "10:00" (wrong)'),
        ('tickA', '"b42 vừa đổi"', '"b42 changed"'), ('tickB', '"b42 vừa đổi" (cùng khóa)', '"b42 changed" (same key)'), ('collapse', 'gộp: còn một', 'collapsed: one left'),
        ('gotT', '"b42 vừa đổi"', '"b42 changed" arrives'), ('fetch', 'GET /bookings/b42', 'GET /bookings/b42 (sync)'), ('latest', '9:30 (bản mới nhất)', '9:30 (latest version)'),
        ('drop', 'push bị bỏ', 'push dropped'), ('open', 'người dùng mở app', 'the user opens the app'),
        ('sendE', 'push e17', 'push e17 sent'), ('timeout', 'không có xác nhận: timeout', 'no acknowledgement: timeout'), ('resend', 'gửi lại e17', 'resend e17'),
        ('gotE', 'e17', 'e17 arrives'), ('gotE2', 'e17 lần hai', 'e17 again'), ('dedupe', 'e17 đã thấy: bỏ', 'e17 seen: dropped')]:
        z('pu.m.' + k, vi, en)
    z('pu.gcap', 'Dịch vụ đẩy không bảo đảm gì, và thiết kế đáp lại thế nào. Hàng tô là hàng tình huống này cho thấy.', 'What a push service does not guarantee, and how the design responds. The highlighted row is the one this situation shows.')
    for k, vi, en in [('what', 'Câu hỏi', 'Question'), ('no', 'Dịch vụ đẩy', 'Push service'), ('do', 'Thiết kế đáp lại', 'Design response')]:
        z('pu.gcol.' + k, vi, en)
    for k, q, qe, no, noe, do, doe in [
        ('order', 'Tới đúng thứ tự?', 'Arrives in order?', 'không bảo đảm', 'not guaranteed', 'push chỉ báo có thay đổi; giờ thật lấy từ server', 'the push only signals; the real time comes from the server'),
        ('once', 'Tới đúng một lần?', 'Arrives exactly once?', 'không bảo đảm', 'not guaranteed either', 'khử trùng theo id sự kiện, lưu trong database', 'dedupe by event ID, stored in the database'),
        ('arrive', 'Chắc chắn tới?', 'Always arrives?', 'không: máy tắt lâu, quá nhiều push chờ, ID đăng ký cũ', 'no: phone off for long, too many pending, stale registration', 'đồng bộ khi mở app; lời nhắc quan trọng dùng thêm kênh khác', 'sync on open; add another channel for critical reminders'),
        ('size', 'Chứa được bao nhiêu?', 'How much fits?', 'vài KB (FCM: 4096 byte)', 'a few KB (FCM: 4096 bytes)', 'chỉ gửi loại và id; nội dung tải sau', 'send only a type and an id; fetch the content later'),
        ('when', 'Tới lúc nào?', 'When does it arrive?', 'có thể trễ khi máy ngủ sâu (Doze, chương I4)', 'may be late while the phone sleeps (Doze, chapter I4)', 'không dùng push để báo giờ chính xác tới từng phút', 'do not use push for minute-exact timing')]:
        z('pu.g.' + k, q, qe); z('pu.g.%s.no' % k, no, noe); z('pu.g.%s.do' % k, do, doe)
    z('pu.legend', 'Viền cam ở bảng: điều không được bảo đảm mà tình huống này chạm tới. Cột phải: cách thiết kế đáp lại.', 'Orange outline in the table: the missing guarantee this situation touches. Right column: how the design responds.')

    C = 'i9'
    a(C + '.title', 'Thông báo đẩy: tín hiệu, không phải dữ liệu', 'Push notifications: signals, not data')
    a(C + '.essence', 'Dịch vụ đẩy (trên Android thường là FCM) không bảo đảm thứ tự, không bảo đảm đúng một lần, không bảo đảm tới, và chỉ chứa vài KB.\nVì vậy push nên là tín hiệu "có gì đó đổi, hãy đồng bộ"; sự thật nằm ở server. App tải bản mới nhất, khử trùng theo id sự kiện, và đồng bộ cả khi được mở.\nServer giữ danh sách thiết bị của từng người, cập nhật ID mỗi lần app gửi lên và bỏ những ID đã lâu không hoạt động; app xin quyền thông báo vào lúc người dùng thấy lý do.',
      'A push service (on Android usually FCM) guarantees neither order, nor exactly-once, nor delivery, and holds only a few KB.\nSo a push should be a signal, "something changed, sync"; the truth lives on the server. The app fetches the latest, dedupes by event ID, and also syncs when opened.\nThe server keeps each user\'s device list, refreshes an ID whenever the app uploads it and drops IDs inactive for long; the app asks for notification permission when the user can see why.')
    a(C + '.goal.g1', 'Đã thấy push tới điện thoại', 'Saw the push reach the phone')
    a(C + '.goal.g2', 'Đã thấy giờ cuối cùng hiện ra', 'Saw the final time shown')
    a(C + '.sim.sysdesign.push', 'push mang nội dung, push chỉ báo thay đổi, push mất, push trùng', 'push with content, push as signal, lost push, duplicate push')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Server gửi hai push liên tiếp: "giờ khám 10:00" rồi "giờ khám 9:30". Điện thoại đang ngủ, nhận cả hai một lúc sau. Thông báo cuối người dùng thấy ghi giờ nào? Bạn sửa thiết kế ra sao để câu trả lời luôn đúng?',
      'The server sends two pushes in a row: "visit at 10:00", then "visit at 9:30". The phone is asleep and receives both later. Which time does the last notification show? How would you change the design so it is always right?')
    B(C, S_, 1, 'ans', 'Không biết được: dịch vụ đẩy không bảo đảm thứ tự, nên có thể là 10:00. Sửa bằng cách để push chỉ báo "lịch b42 vừa đổi" và app tải giờ thật từ server; thứ tự push khi đó không còn quan trọng. [[src:fcm-collapsible]]',
      'You cannot know: the push service does not guarantee order, so it may be 10:00. Fix it by making the push only say "booking b42 changed" and having the app fetch the real time from the server; then push order no longer matters. [[src:fcm-collapsible]]')

    S_ = 'signal'
    a(C + '.sec.%s.title' % S_, 'Push là tín hiệu đánh thức', 'A push is a wake-up signal')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Ở chương I4, push thắng các kênh khác vì một kết nối dùng chung cho cả máy, sống được khi máy ngủ. Cái giá là app không kiểm soát được kênh đó: không quyết định thứ tự, thời điểm, hay việc có tới hay không. Cách nghĩ hợp lý: push nói "có gì đó đổi", còn "đổi thành gì" thì app hỏi server, nơi giữ sự thật. Đây là diễn giải của site, nhất quán với chương I6 và track Kiến trúc (G4).',
      'In chapter I4, push beat the other channels because one shared connection serves the whole device and survives sleep. The price is that the app does not control that channel: not the order, the timing, or whether it arrives. The sensible way to think: a push says "something changed", and "changed to what" is asked of the server, which holds the truth. This is the site\'s interpretation, consistent with chapter I6 and the Architecture track (G4).')
    B(C, S_, 2, 'p', 'Hai chi tiết thực tế, lấy FCM làm ví dụ. Callback nhận push chỉ có vài giây, nên việc tải giao cho WorkManager. Push cùng khóa gộp thay push cũ chưa giao, nên mười lần đổi một lịch chỉ còn một tín hiệu. Tên API cụ thể đổi theo phiên bản SDK; khi làm thật, đọc tài liệu hiện hành. [[src:fcm-priority]] [[src:fcm-collapsible]]',
      'Two practical details, with FCM as the example. The push callback only gets a few seconds, so the fetch goes to WorkManager. A push with the same collapse key replaces an undelivered older one, so ten changes to one booking leave a single signal. Exact API names change with SDK versions; read the current docs when you build it. [[src:fcm-priority]] [[src:fcm-collapsible]]')

    S_ = 'guarantees'
    a(C + '.sec.%s.title' % S_, 'Ba điều không được bảo đảm', 'Three things not guaranteed')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Thứ tự: không bảo đảm. Đúng một lần: Alex Xu (tập 1) nói thẳng là không; phần lớn tới một lần nhưng hệ phân tán có thể tạo bản trùng, nên khử trùng bằng id sự kiện. Tới nơi: không; máy tắt lâu, quá nhiều push chờ, hay ID đăng ký đã cũ đều làm push không tới. Sách đặt yêu cầu ngược lại cho phía server: thông báo có thể trễ hay đảo thứ tự nhưng không được mất, nên server lưu và thử lại. [[src:book-xu1]] [[src:fcm-collapsible]]',
      'Order: not guaranteed. Exactly once: Alex Xu says plainly no; most arrive once but a distributed system can create duplicates, so dedupe by event ID. Delivery: no; a phone off for long, too many pending pushes, or a stale registration ID all stop a push. The book puts the opposite requirement on the server: notifications may be delayed or reordered but never lost, so the server persists and retries. [[src:book-xu1]] [[src:fcm-collapsible]]')
    B(C, S_, 2, 'note', 'Server gửi lại để không mất, app khử trùng để không hiện hai lần: đây là cặp "ít nhất một lần + idempotent" của chương I5, nhìn từ phía nhận.',
      'The server resends so nothing is lost, the app dedupes so nothing shows twice: the "at least once + idempotent" pair from chapter I5, seen from the receiving side.')
    B(C, S_, 2, 'kind', 'mechanism')

    S_ = 'devices'
    a(C + '.sec.%s.title' % S_, 'Một người, nhiều thiết bị, ID đổi theo thời gian', 'One user, many devices, IDs that change')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Alex Xu (tập 1): server thu ID thiết bị khi người dùng cài app hay đăng ký, lưu trong một bảng thiết bị riêng, vì một người có thể có nhiều thiết bị và push được gửi tới tất cả. ID đó không cố định: cài lại app, xóa dữ liệu, hay khôi phục sang máy mới đều có thể tạo ID mới. [[src:book-xu1]]',
      'Alex Xu: the server collects device IDs when the user installs or signs up and stores them in a separate device table, since one user may have many devices and pushes go to all of them. The ID is not fixed: reinstalling, clearing data or restoring onto a new phone can all produce a new one. [[src:book-xu1]]')
    B(C, S_, 2, 'p', 'Hệ quả cho thiết kế: app gửi ID lên mỗi khi nhận được (không chỉ một lần lúc đăng nhập), server lưu kèm thời điểm và bỏ những ID lâu không hoạt động. Lấy FCM làm ví dụ: mặc định coi một đăng ký là cũ khi app không kết nối một tháng, và push tới đó khó bao giờ tới. [[src:fcm-tokens]]',
      'For the design: the app uploads its ID whenever it gets one (not only once at login), and the server stores it with a timestamp and drops IDs inactive for long. With FCM as the example: by default a registration is stale after a month without connecting, and pushes to it are unlikely to ever arrive. [[src:fcm-tokens]]')

    S_ = 'permission'
    a(C + '.sec.%s.title' % S_, 'Quyền thông báo: hỏi đúng lúc', 'Notification permission: ask at the right moment')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', 'Từ Android 13 (API 33), app cần quyền chạy POST_NOTIFICATIONS để hiện thông báo; với app mới cài, thông báo tắt mặc định. Push vẫn tới máy, nhưng không hiện gì. Tài liệu khuyên hỏi vào lúc người dùng tự chọn, như sau khi đặt lịch ("Nhắc tôi 1 giờ trước giờ khám?"), và giải thích lý do trước, thay vì hỏi ngay lần mở đầu tiên. [[src:ax-notif-perm]]',
      'From Android 13 (API 33), an app needs the POST_NOTIFICATIONS runtime permission to show notifications; for newly installed apps they are off by default. Pushes still reach the device, but nothing shows. The docs advise asking at a user-driven moment, such as right after booking ("Remind me 1 hour before the visit?"), and explaining why first, rather than on the very first launch. [[src:ax-notif-perm]]')
    B(C, S_, 2, 'note', 'Alex Xu (tập 1) cũng đặt việc tôn trọng lựa chọn tắt thông báo vào thiết kế server: kiểm tra người dùng có đồng ý nhận loại thông báo đó không trước khi gửi. [[src:book-xu1]]',
      'Alex Xu also builds respect for opt-outs into the server design: check that the user agreed to that type of notification before sending. [[src:book-xu1]]')
    B(C, S_, 2, 'kind', 'android')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Đổi sang điện thoại mới, người dùng không còn nhận nhắc lịch.', 'After moving to a new phone, the user no longer gets reminders.')
    B(C, S_, 1, 'cause', 'App chỉ gửi ID lên một lần và ghi cờ "đã gửi" vào SharedPreferences; bản sao lưu khôi phục cờ đó sang máy mới, nên ID mới không bao giờ được gửi. Server vẫn gửi tới ID của máy cũ.', 'The app uploaded its ID once and saved an "already sent" flag in SharedPreferences; the backup restored that flag onto the new phone, so the new ID was never sent. The server keeps sending to the old phone\'s ID.')
    B(C, S_, 1, 'fix', 'Gửi ID mỗi khi app nhận được ID (kể cả khi trùng), server lưu kèm thời điểm; dọn ID cũ. Xem thêm sao lưu ở track Lưu dữ liệu (H9). [[src:fcm-tokens]]', 'Upload the ID whenever the app receives one (even if unchanged), with the server storing a timestamp; prune old IDs. See backups in the Saving Data track (H9). [[src:fcm-tokens]]')
    B(C, S_, 2, 'bug', 'Thông báo nhắc lịch hiện ảnh bác sĩ, nhưng thỉnh thoảng không hiện gì cả.', 'Reminder notifications show the doctor\'s photo, but sometimes nothing shows at all.')
    B(C, S_, 2, 'cause', 'App tải ảnh ngay trong callback nhận push rồi mới hiện; mạng chậm thì vượt vài giây cho phép và bị dừng giữa chừng.', 'The app downloads the photo inside the push callback before showing; on a slow network it exceeds the few seconds allowed and is stopped midway.')
    B(C, S_, 2, 'fix', 'Hiện thông báo ngay với nội dung tối thiểu, giao việc tải ảnh cho WorkManager rồi cập nhật thông báo. [[src:fcm-priority]]', 'Show the notification at once with minimal content, hand the photo download to WorkManager, then update the notification. [[src:fcm-priority]]')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Thiết kế thông báo cho ba sự kiện: (a) kết quả xét nghiệm đã có; (b) bác sĩ nhắn tin trong cuộc trò chuyện; (c) nhắc khám 1 giờ trước. Với mỗi cái: push mang gì, app làm gì khi nhận, và cần đường dự phòng nào nếu push không tới?',
      'Design notifications for three events: (a) lab results are ready; (b) the doctor sends a chat message; (c) a reminder 1 hour before a visit. For each: what does the push carry, what does the app do on receipt, and what fallback is needed if the push never arrives?')
    B(C, S_, 1, 'hint', 'Cái nào nhạy cảm? Cái nào phải đúng giờ? Cái nào có thể tới nhiều lần?', 'Which is sensitive? Which must be on time? Which can arrive many times?')
    B(C, S_, 1, 'sol', '(a) Chỉ "có kết quả mới" và id, không bao giờ kèm kết quả (nhạy cảm, và thông báo có thể hiện trên màn hình khóa); app tải sau khi người dùng mở và xác thực; dự phòng: đồng bộ khi mở app. (b) Chỉ id cuộc trò chuyện, gộp theo cuộc trò chuyện; app tải tin mới, khử trùng theo id tin; dự phòng: đồng bộ khi mở. (c) Đừng dựa vào push để đúng giờ: khi đặt lịch, app tự hẹn giờ nhắc trên máy, còn push chỉ để báo lịch đã đổi; lời nhắc quan trọng có thể thêm SMS từ server.',
      '(a) Only "new results" and an id, never the results themselves (sensitive, and notifications can show on the lock screen); the app fetches after the user opens and authenticates; fallback: sync on open. (b) Only the conversation id, collapsed per conversation; the app fetches new messages and dedupes by message id; fallback: sync on open. (c) Do not rely on push for timing: when booking, the app schedules the reminder on the device, and push only signals that the booking changed; critical reminders can add an SMS from the server.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Theo yêu cầu của người học, chương chỉ dạy cách nghĩ về push và dùng FCM làm ví dụ, vì API của dịch vụ bên thứ ba đổi liên tục. Không mất phía server, không đúng một lần, khử trùng, bảng thiết bị, opt-out theo Alex Xu tập 1; không bảo đảm thứ tự, gộp message, giới hạn 4096 byte, callback vài giây, ID cũ sau một tháng theo tài liệu FCM; quyền POST_NOTIFICATIONS theo tài liệu Android; đọc ngày 2026-11-24, diễn đạt lại. Mốc giờ, id, việc B tới trước A, lỗi cờ "đã gửi" bị khôi phục và lời giải bài tập là của site. Chương không bàn loại message, kênh thông báo, hay cách cấu hình SDK.',
      'At the learner\'s request, the chapter teaches only how to think about push and uses FCM as an example, since third-party APIs change constantly. Never losing on the server, no exactly-once, deduping, the device table and opt-outs follow Alex Xu vol. 1; no ordering, collapsing, the 4096-byte limit, the few-second callback and stale IDs after a month follow the FCM docs; POST_NOTIFICATIONS follows the Android docs; read on 2026-11-24, paraphrased. The times, ids, B arriving before A, the restored "already sent" flag bug and the exercise answers are the site\'s. The chapter does not cover message types, notification channels, or SDK configuration.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Vì sao không nên đặt giờ khám mới vào nội dung push?', 'Why not put the new visit time in the push content?', 'Push không bảo đảm thứ tự hay đúng một lần, nên giá trị cũ có thể tới sau giá trị mới.', 'Pushes guarantee neither order nor exactly-once, so an older value can arrive after the newer one.', 'Để push chỉ báo có thay đổi, giờ thật lấy từ server.', 'Let the push signal a change and fetch the real time from the server.'),
        ('q2', 'Push bị mất. Làm sao màn hình vẫn đúng?', 'A push is lost. How does the screen stay right?', 'App đồng bộ với server khi được mở, không chỉ khi có push.', 'The app syncs with the server when opened, not only on a push.', 'Push là đường tắt, không phải đường duy nhất.', 'Push is a shortcut, not the only path.'),
        ('q3', 'Cùng một push tới hai lần. App nên làm gì?', 'The same push arrives twice. What should the app do?', 'Khử trùng theo id sự kiện, lưu trong database để sống qua process bị giết.', 'Dedupe by event ID, kept in the database so it survives process death.', 'Không có giao đúng một lần.', 'There is no exactly-once delivery.'),
        ('q4', 'Khi nào app nên gửi ID thiết bị lên server?', 'When should the app upload its device ID?', 'Mỗi khi nhận được ID, kể cả khi không đổi; server lưu kèm thời điểm.', 'Whenever it receives one, even if unchanged; the server stores a timestamp.', 'ID đổi khi cài lại, xóa dữ liệu, hay khôi phục sang máy mới.', 'IDs change on reinstall, data clearing, or restoring onto a new phone.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
