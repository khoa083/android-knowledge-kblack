# TRACK J — Mã sạch và kỷ luật làm nghề / Clean Code and Craft (`cleancode`)

> **ĐÃ DUYỆT (2026-11-24).** Hai câu hỏi cuối theo mặc định (người dùng đổi được): **giữ j11**, tên track **"Mã sạch và kỷ luật làm nghề"**. Chưa xây; làm sau track I.
> Nguyên tắc: **cần và đủ**; ví dụ bằng Kotlin trên app "Hẹn Khám". Mỗi chương bắt đầu từ một lỗi thật: sửa một chỗ hỏng chỗ khác, test vỡ khi refactor, bug không tái hiện được.

## Manifest đề xuất
| Trường | Giá trị |
|---|---|
| id / code / order | `cleancode` / J / 100 |
| domain | engineering |
| Tên vi / en | Mã sạch và kỷ luật làm nghề / Clean Code and Craft |
| level / estMinutes | intermediate / 360 |
| prerequisites | [] (nên đọc Kotlin K1–K7 trước) |
| status | `draft` trong lúc viết, `stable` sau j0 |

## Nguồn đã đọc để soạn dàn ý (chỉ mục lục)
- **Cập nhật 2026-11-24 (người dùng bổ sung):** kho đã có *Clean Code* (Martin, 2008), cùng hai bản dịch tiếng Việt do cộng đồng làm. Xem mục "Clean Code (2008)" ngay dưới. Các nguồn khác:
  - **Seemann, *Code That Fits in Your Head*.**
    - Phần I (ch.1–9): checklist, độ phức tạp, vertical slice, đóng gói, triangulation, tách nhỏ, API design, làm việc nhóm.
    - Phần II (ch.10–16): sửa mã, sửa unit test, gỡ lỗi, tách mối quan tâm, nhịp làm việc.
    - Phụ lục A gồm 28 thực hành: 50/72, 80/24, AAA, bisection, CQS, đếm biến, cyclomatic complexity, functional core/imperative shell, parse don't validate, red green refactor, reproduce defects as tests, strangler, X out names…
  - **Martin, *Clean Craftsmanship*:** ch.2–3 TDD, ch.4 thiết kế test, ch.5 refactoring, ch.6 simple design, ch.7 lập trình cùng nhau, ch.8 acceptance test, ch.9–11 chuẩn mực, ch.12–14 đạo đức.
  - **Martin, *Clean Architecture*:** chỉ phần III (SOLID, ch.7–11) và phần IV (nguyên lý thành phần, ch.12–14). Phần V–VI thuộc track G.
  - **Martin, *The Clean Coder*:** ch.1 chuyên nghiệp, ch.2–3 nói không và nói có, ch.5 TDD, ch.10 ước lượng, ch.11 áp lực, ch.12–13 làm việc nhóm.
  - **Moskała, *Effective Kotlin*.**
    - Phần 1: an toàn và dễ đọc (Item 10–18).
    - Phần 2: tái sử dụng (Item 19–24), thiết kế trừu tượng (Item 25–31), tạo object (Item 32–35), thiết kế lớp (Item 36–46).
    - Dùng làm nguồn ví dụ Kotlin. Track Kotlin đã dùng các Item an toàn và hiệu năng.
  - **Kodeco, *Android Test-Driven Development*:** ch.3 TDD, ch.4 kim tự tháp test, ch.12 vấn đề của app cũ, ch.14–15 refactor có test.
  - **Dùng rất ít:**
    - Martin, *Clean Agile*: ch.5 thực hành kỹ thuật;
    - Mancuso, *The Software Craftsman*: ch.7 thực hành kỹ thuật, ch.14 thúc đẩy thay đổi kỹ thuật.
