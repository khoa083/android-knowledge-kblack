/* Nguồn của track H (Lưu dữ liệu). Trang developer.android.com và mã AOSP đọc ngày 2026-11-24 (docs/research/storage.md). */
(function () {
  var D = 'https://developer.android.com/';
  var s = function (id, title, url, org, label, vi, en) { return { id: id, title: title, url: url, org: org, tracks: ['storage'], label: label, lang: 'en', supports: { vi: vi, en: en } }; };
  ADE.addSources([
    s('ax-storage-overview', 'Data and file storage overview', D + 'training/data-storage', 'Android Developers', 'stable',
      'Bốn lựa chọn: lưu riêng của app, lưu chung (media, tài liệu), preferences, database (Room). Bảng so sánh: cách truy cập, quyền, app khác có đọc được không, có bị xóa khi gỡ app không. Bốn câu hỏi khi chọn: dung lượng, độ tin cậy, loại dữ liệu, có riêng tư không. Không viết cứng đường dẫn (H1).',
      'Four options: app-specific storage, shared storage (media, documents), preferences, databases (Room). A comparison table: access method, permissions, whether other apps can access it, whether it is removed on uninstall. Four questions when choosing: space, reliability, kind of data, privacy. Do not hardcode paths (H1).'),
    s('ax-app-specific', 'Access app-specific files', D + 'training/data-storage/app-specific', 'Android Developers', 'stable',
      'filesDir và cacheDir không cần quyền; từ Android 10 các thư mục nội bộ được mã hóa; file riêng của app bị xóa khi gỡ app. Khi máy thiếu dung lượng, hệ thống có thể xóa file cache; phải kiểm file còn trước khi đọc. Bộ nhớ ngoài của app không phải lúc nào cũng truy cập được (H1, H2).',
      'filesDir and cacheDir need no permissions; from Android 10 the internal locations are encrypted; app-specific files are removed on uninstall. When the device is low on storage, the system may delete cache files; check a cache file exists before reading it. App-specific external storage is not always accessible (H1, H2).'),
    s('ax-datastore', 'DataStore', D + 'topic/libraries/architecture/datastore', 'Android Developers', 'stable',
      'Lưu cặp khóa–giá trị hay đối tượng có kiểu, bất đồng bộ, nhất quán, theo giao dịch, bằng coroutine và Flow. Nên chuyển từ SharedPreferences sang DataStore. DataStore hợp với dữ liệu nhỏ, không hỗ trợ cập nhật từng phần hay ràng buộc tham chiếu; cần những thứ đó thì dùng Room. Không tạo hai instance cho cùng một file trong một tiến trình. Nhiều tiến trình từ bản 1.1.0. Bản trong hướng dẫn: 1.3.0 (H1, H3).',
      'Stores key–value pairs or typed objects asynchronously, consistently and transactionally, using coroutines and Flow. Consider migrating from SharedPreferences to DataStore. DataStore suits small datasets and does not support partial updates or referential integrity; use Room when you need those. Never create two instances for the same file in one process. Multi-process since 1.1.0. Version in the guide: 1.3.0 (H1, H3).'),
    s('ax-sp-editor', 'SharedPreferences.Editor (reference)', D + 'reference/android/content/SharedPreferences.Editor', 'Android Developers', 'stable',
      'commit() ghi đồng bộ và trả về true nếu ghi xuống bộ nhớ bền thành công. apply() đổi bản trong bộ nhớ ngay, ghi đĩa bất đồng bộ, không báo lỗi. Các lần apply() đang chờ có thể chặn main thread lúc chuyển trạng thái vòng đời, một nguồn ANR hay gặp (H3).',
      'commit() writes synchronously and returns true if the values were written to persistent storage. apply() changes the in-memory copy at once, writes to disk asynchronously and reports no failure. Pending apply() calls can block the main thread during lifecycle transitions, a common source of ANRs (H3).'),
    s('aosp-sp-impl', 'SharedPreferencesImpl.java (AOSP, nhánh main)', 'https://android.googlesource.com/platform/frameworks/base/+/refs/heads/main/core/java/android/app/SharedPreferencesImpl.java', 'Android Open Source Project', 'impl',
      'Nạp cả file XML vào một map trong bộ nhớ ở luồng nền (loadFromDisk); hàm get chờ tới khi nạp xong (awaitLoadedLocked). Mỗi lần ghi, writeToFile ghi lại toàn bộ map rồi sync; có file .bak để khôi phục khi ghi hỏng (H1, H3).',
      'Loads the whole XML file into an in-memory map on a background thread (loadFromDisk); getters wait until loading finishes (awaitLoadedLocked). Each write, writeToFile writes the whole map then syncs; a .bak file allows recovery from a failed write (H1, H3).'),
    s('ax-room', 'Save data in a local database using Room', D + 'training/data-storage/room', 'Android Developers', 'stable',
      'Ba thành phần: lớp database, entity, DAO. Room kiểm câu SQL lúc biên dịch, giảm mã lặp, có đường migration. Nên dùng Room thay cho API SQLite trực tiếp (H1, H4).',
      'Three components: the database class, entities, DAOs. Room verifies SQL at compile time, reduces boilerplate and provides migration paths. Use Room rather than the SQLite APIs directly (H1, H4).')
  ]);
})();
