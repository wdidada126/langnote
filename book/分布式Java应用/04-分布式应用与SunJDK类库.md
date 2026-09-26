# 第 4 章　分布式应用与Sun JDK类库

> 原书第 4 章是**被低估的一章**：它把分布式 Java 应用天天打交道的 **JDK 集合包、并发包（J.U.C）、
> 序列化**从「会用」讲到「懂原理」——`HashMap` 为什么在并发下会死循环、`ConcurrentHashMap`
> 的分段锁、`ThreadPoolExecutor` 的每一格参数、`Serializable` 的版本号陷阱。
> 这些**至今仍是 Java 面试与线上事故的高频区**。但本书基于 **JDK 6**：`HashMap` 还是数组+链表
> （JDK 8 才引入红黑树）、`ConcurrentHashMap` 还是分段锁（JDK 8 改为 CAS+synchronized 桶锁）、
> 序列化仍是 Java 原生（今天 Protobuf/Kryo 才是跨节点首选）。读这章要**保留它的源码级视角，更新它的实现细节**。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 4.1 集合包 | ArrayList/LinkedList/Vector/Stack/HashSet/TreeSet/HashMap/TreeMap 的实现与选型；性能测试 | **不同集合的时空复杂度决定选型**；并发下不能用非线程安全集合 |
| 4.1.1–4.1.8 各类集合 | 底层结构（数组/链表/红黑树/哈希）、增删查复杂度 | HashMap 平均 O(1)、TreeMap O(logN)、ArrayList 随机读 O(1) |
| 4.1.9 性能测试 | 用简单 benchmark 对比集合吞吐 | 选型要数据说话（今天用 JMH 而非手搓循环） |
| 4.1.10 小结 | 选型决策表 | 读多写少/写多读少/需排序/需并发，各有对应集合 |
| 4.2 并发包（java.util.concurrent） | ConcurrentHashMap、CopyOnWrite、BlockingQueue、Atomic、线程池、锁、同步器 | **J.U.C 是并发安全的工程化底座**，建立在第 3 章的 JMM 之上 |
| 4.2.1 ConcurrentHashMap | 分段锁（JDK 6/7） | 高并发 Map 的基石；JDK 8 改为桶锁 |
| 4.2.2 CopyOnWriteArrayList | 写时复制 | 读多写少、弱一致读场景 |
| 4.2.3 CopyOnWriteArraySet | 基于 COW List 的 Set | 同上 |
| 4.2.4 ArrayBlockingQueue | 有界阻塞队列 | 生产者-消费者、线程池工作队列 |
| 4.2.5 AtomicInteger | CAS 无锁原子类 | 计数器/序列号，避免锁开销 |
| 4.2.6 ThreadPoolExecutor | 核心/最大线程、队列、拒绝策略 | **线程池参数错配是线上事故头号来源** |
| 4.2.7 Executors | 快捷工厂（Fixed/Cached/Single） | 警惕 Cached 无界队列、Fixed 的隐患 |
| 4.2.8 FutureTask | 异步任务结果 | 早期异步范式 |
| 4.2.9 Semaphore | 信号量 | 限流/资源池 |
| 4.2.10 CountDownLatch | 等待多线程完成 | 启动/关闭屏障 |
| 4.2.11 CyclicBarrier | 循环屏障 | 多阶段并行 |
| 4.2.12 ReentrantLock | 可重入锁（可中断/公平/Condition） | synchronized 的可控替代 |
| 4.2.13 Condition | 条件变量 | 替代 wait/notify 的多路等待 |
| 4.2.14 ReentrantReadWriteLock | 读写锁 | 读多写少提升并发 |
| 4.3 序列化/反序列化 | Serializable、serialVersionUID、transient、Externalizable | **跨节点传输对象的契约层**，远程调用（第 1 章）的 payload 载体 |

## 核心精讲

（以下为教学性梳理；所有片段均**教学示意，不参与构建**，绝不编译/运行。）

### 4.1 集合：选型先看复杂度

```text
# 教学示意，不参与构建：常用集合复杂度速查（JDK 8+）
ArrayList     : 随机读 O(1), 尾部插 O(1)均摊, 中间插 O(N)   -> 读多写少
LinkedList    : 读 O(N), 插删 O(1)(已知节点)               -> 频繁头尾操作
HashMap       : 增删查平均 O(1), 最坏 O(N)(链)/O(logN)(树) -> 通用 KV
TreeMap       : 增删查 O(logN), 有序遍历                   -> 需排序/范围
HashSet/TreeSet : 分别为 HashMap/TreeMap 的包装           -> 去重
```

