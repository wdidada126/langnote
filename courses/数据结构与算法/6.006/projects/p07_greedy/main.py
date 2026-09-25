"""p07 贪心（L11 贪心正确性、L18 Huffman 用堆）：区间调度 + Huffman 编码。

区间调度：三策略对照（最早开始/最短区间/最早结束），随机反例搜索证明只有
"最早结束"恒等于暴力最优；Huffman：堆合并构造前缀码，验证 Kraft 等式与
熵下界 H ≤ L < H+1。
"""
import heapq
import itertools
import math
import random


# ---------------- 区间调度 ----------------
def schedule_by(intervals, key):
    """贪心框架：按 key 排序后依次接受兼容区间。返回 (选择数, 选择集合)。"""
    sel, last_end = [], None
    for iv in sorted(intervals, key=key):
        if last_end is None or iv[0] >= last_end:
            sel.append(iv)
            last_end = iv[1]
    return len(sel), sel


def schedule_brute(intervals):
    best = 0
    for r in range(len(intervals) + 1):
        for comb in itertools.combinations(intervals, r):
            ok = all(a[1] <= b[0] or b[1] <= a[0]
                     for a, b in itertools.combinations(comb, 2))
            if ok:
                best = max(best, r)
    return best


def earliest_finish(intervals):
    return schedule_by(intervals, key=lambda iv: iv[1])[0]


# ---------------- Huffman ----------------
def huffman_lengths(freqs):
    """freqs: dict symbol->count。用堆显式建树，返回 (每符号码长 dict, 加权平均码长)。"""
    total = sum(freqs.values())
    if len(freqs) == 1:
        return {next(iter(freqs)): 1}, 1.0

    class N:
        __slots__ = ('w', 'syms', 'l', 'r')
        def __init__(self, w, syms, l=None, r=None):
            self.w, self.syms, self.l, self.r = w, syms, l, r

    heap = [[c, i, N(c, [s])] for i, (s, c) in enumerate(freqs.items())]
    heapq.heapify(heap)
    tie = len(freqs)                       # 第二关键字: 稳定合并次序
    while len(heap) > 1:
        _, _, a = heapq.heappop(heap)
        _, _, b = heapq.heappop(heap)
        n = N(a.w + b.w, a.syms + b.syms, a, b)
        heapq.heappush(heap, [n.w, tie, n])
        tie += 1

    lengths = {}
    def assign(node, depth):
        if node.l is None and node.r is None:
            lengths[node.syms[0]] = depth
            return
        if node.l:
            assign(node.l, depth + 1)
        if node.r:
            assign(node.r, depth + 1)
    assign(heap[0][2], 0)
    avg = sum(freqs[s] * lengths[s] for s in freqs) / total
    return lengths, avg


def entropy(freqs):
    total = sum(freqs.values())
    return -sum((c / total) * math.log2(c / total) for c in freqs.values() if c)


def prefix_free_check(freqs, lengths):
    """Kraft 不等式: Σ 2^-l ≤ 1（恰为满树取等）→ 前缀码存在。"""
    kraft = sum(2.0 ** (-l) for l in lengths.values())
    assert kraft <= 1.0 + 1e-9, kraft
    return kraft


# ---------------- 自测与实验 ----------------
def self_test():
    intervals = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11)]
    assert earliest_finish(intervals) == schedule_brute(intervals) == 3
    print('CLRS 16.1 经典例：最早结束=3=暴力最优。')

    rnd = random.Random(4)
    bad_start_gap = bad_len_gap = 0
    for _ in range(300):
        n = rnd.randint(2, 9)
        ivs = []
        for _ in range(n):
            a = rnd.randint(0, 20)
            ivs.append((a, a + rnd.randint(1, 8)))
        opt = schedule_brute(ivs)
        ef = schedule_by(ivs, lambda iv: iv[1])[0]
        st = schedule_by(ivs, lambda iv: iv[0])[0]
        ln = schedule_by(ivs, lambda iv: (iv[1] - iv[0], iv[1]))[0]
        assert ef == opt, ivs
        bad_start_gap = max(bad_start_gap, opt - st)
        bad_len_gap = max(bad_len_gap, opt - ln)
    assert bad_start_gap > 0 and bad_len_gap > 0, '反例搜索失败?!'
    print(f'300 组随机实例：最早结束恒最优(交换论证 L11)；最早开始最大落后 {bad_start_gap}、'
          f'最短区间最大落后 {bad_len_gap} —— 反例已被自动找到。')

    freqs = {'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5}
    lengths, avg = huffman_lengths(freqs)
    H = entropy(freqs)
    prefix_free_check(freqs, lengths)
    assert H <= avg < H + 1, (H, avg)
    print(f'Huffman(CLSR 例): 加权码长 {avg:.3f} bit/符 落在 [H={H:.3f}, H+1) 内；码长 {lengths}')


def experiment():
    rnd = random.Random(42)
    print('== Zipf 分布上的 Huffman：码长与熵 ==')
    print(f"{'字母表':>6} | {'熵 H':>7} | {'Huffman L':>9} | {'定长':>6} | 省比率")
    for sigma in (8, 16, 32, 64):
        freqs = {}
        for i in range(sigma):
            freqs[chr(97 + i % 26) + str(i)] = max(1, int(rnd.paretovariate(1.0)))
        lengths, avg = huffman_lengths(freqs)
        H = entropy(freqs)
        fixed = math.ceil(math.log2(sigma))
        total_bits = sum(freqs.values())
        saving = (fixed - avg) / fixed
        print(f"{sigma:6d} | {H:7.3f} | {avg:9.3f} | {fixed:6d} | {saving:6.1%}"
              f"   (最大码长 {max(lengths.values())})")
    print('（偏斜越大省得越多；最大码长可能远超 log σ —— 极端偏斜时 Huffman 码长无上界，L18 注脚。）')


if __name__ == '__main__':
    self_test()
    experiment()
