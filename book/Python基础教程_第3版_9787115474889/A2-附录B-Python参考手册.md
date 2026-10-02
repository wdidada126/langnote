# 附录B Python参考手册（原书 pp.447-458）

> 一句话定位本附录：把 Python 的**表达式、内置函数、语句**做成三张速查表——它不是教程而是「忘了就翻」的手册；本目录在保留这三张表的同时，补一列「3.12–3.14 现状」。
> 基线：原书 Python 3.5；本目录按 3.12+ 校验。
> 对应英文章名：Appendix B: Python Reference

## 本章地图

| 主题（按原书结构） | 内容 | 结论 |
| --- | --- | --- |
| 表达式 | 字面量、运算符与优先级、容器构造、推导式、`lambda`、条件表达式 | 表达式**求值**出一个对象；理解优先级可少写很多括号 |
| 内置函数 | 约 70 个无需导入即可用的函数 | 内置函数是「Python 方言」的核心词汇量 |
| 语句 | 赋值、控制流、异常、`with`、函数/类定义、`import`、`yield`、`async`、`match` | 语句**执行**一个动作，不产生值 |
| 版本变化 | 哪些条目在 3.6–3.14 变了 | 手册类内容最怕「版本漂移」，必须定期对照官方文档 |

## 核心精讲

> 以下代码均为**教学示意，不参与构建**：本附录用一个自足脚本验证表中最容易记错的语义。

### 一、表达式：运算符优先级（从高到低，原书同序）

| 级别 | 运算符 | 说明 |
| --- | --- | --- |
| 最高 | `**` | 幂，**右结合**（`2**3**2 == 512`） |
| | `+x` `-x` `~x` | 一元正负与按位取反 |
| | `*` `/` `//` `%` `@` | `@` 为矩阵乘（3.5+） |
| | `+` `-` | 二元加减 |
| | `<<` `>>` | 位移 |
| | `&` `^` `\|` | 按位与/异或/或 |
| | `in` `not in` `is` `is not` `<` `<=` `>` `>=` `!=` `==` | 比较与成员/身份，**可链式**（`1 < x < 10`） |
| | `not x` | 逻辑非 |
| | `and` | 🔴 返回**操作数**而非布尔值，且短路 |
| | `or` | 同上 |
| 最低 | `if ... else ...`（条件表达式）、`lambda` | 三元表达式 `x if cond else y` |

### 二、内置函数速查（按用途分组，🔧 为版本提示）

| 分组 | 函数 |
| --- | --- |
| 类型构造与转换 | `bool` `int` `float` `complex` `str` `bytes` `bytearray` `list` `tuple` `dict` `set` `frozenset` `object` `type` |
| 数学与数值 | `abs` `round`（银行家舍入）`pow` `divmod` `min` `max` `sum` `bin` `oct` `hex` `hash` |
| 迭代与序列 | `len` `range` `enumerate` `zip`（3.10+ `strict=`）`iter` `next` `reversed` `sorted` `filter` `map` `all` `any` `slice` |
| 属性与反射 | `getattr` `setattr` `delattr` `hasattr` `dir` `vars` `locals` `globals` `id` `isinstance` `issubclass` `callable` |
| 输入输出 | `print`（`sep`/`end`/`file`/`flush`）`input` `open` `repr` `ascii` `format` |
| 代码与执行 | `eval` `exec` `compile` `__import__` |
| 装饰与元编程 | `property` `classmethod` `staticmethod` `super` `help` |
| 异步 | `aiter` `anext`（🔧 3.10+） |
| 调试 | `breakpoint`（🔧 3.7+） |

### 三、语句速查

| 语句 | 形式 | 备注 |
| --- | --- | --- |
| 赋值 | `a = b`；`a, b = b, a`；`a = b = 0`；`a += 1` | 多重赋值与交换不需要临时变量 |
| 星号解包 | `first, *rest = seq` | 左右两侧都可用 `*` |
| 增强赋值 | `+=` `-=` `*=` `/=` `//=` `%=` `**=` `\|=` `&=` `^=` `>>=` `<<=` `@=` | 对 list 而言 `+=` 与 `+` 语义不同（原地扩展） |
| `del` | `del x` / `del d[k]` / `del a[i:j]` | 删除的是**名字绑定**或容器项 |
| `if` | `if / elif / else` | 无括号，靠缩进 |
| `while` / `for` | 均可带 `else`（未被 `break` 时执行） | `else` 子句是最常被误解的一条 |
| 跳转 | `break` `continue` `pass` | `pass` 是空操作占位 |
| `match` | `match x: case ...:` | 🔧 3.10+（PEP 634/635/636） |
| `try` | `try / except / except* / else / finally` | 🔧 `except*` 为 3.11+（PEP 654） |
| `raise` | `raise E(...)`；`raise ... from cause`；裸 `raise` 重抛 | 异常链保留原始原因 |
| `with` | `with expr as x:` 与多上下文 | PEP 343；3.10 起支持括号多行 |
| `assert` | `assert cond, msg` | `-O` 模式下被移除，**不要**用它做校验 |
| 定义 | `def` `class` `lambda` `return` `yield` `yield from` | `yield from`（PEP 380） |
| 异步 | `async def` `await` `async for` `async with` | PEP 492 |
| 作用域 | `global` `nonlocal` | 只影响名字绑定，不影响可变对象的修改 |
| 导入 | `import x` / `from x import y as z` / `import x.y` | 避免 `from x import *` |
| 类型别名 | `type Alias = int \| str` | 🔧 3.12+（PEP 695） |

