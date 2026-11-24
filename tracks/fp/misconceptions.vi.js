/* Hiểu lầm track fp (tiếng Việt). */
ADE.addMisconceptions('vi', 'fp', {
  "no-mutation-means-pure": { wrong: "Hàm không sửa biến nào thì là hàm thuần.", right: "Còn phải tất định: đọc đồng hồ, số ngẫu nhiên, UUID, tệp hay database đều làm cùng một lời gọi cho ra kết quả khác nhau. [[src:book-seemann]] [[src:book-fp-tut]]", example: "Chương K1: fee() không sửa gì ngoài biến đếm, nhưng trả 200.000 hôm thứ Hai và 300.000 hôm thứ Bảy.", chapter: "fp/p1" },
  "extract-variable-always-safe": { wrong: "Tách một biểu thức ra biến, hay gộp biến vào chỗ dùng, là refactor luôn an toàn.", right: "Chỉ an toàn với biểu thức referentially transparent. Với lời gọi có side effect hay không tất định, số lần gọi đổi thì chương trình đổi. [[src:book-fp-tut]]", example: "Chương K1: val a = fee(); a + a làm biến đếm tăng 1 thay vì 2; tạo UUID trong vòng thử lại thay vì một lần ở ngoài làm mỗi lần thử có khóa khác.", chapter: "fp/p1" }
});
