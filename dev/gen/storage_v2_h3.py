# Lưu dữ liệu · H3: từ SharedPreferences tới DataStore (Phần 1)
# Nguồn: developer.android.com SharedPreferences.Editor, DataStore, SharedPreferencesMigration, ANRs (đọc 2026-11-24);
# mã AOSP SharedPreferencesImpl.java nhánh main. Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'h3': ['hook', 'prefsapi', 'datastore', 'rules', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.prefs', 'Lưu dữ liệu · commit(), apply() và DataStore trên main thread', 'Saving data · commit(), apply() and DataStore on the main thread')
    m = lambda k, vi, en=None: a('m.prefs.' + k, vi, en)
    m('title', 'Lưu một cài đặt mà không chặn main thread', 'Saving a setting without blocking the main thread')
    m('overview', 'Người dùng bật chủ đề tối trong màn Cài đặt của Hẹn Khám. Có ba cách lưu cài đặt này: SharedPreferences với commit(), SharedPreferences với apply(), và DataStore. Ta theo dõi ba làn cùng lúc: main thread (luồng vẽ giao diện và nhận chạm), một luồng IO (luồng nền làm việc với đĩa), và file trên đĩa. Máy trong ví dụ có bộ nhớ chậm.',
      "The user turns on the dark theme in ClinicBook's Settings screen. There are three ways to save it: SharedPreferences with commit(), SharedPreferences with apply(), and DataStore. We follow three lanes at once: the main thread (the thread that draws the UI and handles touches), an IO thread (a background thread that works with the disk), and the file on disk. The device in the example has slow storage.")
    m('wrapup', 'commit() bắt main thread đứng chờ suốt lúc ghi cả file. apply() trả về ngay, nhưng chỉ dời chỗ chờ đi chỗ khác: lúc Activity dừng, hệ thống đợi các lần ghi còn dở, và nếu ghi lỗi thì không ai được báo. DataStore ghi trong một hàm suspend trên luồng khác và báo kết quả qua Flow, nên main thread không bao giờ phải chờ đĩa.\nHình dung: commit() là đứng ở quầy chờ in hóa đơn; apply() là đi trước, nhưng tới cửa ra lại bị gọi quay lại chờ; DataStore là để lại số điện thoại, xong người ta báo.',
      'commit() makes the main thread stand and wait for the whole file write. apply() returns at once but only moves the wait elsewhere: when the Activity stops, the system waits for unfinished writes, and if a write fails nobody is told. DataStore writes inside a suspend function on another thread and reports results through a Flow, so the main thread never waits for the disk.\nPicture it: commit() is waiting at the counter for the receipt to print; apply() is walking off, only to be called back at the exit; DataStore is leaving your phone number and being told when it is done.')
    m('simp.1', 'Ba làn là mô hình rút gọn; thời gian ghi phụ thuộc kích thước file và tốc độ bộ nhớ của máy. Máy "bộ nhớ chậm" là tình huống của site.', 'The three lanes are a simplified model; write time depends on file size and the device\'s storage speed. The "slow storage" device is the site\'s scenario.')
    m('simp.2', 'Hành vi commit và apply theo tài liệu tham chiếu của Android và mã nguồn Android (AOSP, nhánh main); DataStore theo tài liệu hướng dẫn, bản 1.3.0; ngưỡng ANR 5 giây theo tài liệu Android; tất cả đọc ngày 2026-11-24. Lần ghi thất bại vì đĩa đầy là tình huống của site. Proto DataStore và DataStore nhiều tiến trình chỉ được nhắc tên.',
      "commit and apply behaviour follows the Android reference docs and the Android source code (AOSP, main branch); DataStore follows its guide, version 1.3.0; the 5-second ANR threshold follows the Android docs; all read on 2026-11-24. The write failing on a full disk is the site's scenario. Proto DataStore and multi-process DataStore are only named.")
    m('ctl.hint', 'Đổi cách lưu rồi đi lại; nhìn làn "Main thread": ô gạch đỏ là lúc main bị chặn.', 'Switch the approach and walk again; watch the "Main thread" lane: red hatched cells are when main is blocked.')
    m('ctl.case', 'Cách lưu', 'Approach')
    for k, vi, en in [('commit', 'SharedPreferences.commit()', 'SharedPreferences commit()'), ('apply', 'SharedPreferences.apply()', 'SharedPreferences apply()'), ('datastore', 'DataStore.edit (suspend)', 'DataStore edit (suspend)')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Main thread, luồng IO, file trên đĩa', 'Main thread, IO thread, file on disk')
    m('diagramDesc', 'Ai ghi xuống đĩa: main thread trực tiếp, hay một luồng IO trong khi main chạy tiếp', 'Who writes to disk: the main thread directly, or an IO thread while main carries on')
    for k, vi, en in [('main', 'Main thread', 'Main thread'), ('io', 'Luồng IO', 'IO thread'), ('disk', 'File trên đĩa', 'File on disk')]:
        m('n.' + k, vi, en)
    m('met.main', 'Main thread', 'Main thread'); m('met.saved', 'Cài đặt đã lưu ở', 'Setting saved in')
    for k, vi, en in [('busy', 'đang chạy onClick', 'running onClick'), ('blocked', 'bị chặn chờ đĩa', 'blocked on the disk'), ('anr', 'bị chặn lâu, nguy cơ ANR', 'blocked long, ANR risk'), ('free', 'rảnh, vẽ được', 'free, can draw')]:
        m('main.' + k, vi, en)
    for k, vi, en in [('none', 'chưa lưu', 'not saved yet'), ('mem', 'chỉ trong bộ nhớ', 'memory only'), ('pending', 'đang ghi xuống đĩa', 'being written to disk'), ('disk', 'trên đĩa, đã xác nhận', 'on disk, confirmed'), ('unknown', 'không rõ: lỗi không được báo', 'unknown: the failure was not reported')]:
        m('saved.' + k, vi, en)
    a('cap.prefs', 'Main thread ở trên, luồng IO ở dưới, file bên phải. Mũi tên cho biết ai đang ghi xuống đĩa; khối viền đỏ là main thread bị chặn hay lỗi bị nuốt.', 'The main thread on top, the IO thread below, the file on the right. The arrow shows who is writing to disk; a red outline marks a blocked main thread or a swallowed error.')
    S = [
        ('commit', 's1', 'Bấm bật chủ đề tối: gọi commit() trên main', 'Tap the dark theme switch: commit() on main',
         'onClick chạy trên main thread và gọi commit(). commit đổi bản trong bộ nhớ rồi ghi xuống đĩa ngay trong lời gọi, và chỉ trả về khi ghi xong.', 'onClick runs on the main thread and calls commit(). commit updates the in-memory copy and writes to disk within the call, returning only when the write is done.'),
        ('commit', 's2', 'Main thread đứng chờ ghi cả file', 'The main thread waits for the whole file',
         'Trong mã AOSP, mỗi lần ghi viết lại toàn bộ file XML rồi sync. Suốt lúc đó main không vẽ khung hình nào và không nhận chạm nào.', 'In the AOSP code, every write rewrites the whole XML file and then syncs it. Meanwhile main draws no frames and handles no touches.'),
        ('commit', 's3', 'Bộ nhớ chậm: main bị chặn lâu, nguy cơ ANR', 'Slow storage: main is blocked long, ANR risk',
         'Máy rẻ, bộ nhớ đang bận (đang cập nhật app khác). Ghi mất vài trăm mili giây hay hơn. Màn hình đứng; nếu một lần chạm không được phản hồi trong 5 giây, hệ thống báo ANR.', 'A cheap device, storage busy (another app is updating). The write takes hundreds of milliseconds or more. The screen freezes; if a touch goes unanswered for 5 seconds, the system shows an ANR.'),
        ('commit', 's4', 'commit() trả về true, màn hình mới vẽ lại', 'commit() returns true, and only then the screen redraws',
         'Ưu điểm duy nhất: biết chắc đã lưu (true) hay chưa (false). Cái giá là main thread đã đứng suốt thời gian ghi.', 'The one upside: you know for sure it was saved (true) or not (false). The price is a main thread that stood still for the whole write.'),
        ('apply', 's1', 'Bấm bật chủ đề tối: gọi apply()', 'Tap the dark theme switch: apply()',
         'apply đổi bản trong bộ nhớ ngay rồi trả về; việc ghi xuống đĩa được xếp hàng cho một luồng khác. Đọc lại khóa ngay sau đó thấy giá trị mới.', 'apply updates the in-memory copy at once and returns; the disk write is queued for another thread. Reading the key right after sees the new value.'),
        ('apply', 's2', 'Luồng khác ghi cả file, main rảnh', 'Another thread writes the whole file, main is free',
         'Vẫn là ghi lại toàn bộ file và sync, nhưng ở luồng nền. Màn hình vẽ lại ngay.', 'Still a rewrite of the whole file plus a sync, but on a background thread. The screen redraws at once.'),
        ('apply', 's3', 'Người dùng về màn hình chính: main chờ lần ghi dở', 'The user goes home: main waits for the unfinished write',
         'Activity chuyển sang onStop. Framework bảo đảm các lần apply() đang ghi phải xong trước khi Activity hay Service đổi trạng thái, nên main thread đứng chờ luồng ghi. Đĩa chậm thì đây chính là ANR.', 'The Activity moves to onStop. The framework makes sure in-flight apply() writes finish before an Activity or Service changes state, so the main thread waits for the writer. With a slow disk, this is the ANR.'),
        ('apply', 's4', 'Ghi lỗi: không ai được báo', 'The write fails: nobody is told',
         'Giả sử đĩa đầy và lần ghi thất bại. apply không có giá trị trả về và không gọi lại; bộ nhớ nói "đã bật", đĩa nói "chưa". Lần mở app sau, chủ đề tối biến mất.', 'Suppose the disk is full and the write fails. apply has no return value and no callback; memory says "on", the disk says "not saved". Next launch, the dark theme is gone.'),
        ('datastore', 's1', 'Bấm bật chủ đề tối: edit trong viewModelScope', 'Tap the dark theme switch: edit inside viewModelScope',
         'onClick gọi ViewModel; ViewModel khởi chạy một coroutine gọi dataStore.edit. edit là hàm suspend nên main không chờ, nó chỉ tạm dừng coroutine.', 'onClick calls the ViewModel; the ViewModel launches a coroutine that calls dataStore.edit. edit is a suspend function, so main does not wait; only the coroutine pauses.'),
        ('datastore', 's2', 'DataStore ghi trên luồng IO, main rảnh', 'DataStore writes on an IO thread, main is free',
         'Khối edit là một giao dịch đọc–sửa–ghi; DataStore ghi cả file (dữ liệu nhỏ, không cập nhật từng phần) trên dispatcher của nó, không trên main.', 'The edit block is one read–modify–write transaction; DataStore writes the whole file (small data, no partial updates) on its own dispatcher, not on main.'),
        ('datastore', 's3', 'Người dùng về màn hình chính: main không chờ gì', 'The user goes home: main waits for nothing',
         'DataStore không đăng ký việc ghi vào hàng chờ của vòng đời Activity, nên onStop chạy ngay. Coroutine ghi vẫn chạy tiếp trên luồng của nó.', 'DataStore does not register its write with the Activity lifecycle queue, so onStop runs at once. The writing coroutine carries on on its own thread.'),
        ('datastore', 's4', 'Flow phát giá trị mới, UI đổi màu', 'The Flow emits the new value, the UI changes colour',
         'data là một Flow; khi ghi xong nó phát Preferences mới và UI đang thu Flow đổi sang chủ đề tối. Nếu ghi lỗi, ngoại lệ ném ra từ edit ở đúng coroutine đã gọi, bắt được bằng try/catch.', 'data is a Flow; once written it emits the new Preferences and the UI collecting it switches to the dark theme. If the write fails, the exception is thrown from edit in the coroutine that called it, catchable with try/catch.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cách; đếm số ô gạch đỏ ở làn Main thread.', 'Walk all four steps of each approach; count the red hatched cells in the Main thread lane.'),
        ('commit.s2', 'Mã nguồn Android (SharedPreferencesImpl) cho thấy: writeToFile ghi lại toàn bộ nội dung bằng XmlUtils.writeMapXml rồi sync. [[src:aosp-sp-impl]]', 'The Android source code (SharedPreferencesImpl) shows: writeToFile writes the whole contents with XmlUtils.writeMapXml, then syncs. [[src:aosp-sp-impl]]'),
        ('commit.s3', 'Tài liệu Android nói: không phản hồi sự kiện nhập trong 5 giây thì bị báo ANR; I/O trên main thread là một nguyên nhân hay gặp. [[src:ax-anr]]', 'The Android docs say: an input event not answered within 5 seconds triggers an ANR; I/O on the main thread is a common cause. [[src:ax-anr]]'),
        ('commit.s4', 'Tài liệu Android nói: commit trả về true nếu giá trị mới đã ghi thành công xuống bộ nhớ bền. [[src:ax-sp-editor]]', 'The Android docs say: commit returns true if the new values were successfully written to persistent storage. [[src:ax-sp-editor]]'),
        ('apply.s2', 'Tài liệu Android nói: apply đổi bản trong bộ nhớ ngay và bắt đầu ghi đĩa bất đồng bộ. [[src:ax-sp-editor]]', 'The Android docs say: apply changes the in-memory copy at once and starts an asynchronous write to disk. [[src:ax-sp-editor]]'),
        ('apply.s3', 'Tài liệu đó cũng cảnh báo: các lần apply() đang chờ có thể chặn main thread lúc chuyển vòng đời, một nguồn ANR hay gặp. [[src:ax-sp-editor]]', 'The Android docs warn: pending apply() calls can block the main thread during lifecycle transitions, a common source of ANRs. [[src:ax-sp-editor]]'),
        ('apply.s4', 'Tài liệu Android nói: với apply, bạn không được báo nếu ghi thất bại. [[src:ax-sp-editor]]', 'The Android docs say: with apply, you will not be notified of any failures. [[src:ax-sp-editor]]'),
        ('datastore.s2', 'Tài liệu Android nói: updateData cập nhật theo giao dịch, một thao tác đọc–sửa–ghi nguyên tử; mọi mã trong khối là một giao dịch. [[src:ax-datastore]]', 'The Android docs say: updateData updates transactionally, in one atomic read–modify–write; all code in the block is one transaction. [[src:ax-datastore]]'),
        ('datastore.s3', 'Tài liệu Android nói: DataStore dùng coroutine và Flow để lưu bất đồng bộ, nhất quán và theo giao dịch. [[src:ax-datastore]]', 'The Android docs say: DataStore uses coroutines and Flow to store data asynchronously, consistently and transactionally. [[src:ax-datastore]]'),
        ('datastore.s4', 'Tài liệu Android nói: đọc qua data, một Flow; trang khuyên đặt việc đọc ghi trong repository và ViewModel, không trong composable. [[src:ax-datastore]]', 'The Android docs say: read through data, a Flow; the page advises putting reads and writes in a repository and ViewModel, not in composables. [[src:ax-datastore]]')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.pf', 'Làn luồng', 'Thread lanes')
    z('pf.cap', 'Mỗi hàng là một làn, mỗi cột là một bước. Ô gạch đỏ ở làn Main thread là lúc màn hình đứng; ô gạch đỏ ở làn IO hay Đĩa là lỗi.', 'Each row is a lane, each column a step. A red hatched cell in the Main thread lane is a frozen screen; one in the IO or Disk lane is a failure.')
    z('pf.legend', 'Ô gạch đỏ nối nhau ở làn Main thread là một đoạn main bị chặn: càng dài, màn hình càng đứng lâu.', 'Consecutive red hatched cells in the Main thread lane form one blocked stretch: the longer it is, the longer the screen freezes.')
    z('pf.lane', 'Làn', 'Lane')
    for k, vi, en in [('main', 'Main thread', 'Main thread'), ('io', 'Luồng IO', 'IO thread'), ('disk', 'Đĩa', 'Disk')]:
        z('pf.lane.' + k, vi, en)
    for c, cols in [('commit', [('bấm', 'tap'), ('ghi', 'write'), ('đĩa chậm', 'slow disk'), ('trả về', 'returns')]),
                    ('apply', [('bấm', 'tap'), ('ghi nền', 'background write'), ('onStop', 'onStop()'), ('ghi lỗi', 'write fails')]),
                    ('datastore', [('bấm', 'tap'), ('ghi nền', 'background write'), ('onStop', 'onStop()'), ('Flow phát', 'Flow emits')])]:
        for i, (vi, en) in enumerate(cols):
            z('pf.col.%s.%d' % (c, i), vi, en)
    for k, vi, en in [
        ('tapCommit', 'onClick → commit()', 'onClick calls commit()'), ('none', '·', '–'), ('idle', 'file cài đặt cũ', 'old settings file'),
        ('waitDisk', 'đứng chờ commit', 'stuck waiting on commit'), ('writeAll', 'ghi lại cả file + sync', 'rewrite whole file + sync'),
        ('waitSlow', 'vẫn đứng chờ: màn hình đơ', 'still waiting: screen frozen'), ('slow', 'bộ nhớ chậm, ghi lâu', 'slow storage, long write'),
        ('commitTrue', 'commit() = true, vẽ lại', 'commit() is true, redraw'), ('saved', 'đã lưu: dark_theme = true', 'saved: dark_theme = true'),
        ('tapApply', 'onClick → apply(), trả về ngay', 'onClick calls apply(), returns at once'), ('queued', 'nhận việc ghi', 'picks up the write'),
        ('free', 'rảnh, vẽ khung hình', 'free, drawing frames'), ('writing', 'đang ghi', 'writing'),
        ('onStopWait', 'onStop chờ lần ghi dở', 'onStop waits for the write'), ('failSilent', 'ghi lỗi, không báo', 'write fails silently'),
        ('notSaved', 'không lưu được (đĩa đầy)', 'not saved (disk full)'),
        ('tapEdit', 'onClick → launch { edit }', 'onClick launches { edit }'), ('suspended', 'coroutine tạm dừng, main rảnh', 'coroutine suspended, main free'),
        ('dsWrite', 'DataStore ghi', 'DataStore writing'), ('onStopFree', 'onStop chạy ngay', 'onStop runs at once'),
        ('flowEmits', 'data phát giá trị mới → UI', 'data emits the new value to the UI'), ('dsDone', 'ghi xong', 'write done')]:
        z('pf.cell.' + k, vi, en)

    C = 'h3'
    a(C + '.title', 'Từ SharedPreferences tới DataStore', 'From SharedPreferences to DataStore')
    a(C + '.essence', 'commit() ghi đồng bộ, tức ghi xong mới trả về, ngay trên luồng gọi nó. Gọi từ main thread là main đứng chờ suốt lần ghi.\napply() trả về ngay. Nhưng khi Activity hay Service đổi trạng thái, hệ thống chờ các lần ghi còn dở, và lỗi ghi không được báo.\nDataStore đọc bằng Flow và ghi bằng hàm suspend, mỗi lần ghi là một giao dịch trọn vẹn. Tài liệu chính thức khuyên chuyển từ SharedPreferences sang DataStore.',
      'commit() writes synchronously, meaning it returns only after the write, right on the thread that called it. Called from the main thread, main waits for the whole write.\napply() returns at once. But when an Activity or Service changes state, the system waits for unfinished writes, and failed writes are not reported.\nDataStore reads through a Flow and writes with suspend functions, each write one complete transaction. The official docs recommend moving from SharedPreferences to DataStore.')
    a(C + '.goal.g1', 'Đã thấy main thread bị chặn', 'Saw the main thread blocked')
    a(C + '.goal.g2', 'Đã đi hết một cách lưu', 'Walked one approach to the end')
    a(C + '.sim.storage.prefs', 'commit(), apply() và DataStore', 'commit(), apply() and DataStore')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Một bạn đổi mọi commit() thành apply() để hết ANR ở màn Cài đặt. Tuần sau, báo cáo ANR vẫn còn, nhưng giờ nằm ở lúc người dùng rời màn hình. Vì sao?',
      'A teammate replaces every commit() with apply() to get rid of the ANRs on the Settings screen. A week later ANR reports are still there, now when users leave the screen. Why?')
    B(C, S_, 1, 'ans', 'apply() không xóa việc chờ đĩa, nó chỉ dời việc chờ đi chỗ khác. Khi Activity chuyển sang onStop (lúc người dùng rời màn hình), hệ thống chờ mọi lần apply() đang ghi cho xong, ngay trên main thread. Mô phỏng ngay dưới cho thấy chỗ chặn dời từ lúc bấm sang lúc rời màn hình. [[src:ax-sp-editor]]',
      'apply() does not remove the wait for the disk; it only moves it. When the Activity goes to onStop (as the user leaves the screen), the system waits for every in-flight apply() to finish, right on the main thread. The simulation just below shows the block moving from the tap to leaving the screen. [[src:ax-sp-editor]]')

    S_ = 'prefsapi'
    a(C + '.sec.%s.title' % S_, 'commit() và apply() thật sự làm gì', 'What commit() and apply() really do')
    a(C + '.sec.%s.badge' % S_, 'impl')
    B(C, S_, 1, 'p', 'Tài liệu Android mô tả hai hàm như sau. commit() ghi đồng bộ và nguyên tử (trọn vẹn hoặc không gì cả), rồi trả về true nếu giá trị đã xuống bộ nhớ bền. apply() đổi bản trong bộ nhớ ngay, bắt đầu ghi đĩa ở nền, và không báo lỗi gì. Nếu một commit() chạy trong lúc còn apply() đang chờ ghi, commit phải đợi mọi lần ghi xong.\nQuy tắc dễ nhớ: commit() cho biết kết quả nhưng bắt bạn chờ; apply() không bắt chờ ngay nhưng không cho biết kết quả. [[src:ax-sp-editor]]',
      'The Android docs describe the two functions like this. commit() writes synchronously and atomically (all or nothing), then returns true if the values reached persistent storage. apply() changes the in-memory copy at once, starts the disk write in the background, and reports no failure. If a commit() runs while an apply() is still waiting to write, commit must wait for all writes to finish.\nRule of thumb: commit() tells you the result but makes you wait; apply() does not make you wait now, but never tells you the result. [[src:ax-sp-editor]]')
    B(C, S_, 2, 'p', 'Bên trong mã nguồn Android, apply() làm ba việc. Nó đổi bản trong bộ nhớ ngay trên luồng gọi. Nó đăng ký một việc "chờ ghi xong" vào một hàng đợi của hệ thống (QueuedWork). Rồi nó giao việc ghi cho luồng nền; việc ghi đó vẫn là ghi lại cả file rồi sync.\nTài liệu nói nốt phần còn lại: hệ thống bảo đảm các lần ghi này xong trước khi Activity hay Service đổi trạng thái. Nghĩa là lúc chuyển trạng thái, main thread phải đứng chờ chúng. [[src:aosp-sp-impl]] [[src:ax-sp-editor]]',
      'Inside the Android source code, apply() does three things. It changes the in-memory copy right away on the calling thread. It registers a "wait for the write" task in a system queue (QueuedWork). Then it hands the write to a background thread; that write is still a full-file rewrite plus a sync.\nThe docs tell the rest: the system makes sure these writes finish before an Activity or Service changes state. So during that transition, the main thread has to wait for them. [[src:aosp-sp-impl]] [[src:ax-sp-editor]]')
    B(C, S_, 3, 'note', 'Đổi commit() thành apply() vẫn đúng khi bạn không cần giá trị trả về; tài liệu nói vậy. Nhưng đó không chữa được ANR tận gốc: file càng lớn thì lần chờ lúc onStop càng dài. Gốc của vấn đề là dữ liệu lớn nằm trong preferences (chương H1, "Chọn nơi lưu"), và việc ghi bị buộc vào vòng đời màn hình.',
      'Replacing commit() with apply() is fine when you do not need the return value; the docs say so. But it does not cure the ANR at its root: the bigger the file, the longer the wait at onStop. The root is large data sitting in preferences (chapter H1, "Choosing where to store data"), and writes being tied to the screen lifecycle.')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'datastore'
    a(C + '.sec.%s.title' % S_, 'DataStore: Flow để đọc, suspend để ghi', 'DataStore: a Flow to read, suspend to write')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', 'DataStore lưu hai loại dữ liệu. Preferences DataStore lưu cặp khóa–giá trị, giống SharedPreferences. Proto DataStore lưu một đối tượng có kiểu rõ ràng, cần một bản mô tả .proto và một Serializer (bộ chuyển đối tượng thành byte).\nDataStore dùng coroutine và Flow nên đọc ghi đều không chặn main thread, dữ liệu luôn nhất quán, và mỗi lần ghi là một giao dịch. Tài liệu Android nói thẳng: đang dùng SharedPreferences thì nên cân nhắc chuyển sang DataStore. Bản trong tài liệu đọc ngày 2026-11-24 là 1.3.0. [[src:ax-datastore]]',
      'DataStore stores two kinds of data. Preferences DataStore stores key–value pairs, like SharedPreferences. Proto DataStore stores one strongly typed object, which needs a .proto description and a Serializer (something that turns the object into bytes).\nDataStore uses coroutines and Flow, so neither reads nor writes block the main thread, data stays consistent, and every write is a transaction. The Android docs say it plainly: if you use SharedPreferences, consider moving to DataStore. The version in the docs as read on 2026-11-24 is 1.3.0. [[src:ax-datastore]]')
    B(C, S_, 2, 'kt', '// một lần, ở cấp cao nhất của file\nval Context.dataStore by preferencesDataStore(name = "settings")\nval DARK = booleanPreferencesKey("dark_theme")\n\nclass SettingsRepository(private val store: DataStore<Preferences>) {\n    val dark: Flow<Boolean> = store.data.map { it[DARK] ?: false }\n    suspend fun setDark(v: Boolean) { store.edit { it[DARK] = v } }   // một giao dịch\n}',
      '// once, at the top level of a file\nval Context.dataStore by preferencesDataStore(name = "settings")\nval DARK = booleanPreferencesKey("dark_theme")\n\nclass SettingsRepository(private val store: DataStore<Preferences>) {\n    val dark: Flow<Boolean> = store.data.map { it[DARK] ?: false }\n    suspend fun setDark(v: Boolean) { store.edit { it[DARK] = v } }   // one transaction\n}')
    B(C, S_, 3, 'p', 'Ghi bằng updateData (hay edit với Preferences) là một thao tác đọc–sửa–ghi nguyên tử: mọi mã trong khối là một giao dịch. Vì vậy hai lần sửa cùng lúc không đè mất nhau. Với SharedPreferences thì khác: hai Editor sửa cùng lúc, lần gọi apply hay commit sau cùng thắng.\nĐọc thì qua data, một Flow. Giao diện thu Flow đó và tự cập nhật khi giá trị đổi.\nQuy tắc dễ nhớ: với DataStore, đọc là "lắng nghe", ghi là "chờ không chặn". [[src:ax-datastore]] [[src:ax-sp-editor]]',
      'Writing with updateData (or edit for Preferences) is one atomic read–modify–write: all code in the block is one transaction. So two edits at the same time do not overwrite each other. SharedPreferences is different: when two Editors change things at once, the last apply or commit wins.\nReading goes through data, a Flow. The UI collects that Flow and updates itself when the value changes.\nRule of thumb: with DataStore, reading is "listening" and writing is "waiting without blocking". [[src:ax-datastore]] [[src:ax-sp-editor]]')

    S_ = 'rules'
    a(C + '.sec.%s.title' % S_, 'Ba quy tắc và cách chuyển dữ liệu cũ', 'Three rules, and moving old data')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Tài liệu Android nêu ba quy tắc khi dùng DataStore.\n(1) Không bao giờ tạo hơn một instance DataStore cho cùng một file trong một tiến trình. Nếu có, đọc hay ghi sẽ ném IllegalStateException. Vì vậy hãy khai báo nó một lần ở cấp cao nhất của file.\n(2) Kiểu T trong DataStore<T> phải bất biến (không sửa được sau khi tạo).\n(3) Không trộn DataStore một tiến trình và nhiều tiến trình cho cùng một file; hỗ trợ nhiều tiến trình có từ bản 1.1.0. [[src:ax-datastore]]',
      'The Android docs give three rules for DataStore.\n(1) Never create more than one DataStore instance for the same file in one process. If you do, reads or writes throw IllegalStateException. So declare it once, at the top level of a file.\n(2) The type T in DataStore<T> must be immutable (unchangeable after creation).\n(3) Do not mix single-process and multi-process DataStore for the same file; multi-process support exists since 1.1.0. [[src:ax-datastore]]')
    B(C, S_, 2, 'p', 'Để chuyển cài đặt cũ sang, truyền một SharedPreferencesMigration khi tạo DataStore. Nó chép các khóa kiểu boolean, float, int, long, string và tập string. Khóa nào đã có trong DataStore thì không chép lại. Nếu SharedPreferences trống sau khi chuyển, nó cố xóa file cũ.\nMigration chạy trước lần đọc đầu tiên. Vì vậy đừng đọc DataStore bên trong migration: hai bên chờ nhau mãi (deadlock). [[src:ax-sp-migration]]',
      'To move old settings over, pass a SharedPreferencesMigration when creating the DataStore. It copies boolean, float, int, long, string and string-set keys. Keys already in DataStore are not copied again. If the SharedPreferences is empty afterwards, it tries to delete the old file.\nMigrations run before the first read. So do not read DataStore inside a migration: the two would wait for each other forever (a deadlock). [[src:ax-sp-migration]]')
    B(C, S_, 3, 'kt', 'val Context.dataStore by preferencesDataStore(\n    name = "settings",\n    produceMigrations = { ctx -> listOf(SharedPreferencesMigration(ctx, "settings_prefs")) },\n)',
      'val Context.dataStore by preferencesDataStore(\n    name = "settings",\n    produceMigrations = { ctx -> listOf(SharedPreferencesMigration(ctx, "settings_prefs")) },\n)')
    B(C, S_, 4, 'note', 'DataStore vẫn chỉ dành cho dữ liệu nhỏ. Nó không cập nhật từng phần, nên mỗi lần ghi là ghi lại cả file. Chuyển một danh sách lớn từ SharedPreferences sang DataStore chỉ là dời vấn đề sang chỗ khác; danh sách thuộc về Room (chương H4, "Room cơ bản").\nQuy tắc dễ nhớ: DataStore cho vài công tắc, Room cho cả danh sách. [[src:ax-datastore]]',
      'DataStore is still only for small data. It has no partial updates, so every write rewrites the whole file. Moving a big list from SharedPreferences to DataStore just moves the problem elsewhere; the list belongs in Room (chapter H4, "Room basics").\nRule of thumb: DataStore for a few switches, Room for whole lists. [[src:ax-datastore]]')
    B(C, S_, 4, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'App crash với IllegalStateException: "There are multiple DataStores active for the same file".', 'The app crashes with IllegalStateException: "There are multiple DataStores active for the same file".')
    B(C, S_, 1, 'cause', 'Mỗi màn hình tự gọi PreferenceDataStoreFactory.create(...) cho cùng file settings, tạo nhiều instance trong một tiến trình.', 'Each screen calls PreferenceDataStoreFactory.create(...) for the same settings file, creating several instances in one process.')
    B(C, S_, 1, 'fix', 'Một instance cho cả app: delegate preferencesDataStore ở cấp cao nhất, hoặc một singleton được DI cung cấp (chương G6).', 'One instance for the whole app: the preferencesDataStore delegate at the top level, or a singleton provided by DI (chapter G6).')
    B(C, S_, 2, 'bug', 'Người dùng bật thông báo nhắc lịch, đóng app; lần mở sau, công tắc lại tắt. Không có lỗi nào trong log.', 'A user turns on appointment reminders and closes the app; next launch, the switch is off again. Nothing in the log.')
    B(C, S_, 2, 'cause', 'Cài đặt được lưu bằng apply(); lần ghi xuống đĩa thất bại (máy gần đầy) và apply không báo lỗi. Bộ nhớ nói đã bật, đĩa thì chưa.', 'The setting was saved with apply(); the disk write failed (the device was nearly full) and apply reports no failure. Memory said on, the disk did not.')
    B(C, S_, 2, 'fix', 'Chuyển sang DataStore: lỗi ghi ném ra từ edit, bắt được và báo cho người dùng; UI đọc từ Flow nên luôn hiện giá trị đã thật sự lưu.', 'Move to DataStore: a write failure is thrown from edit, so you can catch it and tell the user; the UI reads from the Flow, so it always shows the value actually stored.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Hẹn Khám đang lưu ba cài đặt trong SharedPreferences "settings_prefs": dark_theme (boolean), reminder_minutes (int), language (string). Viết SettingsRepository dùng Preferences DataStore: (1) chuyển ba khóa cũ một lần; (2) lộ ra một Flow<Settings> gộp cả ba; (3) một hàm suspend đổi reminder_minutes, không cho giá trị ngoài 0..1440.',
      'ClinicBook stores three settings in the SharedPreferences "settings_prefs": dark_theme (boolean), reminder_minutes (int), language (string). Write a SettingsRepository using Preferences DataStore: (1) migrate the three old keys once; (2) expose one Flow<Settings> combining all three; (3) a suspend function that changes reminder_minutes, rejecting values outside 0..1440.')
    B(C, S_, 1, 'hint', 'SharedPreferencesMigration đặt trong produceMigrations; ba khóa giữ nguyên tên nên đọc lại bằng cùng tên khóa. Settings là data class bất biến.', 'Put SharedPreferencesMigration in produceMigrations; the three keys keep their names, so read them back by the same names. Settings is an immutable data class.')
    B(C, S_, 1, 'sol', 'Khai báo DataStore một lần ở cấp cao nhất với produceMigrations. Ba khóa: booleanPreferencesKey, intPreferencesKey, stringPreferencesKey cùng tên cũ. data.map dựng Settings với giá trị mặc định khi thiếu khóa. setReminder kiểm khoảng trước rồi edit.',
      'Declare the DataStore once at the top level with produceMigrations. Three keys: booleanPreferencesKey, intPreferencesKey, stringPreferencesKey with the old names. data.map builds Settings with defaults when a key is missing. setReminder checks the range, then edits.')
    B(C, S_, 1, 'solkt', 'data class Settings(val dark: Boolean = false, val reminderMinutes: Int = 60, val language: String = "vi")\n\nval Context.settingsStore by preferencesDataStore("settings",\n    produceMigrations = { listOf(SharedPreferencesMigration(it, "settings_prefs")) })\n\nprivate val DARK = booleanPreferencesKey("dark_theme")\nprivate val REMIND = intPreferencesKey("reminder_minutes")\nprivate val LANG = stringPreferencesKey("language")\n\nclass SettingsRepository(private val store: DataStore<Preferences>) {\n    val settings: Flow<Settings> = store.data.map {\n        Settings(it[DARK] ?: false, it[REMIND] ?: 60, it[LANG] ?: "vi")\n    }\n    suspend fun setReminder(min: Int) {\n        require(min in 0..1440) { "reminder out of range" }\n        store.edit { it[REMIND] = min }\n    }\n}')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'apply() có thể chặn main thread lúc nào?', 'When can apply() block the main thread?')
    B(C, S_, 1, 'ans', 'Lúc Activity hay Service đổi trạng thái (ví dụ onStop): framework chờ các lần apply() đang ghi cho xong.', 'When an Activity or Service changes state (for example onStop): the framework waits for in-flight apply() writes to finish.')
    B(C, S_, 2, 'ask', 'Vì sao chỉ được có một instance DataStore cho một file trong một tiến trình?', 'Why may there be only one DataStore instance per file in a process?')
    B(C, S_, 2, 'ans', 'DataStore giữ dữ liệu và bảo đảm giao dịch cho file đó; hai instance sẽ phá đảm bảo này, nên DataStore ném IllegalStateException khi phát hiện.', 'DataStore owns the data and the transactional guarantees for that file; two instances would break them, so DataStore throws IllegalStateException when it detects one.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'commit() trả về gì?', 'What does commit() return?', 'true nếu giá trị mới đã ghi thành công xuống bộ nhớ bền.', 'true if the new values were written to persistent storage.', 'Và nó chỉ trả về khi ghi xong, trên luồng gọi.', 'And it returns only once the write is done, on the calling thread.'),
        ('q2', 'apply() báo lỗi ghi đĩa thế nào?', 'How does apply() report a disk write failure?', 'Không báo.', 'It does not.', 'Không có giá trị trả về, không có callback.', 'No return value, no callback.'),
        ('q3', 'Hàm ghi của DataStore là loại hàm gì?', 'What kind of function is DataStore\'s write?', 'Hàm suspend (edit hay updateData), chạy như một giao dịch.', 'A suspend function (edit or updateData), run as one transaction.', 'Main thread không bị chặn; chỉ coroutine tạm dừng.', 'The main thread is not blocked; only the coroutine suspends.'),
        ('q4', 'Hỗ trợ nhiều tiến trình của DataStore có từ bản nào?', 'Since which version does DataStore support multiple processes?', '1.1.0.', '1.1.0.', 'Không trộn DataStore một tiến trình và nhiều tiến trình cho cùng một file.', 'Do not mix single- and multi-process DataStore for the same file.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
