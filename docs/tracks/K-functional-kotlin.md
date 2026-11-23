# TRACK K — Lập trình hàm với Kotlin / Functional Programming in Kotlin (`fp`)

> **ĐÃ DUYỆT (2026-11-24).** Hai câu hỏi cuối theo mặc định (người dùng đổi được): **dùng Arrow ở p5 và p10** (có bản Kotlin thuần đi trước), **property-based testing để OUT**. Chưa xây; làm sau track J.
> Nguyên tắc: **cần và đủ**. Dạy FP để viết mã Android an toàn hơn: ít trạng thái lẫn lộn, lỗi hiện ra trong kiểu, logic test được không cần mock. Không bắt đầu từ lý thuyết phạm trù.

## Manifest đề xuất
| Trường | Giá trị |
|---|---|
| id / code / order | `fp` / K / 110 |
| domain | engineering |
| Tên vi / en | Lập trình hàm với Kotlin / Functional Programming in Kotlin |
| level / estMinutes | advanced / 330 |
| prerequisites | [] (cần Kotlin K1–K12, nhất là K5, K7–K9) |
| status | `draft` trong lúc viết, `stable` sau p0 |

## Nguồn đã đọc để soạn dàn ý (chỉ mục lục)
- **Kodeco, *Functional Programming in Kotlin by Tutorials*** (PDF **gần như không có lớp text**; phải đọc dạng ảnh trang khi viết).
  - ch.1–4: vì sao FP, hàm, khái niệm (hàm thuần, referential transparency, side effect), lười và memoization.
  - ch.5–8: hàm bậc cao, bất biến và đệ quy, cấu trúc dữ liệu hàm, composition.
  - ch.9–13: kiểu dữ liệu, ADT, functor, monoid và semigroup, monad.
  - ch.14–16: xử lý lỗi, quản lý state, xử lý side effect.
  - ch.17–19: Sequence và Flow, Mobius, Arrow.
- **Vermeulen, Bjarnason, Chiusano, *Functional Programming in Kotlin*** (Manning).
  - ch.1–6: FP là gì, cấu trúc dữ liệu hàm, xử lý lỗi không dùng ngoại lệ, strict và lazy, state thuần.
  - ch.7–9: song song, property-based testing, parser combinator.
  - ch.10–12: monoid, monad, applicative.
  - ch.13–15: hiệu ứng và I/O, xử lý luồng.
- **Barbini, *From Objects to Functions***: dựng app to-do "Zettai" theo kiểu hàm.
  - ch.3–4: tách domain khỏi hạ tầng, DI theo kiểu hàm.
  - ch.5–6: event để đổi state, command sinh event.
  - ch.7: lỗi theo kiểu hàm; ch.8: functor; ch.9: monad; ch.11: validate bằng applicative.
  - ch.13: kiến trúc hàm.
- **Moskała, *Functional Kotlin***: kiểu hàm, lambda, tham chiếu hàm, inline, xử lý collection, Sequence. Gần như toàn bộ đã có ở track **Kotlin** (K7–K9).
- **Seemann, *Code That Fits in Your Head***: A.12 Functional Core, Imperative Shell; A.15 Parse, Don't Validate.
- **Chính thức, đã kiểm HTTP 200:**
  - kotlinlang.org: Functions (gồm `tailrec`), Sealed classes, API `Result`;
  - arrow-kt.io: Typed errors, Immutable data.

## Điểm cần nói rõ trong track
- **Arrow là thư viện bên ngoài**, không phải một phần của Kotlin. Chương dùng Arrow ghi phiên bản đã kiểm. Mỗi ý đều có bản viết bằng Kotlin thuần trước, để người học không phụ thuộc thư viện.
- Thuật ngữ functor, monad, applicative được giới thiệu **qua ví dụ có sẵn** (`List.map`, `Result.map`, `flatMap`, `Flow`) trước khi gọi tên. Luật (law) chỉ nêu ở mức "kiểm được bằng ví dụ".
- Ví dụ của *From Objects to Functions* là ứng dụng web phía server. Site chỉ lấy phần domain (event, command, lỗi, validate) và chuyển sang app "Hẹn Khám". Ghi rõ đó là diễn giải của site.

