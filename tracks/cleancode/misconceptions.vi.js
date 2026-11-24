/* Hiểu lầm track cleancode (tiếng Việt). */
ADE.addMisconceptions('vi', 'cleancode', {
  "short-means-simple": { wrong: "Hàm ngắn, dưới 24 dòng, là đủ đơn giản.", right: "Số dòng chỉ là một cách đếm. Hàm vẫn có thể có quá nhiều đường đi và quá nhiều biến phải theo dõi cùng lúc. [[src:book-seemann]]", example: "Chương J1: hàm 19 dòng có 9 đường đi và 13 biến.", chapter: "cleancode/j1" },
  "get-is-harmless": { wrong: "Hàm tên get… thì gọi bao nhiêu lần cũng vô hại.", right: "Chỉ khi nó thật sự là query. Tên không được trình biên dịch kiểm; hàm trả dữ liệu mà vẫn ghi sẽ làm số lần và thứ tự gọi trở nên quan trọng. Tách command và query. [[src:book-seemann]]", example: "Chương J2: getAppointments() xóa cache, lần gọi thứ hai khi mất mạng trả danh sách rỗng.", chapter: "cleancode/j2" },
  "seven-is-a-law": { wrong: "Não người chỉ nhớ đúng 7 thứ, nên mọi hàm phải dưới 7.", right: "Seemann nói rõ 7 là con số tượng trưng, con số chính xác không quan trọng; điều có tác dụng là có một ngưỡng và để ý tới nó. [[src:book-seemann]]", example: "Chương J1: vượt ngưỡng đôi khi là cách xử lý tốt nhất, miễn là đưa mã về lại sau.", chapter: "cleancode/j1" }
});
