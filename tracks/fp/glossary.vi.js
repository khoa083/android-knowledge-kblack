/* Thuật ngữ track fp (tiếng Việt). */
ADE.addGlossary('vi', 'fp', {
  "pure-function": { term: "hàm thuần (pure function)", def: "Hàm thỏa hai điều kiện: cùng đầu vào luôn cho cùng đầu ra, và lời gọi không làm gì khác ngoài trả kết quả (không đọc đồng hồ, không ghi log, không sửa biến bên ngoài). Seemann gọi gọn: tất định và không side effect.", chapter: "fp/p1" },
  "referential-transparency": { term: "referential transparency", def: "Tính chất của một biểu thức: thay nó bằng giá trị của nó ở mọi chỗ dùng mà chương trình không đổi nghĩa. Hàm thuần khi lời gọi của nó, với đối số cũng như vậy, có tính chất này.", chapter: "fp/p1" },
  "substitution-model": { term: "mô hình thay thế (substitution model)", def: "Cách suy luận về chương trình bằng cách thay từng biểu thức bằng giá trị của nó, như giải một phương trình, cho tới khi còn một giá trị. Chỉ dùng được khi các biểu thức referentially transparent.", chapter: "fp/p1" }
});
