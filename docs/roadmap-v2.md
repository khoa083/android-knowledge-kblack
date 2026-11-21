# Lộ trình v2: học sâu, đầy đủ, dễ hiểu hơn đọc sách (ghi 2026-11-21)

## Vì sao có v2 (lời người dùng, tóm ý)

- Site hiện tại **quá rút gọn**. Với người mới, đọc sách (nhất là *Kotlin Coroutines: Deep Dive*) còn dễ hiểu hơn.
- Mục tiêu là hiểu **bản chất và cơ chế** để tự sửa được những bug mà AI không nhìn ra.
- Không ngại dài. Phải chi tiết, đầy đủ và dễ hiểu hết mức có thể.
- **Quyết định của người dùng:** site chỉ dùng nội bộ, cá nhân, để tự học. Vì vậy được **tận dụng tối đa** sách trong `E:\AndroidBooks`:
  - sách thành nguồn giảng dạy chính, cùng với tài liệu chính thức;
  - tìm thêm cách giảng dễ hiểu trên mạng.
  - Điều này thay quy tắc "sách chỉ là nguồn phụ, không chép" trước đây. CLAUDE.md đã sửa theo.
  - Vẫn giữ: không ghi đường dẫn file cục bộ lên site; chi tiết nội bộ có phiên bản; mô hình giản lược phải gắn nhãn.

## Cách làm mỗi chương (thay kiểu "1 đoạn bản chất + 1 sim")

Mỗi chương gồm các phần sau, theo thứ tự:

1. **Vấn đề trước khi có khái niệm:** viết theo cách cũ thì đau ở đâu, có ví dụ mã.
2. **Giảng từng bước:** nhiều đoạn, đi theo mạch của sách, ví dụ chạy được và có output dự đoán.
3. **Dưới mui xe:** cơ chế thật, gồm mã sau khi compiler biến đổi, cấu trúc dữ liệu và trích mã nguồn thư viện có ghi phiên bản.
4. **Sim / hình**, giữ phần đã làm.
5. **Bug thường gặp:**
   - triệu chứng → nguyên nhân cơ chế → cách sửa;
   - bài "đoán output" và "tìm bug".
6. **Bài tập** (lấy ý từ *Kotlin Exercises* và từ bài tập trong sách) cùng lời giải.
7. **Tóm tắt và câu hỏi tự kiểm.**

Kỹ thuật: thêm loại mục `sec.*.deep`, `sec.*.bug`, `sec.*.exercise` cho thân chương dài. Nếu cần, thêm chế độ "đọc dài" có mục lục nổi. Viết nội dung qua generator `dev/gen/*_content.py`.

## Thứ tự ưu tiên

