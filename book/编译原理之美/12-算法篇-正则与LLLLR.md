# 第 12 章 算法篇：正则工具、First/Follow 与 LL / LR（讲 16–19）

> **一句话**：这一篇把前三章的「工程直觉」换成「算法」——把 NFA/DFA 做成一个真正的正则表达式工具，用 First/Follow 集合推演 LL(1)，用「移进/规约」推演 LR；最后用一场答疑收尾「左递归」这个经典疑问。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 12.1 | NFA / DFA：做一个正则表达式工具 | 讲 16：正则式 → NFA → DFA → 最小化 → 引擎 |
| 12.2 | 正则引擎的两种实现 | 自动机型（线性）vs 回溯型（指数） |
| 12.3 | First 集合 | 一个非终结符能派生出的**第一个终结符**集合 |
| 12.4 | Follow 集合 | 紧跟在非终结符之后的**终结符**集合 |
| 12.5 | LL 算法推演 | 讲 17：第一个 L = Left-to-right，第二个 L = Leftmost |
| 12.6 | LL(1) 分析表 | 预测分析表怎么填、怎么查 |
| 12.7 | 移进与规约（Shift-Reduce） | 讲 18：自底向上分析的核心动作 |
| 12.8 | LR 算法推演 | 讲 18：用「反向最右推导」理解 |
| 12.9 | 讲 19 答疑：左递归的推导 | 消除左递归 ≠ 消除左结合 |
| 12.10 | LR 之外的选择 | Earley / GLR / PEG |

---

## 核心精讲

### 12.1 讲 16：自己实现一个正则表达式工具

```python
# 教学示意：正则式 -> 后缀式 -> NFA（不参与构建、不编译、不运行）
# 1) 中缀转后缀（Shunting-yard）:  a|b*  ->  a b | *
# 2) Thompson 构造: 每个片段产生一个小 NFA
NFA(frag='a')   ->  s --a--> f
NFA(frag='b*')  ->  (s,ε)->(0) --b-> (1) --ε-> (2) ; (s,ε)->(2)
# 3) 拼接 / 合并 / 加环
# 4) 子集构造 -> DFA（见 02 章）
# 5) 最小化 -> 最终引擎
```

一个可用的正则工具至少要有：贪婪/非贪婪、`|`、`?`、`*`、`+`、字符类、捕获组、以及**最重要的——超时或步数上限**。

### 12.2 两种正则引擎，两种世界观

| | 自动机型（DFA/NFA 模拟） | 回溯型（PCRE 等） |
| --- | --- | --- |
| 最坏复杂度 | **线性**（RE2 / Rust regex） | **指数**（灾难性回溯） |
| 支持的子集 | 受限（无反向引用） | 完整 PCRE |
| 典型实现 | RE2、hyperscan、Go `regexp` | PCRE、Python `re` |

课程讲 16 让你手搓一个自动机型，正是为了让你体会**「线性保证」这件事的价值**。

### 12.3 First 集合

定义：`FIRST(α)` = α 能派生出的所有串的**第一个终结符**的集合。

```text
E  -> T E'
E' -> '+' T E' | ε
T  -> F T'
T' -> '*' F T' | ε
F  -> NUM | ID | '(' E ')'

FIRST(E)  = { NUM, ID, '(' }
FIRST(E') = { '+', ε }
FIRST(T') = { '*', ε }
FIRST(F)  = { NUM, ID, '(' }
```

计算规则（不动点迭代）：

```python
# 教学示意：First 集合的不动点计算（不参与构建）
FIRST = {A: set() for A in nonterminals}
while changed:
    for lhs, alts in productions.items():
        for beta in alts:
            if is_terminal(first_token(beta)):
                FIRST[lhs] |= {first_token(beta)}
            else:
                # 把 beta 里每个非终结符的 FIRST 并进来，遇到非 ε 就停止
                for X in beta:
                    FIRST[lhs] |= FIRST[X] - {EPS}
                    if EPS not in FIRST[X]: break
                else:
                    FIRST[lhs] |= {EPS}
```

### 12.4 Follow 集合

定义：`FOLLOW(A)` = 在所有推导中，**紧跟在 A 之后**可能出现的终结符集合。

```text
FOLLOW(E)  = { ')', EOF }              // E 可以出现在 '(' E ')' 里，也可能是整句
FOLLOW(E') = FOLLOW(E) = { ')', EOF, '+' }
FOLLOW(T)  = FOLLOW(E) ∪ { '+' } = { ')', EOF, '+' }
FOLLOW(T') = FOLLOW(T)
FOLLOW(F)  = FOLLOW(T) ∪ { '*' }
```

初始化技巧：

