# Nghiên cứu track L (Gỡ lỗi và hiệu năng Android)

> Track đã duyệt 2026-11-24, chưa xây. Dàn ý: `docs/tracks/L-debugging-performance.md`. Nguồn chính thức thắng khi mâu thuẫn.

## Đã đọc để soạn dàn ý (2026-11-24, chỉ mục lục)
- **Kodeco, *Android Debugging by Tutorials*:** ch.1–12, lấy từ bookmark PDF trong catalog. PDF không có lớp text nên khi viết phải đọc dạng ảnh trang.
- **Kodeco, *Android Test-Driven Development*:** ch.12–14.
- **URL kiểm HTTP 200 bằng curl ngày 2026-11-24:**
  - developer.android.com:
    - studio/debug, studio/debug/logcat, studio/debug/layout-inspector;
    - studio/inspect/task;
    - studio/profile, studio/profile/memory-profiler, studio/profile/record-traces, studio/debug/network-profiler;
    - topic/performance/tracing, topic/performance/vitals, topic/performance/vitals/anr, topic/performance/memory;
    - build/shrink-code, studio/command-line/retrace;
    - reference/android/os/StrictMode;
    - topic/performance/benchmarking/macrobenchmark-overview;
    - tools/adb, studio/debug/bug-report.
  - Ngoài developer.android.com: perfetto.dev/docs, square.github.io/leakcanary.
  - Trả 404: studio/inspect/database-inspector. Phải tìm đường dẫn mới.
- **Chưa xác minh:** Energy Profiler (ch.12 của sách) còn trong bản Android Studio hiện tại không.

## Bảng nguồn theo chương
Điền khi viết từng chương. Ghi phiên bản Android Studio đã đối chiếu.

### l1 Quy trình gỡ lỗi, adb và bug report (đọc 2026-11-25, trang không ghi ngày cập nhật)
| Ý trên site | Nguồn |
|---|---|
| adb gồm client, server (cổng TCP 5037), daemon adbd; USB debugging; gỡ lỗi không dây từ Android 11; adb devices, install, shell, pull, push; am start, am kill (chỉ đóng tiến trình đóng được an toàn) | developer.android.com/tools/adb |
| Bug report chứa log, stack trace, thông tin chẩn đoán; lấy bằng Take bug report, emulator, adb bugreport; ZIP với bugreport-*.txt gồm dumpsys, dumpstate, logcat; Play Console và Crashlytics thu crash, ANR của người dùng | developer.android.com/studio/debug/bug-report |
| Breakpoint trong Java, Kotlin, C/C++; xem biến, tính biểu thức; bật gỡ lỗi trên thiết bị; biến thể build debuggable | developer.android.com/studio/debug (trang ngắn; chi tiết breakpoint ở tài liệu IntelliJ IDEA, sẽ đọc cho l2) |
| **Của site:** vòng tái hiện, thu hẹp, giả thuyết, kiểm, khóa bằng test; 8 kịch bản thao tác, 4 làm màn hình bị tạo lại; Fragment nhận dữ liệu qua setter; khóa dọc còn 3 crash, phép kiểm isInitialized thành 3 màn trống; truyền id qua arguments và test FragmentScenario.recreate | — |
- Sách Android Debugging by Tutorials chưa đọc cho l1 (PDF không có lớp text); chương này chỉ dựa trên tài liệu chính thức.

### l2 Debugger: breakpoint, watch, evaluate (đọc 2026-11-25)
| Ý trên site | Nguồn |
|---|---|
| Bốn loại breakpoint (dòng, hàm vào/ra, watchpoint trên trường, ngoại lệ); điều kiện tính mỗi lần chạm, có thể có side effect; Suspend tắt thì chỉ ghi log hay làm cò; chính sách All và Thread; Evaluate and log; Remove once hit; breakpoint phụ thuộc; pass count; breakpoint hàm được mô phỏng vì bản thật chậm | jetbrains.com/help/idea/using-breakpoints.html (IntelliJ IDEA 2026.3, ngày trang 17/11/2026) |
| Watch tính lại mỗi bước, có thể nặng; watch và evaluate chỉ chạy khi dừng ở breakpoint; evaluate tính mọi biểu thức kể cả gọi hàm; cảnh báo side effect; breakpoint trong hàm được gọi lúc evaluate bị bỏ qua | jetbrains.com/help/idea/examining-suspended-program.html |
| Chế độ debug của kotlinx-coroutines (tên coroutine, -Dkotlinx.coroutines.debug, -ea, chi phí không đáng kể); khôi phục stack trace, cause là ngoại lệ gốc, frame _COROUTINE._BOUNDARY; DebugProbes không chạy trên Android | kotlinlang.org/docs/coroutines-debugging.html (1.11.0, ngày trang 07/09/2026); kotlinx-coroutines-debug README |
| **Của site:** 500 lịch, đơn 347 giảm 120 % (phí −40.000); 348 lần dừng so với 1; luồng đồng bộ nhịp mỗi giây, hạn 10 giây, xem biến 30 giây | — |
- Trang kotlinlang.org/docs/debug-coroutines-using-intellij.html trả 404 (2026-11-25); trang developer.android.com/studio/debug không có chi tiết breakpoint.
