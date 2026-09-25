"""p04 随机化（L26/L17）：随机化 quickselect 中位数 + Erdős–Rényi 随机图连通阈值。

quickselect：随机 pivot 期望 O(n)（用划分比较次数对拍 2n 量级）；
随机图：G(n, p) 生成 + BFS 数连通分量，扫描 p 观察 0→1 阈值在 p=1/n 附近。
"""
import random
from collections import deque


# ---------------- 随机化 quickselect ----------------
def _partition(a, lo, hi, rnd):
    r = rnd.randint(lo, hi)
    a[r], a[hi] = a[hi], a[r]
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i


def quickselect(a, k, rnd, stats=None):
    lo, hi = 0, len(a) - 1
    while True:
        p = _partition(a, lo, hi, rnd)
        if stats is not None:
            stats[0] += hi - lo
        if p == k:
            return a[k]
        if k < p:
            hi = p - 1
        else:
            lo = p + 1


def median(a, rnd, stats=None):
    b = a[:]
    n = len(b)
    if n % 2 == 1:
        return quickselect(b, n // 2, rnd, stats)
    lo = quickselect(b, n // 2 - 1, rnd, stats)
    hi = quickselect(b, n // 2, rnd, stats)   # 简化: 两次选择, 常数 2 不影响阶
    return (lo + hi) / 2.0


# ---------------- ER 随机图 ----------------
def er_graph(n, p, rnd):
    adj = [[] for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if rnd.random() < p:
                adj[u].append(v)
                adj[v].append(u)
    return adj


def num_components(adj):
    seen = [False] * len(adj)
    comp = 0
    for s in range(len(adj)):
        if seen[s]:
            continue
        comp += 1
        seen[s] = True
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    q.append(v)
    return comp


# ---------------- 自测与实验 ----------------
def self_test():
    rnd = random.Random(2024)
    for trial in range(200):
        n = rnd.randint(1, 200)
        a = [rnd.randint(-1000, 1000) for _ in range(n)]
        k = rnd.randrange(n)
        assert quickselect(a[:], k, rnd) == sorted(a)[k], 'quickselect vs sorted'
        med = median(a[:], rnd)
        s = sorted(a)
        want = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0
        assert abs(med - want) < 1e-9, 'median'
    print('quickselect 自测通过：200 组与 sorted() 对拍一致。')

    adj = er_graph(60, 0.05, random.Random(1))
    assert num_components(adj) >= 1
    assert num_components([]) == 0
    print('随机图生成/分量计数冒烟通过。')


def experiment_select(sizes=(2000, 8000, 32000, 128000)):
    print('== quickselect 期望线性：平均划分工作量 vs n ==')
    print(f"{'n':>8} | {'平均工作量(≈c·n)':>16} | {'c':>6}")
    for n in sizes:
        total, trials = 0, 20
        for t in range(trials):
            rnd = random.Random(1000 + t)
            a = [rnd.randint(0, 10 ** 6) for _ in range(n)]
            s = [0]
            quickselect(a, n // 2, rnd, s)
            total += s[0]
        avg = total / trials
        print(f"{n:8d} | {avg:16.0f} | {avg / n:6.2f}   (理论 E~2n 量级, 与 n 无关的 c)")


def experiment_threshold(ns=(400,)):
    for n in ns:
        print(f'== G({n}, p) 巨分量涌现：p 扫过 1/n={1 / n:.4f} ==')
        print(f"{'p·n':>6} | {'p':>8} | {'最大分量规模/n':>14} | 连通比例")
        for c in (0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0):
            p = c / n
            biggest_sum = 0
            conn = 0
            trials = 40
            for t in range(trials):
                adj = er_graph(n, p, random.Random(500 + t))
                seen = [False] * n
                biggest = 0
                for s in range(n):
                    if seen[s]:
                        continue
                    cnt = 0
                    q = deque([s]); seen[s] = True
                    while q:
                        u = q.popleft(); cnt += 1
                        for v in adj[u]:
                            if not seen[v]:
                                seen[v] = True; q.append(v)
                    biggest = max(biggest, cnt)
                biggest_sum += biggest
                conn += 1 if biggest == n else 0
            print(f"{c:6.1f} | {p:8.4f} | {biggest_sum / trials / n:14.3f} | {conn / trials:.2f}")
        print('（p<1/n 只有小分量；p>1/n 出现巨分量；n 有限时连通在 c>~ln n 才饱和。）')


if __name__ == '__main__':
    self_test()
    experiment_select()
    experiment_threshold()
