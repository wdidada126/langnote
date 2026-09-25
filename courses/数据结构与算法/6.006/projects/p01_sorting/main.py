"""p01 排序与渐近（L03-L05, L18）：插入排序 / 归并排序 / 堆排序。

思想：用"比较次数"代替挂钟时间做增长率实验（确定性、可复现），
验证 插入 ~ n^2/2、归并/堆 ~ n log2 n 的渐近斜率（2n/n 比值：二次→~4，nlogn→~2+一点）。
"""
import random


# ---------------- 插入排序（L05） ----------------
def insertion_sort(a, stats=None):
    n = len(a)
    for j in range(1, n):
        key = a[j]
        i = j - 1
        while i >= 0:
            if stats is not None:
                stats[0] += 1
            if a[i] <= key:
                break
            a[i + 1] = a[i]
            i -= 1
        a[i + 1] = key


# ---------------- 归并排序（L04） ----------------
def merge_sort(a, stats=None):
    if len(a) <= 1:
        return a[:]
    mid = len(a) // 2
    left = merge_sort(a[:mid], stats)
    right = merge_sort(a[mid:], stats)
    return _merge(left, right, stats)


def _merge(left, right, stats):
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if stats is not None:
            stats[0] += 1
        if left[i] <= right[j]:        # 取等 -> 稳定
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


# ---------------- 堆排序（L18） ----------------
def _sift_down(a, i, size, stats):
    while True:
        best = i
        l, r = 2 * i + 1, 2 * i + 2
        for c in (l, r):
            if c < size:
                if stats is not None:
                    stats[0] += 1
                if a[c] > a[best]:
                    best = c
        if best == i:
            return
        a[i], a[best] = a[best], a[i]
        i = best


def build_heap(a, stats=None):
    for i in range(len(a) // 2 - 1, -1, -1):   # Θ(n) 建堆（L18 和式）
        _sift_down(a, i, len(a), stats)


def heap_sort(a, stats=None):
    build_heap(a, stats)                       # 建堆不计入比较统计亦可
    for k in range(len(a) - 1, 0, -1):
        a[0], a[k] = a[k], a[0]               # 最大值就位
        _sift_down(a, 0, k, stats)


# ---------------- 实验 ----------------
def _lg(n):
    return n.bit_length() - 1 if n >= 1 else 0


def growth_table(sizes=(500, 1000, 2000, 4000, 8000)):
    print('== 比较次数增长率表（随机排列, 种子 42） ==')
    header = f"{'n':>6} | {'插入':>10} | {'归并':>10} | {'堆排':>10} | {'n^2/2':>12} | {'n·lg n':>9}"
    print(header)
    print('-' * len(header))
    prev = None
    for n in sizes:
        rnd = random.Random(42)
        base = list(range(n))
        rnd.shuffle(base)
        s = [0]
        a = base[:]; insertion_sort(a, s); ins = s[0]
        s = [0]
        merge_sort(base[:], s); mrg = s[0]
        s = [0]
        a = base[:]; heap_sort(a, s); hsp = s[0]
        assert a == sorted(base)
        ratio = ''
        if prev:
            ratio = (f"  倍率 插入 {ins / prev[0]:5.2f} 归并 {mrg / prev[1]:5.2f}"
                     f" 堆排 {hsp / prev[2]:5.2f}（理论: 二次≈4.00, nlogn≈2+）")
        print(f"{n:6d} | {ins:10d} | {mrg:10d} | {hsp:10d} | {n * n // 2:12d} | {n * _lg(n):9d}")
        if ratio:
            print(ratio)
        prev = (ins, mrg, hsp)


def best_case_check():
    print('== 最好/最坏情况（L05） ==')
    n = 4000
    s = [0]
    insertion_sort(list(range(n)), s)
    best = s[0]
    s = [0]
    insertion_sort(list(range(n, 0, -1)), s)
    worst = s[0]
    print(f"已排输入比较数 = {best} (Θ(n), 期望 n-1={n - 1})")
    print(f"逆序输入比较数 = {worst} (Θ(n²), n(n-1)/2={n * (n - 1) // 2})")
    assert best == n - 1
    assert worst == n * (n - 1) // 2


def self_test():
    rnd = random.Random(7)
    for trial in range(200):
        n = rnd.randint(0, 60)
        base = [rnd.randint(-50, 50) for _ in range(n)]
        want = sorted(base)
        a = base[:]; insertion_sort(a); assert a == want, 'insertion'
        assert merge_sort(base[:]) == want, 'merge'
        a = base[:]; heap_sort(a); assert a == want, 'heap'
    # 稳定性抽查：键相同、只按 key 比较时，稳定排序应保持原相对序
    class Item:
        __slots__ = ('key', 'tag')
        def __init__(self, key, tag):
            self.key = key; self.tag = tag
        def __lt__(self, other): return self.key < other.key
        def __le__(self, other): return self.key <= other.key
        def __eq__(self, other): return self.key == other.key
    items = [Item(1, i) for i in range(30)]
    got = merge_sort(items[:])                  # 归并取等先走左侧 -> 稳定
    assert all(x.tag == i for i, x in enumerate(got)), 'merge stability'
    a = items[:]; insertion_sort(a)             # 插入的 `a[i] <= key` 亦稳定
    assert all(x.tag == i for i, x in enumerate(a)), 'insertion stability'
    print('自测通过：三种排序对 200 组随机数组与 sorted() 一致；归并/插入稳定性通过。')


if __name__ == '__main__':
    self_test()
    best_case_check()
    growth_table()
    print('\n提示：把表里"倍率"列与 4.00 / ~2.17 对比即 L03 增长阶的实测证据。')
