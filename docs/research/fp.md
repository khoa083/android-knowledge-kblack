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

### K2 Bất biến, dữ liệu dùng chung và đệ quy
| Ý trên site | Nguồn |
|---|---|
| Bất biến (object) khác hằng (tham chiếu): val MutableUser vẫn sửa được; data class toàn val chưa đủ nếu có thuộc tính kiểu sửa được (Date); List là read-only; lợi ích: đơn giản, nhất quán (khóa Map), tránh tạo trùng, an toàn luồng | Carli ch.6 |
| Đệ quy thay vòng lặp; khai triển recursiveFactorial(5); tailRecFactorial với tham số tích lũy; mã dịch ngược của hàm tailrec là while(true) | Carli ch.6 (Tailrec functions) |
| Ba từ: immutable, functional, persistent; thêm phần tử mới thì đối tượng cũ thành đuôi của đối tượng mới | Carli ch.7 |
| Data sharing: thêm vào đầu là Cons(x, xs), không chép xs; bỏ đầu là trả tail; persistent; pessimistic copying trong chương trình lớn; append chỉ chép a1; init phải chép mọi nút trước | Vermeulen và cộng sự 3.3, 3.3.1 |
| Vị trí đuôi; Kotlin cần tailrec mới bỏ tail call; gắn tailrec cho hàm không có lời gọi đuôi chỉ bị cảnh báo; foldRight không stack-safe, foldLeft tailrec (Exercise 3.9) | Vermeulen và cộng sự ch.2, ch.3 |
| Điều kiện của tailrec: gọi chính nó như thao tác cuối; không khi còn mã sau lời gọi, trong try/catch/finally, hàm open; trình biên dịch để lại một vòng lặp | Kotlin docs, Functions (đọc 2026-11-24; nguồn kt-functions của track Kotlin, mở rộng cho fp) |
| **Của site:** FList tự viết, màn "Chọn lịch để hủy", 50.000 lịch, phí 200.000 đ, giới hạn minh họa 10.000 khung (độ sâu thật tùy stack của luồng) | — |

### K3 Ghép hàm: composition, currying, partial application
| Ý trên site | Nguồn |
|---|---|
| compose và after; ví dụ double, square, stringify; tính kết hợp; curry, mọi hàm nhiều tham số thành hàm bậc cao một tham số, sum(3)(4); tên Haskell Curry; pipe; partial application với CalculatorFactory, gần với dependency injection; đặt tham số ít đổi lên trước, quá nhiều tham số là thói quen xấu; curry và flip với nhiều tham số làm mã khó đọc; side effect phá ghép: map(f).map(g) và map(f compose g) | Carli ch.8 |
| partial1, curry, uncurry, compose như câu đố kiểu (chỉ một thân hàm hợp kiểu); closure giữ a (Exercise 2.3–2.5) | Vermeulen và cộng sự ch.2 |
| Đếm tham số như thứ phải giữ trong đầu | Seemann 7.2.7 (đã dùng ở J1) |
| **Của site:** bốn hàm parse, assign, price, format; hàm 6 tham số gọi ở bốn màn; lỗi UTC chép từ test; formatFor; let như pipe của thư viện chuẩn; hai múi giờ trong mô phỏng | — |

### K4 Kiểu dữ liệu đại số
| Ý trên site | Nguồn |
|---|---|
| Pair là tích Descartes, số giá trị nhân; Triage 3 giá trị; Struct = Boolean × Triage × Byte = 1.536; Unit là 1, Nothing là 0; Either là tổng; callback (Data, Result?, Error?) không an toàn kiểu, viết lại thành Result × (Info + Error), "điều không làm được quan trọng hơn điều làm được"; Optional là A + 1; Exercise 10.1, 10.3 | Carli ch.10 |
| Kiểu con trực tiếp của sealed biết lúc biên dịch, when phủ đủ không cần else | Kotlin docs, Sealed classes (nguồn kt-sealed của track Kotlin, mở rộng cho fp) |
| **Của site:** màn "Lịch trống" và thiết kế của nó (vào là tải; bản 2 thêm tải lại giữ dữ liệu cũ), đếm theo dạng (nullable tính có hoặc không), ba màn dùng chung state, khối catch quên tắt isLoading, crash slots!!; cầu nối X24 tới Kotlin K5 và Kiến trúc G7 | — |

