/* Thuật ngữ track cleancode (tiếng Việt). */
ADE.addGlossary('vi', 'cleancode', {
  "cyclomatic-complexity": { term: "cyclomatic complexity", def: "Số đường đi qua một đoạn mã. Đếm tay theo Seemann: bắt đầu từ 1, mỗi lệnh rẽ nhánh hay lặp (if, for, while, mỗi nhánh when) cộng 1. Cũng là số test tối thiểu để đi qua mọi đường.", chapter: "cleancode/j1" },
  "working-memory": { term: "bộ nhớ làm việc", def: "Phần trí nhớ ngắn hạn giữ những gì đang nghĩ tới. Chỉ chứa được vài mẩu thông tin cùng lúc; Seemann dùng con số 7 làm ngưỡng tượng trưng khi đọc mã.", chapter: "cleancode/j1" },
  "stepdown-rule": { term: "stepdown rule", def: "Quy tắc của Martin: mã đọc từ trên xuống như một câu chuyện, mỗi hàm theo sau bởi các hàm ở mức trừu tượng thấp hơn một bậc.", chapter: "cleancode/j1" },
  "cqs": { term: "command query separation (CQS)", def: "Nguyên tắc của Bertrand Meyer: hàm đổi trạng thái (command) thì không trả dữ liệu; hàm trả dữ liệu (query) thì không đổi trạng thái. Nhờ đó chữ ký đủ để biết hàm đọc hay ghi.", chapter: "cleancode/j2" },
  "observable-side-effect": { term: "side effect (quan sát được)", def: "Thay đổi mà người gọi quan sát được ngoài giá trị trả về: ghi database, xóa cache, sửa field của object, gửi mạng. Sửa biến cục bộ bên trong hàm không tính.", chapter: "cleancode/j2" },
  "flag-argument": { term: "tham số cờ", def: "Tham số Boolean quyết định hàm làm việc này hay việc kia. Martin coi nó là dấu hiệu hàm làm hai việc; tách thành hai hàm có tên.", chapter: "cleancode/j2" },
  "parse-dont-validate": { term: "parse, don't validate", def: "Thay vì kiểm hợp lệ rồi trả Boolean, chuyển dữ liệu thô thành kiểu của miền (hoặc từ chối) ngay ở ranh giới. Kiểu mang theo bảo đảm, nên bên trong không phải kiểm lại. Cách gọi của Alexis King, Seemann trích.", chapter: "cleancode/j3" },
  "class-invariant": { term: "bất biến của lớp", def: "Điều kiện luôn đúng với mọi object của lớp, ví dụ số điện thoại luôn đúng định dạng. Với object bất biến, chỉ cần kiểm ở constructor.", chapter: "cleancode/j3" },
  "postels-law": { term: "luật Postel", def: "Thận trọng với những gì gửi đi, dễ dãi với những gì nhận vào. Seemann dùng cho thiết kế API: nhận đầu vào chừng nào còn làm việc được với nó, không được thì từ chối ngay.", chapter: "cleancode/j3" },
  "red-green-refactor": { term: "đỏ, xanh, refactor", def: "Vòng của TDD: viết một test đỏ; thay đổi tối thiểu để mọi test xanh; cải thiện mã mà không đổi hành vi; lặp lại.", chapter: "cleancode/j4" },
  "triangulation": { term: "tam giác hóa", def: "Thêm ví dụ cho tới khi cài đặt đơn giản sai không còn qua được test, buộc mã phải tổng quát. Test càng cụ thể, mã càng tổng quát.", chapter: "cleancode/j4" },
  "devils-advocate": { term: "Devil's Advocate", def: "Kỹ thuật của Seemann: cố tình viết cài đặt sai rõ ràng mà vẫn qua mọi test. Làm được thì danh sách test còn thiếu.", chapter: "cleancode/j4" },
  "test-double-kinds": { term: "năm loại test double", def: "Thứ đứng thay một object thật khi test chạy. Theo Meszaros: dummy (điền chỗ), stub (trả giá trị định sẵn), spy (ghi lại lời gọi), mock (spy biết kỳ vọng), fake (cài đặt thật nhưng đơn giản).", chapter: "cleancode/j5" },
  "fragile-test": { term: "test dễ vỡ", def: "Test vỡ khi mã đổi mà hành vi không đổi, thường vì nó chạm vào chi tiết bên trong. Martin coi đó là vấn đề thiết kế của test.", chapter: "cleancode/j5" },
  "arrange-act-assert": { term: "Arrange, Act, Assert", def: "Cấu trúc ba phần của một test: chuẩn bị, gọi đúng một thao tác, so kết quả với mong đợi; cách nhau bởi dòng trống.", chapter: "cleancode/j5" },
  "code-rot": { term: "mã mục dần", def: "Mã phức tạp dần qua từng thay đổi nhỏ mà không ai để ý, tới lúc không còn ai dám sửa. Seemann đề xuất đặt ngưỡng cho một chỉ số để chặn nó.", chapter: "cleancode/j1" }
});
