# 05 · Lists, tuples, and sets

> 一句话定位：三种序列/集合容器——可变列表、不可变元组、去重集合，选对容器。
> 原书 pp. 英文 4e 第 5 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 5.1 | list | 有序可变 |
| 5.2 | tuple | 有序不可变 |
| 5.3 | set/frozenset | 无序去重 |
| 5.4 | 推导式 | 生成式 |
| 5.5 | 选择 | 场景 |

## 核心精讲

```
# 教学示意，不参与构建
lst = [1, 2, 3]
t = (1, 2)                 # 不可变
s = {1, 2, 2, 3}           # {1, 2, 3}
squares = {x * x for x in range(5)}
print(lst[0], t[1], s)
```

- `list` 可变有序；`tuple` 不可变（作记录/字典键）。
- `set` 去重集合运算（并交差）；`frozenset` 不可变集合可作键。
- 推导式：`[...]`/`{...}` 列表/集合推导。

## 版本演进

- dict 保序（PEP 520，3.7）；`list`/`dict` 标注 `list[int]`（PEP 585）。
- `set` 合并 `|`（PEP 654 实际是 dict；set 合并 `|` 在 3.9）。
- `list`/`tuple`/`set` 泛型标注无需 `typing`。

## 经典论文与原始文献

- PEP 585 — 标准库泛型标注；Python 内建类型文档。
- Python 教程「Data Structures」。

## 近年研究与工业界开源实践（2015–2026）

- `more-itertools` 补充序列工具。
- 不可变数据用 `tuple`/`NamedTuple`/`dataclass(frozen=True)`。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 用 list 当去重 | 用 set |
| tuple 当「只读 list」 | 语义是记录（异构） |
| 推导式过复杂 | 超 2 层考虑循环 |
| 🔧 4e 标注 3.13 | 以官方为准 |

## 与其他章 / 其他书的联系

- 字典见[第07章 Dictionaries](07-Dictionaries.md)。
- 算法见 [`Python算法教程（第2版）/00-总览与阅读地图.md`](../Python算法教程（第2版）/00-总览与阅读地图.md)。
