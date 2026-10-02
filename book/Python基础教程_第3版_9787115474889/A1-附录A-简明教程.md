# 附录A 简明教程（原书 pp.440-446）

> 一句话定位本附录：用**十页**把 Python 的语法骨架、内置类型、控制流、函数、类、模块与异常讲完——给有其他语言经验者的速成入口；本目录的角色是给它补一份「原书条目 → 2026 现状」的对照表。
> 基线：原书 Python 3.5；本目录按 3.12+ 校验。
> 对应英文章名：Appendix A: The Short Version

## 本章地图

| 主题（按原书行文顺序） | 内容 | 结论 |
| --- | --- | --- |
| 语法骨架 | 缩进即块、注释 `#`、一行一句、行继续 `\` 与括号 | Python 用**缩进**代替大括号，这是唯一需要重新适应的地方 |
| 变量与内置类型 | 动态类型、`int/float/str/bytes/bool/None`、容器 `list/tuple/dict/set` | 一切皆对象；名字是「标签」不是「盒子」 |
| 表达式与运算符 | 算术、比较、逻辑、成员 `in`、身份 `is`、切片 | 🔴 除法 `/` 返回浮点、`//` 才是整除 |
| 语句 | `if/elif/else`、`while`、`for ... in`、`break/continue`、`pass` | 只有这几种控制流，没有 `switch`（3.10 起有 `match`） |
| 函数 | `def`、默认参数、关键字参数、`*args/**kwargs`、`return` | 函数是一等对象，可赋值、可传参、可返回 |
| 类与对象 | `class`、`self`、`__init__`、继承、属性 | 一切属性默认公开，「私有」靠约定 |
| 模块与包 | `import` / `from ... import`、`__name__ == "__main__"` | 一个文件就是一个模块，一个目录就是一个包 |
| 文件与异常 | `open()` + `with`、`try/except/finally`、`raise` | `with` 保证关闭；异常是正常控制流的一部分 |
| 接着学什么 | 标准库、测试、打包、类型提示 | 原书十页之外的东西才是 Python 生态的大头 |

## 核心精讲

> 以下代码均为**教学示意，不参与构建**：本附录用一个自足脚本覆盖原书十页的核心条目。

### 一份「十页速成」的现代版脚本

```python
# short_version_demo.py —— 教学示意，不参与构建（纯标准库，Python 3.12+）
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

# —— 变量与容器 ——
nums: list[int] = [1, 2, 3, 4, 5]
squares = [n * n for n in nums if n % 2]            # 列表推导 + 过滤
name, *rest = nums                                   # 星号解包：多余元素收进 rest
point = (10, 20)                                     # 元组：不可变，常作多返回值
lookup = {"a": 1} | {"b": 2}                         # dict 合并运算符（3.9+）
unique = {1, 2, 2, 3}                                # set：去重

# —— 函数：默认参数、仅位置参数（3.8+）、类型注解（PEP 484） ——
def greet(who: str, /, *, punctuation: str = "!") -> str:
    """who 只能按位置传，punctuation 只能按关键字传。"""
    return f"你好，{who}{punctuation}"

def total(*values: float, offset: float = 0.0) -> float:
    return sum(values) + offset

# —— 类：dataclass（3.7+）省掉样板代码 ——
@dataclass(slots=True)                               # slots=True 需 3.10+
class Point:
    x: float = 0.0
    y: float = 0.0

    def norm(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

# —— 控制流：结构模式匹配（3.10+）替代多分支 if ——
def classify(value: int | str) -> str:               # X | Y 联合类型（3.10+）
    match value:
        case int() if value < 0:
            return "负整数"
        case int():
            return "整数"
        case str() if value.isdigit():
            return "数字字符串"
        case _:
            return "其他"

# —— 泛型函数：类型参数语法（3.12+） ——
def first[T](items: list[T]) -> T:
    return items[0]

def parse_int(text: str) -> int:
    try:
        return int(text)
    except ValueError as exc:
        raise RuntimeError(f"解析失败：{text!r}") from exc   # 异常链，保留原始原因

def main() -> None:
    # f-string 调试语法（3.8+）：变量名与值一起打印
    print(f"{squares=} {lookup=} {unique=}")
    print(greet("世界"), total(1, 2, 3, offset=10))
    print(classify(-3), classify("42"), Point(3, 4).norm(), first(nums))

    # —— 文件与 with：自动关闭，异常也安全 ——
    out = Path("demo.json")
    out.write_text(json.dumps({"nums": nums}, ensure_ascii=False), encoding="utf-8")
    data = json.loads(out.read_text(encoding="utf-8"))
    print("读回：", data["nums"])

    # —— 异常：try/except/finally 与 raise ... from ——
    try:
        parse_int("abc")
    except RuntimeError as exc:
        print("捕获：", exc, "| 原始原因：", type(exc.__cause__).__name__)
    finally:
        out.unlink(missing_ok=True)                   # missing_ok 需 3.8+

if __name__ == "__main__":
    main()
```

