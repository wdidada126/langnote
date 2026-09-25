# KAIST CS431 并发编程 (Rust)

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | KAIST CS431: Concurrent Programming |
| 学校 | KAIST |
| 主讲 | Jeehoon Kang（ku-ccamp 实验室） |
| 教材 | 课程自研 Slides；无出版教材 |
| csdiy 路径 | https://csdiy.wiki/编程入门/Rust/cs431/ （页面更新 2024-04-14） |
| 最新期次 | 秋季学期滚动开课（csdiy 收录时以最新官网 slides/作业为准） |
| 难度/学时 | 🌟🌟🌟🌟 / 约 50 小时 |
| 状态 | 骨架 |

## 为什么学

- 并发编程的深度课：理论部分建立并发情形下的编程模型（promising semantics、访存模型），实践部分吃透 Rust 相关库中锁与无锁数据结构的实现原理。
- 作业代码量不大但并不简单：从基于锁的并发安全 LRU 缓存与链表，到无锁哈希表和著名的 hazard pointer，全部配有详细本地测试，适合自学。
- 学完后，自旋锁/互斥锁只是起点：promising semantics、memory reclamation、无锁数据结构会让你对并发和 Rust 的理解超出大部分课程。

## 先修与知识联系

- 先修：Rust 编程基础（CS110L/cs220 级别）+ 对并发的初步了解。
- 联系：上承 CS110L 并发章节与 cs220 L10；下接 15-418/CS149 并行计算、MIT 6.824 分布式共识（并发错误的分布式放大）；访存模型与 CSAPP/体系结构课呼应；验证部分衔接 CS242/程序语言理论。

## 最新年份讲义章节目录（按官网 slides 主题，约 13–14 讲；以当期 syllabus 为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 导论：并发的困难与非确定性 | Slides 1 |
| L2 | 并发正确性概念：linearizability | Slides 2；Herlihy & Wing 1990 |
| L3 | 锁与临界区：spinlock/mutex/读写锁 | Slides 3；Rust std::sync |
| L4 | 内存模型 I：sequential consistency 与编译器/CPU 重排 | Slides 4；Adve & Gharachorloo 1996 |
| L5 | 内存模型 II：C11/Rust atomics、acquire/release | Slides 5；cppreference atomics |
| L6 | Promising semantics：并发语义的形式模型 | Slides 6；Kang et al. 2020 |
| L7 | 无锁算法 I：Treiber stack / Michael-Scott queue | Slides 7；经典论文两篇 |
| L8 | 无锁算法 II：CAS 循环与 ABA 问题 | Slides 8 |
| L9 | 内存回收：reference counting, EBR, hazard pointers | Slides 9；Michael 2004 |
| L10 | RCU 与读优化数据结构 | Slides 10；McKenney 文章 |
| L11 | 并发哈希表 | Slides 11；Flurry/Go map 对照 |
| L12 | 软件事务内存 (STM) | Slides 12；Herlihy et al. 1992 |
| L13 | 并发程序验证初步（Iris/证明思路，视当期） | Slides 13 |
| L14 | 复习与 project 展示 | Homework 冲刺 |
