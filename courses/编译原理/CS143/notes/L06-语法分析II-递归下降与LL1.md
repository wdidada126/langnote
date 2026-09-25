# L6 语法分析 II：自顶向下与 LL(1)

> 讲次：CS143 L6 ｜ 阅读：龙书 ch4.3-4.4 ｜ 配套：projects/02_parser（手写递归下降）

## 核心概念

### 递归下降（面向实践的主线，PA2 精神）
- 每个非终结符一个过程；产生式右部顺序 = 代码顺序；`{ return new IfStmt(...); }` 即构树动作。
- 预测冲突处插入前瞻：k 个 token 决定分支。LL(1) 就是"1 个前瞻足够"的文法性质。
- 错误恢复：panic mode——丢弃 token 直到同步集（`;`、`}`、语句起点），保证不崩溃、每错误只报一次。

### LL(1) 判定：FIRST 与 FOLLOW
```
FIRST(α):
  终结符 a            -> {a}
  A -> X1..Xn          -> 累加 FIRST(X1)
  若 X1..Xi-1 全可推 ε -> 并入 FIRST(Xi)
  若全部 nullable      -> 并入 ε
FOLLOW(A):
  起点 S: 加 $
  A -> α B β:  FIRST(β)\{ε} 入 FOLLOW(B)
  若 β ⇒* ε 或 A -> α B:     FOLLOW(A) 入 FOLLOW(B)
LL(1) 条件: 对 A -> α | β 两条：
  1) FIRST(α) ∩ FIRST(β) = ∅
  2) 若 ε ∈ FIRST(β)，则 FIRST(α) ∩ FOLLOW(A) = ∅
```
手算例题（MiniC 语句层）：
```
stmt -> if_stmt | while_stmt | block | assign | print | return | decl
FIRST(if_stmt)={if} FIRST(while)={while} FIRST(block)={{} ...两两不交 ⇒ 语句层 LL(1) 成立。
表达式若写成 E -> T E', E' -> + T E' | - T E' | ε 也满足；
若忘消左递归：E -> E + T | T，FIRST 相交 {id,(} ⇒ 不是 LL(1)，且递归下降直接栈溢出（无限左递归调用）。
```
LL(1) 分析表：`M[A, a] = A -> α iff a ∈ FIRST(α)`；ε 产生式填 `FOLLOW(A)` 列。表冲突 = 文法不是 LL(1)。

### 实战绕过 LL(1) 限制
- 左递归：LL 不可，但 `E = E + T` 可改循环 `p = term(); while accept(+/-) p = binop(...)`——**这是 projects/02 的做法**，等价于算符优先级提升（Pratt parsing 的雏形）。
- if 后接括号 vs 表达式后缀：常见语言需要任意前瞻 → 递归下降 + 手工前瞻（Kotlin/Swift 路线），而不是死守 LL(1) 表。

## 与前后讲的联系
- 上承 L5 文法转换（消左递归/提公因子就是为 LL 服务）；下启 L7：LR 能吃的文法严格更大，且自底向上对错误定位更准。
- PA2 用 bison（LALR）而非手写，但本讲的树形心智是 PA3/PA4 遍历 AST 的基础。
- 递归下降天然把文法结构映射成代码结构，属性/动作（L9）以构造函数参数形式出现——"语法制导"在手工分析器里是显式的。

## 跨课程联系
- **6.006/CS170**：FIRST/FOLLOW 闭包计算 = 工作列表算法（不动点迭代），与 DFA 子集构造、数据流分析（L14）同一个骨架；LL 分析表构造即"文法上的可达性分析"。
- **CS3110/CS242**：递归下降是"解析树 = 代数数据类型"的直白实现，OCaml variant + pattern match 写 PA2 会短一半。
- **CSAPP**：递归下降的调用栈深度即表达式嵌套深度——恶意输入爆栈是真实安全问题（对比 LR 的显式栈）。

## 开源项目中的应用
- **rustc**：`parse_expr` 用手写递归下降 + 前瞻集合；正式文档明言"我们不做 LL(k) 表，用代码里的 look-ahead 组合"。
- **CPython**：PEG 分析器本质是带有序选择的递归下降（PEG 以首匹配消二义）；实现用标记栈回卷而非完整 packrat 记忆化（见 PEP 617），是对"回溯代价"的工程答案。
- **Clang**：`ParseExpression` 递归下降 + `Tok.is()` 前瞻；错误恢复策略（`SkipUntil`）值得读源码。
- **tree-sitter**：GLR（L7）但保留 `preferred_sibling` 等"类 LL"前瞻提示，说明两类算法在混合。

## 延伸阅读
- 龙书 ch4.3.2-4.4（含 LL(1) 表构造全套例题）；HW2 的 FIRST/FOLLOW 计算。
- Parr "LL(*)" 论文（自适应前瞻）；Pratt 1973 算符优先递归下降原文。
- Medeiros "Lost in Translation"（递归下降错误恢复的坑）。