### K5 Lỗi là giá trị
| Ý trên site | Nguồn |
|---|---|
| Ném ngoại lệ là mất kiểm soát: chương trình dừng hoặc ai đó ở trên bắt; ngoại lệ phá RT (failingFn: cùng dòng ném, trong try trả 43, ngoài try thì dừng; nghĩa phụ thuộc ngữ cảnh); không an toàn kiểu ((Int) -> Int không nói gì về lỗi); checked exception không hợp với hàm bậc cao; sentinel value để lỗi lặng lẽ đi tiếp, nơi gọi có thể quên kiểm | Vermeulen và cộng sự 4.1, 4.2 |
| Ngoại lệ là side effect; làm "sạch" hàm bằng cách đưa side effect vào kiểu trả về; hai chiến lược: fail fast (Optional, Either) và gom lỗi (applicative, để chương sau); Optional mất lý do lỗi; Either giữ lỗi đầu tiên; Result<T> của Kotlin, lỗi là Throwable, có map nhưng không có flatMap; ViewModel dùng fold để chọn trạng thái (NoSearchDone, SearchRunning, Failure, Success, NoResult) | Carli ch.14 |
| null khi lỗi đủ dùng nếu lý do hiển nhiên; trả kèm chuỗi lỗi (Pair) vẫn buộc kiểm null; ngoại lệ phá chuỗi hàm và làm hỏng việc chạy hàng loạt; chỉ dùng ngoại lệ cho tình huống không thể phục hồi; Outcome sealed (Success, Failure) và onFailure { return it } trả về sớm | Barbini ch.7 |
| Result gói giá trị T hoặc Throwable; danh sách hàm (map, mapCatching, recover, fold, getOrElse…), không có flatMap; runCatching bắt mọi Throwable | API kotlin.Result, runCatching (bản 2.4, đọc 2026-11-25) |
| Either và Raise; either { }, bind, raise, ensure, ensureNotNull, fold, getOrElse, recover; catch tự bỏ qua OutOfMemoryError và CancellationException; bản 2.3.0 | arrow-kt.io typed errors, setup (đọc 2026-11-25) |
| **Của site:** luồng đặt lịch bốn bước (parsePhone, findFreeSlot, checkQuota, save), bốn cách viết, bốn tình huống (suôn sẻ, giờ S07 đã đặt, bug quotas[phone]!! với số mới, lỗi mới ClinicClosed), kiểu Outcome ba dòng, hệ quả "runCatching gói cả CancellationException" suy từ "bắt mọi Throwable", bài tập hủy lịch | — |

### K6 map và flatMap: functor và monad qua ví dụ
| Ý trên site | Nguồn |
|---|---|
| Functor ánh xạ giữ cấu trúc; giữ cấu trúc nghĩa là giữ đơn vị và phép ghép (luật functor) | Carli ch.11 (Key points) |
| Hàm dạng (A) -> M<B> (Kleisli) cần cách ghép riêng; flatten có kiểu M<M<A>> -> M<A>; flatMap dựng từ map và flatten (hoặc fish, bind); monad là cách ghép các hàm đưa side effect vào kiểu trả về | Carli ch.13 (Key points) |
| Result của Kotlin có map nhưng không có flatMap; tự viết flatten, bind, flatMap cho Result | Carli ch.14 |
| map của Option, Gen, Parser chỉ khác tên kiểu, tổng quát hóa thành Functor; monad thường cũng là functor; monad = flatMap cùng unit; luật kết hợp và luật đơn vị trái, phải | Vermeulen và cộng sự 11.1, 11.2, 11.4 |
| **Của site:** ba hộp (List bác sĩ, Patient?, Outcome), f và g của từng hộp, ?.let không lồng (không có kiểu T?? riêng), Result.flatMap viết bằng fold, ensureQuota trả Outcome, chuỗi book bằng flatMap dừng ở S07, bài tập cancel viết thẳng hàng | — |
