# 第 7 章 synchronized 核心原理

> 对象头 Mark Word、Monitor（`ObjectMonitor`）、`monitorenter`/`monitorexit`、锁升级（无锁→偏向→轻量→重量）、偏向锁废弃。本书图解 Monitor 与锁升级全流程。详见方腾飞《艺术》2 章、深度解析 2 章、之美 06/comcepts/JMM。

## 一、核心精讲

### 7.1 🔧 Mark Word + Monitor
- 锁状态存对象头 Mark Word；重量级锁指向 `ObjectMonitor`（等待队列）（🔧 JOL 可观对象头）。

### 7.2 锁升级单向
- 偏向（单线程 CAS 记 ID）→ 轻量（交替 CAS 自旋）→ 重量（膨胀 Monitor，阻塞）（🔧 JDK 15 默认禁偏向、JDK 18 移除，JEP 374；维护成本高+伪共享）。

### 7.3 虚拟线程 pin
- 虚拟线程内 `synchronized` 会 pin carrier（🔧 长同步块用 `ReentrantLock` 替代）。

## 二、版本演进 / 论文 / 前沿

- 文献：HotSpot `ObjectMonitor`；JEP 374、JEP 444。
- 工具：JOL、async-profiler。

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "偏向锁还在用" | JDK15+ 移除 |
| 2 | "synchronized 慢" | 锁升级后不慢 |
| 3 | "虚拟线程随意 synchronized" | pin carrier |
