# 第 6 章 J.U.C 并发工具集实战及原理分析

> 同步器实战：`CountDownLatch`、`CyclicBarrier`、`Semaphore`、`Exchanger`、`Phaser`。本书重「各自底层（AQS 共享/独占）与选用区别」。详见方腾飞《艺术》8 章、之美 10 章、手册 3 章、精通2 6 章。

## 一、核心精讲

### 2.1 🔧 选型矩阵
- **等待 N 个事件完成**（一次性）→ `CountDownLatch`（AQS 共享，`countDown` 释放）（🔧 不可重用）。
- **多任务到齐再继续**（可重入代际）→ `CyclicBarrier`（`ReentrantLock`+`Condition`，非 AQS）（🔧 可 reset 重用）。
- **限流/资源池** → `Semaphore`（AQS 共享，permits）。
- **两任务交换数据** → `Exchanger`（槽位 CAS）。
- **动态多阶段** → `Phaser`（见精通2 6 章）。

### 2.2 CyclicBarrier 非 AQS
- 内部用 `ReentrantLock` + `Condition` + `generation`（代际）实现，与 CountDownLatch 的 AQS 共享模式不同（🔧 见之美 10 章辨析，避免混淆「它们底层都一样」的误判）。

## 二、版本演进 / 论文 / 前沿

- 论文：Lea AQS（SCIENCE'04）；屏障原语源自 Dijkstra（1975）。
- 工业界：JDK `java.util.concurrent`；结构化并发 `StructuredTaskScope` 是现代替代（JEP 453/505，见之美 concepts/结构化并发与ScopedValue）。

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "CyclicBarrier 用 AQS" | 用 Lock+Condition |
| 2 | "Latch 可重用" | 用 Barrier/Phaser |
| 3 | "Barrier 超时即崩" | 超时会破代，需处理 |
