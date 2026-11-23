# Kotlin · chuỗi cho hình trực quan (tracks/kotlin/views/visuals.js): bảng bucket K4, bảng từng phần tử K9,
# ma trận gán K10, hộp receiver K12, bảng tra K0. Không có khẳng định mới; chỉ trình bày lại dữ liệu của các chương.


def add(a):
    v = lambda k, vi, en: a('vz.' + k, vi, en)
    for k, vi, en in [('hash', 'Bảng bucket', 'Bucket table'), ('seq', 'Bảng từng phần tử', 'Element grid'), ('var', 'Ma trận gán', 'Assignment matrix'),
                      ('scope', 'Hộp receiver', 'Receiver boxes'), ('map', 'Bảng tra', 'Lookup table')]:
        v('tab.' + k, vi, en)
    # K4
    v('hash.cap', 'Bảng băm chia phần tử vào các ô (bucket) theo hashCode. Ở đây bucket = tổng mã ký tự của khoá chia lấy dư 4, chỉ để minh họa; HashSet thật dùng nhiều ô hơn và đổi kích thước.',
      'A hash table spreads elements into slots (buckets) by hashCode. Here bucket = sum of the key\'s character codes mod 4, for illustration only; a real HashSet uses more buckets and resizes.')
    v('hash.colBucket', 'Ô (bucket)', 'Bucket'); v('hash.colItems', 'Phần tử đang nằm ở đây', 'Elements stored here')
    v('hash.look', 'contains tìm ở ô {b}', 'contains looks in bucket {b}')
    v('hash.found', 'tìm thấy', 'found'); v('hash.notFound', 'ô trống, không tìm thấy', 'empty bucket, not found'); v('hash.empty', 'trống', 'empty')
    v('hash.newHash', 'Sau khi sửa surname, hashCode của lan giờ trỏ tới ô {b}, nhưng object vẫn nằm ở ô cũ.', 'After surname changes, lan\'s hashCode now points to bucket {b}, but the object still sits in the old one.')
    v('hash.copy', 'bản copy', 'the copy')
    v('hash.moved', 'Bỏ lan khỏi ô {a}, thêm bản copy vào ô {b}: vị trí luôn khớp với hashCode.', 'lan is removed from bucket {a} and the copy added to bucket {b}: positions always match the hashCode.')
    v('hash.idOnly', 'hashCode chỉ tính từ id (property của constructor chính), nên luôn là ô {b}.', 'hashCode is computed from id only (the primary constructor property), so it is always bucket {b}.')
    v('hash.bodyEq', 'b có cùng id với a nên equals trả true: set coi b đã có.', 'b has the same id as a, so equals returns true: the set treats b as already present.')
    v('hash.bodyNote', 'Set chỉ giữ một phần tử; note của a không giúp phân biệt hai object.', 'The set keeps a single element; a\'s note does not tell the two objects apart.')
    v('hash.plainNote', 'Class thường: equals/hashCode mặc định theo từng object, nên a và b nằm ở hai chỗ (vị trí trong bảng là minh họa).', 'A plain class: default equals/hashCode are per object, so a and b sit in two places (the positions are illustrative).')
    # K9
    v('seq.colHour', 'Giờ hẹn', 'Hour'); v('seq.colFilter', 'filter: giờ < 12', 'filter: hour < 12'); v('seq.colMap', 'map', 'map step')
    v('seq.colTake', 'take(2)', 'take(2) step'); v('seq.colEach', 'forEach: gửi nhắc', 'forEach: send reminder')
    v('seq.keep', 'giữ', 'kept'); v('seq.drop', 'tính rồi bỏ', 'computed, dropped'); v('seq.unread', 'không đọc', 'never read'); v('seq.sent', 'đã gửi', 'sent'); v('seq.notRun', 'chưa chạy', 'not run')
    v('seq.legend', '#n là lần chạy lambda thứ n; ✓/✗ là kết quả filter. Tổng tới bước này: {n} lần.', '#n is the n-th lambda run; ✓/✗ is the filter result. Total so far: {n} runs.')
    v('seq.cap.list', 'List: chạy hết cột filter cho cả 8 hàng, rồi mới tới cột map. Đọc theo CỘT.', 'List: the whole filter column runs for all 8 rows before the map column starts. Read it by COLUMN.')
    v('seq.cap.sequence', 'Sequence: mỗi hàng chạy qua filter rồi map ngay, rồi mới tới hàng sau; đủ 2 thì dừng. Đọc theo HÀNG.', 'Sequence: each row goes through filter and then map at once before the next row; it stops at 2. Read it by ROW.')
    v('seq.cap.noTerminal', 'Sequence không có thao tác cuối: bảng trống cho tới khi thêm forEach.', 'A Sequence with no terminal operation: the grid stays empty until forEach is added.')
    # K10
    v('var.cap', 'Doctor là Staff. Mỗi hàng là một cách khai báo tham số kiểu; mỗi cột là một chiều gán. Ô viền là phép gán đang xét ở bước này.', 'A Doctor is a Staff. Each row is a way of declaring the type parameter; each column is an assignment direction. The outlined cell is the assignment checked at this step.')
    v('var.colType', 'Khai báo', 'Declaration'); v('var.colUp', 'C<Doctor> gán cho biến C<Staff>', 'C<Doctor> into a C<Staff> variable'); v('var.colDown', 'C<Staff> gán cho biến C<Doctor>', 'C<Staff> into a C<Doctor> variable'); v('var.colWhy', 'Vì sao', 'Why')
    v('var.ok', 'được', 'allowed'); v('var.err', 'lỗi biên dịch', 'compile error')
    v('var.why.out', 'chỉ trả T ra (hiệp biến)', 'only gives T out (covariant)'); v('var.why.inv', 'vừa nhận vừa trả T (bất biến)', 'takes and gives T (invariant)'); v('var.why.in', 'chỉ nhận T vào (nghịch biến)', 'only takes T in (contravariant)')
    v('var.copyNote', 'Cách sửa không đổi ô nào của bảng: toMutableList<Staff>() tạo một list MỚI kiểu MutableList<Staff>, không gán chính list bác sĩ.', 'The fix changes no cell of the table: toMutableList<Staff>() creates a NEW MutableList<Staff> instead of assigning the doctors list itself.')
    # K12
    v('scope.cap', 'Mỗi hộp là một receiver ngầm (this) hay một tham số đang có trong lambda. Một tên không có tiền tố được tìm từ hộp trong ra hộp ngoài. Hộp viền là nơi tên được hiểu ở bước này.', 'Each box is an implicit receiver (this) or a parameter available in the lambda. An unprefixed name is looked up from the inner box outwards. The outlined box is where the name resolves at this step.')
    v('scope.legend', 'Viền đỏ: tên được hiểu theo hộp mà người viết không định.', 'Red outline: the name resolved against a box the author did not intend.')
    S = {
        'nestedApply': [('outer', 'apply ngoài: this = Booking', 'outer apply: this = the Booking'), ('outerFix', 'apply ngoài: this = Booking', 'outer apply: this = the Booking (unchanged)'),
                        ('outerMembers', 'có: title, patient', 'has: title, patient'), ('inner', 'apply trong: this = Patient', 'inner apply: this = the Patient'),
                        ('innerFix', 'also { p -> }: p = Patient (tham số có tên)', 'also { p -> }: p = the Patient (named parameter)'), ('innerMembers', 'có: name, salutation (không có title)', 'has: name, salutation (no title)'),
                        ('name', 'title = …', 'title = … assignment'), ('res1', 'Booking.title (apply ngoài): đúng ý', 'Booking.title (outer apply): as intended'),
                        ('res2', 'Patient không có title, nên hiểu thành Booking.title: ghi đè', 'Patient has no title, so it becomes Booking.title: overwritten'), ('res3', 'p.salutation; p.title sẽ là lỗi biên dịch', 'p.salutation; p.title would be a compile error')],
        'letElvis': [('outer', 'cả biểu thức: (…) ?: logout()', 'the whole expression: (…) ?: logout()'), ('outerFix', 'if (token == null) logout() else …', 'if (token == null) logout() else … form'),
                     ('outerMembers', 'vế phải chạy khi vế trái là null', 'the right side runs when the left side is null'), ('inner', 'token?.let { it -> api.refresh(it) }', 'token?.let { it -> api.refresh(it) } call'),
                     ('innerFix', 'api.refresh(token) ?: showRetry()', 'api.refresh(token) ?: showRetry() call'), ('innerMembers', 'it = token; let trả kết quả lambda', 'it = the token; let returns the lambda result'),
                     ('name', 'kết quả của vế trái', 'the left side\'s value'), ('res1', 'let chạy, it = token', 'let runs, it = the token'),
                     ('res2', 'refresh trả null nên cả vế trái là null: logout() chạy', 'refresh returns null, so the whole left side is null: logout() runs'), ('res3', 'hai trường hợp tách bằng if: chỉ thử lại', 'the two cases split with if: just retry')],
        'dslMarker': [('outer', 'bookingForm { }: this = Form', 'bookingForm { }: this = the Form'), ('outerFix', '@FormDsl Form: chỉ gọi được bằng this@bookingForm', '@FormDsl Form: callable only via this@bookingForm'),
                      ('outerMembers', 'có: section()', 'has: section()'), ('inner', 'section { }: this = Section', 'section { }: this = the Section'),
                      ('innerFix', '@FormDsl Section: receiver gần nhất', '@FormDsl Section: the nearest receiver'), ('innerMembers', 'có: field() (không có section())', 'has: field() (no section())'),
                      ('name', 'tên field(…) / section(…)', 'the name field(…) / section(…)'), ('res1', 'field("name") → Section.field: đúng ý', 'field("name") → Section.field: as intended'),
                      ('res2', 'section("Ghi chú") → Form.section: mục nằm sai chỗ', 'section("Notes") → Form.section: misplaced section'), ('res3', 'section("Ghi chú") thành lỗi biên dịch', 'section("Notes") becomes a compile error')],
    }
    for case, items in S.items():
        for k, vi, en in items:
            v('scope.%s.%s' % (case, k), vi, en)
    # K0
    v('map.cap', 'Mỗi hàng là một triệu chứng và chương giải thích nó. Hàng viền là triệu chứng đang chọn; cột "Lộ ra lúc" và "Chương" của nó hiện dần theo bước.', 'Each row is a symptom and the chapter that explains it. The outlined row is the selected symptom; its "Shows up" and "Chapter" cells appear step by step.')
    v('map.colSym', 'Triệu chứng', 'Symptom'); v('map.colPhase', 'Lộ ra lúc', 'Shows up'); v('map.colCh', 'Chương', 'Chapter')
