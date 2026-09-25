# NJU 编译原理 — 论文与延伸阅读骨架

## 经典论文（编译课标准配置：龙书配套 + 关键专题）

| 论文 | 年份 | 与课程知识点的关系 |
| --- | --- | --- |
| Aho, Sethi, Ullman — *Compilers: Principles, Techniques, and Tools* | 1986/2006 | 理论主线总纲（龙书本身即"课程论文"） |
| Parr & Quattlebaum — LL(\*): The Foundation of the ANTLR Parser Generator | 2011 | 本课程核心工具的理论基础 |
| Parr — Adaptive LL(\*) Parsing: The Power of Dynamic Analysis | 2014 | ALL(\*) 无限前瞻机制详解 |
| Knuth — On the Translation of Languages from Postfix to Infix Expressions | 1965 | LR 解析理论开山 |
| Aho & Johnson — LR Parsing | 1959 | LALR 构造经典综述 |
| Allen — Program Statistics as a Guide to Optimization / Cocke & Allen — A Machine Program for Analysis | 1969/1970 | 数据流分析源头（L11/L13） |
| Cytron et al. — Efficiently Computing Static Single Assignment Form | 1991 | SSA 构造标准算法（L9/L12） |
| Chaitin et al. — Register Allocation via Spilling and Coloring | 1981 | 图着色寄存器分配（L12） |
| Briggs et al. — Color Through Potential Spills / Practical Register Allocation | 1994/2003 | 快排式/启发式 RA 工程化 |
| Cooper & Torczon — Engineering a Compiler（教材性补充） | 2011 | 与现代实践衔接 |

## 近 5 年论文（2021–2026）

| 论文 | 出处/年份 | 方向 |
| --- | --- | --- |
| CompCert 后端算术正确性（C--{} 机制） | POPL 2021 | 编译器翻译正确性验证 |
| TreeSitter: An Incremental Parsing Framework 相关生态研究 | arXiv/GitHub 2021-2024 | GLR 增量解析（对照 ANTLR 路线） |
| SSA-based 优化与 RA 的新求解（ILP/SMT）方向综述（如 RegAllocAI 后续） | CGO/TOPLAS 2021-2024 | 寄存器分配自动化/学习化 |
| MLIR 及其 dialect 演化系列 | PLDI/OOPSLA 2021-2025 | IR 设计的当代形态 |
| 国内系统能力大赛编译赛道教学与评测论文 | 计算机教育 2021-2024 | 课程评测体系参照 |

## 知识点在开源项目中的应用

| 知识点（本课程） | 开源项目 | 具体应用 |
| --- | --- | --- |
| LL/ALL(\*) 解析 | ANTLR 4、tree-sitter | 现代语言前端、编辑器语法高亮 |
| 语法制导翻译 | GCC 前端、Clang AST | AST 遍历与 Sema 阶段 |
| 三地址/SSA IR | LLVM IR、Rustc MIR | 中端 pass 的输入格式 |
| 数据流分析 | LLVM（Mem2Reg、GVN）、CodeQL | 可达定义/活跃分析驱动优化与安全查询 |
| 寄存器分配 | GCC（LRA）、LLVM FastRA | 图着色/线性扫描工业实现 |
| 符号表与类型检查 | OpenJDK javac | 作用域/类型推断管线 |
