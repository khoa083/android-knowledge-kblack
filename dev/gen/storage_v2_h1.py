# Lưu dữ liệu · H1: chọn nơi lưu (Phần 1)
# Nguồn: developer.android.com Data and file storage overview, App-specific storage, DataStore, Room (đọc 2026-11-24);
# mã AOSP SharedPreferencesImpl.java nhánh main (đọc 2026-11-24). Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'h1': ['hook', 'places', 'questions', 'prefsjson', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.choose.' + k, vi, en)
    m('title', 'Chọn nơi lưu bằng bốn câu hỏi', 'Choosing where to store with four questions')
    m('overview', 'App Hẹn Khám có năm loại dữ liệu: 500 lịch hẹn, vài cài đặt, một ảnh hồ sơ, một file PDF kết quả xét nghiệm, và một bản nháp ghi chú. Mỗi loại cần một chỗ ở khác nhau. Để chọn, ta hỏi lần lượt tối đa bốn câu. Câu nào được trả lời "có" trước thì câu đó quyết định nơi lưu.',
      'The ClinicBook app has five kinds of data: 500 appointments, a few settings, a profile photo, a lab-results PDF, and a draft note. Each needs a different home. To choose, we ask up to four questions in turn. The first question answered "yes" decides where the data goes.')
    m('wrapup', 'Nơi lưu đi theo tính chất của dữ liệu, không theo thói quen. Thứ người dùng muốn giữ và mở bằng app khác thì vào bộ nhớ chung. Thứ tải lại được thì vào cache. Vài cài đặt nhỏ thì vào DataStore. Nhiều bản ghi cần lọc và sửa thì vào Room. Còn lại là một file riêng của app.\nChọn sai không báo lỗi ngay. Nó lộ ra muộn: khi danh sách lớn dần, khi máy hết chỗ, hay khi người dùng gỡ app.\nHình dung một căn nhà: tủ lạnh cho đồ ăn hỏng được, két sắt cho giấy tờ, kệ sách cho thứ cần tra cứu. Để nhầm chỗ thì không hỏng ngay, nhưng sớm muộn sẽ khổ.',
      'Where data goes follows what the data is, not habit. What the user wants to keep and open in other apps goes to shared storage. What can be downloaded again goes to the cache. A few small settings go to DataStore. Many records you filter and edit go to Room. Everything else is an app-specific file.\nA wrong choice does not fail at once. It shows up later: as the list grows, when the device runs out of space, or when the user uninstalls.\nPicture a house: a fridge for food that spoils, a safe for papers, a bookshelf for things you look up. Putting things in the wrong place does not break anything today, but it hurts sooner or later.')
    m('simp.1', 'Bốn câu hỏi và thứ tự của chúng là cách site tóm tắt tài liệu Android về lưu trữ (đọc ngày 2026-11-24), không phải sơ đồ có sẵn trong tài liệu. App thật hay kết hợp nhiều nơi: Room giữ bản ghi kèm đường dẫn, còn ảnh nằm trong file.',
      "The four questions and their order are the site's summary of the Android storage docs (read on 2026-11-24), not a diagram taken from them. Real apps often combine places: Room keeps a record with a path, while the image lives in a file.")
    m('simp.2', 'Bộ nhớ ngoài riêng của app được gộp vào "file riêng"; tài liệu mở qua Storage Access Framework (bộ chọn file của hệ thống) được gộp vào "bộ nhớ chung". Chương H2 và H8 tách rõ hai phần này. Cách SharedPreferences đọc và ghi theo mã nguồn Android (AOSP, nhánh main); đó là chi tiết cài đặt, có thể đổi. Lưu trên đám mây nằm ngoài track.',
      'App-specific external storage is folded into "app-specific file"; documents opened through the Storage Access Framework (the system file picker) are folded into "shared storage". Chapters H2 and H8 separate them. How SharedPreferences reads and writes follows the Android source code (AOSP, main branch); that is an implementation detail and may change. Cloud storage is outside this track.')
    m('ctl.hint', 'Chọn loại dữ liệu rồi đi qua từng câu hỏi; cây bên dưới tô đường đã đi.', 'Pick a kind of data and walk through each question; the tree below marks the path taken.')
    m('ctl.data', 'Loại dữ liệu', 'Kind of data')
    for k, vi, en in [('appts', '500 lịch hẹn', '500 appointments'), ('settings', 'cài đặt của người dùng', 'user settings'), ('photo', 'ảnh hồ sơ người dùng chụp', 'a profile photo the user took'),
                      ('pdf', 'PDF kết quả xét nghiệm', 'a lab-results PDF'), ('draft', 'bản nháp ghi chú dài', 'a long draft note')]:
        m('ctl.data.' + k, vi, en)
    m('diagramTitle', 'Loại dữ liệu, câu hỏi, nơi lưu, chương', 'Kind of data, question, storage place, chapter')
    m('diagramDesc', 'Một loại dữ liệu đi qua các câu hỏi tới nơi lưu, rồi tới chương giảng nơi lưu đó', 'A kind of data goes through the questions to a storage place, then to the chapter that teaches it')
    for k, vi, en in [('data', 'Loại dữ liệu', 'Kind of data'), ('question', 'Câu hỏi', 'Question'), ('place', 'Nơi lưu', 'Storage place'), ('chapter', 'Chương', 'Chapter')]:
        m('n.' + k, vi, en)
    m('met.place', 'Nơi lưu', 'Storage place'); m('met.chapter', 'Đọc tiếp ở', 'Read next')
    for k, vi, en in [('none', 'chưa rõ', 'not yet known'), ('files', 'file riêng của app (filesDir)', 'app-specific file (filesDir)'), ('cache', 'cache của app (cacheDir)', 'app cache (cacheDir)'),
                      ('datastore', 'DataStore (khóa–giá trị)', 'DataStore (key–value)'), ('room', 'Room (database SQLite)', 'Room (SQLite database)'), ('media', 'bộ nhớ chung (MediaStore)', 'shared storage (MediaStore)')]:
        m('place.' + k, vi, en)
    for k, vi, en in [('none', 'chưa rõ', 'not yet known'), ('h2', 'H2 · File riêng của app', 'H2 · App-specific files'), ('h3', 'H3 · Từ SharedPreferences tới DataStore', 'H3 · From SharedPreferences to DataStore'),
                      ('h4', 'H4 · Room cơ bản', 'H4 · Room basics'), ('h8', 'H8 · Shared storage và MediaStore', 'H8 · Shared storage and MediaStore')]:
        m('ch.' + k, vi, en)
    for k, vi, en in [('share', 'Người dùng hay app khác cần thấy nó, và nó phải còn sau khi gỡ app?', 'Must the user or other apps see it, and must it outlive an uninstall?'),
                      ('regen', 'Nếu mất, có tải lại hay tạo lại được không?', 'If it is lost, can you download or recreate it?'),
                      ('kv', 'Chỉ là vài giá trị nhỏ dạng khóa–giá trị, đọc ghi cả khối?', 'Is it just a few small key–value settings, read and written as a whole?'),
                      ('rows', 'Nhiều bản ghi cùng kiểu, cần lọc, sắp xếp hay sửa từng bản ghi?', 'Many records of one shape that you filter, sort or edit one at a time?')]:
        m('q.' + k, vi, en)
    a('cap.choose', 'Từ trái sang phải: loại dữ liệu, câu hỏi đang xét, nơi lưu, chương đọc tiếp. Câu trả lời "không" làm khối câu hỏi mờ đi và đi tiếp xuống câu sau.',
      'Left to right: the kind of data, the question being asked, the storage place, the chapter to read next. A "no" greys the question block and moves on to the next question.')
    S = [
        ('appts', 'start', '500 lịch hẹn: lọc theo bác sĩ, theo ngày, sửa từng cái', '500 appointments: filtered by doctor and date, edited one by one',
         'Danh sách lớn dần theo thời gian. Màn hình cần lọc theo bác sĩ, sắp theo ngày, và người dùng đổi giờ của một lịch hẹn.', 'The list grows over time. Screens filter by doctor and sort by date, and the user changes the time of a single appointment.'),
        ('appts', 'share', 'Câu 1: không, lịch hẹn là dữ liệu riêng của app', 'Question 1: no, appointments are the app\'s own data',
         'Người dùng không mở lịch hẹn bằng app khác, và không cần chúng còn sau khi gỡ app.', 'The user does not open appointments in another app and does not need them to outlive an uninstall.'),
        ('appts', 'regen', 'Câu 2: không hẳn, lịch đặt lúc mất mạng chỉ có trên máy', 'Question 2: not quite, appointments booked offline exist only on the device',
         'Phần đã đồng bộ tải lại được từ máy chủ, nhưng lịch đặt lúc mất mạng chỉ nằm trên máy cho tới khi gửi đi (chương H7). Mất là mất thật, nên không để trong cache.', 'The synced part can be downloaded again, but an appointment booked offline lives only on the device until it is sent (chapter H7). Losing it is real loss, so it cannot live in the cache.'),
        ('appts', 'kv', 'Câu 3: không, đây là 500 bản ghi chứ không phải vài cài đặt', 'Question 3: no, this is 500 records, not a few settings',
         'Mỗi lịch hẹn có cùng các trường: bác sĩ, giờ, trạng thái. Đó là một bảng, không phải vài cặp khóa–giá trị.', 'Every appointment has the same fields: doctor, time, status. That is a table, not a few key–value pairs.'),
        ('appts', 'rows', 'Câu 4: có, nhiều bản ghi cần lọc và sửa từng cái', 'Question 4: yes, many records to filter and edit one by one',
         'Lọc, sắp xếp và sửa một dòng là việc của database. Câu "có" đầu tiên dẫn tới Room.', 'Filtering, sorting and editing one row is a database\'s job. The first "yes" leads to Room.'),
        ('appts', 'leaf', 'Kết quả: Room', 'Result: Room',
         'Đổi giờ một lịch hẹn chỉ cập nhật một dòng; câu lọc theo bác sĩ chạy trong SQLite thay vì parse cả danh sách. Chương H4 giảng Room.', 'Changing one appointment updates one row; the doctor filter runs inside SQLite instead of parsing the whole list. Chapter H4 teaches Room.'),
        ('settings', 'start', 'Cài đặt: chủ đề tối, nhắc trước 60 phút, ngôn ngữ', 'Settings: dark theme, a 60-minute reminder, language',
         'Ba giá trị nhỏ, đọc lúc mở app và đổi khi người dùng vào màn Cài đặt.', 'Three small values, read when the app opens and changed when the user visits Settings.'),
        ('settings', 'share', 'Câu 1: không, cài đặt chỉ app này dùng', 'Question 1: no, only this app uses its settings',
         'Không app nào khác cần đọc chủ đề hay giờ nhắc của Hẹn Khám.', 'No other app needs ClinicBook\'s theme or reminder time.'),
        ('settings', 'regen', 'Câu 2: không, đó là lựa chọn của người dùng', 'Question 2: no, they are the user\'s choices',
         'Mất cài đặt thì app quay về mặc định và người dùng phải chọn lại. Không tạo lại được, nên không để trong cache.', 'Losing settings sends the app back to defaults and the user must choose again. They cannot be recreated, so not the cache.'),
        ('settings', 'kv', 'Câu 3: có, vài giá trị nhỏ dạng khóa–giá trị', 'Question 3: yes, a few small key–value pairs',
         'Mỗi cài đặt là một khóa với một giá trị. Câu "có" đầu tiên dẫn tới DataStore.', 'Each setting is a key with one value. The first "yes" leads to DataStore.'),
        ('settings', 'leaf', 'Kết quả: DataStore', 'Result: DataStore',
         'DataStore đọc bằng Flow và ghi bằng hàm suspend, không chặn main thread. Chương H3 giảng vì sao bỏ SharedPreferences.', 'DataStore reads through a Flow and writes with suspend functions, without blocking the main thread. Chapter H3 explains why SharedPreferences is left behind.'),
        ('photo', 'start', 'Ảnh hồ sơ người dùng chụp bằng app', 'A profile photo the user takes with the app',
         'Người dùng muốn thấy ảnh trong Thư viện ảnh, gửi cho người khác, và vẫn giữ nó nếu lỡ gỡ app.', 'The user wants to see the photo in their gallery, send it to others, and keep it if they uninstall the app.'),
        ('photo', 'share', 'Câu 1: có, người dùng muốn giữ và thấy ở app khác', 'Question 1: yes, the user wants to keep it and see it in other apps',
         'File riêng của app bị xóa khi gỡ app và app khác không thấy. Câu "có" đầu tiên dẫn tới bộ nhớ chung.', 'App-specific files are removed on uninstall and invisible to other apps. The first "yes" leads to shared storage.'),
        ('photo', 'leaf', 'Kết quả: bộ nhớ chung qua MediaStore', 'Result: shared storage through MediaStore',
         'Ảnh vào bộ sưu tập ảnh qua MediaStore; cách ghi và quyền đổi theo phiên bản Android. Chương H8 giảng chi tiết.', 'The photo goes into the images collection through MediaStore; how you write it and which permissions apply change across Android versions. Chapter H8 covers the details.'),
        ('pdf', 'start', 'PDF kết quả xét nghiệm tải về để xem nhanh', 'A lab-results PDF downloaded for quick viewing',
         'Máy chủ giữ bản gốc. App tải về để mở lại nhanh, không phải tải mỗi lần.', 'The server keeps the original. The app downloads it so it opens quickly next time, instead of downloading each time.'),
        ('pdf', 'share', 'Câu 1: không, chỉ xem trong app', 'Question 1: no, it is only viewed inside the app',
         'Nếu người dùng muốn lưu một bản để gửi đi, đó là một thao tác "xuất" riêng, ghi vào bộ nhớ chung (H8).', 'If the user wants to keep a copy to send, that is a separate "export" action that writes to shared storage (H8).'),
        ('pdf', 'regen', 'Câu 2: có, tải lại được từ máy chủ', 'Question 2: yes, it can be downloaded again',
         'Mất bản trên máy chỉ tốn thêm một lần tải. Câu "có" đầu tiên dẫn tới cache.', 'Losing the local copy only costs one more download. The first "yes" leads to the cache.'),
        ('pdf', 'leaf', 'Kết quả: cache của app', 'Result: the app cache',
         'Hệ thống có thể xóa file cache khi máy thiếu chỗ, nên trước khi mở phải kiểm file còn không, còn thiếu thì tải lại. Chương H2 giảng cache và file riêng.', 'The system may delete cache files when space runs low, so check that the file exists before opening it and download again if it is missing. Chapter H2 covers the cache and app-specific files.'),
        ('draft', 'start', 'Bản nháp ghi chú dài gửi bác sĩ', 'A long draft note for the doctor',
         'Người dùng gõ một đoạn mô tả triệu chứng, có thể dài vài chục KB, rồi gửi sau.', 'The user types a description of symptoms, possibly tens of KB long, to send later.'),
        ('draft', 'share', 'Câu 1: không, bản nháp chỉ dùng trong app', 'Question 1: no, the draft is used only inside the app',
         'Không app nào khác cần đọc nó, và không cần giữ nó sau khi gỡ app.', 'No other app needs it, and it need not outlive an uninstall.'),
        ('draft', 'regen', 'Câu 2: không, người dùng tự gõ', 'Question 2: no, the user typed it',
         'Mất bản nháp là mất công người dùng gõ. Không để trong cache.', 'Losing the draft throws away what the user typed. Not the cache.'),
        ('draft', 'kv', 'Câu 3: không, đó là một khối văn bản lớn', 'Question 3: no, it is one large block of text',
         'Không phải vài giá trị cài đặt nhỏ. DataStore dành cho dữ liệu nhỏ và mỗi lần ghi là ghi lại cả khối.', 'It is not a few small settings. DataStore is for small data, and every write rewrites the whole thing.'),
        ('draft', 'rows', 'Câu 4: không, chỉ một tài liệu, không cần truy vấn', 'Question 4: no, it is a single document, nothing to query',
         'Không có nhiều bản ghi để lọc hay sắp xếp. Hết bốn câu mà chưa có "có": dùng file riêng của app.', 'There are no records to filter or sort. Four questions and no "yes": use an app-specific file.'),
        ('draft', 'leaf', 'Kết quả: file riêng của app', 'Result: an app-specific file',
         'Một file trong filesDir: không cần quyền, app khác không đọc được, bị xóa khi gỡ app. Chương H2 giảng cách ghi để file không hỏng khi app bị tắt giữa chừng.', 'A file in filesDir: no permission needed, unreadable by other apps, removed on uninstall. Chapter H2 shows how to write it so the file is not corrupted if the app is killed halfway.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Thử cả năm loại dữ liệu; mỗi loại dừng ở một nơi lưu khác nhau.', 'Try all five kinds of data; each one stops at a different storage place.'),
        ('media', 'Tài liệu Android nói: đừng để trong bộ nhớ riêng của app dữ liệu người dùng muốn giữ sau khi gỡ app, ví dụ ảnh; ảnh thuộc về bộ sưu tập của MediaStore. [[src:ax-app-specific]]', 'The Android docs say: do not keep data users expect to persist after uninstalling in app-specific storage, such as photos; photos belong in a MediaStore collection. [[src:ax-app-specific]]'),
        ('cache', 'Tài liệu Android nói: khi máy thiếu bộ nhớ trong, Android có thể xóa file cache để lấy lại chỗ; hãy kiểm file còn trước khi đọc. [[src:ax-app-specific]]', 'The Android docs say: when the device is low on internal storage, Android may delete cache files to reclaim space; check a file exists before reading it. [[src:ax-app-specific]]'),
        ('datastore', 'Tài liệu Android nói: DataStore hợp với tập dữ liệu nhỏ; dùng SharedPreferences thì nên cân nhắc chuyển sang DataStore. [[src:ax-datastore]]', 'The Android docs say: DataStore is ideal for small datasets; if you use SharedPreferences, consider migrating to DataStore. [[src:ax-datastore]]'),
        ('room', 'Tài liệu Android nói: cần tập dữ liệu lớn hay phức tạp, cập nhật từng phần hay ràng buộc tham chiếu thì dùng Room thay cho DataStore. [[src:ax-datastore]] [[src:ax-room]]', 'The Android docs say: if you need large or complex datasets, partial updates or referential integrity, use Room instead of DataStore. [[src:ax-datastore]] [[src:ax-room]]'),
        ('files', 'Tài liệu Android nói: thư mục nội bộ không cần quyền, app khác không truy cập được, được mã hóa từ Android 10, và bị xóa khi gỡ app. [[src:ax-app-specific]]', 'The Android docs say: internal directories need no permission, other apps cannot access them, they are encrypted from Android 10, and they are removed on uninstall. [[src:ax-app-specific]]')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.dt', 'Cây quyết định', 'Decision tree')
    z('dt.cap', 'Đọc từ trên xuống: trả lời "có" thì rẽ phải tới nơi lưu, "không" thì xuống câu tiếp. Đường đã đi được tô đậm; câu đang xét có viền.', 'Read top to bottom: a "yes" turns right to a storage place, a "no" goes down to the next question. The path taken is in bold; the current question is outlined.')
    z('dt.q', 'Câu {n}', 'Question {n}')
    z('dt.yes', 'Có', 'Yes'); z('dt.no', 'Không', 'No')
    z('dt.end', 'Hết câu hỏi', 'No questions left')
    z('dt.chapter', 'chương {ch}', 'chapter {ch}')
    z('dt.legend', 'Bảng thuộc tính theo bảng so sánh của trang Data and file storage overview. "Hệ thống tự xóa": khi máy thiếu bộ nhớ trong. "MediaStore" ở đây là ảnh, video, âm thanh.', 'Properties follow the comparison table on the Data and file storage overview page. "System may delete": when internal storage runs low. "MediaStore" here means images, video and audio.')
    z('pt.cap', 'Năm nơi lưu khác nhau ở ba điểm. Hàng của kết quả được viền ở bước cuối.', 'The five places differ on three points. The result\'s row is outlined at the last step.')
    z('pt.place', 'Nơi lưu', 'Place'); z('pt.other', 'App khác đọc được', 'Other apps can read'); z('pt.uninstall', 'Gỡ app thì', 'On uninstall'); z('pt.sysdel', 'Hệ thống tự xóa', 'System may delete')
    for k, y, n in [('other', ('có, nếu có quyền', 'yes, with permission'), ('không', 'no')), ('uninstall', ('vẫn còn', 'kept'), ('bị xóa', 'removed')), ('sysdel', ('có thể', 'may'), ('không', 'no'))]:
        z('pt.v.%s.yes' % k, y[0], y[1]); z('pt.v.%s.no' % k, n[0], n[1])

    C = 'h1'
    a(C + '.title', 'Chọn nơi lưu', 'Choosing where to store data')
    a(C + '.essence', 'Android có bốn nhóm chỗ lưu. File riêng của app (filesDir, cacheDir). Bộ nhớ chung, nơi ảnh, video, tài liệu được nhiều app cùng thấy (MediaStore, Storage Access Framework). Cặp khóa–giá trị cho vài cài đặt (DataStore). Và database cho nhiều bản ghi (Room).\nChúng khác nhau ở ba điểm: app khác có đọc được không; còn hay mất khi gỡ app; và hệ thống có tự xóa khi máy thiếu chỗ không.\nChọn theo tính chất của dữ liệu: có cần chia sẻ không, mất có lấy lại được không, có phải vài giá trị nhỏ không, có phải nhiều bản ghi cần truy vấn không.',
      'Android has four groups of storage. App-specific files (filesDir, cacheDir). Shared storage, where images, video and documents are visible to many apps (MediaStore, the Storage Access Framework). Key–value pairs for a few settings (DataStore). And a database for many records (Room).\nThey differ on three points: whether other apps can read them; whether they survive an uninstall; and whether the system deletes them when space runs low.\nChoose by what the data is: must it be shared, can it be recovered if lost, is it a few small values, is it many records you query.')
    a(C + '.goal.g1', 'Đã trả lời câu hỏi đầu tiên', 'Answered the first question')
    a(C + '.goal.g2', 'Đã tới một nơi lưu', 'Reached a storage place')
    a(C + '.sim.storage.choose', 'cây quyết định chọn nơi lưu', 'the storage decision tree')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'impl')
    B(C, S_, 1, 'predict', 'Bản đầu của Hẹn Khám lưu cả danh sách 500 lịch hẹn thành một chuỗi JSON trong SharedPreferences. Người dùng đổi giờ của đúng một lịch hẹn. Trên đĩa, bao nhiêu dữ liệu được ghi lại?',
      'The first version of ClinicBook stores the whole list of 500 appointments as one JSON string in SharedPreferences. The user changes the time of exactly one appointment. How much data gets written to disk?')
    B(C, S_, 1, 'ans', 'Cả file. App phải đọc cả chuỗi JSON (một dạng văn bản mô tả dữ liệu), sửa một phần tử, rồi ghép lại chuỗi mới. Sau đó SharedPreferences ghi lại toàn bộ file trên đĩa: cả 500 lịch hẹn lẫn mọi cài đặt khác. Với Room, chỉ đúng một dòng được cập nhật. Cây quyết định ngay dưới cho thấy dữ liệu này nên ở đâu. [[src:aosp-sp-impl]]',
      'The whole file. The app must read the whole JSON string (a text format describing data), change one element, then build a new string. SharedPreferences then rewrites the entire file on disk: all 500 appointments plus every other setting. With Room, exactly one row is updated. The decision tree just below shows where this data belongs. [[src:aosp-sp-impl]]')

    S_ = 'places'
    a(C + '.sec.%s.title' % S_, 'Bốn nhóm nơi lưu', 'Four groups of storage')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Tài liệu Android chia chỗ lưu thành bốn nhóm.\n(1) Bộ nhớ riêng của app: file chỉ app này dùng, nằm trong thư mục riêng (filesDir cho dữ liệu cần giữ, cacheDir cho dữ liệu tạm).\n(2) Bộ nhớ chung: file app muốn chia sẻ, như ảnh, video, âm thanh (qua MediaStore) và tài liệu (qua Storage Access Framework, bộ chọn file của hệ thống).\n(3) Preferences: vài cặp khóa–giá trị riêng tư, như "chủ đề = tối"; ngày nay dùng DataStore.\n(4) Database: dữ liệu có cấu trúc, nhiều dòng cùng kiểu, qua Room. [[src:ax-storage-overview]]',
      'The Android docs split storage into four groups.\n(1) App-specific storage: files only this app uses, in its own directories (filesDir for data to keep, cacheDir for temporary data).\n(2) Shared storage: files the app means to share, such as images, video and audio (through MediaStore) and documents (through the Storage Access Framework, the system file picker).\n(3) Preferences: a few private key–value pairs, such as "theme = dark"; today that is DataStore.\n(4) Databases: structured data, many rows of the same shape, through Room. [[src:ax-storage-overview]]')
    B(C, S_, 2, 'p', 'Bộ nhớ trong (thư mục riêng trong máy) luôn sẵn, không cần xin quyền, app khác không đọc được, và được mã hóa từ Android 10. Bộ nhớ ngoài thường rộng hơn nhưng không phải lúc nào cũng có, ví dụ khi tháo thẻ nhớ; vì vậy dữ liệu app cần để chạy nên ở bộ nhớ trong. Mọi file riêng của app, dù trong hay ngoài, đều bị xóa khi gỡ app.\nQuy tắc dễ nhớ: "riêng của app" nghĩa là đi cùng app; app đi thì nó đi. [[src:ax-app-specific]] [[src:ax-storage-overview]]',
      'Internal storage (the app\'s own directories on the device) is always there, needs no permission, cannot be read by other apps, and is encrypted from Android 10. External storage is usually larger but not always present, for example when an SD card is removed; so data the app needs to run belongs in internal storage. All app-specific files, internal or external, are removed on uninstall.\nRule of thumb: "app-specific" means it travels with the app; when the app goes, it goes. [[src:ax-app-specific]] [[src:ax-storage-overview]]')
    B(C, S_, 3, 'kt', 'val notes = File(context.filesDir, "draft.txt")      // riêng, còn tới khi gỡ app\nval tmp = File(context.cacheDir, "result-123.pdf")   // riêng, hệ thống có thể xóa\nval settings = context.dataStore                       // DataStore: vài giá trị nhỏ\nval db = AppDatabase.get(context)                      // Room: nhiều bản ghi, truy vấn\n// ảnh người dùng muốn giữ: MediaStore (chương H8)',
      'val notes = File(context.filesDir, "draft.txt")      // private, kept until uninstall\nval tmp = File(context.cacheDir, "result-123.pdf")   // private, the system may delete it\nval settings = context.dataStore                       // DataStore: a few small values\nval db = AppDatabase.get(context)                      // Room: many records, queries\n// photos the user wants to keep: MediaStore (chapter H8)')
    B(C, S_, 4, 'note', 'Đừng viết cứng đường dẫn như "/data/data/<gói>/files": mỗi máy đặt thư mục một chỗ khác. Luôn hỏi Context (đối tượng cho app truy cập tài nguyên của nó) để lấy thư mục: filesDir, cacheDir, getExternalFilesDir. [[src:ax-storage-overview]]',
      'Do not hardcode paths such as "/data/data/<package>/files": each device puts directories in a different place. Always ask the Context (the object that gives the app access to its resources) for the directory: filesDir, cacheDir, getExternalFilesDir. [[src:ax-storage-overview]]')
    B(C, S_, 4, 'kind', 'pitfall')

    S_ = 'questions'
    a(C + '.sec.%s.title' % S_, 'Bốn câu hỏi', 'Four questions')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Tài liệu Android gợi ý tự hỏi bốn điều trước khi chọn chỗ lưu. Dữ liệu cần bao nhiêu chỗ, vì bộ nhớ trong có hạn? Cần đọc được chắc chắn tới mức nào, vì dữ liệu cần lúc mở app nên ở bộ nhớ trong hay database? Đó là loại dữ liệu gì: khóa–giá trị thì dùng preferences, có cấu trúc thì dùng database? Và có cần giữ riêng tư không? [[src:ax-storage-overview]]',
      'The Android docs suggest asking four things before picking a place. How much space does the data need, since internal storage is limited? How reliably must it be readable, since data needed at startup belongs in internal storage or a database? What kind of data is it: key–value goes to preferences, structured data to a database? And must it stay private? [[src:ax-storage-overview]]')
    B(C, S_, 2, 'p', 'Site gom các ý đó thành bốn câu hỏi có thứ tự; câu loại được nhiều chỗ nhất thì hỏi trước.\nCâu 1: người dùng có cần giữ nó sau khi gỡ app, hay mở nó bằng app khác? Chỉ bộ nhớ chung làm được.\nCâu 2: mất rồi có lấy lại được không? Nếu có, cache là đủ, vì cache chấp nhận mất.\nCâu 3: có phải chỉ vài giá trị nhỏ không? Nếu có, dùng DataStore.\nCâu 4: có phải nhiều bản ghi cần lọc, sắp xếp hay sửa từng cái không? Nếu có, dùng Room, vì DataStore không cập nhật từng phần (mỗi lần ghi là ghi lại cả khối) và không có ràng buộc giữa các bản ghi.\nKhông câu nào "có" thì dùng một file riêng. [[src:ax-datastore]]',
      'The site folds those ideas into four ordered questions; the one that rules out the most places comes first.\nQuestion 1: must the user keep it after uninstalling, or open it in another app? Only shared storage can do that.\nQuestion 2: if it is lost, can you get it back? If so, the cache is enough, because the cache accepts loss.\nQuestion 3: is it just a few small values? If so, use DataStore.\nQuestion 4: is it many records you filter, sort or edit one at a time? If so, use Room, because DataStore has no partial updates (every write rewrites the whole thing) and no links between records.\nNo "yes" at all: use an app-specific file. [[src:ax-datastore]]')
    B(C, S_, 3, 'note', 'Thứ tự câu hỏi là của site, không phải của tài liệu chính thức. Một màn hình thật thường dùng vài chỗ cùng lúc: Room giữ bản ghi kèm đường dẫn ảnh, còn ảnh nằm trong một file.\nQuy tắc dễ nhớ: hỏi "ai cần thấy nó?" trước, rồi mới hỏi "nó trông ra sao?".',
      'The order of the questions is the site\'s, not the official docs\'. A real screen often uses several places at once: Room keeps the record and a photo path, while the photo lives in a file.\nRule of thumb: ask "who needs to see it?" first, then "what does it look like?".')
    B(C, S_, 3, 'kind', 'android')

    S_ = 'prefsjson'
    a(C + '.sec.%s.title' % S_, 'Vì sao danh sách không nên nằm trong SharedPreferences', 'Why a list does not belong in SharedPreferences')
    a(C + '.sec.%s.badge' % S_, 'impl')
    B(C, S_, 1, 'p', 'Vì sao một danh sách lớn trong SharedPreferences lại chậm? Hãy xem mã nguồn Android (SharedPreferencesImpl, nhánh main). Lần đầu mở một file preferences, nó đọc cả file vào bộ nhớ, ở một luồng nền. Mọi lệnh get (đọc một giá trị) đều phải chờ tới khi đọc xong cả file. File càng lớn thì lần get đầu tiên trên main thread (luồng vẽ giao diện) càng có thể phải đợi lâu. [[src:aosp-sp-impl]]',
      'Why is a big list in SharedPreferences slow? Look at the Android source code (SharedPreferencesImpl, main branch). The first time a preferences file is opened, it reads the whole file into memory, on a background thread. Every get (reading one value) must wait until the whole file has been read. The bigger the file, the longer the first get on the main thread (the thread that draws the UI) may have to wait. [[src:aosp-sp-impl]]')
    B(C, S_, 2, 'p', 'Khi ghi thì còn tệ hơn. Mỗi lần ghi, nó ghi lại toàn bộ nội dung ra file, không chỉ khóa vừa đổi. Với một danh sách JSON 500 phần tử, mỗi lần đổi một lịch hẹn là ba việc lớn: đọc cả chuỗi, dựng lại cả chuỗi, ghi lại cả file. Room thì chỉ ghi đúng một dòng bằng một câu lệnh UPDATE.\nHình dung: sửa một chữ trong cuốn sổ mà phải chép lại cả cuốn. [[src:aosp-sp-impl]] [[src:ax-room]]',
      'Writing is worse. On every write, it rewrites the entire contents to the file, not just the key that changed. With a 500-element JSON list, every change to one appointment means three big jobs: read the whole string, rebuild the whole string, rewrite the whole file. Room writes exactly one row with one UPDATE statement.\nPicture fixing one word in a notebook by copying out the whole notebook. [[src:aosp-sp-impl]] [[src:ax-room]]')
    B(C, S_, 3, 'kt', '// trước: một chuỗi cho cả danh sách\nval list = Json.decodeFromString<List<Appt>>(prefs.getString("appts", "[]")!!)\nval updated = list.map { if (it.id == id) it.copy(time = newTime) else it }\nprefs.edit { putString("appts", Json.encodeToString(updated)) }   // ghi lại cả file\n\n// sau: một dòng trong Room\n@Query("UPDATE appointment SET time = :newTime WHERE id = :id")\nsuspend fun reschedule(id: Long, newTime: Instant)',
      '// before: one string for the whole list\nval list = Json.decodeFromString<List<Appt>>(prefs.getString("appts", "[]")!!)\nval updated = list.map { if (it.id == id) it.copy(time = newTime) else it }\nprefs.edit { putString("appts", Json.encodeToString(updated)) }   // rewrites the whole file\n\n// after: one row in Room\n@Query("UPDATE appointment SET time = :newTime WHERE id = :id")\nsuspend fun reschedule(id: Long, newTime: Instant)')
    B(C, S_, 4, 'note', 'Chuyển sang DataStore không giải quyết chuyện này. Tài liệu Android nói rõ DataStore dành cho dữ liệu nhỏ và không cập nhật từng phần. Danh sách vẫn phải vào Room.\nQuy tắc dễ nhớ: thấy mình lưu một danh sách dưới dạng một chuỗi, đó là lúc cần một database. [[src:ax-datastore]]',
      'Moving to DataStore does not solve this. The Android docs state that DataStore is for small data and has no partial updates. The list still belongs in Room.\nRule of thumb: the moment you store a list as one string, you need a database. [[src:ax-datastore]]')
    B(C, S_, 4, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Sau vài tháng dùng, app khựng lúc mở và thỉnh thoảng báo ANR ở màn hình đầu tiên.', 'After a few months of use, the app stutters on launch and occasionally shows an ANR on the first screen.')
    B(C, S_, 1, 'cause', 'File preferences đã lên vài MB vì chứa cả danh sách lịch hẹn và lịch sử. Màn hình đầu đọc một cài đặt trên main thread, và lệnh get đó phải chờ đọc xong cả file. ANR (thông báo "ứng dụng không phản hồi") xuất hiện khi main thread bị chặn quá lâu.',
      'The preferences file has grown to several MB because it holds the appointment list and history. The first screen reads one setting on the main thread, and that get must wait for the whole file. An ANR (the "app is not responding" dialog) appears when the main thread is blocked for too long.')
    B(C, S_, 1, 'fix', 'Chuyển danh sách sang Room; để preferences chỉ còn vài cài đặt nhỏ, rồi chuyển chúng sang DataStore (chương H3).', 'Move the lists to Room; leave preferences with only a few small settings, then move those to DataStore (chapter H3).')
    B(C, S_, 2, 'bug', 'Người dùng gỡ app rồi cài lại: ảnh hồ sơ đã chụp biến mất, và họ chưa bao giờ thấy nó trong Thư viện ảnh.', 'A user uninstalls and reinstalls the app: the profile photo they took is gone, and it never showed up in their gallery.')
    B(C, S_, 2, 'cause', 'Ảnh được ghi vào filesDir. Đó là bộ nhớ riêng của app: app khác không thấy, và nó bị xóa khi gỡ app.', 'The photo was written to filesDir. That is app-specific storage: other apps cannot see it, and it is removed on uninstall.')
    B(C, S_, 2, 'fix', 'Ảnh người dùng muốn giữ thì ghi vào bộ sưu tập ảnh qua MediaStore (chương H8). Ảnh chỉ app dùng, như ảnh thu nhỏ tải về, thì để cache.', 'Photos the user wants to keep go into the images collection through MediaStore (chapter H8). Images only the app uses, such as downloaded thumbnails, go in the cache.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Đặt sáu loại dữ liệu của Hẹn Khám vào nơi lưu, và ghi câu hỏi nào quyết định: (a) ngôn ngữ người dùng chọn trong app; (b) ảnh đại diện bác sĩ tải từ máy chủ; (c) lịch sử hai năm khám, mỗi lượt khám có nhiều đơn thuốc; (d) hóa đơn PDF người dùng muốn lưu để gửi công ty bảo hiểm; (e) token phiên đăng nhập; (f) file log gỡ lỗi khoảng 1 MB gửi kèm khi người dùng báo lỗi.',
      'Place six kinds of ClinicBook data, and note which question decides: (a) the language the user picked in the app; (b) doctors\' avatars downloaded from the server; (c) two years of visit history, each visit with several prescriptions; (d) an invoice PDF the user wants to keep and send to their insurer; (e) the login session token; (f) a debug log of about 1 MB attached when the user reports a bug.')
    B(C, S_, 1, 'hint', 'Đi lần lượt bốn câu: chia sẻ và giữ sau khi gỡ app; lấy lại được; vài giá trị nhỏ; nhiều bản ghi cần truy vấn.', 'Go through the four questions in order: shared and kept after uninstall; recoverable; a few small values; many records you query.')
    B(C, S_, 1, 'sol', '(a) DataStore, câu 3. (b) cache, câu 2: tải lại được. (c) Room, câu 4; quan hệ lượt khám và đơn thuốc là chương H5. (d) bộ nhớ chung, câu 1: người dùng muốn giữ và mở bằng app khác; tài liệu đi qua Storage Access Framework hay MediaStore (H8). (e) DataStore, câu 3; chương H9 bàn chuyện loại nó khỏi bản sao lưu. (f) file riêng trong filesDir, hết câu hỏi: không chia sẻ, không tạo lại được, không phải khóa–giá trị, không cần truy vấn.',
      '(a) DataStore, question 3. (b) the cache, question 2: it can be downloaded again. (c) Room, question 4; the relation between visits and prescriptions is chapter H5. (d) shared storage, question 1: the user wants to keep it and open it in other apps; documents go through the Storage Access Framework or MediaStore (H8). (e) DataStore, question 3; chapter H9 discusses excluding it from backups. (f) an app-specific file in filesDir, no question says yes: not shared, not recreatable, not key–value, nothing to query.')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Nơi lưu nào hệ thống có thể tự xóa khi máy thiếu chỗ?', 'Which storage place may the system delete on its own when space runs low?')
    B(C, S_, 1, 'ans', 'Cache của app (cacheDir). Vì vậy chỉ để ở đó thứ lấy lại được, và kiểm file còn trước khi đọc.', 'The app cache (cacheDir). So keep only recoverable things there, and check the file exists before reading it.')
    B(C, S_, 2, 'ask', 'Vì sao 500 lịch hẹn không nên nằm trong DataStore, dù DataStore tốt hơn SharedPreferences?', 'Why should 500 appointments not go in DataStore, even though DataStore is better than SharedPreferences?')
    B(C, S_, 2, 'ans', 'DataStore dành cho dữ liệu nhỏ, không cập nhật từng phần và không có ràng buộc tham chiếu; đổi một lịch hẹn sẽ ghi lại cả khối. Room cập nhật đúng một dòng.', 'DataStore is meant for small data, has no partial updates and no referential integrity; changing one appointment rewrites the whole thing. Room updates exactly one row.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Gỡ app thì dữ liệu ở đâu còn lại?', 'Which data survives an uninstall?', 'Dữ liệu trong bộ nhớ chung (MediaStore, tài liệu qua Storage Access Framework).', 'Data in shared storage (MediaStore, documents through the Storage Access Framework).', 'File riêng, DataStore và Room đều nằm trong bộ nhớ riêng của app và bị xóa theo app.', 'App-specific files, DataStore and Room all live in app-specific storage and go with the app.'),
        ('q2', 'Ghi vào filesDir có cần xin quyền không?', 'Does writing to filesDir need a permission?', 'Không.', 'No.', 'Thư mục nội bộ của app không cần quyền nào.', 'An app\'s internal directories need no permission.'),
        ('q3', 'Khi nào trang DataStore khuyên dùng Room thay thế?', 'When does the DataStore page recommend Room instead?', 'Khi cần dữ liệu lớn hay phức tạp, cập nhật từng phần, hay ràng buộc tham chiếu.', 'When you need large or complex datasets, partial updates, or referential integrity.', 'DataStore hợp với dữ liệu nhỏ.', 'DataStore suits small datasets.'),
        ('q4', 'SharedPreferences ghi gì xuống đĩa khi đổi một khóa?', 'What does SharedPreferences write to disk when one key changes?', 'Toàn bộ file, gồm mọi khóa.', 'The whole file, every key.', 'writeToFile ghi lại cả map (mã AOSP).', 'writeToFile writes the whole map back (AOSP code).')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
