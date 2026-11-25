# Lưu dữ liệu · H8: shared storage và MediaStore (Phần 2)
# Nguồn: developer.android.com Access media files from shared storage, Photo picker, Data and file storage overview (đọc 2026-11-24).
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'h8': ['hook', 'scoped', 'write', 'read', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.media', 'Lưu dữ liệu · ảnh hồ sơ qua bốn đời Android', 'Saving data · a profile photo across four Android versions')
    m = lambda k, vi, en=None: a('m.media.' + k, vi, en)
    m('title', 'Lưu và chọn ảnh hồ sơ qua bốn đời Android', 'Saving and picking a profile photo across four Android versions')
    m('overview', 'Hẹn Khám cần lưu ảnh hồ sơ người dùng chụp vào Thư viện ảnh, và cho người dùng chọn một ảnh có sẵn. Bốn cách: ghi thẳng vào thư mục Pictures bằng đường dẫn tệp; thêm qua MediaStore; đọc toàn bộ ảnh trong máy để tự làm màn chọn; dùng photo picker của hệ thống. Mỗi cách được thử trên Android 9, 10, 11–12 và 13 trở lên.',
      'ClinicBook needs to save the profile photo the user takes into their gallery, and let them pick an existing photo. Four ways: write straight into Pictures with a file path; add it through MediaStore; read every photo on the device to build its own chooser; use the system photo picker. Each is tried on Android 9, 10, 11–12 and 13 and up.')
    m('wrapup', 'Từ Android 10, bộ nhớ chung chia theo app (scoped storage): app thêm và sửa media của chính nó qua MediaStore mà không cần quyền, còn đường dẫn tệp kiểu cũ hỏng ở Android 10 và chỉ chạy lại từ Android 11. Đọc ảnh của app khác cần quyền, và từ Android 13 quyền đó bị chính sách Play giới hạn. Muốn người dùng chọn một ảnh thì dùng photo picker: không cần quyền ở mọi phiên bản.',
      'From Android 10, shared storage is partitioned by app (scoped storage): an app adds and edits its own media through MediaStore with no permission, while old-style file paths break on Android 10 and only work again from Android 11. Reading other apps\' photos needs a permission, and from Android 13 that permission is limited by Play policy. To let the user choose one photo, use the photo picker: no permission on any version.')
    m('simp.1', 'Bốn hàng gom phiên bản theo các mốc tài liệu nêu (9, 10, 11, 13); Android 12 xếp chung với 11. App giả định target SDK mới nhất.', 'The four rows group versions by the milestones the docs mention (9, 10, 11, 13); Android 12 sits with 11. The app is assumed to target the latest SDK.')
    m('simp.2', 'Quyền và hành vi theo trang Access media files from shared storage và Photo picker đọc ngày 2026-11-24. Site không chạy app trên máy thật.', 'Permissions and behaviour follow the Access media files from shared storage and Photo picker pages as read on 2026-11-24. The site does not run the app on real devices.')
    m('ctl.hint', 'Đổi cách rồi đi qua bốn đời Android; cột đang chọn mở dần trong ma trận.', 'Switch the approach and walk through four Android versions; the chosen column fills in step by step.')
    m('ctl.case', 'Cách', 'Approach')
    for k, vi, en in [('path', 'ghi bằng đường dẫn tệp', 'write with a file path'), ('mediastore', 'thêm qua MediaStore', 'add through MediaStore'), ('read', 'đọc mọi ảnh để tự làm màn chọn', 'read every photo for a custom chooser'), ('picker', 'photo picker của hệ thống', 'the system photo picker')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'App, API lưu trữ, bộ nhớ chung', 'App, storage API, shared storage')
    m('diagramDesc', 'App đi qua một API (đường dẫn tệp, MediaStore hay picker) để tới bộ nhớ chung', 'The app goes through an API (file path, MediaStore or picker) to reach shared storage')
    for k, vi, en in [('app', 'App Hẹn Khám', 'ClinicBook app'), ('api', 'API dùng (File, MediaStore, picker)', 'API used (File, MediaStore, picker)'), ('store', 'Bộ nhớ chung (Pictures/)', 'Shared storage (Pictures/)')]:
        m('n.' + k, vi, en)
    m('met.ver', 'Phiên bản Android', 'Android version'); m('met.res', 'Kết quả', 'Result')
    for k, vi, en in [('a9', 'Android 9 (API 28)', 'Android 9 (API level 28)'), ('a10', 'Android 10 (API 29)', 'Android 10 (API level 29)'), ('a11', 'Android 11–12 (API 30–32)', 'Android 11–12 (API levels 30–32)'), ('a13', 'Android 13+ (API 33+)', 'Android 13+ (API level 33+)')]:
        m('row.' + k, vi, en)
    for k, vi, en in [('ok', 'chạy, không cần quyền', 'works, no permission'), ('perm', 'chạy nếu được cấp quyền', 'works if granted a permission'),
                      ('legacy', 'hỏng, trừ khi tạm thoát scoped storage', 'fails unless scoped storage is opted out'), ('slow', 'chạy với file của chính app, có thể chậm hơn', 'works for the app\'s own files, may be slower'),
                      ('restricted', 'cần READ_MEDIA_IMAGES, bị Play giới hạn', 'needs READ_MEDIA_IMAGES, limited by Play')]:
        m('cell.' + k, vi, en)
    a('cap.media', 'App đi qua một API để tới bộ nhớ chung. Khối viền đỏ là API bị chặn ở phiên bản này; viền cam là API chạy nhưng cần quyền hay có giới hạn.', 'The app goes through an API to reach shared storage. A red outline marks an API blocked on this version; an orange one marks an API that works but needs a permission or has limits.')
    S = [
        ('path', 's1', 'Android 9: ghi vào Pictures sau khi xin quyền', 'Android 9: write into Pictures after asking for permission',
         'Cách cũ: getExternalStoragePublicDirectory rồi FileOutputStream. Chạy được nếu người dùng cấp WRITE_EXTERNAL_STORAGE lúc chạy.', 'The old way: getExternalStoragePublicDirectory, then a FileOutputStream. Works if the user grants WRITE_EXTERNAL_STORAGE at runtime.'),
        ('path', 's2', 'Android 10: đường dẫn tệp bị scoped storage chặn', 'Android 10: scoped storage blocks the file path',
         'App target Android 10 trở lên nằm trong scoped storage; Android 10 chưa cho dùng File trên bộ nhớ chung. Mở file báo lỗi, trừ khi app tạm thoát bằng requestLegacyExternalStorage.', 'Apps targeting Android 10 or higher get scoped storage; Android 10 does not yet allow File on shared storage. Opening the file fails, unless the app temporarily opts out with requestLegacyExternalStorage.'),
        ('path', 's3', 'Android 11–12: File chạy lại với file của chính app', 'Android 11–12: File works again for the app\'s own files',
         'Từ Android 11, File và fopen dùng được trên bộ nhớ chung với media của chính app, nhưng đọc ghi ngẫu nhiên có thể chậm gấp đôi MediaStore. WRITE_EXTERNAL_STORAGE không còn tác dụng.', 'From Android 11, File and fopen work on shared storage for the app\'s own media, but random reads and writes can be up to twice as slow as MediaStore. WRITE_EXTERNAL_STORAGE no longer has any effect.'),
        ('path', 's4', 'Android 13+: như Android 11', 'Android 13+: same as Android 11',
         'Không đổi so với Android 11. Đường dẫn tệp vẫn là đường vòng: một lỗ hổng ở Android 10 và chậm hơn ở các bản sau.', 'No change from Android 11. The file path is still a detour: a hole on Android 10 and slower on later versions.'),
        ('mediastore', 's1', 'Android 9: MediaStore cần quyền ghi', 'Android 9: MediaStore needs the write permission',
         'Trước scoped storage, sửa bộ nhớ chung theo cách nào cũng cần WRITE_EXTERNAL_STORAGE. Trang khuyên khai báo nó với android:maxSdkVersion="29".', 'Before scoped storage, modifying shared storage in any way needs WRITE_EXTERNAL_STORAGE. The page recommends declaring it with android:maxSdkVersion="29".'),
        ('mediastore', 's2', 'Android 10: thêm ảnh của chính app, không cần quyền', 'Android 10: add the app\'s own photo, no permission',
         'insert vào bộ sưu tập Images với IS_PENDING = 1, ghi xong đặt lại 0. Hệ thống ghi nhận ảnh thuộc về app nên không cần quyền.', 'insert into the Images collection with IS_PENDING = 1, set it back to 0 when done. The system attributes the photo to the app, so no permission is needed.'),
        ('mediastore', 's3', 'Android 11–12: vẫn chạy, không cần quyền', 'Android 11–12: still works, no permission',
         'Cùng mã như Android 10. Ảnh hiện trong Thư viện ảnh và còn đó sau khi gỡ app.', 'The same code as Android 10. The photo shows in the gallery and stays after uninstall.'),
        ('mediastore', 's4', 'Android 13+: vẫn chạy, không cần quyền', 'Android 13+: still works, no permission',
         'Không đổi. Đây là cách ổn định nhất để lưu ảnh người dùng muốn giữ.', 'Unchanged. This is the most stable way to save photos the user wants to keep.'),
        ('read', 's1', 'Android 9: đọc mọi ảnh cần READ_EXTERNAL_STORAGE', 'Android 9: reading every photo needs READ_EXTERNAL_STORAGE',
         'Màn chọn ảnh tự làm query toàn bộ bộ sưu tập Images; cần quyền đọc bộ nhớ ngoài.', 'A home-made chooser queries the whole Images collection; it needs the external storage read permission.'),
        ('read', 's2', 'Android 10: ảnh của app khác vẫn cần quyền đọc', 'Android 10: other apps\' photos still need the read permission',
         'Scoped storage không cho thấy ảnh của app khác nếu không có quyền. Người dùng phải đồng ý cho app xem cả thư viện.', 'Scoped storage hides other apps\' photos without a permission. The user must agree to let the app see the whole library.'),
        ('read', 's3', 'Android 11–12: vẫn cần quyền đọc', 'Android 11–12: still needs the read permission',
         'Không đổi. Để chọn một ảnh, app vẫn đòi quyền xem mọi ảnh.', 'No change. To pick one photo, the app still asks to see every photo.'),
        ('read', 's4', 'Android 13+: READ_MEDIA_IMAGES, bị Play giới hạn', 'Android 13+: READ_MEDIA_IMAGES, limited by Play',
         'Quyền đọc tách thành READ_MEDIA_IMAGES, READ_MEDIA_VIDEO, READ_MEDIA_AUDIO. Chính sách Google Play chỉ cho dùng hai quyền ảnh và video trong một số trường hợp; trang khuyên photo picker.', 'The read permission splits into READ_MEDIA_IMAGES, READ_MEDIA_VIDEO and READ_MEDIA_AUDIO. Google Play policy allows the image and video ones only for certain use cases; the page recommends the photo picker.'),
        ('picker', 's1', 'Android 9: picker qua Google Play services', 'Android 9: the picker through Google Play services',
         'Photo picker được backport qua Google Play services cho Android 4.4 tới 10. App nhận URI của đúng ảnh người dùng chọn, không cần quyền.', 'The photo picker is backported through Google Play services to Android 4.4 through 10. The app receives the URI of exactly the photo the user picked, with no permission.'),
        ('picker', 's2', 'Android 10: vẫn chạy, không cần quyền', 'Android 10: still works, no permission',
         'Cùng mã. Nếu máy không có picker, thư viện tự dùng ACTION_OPEN_DOCUMENT.', 'The same code. If the device has no picker, the library falls back to ACTION_OPEN_DOCUMENT.'),
        ('picker', 's3', 'Android 11–12: picker có sẵn trong hệ thống', 'Android 11–12: the picker is built into the system',
         'Từ Android 11, picker có sẵn và được cập nhật qua Google System Updates.', 'From Android 11 the picker is built in and updated through Google System Updates.'),
        ('picker', 's4', 'Android 13+: vẫn không cần quyền', 'Android 13+: still no permission',
         'Không cần READ_MEDIA_IMAGES, không vướng chính sách Play. Muốn giữ quyền đọc ảnh qua lần khởi động lại thì gọi takePersistableUriPermission.', 'No READ_MEDIA_IMAGES, no Play policy hurdle. To keep read access across restarts, call takePersistableUriPermission.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    co = [
        ('try', 'Thử cả bốn cách; so cột của chúng trong ma trận ở bước cuối.', 'Try all four approaches; compare their columns in the matrix at the last step.'),
        ('path.s2', 'Tài liệu Android nói: ở Android 10, đặt requestLegacyExternalStorage = true để tạm thoát scoped storage; đó là lối thoát tạm, không phải cách sửa. [[src:ax-shared-media]]', 'The Android docs say: on Android 10, set requestLegacyExternalStorage = true to temporarily opt out of scoped storage; a stopgap, not a fix. [[src:ax-shared-media]]'),
        ('path.s3', 'Tài liệu Android nói: từ Android 11 dùng được File và fopen trên bộ nhớ chung; đọc ghi ngẫu nhiên có thể chậm tới gấp đôi. [[src:ax-shared-media]]', 'The Android docs say: from Android 11, File and fopen work on shared storage; random reads and writes can be up to twice as slow. [[src:ax-shared-media]]'),
        ('path.s4', 'Tài liệu Android nói: app target API 30 trở lên thì WRITE_EXTERNAL_STORAGE không còn tác dụng gì. [[src:ax-storage-overview]]', 'The Android docs say: for apps targeting API 30 or higher, WRITE_EXTERNAL_STORAGE has no effect. [[src:ax-storage-overview]]'),
        ('mediastore.s2', 'Tài liệu Android nói: từ Android 10, không cần quyền lưu trữ để truy cập và sửa media do app sở hữu. IS_PENDING = 1 giữ ảnh ẩn với app khác tới khi ghi xong. [[src:ax-shared-media]]', 'The Android docs say: from Android 10, no storage permission is needed to access and modify media your app owns. IS_PENDING = 1 keeps the item hidden from other apps until the write finishes. [[src:ax-shared-media]]'),
        ('mediastore.s3', 'Ảnh trong bộ nhớ chung không bị xóa khi gỡ app (bảng so sánh của trang tổng quan). [[src:ax-storage-overview]]', 'Photos in shared storage are not removed on uninstall (the overview page\'s comparison table). [[src:ax-storage-overview]]'),
        ('mediastore.s4', 'Lưu ý từ trang media: cài lại app thì cần quyền đọc để thấy lại các file app đã tạo trước đó. [[src:ax-shared-media]]', 'A note from the Android docs: after reinstalling, the app needs the read permission to see files it created earlier. [[src:ax-shared-media]]'),
        ('read.s2', 'Scoped storage gán mỗi file cho app đã tạo nó; app khác cần quyền đọc mới thấy. [[src:ax-shared-media]]', 'Scoped storage attributes each file to the app that created it; other apps need a read permission to see it. [[src:ax-shared-media]]'),
        ('read.s3', 'Xin quyền xem cả thư viện chỉ để chọn một ảnh là đòi nhiều hơn cần; người dùng hay từ chối.', 'Asking to see the whole library just to pick one photo asks for more than needed; users often refuse.'),
        ('read.s4', 'Tài liệu Android nói: READ_MEDIA_IMAGES và READ_MEDIA_VIDEO bị chính sách Google Play giới hạn ở một số trường hợp dùng; trang khuyên dùng photo picker. [[src:ax-shared-media]]', 'The Android docs say: READ_MEDIA_IMAGES and READ_MEDIA_VIDEO are restricted to certain use cases by Google Play policy; the page recommends the photo picker. [[src:ax-shared-media]]'),
        ('picker.s2', 'Tài liệu Android nói: không có picker thì thư viện gọi ACTION_OPEN_DOCUMENT, có từ Android 4.4. [[src:ax-photo-picker]]', 'The Android docs say: without a picker the library invokes ACTION_OPEN_DOCUMENT, available since Android 4.4. [[src:ax-photo-picker]]'),
        ('picker.s3', 'Picker có sẵn từ Android 11 qua cập nhật thành phần hệ thống; Android 4.4 tới 10 dùng bản backport qua Google Play services. [[src:ax-photo-picker]]', 'The picker is built in from Android 11 through system component updates; Android 4.4 to 10 use the backport through Google Play services. [[src:ax-photo-picker]]'),
        ('picker.s4', 'takePersistableUriPermission giữ quyền đọc URI qua lần khởi động lại; trang nêu giới hạn 5.000 lượt cấp. [[src:ax-photo-picker]]', 'takePersistableUriPermission keeps read access to the URI across restarts; the page mentions a limit of 5,000 grants. [[src:ax-photo-picker]]')]
    for k, vi, en in co:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.md', 'Ma trận phiên bản', 'Version matrix')
    z('md.cap', 'Hàng là phiên bản Android, cột là cách làm. Cột đang chọn mở dần theo bước; các cột khác hiện mờ để so.', 'Rows are Android versions, columns are approaches. The chosen column fills in step by step; the others are dimmed for comparison.')
    z('md.ver', 'Phiên bản', 'Version')
    for k, vi, en in [('path', 'Đường dẫn tệp', 'File path'), ('mediastore', 'MediaStore', 'MediaStore insert'), ('read', 'Đọc mọi ảnh', 'Read all photos'), ('picker', 'Photo picker', 'Photo picker UI')]:
        z('md.col.' + k, vi, en)
    z('md.legend', 'Ô gạch đỏ: hỏng hay vướng chính sách. Ô đậm: chạy không cần quyền. App giả định target SDK mới nhất.', 'Red hatched: broken or blocked by policy. Bold: works with no permission. The app is assumed to target the latest SDK.')

    C = 'h8'
    a(C + '.title', 'Shared storage và MediaStore', 'Shared storage and MediaStore')
    a(C + '.essence', 'Bộ nhớ chung giữ file người dùng muốn giữ và app khác thấy được; nó còn sau khi gỡ app. Ảnh, video, âm thanh đi qua MediaStore; tài liệu đi qua Storage Access Framework.\nTừ Android 10 (scoped storage), app thêm và sửa media của chính nó qua MediaStore mà không cần quyền; đọc media của app khác thì cần quyền.\nĐể người dùng chọn một ảnh, dùng photo picker: không cần quyền ở mọi phiên bản.',
      'Shared storage holds files the user wants to keep and other apps can see; it outlives an uninstall. Images, video and audio go through MediaStore; documents through the Storage Access Framework.\nFrom Android 10 (scoped storage), an app adds and edits its own media through MediaStore with no permission; reading other apps\' media needs a permission.\nTo let the user choose a photo, use the photo picker: no permission on any version.')
    a(C + '.goal.g1', 'Đã thấy Android 10', 'Saw Android 10')
    a(C + '.goal.g2', 'Đã đi tới Android 13+', 'Reached Android 13+')
    a(C + '.sim.storage.media', 'bốn cách qua bốn đời Android', 'four approaches across four Android versions')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Mã lưu ảnh hồ sơ dùng getExternalStoragePublicDirectory(DIRECTORY_PICTURES) và xin WRITE_EXTERNAL_STORAGE. Nó chạy tốt trên Android 9. App nâng target lên SDK mới nhất. Trên máy Android 10 của người dùng, chuyện gì xảy ra?',
      'The code that saves the profile photo uses getExternalStoragePublicDirectory(DIRECTORY_PICTURES) and asks for WRITE_EXTERNAL_STORAGE. It works on Android 9. The app raises its target to the latest SDK. On a user\'s Android 10 device, what happens?')
    B(C, S_, 1, 'ans', 'Ghi file thất bại. App target Android 10 trở lên nằm trong scoped storage, và Android 10 chưa cho dùng đường dẫn tệp trên bộ nhớ chung; chỉ requestLegacyExternalStorage mới tạm cứu. Từ Android 11, File chạy lại. Cách bền là MediaStore. [[src:ax-shared-media]]',
      'The write fails. Apps targeting Android 10 or higher get scoped storage, and Android 10 does not yet allow file paths on shared storage; only requestLegacyExternalStorage rescues it temporarily. From Android 11, File works again. The lasting fix is MediaStore. [[src:ax-shared-media]]')

    S_ = 'scoped'
    a(C + '.sec.%s.title' % S_, 'Scoped storage qua các phiên bản', 'Scoped storage across versions')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', 'Android 9 trở xuống: bộ nhớ chung là một không gian chung, đọc cần READ_EXTERNAL_STORAGE, sửa cần WRITE_EXTERNAL_STORAGE (khai với android:maxSdkVersion="29"). Từ Android 10, app target Android 10 trở lên có scoped storage mặc định: hệ thống gán mỗi file cho app đã tạo nó, app truy cập file của mình mà không cần quyền, còn file của app khác thì cần quyền đọc. [[src:ax-shared-media]] [[src:ax-storage-overview]]',
      'Android 9 and lower: shared storage is one common space; reading needs READ_EXTERNAL_STORAGE, modifying needs WRITE_EXTERNAL_STORAGE (declared with android:maxSdkVersion="29"). From Android 10, apps targeting Android 10 or higher get scoped storage by default: the system attributes each file to the app that created it, the app reaches its own files with no permission, and other apps\' files need a read permission. [[src:ax-shared-media]] [[src:ax-storage-overview]]')
    B(C, S_, 2, 'p', 'Android 10 là bản chuyển tiếp: requestLegacyExternalStorage = true cho phép tạm thoát scoped storage. Từ Android 11, File và fopen dùng lại được trên bộ nhớ chung với file của chính app (và các file app có quyền), nhưng đọc ghi ngẫu nhiên có thể chậm tới gấp đôi MediaStore. App target API 30 trở lên thì WRITE_EXTERNAL_STORAGE không còn tác dụng. [[src:ax-shared-media]] [[src:ax-storage-overview]]',
      'Android 10 is a transition: requestLegacyExternalStorage = true allows a temporary opt-out of scoped storage. From Android 11, File and fopen work on shared storage again for the app\'s own files (and files it has permission for), but random reads and writes can be up to twice as slow as MediaStore. For apps targeting API 30 or higher, WRITE_EXTERNAL_STORAGE has no effect. [[src:ax-shared-media]] [[src:ax-storage-overview]]')
    B(C, S_, 3, 'note', 'Nhiều hướng dẫn cũ trên mạng vẫn dùng getExternalStoragePublicDirectory và WRITE_EXTERNAL_STORAGE. Hàm đó đã bị đánh dấu deprecated từ Android 10; đọc mã mẫu nhớ để ý năm viết.',
      'Many old tutorials still use getExternalStoragePublicDirectory and WRITE_EXTERNAL_STORAGE. That function has been deprecated since Android 10; when reading sample code, check when it was written.')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'write'
    a(C + '.sec.%s.title' % S_, 'Thêm ảnh qua MediaStore', 'Adding a photo through MediaStore')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'MediaStore chia bộ nhớ chung thành các bộ sưu tập: Images (DCIM/, Pictures/), Video, Audio, và Downloads (từ Android 10). Thêm một mục là gọi ContentResolver.insert với ContentValues, nhận về URI, rồi ghi nội dung qua openOutputStream. Dùng DISPLAY_NAME và RELATIVE_PATH để đặt tên và thư mục, không dùng cột DATA. [[src:ax-shared-media]]',
      'MediaStore splits shared storage into collections: Images (DCIM/, Pictures/), Video, Audio, and Downloads (from Android 10). Adding an item means calling ContentResolver.insert with ContentValues, getting back a URI, then writing the content through openOutputStream. Use DISPLAY_NAME and RELATIVE_PATH to set the name and folder, not the DATA column. [[src:ax-shared-media]]')
    B(C, S_, 2, 'kt', 'val values = contentValuesOf(\n    MediaStore.Images.Media.DISPLAY_NAME to "avatar.jpg",\n    MediaStore.Images.Media.MIME_TYPE to "image/jpeg",\n    MediaStore.Images.Media.RELATIVE_PATH to "Pictures/HenKham",\n    MediaStore.Images.Media.IS_PENDING to 1,          // app khác chưa thấy\n)\nval uri = resolver.insert(MediaStore.Images.Media.getContentUri(MediaStore.VOLUME_EXTERNAL_PRIMARY), values)!!\nresolver.openOutputStream(uri)!!.use { bitmap.compress(Bitmap.CompressFormat.JPEG, 90, it) }\nresolver.update(uri, contentValuesOf(MediaStore.Images.Media.IS_PENDING to 0), null, null)',
      'val values = contentValuesOf(\n    MediaStore.Images.Media.DISPLAY_NAME to "avatar.jpg",\n    MediaStore.Images.Media.MIME_TYPE to "image/jpeg",\n    MediaStore.Images.Media.RELATIVE_PATH to "Pictures/ClinicBook",\n    MediaStore.Images.Media.IS_PENDING to 1,          // other apps cannot see it yet\n)\nval uri = resolver.insert(MediaStore.Images.Media.getContentUri(MediaStore.VOLUME_EXTERNAL_PRIMARY), values)!!\nresolver.openOutputStream(uri)!!.use { bitmap.compress(Bitmap.CompressFormat.JPEG, 90, it) }\nresolver.update(uri, contentValuesOf(MediaStore.Images.Media.IS_PENDING to 0), null, null)')
    B(C, S_, 3, 'p', 'IS_PENDING = 1 giữ mục ẩn với app khác trong lúc ghi, giống tinh thần ghi an toàn ở chương H2: không ai thấy một ảnh ghi dở. Ghi xong đặt lại 0. IS_PENDING và RELATIVE_PATH có từ Android 10; trên Android 9 phải bỏ chúng và cần WRITE_EXTERNAL_STORAGE. Tài liệu (PDF, hóa đơn) muốn lưu vào Download của app khác thấy thì đi qua Storage Access Framework. [[src:ax-shared-media]]',
      'IS_PENDING = 1 keeps the item hidden from other apps while writing, in the same spirit as the safe writes of chapter H2: nobody sees a half-written photo. Set it back to 0 when done. IS_PENDING and RELATIVE_PATH exist from Android 10; on Android 9 drop them and the WRITE_EXTERNAL_STORAGE permission is needed. Documents (PDFs, invoices) that other apps should see in Downloads go through the Storage Access Framework. [[src:ax-shared-media]]')

    S_ = 'read'
    a(C + '.sec.%s.title' % S_, 'Chọn ảnh: photo picker thay cho quyền đọc', 'Picking photos: the photo picker instead of read permissions')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', 'Đọc media của app khác cần quyền: READ_EXTERNAL_STORAGE ở các bản cũ, rồi READ_MEDIA_IMAGES, READ_MEDIA_VIDEO, READ_MEDIA_AUDIO ở các bản mới. Trang media cảnh báo READ_MEDIA_IMAGES và READ_MEDIA_VIDEO bị chính sách Google Play giới hạn ở một số trường hợp dùng, và khuyên dùng photo picker. [[src:ax-shared-media]]',
      'Reading other apps\' media needs a permission: READ_EXTERNAL_STORAGE on older versions, then READ_MEDIA_IMAGES, READ_MEDIA_VIDEO and READ_MEDIA_AUDIO on newer ones. The media page warns that READ_MEDIA_IMAGES and READ_MEDIA_VIDEO are restricted to certain use cases by Google Play policy, and recommends the photo picker. [[src:ax-shared-media]]')
    B(C, S_, 2, 'kt', 'val pick = registerForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri ->\n    if (uri != null) viewModel.setAvatar(uri)\n}\npick.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))',
      'val pick = registerForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri ->\n    if (uri != null) viewModel.setAvatar(uri)\n}\npick.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))')
    B(C, S_, 3, 'p', 'Photo picker (PickVisualMedia, androidx.activity 1.7.0 trở lên) cho người dùng chọn ảnh mà không phải cấp cho app quyền xem cả thư viện. Nó có sẵn từ Android 11 và được backport qua Google Play services cho Android 4.4 tới 10; máy không có thì thư viện dùng ACTION_OPEN_DOCUMENT. URI trả về chỉ đọc được tạm thời; muốn giữ quyền qua lần khởi động lại thì gọi takePersistableUriPermission, hoặc chép ảnh vào filesDir. [[src:ax-photo-picker]]',
      'The photo picker (PickVisualMedia, androidx.activity 1.7.0 or higher) lets the user choose photos without granting the app access to the whole library. It is built in from Android 11 and backported through Google Play services for Android 4.4 to 10; where missing, the library uses ACTION_OPEN_DOCUMENT. The returned URI is readable only temporarily; to keep access across restarts, call takePersistableUriPermission, or copy the photo into filesDir. [[src:ax-photo-picker]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Sau khi nâng target SDK, nút "Lưu ảnh vào máy" báo lỗi trên một nhóm người dùng, chỉ nhóm dùng Android 10.', 'After raising the target SDK, the "Save photo to device" button fails for one group of users, only those on Android 10.')
    B(C, S_, 1, 'cause', 'Mã ghi bằng getExternalStoragePublicDirectory và FileOutputStream. Android 10 với scoped storage không cho đường dẫn tệp trên bộ nhớ chung; Android 11 trở lên cho lại nên lỗi chỉ lộ ở Android 10.', 'The code writes with getExternalStoragePublicDirectory and a FileOutputStream. Android 10 under scoped storage forbids file paths on shared storage; Android 11 and up allow them again, so the bug only shows on Android 10.')
    B(C, S_, 1, 'fix', 'Chuyển sang MediaStore.insert với IS_PENDING; trên Android 9 xin WRITE_EXTERNAL_STORAGE khai maxSdkVersion 28 hay 29.', 'Switch to MediaStore.insert with IS_PENDING; on Android 9, request WRITE_EXTERNAL_STORAGE declared with maxSdkVersion 28 or 29.')
    B(C, S_, 2, 'bug', 'Ảnh đại diện người dùng chọn hiện được lần đầu, nhưng sau khi khởi động lại máy thì thành ô trống.', 'The avatar the user picked shows the first time, but after a reboot it becomes a blank square.')
    B(C, S_, 2, 'cause', 'App lưu URI từ photo picker vào DataStore và đọc lại sau. Quyền đọc URI đó chỉ là tạm thời.', 'The app saved the photo picker\'s URI in DataStore and read it back later. Read access to that URI was only temporary.')
    B(C, S_, 2, 'fix', 'Gọi takePersistableUriPermission với FLAG_GRANT_READ_URI_PERMISSION ngay khi nhận URI, hoặc chép ảnh vào filesDir và lưu đường dẫn của bản chép.', 'Call takePersistableUriPermission with FLAG_GRANT_READ_URI_PERMISSION as soon as the URI arrives, or copy the photo into filesDir and store the copy\'s path.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Màn Hồ sơ của Hẹn Khám có hai nút: "Chọn ảnh đại diện" và "Lưu thẻ khám vào Thư viện ảnh" (một ảnh PNG app tự vẽ). minSdk là 26. Với mỗi nút: chọn API, liệt kê quyền cần khai trong manifest (kèm maxSdkVersion nếu có), và nói ảnh nằm ở đâu sau khi gỡ app.',
      'ClinicBook\'s Profile screen has two buttons: "Choose avatar" and "Save visit card to gallery" (a PNG the app draws). minSdk is 26. For each button: choose the API, list the manifest permissions (with maxSdkVersion where relevant), and say where the image ends up after uninstall.')
    B(C, S_, 1, 'hint', 'Một nút đọc ảnh người dùng chọn, một nút ghi ảnh của chính app. Tra ma trận ở mô phỏng.', 'One button reads a photo the user picks, the other writes the app\'s own image. Look it up in the simulation\'s matrix.')
    B(C, S_, 1, 'sol', '"Chọn ảnh đại diện": photo picker, không cần quyền nào; chép ảnh đã chọn vào filesDir (bị xóa khi gỡ app, đúng ý vì đây là bản riêng của app). "Lưu thẻ khám": MediaStore.insert vào Images với IS_PENDING trên Android 10 trở lên; với Android 8–9 (API 26–28) khai WRITE_EXTERNAL_STORAGE với android:maxSdkVersion="28" và xin lúc chạy. Thẻ khám nằm trong Pictures và còn sau khi gỡ app.',
      '"Choose avatar": the photo picker, no permission at all; copy the chosen photo into filesDir (removed on uninstall, which is right for the app\'s private copy). "Save visit card": MediaStore.insert into Images with IS_PENDING on Android 10 and up; for Android 8–9 (API 26–28) declare WRITE_EXTERNAL_STORAGE with android:maxSdkVersion="28" and request it at runtime. The card lives in Pictures and stays after uninstall.')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Từ Android 10, app thêm ảnh của chính nó qua MediaStore có cần quyền không?', 'From Android 10, does an app need a permission to add its own photo through MediaStore?')
    B(C, S_, 1, 'ans', 'Không. Hệ thống gán ảnh cho app đã tạo nó.', 'No. The system attributes the photo to the app that created it.')
    B(C, S_, 2, 'ask', 'Vì sao nên dùng photo picker thay cho READ_MEDIA_IMAGES?', 'Why use the photo picker instead of READ_MEDIA_IMAGES?')
    B(C, S_, 2, 'ans', 'Picker không cần quyền và chỉ trao đúng ảnh người dùng chọn; READ_MEDIA_IMAGES mở cả thư viện và bị chính sách Play giới hạn.', 'The picker needs no permission and hands over only the photo the user chose; READ_MEDIA_IMAGES opens the whole library and is limited by Play policy.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Quyền, scoped storage, bộ sưu tập, IS_PENDING, RELATIVE_PATH và đường dẫn tệp theo trang Access media files from shared storage; photo picker theo trang Photo picker; tất cả đọc ngày 2026-11-24. Ma trận gom Android 11 và 12, giả định app target SDK mới nhất, và chỉ xét ảnh; video và âm thanh theo cùng quy tắc với quyền riêng. Chương không bàn Storage Access Framework chi tiết, quyền truy cập ảnh một phần của người dùng, ACCESS_MEDIA_LOCATION hay MANAGE_EXTERNAL_STORAGE.',
      'Permissions, scoped storage, collections, IS_PENDING, RELATIVE_PATH and file paths follow the Access media files from shared storage page; the photo picker follows the Photo picker page; all read on 2026-11-24. The matrix groups Android 11 and 12, assumes the app targets the latest SDK, and covers only images; video and audio follow the same rules with their own permissions. The chapter does not detail the Storage Access Framework, partial photo access, ACCESS_MEDIA_LOCATION or MANAGE_EXTERNAL_STORAGE.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Ảnh lưu qua MediaStore vào Pictures có bị xóa khi gỡ app không?', 'Is a photo saved through MediaStore into Pictures removed on uninstall?', 'Không.', 'No.', 'Bộ nhớ chung không bị xóa theo app.', 'Shared storage is not removed with the app.'),
        ('q2', 'IS_PENDING = 1 để làm gì?', 'What is IS_PENDING = 1 for?', 'Giữ mục ẩn với app khác trong lúc đang ghi.', 'It hides the item from other apps while it is being written.', 'Ghi xong đặt lại 0.', 'Set it back to 0 when done.'),
        ('q3', 'Phiên bản nào chặn đường dẫn tệp trên bộ nhớ chung mà chưa cho lại?', 'Which version blocks file paths on shared storage without allowing them back?', 'Android 10.', 'Android 10.', 'Android 11 cho dùng lại File; Android 10 chỉ có requestLegacyExternalStorage.', 'Android 11 allows File again; Android 10 only has requestLegacyExternalStorage.'),
        ('q4', 'Photo picker cần quyền gì?', 'What permission does the photo picker need?', 'Không cần quyền nào.', 'None.', 'Người dùng chọn ảnh; app chỉ nhận URI của ảnh đó.', 'The user picks; the app only receives that photo\'s URI.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
