# 第 7 章 ForkJoinPool（原书 pp.190-225）

> 手写 `ForkJoinPool` 与工作窃取（Work-Stealing）双端队列、手写 `ForkJoinTask`/`RecursiveTask`（`fork`/`join`）。与《艺术》6 章 + 《之美》`concepts/ForkJoin与工作窃取.md` 互补。

## 一、本章地图

| 主题 | 手写要点 |
| --- | --- |
| 工作窃取队列 | 每个 worker 一个双端队列（deque）；自己从头取，偷别人从尾取 |
| `fork`/`join` | `fork` 把子任务压自己队列头；`join` 等结果（空则去偷） |
| `RecursiveTask`/`RecursiveAction` | `compute()` 拆分 + 合并 |
| 窃取竞争 | 偷尾减少与 owner 的 head 竞争 |

## 二、核心精讲

### 2.1 手写工作窃取双端队列
- 每个 worker 持有 `deque`（数组 + `base`/`top` 指针）。
- **owner** 取任务：从 `top` 端 `pop`（LIFO，缓存友好）；**stealer** 取任务：从 `base` 端 `poll`（FIFO）。
- 两端操作方向相反 → owner 与 stealer 几乎不抢同一指针 → 低竞争。

### 2.2 手写 `fork`/`join`
- `fork()`：把当前子任务 `push` 到自己 deque 的 `top`（不立即执行，继续干手头）。
- `join()`：若任务已完成返回结果；否则尝试 `pop` 自己队列继续干（work-first，减少窃取），若自己空则 `poll` 偷别人队列；等待期间帮别人算。
- **递归分解**：`compute()` 把大问题拆小，小到阈值直接算，再 `join` 合并（分治）。

### 2.3 适用与不适
- 适合：**可分解的 CPU 密集**任务（归并排序、并行流、MapReduce 式）。
- 不适合：**I/O 阻塞**任务——阻塞会卡住 stealer 的窃取（虚拟线程更合适）；任务间有依赖会串行化。

## 三、版本演进

- **JDK 7 (2011)**：`ForkJoinPool`/`ForkJoinTask` 引入（Lea）。
- **JDK 8 (2014)**：`parallelStream()` / `CompletableFuture` 默认用 `ForkJoinPool.commonPool()`。
- **JDK 21**：虚拟线程让"I/O 并发"不再依赖 ForkJoin；但 CPU 密集分治仍是 ForkJoin 主场。

## 四、经典论文 / 原始文献

- **Lea, "A Java Fork/Join Framework" (2000)**——工作窃取框架设计（必读）。
- **Blumofe & Leiserson, "Scheduling Multithreaded Computations by Work Stealing" (JACM 1999)**——工作窃取理论（Cilk 起源）。- **Herlihy & Shavit**——分治并行算法。

## 五、工业界前沿

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **openjdk/jdk** | 23.4k | `ForkJoinPool`/`ForkJoinTask`/`RecursiveTask` |
| **rayon-rs/rayon** | 12k | Rust 工作窃取并行迭代器（思想同源） |
| **crossbeam-rs/crossbeam** | 8.6k | Rust deque/MPMC（手写 deque 对照） |
| **oneapi-src/oneTBB** | 6.8k | Intel TBB 并行算法（工作窃取） |

## 六、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "ForkJoin 适合所有并发" | 仅 CPU 密集可分解；I/O 阻塞用虚拟线程 |
| 2 | "fork 立即执行子任务" | 默认只是入队，靠窃取/继续干 |
| 3 | "commonPool 随便用" | 共享池，别提交阻塞任务（会饿死全局并行流） |
| 4 | "任务越小越好" | 拆分有开销；设合理阈值 |
| 5 | "join 会死锁" | 正确分治不会；但任务间循环依赖会 |
