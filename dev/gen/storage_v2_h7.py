# Lưu dữ liệu · H7: offline-first và đồng bộ nền (Phần 2)
# Nguồn: developer.android.com Build an offline-first app, Persistent work (đọc 2026-11-24). Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'h7': ['hook', 'strategies', 'queue', 'worker', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.sync', 'Lưu dữ liệu · đặt lịch lúc mất mạng rồi tắt app', 'Saving data · booking offline, then closing the app')
    m = lambda k, vi, en=None: a('m.sync.' + k, vi, en)
    m('title', 'Đặt lịch lúc mất mạng, rồi tắt app', 'Booking while offline, then closing the app')
    m('overview', 'Người dùng đặt lịch #9 trong thang máy, lúc không có mạng, rồi vuốt tắt app. Có ba cách ghi. Một: gọi thẳng máy chủ (online-only, chỉ ghi khi có mạng). Hai: lưu vào Room rồi thử gửi lại trong một coroutine. Ba: lưu vào Room rồi giao việc gửi cho WorkManager (thư viện chạy việc nền bền bỉ); cách này gọi là lazy write, ghi trước gửi sau. Sơ đồ tuần tự theo dõi app, Room, WorkManager và máy chủ.',
      'The user books appointment #9 in a lift, with no network, then swipes the app away. There are three ways to write. One: call the server directly (online-only, write only with a network). Two: save to Room, then retry sending in a coroutine. Three: save to Room, then hand the sending to WorkManager (a library for persistent background work); this is called a lazy write, write now and send later. The sequence diagram follows the app, Room, WorkManager and the server.')
    m('wrapup', 'Dữ liệu quan trọng phải được ghi xuống máy trước, rồi mới tính chuyện gửi đi. Đó là chiến lược lazy write.\nViệc gửi phải giao cho thứ sống lâu hơn app. Coroutine dừng ngay khi app đóng. WorkManager thì lưu công việc của nó trong database riêng, và chạy lại khi có mạng, kể cả sau khi khởi động lại máy. Cột "chờ gửi" trong Room chính là hàng chờ mà worker đọc.\nHình dung: viết thư rồi bỏ vào hòm thư của bưu điện, thay vì cầm thư đứng chờ người đưa thư; bạn có đi đâu thì thư vẫn được gửi.',
      'Important data must be written to the device first; sending comes after. That is the lazy-write strategy.\nThe sending must be handed to something that outlives the app. A coroutine stops as soon as the app closes. WorkManager stores its work in its own database and runs it when the network returns, even after a reboot. The "pending" column in Room is the queue the worker reads.\nPicture writing a letter and dropping it in the post box, instead of holding it while waiting for the postman; wherever you go, the letter still gets sent.')
    m('simp.1', 'Lịch #9, lúc mất mạng và lúc có mạng lại là tình huống của site. Sơ đồ chỉ vẽ tin nhắn chính; WorkManager còn tự lên lịch lại với JobScheduler và thử lại với backoff.', 'Appointment #9 and the moments the network drops and returns are the site\'s scenario. The diagram shows only the main messages; WorkManager also reschedules itself through JobScheduler and retries with backoff.')
    m('simp.2', 'Ba chiến lược ghi và việc dùng Room làm hàng chờ theo tài liệu Android về app offline-first; WorkManager lưu việc bền bỉ còn coroutine dừng khi app đóng theo tài liệu Android về việc chạy nền; đọc ngày 2026-11-24. Cột trạng thái PENDING/SYNCED, id do máy sinh và bài tập Hủy lịch là thiết kế của site. Đồng bộ chiều kéo từ máy chủ và xung đột giữa nhiều máy thuộc track Thiết kế hệ thống phía mobile.',
      "The three write strategies and using Room as the queue follow the Android docs on offline-first apps; WorkManager persisting work while coroutines stop when the app closes follows the Android docs on background work; read on 2026-11-24. The PENDING/SYNCED column, device-generated ids and the Cancel exercise are the site's design. Pull sync from the server and conflicts between devices belong to the Mobile System Design track.")
    m('ctl.hint', 'Đổi cách ghi rồi đi lại; nhìn cột "Máy chủ có" ở bước cuối.', 'Switch the write strategy and walk again; watch the "Server has it" column at the last step.')
    m('ctl.case', 'Cách ghi', 'Write strategy')
    for k, vi, en in [('online', 'gọi máy chủ trực tiếp', 'call the server directly'), ('coroutine', 'lưu Room + thử lại trong coroutine', 'Room + retry in a coroutine'), ('lazy', 'lưu Room + WorkManager', 'Room + WorkManager')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'App, Room, WorkManager, máy chủ', 'App, Room, WorkManager, server')
    m('diagramDesc', 'Lịch hẹn đi từ app vào Room; WorkManager đọc hàng chờ trong Room và gửi lên máy chủ', 'The appointment goes from the app into Room; WorkManager reads the queue in Room and sends it to the server')
    for k, vi, en in [('app', 'App (lớp ViewModel)', 'App (ViewModel)'), ('db', 'Room (bảng appointment)', 'Room (appointment table)'), ('wm', 'WorkManager', 'WorkManager'), ('server', 'Máy chủ', 'Server')]:
        m('n.' + k, vi, en)
    m('met.inDb', 'Lịch #9 trên máy', 'Appointment #9 on device'); m('met.state', 'Trạng thái đồng bộ', 'Sync state'); m('met.server', 'Máy chủ có #9', 'Server has #9')
    for k, vi, en in [('yes', 'có', 'yes'), ('no', 'không', 'no')]:
        m('yn.' + k, vi, en)
    for k, vi, en in [('none', 'không có', 'none'), ('pending', 'PENDING (chờ gửi)', 'PENDING (waiting)'), ('sending', 'đang gửi', 'sending'), ('synced', 'SYNCED (đã gửi)', 'SYNCED (sent)')]:
        m('q.' + k, vi, en)
    a('cap.sync', 'Từ trái sang phải: app, Room, WorkManager, máy chủ. Tab chính vẽ cùng bốn bên thành sơ đồ tuần tự; khối viền đỏ là chỗ lịch hẹn bị mất hay kẹt.', 'Left to right: app, Room, WorkManager, server. The main tab draws the same four as a sequence diagram; a red outline marks where the appointment is lost or stuck.')
    S = [
        ('online', 's1', 'Bấm Đặt lịch: gọi máy chủ ngay', 'Tap Book: call the server right away',
         'ViewModel gọi api.book trực tiếp. Không có mạng nên yêu cầu không tới được máy chủ.', 'The ViewModel calls api.book directly. There is no network, so the request never reaches the server.'),
        ('online', 's2', 'IOException: không có mạng', 'IOException: no network',
         'Lời gọi ném IOException. Không có gì được ghi ở đâu cả: máy không lưu, máy chủ không nhận.', 'The call throws IOException. Nothing is written anywhere: not on the device, not on the server.'),
        ('online', 's3', 'Báo lỗi cho người dùng', 'Show the user an error',
         'Màn hình hiện "Không có mạng, thử lại sau". Đúng với thao tác phải xác nhận ngay như chuyển tiền; với đặt lịch, người dùng mong app nhớ giúp.', 'The screen says "No network, try later". Right for actions that must be confirmed at once, such as a bank transfer; for a booking, the user expects the app to remember it.'),
        ('online', 's4', 'Người dùng tắt app: lịch chưa từng tồn tại', 'The user closes the app: the booking never existed',
         'Người dùng tưởng đã đặt, hoặc quên thử lại. Không còn dấu vết nào của lịch #9.', 'The user thinks it was booked, or forgets to retry. No trace of appointment #9 remains.'),
        ('coroutine', 's1', 'Lưu #9 vào Room với trạng thái PENDING', 'Save #9 to Room as PENDING',
         'Ghi máy trước: lịch #9 vào bảng appointment với cột sync = PENDING. UI đọc Flow từ Room nên hiện lịch ngay.', 'Local first: #9 goes into the appointment table with sync = PENDING. The UI reads a Flow from Room, so it shows at once.'),
        ('coroutine', 's2', 'Coroutine thử gửi lại mỗi 30 giây', 'A coroutine retries every 30 seconds',
         'Một vòng lặp trong viewModelScope gọi máy chủ, lỗi thì delay rồi thử lại.', 'A loop in viewModelScope calls the server and, on failure, delays and tries again.'),
        ('coroutine', 's3', 'Vuốt tắt app: coroutine dừng theo', 'Swipe the app away: the coroutine stops with it',
         'viewModelScope bị hủy cùng ViewModel; tiến trình có thể bị giết luôn. Không còn ai thử gửi #9.', 'viewModelScope is cancelled with the ViewModel; the process may be killed too. Nobody is left to send #9.'),
        ('coroutine', 's4', '#9 kẹt ở PENDING', '#9 is stuck at PENDING',
         'Lịch vẫn nằm trong Room, nên không mất. Nhưng máy chủ không bao giờ nhận được, tới khi người dùng tình cờ mở lại đúng màn hình đó.', 'The appointment is still in Room, so it is not lost. But the server never gets it, until the user happens to reopen that exact screen.'),
        ('lazy', 's1', 'Lưu #9 vào Room, rồi xếp việc cho WorkManager', 'Save #9 to Room, then enqueue work with WorkManager',
         'Hai dòng: insert với sync = PENDING, rồi enqueueUniqueWork("sync", KEEP, …) với ràng buộc chỉ chạy khi có mạng. Cả hai xong trong vài mili giây.', 'Two lines: insert with sync = PENDING, then enqueueUniqueWork("sync", KEEP, …) constrained to run only with a network. Both finish in milliseconds.'),
        ('lazy', 's2', 'App bị tắt; công việc vẫn được giữ', 'The app is killed; the work is kept',
         'WorkManager đã lưu yêu cầu trong database SQLite riêng của nó. App đóng hay máy khởi động lại, công việc vẫn còn đó.', 'WorkManager has stored the request in its own SQLite database. Whether the app closes or the device reboots, the work is still there.'),
        ('lazy', 's3', 'Có mạng lại: worker đọc hàng chờ và gửi', 'Network back: the worker reads the queue and sends',
         'Ràng buộc mạng được thỏa, WorkManager chạy SyncWorker, kể cả khi app không mở. Worker đọc mọi dòng PENDING trong Room và gửi từng cái; máy chủ trả 201.', 'The network constraint is met and WorkManager runs SyncWorker, even with the app closed. The worker reads every PENDING row in Room and sends each one; the server answers 201.'),
        ('lazy', 's4', 'Đánh dấu SYNCED; lần mở sau, UI thấy ngay', 'Mark it SYNCED; next time the UI sees it',
         'Worker cập nhật #9 thành SYNCED. Lần sau mở app, Flow từ Room hiện lịch đã xác nhận. Nếu gửi lỗi, Result.retry() để WorkManager thử lại với backoff.', 'The worker updates #9 to SYNCED. Next time the app opens, the Flow from Room shows it confirmed. If sending fails, Result.retry() lets WorkManager try again with backoff.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cách ghi; để ý bảng hàng chờ dưới sơ đồ.', 'Walk all four steps of each strategy; watch the queue table below the diagram.'),
        ('online.s2', 'Trang offline-first gọi đây là ghi online-only: ghi qua mạng trước, thành công mới cập nhật máy, lỗi thì ném ra cho bên gọi. [[src:ax-offline-first-data]]', 'The offline-first page calls this an online-only write: write over the network first, update locally on success, otherwise throw to the caller. [[src:ax-offline-first-data]]'),
        ('online.s3', 'Tài liệu đó cũng nói: online-only hợp với thao tác cần gần như thời gian thực, ví dụ chuyển tiền. [[src:ax-offline-first-data]]', 'The same docs say: online-only suits near-real-time actions, such as a bank transfer. [[src:ax-offline-first-data]]'),
        ('online.s4', 'Với dữ liệu người dùng mong app giữ giúp, online-only biến một lần mất mạng thành một lần mất dữ liệu.', 'For data users expect the app to keep, online-only turns a lost connection into lost data.'),
        ('coroutine.s2', 'Ghi máy trước là đúng; phần sai là để việc gửi sống trong một coroutine gắn với màn hình.', 'Writing locally first is right; the mistake is letting the upload live in a coroutine tied to a screen.'),
        ('coroutine.s3', 'Tài liệu Android nói: coroutine dừng ngay khi app đóng; WorkManager dành cho việc phải chạy kể cả khi app thoát hay máy khởi động lại. [[src:ax-persistent-work]]', 'The Android docs say: coroutines stop as soon as the app closes; WorkManager is for work that must run even if the app exits or the device restarts. [[src:ax-persistent-work]]'),
        ('coroutine.s4', 'Dữ liệu không mất nhưng không đi tới đâu: lỗi kiểu này chỉ lộ ra khi máy chủ và máy lệch nhau.', 'The data is not lost but goes nowhere: this kind of bug only shows when server and device disagree.'),
        ('lazy.s2', 'Tài liệu Android nói: công việc đã lên lịch được lưu trong một database SQLite do WorkManager quản lý và được lên lịch lại sau khi khởi động lại máy. [[src:ax-persistent-work]]', 'The Android docs say: scheduled work is stored in an internally managed SQLite database and rescheduled across device reboots. [[src:ax-persistent-work]]'),
        ('lazy.s3', 'Tài liệu Android nói: hàng chờ có thể giữ trong Room và rút như công việc bền bằng WorkManager; ví dụ của trang dùng enqueueUniqueWork với KEEP và NetworkType.CONNECTED. [[src:ax-offline-first-data]]', 'The Android docs say: the queue can be kept in Room and drained as persistent work with WorkManager; its example uses enqueueUniqueWork with KEEP and NetworkType.CONNECTED. [[src:ax-offline-first-data]]'),
        ('lazy.s4', 'Ghi lazy: ghi máy trước, rồi xếp lệnh ghi mạng sớm nhất có thể; trang gọi đây là lựa chọn đúng khi dữ liệu quan trọng. [[src:ax-offline-first-data]]', 'A lazy write: write locally first, then queue the network write at the earliest opportunity; the page calls it the right choice when data is critical. [[src:ax-offline-first-data]]')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.sq', 'Sơ đồ tuần tự', 'Sequence diagram')
    z('sq.cap', 'Cột là các bên, thời gian chạy từ trên xuống. Tin của bước đang xem tô màu chính; nét đứt đỏ là lỗi hay mất mát.', 'Columns are the parties, time runs top to bottom. The current step\'s messages are in the brand colour; red dashes mark failures or loss.')
    z('sq.qcap', 'Hàng chờ gửi: lịch #9 đang ở đâu sau bước này.', 'Upload queue: where appointment #9 is after this step.')
    z('sq.legend', 'Mũi tên quay về chính cột đó là việc một bên tự làm (tự gửi cho mình).', 'An arrow looping back to the same column is something a party does on its own.')
    for k, vi, en in [('app', 'App', 'App (ViewModel)'), ('db', 'Room', 'Room DB'), ('wm', 'WorkManager', 'WorkManager (job)'), ('server', 'Máy chủ', 'Server')]:
        z('sq.p.' + k, vi, en)
    for k, vi, en in [
        ('post', 'POST /appointments (mất mạng)', 'POST /appointments (offline)'), ('ioerr', 'IOException', 'IOException thrown'),
        ('showErr', 'báo lỗi, không lưu gì', 'error shown, nothing saved'), ('closed', 'người dùng tắt app', 'user closes the app'),
        ('insertPending', 'INSERT #9 (PENDING)', 'INSERT #9 as PENDING'), ('flowShow', 'Flow: hiện #9', 'Flow: shows #9'),
        ('retryLater', 'delay(30 s) rồi thử lại', 'delay 30 s, retry'), ('killedCo', 'app tắt: coroutine bị hủy', 'app gone: coroutine cancelled'),
        ('stuck', '#9 kẹt PENDING', '#9 stuck at PENDING'), ('enqueue', 'enqueueUniqueWork(sync, KEEP)', 'enqueueUniqueWork(sync, KEEP) call'),
        ('persisted', 'lưu việc vào SQLite riêng', 'work saved in its SQLite'), ('readPending', 'đọc các dòng PENDING', 'read PENDING rows'),
        ('postWm', 'POST #9', 'POST #9 upload'), ('created', '201 Created', '201 Created reply'),
        ('markSynced', 'UPDATE #9 → SYNCED', 'UPDATE #9 to SYNCED'), ('flowSynced', 'Flow: #9 đã xác nhận', 'Flow: #9 confirmed')]:
        z('sq.m.' + k, vi, en)
    for k, vi, en in [('appt', 'Lịch', 'Appointment'), ('inDb', 'Trên máy', 'On device'), ('state', 'Trạng thái', 'State'), ('server', 'Máy chủ có', 'Server has it')]:
        z('sq.qc.' + k, vi, en)

    C = 'h7'
    a(C + '.title', 'Offline-first và đồng bộ nền', 'Offline-first and background sync')
    a(C + '.essence', 'App offline-first (app vẫn chạy khi mất mạng) đọc từ database trên máy làm nguồn sự thật, và ghi xuống máy trước.\nTài liệu Android nêu ba chiến lược ghi. Online-only: gửi mạng trước, lỗi thì báo. Queued: xếp vào hàng, gửi sau; dành cho dữ liệu không quan trọng. Lazy: ghi máy trước rồi xếp lệnh gửi; dành cho dữ liệu quan trọng.\nViệc gửi phải giao cho WorkManager. Nó lưu công việc trong database riêng, chạy khi đủ điều kiện (có mạng), và sống qua lần tắt app hay khởi động lại máy. Coroutine thì không.',
      'An offline-first app (one that keeps working without a network) reads from the on-device database as its source of truth, and writes to the device first.\nThe Android docs give three write strategies. Online-only: send over the network first, report failures. Queued: put it in a queue, send later; for unimportant data. Lazy: write locally first, then queue the send; for important data.\nThe sending must be handed to WorkManager. It stores work in its own database, runs it when conditions are met (a network), and survives the app being closed or the device rebooting. A coroutine does not.')
    a(C + '.goal.g1', 'Đã thấy app bị tắt', 'Saw the app get closed')
    a(C + '.goal.g2', 'Đã thấy máy chủ có nhận lịch hay không', 'Saw whether the server received the booking')
    a(C + '.sim.storage.sync', 'ba cách ghi khi mất mạng', 'three ways to write while offline')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Hẹn Khám lưu lịch mới vào Room trước, rồi trong viewModelScope thử gửi lên máy chủ mỗi 30 giây tới khi được. Người dùng đặt lịch lúc mất mạng rồi tắt app. Một tuần sau, phòng khám có thấy lịch đó không?',
      'ClinicBook saves a new booking to Room first, then retries sending it to the server every 30 seconds from viewModelScope until it works. A user books while offline and closes the app. A week later, does the clinic see that booking?')
    B(C, S_, 1, 'ans', 'Không, trừ khi người dùng tình cờ mở lại đúng màn hình đó. Lịch vẫn nằm trong Room, nhưng coroutine phụ trách gửi đã dừng ngay khi app đóng. Mô phỏng ngay dưới so cách này với việc giao cho WorkManager. [[src:ax-persistent-work]]',
      'No, unless the user happens to reopen that exact screen. The appointment is still in Room, but the coroutine in charge of sending stopped as soon as the app closed. The simulation just below compares this with handing the job to WorkManager. [[src:ax-persistent-work]]')

    S_ = 'strategies'
    a(C + '.sec.%s.title' % S_, 'Ba chiến lược ghi', 'Three write strategies')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Tài liệu Android về app offline-first đặt database trên máy làm nguồn sự thật. Repository lộ Flow đọc từ database, giao diện quan sát Flow đó, nên việc đọc luôn chạy được khi mất mạng.\nVới việc ghi, tài liệu nêu ba chiến lược. Chiến lược đầu là online-only: ghi qua mạng trước, thành công mới cập nhật máy, lỗi thì ném ra cho người dùng biết. Cách này hợp với việc cần kết quả gần như ngay, như chuyển tiền. [[src:ax-offline-first-data]]',
      'The Android docs on offline-first apps make the on-device database the source of truth. The repository exposes a Flow read from the database and the UI observes it, so reading always works offline.\nFor writes, the docs give three strategies. The first is online-only: write over the network first, update the device only on success, and throw on failure so the user knows. This suits things that need an almost immediate result, such as transferring money. [[src:ax-offline-first-data]]')
    B(C, S_, 2, 'p', 'Chiến lược thứ hai là queued: đưa thao tác vào một hàng chờ, có mạng lại thì gửi dần, mỗi lần lỗi lại chờ lâu hơn (backoff lũy thừa). Hợp với dữ liệu không quan trọng, không gấp, như log hay analytics (số liệu thống kê).\nChiến lược thứ ba là lazy: ghi xuống máy trước, rồi xếp lệnh gửi lên mạng sớm nhất có thể. Tài liệu gọi đây là lựa chọn đúng khi dữ liệu quan trọng, như một lịch hẹn đặt lúc mất mạng. Cái giá: có thể xung đột nếu máy chủ cũng đổi cùng dữ liệu.\nQuy tắc dễ nhớ: thứ người dùng không được phép mất thì ghi máy trước, gửi sau. [[src:ax-offline-first-data]]',
      'The second strategy is queued: put the operation in a queue and send it gradually once the network is back, waiting longer after each failure (exponential backoff). This suits unimportant, non-urgent data such as logs or analytics (usage statistics).\nThe third strategy is lazy: write to the device first, then queue the network write at the earliest opportunity. The docs call this the right choice when the data matters, such as an appointment booked offline. The cost: conflicts are possible if the server changes the same data too.\nRule of thumb: whatever the user must not lose is written locally first and sent later. [[src:ax-offline-first-data]]')
    B(C, S_, 3, 'note', 'Xung đột khi nhiều thiết bị cùng sửa một dữ liệu nằm ngoài chương này (chương I8, "Nhiều thiết bị và xung đột", của track Thiết kế hệ thống phía mobile). Tài liệu chỉ nêu một cách phổ biến: "last write wins", tức mỗi lần ghi kèm dấu thời gian, và máy chủ giữ bản mới hơn. [[src:ax-offline-first-data]]',
      'Conflicts when several devices change the same data are outside this chapter (chapter I8, "Multiple devices and conflicts", of the Mobile System Design track). The docs name one common approach: "last write wins", meaning every write carries a timestamp and the server keeps the newer one. [[src:ax-offline-first-data]]')
    B(C, S_, 3, 'kind', 'source')

    S_ = 'queue'
    a(C + '.sec.%s.title' % S_, 'Hàng chờ nằm trong Room', 'The queue lives in Room')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Với lazy write, chính bảng dữ liệu là hàng chờ. Mỗi dòng có thêm một cột trạng thái đồng bộ, ở đây là PENDING (chờ gửi) hay SYNCED (đã gửi). Lịch mới được chèn với PENDING. Worker đọc mọi dòng PENDING, gửi đi, rồi đổi thành SYNCED.\nVì hàng chờ nằm trong database, nó sống qua mọi lần tắt app. Giao diện còn có thể hiện lịch chưa xác nhận bằng một biểu tượng riêng. Tài liệu Android nói hàng chờ có thể giữ trong Room và rút ra bằng WorkManager. [[src:ax-offline-first-data]]',
      'With a lazy write, the data table itself is the queue. Each row gets an extra sync-status column, here PENDING (waiting to send) or SYNCED (sent). A new appointment is inserted as PENDING. The worker reads every PENDING row, sends it, then marks it SYNCED.\nBecause the queue lives in the database, it survives every time the app is closed. The UI can even show unconfirmed appointments with their own icon. The Android docs say the queue can live in Room and be drained with WorkManager. [[src:ax-offline-first-data]]')
    B(C, S_, 2, 'kt', 'enum class SyncState { PENDING, SYNCED }\n\n@Entity data class Appointment(\n    @PrimaryKey(autoGenerate = true) val id: Long = 0,\n    val slotId: Long,\n    val sync: SyncState = SyncState.PENDING,   // cột trạng thái đồng bộ (cần TypeConverter hay lưu dạng String)\n)\n\n@Query("SELECT * FROM appointment WHERE sync = \'PENDING\' ORDER BY id")\nsuspend fun pending(): List<Appointment>',
      'enum class SyncState { PENDING, SYNCED }\n\n@Entity data class Appointment(\n    @PrimaryKey(autoGenerate = true) val id: Long = 0,\n    val slotId: Long,\n    val sync: SyncState = SyncState.PENDING,   // sync-state column (needs a TypeConverter or String storage)\n)\n\n@Query("SELECT * FROM appointment WHERE sync = \'PENDING\' ORDER BY id")\nsuspend fun pending(): List<Appointment>')
    B(C, S_, 3, 'note', 'Có một bẫy: lịch đã tới máy chủ nhưng tiến trình chết trước khi kịp đánh dấu SYNCED. Lần chạy sau thấy dòng vẫn PENDING và gửi lại, tạo lịch trùng. Cách chữa: gửi kèm một id do máy sinh ra, để máy chủ nhận ra lần gửi lặp và bỏ qua.\nQuy tắc dễ nhớ: mọi lần gửi lại phải an toàn khi bị lặp.',
      'There is a trap: the appointment reached the server but the process died before marking it SYNCED. The next run sees the row still PENDING and sends it again, creating a duplicate. The cure: send a device-generated id with it, so the server recognises the repeat and ignores it.\nRule of thumb: every retry must be safe to repeat.')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'worker'
    a(C + '.sec.%s.title' % S_, 'Giao việc gửi cho WorkManager', 'Handing the upload to WorkManager')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'WorkManager dành cho việc phải chạy chắc chắn, kể cả khi người dùng rời màn hình, app thoát, hay máy khởi động lại. Công việc đã lên lịch được lưu trong một database riêng do WorkManager quản lý.\nNó có ràng buộc (chỉ chạy khi có mạng, khi pin đủ), có công việc duy nhất (không xếp trùng), và có chính sách thử lại với backoff lũy thừa. Coroutine thì dừng ngay khi app đóng.\nQuy tắc dễ nhớ: việc phải xong dù app đã tắt thì giao cho WorkManager, không giao cho coroutine. [[src:ax-persistent-work]]',
      'WorkManager is for work that must run for sure, even if the user leaves the screen, the app exits, or the device reboots. Scheduled work is stored in a database WorkManager manages itself.\nIt has constraints (run only with a network, only with enough battery), unique work (no duplicate queueing), and a retry policy with exponential backoff. A coroutine stops as soon as the app closes.\nRule of thumb: work that must finish even after the app is closed goes to WorkManager, not to a coroutine. [[src:ax-persistent-work]]')
    B(C, S_, 2, 'kt', 'val onlyWhenOnline = Constraints.Builder()\n    .setRequiredNetworkType(NetworkType.CONNECTED)\n    .build()\n\nworkManager.enqueueUniqueWork(\n    "sync",\n    ExistingWorkPolicy.KEEP,          // đã có việc "sync" đang chờ thì giữ nó, không tạo thêm\n    OneTimeWorkRequestBuilder<SyncWorker>().setConstraints(onlyWhenOnline).build(),\n)',
      'val onlyWhenOnline = Constraints.Builder()\n    .setRequiredNetworkType(NetworkType.CONNECTED)\n    .build()\n\nworkManager.enqueueUniqueWork(\n    "sync",\n    ExistingWorkPolicy.KEEP,          // if a "sync" job is already waiting, keep it; do not add another\n    OneTimeWorkRequestBuilder<SyncWorker>().setConstraints(onlyWhenOnline).build(),\n)')
    B(C, S_, 3, 'p', 'Một worker cho cả hàng chờ, không phải một worker cho mỗi lịch. Worker đọc mọi dòng PENDING lúc nó chạy, nên đặt ba lịch lúc mất mạng chỉ cần một công việc "sync".\nTrong doWork (của CoroutineWorker, là hàm suspend), lỗi mạng thì trả Result.retry() để WorkManager thử lại sau, mỗi lần chờ lâu hơn. Gửi xong hết thì trả Result.success(). Ví dụ trong tài liệu Android dùng đúng chính sách KEEP (giữ việc đang chờ, không xếp thêm) và điều kiện NetworkType.CONNECTED. [[src:ax-offline-first-data]]',
      'One worker for the whole queue, not one worker per appointment. The worker reads every PENDING row when it runs, so booking three appointments offline needs just one "sync" job.\nIn doWork (of a CoroutineWorker, a suspend function), a network error returns Result.retry() so WorkManager tries again later, waiting longer each time. When everything is sent, it returns Result.success(). The example in the Android docs uses exactly the KEEP policy (keep the waiting job, do not queue another) and the NetworkType.CONNECTED constraint. [[src:ax-offline-first-data]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Phòng khám không thấy một số lịch người dùng khẳng định đã đặt; trên máy người dùng, các lịch đó vẫn hiện bình thường.', 'The clinic is missing some bookings users insist they made; on the users\' devices, those bookings still show normally.')
    B(C, S_, 1, 'cause', 'Lịch được lưu vào Room nhưng việc gửi chạy trong viewModelScope. App bị tắt trước khi có mạng, và không còn ai gửi.', 'The bookings were saved to Room, but the upload ran in viewModelScope. The app was closed before the network came back, and nobody was left to send them.')
    B(C, S_, 1, 'fix', 'Sau khi chèn, gọi enqueueUniqueWork với ràng buộc có mạng; để worker đọc hàng chờ PENDING. UI hiện biểu tượng "chờ gửi" cho dòng PENDING.', 'After inserting, call enqueueUniqueWork with a network constraint; let the worker read the PENDING queue. Show a "waiting to send" icon for PENDING rows.')
    B(C, S_, 2, 'bug', 'Sau một đêm mất mạng, máy chủ nhận cùng một lịch hai lần.', 'After a night offline, the server receives the same booking twice.')
    B(C, S_, 2, 'cause', 'Worker gửi thành công, nhưng tiến trình bị dừng trước khi kịp đánh dấu SYNCED. Lần chạy sau thấy dòng vẫn PENDING và gửi lại.', 'The worker sent it successfully, but the process stopped before it could mark the row SYNCED. The next run saw it still PENDING and sent it again.')
    B(C, S_, 2, 'fix', 'Gửi kèm một id do máy sinh khi tạo lịch; máy chủ dùng nó để bỏ qua lần gửi lặp.', 'Send a client-generated id created with the booking; the server uses it to ignore repeated sends.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Thêm chức năng Hủy lịch chạy được lúc mất mạng. Yêu cầu: (1) lịch hủy biến khỏi danh sách ngay; (2) lệnh hủy tới máy chủ dù người dùng tắt app; (3) hủy một lịch còn PENDING (chưa từng lên máy chủ) thì không gọi máy chủ. Mô tả cột trạng thái, các bước trong repository và việc worker làm.',
      'Add a Cancel booking feature that works offline. Requirements: (1) the cancelled booking disappears from the list at once; (2) the cancellation reaches the server even if the user closes the app; (3) cancelling a booking still PENDING (never on the server) does not call the server. Describe the state column, the repository steps and what the worker does.')
    B(C, S_, 1, 'hint', 'Thêm một trạng thái cho "chờ hủy". Danh sách lọc bỏ trạng thái đó. Trường hợp (3) xử lý ngay trong repository, không cần mạng.', 'Add a state for "waiting to cancel". The list filters it out. Case (3) is handled right in the repository, no network needed.')
    B(C, S_, 1, 'sol', 'Cột sync có ba giá trị: PENDING, SYNCED, CANCEL_PENDING. Repository.cancel(id): nếu dòng đang PENDING thì xóa luôn dòng (máy chủ chưa biết nó); nếu SYNCED thì đổi thành CANCEL_PENDING rồi enqueueUniqueWork("sync", KEEP, …). Truy vấn danh sách bỏ các dòng CANCEL_PENDING nên lịch biến mất ngay. Worker gửi các dòng PENDING như cũ, gửi lệnh hủy cho các dòng CANCEL_PENDING rồi xóa chúng; lỗi mạng thì Result.retry().',
      'The sync column has three values: PENDING, SYNCED, CANCEL_PENDING. Repository.cancel(id): if the row is PENDING, delete it outright (the server never knew it); if SYNCED, change it to CANCEL_PENDING, then enqueueUniqueWork("sync", KEEP, …). The list query excludes CANCEL_PENDING rows, so the booking vanishes at once. The worker sends PENDING rows as before, sends a cancellation for CANCEL_PENDING rows and then deletes them; on a network error it returns Result.retry().')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Với dữ liệu quan trọng như một lịch hẹn, trang offline-first khuyên chiến lược ghi nào?', 'For critical data such as a booking, which write strategy does the offline-first page recommend?')
    B(C, S_, 1, 'ans', 'Lazy write: ghi máy trước, rồi xếp lệnh ghi mạng sớm nhất có thể.', 'A lazy write: write locally first, then queue the network write at the earliest opportunity.')
    B(C, S_, 2, 'ask', 'Vì sao WorkManager vẫn chạy được việc gửi sau khi app bị tắt?', 'Why can WorkManager still run the upload after the app is killed?')
    B(C, S_, 2, 'ans', 'Nó lưu công việc trong database SQLite riêng và lên lịch lại cả sau khi khởi động lại máy; khi ràng buộc mạng được thỏa, nó chạy worker dù app không mở.', 'It stores work in its own SQLite database and reschedules it even after a reboot; once the network constraint is met, it runs the worker even with the app closed.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Ba chiến lược ghi trong trang offline-first là gì?', 'What are the three write strategies on the offline-first page?', 'Online-only (chỉ ghi mạng), queued (xếp hàng), lazy (ghi máy trước).', 'Online-only, queued, lazy.', 'Online-only cho việc thời gian thực; queued cho dữ liệu không quan trọng; lazy cho dữ liệu quan trọng.', 'Online-only for real-time work; queued for non-critical data; lazy for critical data.'),
        ('q2', 'Coroutine trong viewModelScope có tiếp tục gửi sau khi app đóng không?', 'Does a coroutine in viewModelScope keep uploading after the app closes?', 'Không.', 'No.', 'Coroutine dừng khi app đóng; việc phải sống lâu hơn app thì giao WorkManager.', 'Coroutines stop when the app closes; work that must outlive the app goes to WorkManager.'),
        ('q3', 'ExistingWorkPolicy.KEEP làm gì khi đã có việc "sync" đang chờ?', 'What does ExistingWorkPolicy.KEEP do when a "sync" job is already waiting?', 'Giữ việc cũ, không thêm việc mới.', 'Keeps the existing one and adds nothing.', 'Một worker đọc cả hàng chờ, nên không cần nhiều việc.', 'One worker reads the whole queue, so more jobs are not needed.'),
        ('q4', 'Worker gặp lỗi mạng thì trả về gì?', 'What does the worker return on a network error?', 'Result.retry().', 'Result.retry().', 'WorkManager thử lại với backoff lũy thừa.', 'WorkManager retries with exponential backoff.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
