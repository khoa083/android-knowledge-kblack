# Nghiên cứu track K (Lập trình hàm với Kotlin)

> Track đã duyệt 2026-11-24, đang viết. Dàn ý: `docs/tracks/K-functional-kotlin.md`. Nguồn chính thức thắng khi mâu thuẫn.
> Ví dụ của sách được viết lại bằng Kotlin trên app Hẹn Khám; không chép mã hay câu chữ của sách. Arrow là thư viện bên ngoài: chương dùng Arrow ghi phiên bản đã kiểm và luôn có bản Kotlin thuần đi trước.

## Đã đọc để soạn dàn ý (2026-11-24, chỉ mục lục, lấy từ bookmark PDF trong catalog)
- Kodeco, *Functional Programming in Kotlin by Tutorials*: ch.1–19.
  - PDF gần như không có lớp text, nên khi viết phải đọc dạng ảnh trang. (Cập nhật khi viết K1: bản PDF khác trong thư viện có lớp text đọc được, xem mục Sách.)
- Vermeulen, Bjarnason, Chiusano, *Functional Programming in Kotlin* (Manning): ch.1–15 và phụ lục.
- Barbini, *From Objects to Functions*: ch.1–13.
- Moskała, *Functional Kotlin*: phần lớn trùng track Kotlin.
- Seemann, *Code That Fits in Your Head*: A.12, A.15.
- URL kiểm HTTP 200 ngày 2026-11-24:
  - kotlinlang.org/docs/functions.html, kotlinlang.org/docs/sealed-classes.html;
  - kotlinlang.org/api/core/kotlin-stdlib/kotlin/-result/;
  - arrow-kt.io/learn/typed-errors/, arrow-kt.io/learn/immutable-data/intro/.

## Sách (bản trong thư viện cá nhân; trên site chỉ ghi trang của nhà xuất bản)
- **Massimo Carli, *Functional Programming in Kotlin by Tutorials* (Kodeco, 2022)** (`book-fp-tut`). Bản PDF trong thư viện có lớp text đọc được bằng `pdftotext -layout` (dàn ý cũ ghi "gần như không có lớp text" là của một bản khác).
- **Marco Vermeulen, Rúnar Bjarnason, Paul Chiusano, *Functional Programming in Kotlin* (Manning, 2021)** (`book-fp-manning`).
- **Mark Seemann, *Code That Fits in Your Head*** (`book-seemann`, khai báo ở `tracks/sysdesign/sources.js`, dùng chung với Mã sạch và Lập trình hàm).
- Sẽ thêm khi tới chương dùng: Uberto Barbini, *From Objects to Functions*; tài liệu Kotlin (Functions, Sealed classes, `Result`); Arrow (Typed errors, Immutable data).

## Bảng nguồn theo chương

### K1 Hàm thuần và referential transparency
| Ý trên site | Nguồn |
|---|---|
| Hàm thuần: cùng đầu vào cho cùng đầu ra, và "vũ trụ" không đổi sau mỗi lần gọi; twice so với twiceAndLog (println), randomInc (Random đổi trạng thái); so hai chương trình (gọi ở từng chỗ so với tính một lần rồi dùng lại); println trả Unit ở cả hai cách nhưng số dòng in khác; ngoại lệ là side effect vì chữ ký không nói | Carli ch.3 (Pure functions; Referential transparency and the substitution model; ch.1 Pure functions and testability) |
| Ý bài tập: hàm nào thuần (Exercise 3.1 `inc` với biến đếm toàn cục, 3.2 `inc2`) | Carli ch.3 |
| Định nghĩa referential transparency (mọi chương trình, thay bằng kết quả không đổi nghĩa) và hàm thuần (f(x) RT với mọi x RT); mô hình thay thế, suy luận như giải phương trình; quán cà phê: buyCoffee gọi charge là side effect, trả Charge như giá trị thì test không cần mock; lõi thuần với lớp mỏng bên ngoài xử lý hiệu ứng; sửa dữ liệu cục bộ không ai thấy vẫn chấp nhận được; tới lúc nào đó chương trình phải tác động lên thế giới | Vermeulen và cộng sự ch.1 (1.1, 1.2, 1.3) |
| Query phải tất định: không số ngẫu nhiên, GUID, giờ trong ngày, ngày trong tháng, tệp, database; tất định và không side effect là RT, là hàm thuần; lời gọi thay được bằng kết quả | Seemann 13.1.3 |
| WillAccept nhận now làm tham số, bộ điều khiển truyền DateTime.Now | Seemann 8.2.2 |
| **Của site:** hàm phí hai mức (200.000 và 300.000 đ), tuần 23–29/11/2026 (lịch thật, kiểm bằng selfCheck), biến đếm calls, bảng thế, lỗi UUID gộp vào vòng thử lại | — |
