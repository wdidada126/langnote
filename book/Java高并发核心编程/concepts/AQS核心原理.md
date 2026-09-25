# 卷2·AQS 抽象同步器的核心原理（尼恩）

> 卷2 第 6 章。`AbstractQueuedSynchronizer` 的 CLH 队列、`state`、`Node.waitStatus`、独占/共享模式。详见《之美》concepts/AQS抽象同步队列.md（源码级最细）、方腾飞《艺术》5 章、冷血《实现原理》3 章（手写 AQS）。

## 一、核心精讲

### 1.1 三组件
- `state`（int，语义由子类定）、`head`/`tail` 双向 CLH 队列、`Node.waitStatus`（CANCELLED/SIGNAL/CONDITION/PROPAGATE）（🔧 见之美 AQS 专篇完整状态机）。

### 1.2 复用 AQS 的同步器
- 独占：`ReentrantLock`；共享：`Semaphore`/`CountDownLatch`/`ReentrantReadWriteLock.ReadLock`；`CyclicBarrier` 用 `ReentrantLock`+`Condition` 而非 AQS（🔧 见之美 10 章辨析）；`StampedLock` 故意不基于 AQS。

### 1.3 unparkSuccessor 从尾遍历
- 因 `next` 在 CAS 入队后才设、可能不可靠，唤醒时从 `tail` 反向找最近未取消节点（🔧 见之美 AQS 专篇）。

## 二、版本演进 / 论文 / 前沿

- 论文：Lea AQS（SCIENCE'04）；Craig CLH（1993）；Magnussen/Landin/Hagersten MCS（IPPS'94）。
- 工业界：JDK `java.util.concurrent` 全部同步器基石；Netty `AbstractQueuedSynchronizer` 思路借鉴。
- 开源 stars（2026-09）：JDK 23.4k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "AQS 有论文" | 无；源码注释是权威文档 |
| 2 | "CyclicBarrier 用 AQS" | 用 Lock+Condition |
| 3 | "唤醒从 head 正向" | 从 tail 反向遍历 |
