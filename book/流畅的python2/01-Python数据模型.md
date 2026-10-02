# 第 1 章 Python数据模型（原书 pp.3–15）

> 一句话定位本章：整本书的地基——用双下划线「特殊方法」让自己的对象融入语言本身。
> 基线：原书 Python 3.10；本目录按 3.12+ 校验。

## 本章地图

| 小节 | 内容 | 结论（一句话） |
| --- | --- | --- |
| 1.1 本章新增内容（p.4） | 第 2 版相对第 1 版的改动清单 | 本章新增 `f-string`、`match` 相关表述；数据模型本身几乎没变 |
| 1.2 一摞Python风格的纸牌（p.4） | `FrenchDeck`：只实现 `__len__` 与 `__getitem__` | 两个特殊方法换来 `len()`、索引、切片、迭代、`in`、`random.choice` 全套行为 |
| 1.3 特殊方法是如何使用的（p.7） | 特殊方法由**解释器隐式调用**，不由你直接调用 | `for i in x`、`x[i]`、`+` 等语法背后全是 `type(x).__xxx__` 的查找 |
| 1.3.1 模拟数值类型（p.8） | `Vector`：`__add__` / `__mul__` / `__abs__` / `__bool__` | 运算符重载就是实现对应特殊方法，返回值应是新对象 |
| 1.3.2 字符串表示形式（p.10） | `__repr__` 面向开发者、`__str__` 面向用户 | 二者都没定义时，`str()` 回退到 `__repr__` |
| 1.3.3 自定义类型的布尔值（p.11） | `__bool__` 优先、`__len__` 兜底 | 默认任何实例为真，这是 doctest 与真值判断出错的常见原因 |
| 1.3.4 容器API（p.12） | `__len__` / `__getitem__` / `__contains__` / `__iter__` | 容器协议是「部分实现也算实现」的典型鸭子类型 |
| 1.4 特殊方法概述（p.13） | 按类别罗列近百个特殊方法 | 现代补充：`__match_args__`（随模式匹配引入）也应进这张表 |
| 1.5 len为什么不是方法（p.14） | `len(x)` 不是 `x.len()` 的原因 | CPython 对内置类型直接读 `PyVarObject.ob_size` 字段，绕开属性查找 |
| 1.6 本章小结（p.14） | 「Pythonic 对象」= 利用数据模型 | 写类时先问：我要它支持哪些语法？再写对应特殊方法 |
| 1.7 延伸阅读（p.15） | 语言参考「Data model」章节 | 本章延伸的首读材料；细节以 docs.python.org 为准 |

## 核心精讲

### 1.2 一摞Python风格的纸牌：两个方法换来十种行为

```python
# 教学示意，不参与构建 —— 可在 Python 3.13 REPL 中直接粘贴
import collections
from random import choice

Card = collections.namedtuple('Card', 'rank suit')


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self) -> None:
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self) -> int:
        return len(self._cards)

    def __getitem__(self, position: int) -> Card:
        return self._cards[position]


deck = FrenchDeck()
print(len(deck), deck[0], deck[-1])
print(choice(deck))
print(deck[:3])
print(Card('Q', 'hearts') in deck)
```

关键不在代码量，而在**行为的来源**：`len()`、`deck[0]`、`deck[-1]`、负索引、切片、迭代、`in`、`random.choice(deck)`、
`reversed(deck)`、`sorted(deck, key=...)`——这些实现一行都没写，全部由 `__len__` + `__getitem__` 派生出来。
这就是「数据模型」的含义：**你的对象实现了协议的哪一部分，就能被对应语法使用**。

### 1.3 特殊方法总是由解释器隐式调用

`for i in x` 里 Python 实际做的是 `iter(x)` → `type(x).__iter__(x)`；`x[i]` 是 `type(x).__getitem__(x, i)`。
两个必须记住的细节：

1. **只在类型上查找，不在实例上查找**。给实例挂一个 `__len__` 属性不会生效。
2. `contains` 的实现有优先级：先看 `__contains__`，没有才退化到 `__iter__`，再退化到 `__getitem__` 老式迭代协议。

