# 第 14 章 代码优化、数据流分析与 LLVM 生态（讲 25、27、28、31、34、35 及第三部分主题）

> **一句话**：优化的唯一准则是「**不改变观察得到的行为**」；所有优化 pass 都建立在同一件事上——**你比程序员更懂他的程序**（数据流分析）。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 14.1 | 优化的分类（讲 27） | 独立于机器 vs 依赖于机器（课程原摘录已记） |
| 14.2 | 常量折叠与死代码消除 | 最基础的两种优化 |
| 14.3 | SSA：优化的地基 | phi 节点、支配树 |
| 14.4 | 数据流分析（讲 28） | 本地分析 / 全局分析 / 不动点法（原摘录已记） |
| 14.5 | 常见全局优化 pass | CSE、DCE、内联、循环不变量外提、向量化 |
| 14.6 | LLVM 工具链（讲 25） | clang / opt / pass 管理 / 调试技巧 |
| 14.7 | 讲 31 内存计算 | 向量化、缓存、SIMD 与并行 |
| 14.8 | 讲 34 JIT | 运行时优化：为什么运行时能比编译时更聪明 |
| 14.9 | 讲 35 答疑 | 后端真的比前端难吗 |
| 14.10 | AI 编译器与 WASM（2026 必修） | TVM / MLIR / Triton / TorchInductor / wasmtime |

---

## 核心精讲

### 14.1 优化的两类（课程原摘录）

用户原摘录里已经记了这个划分，这里展开：

> 优化工作又分为「**独立于机器的优化**」和「**依赖于机器的优化**」两种。
> **独立于机器的优化** 不依赖硬件特征，在 IR 上做，因此可以被多目标复用；
> **依赖于机器的优化** 依赖硬件特征：寄存器优化、充分利用高速缓存、并行性、流水线、指令选择。

| 独立于机器（IR 层，可移植） | 依赖于机器（后端层） |
| --- | --- |
| 常量折叠、常量传播 | 寄存器分配 |
| 死代码消除 | 指令选择 / 指令调度 |
| 公共子表达式消除（CSE） | 缓存行对齐与预取 |
| 循环不变量外提（LICM） | SIMD 向量化（AVX/NEON/RVV） |
| 内联 | 流水线调度 |
| 无用代码消除 | 分支预测提示 |

### 14.2 两种最简单的优化

```c
// 教学示意：常量折叠（不参与构建、不编译、不运行）
// 前：         后：
// a = 3 * 5;   a = 15;
// b = a + 2;   b = 17;
```

```c
// 教学示意：死代码消除（不参与构建）
// 前：                 后：
// if (false) x = 1;    // 整块消失
// y = 2;               y = 2;
```

**为什么这两个这么重要？** 因为它们是所有其他优化的基础：常量传播能打开更多优化机会，死代码消除能让「无用的计算」不白跑。

### 14.3 SSA：让优化变简单的那一步

```text
// 教学示意：把普通 IR 转成 SSA（不参与构建）
// 前（非 SSA，同一个变量被多次赋值）
    y = 1
    y = 2
    x = y + 1
// 后（SSA，每个变量只赋值一次；歧义处用 phi 合并）
    y_1 = 1
    y_2 = 2
    x_1 = y_2 + 1
// 若控制流合并：
    if (c) y_1 = 1; else y_2 = 2;
    y_3 = phi(1, 2)        // 取决于走哪条分支
    x_1 = y_3 + 1
```

SSA 的三个好处：

1. **定义即使用**：一个变量的定义点唯一，生命周期清晰。
2. **常量传播变成简单的赋值传播**。
3. **无用代码消除变成「删除未被使用的定义」**，不需要做任何别名分析。

**支配树（Dominator Tree）** 是 SSA 上的核心工具：`domp(a, b)` 表示「从入口到 `b` 的任何路径都必经 `a`」，这是做循环优化与安全性的前提。

### 14.4 讲 28：数据流分析

课程原摘录记了三个术语，这里是它们的标准形式：

> 全局分析 / 本地分析 / 不动点法

