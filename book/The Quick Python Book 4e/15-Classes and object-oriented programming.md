# 15 · Classes and object-oriented programming

> 一句话定位：`class`、属性、继承、特殊方法——用对象建模领域。
> 原书 pp. 英文 4e 第 15 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 15.1 | `class`/`__init__` | 构造 |
| 15.2 | 方法/`self` | 实例方法 |
| 15.3 | 继承 | 复用 |
| 15.4 | 特殊方法 | `__repr__` 等 |
| 15.5 | `@dataclass` | 数据类 |
| 15.6 | 属性 | `@property` |

## 核心精讲

```
# 教学示意，不参与构建
from dataclasses import dataclass
@dataclass
class Point:
    x: int
    y: int
    def __add__(self, o: 'Point') -> 'Point':
        return Point(self.x + o.x, self.y + o.y)
print(Point(1, 2) + Point(3, 4))   # Point(x=4, y=6)
```

- `self` 是实例；`__init__` 初始化。
- 特殊方法（`__len__`/`__getitem__`）让对象像内建类型。
- `@dataclass`（PEP 557，3.7）自动生成样板；`@property` 控制属性访问。

## 版本演进

- `@dataclass`（PEP 557）；`slots=True`（3.10）省内存。
- `__init_subclass__`（PEP 487）钩子；`Protocol`（PEP 544，3.8）。

## 经典论文与原始文献

- PEP 557 / PEP 487 / PEP 544；Python 类文档。
- Python 教程「Classes」。

## 近年研究与工业界开源实践（2015–2026）

- `pydantic` 做校验数据类；`attrs` 替代手写。
- 组合优于继承（设计原则）。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 手写 `__init__` 样板 | 用 `@dataclass` |
| 滥用继承 | 优先组合/`Protocol` |
| 🔧 4e 标 3.13 | 以官方为准 |

## 与其他章 / 其他书的联系

- 作用域见[第10章](10-Modules and scoping rules.md)与[concepts/作用域与LEGB.md](concepts/作用域与LEGB.md)。
- OOP 深讲见 [`Python学习手册（第5版）/00-总览与阅读地图.md`](../Python学习手册（第5版）/00-总览与阅读地图.md)。
