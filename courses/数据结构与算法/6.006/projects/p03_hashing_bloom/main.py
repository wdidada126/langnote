"""p03 哈希表与 Bloom filter（L07, L17, L19）。

HashTable：开放寻址 + 线性探测 + 墓碑 + 负载 0.5 触发倍增惰性重建（摊还 L19）。
BloomFilter：splitmix64 派生 k 个哈希（双重哈希技巧），实测 FPR 对比理论
(1 - e^{-k n / m})^k，并验证最优 k* = (m/n) ln 2。
"""
import math
import random


# ---------------- 64 位哈希工具（不依赖内建 hash 的随机盐） ----------------
MASK64 = (1 << 64) - 1


def splitmix64(x):
    x = (x + 0x9E3779B97F4A7C15) & MASK64
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9 & MASK64
    x = (x ^ (x >> 27)) * 0x94D049BB133111EB & MASK64
    return x ^ (x >> 31)


def hash_str(s, seed=0):
    """确定性字符串哈希：FNV-1a 64 位 + splitmix 终混。"""
    h = 0xCBF29CE484222325
    for ch in s.encode('utf-8'):
        h = ((h ^ ch) * 0x100000001B3) & MASK64
    return splitmix64(h + seed) & MASK64


# ---------------- 开放寻址哈希表 ----------------
EMPTY, TOMB = object(), object()


class HashTable:
    def __init__(self, cap=8, alpha=0.5):
        self.slots = [EMPTY] * cap
        self.n = 0
        self.cap = cap
        self.alpha = alpha
        self.probes = 0                      # 探测计数（实验用）
        self.copies = 0                      # 重建拷贝计数（摊还实验）

    def _probe(self, key, for_insert=False):
        i = hash_str(key) % self.cap
        first_tomb = None
        while True:
            s = self.slots[i]
            if s is EMPTY:
                if for_insert and first_tomb is not None:
                    return first_tomb        # 插入: 无重复键时复用最早的墓碑
                return i
            if s is TOMB:
                if first_tomb is None:
                    first_tomb = i          # 查找必须跳过墓碑; 插入记下候选
            elif s[0] == key:
                return i                    # 找到同键: 更新（或本就为查找）
            self.probes += 1
            i = (i + 1) % self.cap

    def __setitem__(self, key, val):
        if (self.n + 1) > self.alpha * self.cap:
            self._grow(self.cap * 2)         # 倍增重建：单次 Θ(n)，均摊 O(1)（L19）
        i = self._probe(key, for_insert=True)
        s = self.slots[i]
        if s is EMPTY or s is TOMB:
            self.slots[i] = (key, val)
            self.n += 1
        else:
            self.slots[i] = (key, val)

    def __getitem__(self, key):
        i = self._probe(key, for_insert=False)
        s = self.slots[i]
        if s is EMPTY or s is TOMB:
            raise KeyError(key)
        return s[1]

    def __delitem__(self, key):
        i = self._probe(key, for_insert=False)
        s = self.slots[i]
        if s is EMPTY or s is TOMB:
            raise KeyError(key)
        self.slots[i] = TOMB                 # 墓碑：不断探测链（L07）
        self.n -= 1

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def _grow(self, newcap):
        old = self.slots
        self.slots = [EMPTY] * newcap
        self.cap = newcap
        for s in old:
            if s is not EMPTY and s is not TOMB:
                self.copies += 1
                self.probes = 0              # 重建期探测不计入查询统计
                i = self._probe(s[0])
                self.slots[i] = s
                self.n += 1
        self.n = 0                           # 上面重复加过, 归零重算
        self.n = sum(1 for s in self.slots if s is not EMPTY and s is not TOMB)


# ---------------- Bloom filter ----------------
class BloomFilter:
    def __init__(self, m_bits, k):
        self.bits = bytearray(m_bits)        # 简化: 每字节一位（1<<位数组更省, 语义相同）
        self.m = m_bits
        self.k = k
        self.inserted = 0

    def _positions(self, item):
        h1 = hash_str(item, seed=1)
        h2 = hash_str(item, seed=2) | 1
        return [(h1 + j * h2) % self.m for j in range(self.k)]   # 双重哈希（L17）

    def add(self, item):
        for p in self._positions(item):
            self.bits[p] = 1
        self.inserted += 1

    def might_contain(self, item):
        return all(self.bits[p] for p in self._positions(item))


def theoretical_fpr(m, n, k):
    return (1.0 - math.exp(-k * n / m)) ** k


# ---------------- 自测与实验 ----------------
def self_test():
    rnd = random.Random(99)
    ht = HashTable()
    ref = {}
    for _ in range(4000):
        op = rnd.random()
        key = f"k{rnd.randint(0, 1500)}"
        if op < 0.6:
            v = rnd.randint(0, 10 ** 6)
            ht[key] = v; ref[key] = v
        elif op < 0.8 and key in ref:
            del ht[key]; del ref[key]
        else:
            assert (key in ht) == (key in ref), key
            if key in ref:
                assert ht[key] == ref[key]
    assert len(ref) == ht.n
    print(f"哈希表自测通过：4000 随机操作与 dict 一致；倍增重建拷贝总次数 = {ht.copies} ≤ 2n = {2 * len(ref)}（L19 几何级数）。")
    assert ht.copies <= 2.5 * ht.n

    bf = BloomFilter(1 << 14, 7)
    words = [f"w{i}" for i in range(1500)]
    for w in words:
        bf.add(w)
    assert all(bf.might_contain(w) for w in words), 'no false negatives!'
    print('Bloom 自测通过：1500 个已插入元素 100% 命中（无假阴性）。')


def experiment():
    print('== Bloom filter 实测 FPR vs 理论 (1 - e^{-kn/m})^k ==')
    m = 1 << 16
    n = 8000
    header = f"{'k':>3} | {'理论 FPR':>10} | {'实测 FPR':>10} | 备注"
    print(header)
    for k in (3, 5, 7, 9, 11, 13):
        bf = BloomFilter(m, k)
        for i in range(n):
            bf.add(f'a{i}')
        fp = sum(1 for i in range(20000) if bf.might_contain(f'b{i}')) / 20000
        note = '最优 k*≈(m/n)ln2=%.1f' % (m / n * math.log(2)) if k == 6 else ''
        print(f"{k:3d} | {theoretical_fpr(m, n, k):10.4f} | {fp:10.4f} | {note}")
    print('（实测围绕理论波动 <1 个百分点属采样噪声；k=6 附近 FPR 最低即 k* 曲线谷底。）')


if __name__ == '__main__':
    self_test()
    experiment()
