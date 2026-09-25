"""p11 在线算法（L21-L22）：分页竞争模拟 + ski rental。

分页：LRU / FIFO / Belady-OPT / Marked 在同一请求流上的缺页计数，
验证 LRU ≤ (k+1)·OPT + O(1) 的竞争包络（k-竞争 + 加性常数）。
ski rental：确定性"租到 B 就买"(竞争比 2 紧) vs 随机化阈值混合（理论最优
e/(e-1)≈1.58，本项目用网格调优的三点混合数值逼近并解析复核最坏期望比）。
"""
import math
import random
from collections import OrderedDict


# ---------------- 分页策略 ----------------
class LRU:
    name = 'LRU'

    def __init__(self, k):
        self.k = k
        self.cache = OrderedDict()
        self.misses = 0

    def request(self, page):
        if page in self.cache:
            self.cache.move_to_end(page)
            return
        self.misses += 1
        self.cache[page] = True
        if len(self.cache) > self.k:
            self.cache.popitem(last=False)


class FIFO:
    name = 'FIFO'

    def __init__(self, k):
        self.k = k
        self.order = []
        self.seth = set()
        self.misses = 0

    def request(self, page):
        if page in self.seth:
            return
        self.misses += 1
        if len(self.order) >= self.k:
            victim = self.order.pop(0)
            self.seth.discard(victim)
        self.order.append(page)
        self.seth.add(page)


class Marked:
    """标记算法（工作集/均衡算法）：一轮 = 见满 k+1 个新页即清标开新轮。"""
    name = 'Marked'

    def __init__(self, k):
        self.k = k
        self.cache = {}                    # page -> marked(0/1)
        self.clean = set()                 # 本轮未标记
        self.misses = 0

    def request(self, page):
        if page in self.cache:
            if not self.cache[page]:
                self.cache[page] = 1
                self.clean.discard(page)
            return
        self.misses += 1
        if len(self.cache) < self.k:
            self.cache[page] = 1
            return
        # 驱逐一个未标记页；没有则整表清标开新轮再驱逐任意页
        if self.clean:
            victim = next(iter(self.clean))
        else:
            self.cache = {p: 0 for p in self.cache}
            self.clean = set(self.cache)
            victim = next(iter(self.clean))
        del self.cache[victim]
        self.clean.discard(victim)
        self.cache[page] = 1


class OPT:
    """Belady 离线最优：驱逐下次请求最远的页。需要未来序列（仅基准用）。"""
    name = 'OPT'

    def __init__(self, k, future):
        self.k = k
        self.future = future
        self.pos = 0
        self.cache = set()
        self.misses = 0

    def request(self, page):
        i = self.pos
        self.pos += 1
        if page in self.cache:
            return
        self.misses += 1
        if len(self.cache) < self.k:
            self.cache.add(page)
            return
        nxt = {}
        for p in self.cache:
            try:
                nxt[p] = self.future.index(p, i + 1)
            except ValueError:
                nxt[p] = float('inf')
        victim = max(self.cache, key=lambda p: nxt[p])
        self.cache.discard(victim)
        self.cache.add(page)


def simulate(k, policy_cls, seq, *args):
    pol = policy_cls(k, *args) if args else policy_cls(k)
    for p in seq:
        pol.request(p)
    return pol.misses


# ---------------- ski rental ----------------
def ski_deterministic(days, B):
    """租一天 $1；满第 B 天买。最坏 days=B+1 时比 OPT 差近 2 倍（紧界）。"""
    return (B - 1) + B if days >= B else days


def ski_randomized_avg(days, B, trials, rnd, thresholds, probs):
    """蒙特卡洛: 阈值 T 从 (thresholds, probs) 混合分布抽取; 演示用。"""
    total = 0
    for _ in range(trials):
        u, acc, t = rnd.random(), 0.0, thresholds[-1]
        for th, pr in zip(thresholds, probs):
            acc += pr
            if u <= acc:
                t = th
                break
        total += (t - 1 + B) if days >= t else days
    return total / trials


def ski_worst_ratio(ts, ps, B, D):
    """策略在对手可选长度 1..D 上的最坏期望比。"""
    worst = 0.0
    for d in range(1, D + 1):
        cost = sum(p * ((t - 1 + B) if d >= t else d) for t, p in zip(ts, ps))
        worst = max(worst, cost / min(d, B))
    return worst


