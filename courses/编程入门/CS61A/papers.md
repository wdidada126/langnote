# CS61A 论文与开源应用清单

> 状态：全量（2026-09）。事实性条目以能核实者为准，不确定处标"待核实"。

## 1. 经典文献 / 元典

| 文献 | 年份 | 主题 | 关联讲次 |
| --- | --- | --- | --- |
| Abelson & Sussman（+ Sussman），*Structure and Interpretation of Computer Programs*（MIT 6.001 教材，电影《Little Man, Little Man》配套） | 1985/1996（1/2 版） | 过程/数据/模块化/元循环四大抽象 | 全课程骨架，尤 L08/L10/L19-L22/L26 |
| *Composing Programs*（Pritchard, Hilfinger, Pham, Sexton；CS61A 官方教材，CP 缩写出处） | 2012-2019（1/2 版） | Python 化 SICP；计算器/解释器/流/宏章节 | 全部讲义主阅读 |
| McCarthy，《Recursive Functions of Symbolic Expressions and Their Computation by Machine》（"Recursive Function"） | 1960 | Lisp/`eval` 首创：代码即数据、cons/car/cdr、条件表达式 | L19-L22（eval/apply 的思想源头） |
| Abelson, Sussman & Sussman，《Scheme: An Interpreter for Extended Computer Languages》（"Little Scheme"） | 1983/1985 | 用元循环解释器扩展语言；与 P4 结构几乎同构 | L20-L22 |
| Friedman, Byrd, Combs（2 版增 Kiselyov? 待核实），《The Reasoned Schemer》 | 2005/2018 | miniKanren：逻辑编程扩展 Scheme；关系式编程视角（注：**非** Friedman & Wand 合著——二人真实合作是指称语义未刊稿《The Little Semantist》） | L24（声明式对照）、L22 |
| "Lambda: The Ultimate Imperative"（Abelson & Sussman, MIT AI Lab, 1977，讲义性质）与常被并称的 "Lambda: The Ultimate Formula"（作者归属**待核实**，网络亦有误传 McCarthy/Streett 版本；建议以 MIT OCW 6.001 媒体清单为准） | 1977/1986 | lambda 表达一切：过程即数据 | L05-L06、L21-L22 |
| Landin，《The Mechanical Evaluation of Expressions》 | 1964 | SECD 机：环境+栈的求值机器模型 | L02、L22（蹦床/帧的机器观） |
| Mosses（Scott-Strachey 学派讲义）或 ten Teije? 以 Scott-Strachey 域方程原著为准（待核实），指称语义奠基文献群 | 1970s | 指称语义："eval 的数学化" | L22（元循环的理论面） |
| Kay 等关于 Smalltalk 消息传递 OOP 的论文（"The Early History of Smalltalk"） | 1993（HOPL-II） | OOP=消息传递：CP §2.3/2.4 的历史源头 | L13-L15 |
| Hughes，《Why Functional Programming Matters》（Computer Journal 33(2)） | 1990 | 惰性求值与函数组合的力量（流的模块化） | L23 |
| Ousterhout，《Scripting: Higher Level Development for the 21st Century》 | 1998 | 嵌入式脚本语言（Scheme 嵌入的工程理由） | L19-L22、L24 |
| 《Reversible Scheme》（Pottier）等元循环变体论文 | 1990s | 改变 eval 即改变语言 | L22（选读） |
| C. A. R. Hoare，《Quicksort》/《Algorithm 64: Heapsort》 | 1961/1964 | 排序算法原始文献（本课只到 merge/insertion，作延伸） | L18 |
| GIL 无原始论文——以 CPython 文档、python-dev 归档与 PEP 703（free-threading）为准 | 1992+/2023 | 全局解释器锁史与 no-GIL 演进 | L25 |
| 关系模型：Codd，《A Relational Model of Data for Large Shared Data Banks》 | 1970 | SQL 的理论地基 | L24 |

**事实核查备注**：
- 《Lambda: The Ultimate Imperative》确为 Abelson & Sussman（MIT AI Lab, 1977）的讲义/
  演讲材料，非期刊论文；姊妹篇《Lambda: The Ultimate Formula》的作者归属存在多种网络
  说法（Eugene Koh / Street / McCarthy 等），**均待核实**，建议以 MIT OCW 6.001 媒体清单为准。
- 《The Reasoned Schemer》（MIT Press）与 Friedman & Wand 无关；Wand 与 Friedman 并无此
  合著（网传说法不属实）。该书 2005 初版与 2018 二版的作者名单细节**待核实**，本书只保证
  "miniKanren/逻辑编程"主题归属无误。
