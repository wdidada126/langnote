# 第 1 章 构造过程抽象（1.1 与 1.2 前半：表达式、求值、抽象）

> **一句话**：程序是「表达式在环境里求值」的一件事，抽象就是把细节关进黑箱、只留下名字——**命名是程序员最根本的操作**。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 1.1.1 | 表达式 | `(+ 137 349)` 这样的**前缀组合式**是本书唯一的语法主场 |
| 1.1.2 | 命名和环境 | `define` 不是「赋值」，而是**在环境里建立名字到值的绑定** |
| 1.1.3 | 组合式的求值 | 求值 = 求各子表达式 → 将过程作用于实参； Lombard 街…（见 1.3） |
| 1.1.4 | 复合过程 | `(define (square x) (* x x))` 把「过程定义」与「过程调用」分开 |
| 1.1.5 | 代换模型 | 先把代换当**教学模型**用，后面 3.2 会把它推翻为环境模型 |
| 1.1.6 | 条件表达式和谓词 | `cond` / `else` / 谓词求值为真值而非布尔 |
| 1.1.7 | 实例：牛顿法求平方根 | 第一个真正「像样」的程序：迭代 + 容差收敛 |
| 1.1.8 | 过程作为黑箱抽象 | **局部性**：过程内部不该依赖外部名字 |
| 1.2.1 | 线性的递归和迭代 | 两者都是过程，区别在**解释器保留多少「待做事」的痕迹** |

---

## 核心精讲

> 以下全部是**教学示意代码，不参与构建、不编译、不运行**。

### 表达式与组合式

```scheme
; Scheme 只有一种复合表达式形式：组合式（operator operand ...）
(+ 137 349)                    ; ==> 486
(+ (* 3 5) (- 10 6))           ; ==> 19
(define pi 3.14159)            ; 定义：把值绑定到名字
(* pi (* 2 (/ 3 4)))           ; ==> 0.7853975 左右
```

要点：**前缀表示法 + 统一语法**，使得「数据即程序、程序即数据」在语法层面直接成立（这一点在 2.3 符号数据里被反复用到）。

### 命名与环境：别把 `define` 理解成赋值

```scheme
; define 在当前环境中建立「名字 → 值」的绑定
(define (square x) (* x x))    ; 语法糖，等价于
(define square (lambda (x) (* x x)))

(square 4)                     ; ==> 16
```

> 「环境」这个词在 1.1 只出现雏形，真正的**环境模型**在 3.2 才确立。这里只需记住：**名字不指向内存地址，而是指向环境里的一个绑定**。这也是 SICP 与 C 语言截然不同的心智模型。

### 代换模型（教学模型，不是实现）

```scheme
(define (f a b) (+ a (* b 2)))
(f 5 1)   ; 代换模型推演：
          ; (+ 5 (* 1 2))
          ; (+ 5 2)
          ; ==> 7
```

代换模型有两个致命缺陷，SICP 在 3.2 用环境模型正面回答：

1. 它假装**没有副作用**，但 3.1 引入 `set!` 后不再成立；
2. 它假装**过程没有状态**，但局部状态需要「每个调用各自一份」的环境才行。

### 条件与谓词

```scheme
(define (abs x)
  (cond ((< x 0) (- x))
        ((= x 0) 0)
        (else x)))

; 也可以用 if 表达
(define (abs2 x) (if (< x 0) (- x) x))
```

Scheme 的「真」是**非 #f 即真**，不做类型广播；`else` 是 `cond` 的默认分支。

### 牛顿法求平方根：本书第一个完整实例

```scheme
(define (sqrt-iter guess x)
  (if (good-enough? guess x)
      guess
      (sqrt-iter (improve guess x) x)))

(define (improve guess x)
  (average guess (/ x guess)))

(define (average a b) (/ (+ a b) 2))

(define (good-enough? guess x)
  (< (abs (- (square guess) x)) 0.001))

(define (sqrt x)
  (sqrt-iter 1.0 x))

(sqrt 2)   ; ==> 1.4142135623730951 左右
```

这里第一次显式呈现了 **1.2 节的核心张力**：`sqrt-iter` 是尾调用，但它写成递归形态却**消耗栈**（因为 Scheme 的解释器不保证尾调用优化）；第 2 章之后我们会用 `let` 与内部定义把它重构成真正的迭代。

### 黑箱抽象与局部性

