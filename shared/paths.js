/* Lộ trình học (master 2.2). Mỗi bước là 'trackId' hoặc 'trackId/chapterId'.
   Lộ trình chỉ hiện trên trang chủ khi có ít nhất một bước đã đăng ký. */
ADE.addPaths([
  { id: 'compose-engineer', steps: ['coroutines', 'runtime', 'animation', 'ui/e8', 'ui/e10'] },
  { id: 'product-designer', steps: ['ux', 'ui', 'runtime/b9', 'animation/c0'] },
  { id: 'full-stack-android', steps: ['coroutines', 'runtime', 'animation', 'ux', 'ui'] }
]);
ADE.addSharedStrings('vi', {
  'shared.path.compose-engineer.title': 'Kỹ sư Compose',
  'shared.path.compose-engineer.desc': 'Từ coroutine tới Compose Runtime và Animation, rồi sang design token và accessibility để triển khai giao diện đúng cách.',
  'shared.path.product-designer.title': 'Product designer làm việc với Android',
  'shared.path.product-designer.desc': 'Bắt đầu từ cách con người nghĩ và hành động, sang giao diện Android, rồi nhìn một chút bên dưới để hiểu vì sao Compose cư xử như vậy.',
  'shared.path.full-stack-android.title': 'Android toàn diện',
  'shared.path.full-stack-android.desc': 'Đi qua cả năm track theo thứ tự: engineering trước, design sau, với các chương cầu nối nối hai bên.'
});
ADE.addSharedStrings('en', {
  'shared.path.compose-engineer.title': 'Compose engineer',
  'shared.path.compose-engineer.desc': 'From coroutines to the Compose Runtime and Animation, then design tokens and accessibility so you can ship the interface properly.',
  'shared.path.product-designer.title': 'Product designer working with Android',
  'shared.path.product-designer.desc': 'Start with how people think and act, move on to Android interfaces, then look a little underneath to see why Compose behaves the way it does.',
  'shared.path.full-stack-android.title': 'Android, end to end',
  'shared.path.full-stack-android.desc': 'Go through all five tracks in order: engineering first, design after, with bridge chapters connecting the two sides.'
});
