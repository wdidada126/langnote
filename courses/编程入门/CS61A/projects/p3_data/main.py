"""main.py —— P3 演示入口。运行：python main.py

自检：python -m py_compile linked.py trees.py odict.py minisql.py main.py
"""

import time

from linked import link, length, reverse, prepend
from trees import Tree, build
from odict import OrderedDict, LRUCache
import minisql


def demo_linked():
    print('== 链表（L13） ==')
    s = link([1, 2, 3])
    print('  link([1,2,3]) =', s, ' len =', length(s))
    print('  prepend 头插 Θ(1):', prepend(s, 0))
    print('  reverse      :', reverse(link([1, 2, 3, 4])))


def demo_tree():
    print('== 树（L16 / P3 评论树） ==')
    t = build('post', [
        ('c1 Ada: 顶', [('c1.1 Hacker: +1', [])]),
        ('c2 Nobody: 路过', []),
    ])
    print('  tree =', t)
    print('  depth =', t.depth(), ' size =', t.size())
    print('  先序评论:')
    t.accumulate(lambda v, acc: print('   ·', v), None)


def demo_odict():
    print('== OrderedDict / LRU（L16 组织策略） ==')
    d = OrderedDict()
    for w in 'hippopotamus':
        d[w] = d.get(w, 0) + 1
    print('  按首次出现序:', d.items())
    c = LRUCache(3)
    for i in range(8):
        c.put(i, i * i)
        c.get(i % 2)
    print('  LRU(3) 内容 :', c)
    print(f'  hits={c.hits} misses={c.misses}')


def demo_sql():
    print('== 迷你 SQL（L24 前哨） ==')
    c, u = minisql.comments_table(), minisql.users_table()
    print(c)
    hj = minisql.hash_join(c, u, 'user_id', 'id')
    print('  JOIN 后行数:', len(hj))
    print('  top_authors(likes>=10):', minisql.top_authors(10))

    # 复杂度实证：嵌套循环 vs 哈希连接（L08/L16）
    big_a = minisql.Table('a', ['k', 'v'], [{'k': i, 'v': i} for i in range(2000)])
    big_b = minisql.Table('b', ['k', 'w'], [{'k': i, 'w': -i} for i in range(2000)])
    t0 = time.perf_counter()
    n1 = len(minisql.nested_loop_join(
        big_a, big_b, lambda x, y: x['k'] == y['k']))
    t1 = time.perf_counter()
    n2 = len(minisql.hash_join(big_a, big_b, 'k', 'k'))
    t2 = time.perf_counter()
    assert n1 == n2
    print(f'  2000x2000 等值连接: nested={t1-t0:.3f}s  hash={t2-t1:.4f}s '
          f'（约 {(t1-t0)/max(t2-t1,1e-9):.0f} 倍差距）')


def main():
    demo_linked()
    demo_tree()
    demo_odict()
    demo_sql()


if __name__ == '__main__':
    main()
