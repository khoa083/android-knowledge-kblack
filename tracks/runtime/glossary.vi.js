/* Thuật ngữ track runtime (tiếng Việt). */
ADE.addGlossary('vi', 'runtime', {
  "composition": { term: "Composition", def: "Kết quả của việc chạy các composable cho một cây UI, được runtime giữ và cập nhật tăng dần.", chapter: "runtime/b0" },
  "recomposition": { term: "recomposition", def: "Chạy lại các composable có thể đã đổi khi đầu vào đổi; phần không đổi được skip. Không đồng nghĩa với vẽ lại.", chapter: "runtime/b7" },
  "recomposer": { term: "Recomposer", def: "Bộ lập lịch recomposition và việc áp dụng thay đổi cho một hoặc nhiều Composition.", chapter: "runtime/b5" },
  "composer": { term: "Composer", def: "Giao diện mà mã do Compose Compiler sinh ra gọi tới để nhớ theo vị trí, phát hiện thay đổi và chạy lại tăng dần.", chapter: "runtime/b2" },
  "applier": { term: "Applier", def: "Thành phần áp dụng thao tác cây (chèn, xóa, di chuyển, cập nhật) mà composition phát ra; generic theo kiểu node.", chapter: "runtime/b6" },
  "slot-table": { term: "SlotTable", def: "Dữ liệu theo group và vị trí dùng để nhớ giá trị và nhận diện phần composition; không phải cây UI. Chi tiết cài đặt có thể đổi.", chapter: "runtime/b3" },
  "snapshot": { term: "Snapshot", def: "Góc nhìn cách ly về giá trị của các state object; thay đổi trong mutable snapshot được apply nguyên tử.", chapter: "runtime/b4" },
  "restart-scope": { term: "restart scope", def: "Phần composition có thể chạy lại riêng khi state nó đã đọc thay đổi.", chapter: "runtime/b2" },
  "composition-identity": { term: "composition identity", def: "Cách runtime nhận ra cùng một instance composable giữa các lần chạy: call site, thứ tự và key().", chapter: "runtime/b3" },
  "stability": { term: "stability", def: "Tính chất của kiểu cho biết Compose có thể so tham số bằng equals và tin rằng mọi thay đổi được báo.", chapter: "runtime/b8" },
  "strong-skipping": { term: "strong skipping", def: "Chế độ compiler (mặc định từ Kotlin 2.0.20) cho composable có tham số unstable được skip, so tham số unstable bằng ===.", chapter: "runtime/b8" },
  "compose-phases": { term: "Compose phases", def: "Ba phase Composition, Layout, Drawing; phase đọc state là phase cần chạy lại.", chapter: "runtime/b7" },
  "semantics-tree": { term: "semantics tree", def: "Cây song song mô tả ý nghĩa của phần tử UI, dùng cho dịch vụ trợ năng và kiểm thử.", chapter: "runtime/b9" },
  "compose-view": { term: "ComposeView", def: "View của Android chứa nội dung Compose; composition ban đầu khi gắn window hoặc createComposition().", chapter: "runtime/b1" },
  "composition-local": { term: "CompositionLocal", def: "Dữ liệu được truyền ngầm xuống theo cây composition, ví dụ theme.", chapter: "runtime/b0" }
});
