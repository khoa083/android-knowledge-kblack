/* Thuật ngữ track animation (tiếng Việt). frame-clock và launched-effect đã có ở track coroutines (id toàn cục). */
ADE.addGlossary('vi', 'animation', {
  "animation-spec": { term: "AnimationSpec", def: "Quy định cách giá trị đi từ đầu tới đích theo thời gian: spring, tween, keyframes, repeatable, snap.", chapter: "animation/c2" },
  "spring-spec": { term: "spring", def: "Spec mô phỏng lò xo với damping ratio và stiffness; giữ vận tốc liên tục khi đổi target. Mặc định của animate*AsState.", chapter: "animation/c2" },
  "tween-spec": { term: "tween", def: "Spec chạy trong một thời lượng với một easing; mặc định 300 ms và FastOutSlowInEasing.", chapter: "animation/c2" },
  "easing": { term: "easing", def: "Hàm biến tỉ lệ thời gian thành tỉ lệ tiến độ; các easing chuẩn là đường cubic-bezier.", chapter: "animation/c2" },
  "decay": { term: "decay animation", def: "Animation không có đích cố định: đích được tính từ vận tốc ban đầu, thường dùng sau fling.", chapter: "animation/c6" },
  "animatable": { term: "Animatable", def: "Value holder điều khiển bằng suspend API (animateTo, snapTo, animateDecay, stop); animation mới hủy animation đang chạy.", chapter: "animation/c6" },
  "animate-as-state": { term: "animate*AsState", def: "API trả về giá trị animation đi theo một target; đổi target giữa chừng thì chạy tiếp từ giá trị và vận tốc hiện tại.", chapter: "animation/c1" },
  "transition": { term: "Transition", def: "Nhiều giá trị animation cùng đi theo một state; mỗi child có thể có spec riêng.", chapter: "animation/c3" },
  "animated-visibility": { term: "AnimatedVisibility", def: "Composable animate việc hiện/ẩn; nội dung rời Composition sau khi exit kết thúc.", chapter: "animation/c4" },
  "animated-content": { term: "AnimatedContent", def: "Composable animate việc đổi nội dung theo targetState; phải dùng tham số của content lambda.", chapter: "animation/c4" },
  "target-value": { term: "target value", def: "Giá trị animation đang hướng tới; khác với current value đang hiển thị.", chapter: "animation/c1" },
  "test-clock": { term: "mainClock", def: "Đồng hồ test của ComposeTestRule; tắt autoAdvance để tự tiến thời gian, advanceTimeBy làm tròn lên theo frame.", chapter: "animation/c8" },
  "graphics-layer": { term: "graphicsLayer", def: "Modifier biến đổi lúc vẽ (scale, translation, alpha…); đọc state trong lambda của nó chỉ ảnh hưởng phase draw.", chapter: "animation/c7" }
});
