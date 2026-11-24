/* Thuật ngữ track cleancode (tiếng Việt). */
ADE.addGlossary('vi', 'cleancode', {
  "cyclomatic-complexity": { term: "cyclomatic complexity", def: "Số đường đi qua một đoạn mã. Đếm tay theo Seemann: bắt đầu từ 1, mỗi lệnh rẽ nhánh hay lặp (if, for, while, mỗi nhánh when) cộng 1. Cũng là số test tối thiểu để đi qua mọi đường.", chapter: "cleancode/j1" },
  "working-memory": { term: "bộ nhớ làm việc", def: "Phần trí nhớ ngắn hạn giữ những gì đang nghĩ tới. Chỉ chứa được vài mẩu thông tin cùng lúc; Seemann dùng con số 7 làm ngưỡng tượng trưng khi đọc mã.", chapter: "cleancode/j1" },
  "stepdown-rule": { term: "stepdown rule", def: "Quy tắc của Martin: mã đọc từ trên xuống như một câu chuyện, mỗi hàm theo sau bởi các hàm ở mức trừu tượng thấp hơn một bậc.", chapter: "cleancode/j1" },
  "cqs": { term: "command query separation (CQS)", def: "Nguyên tắc của Bertrand Meyer: hàm đổi trạng thái (command) thì không trả dữ liệu; hàm trả dữ liệu (query) thì không đổi trạng thái. Nhờ đó chữ ký đủ để biết hàm đọc hay ghi.", chapter: "cleancode/j2" },
  "observable-side-effect": { term: "side effect (quan sát được)", def: "Thay đổi mà người gọi quan sát được ngoài giá trị trả về: ghi database, xóa cache, sửa field của object, gửi mạng. Sửa biến cục bộ bên trong hàm không tính.", chapter: "cleancode/j2" },
  "flag-argument": { term: "tham số cờ", def: "Tham số Boolean quyết định hàm làm việc này hay việc kia. Martin coi nó là dấu hiệu hàm làm hai việc; tách thành hai hàm có tên.", chapter: "cleancode/j2" },
  "code-rot": { term: "mã mục dần", def: "Mã phức tạp dần qua từng thay đổi nhỏ mà không ai để ý, tới lúc không còn ai dám sửa. Seemann đề xuất đặt ngưỡng cho một chỉ số để chặn nó.", chapter: "cleancode/j1" }
});
