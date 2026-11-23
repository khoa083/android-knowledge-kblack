/* Thuật ngữ track kotlin (tiếng Việt). */
ADE.addGlossary('vi', 'kotlin', {
  "val-var": { term: "val / var", def: "val là tham chiếu chỉ gán một lần; var gán lại được. val không làm object bên trong bất biến: một val trỏ tới MutableList vẫn thêm phần tử được.", chapter: "kotlin/k1" },
  "type-inference": { term: "suy kiểu (type inference)", def: "Trình biên dịch tự xác định kiểu của biến hoặc biểu thức từ giá trị khởi tạo; kiểu được chốt lúc biên dịch, không đổi lúc chạy.", chapter: "kotlin/k1" },
  "integer-division": { term: "chia nguyên", def: "Phép chia giữa hai số nguyên trả về số nguyên, phần lẻ bị bỏ (5 / 2 = 2). Muốn có phần lẻ, một toán hạng phải là Double hoặc Float.", chapter: "kotlin/k1" },
  "smart-cast": { term: "smart cast", def: "Trình biên dịch tự coi biến là kiểu hẹp hơn (ví dụ String thay vì String?) sau một phép kiểm, chỉ khi chứng minh được biến không đổi giữa lúc kiểm và lúc dùng.", chapter: "kotlin/k2" },
  "platform-type": { term: "platform type (T!)", def: "Kiểu của giá trị đến từ Java không có chú thích nullability; nghĩa là T hoặc T?. Kotlin nới kiểm tra null cho nó, nên có thể NPE lúc chạy.", chapter: "kotlin/k2" },
  "elvis": { term: "Elvis ?:", def: "Toán tử trả về vế trái nếu khác null, ngược lại trả vế phải; vế phải có thể là return hoặc throw.", chapter: "kotlin/k2" },
  "when-expression": { term: "biểu thức when", def: "when trả về giá trị của nhánh khớp đầu tiên; khi dùng như biểu thức, các nhánh phải phủ đủ mọi trường hợp (thường bằng else).", chapter: "kotlin/k1" }
});
