# Lưu dữ liệu · H9: sao lưu và dữ liệu nhạy cảm (Phần 2)
# Nguồn: developer.android.com Back up user data with Auto Backup (đọc 2026-11-24); DataStore (file nằm trong files/datastore/, được sao lưu mặc định).
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'h9': ['hook', 'what', 'rules', 'sensitive', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.backup', 'Lưu dữ liệu · đổi máy mới và Auto Backup', 'Saving data · moving to a new phone with Auto Backup')
    m = lambda k, vi, en=None: a('m.backup.' + k, vi, en)
    m('title', 'Đổi sang máy mới: thứ gì đi theo, thứ gì không', 'Moving to a new phone: what comes along, what does not')
    m('overview', 'Người dùng Hẹn Khám đổi điện thoại và khôi phục từ bản sao lưu Google. App có cài đặt, bản nháp, database lịch hẹn, một file phiên đăng nhập, một mã cài đặt và PDF trong cache. Ba cấu hình: để mặc định; thêm quy tắc loại trừ file phiên; tắt sao lưu bằng allowBackup="false".',
      'A ClinicBook user switches phones and restores from their Google backup. The app has settings, a draft, an appointments database, a login session file, an install id and a PDF in the cache. Three setups: leave the defaults; add a rule excluding the session file; turn backup off with allowBackup="false".')
    m('wrapup', 'Auto Backup bật sẵn và sao lưu gần như mọi thứ trong bộ nhớ riêng của app, trừ cache và no_backup. Thứ người dùng muốn giữ (cài đặt, lịch hẹn) nên đi theo; thứ gắn với một máy hay một phiên (token đăng nhập, token FCM, mã cài đặt) thì không. Loại trừ đúng những file đó bằng dataExtractionRules, hoặc đặt chúng vào noBackupFilesDir; tắt hẳn sao lưu làm người dùng mất cả phần đáng giữ.',
      'Auto Backup is on by default and backs up almost everything in the app\'s private storage except the cache and no_backup. What the user wants to keep (settings, appointments) should come along; what is tied to one device or one session (login tokens, the FCM token, an install id) should not. Exclude exactly those files with dataExtractionRules, or put them in noBackupFilesDir; switching backup off entirely makes the user lose the parts worth keeping too.')
    m('simp.1', 'Cây thư mục, tên file và nội dung là của site. Bản sao lưu thật chạy khoảng mỗi đêm khi máy rảnh và có Wi-Fi; ở đây gói thành một bước.', 'The directory tree, file names and contents are the site\'s. Real backups run roughly nightly when the device is idle and on Wi-Fi; here it is one step.')
    m('simp.2', 'Hành vi sao lưu và khôi phục theo trang Auto Backup đọc ngày 2026-11-24. Hậu quả của việc khôi phục phiên cũ (đăng xuất, lỗi 401) là tình huống của site.', 'Backup and restore behaviour follows the Auto Backup page as read on 2026-11-24. The consequences of restoring an old session (sign-out, 401 errors) are the site\'s scenario.')
    m('ctl.hint', 'Đổi cấu hình rồi đi lại; nhìn dòng session.preferences_pb trên máy mới.', 'Switch the setup and walk again; watch the session.preferences_pb row on the new phone.')
    m('ctl.case', 'Cấu hình', 'Setup')
    for k, vi, en in [('default', 'mặc định (không quy tắc)', 'defaults (no rules)'), ('rules', 'loại trừ file phiên', 'exclude the session file'), ('off', 'allowBackup="false"', 'allowBackup set to false')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Máy cũ, bản sao lưu trên Google Drive, máy mới', 'Old phone, backup on Google Drive, new phone')
    m('diagramDesc', 'Dữ liệu đi từ máy cũ lên bản sao lưu, rồi từ bản sao lưu xuống máy mới khi cài app', 'Data goes from the old phone to the backup, then from the backup to the new phone when the app installs')
    for k, vi, en in [('old', 'Máy cũ', 'Old phone'), ('cloud', 'Bản sao lưu (Google Drive)', 'Backup (Google Drive)'), ('new', 'Máy mới', 'New phone')]:
        m('n.' + k, vi, en)
    m('met.backed', 'File được sao lưu', 'Files backed up'); m('met.session', 'Phiên đăng nhập', 'Login session'); m('met.out', 'Lần mở đầu trên máy mới', 'First launch on the new phone')
    for k, vi, en in [('old', 'chỉ trên máy cũ', 'only on the old phone'), ('restored', 'phiên cũ bị khôi phục', 'old session restored'), ('absent', 'không có, đăng nhập mới', 'absent, fresh sign-in')]:
        m('sess.' + k, vi, en)
    for k, vi, en in [('none', 'chưa tới', 'not yet'), ('stale', 'phiên cũ hết hạn: lỗi 401, đăng xuất giữa chừng', 'stale session: 401 errors, signed out mid-use'),
                      ('fresh', 'đăng nhập lại; cài đặt và lịch hẹn vẫn còn', 'signs in again; settings and appointments kept'), ('empty', 'như cài mới: mất cài đặt và lịch chưa gửi', 'like a fresh install: settings and unsent appointments lost')]:
        m('out.' + k, vi, en)
    a('cap.backup', 'Máy cũ gửi bản sao lưu lên Google Drive; máy mới nhận lại khi cài app. Khối viền đỏ là chỗ dữ liệu sai hay mất.', 'The old phone uploads a backup to Google Drive; the new phone receives it when the app installs. A red outline marks wrong or lost data.')
    S = [
        ('default', 's1', 'Máy cũ: app có sáu file', 'Old phone: the app has six files',
         'Không có quy tắc sao lưu nào; allowBackup mặc định là true.', 'No backup rules at all; allowBackup defaults to true.'),
        ('default', 's2', 'Sao lưu đêm: mọi thứ trừ cache và no_backup', 'Nightly backup: everything except cache and no_backup',
         'filesDir (gồm cả files/datastore) và databases đều được sao lưu, kể cả session.preferences_pb chứa token đăng nhập và token FCM.', 'filesDir (including files/datastore) and databases are backed up, including session.preferences_pb with the login token and the FCM token.'),
        ('default', 's3', 'Máy mới: khôi phục trước lần mở đầu', 'New phone: restored before the first launch',
         'Cài app xong, hệ thống khôi phục bản sao lưu trước khi người dùng mở được app. Token cũ nằm sẵn trên máy mới.', 'After the app installs, the system restores the backup before the user can open the app. The old tokens are already on the new phone.'),
        ('default', 's4', 'Mở app: phiên cũ, token FCM cũ', 'Open the app: an old session, an old FCM token',
         'App tưởng đã đăng nhập và gọi máy chủ với token cũ (có thể đã hết hạn), nhận 401 rồi đăng xuất giữa chừng. Token FCM cũ thuộc máy kia nên thông báo nhắc lịch không tới.', 'The app thinks it is signed in and calls the server with the old (possibly expired) token, gets 401s and signs out mid-use. The old FCM token belongs to the other phone, so reminders never arrive.'),
        ('rules', 's1', 'Máy cũ: cùng sáu file, thêm quy tắc', 'Old phone: the same six files, plus rules',
         'Manifest trỏ tới data_extraction_rules.xml, loại session.preferences_pb khỏi cả sao lưu đám mây lẫn chuyển máy-sang-máy.', 'The manifest points to data_extraction_rules.xml, excluding session.preferences_pb from both cloud backup and device-to-device transfer.'),
        ('rules', 's2', 'Sao lưu đêm: bỏ file phiên', 'Nightly backup: the session file is skipped',
         'Cài đặt, bản nháp và database được sao lưu; file phiên bị quy tắc loại; cache và no_backup bị loại như mặc định.', 'Settings, the draft and the database are backed up; the session file is excluded by the rule; cache and no_backup are excluded as always.'),
        ('rules', 's3', 'Máy mới: khôi phục phần đáng giữ', 'New phone: the parts worth keeping are restored',
         'Cài đặt, bản nháp và lịch hẹn có mặt; không có token nào.', 'Settings, the draft and the appointments are there; no tokens.'),
        ('rules', 's4', 'Mở app: đăng nhập lại, dữ liệu vẫn còn', 'Open the app: sign in again, data still there',
         'Người dùng đăng nhập một lần; app lấy token mới và đăng ký token FCM mới cho máy này. Chủ đề tối và lịch hẹn vẫn như cũ.', 'The user signs in once; the app gets a new token and registers a new FCM token for this phone. The dark theme and appointments are as before.'),
        ('off', 's1', 'Máy cũ: allowBackup="false"', 'Old phone: allowBackup="false"',
         'Đội phát triển tắt sao lưu "cho an toàn" vì lo token bị khôi phục.', 'The team turned backup off "to be safe", worried about restored tokens.'),
        ('off', 's2', 'Sao lưu đêm: không có gì được gửi', 'Nightly backup: nothing is sent',
         'Cả cài đặt lẫn lịch hẹn chưa gửi lên máy chủ đều không được sao lưu.', 'Neither the settings nor appointments not yet sent to the server are backed up.'),
        ('off', 's3', 'Máy mới: không có gì để khôi phục', 'New phone: nothing to restore',
         'App cài mới hoàn toàn. Lưu ý: trên một số máy Android 12+, allowBackup="false" không chặn chuyển máy-sang-máy.', 'The app installs completely fresh. Note: on some Android 12+ devices, allowBackup="false" does not block device-to-device transfer.'),
        ('off', 's4', 'Mở app: như mới cài', 'Open the app: like a fresh install',
         'Không lỗi 401, nhưng người dùng phải chỉnh lại mọi cài đặt, và lịch đặt lúc mất mạng chưa gửi lên máy chủ thì mất hẳn.', 'No 401s, but the user must redo every setting, and appointments booked offline but not yet sent are gone for good.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cấu hình; so cột "Trên máy mới".', 'Walk all four steps of each setup; compare the "On the new phone" column.'),
        ('default.s2', 'Tài liệu Android nói: mặc định sao lưu SharedPreferences, file trong filesDir, database và getExternalFilesDir; luôn loại cacheDir, codeCacheDir, noBackupFilesDir. File DataStore nằm trong files/datastore nên cũng được sao lưu. [[src:ax-autobackup]] [[src:ax-datastore]]', 'The Android docs say: by default it backs up SharedPreferences, files in filesDir, databases and getExternalFilesDir; it always excludes cacheDir, codeCacheDir and noBackupFilesDir. DataStore files live in files/datastore, so they are backed up too. [[src:ax-autobackup]] [[src:ax-datastore]]'),
        ('default.s3', 'Khôi phục xảy ra khi cài app (từ Play, lúc thiết lập máy, hay adb install), sau khi cài APK và trước khi người dùng mở được app. [[src:ax-autobackup]]', 'Restore happens on app install (from Play, during device setup, or adb install), after the APK installs and before the user can open the app. [[src:ax-autobackup]]'),
        ('default.s4', 'Tài liệu Android nói: file chứa định danh riêng của thiết bị thường bị loại; ví dụ token FCM, khôi phục token cũ có thể làm app chạy sai. [[src:ax-autobackup]]', 'The Android docs say: files with device-specific identifiers are typically excluded; with the FCM token as the example, restoring the old token can make the app misbehave. [[src:ax-autobackup]]'),
        ('rules.s2', 'Android 12+: android:dataExtractionRules trỏ tới file có hai phần cloud-backup và device-transfer; mỗi phần chỉ áp cho kiểu chuyển của nó. [[src:ax-autobackup]]', 'Android 12+: android:dataExtractionRules points to a file with cloud-backup and device-transfer sections; each applies only to its own transfer type. [[src:ax-autobackup]]'),
        ('rules.s3', 'exclude thắng include; nếu có bất kỳ include nào thì chỉ những file được include mới được sao lưu. [[src:ax-autobackup]]', 'exclude wins over include; if any include is present, only the included files are backed up. [[src:ax-autobackup]]'),
        ('rules.s4', 'Tài liệu Android nói: muốn sao lưu thông tin đăng nhập và token xác thực thì đừng để trong SharedPreferences hay file, hãy dùng Block Store. [[src:ax-autobackup]]', 'The Android docs say: to back up user credentials and auth tokens, do not keep them in shared preferences or a file; use Block Store instead. [[src:ax-autobackup]]'),
        ('off.s2', 'allowBackup="false" tắt sao lưu cho cả app; trang gợi ý dùng nó khi trạng thái tạo lại được bằng cách khác, hay dữ liệu nhạy cảm. [[src:ax-autobackup]]', 'allowBackup="false" disables backup for the whole app; the page suggests it when state can be recreated another way, or for sensitive data. [[src:ax-autobackup]]'),
        ('off.s3', 'Tài liệu Android nói: từ Android 12, trên máy của một số hãng, allowBackup="false" tắt sao lưu đám mây nhưng không tắt chuyển máy-sang-máy. [[src:ax-autobackup]]', 'The Android docs say: from Android 12, on some manufacturers\' devices, allowBackup="false" disables cloud backup but not device-to-device transfer. [[src:ax-autobackup]]'),
        ('off.s4', 'Tắt sao lưu chữa được một file sai bằng cách bỏ cả những file đúng. Loại trừ đúng file nhạy cảm là đủ.', 'Turning backup off fixes one wrong file by dropping all the right ones too. Excluding exactly the sensitive file is enough.')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.bk', 'Cây thư mục', 'Directory tree')
    z('bk.cap', 'Cây thư mục riêng của app. Cột giữa: file có được sao lưu không (hiện từ bước 2). Cột phải: file có mặt trên máy mới không (từ bước 3).', 'The app\'s private directory tree. Middle column: whether each file is backed up (from step 2). Right column: whether it is on the new phone (from step 3).')
    for k, vi, en in [('path', 'Đường dẫn', 'Path'), ('backup', 'Sao lưu', 'Backup'), ('newdev', 'Trên máy mới', 'On the new phone')]:
        z('bk.col.' + k, vi, en)
    for k, vi, en in [('files', 'files/', 'files/ (filesDir)'), ('draft', 'draft.txt (bản nháp)', 'draft.txt (draft)'), ('datastore', 'datastore/', 'datastore/ folder'),
                      ('settings', 'settings.preferences_pb (cài đặt)', 'settings.preferences_pb (settings)'), ('session', 'session.preferences_pb (token)', 'session.preferences_pb (tokens)'),
                      ('databases', 'databases/', 'databases/ folder'), ('clinicdb', 'clinic.db (lịch hẹn)', 'clinic.db (appointments)'),
                      ('noBackup', 'no_backup/', 'no_backup/ (noBackupFilesDir)'), ('installId', 'install_id (mã cài đặt)', 'install_id (install id)'),
                      ('cache', 'cache/', 'cache/ (cacheDir)'), ('pdf', 'result-12.pdf', 'result-12.pdf (cached)')]:
        z('bk.n.' + k, vi, en)
    for k, vi, en in [('b', 'được sao lưu', 'backed up'), ('x', 'luôn bị loại', 'always excluded'), ('r', 'loại theo quy tắc', 'excluded by rule'), ('o', 'sao lưu đã tắt', 'backup is off')]:
        z('bk.st.' + k, vi, en)
    for k, vi, en in [('restored', 'được khôi phục', 'restored'), ('fresh', 'tạo mới', 'created fresh'), ('missing', 'không có', 'missing')]:
        z('bk.new.' + k, vi, en)
    z('bk.out', 'Lần mở đầu:', 'First launch:')
    z('bk.legend', 'Ô đỏ ở cột phải: file lẽ ra không nên có (token cũ bị khôi phục) hay lẽ ra phải có (dữ liệu người dùng mất).', 'A red cell in the right column: a file that should not be there (a restored old token) or should be there (lost user data).')

    C = 'h9'
    a(C + '.title', 'Sao lưu và dữ liệu nhạy cảm', 'Backup and sensitive data')
    a(C + '.essence', 'Auto Backup bật sẵn từ Android 6.0: sao lưu SharedPreferences, filesDir (gồm file DataStore), database và getExternalFilesDir lên Google Drive, tối đa 25 MB; luôn loại cacheDir, codeCacheDir, noBackupFilesDir.\nBản sao lưu được khôi phục khi cài app, trước lần mở đầu, nên token đăng nhập và token FCM của máy cũ đi theo nếu không loại trừ.\nLoại đúng file nhạy cảm bằng dataExtractionRules (Android 12+) và fullBackupContent (Android 11 trở xuống), hoặc đặt chúng vào noBackupFilesDir; token đăng nhập muốn đi theo thì dùng Block Store.',
      'Auto Backup is on by default from Android 6.0: it backs up SharedPreferences, filesDir (including DataStore files), databases and getExternalFilesDir to Google Drive, up to 25 MB; it always excludes cacheDir, codeCacheDir and noBackupFilesDir.\nThe backup is restored when the app installs, before the first launch, so the old phone\'s login and FCM tokens come along unless excluded.\nExclude exactly the sensitive files with dataExtractionRules (Android 12+) and fullBackupContent (Android 11 and lower), or keep them in noBackupFilesDir; login tokens that should travel belong in Block Store.')
    a(C + '.goal.g1', 'Đã thấy dữ liệu tới máy mới', 'Saw data reach the new phone')
    a(C + '.goal.g2', 'Đã thấy lần mở đầu trên máy mới', 'Saw the first launch on the new phone')
    a(C + '.sim.storage.backup', 'đổi máy với ba cấu hình sao lưu', 'switching phones with three backup setups')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Hẹn Khám lưu token đăng nhập trong một file DataStore và chưa từng viết quy tắc sao lưu nào. Người dùng đổi máy, khôi phục từ Google. Lần đầu mở app trên máy mới, họ thấy gì?',
      'ClinicBook keeps its login token in a DataStore file and has never written any backup rules. A user switches phones and restores from Google. The first time they open the app on the new phone, what do they see?')
    B(C, S_, 1, 'ans', 'App tưởng vẫn đăng nhập: file DataStore nằm trong filesDir nên đã được sao lưu và khôi phục trước lần mở đầu. Token cũ có thể đã hết hạn, nên lời gọi đầu tiên nhận 401; token FCM cũ thuộc máy kia nên thông báo không tới. Mô phỏng ngay dưới so ba cấu hình. [[src:ax-autobackup]]',
      'The app thinks it is still signed in: the DataStore file lives in filesDir, so it was backed up and restored before the first launch. The old token may have expired, so the first call gets a 401; the old FCM token belongs to the other phone, so notifications never arrive. The simulation just below compares three setups. [[src:ax-autobackup]]')

    S_ = 'what'
    a(C + '.sec.%s.title' % S_, 'Auto Backup sao lưu gì, khi nào', 'What Auto Backup saves, and when')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Auto Backup áp cho app target và chạy trên Android 6.0 trở lên, bật sẵn (allowBackup mặc định là true). Mặc định nó sao lưu SharedPreferences, file trong filesDir và getDir, database và file trong getExternalFilesDir; luôn loại cacheDir, codeCacheDir và noBackupFilesDir, kể cả khi bạn cố include chúng. Mỗi app tối đa 25 MB, lưu trong thư mục riêng trên Google Drive mà người dùng và app khác không đọc được, mã hóa đầu cuối từ Android 9. [[src:ax-autobackup]]',
      'Auto Backup applies to apps targeting and running on Android 6.0 or higher, and is on by default (allowBackup defaults to true). By default it backs up SharedPreferences, files in filesDir and getDir, databases, and files in getExternalFilesDir; it always excludes cacheDir, codeCacheDir and noBackupFilesDir, even if you try to include them. Each app gets up to 25 MB, stored in a private Google Drive folder that neither the user nor other apps can read, end-to-end encrypted from Android 9. [[src:ax-autobackup]]')
    B(C, S_, 2, 'p', 'Sao lưu chạy khi máy bật sao lưu, đã qua ít nhất 24 giờ từ lần trước, máy rảnh và có Wi-Fi; thực tế khoảng mỗi đêm, và chỉ tải lên khi dữ liệu đổi. Khôi phục xảy ra mỗi khi cài app (từ Play, lúc thiết lập máy mới, hay adb install), sau khi cài APK và trước khi người dùng mở được app. [[src:ax-autobackup]]',
      'Backups run when backup is enabled on the device, at least 24 hours have passed, the device is idle and on Wi-Fi; roughly nightly in practice, uploading only if data changed. Restore happens on any app install (from Play, during new-device setup, or adb install), after the APK installs and before the user can open the app. [[src:ax-autobackup]]')
    B(C, S_, 3, 'note', 'DataStore và Room lưu file trong filesDir và databases, nên được sao lưu mặc định cùng mọi thứ khác. Trang DataStore nhắc điều này và trỏ tới data_extraction_rules để cấu hình. [[src:ax-datastore]]',
      'DataStore and Room keep their files in filesDir and databases, so they are backed up by default along with everything else. The DataStore page mentions this and points to data_extraction_rules for configuration. [[src:ax-datastore]]')
    B(C, S_, 3, 'kind', 'android')

    S_ = 'rules'
    a(C + '.sec.%s.title' % S_, 'Quy tắc include và exclude', 'include and exclude rules')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', 'Từ Android 12, khai android:dataExtractionRules trỏ tới một file data-extraction-rules có hai phần: cloud-backup (sao lưu đám mây) và device-transfer (chuyển máy-sang-máy). Mỗi phần chỉ áp cho kiểu chuyển của nó; thiếu một phần thì kiểu đó được bật đầy đủ, trừ cache và no_backup. Thiết bị Android 11 trở xuống đọc file cũ qua android:fullBackupContent, nên app target 12+ vẫn cần cả hai. [[src:ax-autobackup]]',
      'From Android 12, declare android:dataExtractionRules pointing to a data-extraction-rules file with two sections: cloud-backup and device-transfer. Each applies only to its own transfer type; a missing section means that type is fully enabled, except cache and no_backup. Devices on Android 11 or lower read the older file through android:fullBackupContent, so apps targeting 12+ still need both. [[src:ax-autobackup]]')
    B(C, S_, 2, 'kt', '<data-extraction-rules>\n  <cloud-backup>\n    <exclude domain="file" path="datastore/session.preferences_pb"/>\n  </cloud-backup>\n  <device-transfer>\n    <exclude domain="file" path="datastore/session.preferences_pb"/>\n  </device-transfer>\n</data-extraction-rules>',
      '<data-extraction-rules>\n  <cloud-backup>\n    <exclude domain="file" path="datastore/session.preferences_pb"/>\n  </cloud-backup>\n  <device-transfer>\n    <exclude domain="file" path="datastore/session.preferences_pb"/>\n  </device-transfer>\n</data-extraction-rules>')
    B(C, S_, 3, 'p', 'Mỗi include hay exclude cần domain (root, file, database, sharedpref, external, hay bản device_ của chúng) và path tương đối; không có ký tự đại diện hay biểu thức chính quy, thư mục áp đệ quy. exclude thắng include. Cẩn thận với include: chỉ cần có một include là chỉ những file được include mới được sao lưu. [[src:ax-autobackup]]',
      'Each include or exclude needs a domain (root, file, database, sharedpref, external, or their device_ variants) and a relative path; no wildcards or regular expressions, and a directory applies recursively. exclude wins over include. Careful with include: a single include means only the included files are backed up. [[src:ax-autobackup]]')

    S_ = 'sensitive'
    a(C + '.sec.%s.title' % S_, 'Thứ không nên đi theo sang máy mới', 'What should not follow the user to a new phone')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Trang Auto Backup nêu file chứa định danh riêng của thiết bị thường bị loại khỏi sao lưu; ví dụ của trang là token đăng ký FCM: khôi phục token cũ có thể làm app chạy sai. Cùng nhóm này có mã cài đặt, khóa gắn với phần cứng, và file gỡ lỗi. Cách gọn nhất là để chúng trong noBackupFilesDir, nơi luôn bị loại. [[src:ax-autobackup]]',
      'The Auto Backup page says files with device-specific identifiers are typically excluded from backup; its example is the FCM registration token: restoring the old token can make the app misbehave. The same group includes install ids, hardware-bound keys and debug files. The simplest home for them is noBackupFilesDir, which is always excluded. [[src:ax-autobackup]]')
    B(C, S_, 2, 'p', 'Token đăng nhập là trường hợp riêng: người dùng có thể muốn không phải đăng nhập lại trên máy mới. Trang Auto Backup khuyên khi đó đừng để token trong SharedPreferences hay file, mà dùng Block Store. Nếu không dùng Block Store, loại file token khỏi sao lưu và để người dùng đăng nhập lại một lần. [[src:ax-autobackup]]',
      'Login tokens are a special case: users may want to skip signing in again on a new phone. The Auto Backup page advises that, in that case, tokens should not live in shared preferences or a file, but in Block Store. Without Block Store, exclude the token file from backup and let the user sign in once more. [[src:ax-autobackup]]')
    B(C, S_, 3, 'note', 'allowBackup="false" có vẻ an toàn nhất nhưng làm người dùng mất cả cài đặt và dữ liệu đáng giữ. Trang còn lưu ý: trên một số máy Android 12+, nó không chặn chuyển máy-sang-máy. Loại trừ đúng file nhạy cảm ở cả hai phần của quy tắc thì chắc hơn. [[src:ax-autobackup]]',
      'allowBackup="false" looks safest but makes users lose settings and data worth keeping. The page also notes that on some Android 12+ devices it does not block device-to-device transfer. Excluding exactly the sensitive files in both rule sections is more reliable. [[src:ax-autobackup]]')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Người dùng đổi máy không còn nhận thông báo nhắc lịch, dù app báo đã bật.', 'Users who switch phones stop getting appointment reminders, though the app says they are on.')
    B(C, S_, 1, 'cause', 'Token FCM được lưu trong DataStore và được khôi phục từ máy cũ. App thấy đã có token nên không đăng ký lại; máy chủ gửi tới token của máy kia.', 'The FCM token was stored in DataStore and restored from the old phone. The app saw a token and never registered again; the server sends to the other phone\'s token.')
    B(C, S_, 1, 'fix', 'Lưu token FCM trong noBackupFilesDir (hay loại file của nó bằng quy tắc), và luôn đăng ký token hiện tại lúc khởi động.', 'Keep the FCM token in noBackupFilesDir (or exclude its file by rule), and always register the current token at startup.')
    B(C, S_, 2, 'bug', 'Sau khi thêm một quy tắc include cho database, người dùng đổi máy mất hết cài đặt.', 'After adding an include rule for the database, users who switch phones lose all their settings.')
    B(C, S_, 2, 'cause', 'Có một include là chỉ những file được include mới được sao lưu. File DataStore cài đặt không nằm trong include nên bị bỏ.', 'Once there is an include, only included files are backed up. The settings DataStore file was not included, so it was dropped.')
    B(C, S_, 2, 'fix', 'Dùng exclude cho đúng file cần loại thay vì include cho file cần giữ, hoặc liệt kê đủ mọi file cần giữ; kiểm lại bằng một lần sao lưu và khôi phục thật.', 'Use exclude for exactly the files to drop instead of include for the files to keep, or list every file to keep; verify with a real backup and restore.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Hẹn Khám có: settings.preferences_pb (cài đặt), session.preferences_pb (token đăng nhập), fcm.preferences_pb (token FCM), clinic.db (lịch hẹn, có cả lịch PENDING), logs/ trong filesDir (log gỡ lỗi, có thể vài MB), và thumbs/ trong cacheDir. Với mỗi thứ, quyết định: đi theo khi đổi máy hay không, và bằng cách nào (mặc định, exclude, chuyển thư mục). Viết file quy tắc.',
      'ClinicBook has: settings.preferences_pb (settings), session.preferences_pb (login token), fcm.preferences_pb (FCM token), clinic.db (appointments, including PENDING ones), logs/ in filesDir (debug logs, possibly several MB), and thumbs/ in cacheDir. For each, decide whether it follows the user to a new phone and how (default, exclude, move directory). Write the rules file.')
    B(C, S_, 1, 'hint', 'Ba câu hỏi: người dùng có muốn nó trên máy mới không; nó có gắn với máy hay phiên cũ không; nó có làm vượt 25 MB không.', 'Three questions: does the user want it on the new phone; is it tied to the old device or session; could it push past 25 MB?')
    B(C, S_, 1, 'sol', 'Đi theo mặc định: settings.preferences_pb, clinic.db (lịch PENDING sẽ được worker gửi trên máy mới). Exclude ở cả cloud-backup và device-transfer: session.preferences_pb (đăng nhập lại, hoặc chuyển sang Block Store), logs/ (gỡ lỗi, có thể lớn). Chuyển fcm.preferences_pb sang noBackupFilesDir, hoặc exclude, rồi đăng ký lại lúc khởi động. thumbs/ trong cache: đã luôn bị loại.',
      'Follow by default: settings.preferences_pb, clinic.db (PENDING appointments will be sent by the worker on the new phone). Exclude in both cloud-backup and device-transfer: session.preferences_pb (sign in again, or move to Block Store), logs/ (debug, possibly large). Move fcm.preferences_pb to noBackupFilesDir, or exclude it, then register again at startup. thumbs/ in the cache: already always excluded.')
    B(C, S_, 1, 'solkt', '<data-extraction-rules>\n  <cloud-backup>\n    <exclude domain="file" path="datastore/session.preferences_pb"/>\n    <exclude domain="file" path="datastore/fcm.preferences_pb"/>\n    <exclude domain="file" path="logs/"/>\n  </cloud-backup>\n  <device-transfer>\n    <exclude domain="file" path="datastore/session.preferences_pb"/>\n    <exclude domain="file" path="datastore/fcm.preferences_pb"/>\n    <exclude domain="file" path="logs/"/>\n  </device-transfer>\n</data-extraction-rules>')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Những thư mục nào luôn bị Auto Backup loại?', 'Which directories does Auto Backup always exclude?')
    B(C, S_, 1, 'ans', 'cacheDir, codeCacheDir và noBackupFilesDir.', 'cacheDir, codeCacheDir and noBackupFilesDir.')
    B(C, S_, 2, 'ask', 'Khôi phục xảy ra lúc nào so với lần mở app đầu tiên?', 'When does restore happen relative to the first app launch?')
    B(C, S_, 2, 'ans', 'Trước: sau khi cài APK và trước khi người dùng mở được app.', 'Before it: after the APK installs and before the user can open the app.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Phạm vi sao lưu, lịch chạy, giới hạn 25 MB, mã hóa, thời điểm khôi phục, quy tắc dataExtractionRules và fullBackupContent, lời khuyên về token FCM và Block Store theo trang Auto Backup đọc ngày 2026-11-24. Hậu quả cụ thể của việc khôi phục token cũ (401, đăng xuất) là tình huống của site. Chương không bàn BackupAgent, sao lưu key-value, requireFlags, phần chuyển sang iOS của Android 16, hay cách dùng Block Store.',
      'Backup scope, schedule, the 25 MB limit, encryption, restore timing, dataExtractionRules and fullBackupContent rules, and the advice on FCM tokens and Block Store follow the Auto Backup page as read on 2026-11-24. The specific consequences of restoring old tokens (401s, sign-out) are the site\'s scenario. The chapter does not cover BackupAgent, key-value backup, requireFlags, Android 16\'s iOS transfer section, or how to use Block Store.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'File DataStore có được Auto Backup sao lưu mặc định không?', 'Are DataStore files backed up by Auto Backup by default?', 'Có, vì chúng nằm trong filesDir.', 'Yes, because they live in filesDir.', 'filesDir được sao lưu mặc định.', 'filesDir is backed up by default.'),
        ('q2', 'Mỗi app được sao lưu tối đa bao nhiêu?', 'How much can each app back up?', '25 MB.', '25 MB.', 'Vượt mức thì không gì được gửi lên tới khi dữ liệu nhỏ lại.', 'Over that, nothing is uploaded until the data shrinks.'),
        ('q3', 'Có một include cho database và không có gì khác. File cài đặt có được sao lưu không?', 'There is one include for the database and nothing else. Is the settings file backed up?', 'Không.', 'No.', 'Có include thì chỉ những file được include mới được sao lưu.', 'With any include, only included files are backed up.'),
        ('q4', 'Token FCM nên nằm ở đâu để không bị sao lưu?', 'Where should the FCM token live so it is never backed up?', 'noBackupFilesDir (hoặc loại bằng quy tắc).', 'noBackupFilesDir (or excluded by a rule).', 'Đó là định danh riêng của thiết bị; khôi phục token cũ làm app chạy sai.', 'It is a device-specific identifier; restoring the old one makes the app misbehave.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
