# Lưu dữ liệu · H2: file riêng của app (Phần 1)
# Nguồn: developer.android.com App-specific storage, AtomicFile (androidx.core) (đọc 2026-11-24); rename(2) man7.org.
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'h2': ['hook', 'dirs', 'atomic', 'cache', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.file', 'Lưu dữ liệu · ghi file an toàn và file trong cache', 'Saving data · writing files safely, and files in the cache')
    m = lambda k, vi, en=None: a('m.file.' + k, vi, en)
    m('title', 'Ghi file khi tiến trình có thể chết bất cứ lúc nào', 'Writing a file when the process can die at any moment')
    m('overview', 'Bản nháp ghi chú của Hẹn Khám được lưu vào filesDir theo hai cách: ghi thẳng vào draft.txt, hoặc ghi qua AtomicFile. Ở giữa lúc ghi, tiến trình bị giết. Cách thứ ba theo dõi một file PDF trong cache qua một lần máy thiếu chỗ.',
      'ClinicBook\'s draft note is saved to filesDir two ways: written straight into draft.txt, or written through AtomicFile. Halfway through the write, the process is killed. A third case follows a PDF in the cache through a low-storage event.')
    m('wrapup', 'Mở FileOutputStream là cắt file về 0 byte ngay, nên một cú kill giữa chừng để lại file dở dang. AtomicFile ghi sang file .new, sync rồi đổi tên đè lên: lúc nào trên đĩa cũng có một bản trọn vẹn, cùng lắm mất lần sửa đang ghi. Còn cache thì không phải chỗ lưu bền: hệ thống được xóa nó, nên luôn kiểm file còn trước khi đọc.',
      'Opening a FileOutputStream truncates the file to 0 bytes at once, so a kill halfway leaves a half-written file. AtomicFile writes to a .new file, syncs, then renames it over: there is always one complete version on disk, and at worst you lose the edit being written. The cache is not durable storage: the system may delete it, so always check a file exists before reading it.')
    m('simp.1', 'Bốn bước là bốn thời điểm chọn lọc; ghi thật có thể nhanh hơn một lần kill rất nhiều. Cú kill đại diện cho mọi lần tiến trình chết giữa chừng: hệ thống thu hồi bộ nhớ, app crash, máy sập nguồn.',
      'The four steps are four chosen moments; a real write may be far quicker than any kill. The kill stands for every way a process can die mid-write: the system reclaiming memory, a crash, a power loss.')
    m('simp.2', 'Hành vi của AtomicFile theo trang tham chiếu androidx.core; tính nguyên tử của đổi tên theo rename(2) trên Linux. Site không chạy app thật.', 'AtomicFile\'s behaviour follows the androidx.core reference page; the atomic rename follows rename(2) on Linux. The site does not run a real app.')
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
    a(C + '.essence', 'filesDir giữ file tới khi gỡ app; cacheDir dành cho thứ lấy lại được, vì hệ thống có thể xóa nó khi thiếu chỗ. Cả hai không cần quyền.\nMở FileOutputStream là cắt file cũ về 0 byte; tiến trình chết giữa lúc ghi thì để lại file dở dang.\nAtomicFile ghi sang file .new, sync rồi đổi tên đè lên file gốc, nên trên đĩa lúc nào cũng có một bản trọn vẹn.',
      'filesDir keeps files until uninstall; cacheDir is for things you can get back, because the system may delete it when space runs low. Neither needs a permission.\nOpening a FileOutputStream truncates the old file to 0 bytes; if the process dies mid-write, a half-written file is left behind.\nAtomicFile writes to a .new file, syncs it, then renames it over the original, so there is always one complete version on disk.')
    a(C + '.goal.g1', 'Đã thấy cú kill giữa lúc ghi', 'Saw the mid-write kill')
    a(C + '.goal.g2', 'Đã mở lại file sau cú kill', 'Reopened the file after the kill')
    a(C + '.sim.storage.file', 'ghi file khi tiến trình có thể chết', 'writing a file when the process may die')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Hàm lưu bản nháp mở FileOutputStream(draft.txt) rồi ghi 40 KB. Tiến trình bị giết khi mới ghi được 20 KB. Lần sau mở app, draft.txt chứa gì: bản nháp cũ, bản nháp mới, hay thứ khác?',
      'The save function opens FileOutputStream(draft.txt) and writes 40 KB. The process is killed after 20 KB. Next time the app opens, what does draft.txt hold: the old draft, the new draft, or something else?')
    B(C, S_, 1, 'ans', 'Thứ khác: 20 KB đầu của bản mới. Bản cũ đã mất ngay lúc mở stream, vì FileOutputStream cắt file về 0 byte khi mở. Mô phỏng ngay dưới so cách này với AtomicFile.',
      'Something else: the first 20 KB of the new draft. The old version was lost the moment the stream opened, because FileOutputStream truncates the file to 0 bytes on open. The simulation just below compares this with AtomicFile.')

    S_ = 'dirs'
    a(C + '.sec.%s.title' % S_, 'Thư mục riêng của app', 'The app\'s own directories')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Bộ nhớ trong có hai thư mục chính: filesDir cho file lâu dài và cacheDir cho file tạm. Cả hai không cần quyền, app khác không truy cập được, được mã hóa từ Android 10 và bị xóa khi gỡ app. Bản ngoài tương ứng là getExternalFilesDir() và externalCacheDir: lớn hơn, không cần quyền từ Android 4.4, nhưng không phải lúc nào cũng truy cập được, nên dữ liệu app cần để chạy phải ở bộ nhớ trong. [[src:ax-app-specific]]',
      'Internal storage has two main directories: filesDir for lasting files and cacheDir for temporary ones. Neither needs a permission, other apps cannot access them, they are encrypted from Android 10, and they are removed on uninstall. The external counterparts are getExternalFilesDir() and externalCacheDir: larger, permission-free from Android 4.4, but not always accessible, so data the app needs to run must be internal. [[src:ax-app-specific]]')
    B(C, S_, 2, 'kt', 'File(context.filesDir, "draft.txt").writeText(text)          // lâu dài, riêng tư\nFile.createTempFile("result", ".pdf", context.cacheDir)       // tạm thời\ncontext.openFileOutput("log.txt", Context.MODE_PRIVATE)      // API cũ hơn, cũng vào filesDir\ncontext.getExternalFilesDir(Environment.DIRECTORY_PICTURES)  // ngoài, có thể null nếu không gắn',
      'File(context.filesDir, "draft.txt").writeText(text)          // lasting, private\nFile.createTempFile("result", ".pdf", context.cacheDir)       // temporary\ncontext.openFileOutput("log.txt", Context.MODE_PRIVATE)      // older API, also into filesDir\ncontext.getExternalFilesDir(Environment.DIRECTORY_PICTURES)  // external, may be null if not mounted')
    B(C, S_, 3, 'note', 'Từ Android 7.0, openFileOutput với chế độ khác MODE_PRIVATE ném SecurityException. Muốn chia sẻ một file nội bộ cho app khác thì dùng FileProvider với quyền URI tạm thời, không mở quyền của file. [[src:ax-app-specific]]',
      'From Android 7.0, openFileOutput with any mode other than MODE_PRIVATE throws a SecurityException. To share an internal file with another app, use FileProvider with a temporary URI permission instead of opening up the file\'s permissions. [[src:ax-app-specific]]')
    B(C, S_, 3, 'kind', 'android')

    S_ = 'atomic'
    a(C + '.sec.%s.title' % S_, 'Ghi để không bao giờ có file dở dang', 'Writing so there is never a half-written file')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Ghi thẳng có hai điểm yếu nối nhau: mở stream là cắt file cũ, và ghi cần thời gian. Ở giữa, trên đĩa không có bản nào trọn vẹn. Cách sửa là không bao giờ ghi đè lên chính file đang dùng: ghi bản mới sang file khác, đẩy xuống đĩa, rồi đổi tên đè lên trong một bước.',
      'Writing in place has two weaknesses back to back: opening the stream truncates the old file, and writing takes time. In between, no complete version exists on disk. The fix is never to overwrite the file in use: write the new version to another file, push it to disk, then rename it over in one step.')
    B(C, S_, 2, 'p', 'AtomicFile (androidx.core, từ 1.1.0) làm đúng việc đó. startWrite mở "<tên>.new"; finishWrite đóng stream, sync xuống đĩa rồi đổi tên đè lên file gốc; failWrite đóng và xóa file .new. Đổi tên đè lên một tên đã có là nguyên tử trên Linux: người đọc thấy bản cũ hoặc bản mới, không có lúc nào file biến mất. [[src:ax-atomicfile]] [[src:man-rename]]',
      'AtomicFile (androidx.core, since 1.1.0) does exactly that. startWrite opens "<name>.new"; finishWrite closes the stream, syncs it to disk and renames it over the original; failWrite closes and deletes the .new file. Renaming over an existing name is atomic on Linux: a reader sees the old version or the new one, and the file is never missing. [[src:ax-atomicfile]] [[src:man-rename]]')
    B(C, S_, 3, 'kt', 'val file = AtomicFile(File(filesDir, "draft.txt"))\nval out = file.startWrite()            // không gọi out.close() tự tay\ntry {\n    out.write(text.toByteArray())\n    file.finishWrite(out)              // close + sync + rename\n} catch (e: IOException) {\n    file.failWrite(out)                // xóa draft.txt.new, bản cũ còn nguyên\n    throw e\n}',
      'val file = AtomicFile(File(filesDir, "draft.txt"))\nval out = file.startWrite()            // do not call out.close() yourself\ntry {\n    out.write(text.toByteArray())\n    file.finishWrite(out)              // close + sync + rename\n} catch (e: IOException) {\n    file.failWrite(out)                // deletes draft.txt.new, the old one is intact\n    throw e\n}')
    B(C, S_, 4, 'note', 'AtomicFile không khóa file. Hai luồng cùng gọi startWrite trên một file thì lần ghi của luồng đầu không còn an toàn hay bị mất. Hãy để một nơi duy nhất ghi file đó, ví dụ một repository chạy trên một coroutine dispatcher giới hạn một luồng hay giữ một Mutex. [[src:ax-atomicfile]]',
      'AtomicFile does not lock the file. If two threads call startWrite on the same file, the first thread\'s write is no longer safe or is lost. Let a single place write that file, for example a repository that serialises writes with a Mutex or a single-threaded dispatcher. [[src:ax-atomicfile]]')
    B(C, S_, 4, 'kind', 'pitfall')

    S_ = 'cache'
    a(C + '.sec.%s.title' % S_, 'Cache không phải chỗ lưu bền', 'The cache is not durable storage')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Khi máy thiếu bộ nhớ trong, Android có thể xóa file trong cacheDir để lấy lại chỗ, sớm hơn nhiều so với lúc gỡ app, và không báo cho app. Vì vậy trang App-specific storage dặn hai điều: kiểm file cache còn trước khi đọc, và đừng trông vào hệ thống để dọn cache cho mình; tự xóa file không cần nữa bằng File.delete() hay deleteFile(). [[src:ax-app-specific]]',
      'When the device is low on internal storage, Android may delete files in cacheDir to reclaim space, much sooner than uninstall, and without telling the app. So the App-specific storage page says two things: check a cache file exists before reading it, and do not rely on the system to clean up your cache; delete files you no longer need with File.delete() or deleteFile(). [[src:ax-app-specific]]')
    B(C, S_, 2, 'p', 'Muốn biết nên giữ cache lớn tới đâu, StorageManager.getCacheQuotaBytes() cho hạn mức gợi ý của app. Trước khi ghi một file lớn, getAllocatableBytes() và allocateBytes() cho biết và giữ trước chỗ trống; con số này có thể lớn hơn chỗ trống hiện có vì hệ thống tính cả cache của app khác mà nó có thể xóa. [[src:ax-app-specific]]',
      'To know how large your cache should grow, StorageManager.getCacheQuotaBytes() gives the app\'s suggested quota. Before writing a large file, getAllocatableBytes() and allocateBytes() tell you how much space you can get and reserve it; that number can exceed current free space because the system counts other apps\' caches it can delete. [[src:ax-app-specific]]')
    B(C, S_, 3, 'note', 'Thứ người dùng tạo ra (bản nháp, ảnh chụp, lịch đặt lúc mất mạng) không bao giờ để trong cache. Câu hỏi để kiểm: "nếu file này biến mất ngay bây giờ, có lấy lại được không?"',
      'Things the user creates (drafts, photos, appointments booked offline) never go in the cache. The test question: "if this file vanished right now, could I get it back?"')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Vài người dùng báo app crash ngay lúc mở, gỡ ra cài lại mới hết. Log có JsonDecodeException: Unexpected end of input.', 'A few users report the app crashing on launch until they reinstall. The log shows JsonDecodeException: Unexpected end of input.')
    B(C, S_, 1, 'cause', 'File cấu hình JSON được ghi thẳng bằng writeText. Một lần tiến trình bị giết giữa lúc ghi để lại file cụt; mỗi lần mở app sau đó parse file cụt và crash.', 'The JSON config file is written in place with writeText. One kill mid-write left a truncated file; every launch since parses it and crashes.')
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

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Thư mục, quyền, mã hóa và hành vi của cache theo trang App-specific storage; AtomicFile theo trang tham chiếu androidx.core; cả hai đọc ngày 2026-11-24. Tính nguyên tử của đổi tên theo rename(2) trên Linux, nền của Android. Chương không bàn chuyện đổi tên giữa hai hệ thống file khác nhau (không nguyên tử), cũng không bàn việc đĩa có thể sắp xếp lại thứ tự ghi; AtomicFile lo phần sync trước khi đổi tên. DataStore và Room tự lo việc ghi an toàn cho file của chúng (chương H3, H4).',
      'Directories, permissions, encryption and cache behaviour follow the App-specific storage page; AtomicFile follows the androidx.core reference page; both read on 2026-11-24. Atomic rename follows rename(2) on Linux, which Android is built on. The chapter does not cover renaming across two different file systems (not atomic), nor disks reordering writes; AtomicFile handles the sync before the rename. DataStore and Room handle safe writes of their own files themselves (chapters H3, H4).')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Mở FileOutputStream(file) không ở chế độ nối thêm làm gì với nội dung cũ?', 'What does opening FileOutputStream(file) without append mode do to the old contents?', 'Cắt về 0 byte ngay khi mở.', 'Truncates them to 0 bytes on open.', 'Bản cũ mất trước khi ghi byte đầu tiên.', 'The old version is gone before the first byte is written.'),
        ('q2', 'AtomicFile đổi tên file .new đè lên file gốc ở hàm nào?', 'In which function does AtomicFile rename the .new file over the original?', 'finishWrite.', 'finishWrite.', 'finishWrite đóng, sync rồi đổi tên; failWrite xóa file .new.', 'finishWrite closes, syncs, then renames; failWrite deletes the .new file.'),
        ('q3', 'Khi nào hệ thống có thể xóa file trong cacheDir?', 'When may the system delete files in cacheDir?', 'Khi máy thiếu bộ nhớ trong.', 'When the device is low on internal storage.', 'Không báo cho app; phải kiểm file còn trước khi đọc.', 'The app is not told; check the file exists before reading it.'),
        ('q4', 'AtomicFile có ngăn hai luồng cùng ghi một file không?', 'Does AtomicFile stop two threads writing the same file?', 'Không; nó không khóa file.', 'No; it does not lock the file.', 'Phải tự loại trừ, ví dụ bằng Mutex.', 'You must exclude them yourself, for example with a Mutex.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
