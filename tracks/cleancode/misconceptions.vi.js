/* Hiểu lầm track cleancode (tiếng Việt). */
ADE.addMisconceptions('vi', 'cleancode', {
  "short-means-simple": { wrong: "Hàm ngắn, dưới 24 dòng, là đủ đơn giản.", right: "Số dòng chỉ là một cách đếm. Hàm vẫn có thể có quá nhiều đường đi và quá nhiều biến phải theo dõi cùng lúc. [[src:book-seemann]]", example: "Chương J1: hàm 19 dòng có 9 đường đi và 13 biến.", chapter: "cleancode/j1" },
  "seven-is-a-law": { wrong: "Não người chỉ nhớ đúng 7 thứ, nên mọi hàm phải dưới 7.", right: "Seemann nói rõ 7 là con số tượng trưng, con số chính xác không quan trọng; điều có tác dụng là có một ngưỡng và để ý tới nó. [[src:book-seemann]]", example: "Chương J1: vượt ngưỡng đôi khi là cách xử lý tốt nhất, miễn là đưa mã về lại sau.", chapter: "cleancode/j1" }
});