```python
# 教学示意：一个数据流分析 pass 的骨架（不参与构建）
# 方向：前向（forward）
# 传递函数：OUT = f(IN) = gen ∪ (IN \ kill)
IN[entry]   = {}                       # 入口的初始集合
IN[b]       = OUT[preds(b)] 的并集    # 交汇运算（ Meet ）：前向用 ∪，后向用 ∩
OUT[b]      = transfer(b, IN[b])       # 每个块内部按语句顺序跑
# 反复迭代直到所有 IN/OUT 不再变化 —— 这就是「不动点法」
```

| 分析 | 方向 | 交汇运算 | 用途 |
| --- | --- | --- | --- |
| **可用表达式（Available Expressions）** | 前向 | 交 | CSE |
| **活跃变量（Liveness）** | 后向 | 并 | 寄存器分配、DCE |
| **可到达定义（Reaching Defs）** | 前向 | 并 | 常量传播 |
| **常量传播** | 前向 | 交 | 打开其他优化 |

**不动点法为什么一定收敛？** 因为传递函数是单调的，且集合的定向有限（最多 |变量| × |位宽| 步）。这也是为什么 LLVM 里的 pass 都要求「instruction is monotone」。

### 14.5 常见全局优化 pass

```
; 教学示意：一个循环优化的 LLVM IR 片段（不参与构建）
; 优化前：循环体内每次都重算
for (i = 0; i < 1000000; i++) sum += a[i] * k;
;
; 优化后（LICM：k 提到循环外；向量化：4~8 路并行）
```

| Pass | 作用 | 风险 |
| --- | --- | --- |
| **CSE** | 消除重复计算 | 需要别名分析，别名分析错了就会改错行为 |
| **DCE** | 删除无用代码 | 要小心有副作用的调用（`printf`） |
| **Inline** | 内联展开 | 代码膨胀、编译时间变长 |
| **LICM** | 循环不变量外提 | 需要处理内存别名与异常路径 |
| **GVN** | 全局值编号 | 消除语义相同的表达式 |
| **Vectorize** | 自动向量化 | 浮点重排可能有精度差异（需 fast-math） |
| **InstCombine** | 指令级简化 | 组合子优化，收益常被低估 |

> **一条重要的工程经验**：优化 pass 的正确性风险远比收益风险大。LLVM 有 `FileCheck` 与完整的回归测试，任何「看起来很聪明」的优化都应该先用 `opt` 验证。

### 14.6 讲 25：LLVM 工具链

```bash
# 教学示意：LLVM 常用命令（不参与构建，仅命令示例）
clang -S -emit-llvm fib.c -o fib.ll        # 生成人类可读的 IR
opt -passes='instcombine,gvn' fib.ll -S    # 跑指定的优化 pass
llc fib.ll -o fib.s                        # IR -> 汇编
clang fib.s -o fib                         # 汇编 -> 可执行文件
opt -passes='print<domtree>' fib.ll        # 打印支配树，调优化时最有用
```

**调试优化的三件套**：

| 手段 | 用途 |
| --- | --- |
| `-Rpass=xxx` | 查看哪些循环被向量化成功 |
| `-Rpass-analysis=xxx` | 看分析为什么失败 |
| `print<domtree>` / `breakpoint` | 插入调试 pass 观察 IR |

### 14.7 讲 31：内存计算——对海量数据做计算可以有多快

这一讲的落点是**内存墙**：CPU 越来越快，内存越来越跟不上。于是优化的重点变成「**让数据离 CPU 更近**」：

```c
// 教学示意：缓存友好 vs 缓存不友好（不参与构建）
// 不友好：按列遍历二维数组，每次都跨缓存行
for (int i = 0; i < N; i++) sum += a[i][j];
// 友好：按行遍历
for (int i = 0; i < N; i++) sum += a[i][j];
```

