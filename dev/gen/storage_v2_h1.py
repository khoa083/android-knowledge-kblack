# Lưu dữ liệu · H1: chọn nơi lưu (Phần 1)
# Nguồn: developer.android.com Data and file storage overview, App-specific storage, DataStore, Room (đọc 2026-11-24);
# mã AOSP SharedPreferencesImpl.java nhánh main (đọc 2026-11-24). Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'h1': ['hook', 'places', 'questions', 'prefsjson', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    m = lambda k, vi, en=None: a('m.choose.' + k, vi, en)
    m('title', 'Chọn nơi lưu bằng bốn câu hỏi', 'Choosing where to store with four questions')
    m('overview', 'App Hẹn Khám có năm loại dữ liệu: 500 lịch hẹn, cài đặt, ảnh hồ sơ, PDF kết quả xét nghiệm và một bản nháp ghi chú. Mỗi loại đi qua tối đa bốn câu hỏi, theo thứ tự: có cần cho người khác thấy không, mất có lấy lại được không, có phải vài giá trị nhỏ không, có phải nhiều bản ghi cần truy vấn không. Câu "có" đầu tiên quyết định nơi lưu.',
      'The ClinicBook app has five kinds of data: 500 appointments, settings, a profile photo, a lab-results PDF and a draft note. Each goes through at most four questions, in order: must others see it, can it be recovered if lost, is it a few small values, is it many records you query. The first "yes" decides where it goes.')
    m('wrapup', 'Nơi lưu đi theo tính chất của dữ liệu, không theo thói quen. Dữ liệu người dùng muốn giữ và chia sẻ thì vào bộ nhớ chung; thứ lấy lại được thì vào cache; vài giá trị cài đặt thì vào DataStore; nhiều bản ghi cần truy vấn thì vào Room; còn lại là file riêng của app. Chọn sai không lỗi ngay: nó lộ ra khi danh sách lớn dần, khi máy hết chỗ, hay khi người dùng gỡ app.',
      'Where data goes follows what the data is, not habit. Data the user wants to keep and share goes to shared storage; things you can get back go to the cache; a few settings go to DataStore; many records you query go to Room; everything else is an app-specific file. A wrong choice does not fail at once: it shows up as the list grows, when the device runs out of space, or when the user uninstalls.')
    m('simp.1', 'Bốn câu hỏi và thứ tự của chúng là của site, gom từ bốn câu hỏi trong trang Data and file storage overview và giới hạn ghi trong trang DataStore. App thật hay kết hợp: Room giữ đường dẫn, còn ảnh nằm trong file.',
      'The four questions and their order are the site\'s, distilled from the four questions on the Data and file storage overview page and the limits stated on the DataStore page. Real apps often combine places: Room keeps a path while the image lives in a file.')
    m('simp.2', 'Bộ nhớ ngoài riêng của app gộp vào "file riêng"; tài liệu qua Storage Access Framework gộp vào "bộ nhớ chung". Chương H2 và H8 tách rõ.',
      'App-specific external storage is folded into "app-specific file"; documents through the Storage Access Framework are folded into "shared storage". Chapters H2 and H8 separate them.')
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
        ('media', 'Trang App-specific storage: đừng để trong bộ nhớ riêng của app dữ liệu người dùng muốn giữ sau khi gỡ app, ví dụ ảnh; ảnh thuộc về bộ sưu tập của MediaStore. [[src:ax-app-specific]]', 'The App-specific storage page: do not keep data users expect to persist after uninstalling in app-specific storage, such as photos; photos belong in a MediaStore collection. [[src:ax-app-specific]]'),
        ('cache', 'Trang App-specific storage: khi máy thiếu bộ nhớ trong, Android có thể xóa file cache để lấy lại chỗ; hãy kiểm file còn trước khi đọc. [[src:ax-app-specific]]', 'The App-specific storage page: when the device is low on internal storage, Android may delete cache files to reclaim space; check a file exists before reading it. [[src:ax-app-specific]]'),
        ('datastore', 'Trang DataStore: DataStore hợp với tập dữ liệu nhỏ; dùng SharedPreferences thì nên cân nhắc chuyển sang DataStore. [[src:ax-datastore]]', 'The DataStore page: DataStore is ideal for small datasets; if you use SharedPreferences, consider migrating to DataStore. [[src:ax-datastore]]'),
        ('room', 'Trang DataStore: cần tập dữ liệu lớn hay phức tạp, cập nhật từng phần hay ràng buộc tham chiếu thì dùng Room thay cho DataStore. [[src:ax-datastore]] [[src:ax-room]]', 'The DataStore page: if you need large or complex datasets, partial updates or referential integrity, use Room instead of DataStore. [[src:ax-datastore]] [[src:ax-room]]'),
        ('files', 'Trang App-specific storage: thư mục nội bộ không cần quyền, app khác không truy cập được, được mã hóa từ Android 10, và bị xóa khi gỡ app. [[src:ax-app-specific]]', 'The App-specific storage page: internal directories need no permission, other apps cannot access them, they are encrypted from Android 10, and they are removed on uninstall. [[src:ax-app-specific]]')]:
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
    a(C + '.essence', 'Android có bốn nhóm nơi lưu: file riêng của app (filesDir, cacheDir), bộ nhớ chung (MediaStore, Storage Access Framework), cặp khóa–giá trị (DataStore), và database (Room).\nChúng khác nhau ở ba điểm: app khác có đọc được không, có còn sau khi gỡ app không, và hệ thống có tự xóa khi thiếu chỗ không.\nChọn theo tính chất của dữ liệu: có cần chia sẻ, có lấy lại được, có phải vài giá trị nhỏ, có phải nhiều bản ghi cần truy vấn.',
      'Android has four groups of storage: app-specific files (filesDir, cacheDir), shared storage (MediaStore, the Storage Access Framework), key–value pairs (DataStore), and databases (Room).\nThey differ on three points: whether other apps can read them, whether they outlive an uninstall, and whether the system deletes them when space runs low.\nChoose by what the data is: must it be shared, can it be recovered, is it a few small values, is it many records you query.')
    a(C + '.goal.g1', 'Đã trả lời câu hỏi đầu tiên', 'Answered the first question')
    a(C + '.goal.g2', 'Đã tới một nơi lưu', 'Reached a storage place')
    a(C + '.sim.storage.choose', 'cây quyết định chọn nơi lưu', 'the storage decision tree')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'impl')
    B(C, S_, 1, 'predict', 'Bản đầu của Hẹn Khám lưu cả danh sách 500 lịch hẹn thành một chuỗi JSON trong SharedPreferences. Người dùng đổi giờ của đúng một lịch hẹn. Trên đĩa, bao nhiêu dữ liệu được ghi lại?',
      'The first version of ClinicBook stores the whole list of 500 appointments as one JSON string in SharedPreferences. The user changes the time of exactly one appointment. How much data gets written to disk?')
    B(C, S_, 1, 'ans', 'Cả file. App phải parse cả chuỗi JSON, sửa một phần tử, ghép lại chuỗi mới; rồi SharedPreferences ghi lại toàn bộ file XML, gồm cả 500 lịch hẹn lẫn mọi cài đặt khác. Room chỉ cập nhật một dòng. Cây quyết định ngay dưới cho thấy dữ liệu này nên ở đâu. [[src:aosp-sp-impl]]',
      'The whole file. The app must parse the entire JSON string, change one element and build a new string; then SharedPreferences rewrites the whole XML file, all 500 appointments plus every other setting. Room updates one row. The decision tree just below shows where this data belongs. [[src:aosp-sp-impl]]')

    S_ = 'places'
    a(C + '.sec.%s.title' % S_, 'Bốn nhóm nơi lưu', 'Four groups of storage')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Trang tổng quan của Android chia nơi lưu thành bốn nhóm. (1) Bộ nhớ riêng của app: file chỉ app dùng, trong thư mục nội bộ (filesDir, cacheDir) hay thư mục riêng trên bộ nhớ ngoài. (2) Bộ nhớ chung: file app muốn chia sẻ, như ảnh, video, âm thanh (MediaStore) và tài liệu (Storage Access Framework). (3) Preferences: cặp khóa–giá trị riêng tư; nay là DataStore. (4) Database: dữ liệu có cấu trúc trong database riêng, qua Room. [[src:ax-storage-overview]]',
      'Android\'s overview page splits storage into four groups. (1) App-specific storage: files only your app uses, in internal directories (filesDir, cacheDir) or private directories on external storage. (2) Shared storage: files your app means to share, such as images, video and audio (MediaStore) and documents (the Storage Access Framework). (3) Preferences: private key–value pairs; today that is DataStore. (4) Databases: structured data in a private database, through Room. [[src:ax-storage-overview]]')
    B(C, S_, 2, 'p', 'Thư mục nội bộ luôn có sẵn, không cần quyền, app khác không truy cập được, và được mã hóa từ Android 10. Bộ nhớ ngoài thường lớn hơn nhưng không phải lúc nào cũng truy cập được, ví dụ khi tháo thẻ nhớ; dữ liệu app cần để chạy nên nằm ở bộ nhớ trong. Mọi file riêng của app, trong hay ngoài, đều bị xóa khi gỡ app. [[src:ax-app-specific]] [[src:ax-storage-overview]]',
      'Internal directories are always available, need no permission, cannot be accessed by other apps, and are encrypted from Android 10. External storage is usually larger but not always accessible, for example when an SD card is removed; data the app needs to work belongs in internal storage. All app-specific files, internal or external, are removed on uninstall. [[src:ax-app-specific]] [[src:ax-storage-overview]]')
    B(C, S_, 3, 'kt', 'val notes = File(context.filesDir, "draft.txt")      // riêng, còn tới khi gỡ app\nval tmp = File(context.cacheDir, "result-123.pdf")   // riêng, hệ thống có thể xóa\nval settings = context.dataStore                       // DataStore: vài giá trị nhỏ\nval db = AppDatabase.get(context)                      // Room: nhiều bản ghi, truy vấn\n// ảnh người dùng muốn giữ: MediaStore (chương H8)',
      'val notes = File(context.filesDir, "draft.txt")      // private, kept until uninstall\nval tmp = File(context.cacheDir, "result-123.pdf")   // private, the system may delete it\nval settings = context.dataStore                       // DataStore: a few small values\nval db = AppDatabase.get(context)                      // Room: many records, queries\n// photos the user wants to keep: MediaStore (chapter H8)')
    B(C, S_, 4, 'note', 'Đừng viết cứng đường dẫn như "/data/data/<gói>/files": vị trí khác nhau giữa các máy. Luôn lấy thư mục qua Context (filesDir, cacheDir, getExternalFilesDir). [[src:ax-storage-overview]]',
      'Do not hardcode paths such as "/data/data/<package>/files": locations differ across devices. Always get directories through Context (filesDir, cacheDir, getExternalFilesDir). [[src:ax-storage-overview]]')
    B(C, S_, 4, 'kind', 'pitfall')

    S_ = 'questions'
    a(C + '.sec.%s.title' % S_, 'Bốn câu hỏi', 'Four questions')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Trang tổng quan gợi ý tự hỏi bốn điều: dữ liệu cần bao nhiêu chỗ (bộ nhớ trong có hạn); cần truy cập tin cậy đến đâu (dữ liệu cần lúc khởi động thì để ở bộ nhớ trong hay database); là loại dữ liệu gì (khóa–giá trị thì preferences, có cấu trúc thì database); có cần riêng tư không. [[src:ax-storage-overview]]',
      'The overview page suggests asking four things: how much space the data needs (internal storage is limited); how reliable access must be (data needed at startup goes in internal storage or a database); what kind of data it is (key–value goes to preferences, structured data to a database); whether it must be private. [[src:ax-storage-overview]]')
    B(C, S_, 2, 'p', 'Site gom chúng thành bốn câu hỏi có thứ tự, câu loại trừ được nhiều nhất hỏi trước. Câu 1, chia sẻ và giữ sau khi gỡ app: chỉ bộ nhớ chung làm được. Câu 2, lấy lại được: cache chấp nhận mất. Câu 3, vài giá trị nhỏ: DataStore. Câu 4, nhiều bản ghi cần truy vấn: Room, vì DataStore không cập nhật từng phần và không có ràng buộc tham chiếu. Không câu nào "có": một file riêng. [[src:ax-datastore]]',
      'The site folds them into four ordered questions, asking the one that rules out the most first. Question 1, shared and kept after uninstall: only shared storage can do that. Question 2, recoverable: the cache accepts loss. Question 3, a few small values: DataStore. Question 4, many records you query: Room, because DataStore has no partial updates and no referential integrity. No "yes" at all: an app-specific file. [[src:ax-datastore]]')
    B(C, S_, 3, 'note', 'Thứ tự câu hỏi là của site, không phải của tài liệu chính thức. Một màn hình thật thường dùng vài nơi cùng lúc: Room giữ bản ghi kèm đường dẫn ảnh, còn ảnh nằm trong file.',
      'The order of the questions is the site\'s, not the official docs\'. A real screen often uses several places at once: Room keeps the record and a photo path, while the photo lives in a file.')
    B(C, S_, 3, 'kind', 'android')

    S_ = 'prefsjson'
    a(C + '.sec.%s.title' % S_, 'Vì sao danh sách không nên nằm trong SharedPreferences', 'Why a list does not belong in SharedPreferences')
    a(C + '.sec.%s.badge' % S_, 'impl')
    B(C, S_, 1, 'p', 'Trong mã AOSP (SharedPreferencesImpl, nhánh main), lần đầu mở một file preferences, loadFromDisk đọc cả file XML vào một map trong bộ nhớ ở luồng nền. Mọi hàm get đều chờ tới khi nạp xong (awaitLoadedLocked). File càng lớn, lần get đầu tiên trên main thread càng có thể phải đợi. [[src:aosp-sp-impl]]',
      'In the AOSP code (SharedPreferencesImpl, main branch), the first time a preferences file is opened, loadFromDisk reads the whole XML file into an in-memory map on a background thread. Every getter waits until loading finishes (awaitLoadedLocked). The bigger the file, the longer the first get on the main thread may wait. [[src:aosp-sp-impl]]')
    B(C, S_, 2, 'p', 'Mỗi lần ghi, writeToFile ghi lại toàn bộ map ra file rồi sync, không chỉ khóa vừa đổi. Một danh sách JSON 500 phần tử nghĩa là mỗi lần đổi một lịch hẹn: parse cả chuỗi, dựng lại cả chuỗi, ghi lại cả file. Room ghi đúng một dòng bằng một câu UPDATE. [[src:aosp-sp-impl]] [[src:ax-room]]',
      'On every write, writeToFile writes the whole map back to the file and syncs it, not just the changed key. A 500-element JSON list means every time one appointment changes: parse the whole string, rebuild the whole string, rewrite the whole file. Room writes exactly one row with one UPDATE. [[src:aosp-sp-impl]] [[src:ax-room]]')
    B(C, S_, 3, 'kt', '// trước: một chuỗi cho cả danh sách\nval list = Json.decodeFromString<List<Appt>>(prefs.getString("appts", "[]")!!)\nval updated = list.map { if (it.id == id) it.copy(time = newTime) else it }\nprefs.edit { putString("appts", Json.encodeToString(updated)) }   // ghi lại cả file\n\n// sau: một dòng trong Room\n@Query("UPDATE appointment SET time = :newTime WHERE id = :id")\nsuspend fun reschedule(id: Long, newTime: Instant)',
      '// before: one string for the whole list\nval list = Json.decodeFromString<List<Appt>>(prefs.getString("appts", "[]")!!)\nval updated = list.map { if (it.id == id) it.copy(time = newTime) else it }\nprefs.edit { putString("appts", Json.encodeToString(updated)) }   // rewrites the whole file\n\n// after: one row in Room\n@Query("UPDATE appointment SET time = :newTime WHERE id = :id")\nsuspend fun reschedule(id: Long, newTime: Instant)')
    B(C, S_, 4, 'note', 'Chuyển sang DataStore không giải quyết chuyện này: trang DataStore nói rõ nó dành cho dữ liệu nhỏ và không hỗ trợ cập nhật từng phần. Danh sách vẫn phải vào Room. [[src:ax-datastore]]',
      'Moving to DataStore does not solve this: the DataStore page states it is for small datasets and does not support partial updates. The list still belongs in Room. [[src:ax-datastore]]')
    B(C, S_, 4, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Sau vài tháng dùng, app khựng lúc mở và thỉnh thoảng báo ANR ở màn hình đầu tiên.', 'After a few months of use, the app stutters on launch and occasionally shows an ANR on the first screen.')
    B(C, S_, 1, 'cause', 'File preferences đã lên vài MB vì chứa cả danh sách lịch hẹn và lịch sử. Màn hình đầu đọc một cài đặt trên main thread, và lời gọi get phải chờ nạp xong cả file.', 'The preferences file has grown to several MB because it holds the appointment list and history. The first screen reads one setting on the main thread, and that get has to wait for the whole file to load.')
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

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Bốn nhóm nơi lưu, bảng thuộc tính và giới hạn của DataStore theo các trang Data and file storage overview, App-specific storage và DataStore đọc ngày 2026-11-24. Hành vi nạp và ghi của SharedPreferences theo mã AOSP SharedPreferencesImpl.java nhánh main cùng ngày; đó là chi tiết cài đặt, có thể đổi. Bốn câu hỏi có thứ tự là của site. Chương gộp bộ nhớ ngoài riêng của app vào "file riêng" và gộp Storage Access Framework vào "bộ nhớ chung". Các nơi lưu trên đám mây (Firebase) nằm ngoài track này.',
      'The four groups, the property table and DataStore\'s limits follow the Data and file storage overview, App-specific storage and DataStore pages as read on 2026-11-24. SharedPreferences\' load and write behaviour follows the AOSP SharedPreferencesImpl.java on the main branch, same date; that is an implementation detail and may change. The ordered four questions are the site\'s. The chapter folds app-specific external storage into "app-specific file" and the Storage Access Framework into "shared storage". Cloud storage (Firebase) is outside this track.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Gỡ app thì dữ liệu ở đâu còn lại?', 'Which data survives an uninstall?', 'Dữ liệu trong bộ nhớ chung (MediaStore, tài liệu qua Storage Access Framework).', 'Data in shared storage (MediaStore, documents through the Storage Access Framework).', 'File riêng, DataStore và Room đều nằm trong bộ nhớ riêng của app và bị xóa theo app.', 'App-specific files, DataStore and Room all live in app-specific storage and go with the app.'),
        ('q2', 'Ghi vào filesDir có cần xin quyền không?', 'Does writing to filesDir need a permission?', 'Không.', 'No.', 'Thư mục nội bộ của app không cần quyền nào.', 'An app\'s internal directories need no permission.'),
        ('q3', 'Khi nào trang DataStore khuyên dùng Room thay thế?', 'When does the DataStore page recommend Room instead?', 'Khi cần dữ liệu lớn hay phức tạp, cập nhật từng phần, hay ràng buộc tham chiếu.', 'When you need large or complex datasets, partial updates, or referential integrity.', 'DataStore hợp với dữ liệu nhỏ.', 'DataStore suits small datasets.'),
        ('q4', 'SharedPreferences ghi gì xuống đĩa khi đổi một khóa?', 'What does SharedPreferences write to disk when one key changes?', 'Toàn bộ file, gồm mọi khóa.', 'The whole file, every key.', 'writeToFile ghi lại cả map (mã AOSP).', 'writeToFile writes the whole map back (AOSP code).')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