### 语法骨架速查（原书十页的骨架部分）

| 条目 | 写法 | 备注 |
| --- | --- | --- |
| 缩进 | 4 空格，同缩进即同块 | 不要混用 Tab |
| 注释 | `#` 单行；文档字符串用三引号 | 文档字符串可用 `help()` 查看 |
| 续行 | 括号内的换行天然续行；否则用 `\` | 优先用括号 |
| 真假 | 假值：`False/None/0/"" /[]/()/{}/set()` | 自定义对象可定义 `__bool__` |
| 身份 vs 相等 | `is` 比身份，`==` 比值 | 小整数缓存会让 `is` 偶尔「看起来对」，别依赖 |
| 除法 | `/` 浮点，`//` 整除，`%` 取余 | 🔴 与 C/Java 直觉不同 |
| 字符串 | 不可变；`+` 拼接、`join` 高效、f-string 最可读 | 3.12 起 f-string 内可复用引号 |

### 从原书十页到 2026 年：必须补的三件事

| 缺口 | 为什么必须补 | 去哪看 |
| --- | --- | --- |
| 类型提示 | 原书基本不讲；现代 Python 代码的注解已成常态 | PEP 484 / mypy / pyright |
| 项目结构与打包 | 十页只讲单文件 | PEP 517/518、`pyproject.toml`、`uv` |
| 测试与工具链 | 十页没有测试 | `pytest`、`ruff`；本书第 16 章 |

## 版本演进

| 版本 | 与本附录相关的变化 |
| --- | --- |
| 3.5（原书基线） | `print`/`exec` 均为函数；`/` 为真除法；`async/await` 刚落地 |
| 3.6 | 🔴 f-string（PEP 498），字符串格式化进入新时代；变量注解 |
| 3.7 | 🔴 `dataclasses`（PEP 557）；`breakpoint()`；dict 保序进入语言规范 |
| 3.8 | 🔴 海象运算符（PEP 572）；仅位置参数 `/`；f-string `=` 调试语法 |
| 3.9 | dict 合并 `|`；内置泛型 `list[int]`；`str.removeprefix/removesuffix` |
| 3.10 | 🔴 `match`（PEP 634/635/636）；`X \| Y`（PEP 604）；`dataclass(slots=True)` |
| 3.11 | `ExceptionGroup` / `except*`（PEP 654）；`tomllib`（PEP 680）；`Self` |
| 3.12 | 🔴 类型参数语法 `def f[T]()`（PEP 695）；f-string 语法自由化 |
| 3.13 | 死电池移除（PEP 594）；新 REPL；free-threaded 构建（PEP 703） |
| 3.14 | 🔧 模板字符串 t-string、注解延迟求值；以官方 What's New 为准 |

## 经典论文与原始文献

> 以下均为**规范文档，非同行评审论文**。

| 编号 | 标题 | 年份 | URL |
| --- | --- | --- | --- |
| PEP 8 | Style Guide for Python Code | 2001 | https://peps.python.org/pep-0008/ |
| PEP 484 | Type Hints | 2014 提出，3.5 落地 | https://peps.python.org/pep-0484/ |
| PEP 498 | Literal String Interpolation（f-string） | 2016（3.6 落地） | https://peps.python.org/pep-0498/ |
| PEP 557 | Data Classes | 2017（3.7 落地） | https://peps.python.org/pep-0557/ |
| PEP 572 | Assignment Expressions | 2018（3.8 落地） | https://peps.python.org/pep-0572/ |
| PEP 634 | Structural Pattern Matching: Specification | 2020（3.10 落地） | https://peps.python.org/pep-0634/ |
| PEP 695 | Type Parameter Syntax | 2023（3.12 落地） | https://peps.python.org/pep-0695/ |
| PEP 517 / 518 | 构建系统与 `pyproject.toml` | 2015 / 2016 | https://peps.python.org/pep-0517/ ｜ https://peps.python.org/pep-0518/ |

