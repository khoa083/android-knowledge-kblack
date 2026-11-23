# TRACK H — Lưu dữ liệu trên Android / Saving Data on Android (`storage`)

> **ĐÃ DUYỆT (2026-11-24).** Người dùng duyệt IN/OUT và dàn chương. Hai câu hỏi cuối theo mặc định (người dùng đổi được): **giữ h8**, **bỏ hẳn Firebase**. Chưa xây; làm sau khi xong track G.
> Nguyên tắc: **cần và đủ**. Mỗi chương bắt đầu từ một lỗi thật: mất dữ liệu, ANR, crash khi nâng cấp app.

## Manifest đề xuất
| Trường | Giá trị |
|---|---|
| id / code / order | `storage` / H / 80 |
| domain | engineering |
| Tên vi / en | Lưu dữ liệu trên Android / Saving Data on Android |
| level / estMinutes | intermediate / 300 |
| prerequisites | [] (nên đọc Kotlin K1–K7 và Coroutines A1–A3 trước) |
| status | `draft` trong lúc viết, `stable` sau h0 |
| Ví dụ xuyên suốt | App hư cấu "Hẹn Khám": cài đặt, danh sách lịch hẹn, ảnh hồ sơ |

## Nguồn đã đọc để soạn dàn ý
- **Chính thức (thắng khi mâu thuẫn), đã kiểm HTTP 200.** Các trang trên developer.android.com:
  - Data and file storage overview;
  - App-specific storage;
  - Shared storage và MediaStore;
  - DataStore;
  - Room, gồm Relationships, Async queries, Migrating database versions, Testing;
  - Offline-first;
  - Persistent work (WorkManager);
  - Auto Backup.
- **Sách *Saving Data on Android* (raywenderlich), đã đọc mục lục:**
  - nội dung: File, SharedPreferences, SQLite, ContentProvider, Room (kiến trúc, entity, quan hệ, DAO, dùng với Architecture Components, migration), rồi 10 chương Firebase;
  - **sách ra trước DataStore** và vẫn lấy SharedPreferences làm lựa chọn chính, nên chỉ dùng phần Room, File và SQLite làm nguồn phụ;
  - chỗ nào lệch tài liệu hiện tại thì theo tài liệu và ghi rõ.
- **Sách khác:** Dumbravan ch2 và ch7 (Room, DataStore trong một app có kiến trúc).
- **Những điểm tài liệu chính thức nói rõ:**
  - nên chuyển từ SharedPreferences sang DataStore;
  - DataStore hợp với dữ liệu nhỏ, không có cập nhật từng phần hay ràng buộc tham chiếu; khi cần những thứ đó thì dùng Room;
  - DataStore hỗ trợ nhiều tiến trình từ bản 1.1.0.

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
| Firebase lưu dữ liệu (Realtime Database, Firestore, Cloud Storage; 10 chương của sách) | Là dịch vụ backend cụ thể, không phải cơ chế lưu trên máy; chỉ để "đọc thêm". (Thông báo đẩy FCM là chuyện khác, thuộc track **I**.) |
| SQLiteOpenHelper và SQL thuần, ContentProvider tự viết | Room thay thế cho app thông thường; ContentProvider chỉ nhắc khi đọc MediaStore |
| SharedPreferences chi tiết | Chỉ đủ để hiểu lỗi và cách chuyển sang DataStore |
| Proto DataStore chi tiết (schema protobuf) | Chỉ một mục so sánh; tập trung Preferences DataStore |
| Paging 3 | Thư viện riêng về hiển thị dữ liệu lớn; phân trang ở mức thiết kế thuộc track **I** |
| Mã hóa dữ liệu bằng thư viện bên ngoài | Chỉ nêu nguyên tắc (đừng lưu bí mật ở dạng đọc được); không khẳng định thư viện cụ thể khi chưa kiểm trạng thái của nó |
| Repository, SSOT ở mức kiến trúc | Thuộc track **G** (g4): ở đây chỉ phần cơ chế đồng bộ và lưu |
| Xung đột khi nhiều thiết bị cùng sửa | Thuộc track **I** (i8): ở đây chỉ hàng đợi thao tác chờ gửi trên một máy |
| Flow, coroutine, Dispatchers.IO | Thuộc track **Coroutines**: chỉ dẫn link |

## Chương (10)
Cột **Hình chính** là tab mặc định; sơ đồ node của sim ở tab phụ. Mọi kiểu hình ở đây đã có cách vẽ (xem `docs/chapter-template-v2.md`), trừ h7 cần **sơ đồ tuần tự MỚI** (viết ở track I hoặc ở đây, tùy track nào làm trước).

