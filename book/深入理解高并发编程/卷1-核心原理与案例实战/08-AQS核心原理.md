# 第 8 章 AQS 核心原理

> `AbstractQueuedSynchronizer` 的 CLH 队列、`state`、`Node.waitStatus`、独占/共享 acquire/release、条件队列、`unparkSuccessor` 从尾遍历。本书把 AQS 讲成「JDK 并发基石」。详见《之美》concepts/AQS抽象同步队列.md、方腾飞《艺术》5 章、冷血《实现原理》3 章。

## 一、核心精讲

### 8.1 三组件
- `state`（语义由子类定）、`head`/`tail` 双向 CLH、`Node.waitStatus`（🔧 见《之美》AQS 专篇完整状态机）。

### 8.2 哪些基于 AQS
- 独占：`ReentrantLock`；共享：`Semaphore`/`CountDownLatch`/`ReadLock`；`CyclicBarrier` 用 `Lock`+`Condition` 而非 AQS（🔧 见《之美》10 章）。

### 8.3 从尾唤醒
- `next` 在 CAS 入队后才设、不可靠，唤醒从 `tail` 反向找（🔧 见《之美》AQS 专篇）。

## 二、版本演进 / 论文 / 前沿

- 论文：Lea AQS（SCIENCE'04）；Craig CLH（1993）；MCS（IPPS'94）。
- 工业界：JDK `java.util.concurrent`；Netty 借鉴。
- 开源 stars（2026-09）：JDK 23.4k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "AQS 有论文" | 源码注释为权威 |
| 2 | "CyclicBarrier 用 AQS" | Lock+Condition |
| 3 | "唤醒正向" | 从 tail 反向 |
