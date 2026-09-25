# CS431 参考文献与开源应用（骨架）

## 经典论文 / 文献

| 文献 | 作者/年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| Linearizability: A Correctness Condition for Concurrent Objects | Herlihy & Wing, 1990 | L2 | 并发正确性金标准 |
| Sharing Memory Efficiently (Relaxed Consistency) | Adve & Gharachorloo, 1996 | L4 | 程序员/编译器/硬件三方契约的 relaxed consistency 定义 |
| Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms | Michael & Scott, PODC 1996 | L7 | MS 队列原始论文 |
| Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects | M. Michael, TOCS 2004 | L9 | csdiy 点名"著名的 hazard pointer" |
| Memory Management for Concurrent Concurrent Data Structures (博士论文, EBR) | T. Fraser, 2004 | L9 | Epoch-Based Reclamation 出处 |
| What Is an RCU? | P. McKenney, 内核白皮书 | L10 | RCU 设计说明 |
| Software Transactional Memory (STTM) | Guerraoui, Kapalka, Vitek? 稳妥取: Herlihy & Moss 1998 (HOTS) | L12 | TMS/STM 概念源头 |
| Promising Semantics | Kang, Kim, Vafeiadis (ESOP 2017) / POPL 2020 journal 版 | L6 | 课程招牌理论 |

## 近 5 年文献 / 资料（2021–2025）

| 资料 | 年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| Promising Semantics 后续工具与修订（PromisingCoq 等） | 2021–2023 | L6 | 课程特色理论的最新演进 |
| Tree Borrows: A New Alias Policy for Rust | Jung et al., 2023 | L5/L6 | Rust 别名/并发语义新提案 |
| crossbeam / flurry / arc-swap 文档与版本演进 | 2021–2025 | L9/L11 | 课程作业知识点的库化现状 |
| 并发 bug 实证研究（ASPLOS/OSDI 近年的 memory-model bug 挖掘工作） | 2021+ | L1/L4 | 弱内存序真实案例库 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 锁 + LRU | moka (Rust 缓存库) | 分段锁并发缓存设计 |
| 无锁队列 | crossbeam-queue | MS queue 的 Rust 实现 |
| Hazard pointers / EBR | crossbeam-epoch / Flurry | 双回收策略对照 |
| RCU | Linux 内核；用户态 userspace-rcu | 读多写少结构的极致优化 |
| 并发哈希表 | folly ConcurrentHashMap / DashMap | 课程 HW 哈希表的工业对照 |
| 内存序实践 | Tokio / rayon | ordering 选择的工程样本 |
| 形式验证 | Iris (Coq) / verus (Rust) | L13 验证方向的前沿落地 |
