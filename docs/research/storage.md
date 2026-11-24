# Nghiên cứu track H (Lưu dữ liệu trên Android)

> Track đã duyệt 2026-11-24, đang viết. Dàn ý: `docs/tracks/H-saving-data.md`. Nguồn chính thức thắng khi mâu thuẫn.

## Đã đọc để soạn dàn ý (2026-11-23)
- **developer.android.com (HTTP 200):**
  - Data and file storage overview, App-specific storage, Shared storage và MediaStore;
  - DataStore;
  - Room (Relationships, Async queries, Migrating database versions, Testing);
  - Offline-first, Persistent work, Auto Backup.
- **Sách *Saving Data on Android* (raywenderlich): mới đọc mục lục.**
  - Phần dùng được: File, SharedPreferences, SQLite, ContentProvider, Room.
  - Phần Firebase: 10 chương.
  - Sách ra trước DataStore, nên chỉ là nguồn phụ.

## Bảng nguồn theo chương
Điền khi viết từng chương, cùng khuôn với `docs/research/arch.md`: khẳng định → nguồn → loại (stable, impl, guideline, simplified).

## Đọc thêm khi viết (2026-11-24)
- developer.android.com: Data and file storage overview, App-specific storage, DataStore, SharedPreferences.Editor, AtomicFile (androidx.core), SharedPreferencesMigration, Room (tổng quan, Async queries, Accessing data). Tất cả HTTP 200.
- Mã AOSP `SharedPreferencesImpl.java` nhánh main (android.googlesource.com): loadFromDisk nạp cả file vào map ở luồng nền; getter chờ `awaitLoadedLocked`; `writeToFile` ghi lại toàn bộ map rồi sync, có file `.bak`; `apply()` đổi bộ nhớ ngay rồi xếp việc ghi qua `QueuedWork`.
- Lưu ý phiên bản: hướng dẫn Room đọc ngày 2026-11-24 dùng **Room 3.0** (gói `androidx.room3`, cần KSP); DataStore 1.3.0. Mã minh họa của site dùng các annotation chung (@Entity, @Dao, @Query) có ở cả 2.x và 3.0.

### H1 · Chọn nơi lưu
| Khẳng định | Nguồn | Loại |
|---|---|---|
| Bốn nhóm: riêng của app, chung (media, tài liệu), preferences, database (Room) | ax-storage-overview | stable |
| Bảng: app riêng không cần quyền nội bộ, app khác không đọc, xóa khi gỡ; media: app khác đọc (cần quyền), còn sau gỡ | ax-storage-overview | stable |
| Bốn câu hỏi: dung lượng, độ tin cậy, loại dữ liệu, riêng tư; không viết cứng đường dẫn | ax-storage-overview | guideline |
| Nội bộ mã hóa từ Android 10; ngoài không luôn truy cập được; cache có thể bị xóa khi thiếu chỗ; ảnh người dùng muốn giữ thuộc MediaStore | ax-app-specific | stable |
| DataStore cho dữ liệu nhỏ, không cập nhật từng phần hay ràng buộc tham chiếu → Room | ax-datastore | stable |
| SharedPreferences nạp cả file, mỗi lần ghi ghi lại toàn bộ | aosp-sp-impl | impl |
| Thứ tự bốn câu hỏi dạng bậc thang | site | simplified |

### H2 · File riêng của app
| Khẳng định | Nguồn | Loại |
|---|---|---|
| filesDir, cacheDir không cần quyền; external không cần quyền từ 4.4; openFileOutput khác MODE_PRIVATE ném SecurityException từ 7.0; FileProvider để chia sẻ | ax-app-specific | stable |
| Cache có thể bị xóa khi thiếu bộ nhớ trong; kiểm còn trước khi đọc; đừng trông vào hệ thống dọn; getCacheQuotaBytes, getAllocatableBytes/allocateBytes | ax-app-specific | stable |
| AtomicFile: ghi `.new`, sync rồi đổi tên; startWrite/finishWrite/failWrite; không khóa file | ax-atomicfile | stable |
| Đổi tên đè lên tên có sẵn là nguyên tử | man-rename | impl |
| FileOutputStream không nối thêm cắt file khi mở | Java SE (kiến thức chuẩn, không gắn nguồn trên site) | stable |
