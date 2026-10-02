# 第 11 章 符合Python风格的对象（原书 pp.279–301）

> 一句话定位：本章以 `Vector2d` 为载体，讲「一个 Pythonic 的对象应该实现哪些特殊方法」——表示形式、备选构造、格式化、可哈希、位置模式匹配、私有属性、`__slots__`、类属性覆盖。
> 基线：原书 Python 3.10；本目录按 3.12+ 校验。

## 本章地图

| 小节 | 内容 | 结论 |
| --- | --- | --- |
| 11.1 本章新增内容 | 相对第 1 版的改动 | 新增 `__match_args__`、f-string 相关讨论 |
| 11.2 对象表示形式 | `__repr__` / `__str__` / `__bytes__` / `__format__` | `repr` 给开发者、`str` 给用户，二者目标不同 |
| 11.3 再谈向量类 | `Vector2d` 的属性与迭代 | 用 `property` 把内部存储与公开接口分离 |
| 11.4 备选构造函数 | `frombytes` 类方法 | 构造函数不止一个入口时，用类方法命名不同语义 |
| 11.5 `classmethod` 与 `staticmethod` | 两者的区别与误用 | `classmethod` 拿 `cls`，`staticmethod` 只是挂在类上的普通函数 |
| 11.6 格式化显示 | `__format__` 与格式规范微语言 | 自定义类型应支持 `format()` 与 f-string 的格式规范 |
| 11.7 可哈希的 `Vector2d` | `__hash__` + `__eq__` + 只读属性 | 定义 `__eq__` 而不定义 `__hash__`，对象会变不可哈希 |
| 11.8 支持位置模式匹配 | `__match_args__`（3.10） | 类实例可用位置模式解构 |
| 11.9 第 3 版完整代码 | `Vector2d` 汇总 | 本章的落点是一份可复用的模板 |
| 11.10 私有与「受保护」属性 | 名称改写 `__x` → `_Class__x` | 只是约定层面的私有，防误用不防攻击 |
| 11.11 `__slots__` 节省空间 | 内存收益与代价 | 数百万小对象时收益显著；代价是失去 `__dict__` 与灵活性 |
| 11.11.1 衡量节省的内存 | `sys.getsizeof` 对比 | 每实例可省几百字节（主要是 `__dict__`） |
| 11.11.2 总结 `__slots__` 的问题 | 继承、弱引用、pickle 等限制 | 不要为了「看起来专业」而加 `__slots__` |
| 11.12 覆盖类属性 | 实例属性遮蔽同名类属性 | `self.typecode = ...` 会遮蔽 `Vector2d.typecode` |

## 核心精讲

### 一、第 3 版 `Vector2d`（可直接复用的模板）

```python
# 教学示意，不参与构建；本机 Python 3.13 验证通过
from array import array
import math
from typing import Self

class Vector2d:
    __slots__ = ('__x', '__y')      # 配合 property，既省内存又保持只读
    typecode = 'd'
    __match_args__ = ('x', 'y')     # 3.10 起支持位置模式

    def __init__(self, x: float, y: float) -> None:
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))        # 有了它就能拆包、转元组

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.x!r}, {self.y!r})'

    def __str__(self) -> str:
        return str(tuple(self))

    def __bytes__(self) -> bytes:
        return bytes([ord(self.typecode)]) + bytes(array(self.typecode, self))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector2d):
            return (self.x, self.y) == (other.x, other.y)
        return NotImplemented                        # 交给解释器再试一次反射

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    def __bool__(self) -> bool:
        return bool(abs(self))

    def angle(self) -> float:
        return math.atan2(self.y, self.x)

    def __format__(self, fmt_spec: str = '') -> str:
        if fmt_spec.endswith('p'):                   # 自定义：极坐标 'p'
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer = '<{}, {}>'
        else:
            coords, outer = (self.x, self.y), '({}, {})'
        return outer.format(*(format(c, fmt_spec) for c in coords))

    @classmethod
    def frombytes(cls, octets: bytes) -> Self:       # PEP 673（3.11）
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)

v = Vector2d(3, 4)
print(repr(v), str(v), abs(v), bool(v))
print(format(v), format(v, '.2f'), format(v, '.3ep'))   # (3.0, 4.0) (3.00, 4.00) <5.000e+00, 9.273e-01>
print(bytes(v), Vector2d.frombytes(bytes(v)))
print(hash(Vector2d(3, 4)) == hash(v))                  # True
```

