# Nghiên cứu track M (Nền tảng Android: component và vòng đời)

> Dàn ý soạn và được duyệt 2026-11-25, chưa xây. Dàn ý nằm ở `docs/tracks/M-android-platform.md`. Khi có mâu thuẫn, nguồn chính thức thắng.

## Đã đọc để soạn dàn ý (2026-11-25, chỉ mục lục)

### Sách
- **Big Nerd Ranch, *Android Programming* bản 5** (EPUB):
  - ch.3–4: vòng đời và giữ state;
  - ch.7–9: Activity thứ hai, SDK, Fragment;
  - ch.13–14: điều hướng giữa Fragment, DialogFragment;
  - ch.16–18: implicit intent, chụp ảnh qua intent, tài nguyên theo cấu hình;
  - ch.22: WorkManager và thông báo.
- **Späth, *Pro Android with Kotlin* bản 2** (EPUB). Mục lục NCX chỉ có một cấp, nên các tiêu đề h1–h3 được lấy thẳng từ HTML của chương.
  - ch.1–7: hệ thống, Application, Activity, Service, Broadcast, Content Provider, Permission;
  - ch.8: Scheduling, Notifications;
  - ch.9: Handler, Fragment;
  - ch.19: CLI.
- **Laurence và cộng sự, *Programming Android with Kotlin*** (EPUB): ch.3–4.
- **Kickstart Modern Android Development** (PDF; bookmark lấy từ `docs/androidbooks-knowledge/catalog.json`, mục B100): ch.2, ch.5, ch.12.

### URL đã kiểm, cả 50 trang trả HTTP 200 bằng curl ngày 2026-11-25
Danh sách đầy đủ nằm ở mục "Nguồn" của dàn ý. Mọi trang đều thuộc developer.android.com.

### Chưa đọc nội dung, phải đọc khi viết
- Các trang behavior changes của Android 14, 15 và 16. Lấy ở đó mọi luật đổi theo phiên bản, kèm ngày đọc.
- Mã AOSP của ActivityThread, Looper, MessageQueue và ZygoteInit. Khi đọc phải ghi tag nhánh.

### Ranh giới với các track đã có (đã đọc tiêu đề mục)
| Chương đã có | Nội dung | Ranh giới với M |
|---|---|---|
| i2 | Form trong ViewModel hay trong saved state; process bị lmkd giết khi mở Camera | m5 chỉ dạy ma trận sống sót và giới hạn Bundle, rồi dẫn link sang i2 |
| g3 | Sự kiện "Đã đặt lịch" qua một lần xoay | m5 chỉ dạy vì sao ViewModel sống qua lần xoay (ViewModelStore) |
| h7 | Đồng bộ offline bằng WorkManager | m13 dạy cách chọn công cụ và cơ chế của WorkManager |
| l7 | Đọc trạng thái worker bằng Background Task Inspector | Không lặp lại |

## Bảng nguồn theo chương
Điền dần khi viết từng chương, theo cùng mẫu với `docs/research/debugging.md`.
