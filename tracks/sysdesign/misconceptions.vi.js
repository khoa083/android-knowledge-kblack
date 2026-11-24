/* Hiểu lầm track sysdesign (tiếng Việt). */
ADE.addMisconceptions('vi', 'sysdesign', {
  "design-is-complete": { wrong: "Bản thiết kế màn hình đã đủ để bắt đầu viết mã.", right: "Bản thiết kế thường chỉ vẽ trường hợp đẹp: nội dung gọn, mạng tốt. Lỗi, rỗng, mất mạng, hết phiên và mã lỗi phải hỏi designer và backend trước. [[src:book-tjeerd]]", example: "Chương I1: sáu câu hỏi đổi thành sáu yêu cầu phụ.", chapter: "sysdesign/i1" },
  "viewmodel-survives-death": { wrong: "ViewModel giữ dữ liệu qua mọi thứ, nên form trong ViewModel là an toàn.", right: "ViewModel sống qua đổi cấu hình, nhưng mất khi hệ thống giết process. Phần nhỏ người dùng vừa nhập phải vào saved state; phần lớn hay cần giữ lâu vào lưu trữ bền. [[src:ax-saving-states]]", example: "Chương I2: mở Camera, process bị giết, quay lại thì form trống.", chapter: "sysdesign/i2" }
});