```scheme
; 内部定义：把 sqrt 的所有辅助过程关进黑箱
(define (sqrt x)
  (define (improve guess) (average guess (/ x guess)))
  (define (good-enough? guess)
    (< (abs (- (square guess) x)) 0.001))
  (define (sqrt-iter guess)
    (if (good-enough? guess)
        guess
        (sqrt-iter (improve guess))))
  (sqrt-iter 1.0))
```

> 注意这里已经出现了「**块结构（block structure）**」的雏形，它是 2.4.4 / 3.2 环境模型的直接前身——**内部定义的 `x` 就是自由变量，靠外层环境保持绑定**。

---

## 版本演进

| 阶段 | 该阶段的关键差异 |
| --- | --- |
| **LISP 1.5（1960）** | 只有 S 表达式、`lambda`、`cond`、递归；没有词法作用域（动态作用域），没有尾调用保证 |
| **Scheme 1975（AI Memo 394）** | 引入**尾递归优化**与**词法作用域**，这是 SICP 全部代码能跑起来的两个前提 |
| **R5RS（1998）** | 统一 `let`/`let*`/`letrec`，明确 `#t`/`#f`，把 `define` 的内部定义写入规范，牛顿法那套写法基本可以直接照抄 |
| **R6RS（2007）/ R7RS-small（2017）** | 增加库系统、`define-record-type`、`let-values`；`#lang racket` 生态里 `define-struct` 取代了本书的 `(define (cons x y) ...)` 手工构造 |
| **Common Lisp 的分野** | CL 坚持**动态作用域 + 多重返回值 + 宏系统**，牺牲了「表达式即数据」的纯净性以换工程能力；SICP 选了另一侧，这是两种哲学，不是优劣 |
| **2026 现状** | 教学用 Scheme 基本被 Racket 吸收：`#lang racket` + `provide/require` 补上模块；`λ` 可由编辑器直接输入；`conduif` 等新语法 sugar 进入标准库 |

> **1996 → 2026 的语言发展**：静态类型（Typed Racket、Racket 的 `typed/racket`）、不可变数据结构（immutable hash、vector→persistent data structure）、尾调用在 **Java/Python 依然没有**——所以本书 1.2 节的尾递归讨论 **C/Java 程序员今天仍会踩坑**。

---

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| *The LISP 1.5 Programmer's Manual* | John McCarthy 等，CACM 3(4)，1960 | 定义 S 表达式、`lambda` 记号、`cond`、递归函数的可计算性；`eval` 的最早形态（后来成为 4.1 元循环求值器的原型） |
| *Recursive Functions of Symbolic Expressions and Their Computation by Machine, Part I* | McCarthy, CACM 4(1)，1961 | 提出 ** metacircular evaluator**（用 Lisp 写 Lisp 的解释器），SICP 第 4 章直接继承 |
| *Scheme: An Interpreter for Extended Lambda Calculus* | Sussman & Steele, AI Memo 394, 1975 | 尾递归 + 词法作用域的正式提出；把 1.1–1.2 的求值直觉从「代换」升级为「环境」 |
| *The Revised Report on the Algorithm Language Scheme* | Abelson & Sussman, SIGPLAN Notices 13(8)，1978 | 第一个标准化草案，确立 `lambda`/`define`/`cond` 的规范语义 |
| *The Art of the Interpreter* | Abelson, Sussman, Sussman, MIT AI Memo 505, 1982 | 把「解释器即抽象机器」讲成一条连续谱：求值器 → 非确定性 → 约束传播 → 编译器，SICP 第 3–5 章的骨架 |
| *The Concise Encyclopedia of Programming Languages* | John C. Reynolds, 2020（在线版） | 作为参照：从Algol 60 到 LaCroix 的语言谱系表，可用来定位 Scheme 在其中的坐标 |

---

## 近年研究与工业界开源实践（2015–2026）

**趋势**：SICP 的教学代码从「手写 `define` 的列表解释器」迁移到「Racket 的 `#lang` + 模块化 + 测试」；同时 JS/Python 生态补上了 Haskell/Scheme 早已普及的高阶函数与不可变数据。