- `FOLLOW(start) ⊇ { EOF }`。
- 对每条产生式 `A -> βBγ`，把 `FIRST(γ)`（去掉 `ε`）并入 `FOLLOW(B)`；若 `γ` 可派生 `ε`，把 `FOLLOW(A)` 也并入 `FOLLOW(B)`。

### 12.5 LL 算法：名字里藏着的答案

课程原摘录写得很清楚：

> **LL 算法就属于这类预测性的算法。** 第一个 L，是 Left-to-right，代表从左向右处理程序代码。第二个 L，是 Leftmost，意思是最左推导。

于是：

| LL(k) 里的 k | 含义 |
| --- | --- |
| Left-to-right | 从左到右扫输入 |
| Leftmost | 最左推导（总是先展开最左边的非终结符） |
| k | 往前看 **k 个** Token 才能决定用哪条产生式 |

```text
对状态 (A, 当前Token t)：
    若 A -> α 且 t ∈ FIRST(α)         -> 用 α 展开（预测）
    若 A -> ε 且 t ∈ FOLLOW(A)        -> 空转（匹配 ε）
    否则                              -> 报错
```

### 12.6 LL(1) 分析表

```python
# 教学示意：预测分析表（不参与构建）
def predict_table(P):
    T = {}
    for lhs, alts in P.items():
        for alpha in alts:
            first = FIRST(alpha)
            for t in first - {EPS}:  T[(lhs, t)] = alpha
            if EPS in first:
                for t in FOLLOW(lhs): T[(lhs, t)] = alpha
    return T          # T[(A,t)] 有两条以上 => 不是 LL(1)，有冲突
```

| 冲突类型 | 例子 | 解决 |
| --- | --- | --- |
| **提取左因子** | `A -> x y | x z` | 改写成 `A -> x (y | z)` |
| **消除左递归** | `A -> A a | b` | 见 04 章 / 讲 19 |
| **公共前缀** | `stmt -> if ... | if ... else ...` | dangling else（ANTLR 用「改写优先级」解决） |

### 12.7 移进与规约：自底向上

课程讲 18 的标题就是这两个动作。核心洞察在用户原摘录里：

> **反向最右推导（Reverse RightMost Derivation）**

LR 分析的过程，就是**反向进行最右推导**：

```text
最右推导（自上而下地"生成"）：
  E => E + T => E + T * F => E + T * NUM => ...
                                    ^^^^^^
反向最右推导（自下而上地"归约"）：
  NUM --规约--> F --规约--> T*F --规约--> E+T ...
```

```python
# 教学示意：LR 分析器的两个动作（不参与构建）
def step(action_table, goto_table, stack, ip):
    a = input[ip]
    act = action_table[top(stack)][a]
    if act == 'shift':                 # 移进：把 a 压栈，读下一个
        stack.append(a); ip += 1
    elif act == 'reduce':              # 规约：弹出 r 个，压入左部，按 goto 转状态
        for _ in range(rhs_len): stack.pop()
        stack.append(lhs)
        stack.append(goto_table[top(stack)][lhs])
    elif act == 'accept': return True
    else: raise SyntaxError(...)
```

**为什么 LR 更强大？** 因为 LL 是「**预测**：看到 k 个 Token 猜一条产生式」；LR 是「**决策**：用整个栈 + 当前 Token 维护一个确定性的状态机」。LL 有回溯的可能，LR 没有——这就是讲 18 存在的意义。

### 12.8 LR 族谱

| 算法 | 前看数 | 表大小 | 说明 |
| --- | --- | --- | --- |
| SLR | 1 | 小 | 用 FOLLOW 填表，最弱 |
| LR(0) | 0 | 中 | 状态最多 |
| LR(1) | 1 | 大 | 最精确 |
| **LALR** | 1 | 中 | 合并同核心状态，**yacc 用的就是它** |

DeRemer 与 Pennello 1982 解决了「LALR 前看集高效计算」的工程难题，这才让 yacc 能稳定可用。

### 12.9 讲 19 答疑：为什么推导不是左递归的

回顾四个概念，这次放在一起看：

| 概念 | 层次 | 是否随「消除左递归」改变 |
| --- | --- | --- |
| 文法里的直接左递归 | **语法形式** | ❌ 被消除了 |
| 分析器的分析方向 | **算法行为** | ❌ 仍然是从左到右挂左子树 |
| 运算符的结合性 | **语义约定** | ❌ 仍然是左结合 |
| 生成的语法树形状 | **产出结果** | ❌ 仍然是左倾树 |

**结论**：消除左递归只是为了让递归下降分析器**能停机**；语义上的左结合性**必须保留**，否则 `1-2-3` 会算成 `1-(2-3)`。这是本课程最经典的一个答疑点。

