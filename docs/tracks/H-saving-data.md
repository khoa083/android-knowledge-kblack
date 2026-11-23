# TRACK H — Lưu dữ liệu trên Android / Saving Data on Android (`storage`)

> **BẢN NHÁP – CHỜ DUYỆT (2026-11-23).** Chưa tạo manifest, model hay nội dung. Người dùng duyệt IN/OUT và dàn chương trước khi bắt đầu.
> Nguyên tắc: **cần và đủ**; mỗi chương bắt đầu từ một lỗi thật (mất dữ liệu, ANR, crash khi nâng cấp app).

## Nguồn đã đọc để soạn dàn ý
- **Chính thức (thắng khi mâu thuẫn), đã kiểm HTTP 200:** developer.android.com: Data and file storage overview, App-specific storage, Shared storage và MediaStore, DataStore, Room (gồm Relationships, Async queries, Migrating database versions, Testing), Offline-first, Persistent work (WorkManager), Auto Backup.
- **Sách:** *Saving Data on Android* (raywenderlich, đã đọc mục lục): File, SharedPreferences, SQLite, ContentProvider, Room (kiến trúc, entity, quan hệ, DAO, dùng với Architecture Components, migration), rồi 10 chương Firebase. **Sách ra trước DataStore** và còn dùng SharedPreferences làm lựa chọn chính, nên chỉ dùng phần Room, File và SQLite làm nguồn phụ; chỗ nào lệch tài liệu hiện tại thì theo tài liệu và ghi rõ. Thêm Dumbravan ch2, ch7 (Room, DataStore trong một app có kiến trúc).
- **Điểm tài liệu chính thức nói rõ:** nên chuyển từ SharedPreferences sang DataStore; DataStore hợp với dữ liệu nhỏ, không có cập nhật từng phần hay ràng buộc tham chiếu, khi cần những thứ đó thì dùng Room; DataStore hỗ trợ nhiều tiến trình từ bản 1.1.0.

## IN (đưa vào) và lý do
| Nội dung | Lý do |
|---|---|
| Chọn nơi lưu theo loại dữ liệu (file riêng của app, shared storage, DataStore, Room) | Chọn sai là gốc của nhiều lỗi: danh sách lớn trong preferences, file mất khi gỡ app |
| File riêng của app: internal, cache, ghi an toàn | Cache có thể bị hệ thống xóa; file ghi dở khi app bị kill thì hỏng |
| SharedPreferences và vì sao chuyển sang DataStore | ANR do ghi đồng bộ trên main thread; tài liệu khuyên chuyển |
| DataStore: Flow để đọc, cập nhật bằng suspend, giao dịch | Lựa chọn chính thức cho cài đặt và dữ liệu nhỏ |
| Room: entity, DAO, database, truy vấn suspend và Flow | Lựa chọn chính thức cho dữ liệu có cấu trúc; lỗi truy vấn trên main thread |
| Room: quan hệ, @Transaction | Lỗi đọc dữ liệu không nhất quán, truy vấn N+1 |
| Room: migration, auto-migration, kiểm thử migration | Lỗi nguy hiểm nhất: crash sau khi cập nhật app, hoặc migration phá hủy làm mất dữ liệu người dùng |
| Offline-first và đồng bộ nền bằng WorkManager | Thao tác lúc mất mạng bị mất khi app tắt |
| Shared storage và MediaStore (ở mức đủ dùng) | Ảnh, tài liệu người dùng; quyền truy cập đổi theo phiên bản Android |
| Sao lưu (Auto Backup) và dữ liệu nhạy cảm | Dữ liệu được khôi phục sang máy mới mà không ngờ (ví dụ phiên đăng nhập cũ) |

## OUT (bỏ ra hoặc chỉ nhắc) và lý do
| Nội dung | Lý do |
|---|---|
| Firebase (Realtime Database, Firestore, Cloud Storage; 10 chương của sách) | Là dịch vụ backend cụ thể, không phải cơ chế lưu trên máy; chỉ để "đọc thêm" |
| SQLiteOpenHelper và SQL thuần, ContentProvider tự viết | Room thay thế cho app thông thường; ContentProvider chỉ nhắc khi đọc MediaStore |
| SharedPreferences chi tiết | Chỉ đủ để hiểu lỗi và cách chuyển sang DataStore |
| Proto DataStore chi tiết (schema protobuf) | Chỉ một mục so sánh; tập trung Preferences DataStore |
| Paging 3 | Thư viện riêng về hiển thị dữ liệu lớn; "đọc thêm" |
| Mã hóa dữ liệu bằng thư viện bên ngoài | Chỉ nêu nguyên tắc (đừng lưu bí mật ở dạng đọc được); không khẳng định thư viện cụ thể khi chưa kiểm trạng thái của nó |
| Repository, SSOT ở mức kiến trúc | Thuộc track **G** (g4): ở đây chỉ phần cơ chế đồng bộ và lưu |
| Flow, coroutine, Dispatchers.IO | Thuộc track **Coroutines**: chỉ dẫn link |

