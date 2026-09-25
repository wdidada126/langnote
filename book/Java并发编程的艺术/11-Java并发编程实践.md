# 第 11 章 Java并发编程实践（原书第 2 版 pp.366-382）

> 实战收尾：生产-消费者模式（双缓冲/队列）、线上并发问题的排查套路、性能调优经验。与《实战》12 章（测试）+ 11 章（性能）互补，本书偏"踩过的坑与排查命令"。

## 一、本章地图

| 主题 | 关键结论 |
| --- | --- |
| 生产-消费者 | 用阻塞队列解耦；双缓冲降低锁竞争（读写各一把锁） |
| 线上问题 | CPU 100% / 死锁 / OOM / 响应慢 的排查链路 |
| 排查工具 | `top`/`jstack`/`jmap`/`jcmd`/JFR/async-profiler |
| 性能调优 | 减小锁粒度、用并发容器、异步化、避免伪共享 |

## 二、核心精讲

### 2.1 生产-消费者模式
- 经典：`BlockingQueue` 作缓冲，生产者 `put`、消费者 `take`，天然解耦速度差。
- 双缓冲变体：读写各用一把锁 + 两块 buffer 轮换 → 把锁竞争降到"换 buffer 那一刻"（减少临界区）。
- 背压：队列满时生产者应阻塞/限流，而非无限堆积（避免 OOM）。

### 2.2 线上并发问题排查链路
- **CPU 100%**：`top -H` 找高 CPU 线程 → `printf %x` 转 16 进制 → `jstack` 定位到具体线程栈 → 多为死循环/自旋（如 CAS 无退避）。
- **死锁**：`jstack`/`jcmd Thread.print` 自动报告 Java 级 monitor 死锁（含等待链）；`ReentrantLock` 死锁需 `jstack` 的"ownable synchronizers"段或 JFR。
- **OOM / 内存泄漏**：`jmap -histo` 看对象；`ThreadLocal` 泄漏（线程池线程 value 强引用）是高频元凶（见《之美》ThreadLocal 专篇）。
- **响应慢**：JFR 看"锁等待/阻塞/GC 停顿"；`async-profiler -e lock` 量化锁竞争占比。

### 2.3 性能调优经验
- 减小锁粒度/范围（快进快出）；用并发容器替代 `synchronized` 集合。
- **伪共享**：高频计数字段用 `@Contended`（JDK 8+）或 `LongAdder` 隔离缓存行（见《之美》伪共享专篇）。
- 异步化：把阻塞 I/O 移出热路径；或用虚拟线程（JDK 21+）。
- 不要"过早优化"：先 JMH 量、再改（避免《实战》11/12 章陷阱）。

## 三、版本演进

- **成书（JDK 7/8）**：排查靠 `jstack`/`jmap`；调优靠减小锁 + 并发容器。
- **JDK 9+**：JFR 开源 + JMC 可视化 → 运行时观测平民化。
- **JDK 11+**：`jcmd` 统一诊断入口（替代部分 `jstack`/`jmap`）。
- **JDK 21+**：虚拟线程把"线程池调优"大幅简化；`@Contended` 默认需 `-XX:-RestrictContended` 或模块开放。

## 四、经典论文 / 原始文献

- **Goetz, "Java Concurrency in Practice" 第 11/12 章**——性能与测试方法论。
- **JEP 444 (Virtual Threads)** / **JEP 453 (Structured Concurrency)**——现代并发工程范式。
- **Adve & Hill (TPDS 1993) / Amdahl (1967)**——性能/可伸缩理论（见《实战》11 章 + 之美 Amdahl 专篇）。

## 五、工业界前沿

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **async-profiler** | 11k | CPU/锁/分配火焰图，线上排查标配 |
| **openjdk/jmc (JFR)** | 23.4k | 生产低开销录制：锁等待/阻塞/GC |
| **Arthas (alibaba)** | 36k | 线上诊断：`thread`/`dashboard`/`trace` 实时看并发热点 |
| **Netflix/concurrency-limits** | 1.4k | 自适应并发限制，防"队列堆积/OOM" |
| **ben-manes/caffeine** | 17.9k | 高并发缓存实战 |

## 六、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "线程池越大吞吐越高" | 受资源；公式 + 压测 |
| 2 | "队列无界最稳" | 任务暴增撑爆 OOM；务必有界 + 背压 |
| 3 | "看到 CPU 100% 就是计算多" | 可能是 CAS 自旋/死循环；`jstack` + 火焰图定位 |
| 4 | "调优凭感觉" | 先 JMH/JFR 量，再改 |
| 5 | "排查靠重启" | `jstack`/`jcmd`/`async-profiler` 在线抓现场 |
| 6 | "新代码还要手动维护线程池" | IO 密集改虚拟线程 + 结构化并发 |