### 12.10 LR 之外的选择

课程只讲了 LL 与 LR，但工程上「第三条路」不少：

| 算法 | 能力 | 代表 |
| --- | --- | --- |
| **Earley** | 任意 CFG，多项式时间，天然支持左递归，无需提取左因子 | `lark` 的 earley 模式、Cy 的 `earley` 解析器 |
| **GLR（Tomita）** | 通用 LR，冲突时并行展开 | `parse` 库、ANTLR 的 ALL(\*) 部分思路 |
| **PEG** | 无回溯但有有序选择 | `lark`、`chevrotain` |
| **GLR + 增量** | 增量解析 | **Tree-sitter** |

```text
Earley 的核心：每个位置维护一个「项集(items)」，
  X -> α • β   表示「已经匹配了 α，接下来期待 β」
三种动作：扫描(scan) / 预测(predict) / 归约(reduce)
```

> Earley 解析器最大的工程价值是：**它不需要你消除左递归、不需要提取左因子**，对「先用着、语法还没定型」的 DSL 极其友好。课程 2019 年上线时没有把 Earley 放进正文，这是 2026 年值得补的一块（见「常见误区」）。

---

## 版本演进

| 年份 | 事件 |
| --- | --- |
| 1964 | **Knuth** 提出 LR(k) 文法，自底向上分析有了理论框架 |
| 1965 | Knuth 提出**算符优先文法** |
| 1968 | **Earley** 的通用解析算法（CACM 1970 正式发表） |
| 1970 | Earley, J.，*An Efficient Context-Free Parsing Algorithm*（CACM） |
| 1972 | **Tomita** 提出 GLR 的早期形态；1986 年正式发表（TOPLAS） |
| 1975 | **yacc**（LALR(1)）成为事实标准 |
| 1977 | **Aho & Johnson** 的 *LR Parsing* 综述，LR 理论成熟 |
| 1982 | **DeRemer & Pennello**，LALR(1) 前看集高效计算（TOPLAS） |
| 1986 | Tomita, M.，*An Efficient Augmented LR Parser*（TOPLAS） |
| 1988 | **ANTLR 1**（PCCTS），LL(k) + 语法谓词 |
| 1998 | Parr & Quong，ANTLR 的 Predicated-LL(k) 论文 |
| 2004 | **PEG**（Ford, POPL），有序选择的无歧义解析 |
| 2010 | `boost::spirit` 把 PEG 带进 C++ |
| 2013 | **ANTLR 4** 的 ALL(\*)，自适应前看取代静态 k |
| 2018 | **Tree-sitter**（ICSE 2018）：增量 + 容错，LR(1) 的增量版本 |
| 2019 | 本专栏上线，讲 16–18 覆盖正则工具/LL/LR |
| 2021 | **ANTLR 4.12.0** 增加 TypeScript 运行时 |
| 2024 | **ANTLR 4.13.2** 仍为最新稳定版 |
| 2025–2026 | LLM 写 LL/LR 语法时的**经典错误**就是本讲讲过的三类：左递归、提取左因子、dangling else |

---

## 经典论文与原始文献

| 文献 | 出处 | 与本讲的关系 |
| --- | --- | --- |
| Knuth, D. E.，*The Art of Computer Programming, Vol. 1*（形式化算法与复杂度基础） | **1968 / 2nd ed. 1973** | LR 分析的理论源头与其复杂度论证 |
| Earley, J.，*An Efficient Context-Free Parsing Algorithm* | **CACM 13(2), 1970** | LR 之外最重要的通用解析算法 |
| Aho, A. V. & Johnson, J. C.，*LR Parsing* | **SIGPLAN Notices 12(12), 1977** | LR 分析的经典综述 |
| DeRemer, F. & Pennello, T.，*Efficient Computation of LALR(1) Lookahead Sets* | **TOPLAS 4(1), 1982** | yacc 能稳定的理论保证 |
| Tomita, M.，*An Efficient Augmented LR Parser*（GLR） | **TOPLAS 8(4), 1986** | 通用 LR 解析 |
| Knuth, D. E.，*The Art of Computer Programming, Vol. 1: Fundamental Algorithms* | **1968 / 2nd ed. 1973** | 形式化算法与复杂度 |
| Johnson, S. C.，*Yacc: Yet Another Compiler-Compiler* | **UNIX Programmer's Manual, 1975** | LALR(1) 的工业标准实现 |
| Ford, B.，*Parsing Expression Grammars* | **POPL 2004** | LR 之外的第四条路 |

---

## 近年研究与工业界开源实践（2015–2026）

