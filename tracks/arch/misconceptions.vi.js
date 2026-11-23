/* Hiểu lầm track arch (tiếng Việt). */
ADE.addMisconceptions('vi', 'arch', {
  "activity-keeps-data": { wrong: "Dữ liệu giữ trong biến của Activity vẫn còn sau khi xoay màn hình.", right: "Khi đổi cấu hình, hệ thống hủy Activity và tạo instance mới; biến của instance cũ mất theo. Giữ state trong ViewModel. [[src:ax-config-changes]] [[src:ax-viewmodel]]", example: "Chương G1: danh sách giờ trống phải tải lại sau mỗi lần xoay.", chapter: "arch/g1" },
  "domain-required": { wrong: "Kiến trúc chuẩn của Android bắt buộc có domain layer với use case.", right: "Hướng dẫn chính thức yêu cầu tối thiểu UI và data; domain layer là tùy chọn, dùng khi logic phức tạp hay được nhiều ViewModel dùng lại. [[src:ax-arch-guide]]", example: "Màn hình chỉ đọc một danh sách thì use case chuyển tiếp nguyên lời gọi repository là thừa.", chapter: "arch/g1" }
});
