"""linked.py —— P3 单向链表（对应讲义 L13；直接复用为 P4 的 Pair）。

可变节点 + 递归函数族。所有操作自注复杂度（L08/L16 组织策略）。
自检：python -m py_compile linked.py
"""


class LinkedNode:
    """一个节点 = first(值) + rest(下一个节点或 None)。"""

    def __init__(self, first, rest=None):
        self.first = first
        self.rest = rest

    def __repr__(self):
        parts = []
        cur = self
        while cur is not None:
            parts.append(repr(cur.first))
            cur = cur.rest
        return 'Link(' + ', '.join(parts) + ')'

    def __eq__(self, other):
        a, b = self, other
        while a is not None and b is not None:
            if a.first != b.first:
                return False
            a, b = a.rest, b.rest
        return a is None and b is None


def link(values):
    """[1,2,3] -> LinkedNode 链。Θ(n)。"""
    head = cur = None
    for v in values:
        node = LinkedNode(v)
        if head is None:
            head = cur = node
        else:
            cur.rest = node
            cur = node
    return head


def prepend(head, value):
    """头部插入 Θ(1) —— 链表对 list.insert(0,x) Θ(n) 的胜利（L16）。"""
    return LinkedNode(value, head)


def length(s):
    return 0 if s is None else 1 + length(s.rest)          # Θ(n) 递归


def total(s):
    return 0 if s is None else s.first + total(s.rest)


def map_link(s, fn):
    """新链，元素逐一 fn。返回新表（不原地改）。"""
    if s is None:
        return None
    return LinkedNode(fn(s.first), map_link(s.rest, fn))


def reverse(s):
    """迭代三指针反转 Θ(n)（Lab07 重点：画图防断链）。"""
    prev, cur = None, s
    while cur is not None:
        nxt = cur.rest
        cur.rest = prev
        prev, cur = cur, nxt
    return prev


def _selftest():
    s = link([1, 2, 3])
    assert repr(s) == 'Link(1, 2, 3)'
    assert length(s) == 3 and total(s) == 6
    assert prepend(s, 0) == link([0, 1, 2, 3])
    assert reverse(link([1, 2, 3])) == link([3, 2, 1])
    assert map_link(s, lambda x: x * x) == link([1, 4, 9])
    print('linked selftest OK')


if __name__ == '__main__':
    _selftest()
