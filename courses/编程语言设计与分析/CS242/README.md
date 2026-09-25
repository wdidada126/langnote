# Stanford CS242: Programming Languages（从理论到系统）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | Stanford CS242: Programming Languages |
| 学校 | 斯坦福大学（Stanford University） |
| 主讲 | Will Crichton（课程设计/授课） |
| 教材 | 前半：TAPL（Pierce, *Types and Programming Languages*）；后半无固定教材（课程笔记） |
| csdiy 路径 | https://csdiy.wiki/编程语言设计与分析/CS242/ （页面更新 2025-08-19） |
| 最新期次 | csdiy 链接为 2019 秋版本页面；作业仓库随讲师更新（2025-08 校订笔记） |
| 状态 | 🚧 骨架已建，逐讲正文待填充 |
| 先修要求 | 对计算机系统和编程语言理论有初步了解 |
| 实现语言 | OCaml、Rust |
| 预计学时 | 约 60 小时（csdiy 难度 ★×4） |

## 为什么学

- "理论驱动系统"的独特路线：Lambda 演算/类型系统不是终点，而是解释 Rust 所有权、线性类型、会话类型、异步系统的透镜。
- 作业工程量大且测试详尽（深度学习框架作业 200+ 测试），自学可验证性强。
- 主讲人教学理念成文：*From Theory to Systems: A Grounded Approach to Programming Language Education*（POPL 2024），课程即该论文的实现。
- 大作业四选一（Lean 证明/Rust RLU/F* 文件系统验证/OCaml 深度学习框架），直通 PL 系统与形式化验证前沿。

## 先修与知识联系

- **先修**：CS61A/CS110L 级；建议先修或并行 CS143（解释器/类型检查工程对照）。
- **互练**：Cambridge-Semantics（更纯理论的语义学入门）；NJU/PKU-SoftwareAnalysis（类型之外的"分析"半壁）；Rust 语言进阶。
- **知识映射**：L1-L4 ↔ TAPL ch5-ch11/ch18；L6-L8 ↔ Rust 参考书 + 线性类型文献；Wasm ↔ 官方规范与论文。

## 讲义章节目录（按 csdiy 作业序列整理；正式笔记以课程笔记为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论：为什么 PL 理论需要"落地" | 课程笔记 Lecture 1；From Theory to Systems 摘要 |
| L2 | JSON 的形式化与证明（HW1） | TAPL ch4-5（形式化方法） |
| L3 | Lambda 演算 | TAPL ch5-6 |
| L4 | 函数式编程入门：OCaml（HW2/HW3） | Real World OCaml 基础章 |
| L5 | 类型检查器与解释器：实现一个函数式语言（HW4） | TAPL ch9-11, ch18 |
| L6 | WebAssembly：理论与实践（HW5） | Wasm 规范；*Where's the Soundness* 论文 |
| L7 | 线性类型与 Rust 所有权机制（HW6） | Rust Book ch4, 10；线性逻辑文献 |
| L8 | Rust 异步编程（HW7） | Rust 异步 Book；tokio 文档 |
| L9 | 用类型系统设计状态机：session-typed TCP（HW8） | 会话类型经典（Honda 1993）；stakette/rusty_hoop 论文 |
| L10 | 大作业工作坊 I：Lean 定理证明 / F* 验证文件系统 | Lean 教程；F* 论文 |
| L11 | 大作业工作坊 II：Rust 实现 RLU 同步 / OCaml 深度学习框架 | RLU 论文；小 ML 反向模式 AD 文献 |
| L12 | 课程总结：PL 理论→系统设计的迁移图谱 | 课程笔记最后一讲 |

## 备注

- 作业编号以作业仓库为准；csdiy 提示作业偏难，属正常体验。