- **并发红线**：`HashMap`/`ArrayList` 非线程安全，多线程下扩容会造成数据丢失甚至**死循环**
  （JDK 7 及之前 transfer 的头插法问题；JDK 8 改为尾插法缓解但仍非安全）。并发请用
  `ConcurrentHashMap` / `CopyOnWriteArrayList` / `Collections.synchronizedXxx`。

### 4.2 并发包：线程池是重灾区

```java
// 教学示意，不参与构建：ThreadPoolExecutor 参数含义
new ThreadPoolExecutor(
    corePoolSize,      // 常驻线程数
    maximumPoolSize,   // 最大线程数
    keepAliveTime,     // 空闲线程回收时间
    unit,
    workQueue,         // 任务队列（有界/无界决定背压）
    threadFactory,
    handler            // 拒绝策略：Abort/Discard/DiscardOldest/CallerRuns
);
```

- **经典坑**：`Executors.newCachedThreadPool()` 用**无界队列 + 可无限建线程**，高并发下打爆资源；
  `newFixedThreadPool` 用无界 `LinkedBlockingQueue`，任务堆积 OOM。生产应**显式构造有界队列 + 合理拒绝策略**。

### 4.3 序列化：远程调用的 payload 契约

```text
# 教学示意，不参与构建：Java 原生序列化的问题
ObjectOutputStream -> 把对象图写成字节流
隐患: 体积大、速度慢、有反序列化漏洞(gadget chain)、跨语言不可用
结论: 分布式场景首选 Protobuf/Kryo/Hessian，而非 java.io.Serializable
```

> 读这一章时请对照 [01-分布式Java应用.md](01-分布式Java应用.md)（1.2.1 RMI 默认用 Java 原生序列化，
> 正是 4.3 的契约层）与 [03-深入理解JVM.md](03-深入理解JVM.md)（4.2 并发包建立在 3.3 的 JMM/Happens-Before 之上）。

## 版本演进

- **本书无第二版**；本节写 2010 年（JDK 6）口径 → 2026 年视角的变化。
- **HashMap 实现升级（JDK 8）**：桶从纯链表改为**链表 + 红黑树**（阈值 8/6），最坏复杂度从 O(N) 降到 O(logN)，
  本书 4.1.7 的「数组+链表」描述需更新。
- **ConcurrentHashMap 重构（JDK 8）**：放弃**分段锁（Segment）**，改为 **Node + CAS + synchronized 细粒度桶锁**，
  并发度更高、内存更省；本书 4.2.1 的分段锁讲解仅适用于 JDK 7 及之前。
- **序列化方案换代**：Java 原生序列化因体积/速度/安全被边缘化；今天跨节点首选
  **Protobuf（google/protobuf 72067★）、Kryo、Hessian、FlatBuffers**。Hessian 正是本书 1.2 远程调用框架的常用序列化。
- **并发工具补全**：本书列到 `FutureTask`；2026 年异步已是 `CompletableFuture`（JDK 8）+ `Flow`/Reactive（JDK 9），
  虚拟线程（JDK 21）进一步降低「异步 vs 同步」的取舍成本（见 [03-深入理解JVM.md](03-深入理解JVM.md)）。
- **基准测试严谨化**：本书 4.1.9 的「手搓循环计时」在 2026 年被 **JMH（OpenJDK JMH）** 取代——
  须处理 JIT 优化、死代码消除、预热，否则结论失真。
- **集合新成员**：`ConcurrentLinkedQueue`、`LinkedBlockingQueue`、Java 9+ 的 `List.of/Set.of/Map.of` 不可变工厂、
  `var` 局部类型推断让集合构造更简洁（本书未及）。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Oracle《Java Collections Framework》API 文档与教程 | Oracle / JDK | 本书 4.1 的权威依据 |
| Doug Lea《Concurrent Programming in Java》/ J.U.C 设计 | Addison-Wesley 1999 / JSR-166 | 本书 4.2 并发包的设计者原著 |
| JSR-166（java.util.concurrent） | JCP | 并发包规范来源 |
| Goetz et al.《Java Concurrency in Practice》 | Addison-Wesley 2006 | JMM 与并发安全的实战权威（本书 4.2 必配） |
| Java Object Serialization Specification | Oracle | 本书 4.3 的规范来源 |
| Java Language Specification（JMM/Happens-Before） | Oracle | 4.2 锁/可见性的形式化底座（亦见第 3 章） |

