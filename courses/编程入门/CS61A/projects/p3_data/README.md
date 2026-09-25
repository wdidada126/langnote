# P3 数据结构与 OOP：链表 / 树 / OrderedDict / 迷你 SQL

> 对应讲次：L13（可变数据与链表）、L14-L15（OOP/分派）、L16（树、字典、组织策略）、
> L18（排序）、L24（SQL 前哨）。官方 Project 3 Comments（社交网络：OOP+树+链表）的
> 知识点在这里全部以"手撕"形式重现（骨架从简，未做 okpy 网络层）。

## 内容

| 文件 | 说明 |
| --- | --- |
| `linked.py` | 单向链表 `LinkedNode` + 递归/迭代函数族（length/map/reverse 三指针）。P4 的 `Pair` 即其孪生。 |
| `trees.py` | `Tree(root, children链表)`：depth/size/accumulate(先序折叠)/map_tree/`__repr__`/`__eq__`——官方 P3 骨架件。 |
| `odict.py` | 手写 OrderedDict（dict+双链）与 LRU 缓存。 |
| `minisql.py` | 表 + select/project/order_by + **嵌套循环连接 vs 哈希连接**复杂度实证；users/comments 小样 + top_authors 聚合（GROUP BY 手写版）。 |
| `main.py` | 演示入口，四个 demo 串起 L13→L24。 |

## 运行

```bash
python main.py
python linked.py && python trees.py && python odict.py && python minisql.py  # 自检
```

`run.bat` / `run.sh`；语法自检：`python -m py_compile linked.py trees.py odict.py minisql.py main.py`

## 知识点对照

- L13：prepend Θ(1) vs `list.insert(0)` Θ(n)；`__eq__` 内容相等 vs `is` 身份；
- L14-15：dunder（`__repr__`/`__eq__`）协议；`accumulate` 是消息传递式分派；
- L16：同一份评论数据的三种组织（链/树/哈希索引）与查询模式匹配；
- L18：`order_by` 用 `sorted`（Timsort 稳定）；
- L24：σ/π/τ/⋈ 四算子手写 → 对照真 SQL 语句（minisql.py 顶部 docstring）。
