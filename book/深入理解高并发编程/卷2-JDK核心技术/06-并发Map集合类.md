# 第 6 章 并发 Map 集合类

> `ConcurrentHashMap`（JDK8 桶级 CAS+锁、红黑树、扩容协助、计数）、`ConcurrentSkipListMap`（有序跳表）。本书逐类源码级，是最实用章之一。详见方腾飞《艺术》6 章、深度解析 9 章、之美 concepts/JMM与并发集合。

## 一、核心精讲

### 6.1 🔧 CHM 桶级锁（JDK8+）
- 弃分段锁；初始化/写用 CAS 或 `synchronized` 锁单桶；链表 >8 转红黑树；`sizeCtl` 控初始化/扩容（🔧 扩容多线程协助迁移，读不阻塞；`get` 无锁；`mappingCount` 代替 `size`）。

### 6.2 计数与聚合
- `CounterCell` 分段计数（`baseCount` + `counterCells`），类似 `LongAdder`（🔧 `size()` 是估计值，非精确快照）。

### 6.3 ConcurrentSkipListMap
- 无锁跳表，有序，支持范围视图（🔧 需要有序/范围查询用；否则 CHM 更快）。

## 二、版本演进 / 论文 / 前沿

- 论文：跳表（Pugh 1990）；Lea AQS（SCIENCE'04）；Michael-Scott（PODC'96）。
- 工业界：Caffeine（17.9k，W-TinyLFU）、JCTools（3.9k）。
- 开源 stars（2026-09）：JDK 23.4k / caffeine 17.9k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "CHM 分段锁" | JDK8+ 桶级锁 |
| 2 | "size() 精确" | 估计值 |
| 3 | "CHM 有序" | 用 SkipListMap |
