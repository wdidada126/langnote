"""sieve.py —— 无穷素数筛的两种惰性实现（对应讲义 L23；SICP §3.5.2 练习 3.67 谱系）。

A) stream_sieve：埃氏筛的"流"版——每发现一个素数，就过滤掉它的倍数，
   递归构造无穷流；第 n 个素数只需按需 force。
B) gen_sieve：同一算法的生成器版（L12），用 yield/yield from。
运行：python sieve.py ；自检：python -m py_compile sieve.py streams.py sieve.py
"""

import time

from streams import Stream, Thunk, integers_from, s_take


# ---------------- A) memoized 流版（可重放） ----------------

def stream_sieve(s):
    """取首元素为素数 p，其余过滤 p 的倍数后递归构造无穷流。"""
    p = s.first
    return Stream(p, Thunk(lambda: stream_sieve(_filter_not_mult(p, s.cdr()))))


def _filter_not_mult(p, s):
    x = s.first
    if x % p == 0:
        return _filter_not_mult(p, s.cdr())
    return Stream(x, Thunk(lambda: _filter_not_mult(p, s.cdr())))


def prime_stream():
    return stream_sieve(integers_from(2))


# ---------------- B) 生成器版（一次性，更省内存样板） ----------------

def gen_sieve(it):
    head = next(it)
    yield head
    yield from gen_sieve(x for x in it if x % head)


def gen_primes(start=2):
    return gen_sieve(iter(range(start, 10 ** 9)))   # 足够"无穷"


def main():
    print('== 无穷素数筛（L23 流与惰性求值） ==')
    sp = prime_stream()
    t0 = time.perf_counter()
    first10_stream = s_take(10, sp)
    t1 = time.perf_counter()
    # memo 演示：第 101 个素数只需推进一次，随后重放 O(1)
    p101_walk = sp
    t2 = time.perf_counter()
    for _ in range(100):
        p101_walk = p101_walk.cdr()
    p101 = p101_walk.first
    t3 = time.perf_counter()
    replay0 = p101_walk.first
    t4 = time.perf_counter()

    gp = gen_primes()
    t5 = time.perf_counter()
    first10_gen = [next(gp) for _ in range(10)]
    t6 = time.perf_counter()

    assert first10_stream == first10_gen == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert p101 == 547 and replay0 == 547
    print(f'流版  前 10 素数: {first10_stream}  ({(t1-t0)*1e3:.2f} ms)')
    print(f'生成器 前 10 素数: {first10_gen}  ({(t6-t5)*1e3:.2f} ms)')
    print(f'第 101 个素数 = {p101}；首次走到: {(t3-t2)*1e3:.2f} ms，'
          f'memo 重放: {(t4-t3)*1e6:.1f} µs —— 惰性+记忆化 = 时间空间互买（L08/L23）')

    # 孪生素数流：map + filter 的组合子玩法
    from streams import s_filter
    twins_head = s_filter(
        lambda p: p > 3 and is_twin(p),
        prime_stream())
    print('孪生素数(前 8):', s_take(8, twins_head))


def is_twin(p):
    """p 与 p-2 皆素数（小范围试除即可）。"""
    def is_prime(n):
        if n < 2:
            return False
        i = 2
        while i * i <= n:
            if n % i == 0:
                return False
            i += 1
        return True
    return is_prime(p - 2)


if __name__ == '__main__':
    main()
