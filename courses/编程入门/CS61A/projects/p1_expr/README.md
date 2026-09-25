# P1 表达式：整数/布尔完整算术 + 玩具分数

> 对应讲次：L01（整数与布尔）、L02（表达式求值与环境）、L04（域假设）、
> 并为 L20（词法/语法分析）打底。官方课程对应 Project 1 Hog；本迷你版换成了
> 更贴近"求值本质"的表达式计算器，知识点覆盖不变（函数、递归、精确算术、真值性）。

## 内容

| 文件 | 说明 |
| --- | --- |
| `rat.py` | 不可变有理数 `Rat`：构造即约分（`gcd`）、符号归一、全比较、幂。对应 L01 "任意精度/精确算术" 与 L10 数据抽象（构造/选择器契约）。 |
| `expr.py` | 完整流水线：`tokenize`（正则词法）→ `Parser`（递归下降，优先级表）→ `evaluate`（AST 求值，短路 and/or、链式比较、`/` 产出 Rat、`// %` 地板语义）。 |
| `main.py` | 演示入口 + `expr._selftest()/rat._selftest()` 内建断言。 |

## 运行

```bash
python main.py          # 演示
python expr.py          # 单独跑自检
```

Windows 双击 `run.bat`，或 `run.sh`。语法自检：
`python -m py_compile rat.py expr.py main.py`

## 知识点对照（CS61A）

- L01：`-7//2 == -4`、`-7%2 == 1`、`or` 返回操作数、bignum `2**100`；
- L02：AST 树形求值=组合式归约；`/` 产生 `Rat` 体现"数据抽象屏障"；
- L04：`ParseError/EvalError` 显式域检查（守卫生则）；
- L20：递归下降与 Scheme `scheme_read` 同法，提前体验 P4 前端。