## Chương (10)
### Phần 1: Nền tảng
| Id | Chương | Lỗi dẫn dắt | Sim (sơ đồ node) | Nguồn chính |
|---|---|---|---|---|
| h1 | Chọn nơi lưu | Danh sách 500 lịch hẹn lưu thành một chuỗi JSON trong SharedPreferences | `storage.choose`: loại dữ liệu → câu hỏi (nhỏ hay lớn, có quan hệ, có chia sẻ với app khác) → nơi lưu | Data and file storage overview; DataStore |
| h2 | File riêng của app | File ghi dở khi app bị kill nên hỏng; ảnh tạm trong cache biến mất | `storage.file`: ghi trực tiếp so với ghi tệp tạm rồi thay thế; cache bị hệ thống dọn | App-specific storage; sách ch1 |
| h3 | Từ SharedPreferences tới DataStore | ANR khi lưu cài đặt bằng commit() trên main thread | `storage.prefs`: ghi qua SharedPreferences (commit/apply) so với DataStore.updateData (suspend), đọc bằng Flow | DataStore; sách ch2 |
| h4 | Room cơ bản | Truy vấn trên main thread; màn hình không tự cập nhật khi dữ liệu đổi | `storage.room`: DAO → mã Room sinh ra → SQLite → Flow phát lại khi bảng đổi | Room; Async queries; sách ch5–8 |
| h5 | Quan hệ và giao dịch | Danh sách bác sĩ kèm lịch hẹn đọc lệch nhau; truy vấn N+1 | `storage.relation`: @Relation và @Transaction so với đọc từng bảng riêng | Relationships; sách ch7 |
| h6 | Migration | Cập nhật app xong là crash; hoặc mất hết lịch hẹn vì migration phá hủy | `storage.migration`: version 1 → 2 với Migration, auto-migration, fallbackToDestructiveMigration | Migrating database versions; Testing; sách ch10 |
### Phần 2: Thực hành sâu
| Id | Chương | Lỗi dẫn dắt | Sim | Nguồn chính |
|---|---|---|---|---|
| h7 | Offline-first và đồng bộ nền | Đặt lịch lúc mất mạng, tắt app, lịch biến mất | `storage.sync`: ghi DB trước, đánh dấu chờ đồng bộ, WorkManager đẩy lên khi có mạng | Offline-first; Persistent work |
| h8 | Shared storage và MediaStore | Lưu ảnh hồ sơ vào thư mục chung theo cách cũ không còn chạy trên Android mới | `storage.media`: ghi qua MediaStore so với đường dẫn tệp trực tiếp, theo phiên bản Android | Shared storage; Media |
| h9 | Sao lưu và dữ liệu nhạy cảm | Đổi máy mới, app khôi phục phiên đăng nhập cũ và lỗi | `storage.backup`: dữ liệu nào được Auto Backup, quy tắc loại trừ | Auto Backup |
| h0 | Bản đồ track (viết CUỐI) | Gặp triệu chứng X thì đọc chương nào | cây triệu chứng → chương | — |

Khuôn mỗi chương như track Kotlin (tối đa 8 mục, 2 lỗi thật, 1 bài tập, quiz 3–4 câu). Bài tập do site tự viết theo ý sách, ghi nguồn ý.

## Cầu nối dự kiến
- h3, h4 ↔ Coroutines (Flow, suspend, Dispatchers).
- h7 ↔ track G g4 (repository, SSOT): G dạy vai trò, H dạy cơ chế lưu và đồng bộ.
- h4 ↔ Kotlin K7 (collection read-only) và K4 (data class làm entity).

## Gợi ý kiểu sơ đồ (báo người dùng, chưa đổi)
h1 (chọn nơi lưu) là **cây quyết định**, giống chương chọn API của track Animation; có thể dễ đọc hơn dạng cây thay cho pipeline bốn khối.

## Câu hỏi cần người dùng quyết
1. Có giữ h8 (shared storage, MediaStore) không, hay bỏ để track gọn hơn (9 chương)?
2. Firebase: bỏ hẳn (đề xuất) hay thêm một chương tổng quan "khi nào cần backend đồng bộ"?
