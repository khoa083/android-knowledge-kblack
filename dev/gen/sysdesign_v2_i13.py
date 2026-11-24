# Thiết kế hệ thống phía mobile · I13: bài mẫu — app nhắn tin với phòng khám (Phần 2)
# Nguồn: Alex Xu tập 1 ch.12 (message_id duy nhất, tăng theo thời gian; cur_max_message_id; push khi offline), Zhiyong Tan, Acing ch.14
# (xác nhận đã nhận, đã xem; ghi ở message service trước; phía nhận kiểm tra trùng). Gom các chương I2, I4, I5, I7, I8, I9. Đọc 2026-11-24.

SEC_ORDER = {'i13': ['hook', 'reqs', 'arch', 'send', 'receive', 'map', 'ex']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.chat', 'Thiết kế hệ thống · một tin nhắn từ lúc gõ tới "đã xem"', 'System design · one message from typing to "seen"')
    m = lambda k, vi, en=None: a('m.chat.' + k, vi, en)
    m('title', 'Một tin nhắn đi qua cả hệ thống', 'One message through the whole system')
    m('overview', 'Người bệnh nhắn phòng khám: "Tôi đến muộn 10 phút". Theo dõi tin đó qua sáu bước: gõ và bấm gửi, chờ mạng, server nhận, giao cho người nhận, người nhận đọc, máy tính bảng của người gửi đồng bộ. Ba tình huống: mọi thứ có mạng; người gửi mất mạng và response đầu bị mất; app của người nhận đang tắt.',
      'A patient messages the clinic: "I will be 10 minutes late". Follow that message through six steps: type and tap send, wait for the network, the server receives it, delivery to the recipient, the recipient reads it, the sender\'s tablet syncs. Three situations: everything online; the sender offline with the first response lost; the recipient\'s app closed.')
    m('wrapup', 'Một tin nhắn chạm tới gần hết các chương trước. Ghi vào outbox trên đĩa trước rồi mới gửi, để sống qua process chết (I2). Gửi bằng WorkManager với khóa chống trùng, để thử lại an toàn (I5). Server cấp message_id tăng dần làm thứ tự (I7). Người nhận online thì nhận qua kết nối sống, offline thì push chỉ báo rồi app tự tải (I4, I9). Mỗi thiết bị đồng bộ theo message_id lớn nhất đã có (I8).',
      'One message touches almost every earlier chapter. Write it to an on-disk outbox before sending, to survive process death (I2). Send with WorkManager and a duplicate-send key, so retries are safe (I5). The server assigns an increasing message_id as the order (I7). An online recipient gets it over a live connection; offline, a push only signals and the app fetches (I4, I9). Each device syncs from the highest message_id it has (I8).')
    m('simp.1', 'Thành phần app, sáu bước và ba tình huống là sơ đồ của site, không phải kiến trúc của một app cụ thể. Không bàn mã hóa đầu cuối (chỉ hai đầu đọc được tin), nhóm chat, trạng thái online (ai đang trực tuyến) hay tìm kiếm tin.', 'The app components, six steps and three situations are the site\'s sketch, not any specific app\'s architecture. End-to-end encryption (only the two ends can read the message), group chats, presence (who is online) and message search are not covered.')
    m('simp.2', 'message_id 812, clientId 7f3… và các mốc thời gian chỉ là ví dụ minh họa; app nhắn tin thật còn nhiều chi tiết khác (tin sửa, tin xóa, tin rất lớn) mà mô phỏng bỏ qua.', 'message_id 812, clientId 7f3… and the times are only illustrative; a real messaging app has many more details (edited messages, deleted messages, very large messages) that the simulation leaves out.')
    m('ctl.hint', 'Đổi tình huống rồi đi lại; nhìn thành phần nào sáng ở đồ thị và dấu tick ở mỗi bước.', 'Switch the situation and walk again; watch which components light up and the tick marks at each step.')
    m('ctl.case', 'Tình huống', 'Situation')
    for k, vi, en in [('online', 'mọi thứ có mạng', 'everything online'), ('offline', 'người gửi mất mạng, mất response', 'sender offline, response lost'), ('away', 'app người nhận đang tắt', 'recipient app closed')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Điện thoại người gửi, server, máy người nhận', 'Sender phone, server, recipient device')
    m('diagramDesc', 'Tin đi từ điện thoại người gửi qua server tới máy người nhận', 'The message goes from the sender\'s phone through the server to the recipient\'s device')
    for k, vi, en in [('phone', 'Điện thoại người gửi', 'Sender phone'), ('server', 'Server tin nhắn', 'Message server'), ('peer', 'Máy phòng khám', 'Clinic device')]:
        m('n.' + k, vi, en)
    m('met.ticks', 'Dấu tick (0 tới 3)', 'Ticks (0 to 3)'); m('met.copies', 'Bản tin trên server', 'Copies on the server'); m('met.devices', 'Máy người gửi đã có tin', 'Sender devices with it')
    a('cap.chat', 'Điện thoại bên trái gửi qua server ở giữa tới máy phòng khám bên phải.', 'The phone on the left sends through the server in the middle to the clinic device on the right.')
    common = {
        's1': ('Gõ "Tôi đến muộn 10 phút", bấm gửi: ghi vào outbox, hiện đồng hồ chờ', 'Type "I will be 10 minutes late", tap send: written to the outbox, a clock icon shows', 'Tin nằm trên đĩa trước khi đi đâu cả, kèm một clientId (mã ngẫu nhiên app sinh cho mỗi tin).', 'The message is on disk before going anywhere, with a random clientId (a code the app generates for each message).'),
        's4': ('Server giao cho máy phòng khám; máy đó báo đã nhận: hai tick', 'The server delivers to the clinic device; it confirms receipt: two ticks', 'Máy nhận kiểm tra message_id đã có chưa trước khi hiện.', 'The receiver checks whether it already has that message_id before showing it.'),
        's5': ('Lễ tân đọc tin; read receipt về người gửi: đã xem', 'The receptionist reads it; a read receipt goes back: seen', 'Chỉ cần gửi message_id lớn nhất đã đọc, không cần từng tin một (gợi ý của site).', 'Sending the highest message_id read is enough, not one receipt per message (the site\'s suggestion).'),
        's6': ('Máy tính bảng của người gửi mở app: tải các tin sau cur_max_message_id', 'The sender\'s tablet opens the app: fetches messages after cur_max_message_id', 'cur_max_message_id là message_id lớn nhất máy này đã có. Tin vừa gửi từ điện thoại hiện trên máy tính bảng, đúng thứ tự.', 'cur_max_message_id is the highest message_id this device already has. The message just sent from the phone appears on the tablet, in order.')}
    S = []
    for c in ['online', 'offline', 'away']:
        S.append((c, 's1') + common['s1'])
    S += [
        ('online', 's2', 'Có mạng: WorkManager chạy việc gửi ngay', 'Online: WorkManager runs the send job at once', 'Ràng buộc "có mạng" (điều kiện để việc được chạy) thỏa nên không phải chờ.', 'The "network" constraint (a condition for the job to run) is met, so there is no wait.'),
        ('online', 's3', 'POST /messages kèm khóa clientId; server cấp message_id 812: một tick', 'POST /messages with the clientId key; the server assigns message_id 812: one tick', 'Tin chuyển từ outbox sang bảng tin đã gửi.', 'The message moves from the outbox to the sent messages table.'),
        ('online', 's4') + common['s4'], ('online', 's5') + common['s5'], ('online', 's6') + common['s6'],
        ('offline', 's2', 'Mất mạng: việc gửi chờ, tin vẫn hiện đồng hồ', 'Offline: the send job waits, the message still shows a clock', 'Người dùng có thể tắt app; outbox trên đĩa vẫn còn.', 'The user may close the app; the on-disk outbox remains.'),
        ('offline', 's3', 'Có mạng lại: POST, server lưu, response bị mất; thử lại cùng khóa: server trả lại 812', 'Back online: POST, the server stores it, the response is lost; retry with the same key: the server returns 812 again', 'Không có bản tin thứ hai: khóa chống trùng làm việc thử lại an toàn.', 'No second copy: the duplicate-send key makes the retry safe.'),
        ('offline', 's4') + common['s4'], ('offline', 's5') + common['s5'], ('offline', 's6') + common['s6'],
        ('away', 's2', 'Có mạng: WorkManager chạy việc gửi', 'Online: WorkManager runs the send job', 'Như trường hợp đầu.', 'As in the first case.'),
        ('away', 's3', 'Server nhận, cấp message_id 812: một tick', 'The server receives it and assigns message_id 812: one tick', 'Tin đã an toàn trên server dù người nhận chưa có mạng.', 'The message is safe on the server even though the recipient is not connected.'),
        ('away', 's4', 'Máy phòng khám không có kết nối sống: push chỉ báo "có tin mới", app tự tải: hai tick', 'The clinic device has no live connection: a push only says "new message", the app fetches: two ticks', 'Push không mang nội dung tin; nội dung tải từ server theo cur_max_message_id.', 'The push carries no message content; the content is fetched from the server by cur_max_message_id.'),
        ('away', 's5') + common['s5'], ('away', 's6') + common['s6']]
    for row in S:
        case, k, tv, te, xv, xe = row
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    co = {
        's2': ('Chương I2, "Tiến trình, bộ nhớ và cái chết của process": process có thể bị giết khi app ở nền; tin nằm trong outbox trên đĩa nên không mất.', 'Chapter I2, "Processes, memory and process death": the process may be killed in the background; the message is in the on-disk outbox, so it is not lost.'),
        's4': ('Zhiyong Tan nêu: phía nhận kiểm tra tin có trùng không rồi mới hiện, và gửi xác nhận đã nhận về người gửi. [[src:book-acing]]', 'Zhiyong Tan notes: the receiver checks for duplicates before showing, and sends a delivery confirmation back to the sender. [[src:book-acing]]'),
        's5': ('Zhiyong Tan nêu: khi người dùng đọc tin, app gửi read receipt (báo đã xem) về người gửi, giao theo cùng cách. [[src:book-acing]]', 'Zhiyong Tan notes: when the user reads the message, the app sends a read receipt (a "seen" notice) to the sender, delivered the same way. [[src:book-acing]]'),
        's6': ('Alex Xu nêu: mỗi thiết bị giữ cur_max_message_id; tin mới là tin có message_id lớn hơn số đó. [[src:book-xu1]]', 'Alex Xu notes: each device keeps cur_max_message_id; new messages are those with a larger message_id. [[src:book-xu1]]')}
    for c in ['online', 'offline', 'away']:
        m('co.%s.s2' % c, *co['s2'])
        m('co.%s.s4' % c, *co['s4']) if c != 'away' else None
        m('co.%s.s5' % c, *co['s5']); m('co.%s.s6' % c, *co['s6'])
    m('co.try', 'Đi hết sáu bước; ở mỗi bước nhìn thành phần nào sáng trên đồ thị và dòng mới trên sơ đồ tuần tự.', 'Walk all six steps; at each, watch which components light up and the new rows in the sequence diagram.')
    m('co.online.s3', 'Alex Xu nêu: message_id phải duy nhất và tăng theo thời gian; không dựa vào created_at (cột ghi giờ tạo tin) vì hai tin có thể cùng lúc. [[src:book-xu1]]', 'Alex Xu notes: message_id must be unique and sortable by time; do not rely on created_at (the column holding the creation time), as two messages can share it. [[src:book-xu1]]')
    m('co.offline.s3', 'Chương I5, "Mạng không tin cậy: timeout, thử lại, idempotency": không biết request mất hay response mất; thử lại với cùng khóa thì server trả lại kết quả cũ thay vì tạo bản mới.', 'Chapter I5, "Unreliable networks: timeouts, retries, idempotency": you cannot tell a lost request from a lost response; retrying with the same key makes the server return the old result instead of a new copy.')
    m('co.away.s3', 'Zhiyong Tan nêu: tin được ghi ở message service (dịch vụ nhận và lưu tin) trước; giao không được thì bỏ, vì máy sẽ lấy lại sau. [[src:book-acing]]', 'Zhiyong Tan notes: the message is recorded in the message service (the service that receives and stores messages) first; undeliverable sends are dropped, since the device fetches later. [[src:book-acing]]')
    m('co.away.s4', 'Alex Xu nêu: người nhận offline thì server gửi thông báo đẩy; chương I9, "Thông báo đẩy: tín hiệu, không phải dữ liệu": push chỉ là tín hiệu, nội dung lấy từ server. [[src:book-xu1]]', 'Alex Xu notes: if the recipient is offline the server sends a push notification; chapter I9, "Push notifications: signals, not data": the push is only a signal, content comes from the server. [[src:book-xu1]]')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.ct', 'Thành phần và đường đi của tin', 'Components and the message path')
    z('ct.gcap', 'Các thành phần trong app (khung lớn) và server; thành phần và mũi tên của bước hiện tại sáng lên.', 'The components inside the app (large frame) and the server; the current step\'s components and arrows light up.')
    z('ct.app', 'App (máy gửi và máy nhận dùng cùng thiết kế)', 'App (sender and recipient devices share this design)')
    for k, vi, en in [('ui', 'Màn chat', 'Chat screen'), ('vm', 'ViewModel', 'ViewModel (state)'), ('repo', 'Repository', 'Repository layer'), ('db', 'Room: outbox, tin', 'Room: outbox, messages'),
                      ('worker', 'WorkManager gửi', 'WorkManager sender'), ('ws', 'Kết nối sống', 'Live connection'), ('push', 'Nhận push', 'Push receiver'), ('server', 'Server tin', 'Message server')]:
        z('ct.c.' + k, vi, en)
    z('ct.scap', 'Sơ đồ tuần tự của tin qua các bước; mũi tên đỏ đứt là chỗ hỏng.', 'Sequence diagram of the message over the steps; red dashed arrows are failures.')
    for k, vi, en in [('a', 'Điện thoại gửi', 'Sender phone'), ('a2', 'Máy tính bảng gửi', 'Sender tablet'), ('srv', 'Server', 'Server side'), ('b', 'Máy phòng khám', 'Clinic device')]:
        z('ct.p.' + k, vi, en)
    for k, vi, en in [
        ('pending', 'ghi outbox, hiện đồng hồ', 'outbox write, clock shown'), ('netok', 'có mạng: chạy ngay', 'online: run now'), ('netwait', 'mất mạng: chờ', 'offline: waiting'),
        ('post', 'POST, khóa clientId', 'POST, clientId key'), ('ack', 'message_id 812: một tick', 'message_id 812: one tick'), ('stored', 'lưu 812', 'stores 812'),
        ('lostack', 'response mất', 'response lost'), ('retry', 'thử lại, cùng khóa', 'retry, same key'), ('samekey', 'trả lại 812, không tạo mới', 'returns 812, no new copy'),
        ('wsdeliver', 'giao qua kết nối sống', 'deliver over live connection'), ('delivered', 'đã nhận', 'delivered'), ('ticks2', 'hai tick', 'two ticks'),
        ('wsnone', 'không có kết nối sống', 'no live connection'), ('tickle', 'push: "có tin mới"', 'push: "new message"'), ('fetch', 'GET sau cur_max_message_id', 'GET after cur_max_message_id'),
        ('read', 'đã xem tới 812', 'read up to 812'), ('seen', 'đã xem', 'seen'), ('sync', 'GET sau cur_max_message_id', 'GET after cur_max_message_id'), ('syncres', 'tin 812', 'message 812')]:
        z('ct.m.' + k, vi, en)
    z('ct.tickh', 'Trạng thái tin trên điện thoại người gửi', 'Message state on the sender\'s phone')
    for k, vi, en in [('0', '🕓 chờ gửi (nằm trong outbox)', '🕓 waiting to send (in the outbox)'), ('1', '✓ server đã nhận', '✓ received by the server'), ('2', '✓✓ máy phòng khám đã nhận', '✓✓ delivered to the clinic device'), ('3', '✓✓ đã xem', '✓✓ seen')]:
        z('ct.tick.' + k, vi, en)
    z('ct.legend', 'Hộp sáng: thành phần làm việc ở bước này. Mũi tên đỏ: hỏng hay không có đường.', 'Lit boxes: the components working at this step. Red arrows: failures or no path.')

    C = 'i13'
    a(C + '.title', 'Bài mẫu: app nhắn tin với phòng khám', 'Worked example: a clinic messaging app')
    a(C + '.essence', 'Một tin nhắn gom gần hết track: ghi vào outbox (hộp tin chờ gửi, lưu trong database trên đĩa) trước rồi mới gửi (I2), gửi bằng WorkManager (công cụ chạy việc nền của Android) với khóa chống trùng (Idempotency-Key ở chương I5: mã để server nhận ra lần thử lại), server cấp message_id (số thứ tự cho mỗi tin) tăng dần làm thứ tự (I7).\nNgười nhận online thì nhận qua kết nối sống (kết nối mở liên tục, như WebSocket); offline thì push (tin do dịch vụ đẩy gửi tới máy) chỉ báo rồi app tự tải (I4, I9). Xác nhận đã nhận, đã xem (read receipt) đi ngược về người gửi.\nMỗi thiết bị đồng bộ theo message_id lớn nhất đã có (I8), nên tin gửi từ điện thoại hiện đúng thứ tự trên máy tính bảng. Tên từng chương nằm ở mục cuối.',
      'One message pulls together most of the track: write it to an outbox (a box of messages waiting to send, stored in an on-disk database) before sending (I2), send with WorkManager (Android\'s tool for background work) and a duplicate-send key (the Idempotency-Key of chapter I5: a code that lets the server recognise a retry), and the server assigns an increasing message_id (a sequence number per message) as the order (I7).\nAn online recipient gets it over a live connection (a connection kept open, such as a WebSocket); offline, a push (a message the push service delivers to the device) only signals and the app fetches (I4, I9). Delivery and read receipts ("seen" notices) flow back to the sender.\nEach device syncs from the highest message_id it has (I8), so a message sent from the phone shows in order on the tablet. The chapter titles are in the last section.')
    a(C + '.goal.g1', 'Đã thấy server nhận tin', 'Saw the server receive the message')
    a(C + '.goal.g2', 'Đã thấy tin tới "đã xem"', 'Saw the message reach "seen"')
    a(C + '.sim.sysdesign.chat', 'một tin nhắn qua sáu bước', 'one message in six steps')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Người bệnh bấm gửi trong thang máy (không có sóng), rồi tắt màn hình. Mười phút sau ra khỏi thang máy. Theo thiết kế của bạn, tin có tới phòng khám không, và có bị gửi hai lần không?',
      'A patient taps send in a lift (no signal), then turns off the screen. Ten minutes later they leave the lift. In your design, does the message reach the clinic, and could it be sent twice?')
    B(C, S_, 1, 'ans', 'Tới, nếu tin được ghi vào outbox trên đĩa và việc gửi giao cho WorkManager với ràng buộc "có mạng": app tắt cũng không sao. Không trùng, nếu mỗi tin có một khóa chống trùng để server nhận ra lần thử lại. [[src:book-xu1]] [[src:book-acing]]',
      'It does, if the message is written to an on-disk outbox and sending is handed to WorkManager with a "network" constraint: closing the app does not matter. No duplicate, if each message carries a duplicate-send key so the server recognises the retry. [[src:book-xu1]] [[src:book-acing]]')

    S_ = 'reqs'
    a(C + '.sec.%s.title' % S_, 'Yêu cầu trước khi vẽ', 'Requirements before drawing')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Theo cách của chương I1, "Từ đề bài tới kế hoạch", hỏi trước khi thiết kế. Tin có được mất không? (Không.) Có cần đúng thứ tự không? (Có, trong một cuộc trò chuyện.) Người dùng có nhiều máy không? (Có: điện thoại và máy tính bảng.) Cần dấu đã nhận, đã xem không? (Có.) Gửi được lúc mất mạng không? (Có, gửi khi có mạng lại.) Mỗi câu trả lời biến thành một phần của thiết kế bên dưới. Đây là cách đặt bài của site.',
      'Following chapter I1, "From a brief to a plan", ask before designing. May messages be lost? (No.) Must order be kept? (Yes, within a conversation.) Do users have several devices? (Yes: phone and tablet.) Are delivered and seen marks needed? (Yes.) Can users send while offline? (Yes, sent once back online.) Each answer becomes a part of the design below. This framing is the site\'s.')

    S_ = 'arch'
    a(C + '.sec.%s.title' % S_, 'Các thành phần của app', 'The app\'s components')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Màn chat quan sát ViewModel (đối tượng giữ dữ liệu cho màn hình); ViewModel gọi repository (lớp lấy dữ liệu cho app); repository là chỗ duy nhất đọc ghi Room (database của Android: outbox và bảng tin) và giao việc gửi cho WorkManager. Kết nối sống (WebSocket, chương I4) và bộ nhận push đều chỉ đẩy tin mới vào repository, nên màn hình luôn đọc từ một nguồn sự thật là database (chương G4 của track Kiến trúc app Android, chương H7 của track Lưu dữ liệu trên Android). Đây là sơ đồ của site.',
      'The chat screen observes the ViewModel (the object holding data for the screen); the ViewModel calls the repository (the layer that gets data for the app); the repository is the only place reading and writing Room (Android\'s database: outbox and messages) and hands sending to WorkManager. The live connection (WebSocket, chapter I4) and the push receiver both only feed new messages into the repository, so the screen always reads one source of truth, the database (chapter G4 of the Android App Architecture track, chapter H7 of the Saving Data on Android track). This sketch is the site\'s.')

    S_ = 'send'
    a(C + '.sec.%s.title' % S_, 'Gửi: outbox, khóa chống trùng, message_id', 'Sending: outbox, duplicate key, message_id')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Ghi trước, gửi sau: tin vào outbox cùng một clientId ngẫu nhiên, rồi WorkManager gửi khi có mạng. Server dùng clientId làm khóa chống trùng (chương I5): thử lại sau khi hết thời gian chờ không tạo bản thứ hai. Server cấp message_id; Alex Xu yêu cầu id này duy nhất và tăng theo thời gian, và nói id tăng dần trong một cuộc trò chuyện là đủ, không cần id toàn cục (duy nhất trên cả hệ thống). [[src:book-xu1]]',
      'Write first, send later: the message goes into the outbox with a random clientId, then WorkManager sends it when online. The server uses the clientId as the duplicate-send key (chapter I5): a retry after a timeout creates no second copy. The server assigns the message_id; Alex Xu requires it to be unique and sortable by time, and says an ID increasing within one conversation is enough, without a global one (unique across the whole system). [[src:book-xu1]]')
    B(C, S_, 2, 'kt', 'outbox: (clientId=7f3…, "Tôi đến muộn 10 phút", trạng thái=chờ)\nPOST /messages   Idempotency-Key: 7f3…\n← 201 { "messageId": 812 }          → chuyển sang bảng tin, một tick\n(timeout, thử lại cùng khóa)\n← 201 { "messageId": 812 }          → không có bản thứ hai',
      'outbox: (clientId=7f3…, "I will be 10 minutes late", state=pending)\nPOST /messages   Idempotency-Key: 7f3…\n← 201 { "messageId": 812 }          → moved to messages, one tick\n(timeout, retry with the same key)\n← 201 { "messageId": 812 }          → no second copy')

    S_ = 'receive'
    a(C + '.sec.%s.title' % S_, 'Nhận, xác nhận và đồng bộ nhiều máy', 'Receiving, receipts and multi-device sync')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Zhiyong Tan mô tả đường đi của tin: tin được ghi ở message service trước; giao qua kết nối sống không được thì bỏ, vì máy sẽ lấy lại sau; phía nhận kiểm tra trùng rồi mới hiện, gửi xác nhận đã nhận, và khi người dùng đọc thì gửi read receipt về người gửi. Alex Xu nêu: người nhận offline thì server gửi thông báo đẩy. [[src:book-acing]] [[src:book-xu1]]',
      'Zhiyong Tan describes the path of a message: the message is recorded in the message service first; if delivery over the live connection fails it is dropped, since the device fetches later; the receiver checks for duplicates before showing, sends a delivery confirmation, and when the user reads it sends a read receipt to the sender. Alex Xu notes: if the recipient is offline the server sends a push notification. [[src:book-acing]] [[src:book-xu1]]')
    B(C, S_, 2, 'p', 'Alex Xu mô tả đồng bộ nhiều máy như sau: mỗi thiết bị giữ cur_max_message_id, và tin mới là tin có message_id lớn hơn số đó. Đây cũng là phân trang bằng cursor của chương I7: "các tin sau 811" không lệch khi có tin mới. Read receipt chỉ cần mang message_id lớn nhất đã đọc (gợi ý của site). [[src:book-xu1]]',
      'Alex Xu describes multi-device sync like this: each device keeps cur_max_message_id, and new messages are those with a larger message_id. It is also chapter I7\'s cursor paging: "messages after 811" does not shift when new ones arrive. A read receipt only needs the highest message_id read (the site\'s suggestion). [[src:book-xu1]]')

    S_ = 'map'
    a(C + '.sec.%s.title' % S_, 'Mỗi phần đến từ chương nào', 'Which chapter each part comes from')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Outbox trên đĩa: I2, "Tiến trình, bộ nhớ và cái chết của process". Lock để nhiều luồng không ghi outbox cùng lúc: I3, "Luồng, khóa, ANR và deadlock". Kết nối sống so với push: I4, "Chọn kênh giao tiếp". Khóa chống trùng, thử lại có backoff (khoảng chờ giãn dần): I5, "Mạng không tin cậy: timeout, thử lại, idempotency". Ảnh đại diện có cache: I6, "Cache: RAM, đĩa và HTTP". Lịch sử theo cursor message_id: I7, "Phân trang: offset và cursor". Nhiều máy, ghi chú sửa ở hai nơi: I8, "Nhiều thiết bị và xung đột". Push chỉ là tín hiệu: I9, "Thông báo đẩy: tín hiệu, không phải dữ liệu". Gửi ảnh vết thương theo khúc: I10, "Ảnh và tệp lớn". Khởi tạo SDK chat lười: I11, "Khởi động, pin và kích thước app". Bật tính năng chat sau feature flag, API có phiên bản: I12, "Quan sát và phát hành an toàn". Bảng này là của site.',
      'On-disk outbox: I2, "Processes, memory and process death". A lock so several threads do not write the outbox at once: I3, "Threads, locks, ANRs and deadlock". Live connection versus push: I4, "Choosing a channel". Duplicate-send key, retries with backoff (growing waits): I5, "Unreliable networks: timeouts, retries, idempotency". Cached avatars: I6, "Caching: memory, disk and HTTP". History by message_id cursor: I7, "Paging: offset and cursor". Several devices, notes edited in two places: I8, "Multiple devices and conflicts". Push as a signal: I9, "Push notifications: signals, not data". Sending wound photos in chunks: I10, "Images and large files". Lazy chat SDK init: I11, "Startup, battery and app size". Chat behind a feature flag, versioned API: I12, "Observability and safe releases". This table is the site\'s.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Thêm tính năng gửi ảnh vết thương trong chat. Liệt kê những gì thay đổi ở: outbox, cách gửi, tin trên server, máy nhận, và màn hình người gửi trong lúc ảnh đang tải lên.',
      'Add sending wound photos in chat. List what changes in: the outbox, how it is sent, the message on the server, the receiving device, and the sender\'s screen while the photo uploads.')
    B(C, S_, 1, 'hint', 'Xem lại chương I10, "Ảnh và tệp lớn", và chương I6, "Cache: RAM, đĩa và HTTP".', 'Revisit chapter I10, "Images and large files", and chapter I6, "Caching: memory, disk and HTTP".')
    B(C, S_, 1, 'sol', 'Outbox lưu đường dẫn ảnh đã thu nhỏ và địa chỉ upload. Gửi hai phần: upload tiếp tục được (I10) trong WorkManager, xong mới POST tin có tham chiếu ảnh, cùng khóa chống trùng. Server lưu tin với id ảnh, không nhúng ảnh. Máy nhận tải ảnh theo kích thước ô, có cache (I6, I10). Màn hình người gửi hiện tiến độ upload và nút thử lại; tin chỉ có một tick khi cả ảnh lẫn tin đã lên server.',
      'The outbox stores the resized image path and the upload address. Send in two parts: a resumable upload (I10) in WorkManager, then POST the message referencing the image, with the duplicate-send key. The server stores the message with the image id, not the image itself. The receiver loads the image at cell size, cached (I6, I10). The sender\'s screen shows upload progress and a retry button; the message gets one tick only once both image and message are on the server.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Vì sao ghi tin vào outbox trên đĩa trước khi gửi?', 'Why write the message to an on-disk outbox before sending?', 'Để tin sống qua process bị giết và mất mạng; WorkManager gửi khi có mạng.', 'So it survives process death and lost connectivity; WorkManager sends once online.', 'Xem chương I2, "Tiến trình, bộ nhớ và cái chết của process".', 'See chapter I2, "Processes, memory and process death".'),
        ('q2', 'Điều gì ngăn tin bị gửi hai lần khi thử lại sau timeout?', 'What stops a message being sent twice when retried after a timeout?', 'Khóa chống trùng (clientId) gửi kèm; server nhận ra và trả lại kết quả cũ.', 'The duplicate-send key (clientId); the server recognises it and returns the earlier result.', 'Xem chương I5, "Mạng không tin cậy: timeout, thử lại, idempotency".', 'See chapter I5, "Unreliable networks: timeouts, retries, idempotency".'),
        ('q3', 'Vì sao không dùng created_at để xếp thứ tự tin?', 'Why not order messages by created_at?', 'Hai tin có thể cùng thời điểm; message_id duy nhất, tăng dần mới xếp được chắc chắn.', 'Two messages can share a timestamp; only a unique, increasing message_id orders them reliably.', 'Thứ tự phải do server cấp; giờ tạo có thể trùng.', 'The order must come from the server; creation times can collide.'),
        ('q4', 'Máy tính bảng biết tải những tin nào khi mở app?', 'How does the tablet know which messages to fetch when opened?', 'Các tin có message_id lớn hơn cur_max_message_id của chính nó.', 'Those with a message_id larger than its own cur_max_message_id.', 'Giống cursor ở chương I7, "Phân trang: offset và cursor".', 'Like the cursor in chapter I7, "Paging: offset and cursor".')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