### 四、一个自足的语义自测脚本

```python
# reference_selftest.py —— 教学示意，不参与构建（纯标准库，Python 3.12+）
from __future__ import annotations

def main() -> None:
    # 1) and / or 返回操作数，不是布尔值
    print("and/or:", (0 or "fallback"), ([] or [1, 2]), ("a" and 42))

    # 2) 链式比较与幂的右结合
    print("链式:", 1 < 2 < 3, "| 幂右结合:", 2 ** 3 ** 2)

    # 3) 银行家舍入：round 对 .5 取最近的偶数
    print("round:", round(0.5), round(1.5), round(2.5), round(2.675, 2))

    # 4) divmod 一次拿商和余
    print("divmod:", divmod(-7, 3))

    # 5) enumerate(start=) 与 zip(strict=)（strict 为 3.10+）
    print("enumerate:", list(enumerate(["a", "b"], start=1)))
    print("zip:", list(zip([1, 2], "ab", strict=True)))
    try:
        list(zip([1, 2, 3], "ab", strict=True))
    except ValueError as exc:
        print("zip strict 捕获:", exc)

    # 6) sorted(key=) 与稳定性
    data = [("b", 2), ("a", 3), ("c", 1)]
    print("sorted:", sorted(data, key=lambda t: t[1]))

    # 7) any / all 短路
    print("any/all:", any([0, "", 3]), all([1, "x", True]), any([]), all([]))

    # 8) getattr 默认值，避免在 __init__ 里写一堆 if
    class C:
        x = 10
    print("getattr:", getattr(C(), "x"), getattr(C(), "missing", "默认值"))

    # 9) vars / dir 的区别：vars 看实例字典，dir 看可访问名
    print("vars:", vars(C()), "| dir 数量:", len(dir(C())))

    # 10) 3.12 类型别名语句
    type Number = int | float
    print("type alias:", Number)

    # 11) 增强赋值对 list 是原地扩展，与 + 不同（+ 产生新对象）
    a = b = [1]
    a += [2]
    c = [1]; d = c + [2]
    print("+= 原地:", a is b, "| + 新建:", d is not c)

if __name__ == "__main__":
    main()
```

## 版本演进

| 版本 | 与本附录相关的变化 |
| --- | --- |
| 3.5（原书基线） | `zip` 无 `strict`；无 `breakpoint`；`match` 尚未出现；`@` 矩阵乘刚加入 |
| 3.6 | f-string（PEP 498）改变格式化写法；数字下划线 `1_000_000` |
| 3.7 | `breakpoint()` 进入内置；`dataclasses` |
| 3.8 | 海象运算符（PEP 572）；f-string `=`；仅位置参数 |
| 3.10 | 🔴 `match` 语句（PEP 634/635/636）；`zip(strict=)`；`aiter`/`anext`；`X \| Y`（PEP 604） |
| 3.11 | 🔴 `except*` 与 `ExceptionGroup`（PEP 654）成为新的语句形式；`tomllib` |
| 3.12 | 🔴 `type X = ...` 类型别名语句（PEP 695）；f-string 语法自由化 |
| 3.13 | 死电池移除（PEP 594）：`cgi`、`cgitb` 等不再是内置/标准库选项；新 REPL |
| 3.14 | 🔧 模板字符串 t-string、注解延迟求值；以官方 What's New 为准 |

## 经典论文与原始文献

> 以下均为**规范文档，非同行评审论文**。

| 编号 | 标题 | 年份 | URL |
| --- | --- | --- | --- |
| PEP 343 | The "with" Statement | 2005（2.5 落地） | https://peps.python.org/pep-0343/ |
| PEP 380 | Syntax for Delegating to a Subgenerator（`yield from`） | 2009（3.3 落地） | https://peps.python.org/pep-0380/ |
| PEP 492 | Coroutines with async and await syntax | 2015（3.5 落地） | https://peps.python.org/pep-0492/ |
| PEP 498 | Literal String Interpolation | 2016（3.6 落地） | https://peps.python.org/pep-0498/ |
| PEP 572 | Assignment Expressions | 2018（3.8 落地） | https://peps.python.org/pep-0572/ |
| PEP 604 | Allow writing union types as `X \| Y` | 2019 提出，3.10 落地 | https://peps.python.org/pep-0604/ |
| PEP 634 | Structural Pattern Matching: Specification | 2020（3.10 落地） | https://peps.python.org/pep-0634/ |
| PEP 654 | Exception Groups and except* | 2020 提出，3.11 落地 | https://peps.python.org/pep-0654/ |
| PEP 695 | Type Parameter Syntax（含 `type X = ...`） | 2023（3.12 落地） | https://peps.python.org/pep-0695/ |
| 官方文档 | Built-in Functions / Expressions / Simple statements | 持续更新 | https://docs.python.org/3/library/functions.html |