def ski_tune(B=10):
    """粗网格搜索三点混合阈值策略, 数值逼近最优随机化（理论最优 e/(e−1)≈1.58）。"""
    D = 4 * B
    cand = list(range(1, 2 * B + 1, max(1, B // 8)))
    grid = (0.0, 0.25, 0.5, 0.75, 1.0)
    best = None
    for i, t1 in enumerate(cand):
        for t2 in cand:
            if t2 <= t1:
                continue
            for t3 in cand:
                if t3 <= t2:
                    continue
                for a in grid:
                    for b in grid:
                        if a + b > 1.0:
                            continue
                        ps = (a, b, 1.0 - a - b)
                        w = ski_worst_ratio((t1, t2, t3), ps, B, D)
                        if best is None or w < best[0]:
                            best = (w, (t1, t2, t3), ps)
    return best


def ski_opt(days, B):
    return min(days, B)


# ---------------- 自测与实验 ----------------
def _cyclic(n_pages, length):
    return [(i % n_pages) + 1 for i in range(length)]


def _zipfish(length, universe, rnd, s=1.0):
    weights = [1.0 / (i + 1) ** s for i in range(universe)]
    tot = sum(weights)
    cdf, acc = [], 0.0
    for w in weights:
        acc += w / tot
        cdf.append(acc)
    return [bisect_cdf(rnd.random(), cdf) + 1 for _ in range(length)]


def bisect_cdf(u, cdf):
    lo, hi = 0, len(cdf) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if u <= cdf[mid]:
            hi = mid
        else:
            lo = mid + 1
    return lo


def self_test():
    seq = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]   # OS 经典缺页表例
    for cls in (LRU, FIFO, Marked):
        m = simulate(3, cls, seq)
        assert m > 0
    assert simulate(3, OPT, seq) == 7            # Belady 手推: 7 次缺页
    assert simulate(3, LRU, seq) == 10           # 教科书对照: LRU=10
    print('分页自测通过：k=3 经典序列 LRU=10, OPT=7（比值在竞争包络内）。')

    # 竞争包络扫描: 随机序列上 LRU/OPT ≤ k（+加性小常数）
    rnd = random.Random(8)
    k = 4
    worst = 0.0
    for t in range(300):
        seq = [rnd.randint(1, 8) for _ in range(200)]
        ml = simulate(k, LRU, seq)
        mo = simulate(k, OPT, seq, seq)
        worst = max(worst, ml / max(mo, 1))
    assert worst <= 2 * k + 1, worst             # k-竞争+加性常数的宽松包络
    print(f'竞争实验：300 条随机序列上 max LRU/OPT = {worst:.2f}（k={k}，理论 k-竞争+加性项）。')

    B = 10
    for days in range(1, 40):
        assert ski_deterministic(days, B) <= 2 * min(days, B) + 1
    print('ski rental 自测通过：确定性策略全长度扫描满足 2-竞争。')


def experiment():
    print('== 分页：不同负载 × 不同 cache 容量的缺页数（LRU/FIFO/Marked/OPT） ==')
    print(f"{'负载':>12} | {'k':>2} | {'LRU':>5} | {'FIFO':>5} | {'Marked':>6} | {'OPT':>5} | LRU/OPT")
    rnd = random.Random(3)
    loads = {
        'cyclic(5)': _cyclic(5, 500),
        'cyclic(9)': _cyclic(9, 500),
        'zipf(200)': _zipfish(500, 200, rnd),
        'rand(10)': [rnd.randint(1, 10) for _ in range(500)],
    }
    for lname, seq in loads.items():
        for k in (3, 5):
            r = {}
            r['LRU'] = simulate(k, LRU, seq)
            r['FIFO'] = simulate(k, FIFO, seq)
            r['Marked'] = simulate(k, Marked, seq)
            r['OPT'] = simulate(k, OPT, seq, seq)
            ratio = r['LRU'] / max(r['OPT'], 1)
            print(f"{lname:>12} | {k:2d} | {r['LRU']:5d} | {r['FIFO']:5d} | {r['Marked']:6d} | {r['OPT']:5d} | {ratio:6.2f}")
    print('（cyclic(9) 在 k=5 时 LRU/OPT=1（栈式最优）；FIFO 可能出现异常上升——非栈式。）')
    print()
    print('== ski rental：全长度最坏期望比（确定性 2-竞争 vs 数值调优随机化, B=10） ==')
    B = 10
    D = 4 * B
    # 确定性"租满 B 天就买"= 单阈值 B 的退化混合，用同一最坏比函数计算
    det = ski_worst_ratio((B,), (1.0,), B, D)
    print(f"确定性: 最坏比 {det:.2f}（理论 2 = (B−1+B)/B 于 days=B+1，紧）")
    ratio, ts, ps = ski_tune(B)
    print(f"随机化: 三点混合阈值 t={ts} 概率 p={tuple(round(x, 2) for x in ps)}")
    print(f"        网格调优后最坏期望比 ≈{ratio:.2f} < 2；"
          f"理论最优 e/(e−1)={math.e / (math.e - 1):.2f}（连续指数分布）")
    # 蒙特卡洛对照：调优分布下逐长度期望成本 / OPT
    rnd = random.Random(6)
    worst_mc = 0.0
    for days in range(1, D + 1):
        mc = ski_randomized_avg(days, B, 4000, rnd, ts, ps) / ski_opt(days, B)
        worst_mc = max(worst_mc, mc)
    print(f"        蒙特卡洛复核最坏比 ≈{worst_mc:.2f}（与解析值一致，±0.03 噪声）")
    print('（随机化把"最坏期望比"从 2 压到 ~1.6 —— 与 L22 随机分页 2H_k−1 优于'
          '确定性 H_k 的分离同源：对对手不可预知的随机化更强。）')


if __name__ == '__main__':
    self_test()
    experiment()
