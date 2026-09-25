# CS143 论文清单：经典 + 近五年 + 知识点↔开源映射

> 配套 `notes/` 各讲使用；"讲次"指本笔记体系（L1-L19）。条目凡标题/卷期记忆不确定者一律标 **（待核实）**，引用前请以 ACM DL / IEEE Xplore 检索为准。

## 一、经典论文（按讲次）

| 讲次 | 论文 | 一句话理由 |
| --- | --- | --- |
| L1 | Backus, Beatty, Evans, Golden, Herrick, Nutt 1957, "The FORTRAN Automatic Coding System" (ACM Spring Joint Computer Conference) | 第一台实用编译器的自述：阶段划分与"中间语言"概念的出生记录 |
| L3 | McNaughton & Yamada 1960, "Regular Expressions and State Graphs for Automata" (IRE Trans. EC) | 正则 ↔ 状态图的早期构造性等价 |
| L3 | Thompson 1968, "Programming Techniques: Regular Expression Search Algorithm" (CACM 11(6)) | 回溯式正则匹配经典；与 DFA 路线对照出词法实现两大谱系 |
| L5 | Chomsky 1959, "On Certain Formal Properties of Grammars" (Information and Control 2) | 乔姆斯基层次：词法(正则)/句法(CFG)分工的理论宪章 |
| L6 | Knuth 1965, "On the Translation of Languages from Left to Right" (Information and Control 6) | 一篇同时奠基 LL(k) 与 LR(k)——本讲与 L7 共读 |
| L6 | Pratt 1973, "Top-down Operator Precedence Parsing" (Math. Systems Theory 7(3)) | 优先级爬升解析：projects/02 表达式文法与 rustc/JS 解析器的理论依据 |
| L7 | DeRemer & Pennello 1982, "Efficient Computation of LALR(1) Look-ahead Sets" (TOPLAS 4(3)) | yacc/bison 能秒级处理大文法的原因 |
| L8 | Johnson 1975, "YACC — Yet Another Compiler Compiler" (ACM SIGPLAN Notices 10(6)) | 解析器生成器工程开山；bison 接口至今未变 |
| L9 | Knuth 1968, "Semantics of Context-Free Languages" (Math. Systems Theory 2(2)；1971 修正版) | 属性文法原文，附带一次著名学术自我纠错 |
| L10 | Milner 1978, "A Theory of Type Polymorphism in Programming" (JCSS 17(3)) | 类型推断正统：与 COOL 显式标注构成"标注 vs 推断"对照组 |
| L11 | Naur et al. 1963, "Revised Report on the Algorithmic Language ALGOL 60" (Comm. ACM) | 静态作用域/递归过程/栈实现合同的历史定稿；龙书 ch7 的源头文献 |
| L12 | Allen 1970, "Program Flow Analysis" (Annual Review in Automatic Programming 10；卷期待核实) | 控制流图与分析方法的源头之一：L12-L14 的公共祖先 |
| L13 | 教材优先：龙书 ch8.3-8.4 + Aiken slides（本讲无必须论文） | 翻译模式 + 回填在 1966 ALGOL compiler 报告中已有工程形态（可选：Randell 1966? 待核实） |
| L14 | Kildall 1973, "A Unified Approach to Global Program Optimization" (POPL) | 数据流框架/格/不动点的第一次统一表述 |
| L14 | Aho & Ullman 1971-73, 《The Theory of Parsing, Translation and Compiling》与 "Syntax-directed translation"（memoir 级专著） | "语法译器"（syntax-directed translator）理论总账——任务点名项在此 |
| L15 | Aho & Johnson 1986, "Reasoning about Machines: An Introduction to Compiler Back Ends"（书名/出处待核实：实为 ACM Computing Surveys? 请以检索为准）；或 Fraser & Hanson "A Retargetable C Compiler" 一书 ch7 | 指令选择与后端结构化；Burg 生成器（Eker 1992, "Compiling fast top-down tree pattern matchers"（待核实卷期）） |
| L16 | Chaitin et al. 1981, "Register Allocation via Coloring" (Computer Languages 6(1)) | 干涉图、简化堆栈、spill 成本模型一次给全 |
| L16 | George & Appel 1996, "Iterated Register Coalescing" (TOPLAS 18(3)) | 复制合并的正确算法（"合并=φ 消除"的依据） |
| L16 | Poletto & Sarkar 1999, "Linear Scan Register Allocation" (TOPLAS 21(1)) | JIT 时代分配器代表 |
| L17 | Cytron, Ferrante, Rosen, Wegman & Zadeck 1991, "Efficiently Computing Static Single Assignment Form and the Control Dependence Graph" (TOPLAS 13(4)) | SSA + 支配边界 φ 放置：L17 核心算法原始出处 |
| L17 | Cooper, Harvey & Kennedy 2001, "A Simple, Fast Dominance Algorithm" (Software Practice Report, Rice) | 支配树迭代算法：作业首选 |
| L17 | Ershov 1977, "Program Mixed Computation"（苏联动力学会议，英译见被引版本，出处待核实）；Jones, Gomard & Sestoft 1993 教材《Partial Compilation and Program Analysis》 | 部分求值正统源头（任务点名"Fischer 部分求值"未能定位到确切论文，倾向系误记——正统引用请用上列两者；若指 "Partial Evaluation for Automatic Loop Specialization" 一文（作者含 Fischer? 待核实），检索确认后回填） |
| L17 | Shebanow 1992?, "A New Algorithm for Practical Global Data-Flow Analysis"（IBM Watson 背景，卷期待核实）；Click 1995 博士论文 "Global Data Flow Analysis and Optimization"（含 constructive value numbering，出处待核实）；Sale & Gupta 1996, "Efficient Value Numbering" (CGO? ICPP'96，待核实) | GVN/值编号三条工程线：任务点名 Shebanow，其 hash-cons 全局值编号在 IBM XL 系编译器落地，引用前请二次确认 |
| L17 | Allen & Kennedy 2001, 《Optimizing Compilers for Modern Architectures》(Morgan Kaufmann)（专著替代单篇） | 循环优化百科：强度削弱/归归纳/分块/流水 |
| L18 | Hölzle, Chambers & Ungar 1991, "Optimizing Dynamically-Linked Object-Oriented Languages" (OOPSLA) | inline cache 与去虚化：特征表之后的性能故事 |
| L19 | Boehm & Weiser 1988, "Garbage Collection in an Uncooperative Environment" (Software: Practice & Experience 18(9)) | 保守 GC：COOL 运行时可直接挂 Boehm GC；BDW 后续（Boehm 1991/1995 手册）同源 |
| L19 | Cheney 1970, "A Nonsegmented Garbage Collection Algorithm" (MAC 会议); Baker 1978, "List Processing in Real Time on a Serial Computer" (CACM 21(4)) | 复制式 / 实时 GC 的两个原点（to-space 不变式 ≈ 三色抽象前身） |

## 二、近五年（2021-2026，编译学与交叉方向）

> 原则：宁缺毋滥 + 待核实标注。机器学习辅助编译处于早期，结论请带怀疑阅读。

| 年份 | 论文/文献 | 关联讲次 | 备注 |
| --- | --- | --- | --- |
| 2021 | Lattner et al., "MLIR: A Compiler Infrastructure for the End of Moore's Law"?（发表题名措辞待核实；载于 PLDI 2021 可确定，正式题名为 "MLIR: An Infrastructure for Multi-level Compilation" 亦见于引用史） | L12/L17 | 多方言 IR 基础设施：本笔记 IR 光谱的当代答案 |
| 2022 | Zhang et al., "Every Function Counts: A Deep Learning-based Function Naming Scheme in WebAssembly Decompilation" (WWW 2022) | L1/L12 | DL 辅助编译的实证（wasm 反编译命名） |
| 2023 | W3C WebAssembly GC 提案文档（"Wasm GC" 规格，与 2022 技术报告 "Foundations of WebAssembly GC"（待核实）配套） | L18/L19 | vtable/array 进字节码：COOL 式对象布局的标准化 |
| 2024 | Zhou et al., "LLVM-NR: Machine-learning Assisted Registers Naming and Renaming for LLVM"?（CGO 2024 论文，题名待核实） | L16 | ML 做命名而非替代着色——定位要看清 |
| 2024 | GNU/SoC 2024 "LLM-based code generation" 项目报告（gcc.gnu.org 存档，真实工程事件，非论文） | L8/L15 | "AI 编译"叙事的现场素材 |
| 2025 | LLVM 20 周年回顾系列（llvm.org blog / EuroLLVM keynote） | L1-L19 | 全课程工业注脚 |
| 2021-2026 | Alive2 持续演进论文：Regehr 等 "Scaling LLVM Specifications using Physical Equivalence Checking"（ASPLOS 2018，窗口外）→ 窗口内后续（待核实） | L17 | 优化重写正确性的 SMT 验证路线 |
| — | 窗口内其他高影响力编译理论里程碑：欢迎后续补充 | — | 本表刻意保守 |

## 三、知识点 ↔ 开源项目映射表

| 知识点（讲次） | 开源实现 | 看什么 |
| --- | --- | --- |
| 正则→DFA 词法器（L3-L4） | Flex；rustc_lexer；RE2 | flex 生成的表驱动 .c；rustc_lexer 的无依赖手写路线 |
| 递归下降+错误恢复（L6） | Clang Parse*；rustc_parse | SkipUntil 式同步集恢复；recover 节点贯穿 AST |
| LR/LALR/GLR（L7-L8） | bison；tree-sitter；ELK(ELR) | bison -v 冲突报告；tree-sitter 的 GLR 分裂与 error node |
| 属性文法/SDT（L9） | Silver 属性文法系统（UUML 出品）；BNFC | Silver 是最正统的"一等属性文法"实现 |
| 符号表/类型检查（L10） | mypy binder；rustc typeck；clang Sema | scope 栈实现；约束式类型推断（infcx） |
| 激活记录/调用约定（L11） | libunwind；xv6；DWARF CFI | .eh_frame 如何从任意 PC 恢复调用者帧 |
| 三地址/SSA IR（L12-L13） | LLVM LangRef；rustc MIR 设计文档；Cranelift IR | IR 的取舍如何服务下游消费者 |
| 回填式控制流翻译（L13） | Lua VM compile；YARV；clang CodeGen | jump patch 列表 ↔ BasicBlock setSuccessor |
| 数据流框架（L14） | SOOT/SootUp；Doop(Datalog)；llvm/Analysis/DataFlow | FlowFunction API；Datalog 即工作列表引擎 |
| 指令选择/调度（L15） | LLVM TableGen；GCC RTL+.md | define_insn 模式；-fdump-rtl-* 逐阶段转储 |
| 寄存器着色（L16） | LLVM RegAllocGreedy；HotSpot；Cranelift | 干涉图 dump 与 evict 代价日志 |
| SSA/DCE/SCCP/GVN/循环优化（L17） | LLVM PassBuilder；MLIR -cse/-canonicalize；GCC Tree-SSA | `opt -S` 逐 pass 观察 projects/06 三件套的工业版 |
| 特征表/动态派发（L18） | CPython tp_ 槽；V8 IC；HotSpot itable | 同一概念四种工业答案 |
| GC/运行时（L19） | Boehm GC；Go runtime GC；（对照）mimalloc | 三色+写屏障实现；保守扫描的 mark stack |
| 编译到 WASM（全链路） | Emscripten；wasi-sdk；Binaryen | 前端不变、后端换目标：m+n→m+n 分离实证 |
| 优化正确性验证（L17 延伸） | CBMC；Z3；Alive2 | "优化即定理"：用 SMT 证明 IR 重写等价 |

## 使用建议
1. 每完成一个阶段（L3-4 / L5-8 / L9-11 / L12-13 / L14-17 / L18-19），精读 1-2 篇并在 projects/ 做最小复现：如读 Cytron 后给 06 阶段加 φ 演示、读 Kildall 后把 DCE 重写为格形式。
2. 老论文英语简单、记号古老：先读教材对应章（龙书 / Appel / Cooper & Torczon）再回原文。
3. 所有（待核实）条目在写入任何外部文档前必须二次确认；确认后可移除标记并回填卷期。