## 近年研究与工业界开源实践（2015–2026）

- **官方文档取代纸质手册**：内置函数与语句的权威口径在 docs.python.org，版本切换方便；本附录的价值在于「知道要查什么」。
- **静态检查补全手册**：`ruff` / `mypy` 会在你用错内置函数签名或误用 `assert` 做校验时直接报警，等于给手册配了自动校对。
- **`breakpoint()` 取代手写 `pdb.set_trace()`**：3.7 起成为内置，且可通过 `PYTHONBREAKPOINT` 切换调试器。
- **结构化并发带来的新语句**：`async with`、`async for`、`except*` 让「语句速查表」在 3.10–3.11 两年内连续扩容。
- **语言演进节奏**：3.9 起改为**每年一个次版本**（PEP 602 引入的年度发布节奏，🔧 以官方口径为准），手册类内容需按年复查。
- 🔧 以上版本号与细节以官方文档为准。

## 常见误区与本书需修正之处（原书条目 → 2026 现状）

| # | 原书条目 / 常见误区 | 2026 现状 |
| --- | --- | --- |
| 1 | 🔧 认为 `and`/`or` 返回布尔 | 返回**操作数**（`0 or "x"` → `"x"`），只是**真值**参与判断 |
| 2 | `round(2.5) == 3` | 银行家舍入：结果为 `2`（取最近偶数），`round(1.5) == 2` |
| 3 | 🔧 `zip` 长度不等时静默截断 | 3.10 起 `zip(..., strict=True)` 会抛 `ValueError` |
| 4 | 🔧 没有 `match` | 3.10 起有结构模式匹配（PEP 634/635/636） |
| 5 | 🔧 `try` 只有 `except/else/finally` | 3.11 起多一个 `except*`（PEP 654），用于 `ExceptionGroup` |
| 6 | 🔧 类型别名只能写 `Alias = int` | 3.12 起可写 `type Alias = int \| str`（PEP 695），支持惰性求值 |
| 7 | 🔧 联合类型只能 `Union[X, Y]` | 3.10 起 `X \| Y`（PEP 604） |
| 8 | 🔧 格式化只用 `%` 或 `format` | 首选 f-string（PEP 498）；3.14 还有 t-string 🔧 |
| 9 | 用 `assert` 校验用户输入 | `-O` 模式下 `assert` 被整体移除；校验应显式 `raise` |
| 10 | 🔧 调试用 `pdb.set_trace()` | 3.7 起内置 `breakpoint()`，可用 `PYTHONBREAKPOINT` 换调试器 |
| 11 | 以为 `is` 判断相等 | `is` 比身份；仅用于 `None`/`True`/`False`/单例比较 |
| 12 | 🔧 `for/while` 的 `else` 被忽略 | 语义是「循环未被 `break` 时才执行」，命名反直觉但很有用 |
| 13 | 🔧 `print` 只能输出到屏幕 | `file=` 可写文件对象，`flush=True` 控制缓冲 |
| 14 | 🔧 手册内容记下来就够 | 3.9 起年度发布，内置与语句逐年增删，需按年对照官方文档复查 |

## 与其他章 / 其他书的联系

- 本书：本附录是 **[A1-附录A 简明教程.md](A1-附录A-简明教程.md)** 的查表版；表达式与语句的讲解分布在 [01-快速上手：基础知识.md](01-快速上手：基础知识.md)、[03-使用字符串.md](03-使用字符串.md)、[05-条件、循环及其他语句.md](05-条件、循环及其他语句.md)、[06-抽象.md](06-抽象.md)；`with` 见 [11-文件.md](11-文件.md)；异常见 [08-异常.md](08-异常.md)；生成器见 [09-魔法方法、特性和迭代器.md](09-魔法方法、特性和迭代器.md)。
- 工程侧：打包与类型分别见 [18-程序打包.md](18-程序打包.md) 与本目录对 PEP 484/695 的说明。
- 他书：权威口径始终是官方 Language Reference 与 Built-in Functions 页面；《流畅的Python》对内置函数背后的数据模型有深入讨论（本仓库暂无笔记 🔧）。
- 回到总览：[00-总览与阅读地图.md](00-总览与阅读地图.md)
