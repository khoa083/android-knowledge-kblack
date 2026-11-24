# Mã sạch · J9: nguyên lý thành phần (Phần 3: thiết kế)
# Nguồn: Martin, Clean Architecture ch.13 (cohesion: REP "đơn vị dùng lại là đơn vị phát hành", CCP là SRP cho thành phần, CRP đừng buộc người dùng
# phụ thuộc thứ không cần), ch.14 (coupling: ADP không vòng; SDP phụ thuộc theo hướng ổn định; ổn định là "khó dời đi", không liên quan tần suất đổi;
# Fan-in, Fan-out, I = Fan-out / (Fan-in + Fan-out), ví dụ Cc: 3 vào, 1 ra, I = 1/4; mũi tên chỉ lên là vi phạm; sửa vi phạm bằng DIP với thành phần
# chỉ chứa giao diện; SAP thành phần ổn định nên trừu tượng; SDP + SAP là DIP cho thành phần). Đọc 2026-11-24, diễn đạt lại.
# Mô phỏng đếm theo MODULE (số module phụ thuộc), còn Martin đếm theo LỚP; tần suất đổi và số lần build là minh họa.

SEC_ORDER = {'j9': ['hook', 'cohesion', 'stability', 'sdp', 'sap', 'bugs', 'ex', 'honest']}


