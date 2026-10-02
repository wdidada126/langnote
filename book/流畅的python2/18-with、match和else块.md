# 第 18 章 with、match和else块（原书 pp.507–533）

> 一句话定位本章：三个「被低估」的语法糖——`with` 让资源清理自动化、`match` 让多分支解构优雅、`for/while/try` 的 `else` 让「没 break 才执行」语义显式。
> 基线：原书 Python 3.10；本目录按 3.12+ 校验。

## 本章地图

| 小节 | 内容 | 结论（一句话） |
| --- | --- | --- |
| 18.1 本章新增内容（p.508） | 第 2 版改动 | 本章是 `match`（PEP 634–636，3.10）落地后的重写 |
| 18.2 上下文管理器和 `with` 块（p.508） | `__enter__`/`__exit__` | `with` 保证退出时 `__exit__` 被调用（含异常） |
| 18.2.1 `contextlib` 实用工具（p.511） | `closing`/`suppress`/`redirect_*` | 标准库现成的上下文管理器 |
| 18.2.2 `@contextmanager`（p.512） | 用生成器写 CM | 一个 `yield` 把代码切成「进入后/退出前」两段 |
| 18.3 lis.py 中的模式匹配（p.516） | 用 `match` 解析 Scheme | 真实案例展示 `match` 的解构威力 |
| 18.3.8 使用 OR 模式（p.529） | `case x | y` | 多模式或、`as` 捕获、守卫 `if` |
| 18.4 `if` 之外的 `else` 块（p.530） | `for`/`while`/`try` 的 `else` | `else` = 「正常完成、未被 break/except」 |
| 18.5 本章小结（p.532） | 三个语法糖总结 | `with` 管资源、`match` 管分支、`else` 管「无异常/无中断」 |
| 18.6 延伸阅读（p.533） | `contextlib`、PEP 634 | 官方文档与模式匹配规范 |

## 核心精讲

### 18.2.2 `@contextmanager`：生成器写上下文管理器

```python
# 教学示意，不参与构建
from contextlib import contextmanager

@contextmanager
def tag(name):
    print(f"<{name}>")     # __enter__ 之前
    yield name             # as 收到的值
    print(f"</{name}>")    # __exit__ 之后（异常也会走到这）

with tag("div") as t:
    print(f"  inside {t}")
```

### 18.3 用 `match` 解构（3.10 起）

```python
# 教学示意，不参与构建 —— Python 3.10+
def handle(node):
    match node:
        case ("let", name, value):
            print(f"绑定 {name} = {value}")
        case ("if", cond, then, else_):
            print("条件分支")
        case ("quote", expr):
            print(f"原样返回 {expr}")
        case _:
            raise ValueError("未知语法")

handle(("let", "x", 10))
```

### 18.4 `for...else`：没 break 才执行

```python
# 教学示意，不参与构建
def find(seq, target):
    for item in seq:
        if item == target:
            print("找到")
            break
    else:
        print("遍历完也没找到")   # 仅在未 break 时执行
```

## 版本演进

- 🔴 **PEP 634/635/636 — Structural Pattern Matching（3.10）**：`match`/`case` 是本章第 2 版重写的头号理由，也是全书的现代语法基石。3.12+ 行为稳定；3.12 `PEP 701` 让 f-string 与 match 文本模式共存更顺。
- **PEP 654 — ExceptionGroup 与 `except*`（3.11）**：与 `try/else` 配合——多个异常聚合时 `except*` 按类型分别处理，影响本章「异常处理」的现代写法。
- **PEP 343 — `with` 语句（2.5）**：上下文管理器协议总源头，3.12+ 不变。
- 3.11 新增 `contextlib.chdir`（🔧 以官方文档为准）：切换工作目录的上下文管理器，是 `contextlib` 的现代补充。
- 3.10 `match` 的「序列模式」直接消费可迭代对象（见 [17-迭代器、生成器和经典协程.md](17-迭代器、生成器和经典协程.md)），二者天然联动。
- 🔧 关于 `match` 是否会支持「类型守卫式模式」（如 `case x: int`）的扩展，以官方 What's New 为准。

