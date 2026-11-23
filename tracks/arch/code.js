/* Đoạn mã track G (minh họa, rút gọn; không chạy trong trang). Số dòng được tham chiếu bởi codeHighlight trong models/models.js. */
(function () {
  var add = function (id, lines) { ADE.addCode('arch', id, { lang: 'kotlin', illustrative: true, lines: lines }); };
  var c = function (vi, en) { return { vi: vi, en: en }; };
  add('g1.god', [
    'class ChooseTimeActivity : ComponentActivity() {',
    c('    private var slots: List<Slot> = emptyList()      // dữ liệu nằm trong Activity', '    private var slots: List<Slot> = emptyList()      // data lives in the Activity'),
    '    fun onBookClick(day: LocalDate) = lifecycleScope.launch {',
    c('        val json = http.get("/slots?day=$day")        // gọi mạng', '        val json = http.get("/slots?day=$day")        // network call'),
    c('        slots = parseSlots(json)                      // tự parse JSON', '        slots = parseSlots(json)                      // parses JSON itself'),
    c('        prefs.edit { putString("cache", json) }       // tự lưu cache', '        prefs.edit { putString("cache", json) }       // caches it itself'),
    c('        render(slots)                                 // cập nhật UI', '        render(slots)                                 // updates the UI'),
    '    }',
    '}'
  ]);
  add('g1.layered', [
    'class ChooseTimeActivity : ComponentActivity() {',
    '    private val vm: ChooseTimeViewModel by viewModels()',
    c('    // UI chỉ gửi sự kiện và vẽ state', '    // the UI only sends events and draws state'),
    '}',
    'class ChooseTimeViewModel(private val repo: SlotRepository) : ViewModel() {',
    '    val state = MutableStateFlow<UiState>(UiState.Loading)',
    '}',
    'class SlotRepository(private val remote: SlotApi, private val local: SlotDao) { … }',
    c('class SlotApi { fun slots(day: LocalDate): List<SlotDto> = … }   // chỉ nơi này biết JSON', 'class SlotApi { fun slots(day: LocalDate): List<SlotDto> = … }   // the only place that knows the JSON'),
    c('// kiểm thử trên máy, không cần thiết bị:', '// tested on your machine, no device needed:'),
    'val vm = ChooseTimeViewModel(FakeSlotRepository(listOf(slot9h)))',
    'vm.load(today); assertEquals(UiState.Success(listOf(slot9h)), vm.state.value)'
  ]);
})();