| 手段 | 效果 |
| --- | --- |
| 循环分块（Loop Tiling / Blocking） | 提高缓存命中率 |
| 向量化（SIMD） | 一条指令处理多个数据 |
| 预取（Prefetch） | 掩盖内存延迟 |
| 数据布局重构（SoA→AoS） | 让需要的字段连续 |
| NHive / 列式存储 | 内存计算引擎（DuckDB、Velox）的看家本领 |

### 14.8 讲 34：运行时优化（JIT）

JIT 的核心洞察是：**运行时的信息比编译时更多**。

```java
// 教学示意：JIT 的典型结构（不参与构建）
// 1. 解释执行，同时做「性能计数」
// 2. 某个方法超过阈值 -> 触发编译
// 3. 用运行期 profiler 数据（哪个分支最热、动态类型只有一个吗）优化
// 4. 生成优化后的机器码，换掉解释入口
// 5. 去优化（deoptimization）：假设不成立时回退到解释器
```

**JIT 能做到的三件编译期做不到的事**：

| 运行时信息 | 带来的优化 |
| --- | --- |
| 实际动态类型只有一个 | **去虚化（devirtualization）** + 内联 |
| 某个分支执行了 99% | 分支布局优化 |
| 数组从未越界（边界检查已证明） | 删除边界检查 |

> 第 1 条是最大的收益来源：**Java 的 C2/C1、HotSpot 的_inline caches_ 都靠它**。

### 14.9 讲 35 答疑：后端真的比前端难吗？

课程讲 35 的标题就是这个。一个诚实的判断：

| | 前端 | 后端 |
| --- | --- | --- |
| 概念数量 | 多但彼此独立 | 少但彼此耦合 |
| 正确性要求 | 「能解析」是软要求 | 「不改行为」是硬要求 |
| 可验证性 | 容易（错误信息对不对） | 难（优化对不对要跑测试） |
| 学习曲线 | 平缓 | 陡峭 |

**结论**：前端难在「面广」，后端难在「容错为零」。课程把它们分成两个模块，是因为**前端的收益更快、更可复用**（对应讲 14/15 的两个业务案例），而后端是「投入产生比递减」的一段。

### 14.10 AI 编译器与 WASM：2026 年必须补的一块

课程第三部分（36–45 讲，主题为「AI 与编译技术」）在 2019 年只是一个趋势展望，到 2026 年它已经是一条完整的产业主线。

| 方向 | 代表 | 核心思想 |
| --- | --- | --- |
| **自动调优编译器** | `apache/tvm`（**13,778★**） | 用 AutoTVM/Autoscheduler 搜索最优调度参数 |
| **多层 IR** | `llvm/mlir`（在 `llvm/llvm-project`，**40,652★**） | 每层 dialect 各管一层抽象 |
| **GPU DSL** | `triton-lang/triton`（**20,239★**） | 用 Python 写 kernel，编译器负责向量化/共享内存 |
| **框架内置 codegen** | `pytorch/pytorch`（**103,293★**，TorchInductor） | 把 torch 算子图编译成 Triton/C++ |
| **WASM 运行时** | `bytecodealliance/wasmtime`（**18,657★**） | 沙箱 + JIT + 增量 |
| **C/C++ 到 WASM** | `emscripten-core/emscripten`（**27,631★**） | LLVM 后端换目标即可 |
| **WASM 优化器** | `WebAssembly/binaryen`（**8,638★**） | wasm-opt 做 SSA 级优化 |

> **一个统一的观察**：AI 编译器做的事，和本章讲的所有 pass 是同一套——**都建立在「IR + 数据流分析 + 改写」这三件事上**。区别只是 IR 从「三地址码」变成了「计算图」。

---

## 版本演进

