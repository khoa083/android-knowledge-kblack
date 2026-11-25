"""Công cụ viết lại một module chương: rep (thay đúng một chỗ), call (thay hai chuỗi của một lời gọi một/hai dòng), drop_honest."""
import io


class RW:
    def __init__(self, path):
        self.p = path
        self.s = io.open(path, encoding='utf-8').read()

    def rep(self, a, b):
        assert self.s.count(a) == 1, (self.s.count(a), a[:100])
        self.s = self.s.replace(a, b)

    def call(self, head, vi, en, nth=None):
        s = self.s
        if nth is None:
            assert s.count(head) == 1, (s.count(head), head)
            i = s.index(head) + len(head)
        else:
            i = -1
            for _ in range(nth + 1):
                i = s.index(head, i + 1)
            i += len(head)
        j = s.index(')\n', i)
        assert s[i:j].count('\n') <= 1, head
        self.s = s[:i] + ', ' + repr(vi) + ',\n      ' + repr(en) + s[j:]

    def block(self, sec, n, field, vi, en):
        """Thay cả hai chuỗi của B(C, S_, n, 'field', vi, en) trong mục S_ = 'sec'."""
        s = self.s
        i = s.index("    S_ = '%s'" % sec)
        j = s.find("    S_ = '", i + 5)
        if j < 0:
            j = len(s)
        head = "    B(C, S_, %d, '%s', " % (n, field)
        k = s.index(head, i)
        assert k < j, (sec, n, field)
        start = k + len(head)
        end = s.index(')\n', start)
        self.s = s[:start] + repr(vi) + ',\n      ' + repr(en) + s[end:]

    def block2(self, sec, n, field, vi, en, var='S'):
        """Như block, cho module dùng `S = 'sec'` và `B(C, S, n, 'field',` (chuỗi có thể nằm ở dòng sau), như track coroutines."""
        s = self.s
        i = s.index("    %s = '%s'" % (var, sec))
        j = s.find("    %s = '" % var, i + 5)
        if j < 0:
            j = len(s)
        head = "    B(C, %s, %d, '%s'," % (var, n, field)
        k = s.index(head, i)
        assert k < j, (sec, n, field)
        start = k + len(head)
        end = s.index(')\n', start)
        self.s = s[:start] + ' ' + repr(vi) + ',\n      ' + repr(en) + s[end:]

    def drop_honest(self, ch):
        self.rep(", 'recall', 'honest']}", ", 'recall']}")
        i = self.s.index("    S_ = 'honest'")
        j = self.s.index("    for q, qv, qe", i)
        self.s = self.s[:i] + self.s[j:]

    def save(self):
        io.open(self.p, 'w', encoding='utf-8', newline='\n').write(self.s)
        print('ok', self.p.rsplit('/', 1)[-1])
