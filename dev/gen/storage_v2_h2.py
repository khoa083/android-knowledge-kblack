# Lưu dữ liệu · H2: file riêng của app (Phần 1)
# Nguồn: developer.android.com App-specific storage, AtomicFile (androidx.core) (đọc 2026-11-24); rename(2) man7.org.
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'h2': ['hook', 'dirs', 'atomic', 'cache', 'bugs', 'ex', 'recall']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.file', 'Lưu dữ liệu · ghi file an toàn và file trong cache', 'Saving data · writing files safely, and files in the cache')
    m = lambda k, vi, en=None: a('m.file.' + k, vi, en)
    m('title', 'Ghi file khi tiến trình có thể chết bất cứ lúc nào', 'Writing a file when the process can die at any moment')
    m('overview', 'Người dùng đang gõ dở một bản nháp ghi chú trong app Hẹn Khám, và app lưu nó vào filesDir (thư mục riêng của app). Có hai cách lưu: ghi thẳng vào draft.txt, hoặc ghi qua AtomicFile. Đúng lúc đang ghi thì tiến trình (process, chương trình đang chạy của app) bị hệ thống giết. Tình huống thứ ba theo một file PDF nằm trong cache qua một lần máy thiếu chỗ.',
      "The user is halfway through a draft note in ClinicBook, and the app saves it to filesDir (the app's own directory). There are two ways to save: write straight into draft.txt, or write through AtomicFile. Right in the middle of the write, the system kills the process (the app's running program). A third case follows a PDF in the cache through a low-storage event.")
    m('wrapup', 'Mở FileOutputStream là file cũ bị cắt về 0 byte ngay lập tức. Nếu tiến trình chết giữa lúc ghi, trên đĩa chỉ còn một file dở dang. AtomicFile thì ghi sang một file phụ tên .new, đẩy hết xuống đĩa, rồi mới đổi tên đè lên file gốc. Nhờ vậy lúc nào trên đĩa cũng có một bản trọn vẹn; cùng lắm mất lần sửa đang ghi.\nCache thì khác: đó không phải chỗ lưu bền. Hệ thống được quyền xóa nó, nên luôn kiểm file còn trước khi đọc.\nHình dung: viết lại một lá thư ra tờ giấy mới, viết xong mới thay tờ cũ, thay vì tẩy trắng tờ cũ rồi viết lên.',
      'Opening a FileOutputStream cuts the old file to 0 bytes at once. If the process dies mid-write, only a half-written file is left on disk. AtomicFile instead writes to a side file named .new, pushes it all to disk, and only then renames it over the original. So there is always one complete version on disk; at worst you lose the edit being written.\nThe cache is different: it is not durable storage. The system is allowed to delete it, so always check a file exists before reading it.\nPicture rewriting a letter on a fresh sheet and swapping it in only when finished, instead of erasing the old sheet and writing over it.')
    m('simp.1', 'Bốn bước là bốn thời điểm chọn lọc; ghi thật có thể nhanh hơn một lần kill rất nhiều. Cú kill đại diện cho mọi lần tiến trình chết giữa chừng: hệ thống thu hồi bộ nhớ, app crash, máy sập nguồn.',
      'The four steps are four chosen moments; a real write may be far quicker than any kill. The kill stands for every way a process can die mid-write: the system reclaiming memory, a crash, a power loss.')
    m('simp.2', 'Hành vi của AtomicFile theo tài liệu tham chiếu của androidx.core; việc đổi tên là nguyên tử (xảy ra trọn trong một bước) theo tài liệu rename(2) của Linux, nền của Android. Site không chạy app thật. Chương không bàn đổi tên giữa hai hệ thống file khác nhau (khi đó không nguyên tử). DataStore và Room tự lo ghi an toàn cho file của chúng (chương H3, H4).',
      "AtomicFile's behaviour follows the androidx.core reference docs; the rename being atomic (happening whole, in one step) follows Linux's rename(2) docs, which Android is built on. The site does not run a real app. The chapter does not cover renaming across two different file systems (not atomic then). DataStore and Room handle safe writes of their own files (chapters H3, H4).")
    m('ctl.hint', 'Đổi cách rồi đi lại; so cột "Đĩa" ở bước 3 và bước 4.', 'Switch the case and walk again; compare the "Disk" row at steps 3 and 4.')
    m('ctl.case', 'Cách', 'Case')
    for k, vi, en in [('direct', 'ghi thẳng vào draft.txt', 'write straight into draft.txt'), ('atomic', 'ghi qua AtomicFile', 'write through AtomicFile'), ('cache', 'PDF trong cache', 'a PDF in the cache')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'App, hệ thống, file trên đĩa', 'App, system, file on disk')
    m('diagramDesc', 'App ghi và đọc file; hệ thống có thể giết tiến trình hay xóa cache', 'The app writes and reads the file; the system may kill the process or delete the cache')
    for k, vi, en in [('app', 'Tiến trình app', 'App process'), ('disk', 'File trên đĩa', 'File on disk'), ('sys', 'Hệ thống Android', 'Android system')]:
        m('n.' + k, vi, en)
    m('met.file', 'File trên đĩa', 'File on disk'); m('met.lost', 'Người dùng mất', 'The user loses')
    for k, vi, en in [('empty', 'rỗng (vừa bị cắt)', 'empty (just truncated)'), ('partial', 'dở dang', 'half-written'), ('intact', 'trọn vẹn', 'complete'), ('missing', 'không còn', 'gone')]:
        m('file.' + k, vi, en)
    for k, vi, en in [('none', 'chưa mất gì', 'nothing yet'), ('all', 'cả bản nháp', 'the whole draft'), ('edit', 'chỉ lần sửa đang ghi', 'only the edit being written'), ('crash', 'app báo lỗi khi mở', 'the app fails to open it')]:
        m('lost.' + k, vi, en)
    a('cap.file', 'App ghi xuống file trên đĩa; hệ thống (bên dưới) có thể giết tiến trình hay dọn cache. Khối viền đỏ là chỗ dữ liệu hỏng hay mất.', 'The app writes to the file on disk; the system (below) may kill the process or clear the cache. A red outline marks where data is corrupted or lost.')
    S = [
        ('direct', 's1', 'Mở FileOutputStream: draft.txt về 0 byte', 'Open a FileOutputStream: draft.txt drops to 0 bytes',
         'Mở FileOutputStream không ở chế độ nối thêm thì nội dung cũ bị cắt ngay khi mở, trước khi ghi byte nào. Từ lúc này, bản nháp cũ không còn trên đĩa.', 'Opening a FileOutputStream without append mode truncates the old contents the moment it opens, before a single byte is written. From here on, the old draft is no longer on disk.'),
        ('direct', 's2', 'Ghi được nửa bản nháp mới', 'Half of the new draft is written',
         'Bản nháp 40 KB đang được ghi; trên đĩa mới có 20 KB đầu. Nếu mọi thứ suôn sẻ, vài mili giây nữa là xong.', 'The 40 KB draft is being written; the first 20 KB are on disk. If all goes well, it finishes in a few milliseconds.'),
        ('direct', 's3', 'Tiến trình bị giết giữa lúc ghi', 'The process is killed mid-write',
         'App ở nền, máy thiếu bộ nhớ, hệ thống giết tiến trình. Không có cơ hội chạy finally hay đóng stream. Trên đĩa còn nửa file mới; bản cũ đã mất từ bước 1.', 'The app is in the background, memory is short, the system kills the process. No chance to run finally or close the stream. Half of the new file is on disk; the old version was lost at step 1.'),
        ('direct', 's4', 'Mở lại app: đọc được nửa bản nháp', 'Reopen the app: half a draft is read',
         'readText trả về 20 KB đầu, không báo lỗi. Nếu file là JSON, parse sẽ ném ngoại lệ; nếu là văn bản, người dùng thấy bản nháp bị cụt mà không biết vì sao.', 'readText returns the first 20 KB without complaint. If the file is JSON, parsing throws; if it is text, the user sees a truncated draft with no idea why.'),
        ('atomic', 's1', 'startWrite: ghi vào draft.txt.new', 'startWrite: writing to draft.txt.new',
         'AtomicFile không đụng tới draft.txt. Nó mở một file mới tên draft.txt.new và trả stream của file đó.', 'AtomicFile does not touch draft.txt. It opens a new file named draft.txt.new and returns that file\'s stream.'),
        ('atomic', 's2', 'Ghi được nửa bản nháp vào file .new', 'Half the draft is written to the .new file',
         'draft.txt vẫn là bản cũ trọn vẹn; nửa bản mới nằm trong draft.txt.new.', 'draft.txt is still the complete old version; half of the new one sits in draft.txt.new.'),
        ('atomic', 's3', 'Tiến trình bị giết giữa lúc ghi', 'The process is killed mid-write',
         'Cùng cú kill như cách kia. finishWrite chưa chạy, nên chưa có lần đổi tên nào; file gốc không hề bị đụng tới.', 'The same kill as before. finishWrite never ran, so no rename happened; the original file was never touched.'),
        ('atomic', 's4', 'Mở lại app: đọc bản cũ trọn vẹn', 'Reopen the app: the complete old version is read',
         'readFully đọc draft.txt: bản trước lần sửa cuối. Người dùng mất đúng lần sửa đang ghi, không mất cả bản nháp, và file không bao giờ dở dang.', 'readFully reads draft.txt: the version before the last edit. The user loses exactly the edit being written, not the whole draft, and the file is never half-written.'),
        ('cache', 's1', 'Tải PDF kết quả về cacheDir', 'Download the results PDF into cacheDir',
         'Lần đầu mở kết quả xét nghiệm, app tải PDF 2 MB và lưu vào cacheDir để lần sau mở ngay.', 'The first time the lab results are opened, the app downloads a 2 MB PDF and saves it in cacheDir so it opens instantly next time.'),
        ('cache', 's2', 'Máy thiếu chỗ: hệ thống xóa file cache', 'Space runs low: the system deletes cache files',
         'Vài ngày sau người dùng quay video dài, bộ nhớ trong gần đầy. Hệ thống xóa file trong cache của các app để lấy lại chỗ; app không được báo.', 'Days later the user records a long video and internal storage is nearly full. The system deletes files from apps\' caches to reclaim space; the app is not told.'),
        ('cache', 's3', 'Mở thẳng file: FileNotFoundException', 'Open the file as is: FileNotFoundException',
         'App giả định file vẫn còn và mở thẳng. File không còn nữa: mở báo FileNotFoundException, màn hình kết quả báo lỗi.', 'The app assumes the file is still there and opens it. It is gone: opening throws FileNotFoundException and the results screen shows an error.'),
        ('cache', 's4', 'Kiểm trước, thiếu thì tải lại', 'Check first, download again if missing',
         'Kiểm exists() trước khi đọc; không còn thì tải lại. Người dùng chỉ chờ thêm một lần tải, không thấy lỗi.', 'Check exists() before reading; if it is missing, download it again. The user waits for one more download and sees no error.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cách; để ý làn "Đĩa".', 'Walk all four steps of each case; watch the "Disk" row.'),
        ('direct.s2', 'Không có gì sai ở bước này. Vấn đề nằm ở chỗ bản cũ đã mất từ lúc mở stream, nên mọi khoảng thời gian ghi đều là khoảng nguy hiểm.', 'Nothing is wrong at this step. The trouble is that the old version was gone the moment the stream opened, so the whole write is a window of danger.'),
        ('direct.s3', 'Tiến trình đã chết thì không còn mã nào chạy để dọn dẹp. Mọi lần ghi phải giả định có thể bị cắt ở bất kỳ byte nào.', 'A dead process runs no more code, so no cleanup can happen. Every write must assume it can be cut off at any byte.'),
        ('direct.s4', 'Đọc file dở dang không báo lỗi: readText trả về bao nhiêu byte có trên đĩa. Lỗi chỉ lộ ra ở bước parse hay khi người dùng đọc.', 'Reading a half-written file raises no error: readText returns whatever bytes are on disk. The failure only shows when parsing, or when the user reads it.'),
        ('atomic.s2', 'Tài liệu Android nói: ghi vào file mới có thêm hậu tố ".new", xong mới đổi tên đè lên file gốc. [[src:ax-atomicfile]]', 'The Android docs say: it writes to a new file with ".new" appended, and only then renames it over the original. [[src:ax-atomicfile]]'),
        ('atomic.s3', 'finishWrite mới là lúc đóng, sync xuống đĩa và đổi tên. Chưa tới đó thì file gốc vẫn y nguyên. [[src:ax-atomicfile]]', 'finishWrite is when the stream is closed, synced to disk and renamed. Until then the original file is untouched. [[src:ax-atomicfile]]'),
        ('atomic.s4', 'Đổi tên đè lên một tên đã có là nguyên tử trên Linux: không có lúc nào tên đích không tồn tại. Người đọc thấy bản cũ hoặc bản mới, không bao giờ thấy nửa bản. [[src:man-rename]]', 'Renaming over an existing name is atomic on Linux: there is no moment when the target name is missing. A reader sees the old version or the new one, never half of one. [[src:man-rename]]'),
        ('cache.s2', 'Tài liệu Android nói: khi máy thiếu bộ nhớ trong, Android có thể xóa file cache để lấy lại chỗ. [[src:ax-app-specific]]', 'The Android docs say: when the device is low on internal storage, Android may delete cache files to reclaim space. [[src:ax-app-specific]]'),
        ('cache.s3', 'Tài liệu đó cũng dặn: kiểm file cache còn tồn tại trước khi đọc. [[src:ax-app-specific]]', 'The same docs say: check that a cache file exists before reading it. [[src:ax-app-specific]]'),
        ('cache.s4', 'Cache chỉ dành cho thứ lấy lại được. Kiểm rồi tải lại biến chuyện file bị xóa thành một lần chờ, không thành lỗi. [[src:ax-app-specific]]', 'The cache is only for things you can get back. Checking and downloading again turns a deleted file into a short wait, not an error. [[src:ax-app-specific]]')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.fl', 'Làn thời gian', 'Timeline lanes')
    z('fl.cap', 'Mỗi hàng là một làn, mỗi cột là một bước. Cột đang xem có viền; ô gạch đỏ là chỗ dữ liệu hỏng, mất hay lỗi.', 'Each row is a lane, each column a step. The current column is outlined; a red hatched cell is where data is corrupted, lost or fails.')
    z('fl.legend', '"Đĩa" là những gì thật sự nằm trên bộ nhớ, thứ còn lại sau khi tiến trình chết.', '"Disk" is what is really in storage: what is left after the process dies.')
    z('fl.lane', 'Làn', 'Lane')
    for k, vi, en in [('app', 'App', 'App'), ('sys', 'Hệ thống', 'System'), ('disk', 'Đĩa', 'Disk')]:
        z('fl.lane.' + k, vi, en)
    for c, cols in [('direct', [('mở stream', 'open stream'), ('đang ghi', 'writing'), ('bị giết', 'killed'), ('mở lại', 'reopen')]),
                    ('atomic', [('startWrite', 'startWrite()'), ('đang ghi', 'writing'), ('bị giết', 'killed'), ('mở lại', 'reopen')]),
                    ('cache', [('tải về', 'download'), ('thiếu chỗ', 'low space'), ('mở thẳng', 'open as is'), ('kiểm rồi mở', 'check, then open')])]:
        for i, (vi, en) in enumerate(cols):
            z('fl.col.%s.%d' % (c, i), vi, en)
    for k, vi, en in [
        ('openOut', 'FileOutputStream(draft.txt)', 'FileOutputStream(draft.txt) opened'), ('idle', '·', '–'),
        ('truncated', 'draft.txt: 0 byte, bản cũ mất', 'draft.txt: 0 bytes, old version gone'),
        ('writeHalf', 'ghi 20/40 KB', 'wrote 20/40 KB'), ('halfNew', 'draft.txt: nửa bản mới', 'draft.txt: half of the new one'),
        ('dead', 'đã chết, không dọn dẹp', 'dead, no cleanup'), ('kill', 'giết tiến trình', 'kills the process'),
        ('readHalf', 'đọc được nửa bản nháp', 'reads half a draft'), ('restart', 'khởi động lại app', 'restarts the app'),
        ('startWrite', 'startWrite()', 'startWrite() called'), ('oldPlusNew', 'draft.txt cũ nguyên; .new rỗng', 'old draft.txt intact; .new empty'),
        ('oldPlusHalf', 'draft.txt cũ nguyên; .new nửa', 'old draft.txt intact; .new half'),
        ('readOld', 'đọc bản cũ trọn vẹn', 'reads the complete old version'), ('oldOnly', 'draft.txt cũ nguyên', 'old draft.txt intact'),
        ('download', 'tải PDF vào cacheDir', 'downloads the PDF into cacheDir'), ('pdfCached', 'cache/result.pdf 2 MB', 'cache/result.pdf, 2 MB'),
        ('background', 'nằm nền', 'in the background'), ('lowSpace', 'thiếu chỗ: xóa file cache', 'low space: deletes cache files'),
        ('pdfGone', 'result.pdf không còn', 'result.pdf is gone'), ('openBlind', 'mở thẳng: FileNotFoundException', 'opens it: FileNotFoundException'),
        ('checkRefetch', 'exists() sai → tải lại', 'exists() is false → downloads again')]:
        z('fl.cell.' + k, vi, en)

    C = 'h2'
    a(C + '.title', 'File riêng của app', 'App-specific files')
    a(C + '.essence', 'filesDir giữ file tới khi gỡ app. cacheDir dành cho thứ lấy lại được, vì hệ thống có thể xóa nó khi máy thiếu chỗ. Cả hai đều không cần xin quyền.\nMở FileOutputStream là cắt file cũ về 0 byte. Nếu tiến trình chết giữa lúc ghi, file sẽ bị dở dang.\nAtomicFile ghi sang file .new, đẩy xuống đĩa rồi đổi tên đè lên file gốc, nên trên đĩa lúc nào cũng có một bản trọn vẹn.',
      'filesDir keeps files until uninstall. cacheDir is for things you can get back, because the system may delete it when space runs low. Neither needs a permission.\nOpening a FileOutputStream cuts the old file to 0 bytes. If the process dies mid-write, the file is left half-written.\nAtomicFile writes to a .new file, pushes it to disk, then renames it over the original, so there is always one complete version on disk.')
    a(C + '.goal.g1', 'Đã thấy cú kill giữa lúc ghi', 'Saw the mid-write kill')
    a(C + '.goal.g2', 'Đã mở lại file sau cú kill', 'Reopened the file after the kill')
    a(C + '.sim.storage.file', 'ghi file khi tiến trình có thể chết', 'writing a file when the process may die')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Hàm lưu bản nháp mở FileOutputStream(draft.txt) rồi ghi 40 KB. Tiến trình bị giết khi mới ghi được 20 KB. Lần sau mở app, draft.txt chứa gì: bản nháp cũ, bản nháp mới, hay thứ khác?',
      'The save function opens FileOutputStream(draft.txt) and writes 40 KB. The process is killed after 20 KB. Next time the app opens, what does draft.txt hold: the old draft, the new draft, or something else?')
    B(C, S_, 1, 'ans', 'Thứ khác: 20 KB đầu của bản mới. Bản cũ đã mất ngay lúc mở stream (luồng ghi), vì FileOutputStream cắt file về 0 byte khi mở. Lần sau mở app sẽ đọc được một bản nháp bị cụt. Mô phỏng ngay dưới so cách này với AtomicFile.',
      'Something else: the first 20 KB of the new draft. The old version was lost the moment the stream (the write channel) opened, because FileOutputStream cuts the file to 0 bytes on open. Next launch reads a truncated draft. The simulation just below compares this with AtomicFile.')

    S_ = 'dirs'
    a(C + '.sec.%s.title' % S_, 'Thư mục riêng của app', 'The app\'s own directories')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Mỗi app có hai thư mục riêng trong bộ nhớ trong. filesDir dành cho file cần giữ lâu, như bản nháp. cacheDir dành cho file tạm, như PDF tải về để xem nhanh. Cả hai không cần xin quyền, app khác không đọc được, được mã hóa từ Android 10, và bị xóa khi gỡ app.\nỞ bộ nhớ ngoài có hai thư mục tương ứng: getExternalFilesDir() và externalCacheDir. Chúng rộng hơn, không cần quyền từ Android 4.4, nhưng không phải lúc nào cũng có (ví dụ khi tháo thẻ nhớ). Vì vậy dữ liệu app cần để chạy phải ở bộ nhớ trong.\nQuy tắc dễ nhớ: filesDir là ngăn kéo, cacheDir là cái bàn mà người dọn dẹp có thể lau bất cứ lúc nào. [[src:ax-app-specific]]',
      'Each app has two private directories in internal storage. filesDir is for files to keep, such as a draft. cacheDir is for temporary files, such as a PDF downloaded for quick viewing. Neither needs a permission, other apps cannot read them, they are encrypted from Android 10, and they are removed on uninstall.\nExternal storage has two matching directories: getExternalFilesDir() and externalCacheDir. They are larger and permission-free from Android 4.4, but not always present (for example when an SD card is removed). So data the app needs to run must be internal.\nRule of thumb: filesDir is a drawer; cacheDir is a desk the cleaner may wipe at any time. [[src:ax-app-specific]]')
    B(C, S_, 2, 'kt', 'File(context.filesDir, "draft.txt").writeText(text)          // lâu dài, riêng tư\nFile.createTempFile("result", ".pdf", context.cacheDir)       // tạm thời\ncontext.openFileOutput("log.txt", Context.MODE_PRIVATE)      // API cũ hơn, cũng vào filesDir\ncontext.getExternalFilesDir(Environment.DIRECTORY_PICTURES)  // ngoài, có thể null nếu không gắn',
      'File(context.filesDir, "draft.txt").writeText(text)          // lasting, private\nFile.createTempFile("result", ".pdf", context.cacheDir)       // temporary\ncontext.openFileOutput("log.txt", Context.MODE_PRIVATE)      // older API, also into filesDir\ncontext.getExternalFilesDir(Environment.DIRECTORY_PICTURES)  // external, may be null if not mounted')
    B(C, S_, 3, 'note', 'Từ Android 7.0, gọi openFileOutput với chế độ khác MODE_PRIVATE sẽ ném SecurityException (lỗi bảo mật). Muốn đưa một file nội bộ cho app khác, đừng mở quyền của file. Hãy dùng FileProvider: nó đưa cho app kia một URI (địa chỉ dạng content://) kèm quyền đọc tạm thời. [[src:ax-app-specific]]',
      "From Android 7.0, calling openFileOutput with any mode other than MODE_PRIVATE throws a SecurityException. To hand an internal file to another app, do not open up the file's permissions. Use FileProvider: it gives the other app a URI (a content:// address) with temporary read permission. [[src:ax-app-specific]]")
    B(C, S_, 3, 'kind', 'android')

    S_ = 'atomic'
    a(C + '.sec.%s.title' % S_, 'Ghi để không bao giờ có file dở dang', 'Writing so there is never a half-written file')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Ghi thẳng vào file có hai điểm yếu nối tiếp nhau. Thứ nhất, mở stream là file cũ bị cắt ngay. Thứ hai, việc ghi cần thời gian. Trong khoảng giữa đó, trên đĩa không có bản nào trọn vẹn, và tiến trình có thể chết đúng lúc ấy.\nCách sửa là đừng bao giờ ghi đè lên chính file đang dùng. Ghi bản mới sang một file khác, đẩy hết xuống đĩa, rồi đổi tên đè lên file cũ trong một bước.\nQuy tắc dễ nhớ: đừng phá bản cũ khi bản mới chưa xong.',
      'Writing straight into a file has two weaknesses back to back. First, opening the stream cuts the old file at once. Second, writing takes time. In between, no complete version exists on disk, and the process may die right then.\nThe fix is never to overwrite the file in use. Write the new version to another file, push it all to disk, then rename it over the old one in a single step.\nRule of thumb: do not destroy the old version before the new one is finished.')
    B(C, S_, 2, 'p', 'AtomicFile (có trong androidx.core từ bản 1.1.0) làm đúng việc đó, qua ba hàm. startWrite mở một file mới tên "<tên>.new". finishWrite đóng stream, sync (đẩy dữ liệu từ bộ nhớ đệm xuống hẳn đĩa), rồi đổi tên đè lên file gốc. failWrite đóng và xóa file .new khi có lỗi.\nTrên Linux, đổi tên đè lên một tên đã có là nguyên tử: người đọc thấy bản cũ hoặc bản mới, không có lúc nào file biến mất hay chỉ có một nửa. [[src:ax-atomicfile]] [[src:man-rename]]',
      'AtomicFile (in androidx.core since 1.1.0) does exactly that, through three functions. startWrite opens a new file named "<name>.new". finishWrite closes the stream, syncs it (pushes the data from memory buffers all the way to disk), then renames it over the original. failWrite closes and deletes the .new file on error.\nOn Linux, renaming over an existing name is atomic: a reader sees the old version or the new one, and the file is never missing or half there. [[src:ax-atomicfile]] [[src:man-rename]]')
    B(C, S_, 3, 'kt', 'val file = AtomicFile(File(filesDir, "draft.txt"))\nval out = file.startWrite()            // không gọi out.close() tự tay\ntry {\n    out.write(text.toByteArray())\n    file.finishWrite(out)              // close + sync + rename\n} catch (e: IOException) {\n    file.failWrite(out)                // xóa draft.txt.new, bản cũ còn nguyên\n    throw e\n}',
      'val file = AtomicFile(File(filesDir, "draft.txt"))\nval out = file.startWrite()            // do not call out.close() yourself\ntry {\n    out.write(text.toByteArray())\n    file.finishWrite(out)              // close + sync + rename\n} catch (e: IOException) {\n    file.failWrite(out)                // deletes draft.txt.new, the old one is intact\n    throw e\n}')
    B(C, S_, 4, 'note', 'AtomicFile không khóa file. Nếu hai luồng cùng gọi startWrite trên một file, lần ghi của luồng đầu có thể bị hỏng hay mất. Hãy để một nơi duy nhất ghi file đó, ví dụ một repository dùng Mutex (khóa cho coroutine) để mỗi lúc chỉ một lần ghi chạy. [[src:ax-atomicfile]]',
      "AtomicFile does not lock the file. If two threads call startWrite on the same file, the first thread's write may be corrupted or lost. Let a single place write that file, for example a repository that uses a Mutex (a lock for coroutines) so only one write runs at a time. [[src:ax-atomicfile]]")
    B(C, S_, 4, 'kind', 'pitfall')

    S_ = 'cache'
    a(C + '.sec.%s.title' % S_, 'Cache không phải chỗ lưu bền', 'The cache is not durable storage')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Khi máy thiếu bộ nhớ trong, Android có thể xóa file trong cacheDir để lấy lại chỗ. Việc này có thể xảy ra bất cứ lúc nào, sớm hơn nhiều so với lúc gỡ app, và app không được báo.\nVì vậy tài liệu Android dặn hai điều. Một: kiểm file cache còn không trước khi đọc. Hai: đừng trông vào hệ thống để dọn cache hộ mình; file nào không cần nữa thì tự xóa bằng File.delete() hay deleteFile(). [[src:ax-app-specific]]',
      'When the device is low on internal storage, Android may delete files in cacheDir to reclaim space. This can happen at any time, much sooner than an uninstall, and the app is not told.\nSo the Android docs say two things. One: check that a cache file still exists before reading it. Two: do not rely on the system to clean your cache for you; delete files you no longer need with File.delete() or deleteFile(). [[src:ax-app-specific]]')
    B(C, S_, 2, 'p', 'Cache nên lớn tới đâu? StorageManager.getCacheQuotaBytes() cho biết hạn mức gợi ý cho app. Trước khi ghi một file lớn, getAllocatableBytes() cho biết có thể lấy được bao nhiêu chỗ, và allocateBytes() giữ trước chỗ đó. Con số này có thể lớn hơn chỗ trống hiện có, vì hệ thống tính cả cache của app khác mà nó được phép xóa. [[src:ax-app-specific]]',
      "How large should the cache grow? StorageManager.getCacheQuotaBytes() gives the app's suggested quota. Before writing a large file, getAllocatableBytes() tells you how much space you can get, and allocateBytes() reserves it. That number can exceed current free space, because the system counts other apps' caches it is allowed to delete. [[src:ax-app-specific]]")
    B(C, S_, 3, 'note', 'Thứ người dùng tự tạo ra (bản nháp, ảnh chụp, lịch đặt lúc mất mạng) không bao giờ để trong cache.\nQuy tắc dễ nhớ: tự hỏi "nếu file này biến mất ngay bây giờ, mình có lấy lại được không?". Không thì đừng để trong cache.',
      'Things the user creates (drafts, photos, appointments booked offline) never go in the cache.\nRule of thumb: ask "if this file vanished right now, could I get it back?". If not, keep it out of the cache.')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Vài người dùng báo app crash ngay lúc mở, gỡ ra cài lại mới hết. Log có JsonDecodeException: Unexpected end of input.', 'A few users report the app crashing on launch until they reinstall. The log shows JsonDecodeException: Unexpected end of input.')
    B(C, S_, 1, 'cause', 'File cấu hình JSON được ghi thẳng bằng writeText. Một lần tiến trình bị giết giữa lúc ghi đã để lại file cụt. Từ đó, mỗi lần mở app đều đọc file cụt này, parse thất bại và crash.',
      'The JSON config file is written in place with writeText. One kill mid-write left a truncated file. Since then, every launch reads that truncated file, fails to parse it, and crashes.')
    B(C, S_, 1, 'fix', 'Ghi qua AtomicFile; khi đọc, bắt lỗi parse và quay về mặc định thay vì crash.', 'Write through AtomicFile; when reading, catch parse errors and fall back to defaults instead of crashing.')
    B(C, S_, 2, 'bug', 'Ảnh thu nhỏ của bác sĩ thỉnh thoảng hiện ô trống; màn hình không bao giờ tải lại.', 'Doctors\' thumbnails sometimes show as blank squares; the screen never reloads them.')
    B(C, S_, 2, 'cause', 'App lưu đường dẫn ảnh trong cache vào database và coi là "đã tải". Hệ thống xóa cache khi máy thiếu chỗ; database vẫn nói ảnh đã có.', 'The app stores the cached image path in its database and treats it as "downloaded". The system cleared the cache when space ran low; the database still says the image is there.')
    B(C, S_, 2, 'fix', 'Không coi file cache là đã có: kiểm exists() lúc hiển thị và tải lại khi thiếu.', 'Never treat a cache file as present: check exists() when displaying and download again when it is missing.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Viết hàm saveConfig(config: Config) ghi config dạng JSON vào filesDir/config.json sao cho: (1) một cú kill ở bất kỳ byte nào không bao giờ để lại file hỏng; (2) hai lời gọi saveConfig cùng lúc từ hai coroutine không phá nhau. Viết thêm loadConfig() trả về Config mặc định nếu file chưa có hay không đọc được.',
      'Write saveConfig(config: Config) that stores config as JSON in filesDir/config.json so that: (1) a kill at any byte never leaves a corrupted file; (2) two concurrent saveConfig calls from two coroutines do not break each other. Also write loadConfig() that returns the default Config if the file is missing or unreadable.')
    B(C, S_, 1, 'hint', 'AtomicFile lo yêu cầu (1) nhưng không khóa file; yêu cầu (2) cần một Mutex hay một nơi duy nhất ghi.', 'AtomicFile handles requirement (1) but does not lock the file; requirement (2) needs a Mutex or a single writer.')
    B(C, S_, 1, 'sol', 'Dùng một AtomicFile và một Mutex trong cùng một lớp (một instance cho cả app). saveConfig khóa Mutex, chuyển sang Dispatchers.IO, startWrite, ghi, finishWrite, failWrite khi lỗi. loadConfig đọc readFully, bắt FileNotFoundException và lỗi parse để trả mặc định.',
      'Use one AtomicFile and one Mutex inside a single class (one instance for the whole app). saveConfig locks the Mutex, switches to Dispatchers.IO, calls startWrite, writes, finishWrite, and failWrite on error. loadConfig calls readFully and catches FileNotFoundException and parse errors to return the default.')
    B(C, S_, 1, 'solkt', 'class ConfigStore(dir: File) {\n    private val file = AtomicFile(File(dir, "config.json"))\n    private val lock = Mutex()\n\n    suspend fun save(c: Config) = lock.withLock {\n        withContext(Dispatchers.IO) {\n            val out = file.startWrite()\n            try { out.write(Json.encodeToString(c).toByteArray()); file.finishWrite(out) }\n            catch (e: IOException) { file.failWrite(out); throw e }\n        }\n    }\n\n    suspend fun load(): Config = withContext(Dispatchers.IO) {\n        try { Json.decodeFromString(file.readFully().decodeToString()) }\n        catch (e: FileNotFoundException) { Config() }\n        catch (e: SerializationException) { Config() }\n    }\n}')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Vì sao ghi thẳng vào draft.txt có thể làm mất cả bản cũ lẫn bản mới?', 'Why can writing straight into draft.txt lose both the old and the new version?')
    B(C, S_, 1, 'ans', 'Mở stream cắt bản cũ về 0 byte; nếu tiến trình chết trước khi ghi xong, bản mới cũng chỉ có một phần.', 'Opening the stream truncates the old version to 0 bytes; if the process dies before the write finishes, the new version is only partial too.')
    B(C, S_, 2, 'ask', 'Sau một cú kill giữa lúc ghi qua AtomicFile, người dùng mất gì?', 'After a kill in the middle of an AtomicFile write, what does the user lose?')
    B(C, S_, 2, 'ans', 'Chỉ lần sửa đang ghi. File gốc chưa bị đụng tới vì việc đổi tên chỉ xảy ra trong finishWrite.', 'Only the edit being written. The original file was never touched, because the rename only happens in finishWrite.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Mở FileOutputStream(file) không ở chế độ nối thêm làm gì với nội dung cũ?', 'What does opening FileOutputStream(file) without append mode do to the old contents?', 'Cắt về 0 byte ngay khi mở.', 'Truncates them to 0 bytes on open.', 'Bản cũ mất trước khi ghi byte đầu tiên.', 'The old version is gone before the first byte is written.'),
        ('q2', 'AtomicFile đổi tên file .new đè lên file gốc ở hàm nào?', 'In which function does AtomicFile rename the .new file over the original?', 'finishWrite.', 'finishWrite.', 'finishWrite đóng, sync rồi đổi tên; failWrite xóa file .new.', 'finishWrite closes, syncs, then renames; failWrite deletes the .new file.'),
        ('q3', 'Khi nào hệ thống có thể xóa file trong cacheDir?', 'When may the system delete files in cacheDir?', 'Khi máy thiếu bộ nhớ trong.', 'When the device is low on internal storage.', 'Không báo cho app; phải kiểm file còn trước khi đọc.', 'The app is not told; check the file exists before reading it.'),
        ('q4', 'AtomicFile có ngăn hai luồng cùng ghi một file không?', 'Does AtomicFile stop two threads writing the same file?', 'Không; nó không khóa file.', 'No; it does not lock the file.', 'Phải tự loại trừ, ví dụ bằng Mutex.', 'You must exclude them yourself, for example with a Mutex.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
