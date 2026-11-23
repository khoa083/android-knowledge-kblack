# TRACK F — Kotlin: cơ chế ngôn ngữ / Kotlin: How the Language Works (`kotlin`)

> Áp dụng toàn bộ hợp đồng chung `00-MASTER-PROMPT.md`. Spec này nằm trong `docs/` của site vì thư mục prompt chỉ được đọc.
> Viết ngày 2026-11-23 theo yêu cầu mới của người dùng: **chọn kiến thức cần và đủ, không bám từng chương sách** (sợ lan man).

## Manifest
| Trường | Giá trị |
|---|---|
| id / code / order | `kotlin` / F / 60 (bội số của 10, không đụng manifest khác) |
| domain | engineering |
| Tên vi / en | Kotlin: cơ chế ngôn ngữ / Kotlin: How the Language Works |
| Tóm tắt | Những cơ chế của Kotlin hay gây bug trên Android: null và platform type, equals/hashCode, sealed và when, thứ tự khởi tạo, lambda và inline, collection và sequence, variance, delegate. Mỗi cơ chế xem tới mức bytecode khi cần. |
| level / estMinutes | beginner / 420 |
| prerequisites | [] (Coroutines, Runtime dựa vào track này) |
| logKinds | dùng lại loại có sẵn trong lõi (`ADE.kinds`), không thêm loại mới: `check`, `run`, `write`, `skip`, `exception`, `complete`, `observe` |
| labels | `stable`, `version`, `impl`, `simplified`, `guideline` |
| status | `draft` trong lúc viết (để track-check bấm được chương); `stable` sau k0 (đã chuyển 2026-11-23) |
| Ví dụ xuyên suốt | Ứng dụng hư cấu "Hẹn Khám" (dùng lại mock-app), nhưng góc nhìn là mã Kotlin của app |

## Nguyên tắc chọn nội dung (cần và đủ)
Giữ một chủ đề khi nó thỏa ít nhất một điều:
1. Là nguyên nhân của một bug thật, khó thấy trên Android (NPE từ Java, key HashSet bị đổi, smart cast thất bại, lambda giữ tham chiếu, khởi tạo sai thứ tự…).
2. Là nền mà track khác dựa vào (inline/crossinline cho Coroutines và Compose; delegate cho `by remember`/`by viewModels`; sealed cho UiState; variance cho Flow<out T>).
3. Ảnh hưởng hiệu năng đo được (allocation của lambda, sequence so với list, value class).

**Cho cả người mới (người dùng nhắc 2026-11-23):** track có hai phần. Phần 1 dạy nền tảng gọn cho người chưa biết Kotlin (không dạy lại lập trình nói chung), mỗi chương vẫn có một bug thật và một sim. Phần 2 đi vào cơ chế. Bài tập của mỗi chương chọn từ *Kotlin Exercises* (Moskała), diễn đạt lại và ghi nguồn.

**Bỏ ra hoặc chỉ nhắc (có lý do):** Kotlin/JS và Multiplatform (không phải app Android); annotation processing, KSP, compiler plugin, detekt, reflection, contract (chỉ một mục tổng quan "đọc thêm" ở k13, vì người mới và mã app Android hiếm khi cần viết chúng); context receivers và Arrow (thử nghiệm hoặc thư viện ngoài); operator overloading (một dòng khi cần); phần "dễ đọc" và "thiết kế lại mã" của Effective Kotlin (để cho track Clean Code sau này). Các mục an toàn và hiệu năng của Effective Kotlin được lồng vào chương có liên quan, không thành chương riêng.

