# NJU 软件分析 — 论文与延伸阅读骨架

## 经典论文（软件分析标准配置）

| 论文 | 年份 | 与课程知识点的关系 |
| --- | --- | --- |
| Cousot & Cousot — Abstract Interpretation: A Unified Lattice Model for Static Analysis (POPL) | 1977 | 静态近似的理论总纲 |
| Andersen — Pointer Analysis for C: Basics, Variants and Applications (PhD) | 1994 | L6 包含式指针分析圣经 |
| Steensgaard — Points-to Analysis in Almost Linear Time (POPL) | 1996 | L6 合一式对照 |
| Reps, Horwitz & Sagiv — Precise Interprocedural Dataflow Analysis via Graph Reachability (POPL) | 1995 | L10 IFDS 开山 |
| Grove, DeFouw, Dean & Chambers — Call Graph Construction in Object-Oriented Languages (ECOOP) | 2001 | L5 RTA 调用图 |
| Milanova, Rountev & Ryder — Context-Sensitive Pointer Analysis for Object-Oriented Languages (SAS) | 2005 | L7 上下文敏感 |
| Arzt et al. — FlowDroid: Precise, Context, Sensitive, Field, Object Sensitive Taint Analysis for Android | 2014 | L9 现代污点标杆 |
| Bravenboer & Smaragdakis — Strictly Declarative Specification of Points-to Analyses (Doop, OOPSLA) | 2009 | L6-L7 声明式分析 |
| Valle-Rai et al. — Soot: A Java Bytecode Optimization Framework | 1999 | L2/L12 工具生态 |

> 作者名单以正式引用核对为准；个别姓名待填充时补全。

## 近 5 年论文（2021–2026）

| 论文 | 出处/年份 | 方向 |
| --- | --- | --- |
| Tai-e: A Static Analysis Framework for Java (Wang et al., ISSTA) | 2022 | 课程作业框架本体 |
| 上下文/字段敏感指针分析的加速算法（Doop/Tai-e 后续） | POPL/SAS/ASE 2021-2024 | L6-L7 前沿 |
| LLM 辅助 source/sink 规范推断 | ICSE/FSE 2023-2025 | L9 自动化 |
| IFDS 可扩展性与摘要压缩 | PLDI/SAS 2021-2024 | L10 工程化 |
| 供应链/智能合约场景的污点与数据流分析 | S&P/CCS 2021-2024 | 应用面 |

## 知识点在开源项目中的应用

| 知识点（本课程） | 开源项目 | 具体应用 |
| --- | --- | --- |
| 数据流框架 | LLVM 数据流库、SootUp | 优化 pass 的通用骨架 |
| 调用图构建 | WALA、Soot（CHA/RTA/Spark） | Java 生态分析入口 |
| 指针分析 | Doop、Tai-e、Soot/Spark | 别名/可达性服务 |
| IFDS | FlowDroid、CodeQL（taint 查询底层思想） | 过程间污点传播 |
| 污点分析 | CodeQL 安全查询、商用 SAST | 漏洞挖掘产品化 |
| 抽象解释 | Astrée、Infer | 零误报方向工业应用 |
