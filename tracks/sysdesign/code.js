/* Đoạn mã track I (minh họa, rút gọn; không chạy trong trang). Số dòng được tham chiếu bởi codeHighlight trong models/models.js. */
(function () {
  var add = function (id, lines) { ADE.addCode('sysdesign', id, { lang: 'kotlin', illustrative: true, lines: lines }); };
  var c = function (vi, en) { return { vi: vi, en: en }; };
  add('i2.vm', [
    'class BookingViewModel : ViewModel() {',
    c('    var doctorId by mutableStateOf<Long?>(null)     // chỉ trong bộ nhớ của process', '    var doctorId by mutableStateOf<Long?>(null)     // only in the process\'s memory'),
    '    var note by mutableStateOf("")',
    c('    var photoUri: Uri? = null                      // Uri của tệp ảnh sắp chụp', '    var photoUri: Uri? = null                      // Uri of the photo file about to be taken'),
    '}',
    c('// Activity: mở Camera, app bị che hẳn → onStop, process vào nhóm cached', '// Activity: open the Camera, the app is fully covered → onStop, the process goes cached'),
    'takePhoto.launch(vm.photoUri)',
    c('// lmkd giết process: ViewModel mất; onDestroy() có thể không chạy', '// lmkd kills the process: the ViewModel is gone; onDestroy() may not run'),
    c('// process mới: ViewModel mới, doctorId = null, note = "", photoUri = null', '// new process: a new ViewModel, doctorId = null, note = "", photoUri = null')
  ]);
  add('i2.saved', [
    'class BookingViewModel(private val state: SavedStateHandle) : ViewModel() {',
    c('    val doctorId = state.getStateFlow<Long?>("doctorId", null)   // chỉ một id', '    val doctorId = state.getStateFlow<Long?>("doctorId", null)   // just an id'),
    '    val note = state.getStateFlow("note", "")',
    c('    fun photoTarget(uri: Uri) { state["photoUri"] = uri }       // Uri, không phải ảnh', '    fun photoTarget(uri: Uri) { state["photoUri"] = uri }       // the Uri, not the image'),
    '}',
    c('// onStop: hệ thống sao saved state ra ngoài process', '// onStop: the system copies saved state outside the process'),
    c('// lmkd giết process: ViewModel mất, bản sao saved state còn', '// lmkd kills the process: the ViewModel is gone, the saved-state copy remains'),
    c('val takePhoto = registerForActivityResult(TakePicture()) { ok ->   // đăng ký mỗi lần tạo Activity', 'val takePhoto = registerForActivityResult(TakePicture()) { ok ->   // registered on every creation'),
    c('    if (ok) vm.attachPhoto()                    // đọc photoUri từ SavedStateHandle đã khôi phục', '    if (ok) vm.attachPhoto()                    // reads photoUri from the restored SavedStateHandle'),
    '}'
  ]);
})();