## Chương (14)
### Phần 1: Nền tảng (người mới)
| Id | Chương | Bug/câu hỏi dẫn dắt | Sim (rời rạc, sơ đồ node) | Nguồn sách | Bài tập (Kotlin Exercises) |
|---|---|---|---|---|---|
| k1 | val/var, kiểu, hàm, biểu thức | `5 / 2` ra 2; `if`/`when` trả giá trị; tham số mặc định và tên | `kotlin.eval`: tính một biểu thức `when`/`if` từng bước, kiểu được suy ra | Essentials: Variables, Basic types, Conditional statements, Functions, for-loop | Basic values operations; Using when; Pretty time display |
| k2 | Null safety và smart cast | Vì sao `if (user.name != null) user.name.length` không biên dịch? NPE từ API Java | `kotlin.smartcast`: một biến qua kiểm null tới chỗ dùng; đổi loại biến (local val, local var bị lambda sửa, property `open`/getter tự viết, property module khác, platform type) | Essentials: Nullability, Smart-casting; Advanced: Java interop (platform type); Effective Item 3 | Person details display; User Information Processor |
| k3 | Class, interface, object và thứ tự khởi tạo | Property còn null trong `init`; gọi hàm `open` trong constructor | `kotlin.init`: thứ tự khởi tạo cha/con, property và `init`, `companion`/`object` khởi tạo lúc nào | Essentials: Classes, Inheritance, Objects | Implementing the Product class; GUI View Hierarchy Simulation |
| k4 | Data class và bằng nhau | Phần tử "biến mất" khỏi HashSet sau khi sửa | `kotlin.hashset`: thêm → sửa thuộc tính → `contains` theo bucket | Essentials: Data classes; Effective Items 1, 37, 42, 43 | Data class practice; Pizza factory |
| k5 | Enum, sealed và when | Thêm trạng thái mới mà quên xử lý một nhánh | `kotlin.sealed`: UiState sealed qua `when` (có/không `else`), thêm subtype mới | Essentials: Enum, Sealed; Effective Items 39–41 | Days of the week enum |
| k6 | Ngoại lệ, require/check và use | Lỗi bị nuốt trong `catch`; tài nguyên không đóng | `kotlin.exception`: ném, lan qua các hàm, `try` là biểu thức, `finally` | Essentials: Exceptions; Effective Items 5, 6, 8 | Catching exceptions; Specify expectations |
| k7 | Collection: read-only, mutable, xử lý | List "read-only" vẫn bị sửa; `map` trên map | `kotlin.collections`: list/set/map qua thêm, sửa, ép kiểu sang Mutable | Essentials: Collections; Functional Kotlin: collection processing | Inventory management; Implement shop functions |
### Phần 2: Cơ chế sâu
| Id | Chương | Bug/câu hỏi dẫn dắt | Sim | Nguồn sách | Bài tập |
|---|---|---|---|---|---|
| k8 | Lambda, closure, inline | `return` trong `forEach` thoát cả hàm; lambda giữ Activity | `kotlin.inline`: hàm bậc cao biên dịch thành object hàm hay chép vào chỗ gọi; non-local return; crossinline; reified | Functional Kotlin: function types, lambdas, references, inline | Function types and literals; Inline functions; Implement map |
| k9 | Sequence và hiệu năng collection | Xử lý chuỗi dài tạo nhiều list trung gian | `kotlin.sequence`: từng phần tử qua filter/map/first, đếm phép tính và list trung gian | Functional Kotlin: Sequences; Effective Items 47, 54–58 | Understanding sequences; Optimize collection processing |
| k10 | Generics và variance | `List<Cat>` thành `List<Animal>` được, `MutableList` thì không; `Flow<out T>` | `kotlin.variance`: thử gán và gọi qua `out`/`in`/bất biến | Advanced: variance; Essentials: Generics (erasure); Functional Kotlin: reified | Usage of generic types; Generic Response |
| k11 | Delegation | `by lazy` trên nhiều luồng; `by remember`, `by viewModels` gọi gì | `kotlin.delegate`: truy cập property qua getValue/setValue, ba chế độ của lazy | Advanced: Interface delegation, Property delegation | Lateinit delegate; Mutable lazy delegate |
| k12 | Scope function và DSL | `apply` lồng `apply`: `this` là ai? | `kotlin.scope`: receiver và `it` qua lồng nhau, @DslMarker | Functional Kotlin: Scope functions, DSL builders | Using scope functions; HTML table DSL |
| k13 | Java interop và dưới mui xe | Gọi Kotlin từ Java: `Companion.`, overload thiếu, `getX()` | `kotlin.jvm`: một khai báo Kotlin nhìn từ Java (static, field, overload, tên) | Advanced: Java interoperability; tổng quan reflection/KSP/contract | Adjust Kotlin for Java usage |
| k0 | Bản đồ track (viết CUỐI) | Gặp triệu chứng X thì đọc chương nào | cây triệu chứng → chương | — | — |

Thứ tự viết: k1 → k2 → … → k13 → k0.

Mỗi chương (gọn hơn UX v2, có trần cụ thể): **tối đa 8 mục**, gồm đoán trước khi đọc, 2–4 mục cơ chế, dưới mui xe, lỗi hay gặp (2 bug), bài tập (1), tự trả lời (2–3 câu), ghi chú trung thực; **mỗi mục cơ chế tối đa 4 khối** (đoạn văn, mã, ghi chú); quiz 3–4 câu. Kiểm trần này trước mỗi commit chương. Sim là sơ đồ node như các track kỹ thuật khác (người dùng: chỉ UI/UX dùng màn hình mẫu).

## Phiên bản và nguồn chính thức (xác nhận ở bước nghiên cứu từng chương)
- Kotlin docs (kotlinlang.org): null safety, typecasts (smart cast), data classes, sealed classes, inline functions, generics, delegated properties, scope functions, type-safe builders, Java interop. Ghi phiên bản Kotlin của trang khi trích.
- Mã stdlib (Lazy.kt, Collections, Sequences) ghim theo tag phát hành Kotlin trên GitHub khi cần chi tiết bên trong.
- Ghim phiên bản: tài liệu kotlinlang.org đọc ngày viết chương; mã stdlib ghim tag **v2.1.0** của JetBrains/kotlin trên GitHub (kiểm URL trước khi dùng; nếu tag khác thì ghi lại ở đây).
- Bytecode: máy không có `kotlinc`/`javap`, nên mọi khẳng định bytecode lấy từ sách hoặc tài liệu, ghi nguồn, gắn nhãn `simplified`, kèm phiên bản Kotlin của sách nếu sách nêu.

## Hiểu lầm dự kiến (≥ 8)
`val` là bất biến; `List` là bất biến; data class so sánh mọi thuộc tính; smart cast luôn chạy sau `!= null`; `lateinit` cho kiểu nguyên thủy; `inline` luôn nhanh hơn; `Sequence` luôn nhanh hơn list; `object` khởi tạo khi app chạy; `by lazy` mặc định không an toàn luồng (thật ra mặc định là SYNCHRONIZED).

## Cầu nối dự kiến
- k5 inline/crossinline ↔ Coroutines (suspend lambda, `coroutineScope`) và Runtime (composable lambda).
- k8 delegate ↔ Runtime (`by remember`, `State.getValue`).
- k3 sealed ↔ UI state trong Compose (Runtime).
- k7 variance ↔ Flow (Coroutines).
