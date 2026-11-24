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

### H3 · Từ SharedPreferences tới DataStore
| Khẳng định | Nguồn | Loại |
|---|---|---|
| commit đồng bộ, trả về true khi đã ghi; apply đổi bộ nhớ ngay, ghi bất đồng bộ, không báo lỗi; apply dở có thể chặn main lúc chuyển vòng đời; commit chờ các apply đang dở; Editor sau cùng thắng | ax-sp-editor | stable |
| apply: commitToMemory, QueuedWork.addFinisher, writeToFile ghi cả map rồi sync | aosp-sp-impl | impl |
| ANR khi không phản hồi sự kiện nhập trong 5 giây; I/O trên main là nguyên nhân hay gặp | ax-anr | stable |
| DataStore: Flow, updateData/edit giao dịch nguyên tử; ba quy tắc; nhiều tiến trình từ 1.1.0; bản 1.3.0 | ax-datastore | stable / version |
| SharedPreferencesMigration: kiểu hỗ trợ, không chép lại khóa đã có, cố xóa prefs rỗng, deadlock nếu đọc DataStore trong migration | ax-sp-migration | stable |
| Máy bộ nhớ chậm, đĩa đầy làm apply lỗi | site | simplified |

### H4 · Room cơ bản
| Khẳng định | Nguồn | Loại |
|---|---|---|
| Ba phần (database, entity, DAO); kiểm SQL lúc biên dịch; một instance mỗi tiến trình; hướng dẫn dùng Room 3.0 `androidx.room3`, KSP, setDriver | ax-room | stable / version |
| Không truy cập database trên main thread; ba loại truy vấn; suspend và Flow; Room 3.0 bắt buộc suspend cho truy vấn một lần | ax-room-async | stable / version |
| Flow chạy lại khi bất kỳ dòng nào của bảng được tham chiếu đổi; distinctUntilChanged; invalidationTracker.createFlow | ax-room-async | stable |
| @Insert trả rowId; @Update/@Delete theo khóa chính, trả số dòng; @Upsert; @Query kiểm lúc biên dịch | ax-room-dao | stable |
| Room 2.x: IllegalStateException khi truy vấn trên main, allowMainThreadQueries | kiến thức bản cũ, ghi rõ trên site là Room 2.x | version |

### H5 · Quan hệ và giao dịch
| Khẳng định | Nguồn | Loại |
|---|---|---|
| Room cấm tham chiếu đối tượng giữa entity; lớp trung gian (@Embedded, @Relation) hay multimap; khuyên multimap nếu không có lý do; multimap để SQL làm nhiều hơn | ax-room-relations | stable |
| @Relation cần hai truy vấn → thêm @Transaction để nguyên tử; nhiều–nhiều: bảng nối + Junction; cú pháp Room 3.0 parentColumns/entityColumns | ax-room-relations | stable / version |
| @Transaction: SELECT nhất quán, @Relation truy vấn riêng; hàm không trừu tượng chạy trong một giao dịch; @Insert/@Update/@Delete vốn có giao dịch; tối đa một giao dịch mỗi lúc, xếp hàng | ax-room-transaction | stable |
| 1 + N truy vấn, đồng bộ chen giữa làm kết quả lệch | site (minh họa) | simplified |

### H6 · Migration
| Khẳng định | Nguồn | Loại |
|---|---|---|
| Migration(start, end), addMigrations; câu truy vấn đầy đủ thay vì hằng; tay thắng tự động cùng phiên bản | ax-room-migrations | stable |
| Thiếu đường → IllegalStateException (trang không nêu nguyên văn thông báo) | ax-room-migrations | stable |
| fallbackToDestructiveMigration xóa vĩnh viễn; biến thể From và OnDowngrade | ax-room-migrations | stable |
| AutoMigration cần schema đã xuất; spec @RenameColumn/@DeleteColumn/@RenameTable/@DeleteTable cho thay đổi mơ hồ | ax-room-migrations | stable |
| Kiểm schema sau khi chạy hết migration; MigrationTestHelper createDatabase / runMigrationsAndValidate; không dùng DAO trong test vì schema mới nhất | ax-room-migrations | stable |
| Room 3.0: migrate(connection: SQLiteConnection) suspend, plugin androidx.room3 schemaDirectory; Room 2.x: SupportSQLiteDatabase | ax-room-migrations / bản cũ | version |

### H7 · Offline-first và đồng bộ nền
| Khẳng định | Nguồn | Loại |
|---|---|---|
| Nguồn cục bộ là nguồn sự thật; ba chiến lược ghi online-only / queued / lazy và khi nào dùng; lazy có thể sinh xung đột; last write wins | ax-offline-first-data | guideline |
| Hàng chờ có thể giữ trong Room, rút bằng WorkManager; ví dụ enqueueUniqueWork KEEP, NetworkType.CONNECTED, Result.retry → backoff lũy thừa | ax-offline-first-data | stable |
| WorkManager sống qua tắt app và khởi động lại; lưu trong SQLite nội bộ; coroutine dừng khi app đóng; ràng buộc, công việc duy nhất, backoff | ax-persistent-work | stable |
| Cột PENDING/SYNCED, id do máy sinh chống gửi trùng, bài tập Hủy lịch | site | simplified |

### H8 · Shared storage và MediaStore
| Khẳng định | Nguồn | Loại |
|---|---|---|
| Bộ sưu tập Images/Video/Audio/Downloads (Downloads từ 10); insert + ContentValues; DISPLAY_NAME, RELATIVE_PATH thay cột DATA; IS_PENDING từ 10 | ax-shared-media | stable |
| Từ 10 không cần quyền cho media của chính app; ≤9 cần READ/WRITE_EXTERNAL_STORAGE (WRITE maxSdkVersion 29); requestLegacyExternalStorage ở 10; File/fopen từ 11, ngẫu nhiên chậm tới gấp đôi | ax-shared-media | version |
| WRITE_EXTERNAL_STORAGE vô hiệu khi target ≥ 30 | ax-storage-overview | version |
| READ_MEDIA_IMAGES/VIDEO bị Play giới hạn, khuyên photo picker; cài lại cần quyền đọc để thấy file cũ | ax-shared-media | stable |
| Photo picker: androidx.activity 1.7.0+, có sẵn từ 11, backport 4.4–10 qua Play services, fallback ACTION_OPEN_DOCUMENT, takePersistableUriPermission (giới hạn 5.000) | ax-photo-picker | stable |
| getExternalStoragePublicDirectory deprecated từ API 29 | kiến thức API reference, không gắn nguồn trên site | version |
