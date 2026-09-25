# Cambridge: Semantics of Programming Languages（剑桥编程语言语义学）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | University of Cambridge — Semantics of Programming Languages（Part IB） |
| 学校 | 剑桥大学 |
| 主讲 | 剑桥计算机系语义教学团队（以 Winskel 教材为纲；csdiy 页未列具体姓名） |
| 教材 | Winskel, *The Formal Semantics of Programming Languages* (1993)；Pierce, *Types and Programming Languages* (2002) |
| csdiy 路径 | https://csdiy.wiki/编程语言设计与分析/Cambridge-Semantics/ （页面更新 2024-05-21） |
| 最新期次 | 课程官网 Latest 页（含公开 YouTube 完整录像） |
| 状态 | 🚧 骨架已建，逐讲正文待填充 |
| 先修要求 | 基础离散数学 |
| 实现语言 | OCaml/ML（练习性） |
| 预计学时 | 20-30 小时（csdiy 难度 ★×3） |

## 为什么学

- 极少数有完整公开视频的 PL 理论课，入门"形式语义"这条最难自学路线的最优解。
- 从操作语义一路到指称语义：BNF 小语言、规则归纳证明、类型安全、域与不动点、并发互模拟——20 学时覆盖语义学全家桶。
- 是类型理论、范畴论、霍尔逻辑、模型检测四大后续方向的公认前置课。
- 体量小、密度高：适合与 CS242/PKU/NJU 分析课并行，为"程序分析为什么正确"补上理论地基。

## 先修与知识联系

- **先修**：离散数学（归纳法、关系、偏序/格初步）。
- **互练**：CS242（L2-L5 与本课程 λ/类型部分强重叠，可互相印证）；软件分析两门课（格的不动点 ↔ 数据流分析理论）。
- **知识映射**：Winskel 书 ch1-2（操作语义）→ ch3-4（类型/可靠性）→ ch5-8（指称语义）→ ch9-11（公理化/并发）。

## 讲义章节目录（按课程公开录像与 Winskel 教材整理；填充时对照官网 Lecture Notes）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 导论：语义是什么；简单命令式语言与 BNF | Winskel ch1 |
| L2 | 结构归纳与规则式定义 | Winskel ch2 前半 |
| L3 | 大步操作语义（自然语义） | Winskel ch2 |
| L4 | 小步操作语义；确定性与抽象机 | Winskel ch2 |
| L5 | 静态语义 I：类型系统的规则化定义 | Winskel ch3 |
| L6 | 静态语义 II：类型安全（soundness）证明套路 | Winskel ch3；TAPL ch1 |
| L7 | λ 演算与函数式视角下的数据 | Winskel ch4；TAPL ch5 |
| L8 | 子类型与多态初步 | TAPL ch15-16 选读 |
| L9 | 指称语义 I：偏序、单调/连续函数与格 | Winskel ch5-6 |
| L10 | 指称语义 II：不动点定理与 while 循环 | Winskel ch7-8 |
| L11 | 语义等价与全抽象（full abstraction）直觉 | Winskel ch9 延伸 |
| L12 | 并发语义与互模拟（bisimulation） | Winskel ch9-11 节选 |
| L13 | 总结：三大语义范式对照与后续路线（霍尔逻辑/模型检测/范畴） | 课程讲义末讲 |

## 备注

- Cambridge 内部 supervision 题与答案不公开；考试真题汇总见 csdiy 链接，笔记填充时把每讲对应真题列入"练习"栏。
