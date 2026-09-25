# 第 5 章 AQS 同步器

> `AbstractQueuedSynchronizer` 详解（本书用大量篇幅）：CLH 队列、`state`、独占/共享、条件队列、唤醒传播。作者称其「JDK 并发基石」。详见《之美》concepts/AQS抽象同步队列.md、艺术 5 章、冷血 3 章、冰河卷1 8 章。

## 一、核心精讲

### 5.1 🔧 三组件
- `state`（语义由子类定）、`head`/`tail` 双向 CLH、`Node.waitStatus`（CANCELLED/SIGNAL/CONDITION/PROPAGATE）（🔧 见《之美》AQS 专篇完整状态机）。

### 5.2 独占 vs 共享
- 独占：`tryAcquire/tryRelease`（`ReentrantLock`）；共享：`tryAcquireShared/tryReleaseShared`，返回值 `<0` 失败/`=0` 成功无剩余/`>0` 成功且需传播（🔧 传播是共享模式关键，见《之美》AQS 专篇）。

### 5.3 条件队列
- 一个 AQS 可挂多个 `ConditionObject`（单向条件队列），`await` 移入、`signal` 移回同步队列（🔧 与 `synchronized` 的单等待集对比）。

### 5.4 从尾唤醒
- `next` 不可靠，从 `tail` 反向找最近未取消节点（🔧 见《之美》AQS 专篇）。

## 二、版本演进 / 论文 / 前沿

- 论文：Lea AQS（SCIENCE'04）；Craig CLH（1993）；MCS（IPPS'94）。
- 工业界：JDK `java.util.concurrent` 全部同步器；Netty 借鉴。
- 开源 stars（2026-09）：JDK 23.4k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "AQS 有论文" | 源码注释权威 |
| 2 | "唤醒正向" | 从 tail 反向 |
| 3 | "共享不需传播" | 必须传播唤醒 |
