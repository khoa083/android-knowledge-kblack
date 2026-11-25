# Lưu dữ liệu · H6: migration (Phần 1)
# Nguồn: developer.android.com Migrate your Room database (gồm phần Test migrations) (đọc 2026-11-24; hướng dẫn dùng Room 3.0).
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'h6': ['hook', 'versions', 'paths', 'test', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.mig', 'Lưu dữ liệu · nâng database từ v1 lên v3', 'Saving data · upgrading the database from v1 to v3')
    m = lambda k, vi, en=None: a('m.mig.' + k, vi, en)
    m('title', 'Cập nhật app khi database của người dùng còn ở v1', 'Updating the app while the user\'s database is still at v1')
    m('overview', 'Một người dùng bỏ qua bản 2 của Hẹn Khám và cập nhật thẳng lên bản 3. Database của họ còn ở schema v1 với 12 lịch hẹn. App mới khai báo version = 3. Ba cấu hình: chỉ có migration 2→3; có thêm fallbackToDestructiveMigration; có đủ đường 1→2 (tự động) và 2→3 (viết tay).',
      'A user skips version 2 of ClinicBook and updates straight to version 3. Their database is still at schema v1 with 12 appointments. The new app declares version = 3. Three setups: only a 2→3 migration; that plus fallbackToDestructiveMigration; a full path with 1→2 (automated) and 2→3 (manual).')
    m('wrapup', 'Room nâng database bằng cách đi từng bước từ phiên bản trên máy tới phiên bản app khai báo. Thiếu một mũi tên trên đường đi thì app crash mỗi lần mở; bật xóa sạch thì app mở được nhưng dữ liệu người dùng mất vĩnh viễn. Cách đúng là có đủ đường cho mọi phiên bản từng phát hành, xuất schema vào git, và kiểm thử từng migration bằng MigrationTestHelper.',
      'Room upgrades a database by walking step by step from the version on the device to the version the app declares. One missing arrow on that path crashes the app on every launch; enabling destructive fallback lets it open but deletes the user\'s data for good. The right way is a full path for every version ever shipped, schemas exported into git, and each migration tested with MigrationTestHelper.')
    m('simp.1', 'Ba phiên bản, 12 lịch hẹn và nội dung từng thay đổi schema là của site. Ở đây chỉ một bảng; app thật đổi nhiều bảng qua nhiều phiên bản.', 'Three versions, 12 appointments and the content of each schema change are the site\'s. Only one table here; real apps change many tables across many versions.')
    m('simp.2', 'Hành vi khi thiếu đường, xóa sạch và kiểm schema theo trang Migrate your Room database đọc ngày 2026-11-24 (Room 3.0). Trang không nêu nguyên văn thông báo lỗi.', 'Behaviour on a missing path, destructive fallback and schema checks follows the Migrate your Room database page as read on 2026-11-24 (Room 3.0). The page does not quote the error messages.')
    m('ctl.hint', 'Đổi cấu hình rồi đi lại; nhìn mũi tên v1 → v2 và số lịch còn lại.', 'Switch the setup and walk again; watch the v1 → v2 arrow and how many appointments remain.')
    m('ctl.case', 'Cấu hình', 'Setup')
    for k, vi, en in [('missing', 'chỉ có migration 2→3', 'only a 2→3 migration'), ('destructive', 'thêm fallbackToDestructiveMigration', 'plus fallbackToDestructiveMigration'), ('complete', 'đủ đường 1→2→3', 'a full 1→2→3 path')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'App mới, Room, file database trên máy', 'New app, Room, database file on the device')
    m('diagramDesc', 'App mới mở database qua Room; Room so phiên bản và chạy migration trên file của người dùng', 'The new app opens the database through Room; Room compares versions and runs migrations on the user\'s file')
    for k, vi, en in [('app', 'App bản 3', 'App version 3'), ('room', 'Room mở database', 'Room opens the database'), ('db', 'clinic.db của người dùng', 'the user\'s clinic.db')]:
        m('n.' + k, vi, en)
    m('met.ver', 'Phiên bản database', 'Database version'); m('met.rows', 'Lịch hẹn còn', 'Appointments left'); m('met.st', 'Tình trạng', 'Status')
    for v in (1, 2, 3):
        m('ver.%d' % v, 'v%d' % v, 'version %d' % v)
    for k, vi, en in [('old', 'app mới, database cũ', 'new app, old database'), ('search', 'Room tìm đường 1 → 3', 'Room looks for a 1 → 3 path'),
                      ('crash', 'IllegalStateException: thiếu migration', 'IllegalStateException: missing migration'), ('loop', 'crash mỗi lần mở app', 'crashes on every launch'),
                      ('wiped', 'đã xóa sạch mọi bảng', 'every table dropped'), ('empty', 'mở được, nhưng trống', 'opens, but empty'),
                      ('step', 'đang chạy migration', 'running a migration'), ('valid', 'schema khớp v3, dữ liệu còn nguyên', 'schema matches v3, data intact')]:
        m('st.' + k, vi, en)
    a('cap.mig', 'App mới mở database qua Room; Room so phiên bản trong file với phiên bản app khai báo và chạy migration. Khối viền đỏ là chỗ crash hay mất dữ liệu.', 'The new app opens the database through Room; Room compares the file\'s version with the declared one and runs migrations. A red outline marks a crash or data loss.')
    S = [
        ('missing', 's1', 'Cập nhật thẳng từ bản 1 lên bản 3', 'Update straight from version 1 to version 3',
         'Người dùng bỏ qua bản 2. clinic.db trên máy ghi version 1, có 12 lịch hẹn. App mới khai báo version = 3 và chỉ đăng ký MIGRATION_2_3.', 'The user skipped version 2. clinic.db on the device says version 1 and holds 12 appointments. The new app declares version = 3 and registers only MIGRATION_2_3.'),
        ('missing', 's2', 'Room tìm đường từ 1 tới 3: thiếu mũi tên 1 → 2', 'Room looks for a path from 1 to 3: the 1 → 2 arrow is missing',
         'Room cần một chuỗi migration nối 1 tới 3. Có 2 → 3, nhưng không có gì bắt đầu từ 1.', 'Room needs a chain of migrations joining 1 to 3. There is 2 → 3, but nothing starts at 1.'),
        ('missing', 's3', 'IllegalStateException khi mở database', 'IllegalStateException when opening the database',
         'Room từ chối mở và ném IllegalStateException. Mọi màn hình đọc database đều crash ngay.', 'Room refuses to open and throws IllegalStateException. Every screen that reads the database crashes at once.'),
        ('missing', 's4', 'Crash mỗi lần mở, tới khi người dùng gỡ app', 'Crashes on every launch, until the user uninstalls',
         'File vẫn ở v1 nên lần mở sau gặp lại đúng lỗi đó. Lối thoát duy nhất của người dùng là gỡ app, và gỡ app xóa luôn 12 lịch hẹn.', 'The file is still at v1, so the next launch hits the same error. The user\'s only way out is uninstalling, which deletes the 12 appointments anyway.'),
        ('destructive', 's1', 'Cập nhật thẳng từ bản 1 lên bản 3', 'Update straight from version 1 to version 3',
         'Như trước, nhưng builder có thêm fallbackToDestructiveMigration() "cho chắc".', 'As before, but the builder adds fallbackToDestructiveMigration() "just in case".'),
        ('destructive', 's2', 'Thiếu đường 1 → 2: Room chuyển sang xóa sạch', 'No 1 → 2 path: Room falls back to destroying',
         'Không tìm được đường, Room không crash mà làm theo fallback.', 'Finding no path, Room does not crash; it follows the fallback.'),
        ('destructive', 's3', 'Xóa mọi bảng, tạo lại theo schema v3', 'Every table dropped, recreated with the v3 schema',
         'Database được dựng lại rỗng ở version 3. 12 lịch hẹn biến mất, kể cả những lịch đặt lúc mất mạng chưa kịp gửi lên máy chủ.', 'The database is rebuilt empty at version 3. The 12 appointments are gone, including any booked offline and not yet sent to the server.'),
        ('destructive', 's4', 'App mở bình thường, danh sách trống', 'The app opens normally, with an empty list',
         'Không crash, không có lỗi trong log. Người dùng chỉ thấy lịch hẹn của mình đã biến mất.', 'No crash, nothing in the log. The user just sees their appointments are gone.'),
        ('complete', 's1', 'Cập nhật thẳng từ bản 1 lên bản 3', 'Update straight from version 1 to version 3',
         'App mới có AutoMigration(1, 2) và MIGRATION_2_3 viết tay: đủ đường cho mọi phiên bản từng phát hành.', 'The new app has AutoMigration(1, 2) and a hand-written MIGRATION_2_3: a path for every version ever shipped.'),
        ('complete', 's2', 'Bước 1 → 2: migration tự động thêm cột note', 'Step 1 → 2: the automated migration adds the note column',
         'Room so schema v1 và v2 đã xuất, thấy chỉ thêm một cột cho phép null, và tự sinh câu ALTER TABLE. 12 lịch vẫn còn.', 'Room compares the exported v1 and v2 schemas, sees a single nullable column added, and generates the ALTER TABLE itself. All 12 appointments remain.'),
        ('complete', 's3', 'Bước 2 → 3: migration tay thêm cột và điền dữ liệu', 'Step 2 → 3: the manual migration adds a column and fills it',
         'Cột statusCode mới phải lấy giá trị từ cột status cũ. Room không đoán được phép biến đổi dữ liệu này, nên nó được viết tay bằng SQL.', 'The new statusCode column must take its value from the old status column. Room cannot guess that data transformation, so it is written by hand in SQL.'),
        ('complete', 's4', 'Room kiểm schema khớp v3 rồi mở', 'Room checks the schema matches v3, then opens',
         'Sau khi chạy hết migration, Room kiểm schema thực tế có khớp schema v3 mà nó mong đợi. Khớp: database mở, 12 lịch còn nguyên.', 'After all migrations run, Room checks the actual schema matches the v3 schema it expects. It matches: the database opens with all 12 appointments.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cấu hình; để ý số lịch hẹn còn lại ở bước cuối.', 'Walk all four steps of each setup; watch how many appointments remain at the end.'),
        ('missing.s2', 'Người dùng không nâng cấp theo thứ tự bạn phát hành. Mỗi phiên bản từng có trên Play phải có đường tới phiên bản mới nhất.', 'Users do not upgrade in the order you release. Every version ever on the store needs a path to the latest one.'),
        ('missing.s3', 'Tài liệu Android nói: nếu thiếu đường migration, Room ném IllegalStateException. [[src:ax-room-migrations]]', 'The Android docs say: if a migration path is missing, Room throws IllegalStateException. [[src:ax-room-migrations]]'),
        ('missing.s4', 'Lỗi này chỉ lộ ra ở máy người dùng còn phiên bản cũ; máy dev cài mới luôn chạy bình thường.', 'This only shows on devices still holding the old version; a developer\'s fresh install always works.'),
        ('destructive.s2', 'fallbackToDestructiveMigration không sửa đường thiếu; nó quyết định rằng mất dữ liệu là chấp nhận được.', 'fallbackToDestructiveMigration does not fix the missing path; it decides that losing data is acceptable.'),
        ('destructive.s3', 'Trang Migrate your Room database cảnh báo: fallbackToDestructiveMigration xóa vĩnh viễn mọi dữ liệu trong các bảng. [[src:ax-room-migrations]]', 'The Android docs warn: fallbackToDestructiveMigration permanently deletes all data from the tables. [[src:ax-room-migrations]]'),
        ('destructive.s4', 'Chỉ dùng xóa sạch cho dữ liệu chỉ là cache của máy chủ. Có biến thể hẹp hơn: fallbackToDestructiveMigrationFrom(các phiên bản) và fallbackToDestructiveMigrationOnDowngrade(). [[src:ax-room-migrations]]', 'Only destroy data that is just a cache of the server. There are narrower variants: fallbackToDestructiveMigrationFrom(versions) and fallbackToDestructiveMigrationOnDowngrade(). [[src:ax-room-migrations]]'),
        ('complete.s2', 'Migration tự động dựa trên schema đã sinh của cả hai phiên bản; nếu exportSchema = false thì nó thất bại. [[src:ax-room-migrations]]', 'Automated migrations rely on the generated schemas of both versions; if exportSchema is false, they fail. [[src:ax-room-migrations]]'),
        ('complete.s3', 'Migration tay: kế thừa Migration(startVersion, endVersion), ghi đè migrate, đăng ký bằng addMigrations. Trang dặn viết câu truy vấn đầy đủ thay vì dùng hằng số. [[src:ax-room-migrations]]', 'Manual migration: extend Migration(startVersion, endVersion), override migrate, register with addMigrations. The page advises writing full queries rather than constants. [[src:ax-room-migrations]]'),
        ('complete.s4', 'Trong ví dụ kiểm thử của trang: Room kiểm schema sau khi chạy xong mọi migration. [[src:ax-room-migrations]]', 'From the page\'s test example: Room validates the schema once all migrations have run. [[src:ax-room-migrations]]')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.mg', 'Dãy phiên bản', 'Version chain')
    z('mg.cap', 'Mỗi ô là một phiên bản schema; mỗi mũi tên là một migration. Ô có viền là phiên bản database trên máy lúc này.', 'Each box is a schema version; each arrow is a migration. The outlined box is the database version on the device right now.')
    z('mg.v1', 'bảng appointment: id, doctorId, time, status', 'appointment table: id, doctorId, time, status')
    z('mg.v2', '+ cột note (cho phép null)', '+ note column (nullable)')
    z('mg.v3', '+ cột statusCode, điền từ status', '+ statusCode column, filled from status')
    z('mg.here', 'ở đây: {n} lịch', 'here: {n} appointments')
    z('mg.target', 'app khai báo', 'declared by the app')
    z('mg.e.auto', 'AutoMigration({a}, {b})', 'AutoMigration({a}, {b}) generated')
    z('mg.e.manual', 'MIGRATION_{a}_{b} (tay)', 'MIGRATION_{a}_{b} (manual)')
    z('mg.e.missing', 'thiếu {a} → {b}', 'missing {a} → {b}')
    z('mg.status', 'Tình trạng:', 'Status:')
    z('mg.legend', 'Mũi tên nét đứt đỏ: không có migration cho bước đó. Ô gạch đỏ: database đã bị xóa sạch.', 'Red dashed arrow: no migration for that step. Red hatched box: the database was wiped.')

    C = 'h6'
    a(C + '.title', 'Migration', 'Migrations')
    a(C + '.essence', 'Mỗi lần đổi schema phải tăng version, và mọi phiên bản từng phát hành phải có đường migration tới phiên bản mới nhất; người dùng có thể nhảy cóc.\nThiếu đường thì Room ném IllegalStateException mỗi lần mở; fallbackToDestructiveMigration tránh crash bằng cách xóa vĩnh viễn mọi dữ liệu.\nMigration tự động lo thay đổi đơn giản dựa trên schema đã xuất; biến đổi dữ liệu thì viết tay. Kiểm thử từng migration bằng MigrationTestHelper.',
      'Every schema change must bump the version, and every version ever shipped needs a migration path to the latest; users can skip versions.\nA missing path makes Room throw IllegalStateException on every open; fallbackToDestructiveMigration avoids the crash by permanently deleting all data.\nAutomated migrations handle simple changes using exported schemas; data transformations are written by hand. Test each migration with MigrationTestHelper.')
    a(C + '.goal.g1', 'Đã thấy kết quả của bước migration đầu', 'Saw what the first migration step did')
    a(C + '.goal.g2', 'Đã thấy database mở được hay không', 'Saw whether the database opens')
    a(C + '.sim.storage.mig', 'nâng database từ v1 lên v3', 'upgrading the database from v1 to v3')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Bản 2 có MIGRATION_1_2; bản 3 thêm MIGRATION_2_3 nhưng lỡ xóa MIGRATION_1_2 khi dọn mã. Bạn cài bản 3 lên máy test mới, mọi thứ chạy tốt. Ai sẽ gặp lỗi, và lỗi gì?',
      'Version 2 had MIGRATION_1_2; version 3 adds MIGRATION_2_3 but MIGRATION_1_2 was deleted during a cleanup. You install version 3 on a fresh test device and everything works. Who hits a problem, and what is it?')
    B(C, S_, 1, 'ans', 'Người dùng còn ở bản 1 và cập nhật thẳng lên bản 3. Room không tìm được đường 1 → 3, ném IllegalStateException, và app crash mỗi lần mở. Máy test mới tạo database thẳng ở v3 nên không bao giờ thấy lỗi. [[src:ax-room-migrations]]',
      'Users still on version 1 who update straight to version 3. Room finds no path from 1 to 3, throws IllegalStateException, and the app crashes on every launch. A fresh test device creates the database directly at v3, so it never sees the problem. [[src:ax-room-migrations]]')

    S_ = 'versions'
    a(C + '.sec.%s.title' % S_, 'Room nâng phiên bản thế nào', 'How Room upgrades a version')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'File database ghi lại phiên bản schema của nó. Lớp @Database khai báo version mà app mong đợi. Khi mở, nếu hai số khác nhau, Room tìm một chuỗi migration nối từ phiên bản trong file tới phiên bản khai báo và chạy lần lượt. Sau khi chạy hết, Room kiểm schema thực tế có khớp schema mong đợi. [[src:ax-room-migrations]]',
      'The database file records its schema version. The @Database class declares the version the app expects. On open, if the two differ, Room looks for a chain of migrations from the file\'s version to the declared one and runs them in order. After all of them run, Room checks the actual schema matches the expected one. [[src:ax-room-migrations]]')
    B(C, S_, 2, 'p', 'Nếu không có chuỗi nào, Room ném IllegalStateException. Bật fallbackToDestructiveMigration() thì thay vì crash, Room xóa mọi bảng và tạo lại; trang hướng dẫn cảnh báo rằng nó xóa vĩnh viễn mọi dữ liệu trong bảng. Biến thể hẹp hơn: fallbackToDestructiveMigrationFrom(…) chỉ cho một số phiên bản cũ, fallbackToDestructiveMigrationOnDowngrade() chỉ khi hạ phiên bản. [[src:ax-room-migrations]]',
      'If there is no chain, Room throws IllegalStateException. With fallbackToDestructiveMigration() enabled, instead of crashing Room drops every table and recreates them; the guide warns this permanently deletes all data in the tables. Narrower variants: fallbackToDestructiveMigrationFrom(…) only for some old versions, fallbackToDestructiveMigrationOnDowngrade() only on downgrades. [[src:ax-room-migrations]]')
    B(C, S_, 3, 'note', 'Xóa sạch chỉ chấp nhận được khi database chỉ là bản sao của máy chủ, tải lại được hết. Với app offline-first, database giữ cả thao tác chưa gửi đi (chương H7): xóa sạch là mất dữ liệu thật.',
      'Destroying is only acceptable when the database is merely a copy of the server that can be fully downloaded again. In an offline-first app the database also holds actions not yet sent (chapter H7): destroying it loses real data.')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'paths'
    a(C + '.sec.%s.title' % S_, 'Migration tự động và viết tay', 'Automated and manual migrations')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', 'Migration tự động khai báo trong @Database(autoMigrations = [AutoMigration(from = 1, to = 2)]). Room so schema đã sinh của hai phiên bản và tự viết SQL. Vì vậy nó cần schema đã xuất: exportSchema = false, hay phiên bản mới chưa được biên dịch, thì migration tự động thất bại. [[src:ax-room-migrations]]',
      'Automated migrations are declared in @Database(autoMigrations = [AutoMigration(from = 1, to = 2)]). Room compares the generated schemas of both versions and writes the SQL itself. So it needs exported schemas: with exportSchema = false, or if the newer version has not been compiled yet, automated migrations fail. [[src:ax-room-migrations]]')
    B(C, S_, 2, 'p', 'Khi thay đổi mơ hồ, Room báo lỗi lúc biên dịch và cần một spec: một lớp hiện thực AutoMigrationSpec gắn @RenameColumn, @DeleteColumn, @RenameTable hay @DeleteTable, truyền vào AutoMigration(from, to, spec = …). Ví dụ đổi tên cột: nếu không có spec, Room không biết đó là đổi tên hay xóa một cột rồi thêm cột khác. [[src:ax-room-migrations]]',
      'When a change is ambiguous, Room reports a compile-time error and needs a spec: a class implementing AutoMigrationSpec annotated with @RenameColumn, @DeleteColumn, @RenameTable or @DeleteTable, passed as AutoMigration(from, to, spec = …). Renaming a column, for example: without a spec, Room cannot tell a rename from deleting one column and adding another. [[src:ax-room-migrations]]')
    B(C, S_, 3, 'kt', 'val MIGRATION_2_3 = object : Migration(2, 3) {\n    override suspend fun migrate(connection: SQLiteConnection) {\n        connection.execSQL("ALTER TABLE appointment ADD COLUMN statusCode INTEGER NOT NULL DEFAULT 0")\n        connection.execSQL("UPDATE appointment SET statusCode = 2 WHERE status = \'done\'")\n    }\n}\n\nRoom.databaseBuilder<AppDatabase>(ctx, "clinic.db")\n    .addMigrations(MIGRATION_2_3)      // 1 → 2 là AutoMigration trong @Database\n    .build()',
      'val MIGRATION_2_3 = object : Migration(2, 3) {\n    override suspend fun migrate(connection: SQLiteConnection) {\n        connection.execSQL("ALTER TABLE appointment ADD COLUMN statusCode INTEGER NOT NULL DEFAULT 0")\n        connection.execSQL("UPDATE appointment SET statusCode = 2 WHERE status = \'done\'")\n    }\n}\n\nRoom.databaseBuilder<AppDatabase>(ctx, "clinic.db")\n    .addMigrations(MIGRATION_2_3)      // 1 → 2 is an AutoMigration in @Database\n    .build()')
    B(C, S_, 4, 'note', 'Chữ ký theo hướng dẫn Room 3.0 (migrate nhận SQLiteConnection và là hàm suspend). Room 2.x viết override fun migrate(db: SupportSQLiteDatabase) và gọi db.execSQL. Biến đổi dữ liệu (điền cột mới từ cột cũ, tách một cột thành hai) luôn cần migration tay; có cả migration tay và tự động cho cùng phiên bản thì Room dùng bản tay. [[src:ax-room-migrations]]',
      'Signature per the Room 3.0 guide (migrate takes a SQLiteConnection and is a suspend function). Room 2.x writes override fun migrate(db: SupportSQLiteDatabase) and calls db.execSQL. Data transformations (filling a new column from an old one, splitting one column into two) always need a manual migration; if both a manual and an automated migration exist for the same versions, Room uses the manual one. [[src:ax-room-migrations]]')
    B(C, S_, 4, 'kind', 'android')

    S_ = 'test'
    a(C + '.sec.%s.title' % S_, 'Kiểm thử migration', 'Testing migrations')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', 'Kiểm thử migration cần schema đã xuất: Room ghi schema dạng JSON lúc biên dịch, và trang dặn đưa các file này vào version control. Với Room 3.0, đặt thư mục qua Gradle plugin androidx.room3 (room3 { schemaDirectory("$projectDir/schemas") }); không dùng plugin thì qua tùy chọn room.schemaLocation. [[src:ax-room-migrations]]',
      'Testing migrations needs exported schemas: Room writes the schema as JSON at compile time, and the page says to keep these files in version control. With Room 3.0, set the directory through the androidx.room3 Gradle plugin (room3 { schemaDirectory("$projectDir/schemas") }); without the plugin, through the room.schemaLocation option. [[src:ax-room-migrations]]')
    B(C, S_, 2, 'kt', '@get:Rule val helper = MigrationTestHelper(instrumentation, AppDatabase::class, driver = AndroidSQLiteDriver(), file = dbFile)\n\n@Test fun migrate2To3() = runTest {\n    helper.createDatabase(2).use { c ->\n        // DAO dùng schema mới nhất nên không dùng được ở đây: chèn bằng SQL\n        c.execSQL("INSERT INTO appointment (id, doctorId, time, status, note) VALUES (1, 7, 0, \'done\', NULL)")\n    }\n    helper.runMigrationsAndValidate(3, listOf(MIGRATION_2_3)).use { c ->\n        // kiểm statusCode = 2 cho dòng id 1\n    }\n}',
      '@get:Rule val helper = MigrationTestHelper(instrumentation, AppDatabase::class, driver = AndroidSQLiteDriver(), file = dbFile)\n\n@Test fun migrate2To3() = runTest {\n    helper.createDatabase(2).use { c ->\n        // DAOs expect the latest schema, so they cannot be used here: insert with SQL\n        c.execSQL("INSERT INTO appointment (id, doctorId, time, status, note) VALUES (1, 7, 0, \'done\', NULL)")\n    }\n    helper.runMigrationsAndValidate(3, listOf(MIGRATION_2_3)).use { c ->\n        // check statusCode = 2 for row id 1\n    }\n}')
    B(C, S_, 3, 'p', 'createDatabase(n) tạo database ở phiên bản cũ; runMigrationsAndValidate chạy migration và tự kiểm schema sau đó. Trang còn gợi ý một test mở database với mọi migration đã đăng ký, để bắt đúng lỗi "thiếu một mũi tên" ở mô phỏng trên. [[src:ax-room-migrations]]',
      'createDatabase(n) creates a database at an old version; runMigrationsAndValidate runs the migration and checks the schema afterwards. The page also suggests a test that opens the database with every registered migration, which catches exactly the "missing arrow" bug from the simulation above. [[src:ax-room-migrations]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Sau bản cập nhật, báo cáo crash tăng vọt, toàn ở người dùng lâu năm; máy của cả đội đều chạy tốt.', 'After an update, crash reports spike, all from long-time users; every device on the team works fine.')
    B(C, S_, 1, 'cause', 'Một migration cũ bị xóa hoặc chưa bao giờ được đăng ký; người dùng nhảy cóc phiên bản không có đường. Máy của đội luôn cài mới hoặc đi qua từng bản.', 'An old migration was deleted or never registered; users skipping versions have no path. Team devices are always fresh installs or upgraded one step at a time.')
    B(C, S_, 1, 'fix', 'Đăng ký đủ migration cho mọi phiên bản từng phát hành, và thêm test mở database từ phiên bản cũ nhất với mọi migration.', 'Register migrations for every version ever shipped, and add a test that opens the database from the oldest version with every migration.')
    B(C, S_, 2, 'bug', 'Người dùng báo mất toàn bộ lịch hẹn sau khi cập nhật, không có crash nào.', 'Users report losing all their appointments after an update, with no crash at all.')
    B(C, S_, 2, 'cause', 'Builder có fallbackToDestructiveMigration() từ hồi làm prototype. Một migration thiếu khiến Room lặng lẽ xóa sạch database.', 'The builder kept fallbackToDestructiveMigration() from the prototype days. One missing migration made Room silently wipe the database.')
    B(C, S_, 2, 'fix', 'Bỏ fallback xóa sạch cho database có dữ liệu người dùng; nếu thật sự cần, chỉ dùng fallbackToDestructiveMigrationFrom cho đúng những phiên bản không thể nâng.', 'Remove destructive fallback for databases holding user data; if truly needed, use only fallbackToDestructiveMigrationFrom for exactly the versions that cannot be upgraded.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Hẹn Khám v3 sắp lên v4 với hai thay đổi: (a) đổi tên cột time thành startTime; (b) xóa cột status vì đã có statusCode. Chọn migration tự động hay viết tay cho bước 3 → 4, viết phần khai báo, và liệt kê các test cần có để chắc chắn người dùng ở v1, v2, v3 đều lên được v4.',
      'ClinicBook v3 is moving to v4 with two changes: (a) rename the time column to startTime; (b) drop the status column since statusCode exists. Choose an automated or manual migration for 3 → 4, write the declaration, and list the tests needed to be sure users on v1, v2 and v3 all reach v4.')
    B(C, S_, 1, 'hint', 'Đổi tên và xóa cột là hai thay đổi mơ hồ mà migration tự động cần spec. Không có biến đổi dữ liệu nào.', 'Renaming and dropping a column are exactly the ambiguous changes an automated migration needs a spec for. There is no data transformation.')
    B(C, S_, 1, 'sol', 'Dùng AutoMigration(from = 3, to = 4, spec = …) với một spec gắn @RenameColumn(tableName = "appointment", fromColumnName = "time", toColumnName = "startTime") và @DeleteColumn(tableName = "appointment", columnName = "status"). Test: runMigrationsAndValidate cho từng bước 1→2, 2→3, 3→4 với dữ liệu mẫu; và một test mở database tạo ở v1 với mọi migration, kiểm dữ liệu còn đủ ở v4.',
      'Use AutoMigration(from = 3, to = 4, spec = …) with a spec annotated @RenameColumn(tableName = "appointment", fromColumnName = "time", toColumnName = "startTime") and @DeleteColumn(tableName = "appointment", columnName = "status"). Tests: runMigrationsAndValidate for each step 1→2, 2→3, 3→4 with sample data; and one test that opens a database created at v1 with every migration and checks all data reached v4.')
    B(C, S_, 1, 'solkt', '@RenameColumn(tableName = "appointment", fromColumnName = "time", toColumnName = "startTime")\n@DeleteColumn(tableName = "appointment", columnName = "status")\nclass Migration3To4 : AutoMigrationSpec\n\n@Database(\n    entities = [Appointment::class], version = 4,\n    autoMigrations = [\n        AutoMigration(from = 1, to = 2),\n        AutoMigration(from = 3, to = 4, spec = Migration3To4::class),\n    ],\n)\nabstract class AppDatabase : RoomDatabase()   // 2 → 3 vẫn là MIGRATION_2_3 viết tay')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Vì sao máy test cài mới không bắt được lỗi thiếu migration?', 'Why does a freshly installed test device not catch a missing migration?')
    B(C, S_, 1, 'ans', 'Cài mới thì Room tạo database thẳng ở phiên bản mới nhất, không chạy migration nào.', 'On a fresh install Room creates the database directly at the latest version and runs no migration.')
    B(C, S_, 2, 'ask', 'Migration tự động cần điều kiện gì?', 'What does an automated migration need?')
    B(C, S_, 2, 'ans', 'Schema đã xuất của cả hai phiên bản; với thay đổi mơ hồ như đổi tên hay xóa thì thêm một spec.', 'The exported schemas of both versions; for ambiguous changes such as renames or deletions, a spec too.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'Mọi hành vi (tìm đường, IllegalStateException, xóa sạch và các biến thể, migration tự động và spec, migration tay, kiểm schema, MigrationTestHelper) theo trang Migrate your Room database đọc ngày 2026-11-24, khi hướng dẫn dùng Room 3.0; trang không nêu nguyên văn thông báo lỗi nên site không trích. Chữ ký Room 2.x ghi để đối chiếu. Ba phiên bản, 12 lịch và nội dung thay đổi là của site. Chương không bàn hạ phiên bản, migration nhiều bảng hay đổi kiểu cột.',
      'All behaviour (path search, IllegalStateException, destructive fallback and its variants, automated migrations and specs, manual migrations, schema validation, MigrationTestHelper) follows the Migrate your Room database page as read on 2026-11-24, when the guide used Room 3.0; the page does not quote error messages, so the site does not either. Room 2.x signatures are given for comparison. The three versions, 12 appointments and the changes are the site\'s. The chapter does not cover downgrades, multi-table migrations or changing column types.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Database trên máy ở v1, app khai báo v3, chỉ có MIGRATION_2_3. Chuyện gì xảy ra?', 'The device database is at v1, the app declares v3, only MIGRATION_2_3 exists. What happens?', 'Room ném IllegalStateException khi mở.', 'Room throws IllegalStateException on open.', 'Không có chuỗi migration nối 1 tới 3.', 'No chain of migrations joins 1 to 3.'),
        ('q2', 'fallbackToDestructiveMigration làm gì khi thiếu đường?', 'What does fallbackToDestructiveMigration do on a missing path?', 'Xóa mọi bảng và tạo lại; dữ liệu mất vĩnh viễn.', 'Drops every table and recreates them; the data is lost for good.', 'App không crash nhưng người dùng mất dữ liệu.', 'The app does not crash, but the user loses data.'),
        ('q3', 'Đổi tên một cột bằng migration tự động cần thêm gì?', 'What does renaming a column with an automated migration need?', 'Một spec gắn @RenameColumn.', 'A spec annotated @RenameColumn.', 'Không có spec, Room không phân biệt được đổi tên với xóa rồi thêm.', 'Without one, Room cannot tell a rename from a delete plus an add.'),
        ('q4', 'Vì sao test migration không chèn dữ liệu bằng DAO?', 'Why does a migration test not insert data through DAOs?', 'DAO dùng schema mới nhất, không khớp database ở phiên bản cũ.', 'DAOs expect the latest schema, which does not match an old-version database.', 'Chèn bằng SQL trên kết nối do createDatabase trả về.', 'Insert with SQL on the connection createDatabase returns.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
