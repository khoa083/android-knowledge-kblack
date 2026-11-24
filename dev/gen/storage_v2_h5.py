# Lưu dữ liệu · H5: quan hệ và giao dịch (Phần 1)
# Nguồn: developer.android.com Define relationships (tổng quan, one-to-many, many-to-many), Transaction reference (đọc 2026-11-24).
# Trần: 8 mục, mục cơ chế ≤ 4 khối.

SEC_ORDER = {'h5': ['hook', 'relation', 'nplus1', 'transaction', 'bugs', 'ex', 'recall', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.rel', 'Lưu dữ liệu · bác sĩ kèm lịch hẹn: N+1, @Relation, multimap', 'Saving data · doctors with appointments: N+1, @Relation, multimap')
    m = lambda k, vi, en=None: a('m.rel.' + k, vi, en)
    m('title', 'Đọc bác sĩ kèm lịch hẹn khi đồng bộ đang ghi', 'Reading doctors with their appointments while sync is writing')
    m('overview', 'Màn Tổng quan hiện ba bác sĩ A, B, C kèm lịch hẹn của từng người. Ba cách đọc: một vòng lặp gọi DAO cho từng bác sĩ, một lớp @Relation có @Transaction, và một câu JOIN trả về Map. Giữa lúc đọc, đồng bộ nền chuyển lịch #7 từ bác sĩ B sang bác sĩ C.',
      'The Overview screen shows three doctors A, B and C with each one\'s appointments. Three ways to read: a loop calling the DAO per doctor, a @Relation class with @Transaction, and a JOIN query returning a Map. Mid-read, background sync moves appointment #7 from doctor B to doctor C.')
    m('wrapup', 'Đọc dữ liệu liên quan bằng nhiều truy vấn rời có hai cái giá: số truy vấn tăng theo số dòng cha (1 + N), và một lần ghi chen giữa làm kết quả ghép lệch nhau, ở đây lịch #7 xuất hiện hai lần. @Relation gom còn hai truy vấn, và @Transaction giữ hai truy vấn đó nhìn cùng một trạng thái. Một câu JOIN trả multimap chỉ cần một truy vấn, và tài liệu khuyên dùng nó khi không có lý do dùng lớp trung gian.',
      'Reading related data through separate queries has two costs: the number of queries grows with the parent rows (1 + N), and a write slipping in between makes the assembled result disagree with itself, here appointment #7 shows up twice. @Relation cuts it to two queries, and @Transaction keeps both looking at the same state. A JOIN returning a multimap needs one query, and the docs recommend it when there is no reason for an intermediate class.')
    m('simp.1', 'Ba bác sĩ, bốn lịch và thời điểm đồng bộ chen vào là của site, để thấy rõ lệch nhau. Trong app thật, chen giữa hiếm hơn nhưng có xảy ra, nhất là khi đồng bộ chạy nền thường xuyên.', 'Three doctors, four appointments and the moment sync slips in are the site\'s, to make the inconsistency visible. In real apps it is rarer but it does happen, especially with frequent background sync.')
    m('simp.2', 'Cách Room chạy @Relation và @Transaction theo trang Relationships và trang tham chiếu Transaction đọc ngày 2026-11-24; site không chạy SQLite thật.', 'How Room runs @Relation and @Transaction follows the Relationships page and the Transaction reference as read on 2026-11-24; the site does not run a real SQLite.')
    m('ctl.hint', 'Đổi cách đọc rồi đi lại; so số truy vấn và số lịch bị đếm trùng ở bước cuối.', 'Switch the read and walk again; compare the query count and the duplicated appointments at the last step.')
    m('ctl.case', 'Cách đọc', 'Read')
    for k, vi, en in [('loop', 'vòng lặp từng bác sĩ (1 + N)', 'a loop per doctor (1 + N)'), ('relation', '@Relation + @Transaction', '@Relation with @Transaction'), ('multimap', 'JOIN trả về Map', 'a JOIN returning a Map')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Bảng doctor, bảng appointment, đồng bộ nền, kết quả ghép', 'doctor table, appointment table, background sync, assembled result')
    m('diagramDesc', 'Đọc đi từ bảng doctor sang bảng appointment rồi ghép thành kết quả; đồng bộ nền ghi vào bảng appointment', 'Reading goes from the doctor table to the appointment table, then into the assembled result; background sync writes into the appointment table')
    for k, vi, en in [('doctors', 'Bảng doctor', 'doctor table'), ('appts', 'Bảng appointment', 'appointment table'), ('result', 'Kết quả ghép', 'Assembled result'), ('sync', 'Đồng bộ nền', 'Background sync')]:
        m('n.' + k, vi, en)
    m('met.q', 'Số truy vấn đã chạy', 'Queries run'); m('met.dup', 'Lịch bị đếm trùng', 'Appointments counted twice')
    a('cap.rel', 'Đọc đi từ bảng doctor sang bảng appointment rồi ghép thành kết quả; đồng bộ nền (bên dưới) ghi vào bảng appointment. Khối viền đỏ là chỗ kết quả lệch.', 'Reading goes from doctor to appointment, then into the result; background sync (below) writes into appointment. A red outline marks where the result disagrees with itself.')
    S = [
        ('loop', 's1', 'Đọc danh sách bác sĩ: truy vấn 1', 'Read the doctors: query 1',
         'dao.doctors() trả về A, B, C. Chưa có lịch nào; mỗi bác sĩ cần thêm một truy vấn.', 'dao.doctors() returns A, B and C. No appointments yet; each doctor needs one more query.'),
        ('loop', 's2', 'Đọc lịch của A rồi của B: đã 3 truy vấn', 'Read A\'s then B\'s appointments: 3 queries so far',
         'A có #5; B có #6 và #7. Mỗi lời gọi là một truy vấn riêng, không có giao dịch bao ngoài.', 'A has #5; B has #6 and #7. Each call is a separate query, with no surrounding transaction.'),
        ('loop', 's3', 'Đồng bộ chen vào: #7 chuyển từ B sang C', 'Sync slips in: #7 moves from B to C',
         'Giữa hai truy vấn, đồng bộ nền cập nhật lịch #7 sang bác sĩ C. Không có gì ngăn nó: vòng lặp không giữ giao dịch.', 'Between two queries, background sync updates appointment #7 to doctor C. Nothing stops it: the loop holds no transaction.'),
        ('loop', 's4', 'Đọc lịch của C: #7 xuất hiện hai lần', 'Read C\'s appointments: #7 appears twice',
         'C có #7 và #8. Kết quả ghép có #7 ở cả B lẫn C: màn hình đếm 5 lịch trong khi database có 4. Tổng 4 truy vấn = 1 + N với N = 3.', 'C has #7 and #8. The assembled result has #7 under both B and C: the screen counts 5 appointments while the database has 4. Total 4 queries = 1 + N with N = 3.'),
        ('relation', 's1', 'Mở giao dịch, đọc bảng doctor: truy vấn 1', 'Open a transaction, read doctor: query 1',
         'Hàm DAO có @Transaction. Room bắt đầu giao dịch rồi chạy SELECT * FROM doctor.', 'The DAO function has @Transaction. Room begins a transaction, then runs SELECT * FROM doctor.'),
        ('relation', 's2', 'Room tự đọc lịch của cả ba: truy vấn 2', 'Room reads all three doctors\' appointments: query 2',
         'Với trường @Relation, Room chạy thêm một truy vấn lấy lịch của mọi bác sĩ vừa đọc, rồi ghép theo doctorId. Hai truy vấn, dù có 3 hay 300 bác sĩ.', 'For the @Relation field, Room runs one more query fetching the appointments of every doctor just read, then groups them by doctorId. Two queries, whether there are 3 doctors or 300.'),
        ('relation', 's3', 'Đồng bộ ghi #7: không lọt vào giữa hai truy vấn', 'Sync writes #7: it does not land between the two queries',
         'Hai truy vấn nằm trong cùng một giao dịch nên nhìn cùng một trạng thái database. Lần ghi của đồng bộ không chen được vào giữa chúng; lần đọc sau sẽ thấy #7 ở C.', 'Both queries are in one transaction, so they see the same database state. The sync write cannot slip in between them; the next read will see #7 under C.'),
        ('relation', 's4', 'Kết quả nhất quán: mỗi lịch đúng một lần', 'A consistent result: each appointment exactly once',
         'A: #5; B: #6, #7; C: #8. Đây là trạng thái trước lần ghi, đủ và không trùng.', 'A: #5; B: #6, #7; C: #8. This is the state before the write, complete and without duplicates.'),
        ('multimap', 's1', 'Một câu JOIN: truy vấn 1 trả 4 dòng (bác sĩ, lịch)', 'One JOIN: query 1 returns 4 (doctor, appointment) rows',
         'SQLite ghép hai bảng trong một câu và trả về mỗi lịch một dòng kèm bác sĩ của nó.', 'SQLite joins both tables in one statement and returns one row per appointment with its doctor.'),
        ('multimap', 's2', 'Room gom các dòng thành Map theo bác sĩ', 'Room groups the rows into a Map by doctor',
         'Kiểu trả về Map<Doctor, List<Appointment>> cho Room biết cách gom. Không có truy vấn thêm.', 'The return type Map<Doctor, List<Appointment>> tells Room how to group. No extra query.'),
        ('multimap', 's3', 'Đồng bộ ghi #7: câu đọc đã xong', 'Sync writes #7: the read has already finished',
         'Một câu SQL đơn lẻ tự nó nhất quán: nó thấy trạng thái trước hoặc sau lần ghi, không bao giờ một nửa.', 'A single SQL statement is consistent on its own: it sees the state before or after the write, never half of it.'),
        ('multimap', 's4', 'Kết quả nhất quán với một truy vấn', 'A consistent result with one query',
         'Cùng kết quả như @Relation, ít hơn một truy vấn. Lưu ý: JOIN thường chỉ trả bác sĩ có ít nhất một lịch; bác sĩ chưa có lịch nào sẽ không xuất hiện.', 'The same result as @Relation, one query fewer. Note: a plain JOIN only returns doctors with at least one appointment; a doctor with none will not appear.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Đi hết bốn bước của mỗi cách; để ý bảng appointment đổi ở bước 3.', 'Walk all four steps of each read; watch the appointment table change at step 3.'),
        ('loop.s2', 'Mỗi bác sĩ thêm một truy vấn: 100 bác sĩ là 101 truy vấn. Đây là kiểu "N+1".', 'Each doctor adds one query: 100 doctors means 101 queries. This is the "N+1" pattern.'),
        ('loop.s3', 'Không có giao dịch thì mỗi truy vấn thấy trạng thái tại lúc nó chạy; các lần ghi xen vào giữa được.', 'Without a transaction, each query sees the state at the moment it runs; writes can slip in between.'),
        ('loop.s4', 'Kết quả ghép từ các truy vấn ở các thời điểm khác nhau nên tự mâu thuẫn: một lịch ở hai bác sĩ.', 'The result is stitched from queries at different moments, so it contradicts itself: one appointment under two doctors.'),
        ('relation.s2', 'Trang One-to-many: hàm trả về lớp có @Relation cần Room chạy hai truy vấn. [[src:ax-room-relations]]', 'The One-to-many page: a function returning a class with @Relation needs Room to run two queries. [[src:ax-room-relations]]'),
        ('relation.s3', 'Vì vậy trang dặn thêm @Transaction để cả thao tác chạy nguyên tử; trang tham chiếu Transaction giải thích rằng các trường @Relation được truy vấn bằng các câu riêng. [[src:ax-room-relations]] [[src:ax-room-transaction]]', 'So the page says to add @Transaction so the whole operation runs atomically; the Transaction reference explains that @Relation fields are fetched in separate queries. [[src:ax-room-relations]] [[src:ax-room-transaction]]'),
        ('relation.s4', 'Thiếu @Transaction thì vẫn là hai truy vấn, nhưng lần ghi có thể chen giữa như ở vòng lặp. [[src:ax-room-transaction]]', 'Without @Transaction it is still two queries, but a write can slip in between, as in the loop. [[src:ax-room-transaction]]'),
        ('multimap.s2', 'Trang Relationships: nếu không có lý do cụ thể để dùng lớp trung gian, nên dùng kiểu trả về multimap. [[src:ax-room-relations]]', 'The Relationships page: if you have no specific reason to use intermediate classes, use the multimap return type. [[src:ax-room-relations]]'),
        ('multimap.s3', 'Cùng trang so sánh: multimap để câu SQL làm nhiều việc hơn, lớp trung gian để mã app làm nhiều việc hơn. [[src:ax-room-relations]]', 'The same page compares: the multimap makes the SQL do more work, the intermediate class makes the app code do more. [[src:ax-room-relations]]'),
        ('multimap.s4', 'Cần cả bác sĩ chưa có lịch thì dùng LEFT JOIN và kiểm kết quả, hoặc quay về @Relation, vốn luôn trả đủ mọi bác sĩ.', 'If you need doctors with no appointments too, use a LEFT JOIN and check the result, or go back to @Relation, which always returns every doctor.')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.rl', 'Bảng và kết quả', 'Tables and result')
    z('rl.cap', 'Trái: bảng appointment trong database (dòng #7 đổi ở bước 3). Phải: kết quả màn hình đã ghép được. Dưới: số truy vấn đã chạy.', 'Left: the appointment table in the database (row #7 changes at step 3). Right: what the screen has assembled. Below: queries run so far.')
    z('rl.t1', 'Bảng appointment', 'appointment table'); z('rl.t2', 'Kết quả ghép', 'Assembled result')
    z('rl.moved', '{from} → {to}', '{from} to {to}')
    z('rl.doctor', 'Bác sĩ {d}', 'Doctor {d}')
    z('rl.dup', '(trùng)', '(duplicate)'); z('rl.notyet', 'chưa đọc', 'not read yet')
    z('rl.col.doctor', 'Bác sĩ', 'Doctor'); z('rl.col.appts', 'Lịch hẹn', 'Appointments')
    z('rl.q', 'Đã chạy {n} truy vấn.', '{n} queries run.')
    z('rl.formula.loop', 'Vòng lặp: 1 + N, với N là số bác sĩ.', 'Loop: 1 + N, where N is the number of doctors.')
    z('rl.formula.relation', '@Relation: luôn 2, bất kể bao nhiêu bác sĩ.', '@Relation: always 2, however many doctors.')
    z('rl.formula.multimap', 'Multimap: 1 câu JOIN.', 'Multimap: 1 JOIN statement.')
    z('rl.legend', 'Chip gạch đỏ: lịch đã có ở bác sĩ khác trong cùng kết quả, dấu hiệu kết quả ghép từ hai thời điểm.', 'Red chip: an appointment already listed under another doctor in the same result, a sign the result was stitched from two moments.')

    C = 'h5'
    a(C + '.title', 'Quan hệ và giao dịch', 'Relations and transactions')
    a(C + '.essence', 'Room không cho entity tham chiếu đối tượng của nhau; dữ liệu liên quan được đọc bằng lớp trung gian (@Embedded, @Relation) hoặc một câu truy vấn trả multimap.\n@Relation khiến Room chạy hai truy vấn; thêm @Transaction để cả hai nhìn cùng một trạng thái database.\nVòng lặp gọi DAO cho từng dòng cha tốn 1 + N truy vấn và có thể ghép ra kết quả tự mâu thuẫn khi có lần ghi chen giữa.',
      'Room does not let entities hold object references to each other; related data is read through an intermediate class (@Embedded, @Relation) or a query returning a multimap.\n@Relation makes Room run two queries; add @Transaction so both see the same database state.\nA loop calling the DAO per parent row costs 1 + N queries and can assemble a self-contradicting result when a write slips in between.')
    a(C + '.goal.g1', 'Đã thấy lần ghi chen vào', 'Saw the write slip in')
    a(C + '.goal.g2', 'Đã thấy kết quả ghép cuối cùng', 'Saw the final assembled result')
    a(C + '.sim.storage.rel', 'N+1, @Relation và multimap', 'N+1, @Relation and multimap')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'predict', 'Màn Tổng quan đọc danh sách bác sĩ, rồi với từng bác sĩ gọi dao.appointmentsOf(id). Database có 4 lịch. Có lúc màn hình hiện 5 lịch. Chuyện gì đã xảy ra?',
      'The Overview screen reads the doctors, then calls dao.appointmentsOf(id) for each one. The database holds 4 appointments. Sometimes the screen shows 5. What happened?')
    B(C, S_, 1, 'ans', 'Một lần ghi đã chen giữa các truy vấn: một lịch chuyển từ bác sĩ đã đọc sang bác sĩ chưa đọc, nên bị đếm ở cả hai. Các truy vấn rời không nằm trong giao dịch, mỗi câu thấy database ở một thời điểm khác. Mô phỏng ngay dưới cho thấy đúng lúc đó.',
      'A write slipped between the queries: an appointment moved from a doctor already read to one not yet read, so it was counted under both. Separate queries outside a transaction each see the database at a different moment. The simulation just below shows that exact moment.')

    S_ = 'relation'
    a(C + '.sec.%s.title' % S_, '@Embedded, @Relation và multimap', '@Embedded, @Relation and multimaps')
    a(C + '.sec.%s.badge' % S_, 'version')
    B(C, S_, 1, 'p', 'Room cấm entity giữ tham chiếu tới đối tượng của entity khác. Muốn đọc một bác sĩ kèm các lịch của họ có hai cách. Một là lớp trung gian: @Embedded chứa dòng cha, @Relation chỉ cột khóa của cha và cột tham chiếu ở bảng con. Hai là truy vấn trả về multimap như Map<Doctor, List<Appointment>>. Trang Relationships khuyên dùng multimap nếu không có lý do cụ thể để dùng lớp trung gian. [[src:ax-room-relations]]',
      'Room forbids entities from holding references to other entities\' objects. To read a doctor with their appointments there are two ways. One is an intermediate class: @Embedded holds the parent row, @Relation names the parent\'s key column and the referencing column in the child table. The other is a query returning a multimap such as Map<Doctor, List<Appointment>>. The Relationships page recommends the multimap unless you have a specific reason for an intermediate class. [[src:ax-room-relations]]')
    B(C, S_, 2, 'kt', 'data class DoctorWithAppointments(\n    @Embedded val doctor: Doctor,\n    @Relation(parentColumns = ["id"], entityColumns = ["doctorId"])\n    val appointments: List<Appointment>,\n)\n\n@Transaction\n@Query("SELECT * FROM doctor")\nsuspend fun doctorsWithAppointments(): List<DoctorWithAppointments>',
      'data class DoctorWithAppointments(\n    @Embedded val doctor: Doctor,\n    @Relation(parentColumns = ["id"], entityColumns = ["doctorId"])\n    val appointments: List<Appointment>,\n)\n\n@Transaction\n@Query("SELECT * FROM doctor")\nsuspend fun doctorsWithAppointments(): List<DoctorWithAppointments>')
    B(C, S_, 3, 'p', 'Quan hệ nhiều–nhiều (một bác sĩ làm ở nhiều phòng khám, một phòng khám có nhiều bác sĩ) cần một bảng nối chứa khóa của cả hai bên, rồi truyền nó vào @Relation qua associateBy = Junction(BảngNối::class). Khi @Relation không diễn tả được, trang gợi ý viết JOIN bằng SQL. [[src:ax-room-relations]]',
      'A many-to-many relation (a doctor works at several clinics, a clinic has several doctors) needs a junction table holding both sides\' keys, passed to @Relation through associateBy = Junction(JunctionTable::class). When @Relation cannot express it, the page suggests writing a JOIN in SQL. [[src:ax-room-relations]]')
    B(C, S_, 4, 'note', 'Cú pháp theo hướng dẫn Room 3.0 đọc ngày 2026-11-24: @Relation(parentColumns = [...], entityColumns = [...]) nhận mảng để hỗ trợ khóa nhiều cột. Room 2.x viết @Relation(parentColumn = "id", entityColumn = "doctorId") với một cột.',
      'Syntax per the Room 3.0 guide read on 2026-11-24: @Relation(parentColumns = [...], entityColumns = [...]) takes arrays to support multi-column keys. Room 2.x writes @Relation(parentColumn = "id", entityColumn = "doctorId") with a single column.')
    B(C, S_, 4, 'kind', 'android')

    S_ = 'nplus1'
    a(C + '.sec.%s.title' % S_, 'Vòng lặp N+1 và vì sao nó lệch', 'The N+1 loop, and why it drifts')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Vòng lặp "đọc cha, rồi với mỗi cha đọc con" trông tự nhiên nhưng tốn 1 + N truy vấn: 3 bác sĩ là 4 truy vấn, 200 bác sĩ là 201. Mỗi truy vấn có chi phí cố định (chuẩn bị câu lệnh, chuyển luồng, tạo đối tượng), nên số truy vấn quan trọng hơn kích thước từng câu. @Relation luôn dùng hai truy vấn; một câu JOIN dùng một.',
      'The "read the parents, then for each parent read its children" loop looks natural but costs 1 + N queries: 3 doctors are 4 queries, 200 doctors are 201. Each query has a fixed cost (preparing the statement, switching threads, building objects), so the number of queries matters more than the size of each one. @Relation always uses two queries; a JOIN uses one.')
    B(C, S_, 2, 'p', 'Vấn đề thứ hai khó thấy hơn: các truy vấn rời không nằm trong giao dịch, nên mỗi câu thấy database tại lúc nó chạy. Nếu đồng bộ nền ghi xen giữa, kết quả ghép lại là một hỗn hợp của hai thời điểm và có thể tự mâu thuẫn: một lịch nằm ở hai bác sĩ, hay biến mất khỏi cả hai. [[src:ax-room-transaction]]',
      'The second problem is harder to see: separate queries are not in a transaction, so each one sees the database as of the moment it runs. If background sync writes in between, the assembled result mixes two moments and can contradict itself: an appointment under two doctors, or missing from both. [[src:ax-room-transaction]]')
    B(C, S_, 3, 'note', 'Lệch kiểu này hiếm và không lặp lại được theo ý muốn, nên thường bị coi là "lỗi ma". Khi một màn hình ghép dữ liệu từ nhiều truy vấn, hãy hỏi: nếu có lần ghi chen giữa thì sao?',
      'This kind of drift is rare and hard to reproduce on demand, so it often gets filed as a "ghost bug". When a screen assembles data from several queries, ask: what if a write lands in between?')
    B(C, S_, 3, 'kind', 'pitfall')

    S_ = 'transaction'
    a(C + '.sec.%s.title' % S_, '@Transaction làm gì', 'What @Transaction does')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Theo trang tham chiếu, @Transaction đánh dấu một hàm DAO là giao dịch. Trên một @Query SELECT, nó có hai tác dụng: kết quả lớn có cái nhìn nhất quán, và các trường @Relation (được truy vấn bằng những câu riêng) nhất quán với dòng cha. @Insert, @Update, @Delete vốn đã chạy trong giao dịch, nên thêm @Transaction cho chúng không có tác dụng. [[src:ax-room-transaction]]',
      'Per the reference, @Transaction marks a DAO method as a transaction. On a SELECT @Query it does two things: a large result gets a consistent view, and @Relation fields (fetched by separate statements) stay consistent with their parent rows. @Insert, @Update and @Delete already run in a transaction, so adding @Transaction to them has no effect. [[src:ax-room-transaction]]')
    B(C, S_, 2, 'kt', '@Dao abstract class BookingDao {\n    @Insert abstract suspend fun insert(a: Appointment): Long\n    @Query("UPDATE slot SET free = 0 WHERE id = :slotId") abstract suspend fun takeSlot(slotId: Long): Int\n\n    @Transaction   // cả hàm là một giao dịch: hoặc cả hai xong, hoặc không có gì\n    open suspend fun book(a: Appointment, slotId: Long) {\n        check(takeSlot(slotId) == 1) { "slot already taken" }\n        insert(a)\n    }\n}',
      '@Dao abstract class BookingDao {\n    @Insert abstract suspend fun insert(a: Appointment): Long\n    @Query("UPDATE slot SET free = 0 WHERE id = :slotId") abstract suspend fun takeSlot(slotId: Long): Int\n\n    @Transaction   // the whole method is one transaction: both succeed or nothing does\n    open suspend fun book(a: Appointment, slotId: Long) {\n        check(takeSlot(slotId) == 1) { "slot already taken" }\n        insert(a)\n    }\n}')
    B(C, S_, 3, 'p', 'Trên một hàm không trừu tượng gọi nhiều hàm DAO, @Transaction chạy cả hàm trong một giao dịch; giao dịch thành công trừ khi có ngoại lệ ném ra. Ở ví dụ, nếu insert lỗi thì giờ trống được trả lại như cũ. Room chạy tối đa một giao dịch mỗi lúc, các giao dịch khác xếp hàng theo thứ tự đến trước, nên giữ giao dịch ngắn: đừng gọi mạng bên trong. [[src:ax-room-transaction]]',
      'On a non-abstract method calling several DAO methods, @Transaction runs the whole method in one transaction, which succeeds unless an exception is thrown. In the example, if the insert fails, the slot is given back. Room performs at most one transaction at a time and queues the rest first come, first served, so keep transactions short: never call the network inside one. [[src:ax-room-transaction]]')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Màn Tổng quan mở chậm dần theo số bác sĩ; với 300 bác sĩ mất hơn một giây.', 'The Overview screen gets slower as doctors are added; with 300 doctors it takes over a second.')
    B(C, S_, 1, 'cause', 'Vòng lặp gọi appointmentsOf cho từng bác sĩ: 301 truy vấn, mỗi câu một lần chuyển luồng và chuẩn bị câu lệnh.', 'A loop calls appointmentsOf per doctor: 301 queries, each with its own thread hop and statement preparation.')
    B(C, S_, 1, 'fix', 'Một hàm DAO trả về Map<Doctor, List<Appointment>> bằng JOIN, hoặc List<DoctorWithAppointments> với @Relation và @Transaction.', 'One DAO function returning Map<Doctor, List<Appointment>> via a JOIN, or List<DoctorWithAppointments> with @Relation and @Transaction.')
    B(C, S_, 2, 'bug', 'Hiếm khi, hai người đặt cùng một giờ trống và cả hai đều thành công.', 'Rarely, two bookings take the same free slot and both succeed.')
    B(C, S_, 2, 'cause', 'Repository gọi riêng "kiểm giờ còn trống" rồi "chèn lịch hẹn" thành hai lời gọi DAO rời. Một lần đặt khác chen vào giữa hai bước.', 'The repository calls "check the slot is free" and "insert the appointment" as two separate DAO calls. Another booking lands between the two steps.')
    B(C, S_, 2, 'fix', 'Gộp hai bước vào một hàm DAO có @Transaction, và để bước kiểm là một câu UPDATE có điều kiện trả về số dòng đổi, như ví dụ book ở trên.', 'Merge both steps into one @Transaction DAO method, with the check as a conditional UPDATE returning the number of rows changed, like the book example above.')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Hẹn Khám có bảng visit (lượt khám) và prescription (đơn thuốc, có cột visitId). Màn Lịch sử cần mỗi lượt khám kèm danh sách đơn thuốc, kể cả lượt khám chưa có đơn nào. Viết hàm DAO theo cách bạn chọn, nói nó chạy bao nhiêu truy vấn, và vì sao nó không thể cho ra một đơn thuốc nằm ở hai lượt khám.',
      'ClinicBook has a visit table and a prescription table (with a visitId column). The History screen needs every visit with its prescriptions, including visits with none. Write the DAO function your way, say how many queries it runs, and why it cannot produce one prescription under two visits.')
    B(C, S_, 1, 'hint', 'Yêu cầu "kể cả lượt khám chưa có đơn" loại một câu JOIN thường. @Relation luôn trả đủ mọi dòng cha.', 'The requirement "including visits with none" rules out a plain JOIN. @Relation always returns every parent row.')
    B(C, S_, 1, 'sol', 'Dùng lớp VisitWithPrescriptions với @Embedded visit và @Relation tới prescription theo visitId; hàm DAO có @Transaction. Room chạy hai truy vấn bất kể số lượt khám. Vì cả hai nằm trong một giao dịch, chúng nhìn cùng một trạng thái, nên một đơn thuốc không thể thuộc hai lượt khám trong cùng kết quả. Lượt khám chưa có đơn nhận danh sách rỗng.',
      'Use a VisitWithPrescriptions class with an @Embedded visit and an @Relation to prescription by visitId; the DAO function has @Transaction. Room runs two queries however many visits there are. Since both are in one transaction they see the same state, so one prescription cannot belong to two visits in the same result. Visits with no prescriptions get an empty list.')
    B(C, S_, 1, 'solkt', 'data class VisitWithPrescriptions(\n    @Embedded val visit: Visit,\n    @Relation(parentColumns = ["id"], entityColumns = ["visitId"])\n    val prescriptions: List<Prescription>,\n)\n\n@Transaction\n@Query("SELECT * FROM visit ORDER BY date DESC")\nfun history(): Flow<List<VisitWithPrescriptions>>')

    S_ = 'recall'
    a(C + '.sec.%s.title' % S_, 'Tự trả lời', 'Answer it yourself')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'ask', 'Một hàm trả về lớp có @Relation khiến Room chạy bao nhiêu truy vấn, và vì sao cần @Transaction?', 'How many queries does a function returning a class with @Relation make Room run, and why is @Transaction needed?')
    B(C, S_, 1, 'ans', 'Hai truy vấn (cha, rồi con). @Transaction giữ cả hai trong một giao dịch để chúng nhìn cùng một trạng thái.', 'Two (the parents, then the children). @Transaction keeps both in one transaction so they see the same state.')
    B(C, S_, 2, 'ask', 'Thêm @Transaction cho một hàm @Insert có tác dụng gì?', 'What does adding @Transaction to an @Insert function do?')
    B(C, S_, 2, 'ans', 'Không gì: @Insert, @Update, @Delete vốn đã chạy trong giao dịch.', 'Nothing: @Insert, @Update and @Delete already run in a transaction.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', '@Embedded, @Relation, multimap, Junction và lời khuyên dùng multimap theo trang Relationships (tổng quan, one-to-many, many-to-many); hành vi @Transaction theo trang tham chiếu; đọc ngày 2026-11-24, cú pháp theo hướng dẫn Room 3.0. Số liệu 3 bác sĩ, 4 lịch và lúc đồng bộ chen vào là của site. Chương không đo thời gian thật của từng truy vấn, không bàn index, khóa ngoại (@ForeignKey) hay cơ chế khóa bên trong SQLite.',
      '@Embedded, @Relation, multimaps, Junction and the multimap recommendation follow the Relationships pages (overview, one-to-many, many-to-many); @Transaction behaviour follows the reference; read on 2026-11-24, syntax per the Room 3.0 guide. The 3 doctors, 4 appointments and the moment sync slips in are the site\'s. The chapter does not measure real query times, nor cover indices, foreign keys (@ForeignKey) or SQLite\'s internal locking.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Đọc 50 bác sĩ bằng vòng lặp gọi DAO cho từng người tốn bao nhiêu truy vấn?', 'How many queries does reading 50 doctors with a per-doctor DAO loop cost?', '51 (1 + N).', '51 (1 + N).', 'Một câu cho danh sách, thêm một câu cho mỗi bác sĩ.', 'One for the list, plus one per doctor.'),
        ('q2', 'Khi không có lý do cụ thể, trang Relationships khuyên cách nào?', 'Without a specific reason, which approach does the Relationships page recommend?', 'Kiểu trả về multimap.', 'The multimap return type.', 'Lớp trung gian với @Relation là cách còn lại.', 'The intermediate class with @Relation is the other way.'),
        ('q3', 'Quan hệ nhiều–nhiều cần thêm gì?', 'What does a many-to-many relation need?', 'Một bảng nối chứa khóa của hai bên, truyền qua Junction.', 'A junction table with both sides\' keys, passed through Junction.', 'associateBy = Junction(BảngNối::class) trong @Relation.', 'associateBy = Junction(JunctionTable::class) in @Relation.'),
        ('q4', 'Vì sao không gọi mạng bên trong một giao dịch Room?', 'Why not call the network inside a Room transaction?', 'Room chạy tối đa một giao dịch mỗi lúc; giao dịch dài làm các giao dịch khác phải chờ.', 'Room runs at most one transaction at a time; a long one makes the others wait.', 'Các giao dịch khác xếp hàng theo thứ tự đến trước.', 'Other transactions queue first come, first served.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
