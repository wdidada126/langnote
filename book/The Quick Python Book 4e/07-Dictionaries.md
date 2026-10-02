# 07 · Dictionaries

> 一句话定位：`dict` 键值映射——Python 里最高频的数据组织方式。
> 原书 pp. 英文 4e 第 7 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 7.1 | 字面量 | `{k: v}` |
| 7.2 | 访问 | `[]`/`get` |
| 7.3 | 方法 | keys/values/items |
| 7.4 | 合并 | `|`（3.9） |
| 7.5 | 推导 | `{k: v}` |

## 核心精讲

```
# 教学示意，不参与构建
d = {'a': 1, 'b': 2}
print(d.get('c', 0))              # 0
d |= {'c': 3}                     # 合并（3.9+）
inv = {v: k for k, v in d.items()}
```

- 键可哈希（字符串/数字/元组）；值任意。
- `get` 避免 KeyError；`setdefault`/`defaultdict` 处理缺失。
- 合并 `|`（PEP 584，3.9）。

## 版本演进

- dict 保序（PEP 520，3.7）；合并 `|`（PEP 584）。
- 标注 `dict[str, int]`（PEP 585）。
- `ChainMap`（3.3）组合多层配置。

## 经典论文与原始文献

- PEP 520 / PEP 584；Python `dict` 文档。
- Python 教程「Data Structures」。

## 近年研究与工业界开源实践（2015–2026）

- `TypedDict`（3.8）给字典加结构。
- `pydantic`/`dataclass` 替代手写字典建模。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 认为 dict 无序 | 3.7+ 保序 |
| `d['k']` 取可能缺失键 | 用 `get`/`defaultdict` |
| 🔧 4e 标 3.13 | 以官方为准 |

## 与其他章 / 其他书的联系

- 集合见[第05章](05-Lists, tuples, and sets.md)。
- 见 [`Effective Python（第2版）/00-总览与阅读地图.md`](../Effective Python（第2版）/00-总览与阅读地图.md) 字典条目。
