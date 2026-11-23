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
  add('aas_impl', [
    '@Composable',
    { vi: 'fun animateFloatAsState(targetValue: Float, /* … */): State<Float> {   // rút gọn từ animateValueAsState', en: 'fun animateFloatAsState(targetValue: Float, /* … */): State<Float> {   // condensed from animateValueAsState' },
    '    val coroutineScope = rememberCoroutineScope()',
    '    var updating = true',
    '    val state = remember { AnimateAsState(targetValue, /* … */, coroutineScope).also { updating = false } }',
    { vi: '    if (updating) SideEffect {                       // không chạy ở lần đầu', en: '    if (updating) SideEffect {                       // does not run the first time' },
    '        state.update(targetValue, /* … */) }',
    '    return state',
    { vi: '}   // đọc state.value → animatable.value', en: '}   // reading state.value → animatable.value' },
    '// AnimateAsState.update():',
    'if (target != animatable.targetValue) restartAnimation(target, spec, isInterrupted)',
    '// restartAnimation():',
    'job?.cancel()',
    'val specToUse = if (animSpec is InterruptionAwareAnimationSpec<T>) /* … */ else animSpec',
    'job = coroutineScope.launch(start = CoroutineStart.UNDISPATCHED) {',
    '    animatable.animateTo(newTarget, specToUse)',
    { vi: '    // mỗi frame: animatable.value đổi → ai đọc state.value bị invalidate', en: '    // every frame: animatable.value changes → whoever reads state.value is invalidated' },
    '    finishedListener?.invoke(animatable.value)',
    '}'
  ]);
  [['vector_dp', 'Dp', 'animateDpAsState(if (big) 100.dp else 0.dp, tween(300))', 'Dp.VectorConverter                       // Dp ↔ AnimationVector1D'],
   ['vector_offset', 'Offset', 'animateOffsetAsState(if (moved) Offset(100f, 40f) else Offset.Zero, spring())', 'Offset.VectorConverter                   // Offset ↔ AnimationVector2D'],
   ['vector_color', 'Color', 'animateColorAsState(if (on) Color.White else Color.Red, tween(300))', 'Color.VectorConverter(colorSpace)        // Color ↔ AnimationVector4D (Oklab)'],
   ['vector_keyframes', 'Float', 'animateFloatAsState(if (go) 100f else 0f, keyframes { durationMillis = 300; 80f at 100; 60f at 200 })', 'Float.VectorConverter                    // Float ↔ AnimationVector1D']
  ].forEach(function (c) {
    add(c[0], [
      { vi: '// ' + c[1] + ': kiểu giá trị bạn animate', en: '// ' + c[1] + ': the value type you animate' },
      c[2],
      c[3],
      'val vSpec = spec.vectorize(converter)    // AnimationSpec<T> → VectorizedAnimationSpec<V>',
      { vi: 'val v = vSpec.getValueFromNanos(t, start, end, velocity)   // tính từng thành phần của vector', en: 'val v = vSpec.getValueFromNanos(t, start, end, velocity)   // computes each vector component' },
      { vi: 'val value = converter.convertFromVector(v)                  // trở lại kiểu ' + c[1], en: 'val value = converter.convertFromVector(v)                  // back to ' + c[1] }
    ]);
  });
  [['seg_update', 'enum class CardState { Collapsed, Expanded }', 'val transition = updateTransition(targetState = cardState, label = "card")'],
   ['seg_mutable', 'val state = remember { MutableTransitionState(CardState.Collapsed).apply { targetState = CardState.Expanded } }', 'val transition = rememberTransition(state, label = "card")']
  ].forEach(function (c) {
    add(c[0], [
      c[1],
      c[2],
      'val color by transition.animateColor(transitionSpec = { tween(300) }, label = "color") { if (it == Expanded) Teal else Gray }',
      'val height by transition.animateDp(transitionSpec = {',
      '    if (Collapsed isTransitioningTo Expanded) spring(stiffness = Spring.StiffnessLow) else tween(300)',
      '}, label = "height") { if (it == Expanded) 200.dp else 64.dp }',
      'val alpha by transition.animateFloat(transitionSpec = { tween(150) }, label = "alpha") { if (it == Expanded) 1f else 0f }',
      { vi: '// transition.currentState chỉ đổi khi MỌI con xong; transition.isRunning', en: '// transition.currentState only changes when EVERY child is done; transition.isRunning' }
    ]);
  });
  [['exit_builtin', '    Card { Text("Banner") }', '    // (không có animation tùy biến)', '    // (no custom animation)'],
   ['exit_custom', '    val bg by transition.animateColor(transitionSpec = { tween(500) }, label = "bg") {', '        if (it == EnterExitState.Visible) Teal else Gray }   // thuộc transition: được chờ', '        if (it == EnterExitState.Visible) Teal else Gray }   // part of the transition: waited for'],
   ['exit_outside', '    val scale by animateFloatAsState(if (visible) 1f else 0.5f, tween(500))', '    // ✗ KHÔNG thuộc transition: không ai chờ', '    // ✗ NOT part of the transition: nobody waits']
  ].forEach(function (c) {
    add(c[0], [
      'AnimatedVisibility(',
      '    visible = visible,',
      '    exit = fadeOut() + shrinkOut()',
      ') {',
      c[1],
      { vi: c[2], en: c[3] },
      '}'
    ]);
  });
  var acsTail = ['        .fillMaxWidth()', '        .clickable { expanded = !expanded }', ')'];
  add('acs_expand', [
    'var expanded by remember { mutableStateOf(false) }',
    'Box(',
    '    Modifier',
    '        .background(Teal)',
    { vi: '        .animateContentSize(finishedListener = { from, to -> log(from, to) })   // ✓ ngoài', en: '        .animateContentSize(finishedListener = { from, to -> log(from, to) })   // ✓ outer' },
    '        .height(if (expanded) 160.dp else 40.dp)'
  ].concat(acsTail));
  add('acs_after', [
    'var expanded by remember { mutableStateOf(false) }',
    'Box(',
    '    Modifier',
    '        .background(Teal)',
    { vi: '        .height(if (expanded) 160.dp else 40.dp)       // ✗ modifier kích thước đứng ngoài', en: '        .height(if (expanded) 160.dp else 40.dp)       // ✗ the size modifier is outside' },
    '        .animateContentSize(finishedListener = { from, to -> log(from, to) })'
  ].concat(acsTail));
  [['rep_restart3', 3, 'Restart'], ['rep_reverse3', 3, 'Reverse'], ['rep_reverse2', 2, 'Reverse']].forEach(function (c) {
    add(c[0], [
      'val v by animateFloatAsState(',
      '    targetValue = if (on) 1f else 0f,',
      '    animationSpec = repeatable(',
      '        iterations = ' + c[1] + ',',
      '        animation = tween(300, easing = LinearEasing),',
      '        repeatMode = RepeatMode.' + c[2],
      '    ),',
      '    label = "v"',
      ')'
    ]);
  });
  add('rep_infinite', [
    'val infinite = rememberInfiniteTransition(label = "pulse")',
    'val v by infinite.animateFloat(',
    '    initialValue = 0f,',
    '    targetValue = 1f,',
    '    animationSpec = infiniteRepeatable(',
    '        animation = tween(300, easing = LinearEasing),',
    '        repeatMode = RepeatMode.Reverse',
    '    ),',
    '    label = "v"',
    ')'
  ]);
  add('mutex_retarget', [
    'val offset = remember { Animatable(0f) }',
    { vi: '// coroutine A', en: '// coroutine A' },
    'scope.launch {',
    '    offset.animateTo(100f)',
    { vi: '    onArrived()                 // ✗ không chạy nếu bị ngắt', en: '    onArrived()                 // ✗ never runs if interrupted' },
    '}',
    { vi: '// coroutine B, lát sau', en: '// coroutine B, a moment later' },
    'scope.launch { offset.animateTo(0f) }'
  ]);
  add('mutex_swipe', [
    'offsetX.stop()',
    'horizontalDrag(id) { change ->',
    '    launch { offsetX.snapTo(offsetX.value + change.positionChange().x) }',
    '    tracker.addPosition(change.uptimeMillis, change.position)',
    '}',
    'val velocity = tracker.calculateVelocity().x',
    'val target = decay.calculateTargetValue(offsetX.value, velocity)',
    'offsetX.updateBounds(-width, width)',
    'if (target.absoluteValue <= width) offsetX.animateTo(0f, initialVelocity = velocity)',
    'else { offsetX.animateDecay(velocity, decay); onDismissed() }'
  ]);
  var seHead = ['SharedTransitionLayout {', '    AnimatedContent(showDetails, label = "screen") { details ->', '        Image(painter, null, Modifier'];
  var seTail = ['            .size(if (details) DpSize(360.dp, 240.dp) else DpSize(64.dp, 64.dp)))', '    }', '}'];
  add('shared_match', seHead.concat([
    '            .sharedElement(rememberSharedContentState(key = "image"), this@AnimatedContent)',
    { vi: '            .clip(RoundedCornerShape(16.dp))     // ✓ sau sharedElement', en: '            .clip(RoundedCornerShape(16.dp))     // ✓ after sharedElement' }
  ]).concat(seTail));
  add('shared_nomatch', seHead.concat([
    { vi: '            .sharedElement(rememberSharedContentState(key = if (details) "img-1" else "image"), this@AnimatedContent)   // ✗ khác key', en: '            .sharedElement(rememberSharedContentState(key = if (details) "img-1" else "image"), this@AnimatedContent)   // ✗ different keys' },
    '            .clip(RoundedCornerShape(16.dp))'
  ]).concat(seTail));
  add('shared_clip', seHead.concat([
    { vi: '            .clip(RoundedCornerShape(16.dp))     // ✗ trước sharedElement', en: '            .clip(RoundedCornerShape(16.dp))     // ✗ before sharedElement' },
    '            .sharedElement(rememberSharedContentState(key = "image"), this@AnimatedContent)'
  ]).concat(seTail));
  add('avd_canvas', [
    'val sweep by animateFloatAsState(progress * 360f, label = "sweep")',
    'Canvas(Modifier.size(64.dp)) {',
    '    drawArc(',
    '        color = Teal, startAngle = -90f,',
    { vi: '        sweepAngle = sweep,                 // đọc trong lambda vẽ', en: '        sweepAngle = sweep,                 // read in the draw lambda' },
    '        useCenter = false, style = Stroke(8.dp.toPx()))',
    '}'
  ]);
  add('avd_vector', [
    'val image = AnimatedImageVector.animatedVectorResource(R.drawable.ic_hourglass_animated)',
    'var atEnd by remember { mutableStateOf(false) }',
    'Image(',
    { vi: '    painter = rememberAnimatedVectorPainter(image, atEnd),   // bên trong: updateTransition(atEnd)', en: '    painter = rememberAnimatedVectorPainter(image, atEnd),   // inside: updateTransition(atEnd)' },
    '    contentDescription = "Timer",',
    '    modifier = Modifier.clickable { atEnd = !atEnd }',
    ')'
  ]);
  add('vf_property', [
    'ObjectAnimator.ofFloat(button, "translationX", 0f, 40f).apply {',
    '    duration = 40',
    '    interpolator = AccelerateDecelerateInterpolator()',
    { vi: '}.start()                       // gọi setTranslationX mỗi frame', en: '}.start()                       // calls setTranslationX every frame' }
  ]);
  add('vf_viewanim', [
    'TranslateAnimation(0f, 40f, 0f, 0f).apply {',
    '    duration = 40; fillAfter = true',
    '    interpolator = AccelerateDecelerateInterpolator()',
    { vi: '}.also { button.startAnimation(it) }   // ✗ chỉ dời hình vẽ', en: '}.also { button.startAnimation(it) }   // ✗ only moves the drawing' }
  ]);
  add('vf_compose', [
    'val x by animateFloatAsState(if (moved) 40f else 0f,',
    '    tween(durationMillis = 40,',
    '        easing = Easing { t -> (cos((t + 1) * PI) / 2 + 0.5).toFloat() }), label = "x")',
    { vi: 'Button(onClick, Modifier.offset { IntOffset(x.roundToInt(), 0) }) { … }   // đọc ở bước đặt', en: 'Button(onClick, Modifier.offset { IntOffset(x.roundToInt(), 0) }) { … }   // read at placement' }
  ]);
  add('fo_body', [
    'val a by animateFloatAsState(if (shown) 1f else 0f, label = "a")',
    { vi: 'Box(Modifier.alpha(a))          // đọc trong thân: recompose mỗi frame', en: 'Box(Modifier.alpha(a))          // read in the body: recompose every frame' }
  ]);
  add('fo_layer', [
    'val a by animateFloatAsState(if (shown) 1f else 0f, label = "a")',
    { vi: 'Box(Modifier.graphicsLayer { alpha = a })   // chỉ cập nhật lớp vẽ', en: 'Box(Modifier.graphicsLayer { alpha = a })   // only the layer updates' }
  ]);
  add('cs_manual', [
    'rule.mainClock.autoAdvance = false',
    { vi: 'enabled = true                         // khởi động tween(250)', en: 'enabled = true                         // kick off tween(250)' },
    { vi: '// frame 16: recompose; frame 32: thời gian chơi = 0', en: '// frame 16: recompose; frame 32: play time = 0' },
    { vi: 'rule.mainClock.advanceTimeBy(50L)      // làm tròn lên 64', en: 'rule.mainClock.advanceTimeBy(50L)      // rounds up to 64' },
    'rule.onRoot().captureToImage().assertAgainstGolden()'
  ]);
  add('cs_ignore', [
    'rule.mainClock.autoAdvance = false',
    'enabled = true',
    'rule.mainClock.advanceTimeBy(50L, ignoreFrameDuration = true)',
    { vi: '// đồng hồ ở 50, nhưng frame chỉ ở 16, 32, 48', en: '// the clock is at 50, but frames only at 16, 32, 48' }
  ]);
  add('cs_auto', [
    { vi: '// autoAdvance = true (mặc định)', en: '// autoAdvance = true (default)' },
    'enabled = true',
    { vi: 'rule.onNodeWithTag("box").assertExists()   // chờ idle: chạy animation tới cuối', en: 'rule.onNodeWithTag("box").assertExists()   // idle wait: runs the animation to the end' }
  ]);
})();