三条设计要点：
1. **`__repr__` 要像 `eval()` 能重建对象的源码**，`__str__` 才是给终端用户看的人话版本。
2. **`__eq__` 不认识的类型返回 `NotImplemented`**，而不是 `False`——否则某些比较会不对称。
3. **定义了 `__eq__` 就必须重新定义 `__hash__`**，否则 Python 3 会把 `__hash__` 置为 `None`，对象直接不可哈希。

### 二、位置模式匹配：`__match_args__`（3.10）

```python
# 教学示意，不参与构建；Python 3.13 验证通过
match v:
    case Vector2d(x=0, y=0):
        print('原点')
    case Vector2d(x, y):          # 位置模式，靠 __match_args__ = ('x', 'y') 生效
        print(f'坐标 {x}, {y}')
```

`__match_args__` 列出位置模式对应的属性名，解释器据此把 `case Vector2d(a, b)` 转成关键字模式。不声明它，类模式就只能写成 `case Vector2d(x=a, y=b)` 的关键字形式（数据类与 `NamedTuple` 由解释器自动支持位置模式）。

### 三、`classmethod` vs `staticmethod`

| 维度 | `classmethod` | `staticmethod` |
| --- | --- | --- |
| 首个参数 | `cls`（实际被调用的类，支持继承多态） | 无，就是普通函数 |
| 典型用途 | 备选构造（`frombytes`）、工厂、对类属性的操作 | 与类相关的工具函数，避免污染模块命名空间 |
| 2026 建议 | 优先使用 | 能用模块级函数就用模块级函数，`staticmethod` 常是多余的 |

`frombytes` 用 `cls(*memv)` 而不是 `Vector2d(*memv)`，子类才能正确构造自己——配合 `Self` 注解（PEP 673，3.11），静态检查器也知道返回的是「调用它的那个类」。

### 四、格式化：从 f-string 到 t-string

```python
# 教学示意，不参与构建；Python 3.13 验证通过
print(f'{v:.3ep}')                      # <5.000e+00, 9.273e-01>：f-string 走 __format__
print(f'{v!r} {v.x = }')                # 3.8 调试语法，'= ' 会同时打印表达式文本
name = 'world'
print(f'{"nested " + name}')            # 3.12（PEP 701）后 f-string 内引号可自由嵌套
```

`__format__` 收到的是格式规范微语言（format spec mini-language）里冒号后面的那一段；f-string 只是 `format()` 的语法糖。3.12 的 PEP 701 把 f-string 正式纳入文法，允许嵌套同型引号、多行表达式、注释与反斜杠。

**3.14 新增的模板字符串 t-string（PEP 750）** 提供第三种形态：`t"..."` 不直接生成 `str`，而是产出一个可检视的模板对象，便于在拼接前做转义/校验（HTML、SQL、日志结构化）。🔧 **t-string 的最终语法与 API 以官方文档为准**，本机 3.13 无法运行。

### 五、`__slots__` 与 `@dataclass(slots=True)`

```python
# 教学示意，不参与构建；Python 3.13 验证通过
import sys
from dataclasses import dataclass

class Plain:
    def __init__(self, x, y): self.x = x; self.y = y

class Slotted:
    __slots__ = ('x', 'y')
    def __init__(self, x, y): self.x = x; self.y = y

p, s = Plain(1, 2), Slotted(1, 2)
print('有 __dict__:', sys.getsizeof(p) + sys.getsizeof(p.__dict__))   # 344
print('有 __slots__:', sys.getsizeof(s))                              # 48

@dataclass(slots=True, frozen=True)     # 3.10 起支持 slots=True
class Point:
    x: float
    y: float

print(Point(1.0, 2.0), hasattr(Point(1.0, 2.0), '__dict__'))         # False
```

| 方案 | 何时用 | 代价 / 坑 |
| --- | --- | --- |
| 手写 `__slots__` | 需要精细控制、还要留弱引用或 `__dict__` | 子类必须重复声明；不能有与类属性同名的槽（`ValueError: 'x' in __slots__ conflicts with class variable`） |
| `@dataclass(slots=True)` | 数据类想顺手省内存（3.10+） | 该选项会**重新创建一个类**，作用于原类的装饰器与零参 `super()` 可能失效 |
| 不加 | 默认选择 | 每实例多一个 `__dict__`（约百字节级），动态属性可用 |

