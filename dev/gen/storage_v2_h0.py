# Lưu dữ liệu · H0: bản đồ track (viết cuối, đặt đầu track)
# Tổng hợp từ H1–H9; mọi khẳng định có nguồn ở chương được trỏ tới. Trần: 6 mục.

SEC_ORDER = {'h0': ['hook', 'order', 'index', 'links', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.map.' + k, vi, en)
    m('title', 'Gặp triệu chứng này thì đọc chương nào', 'Seen this symptom? Read this chapter')
    m('overview', 'Chọn một lỗi lưu dữ liệu hay gặp. Mô phỏng đi qua bốn bước: triệu chứng bạn thấy; lúc nó lộ ra (lúc chạy, sai mà không báo, sau khi cập nhật app, hay khi đổi máy); nguyên nhân bên dưới; và chương giải thích nguyên nhân đó.',
      'Pick a common data-storage bug. The simulation walks four steps: the symptom you see; when it shows up (at runtime, silently wrong, after an app update, or on a new phone); the cause underneath; and the chapter that explains that cause.')
    m('wrapup', 'Lỗi lưu dữ liệu hay lộ ra muộn: sau vài tháng khi file lớn dần, sau một bản cập nhật, hay khi người dùng đổi máy. Tới lúc đó, dữ liệu thật của người dùng đã bị cuốn vào. Biết lỗi thường lộ ra lúc nào giúp bạn kiểm đúng chỗ trước khi phát hành.\nQuy tắc dễ nhớ: với dữ liệu, lỗi hôm nay là dữ liệu mất của tháng sau.',
      "Storage bugs tend to show up late: months later as a file grows, after an update, or when the user switches phones. By then, the user's real data is caught up in it. Knowing when a bug usually shows up helps you test the right places before release.\nRule of thumb: with data, today's bug is next month's lost data.")
    m('simp.1', 'Mỗi triệu chứng chỉ trỏ tới một chương chính; lỗi thật có thể có nhiều nguyên nhân cùng lúc.', 'Each symptom points to one main chapter; real bugs can have several causes at once.')
    m('ctl.hint', 'Chọn triệu chứng rồi đi bốn bước; tab "Bảng tra" liệt kê tất cả.', 'Pick a symptom and walk the four steps; the "Lookup table" tab lists them all.')
    m('ctl.symptom', 'Triệu chứng', 'Symptom')
    m('diagramTitle', 'Triệu chứng, lúc lộ ra, nguyên nhân, chương', 'Symptom, when it shows, cause, chapter')
    m('diagramDesc', 'Từ điều bạn thấy tới chương cần đọc', 'From what you see to the chapter to read')
    for k, vi, en in [('symptom', 'Triệu chứng', 'Symptom'), ('phase', 'Lộ ra lúc', 'Shows up'), ('cause', 'Nguyên nhân', 'Cause'), ('chapter', 'Chương', 'Chapter')]:
        m('n.' + k, vi, en)
    m('met.phase', 'Lộ ra lúc', 'Shows up'); m('met.chapter', 'Chương', 'Chapter')
    m('phase.none', 'chưa xét', 'not yet'); m('ch.none', 'chưa xét', 'not yet')
    for k, vi, en, xv, xe in [
        ('runtime', 'lúc chạy, thấy rõ', 'at runtime, visibly', 'App crash, đứng hay báo lỗi; người dùng thấy ngay.', 'The app crashes, freezes or shows an error; users notice at once.'),
        ('silent', 'sai lặng lẽ', 'silently wrong', 'Không crash: dữ liệu lệch, cũ hay không tới nơi.', 'No crash: data is stale, inconsistent or never arrives.'),
        ('update', 'sau khi cập nhật app', 'after an app update', 'Chỉ lộ ở máy còn database cũ; máy dev cài mới không bao giờ thấy.', 'Only shows on devices with an old database; a developer\'s fresh install never sees it.'),
        ('device', 'khi đổi sang máy mới', 'on a new phone', 'Chỉ lộ sau khi khôi phục bản sao lưu trên máy khác.', 'Only shows after a backup is restored on another device.')]:
        m('phase.' + k, vi, en); m('phase.%s.explain' % k, xv, xe)
    SY = [
        ('slowLaunch', 'App khựng lúc mở, đôi khi ANR', 'The app stutters on launch, sometimes an ANR', 'Sau vài tháng dùng, màn hình đầu mở chậm dần.', 'After months of use, the first screen opens slower and slower.',
         'Danh sách lớn nằm trong SharedPreferences', 'A big list lives in SharedPreferences', 'Lần get đầu tiên chờ nạp cả file preferences vài MB.', 'The first get waits for a multi-MB preferences file to load.', 'Chuyển danh sách sang Room (chương H1, H4).', 'Move the list to Room (chapters H1, H4).'),
        ('photoGone', 'Ảnh hồ sơ mất sau khi gỡ app', 'The profile photo is gone after reinstalling', 'Người dùng gỡ rồi cài lại; ảnh đã chụp không còn, cũng chưa từng có trong Thư viện.', 'The user reinstalls; the photo is gone and was never in the gallery.',
         'Ảnh nằm trong bộ nhớ riêng của app', 'The photo was in app-specific storage', 'filesDir bị xóa khi gỡ app và app khác không thấy.', 'filesDir is removed on uninstall and invisible to other apps.', 'Lưu ảnh người dùng muốn giữ qua MediaStore (chương H1, H8).', 'Save photos users want to keep through MediaStore (chapters H1, H8).'),
        ('halfFile', 'Crash lúc mở: JSON cụt', 'Crash on launch: truncated JSON', 'Một số người dùng crash mỗi lần mở, tới khi cài lại.', 'Some users crash on every launch until they reinstall.',
         'Ghi thẳng file rồi bị giết giữa chừng', 'A file written in place, killed mid-write', 'FileOutputStream cắt file khi mở; cú kill để lại file dở dang.', 'FileOutputStream truncates on open; the kill leaves a half-written file.', 'Ghi qua AtomicFile (chương H2).', 'Write through AtomicFile (chapter H2).'),
        ('cacheMissing', 'FileNotFoundException với file đã tải', 'FileNotFoundException for a downloaded file', 'PDF kết quả đã tải tuần trước bỗng không mở được.', 'A results PDF downloaded last week suddenly will not open.',
         'Hệ thống đã dọn cache', 'The system cleared the cache', 'Máy thiếu chỗ thì file trong cacheDir có thể bị xóa.', 'Files in cacheDir may be deleted when space runs low.', 'Kiểm file còn trước khi đọc, thiếu thì tải lại (chương H2).', 'Check the file exists before reading, download again if missing (chapter H2).'),
        ('anrStop', 'ANR khi rời màn Cài đặt', 'An ANR when leaving the Settings screen', 'Đã đổi commit() thành apply() mà ANR vẫn còn, giờ ở lúc rời màn hình.', 'commit() was changed to apply() but ANRs remain, now when leaving the screen.',
         'apply() đang ghi chặn lúc chuyển vòng đời', 'Pending apply() writes block a lifecycle transition', 'Framework chờ các lần apply() xong trước khi Activity đổi trạng thái.', 'The framework waits for apply() writes before the Activity changes state.', 'Chuyển sang DataStore (chương H3).', 'Move to DataStore (chapter H3).'),
        ('multiDs', 'IllegalStateException: nhiều DataStore cho một file', 'IllegalStateException: several DataStores for one file', 'App crash khi hai màn hình cùng đọc cài đặt.', 'The app crashes when two screens read settings.',
         'Tạo nhiều instance DataStore cho cùng file', 'Several DataStore instances for the same file', 'Mỗi màn hình tự tạo DataStore riêng.', 'Each screen creates its own DataStore.', 'Một instance cho cả app, khai báo ở cấp cao nhất (chương H3).', 'One instance for the whole app, declared at the top level (chapter H3).'),
        ('staleList', 'Đặt lịch xong, danh sách không thấy', 'Booked, but the list does not show it', 'Phải kéo để làm mới mới thấy lịch vừa đặt.', 'The new booking only appears after pull-to-refresh.',
         'Đọc một lần thay cho Flow', 'A one-shot read instead of a Flow', 'Hàm suspend trả ảnh chụp; lần ghi sau không đánh thức ai.', 'A suspend function returns a snapshot; later writes wake nobody.', 'Hàm DAO trả về Flow (chương H4).', 'Make the DAO function return a Flow (chapter H4).'),
        ('dupAppt', 'Một lịch hiện ở hai bác sĩ', 'One appointment under two doctors', 'Thỉnh thoảng màn Tổng quan đếm dư một lịch.', 'Now and then the Overview screen counts one appointment too many.',
         'Nhiều truy vấn rời, không giao dịch', 'Separate queries, no transaction', 'Đồng bộ ghi chen giữa vòng lặp N+1.', 'Sync writes between the N+1 loop\'s queries.', '@Relation với @Transaction, hay một câu JOIN trả Map (chương H5).', '@Relation with @Transaction, or a JOIN returning a Map (chapter H5).'),
        ('crashUpdate', 'Crash mỗi lần mở sau khi cập nhật', 'Crashes on every launch after an update', 'Chỉ người dùng lâu năm bị; máy của đội chạy tốt.', 'Only long-time users are hit; team devices work fine.',
         'Thiếu đường migration', 'A missing migration path', 'Người dùng nhảy cóc phiên bản; Room ném IllegalStateException.', 'Users skip versions; Room throws IllegalStateException.', 'Đủ migration cho mọi phiên bản, có test (chương H6).', 'Migrations for every version, with tests (chapter H6).'),
        ('wiped', 'Mất hết dữ liệu sau khi cập nhật', 'All data gone after an update', 'Không crash, nhưng lịch hẹn biến mất.', 'No crash, but the appointments vanish.',
         'fallbackToDestructiveMigration còn sót', 'A leftover fallbackToDestructiveMigration', 'Một migration thiếu khiến Room xóa sạch database.', 'One missing migration makes Room wipe the database.', 'Bỏ fallback xóa sạch cho dữ liệu người dùng (chương H6).', 'Remove destructive fallback for user data (chapter H6).'),
        ('neverSent', 'Lịch đặt lúc mất mạng không tới phòng khám', 'Offline bookings never reach the clinic', 'Trên máy vẫn thấy lịch, máy chủ thì không có.', 'The device shows the booking; the server never got it.',
         'Việc gửi chạy trong coroutine của màn hình', 'The upload runs in a screen\'s coroutine', 'App đóng thì coroutine dừng; không còn ai gửi.', 'When the app closes the coroutine stops; nobody sends it.', 'Hàng chờ trong Room, gửi bằng WorkManager (chương H7).', 'A queue in Room, sent by WorkManager (chapter H7).'),
        ('android10', 'Lưu ảnh lỗi, chỉ trên Android 10', 'Saving a photo fails, only on Android 10', 'Sau khi nâng target SDK, chỉ người dùng Android 10 báo lỗi.', 'After raising the target SDK, only Android 10 users report failures.',
         'Đường dẫn tệp trên bộ nhớ chung', 'A file path on shared storage', 'Scoped storage chặn đường dẫn tệp ở Android 10; Android 11 cho lại.', 'Scoped storage blocks file paths on Android 10; Android 11 allows them again.', 'Dùng MediaStore.insert (chương H8).', 'Use MediaStore.insert (chapter H8).'),
        ('oldToken', 'Đổi máy: lỗi 401, mất thông báo', 'New phone: 401 errors, no notifications', 'Người dùng đổi máy bị đăng xuất giữa chừng và không nhận nhắc lịch.', 'Users on a new phone get signed out mid-use and miss reminders.',
         'Token cũ được sao lưu và khôi phục', 'Old tokens were backed up and restored', 'File token nằm trong filesDir nên Auto Backup mang theo.', 'The token file sits in filesDir, so Auto Backup carried it over.', 'Loại file token khỏi sao lưu, hay dùng noBackupFilesDir (chương H9).', 'Exclude token files from backup, or use noBackupFilesDir (chapter H9).'),
    ]
    for sid, tv, te, dv, de, cv, ce, cdv, cde, fv, fe in SY:
        m('s.%s.title' % sid, tv, te); m('s.%s.detail' % sid, dv, de); m('s.%s.cause' % sid, cv, ce); m('s.%s.causeDetail' % sid, cdv, cde); m('s.%s.fix' % sid, fv, fe)
        m('ctl.symptom.' + sid, tv, te)
    for h, vi, en in [('h1', 'H1 · Chọn nơi lưu', 'H1 · Choosing where to store'), ('h2', 'H2 · File riêng của app', 'H2 · App-specific files'), ('h3', 'H3 · Từ SharedPreferences tới DataStore', 'H3 · From SharedPreferences to DataStore'),
                      ('h4', 'H4 · Room cơ bản', 'H4 · Room basics'), ('h5', 'H5 · Quan hệ và giao dịch', 'H5 · Relations and transactions'), ('h6', 'H6 · Migration', 'H6 · Migrations'),
                      ('h7', 'H7 · Offline-first và đồng bộ nền', 'H7 · Offline-first and background sync'), ('h8', 'H8 · Shared storage và MediaStore', 'H8 · Shared storage and MediaStore'), ('h9', 'H9 · Sao lưu và dữ liệu nhạy cảm', 'H9 · Backup and sensitive data')]:
        m('ch.' + h, vi, en); m('go.' + h, 'Đọc ' + vi, 'Read ' + en)
    m('co.try', 'Chọn một triệu chứng bạn từng gặp; đi bốn bước rồi mở chương được chỉ tới.', 'Pick a symptom you have met; walk the four steps, then open the chapter pointed to.')
    m('co.cause', 'Nguyên nhân thường nằm ở chỗ chọn nơi lưu hay cách ghi, không phải một dòng sai lẻ.', 'The cause is usually the choice of storage or the way of writing, not a single wrong line.')
    m('co.chapter', 'Chương được chỉ tới có mô phỏng đúng tình huống này, cách sửa và nguồn.', 'The chapter pointed to simulates exactly this case, with the fix and sources.')
    a('cap.map', 'Từ trái sang phải: triệu chứng, lúc nó lộ ra, nguyên nhân, chương giải thích. Tab "Bảng tra" liệt kê mọi triệu chứng.', 'Left to right: the symptom, when it shows up, the cause, the chapter that explains it. The "Lookup table" tab lists every symptom.')
    a('preset.map', 'Lưu dữ liệu · bản đồ triệu chứng và chương', 'Saving data · symptom map to chapters')

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.map', 'Bảng tra', 'Lookup table')
    z('map.cap', 'Mọi triệu chứng của track, lúc chúng lộ ra và chương giải thích. Hàng đang chọn được viền; ô "?" mở dần theo bước.', 'Every symptom in the track, when it shows up and the chapter that explains it. The chosen row is outlined; "?" cells open step by step.')
    z('map.legend', 'Ba trong mười ba triệu chứng chỉ lộ ra sau khi cập nhật app hay đổi máy: kiểm thử phải đi qua cả hai lúc đó.', 'Three of the thirteen symptoms only show up after an update or on a new phone: testing has to cover both moments.')
    for k, vi, en in [('sym', 'Triệu chứng', 'Symptom'), ('phase', 'Lộ ra lúc', 'Shows up'), ('ch', 'Chương', 'Chapter')]:
        z('map.col.' + k, vi, en)

    C = 'h0'
    a(C + '.title', 'Bản đồ track: triệu chứng và chương', 'Track map: symptoms and chapters')
    a(C + '.essence', 'Track này dạy chọn nơi lưu và lưu dữ liệu trên Android sao cho không mất, không hỏng, và không làm màn hình đứng: file riêng, DataStore, Room, đồng bộ nền, bộ nhớ chung và sao lưu, theo tài liệu chính thức của Android.\nPhần 1 (H1–H6) là nền tảng: chọn nơi lưu, ghi file an toàn, DataStore, Room, quan hệ và giao dịch, migration. Phần 2 (H7–H9) là thực hành: offline-first với WorkManager, MediaStore, sao lưu.\nĐang gặp một lỗi cụ thể? Bắt đầu từ bảng tra triệu chứng bên dưới.',
      'This track teaches how to choose where to store data on Android and how to store it so it is never lost, never corrupted, and never freezes the screen: app files, DataStore, Room, background sync, shared storage and backup, following the official Android docs.\nPart 1 (H1–H6) is the foundation: choosing a place, writing files safely, DataStore, Room, relations and transactions, migrations. Part 2 (H7–H9) is practice: offline-first with WorkManager, MediaStore, backup.\nFacing a specific bug? Start from the symptom table below.')
    a(C + '.goal.g1', 'Đã thấy lúc triệu chứng lộ ra', 'Saw when the symptom shows up')
    a(C + '.goal.g2', 'Đã tới chương cần đọc', 'Reached the chapter to read')
    a(C + '.sim.storage.map', 'triệu chứng và chương', 'symptoms and chapters')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Trong 13 triệu chứng của bảng tra, bạn đoán bao nhiêu cái máy của đội phát triển (cài mới, có mạng, không đổi máy) sẽ không bao giờ gặp?',
      'Of the 13 symptoms in the lookup table, how many do you guess a developer\'s device (fresh install, always online, never switched) would never hit?')
    B(C, S_, 1, 'ans', 'Ít nhất bảy. Hai cái lộ ra sau khi cập nhật (thiếu migration, xóa sạch database). Một cái lộ ra khi đổi máy (token cũ). Một cái chỉ có trên Android 10. Và ba cái nữa: cache bị dọn khi máy đầy, lịch đặt lúc mất mạng không tới máy chủ, file preferences lớn dần sau vài tháng. Đây là đếm trên bảng của site, không phải thống kê.',
      "At least seven. Two show up after an update (a missing migration, a wiped database). One shows up on a new phone (an old token). One exists only on Android 10. And three more: the cache cleared when storage fills, an offline booking never reaching the server, a preferences file growing for months. This is a count from the site's table, not a statistic.")

    S_ = 'order'
    a(C + '.sec.%s.title' % S_, 'Thứ tự đọc', 'Reading order')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Đọc H1 trước: nó giúp chọn nơi lưu và trỏ tới chương của từng nơi. H2 và H3 đọc riêng được. H4 → H5 → H6 nối tiếp nhau: Room, rồi quan hệ, rồi migration. H7 cần H4, vì hàng chờ gửi nằm trong Room. H8 và H9 đọc riêng được.\nNên đọc trước các chương K1–K7 của track Kotlin và A1–A3 của track Kotlin Coroutines Explorer, vì các chương ở đây dùng hàm suspend và Flow.',
      "Read H1 first: it helps you choose a place and points to each place's chapter. H2 and H3 stand on their own. H4 → H5 → H6 follow each other: Room, then relations, then migrations. H7 needs H4, because the send queue lives in Room. H8 and H9 stand on their own.\nIt helps to read chapters K1–K7 of the Kotlin track and A1–A3 of the Kotlin Coroutines Explorer track first, since these chapters use suspend functions and Flow.")

    S_ = 'index'
    a(C + '.sec.%s.title' % S_, 'Chỉ mục: mỗi chương dùng hình gì', 'Index: the visual of each chapter')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Mỗi chương dùng một kiểu hình hợp với nội dung của nó. H1: cây quyết định kèm bảng thuộc tính của các nơi lưu. H2: làn thời gian app, hệ thống, đĩa. H3: làn của main thread, luồng IO và đĩa. H4: dãy bốn tầng của Room kèm bảng các lần chạy lại. H5: bảng lịch hẹn cạnh kết quả ghép, kèm bộ đếm truy vấn. H6: dãy các phiên bản schema. H7: sơ đồ tuần tự app, Room, WorkManager, máy chủ. H8: ma trận phiên bản Android nhân cách làm. H9: cây thư mục, kèm cột "được sao lưu" và cột "trên máy mới".',
      'Each chapter uses the kind of picture that fits its content. H1: a decision tree with a table of storage properties. H2: timeline lanes for the app, the system and the disk. H3: lanes for the main thread, an IO thread and the disk. H4: Room\'s four stages with a table of reruns. H5: the appointment table beside the assembled result, with a query counter. H6: a strip of schema versions. H7: a sequence diagram of the app, Room, WorkManager and the server. H8: a matrix of Android versions by approach. H9: a directory tree with "backed up" and "on the new phone" columns.')

    S_ = 'links'
    a(C + '.sec.%s.title' % S_, 'Cầu nối sang track khác', 'Bridges to other tracks')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'H7 nối với chương G4 của track Kiến trúc app Android qua cầu nối X16: G4 dạy vai trò của repository và nguồn sự thật, còn H7 dạy cơ chế lưu và đồng bộ. H4 và H7 nối với chương L7 của track Gỡ lỗi và hiệu năng Android (cầu nối X31), nơi dạy xem database và worker đang chạy. Flow, hàm suspend và dispatcher dùng trong H3, H4, H7 được giảng ở track Kotlin Coroutines Explorer. Xung đột khi nhiều máy cùng sửa, và phân trang, thuộc track Thiết kế hệ thống phía mobile.\nQuy tắc dễ nhớ: track này lo "lưu cho đúng"; các track kia lo "tổ chức", "chạy nền" và "kiểm tra".',
      'H7 links to chapter G4 of the Android App Architecture track through bridge X16: G4 teaches the role of the repository and the source of truth, H7 teaches the storage and sync mechanics. H4 and H7 link to chapter L7 of the Android Debugging and Performance track (bridge X31), which teaches inspecting the live database and workers. Flow, suspend functions and dispatchers used in H3, H4 and H7 are taught in the Kotlin Coroutines Explorer track. Conflicts between devices, and paging, belong to the Mobile System Design track.\nRule of thumb: this track is about "storing it right"; the others cover "organising", "running in the background" and "checking".')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Hai thời điểm nào máy dev hay bỏ sót khi kiểm thử lưu dữ liệu?', 'Which two moments does a developer\'s device usually miss when testing storage?')
    B(C, S_, 1, 'ans', 'Cập nhật từ một phiên bản cũ (migration) và khôi phục sang máy mới (sao lưu).', 'Updating from an old version (migrations) and restoring onto a new phone (backup).')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Crash mỗi lần mở chỉ ở người dùng lâu năm sau khi cập nhật: đọc chương nào?', 'Crashes on every launch only for long-time users after an update: which chapter?', 'H6 · Migration.', 'H6 · Migrations.', 'Thiếu đường migration cho phiên bản cũ.', 'A missing migration path for an old version.'),
        ('q2', 'Lịch đặt lúc mất mạng không tới máy chủ: đọc chương nào?', 'Offline bookings never reach the server: which chapter?', 'H7 · Offline-first và đồng bộ nền.', 'H7 · Offline-first and background sync.', 'Việc gửi phải giao cho WorkManager.', 'The upload must be handed to WorkManager.'),
        ('q3', 'Đổi máy bị lỗi 401: đọc chương nào?', 'A new phone gets 401 errors: which chapter?', 'H9 · Sao lưu và dữ liệu nhạy cảm.', 'H9 · Backup and sensitive data.', 'Token cũ được Auto Backup mang theo.', 'Auto Backup carried the old tokens over.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