## IN (đưa vào) và lý do
| Nội dung | Lý do |
|---|---|
| Hàm thuần, referential transparency, side effect | Gốc của lỗi "test lúc qua lúc trượt" (hàm đọc giờ hệ thống, biến toàn cục) |
| Bất biến, cấu trúc dữ liệu dùng chung phần, đệ quy và `tailrec` | State bị sửa ở chỗ không ngờ; StackOverflow khi đệ quy sâu |
| Composition, currying, partial application | Ghép logic từ hàm nhỏ; nền cho chuỗi xử lý |
| ADT: sum và product type, đếm số trạng thái | Làm cho trạng thái vô nghĩa không biểu diễn được (nối G7 và K5) |
| Xử lý lỗi bằng kiểu: nullable, `Result`, Either/Raise (Arrow) | Lỗi biến mất trong `catch`; lỗi nghiệp vụ lẫn với ngoại lệ hệ thống |
| Functor và monad qua `map`/`flatMap` | Hiểu vì sao `Result`, `List`, `Flow` dùng chung một kiểu thao tác |
| Applicative và validate gom lỗi; monoid | Form báo một lỗi mỗi lần thay vì báo hết; gộp kết quả |
| State thuần: reducer, event sourcing (fold các event) | Nền của MVI; state không còn bị sửa ở nhiều chỗ |
| Functional core, imperative shell | Đẩy side effect ra rìa để logic test được không cần mock |
| FP trên Android: UI state bất biến, sao chép lồng sâu (optics trong Arrow) | Cập nhật state lồng nhau bằng `copy` lồng `copy` rất dễ sai |

## OUT (bỏ ra hoặc chỉ nhắc) và lý do
| Nội dung | Lý do |
|---|---|
| Kiểu hàm, lambda, inline, xử lý collection, Sequence (Functional Kotlin; FP by Tutorials ch.5 một phần) | Đã có ở track **Kotlin** (K7, K8, K9, K12): chỉ dẫn link |
| Flow như dòng dữ liệu (FP by Tutorials ch.17) | Đã có ở track **Coroutines**: chỉ dẫn link |
| Lý thuyết phạm trù (FP by Tutorials ch.2) | Chỉ một đoạn trực giác; không cần để dùng FP |
| Mobius (FP by Tutorials ch.18) | Framework riêng của một công ty; ý reducer đã có ở p8 |
| Song song thuần, parser combinator, property-based testing (Manning ch.7–9) | Ít dùng trong app Android; "đọc thêm" |
| Stream processing, I/O monad đầy đủ (Manning ch.13–15) | Kotlin dùng `suspend` và Flow cho việc này; p9 chỉ nêu ý |
| Mô phỏng higher-kinded type (`Kind`), monad transformer, free monad | Phức tạp, không cần trong Kotlin hiện đại |
| HTTP, JSON, giám sát phía server (From Objects to Functions ch.2, ch.12) | Là phía server |
| Reducer và MVI ở mức kiến trúc | Thuộc track **G** (g7): ở đây chỉ phần hàm thuần |

## Chương (11)
Cột **Hình chính** là tab mặc định; sơ đồ node của sim ở tab phụ. Nhiều khái niệm FP là "thay thế từng bước" và "dữ liệu chảy qua các hàm", nên dùng **bảng thế từng bước** và **luồng**. Riêng xử lý lỗi dùng **đường ray MỚI**.

### Phần 1: Nền tảng
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| p1 | Hàm thuần và referential transparency | Test "phí khám ngày cuối tuần" trượt vào thứ Bảy vì hàm tự đọc `LocalDate.now()` | `fp.pure`: thay lời gọi bằng giá trị của nó; hàm thuần thay được, hàm có side effect thì không | **Bảng thế từng bước** (substitution): mỗi hàng là biểu thức sau một lần thay; hàng không thay được tô đỏ | FP by Tutorials ch.3; Manning ch.1 |
| p2 | Bất biến, cấu trúc dùng chung phần, đệ quy | Sửa danh sách "đã chọn" làm đổi luôn danh sách gốc; đệ quy 50 000 phần tử bị StackOverflow | `fp.persistent`: thêm phần tử vào list bất biến, chia sẻ đuôi; đệ quy thường so với `tailrec` | (1) **Dãy ô** các nút list dùng chung đuôi. (2) **Làn thời gian** chiều sâu stack, `tailrec` giữ phẳng | FP by Tutorials ch.6–7; Manning ch.3; kotlinlang Functions (`tailrec`) |
| p3 | Ghép hàm: composition, currying, partial application | Hàm `formatAppointment` 6 tham số, gọi ở 4 chỗ với 3 tham số giống nhau | `fp.compose`: ghép `parse → validate → price → format`; cố định trước một số tham số | **Luồng**: dữ liệu đi qua các hàm ghép, kiểu của giá trị ghi trên mũi tên | FP by Tutorials ch.5, ch.8 |
| p4 | Kiểu dữ liệu đại số | `UiState(isLoading, error, data)` có 8 tổ hợp, 5 tổ hợp vô nghĩa | `fp.adt`: đếm số trạng thái của product type và sum type | **Bảng tính** số trạng thái (2 × 2 × 2 = 8 so với 1 + 1 + 1 = 3), kèm **ma trận** các tổ hợp hợp lệ | FP by Tutorials ch.9–10; Kotlin Sealed classes; cầu nối Kotlin K5, G g7 |

