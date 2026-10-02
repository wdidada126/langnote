# 10 · Modules and scoping rules

> 一句话定位：`import`、模块、LEGB 作用域——代码如何组织与名字如何查找。
> 原书 pp. 英文 4e 第 10 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 10.1 | 模块 | 一个 `.py` 一个命名空间 |
| 10.2 | `import` | 各种形式 |
| 10.3 | 作用域 L/E/G/B | 查找顺序 |
| 10.4 | `global`/`nonlocal` | 修改外层 |
| 10.5 | `__name__` | 主模块 |

## 核心精讲

```
# 教学示意，不参与构建
import math
from pathlib import Path as P
# 作用域：Local → Enclosing → Global → Builtin
def outer():
    x = 1
    def inner():
        nonlocal x
        x += 1
    inner()
    return x
```

- 模块是独立命名空间；`import` 导入名字。
- LEGB：局部→闭包→全局→内置。
- `global`/`nonlocal` 声明修改外层变量。

## 版本演进

- 相对导入（包内 `.`/`..`）长期稳定。
- `from __future__ import annotations`（3.7）延迟标注。

## 经典论文与原始文献

- Python 作用域官方文档「Execution model」。
- PEP 3104 — `nonlocal` 语句。

## 近年研究与工业界开源实践（2015–2026）

- 类型标注与 `if TYPE_CHECKING` 避免循环导入。
- `importlib` 动态导入。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 用 `global` 改全局 | 优先返回新值 |
| 循环导入 | 延迟导入/`TYPE_CHECKING` |
| 🔧 4e 标 3.13 | 以官方为准 |

## 与其他章 / 其他书的联系

- 概念专篇 [concepts/作用域与LEGB.md](concepts/作用域与LEGB.md)。
- 包见[第18章 Packages](18-Packages.md)；程序见[第11章 Python programs](11-Python programs.md)。
