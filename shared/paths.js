/* Lộ trình học (master 2.2). Mỗi bước là 'trackId' hoặc 'trackId/chapterId'.
   Lộ trình chỉ hiện trên trang chủ khi có ít nhất một bước đã đăng ký.
   `start: true`: lộ trình cho người mới, trang chủ vẽ nó thành mục "Bắt đầu từ đâu" (mỗi bước kèm một câu "vì sao",
   khoá shared.path.<id>.why.<trackId>); `more`: các track nên học sau, tùy nhu cầu. Viết lại 2026-11-26: bỏ lộ trình
   dựa vào UX/UI (đang tạm dừng), thêm các track F–L. */
ADE.addPaths([
  { id: 'starter', start: true, steps: ['kotlin', 'coroutines', 'arch', 'storage', 'runtime', 'animation'],
    more: ['debugging', 'cleancode', 'fp', 'sysdesign'] },
  { id: 'compose-engineer', steps: ['kotlin', 'coroutines', 'runtime', 'animation', 'debugging'] },
  { id: 'app-engineer', steps: ['kotlin', 'coroutines', 'arch', 'storage', 'sysdesign'] },
  { id: 'code-quality', steps: ['kotlin', 'fp', 'cleancode', 'debugging'] }
]);
ADE.addSharedStrings('vi', {
  'shared.path.starter.title': 'Lộ trình cho người mới',
  'shared.path.starter.desc': 'Sáu bước theo thứ tự, từ ngôn ngữ tới giao diện. Mỗi bước dùng kiến thức của bước trước.',
  'shared.path.starter.why.kotlin': 'Ngôn ngữ nền. Mọi track khác đều viết mã bằng Kotlin.',
  'shared.path.starter.why.coroutines': 'Cách app làm việc lâu (gọi mạng, đọc file) mà giao diện không đứng hình.',
  'shared.path.starter.why.arch': 'Chia app thành các tầng để dễ sửa, dễ test.',
  'shared.path.starter.why.storage': 'Lưu dữ liệu xuống máy: file, DataStore, Room.',
  'shared.path.starter.why.runtime': 'Compose vẽ và vẽ lại giao diện thế nào khi state đổi.',
  'shared.path.starter.why.animation': 'Làm giao diện chuyển động mượt, từng khung hình.',
  'shared.path.compose-engineer.title': 'Kỹ sư Compose',
  'shared.path.compose-engineer.desc': 'Tập trung vào giao diện: coroutine, Compose Runtime, Animation, rồi đo và sửa hiệu năng.',
  'shared.path.app-engineer.title': 'Kỹ sư app',
  'shared.path.app-engineer.desc': 'Tập trung vào phần bên dưới giao diện: kiến trúc, lưu dữ liệu, rồi thiết kế cả hệ thống.',
  'shared.path.code-quality.title': 'Viết mã tốt hơn',
  'shared.path.code-quality.desc': 'Lập trình hàm, mã sạch, rồi gỡ lỗi có phương pháp.'
});
ADE.addSharedStrings('en', {
  'shared.path.starter.title': 'Path for newcomers',
  'shared.path.starter.desc': 'Six steps in order, from the language to the interface. Each step builds on the one before.',
  'shared.path.starter.why.kotlin': 'The base language. Every other track writes its code in Kotlin.',
  'shared.path.starter.why.coroutines': 'How an app does slow work (network calls, file reads) without freezing the interface.',
  'shared.path.starter.why.arch': 'Splitting an app into layers so it is easy to change and to test.',
  'shared.path.starter.why.storage': 'Saving data on the device: files, DataStore, Room.',
  'shared.path.starter.why.runtime': 'How Compose draws and redraws the interface when state changes.',
  'shared.path.starter.why.animation': 'Making the interface move smoothly, frame by frame.',
  'shared.path.compose-engineer.title': 'Compose engineer',
  'shared.path.compose-engineer.desc': 'Focused on the interface: coroutines, the Compose Runtime, Animation, then measuring and fixing performance.',
  'shared.path.app-engineer.title': 'App engineer',
  'shared.path.app-engineer.desc': 'Focused on what sits under the interface: architecture, storing data, then designing the whole system.',
  'shared.path.code-quality.title': 'Writing better code',
  'shared.path.code-quality.desc': 'Functional programming, clean code, then methodical debugging.'
});
