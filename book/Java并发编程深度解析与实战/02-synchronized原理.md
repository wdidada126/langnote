# 第 2 章 深度揭秘 synchronized 实现原理

> `synchronized` 的底层：对象头 Mark Word、监视器锁（Monitor/`ObjectMonitor`）、锁升级（无锁→偏向→轻量→重量）、`monitorenter`/`monitorexit` 字节码。本书的「锁升级」原理揭秘是独有亮点，与方腾飞《艺术》2 章互文。

## 一、核心精讲

### 2.1 🔧 对象头 Mark Word
- 每个 Java 对象头含 Mark Word（哈希/分代年龄/锁标志位）和 Klass 指针（🔧 `synchronized` 锁信息存在 Mark Word 的锁标志位里；用 JOL 可观察对象头布局）。

### 2.2 锁升级（JDK 6+）
- 无锁 → **偏向锁**（单线程重复进入，CAS 记录线程 ID）→ **轻量级锁**（多线程交替，CAS 自旋）→ **重量级锁**（竞争激烈，膨胀为 `ObjectMonitor`，线程阻塞挂起）（🔧 升级单向，不降级；偏向锁在 JDK 15 默认禁用、JDK 18 移除，因维护成本高且伪共享，见 JEP 374）。

### 2.3 虚拟线程 pin
- 虚拟线程内 `synchronized` 块会**pin** carrier 平台线程（🔧 长时间同步块阻塞整个 carrier，破坏虚拟化；用 `ReentrantLock` 替代可卸载，见《之美》08 章）。

## 二、版本演进 / 论文 / 前沿

- 论文/文献：HotSpot `ObjectMonitor` 实现；偏向锁（JDK 6 引入，JEP 374 移除）；JEP 444 虚拟线程。
- 工具：JOL（观察对象头/对齐填充，2.1k）、async-profiler。

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "synchronized 慢" | JDK6+ 锁升级后并不慢 |
| 2 | "偏向锁还在用" | JDK15+ 默认禁，JDK18 移除 |
| 3 | "虚拟线程随意 synchronized" | 会 pin carrier |
| 4 | "锁信息在哪" | Mark Word 锁标志位 |
