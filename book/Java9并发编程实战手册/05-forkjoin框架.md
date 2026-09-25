# 第 5 章 fork/join框架（原书 pp.171-207）

> Fork/Join 配方：`ForkJoinPool`/`RecursiveTask`/`RecursiveAction`/`fork`/`join`、工作窃取、阈值调优。菜谱式。与冷血 7 章（手写）+ 《艺术》6 章互补，本书重"递归分解配方 + 阈值"。

## 一、本章地图

| 主题 | 配方 |
| --- | --- |
| `RecursiveTask` | 有返回值的分治 |
| `RecursiveAction` | 无返回值的分治 |
| `fork`/`join` | 分解/合并 |
| 工作窃取 | deque（owner 头 / stealer 尾） |
| 阈值 | 避免过细拆分 |

## 二、核心精讲

- 分治：`compute()` 小于阈值直接计算，否则 `fork` 子任务 + `join` 合并。
- 工作窃取：每个 worker 双端队列，自己从头取、偷别人从尾取 → 低竞争（见冷血 7 章手写）。
- 适用：CPU 密集可分解（归并排序、并行流底层）；🔧 不适合 I/O 阻塞（虚拟线程更合适）。
- 🔧 `commonPool` 别提交阻塞任务（会饿死全局 `parallelStream`）。

## 三、版本演进 / 论文 / 前沿

- Lea Fork/Join (2000)；Blumofe-Leiserson (JACM 1999)。开源 JDK 23.4k / rayon 12k / crossbeam 8.6k / oneTBB 6.8k。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "ForkJoin 适合所有" | 仅 CPU 密集可分解 |
| 2 | "commonPool 提交阻塞" | 饿死全局并行流 |
| 3 | "任务越小越好" | 拆分开销；设阈值 |
| 4 | "join 会死锁" | 正确分治不会 |
