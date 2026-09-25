# 第 16 章 基于 CAS 实现自旋锁实战

> 用 `AtomicReference`/CAS 手写自旋锁：抢锁 CAS 设 owner，失败循环自旋，解锁 CAS 清。本书把第 10 章 CAS 落地。与冷血《实现原理》3 章（手写 AQS 锁）互补。

## 一、核心精讲

### 16.1 🔧 自旋锁结构
- `owner` 用 `AtomicReference<Thread>`；`lock()` 循环 `compareAndSet(null, self)`；`unlock()` 置 null（🔧 缺点：自旋烧 CPU；适合**极短临界区**）。

### 16.2 与 AQS/ReentrantLock 对比
- 自旋锁无排队、无阻塞，临界区极短时最快；长临界区/高争用用 AQS（排队+阻塞）（🔧 见 18 章、之美 06 章）。

### 16.3 可重入扩展
- 加 `holdCount`，同一线程重入 +1（🔧 见 `ReentrantLock` 的 `state` 计数）。

## 二、版本演进 / 论文 / 前沿

- 论文：Herlihy Wait-Free（PODC'91）；x86 `LOCK CMPXCHG`。
- 工业界：JDK `AtomicReference`、JCTools 自旋策略。
- 开源 stars（2026-09）：JDK 23.4k / JCTools 3.9k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "自旋锁通用" | 仅极短临界区 |
| 2 | "自旋不耗 CPU" | 高争用烧 CPU |
| 3 | "CAS 锁可重入" | 需显式 holdCount |
