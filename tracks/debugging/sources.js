/* Nguồn của track L (Gỡ lỗi và hiệu năng Android). Tài liệu chính thức đọc từ 2026-11-25 (docs/research/debugging.md). */
(function () {
  var s = function (id, title, url, org, label, vi, en) { return { id: id, title: title, url: url, org: org, tracks: ['debugging'], label: label, lang: 'en', supports: { vi: vi, en: en } }; };
  ADE.addSources([
    s('ad-adb', 'Android Debug Bridge (adb)', 'https://developer.android.com/tools/adb', 'Android Developers', 'stable',
      'adb gồm client, server (cổng TCP 5037) và daemon adbd trên thiết bị; USB debugging trong tùy chọn nhà phát triển, gỡ lỗi không dây từ Android 11; adb devices, install, shell, pull, push; am start, am kill (chỉ đóng tiến trình đóng được an toàn) (đọc 2026-11-25) (chương "Quy trình gỡ lỗi, adb và bug report").',
      'adb has a client, a server (TCP port 5037) and the adbd daemon on the device; USB debugging in the developer options, wireless debugging from Android 11; adb devices, install, shell, pull, push; am start, am kill (kills only processes that are safe to kill) (read 2026-11-25) (chapter "The debugging process, adb and bug reports").'),
    s('ad-bug-report', 'Capture and read bug reports', 'https://developer.android.com/studio/debug/bug-report', 'Android Developers', 'stable',
      'Bug report chứa log thiết bị, stack trace và thông tin chẩn đoán; lấy bằng mục Take bug report, menu emulator hay adb bugreport; file ZIP với bugreport-*.txt gồm dumpsys, dumpstate, logcat; Play Console và Firebase Crashlytics thu crash và ANR của người dùng (đọc 2026-11-25) (chương "Quy trình gỡ lỗi, adb và bug report").',
      'A bug report holds device logs, stack traces and diagnostic information; capture it with Take bug report, the emulator menu or adb bugreport; a ZIP file whose bugreport-*.txt has dumpsys, dumpstate and logcat output; Play Console and Firebase Crashlytics collect crashes and ANRs from users (read 2026-11-25) (chapter "The debugging process, adb and bug reports").'),
    s('ad-debug', 'Debug your app', 'https://developer.android.com/studio/debug', 'Android Developers', 'stable',
      'Đặt breakpoint trong mã Java, Kotlin, C/C++, xem biến và tính biểu thức lúc chạy; thiết bị thật cần bật gỡ lỗi trong tùy chọn nhà phát triển; biến thể build phải debuggable (đọc 2026-11-25) (chương "Quy trình gỡ lỗi, adb và bug report").',
      'Set breakpoints in Java, Kotlin and C/C++ code, examine variables and evaluate expressions at runtime; a real device needs debugging enabled in the developer options; the build variant must be debuggable (read 2026-11-25) (chapter "The debugging process, adb and bug reports").')
  ]);
})();