- Kay 的 Smalltalk 史文与 Codd 1970 为公认出处；Ousterhout 1998 刊于 IEEE Computer。

## 2. 近 5 年（2021-2026，教学型解释器 / 语言工程，从简）

| 条目 | 年份 | 方向 | 关联 |
| --- | --- | --- | --- |
| PEP 703 "Making the Global Interpreter Lock Optional in CPython" 及后续 no-GIL 实验构建（3.13t） | 2023-2025 | 运行时并发演进 | L25 |
| CPython 3.11/3.12/3.13 性能系列（zero-cost exceptions、adaptive specialization、tail calls 提案 PEP 688? 未合并，待核实） | 2022-2025 | 解释器优化实录 | L20-L22 |
| 教学型解释器文章/仓库：*Writing a Scheme in 500 lines*（*Crafting Interpreters* 的 Scheme/Lisp 章节；Robert Nystrom）持续再版 + MIT 6.001 教材网络免费版（MIT Press 2022 视频修复） | 2021-2024 | 解释器教学 | L19-L22、P4 |
| Racket 7.9→8.x（"The Road to Go"版本叙事、contract system 演进）、Guile 3.0（并发线程库 JIT） | 2020-2024 | Scheme 生态现状 | L19-L23 |
| CS61A spring2024/fall2024/spring2026 课程改版记录（官网 changelog：LLM 选读周进入 syllabus） | 2023-2026 | 课程内容演进 | L17 |
| free-threaded Python 生态适配讨论（numpy 等发行支持 cp313t wheels） | 2024-2026 | L25 | L25 |

## 3. 知识点 ↔ 开源项目映射

| 知识点（讲次） | 开源项目/实现 | 体现 |
| --- | --- | --- |
| 精确整数/bool 语义（L01） | CPython `Objects/longobject.c` | bignum 30-bit digit 数组、Karatsuba 混合乘法 |
| 环境模型/帧（L02、L21） | CPython `Objects/frameobject.c`、PyPy | LOAD_NAME/LOAD_GLOBAL 字节码；PyPy inline cache |
| 高阶函数/闭包（L05-L06） | `functools.lru_cache`、Flask/Django 装饰器 | MAKE_FUNCTION + cell；def 时注册的机制 |
| 递归/树递归（L07） | `json`/`ast`/`tomllib` 解析器 | 递归下降 + 深度限制防爆栈 |
| 增长阶（L08） | CPython list/dict over-allocation；sortedcontainers | 均摊 O(1)；√n 分块结构 |
| 序列/高阶操作（L11） | `itertools`、`functools.reduce`、pandas | 迭代器代数、流水线组合子 |
| 迭代器/生成器（L12、L23） | `contextlib`、ijson、pandas chunksize | 暂停/恢复的帧（genobject.c）与惰性数据源 |
| 链表（L13、L19-L22） | P4 的 `Pair`（本项目 p4_scheme/utils.py）；Racket/Guile pair 原语 | Scheme 一切结构的裸金属 |
| OOP/属性与 MRO（L14-L15） | CPython `typeobject.c`、attrs/pydantic、Django mixin | C3 线性化、描述符协议 |
| 树/字典（L16） | CPython `dictobject.c`（紧凑表/split-key）、sqlite B-tree | 哈希 vs 树两种组织的工程范本 |
| 排序（L18） | CPython listsort（Timsort）、`heapq.merge`、Postgres ORDER BY | 归并+插入混合与 top-N/外部归并 |
| Scheme 解释器（L19-L22） | Racket、Guile、Chicken（Scheme→C）；PyPy（RPython 自举） | eval/apply、TCO、宏系统的三种实现 |
| 元循环/尾递归（L22） | Guile VM（proper tail calls）、P4 蹦床（本项目） | 语言承诺与机器现实的桥 |
| 流/惰性（L23） | Haskell（默认惰性）、polars lazy、Dask 图 | thunk 共享与按需执行 |
| SQL（L24） | sqlite（进程内小解释器+VDBE）、DuckDB | "数据库=另一种解释器"的直证 |
| 并发/GIL（L25） | CPython `pystate.c`（GIL）、asyncio/uvloop、3.13t | refcount 锁与事件循环两方案 |

## 4. 本项目（langnote/CS61A）对应物

- P1-P4 + 流/并发 mini 项目全部为本仓库自制、标准库 only：见 [projects/README.md](projects/README.md)。
- P4 解释器与 SICP"Little Scheme"、CP §4 的骨架同构（约 600 行内），可对照 Guile/Racket 文档找差异。
