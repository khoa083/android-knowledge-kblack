/* Thuật ngữ track debugging (tiếng Việt). */
ADE.addGlossary('vi', 'debugging', {
  "reproduce": { term: "tái hiện lỗi (reproduce)", def: "Tìm một dãy bước làm lỗi xảy ra mỗi lần chạy. Lỗi tái hiện được đều đặn thì mới kiểm được giả thuyết và bản sửa.", chapter: "debugging/l1" },
  "adb": { term: "adb (Android Debug Bridge)", def: "Công cụ dòng lệnh điều khiển thiết bị Android từ máy tính: cài app, chạy lệnh shell, chép file, lấy bug report. Gồm client, server trên máy tính và daemon adbd trên thiết bị.", chapter: "debugging/l1" },
  "bug-report": { term: "bug report", def: "File ZIP gom log hệ thống, log lỗi, trạng thái dịch vụ hệ thống và stack trace của một thiết bị, dùng để tìm lỗi xảy ra trên máy khác.", chapter: "debugging/l1" },
  "breakpoint": { term: "breakpoint", def: "Điểm dừng đặt ở một dòng mã: khi chạy tới đó, debugger dừng app để bạn xem biến. Có thể kèm điều kiện, chỉ ghi log mà không dừng, hay chỉ dừng luồng chạm nó.", chapter: "debugging/l2" },
  "suspend-policy": { term: "chính sách dừng (suspend policy)", def: "Quyết định luồng nào dừng khi một breakpoint được chạm: All dừng mọi luồng của app, Thread chỉ dừng luồng chạm breakpoint.", chapter: "debugging/l2" },
  "logcat": { term: "Logcat", def: "Nơi xem log của cả thiết bị (hệ thống, app khác, app của bạn), đọc từ buffer vòng của tiến trình logd; lọc bằng truy vấn theo tag, package, mức, tiến trình.", chapter: "debugging/l3" },
  "log-tag": { term: "tag (của log)", def: "Chuỗi ngắn đi kèm mỗi dòng log cho biết nó đến từ đâu, thường là tên lớp; dùng để lọc trong Logcat.", chapter: "debugging/l3" }
});
