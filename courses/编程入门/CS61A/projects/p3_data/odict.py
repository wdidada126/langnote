"""odict.py —— P3 手写 OrderedDict（对应讲义 L16：字典均摊 O(1)+插入序）。

标准件：dict 做 O(1) 点查 + 手写**双向链表**做顺序维护（L13 链表复用）。
提供 move_to_end / popitem，最后用 LRU 缓存演示两者合体（P3 评论排序应用）。
自检：python -m py_compile odict.py
"""

_UNSET = object()


class _Node:
    __slots__ = ('key', 'value', 'prev', 'next')

    def __init__(self, key=_UNSET, value=_UNSET):
        self.key, self.value = key, value
        self.prev = self.next = None


class OrderedDict:
    """语义对齐 collections.OrderedDict 的核心子集。"""

    def __init__(self):
        self._map = {}                       # key -> _Node
        head, tail = _Node(), _Node()        # 哨兵，免判空
        head.next, tail.prev = tail, head
        self._head, self._tail = head, tail

    # ---- 链表原语（全部 Θ(1)） ----
    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _append(self, node):
        last = self._tail.prev
        last.next = node
        node.prev, node.next = last, self._tail
        self._tail.prev = node

    def __len__(self):
        return len(self._map)

    def __contains__(self, key):
        return key in self._map

    def __setitem__(self, key, value):
        if key in self._map:
            self._map[key].value = value     # 更新不动位置（与标准库一致）
            return
        node = _Node(key, value)
        self._map[key] = node
        self._append(node)

    def __getitem__(self, key):
        return self._map[key].value

    def get(self, key, default=None):
        node = self._map.get(key, None)
        return default if node is None else node.value

    def __delitem__(self, key):
        node = self._map.pop(key)
        self._unlink(node)

    def __iter__(self):
        cur = self._head.next
        while cur is not self._tail:
            yield cur.key
            cur = cur.next

    def keys(self):
        return list(self)

    def items(self):
        cur = self._head.next
        out = []
        while cur is not self._tail:
            out.append((cur.key, cur.value))
            cur = cur.next
        return out

    def move_to_end(self, key):
        node = self._map[key]
        self._unlink(node)
        self._append(node)

    def popitem(self, last=True):
        if not self._map:
            raise KeyError('OrderedDict is empty')
        node = self._tail.prev if last else self._head.next
        self._map.pop(node.key)
        self._unlink(node)
        return node.key, node.value

    def __repr__(self):
        body = ', '.join(f'({k!r}, {v!r})' for k, v in self.items())
        return f'OrderedDict([{body}])'


class LRUCache:
    """LRU = OrderedDict + move_to_end：3.12 前 lru_cache 的纯 Python 原理。"""

    def __init__(self, capacity):
        self.capacity = capacity
        self.store = OrderedDict()
        self.hits = self.misses = 0

    def get(self, key):
        if key not in self.store:
            self.misses += 1
            return None
        self.store.move_to_end(key)          # 最近使用 → 队尾
        self.hits += 1
        return self.store[key]

    def put(self, key, value):
        self.store[key] = value
        self.store.move_to_end(key)
        if len(self.store) > self.capacity:
            self.store.popitem(last=False)   # 淘汰最久未用（队首）

    def __repr__(self):
        return f'LRU(cap={self.capacity}, items={self.store.items()})'


def _selftest():
    d = OrderedDict()
    for k, v in [('b', 1), ('a', 2), ('c', 3)]:
        d[k] = v
    assert d.keys() == ['b', 'a', 'c']
    d['b'] = 99
    assert d.keys() == ['b', 'a', 'c']       # 更新不移位
    d.move_to_end('a')
    assert d.keys() == ['b', 'c', 'a']
    assert d.popitem() == ('a', 2)
    assert d.keys() == ['b', 'c']

    c = LRUCache(2)
    c.put('x', 1); c.put('y', 2)
    assert c.get('x') == 1                   # x 变最近
    c.put('z', 3)                            # 淘汰 y
    assert c.get('y') is None and c.get('x') == 1 and c.get('z') == 3
    assert c.misses == 1
    print('odict selftest OK')


if __name__ == '__main__':
    _selftest()