## 近年研究与工业界开源实践（2015–2026）

- **类型检查进入日常**：mypy / pyright 与 IDE 补全，让「注解」从可选变成团队默认；PEP 484 之后的 PEP 526、604、695 逐步把类型语法写进语言本体。
- **工具链收敛**：`ruff` 一个二进制同时做 lint 与 format，取代原书时代的 PyChecker/PyLint 组合；`uv` 把虚拟环境与依赖解析合成一步。
- **REPL 体验升级**：3.13 的新 REPL 带语法高亮与多行编辑，速成学习者的第一站体验明显改善（🔧 细节以官方 What's New 为准）。
- **在线学习材料**：官方 Tutorial 与 Language Reference 始终是权威口径；凡速成材料与官方文档冲突，以官方文档为准。
- 🔧 各工具版本号以官方文档为准，本目录不锁定。

## 常见误区与本书需修正之处（原书条目 → 2026 现状）

| # | 原书条目 / 常见误区 | 现状（🔧 = 需以官方文档为准） |
| --- | --- | --- |
| 1 | `print` 是语句（Python 2 遗留印象） | 原书已正确：**Python 3 起 `print` 是函数**；`sep`/`end`/`file`/`flush` 四个关键字参数常用 |
| 2 | `exec` 是语句 | 原书已正确：Python 3 起 `exec` 是函数；🔧 仍应避免执行动态代码 |
| 3 | `3 / 2 == 1`（C/Java 直觉） | 原书已正确：`/` 返回 `1.5`，整除用 `//`，余数用 `%` |
| 4 | 🔧 字符串格式化只讲 `format` / `%` | 2026 年首选 **f-string**（PEP 498）；3.8 起有 `=` 调试语法，3.12 起引号可复用；3.14 有 t-string 🔧 |
| 5 | 🔧 无 `switch` | 3.10 起有 `match`（PEP 634/635/636），能匹配结构而不只是值 |
| 6 | 🔧 类要手写 `__init__` / `__repr__` | 3.7 起 `dataclasses`（PEP 557）代劳；3.10 起支持 `slots=True` |
| 7 | 🔧 联合类型写 `Union[int, str]` | 3.10 起可直接 `int \| str`（PEP 604）；`Optional[X]` → `X \| None` |
| 8 | 🔧 泛型要 `TypeVar` 样板代码 | 3.12 起 `def first[T](...)`（PEP 695） |
| 9 | 🔧 没有「一行判断并赋值」的写法 | 3.8 起海象 `if (n := len(x)) > 10:`（PEP 572） |
| 10 | 🔧 异常只有一个 | 3.11 起 `ExceptionGroup` + `except*`（PEP 654）处理并发的多异常 |
| 11 | 🔧 配置用 `.ini` 或手写解析 | 3.11 起标准库有 `tomllib`（PEP 680）读 TOML |
| 12 | 🔧 十页速成 = 学会 Python | 缺类型系统、打包、测试、并发、安全五块；务必续读第 16–19 章 |

## 与其他章 / 其他书的联系

- 本书：本附录是 **[00-总览与阅读地图.md](00-总览与阅读地图.md)** 里「速查路径」的入口；逐条展开见 [01-快速上手：基础知识.md](01-快速上手：基础知识.md) 到 [09-魔法方法、特性和迭代器.md](09-魔法方法、特性和迭代器.md)；速查表见 [A2-附录B-Python参考手册.md](A2-附录B-Python参考手册.md)。
- 工程部分：类型与打包的补强对应 [18-程序打包.md](18-程序打包.md)、[16-测试基础.md](16-测试基础.md)。
- 他书：类型系统深入可读《流畅的Python》与《Effective Python》（本仓库暂无笔记 🔧）；权威口径始终是官方 Tutorial / Language Reference。
- 回到总览：[00-总览与阅读地图.md](00-总览与阅读地图.md)
