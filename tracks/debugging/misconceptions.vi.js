/* Hiểu lầm track debugging (tiếng Việt). */
ADE.addMisconceptions('vi', 'debugging', {
  "no-crash-means-fixed": { wrong: "Hết crash nghĩa là đã sửa xong lỗi.", right: "Bản sửa có thể chỉ giấu lỗi, như một phép kiểm biến crash thành màn trống. Đã sửa khi biết nguyên nhân, sửa đúng chỗ đó, và có test đỏ trước, xanh sau.", example: "Chương \"Quy trình gỡ lỗi, adb và bug report\": thêm if (!::booking.isInitialized) return làm hết crash nhưng 3 kịch bản ra màn trống.", chapter: "debugging/l1" },
  "cannot-reproduce-means-no-bug": { wrong: "Không tái hiện được trên máy dev thì không có lỗi.", right: "Máy dev hiếm khi gặp điều kiện của người dùng: tiến trình bị đóng ở nền, đổi ngôn ngữ, giao diện tối, mạng chậm. Lấy bug report hay stack trace để biết điều kiện rồi giả nó.", example: "Chương \"Quy trình gỡ lỗi, adb và bug report\": kịch bản 6 dùng adb shell am kill để giả việc hệ thống đóng tiến trình.", chapter: "debugging/l1" }
});