```python
# 教学示意，不参与构建
class Weird:
    pass


w = Weird()
w.__len__ = lambda: 42          # 挂在实例上：无效
print(w.__len__())              # 42 —— 当成普通属性访问当然没问题
try:
    print(len(w))               # TypeError: len() 只看 type(w)
except TypeError as exc:
    print('TypeError:', exc)


class OnlyGetItem:
    def __getitem__(self, i):
        return [10, 20, 30][i]


print(5 in OnlyGetItem(), 20 in OnlyGetItem())   # False True —— 靠 __getitem__ 兜底迭代
```

### 1.3.1–1.3.4 数值类型、表示形式、布尔值、容器API

```python
# 教学示意，不参与构建
from typing import Self          # PEP 673，3.11+
import math


class Vector:
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x, self.y = float(x), float(y)

    def __repr__(self) -> str:                 # 给开发者看：应像源码、无歧义
        return f'Vector({self.x!r}, {self.y!r})'

    def __str__(self) -> str:                  # 给用户看：可读即可
        return f'({self.x}, {self.y})'

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    def __bool__(self) -> bool:                # 没有它时，bool(obj) 用 __len__ 兜底
        return bool(abs(self))

    def __add__(self, other: 'Vector') -> Self:   # 返回新对象，不改动自身
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> Self:
        return Vector(self.x * scalar, self.y * scalar)

    def __len__(self) -> int:
        return 2

    def __iter__(self):
        yield from (self.x, self.y)            # Python 3.3+ 的 yield from（PEP 380）


v = Vector(3, 4)
print(repr(v), str(v), abs(v), bool(v), bool(Vector(0, 0)))
print(v + Vector(1, 1), v * 3, list(v))
```

四条经验：

- `__repr__` 的目标字符串最好能 `eval` 回同值对象；容器类的 `__repr__` 要对元素递归调用 `repr()`，所以一律用 `!r`。
- `__bool__` 与 `__len__` 的语义应当一致（`bool(v) == len(v) > 0`），否则会写出自我矛盾的类。
- 二元运算符返回**新对象**，不要就地修改 `self`；就地修改另有 `__iadd__`。
- 有了 `__iter__`，对象就同时满足可迭代协议，能被拆包、`list()`、`max()` 使用。

### 1.5 为什么 `len` 不是方法

原书 p.14 的解释在 2026 年依然成立，且仍是「Python 实用主义」的最佳例证：

- CPython 对 `list` / `str` / `bytearray` 等**内置类型执行捷径**：`len(x)` 直接读 `PyVarObject.ob_size` C 结构体字段，
  完全不做属性查找。这是最快速、最安全的实现选择，而非语言语义要求。
- 若把 `len` 设计成方法 `x.len()`，内置类型就必须伪造一个方法对象，白白付一次属性查找的成本。
- `abs(x)`、`bool(x)`、`str(x)`、`repr(x)` 同理：它们是**一元运算符**，用函数形式更统一，也让 `sorted(key=len)`、
  `map(len, ...)` 这种高阶用法自然可用。

```python
# 教学示意，不参与构建
print(type(len), len.__module__)       # <class 'builtin_function_or_method'>
lst = list(range(3))
print(lst.__len__())                   # 10 年前今天都能调用，但 len(lst) 才是正统写法
print(len(lst), len('你好'), len(b'ab'))
```

一句话总结：**特殊方法让你从「调用 API」变成「成为语言的一部分」；而 `len` 之所以是函数，是因为 Python 宁可把「求长度」当成一元运算符，也不愿为内置类型牺牲那一次字段读取的速度。**

## 版本演进

