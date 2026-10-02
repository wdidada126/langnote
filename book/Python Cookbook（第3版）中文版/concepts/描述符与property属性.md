# 概念专篇：描述符与 property 属性

> 跨第 8 章（类与对象）8.6（可管理属性）、8.9（新属性）、8.13（类型约束）的专题。阅读地图见 [00-总览与阅读地图.md](../00-总览与阅读地图.md)。

## 本章地图
| 主题 | 内容 | 结论 |
|---|---|---|
| 描述符协议 | `__get__/__set__/__delete__` | 属性访问钩子 |
| `@property` | 只读/可写属性 | 最常用描述符 |
| 延迟属性 | `cached_property` | 3.8+ |
| 类型约束 | 描述符校验 | 校验库底层 |

## 核心精讲
- 描述符协议：定义 `__get__`/`__set__`/`__delete__` 任意一个的类实例，作为类属性时接管该属性的访问。
  - 数据描述符（有 `__set__`）优先于实例 `__dict__`；非数据描述符（仅 `__get__`，如 `property` 只读）次之。
- `@property`：`class C: @property def x(self): return self._x`；`@x.setter` 控写（8.6）。
- 延迟属性：`@functools.cached_property`（3.8）首次访问算一次并缓存（8.10 升级写法）。
- 类型约束：描述符在 `__set__` 里 `isinstance` 校验（8.13），是 pydantic/attrs 的底层机制。

```python
# 教学示意，不参与构建
import functools
class Quantity:
    def __set_name__(self, owner, name): self.name = name
    def __get__(self, obj, objtype=None): return obj.__dict__.get(self.name)
    def __set__(self, obj, value):
        if value < 0: raise ValueError("must be >= 0")
        obj.__dict__[self.name] = value

class Box:
    weight = Quantity()
    @functools.cached_property
    def volume(self): return self._compute()
```

## 版本演进
- **3.6 PEP 0487**：`__set_name__` 让描述符知道自身属性名（8.13 更简洁）。
- **3.8 `functools.cached_property`**：延迟属性进标准库（8.10 升级）。
- **3.7 PEP 0557 `@dataclass`**：`field(default_factory=...)` 与描述符互补做初始化。
- **3.9 PEP 0591 `@final`**：约束覆写，与描述符组合用。
- **3.12 PEP 0695**：类级类型参数简化泛型描述符。
- 🔧 现代数据校验直接用 `pydantic`/`attrs`，不必手写描述符。

## 经典论文与原始文献
- PEP 0252 类型与描述符；`property` 即内置数据描述符。
- PEP 0557 `dataclasses`（3.7）；PEP 0591 `@final`（3.9）；PEP 0695 类型参数（3.12）。
- 🔧 具体编号/年份以 https://peps.python.org/ 为准。

## 近年研究与工业界（2015–2026）
- `pydantic`/`attrs` 把描述符做成声明式校验，Web/配置层标配。
- `cached_property` 在 ORM/懒加载字段广泛使用。
- 描述符是 Django/SQLAlchemy 模型字段的基石。

## 常见误区与本书需修正之处
| 误区 | 修正 |
|---|---|
| 手写 `__init__` 校验 | 用 `pydantic`/描述符或 `dataclass` |
| 手写延迟属性 | 3.8+ `functools.cached_property` |
| 忘记 `__set_name__` | 3.6+ 用其自动获属性名 |
| `@property` 当计算字段滥用 | 重计算用 `cached_property` 缓存 |

## 与其他章 / 其他书的联系
- 类设计见 [../08-类与对象.md](../08-类与对象.md)；泛型见 [../07-函数.md](../07-函数.md)。
- 装饰器互补见 [装饰器与元类.md](装饰器与元类.md)。
- 对照 [../../Effective Python（第2版）/05-类与接口.md](../../Effective Python（第2版）/05-类与接口.md)。