| 项目 | star（2026-09-25 实测） | 与本讲的关系 |
| --- | --- | --- |
| `antlr/antlr4` | **19,015★** | ALL(\*) = 运行期自适应 LL(\*)，本章 12.5 的「k 由工具决定」 |
| `lark-parser/lark` | **5,991★** | **同时支持 LALR 与 Earley 模式**，本章 12.10 最直接的对照物 |
| `tree-sitter/tree-sitter` | **27,046★** | 增量 LR(1)，「LR + 增量」的现代答案 |
| `google/re2` | star 未核验 | 线性时间正则引擎（本章 12.2 的正面样本） |
| `intel/hyperscan` | star 未核验 | 多模式正则匹配 |
| `antlr/grammars-v4` | **11,058★** | 上百种语言的现成语法，都是 LL/LR 的实例 |
| `dotnet/roslyn` | **20,688★** | 大型语言前端，LR 之外的工程选择 |
| `microsoft/Power-Fx` | **3,365★** | 小 DSL 的解析器规模极小，用不上 LR 也够 |

**2026 年的实用建议**：

1. **语法稳定、要求精确** → LALR（yacc/bison）或 ANTLR 4。
2. **语法还在变、想少改语法文件** → **Earley**（lark 的 earley 模式）。
3. **要 IDE 实时性** → **Tree-sitter**（增量 + 容错，坏输入也能出树）。
4. **只要一个表达式/配置解析** → PEG（lark / Chevrotain），比 LR 直观得多。

---

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「LL(1) 就是递归下降」 | 递归下降是**实现**，LL(1) 是**算法**；LL(1) 也可以表驱动非递归 |
| 2 | 「LR 一定比 LL 强」 | LR 能处理的文法多一些，但**错误信息质量更差、文法难写**；工程上常常 LL 更好 |
| 3 | 「First/Follow 不用手算，工具会算」 | 手算一次，才能读懂工具报的冲突信息；这是本章唯一必须动手的内容 |
| 4 | 「dangling else 是语法 bug」 | 它是**二义性**，需要语言设计决策（ANTLR 用改写优先级解决） |
| 5 | 「NFA 模拟就是回溯」 | 自动机型 NFA 模拟（并行状态集）是**线性**的；回溯型引擎才是指数 |
| 6 | 🔧 本课程未把 **Earley** 写进正文 | 2019 年的缺陷；2026 年必须补：任意文法、无需消除左递归、lark 的 earley 模式可直接用 |
| 7 | 🔧 未提 **GLR（Tomita）** | 通用 LR，冲突时并行展开，是 LR 家族的「兜底」算法 |
| 8 | 🔧 未提 **Tree-sitter 的增量解析** | 它把 LR(1) 做成增量的，是 2018 年之后最重要的解析工程进展 |
| 9 | 🔧 未提 **PEG 作为 LR 的替代品** | 有序选择 = 用书写顺序表达优先级，比 First/Follow 直观得多 |
| 10 | 🔧 未提 **ANTLR 4 的 ALL(\*) 与静态 LL(k) 的差别** | `adaptivePredict()` 是运行期按需扩展前看，代价是运行时开销、收益是语法更自由 |
| 11 | 🔧 未提 **LLM 写 LL/LR 语法的高频错误** | 左递归未消、漏提取左因子、dangling else；这三类错误本讲正好全覆盖 |

---

## 与其他章 / 其他书的联系

- **`02-正则文法和有限自动机.md`**：本章 12.1 是那章的「做成产品」版。
- **`03-语法分析入门.md`**：那章讲「怎么写语法」，本章讲「怎么让语法可执行且无歧义」。
- **`04-二元表达式与优先级.md`**：本章 12.3/12.4 的 First/Follow 正是为了讲清那章的分层文法为什么能工作。
- **`06-Antlr与前端工具.md`**：ANTLR 就是 LL(\*) 的工业实现，与本章 12.5 互相印证。
- **`16` 讲对应的正则工具**：正则引擎（RE2/hyperscan）可对照 `book/精通正则表达式.md`。
- **`book/现代编译原理-虎书.md`**：First/Follow、LL(1)、LR(1) 的分析表构造的理论权威版。
- **`book/Lex与Yacc.md`**、**`book/flex与bison中文版.md`**：yacc 的 `.y` 与 LALR 的完整用法。
- **`book/自动机理论、语言和计算导论.md`**：NFA/DFA/First/Follow 的形式化版本。
- **`book/计算机程序的构造和解释（原书第2版）/`**：SICP 的求值器里有 Earley 解析器的完整实现，是本章 12.10 最好的教材版。
- **`book/编程语言实现模式/02-基本解析模式.md`**、**`03-增强解析模式.md`**：P.1–P.7，模式化的解析算法。
