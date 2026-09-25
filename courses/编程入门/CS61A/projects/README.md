# CS61A 配套项目总览

> 语言：Python（**仅标准库**）。每个目录含源码 + README + `run.bat`/`run.sh`
> （脚本注释内附 `python -m py_compile` 语法自检命令）。P1-P4 对应官方四大
> Project 的知识点（骨架从简、主题重映射为可自测的迷你版）；p5/p6 对应 L23/L25
> 两个专题周。

## 讲次 → 项目 → 知识点

| 讲次 | 项目 | 核心知识点 |
| --- | --- | --- |
| L01-L02（+L04/L20 前哨） | [p1_expr](p1_expr/README.md) 表达式计算器 + 玩具分数 | 精确整数/地板除/短路 bool；词法+递归下降解析；AST 求值；数据抽象屏障（Rat） |
| L03-L08 | [p2_abstraction](p2_abstraction/README.md) 函数式 2048 逻辑层 | 纯函数与不可变表示；表示变换归约（transpose/rotate→一个方向）；高阶 `max(key=)`；可注入随机 |
| L13-L18（+L24 前哨） | [p3_data](p3_data/README.md) 链表/树/OrderedDict/迷你 SQL | 身份与可变性；三指针反转；树的 accumulate；dict+双链=OrderedDict/LRU；nested-loop vs hash join 复杂度实证；σ/π/τ/⋈ 算子 |
| L19-L22 | [p4_scheme](p4_scheme/README.md) Scheme 解释器 | Frame 环境链；eval/apply；特殊形式与过程对象；**while 状态机蹦床实现尾递归**；define-macro；<600 行 |
| L23 | [p5_streams](p5_streams/README.md) 流与惰性求值 | delay/force+memoization 流 vs 一次性生成器；无穷素数筛；`cons-stream 1 ones` 自引用流 |
| L25 | [p6_concurrency](p6_concurrency/README.md) 并发与 GIL | 竞态/锁/消息传递；CPU vs I/O 密集下线程池与进程池计时对比 |

## 官方 Project 对照

| 官方 | 主题 | 本项目替代件 |
| --- | --- | --- |
| P1 Hog | 函数与随机性 | p1（精确算术/解析求值）+ p2 的 `rng` 注入 |
| P2 Penguins | 数据抽象+地图 | p2（不可变棋盘+表示变换） |
| P3 Comments | OOP+链表/树+网络层 | p3（链表/树/ODict/迷你 SQL，去掉网络层与 okpy） |
| P4 Scheme | 解释器 | p4（同主题，骨架重写为双文件、自带测试与 REPL） |

## 快速回归

```bash
# 全部语法自检（Windows 把 /  换成 \ 同理）
python -m py_compile p1_expr/rat.py p1_expr/expr.py p1_expr/main.py
python -m py_compile p2_abstraction/game2048.py p2_abstraction/main.py
python -m py_compile p3_data/linked.py p3_data/trees.py p3_data/odict.py p3_data/minisql.py p3_data/main.py
python -m py_compile p4_scheme/utils.py p4_scheme/scheme.py
python -m py_compile p5_streams/streams.py p5_streams/sieve.py
python -m py_compile p6_concurrency/race.py p6_concurrency/gil_demo.py p6_concurrency/main.py

# 行为自检（每个项目都带断言）
python p1_expr/expr.py && python p2_abstraction/game2048.py
python p3_data/linked.py && python p3_data/trees.py && python p3_data/odict.py && python p3_data/minisql.py
python p4_scheme/scheme.py --test && python p4_scheme/scheme.py p4_scheme/demo.scm
python p5_streams/streams.py && python p5_streams/sieve.py
python p6_concurrency/race.py
```
