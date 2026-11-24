# Thiết kế hệ thống phía mobile · I5: mạng không tin cậy (Phần 2)
# Nguồn: Kleppmann và Riccomini, DDIA bản 2 (ch.2 retry storm và exponential backoff; ch.9 Unreliable Networks; ch.12 idempotence);
# IETF draft-ietf-httpapi-idempotency-key-header-09; RFC 9110 (phương thức idempotent); WorkManager define-work (backoff). Đọc 2026-11-24.

SEC_ORDER = {'i5': ['hook', 'unknown', 'idempotent', 'key', 'backoff', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.retry', 'Thiết kế hệ thống · thử lại an toàn', 'System design · retrying safely')
    m = lambda k, vi, en=None: a('m.retry.' + k, vi, en)
    m('title', 'Request mất, response mất, thử lại có key, và cơn bão thử lại', 'Lost request, lost response, retry with a key, and the retry storm')
    m('overview', 'Người dùng bấm "Đặt lịch 9:00". App gửi POST rồi không nhận được trả lời: hết thời gian chờ. App không biết request mất trên đường đi hay response mất trên đường về. Bốn tình huống: request mất rồi thử lại; response mất rồi thử lại không có key; thử lại với Idempotency-Key; và năm máy cùng thử lại sau khi server sập.',
      'The user taps "Book 9:00". The app sends a POST and gets no answer: a timeout. The app cannot tell whether the request was lost on the way there or the response on the way back. Four situations: the request is lost, then retried; the response is lost, then retried without a key; retrying with an Idempotency-Key; and five phones retrying after the server went down.')
    m('wrapup', 'Hết thời gian chờ không cho biết server đã làm hay chưa. Thử lại một thao tác không idempotent (POST tạo lịch) có thể tạo hai lịch. Gắn một Idempotency-Key do app sinh, lưu cùng bản nháp và dùng lại ở mọi lần thử, để server nhận ra lần thử lại và trả lại kết quả cũ. Còn khi nhiều máy cùng thử lại, giãn khoảng chờ theo cấp số nhân và thêm phần ngẫu nhiên (jitter) để chúng không dội vào server cùng lúc.',
      'A timeout does not tell you whether the server did the work. Retrying a non-idempotent operation (a POST that creates a booking) can create two bookings. Attach an Idempotency-Key the app generates, saves with the draft and reuses on every attempt, so the server recognises the retry and returns the earlier result. And when many phones retry, grow the wait exponentially and add randomness (jitter) so they do not hit the server at the same moment.')
    m('simp.1', 'Thời hạn chờ 10 giây, khoảng thử lại và các giá trị jitter là số minh họa (jitter là số cố định để mô phỏng chạy giống nhau mỗi lần).', 'The 10-second timeout, retry intervals and jitter values are illustrative (the jitter values are fixed so the simulation behaves the same every time).')
    m('simp.2', 'Không phân biệt được request mất hay response mất: theo DDIA bản 2 ch.9. Idempotency-Key theo bản nháp IETF số 09 (chưa là RFC). Backoff và jitter theo DDIA bản 2 ch.2 và tài liệu WorkManager. Đọc ngày 2026-11-24.', 'Not being able to tell a lost request from a lost response follows DDIA 2nd ed. ch.9. Idempotency-Key follows IETF draft 09 (not yet an RFC). Backoff and jitter follow DDIA 2nd ed. ch.2 and the WorkManager docs. Read on 2026-11-24.')
    m('ctl.hint', 'Đổi tình huống rồi đi lại; so số lịch trên server ở bước cuối, và đỉnh số yêu cầu cùng lúc trong tình huống bão thử lại.', 'Switch the situation and walk again; compare the server\'s booking count at the last step, and the peak of simultaneous requests in the retry storm.')
    m('ctl.case', 'Tình huống', 'Situation')
    for k, vi, en in [('reqlost', 'request mất, thử lại', 'request lost, retried'), ('resplost', 'response mất, thử lại không key', 'response lost, retried without a key'), ('key', 'response mất, thử lại có Idempotency-Key', 'response lost, retried with an Idempotency-Key'), ('storm', 'năm máy cùng thử lại', 'five phones retrying at once')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'App, mạng, server', 'App, network, server')
    m('diagramDesc', 'Request đi qua mạng tới server, response đi ngược lại; cả hai đều có thể mất', 'The request crosses the network to the server, the response comes back; either can be lost')
    for k, vi, en in [('app', 'App Hẹn Khám', 'ClinicBook app'), ('net', 'Mạng di động', 'Mobile network'), ('server', 'Server đặt lịch', 'Booking server')]:
        m('n.' + k, vi, en)
    m('met.attempts', 'Lượt gửi', 'Attempts'); m('met.bookings', 'Lịch đã tạo trên server', 'Bookings created on the server'); m('met.peak', 'Đỉnh yêu cầu cùng lúc', 'Peak simultaneous requests')
    a('cap.retry', 'App bên trái, server bên phải; mạng ở giữa là nơi request hay response có thể mất.', 'The app on the left, the server on the right; the network in the middle is where a request or response can be lost.')
    S = [
        ('reqlost', 's1', 'Bấm "Đặt lịch": request mất trên đường đi', 'Tap "Book": the request is lost on the way', 'Server không nhận được gì, nên không tạo lịch nào.', 'The server receives nothing, so it creates no booking.'),
        ('reqlost', 's2', '10 giây không có trả lời: hết thời gian chờ', '10 seconds without an answer: timeout', 'App chỉ biết là chưa có response. Nó không biết vì sao.', 'The app only knows there is no response. It does not know why.'),
        ('reqlost', 's3', 'Thử lại sau 1 giây: server tạo lịch #41', 'Retry after 1 second: the server creates booking #41', 'Lần này request tới nơi, response về được.', 'This time the request arrives and the response gets back.'),
        ('reqlost', 's4', 'Kết quả: một lịch, đúng ý người dùng', 'Result: one booking, as the user meant', 'Thử lại không key vẫn đúng, nhưng chỉ vì lần đầu request mất. App không biết được điều đó.', 'Retrying without a key worked, but only because the first request was lost. The app could not know that.'),
        ('resplost', 's1', 'Bấm "Đặt lịch": server tạo lịch #41', 'Tap "Book": the server creates booking #41', 'Request tới nơi, server đã làm xong việc.', 'The request arrives; the server has done the work.'),
        ('resplost', 's2', 'Response mất trên đường về; app hết thời gian chờ', 'The response is lost on the way back; the app times out', 'Nhìn từ app, tình huống này giống hệt request mất.', 'From the app\'s side, this looks exactly like a lost request.'),
        ('resplost', 's3', 'App thử lại: server tạo thêm lịch #42', 'The app retries: the server creates booking #42 too', 'Server thấy một POST mới, không có gì cho biết đây là lần thử lại.', 'The server sees a new POST; nothing says it is a retry.'),
        ('resplost', 's4', 'Kết quả: hai lịch cùng giờ cho một người', 'Result: two bookings at the same time for one person', 'Một chỗ khám bị chiếm phí, người dùng nhận hai thông báo xác nhận.', 'A slot is wasted, and the user gets two confirmations.'),
        ('key', 's1', 'App tạo Idempotency-Key, lưu cùng bản nháp, rồi gửi', 'The app creates an Idempotency-Key, saves it with the draft, then sends', 'Server tạo lịch #41 và ghi lại kết quả theo key.', 'The server creates booking #41 and records the result under the key.'),
        ('key', 's2', 'Response mất; app hết thời gian chờ', 'The response is lost; the app times out', 'Giống tình huống trước, cho tới lúc này.', 'Same as before, up to this point.'),
        ('key', 's3', 'Thử lại với cùng key: server nhận ra', 'Retry with the same key: the server recognises it', 'Key đã thấy, nên server không tạo lịch mới mà trả lại kết quả của lần đầu: #41.', 'The key has been seen, so the server creates nothing new and returns the first result: #41.'),
        ('key', 's4', 'Kết quả: một lịch, dù đã gửi hai lần', 'Result: one booking, though it was sent twice', 'Cùng key thì cùng kết quả. Thử lại trở nên an toàn.', 'Same key, same result. Retrying becomes safe.'),
        ('storm', 's1', 'Giây 0: server quá tải; năm máy cùng nhận lỗi', 'Second 0: the server is overloaded; five phones get errors at once', 'Năm máy gửi cùng lúc, cùng thất bại cùng lúc.', 'Five phones sent together and failed together.'),
        ('storm', 's2', 'Thử lại mỗi 2 giây, khoảng cố định', 'Retry every 2 seconds, a fixed interval', 'Cả năm máy dội vào server cùng một khoảnh khắc, mỗi 2 giây: đỉnh 5 yêu cầu cùng lúc, server không kịp hồi.', 'All five hit the server at the same instant every 2 seconds: a peak of 5 at once, and the server cannot recover.'),
        ('storm', 's3', 'Exponential backoff: chờ 1, 2, 4, 8 giây', 'Exponential backoff: wait 1, 2, 4, 8 seconds', 'Số lần thử ít đi, nhưng các máy vẫn đồng bộ với nhau: vẫn đỉnh 5.', 'Fewer attempts, but the phones are still in lockstep: still a peak of 5.'),
        ('storm', 's4', 'Exponential backoff có jitter: mỗi máy chờ một khoảng ngẫu nhiên', 'Exponential backoff with jitter: each phone waits a random amount', 'Các lần thử rải ra theo thời gian; đỉnh giảm còn 3 ở lần thử đầu tiên rồi 1 đến 2 về sau. Server có chỗ thở để hồi lại.', 'Attempts spread out in time; the peak drops to 3 on the first retry, then 1 to 2 afterwards. The server gets room to recover.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi tình huống; nhìn bảng lịch trên server, hay đỉnh yêu cầu cùng lúc.', 'Walk all four steps of each situation; watch the server\'s booking table, or the peak of simultaneous requests.'),
        ('reqlost.s2', 'DDIA bản 2 (ch.9): gửi request mà không nhận được response thì không thể biết vì sao; cách thường dùng là timeout, nhưng hết thời gian chờ vẫn không biết server đã nhận request chưa. [[src:book-ddia2]]', 'DDIA 2nd ed. (ch.9): if you send a request and get no response, you cannot tell why; the usual answer is a timeout, but after it you still do not know whether the server got the request. [[src:book-ddia2]]'),
        ('reqlost.s3', 'Lần thử lại thành công không chứng minh lần đầu đã mất request; app chỉ gặp may.', 'A successful retry does not prove the first request was lost; the app was just lucky.'),
        ('reqlost.s4', 'Đọc tiếp tình huống "response mất": cùng những gì app nhìn thấy, kết quả khác hẳn.', 'Now try "response lost": the app sees exactly the same thing, with a very different outcome.'),
        ('resplost.s2', 'DDIA bản 2 (ch.9): server có thể đã xử lý request nhưng response mất trên mạng; với bên gửi, các trường hợp này không phân biệt được. [[src:book-ddia2]]', 'DDIA 2nd ed. (ch.9): the server may have processed the request while the response was lost on the network; to the sender these cases are indistinguishable. [[src:book-ddia2]]'),
        ('resplost.s3', 'RFC 9110: POST không phải phương thức idempotent, nên client không được tự gửi lại khi không biết kết quả. [[src:rfc9110]]', 'RFC 9110: POST is not an idempotent method, so a client should not resend it automatically when the outcome is unknown. [[src:rfc9110]]'),
        ('resplost.s4', 'DDIA bản 2 (ch.12): thao tác idempotent là làm nhiều lần có cùng tác dụng như làm một lần; tạo lịch thì không. [[src:book-ddia2]]', 'DDIA 2nd ed. (ch.12): an idempotent operation has the same effect done many times as done once; creating a booking does not. [[src:book-ddia2]]'),
        ('key.s1', 'Bản nháp IETF Idempotency-Key: client sinh một chuỗi duy nhất (nên dùng UUID) cho mỗi thao tác, và không dùng lại key đó cho request có nội dung khác. [[src:ietf-idem-key]]', 'The IETF Idempotency-Key draft: the client generates a unique string (a UUID is recommended) per operation, and must not reuse it for a request with a different payload. [[src:ietf-idem-key]]'),
        ('key.s2', 'Tới đây mọi thứ giống tình huống trước; khác biệt nằm ở key đã được lưu cùng bản nháp, sẵn cho lần thử lại.', 'So far it matches the previous situation; the difference is the key already saved with the draft, ready for the retry.'),
        ('key.s3', 'Bản nháp IETF: lần thử lại sau khi đã xong thì server trả response nhất quán với việc request đã hoàn tất; đang xử lý dở thì trả 409; cùng key mà nội dung khác thì trả 422. [[src:ietf-idem-key]]', 'The IETF draft: a retry after completion gets a response consistent with the request having completed; one arriving while still processing gets 409; the same key with a different payload gets 422. [[src:ietf-idem-key]]'),
        ('key.s4', 'DDIA bản 2 (ch.12): thao tác không tự nhiên idempotent thường làm được idempotent bằng thêm một chút siêu dữ liệu. [[src:book-ddia2]]', 'DDIA 2nd ed. (ch.12): an operation that is not naturally idempotent can often be made so with a little extra metadata. [[src:book-ddia2]]'),
        ('storm.s2', 'DDIA bản 2 (ch.2): khi hệ thống gần quá tải, client hết thời gian chờ rồi gửi lại làm tải tăng thêm: một cơn bão thử lại (retry storm). [[src:book-ddia2]]', 'DDIA 2nd ed. (ch.2): near overload, clients time out and resend, raising the load further: a retry storm. [[src:book-ddia2]]'),
        ('storm.s3', 'WorkManager: Result.retry() thì công việc được xếp lại theo backoff; mặc định EXPONENTIAL với độ trễ 30 giây, tối thiểu 10 giây. [[src:ax-define-work]]', 'WorkManager: Result.retry() reschedules the work with a backoff; the default is EXPONENTIAL with a 30-second delay, at least 10 seconds. [[src:ax-define-work]]'),
        ('storm.s4', 'DDIA bản 2 (ch.2): để retry không đè chết dịch vụ, tăng và ngẫu nhiên hóa khoảng giữa các lần thử ở phía client (exponential backoff), và tạm ngừng gửi tới dịch vụ vừa lỗi (circuit breaker). [[src:book-ddia2]]', 'DDIA 2nd ed. (ch.2): to keep retries from overwhelming a service, increase and randomise the time between retries on the client (exponential backoff), and pause sending to a service that just failed (circuit breaker). [[src:book-ddia2]]')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.rt', 'Sơ đồ tuần tự và lịch trên server', 'Sequence and server bookings')
    z('rt.cap', 'Sơ đồ tuần tự: mỗi hàng là một tin theo thời gian. Mũi tên đỏ đứt: tin bị mất hay việc làm sai.', 'Sequence diagram: each row is one message in time. Red dashed arrow: a lost message or a wrong action.')
    z('rt.p.app', 'App', 'app'); z('rt.p.server', 'Server', 'server')
    for k, vi, en in [
        ('book', 'đặt: POST /appointments 9:00', 'POST /appointments 9:00'), ('lostreq', '✕ mất trên đường đi', '✕ lost on the way'), ('timeout', '10s: hết thời gian chờ, không rõ vì sao', '10s: timeout, cause unknown'),
        ('retry', 'thử lại: POST 9:00', 'retry: POST 9:00'), ('c41', 'tạo lịch #41', 'create booking #41'), ('r41', '201: lịch #41', '201: booking #41'),
        ('lost41', '201 #41 ✕ mất trên đường về', '201 #41 ✕ lost on the way back'), ('c42', 'tạo thêm lịch #42', 'create another booking #42'), ('r42', '201: lịch #42', '201: booking #42'),
        ('two', 'hai lịch 9:00 cho một người', 'two 9:00 bookings for one person'), ('one', 'một lịch 9:00', 'one 9:00 booking'),
        ('genkey', 'tạo key k-7f3a, lưu cùng bản nháp', 'create key k-7f3a, save it with the draft'), ('bookk', 'đặt: POST 9:00, Idempotency-Key: k-7f3a', 'POST 9:00, Idempotency-Key: k-7f3a'),
        ('c41k', 'tạo #41, ghi kết quả theo k-7f3a', 'create #41, store result under k-7f3a'), ('retryk', 'thử lại: cùng key k-7f3a', 'retry: same key k-7f3a'),
        ('seen', 'k-7f3a đã thấy: không tạo mới', 'k-7f3a seen: create nothing'), ('same', '201: lịch #41 (kết quả cũ)', '201: booking #41 (earlier result)')]:
        z('rt.m.' + k, vi, en)
    z('rt.tcap', 'Lịch hẹn 9:00 trên server.', 'The server\'s 9:00 bookings.')
    z('rt.t.id', 'Lịch', 'Booking'); z('rt.t.key', 'Idempotency-Key', 'Idempotency key'); z('rt.t.none', 'chưa có lịch nào', 'no bookings yet'); z('rt.t.dup', 'trùng', 'duplicate'); z('rt.t.nokey', 'không có', 'none')
    z('rt.scap', 'Năm máy thử lại sau khi server quá tải ở giây 0 (0–16 giây). Mỗi chấm là một lần gửi; dòng dưới cùng ghi đỉnh số yêu cầu rơi vào cùng nửa giây.', 'Five phones retrying after the server overloads at second 0 (0–16 seconds). Each dot is one attempt; the bottom line gives the peak number of requests within the same half second.')
    z('rt.s.phone', 'máy {n}', 'phone {n}')
    for k, vi, en in [('fail', 'lần gửi đầu, cùng thất bại', 'the first send, all failing'), ('fixed', 'cố định mỗi 2 giây', 'fixed, every 2 seconds'), ('exp', 'exponential: 1, 2, 4, 8 giây', 'exponential: 1, 2, 4, 8 seconds'), ('jitter', 'exponential có thêm jitter', 'exponential + jitter')]:
        z('rt.s.' + k, vi, en)
    z('rt.s.peak', 'đỉnh: {n} cùng lúc', 'peak: {n} at once')
    z('rt.s.aria', 'Lịch thử lại của năm máy; đỉnh {n} yêu cầu cùng lúc', 'Retry schedule of five phones; peak of {n} requests at once')
    z('rt.legend', 'Ô gạch đỏ: lịch trùng. Chữ đậm: lịch hợp lệ. ✕: tin mất giữa đường.', 'Red hatched: a duplicate booking. Bold: a valid booking. ✕: a message lost on the way.')

    C = 'i5'
    a(C + '.title', 'Mạng không tin cậy: timeout, thử lại, idempotency', 'Unreliable networks: timeouts, retries, idempotency')
    a(C + '.essence', 'Gửi request mà không có response thì không thể biết request mất, server chết hay response mất; hết thời gian chờ chỉ có nghĩa là "chưa thấy trả lời".\nThử lại một thao tác không idempotent (POST tạo lịch) có thể làm hai lần. Gắn Idempotency-Key do app sinh, lưu bền cùng bản nháp và dùng lại ở mọi lần thử, để server trả lại kết quả cũ.\nKhi nhiều máy cùng thử lại, giãn khoảng chờ theo cấp số nhân và thêm jitter, nếu không chính các lần thử lại sẽ đè server.',
      'If a request gets no response, you cannot tell whether the request was lost, the server died, or the response was lost; a timeout only means "no answer yet".\nRetrying a non-idempotent operation (a POST that creates a booking) can do it twice. Attach an Idempotency-Key the app generates, stores durably with the draft and reuses on every attempt, so the server returns the earlier result.\nWhen many phones retry, grow the wait exponentially and add jitter, or the retries themselves will crush the server.')
    a(C + '.goal.g1', 'Đã thấy lần thử lại', 'Saw the retry')
    a(C + '.goal.g2', 'Đã thấy kết quả trên server', 'Saw the result on the server')
    a(C + '.sim.sysdesign.retry', 'request mất, response mất, thử lại có key, bão thử lại', 'lost request, lost response, retry with a key, retry storm')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Để "chống mạng chập chờn", app tự thử lại mọi request lỗi tối đa ba lần. Tuần sau, phòng khám báo nhiều người có hai lịch cùng giờ. Vì sao, và vì sao chỉ thỉnh thoảng?',
      'To "cope with flaky networks", the app retries every failed request up to three times. A week later the clinic reports many people with two bookings at the same time. Why, and why only sometimes?')
    B(C, S_, 1, 'ans', 'Khi response (không phải request) bị mất, server đã tạo lịch rồi; app hết thời gian chờ, gửi lại POST, server tạo thêm một lịch. Chỉ thỉnh thoảng vì phải mất đúng chiều về. App không phân biệt được hai trường hợp, nên lần thử lại phải an toàn trong cả hai. [[src:book-ddia2]]',
      'When the response (not the request) is lost, the server already created the booking; the app times out, resends the POST, and the server creates another. Only sometimes, because it takes losing exactly the way back. The app cannot tell the two cases apart, so the retry must be safe in both. [[src:book-ddia2]]')

    S_ = 'unknown'
    a(C + '.sec.%s.title' % S_, 'Hết thời gian chờ: biết là không biết', 'A timeout: knowing that you do not know')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'DDIA bản 2 (ch.9) liệt kê những gì có thể hỏng khi gửi một request qua mạng: request mất, request nằm trong hàng đợi, server sập, server tạm dừng rồi trả lời sau, server đã xử lý nhưng response mất, hay response bị trễ. Bên gửi không phân biệt được các trường hợp này; thông tin duy nhất là "chưa nhận được response". Cách thường dùng là timeout, và sau đó bạn vẫn không biết server đã nhận request hay chưa. [[src:book-ddia2]]',
      'DDIA 2nd ed. (ch.9) lists what can go wrong when sending a request over a network: the request is lost, it waits in a queue, the server crashed, the server paused and will answer later, the server processed it but the response was lost, or the response is delayed. The sender cannot tell these apart; the only information is "no response yet". The usual answer is a timeout, after which you still do not know whether the server got the request. [[src:book-ddia2]]')
    B(C, S_, 2, 'p', 'Sách viết cho hệ phân tán giữa các server, nhưng điện thoại còn tệ hơn: mạng di động đổi trạng thái liên tục, đi vào thang máy là mất sóng, và app có thể bị giết giữa lúc chờ (chương I2). Với app, "không có response" là chuyện hằng ngày chứ không phải ngoại lệ. Đoạn này là diễn giải của site.',
      'The book is about distributed systems between servers, but a phone is worse: mobile networks change state constantly, an elevator kills the signal, and the app can be killed while waiting (chapter I2). For an app, "no response" is daily life, not an exception. This paragraph is the site\'s interpretation.')

    S_ = 'idempotent'
    a(C + '.sec.%s.title' % S_, 'Thao tác idempotent', 'Idempotent operations')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Thao tác idempotent là làm nhiều lần có cùng tác dụng như làm một lần: xóa một khóa là idempotent (xóa lần nữa không đổi gì), tăng một bộ đếm thì không. Thao tác không tự nhiên idempotent thường làm được idempotent nhờ thêm một chút siêu dữ liệu, như ghi lại id của thông điệp đã xử lý. [[src:book-ddia2]]',
      'An idempotent operation has the same effect done many times as done once: deleting a key is idempotent (deleting again changes nothing), incrementing a counter is not. An operation that is not naturally idempotent can often be made so with a little metadata, such as recording the id of the message already processed. [[src:book-ddia2]]')
    B(C, S_, 2, 'p', 'Trong HTTP, RFC 9110 định nghĩa phương thức idempotent: PUT, DELETE và các phương thức an toàn (GET, HEAD, OPTIONS, TRACE). Client có thể tự gửi lại request idempotent khi kết nối đứt trước lúc nhận được response; POST và PATCH thì không. Vì vậy thư viện HTTP thường chỉ tự thử lại GET; còn "đặt lịch" thì app phải tự làm cho an toàn. [[src:rfc9110]]',
      'In HTTP, RFC 9110 defines the idempotent methods: PUT, DELETE and the safe methods (GET, HEAD, OPTIONS, TRACE). A client may automatically resend an idempotent request when the connection fails before the response arrives; POST and PATCH are not idempotent. That is why HTTP libraries usually only retry GET by themselves, and "book an appointment" is the app\'s job to make safe. [[src:rfc9110]]')

    S_ = 'key'
    a(C + '.sec.%s.title' % S_, 'Idempotency-Key', 'The Idempotency-Key header')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', 'Bản nháp IETF "The Idempotency-Key HTTP Header Field" (bản 09, chưa là RFC) chuẩn hóa một cách làm phổ biến: client gửi kèm header Idempotency-Key, giá trị là chuỗi duy nhất do client sinh (nên dùng UUID), để POST hay PATCH chịu được lỗi. Key không được dùng lại cho request có nội dung khác. Server gặp key đã xong thì trả response nhất quán với việc request đã hoàn tất; gặp key đang xử lý dở thì nên trả 409 Conflict; gặp key cũ với nội dung khác thì nên trả 422. [[src:ietf-idem-key]]',
      'The IETF draft "The Idempotency-Key HTTP Header Field" (version 09, not yet an RFC) standardises a common practice: the client sends an Idempotency-Key header whose value is a unique client-generated string (a UUID is recommended), making POST or PATCH fault-tolerant. A key must not be reused for a request with a different payload. For a completed key the server responds consistently with the request having completed; for one still in progress it should return 409 Conflict; for an old key with a different payload it should return 422. [[src:ietf-idem-key]]')
    B(C, S_, 2, 'p', 'Điểm dễ sai nằm ở phía app: key phải sinh một lần cho một ý định của người dùng, lưu bền cùng bản nháp (Room hay DataStore, track H), và dùng lại ở mọi lần thử, kể cả sau khi app bị giết và WorkManager chạy lại. Sinh key mới ở mỗi lần thử thì header vô dụng. Đoạn này là diễn giải của site.',
      'The easy mistake is on the app side: generate the key once per user intent, store it durably with the draft (Room or DataStore, track H), and reuse it on every attempt, including after the app is killed and WorkManager runs again. A new key per attempt makes the header useless. This paragraph is the site\'s interpretation.')
    B(C, S_, 3, 'kt', '@Entity data class BookingDraft(\n    @PrimaryKey val id: Long,\n    val slot: String,\n    val idempotencyKey: String = UUID.randomUUID().toString(),   // sinh MỘT lần, lưu cùng bản nháp\n)\n\nsuspend fun send(d: BookingDraft) =\n    api.book(d.slot, idempotencyKey = d.idempotencyKey)          // mọi lần thử dùng cùng key',
      '@Entity data class BookingDraft(\n    @PrimaryKey val id: Long,\n    val slot: String,\n    val idempotencyKey: String = UUID.randomUUID().toString(),   // generated ONCE, stored with the draft\n)\n\nsuspend fun send(d: BookingDraft) =\n    api.book(d.slot, idempotencyKey = d.idempotencyKey)          // every attempt uses the same key')

    S_ = 'backoff'
    a(C + '.sec.%s.title' % S_, 'Thử lại bao lâu một lần: backoff và jitter', 'How often to retry: backoff and jitter')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'DDIA bản 2 (ch.2) mô tả cơn bão thử lại: hệ thống gần quá tải thì trả lời chậm, client hết thời gian chờ và gửi lại, tải càng tăng, và hệ thống có thể kẹt trong trạng thái quá tải cả khi tải gốc đã giảm. Cách phòng phía client: tăng và ngẫu nhiên hóa khoảng giữa các lần thử (exponential backoff, sách dẫn bài "Exponential Backoff and Jitter" của Marc Brooker), và tạm ngừng gửi tới dịch vụ vừa lỗi (circuit breaker). [[src:book-ddia2]]',
      'DDIA 2nd ed. (ch.2) describes the retry storm: a system near overload answers slowly, clients time out and resend, the load grows further, and the system can stay stuck overloaded even after the original load drops. Client-side prevention: increase and randomise the time between retries (exponential backoff; the book cites Marc Brooker\'s "Exponential Backoff and Jitter"), and pause sending to a service that just failed (a circuit breaker). [[src:book-ddia2]]')
    B(C, S_, 2, 'p', 'WorkManager có sẵn backoff: worker trả Result.retry() thì công việc được xếp lại; chính sách LINEAR hay EXPONENTIAL, mặc định EXPONENTIAL với 30 giây, tối thiểu 10 giây. Với EXPONENTIAL bắt đầu từ 10 giây, các lần thử rơi vào khoảng 20, 40, 80 giây; thời điểm thật lệch vài giây. Việc gửi lịch hẹn ở nền (H7) nên dùng nó thay vì tự viết vòng lặp delay. [[src:ax-define-work]]',
      'WorkManager has backoff built in: a worker returning Result.retry() is rescheduled; the policy is LINEAR or EXPONENTIAL, defaulting to EXPONENTIAL with 30 seconds, at least 10 seconds. With EXPONENTIAL starting at 10 seconds, attempts land around 20, 40, 80 seconds; real times drift by a few seconds. Sending bookings in the background (H7) should use it instead of a hand-written delay loop. [[src:ax-define-work]]')
    B(C, S_, 3, 'kt', 'fun backoffMillis(attempt: Int): Long {\n    val cap = 1_000L shl attempt              // 1, 2, 4, 8 giây…\n    return Random.nextLong(0, cap)            // jitter: chọn ngẫu nhiên trong [0, cap)\n}\n\n// ở nền: để WorkManager lo\nOneTimeWorkRequestBuilder<SendBookingWorker>()\n    .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 30, TimeUnit.SECONDS)',
      'fun backoffMillis(attempt: Int): Long {\n    val cap = 1_000L shl attempt              // 1, 2, 4, 8 seconds…\n    return Random.nextLong(0, cap)            // jitter: pick at random in [0, cap)\n}\n\n// in the background: let WorkManager handle it\nOneTimeWorkRequestBuilder<SendBookingWorker>()\n    .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 30, TimeUnit.SECONDS)')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Đã thêm Idempotency-Key nhưng vẫn có lịch trùng, nhất là khi gửi lúc mất mạng.', 'An Idempotency-Key was added but duplicates still happen, especially when sending offline.')
    B(C, S_, 1, 'cause', 'Key được sinh trong hàm gửi, nên mỗi lần WorkManager chạy lại là một key mới.', 'The key is generated inside the send function, so every WorkManager rerun gets a new key.')
    B(C, S_, 1, 'fix', 'Sinh key một lần khi người dùng bấm "Đặt lịch", lưu trong bản nháp ở Room, và đọc lại ở mọi lần thử.', 'Generate the key once when the user taps "Book", store it in the Room draft, and read it back on every attempt.')
    B(C, S_, 2, 'bug', 'Server vừa sập 2 phút, khi lên lại thì sập tiếp ngay; cứ thế nửa tiếng.', 'The server was down for 2 minutes, and when it came back it fell over again at once; this went on for half an hour.')
    B(C, S_, 2, 'cause', 'Mọi app thử lại mỗi 5 giây cố định; hàng nghìn máy dội vào cùng một lúc khi server vừa hồi.', 'Every app retried every 5 seconds, fixed; thousands of phones hit the server at the same moment it recovered.')
    B(C, S_, 2, 'fix', 'Exponential backoff có jitter và giới hạn số lần thử; tôn trọng Retry-After nếu server gửi; việc nền để WorkManager với BackoffPolicy.EXPONENTIAL.', 'Exponential backoff with jitter and a retry cap; honour Retry-After if the server sends it; background work goes to WorkManager with BackoffPolicy.EXPONENTIAL.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Với mỗi thao tác của Hẹn Khám, nói nó có idempotent không, và nếu không thì làm sao để thử lại an toàn: (a) tải danh sách bác sĩ; (b) đổi giờ hẹn #41 sang 10:00; (c) hủy lịch #41; (d) thanh toán phí khám 200.000 đ; (e) gửi một tin nhắn cho phòng khám.',
      'For each ClinicBook operation, say whether it is idempotent, and if not, how to make retries safe: (a) load the doctor list; (b) move booking #41 to 10:00; (c) cancel booking #41; (d) pay a 200,000 VND fee; (e) send a message to the clinic.')
    B(C, S_, 1, 'hint', 'Hỏi: làm hai lần có khác làm một lần không? Nếu dùng đúng phương thức HTTP thì sao?', 'Ask: does doing it twice differ from doing it once? What if the right HTTP method is used?')
    B(C, S_, 1, 'sol', '(a) GET: idempotent, thử lại thoải mái. (b) PUT /appointments/41 {time: 10:00}: idempotent, vì đặt giá trị chứ không cộng thêm. (c) DELETE /appointments/41: idempotent; lần thử lại có thể nhận 404, app coi như đã hủy. (d) POST thanh toán: không idempotent, bắt buộc Idempotency-Key lưu cùng đơn, và không bao giờ thử lại bằng key mới. (e) POST tin nhắn: không idempotent; dùng key, hoặc id tin do client sinh để server bỏ bản trùng.',
      '(a) GET: idempotent, retry freely. (b) PUT /appointments/41 {time: 10:00}: idempotent, since it sets a value rather than adding. (c) DELETE /appointments/41: idempotent; a retry may get 404, which the app treats as cancelled. (d) POST payment: not idempotent; an Idempotency-Key stored with the order is mandatory, and never retry with a new key. (e) POST message: not idempotent; use a key, or a client-generated message id so the server drops duplicates.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Không phân biệt được request mất hay response mất, idempotence và cơn bão thử lại theo Kleppmann và Riccomini, DDIA bản 2 (ch.9, ch.12, ch.2); phương thức idempotent theo RFC 9110; Idempotency-Key theo bản nháp IETF số 09 (21/11/2026, chưa là chuẩn, có thể đổi); backoff của WorkManager theo trang "Define work requests"; đọc ngày 2026-11-24. Bài của Marc Brooker chỉ nhắc qua lời dẫn của DDIA, site chưa đọc trực tiếp. Hẹn Khám, key k-7f3a, thời hạn chờ 10 giây và mọi con số jitter là của site. Xu tập 2 ch.11 (thanh toán) chưa dùng.',
      'Not being able to tell a lost request from a lost response, idempotence and the retry storm follow Kleppmann and Riccomini, DDIA 2nd ed. (ch.9, ch.12, ch.2); idempotent methods follow RFC 9110; Idempotency-Key follows IETF draft 09 (21 November 2026, not yet a standard, may change); WorkManager backoff follows "Define work requests"; read on 2026-11-24. Marc Brooker\'s article is only mentioned through DDIA\'s citation; the site has not read it directly. ClinicBook, the key k-7f3a, the 10-second timeout and every jitter value are the site\'s. Xu vol. 2 ch.11 (payments) is not used yet.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'App hết thời gian chờ khi đặt lịch. Nó biết được gì?', 'The app times out while booking. What does it know?', 'Chỉ biết chưa có response; không biết server đã tạo lịch hay chưa.', 'Only that no response came; not whether the server created the booking.', 'Request mất và response mất trông giống hệt nhau.', 'A lost request and a lost response look identical.'),
        ('q2', 'Phương thức HTTP nào idempotent theo RFC 9110?', 'Which HTTP methods are idempotent per RFC 9110?', 'PUT, DELETE và các phương thức an toàn như GET.', 'PUT, DELETE and the safe methods such as GET.', 'POST và PATCH thì không.', 'POST and PATCH are not.'),
        ('q3', 'Idempotency-Key nên được sinh khi nào?', 'When should the Idempotency-Key be generated?', 'Một lần cho mỗi ý định của người dùng, lưu bền và dùng lại ở mọi lần thử.', 'Once per user intent, stored durably and reused on every attempt.', 'Key mới mỗi lần thử thì server không nhận ra lần thử lại.', 'A new key per attempt means the server cannot recognise retries.'),
        ('q4', 'Vì sao cần jitter khi đã có exponential backoff?', 'Why add jitter when you already have exponential backoff?', 'Vì không có jitter, các máy lỗi cùng lúc vẫn thử lại cùng lúc.', 'Because without it, phones that failed together still retry together.', 'Jitter rải các lần thử ra theo thời gian.', 'Jitter spreads the attempts out in time.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