| # | Việc | Sách chính (trong `E:\AndroidBooks`) |
|---|---|---|
| 1 | **Coroutines viết lại theo Deep Dive** (track A mở rộng) | `deep_dive_kotlin/kotlin/Kotlin Coroutines  Deep Dive.pdf`; `Kotlin Coroutines by Tutorials.pdf`; `Programming Android with Kotlin…` |
| 2 | Compose Runtime / Animation sâu hơn | `Jetpack Compose by Tutorials`, `Jetpack Compose 1.3 Essentials`, `Android UI Development with Jetpack Compose`, `Android Animations by Tutorials.pdf` |
| 3 | UX / UI sâu hơn | thư mục `UX/` (Norman, Krug, Podmajersky, Metts & Welfle, Greever, Albert & Tullis); `UI/` (Tidwell *Designing Interfaces*, Neil, MacDonald, Williams, Wendel, Design Sprint, Design Thinking Playbook); `design/` |
| 4 | **Track mới: Kotlin (trừ coroutines)** | `deep_dive_kotlin/kotlin/`: Kotlin Essentials, Advanced Kotlin, Effective Kotlin, Functional Kotlin, Kotlin Exercises |
| 5 | **Track mới: Clean Android Architecture** | `Clean Android Architecture/` (Dumbravan; Boudjnah); `Advanced Android App Architecture….pdf`; `Fundamentals of Software Architecture`; `Dagger by Tutorials` (DI) |
| 6 | **Track mới: Saving Data on Android** | `Saving Data on Android….pdf` (SharedPreferences/DataStore, file, SQLite, Room, đồng bộ) |
| 7 | **Track mới: Mobile System Design** | `deep_dive_kotlin/system-design/`: Mobile System Design (Tjeerd), DDIA (bản 1 và 2), Alex Xu tập 1 và 2, Acing the SDI, OS Concepts (chỉ phần áp dụng được cho mobile: tiến trình/luồng, bộ nhớ, đồng bộ hoá) |
| 8 | **Track mới: Clean Code** (tuyển tập, người dùng bổ sung nguồn) | `deep_dive_kotlin/ggplaybook/`: *The Clean Coder*, *Clean Craftsmanship* (TDD, refactoring, simple design, kỷ luật), *Clean Architecture* (SOLID, nguyên lý thành phần, Dependency Rule; dùng chung với track 5), *Clean Agile*, *Code That Fits in Your Head* (Seemann: heuristic, checklist, đo độ phức tạp), *The Software Craftsman*; cùng với *Effective Kotlin* để có ví dụ Kotlin. Có thể dùng thêm *API Design Patterns* và *Fundamentals of Software Architecture* (cùng thư mục) cho phần thiết kế API và kiến trúc |
| 9 | **Track mới: Functional Programming in Kotlin** ("Build Your Software Faster and Safer…") | `From Objects to Functions….pdf`, `Functional Programming in K_….pdf`, `Functional Programming in Kotlin by Tutorials.pdf`, Functional Kotlin |

Thêm track mới theo `E:\AndroidDeepDiveExplorer-Prompts\P-NEW-TRACK.md` và `TRACK-TEMPLATE.md`. Lõi không phải sửa.

## Coroutines v2: dàn chương dự kiến (bám bố cục Deep Dive, kiểm lại với mục lục sách trước khi viết)

**Phần 1: Hiểu coroutine**
- Vì sao cần coroutine: callback, RxJava, thread.
- Sequence builder (`sequence`/`yield`) là bước đệm để hiểu suspension.
- Suspension hoạt động thế nào: `suspendCoroutine`, `Continuation`, resume với giá trị hoặc exception.
- Coroutine dưới mui xe:
  - CPS;
  - state machine với `label`;
  - continuation lồng nhau như call stack;
  - giá cả hiệu năng.
- Hỗ trợ của ngôn ngữ so với thư viện kotlinx.

**Phần 2: Thư viện**
- Builder: `launch`, `async`, `runBlocking`.
- `CoroutineContext`: là một map, dùng phép `+`, có các phần tử như `Job`, dispatcher, tên, handler.
- Job và chờ con.
- Hủy:
  - hủy là hợp tác;
  - `CancellationException`;
  - `NonCancellable`;
  - `ensureActive`.
- Xử lý exception: `SupervisorJob`, `supervisorScope`, `CoroutineExceptionHandler`.
- Scope functions: `coroutineScope`, `withContext`, `withTimeout`.
- Dispatchers: Default, IO, Main, `limitedParallelism`.
- Tự dựng scope.
- Shared state: `Mutex`, atomic, giới hạn luồng.
- Test: `runTest`, thời gian ảo.

**Phần 3: Channel và Flow**
- Channel và `select`.
- Nguồn nóng và lạnh.
- Flow:
  - Flow tự dựng từ đầu (để hiểu bản chất);
  - tạo flow, vòng đời (`onStart`, `onCompletion`, `catch`);
  - xử lý (`map`, `flatMapConcat`/`Merge`/`Latest`, `combine`, `zip`);
  - `SharedFlow`/`StateFlow`, `stateIn`/`shareIn`;
  - test flow.

**Phần 4: Thực hành Android**
- `viewModelScope`, `lifecycleScope`, `repeatOnLifecycle`.
- Các bug thường gặp: rò scope, nuốt `CancellationException`, `GlobalScope`, block luồng Main.

## Việc kỹ thuật đã làm trong phiên này

- `git init` và commit đầu tiên (snapshot P0–P8 cùng đợt đổi hình minh hoạ).
- `core.autocrlf=false` để generator vẫn tái tạo đúng từng byte.