| 年份 | 事件 |
| --- | --- |
| 1960 | Dijkstra 的寄存器分配与最优代码生成思考 |
| 1973 | Kildall，不动点法做数据流分析（POPL） |
| 1970s | 窥孔优化（peephole）在 B 语言编译器里成型 |
| 1979 | **GCC** 发布；后端架构定型 |
| 1987 | **SGI/ MIPS 的优化编译器**把指令调度做成流水线感知 |
| 1990s | **SUIF**、**OPT** 等研究用优化器；并行化编译器兴起 |
| 1993 | **Polaris** 编译器做循环变换，LICM 成熟 |
| 2000 | **Intel Compiler** 把自动向量化做成卖点 |
| 2002 | LLVM 的前身研究启动 |
| 2004 | **LLVM** 第一版（Lattner & Adve，CGO 2004） |
| 2008 | LLVM 1.0 发布；**Open64** 等开源优化器并存 |
| 2011 | **LLVM 的 SSA 中端**成为主流 |
| 2015 | **LLVM 3.6 引入 MachineScheduler**，机器级指令调度成为独立 pass |
| 2017 | **MLIR 项目启动**（Google）；WebAssembly 论文 |
| 2018 | **TVM**（OSDI 2018）；MLIR 进入 llvm-project |
| 2019 | 本专栏上线，讲 27/28 讲优化与数据流分析 |
| 2020 | **MLIR 白皮书**；LLVM 12 |
| 2021 | MLIR 正式进入 `llvm-project`（CGO 2021） |
| 2022 | **PyTorch 2.0** 引入 TorchInductor |
| 2023 | Triton 成为 GPU kernel 的主流 DSL |
| 2024 | LLM 辅助优化 pass 的实验开始出现 |
| 2025–2026 | **多层 IR 是主流架构**；WASM 在服务端/边缘规模化落地 |

---

## 经典论文与原始文献

| 文献 | 出处 | 与本讲的关系 |
| --- | --- | --- |
| Kildall, G. A.，*A Unified Approach to Global Program Optimization* | **POPL 1973** | 不动点法与数据流分析的起点 |
| Hecht, M. S. & Ullman, J. D.，*Flow Graphs and Elimination Algorithms* | **SIAM J. Comput. 6(3), 1977** | 数据流分析算法 |
| Knoop, J., Rüthing, O. & Steffen, B.，*Partial Dead Code Elimination* | **PLDI 1994** | 一种「不引入 phi 也能做 DCE」的优化 |
| Braun, M. 等，*Simple and Efficient Construction of SSA Form* | **CC 2013** | SSA 线性时间构造，LLVM 现在用的 |
| Chaitin, G. J. 等，*Register Allocation and Spilling via Graph Coloring* | **PLDI 1989** | 图着色分配 |
| Poletto, M. & Sarkar, V.，*Linear Scan Register Allocation* | **TOPLAS 19(5), 1997** | 线性扫描 |
| Lattner, C. & Adve, V.，*LLVM: A Compilation Framework for Lifelong Program Analysis and Transformation* | **CGO 2004** | LLVM 的奠基论文 |
| Lattner, C. 等，*MLIR: A Compiler Infrastructure for the End of Moore's Law* | **arXiv 2002.02103, 2020** | 多层 IR 的代表文献 |
| Chen, T. 等，*TVM: An Automated End-to-End Optimizing Compiler for Deep Learning* | **OSDI 2018** | 自动调优编译器 |
| Tillet, B. 等，*Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations* | **ACM MAPL 2019** | GPU kernel DSL |

---

## 近年研究与工业界开源实践（2015–2026）

| 项目 | star（2026-09-25 实测） | 与本讲的关系 |
| --- | --- | --- |
| `llvm/llvm-project` | **40,652★** | 本章所有 pass 的「现实版」 |
| `llvm/mlir` | 无独立仓库（在 `llvm-project` 内） | 多层 IR |
| `apache/tvm` | **13,778★** | 自动调优编译器 |
| `triton-lang/triton` | **20,239★** | GPU DSL |
| `pytorch/pytorch` | **103,293★** | 内含 TorchInductor |
| `bytecodealliance/wasmtime` | **18,657★** | WASM JIT 运行时 |
| `emscripten-core/emscripten` | **27,631★** | C/C++ → WASM |
| `WebAssembly/binaryen` | **8,638★** | wasm-opt |
| `rust-lang/rust` | **119,157★** | 自举 + LLVM 后端 |
| `ziglang/zig` | **43,306★** | 自举 + 交叉编译 |
| `vlang/v` | **37,912★** | 小型自举编译器 |
| `oracle/graal` | **21,715★** | **多语言 JIT 互操作**的工业范本 |
| `dotnet/roslyn` | **20,688★** | RyuJIT 后端 |