### Phần 1: Nền tảng
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| h1 | Chọn nơi lưu | Danh sách 500 lịch hẹn lưu thành một chuỗi JSON trong SharedPreferences | `storage.choose`: loại dữ liệu → câu hỏi (nhỏ hay lớn, có quan hệ, có chia sẻ với app khác) → nơi lưu | **Cây quyết định** (như Animation C0): mỗi câu hỏi là một nhánh, lá là nơi lưu và chương | Data and file storage overview; DataStore |
| h2 | File riêng của app | File ghi dở khi app bị kill nên hỏng; ảnh tạm trong cache biến mất | `storage.file`: ghi trực tiếp so với ghi tệp tạm rồi thay thế; cache bị hệ thống dọn | **Làn thời gian** app, hệ thống, tệp trên đĩa: thấy cú kill cắt ngang lúc ghi, và tệp còn nguyên hay hỏng | App-specific storage; sách ch1 |
| h3 | Từ SharedPreferences tới DataStore | ANR khi lưu cài đặt bằng commit() trên main thread | `storage.prefs`: ghi qua SharedPreferences (commit/apply) so với DataStore.updateData (suspend), đọc bằng Flow | **Làn thời gian** main thread và luồng IO: đoạn main bị chặn hiện thành thanh dài | DataStore; sách ch2 |
| h4 | Room cơ bản | Truy vấn trên main thread; màn hình không tự cập nhật khi dữ liệu đổi | `storage.room`: DAO → mã Room sinh ra → SQLite → Flow phát lại khi bảng đổi | (1) **Luồng** DAO → mã sinh → SQLite → Flow. (2) **Bảng** "bảng nào đổi → truy vấn nào phát lại" | Room; Async queries; sách ch5–8 |
| h5 | Quan hệ và giao dịch | Danh sách bác sĩ kèm lịch hẹn đọc lệch nhau; truy vấn N+1 | `storage.relation`: @Relation và @Transaction so với đọc từng bảng riêng | **Bảng** các dòng hai bảng và kết quả ghép, kèm **bảng tính** số truy vấn (1 + N so với 2) | Relationships; sách ch7 |
| h6 | Migration | Cập nhật app xong là crash; hoặc mất hết lịch hẹn vì migration phá hủy | `storage.migration`: version 1 → 2 với Migration, auto-migration, fallbackToDestructiveMigration | **Dãy ô** các phiên bản schema v1 → v2 → v3, mỗi mũi tên là một migration có hay thiếu; đường thiếu tô đỏ | Migrating database versions; Testing; sách ch10 |

### Phần 2: Thực hành sâu
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| h7 | Offline-first và đồng bộ nền | Đặt lịch lúc mất mạng, tắt app, lịch biến mất | `storage.sync`: ghi DB trước, đánh dấu chờ đồng bộ, WorkManager đẩy lên khi có mạng | **Sơ đồ tuần tự MỚI** app, DB, WorkManager, server; kèm **bảng** hàng chờ gửi đổi trạng thái theo từng bước | Offline-first; Persistent work |
| h8 | Shared storage và MediaStore | Lưu ảnh hồ sơ vào thư mục chung theo cách cũ không còn chạy trên Android mới | `storage.media`: ghi qua MediaStore so với đường dẫn tệp trực tiếp, theo phiên bản Android | **Ma trận** phiên bản Android × cách ghi (chạy, cần quyền, bị chặn) | Shared storage; Media |
| h9 | Sao lưu và dữ liệu nhạy cảm | Đổi máy mới, app khôi phục phiên đăng nhập cũ và lỗi | `storage.backup`: dữ liệu nào được Auto Backup, quy tắc loại trừ | **Cây** thư mục của app, mỗi nhánh đánh dấu được sao lưu hay bị loại trừ | Auto Backup |
| h0 | Bản đồ track (viết CUỐI) | Gặp triệu chứng X thì đọc chương nào | `storage.map` | **Bảng tra** triệu chứng → chương | — |

Khuôn mỗi chương như track Kotlin:
- tối đa 8 mục;
- 2 lỗi thật;
- 1 bài tập;
- quiz 3–4 câu.

Bài tập do site tự viết theo ý sách, có ghi nguồn ý.

## Cầu nối dự kiến
- h3, h4 ↔ Coroutines (Flow, suspend, Dispatchers).
- h7 ↔ G g4 (repository, SSOT): G dạy vai trò, H dạy cơ chế lưu và đồng bộ.
- h7 ↔ I i8 (xung đột giữa nhiều thiết bị).
- h4 ↔ Kotlin K7 (collection read-only) và K4 (data class làm entity).

## Hai câu hỏi đã có mặc định (người dùng đổi được)
1. Giữ h8 (shared storage, MediaStore), track 10 chương.
2. Firebase lưu dữ liệu: bỏ hẳn, chỉ để "đọc thêm".
