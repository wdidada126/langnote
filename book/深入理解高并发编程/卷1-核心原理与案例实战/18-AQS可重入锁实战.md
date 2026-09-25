# 第 18 章 基于 AQS 实现可重入锁实战

> 继承 `AbstractQueuedSynchronizer` 手写可重入锁：覆写 `tryAcquire`/`tryRelease`（state 记重入），独占模式。本书把第 8 章 AQS 落地。与冷血《实现原理》3 章（手写 AQS）互补——本书最简可重入版。

## 一、核心精讲

### 18.1 🔧 最小化 AQS 锁
- `state`=0 无主，`tryAcquire` CAS 0→1 或 owner 重入 +1；`tryRelease` 减到 0 释放（🔧 其余排队/唤醒由 AQS 托管；别自己写 CLH）。

### 18.2 与 ReentrantLock 对比
- 手写版缺：公平/非公平、`Condition`、可中断（🔧 JDK `ReentrantLock` 见深度解析 4 章、之美 06 章）。

### 18.3 为何手写
- 教学价值；生产用 JDK（🔧 自写锁易出错，优先 `ReentrantLock`/`StampedLock`）。

## 二、版本演进 / 论文 / 前沿

- 论文：Lea AQS（SCIENCE'04）；Craig CLH（1993）/MCS（1994）。
- 工业界：JDK `java.util.concurrent.locks`；Netty 借鉴。
- 开源 stars（2026-09）：JDK 23.4k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "自写队列" | 继承 AQS 即可 |
| 2 | "手写锁上生产" | 用 JDK |
| 3 | "state 随便定义" | 语义要自洽 |
