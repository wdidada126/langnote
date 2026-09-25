# 卷2·JUC 容器类（尼恩）

> 卷2 第 7 章。`ConcurrentHashMap`、`CopyOnWriteArrayList`、`BlockingQueue` 族、`ConcurrentLinkedQueue`、`ConcurrentSkipListMap`。详见方腾飞《艺术》6 章、手册 7 章、之美 08/09/concepts/阻塞队列BlockingQueue.md。

## 一、核心精讲

### 1.1 ConcurrentHashMap
- JDK 8+ 弃分段锁，改桶级 CAS + 链表/红黑树（`sizeCtl` 控扩容）（🔧 详见方腾飞《艺术》6 章；`mappingCount` 取代 `size`）。

### 1.2 CopyOnWriteArrayList
- 写时复制，读无锁（🔧 读多写少；写频繁/OOM 风险，别用于大列表高频写）。

### 1.3 阻塞队列
- `ArrayBlockingQueue`（有界、单锁）、`LinkedBlockingQueue`（默认无界=风险）、`SynchronousQueue`（手递手）、`DelayQueue`（延迟）、`PriorityBlockingQueue`（优先级）（🔧 选型矩阵见之美 concepts/阻塞队列）。

### 1.4 无锁队列
- `ConcurrentLinkedQueue`（Michael-Scott，见之美 concepts/Michael-Scott无锁队列）；高并发可选 JCTools `Mpsc` 队列。

## 二、版本演进 / 论文 / 前沿

- 论文：Michael-Scott（PODC'96）、Lea AQS（SCIENCE'04）。
- 工业界：JCTools（3.9k，无锁队列）、Disruptor（18.5k，环形 buffer）、caffeine（17.9k，W-TinyLFU）。
- 开源 stars（2026-09）：JDK 23.4k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "CHM 分段锁" | JDK8+ 桶级锁 |
| 2 | "LinkedBlockingQueue 安全" | 默认无界，可能 OOM |
| 3 | "COW 写多" | 仅读多写少 |
