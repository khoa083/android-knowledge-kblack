# Kiến trúc · G4: data layer: repository, data source, offline-first (Phần 1)
# Nguồn: developer.android.com Build an offline-first app, Data layer (đọc 2026-11-24).
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'g4': ['hook', 'sources', 'reads', 'writes', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.offline.' + k, vi, en)
    m('title', 'Danh sách giờ trống: đọc từ đâu, ghi vào đâu', 'The free-slot list: where to read, where to write')
    m('overview', 'Màn Chọn giờ có hai nguồn: mạng (máy chủ biết giờ nào còn trống) và database trên máy (bản đã lưu). Ba cách: (1) màn hình đọc database khi mở, nhưng làm mới thì repository trả thẳng kết quả mạng cho UI; (2) database là nguồn sự thật: mạng chỉ ghi vào database, UI chỉ đọc database; (3) hủy một lịch lúc mất mạng bằng cách ghi database trước rồi xếp việc đồng bộ.',
      'The Choose a time screen has two sources: the network (the server knows which slots are free) and the on-device database (the saved copy). Three approaches: (1) the screen reads the database when it opens, but on refresh the repository hands the network result straight to the UI; (2) the database is the source of truth: the network only writes into it and the UI only reads it; (3) cancel an appointment while offline by writing the database first and queueing a sync.')
    m('wrapup', 'Khi UI đọc từ hai nơi, mỗi lần nó thấy một bản khác nhau, và bản mạng vừa tải không sống qua lần mở màn sau. Offline-first đặt database làm nguồn sự thật duy nhất: mạng chỉ cập nhật database, UI quan sát database qua Flow, nên mọi màn thấy cùng một bản, có mạng hay không. Ghi cũng đi qua database trước, rồi mới đẩy lên máy chủ.',
      'When the UI reads from two places it sees a different copy each time, and the freshly downloaded network copy does not survive the next time the screen opens. Offline-first makes the database the single source of truth: the network only updates the database, the UI observes the database through a Flow, so every screen sees the same copy, online or not. Writes also go to the database first, then up to the server.')
    m('simp.1', 'Một màn hình, một bảng giờ trống. Database và WorkManager được rút còn vài lời gọi; chi tiết Room và WorkManager thuộc track Lưu dữ liệu (h4, h7).', 'One screen, one free-slot table. The database and WorkManager are cut to a few calls; Room and WorkManager details belong to the Saving Data track (h4, h7).')
    m('ctl.hint', 'Đổi cách làm rồi đi lại bốn bước; xem tab "Làn thời gian".', 'Switch the approach and walk the four steps again; watch the "Timeline lanes" tab.')
    m('ctl.case', 'Cách làm', 'Approach')
    for k, vi, en in [('mixed', 'UI đọc cả mạng lẫn DB', 'the UI reads both network and DB'), ('ssot', 'DB là nguồn sự thật', 'the DB is the source of truth'), ('lazy', 'hủy lịch lúc mất mạng (ghi lười)', 'cancel while offline (lazy write)')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Màn hình, repository, database, mạng', 'Screen, repository, database, network')
    m('diagramDesc', 'Màn hình hỏi repository; repository đọc và ghi database, gọi mạng; dữ liệu đi ngược lên', 'The screen asks the repository; the repository reads and writes the database and calls the network; data flows back up')
    for k, vi, en in [('ui', 'Màn Chọn giờ', 'Choose a time'), ('repo', 'SlotRepository', 'SlotRepository'), ('db', 'Cơ sở dữ liệu (Room)', 'Database (Room)'), ('net', 'Nguồn mạng (máy chủ)', 'Network source (server)')]:
        m('n.' + k, vi, en)
    m('met.src', 'UI đọc từ', 'The UI reads from'); m('met.ui', 'UI có bản mới nhất', 'The UI has the latest copy'); m('met.db', 'DB có bản mới nhất', 'The DB has the latest copy')
    for k, vi, en in [('db', 'database', 'the database'), ('net', 'mạng (trả thẳng)', 'the network (directly)')]:
        m('src.' + k, vi, en)
    for k, vi, en in [('yes', 'có', 'yes'), ('no', 'không', 'no')]:
        m('fresh.' + k, vi, en)
    a('cap.offline', 'Từ trái sang phải: màn hình, repository, database; mạng ở dưới. Hạt chạy ngược mũi tên là dữ liệu đi lên. Khối viền đỏ đang giữ hay hiện bản cũ; khối gạch chéo là mạng đang mất.',
      'Left to right: screen, repository, database; the network below. Dots moving against an arrow are data going up. A red-outlined box holds or shows a stale copy; a hatched box is the network being unavailable.')
    S = [
        ('mixed', 's1', 'Mở màn: hiện bản đã lưu hôm qua', 'Open the screen: show yesterday\'s saved copy',
         'Repository trả Flow từ database; màn hình hiện 9:00 và 9:30 còn trống, theo bản lưu hôm qua.',
         'The repository returns a Flow from the database; the screen shows 9:00 and 9:30 as free, per yesterday\'s copy.'),
        ('mixed', 's2', 'Kéo làm mới: kết quả mạng đi thẳng tới UI', 'Pull to refresh: the network result goes straight to the UI',
         'Máy chủ trả bản mới: 9:30 đã có người đặt. refresh() trả danh sách này cho ViewModel, ViewModel đưa vào state. UI đúng, nhưng database không được ghi.',
         'The server returns a new copy: 9:30 is now taken. refresh() hands this list to the ViewModel, which puts it in state. The UI is right, but the database was never written.'),
        ('mixed', 's3', 'Mở lại màn: 9:30 lại hiện là còn trống', 'Reopen the screen: 9:30 shows as free again',
         'Lần mở sau, hay một màn khác đọc database, vẫn thấy bản hôm qua. Người dùng chọn 9:30 và nhận lỗi "giờ này đã có người đặt".',
         'The next time it opens, or any other screen reading the database, still sees yesterday\'s copy. The user picks 9:30 and gets "this slot is taken".'),
        ('mixed', 's4', 'Mất mạng: chỉ còn bản cũ', 'Offline: only the old copy is left',
         'Không có mạng thì làm mới thất bại, và database chưa bao giờ nhận bản mới. App vẫn đọc được, nhưng đọc dữ liệu cũ hơn cái người dùng đã thấy.',
         'Offline, the refresh fails, and the database never received the new copy. The app can still read, but it reads data older than what the user has already seen.'),
        ('ssot', 's1', 'Mở màn: UI quan sát database', 'Open the screen: the UI observes the database',
         'Repository chỉ có một hàm đọc: Flow từ database. ViewModel đổi nó thành StateFlow; màn hình hiện bản đã lưu.',
         'The repository has a single read function: a Flow from the database. The ViewModel turns it into a StateFlow; the screen shows the saved copy.'),
        ('ssot', 's2', 'Làm mới: mạng chỉ ghi vào database', 'Refresh: the network only writes into the database',
         'refresh() tải danh sách mới rồi ghi vào database. Nó không trả gì cho UI; UI chưa đổi ở bước này.',
         'refresh() downloads the new list and writes it into the database. It returns nothing to the UI; the UI has not changed yet at this step.'),
        ('ssot', 's3', 'Database phát lại: mọi màn cùng thấy bản mới', 'The database emits again: every screen sees the new copy',
         'Bảng giờ trống đổi nên Flow phát danh sách mới; màn Chọn giờ và mọi màn khác đang quan sát cùng cập nhật. Lần mở sau cũng thấy bản mới, vì nó đã nằm trong database.',
         'The free-slot table changed, so the Flow emits the new list; Choose a time and every other observing screen update together. The next open sees the new copy too, because it is in the database.'),
        ('ssot', 's4', 'Mất mạng: vẫn đọc được bản mới nhất đã lưu', 'Offline: still reads the latest saved copy',
         'Làm mới ném lỗi; repository báo lỗi đó riêng (thông báo "đang ngoại tuyến"), không xóa dữ liệu. Màn hình vẫn hiện bản mới nhất đã lưu.',
         'The refresh throws; the repository reports that error separately ("you are offline") and does not wipe data. The screen still shows the latest saved copy.'),
        ('lazy', 's1', 'Hủy lịch lúc mất mạng: ghi database trước', 'Cancel while offline: write the database first',
         'Người dùng bấm Hủy lịch 10:00. Repository đánh dấu lịch đã hủy trong database, kèm cờ "chờ đồng bộ".',
         'The user taps Cancel on the 10:00 appointment. The repository marks it cancelled in the database, with a "pending sync" flag.'),
        ('lazy', 's2', 'UI cập nhật ngay, dù chưa có mạng', 'The UI updates at once, still offline',
         'Database đổi nên Flow phát lại; màn hình hiện "đã hủy (chờ đồng bộ)". Người dùng không phải chờ mạng.',
         'The database changed, so the Flow emits again; the screen shows "cancelled (pending sync)". The user does not wait for the network.'),
        ('lazy', 's3', 'Xếp việc đồng bộ với WorkManager', 'Queue the sync with WorkManager',
         'Repository xếp một việc duy nhất "sync-cancel-<id>" chỉ chạy khi có mạng. Việc này sống qua cả lúc app bị đóng hay máy khởi động lại.',
         'The repository enqueues a unique "sync-cancel-<id>" job that runs only when online. The job survives the app being closed or the device restarting.'),
        ('lazy', 's4', 'Có mạng: đẩy lên máy chủ, xóa cờ chờ', 'Back online: push to the server, clear the pending flag',
         'WorkManager chạy worker: gọi api.cancel(id); thành công thì xóa cờ chờ trong database, lỗi thì thử lại sau. UI đổi sang "đã hủy".',
         'WorkManager runs the worker: it calls api.cancel(id); on success it clears the pending flag in the database, on failure it retries later. The UI changes to "cancelled".'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi bốn bước của từng cách; so cột "UI có bản mới nhất" và "DB có bản mới nhất".', 'Walk the four steps of each approach; compare "The UI has the latest copy" with "The DB has the latest copy".'),
        ('mixed.s2', 'Offline-first: thao tác đọc của repository đọc thẳng từ nguồn cục bộ; mọi cập nhật ghi vào nguồn cục bộ trước để nó báo cho người đọc. Ở đây cả hai đều bị bỏ qua. [[src:ax-offline-first]]', 'Offline-first: repository reads come straight from the local data source; every update is written there first so it notifies its readers. Both are skipped here. [[src:ax-offline-first]]'),
        ('mixed.s3', 'Nguồn cục bộ phải là nơi duy nhất tầng trên đọc, để dữ liệu nhất quán giữa các trạng thái kết nối. [[src:ax-offline-first]]', 'The local data source must be the only place higher layers read from, to keep data consistent across connection states. [[src:ax-offline-first]]'),
        ('mixed.s4', 'Tối thiểu, một app offline-first phải đọc được khi không có mạng; app này đọc được, nhưng đọc nhầm bản cũ.', 'At a minimum an offline-first app must be able to read without network; this app can, but it reads the stale copy.'),
        ('ssot.s2', 'Repository chỉ báo cho người đọc khi dữ liệu đổi bằng cách cập nhật nguồn cục bộ trước. [[src:ax-offline-first]]', 'The repository can only notify its readers of changes by updating its local data source first. [[src:ax-offline-first]]'),
        ('ssot.s3', 'Đọc qua kiểu quan sát được (Flow) để khi có dữ liệu mới, app hiện ngay; ViewModel đổi Flow thành StateFlow bằng stateIn. [[src:ax-offline-first]]', 'Reads use observable types (Flow) so new data shows as soon as it arrives; the ViewModel turns the Flow into a StateFlow with stateIn. [[src:ax-offline-first]]'),
        ('ssot.s4', 'Lỗi đọc từ mạng xử lý riêng (thử lại với backoff tăng dần, hay chờ có mạng); dữ liệu cục bộ vẫn hiện. [[src:ax-offline-first]]', 'Network read errors are handled separately (retry with exponential backoff, or wait for connectivity); local data keeps showing. [[src:ax-offline-first]]'),
        ('lazy.s2', 'Ghi lười: ghi vào nguồn cục bộ trước, rồi xếp việc báo cho mạng sớm nhất có thể. [[src:ax-offline-first]]', 'Lazy writes: write to the local data source first, then queue the write to notify the network as soon as feasible. [[src:ax-offline-first]]'),
        ('lazy.s3', 'Rút hàng đợi ghi khi có mạng là việc cần chạy bền bỉ, thường giao cho WorkManager. [[src:ax-offline-first]]', 'Draining an offline write queue is persistent work, usually delegated to WorkManager. [[src:ax-offline-first]]'),
        ('lazy.s4', 'Khi cả máy và máy chủ cùng sửa một dữ liệu, cần giải quyết xung đột; phần này nằm ở track Thiết kế hệ thống (i8).', 'When the device and the server both change the same data, conflicts must be resolved; that belongs to the System Design track (i8).')]:
        m('co.' + k, vi, en)
    a('preset.offline', 'Kiến trúc · database là nguồn sự thật (offline-first)', 'Architecture · the database as the source of truth (offline-first)')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.off', 'Làn thời gian', 'Timeline lanes')
    z('off.cap', 'Mỗi hàng là một làn: máy chủ, database trên máy, repository, màn hình. Mỗi cột là một bước; cột của bước đang xem được tô.', 'Each row is a lane: the server, the on-device database, the repository, the screen. Each column is a step; the current step\'s column is highlighted.')
    z('off.legend', 'Ô đỏ: đang giữ hay hiện bản cũ. Ô mờ: làn đó không hoạt động hay đang mất mạng.', 'Red cell: holding or showing a stale copy. Faded cell: that lane is idle or offline.')
    z('off.lane', 'Làn', 'Lane')
    for k, vi, en in [('net', 'Máy chủ (mạng)', 'Server (network)'), ('db', 'Database trên máy', 'On-device database'), ('repo', 'Repository', 'Repository'), ('ui', 'Màn hình', 'Screen')]:
        z('off.lane.' + k, vi, en)
    cols = {
        'mixed': [('Mở màn', 'Open'), ('Làm mới', 'Refresh'), ('Mở lại', 'Reopen'), ('Mất mạng', 'Offline')],
        'ssot': [('Mở màn', 'Open'), ('Làm mới', 'Refresh'), ('DB phát lại', 'DB emits'), ('Mất mạng', 'Offline')],
        'lazy': [('Bấm Hủy (mất mạng)', 'Tap Cancel (offline)'), ('UI cập nhật', 'UI updates'), ('Xếp việc', 'Queue the job'), ('Có mạng lại', 'Back online')],
    }
    for c, lst in cols.items():
        for k, (vi, en) in enumerate(lst):
            z('off.col.%s.%d' % (c, k), vi, en)
    for k, vi, en in [
        ('idle', 'không được gọi', 'not called'), ('offline', 'mất mạng', 'offline'), ('returnsNew', 'trả bản mới: 9:30 đã kín', 'returns the new copy: 9:30 taken'),
        ('receivesCancel', 'nhận cancel(10:00)', 'receives cancel(10:00)'),
        ('oldList', 'bản hôm qua: 9:00, 9:30 trống', 'yesterday\'s copy: 9:00, 9:30 free'), ('stillOld', 'vẫn bản hôm qua', 'still yesterday\'s copy'),
        ('written', 'được ghi bản mới', 'gets the new copy written'), ('emits', 'bảng đổi: Flow phát lại', 'table changed: the Flow emits'), ('keepNew', 'giữ bản mới nhất đã lưu', 'keeps the latest saved copy'),
        ('markPending', 'lịch 10:00: đã hủy, chờ đồng bộ', '10:00: cancelled, pending sync'), ('emitsPending', 'Flow phát lại', 'the Flow emits'), ('pending', 'vẫn chờ đồng bộ', 'still pending sync'),
        ('clearPending', 'xóa cờ chờ', 'clears the pending flag'),
        ('readDb', 'đọc Flow từ DB', 'reads the Flow from the DB'), ('passThrough', 'trả thẳng kết quả mạng cho UI, không ghi DB', 'hands the network result to the UI, no DB write'),
        ('writeDb', 'ghi kết quả mạng vào DB', 'writes the network result into the DB'), ('flowEmits', 'chuyển tiếp Flow', 'forwards the Flow'),
        ('refreshFail', 'làm mới lỗi: báo riêng, không xóa dữ liệu', 'refresh fails: reported separately, data kept'),
        ('writeLocalFirst', 'ghi DB trước', 'writes the DB first'), ('queued', 'WorkManager: chờ có mạng', 'WorkManager: waits for network'), ('workerRuns', 'worker chạy, gọi api.cancel', 'the worker runs, calls api.cancel'),
        ('showOld', '9:00, 9:30 trống', '9:00, 9:30 free'), ('showNew', '9:00 trống, 9:30 đã kín', '9:00 free, 9:30 taken'), ('showOldAgain', 'lại thấy 9:30 trống', 'sees 9:30 free again'),
        ('showOldOffline', 'bản hôm qua, không biết 9:30 đã kín', 'yesterday\'s copy, unaware 9:30 is taken'), ('showNewOffline', 'bản mới nhất đã lưu, kèm "đang ngoại tuyến"', 'the latest saved copy, plus "you are offline"'),
        ('tapCancel', 'bấm Hủy lịch 10:00', 'taps Cancel on 10:00'), ('showPending', '10:00 đã hủy (chờ đồng bộ)', '10:00 cancelled (pending sync)'), ('showSynced', '10:00 đã hủy', '10:00 cancelled')]:
        z('off.cell.' + k, vi, en)

    C = 'g4'
    a(C + '.title', 'Data layer: repository, data source và offline-first', 'The data layer: repositories, data sources and offline-first')
    a(C + '.essence', 'Repository gộp các data source (mạng, database, file) và là lối vào duy nhất của tầng data.\nTrong app offline-first, database trên máy là nguồn sự thật: tầng trên chỉ đọc nó, qua Flow. Mạng không trả dữ liệu thẳng cho UI mà ghi vào database; database đổi thì mọi người đọc cùng thấy.\nGhi cũng đi qua database trước. Với dữ liệu cần đẩy lên máy chủ, xếp việc đồng bộ chạy khi có mạng.',
      'A repository combines data sources (network, database, files) and is the only entry point to the data layer.\nIn an offline-first app, the on-device database is the source of truth: higher layers read only from it, through a Flow. The network does not hand data straight to the UI; it writes into the database, and when the database changes every reader sees it.\nWrites go through the database first too. For data that must reach the server, queue a sync that runs when the network is available.')
    a(C + '.goal.g1', 'Đã thấy bản cũ quay lại khi mở lại màn', 'Saw the stale copy come back on reopening')
    a(C + '.goal.g2', 'Đã đi hết bốn bước', 'Walked all four steps')
    a(C + '.sim.arch.offline', 'đọc từ đâu, ghi vào đâu', 'where to read, where to write')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Màn Chọn giờ đọc database khi mở. Người dùng kéo làm mới; repository gọi mạng và trả danh sách mới thẳng cho ViewModel, không ghi database. Người dùng thoát rồi mở lại màn. Họ thấy bản nào?',
      'Choose a time reads the database when it opens. The user pulls to refresh; the repository calls the network and hands the new list straight to the ViewModel, without writing the database. The user leaves and reopens the screen. Which copy do they see?')
    B(C, S_, 1, 'ans', 'Bản cũ. Bản mới chỉ nằm trong state của lần mở trước; database, nơi màn hình đọc khi mở, chưa bao giờ nhận nó. Mô phỏng bên dưới so cách này với database làm nguồn sự thật. [[src:ax-offline-first]]',
      'The old one. The new copy lived only in the previous visit\'s state; the database, which the screen reads on opening, never received it. The simulation below compares this with the database as source of truth. [[src:ax-offline-first]]')

    S_ = 'sources'
    a(C + '.sec.%s.title' % S_, 'Repository, hai data source và nguồn sự thật', 'A repository, two data sources and the source of truth')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Tầng data gồm các repository, mỗi repository gộp không hoặc nhiều data source. Tầng khác không bao giờ dùng thẳng data source: repository là lối vào. Mỗi repository định nghĩa một nguồn sự thật; dữ liệu nó lộ ra luôn lấy từ nguồn đó. [[src:ax-data-layer]]',
      'The data layer is made of repositories, each combining zero or more data sources. Other layers never use a data source directly: the repository is the entry point. Each repository defines a single source of truth; the data it exposes always comes from that source. [[src:ax-data-layer]]')
    B(C, S_, 2, 'p', 'App offline-first có ít nhất hai data source cho mỗi repository cần mạng. Nguồn cục bộ (Room, DataStore, file) là nguồn sự thật chuẩn và là nơi duy nhất tầng trên đọc, để dữ liệu nhất quán dù có mạng hay không. Nguồn mạng là trạng thái thật của hệ thống; nguồn cục bộ đồng bộ với nó, có lúc chậm hơn nó, có lúc đi trước nó khi chưa đẩy được lên. [[src:ax-offline-first]]',
      'An offline-first app has at least two data sources for every repository that needs the network. The local data source (Room, DataStore, files) is the canonical source of truth and the only place higher layers read from, so data stays consistent online or offline. The network data source is the actual state of the system; the local source syncs with it, sometimes lagging behind it, sometimes ahead of it until changes can be pushed. [[src:ax-offline-first]]')
    B(C, S_, 3, 'note', 'Tối thiểu, app offline-first phải đọc được khi không có mạng. Nếu repository có mạng thì nó phải có nguồn cục bộ. [[src:ax-offline-first]]', 'At a minimum, an offline-first app must be able to read without network access. A repository that uses the network must always have a local data source. [[src:ax-offline-first]]')

    S_ = 'reads'
    a(C + '.sec.%s.title' % S_, 'Đọc: quan sát database, mạng chỉ ghi vào', 'Reads: observe the database; the network only writes into it')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Repository lộ các hàm đọc dưới dạng Flow lấy thẳng từ nguồn cục bộ. Khi mạng trả dữ liệu mới, repository ghi vào nguồn cục bộ; nguồn cục bộ quan sát được nên tự báo cho mọi người đọc. Nghĩa là repository chỉ báo cho người đọc khi dữ liệu đổi bằng một cách: cập nhật nguồn cục bộ trước. [[src:ax-offline-first]]',
      'The repository exposes its reads as Flows taken straight from the local data source. When the network returns new data, the repository writes it into the local source; the local source is observable, so it notifies every reader itself. In other words, the repository notifies readers of changes in only one way: by updating the local source first. [[src:ax-offline-first]]')
    B(C, S_, 2, 'kt', 'class OfflineFirstSlotRepository(private val api: SlotApi, private val dao: SlotDao) {\n    fun slots(day: LocalDate): Flow<List<Slot>> = dao.observe(day)   // đọc: chỉ từ DB\n    suspend fun refresh(day: LocalDate) {\n        dao.replace(day, api.slots(day))                          // mạng chỉ ghi vào DB\n    }\n}\n// ViewModel\nval slots = repo.slots(day).stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())',
      'class OfflineFirstSlotRepository(private val api: SlotApi, private val dao: SlotDao) {\n    fun slots(day: LocalDate): Flow<List<Slot>> = dao.observe(day)   // reads: only from the DB\n    suspend fun refresh(day: LocalDate) {\n        dao.replace(day, api.slots(day))                          // the network only writes the DB\n    }\n}\n// ViewModel\nval slots = repo.slots(day).stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())')
    B(C, S_, 3, 'p', 'Lỗi xử lý theo nguồn. Đọc nguồn cục bộ hiếm khi lỗi; bắt lỗi trên Flow bằng catch để người đọc không bị dừng. Lỗi mạng khi làm mới thì báo riêng và có thể thử lại với khoảng chờ tăng dần, hay chờ tới khi có mạng; dữ liệu cục bộ vẫn hiện trong lúc đó. [[src:ax-offline-first]]',
      'Errors are handled per source. Reading the local source rarely fails; catch errors on the Flow with catch so readers are not stopped. Network errors on refresh are reported separately and can be retried with exponential backoff, or deferred until the network returns; local data keeps showing meanwhile. [[src:ax-offline-first]]')

    S_ = 'writes'
    a(C + '.sec.%s.title' % S_, 'Ghi: ba chiến lược', 'Writes: three strategies')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Đọc dùng kiểu quan sát được; ghi dùng API bất đồng bộ như hàm suspend, vì ghi có thể thất bại khi phải đi qua mạng. Tài liệu nêu ba chiến lược, chọn theo loại dữ liệu. [[src:ax-offline-first]]',
      'Reads use observable types; writes use asynchronous APIs such as suspend functions, because writes can fail when they cross the network. The docs give three strategies, chosen by the kind of data. [[src:ax-offline-first]]')
    B(C, S_, 2, 'p', '(1) Chỉ ghi khi online: ghi qua mạng, thành công mới cập nhật nguồn cục bộ, lỗi thì báo người dùng; hợp với giao dịch cần gần thời gian thực như chuyển tiền. (2) Ghi vào hàng đợi: xếp vào hàng, có mạng thì rút hàng với backoff; hợp với dữ liệu không nhất thiết phải tới máy chủ như log, analytics. (3) Ghi lười: ghi nguồn cục bộ trước, rồi xếp việc báo cho mạng sớm nhất có thể; người dùng thấy kết quả ngay. Rút hàng đợi là việc cần chạy bền bỉ, thường giao cho WorkManager. [[src:ax-offline-first]]',
      '(1) Online-only writes: write across the network, update the local source only on success, tell the user on failure; suits near real-time transactions such as money transfers. (2) Queued writes: put the write in a queue and drain it with backoff when online; suits data that need not reach the server, such as logs and analytics. (3) Lazy writes: write the local source first, then queue a write to the network as soon as feasible; the user sees the result at once. Draining a queue is persistent work, usually delegated to WorkManager. [[src:ax-offline-first]]')
    B(C, S_, 3, 'note', 'Room, WorkManager và hàng đợi đồng bộ chi tiết thuộc track Lưu dữ liệu (h4, h7). Xung đột khi máy và máy chủ cùng sửa một bản ghi thuộc track Thiết kế hệ thống (i8).', 'Room, WorkManager and the sync queue in detail belong to the Saving Data track (h4, h7). Conflicts when the device and the server change the same record belong to the System Design track (i8).')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Làm mới xong thấy 9:30 đã kín, nhưng mở lại màn thì 9:30 lại trống; người dùng chọn và bị báo lỗi.', 'After refreshing, 9:30 shows as taken, but on reopening it is free again; the user picks it and gets an error.')
    B(C, S_, 1, 'cause', 'Repository trả kết quả mạng thẳng cho UI mà không ghi database; màn hình đọc database khi mở.', 'The repository hands the network result straight to the UI without writing the database; the screen reads the database when it opens.')
    B(C, S_, 1, 'fix', 'refresh() chỉ ghi vào database; UI chỉ quan sát Flow từ database.', 'refresh() only writes into the database; the UI only observes the database Flow.')
    B(C, S_, 2, 'bug', 'Mất mạng giữa lúc làm mới thì danh sách trống trơn.', 'Losing the network mid-refresh empties the list.')
    B(C, S_, 2, 'cause', 'Repository xóa bảng rồi mới gọi mạng, hay đổi state thành "lỗi" và vứt dữ liệu cũ khi gọi mạng thất bại.', 'The repository clears the table before calling the network, or switches state to "error" and throws away the old data when the call fails.')
    B(C, S_, 2, 'fix', 'Gọi mạng trước, thành công mới thay dữ liệu trong database (trong một giao dịch); lỗi làm mới báo riêng bên cạnh dữ liệu đang có.', 'Call the network first and replace the database data only on success (in one transaction); report refresh errors alongside the data already shown.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Chọn chiến lược ghi cho bốn thao tác của app Hẹn Khám và giải thích: (a) thanh toán phí khám; (b) gửi sự kiện analytics "đã mở màn Chọn giờ"; (c) đánh dấu một bác sĩ là yêu thích; (d) đặt lịch khám (máy chủ quyết định giờ còn trống hay không). (Bài tập của site, theo ba chiến lược ghi trong tài liệu offline-first.) [[src:ax-offline-first]]',
      'Choose a write strategy for four ClinicBook actions and explain: (a) paying the visit fee; (b) sending the analytics event "opened Choose a time"; (c) marking a doctor as a favourite; (d) booking an appointment (the server decides whether the slot is free). (The site\'s own exercise, after the three write strategies in the offline-first docs.) [[src:ax-offline-first]]')
    B(C, S_, 1, 'hint', 'Hỏi: có bắt buộc tới máy chủ không, có gấp không, người dùng có cần biết ngay nếu thất bại không, và ai là người quyết định kết quả.', 'Ask: must it reach the server, is it time-sensitive, must the user know at once if it fails, and who decides the outcome?')
    B(C, S_, 1, 'sol', '(a) Chỉ online: giao dịch tiền cần kết quả ngay, lỗi phải báo. (b) Hàng đợi: không bắt buộc phải tới, không gấp. (c) Ghi lười: chỉ người dùng này quyết định, UI hiện ngay, đồng bộ sau. (d) Chỉ online (hay ghi lười kèm trạng thái "chờ xác nhận" rõ ràng): máy chủ mới biết giờ còn trống, nên không được báo "đã đặt" khi chưa có xác nhận.',
      '(a) Online-only: a money transaction needs an immediate result, and failures must be shown. (b) Queued: it need not arrive and is not urgent. (c) Lazy: only this user decides it, so show it at once and sync later. (d) Online-only (or lazy with a clear "awaiting confirmation" state): only the server knows if the slot is free, so never say "booked" before it confirms.')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Trong app offline-first, tầng trên đọc dữ liệu từ đâu?', 'In an offline-first app, where do higher layers read data from?')
    B(C, S_, 1, 'ans', 'Chỉ từ nguồn cục bộ (database), qua Flow.', 'Only from the local source (the database), through a Flow.')
    B(C, S_, 2, 'ask', 'Dữ liệu mới từ mạng tới UI theo đường nào?', 'How does new data from the network reach the UI?')
    B(C, S_, 2, 'ans', 'Repository ghi nó vào database; database phát lại cho mọi người đọc, trong đó có UI.', 'The repository writes it into the database; the database emits to every reader, the UI included.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Nguyên tắc theo trang Build an offline-first app và Data layer đọc ngày 2026-11-24. Mô phỏng có một màn hình và một bảng; Room, WorkManager và việc giải quyết xung đột được rút gọn và để cho track Lưu dữ liệu và Thiết kế hệ thống. Tài liệu còn nói về đồng bộ do dịch vụ quản lý và các mô hình dữ liệu khác nhau giữa nguồn cục bộ và nguồn mạng; chương chưa đi vào hai phần đó.',
      'The principles follow the Build an offline-first app and Data layer pages as read on 2026-11-24. The simulation has one screen and one table; Room, WorkManager and conflict resolution are abridged and left to the Saving Data and System Design tracks. The docs also cover managed synchronization services and differing data models between local and network sources; this chapter does not go into either.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Repository trong app offline-first trả dữ liệu đọc từ đâu?', 'Where does an offline-first repository serve reads from?', 'Từ nguồn cục bộ, qua Flow.', 'From the local source, through a Flow.', 'Nguồn cục bộ là nguồn sự thật chuẩn.', 'The local source is the canonical source of truth.'),
        ('q2', 'Kết quả làm mới từ mạng nên đi đâu?', 'Where should a network refresh result go?', 'Vào database; không trả thẳng cho UI.', 'Into the database; not straight to the UI.', 'Database đổi thì mọi người đọc được báo.', 'When the database changes, every reader is notified.'),
        ('q3', 'Ghi lười khác ghi chỉ-online ở điểm nào?', 'How do lazy writes differ from online-only writes?', 'Ghi cục bộ trước và hiện ngay, rồi đồng bộ sau.', 'Write locally first and show it at once, then sync later.', 'Chỉ-online ghi qua mạng trước, thành công mới cập nhật cục bộ.', 'Online-only writes over the network first and updates locally only on success.'),
        ('q4', 'Việc rút hàng đợi ghi khi có mạng thường giao cho ai?', 'Who usually drains the offline write queue?', 'Giao cho WorkManager.', 'WorkManager.', 'Đó là việc cần chạy bền bỉ.', 'It is persistent work.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