## 经典论文与原始文献

- PEP 343 — The "with" Statement（2.5）。https://peps.python.org/pep-0343/ 。规范文档，上下文管理器。
- PEP 634 — Structural Pattern Matching: Specification（3.10）。https://peps.python.org/pep-0634/ 。规范文档，`match` 规范。
- PEP 635 — Structural Pattern Matching: Motivation and Rationale（3.10）。https://peps.python.org/pep-0635/ 。规范文档，动机。
- PEP 636 — Structural Pattern Matching: Tutorial（3.10）。https://peps.python.org/pep-0636/ 。规范文档，教程。
- PEP 654 — Exception Groups and `except*` （3.11）。https://peps.python.org/pep-0654/ 。规范文档，异常组。
- PEP 701 — Formalizing f-string syntax（3.12）。https://peps.python.org/pep-0701/ 。规范文档，与 match 文本模式兼容。
- `contextlib` 模块文档。https://docs.python.org/3/library/contextlib.html 。官方文档。

## 近年研究与工业界开源实践（2015–2026）

- **`match` 在解析器/编译器中的采用**：Ruff、mypy 等用 `match` 处理 AST 节点，可读性显著优于 `if/isinstance` 链（非同行评审，工具源码）。
- **`@contextmanager` 在测试夹具（pytest `tmp_path`、`monkeypatch`）**：上下文管理器是测试资源管理的事实标准（非同行评审）。
- **`except*` 在并发错误聚合**：`asyncio.TaskGroup`（3.11）抛 `ExceptionGroup`，`except*` 按类型分别处理，见 [20-并发执行器.md](20-并发执行器.md)/[21-异步编程.md](21-异步编程.md)。
- **`contextlib.nullcontext` 在可选资源**：「可能为空」的上下文用 `nullcontext` 统一接口（非同行评审）。

## 常见误区与本书需修正之处

| 原书说法 / 习惯 | 问题 | 2026 正确写法 |
| --- | --- | --- |
| 用 `try/finally` 包所有资源 | 冗长易漏 | 用 `with` + 上下文管理器（或 `@contextmanager`） |
| `match` 当 `switch` 用 | `match` 是「解构+守卫」，不是简单分支 | 善用序列/映射/`class`/`as` 模式做结构匹配 |
| 忽略 `case _` | 漏匹配会静默 None | 显式 `case _` 兜底或抛错 |
| 误以为 `for...else` 的 else 是「if 的反面」 | `else` 绑的是「循环正常完成」 | 记：`for/while` 的 `else` = 未被 `break`；`try` 的 `else` = 未被 `except` |
| 多异常逐层 `except` | 并发下多个异常被吞 | 3.11+ 用 `except*` 处理 `ExceptionGroup`（PEP 654） |
| 🔧 `contextlib` 新成员 | 原书未列 `chdir` 等 | 以官方文档为准补 3.11+ 新增 CM |

## 与其他章 / 其他书的联系

- [17-迭代器、生成器和经典协程.md](17-迭代器、生成器和经典协程.md)：`match` 的序列模式直接消费可迭代对象。
- [21-异步编程.md](21-异步编程.md)：`async with` 异步上下文管理器；`TaskGroup` 的 `ExceptionGroup` 与 `except*`。
- [20-并发执行器.md](20-并发执行器.md)：并发错误聚合与 `except*`（PEP 654）。
- 跨书：对应 [Python基础教程_第3版_9787115474889/06-抽象.md](../Python基础教程_第3版_9787115474889/06-抽象.md)（`with` 章节），以及 [Python基础教程_第3版_9787115474889/05-条件、循环及其他语句.md](../Python基础教程_第3版_9787115474889/05-条件、循环及其他语句.md)（`match`/循环 `else`）。