| 维度 | 原书基线（Python 3.10） | 3.11 / 3.12 | 3.13 / 3.14 | 对本章的影响 |
| --- | --- | --- | --- | --- |
| 特殊方法机制 | 解释器隐式调用、类型上查找 | 语义未变 | 语义未变 | 原书 1.3 节结论无需修正 |
| 运算符返回类型注解 | 只能写 `'Vector'` 或用 `TypeVar` 绑定 | 3.11 PEP 673 `Self`；3.12 PEP 695 `class Stack[T]` | 同左 | `__add__` 等可用 `-> Self`，不必再造 `TypeVar` |
| `__repr__` 中的 f-string | 受限于旧 f-string 词法 | 3.12 PEP 701 词法自由化 | 3.14 PEP 750 t-string 另行接管模板场景 | `__repr__` 里嵌复引号、反斜杠更自由 |
| 注解运行时取值 | 立即可取值 | 无变化 | 🔴 3.14 PEP 649 默认延迟求值 | 依赖 `__annotations__` 的元编程写法要改（详见 [第 24 章](24-类元编程.md)） |
| 模式匹配挂钩 | `__match_args__`（随 PEP 634 启用） | 稳定 | 稳定 | 原书 1.4 的方法总表缺此项，建议补上 |
| 对象生命周期 | 引用计数 + 分代回收 | 3.12 immortal objects（CPython 内部优化） | 3.13 free-threading 构建（PEP 703） | Python 层语义不变；写 C 扩展时要重新审查引用计数假设，见 [第 6 章](06-对象引用、可变性和垃圾回收.md) |

## 经典论文与原始文献

> 说明：以下均为 Python 增强提案（PEP）或官方规范文档，**属于规范文档而非同行评审学术论文**，无 DOI；年份为 PEP 创建年份。

| 编号 | 标题 | 年份 | 链接 | 与本章的关系 |
| --- | --- | --- | --- | --- |
| PEP 20 | The Zen of Python | 2004 | https://peps.python.org/pep-0020/ | 「We are all responsible users」「We are all consenting adults」解释了为什么 `__len__` 这类协议靠约定而非私有关键字约束 |
| PEP 8 | Style Guide for Python Code | 2001 | https://peps.python.org/pep-0008/ | 命名约定：双下划线方法是保留的，普通方法不要自造 `__xxx__` |
| PEP 673 | Self Type | 2021 | https://peps.python.org/pep-0673/ | 3.11 起 `__add__(self) -> Self` 是标准写法 |
| PEP 380 | Syntax for Delegating to a Subgenerator | 2009 | https://peps.python.org/pep-0380/ | `yield from` 让 `__iter__` 的委托写法变得可读 |
| PEP 634 / 635 / 636 | Structural Pattern Matching | 2020 | https://peps.python.org/pep-0634/ | 引入 `__match_args__`，补全本章 1.4 的特殊方法清单 |
| PEP 498 | Literal String Interpolation | 2015 | https://peps.python.org/pep-0498/ | `__repr__` / `__str__` 的现代表达方式 |
| PEP 695 | Type Parameter Syntax | 2022 | https://peps.python.org/pep-0695/ | 3.12 起泛型类不必再写 `Generic[T]`，影响本章类的定义头 |
| PEP 649 | Deferred Evaluation Of Annotations Using Descriptors | 2021 | https://peps.python.org/pep-0649/ | 3.14 起注解延迟求值，`__annotations__` 不再是普通 dict 访问语义 |
| 🔧 语言参考「Data model」 | Python Language Reference, §3 Data model | — | https://docs.python.org/3/reference/datamodel.html | 本章的权威口径，**非 PEP**，具体小节与标题以官方文档为准 |

## 近年研究与工业界开源实践（2015–2026）

| 实践 | 时间 | 内容 | 与本章的联系 | 性质 |
| --- | --- | --- | --- | --- |
| Faster CPython 项目 | 2021 起 | 针对常见字节码做特化与内联缓存 | `len()`、方法调用等 hot path 持续优化，但「内置类型走捷径」的结论不变 | 工业界项目文档，非同行评审；性能数字以官方 What's New 为准 🔧 |
| `attrs` | 2016 起 | 自动生成 `__repr__` / `__eq__` / 排序 / 冻结 | 把本章手写 boilerplate 变成 `@define` 一行 | 开源库，非同行评审；版本支持范围以官方发布说明为准 🔧 |
| `pydantic` v2 | 2023 起 | 校验 + 序列化的数据模型 | 它生成的 `__repr__` / `__str__` 与本章准则一致：开发者向 vs 用户向分离 | 同上 🔧 |
| 类型检查器生态 | 2016 起 | mypy / pyright 全面检查 `dataclasses` 与特殊方法签名 | `__add__` 用 `Self` 后 `mypy --strict` 才能推断链式调用的返回类型 | 工具文档 🔧 |
| CPython 对齐 ABIs（3.13+） | 2024 起 | 特殊方法 C 槽位的 ABI 稳定性讨论 | 只在写 C 扩展自定义协议时相关 | 🔧 以 CPython devguide 为准 |