def add(a):
    def B(ch, sec, n, field, vi, en=None):
        a('%s.sec.%s.b.%02d.%s' % (ch, sec, n, field), vi, vi if en is None else en)

    a('preset.components', 'Mã sạch · tính độ bất ổn định của module', 'Clean code · computing module instability')
    m = lambda k, vi, en=None: a('m.components.' + k, vi, en)
    m('title', 'Một module common cho tất cả, hay chia theo lý do thay đổi', 'One common module for everything, or split by reason to change')
    m('overview', 'App Hẹn Khám có chín module Gradle. Ở cách chia thứ nhất, :core:common gom mọi thứ "ai cũng cần": model, định dạng, tên sự kiện analytics, và nó gọi thẳng :core:analytics. Ở cách thứ hai, phần hay đổi được trả về module dùng nó, :core:model chỉ còn data class và giao diện, :core:analytics cài giao diện đó. Đếm Ca, Ce, tính I = Ce / (Ca + Ce), rồi xem tần suất đổi và số module phải build lại.',
      'ClinicBook has nine Gradle modules. In the first split, :core:common gathers everything "everyone needs": models, formatting, analytics event names, and it calls :core:analytics directly. In the second, the volatile parts go back to the modules that use them, :core:model holds only data classes and interfaces, and :core:analytics implements those interfaces. Count Ca and Ce, compute I = Ce / (Ca + Ce), then look at change frequency and how many modules must rebuild.')
    m('wrapup', ':core:common có 5 module phụ thuộc và chỉ 1 phụ thuộc ra ngoài, nên I = 1/6 ≈ 0,17: rất khó dời đi. Vậy mà nó đổi 12 lần mỗi tháng, và mỗi lần kéo theo 6 module build lại. Nó còn phụ thuộc :core:analytics có I ≈ 0,67, kém ổn định hơn nó: mũi tên chỉ lên, vi phạm SDP. Chia lại theo lý do thay đổi (CCP) và đảo phụ thuộc (DIP): :core:model có I = 0, chỉ chứa giao diện và đổi 1 lần mỗi tháng; không còn mũi tên nào chỉ lên; số module build lại mỗi tháng từ 171 giảm còn 90 với cùng khối lượng thay đổi.',
      ':core:common has 5 dependents and only 1 outgoing dependency, so I = 1/6 ≈ 0.17: very hard to move. Yet it changes 12 times a month, each time rebuilding 6 modules. It also depends on :core:analytics with I ≈ 0.67, less stable than itself: an upward arrow, an SDP violation. Splitting by reason to change (CCP) and inverting the dependency (DIP): :core:model has I = 0, holds only interfaces and changes once a month; no arrow points up any more; module rebuilds per month drop from 171 to 90 for the same amount of change.')
    m('simp.1', 'Martin đếm Fan-in và Fan-out theo số LỚP bên ngoài có phụ thuộc vào (hay bị phụ thuộc bởi) lớp bên trong; mô phỏng đếm theo số MODULE cho dễ đọc. Tần suất đổi và cách tính số lần build lại (module đổi cộng mọi module phụ thuộc bắc cầu vào nó) là minh họa.', 'Martin counts Fan-in and Fan-out as the number of CLASSES outside that depend on (or are depended on by) classes inside; the simulation counts MODULES for readability. Change frequencies and the rebuild count (the changed module plus every module transitively depending on it) are illustrative.')
    m('simp.2', 'Build tăng dần thật của Gradle tinh hơn: thay đổi không chạm ABI có thể không làm module phụ thuộc biên dịch lại. Con số ở đây là cận trên, để so hai cách chia.', 'Gradle\'s real incremental build is finer: a change that does not touch the ABI may not recompile dependents. The numbers here are an upper bound for comparing the two splits.')
    m('ctl.hint', 'Đổi cách chia rồi đi lại; nhìn mũi tên đỏ chỉ lên và hàng có cờ "ổn định mà hay đổi".', 'Switch the split and walk again; watch for red upward arrows and the row flagged "stable yet volatile".')
    m('ctl.case', 'Cách chia module', 'Module split')
    for k, vi, en in [('common', 'một :core:common cho tất cả', 'one :core:common for everything'), ('split', 'chia theo lý do thay đổi', 'split by reason to change')]:
        m('ctl.case.' + k, vi, en)
    m('diagramTitle', 'Module, phụ thuộc, độ bất ổn định, build lại', 'Modules, dependencies, instability, rebuilds')
    m('diagramDesc', 'Đếm phụ thuộc vào và ra, tính I, so với tần suất đổi để thấy chi phí build lại', 'Count incoming and outgoing dependencies, compute I, compare with change frequency to see the rebuild cost')
    for k, vi, en in [('graph', 'Đồ thị module', 'Module graph'), ('count', 'Đếm Ca, Ce', 'Count Ca, Ce'), ('metric', 'Tính I', 'Compute I'), ('cost', 'Build lại mỗi tháng', 'Rebuilds per month')]:
        m('n.' + k, vi, en)
    m('met.violations', 'Mũi tên vi phạm SDP', 'Arrows violating SDP'); m('met.hot', 'Module ổn định mà hay đổi', 'Stable yet volatile modules'); m('met.rebuilds', 'Module build lại mỗi tháng', 'Module rebuilds per month')
    a('cap.components', 'Từ đồ thị module đếm Ca, Ce, tính I, rồi nhân với tần suất đổi ra chi phí build lại. Nút đỏ: nơi phát hiện vi phạm hay chi phí cao.', 'From the module graph count Ca and Ce, compute I, then multiply by change frequency for the rebuild cost. Red node: where a violation or high cost shows up.')
    S = [
        ('common', 's1', 'Vẽ đồ thị, đếm phụ thuộc vào và ra', 'Draw the graph, count incoming and outgoing',
         ':core:common được 5 module phụ thuộc vào (Ca = 5) và phụ thuộc 1 module (Ce = 1). :core:analytics có Ca = 1, Ce = 2.', ':core:common is depended on by 5 modules (Ca = 5) and depends on 1 (Ce = 1). :core:analytics has Ca = 1, Ce = 2.'),
        ('common', 's2', 'Tính I; tìm mũi tên chỉ lên', 'Compute I; look for upward arrows',
         'common: I = 1/(5+1) ≈ 0,17. analytics: I = 2/(1+2) ≈ 0,67. common phụ thuộc analytics, tức module ổn định phụ thuộc module kém ổn định hơn: vi phạm SDP.', 'common: I = 1/(5+1) ≈ 0.17. analytics: I = 2/(1+2) ≈ 0.67. common depends on analytics, a stable module depending on a less stable one: an SDP violation.'),
        ('common', 's3', 'Thêm tần suất đổi: common vừa ổn định vừa hay đổi', 'Add change frequency: common is both stable and volatile',
         'common đổi 12 lần mỗi tháng (thêm tên sự kiện, sửa định dạng…). Mỗi lần, nó và 5 module phụ thuộc phải build lại: 6 module.', 'common changes 12 times a month (new event names, formatting fixes…). Each time, it and its 5 dependents rebuild: 6 modules.'),
        ('common', 's4', 'Cộng cả tháng: 171 lần build module', 'Add up the month: 171 module builds',
         'Riêng common góp 72, analytics góp 42 vì mọi thứ phụ thuộc bắc cầu vào nó qua common. Sửa một dòng tên sự kiện build lại cả app.', 'common alone contributes 72, analytics 42 because everything depends on it transitively through common. Editing one event name rebuilds the whole app.'),
        ('split', 's1', 'Vẽ đồ thị, đếm phụ thuộc vào và ra', 'Draw the graph, count incoming and outgoing',
         ':core:model được 5 module phụ thuộc (Ca = 5) và không phụ thuộc gì (Ce = 0). :core:analytics phụ thuộc model, network, prefs (Ce = 3), chỉ app phụ thuộc nó (Ca = 1).', ':core:model is depended on by 5 modules (Ca = 5) and depends on nothing (Ce = 0). :core:analytics depends on model, network and prefs (Ce = 3); only app depends on it (Ca = 1).'),
        ('split', 's2', 'Tính I; không còn mũi tên chỉ lên', 'Compute I; no upward arrows left',
         'model: I = 0, ổn định tối đa. analytics: I = 3/4 = 0,75, nằm phía trên. Mọi mũi tên đi từ I lớn xuống I nhỏ: đúng SDP.', 'model: I = 0, maximally stable. analytics: I = 3/4 = 0.75, near the top. Every arrow runs from higher I to lower I: SDP holds.'),
        ('split', 's3', 'Thêm tần suất đổi: phần hay đổi ở module không ai phụ thuộc', 'Add change frequency: volatile parts sit where nobody depends',
         'Tên sự kiện và định dạng nằm trong từng feature (8 lần đổi mỗi tháng, chỉ app build lại theo). model chỉ đổi 1 lần mỗi tháng.', 'Event names and formatting live in each feature (8 changes a month, only app rebuilds with them). model changes once a month.'),
        ('split', 's4', 'Cộng cả tháng: 90 lần build module', 'Add up the month: 90 module builds',
         'Cùng khối lượng thay đổi (38 so với 37 lần đổi), nhưng thay đổi rơi vào module ít người phụ thuộc. Không module nào vừa ổn định vừa hay đổi.', 'The same amount of change (38 versus 37 changes), but the changes land in modules few depend on. No module is both stable and volatile.'),
    ]
    for case, k, tv, te, xv, xe in S:
        sid = case + '.' + k
        m('s.%s.title' % sid, tv, te); m('s.%s.explain' % sid, xv, xe); m('ev.' + sid, tv, te)
    for k, vi, en in [
        ('try', 'Mũi tên đi từ module phụ thuộc tới module được phụ thuộc. Module kém ổn định ở trên, ổn định ở dưới.', 'Arrows go from the depending module to the module depended on. Unstable modules on top, stable ones below.'),
        ('common.s2', 'Martin: theo quy ước vẽ module kém ổn định ở trên, mũi tên nào chỉ lên là vi phạm SDP. Module được thiết kế để dễ đổi sẽ trở nên khó đổi khi ai đó treo một phụ thuộc vào nó. [[src:book-carch]]', 'Martin: with unstable modules drawn on top, any arrow pointing up violates SDP. A module designed to be easy to change becomes hard to change once someone hangs a dependency on it. [[src:book-carch]]'),
        ('common.s3', 'Martin: ổn định không liên quan tần suất đổi; nó là lượng công sức để dời một thứ. Module có nhiều module phụ thuộc thì khó đổi. Vấn đề là đặt thứ hay đổi vào chỗ khó đổi. [[src:book-carch]]', 'Martin: stability has nothing to do with how often something changes; it is the effort needed to move it. A module with many dependents is hard to change. The problem is putting volatile things in a hard-to-change place. [[src:book-carch]]'),
        ('common.s4', 'Martin, CCP: gom vào một thành phần những lớp đổi cùng lý do và cùng lúc; tách những lớp đổi vì lý do khác. Đó là SRP nói lại cho thành phần. [[src:book-carch]]', 'Martin, CCP: gather into a component the classes that change for the same reasons at the same times; separate those that change for different reasons. It is SRP restated for components. [[src:book-carch]]'),
        ('split.s1', 'Martin sửa vi phạm SDP bằng DIP: đặt một giao diện vào thành phần chỉ chứa giao diện (rất ổn định), để cả hai bên cùng phụ thuộc vào nó. Ở đây là AnalyticsTracker trong :core:model. [[src:book-carch]]', 'Martin fixes an SDP violation with DIP: put an interface in a component holding only interfaces (very stable), so both sides depend on it. Here, AnalyticsTracker in :core:model. [[src:book-carch]]'),
        ('split.s2', 'Martin, SAP: một thành phần nên trừu tượng tương xứng với độ ổn định của nó. model ổn định nhất nên chỉ chứa giao diện và data class; SDP cộng SAP chính là DIP cho thành phần. [[src:book-carch]]', 'Martin, SAP: a component should be as abstract as it is stable. model is the most stable, so it holds only interfaces and data classes; SDP plus SAP amounts to DIP for components. [[src:book-carch]]'),
        ('split.s3', 'Martin: không phải thành phần nào cũng nên ổn định; hệ thống mà mọi thứ đều ổn định tối đa thì không đổi được. Thứ hay đổi nên nằm ở trên, nơi ít ai phụ thuộc. [[src:book-carch]]', 'Martin: not all components should be stable; a system where everything is maximally stable cannot change. Volatile things belong on top, where few depend on them. [[src:book-carch]]'),
        ('split.s4', 'Phép tính dùng cùng công thức cho cả hai cách chia: với mỗi module, số lần đổi nhân với (1 + số module phụ thuộc bắc cầu vào nó), rồi cộng lại.', 'The arithmetic is the same for both splits: for each module, its changes times (1 + the number of modules transitively depending on it), summed.')]:
        m('co.' + k, vi, en)

    z = lambda k, vi, en=None: a('vz.' + k, vi, en)
    z('tab.components', 'Đồ thị module và bảng tính', 'Module graph and table')
    z('cp.cap', 'Mũi tên từ module phụ thuộc tới module được phụ thuộc; module kém ổn định ở trên. Mũi tên đỏ chỉ lên: vi phạm SDP. Số trong ô là I khi đã tính.', 'Arrows run from the depending module to the one depended on; unstable modules on top. A red upward arrow violates SDP. The number in each box is I once computed.')
    z('cp.aria', 'Đồ thị {n} module, {v} mũi tên vi phạm', 'Graph of {n} modules, {v} violating arrows')
    z('cp.tcap', 'Bảng tính kiểm chứng: I = Ce / (Ca + Ce). Cột mở dần theo bước.', 'The worked table: I = Ce / (Ca + Ce). Columns open step by step.')
    for k, vi, en in [('mod', 'Module', 'Module'), ('ca', 'Ca (vào)', 'Ca (in)'), ('ce', 'Ce (ra)', 'Ce (out)'), ('i', 'Độ bất ổn I', 'Instability I'), ('chg', 'Đổi/tháng', 'Changes/month'), ('rb', 'Build theo', 'Rebuilds'), ('flag', 'Ghi chú', 'Note')]:
        z('cp.col.' + k, vi, en)
    z('cp.flag.hot', 'ổn định mà hay đổi', 'stable yet volatile')
    z('cp.flag.sdp', 'phụ thuộc module kém ổn định hơn', 'depends on a less stable module')
    z('cp.total', 'Tổng mỗi tháng: {n} lần build module (Σ đổi × build theo).', 'Monthly total: {n} module builds (Σ changes × rebuilds).')
    z('cp.legend', 'Ô gạch đỏ: vi phạm hay "ổn định mà hay đổi". Cột "Build theo": module đó cộng mọi module phụ thuộc bắc cầu vào nó. "?": chưa tới bước đó.', 'Red hatched: a violation or "stable yet volatile". "Rebuilds" column: that module plus every module transitively depending on it. "?": that step has not come yet.')

    C = 'j9'
    a(C + '.title', 'Nguyên lý thành phần: module nào nên ổn định', 'Component principles: which modules should be stable')
    a(C + '.essence', 'Gom vào một module những lớp đổi cùng lý do (CCP); đừng buộc người dùng module phụ thuộc thứ họ không cần (CRP); không để vòng phụ thuộc (ADP).\nĐộ bất ổn định I = Ce / (Ca + Ce): Ca là số phụ thuộc đi vào, Ce là số đi ra. I gần 0 là khó dời đi (nhiều người dựa vào), I gần 1 là dễ đổi. Phụ thuộc phải đi theo hướng ổn định (SDP): mũi tên từ I lớn xuống I nhỏ.\nModule ổn định nên trừu tượng (SAP). Triệu chứng cần tìm: module I nhỏ mà hay đổi, như :core:common thập cẩm; sửa một dòng là build lại cả app.',
      'Gather into a module the classes that change for the same reason (CCP); do not force a module\'s users to depend on what they do not need (CRP); allow no dependency cycles (ADP).\nInstability I = Ce / (Ca + Ce): Ca is incoming dependencies, Ce outgoing. I near 0 is hard to move (many rely on it), I near 1 is easy to change. Dependencies must run toward stability (SDP): arrows from higher I to lower I.\nStable modules should be abstract (SAP). The symptom to look for: a low-I module that changes often, like a grab-bag :core:common; editing one line rebuilds the whole app.')
    a(C + '.goal.g1', 'Đã đối chiếu tần suất đổi với I', 'Compared change frequency with I')
    a(C + '.goal.g2', 'Đã thấy tổng số lần build', 'Saw the total rebuild count')
    a(C + '.sim.cleancode.components', 'một common cho tất cả hay chia theo lý do thay đổi', 'one common module or split by reason to change')

    S_ = 'hook'
    a(C + '.sec.%s.title' % S_, 'Đoán trước khi đọc', 'Predict before reading')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'predict', 'Module :core:common chứa mọi thứ "dùng chung", và mọi module đều phụ thuộc vào nó. Marketing thêm một tên sự kiện analytics vào common, và cả app build lại mất vài phút. Đó là cái giá không tránh được của việc dùng chung, hay dấu hiệu chia module sai?',
      'The :core:common module holds everything "shared", and every module depends on it. Marketing adds one analytics event name to common, and the whole app rebuilds for minutes. Is that the unavoidable price of sharing, or a sign of a wrong module split?')
    B(C, S_, 1, 'ans', 'Dấu hiệu chia sai. Một module nhiều người phụ thuộc thì khó đổi (Martin gọi là ổn định), nên chỉ nên chứa thứ ít đổi. Tên sự kiện analytics đổi theo từng tính năng, nên thuộc về module của tính năng đó. Mô phỏng ngay dưới tính Ca, Ce, I cho chín module và đếm số lần build lại trong một tháng.',
      'A sign of a wrong split. A module many depend on is hard to change (Martin calls it stable), so it should hold only things that rarely change. Analytics event names change with each feature, so they belong in that feature\'s module. The simulation just below computes Ca, Ce and I for nine modules and counts the rebuilds in a month.')

    S_ = 'cohesion'
    a(C + '.sec.%s.title' % S_, 'Cái gì đi cùng một module: REP, CCP, CRP', 'What goes in one module: REP, CCP, CRP')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'Martin (Clean Architecture) nêu ba nguyên lý gắn kết. REP: đơn vị dùng lại là đơn vị phát hành; người ta chỉ dùng lại thứ có quy trình phát hành và số phiên bản. CCP: gom những lớp đổi cùng lý do, cùng lúc; tách những lớp đổi vì lý do khác; đó là SRP cho thành phần, và với phần lớn app, dễ bảo trì quan trọng hơn dễ dùng lại. CRP: đừng buộc người dùng một thành phần phụ thuộc thứ họ không cần; lớp nào hay được dùng lại cùng nhau thì đặt cùng nhau. [[src:book-carch]]',
      'Martin (Clean Architecture) gives three cohesion principles. REP: the granule of reuse is the granule of release; people only reuse what has a release process and version numbers. CCP: gather classes that change for the same reasons at the same times; separate those that change for different reasons; it is SRP for components, and for most apps maintainability matters more than reusability. CRP: do not force users of a component to depend on things they do not need; classes reused together belong together. [[src:book-carch]]')
    B(C, S_, 2, 'p', 'Ba nguyên lý kéo nhau: REP và CCP làm module to ra, CRP làm module nhỏ lại. Martin cho rằng đầu dự án nên nghiêng về CCP (dễ phát triển), và khi dự án trưởng thành, được dùng lại nhiều hơn, thì nghiêng dần về REP và CRP. Một :core:common thập cẩm vi phạm cả CCP (đổi vì nhiều lý do) lẫn CRP (ai dùng một hàm định dạng cũng kéo theo tên sự kiện analytics). [[src:book-carch]]',
      'The three pull against each other: REP and CCP make modules bigger, CRP makes them smaller. Martin suggests early projects lean toward CCP (ease of development), shifting toward REP and CRP as the project matures and is reused more. A grab-bag :core:common violates both CCP (changes for many reasons) and CRP (anyone using one formatting helper drags in analytics event names). [[src:book-carch]]')

    S_ = 'stability'
    a(C + '.sec.%s.title' % S_, 'Ổn định là gì, và đo bằng I', 'What stability is, and measuring it with I')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'p', 'Martin định nghĩa ổn định là "khó dời đi": nó liên quan tới công sức cần để thay đổi, không liên quan tới tần suất thay đổi. Một cách chắc chắn làm một thành phần khó đổi là cho nhiều thành phần khác phụ thuộc vào nó. Ông đo bằng Fan-in (phụ thuộc đi vào), Fan-out (phụ thuộc đi ra) và I = Fan-out / (Fan-in + Fan-out), từ 0 (ổn định tối đa) tới 1 (bất ổn tối đa). Ví dụ trong sách: thành phần Cc có 3 phụ thuộc vào và 1 ra, nên I = 1/4. [[src:book-carch]]',
      'Martin defines stability as "not easily moved": it is about the effort needed to change something, not how often it changes. One sure way to make a component hard to change is to have many others depend on it. He measures Fan-in (incoming dependencies), Fan-out (outgoing) and I = Fan-out / (Fan-in + Fan-out), from 0 (maximally stable) to 1 (maximally unstable). The book\'s example: component Cc has 3 incoming and 1 outgoing, so I = 1/4. [[src:book-carch]]')
    B(C, S_, 2, 'p', 'Tính tay cho :core:common ở mô phỏng: 5 module phụ thuộc vào nó (app, booking, profile, reminder, data), nó phụ thuộc 1 module (analytics). I = 1 / (5 + 1) = 1/6 ≈ 0,17. Martin đếm theo số lớp bên ngoài có liên quan, mô phỏng đếm theo số module cho dễ đọc; cách lập luận giống nhau.',
      'By hand for :core:common in the simulation: 5 modules depend on it (app, booking, profile, reminder, data), it depends on 1 (analytics). I = 1 / (5 + 1) = 1/6 ≈ 0.17. Martin counts the related classes outside; the simulation counts modules for readability; the reasoning is the same.')

    S_ = 'sdp'
    a(C + '.sec.%s.title' % S_, 'ADP và SDP: không vòng, phụ thuộc theo hướng ổn định', 'ADP and SDP: no cycles, depend toward stability')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'ADP: không cho phép vòng trong đồ thị phụ thuộc thành phần. Martin kể "hội chứng sáng hôm sau": hôm qua mã chạy, sáng nay hỏng vì ai đó đổi thứ mình phụ thuộc. Với module Gradle, vòng phụ thuộc giữa hai module làm build không chạy được, nên ADP ở mức module thường lộ ra sớm; vòng giữa các package trong cùng một module thì không bị chặn như vậy. [[src:book-carch]]',
      'ADP: allow no cycles in the component dependency graph. Martin describes the "morning after syndrome": your code worked yesterday and broke this morning because someone changed something you depend on. With Gradle modules, a dependency cycle between two modules stops the build, so ADP at module level usually surfaces early; cycles between packages inside one module are not blocked that way. [[src:book-carch]]')
    B(C, S_, 2, 'p', 'SDP: phụ thuộc theo hướng ổn định, tức I của một thành phần phải lớn hơn I của những thành phần nó phụ thuộc. Vẽ thành phần kém ổn định ở trên thì mũi tên nào chỉ lên là vi phạm. Cách sửa của Martin là DIP: tạo một giao diện chứa đúng những gì bên ổn định cần, đặt nó vào một thành phần chỉ có giao diện (I = 0), để bên kém ổn định cài nó. Martin cũng nhắc không phải thành phần nào cũng nên ổn định: hệ thống mà mọi thứ ổn định tối đa thì không đổi được. [[src:book-carch]]',
      'SDP: depend in the direction of stability, so a component\'s I must exceed the I of the components it depends on. Draw unstable components on top and any upward arrow is a violation. Martin\'s fix is DIP: create an interface with exactly what the stable side needs, place it in a component holding only interfaces (I = 0), and have the unstable side implement it. Martin also stresses that not all components should be stable: a system where everything is maximally stable cannot change. [[src:book-carch]]')
    B(C, S_, 3, 'kt', '// :core:model (I = 0): chỉ giao diện và data class\ninterface AnalyticsTracker { fun track(event: String, params: Map<String, String>) }\n\n// :core:analytics (I = 3/4): cài giao diện, phụ thuộc model, network, prefs\nclass FirebaseTracker(...) : AnalyticsTracker { /* ... */ }\n\n// :feature:booking: tên sự kiện của chính nó (CCP), gọi qua giao diện\nprivate const val EVENT_BOOKED = "booking_confirmed"',
      '// :core:model (I = 0): interfaces and data classes only\ninterface AnalyticsTracker { fun track(event: String, params: Map<String, String>) }\n\n// :core:analytics (I = 3/4): implements it, depends on model, network, prefs\nclass FirebaseTracker(...) : AnalyticsTracker { /* ... */ }\n\n// :feature:booking: its own event names (CCP), called through the interface\nprivate const val EVENT_BOOKED = "booking_confirmed"')

    S_ = 'sap'
    a(C + '.sec.%s.title' % S_, 'SAP: ổn định thì nên trừu tượng', 'SAP: stable should be abstract')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'p', 'SAP: một thành phần nên trừu tượng tương xứng với độ ổn định. Chính sách cấp cao nên nằm ở thành phần ổn định để không hay bị lung lay; nhưng nếu nó cụ thể thì cũng khó mở rộng. Lời giải là OCP: thành phần ổn định chứa giao diện và lớp trừu tượng, nên vẫn mở rộng được mà không phải sửa. Martin tóm: SDP nói phụ thuộc đi theo hướng ổn định, SAP nói ổn định kéo theo trừu tượng, nên phụ thuộc đi theo hướng trừu tượng; đó là DIP cho thành phần. [[src:book-carch]]',
      'SAP: a component should be as abstract as it is stable. High-level policy should sit in stable components so it is not easily shaken; but if it is concrete, it is also hard to extend. The answer is OCP: stable components hold interfaces and abstract classes, so they can be extended without modification. Martin sums up: SDP says dependencies run toward stability, SAP says stability implies abstraction, so dependencies run toward abstraction; that is DIP for components. [[src:book-carch]]')
    B(C, S_, 2, 'note', 'Track Kiến trúc (G9) dạy cách chia module Android theo tầng và theo tính năng; chương này cho công cụ đo để biết cách chia đó có đúng hướng không.',
      'The Architecture track (G9) teaches splitting Android modules by layer and by feature; this chapter gives the measuring tools to check that split points the right way.')
    B(C, S_, 2, 'kind', 'android')

    S_ = 'bugs'
    a(C + '.sec.%s.title' % S_, 'Hai lỗi hay gặp', 'Two common bugs')
    a(C + '.sec.%s.badge' % S_, 'stable')
    B(C, S_, 1, 'bug', 'Sửa một dòng ở :core:common, cả app build lại vài phút; nhiều người sửa common cùng lúc nên hay xung đột khi gộp.', 'Editing one line in :core:common rebuilds the whole app for minutes; many people edit common at once and merges conflict.')
    B(C, S_, 1, 'cause', 'common có I nhỏ (nhiều module phụ thuộc) nhưng chứa thứ đổi vì nhiều lý do: tên sự kiện, định dạng, cờ tính năng.', 'common has a low I (many dependents) yet holds things that change for many reasons: event names, formatting, feature flags.')
    B(C, S_, 1, 'fix', 'Chia theo CCP: trả phần hay đổi về module tính năng dùng nó; để lại một module ổn định chỉ chứa data class và giao diện.', 'Split by CCP: move the volatile parts back to the feature modules that use them; keep one stable module of data classes and interfaces.')
    B(C, S_, 2, 'bug', 'Nâng phiên bản SDK analytics, nhưng phải biên dịch lại cả các module không hề gửi sự kiện.', 'Upgrading the analytics SDK recompiles even modules that never send events.')
    B(C, S_, 2, 'cause', 'Module ổn định (common) phụ thuộc module kém ổn định (analytics, đi theo SDK): mũi tên chỉ lên, vi phạm SDP; mọi thứ phụ thuộc bắc cầu vào SDK.', 'A stable module (common) depends on a less stable one (analytics, following the SDK): an upward arrow, an SDP violation; everything depends on the SDK transitively.')
    B(C, S_, 2, 'fix', 'Đảo phụ thuộc: giao diện AnalyticsTracker ở module ổn định, analytics cài nó; chỉ :app nối hai bên khi khởi tạo (DI, track Kiến trúc G6).', 'Invert the dependency: an AnalyticsTracker interface in the stable module, implemented by analytics; only :app wires them together at startup (DI, Architecture track G6).')

    S_ = 'ex'
    a(C + '.sec.%s.title' % S_, 'Bài tập', 'Exercise')
    a(C + '.sec.%s.badge' % S_, 'guideline')
    B(C, S_, 1, 'ex', 'Bốn module: :app phụ thuộc :feature:chat và :core:ui; :feature:chat phụ thuộc :core:ui và :core:network; :core:ui phụ thuộc :feature:chat (để lấy màu của bong bóng chat). Tính Ca, Ce, I cho từng module, chỉ ra nguyên lý nào bị vi phạm, và sửa.', 'Four modules: :app depends on :feature:chat and :core:ui; :feature:chat depends on :core:ui and :core:network; :core:ui depends on :feature:chat (to get chat bubble colours). Compute Ca, Ce and I for each, name the principles violated, and fix it.')
    B(C, S_, 1, 'hint', 'Đếm cả phụ thuộc của :core:ui vào :feature:chat. Có vòng nào không? Gradle có build được không?', 'Count :core:ui\'s dependency on :feature:chat too. Is there a cycle? Would Gradle build it?')
    B(C, S_, 1, 'sol', ':app: Ca 0, Ce 2, I = 1. :feature:chat: Ca 2 (app, ui), Ce 2 (ui, network), I = 1/2. :core:ui: Ca 2 (app, chat), Ce 1 (chat), I = 1/3. :core:network: Ca 1, Ce 0, I = 0. Vi phạm ADP: vòng chat ↔ ui (Gradle sẽ không build). Vi phạm SDP: ui (1/3) phụ thuộc chat (1/2). Sửa: màu bong bóng là một token thiết kế, đặt vào :core:ui (hay một module theme); chat đọc nó từ ui, bỏ phụ thuộc ui → chat. Sau sửa: ui có Ca 2, Ce 0, I = 0; chat I = 2/3.',
      ':app: Ca 0, Ce 2, I = 1. :feature:chat: Ca 2 (app, ui), Ce 2 (ui, network), I = 1/2. :core:ui: Ca 2 (app, chat), Ce 1 (chat), I = 1/3. :core:network: Ca 1, Ce 0, I = 0. ADP is violated: the chat ↔ ui cycle (Gradle will not build it). SDP is violated: ui (1/3) depends on chat (1/2). Fix: the bubble colour is a design token; put it in :core:ui (or a theme module); chat reads it from ui, removing the ui → chat dependency. After the fix: ui has Ca 2, Ce 0, I = 0; chat I = 2/3.')

    S_ = 'honest'
    a(C + '.sec.%s.title' % S_, 'Chương này giản lược những gì', 'What this chapter simplifies')
    a(C + '.sec.%s.badge' % S_, 'simplified')
    B(C, S_, 1, 'p', 'REP, CCP, CRP theo Robert C. Martin, Clean Architecture; ADP, SDP, định nghĩa ổn định, Fan-in, Fan-out, I, ví dụ Cc, cách sửa bằng DIP và SAP theo ch.14. Đọc ngày 2026-11-24, diễn đạt lại. Martin đếm theo số lớp; mô phỏng đếm theo số module. Chương không trình bày độ trừu tượng A và khoảng cách tới đường chính (main sequence) của sách. Chín module, tần suất đổi, công thức đếm lần build lại là minh họa của site; build tăng dần thật của Gradle bỏ qua những thay đổi không chạm ABI nên số thật nhỏ hơn. Nhận xét về vòng phụ thuộc giữa module Gradle là của site.',
      'REP, CCP and CRP follow Robert C. Martin, Clean Architecture; ADP, SDP, the definition of stability, Fan-in, Fan-out, I, the Cc example, the DIP fix and SAP follow ch.14. Read on 2026-11-24 and paraphrased. Martin counts classes; the simulation counts modules. The chapter does not present the book\'s abstractness A and distance from the main sequence. The nine modules, change frequencies and rebuild formula are the site\'s illustration; Gradle\'s real incremental build skips changes that do not touch the ABI, so real numbers are lower. The remark about dependency cycles between Gradle modules is the site\'s.')

    for q, qv, qe, av, ae, wv, we in [
        ('q1', 'Module X có 4 module phụ thuộc vào và phụ thuộc 1 module. I của X là bao nhiêu?', 'Module X has 4 dependents and depends on 1 module. What is X\'s I?', '1/5 = 0,2.', '1/5 = 0.2.', 'Thay vào công thức: I = Ce / (Ca + Ce) = 1 / (4 + 1).', 'Plug into the formula: I = Ce / (Ca + Ce) = 1 / (4 + 1).'),
        ('q2', 'Theo Martin, "ổn định" có nghĩa là ít thay đổi không?', 'For Martin, does "stable" mean rarely changing?', 'Không; nghĩa là khó dời đi, vì nhiều thứ dựa vào nó.', 'No; it means hard to move, because many things rely on it.', 'Vấn đề là đặt thứ hay đổi vào module ổn định.', 'The problem is putting volatile things in a stable module.'),
        ('q3', 'Mũi tên phụ thuộc chỉ từ module I = 0,2 tới module I = 0,7. Có vi phạm gì không?', 'A dependency arrow runs from a module with I = 0.2 to one with I = 0.7. Any violation?', 'Có: vi phạm SDP.', 'Yes: it violates SDP.', 'Phụ thuộc phải đi từ I lớn xuống I nhỏ.', 'Dependencies must run from higher I to lower I.'),
        ('q4', 'CCP là nguyên lý SOLID nào nói lại cho thành phần?', 'CCP restates which SOLID principle for components?', 'SRP.', 'SRP.', 'Gom những gì đổi cùng lý do, tách những gì đổi vì lý do khác.', 'Gather what changes for the same reason; separate what changes for different reasons.')]:
        a(C + '.quiz.%s.q' % q, qv, qe); a(C + '.quiz.%s.a' % q, av, ae); a(C + '.quiz.%s.why' % q, wv, we)