- **Martin, *Clean Code: A Handbook of Agile Software Craftsmanship* (2008), bản PDF trong kho** (`deep_dive_kotlin/ggplaybook/`, đọc mục lục bằng pdftotext ngày 2026-11-24). Ví dụ bằng Java. Dùng như sau:
  - ch.2 Meaningful Names (tên lộ ý định, tránh thông tin sai, mỗi khái niệm một từ, tên theo miền bài toán) → j2;
  - ch.3 Functions (hàm nhỏ, làm một việc, một mức trừu tượng mỗi hàm và quy tắc stepdown, tham số cờ, không side effect, command query separation, ngoại lệ thay mã lỗi, DRY) → j1, j2;
  - ch.4 Comments, ch.5 Formatting → một mục ngắn ở j2 và checklist review j10;
  - ch.6 Objects and Data Structures (bất đối xứng dữ liệu và đối tượng, Law of Demeter, train wreck, DTO) và ch.8 Boundaries (bọc mã bên thứ ba, learning test) → j3;
  - ch.7 Error Handling (try-catch-finally trước, ngữ cảnh cho ngoại lệ, luồng bình thường, không trả và không truyền null) → j3, so với Kotlin K6 và track G G8;
  - ch.9 Unit Tests (ba luật TDD, test sạch, một khái niệm mỗi test, F.I.R.S.T.) → j4, j5;
  - ch.10 Classes (lớp nhỏ, SRP, cohesion, tổ chức để dễ thay đổi) và ch.12 Emergence (bốn luật simple design của Kent Beck) → j8;
  - ch.13 Concurrency (giới hạn phạm vi dữ liệu, dùng bản sao, giữ đoạn synchronized nhỏ, phụ thuộc giữa các phương thức synchronized) → nguồn phụ cho track I chương i3;
  - ch.17 Smells and Heuristics → nguồn tra cứu cho j6 (refactoring) và j10 (review).
  - **Trung thực:** mọi quy tắc của sách là heuristic của Martin, ghi tên tác giả. Các ngưỡng như độ dài hàm hay số tham số không phải định luật; mỗi chương nói khi nào không nên áp dụng, và đặt cạnh Seemann khi hai bên khác nhau. Ví dụ Java viết lại bằng Kotlin trên app "Hẹn Khám", không chép mã của sách.
- **Bản dịch tiếng Việt của cộng đồng (người dùng bổ sung, URL kiểm HTTP 200 ngày 2026-11-24):**
  - https://github.com/quoctinnguyen8/Clean-Code---Tieng-Viet
  - https://cleancode.tinnq.com/
  - Chỉ dùng để đối chiếu cách gọi thuật ngữ tiếng Việt (bổ sung cho `I18N-STYLE-GUIDE`). Không chép câu chữ của bản dịch lên site. Khi trích ý, nguồn ghi trên site vẫn là sách gốc.
- **Chính thức, đã kiểm HTTP 200:** Kotlin coding conventions (kotlinlang.org), Android Kotlin style guide, Fundamentals of testing (developer.android.com), git-bisect (git-scm.com).

## Điểm cần nói rõ trong track
- Hầu hết nội dung ở đây là **heuristic của tác giả, không phải định luật**. Mỗi quy tắc ghi tên tác giả, nói nó giải quyết vấn đề gì và khi nào không nên áp dụng:
  - 80/24 và 50/72 là của Seemann;
  - ba luật TDD và bốn luật simple design là của Martin;
  - ngưỡng "bao nhiêu thứ vừa trong đầu" của j1 phải lấy đúng con số và cách lập luận của Seemann (ch.3, chưa đọc thân chương). Khi nhắc tới nghiên cứu trí nhớ ngắn hạn, ghi đúng sắc thái của nghiên cứu.
- Số đo (cyclomatic complexity, độ bất ổn định I = Ce / (Ca + Ce)) luôn có ví dụ tính tay kiểm chứng.

## IN (đưa vào) và lý do
| Nội dung | Lý do |
|---|---|
| Mã phải vừa trong đầu: đếm biến, đếm nhánh, cyclomatic complexity | Gốc của lỗi "sửa một chỗ hỏng chỗ khác": hàm quá nhiều thứ phải nhớ cùng lúc |
| Đặt tên, hàm một mức trừu tượng, command/query tách nhau | Tên sai và hàm vừa đọc vừa ghi làm người đọc hiểu nhầm |
| Đóng gói, bất biến, parse don't validate | Dữ liệu sai lọt sâu vào hệ thống; kiểm hợp lệ lặp ở khắp nơi |
| TDD: ba luật, red green refactor, triangulation | Cách viết test trước để thiết kế; Android TDD cho ví dụ Android |
| Thiết kế test: AAA, test double, test dính vào cài đặt | Test vỡ hàng loạt khi refactor dù hành vi không đổi |
| Refactoring an toàn từng bước nhỏ; strangler cho mã cũ | Refactor lớn một lần làm hỏng app và không quay lại được |
| SOLID với Kotlin | Nguyên lý thiết kế lớp; G dạy hướng phụ thuộc giữa các tầng |
| Nguyên lý thành phần: cohesion, coupling, độ ổn định | Cơ sở cho việc chia module (G9) |
| Gỡ lỗi có phương pháp: tái hiện bằng test, chia đôi (git bisect) | Bug không tái hiện được; không biết commit nào gây lỗi |
| Làm việc nhóm: review, commit message, lập trình cùng nhau | Mã sạch là chuyện của cả nhóm |
| Tính chuyên nghiệp: nói không, ước lượng có khoảng, làm dưới áp lực | Lời hứa sai hạn là nguồn của mã ẩu |