**2026 年的三条尾巴**：

1. **AI 编译器是这块最大的增量**：TVM/MLIR/Triton/TorchInductor 把「优化 pass」的目标从 CPU 指令换成了「计算图 + kernel」。
2. **WASM 从浏览器走向服务端**：`wasmtime` 让「编译一次、到处运行」重新有了沙箱语义。
3. **LLM 进入编译优化**：用模型预测内联决策、寄存器分配顺序、调度优先级，是 2024 年之后活跃的实验方向（仍是研究阶段，不是生产实践）。

---

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「优化就是让代码更快」 | 首要约束是**不改变可观察行为**；任何优化都要能被测试反驳 |
| 2 | 「常量折叠一定能做」 | 需要常量传播 + 别名分析；跨过程优化更难 |
| 3 | 「SSA 只是命名规范」 | 它是**优化的地基**：支配树、phi、常量传播全建立在它上面 |
| 4 | 「不动点法只是理论」 | LLVM 的每个数据流 pass 都是它；不了解单调性就会写出死循环 |
| 5 | 「JIT 一定比 AOT 快」 | JIT 有编译开销；它赢在「用运行时信息做更好的优化」 |
| 6 | 🔧 本课程 2019 年上线，第三部分对 **MLIR** 几乎空白 | 2026 年必须补：多层 IR 是这一章最大的过时点（本章 14.10） |
| 7 | 🔧 未提 **AI 编译器**的真实主线 | 必须补：TVM / MLIR / Triton / TorchInductor 四条线，讲 14/15 的技术在这四条线上全部复用 |
| 8 | 🔧 未提 **WASM** 作为 IR 目标与运行时 | `bytecodealliance/wasmtime` + `emscripten-core/emscripten` + `WebAssembly/binaryen` |
| 9 | 🔧 未提 **GraalVM 的多语言 JIT** | `oracle/graal` 是「一个 JIT 服务多种语言」的最佳样本 |
| 10 | 🔧 未提 **自动向量化的浮点精度问题** | `-ffast-math` 与 `-Rpass=loop-vectorize` 的取舍，是工程上最常被忽视的坑 |
| 11 | 🔧 未提 **LLM 在编译优化中的实验性应用** | 内联决策、调度优先级预测；目前是研究阶段，不要写进生产假设 |

---

## 与其他章 / 其他书的联系

- **`13-中间表示与目标代码生成.md`**：那章讲「怎么生成 IR」，本章讲「怎么改 IR」；两者以 IR 为界。
- **`11-前端技术应用.md`**：本章 14.5 的 pass 在讲 11 的报表工具里已经小规模出现过（谓词下推、列裁剪）。
- **`10-继承与多态.md`**：14.8 的去虚化需要那章的虚表知识。
- **`07-作用域与生存期.md`**：14.5 的活跃变量分析是那章符号表的动态版本。
- **`book/现代编译原理-虎书.md`**：数据流分析与优化的理论权威版。
- **`book/高级编译器设计与实现.md`**（原 *Optimizing Compilers for Modern Architectures*，同级有 `OptimizingCompilersforModernArchitectures.md`）：循环优化与并行化的深入版。
- **`book/LLVM编译器原理与实践.md`**、**`book/深入理解LLVM.md`**、**`book/LearnLLVM17.md`**：LLVM 的系统性读物。
- **`book/TVM编译器原理与实践.md`**（同级单文件笔记）：本章 14.10 的 AI 编译器部分的最佳延伸。
- **`book/深入理解JVM.md`**：JIT 与 GC 的真实实现（讲 34/33 的完整版）。
- **`book/汇编语言4.md`**：指令调度与流水线相关。
- **`book/性能之巅.md`**：从系统层看内存墙，与本章 14.7 互补。
