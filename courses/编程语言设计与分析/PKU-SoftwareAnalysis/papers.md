# PKU 软件分析技术 — 论文与延伸阅读骨架

## 经典论文（分析 + 求解 + 合成三线）

| 论文 | 年份 | 与课程知识点的关系 |
| --- | --- | --- |
| Cousot & Cousot — Abstract Interpretation (POPL) | 1977 | L6 理论基石 |
| Reps, Horwitz & Sagiv — Precise Interprocedural Dataflow Analysis via Graph Reachability (POPL) | 1995 | L3 IFDS |
| Andersen — Pointer Analysis for C (PhD) | 1994 | L4-L5 包含式分析 |
| Steensgaard — Points-to Analysis in Almost Linear Time (POPL) | 1996 | L4 合一式对照 |
| Clarke — A System to Generate Test Data and Symbolic Execution (IEEE TSE) | 1976 | L9 符号执行源头 |
| Moskewicz et al. — Chaff: Engineering an Efficient SAT Solver (DAC) | 2001 | L7 CDCL 工程典范 |
| de Moura & Bjørner — Z3: An Efficient SMT Solver (CAV) | 2008 | L8 求解器核心文献 |
| Manna & Waldinger — Toward Automatic Program Synthesis (IJCAI) | 1971 | L10 演绎式合成源头 |
| Gulwani — Automating String Processing (POPL) | 2012 | L10-L12 PBE/字符串合成 |
| Alur et al. — Syntax-Guided Semantic Synthesis (CAV) | 2013 | L11 SyGuS 正式定义 |
| Jones & Stasko — Automatic Software Fault Isolation via Risk Program Execution (Tarantula) | 2002 | L13 频谱定位 |
| Ochiai et al. — Probabilistic Fault Localization (ICSE) | 2002 | L13 Ochiai 可疑度公式 |
| Le Goues et al. — Genetic Programming for Automatic Software Repair (TSE) | 2012 | L14 APR 代表作 |

## 近 5 年论文（2021–2026）

| 论文 | 出处/年份 | 方向 |
| --- | --- | --- |
| LLM 驱动的程序合成与修复（AlphaRepair 及后续） | ICSE/FSE 2021-2025 | L10/L14 新范式 |
| 可扩展指针分析新算法（Doop/Tai-e 性能线） | PLDI/SAS 2021-2024 | L4-L5 |
| 抽象解释数值域进展（非线性/浮点抽象） | CAV/SAS 2021-2024 | L6 |
| 学习型过程间分析与摘要压缩 | POPL/PLDI 2021-2024 | L3 |
| SyGuS-Comp 年度竞赛系列报告 | arXiv 2021-2024 | L11-L12 |

## 知识点在开源项目中的应用

| 知识点（本课程） | 开源项目 | 具体应用 |
| --- | --- | --- |
| 抽象解释 | Frama-C（value 分析）、Infer | C/Java 无误报验证 |
| 指针/数据流分析 | Soot、WALA、Tai-e、CodeQL | 程序属性推断底座 |
| SAT/CDCL | CaDiCaL、Kissat、Glucose | 约束编码求解 |
| SMT | Z3、CVC5、bitwuzla | 验证/合成/测试生成通用后端 |
| 符号执行 | KLEE、angr | 测试生成与漏洞挖掘 |
| 程序合成 | Rosette、CVC5-SyGuS、Excel FlashFill | DSL 自动化编程 |
| 缺陷定位/APR 评测 | Defects4J、QuixBugs | L13-L14 实验基座 |
