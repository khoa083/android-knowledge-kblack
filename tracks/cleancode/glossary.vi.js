/* Thuật ngữ track cleancode (tiếng Việt). */
ADE.addGlossary('vi', 'cleancode', {
  "cyclomatic-complexity": { term: "cyclomatic complexity", def: "Số đường đi qua một đoạn mã. Đếm tay theo Seemann: bắt đầu từ 1, mỗi lệnh rẽ nhánh hay lặp (if, for, while, mỗi nhánh when) cộng 1. Cũng là số test tối thiểu để đi qua mọi đường.", chapter: "cleancode/j1" },
  "working-memory": { term: "bộ nhớ làm việc", def: "Phần trí nhớ ngắn hạn giữ những gì đang nghĩ tới. Chỉ chứa được vài mẩu thông tin cùng lúc; Seemann dùng con số 7 làm ngưỡng tượng trưng khi đọc mã.", chapter: "cleancode/j1" },
  "stepdown-rule": { term: "stepdown rule", def: "Quy tắc của Martin: mã đọc từ trên xuống như một câu chuyện, mỗi hàm theo sau bởi các hàm ở mức trừu tượng thấp hơn một bậc.", chapter: "cleancode/j1" },
  "code-rot": { term: "mã mục dần", def: "Mã phức tạp dần qua từng thay đổi nhỏ mà không ai để ý, tới lúc không còn ai dám sửa. Seemann đề xuất đặt ngưỡng cho một chỉ số để chặn nó.", chapter: "cleancode/j1" }
});
