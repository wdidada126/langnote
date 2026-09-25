"""p02 搜索树（L14-L16）：二叉搜索树 + 增广区间树。

BST：insert/search/delete/min/successor/中序；区间树：每结点存子树 max(high)，
查询所有与 [lo, hi] 重叠的区间，剪枝规则：子树 max < lo 则整侧跳过。
"""
import random


# ---------------- BST ----------------
class Node:
    __slots__ = ('key', 'val', 'left', 'right', 'parent')

    def __init__(self, key, val=None, parent=None):
        self.key = key; self.val = val
        self.left = None; self.right = None; self.parent = parent


class BST:
    def __init__(self):
        self.root = None
        self.size = 0

    def search(self, key):
        x = self.root
        while x is not None:
            if key == x.key:
                return x
            x = x.left if key < x.key else x.right
        return None

    def minimum(self, x=None):
        x = x if x is not None else self.root
        if x is None:
            return None
        while x.left is not None:
            x = x.left
        return x

    def successor(self, x):
        if x.right is not None:
            return self.minimum(x.right)
        y = x.parent
        while y is not None and x is y.right:
            x, y = y, y.parent
        return y

    def insert(self, key, val=None):
        parent = None
        x = self.root
        while x is not None:
            if key == x.key:
                x.val = val
                return x
            parent = x
            x = x.left if key < x.key else x.right
        node = Node(key, val, parent)
        if parent is None:
            self.root = node
        elif key < parent.key:
            parent.left = node
        else:
            parent.right = node
        self.size += 1
        return node

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def delete(self, z):
        if z.left is None:
            self._transplant(z, z.right)
        elif z.right is None:
            self._transplant(z, z.left)
        else:
            y = self.minimum(z.right)            # 后继至多一(右)子
            if y.parent is not z:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
        self.size -= 1

    def inorder(self):
        out = []
        stack, x = [], self.root
        while stack or x is not None:
            while x is not None:
                stack.append(x); x = x.left
            x = stack.pop()
            out.append(x)
            x = x.right
        return out

    def height(self):
        # 迭代版：升序插入会退化成 12800 深的链，递归会爆栈（L09 警告的工程版）
        best, stack = 0, [(self.root, 1)]
        while stack:
            x, d = stack.pop()
            if x is None:
                continue
            best = max(best, d)
            stack.append((x.left, d + 1))
            stack.append((x.right, d + 1))
        return best


# ---------------- 区间树（CLRS 14.1 增广） ----------------
class INode:
    __slots__ = ('iv', 'max', 'left', 'right')

    def __init__(self, iv):
        self.iv = iv; self.max = iv[1]
        self.left = None; self.right = None


class IntervalTree:
    def __init__(self):
        self.root = None

    def insert(self, lo, hi):
        self.root = self._ins(self.root, (lo, hi))

    def _ins(self, x, iv):
        if x is None:
            return INode(iv)
        if iv[0] < x.iv[0]:
            x.left = self._ins(x.left, iv)
        else:
            x.right = self._ins(x.right, iv)
        x.max = max(x.max, x.left.max if x.left else -1e18,
                            x.right.max if x.right else -1e18)
        return x

    def query_all(self, lo, hi):
        """返回所有与 [lo, hi] 重叠的区间。"""
        out = []
        self._q(self.root, lo, hi, out)
        return out

    def _q(self, x, lo, hi, out):
        if x is None or x.max < lo:               # 剪枝：整棵子树 hi' < lo
            return
        if x.iv[0] <= hi and lo <= x.iv[1]:       # 重叠判定
            out.append(x.iv)
        self._q(x.left, lo, hi, out)
        if x.iv[0] <= hi:                          # 右侧才可能继续重叠
            self._q(x.right, lo, hi, out)


# ---------------- 自测与实验 ----------------
def self_test():
    rnd = random.Random(123)
    for trial in range(50):
        t = BST()
        ref = {}
        keys = rnd.sample(range(-500, 500), rnd.randint(0, 80))
        for k in keys:
            t.insert(k, k * k); ref[k] = k * k
        for k in rnd.sample(keys, len(keys) // 3 + 1):     # 随机删除
            node = t.search(k)
            if node:
                t.delete(node)
            ref.pop(k, None)
        inorder_keys = [n.key for n in t.inorder()]
        assert inorder_keys == sorted(ref.keys()), 'inorder vs sorted'
        assert t.size == len(ref)
        for k in list(ref)[:20]:
            node = t.search(k)
            assert node is not None and node.val == ref[k]
            s = t.successor(node)
            nxt = [x for x in inorder_keys if x > k]
            assert (s.key if s else None) == (nxt[0] if nxt else None)
    print('BST 自测通过：50 轮随机插入/删除后中序=sorted、后继正确。')

    rnd = random.Random(7)
    for trial in range(60):
        it = IntervalTree()
        ivs = []
        for _ in range(rnd.randint(1, 50)):
            a = rnd.randint(0, 60); b = a + rnd.randint(0, 20)
            it.insert(a, b); ivs.append((a, b))
        for _ in range(20):
            lo = rnd.randint(0, 60); hi = lo + rnd.randint(0, 15)
            got = sorted(it.query_all(lo, hi))
            want = sorted(iv for iv in ivs if iv[0] <= hi and lo <= iv[1])
            assert got == want, (lo, hi, got, want)
    print('区间树自测通过：60 棵随机树 × 20 查询与暴力枚举一致。')


def experiment():
    rnd = random.Random(2024)
    print('== 插入序决定树高（L14 退化 vs 随机） ==')
    print(f"{'n':>8} | {'随机序树高':>10} | {'升序树高(退化=链)':>16}")
    for n in (200, 800, 3200, 12800):
        t = BST()
        for k in rnd.sample(range(n * 4), n):
            t.insert(k)
        tr = BST()
        for k in range(n):
            tr.insert(k)
        print(f"{n:8d} | {t.height():10d} | {tr.height():16d}   (log2 n ≈ {n.bit_length() - 1})")


if __name__ == '__main__':
    self_test()
    experiment()
