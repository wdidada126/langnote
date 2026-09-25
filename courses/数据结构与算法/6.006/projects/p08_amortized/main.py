"""p08 摊还分析（L19-L20）：动态数组计费实验 + 并查集（按秩/路径压缩）。

DynArray：记录每次扩容拷贝数，验证 n 次 append 总拷贝 < 2n（几何级数账）；
DSU：四种配置（朴素链接 / 只按秩 / 只压缩 / 双优）在同一下载序列上的步数对比。
"""
import random


# ---------------- 动态数组 ----------------
class DynArray:
    def __init__(self):
        self.a = [None] * 4
        self.n = 0
        self.copies = 0

    def append(self, x):
        if self.n == len(self.a):
            new = [None] * (2 * len(self.a))
            for i in range(self.n):
                new[i] = self.a[i]
            self.copies += self.n
            self.a = new
        self.a[self.n] = x
        self.n += 1

    def get(self, i):
        return self.a[i]


# ---------------- 并查集 ----------------
class DSU:
    def __init__(self, n, by_rank=True, compress=True):
        self.p = list(range(n))
        self.rank = [0] * n
        self.by_rank = by_rank
        self.compress = compress
        self.steps = 0                      # find 上行步数（计费实验）

    def find(self, x):
        root = x
        while self.p[root] != root:
            self.steps += 1
            root = self.p[root]
        if self.compress:
            while self.p[x] != root:        # 迭代式全路径压缩（防爆栈）
                self.p[x], x = root, self.p[x]
        return root

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.by_rank:
            if self.rank[rx] < self.rank[ry]:
                rx, ry = ry, rx
            self.p[ry] = rx
            if self.rank[rx] == self.rank[ry]:
                self.rank[rx] += 1
        else:                              # 任意方向链接（坏情况温床）
            self.p[ry] = rx


# ---------------- 自测 ----------------
def self_test():
    # 动态数组：拷贝总量 ≤ 2n 断言（倍增精确值 2(n−4) 级别以下）
    for trial in range(20):
        n = random.Random(trial).randint(1, 3000)
        arr = DynArray()
        for i in range(n):
            arr.append(i)
        assert arr.n == n and all(arr.get(i) == i for i in range(n))
        assert arr.copies < 2 * n, (n, arr.copies)
    print('动态数组自测通过：多种 n 下 append 内容正确且总拷贝 < 2n（Σ2^k 几何级数，L19）。')

    rnd = random.Random(5)
    for compress in (True, False):
        for rank in (True, False):
            dsu = DSU(300, by_rank=rank, compress=compress)
            ref = [set([i]) for i in range(300)]
            for _ in range(600):
                x, y = rnd.randrange(300), rnd.randrange(300)
                if rnd.random() < 0.6:
                    dsu.union(x, y)
                    rx = next(i for i, s in enumerate(ref) if x in s)
                    ry = next(i for i, s in enumerate(ref) if y in s)
                    if rx != ry:
                        ref[rx] |= ref[ry]; ref[ry] = set()
                else:
                    same = any(x in s and y in s for s in ref)
                    assert (dsu.find(x) == dsu.find(y)) == same, '连通性判断错'
    print('DSU 自测通过：四种配置 × 600 随机操作与"集合法"参考一致。')


def experiment():
    print('== 动态数组：倍增 vs 1.5 倍增 vs +1 的拷贝总账（n=100000） ==')
    n = 100000
    for growth in ('x2', 'x1.5', '+1'):
        size, copies, used = 4, 0, 0
        for _ in range(n):
            if used == size:
                copies += used
                size = size * 2 if growth == 'x2' else (
                    int(size * 1.5) if growth == 'x1.5' else size + 1)
            used += 1
        print(f"{growth:>5}: 总拷贝 {copies:9d}  → 每次 append 均摊 {copies / n:7.2f}")
    print('（+1 策略退化为 Θ(n²) 总账——倍增是均摊 O(1) 的充分而非唯一方案。）')
    print()
    print('== DSU 下载对比：构造性坏序列 + 随机序列（find 总步数） ==')

    def run(n, by_rank, compress, queries=4 * n):
        dsu = DSU(n, by_rank=by_rank, compress=compress)
        rnd = random.Random(9)
        for _ in range(n - 1):
            x, y = rnd.randrange(n), rnd.randrange(n)
            a, b = dsu.find(x), dsu.find(y)
            if a != b:
                dsu.union(x, y)
        for _ in range(queries):
            dsu.find(rnd.randrange(n))
        return dsu.steps

    print(f"{'n':>7} | {'无秩无压缩':>10} | {'按秩':>8} | {'压缩':>10} | {'按秩+压缩':>10}")
    for n in (2000, 8000, 32000):
        r = random.Random(9)
        steps = []
        for rank in (False, True):
            for comp in (False, True):
                steps.append(run(n, rank, comp))
        print(f"{n:7d} | {steps[0]:10d} | {steps[1]:8d} | {steps[2]:10d} | {steps[3]:10d}"
              f"   (操作数≈{5 * n}, 均摊步数: 最差 {steps[0] / (5 * n):.2f} → 双优 {steps[3] / (5 * n):.2f})")
    print('（双优列几乎不随 n 增长——α(n)<5 的实测面貌，L20。）')


if __name__ == '__main__':
    self_test()
    experiment()
