# P4 Scheme 解释器：用 Python 解释 Scheme（毕业项目迷你版）

> 对应讲次：L19（Scheme 与计算器）、L20（词法/语法分析）、L21（环境/特殊形式/过程对象）、
> L22（元循环、尾递归、宏）、L23（流）。官方 Project 4 的教学目标完整保留，
> 骨架重写为 **单文件对 + 内建 REPL**（utils.py + scheme.py 合计 <600 行）。

## 文件

| 文件 | 行数级 | 内容 |
| --- | --- | --- |
| `utils.py` | ~210 | `Pair`（cons 单元/nil）、`Symbol`、词法 `scheme_tokens`、递归下降 `scheme_read`（quote 糖、`#t/#f`、字符串、bignum 整数、点对）。 |
| `scheme.py` | ~380 | `Frame`（环境链）、`BuiltinProcedure/Procedure/Macro/Thunk`、`scheme_eval`（**while 状态机**）、12 个特殊形式、~30 个内建、PRELUDE（map/filter/foldl/stream-ref/list-ref）、REPL、`--test` 全套自测。 |
| `demo.scm` | — | fact/尾递归 10 万步/make-adder 闭包/`when` 宏/偶数流/count-change。 |

## 运行

```bash
python scheme.py --test        # 自测（含 200000 步尾递归、流 memoize）
python scheme.py demo.scm      # 批处理脚本
python scheme.py               # REPL（多行自动续行，Ctrl-D 退出）
```

`run.bat` / `run.sh`（默认进 REPL；`run.bat --test` 可传参）。
语法自检：`python -m py_compile utils.py scheme.py`

## 与官方 P4 的关键差异（有意为之）

1. **尾递归**：官方用 `TailCall` 数据对象 + `scheme_call` 外层蹦床；本实现把蹦床
   **折叠进 `scheme_eval` 的 while 循环**（特殊形式经 `_Jump` 交还尾表达式）——
   语义等价，栈行为同为 O(1) Python 帧。
2. **宏卫生**：官方 P4 宏参数替换做了防捕获处理；本实现直接"参数=未求值表达式 +
   展开环境求值"，够用但同名变量会捕获（练习：自己修）。
3. 无 `lambda` 多体之外的 `do/delayed` 抽象层、无对象系统——保持最小。

## 知识点落点

- L20：token→Pair 树（`scheme_read` 与语法规则一一对应）；
- L21：`Frame.lookup` 沿 parent 链=环境图；`define (f ...)` **先绑壳**实现递归定义；
  Procedure 携带闭合环境= L06 闭包规则；
- L22：eval/apply 合一状态机；`define-macro`（when）与 `and/or` 特殊形式展示
  "控制求值策略"的两种高度；
- L23：`cons-stream` 只 eval 第一参，`Thunk.force` memoized——`(define ones
  (cons-stream 1 ones))` 成为无穷流；
- L01：`(/ 1 3)` → `Fraction`（真除法精确）；`(modulo -7 2)` → 1（欧几里得）。
