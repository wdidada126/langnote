# 第 9 章 Lock 锁核心原理

> `Lock` 接口、`ReentrantLock`（AQS 独占）、`ReentrantReadWriteLock`（state 高低 16 位）、`StampedLock`（乐观读）、与 `synchronized` 对比、公平/非公平。本书图解 state 编码。详见方腾飞《艺术》5 章、深度解析 4 章、之美 06 章。

## 一、核心精讲

### 9.1 🔧 state 编码两锁
- `ReentrantLock`：`state`=重入次数；`ReentrantReadWriteLock`：高 16 读计数 + 低 16 写重入（🔧 CAS 同时改两部分，写饥饿潜在）。

### 9.2 StampedLock 乐观读
- `tryOptimisticRead`+`validate`，非 AQS、不可重入（🔧 读多写少优于读写锁；见《之美》06 章）。

### 9.3 公平 vs 非公平
- 非公平吞吐高但可能饿；公平 FIFO（🔧 按需选）。

## 二、版本演进 / 论文 / 前沿

- 论文：Lea AQS（SCIENCE'04）；seqlock（Linux 内核）。
- 工业界：JDK `locks` 包。
- 开源 stars（2026-09）：JDK 23.4k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "ReentrantLock 总优" | 低争用 synchronized 反超 |
| 2 | "StampedLock 可重入" | 不可重入 |
| 3 | "读写锁无写饿" | 高读用 StampedLock |
