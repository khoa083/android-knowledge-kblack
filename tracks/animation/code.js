/* Đoạn mã track C (minh họa). Số dòng được tham chiếu bởi codeHighlight trong models/models.js. */
(function () {
  var add = function (id, lines) { ADE.addCode('animation', id, { lang: 'kotlin', illustrative: true, lines: lines }); };
  var c = function (vi, en) { return { vi: vi, en: en }; };
  add('choose', [
    c('// một giá trị theo target', '// one value following a target'),
    'val alpha by animateFloatAsState(if (visible) 1f else 0f)',
    c('// nhiều giá trị theo một state', '// several values following one state'),
    'val t = updateTransition(expanded)',
    c('// gesture, fling, tuần tự', '// gestures, flings, sequences'),
    'val offset = remember { Animatable(0f) }'
  ]);
  add('retarget', [
    'var target by remember { mutableFloatStateOf(0f) }',
    'val x by animateFloatAsState(target)',
    'Box(Modifier.offset { IntOffset(x.roundToInt(), 0) })'
  ]);
  add('spec', [
    'spring(dampingRatio = Spring.DampingRatioNoBouncy, stiffness = Spring.StiffnessMedium)',
    'tween(durationMillis = 300, easing = FastOutSlowInEasing)',
    'keyframes { durationMillis = 300; 60f at 75; 40f at 180 }',
    'repeatable(iterations = 2, animation = tween(300), repeatMode = RepeatMode.Reverse)',
    'snap(delayMillis = 150)',
    'exponentialDecay(frictionMultiplier = 1f)'
  ]);
  add('transition', [
    'val t = updateTransition(cardState, label = "card")',
    'val color by t.animateColor(label = "color") { if (it == Expanded) Teal else Gray }',
    'val height by t.animateDp(transitionSpec = { spring() }, label = "height") { if (it == Expanded) 200.dp else 72.dp }',
    'val alpha by t.animateFloat(label = "alpha") { if (it == Expanded) 1f else 0.6f }',
    c('// transitionSpec có thể khác nhau theo hướng chuyển', '// transitionSpec can differ by direction')
  ]);
  add('visibility', [
    'AnimatedVisibility(visible = shown,',
    '  enter = fadeIn() + expandVertically(), exit = fadeOut() + shrinkVertically()) {',
    '  Banner()',
    '}',
    c('val a by animateFloatAsState(...)   // ngoài Transition: không được theo dõi', 'val a by animateFloatAsState(...)   // outside the Transition: not tracked'),
    '',
    'AnimatedContent(targetState = page) { target ->',
    c('  PageContent(target)               // dùng tham số lambda, không dùng page', '  PageContent(target)               // use the lambda parameter, not page'),
    '}',
    'Crossfade(targetState = page) { target -> PageContent(target) }'
  ]);
  add('size', [
    'Box(Modifier',
    c('  .animateContentSize()              // đặt TRƯỚC modifier kích thước', '  .animateContentSize()              // placed BEFORE size modifiers'),
    '  .height(if (expanded) 200.dp else 72.dp))',
    '',
    'Box(Modifier.size(72.dp)',
    '  .graphicsLayer { scaleY = s })       // chỉ đổi lúc vẽ / draw-time only',
    '',
    'Box(Modifier.offset { IntOffset(0, dy.roundToInt()) })'
  ]);
  add('gesture', [
    'val offsetX = remember { Animatable(0f) }',
    'Modifier.pointerInput(Unit) {',
    '  coroutineScope { while (true) {',
    c('    awaitPointerEventScope { awaitFirstDown() }; offsetX.stop()   // chạm: dừng animation', '    awaitPointerEventScope { awaitFirstDown() }; offsetX.stop()   // touch: stop the animation'),
    c('    // kéo: offsetX.snapTo(...), VelocityTracker ghi vị trí', '    // drag: offsetX.snapTo(...), VelocityTracker records positions'),
    c('    // thả: target = decay.calculateTargetValue(...)', '    // release: target = decay.calculateTargetValue(...)'),
    '    launch { offsetX.animateTo(0f, initialVelocity = velocity) }',
    '  } }',
    '}.offset { IntOffset(offsetX.value.roundToInt(), 0) }'
  ]);
  add('phaseread', [
    'val x by animateFloatAsState(target)',
    c('// 1) đọc trong composition', '// 1) read in composition'),
    'Box(Modifier.offset(x = x.dp))',
    c('// 2) đọc trong layout (placement)', '// 2) read in layout (placement)'),
    'Box(Modifier.offset { IntOffset(x.roundToInt(), 0) })',
    c('// 3) đọc trong draw', '// 3) read in drawing'),
    'Box(Modifier.graphicsLayer { translationX = x })'
  ]);
  add('testclock', [
    '@get:Rule val rule = createComposeRule()',
    c('// mặc định: autoAdvance = true', '// default: autoAdvance = true'),
    'rule.mainClock.autoAdvance = false',
    'rule.mainClock.advanceTimeBy(150)',
    'rule.onNodeWithTag("box").assertWidthIsEqualTo(...)'
  ]);
})();
