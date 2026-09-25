# 卷2·JUC 显式锁的原理与实战（尼恩）

> 卷2 第 5 章。`ReentrantLock`、`ReentrantReadWriteLock`、`StampedLock`、`Semaphore`、`Condition`。详见方腾飞《艺术》5 章、之美 06 章、之美 concepts/ThreadLocal与内存泄漏.md（间接）。

## 一、核心精讲

### 1.1 ReentrantLock vs synchronized
- 可中断（`lockInterruptibly`）、可限时（`tryLock(timeout)`）、公平可选、多 `Condition`（🔧 JDK 6 后 `synchronized` 有偏向/轻量/重量三级，低争用已反超；高争用 `ReentrantLock` 更可控；虚拟线程下 `synchronized` 会 pin 平台线程，见之美 08 章）。

### 1.2 读写锁
- `ReentrantReadWriteLock`：读共享、写独占（🔧 读多写少提吞吐；但「写饥饿」：读不停则写等；用 `StampedLock` 乐观读缓解）。

### 1.3 StampedLock
- 乐观读 `tryOptimisticRead` → 校验 `validate`（🔧 非 AQS、不可重入、不能配合 Condition；读多写少性能优于读写锁，见之美 06 章）。

### 1.4 Semaphore（笔记提到）
- 限流/资源池：许可数控制并发访问数（🔧 与 CountDownLatch/CyclicBarrier 分工见之美 10 章）。

## 二、版本演进 / 论文 / 前沿

- 论文：Lea AQS（SCIENCE'04）；seqlock（Linux 内核，StampedLock 乐观读借鉴）；Craig CLH（1993）/MCS（1994）。
- 开源 stars（2026-09）：JDK 23.4k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "ReentrantLock 总优于 synchronized" | JDK6+ 低争用 synchronized 反超 |
| 2 | "StampedLock 可重入" | 不可重入，勿混用 |
| 3 | "读写锁无写饥饿" | 高读用 StampedLock |