决策原则：**只有「实例数量极大 + 属性集固定」时才加 `__slots__`**；为微优化给每个类都加，会换来一堆难以排查的限制（不能加属性、不能弱引用、pickle 与多继承更麻烦）。

### 六、名称改写与「私有」的真相

```python
# 教学示意，不参与构建
print(v._Vector2d__x)      # 3.0：__x 被改写成 _Vector2d__x，仍可访问
```

以双下划线开头、且**最多一个**尾部下划线的标识符会被改写为 `_类名__标识符`。它的作用是避免子类意外覆盖父类的「内部」属性，而不是提供访问控制：任何代码都能通过改写后的名字访问。单下划线 `_name` 纯属约定（且 `from module import *` 不会导入）。

### 七、覆盖类属性

`self.typecode = 'f'` 会在实例 `__dict__` 里创建一个同名属性，从此**遮蔽**类属性 `Vector2d.typecode`——这是「实例属性查找顺序」的直接后果（第 22 章描述符会解释得更彻底）。若 `__slots__` 里声明了与类属性同名的名字，类定义阶段就会直接报错。

## 版本演进

| 版本 | 变化 | 影响 |
| --- | --- | --- |
| 3.10（基线） | `__match_args__`、`@dataclass(slots=True)`、`X \| Y`（PEP 604） | 原书 11.8 与 11.11 的两项新内容都来自 3.10 |
| 3.11 | **`Self`**（PEP 673）、`dataclass_transform`（PEP 681）、Faster CPython（属性访问更快） | `frombytes` 注解改用 `-> Self`；attrs/pydantic 的类也能被检查器当数据类 |
| 3.12 | **PEP 701 f-string 文法化**、PEP 695 类型参数语法、`@override`（PEP 698） | f-string 不再受引号/换行限制；泛型类写 `class Vector[T]` |
| 3.13 | free-threaded 实验构建（PEP 703）；新 REPL | 对象模型语义不变 |
| 3.14 | **PEP 750 模板字符串 t-string**；PEP 649 注解延迟求值 | 格式化出现第三种形态；🔧 语法与 API 以官方文档为准 |

## 经典论文与原始文献

> 均为**规范文档（PEP），非同行评审论文**。年份列按对应 Python 版本发布年标注。

| PEP | 标题 | 版本 / 年份 | 链接 |
| --- | --- | --- | --- |
| PEP 8 | Style Guide for Python Code（命名与私有约定） | 2001 | https://peps.python.org/pep-0008/ |
| PEP 526 | Syntax for Variable Annotations（类属性注解） | 3.6 / 2016 | https://peps.python.org/pep-0526/ |
| PEP 498 | Literal String Interpolation（f-string） | 3.6 / 2016 | https://peps.python.org/pep-0498/ |
| PEP 557 | Data Classes | 3.7 / 2018 | https://peps.python.org/pep-0557/ |
| PEP 604 | Allow Writing Union Types as X \| Y | 3.10 / 2021 | https://peps.python.org/pep-0604/ |
| PEP 634 | Structural Pattern Matching: Specification | 3.10 / 2021 | https://peps.python.org/pep-0634/ |
| PEP 636 | Structural Pattern Matching: Tutorial | 3.10 / 2021 | https://peps.python.org/pep-0636/ |
| PEP 673 | Self Type | 3.11 / 2022 | https://peps.python.org/pep-0673/ |
| PEP 681 | Data Class Transforms | 3.11 / 2022 | https://peps.python.org/pep-0681/ |
| PEP 695 | Type Parameter Syntax | 3.12 / 2023 | https://peps.python.org/pep-0695/ |
| PEP 701 | Syntactic Formalization of f-strings | 3.12 / 2023 | https://peps.python.org/pep-0701/ |
| PEP 649 | Deferred Evaluation of Annotations Using Descriptors | 3.14 / 2025 | https://peps.python.org/pep-0649/ |
| PEP 750 | Template Strings（t-string） | 3.14 / 2025 | https://peps.python.org/pep-0750/ |

## 近年研究与工业界开源实践（2015–2026）