### Phần 2: Lỗi, ngữ cảnh và state
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| p5 | Lỗi là giá trị | `catch (e: Exception)` nuốt cả lỗi lập trình; hàm "có thể thất bại" nhưng chữ ký không nói | `fp.errors`: cùng một luồng đặt lịch viết bằng ngoại lệ, nullable, `Result`, Either/Raise | **Đường ray MỚI**: đường thành công và đường lỗi; bước lỗi rẽ sang đường dưới và bỏ qua các bước sau | FP by Tutorials ch.14; Manning ch.4; From Objects to Functions ch.7; Kotlin `Result`; Arrow Typed errors |
| p6 | map và flatMap: functor và monad qua ví dụ | `Result<Result<T>>` lồng nhau; `map` trả về list của list | `fp.monad`: cùng một thao tác trên `List`, nullable, `Result`; `map` so với `flatMap` | **Bảng** "hộp và giá trị": mỗi hàng một kiểu hộp; cột trước `map`, sau `map`, sau `flatMap` | FP by Tutorials ch.11, ch.13; Manning ch.11; From Objects to Functions ch.8–9 |
| p7 | Validate gom lỗi: applicative và monoid | Form đăng ký báo từng lỗi một, người dùng sửa 4 lần | `fp.validate`: dừng ở lỗi đầu tiên so với gom mọi lỗi; gộp bằng monoid | **Bảng** các trường của form: cột "dừng sớm" và "gom lỗi" hiện khác nhau theo bước | From Objects to Functions ch.11; Manning ch.10, ch.12; FP by Tutorials ch.12 |
| p8 | State thuần: reducer và event | Số lượt khám còn lại sai vì hai chỗ cùng trừ | `fp.reducer`: các event đi qua `fold(state, event)`; phát lại event để dựng lại state | **Bảng** nhật ký event: mỗi hàng là một event và state sau khi fold; hàng đang áp có viền | FP by Tutorials ch.15; From Objects to Functions ch.5–6; cầu nối G g7 |

### Phần 3: Ứng dụng
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| p9 | Functional core, imperative shell | Test logic đặt lịch phải mock 5 thứ (mạng, DB, đồng hồ, log, analytics) | `fp.core`: tách quyết định thuần ra lõi, vỏ chỉ đọc vào và ghi ra | **Hộp lồng**: lõi thuần ở giữa, vỏ có side effect bao ngoài; mũi tên dữ liệu chỉ đi qua ranh giới | Seemann A.12; FP by Tutorials ch.16; Manning ch.13 (ý chính); From Objects to Functions ch.4, ch.13 |
| p10 | FP trên Android: state bất biến và cập nhật lồng sâu | `state.copy(user = state.user.copy(address = …))` quên một tầng nên mất dữ liệu | `fp.optics`: cập nhật một trường sâu bằng `copy` lồng so với lens (Arrow optics) | **Cây** của object state, nhánh được sao chép mới tô màu, nhánh dùng lại giữ nguyên | FP by Tutorials ch.19; Arrow Immutable data; cầu nối Kotlin K4 |
| p0 | Bản đồ track (viết CUỐI) | Gặp triệu chứng X thì đọc chương nào | `fp.map` | **Bảng tra** triệu chứng → chương | — |

Khuôn mỗi chương như track Kotlin:
- tối đa 8 mục;
- 2 lỗi thật;
- 1 bài tập;
- quiz 3–4 câu.

Bài tập lấy ý từ bài tập của FP by Tutorials (Challenges) và Manning (Exercises), diễn đạt lại theo app "Hẹn Khám", có ghi nguồn.

## Cầu nối dự kiến
- p2 ↔ Kotlin K7 (read-only không phải bất biến).
- p3 ↔ Kotlin K8 (lambda, tham chiếu hàm).
- p4 ↔ Kotlin K5 (sealed), G g7 (một state duy nhất).
- p5 ↔ Kotlin K6 (ngoại lệ), G g8 (lỗi qua các tầng).
- p8 ↔ G g7 (MVI).
- p9 ↔ J j3 (parse don't validate), G g10 (test không mock).

## Hai câu hỏi đã có mặc định (người dùng đổi được)
1. Dùng Arrow ở p5 và p10, luôn có bản Kotlin thuần đi trước.
2. Property-based testing (Manning ch.8) để OUT, chỉ "đọc thêm".
