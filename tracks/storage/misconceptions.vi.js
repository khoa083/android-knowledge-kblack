/* Hiểu lầm track storage (tiếng Việt). */
ADE.addMisconceptions('vi', 'storage', {
  "prefs-for-lists": { wrong: "Danh sách dài cứ chuyển thành JSON rồi lưu một chuỗi trong SharedPreferences là được.", right: "SharedPreferences nạp cả file vào bộ nhớ và mỗi lần ghi lại ghi toàn bộ file; sửa một lịch hẹn cũng phải ghi lại cả 500. Dữ liệu nhiều bản ghi, cần truy vấn hay sửa từng dòng thì dùng Room. [[src:aosp-sp-impl]] [[src:ax-datastore]]", example: "Chương H1: 500 lịch hẹn trong một chuỗi JSON.", chapter: "storage/h1" },
  "cache-is-safe": { wrong: "File trong cacheDir còn đó tới khi app tự xóa.", right: "Khi máy thiếu dung lượng, hệ thống có thể xóa file cache. Chỉ để ở đó thứ tạo lại hay tải lại được, và kiểm file còn trước khi đọc. [[src:ax-app-specific]]", example: "Chương H1: bản PDF kết quả khám để trong cache vì tải lại được.", chapter: "storage/h1" }
});
