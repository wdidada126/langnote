"""streams.py —— 流与惰性求值：Scheme 风格 memoized 流 + Python 生成器风格（对应 L23）。

两种实现同一数学对象 Stream = (首值 . 延迟尾流)：
  1. Stream 类：显式 delay/force + memoization（SICP §3.5 原教旨，对接 P4 的
     cons-stream/Thunk）；
  2. 生成器：yield 即语言内建 delay（L12）——但**一次性**、无 memo。
自检：python -m py_compile streams.py
"""


# ---------------- 1) Scheme 风格：delay/force + memo ----------------

class Thunk:
    """延迟计算体：可重放（force 后缓存），对照 scheme.py 的 Thunk。"""

    def __init__(self, fn):
        self.fn, self.value, self.forced = fn, None, False

    def force(self):
        if not self.forced:
            self.value, self.forced = self.fn(), True
        return self.value


class Stream:
    __slots__ = ('first', 'rest_thunk')

    def __init__(self, first, rest_thunk):
        self.first = first                 # 严格首元素
        self.rest_thunk = rest_thunk       # Thunk -> Stream

    def cdr(self):
        return self.rest_thunk.force()     # memo：重复访问 O(1)

    def ref(self, n):
        s = self
        for _ in range(n):
            s = s.cdr()
        return s


def cons_stream(first_fn, rest_fn):
    """首元素也延迟（构造无穷自引用流时需要）。"""
    return Stream(Thunk(first_fn).force(), Thunk(rest_fn))


def integers_from(n=1):
    return Stream(n, Thunk(lambda: integers_from(n + 1)))


def s_map(fn, s):
    return Stream(fn(s.first), Thunk(lambda: s_map(fn, s.cdr())))


def s_filter(pred, s):
    while not pred(s.first):
        s = s.cdr()
    return Stream(s.first, Thunk(lambda: s_filter(pred, s.cdr())))


def s_take(n, s):
    out = []
    for _ in range(n):
        out.append(s.first)
        s = s.cdr()
    return out


# ---------------- 2) 生成器风格：yield = 内建 delay ----------------

def g_integers_from(n=1):
    while True:
        yield n
        n += 1


def g_map(fn, it):
    for x in it:
        yield fn(x)


def g_filter(pred, it):
    for x in it:
        if pred(x):
            yield x


def g_take(n, it):
    out = []
    for _ in range(n):
        out.append(next(it))
    return out


def _selftest():
    # memo 验证：同一 cdr 两次 → 同一对象
    ints = integers_from(1)
    tail = ints.cdr()
    assert tail is ints.cdr()
    assert s_take(5, ints) == [1, 2, 3, 4, 5]
    assert s_take(4, s_map(lambda x: x * x, integers_from(1))) == [1, 4, 9, 16]
    evens = s_filter(lambda x: x % 2 == 0, integers_from(1))
    assert s_take(3, evens) == [2, 4, 6]
    # 无穷自引用流（SICP 名场面）：常数流 ones —— 手工制造循环引用
    ones = Stream(1, None)
    ones.rest_thunk = Thunk(lambda: ones)
    assert ones.cdr().cdr().cdr().first == 1
    # 生成器版等价
    assert g_take(5, g_integers_from(1)) == [1, 2, 3, 4, 5]
    assert g_take(4, g_map(lambda x: x * x, g_integers_from(1))) == [1, 4, 9, 16]
    import itertools
    assert list(itertools.islice((x for x in g_integers_from(2)
                                 if all(x % p for p in itertools.takewhile(
                                     lambda q: q * q <= x, g_integers_from(2)))), 6)) \
        == [2, 3, 5, 7, 11, 13]
    print('streams selftest OK')


if __name__ == '__main__':
    _selftest()