## 常见误区与本书需修正之处

| 原书说法 | 问题 | 2026 年的正确写法 |
| --- | --- | --- |
| 1.3「不要直接调用特殊方法」 | 表述过于绝对 | 语义规则是「**用内置函数/语法调用**」（`len(x)`、`iter(x)`、`next(it)`），因为它们会分派到正确的槽位并处理兜底逻辑；但写 `__init__`、调 `super().__xxx__()`、测试里直接断言 `__repr__` 都是合法且常见的。准确说法是：**不要为了绕过 operator 语义而绕开槽位求值** |
| 1.3 未强调「只在类型上查找」 | 易被误解为实例属性也能覆盖魔术方法 | `obj.__len__ = ...` 对 `len(obj)` 无效；只有 `type(obj)` 上的定义才被解释器采纳 |
| 1.3.2 用 `namedtuple` 建 `Card` | 2026 年的默认选择已改变 | 优先 `typing.NamedTuple`（可注解、可加方法）或 `@dataclass(frozen=True, slots=True)`；`collections.namedtuple` 退化为「不需要类型信息的临时记录」，详见 [第 5 章](05-数据类构建器.md) |
| 1.3.1 运算符返回类型省略或用字符串 | `mypy --strict` 下推断不出链式类型 | 用 `def __add__(self, other: Self) -> Self`，`from typing import Self`（3.11+） |
| 1.4 特殊方法总表 | 缺模式匹配相关项 | 补 `__match_args__`（并留意 `__class_getitem__`，泛型自 PEP 695 后更常用） |
| 1.5 `len` 的解释 | 结论正确，但「CPython 实现细节」的边界要说清 | 「内置类型读 `ob_size`」是 CPython 的实现捷径；PyPy / GraalPy 等实现有自己的优化路径，语言层面只规定 `__len__` 必须返回非负 int。跨解释器不可假定捷径存在 |
| 🔧 1.4 涉及类注解的运行时读取 | 3.14 起 `__annotations__` 语义变化 | PEP 649 让注解延迟求值，不再默认解析为对象；需要具体行为时**以官方文档 What's New / `annotationlib` 为准**，不要用 `__annotations__['x'] is int` 做断言 |

## 与其他章 / 其他书的联系

- **进本书主线**：本章是 [第 11 章 符合Python风格的对象](11-符合Python风格的对象.md)（对象表示、可哈希、`__slots__`）与 [第 16 章 运算符重载](16-运算符重载.md) 的前置；
  想知道自己在 protocols 上做到什么程度，读 [第 13 章 接口、协议和抽象基类](13-接口、协议和抽象基类.md)。
- **回填本章的现代写法**：[第 5 章 数据类构建器](05-数据类构建器.md) 给出替代手写 `__init__`/`__repr__` 的方案；
  [第 6 章 对象引用、可变性和垃圾回收](06-对象引用、可变性和垃圾回收.md) 解释 `Vector` 里的 `+=` 为什么会得到「新对象」。
- **序列与映射**：[第 2 章 丰富的序列](02-丰富的序列.md)、[第 3 章 字典和集合](03-字典和集合.md) 是容器API（1.3.4）的规模化应用。
- **元视角**：特殊方法若想动态生成，见 [第 22 章 动态属性和特性](22-动态属性和特性.md)、[第 23 章 属性描述符](23-属性描述符.md)、[第 24 章 类元编程](24-类元编程.md)。
- **跨书对照**：[《Python基础教程（第3版）》09-魔法方法、特性和迭代器](../Python基础教程_第3版_9787115474889/09-魔法方法、特性和迭代器.md) 是本章的入门版；
  [01-快速上手：基础知识](../Python基础教程_第3版_9787115474889/01-快速上手：基础知识.md) 补 lists 的基础操作语义。
- **回到总览**：[00-总览与阅读地图.md](00-总览与阅读地图.md) 的「主线（对象模型）」把本章排在 01 位。

