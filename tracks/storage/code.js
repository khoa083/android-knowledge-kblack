/* Đoạn mã track H (minh họa, rút gọn; không chạy trong trang). Số dòng được tham chiếu bởi codeHighlight trong models/models.js. */
(function () {
  var add = function (id, lines) { ADE.addCode('storage', id, { lang: 'kotlin', illustrative: true, lines: lines }); };
  var c = function (vi, en) { return { vi: vi, en: en }; };
  add('h3.commit', [
    c('// màn Cài đặt, trong onClick (main thread)', '// Settings screen, inside onClick (main thread)'),
    c('val ok = prefs.edit().putBoolean("dark_theme", true).commit()   // chờ ghi xong cả file', 'val ok = prefs.edit().putBoolean("dark_theme", true).commit()   // waits for the whole file to be written'),
    c('if (ok) recreate()                                                // chỉ chạy khi commit trả về', 'if (ok) recreate()                                                // runs only once commit returns')
  ]);
  add('h3.apply', [
    c('// màn Cài đặt, trong onClick (main thread)', '// Settings screen, inside onClick (main thread)'),
    c('prefs.edit().putBoolean("dark_theme", true).apply()   // đổi bộ nhớ ngay, xếp hàng ghi đĩa', 'prefs.edit().putBoolean("dark_theme", true).apply()   // memory now, disk write queued'),
    c('recreate()', 'recreate()'),
    c('// onStop(): framework chờ các lần apply() đang ghi xong rồi mới chuyển trạng thái', '// onStop(): the framework waits for in-flight apply() writes before switching state'),
    c('// ghi lỗi: không ai được báo', '// a failed write: nobody is told')
  ]);
  add('h3.datastore', [
    'val Context.dataStore by preferencesDataStore(name = "settings")',
    'val DARK = booleanPreferencesKey("dark_theme")',
    c('val dark: Flow<Boolean> = context.dataStore.data', 'val dark: Flow<Boolean> = context.dataStore.data'),
    c('    .map { it[DARK] ?: false }                       // UI thu Flow này', '    .map { it[DARK] ?: false }                       // the UI collects this Flow'),
    c('// màn Cài đặt: onClick → ViewModel', '// Settings screen: onClick → ViewModel'),
    c('fun onDarkChanged(v: Boolean) = viewModelScope.launch {', 'fun onDarkChanged(v: Boolean) = viewModelScope.launch {'),
    c('    context.dataStore.edit { it[DARK] = v }          // suspend: main không bị chặn', '    context.dataStore.edit { it[DARK] = v }          // suspend: main is not blocked'),
    '}'
  ]);
  add('h2.direct', [
    'fun saveDraft(text: String) {',
    c('    FileOutputStream(File(filesDir, "draft.txt")).use { out ->   // mở: file bị cắt về 0 byte', '    FileOutputStream(File(filesDir, "draft.txt")).use { out ->   // open: the file is truncated to 0 bytes'),
    c('        out.write(text.toByteArray())                          // tiến trình chết ở đây: file dở dang', '        out.write(text.toByteArray())                          // process dies here: a half-written file'),
    '    }',
    '}',
    c('fun loadDraft(): String =', 'fun loadDraft(): String ='),
    c('    File(filesDir, "draft.txt").readText()                     // đọc được nửa bản nháp', '    File(filesDir, "draft.txt").readText()                     // reads half a draft')
  ]);
  add('h2.atomic', [
    'fun saveDraft(text: String) {',
    '    val file = AtomicFile(File(filesDir, "draft.txt"))',
    c('    val out = file.startWrite()                                // ghi vào draft.txt.new', '    val out = file.startWrite()                                // writes to draft.txt.new'),
    c('    try { out.write(text.toByteArray()); file.finishWrite(out) } // sync rồi đổi tên đè lên', '    try { out.write(text.toByteArray()); file.finishWrite(out) } // sync, then rename over'),
    c('    catch (e: IOException) { file.failWrite(out); throw e }     // xóa file .new', '    catch (e: IOException) { file.failWrite(out); throw e }     // deletes the .new file'),
    '}',
    'fun loadDraft(): String =',
    '    AtomicFile(File(filesDir, "draft.txt"))',
    c('        .readFully().decodeToString()                          // luôn là bản trọn vẹn gần nhất', '        .readFully().decodeToString()                          // always the last complete version')
  ]);
  add('h2.cache', [
    'suspend fun resultPdf(id: Long): File {',
    c('    val f = File(cacheDir, "result-$id.pdf")', '    val f = File(cacheDir, "result-$id.pdf")'),
    c('    // lần đầu: tải về và ghi vào cache', '    // first time: download and write to the cache'),
    c('    // … vài ngày sau, máy thiếu chỗ: hệ thống có thể xóa f', '    // … days later, space runs low: the system may delete f'),
    c('    return f                    // sai: mở thẳng, f có thể đã không còn', '    return f                    // wrong: opened as is, f may be gone'),
    '}',
    c('suspend fun resultPdfSafe(id: Long): File {', 'suspend fun resultPdfSafe(id: Long): File {'),
    '    val f = File(cacheDir, "result-$id.pdf")',
    c('    if (!f.exists()) api.download(id, f)   // kiểm trước khi đọc, thiếu thì tải lại', '    if (!f.exists()) api.download(id, f)   // check before reading, download again if missing'),
    '    return f',
    '}'
  ]);
})();
