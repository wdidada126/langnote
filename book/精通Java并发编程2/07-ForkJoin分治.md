# 第 7 章 优化分治解决方案：Fork/Join 框架

> `ForkJoinPool` + `RecursiveTask`/`RecursiveAction` + 工作窃取（work-stealing deque）。与艺术/冷血/手册 5 章、之美 concepts/ForkJoin 互补，本书重「分治阈值调优基准」。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| 任务 | RecursiveTask（有值）/RecursiveAction（无值） |
| 分治 | compute 里 fork 子任务 + join |
| 工作窃取 | 双端队列，空闲线程偷尾端 |
| 阈值 | 太小则 fork 开销 > 收益 |

## 二、核心精讲

### 2.1 🔧 不要 join 自己的子树串行
- 错误写法：`left.fork(); right.compute(); left.join();` 让当前线程空等（🔧 正确：`left.fork(); right.fork(); left.join(); right.join();` 或 `invokeAll(left,right)` 让当前线程也偷活）。

### 2.2 阈值基准
- 分治阈值需实测：太小 → fork 任务管理开销反噬；太大 → 并行度不足（🔧 JMH 扫不同阈值找拐点；`commonPool` 并行度 = 核心数-1）。

### 2.3 异常与取消
- `ForkJoinTask` 异常用 `getException()` 取；`cancel` 仅对未开始任务有效（🔧 见手册 5/10 章）。

## 三、版本演进 / 论文 / 前沿

- 论文：Blumofe-Leiserson 工作窃取（JACM'99）；Lea ForkJoin（JDK 7）。
- 工业界：rayon（Rust，work-steel 借鉴）、crossbeam（Rust 无锁）、Akka 分治；R 的 `parallel`、Python `concurrent.futures.ProcessPool` 同思路。
- 开源 stars（2026-09）：rayon 12k / crossbeam 8.6k / JDK 23.4k。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "join 自己的子树" | 用 invokeAll 让本线程也干活 |
| 2 | "阈值越小越好" | 实测找拐点 |
| 3 | "ForkJoin 里做 IO" | 饿死 commonPool；用虚拟线程 |
