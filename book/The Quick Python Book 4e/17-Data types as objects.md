# 17 · Data types as objects

> 一句话定位：一切皆对象——类型、可调用、可哈希、协议与 ABC。
> 原书 pp. 英文 4e 第 17 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 17.1 | 一切皆对象 | 类型即对象 |
| 17.2 | 可调用 | `__call__` |
| 17.3 | 可哈希 | `__hash__` |
| 17.4 | 协议 | 鸭子类型 |
| 17.5 | `ABC` | 抽象基类 |

## 核心精讲

```
# 教学示意，不参与构建
class Adder:
    def __call__(self, a, b):
        return a + b
add = Adder()
print(add(1, 2))                  # 对象可当函数
from collections.abc import Sized
print(isinstance([1, 2], Sized))  # True
```

- 类型是对象，可赋值/传递；`type(x)` 取类型。
- 特殊方法定义行为（`__call__` 可调用、`__hash__` 可哈希）。
- 鸭子类型：有方法即够，不必继承；`collections.abc` 提供正式协议。

## 版本演进

- `typing.Protocol`（PEP 544，3.8）结构化子类型。
- `typing.TypeAlias`（3.10）类型别名。
- `functools.singledispatch`（3.4）单分派泛型。

## 经典论文与原始文献

- PEP 544 — Protocols；Python `collections.abc` 文档。
- Python 数据模型（「Special method names」）。

## 近年研究与工业界开源实践（2015–2026）

- 静态鸭子类型用 `Protocol`；`abc` 定义接口。
- `functools.singledispatchmethod` 方法重载。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 必须继承才能「像某类」 | 鸭子类型/Protocol |
| 自定义对象默认不可哈希 | 定义 `__hash__`/`__eq__` |
| 🔧 4e 标 3.13 | 以官方为准 |

## 与其他章 / 其他书的联系

- 类见[第15章 Classes and OOP](15-Classes and object-oriented programming.md)。
- 类型见 [`Effective Python（第2版）/00-总览与阅读地图.md`](../Effective Python（第2版）/00-总览与阅读地图.md)。