## OUT (bỏ ra hoặc chỉ nhắc) và lý do
| Nội dung | Lý do |
|---|---|
| *Clean Code* ch.11 Systems (Java proxy, AOP, EJB), ch.14–16 (ba bài refactor dài bằng Java: Args, JUnit, SerialDate) | Gắn với Java và công cụ cũ; chỉ lấy ý "refactor từng bước nhỏ" cho j6. DI và tách khởi tạo đã có ở track G (G6) |
| Quy trình Agile (planning, iteration, standup, story point) trong *Clean Agile* | Là quy trình nhóm, không phải mã; chỉ một đoạn ở j11 |
| Tuyển dụng, phỏng vấn, văn hóa (*Software Craftsman* phần II) | Ngoài phạm vi tự học kỹ thuật |
| Phần đạo đức (*Clean Craftsmanship* ch.12–14) | Chỉ một mục ngắn ở j11 |
| Acceptance test bằng công cụ riêng (FitNesse) | Chỉ nói ý; test cấp cao đã có ở G10 |
| Các Item an toàn và hiệu năng của *Effective Kotlin* | Đã có trong track **Kotlin** |
| Kiến trúc tầng, Dependency Rule, module Android | Thuộc track **G** |
| Thiết kế web API (*API Design Patterns*) | Thuộc track **I** (ở mức client) |
| *The Art of Clean Code* (Mayer) | Ví dụ Python, nhiều lời khuyên chung; không cần thiết |

## Chương (12)
Cột **Hình chính** là tab mặc định; sơ đồ node của sim ở tab phụ. Track này ít luồng dữ liệu, nhiều chuyện "đếm và so sánh", nên **bảng** và **đồ thị** là chính. Mọi hình đều đã có cách vẽ, trừ đồ thị phụ thuộc (MỚI, dùng chung với G).

### Phần 1: Mã đọc được
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| j1 | Mã phải vừa trong đầu | Hàm `bookAppointment` 120 dòng: sửa phần tính phí làm hỏng phần gửi nhắc | `cleancode.fits`: đọc hàm từng dòng, đếm biến và nhánh đang phải nhớ; tách hàm rồi đếm lại | (1) **Dãy ô** "bộ nhớ làm việc": mỗi biến hay nhánh là một ô, vượt ngưỡng thì tô đỏ. (2) **Bảng tính** cyclomatic complexity trước và sau khi tách | Seemann ch.1–3, ch.7, A.2 (80/24), A.7, A.8; Clean Code ch.3 |
| j2 | Đặt tên, mức trừu tượng, command và query | `getAppointments()` lại xóa cache; tên `data2`, `tmp` | `cleancode.names`: che tên đi (X out names) rồi đoán hàm làm gì | **Bảng đối chiếu** trước/sau: tên, chữ ký, nó đọc hay ghi | Seemann A.6 (CQS), A.28; Clean Code ch.2–3; Effective Kotlin Item 10–18, Item 25; Kotlin coding conventions |
| j3 | Đóng gói, bất biến, parse don't validate | Số điện thoại sai định dạng đi tới tận lúc gửi SMS mới lỗi; kiểm hợp lệ viết lại ở ba màn hình | `cleancode.parse`: chuỗi thô đi qua ranh giới; kiểm rải rác so với parse một lần thành kiểu riêng | **Hộp lồng**: vùng "dữ liệu thô" bên ngoài, ranh giới parse, vùng "đã chắc đúng" bên trong; giá trị sai dừng ở ranh giới | Seemann ch.5, A.15; Clean Code ch.6–8; Effective Kotlin Item 1 (cầu nối Kotlin K4), Item 29 |

