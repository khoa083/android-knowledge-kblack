/* Thuật ngữ track debugging (tiếng Việt). */
ADE.addGlossary('vi', 'debugging', {
  "reproduce": { term: "tái hiện lỗi (reproduce)", def: "Tìm một dãy bước làm lỗi xảy ra mỗi lần chạy. Lỗi tái hiện được đều đặn thì mới kiểm được giả thuyết và bản sửa.", chapter: "debugging/l1" },
  "adb": { term: "adb (Android Debug Bridge)", def: "Công cụ dòng lệnh điều khiển thiết bị Android từ máy tính: cài app, chạy lệnh shell, chép file, lấy bug report. Gồm client, server trên máy tính và daemon adbd trên thiết bị.", chapter: "debugging/l1" },
  "bug-report": { term: "bug report", def: "File ZIP gom log hệ thống, log lỗi, trạng thái dịch vụ hệ thống và stack trace của một thiết bị, dùng để tìm lỗi xảy ra trên máy khác.", chapter: "debugging/l1" },
  "breakpoint": { term: "breakpoint", def: "Điểm dừng đặt ở một dòng mã: khi chạy tới đó, debugger dừng app để bạn xem biến. Có thể kèm điều kiện, chỉ ghi log mà không dừng, hay chỉ dừng luồng chạm nó.", chapter: "debugging/l2" },
  "suspend-policy": { term: "chính sách dừng (suspend policy)", def: "Quyết định luồng nào dừng khi một breakpoint được chạm: All dừng mọi luồng của app, Thread chỉ dừng luồng chạm breakpoint.", chapter: "debugging/l2" },
  "logcat": { term: "Logcat", def: "Nơi xem log của cả thiết bị (hệ thống, app khác, app của bạn), đọc từ buffer vòng của tiến trình logd; lọc bằng truy vấn theo tag, package, mức, tiến trình.", chapter: "debugging/l3" },
  "log-tag": { term: "tag (của log)", def: "Chuỗi ngắn đi kèm mỗi dòng log cho biết nó đến từ đâu, thường là tên lớp; dùng để lọc trong Logcat.", chapter: "debugging/l3" },
  "stack-trace": { term: "stack trace", def: "Ảnh chụp chuỗi lời gọi hàm tại lúc một ngoại lệ được ném: dòng đầu là loại ngoại lệ và thông điệp, mỗi dòng \"at\" là một frame, frame trên cùng là chỗ ném.", chapter: "debugging/l4" },
  "root-cause": { term: "nguyên nhân gốc (root cause)", def: "Ngoại lệ đầu tiên trong chuỗi bọc lỗi, thường ở phần \"Caused by\" cuối cùng của stack trace; các tầng trên chỉ thêm ngữ cảnh.", chapter: "debugging/l4" },
  "mapping-file": { term: "file mapping (mapping.txt)", def: "File R8 ghi lúc build release, đối chiếu tên rối với tên thật của lớp, hàm, trường kèm khoảng số dòng; mỗi lần build một file, phải lưu theo phiên bản để dịch ngược stack trace.", chapter: "debugging/l5" },
  "keep-rule": { term: "keep rule", def: "Quy tắc báo R8 giữ nguyên tên hay không bỏ một lớp, hàm, trường; cần cho mã được tìm bằng tên qua reflection.", chapter: "debugging/l5" }
});