| 仓库 | star | 说明 |
| --- | --- | --- |
| `racket/racket` | **5214★**（2026-09-25 实测） | 本书在现代的**默认替代品**：`#lang racket`/`#lang sicp`，SICP 题解与教学实现绝大多数跑在它上面 |
| `cisco/ChezScheme` | **7359★**（实测） | R5RS/R6RS 的高质量实现，本书代码最接近「原意运行」的引擎之一 |
| `clojure/clojure` | **10960★**（实测） | 函数式优先 + 宿主互操作，SICP 高阶思维在 JVM 上的主流落点 |
| `ocaml/ocaml` | **6575★**（实测） | 静态类型 + 表达式即值的混合，是「借鉴 Lisp 又不放弃类型」的代表 |
| `nginx/nginx` | **31729★**（实测） | 反向例证：C 写的高性能事件驱动服务器，说明本书的抽象观不等于性能观 |
| `nodejs/node` | **122077★**（实测） | JS 的 `(a => b => c)` 柯里化与 `map/filter/reduce` 直接对应 1.3 节 |
| `openjdk/jdk` | **23379★**（实测） | Java 至今**没有尾调用优化**，1.2 节的递归/迭代之争在 JVM 上依然是真问题 |
| `golang/go` | **138993★**（实测） |goroutine 是 CSP 思路，与本书 3.4 的「时间」主题有关联但机制完全不同 |
| `rust-lang/rust` | **119149★**（实测） | 所有权把 3.1 的共享状态问题在编译期解决，是 SICP 状态观的类型化版本 |
| `vsedach/Parenscript` | **251★**（实测） | Parenscript（Scheme → JS），本书高阶函数思想在 Web 前端的直系后代；仓库已标注迁往 GitLab，数字仅供参考 |

---

## 常见误区与本书需修正之处

| 问题 | 说明 |
| --- | --- |
| 🔧 **方言非标准** | 1.1 的代码用 MIT Scheme 旧写法（`define` 多重内部定义、`#t/#f` 混写、无模块），在 R5RS 严格模式下部分片段需要改写 |
| 🔧 **代换模型被当真** | 1.1.5 明确说「代换只是模型」，但有读者误以为 Scheme 真这么实现；3.2 会推翻它 |
| **前缀表达式误读为波兰式** | `(+ 137 349)` 不是「运算符在前的运算」，而是「一个由过程与实参组成的组合式」，这一层认知差是读 SICP 的第一道坎 |
| **「命名 = 赋值」的误解** | 在环境模型下 `define` 建立绑定；把它读作 C 的指针赋值会在 3.1 的 `set!` 处全面失控 |
| **局部状态缺失** | 1.1.8 只谈「黑箱」不谈状态，导致很多读者到 3.1 才第一次意识到「过程内部可以拥有可变状态」 |
| 🔧 **性能叙述过时** | 1.1.7 牛顿法的容差 `0.001` 在 1996 年的机器上合适，2026 年写 `1e-15` 更常见；但**迭代收敛的思想不过时** |
| 🔧 **未覆盖模块化** | 全书写到 2.5 也没有模块系统，`provide/require` 需要读者自行补上 |

---

## 与其他章 / 其他书的联系

- **→ 本目录 02 章**：1.2 讲透「递归 vs 迭代」，02 章做完整对照实验，专篇 `concepts/尾递归与迭代.md` 展开。
- **→ 本目录 11 章**：1.1.5 的代换模型在 4.1 被元循环求值器**重新实现**，同一套直觉两处印证。
- **↔ `book/代码整洁之道.md`**（*Clean Code*  Roberts 2008）：本书 1.1.8 的「局部性」原则与 Clean Code 的「封装」是同一件事的两面；SICP 更进一步给出**为什么**（因为状态与抽象边界会互相污染）。
- **↔ `book/编程语言实现模式.md`**（Parr）：3.2 的环境模型是典型的「树遍历 + 环境栈」，正是 Parr 说的 tree-walking interpreter；Parr 补上 book/符号表/作用域章节的工程细节。
- **↔ 静态类型与类型系统**：SICP 全书**没有类型**，它的抽象靠「约定」维持（2.1.3 干脆承认这点）。现代静态类型（Racket 的 `Typed Racket`、OCaml/Haskell）用签名替代了这些约定——**抽象屏障从「人的纪律」升级为「编译器的检查」**。想补这一课可看 *Types and Programming Languages*（Pierce, TAPL）。
- **↔ `book/离散数学及其应用（原书第8版）.md`**：1.2.3 增长的阶本质是离散数学的渐进分析；用离散数学的求和技巧可以直接推出 `fib` 的线性递归复杂度。