### Phần 2: Test và thay đổi an toàn
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| j4 | TDD | Viết xong mới test, test chỉ kiểm đường thuận nên bỏ sót ngày nghỉ | `cleancode.tdd`: viết hàm tính phí khám bằng red → green → refactor, thêm ví dụ để triangulate | (1) **Vòng** red, green, refactor; vòng sáng theo bước. (2) **Bảng** danh sách test và trạng thái từng test | Clean Craftsmanship ch.2–3; Clean Code ch.9; Seemann ch.6, A.17, A.26; Android TDD ch.3 |
| j5 | Thiết kế test | Đổi tên một hàm private, 40 test vỡ dù hành vi không đổi | `cleancode.testDesign`: test kiểm hành vi so với test kiểm cách cài đặt (mock từng lời gọi) | **Đồ thị phụ thuộc MỚI** test → mã: test cột vào chi tiết thì có nhiều cạnh, mỗi lần refactor là cạnh đỏ | Clean Craftsmanship ch.4; Clean Code ch.9 (F.I.R.S.T.); Seemann ch.11, A.3 (AAA); Android TDD ch.4, ch.15 |
| j6 | Refactoring từng bước nhỏ | Refactor một lần cả màn hình, app hỏng, không biết bước nào gây ra | `cleancode.refactor`: chuỗi bước nhỏ, mỗi bước chạy test; một bước làm đỏ thì quay lại ngay | **Dãy ô** các commit theo thời gian, mỗi ô xanh hay đỏ theo test; bước to so với chuỗi bước nhỏ | Clean Craftsmanship ch.5; Clean Code ch.17; Seemann A.22, A.24 (strangler); Android TDD ch.14 |
| j7 | Gỡ lỗi có phương pháp | Bug "chỉ xảy ra trên máy tester"; 200 commit không biết commit nào gây lỗi | `cleancode.bisect`: tái hiện thành test, rồi chia đôi khoảng commit | **Dãy ô** commit, mỗi lần chia đôi gạch một nửa; số bước ≈ log2(n) có ví dụ tính | Seemann ch.12, A.4, A.19; git-bisect |

### Phần 3: Thiết kế
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| j8 | Simple design và SOLID | Thêm cách thanh toán mới phải sửa `when` ở năm chỗ; lớp con ném lỗi ở hàm lớp cha | `cleancode.solid`: một yêu cầu thay đổi đi qua thiết kế vi phạm và thiết kế đúng từng nguyên lý | (1) **Ma trận** nguyên lý × triệu chứng khi vi phạm. (2) **Đồ thị phụ thuộc** trước và sau khi đảo phụ thuộc (DIP): mũi tên đổi chiều | Clean Craftsmanship ch.6; Clean Code ch.10, ch.12; *Clean Architecture* ch.7–11; Effective Kotlin Item 26, Item 36 |
| j9 | Nguyên lý thành phần | Module `common` ai cũng phụ thuộc, sửa một dòng phải build lại cả app | `cleancode.components`: tính Ca, Ce, I cho từng module; tìm module ổn định mà lại hay đổi | **Đồ thị phụ thuộc** module, mỗi node ghi I = Ce / (Ca + Ce), kèm **bảng tính** kiểm chứng | *Clean Architecture* ch.12–14; cầu nối G9 |

### Phần 4: Làm nghề
| Id | Chương | Lỗi dẫn dắt | Sim | Hình chính (vì sao hợp) | Nguồn chính |
|---|---|---|---|---|---|
| j10 | Làm việc nhóm với mã | Pull request 3 000 dòng được duyệt sau 2 phút; commit message "fix" | `cleancode.review`: chia PR nhỏ, checklist review, viết commit message | **Bảng checklist** review (Seemann) kèm ví dụ commit message trước/sau theo quy tắc 50/72 | Seemann ch.2, ch.9, A.1, A.20; Clean Craftsmanship ch.7; Clean Code ch.17 (tra cứu) |
| j11 | Tính chuyên nghiệp | Hứa "mai xong" rồi làm ẩu, bỏ test cho kịp | `cleancode.estimate`: ước lượng ba điểm (lạc quan, thường gặp, bi quan) và khoảng tin cậy | **Bảng tính** ước lượng ba điểm, có ví dụ kiểm chứng; kèm bảng "nói không / nói có" theo Martin | The Clean Coder ch.1–3, ch.10–11; Clean Agile ch.5 |
| j0 | Bản đồ track (viết CUỐI) | Gặp triệu chứng X thì đọc chương nào | `cleancode.map` | **Bảng tra** triệu chứng → chương | — |

Khuôn mỗi chương như track Kotlin:
- tối đa 8 mục;
- 2 lỗi thật;
- 1 bài tập (sửa một đoạn mã cho sẵn);
- quiz 3–4 câu.

## Cầu nối dự kiến
- j3 ↔ Kotlin K4 (data class, val), K6 (require/check).
- j4, j5 ↔ G g10 (test theo tầng), Coroutines A9 (runTest).
- j8 ↔ G g2 (hướng phụ thuộc giữa các tầng).
- j9 ↔ G g9 (module hóa).
- j3 ↔ K (FP): parse don't validate và kiểu dữ liệu đại số.

## Hai câu hỏi đã có mặc định (người dùng đổi được)
1. Giữ j11 (tính chuyên nghiệp, ước lượng), track 12 chương.
2. Tên track: "Mã sạch và kỷ luật làm nghề" / "Clean Code and Craft".
