"""trees.py —— P3 通用树（对应讲义 L16 树与分派；P3 官方评论树原型）。

设计：Tree(root, children)；children 用 L13 的链表存 —— 正是官方 P3 骨架
`Tree(root, children)` 且 CS61B 的 AList/DList 同源件。
自检：python -m py_compile trees.py
"""

from linked import LinkedNode, link


class Tree:
    """多叉树：根 + 子树链表。"""

    def __init__(self, root, children=None):
        self.root = root
        self.children = children      # LinkedNode of Tree 或 None

    # ---- 基础访问（构造/选择器契约，L10） ----
    def is_leaf(self):
        return self.children is None

    def child_count(self):
        n, cur = 0, self.children
        while cur is not None:
            n += 1
            cur = cur.rest
        return n

    # ---- 递归族谱（L07 树递归） ----
    def depth(self):
        if self.is_leaf():
            return 1
        best = 0
        cur = self.children
        while cur is not None:
            best = max(best, cur.first.depth())
            cur = cur.rest
        return 1 + best

    def size(self):
        """节点总数 Θ(n)。"""
        if self.is_leaf():
            return 1
        n, cur = 1, self.children
        while cur is not None:
            n += cur.first.size()
            cur = cur.rest
        return n

    def accumulate(self, fn, initial):
        """通用折叠（先序）：每个节点值依次流过 fn(value, acc)。P3 官方必做件。"""
        result = fn(self.root, initial)
        cur = self.children
        while cur is not None:
            result = cur.first.accumulate(fn, result)
            cur = cur.rest
        return result

    def map_tree(self, fn):
        """新树：对每个 root 施加 fn（结构共享不可行——递归重建）。"""
        if self.is_leaf():
            return Tree(fn(self.root))
        mapped = []
        cur = self.children
        while cur is not None:
            mapped.append(cur.first.map_tree(fn))
            cur = cur.rest
        return Tree(fn(self.root), link(mapped))

    # ---- 分派式遍历（L15 explicit dispatch） ----
    def __repr__(self):
        if self.is_leaf():
            return f'Tree({self.root!r})'
        kids = []
        cur = self.children
        while cur is not None:
            kids.append(repr(cur.first))
            cur = cur.rest
        return f'Tree({self.root!r}, Link({", ".join(kids)}))'

    def __eq__(self, other):
        if not isinstance(other, Tree):
            return NotImplemented
        if self.root != other.root:
            return False
        a, b = self.children, other.children
        while a is not None and b is not None:
            if a.first != b.first:
                return False
            a, b = a.rest, b.rest
        return a is None and b is None


def build(root, children):
    """嵌套元组 → Tree：build(1, [ (2,[]), (3,[ (4,[]) ]) ])"""
    node = Tree(root)
    if children:
        node.children = link([build(c, g) for c, g in children])
    return node


def _selftest():
    t = build(1, [(2, []), (3, [(4, [])])])
    assert t.depth() == 3
    assert t.size() == 4
    assert t.child_count() == 2
    assert repr(t) == 'Tree(1, Link(Tree(2), Tree(3, Link(Tree(4)))))'
    seen = []
    t.accumulate(lambda v, acc: (seen.append(v), acc)[1], None)
    assert seen == [1, 2, 3, 4]                      # 先序
    doubled = t.map_tree(lambda v: v * 2)
    assert doubled == build(2, [(4, []), (6, [(8, [])])])
    print('trees selftest OK')


if __name__ == '__main__':
    _selftest()
