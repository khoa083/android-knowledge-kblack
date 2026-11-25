/* Đoạn mã track L (minh họa, rút gọn; không chạy trong trang). Số dòng được tham chiếu bởi codeHighlight trong models/models.js. */
(function () {
  var add = function (id, lines) { ADE.addCode('debugging', id, { lang: 'kotlin', illustrative: true, lines: lines }); };
  var c = function (vi, en) { return { vi: vi, en: en }; };

  /* l1: hai bản sửa theo đoán: khóa màn hình dọc (dòng 1–2) và phép kiểm isInitialized (dòng 7) */
  add('l1.guess', [
    c('// AndroidManifest.xml, bản 1.4.1', '// AndroidManifest.xml, release 1.4.1'),
    '<activity android:name=".MainActivity" android:screenOrientation="portrait" />',
    'class BookingDetailFragment : Fragment() {',
    '    private lateinit var booking: Booking',
    '    fun show(b: Booking) { booking = b }',
    '    override fun onViewCreated(view: View, saved: Bundle?) {',
    c('        if (!::booking.isInitialized) return        // bản 1.4.2: hết crash, ra màn trống', '        if (!::booking.isInitialized) return        // release 1.4.2: no crash, a blank screen'),
    '        binding.patient.text = booking.patientName',
    '    }',
    '}'
  ]);
  /* l1: nguyên nhân: dữ liệu chỉ vào qua setter (dòng 3), đọc ở dòng 5 */
  add('l1.bug', [
    'class BookingDetailFragment : Fragment() {',
    '    private lateinit var booking: Booking',
    c('    fun show(b: Booking) { booking = b }          // chỉ màn danh sách gọi', '    fun show(b: Booking) { booking = b }          // only the list screen calls it'),
    '    override fun onViewCreated(view: View, saved: Bundle?) {',
    c('        binding.patient.text = booking.patientName   // tạo lại: UninitializedPropertyAccessException', '        binding.patient.text = booking.patientName   // after recreation: UninitializedPropertyAccessException'),
    '    }',
    '}'
  ]);
  /* l1: sửa: id đi qua arguments (dòng 2, 9), hệ thống lưu và trả lại khi tạo lại Fragment */
  add('l1.fix', [
    'class BookingDetailFragment : Fragment() {',
    '    private val bookingId get() = requireArguments().getLong("bookingId")',
    '    private val vm: DetailViewModel by viewModels()',
    '    override fun onViewCreated(view: View, saved: Bundle?) {',
    '        vm.load(bookingId)',
    '        vm.booking.observe(viewLifecycleOwner) { binding.patient.text = it.patientName }',
    '    }',
    '}',
    c('BookingDetailFragment().apply { arguments = bundleOf("bookingId" to booking.id) }   // màn danh sách', 'BookingDetailFragment().apply { arguments = bundleOf("bookingId" to booking.id) }   // the list screen'),
    c('// thêm test: launchFragmentInContainer(...).recreate(), kiểm tên bệnh nhân vẫn hiện', '// add a test: launchFragmentInContainer(...).recreate(), check the patient name still shows')
  ]);
})();