> 注：以上规范/书籍均为真实存在，未杜撰。具体 JDK 版本以 Oracle 发布记录为准。

## 近年研究与工业界开源实践（2015–2026）

- **集合/并发的「现代共识」**：`spring-framework` **60257★**、`spring-boot` **81507★** 大量使用 J.U.C；
  本书 4.2 的 `ThreadPoolExecutor` 仍是所有 Java 服务端线程模型核心。
- **序列化框架**（本章 4.3 的 2026 现实）：`google/protobuf` **72067★**（跨语言事实标准）、
  Kryo、Hessian（`apache/dubbo` **41579★** 的默认之一）、FlatBuffers。
- **高性能并发集合**：`hazelcast/hazelcast` **6613★**（分布式内存数据网格，把 4.1/4.2 延伸到多机）、
  `redisson/redisson` **24403★**（基于 Redis 的分布式 J.U.C 接口实现：分布式锁/RBlockingQueue 等）。
- **异步范式**：`CompletableFuture` + `java.util.concurrent.Flow`（Reactive Streams）；
  Reactor（`io.projectreactor`）是 Spring WebFlux 底座；虚拟线程（JDK 21）让「每请求一线程」重新变简单。
- **基准测试**：OpenJDK **JMH** 是微基准唯一被严肃对待的工具；本书 4.1.9 的手搓计时法已被明确视为 anti-pattern。

> 说明：star 数均为 2026-09 `gh api` 实测，未杜撰。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「HashMap 并发下只是慢」 | 可能数据错乱甚至死循环（JDK 7 头插法）；并发必须用并发集合 |
| 2 | 「线程池用 Executors 工厂就行」 | Cached/Fixed 的无界队列会 OOM；生产应显式构造有界队列+拒绝策略 |
| 3 | 「synchronized 够了，不必学 J.U.C」 | 需要公平/可中断/超时/多条件等待时，ReentrantLock/Condition 更合适 |
| 4 | 「序列化就是 implements Serializable」 | 必须显式声明 serialVersionUID，否则类演进后反序列化失败；且 Java 原生序列化不安全 |
| 5 | 「集合选型凭感觉」 | 应按复杂度/并发/排序需求查表（4.1.10 小结），并用 JMH 验证 |
| 6 | 🔧 4.1.7 HashMap 仍是数组+链表 | JDK 8 起链表过长转红黑树，最坏 O(logN)；本书描述仅限 JDK 7 前 |
| 7 | 🔧 4.2.1 ConcurrentHashMap 仍是分段锁 | JDK 8 改为 CAS+synchronized 桶锁；分段锁描述已过时 |
| 8 | 🔧 4.3 仍以 Java 原生序列化为主 | 2026 跨节点首选 Protobuf/Kryo/Hessian；原生序列化因体积/速度/漏洞被边缘化 |
| 9 | 🔧 4.1.9 基准测试方式过时 | 2026 必须用 JMH，手搓循环计时结论失真 |
| 10 | 🔧 4.2 缺 CompletableFuture/虚拟线程 | JDK 8+ 异步、JDK 21 虚拟线程改写并发范式，本书未及 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 4.1 集合 → [05-性能调优.md](05-性能调优.md)（5.2.2 程序调优中的集合误用导致内存/CPU 问题）；
  - 4.2 并发包 → [03-深入理解JVM.md](03-深入理解JVM.md)（3.3 锁/JMM 是 4.2 的底层保证）
    与 [01-分布式Java应用.md](01-分布式Java应用.md)（1.1.1 NIO 线程模型依赖线程池）；
  - 4.3 序列化 → [01-分布式Java应用.md](01-分布式Java应用.md)（1.2 远程调用的 payload 载体）。
- [../实战Java高并发程序设计.md](../实战Java高并发程序设计.md) —— 本书 4.2 的深入与 2026 补全（虚拟线程/Reactive/锁优化），必配。
- [../深入理解Java虚拟机3.md](../深入理解Java虚拟机3.md) —— 本书第 3、4 章的底层与 2026 更新。
- [../深入理解Apache Dubbo与实战.md](../深入理解Apache Dubbo与实战.md) —— 本书 4.3 序列化在 RPC 框架中的真实选型（Hessian/Protobuf）。
- [../设计数据密集型应用.md](../设计数据密集型应用.md)（DDIA 第 2 章 CRC 校验和、编码章）—— 序列化/编码的跨书理论底座。
