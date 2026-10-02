# 08 · Control flow

> 一句话定位：`if`/`for`/`while`/异常——让程序分支与重复。
> 原书 pp. 英文 4e 第 8 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 8.1 | 布尔 | 真值测试 |
| 8.2 | `if` | 分支 |
| 8.3 | `for` | 遍历 |
| 8.4 | `while` | 条件循环 |
| 8.5 | 海象 | `:=`（3.8） |
| 8.6 | 匹配 | `match`（3.10） |

## 核心精讲

```
# 教学示意，不参与构建
for i in range(3):
    print(i)
if (n := len('abc')) > 2:
    print('长', n)
match kind:
    case 'int': ...
    case _: ...
```

- 真值：`0`/`''`/`[]`/`None` 为假，其余为真。
- `for` 遍历可迭代；`enumerate` 取索引。
- `match/case`（3.10）结构化匹配。

## 版本演进

- 海象 `:=`（PEP 572，3.8）。
- 模式匹配 `match`（PEP 634，3.10）。
- `itertools` 提供高级迭代。

## 经典论文与原始文献

- PEP 572 / PEP 634；Python 教程「More Control Flow Tools」。
- Python 官方控制流文档。

## 近年研究与工业界开源实践（2015–2026）

- `match/case` 在命令解析/状态机替代 `if/elif`。
- 生成器表达式惰性求值。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| `range(len(x))` 遍历 | 用 `for item in x` 或 `enumerate` |
| 忽略真值规则 | 显式 `if x is not None` |
| 🔧 4e 强调 match | 多分支学 3.10+ |

## 与其他章 / 其他书的联系

- 函数见[第09章 Functions](09-Functions.md)。
- 见 [`Automate the Boring Stuff with Python 3e/02-控制流.md`](../Automate the Boring Stuff with Python 3e/02-控制流.md)。