| 主题 | 现状 | 实践建议 |
| --- | --- | --- |
| 值对象的写法 | `@dataclass(frozen=True, slots=True)` 已成为不可变小对象的默认配方 | 需要只读 + 省内存时优先数据类；需要特殊方法时再手写类 |
| 只读属性 | `property`（本章写法） vs `frozen=True` 数据类 | 前者可控、可加计算逻辑；后者声明式、自动 `__eq__`/`__hash__` |
| `__slots__` 的真实收益 | 3.11 之后实例 `__dict__` 仍有开销，但 Faster CPython 让属性访问本身更快 | 只有在 `tracemalloc`/`pympler` 量出确有收益时才加；🔧 精确测量工具以官方文档为准 |
| 结构化模式匹配 | 3.10 之后 `__match_args__` 被广泛用于 AST/协议解析类 | 数据类与 `NamedTuple` 默认就支持位置模式，手写类要显式声明 |
| 字符串插值安全 | t-string（PEP 750，3.14）的动机是把「插值」与「转义」解耦，对 HTML/SQL/日志注入场景意义最大 | 🔧 落地 API 以官方文档为准，生产环境暂缓采用 |
| 类型检查配套 | `Self`、`@override`（PEP 698）、`slots=True` 三者都已被 mypy/pyright 支持 | 备选构造 + 继承体系里同时用 `Self` 与 `@override` |

## 常见误区与本书需修正之处

| 原书说法 | 问题 | 2026 正确写法 |
| --- | --- | --- |
| 🔧 备选构造注解为 `-> 'Vector2d'` 或绑 `TypeVar` | 子类会退化成父类类型 | `-> Self`（PEP 673，3.11）；需兼容旧版本用 `typing_extensions.Self` |
| 定义 `__eq__` 后忘记 `__hash__` | 对象变不可哈希 | 同时实现；不可变才配可哈希 |
| `__eq__` 对不认识的类型返回 `False` | 破坏比较对称性 | 返回 `NotImplemented` |
| `__slots__` 是「好风格」标志 | 带来继承、弱引用、动态属性等一串限制 | 仅在海量小对象且属性固定时使用；数据类用 `slots=True` |
| `sys.getsizeof` 就是对象内存 | 不含 `__dict__` 与引用对象 | 加上 `__dict__`，或用 `tracemalloc`/`pympler`；🔧 工具细节以官方文档为准 |
| 🔧 3.14 后 t-string 的用法与 API | 本章写作时 3.14 尚未发布 | 🔧 以官方文档为准；本机 3.13 无法验证 |
| 双下划线属性是「私有」 | 名称改写只是防误用 | 视作内部约定，不要用改写名访问别人的对象 |
| `staticmethod` 是面向对象的必要组成 | 多数情况下模块级函数更清楚 | 只有「这个函数概念上属于这个类」时才用 |
| 类属性可被实例自由覆盖而不出问题 | 遮蔽后类属性不再生效，行为难查 | 需要每实例可配置时显式声明为实例属性，别与类属性同名（`__slots__` 下直接报错） |

## 与其他章 / 其他书的联系

- 前置：[01-Python数据模型.md](01-Python数据模型.md)（特殊方法的世界观）、[06-对象引用、可变性和垃圾回收.md](06-对象引用、可变性和垃圾回收.md)（`==` vs `is`、可变性）、[05-数据类构建器.md](05-数据类构建器.md)（`dataclass` 与其 `slots=True`）。
- 后继：[12-序列的特殊方法.md](12-序列的特殊方法.md) 把 `Vector2d` 扩成 `Vector`（N 维），是本章的直接续篇；[16-运算符重载.md](16-运算符重载.md) 给向量加上 `+`/`*`；[22-动态属性和特性.md](22-动态属性和特性.md) 深入 `property` 与属性查找；[23-属性描述符.md](23-属性描述符.md) 解释 `classmethod`/`staticmethod`/`property` 的共同底座。
- 类型侧：[08-函数中的类型提示.md](08-函数中的类型提示.md)（`Self`）、[13-接口、协议和抽象基类.md](13-接口、协议和抽象基类.md)（何时该用 ABC 而非鸭子类型）。
- 跨书对照：[基础教程 09-魔法方法、特性和迭代器](../Python基础教程_第3版_9787115474889/09-魔法方法、特性和迭代器.md) 讲 `__repr__` 等入门特殊方法，本章是其完整版；[基础教程 07-再谈抽象](../Python基础教程_第3版_9787115474889/07-再谈抽象.md) 对应 11.10 的私有属性讨论。
