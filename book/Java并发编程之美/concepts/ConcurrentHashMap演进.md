# ConcurrentHashMap 演进

> 定位：从 JDK 7 的 **Segment 分段锁**到 JDK 8 的 **CAS + 桶级 synchronized + 红黑树 + CounterCell 散布计数**。这是 Java 并发容器最重要的一次重写。
> 对应《Java并发编程之美》第 5、6 章相关源码剖析；JDK 8 版本基于 JDK 8 源码。

## 一、是什么（最小示例）

```java
ConcurrentHashMap<String, Long> counter = new ConcurrentHashMap<>();

counter.putIfAbsent("k", 1L);                 // 单键原子
counter.computeIfAbsent("k", k -> 0L);        // 复合逻辑也原子（在桶锁内执行）
counter.merge("k", 1L, Long::sum);            // 计数首选

long precise  = counter.mappingCount();       // 推荐：long，避免 int 溢出
int  saturated = counter.size();              // 弱一致结果，且会截断到 Integer.MAX_VALUE
```

`computeIfAbsent` 的映射函数里**绝不能再修改同一个 map**（见误区 4）。

## 二、实现原理（源码级，JDK 8）

**1）整体结构**：`Node<K,V>[] table`，锁粒度从"一段"缩小到"**一个桶（bin）**"。空桶插入用 CAS（无锁），非空桶在**桶头节点**上 `synchronized`，配合 volatile 读实现无锁 `get`。

**2）关键常量**：`TREEIFY_THRESHOLD = 8`、`UNTREEIFY_THRESHOLD = 6`、`MIN_TREEIFY_CAPACITY = 64`、`MOVED = -1`（正在迁移）、`TREEBIN = -2`、`RESERVED = -3`、`HASH_BITS = 0x7fffffff`。哈希用 `spread(h) = (h ^ (h >>> 16)) & HASH_BITS`，把高位混入低位以减少低位碰撞。

**3）树化条件**：链表长度达到 8 **且** `table.length >= 64` 时才转红黑树，否则优先 `resize`——因为小表时扩容比树化更能摊薄成本。树节点包装在 `TreeBin` 里（持有 root，并用 `lockState` 的 `WRITER/WAITER/READER` 三态 + CAS + park 实现读写锁），因此桶头始终是可加锁的普通对象。扩容拆树时若节点数 ≤ 6 会退回链表。

**4）计数：与 LongAdder 同源**：`baseCount` + `CounterCell[] counterCells`，`addCount(x, check)` 先尝试 `casBaseCount`，失败则 `fullAddCount`（初始化/扩容/rehash 流程与 `Striped64.longAccumulate` 几乎一致）。`sumCount()` 遍历求和，所以 `size()` 在并发下是**估计值**；JDK 8 新增 `mappingCount()` 返回 `long`，是官方推荐的取规模方式。

**5）协作扩容**：`sizeCtl` 充当状态机（< 0 表示正在初始化或迁移），线程通过 `transferIndex` 领取一个 `stride`（默认 `MIN_TRANSFER_STRIDE = 16`）的桶区间；迁移完的桶置为 `ForwardingNode`（hash = MOVED），其他线程遇到它便 `helpTransfer` 一起搬。读操作命中 ForwardingNode 会转到 `nextTable` 继续查找。

**6）JDK 7 的 Segment（对照）**：`Segment extends ReentrantLock`，数量由 `concurrencyLevel`（默认 16）决定并向上取到 2 的幂；每个 Segment 内是 `HashEntry[]` + 链表。`size()` 先做两次**不加锁**的累加，若两次结果一致就直接返回，否则锁住**所有** Segment 再统计——这是 JDK 7 时代"尽量不全局加锁"的折中。

## 三、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 8 | 彻底重写：去掉 Segment，改为数组 + 链表/红黑树、CAS + 桶级 `synchronized`、`CounterCell` 散布计数、协作扩容；新增 `mappingCount()`、`reduce*`、`forEach*`、`search*`、`compute*`、`merge` 等批量/函数式方法 |
| JDK 9 | JEP 193（Variable Handles）：内部 volatile/CAS 访问改为 VarHandle；`computeIfAbsent` 增加递归更新检测，递归修改同一键改抛 `IllegalStateException`（JDK 8 是死锁/未定义行为） |
| JDK 11 | 无公开 API 变化 |
| JDK 17 | 无公开 API 变化；JEP 403（JDK 16）强封装后无法再反射其私有字段做"取 size"之类的黑科技 |
| JDK 21 | JEP 444 虚拟线程：容器本身无阻塞语义，不会钉住 carrier；但若映射函数内在 `synchronized` 中做阻塞 IO，JDK 21 会钉住（JDK 24 JEP 491 消除） |
| JDK 25 | 无新 API；随 JEP 471（JDK 23 弃用）/ JEP 498（JDK 24 告警）推进，内部 Unsafe 访问已由 VarHandle 取代 |

## 四、经典论文

| 论文 | 出处 | 与 CHM 的关系 |
| --- | --- | --- |
| The java.util.concurrent Synchronizer Framework | Doug Lea, J. ACM 52(3), 2005 | JDK 7 Segment 依赖的 `ReentrantLock` 的设计说明 |
| Algorithms for Scalable Synchronization on Shared-Memory Multiprocessors | Mellor-Crummey & Scott, TOCS 9(1), 1991 | 分段锁（lock striping）与可伸缩同步的经典依据 |
| Counting Networks | Aspnes, Herlihy & Shavit, STOC 1991 / J. ACM 1994 | `CounterCell` 散布计数的思想源头：把单一计数器拆成网络/数组以降低争用 |
| Distributing Hot-Spot Addressing in Large-Scale Multiprocessors | Yew, Tzeng & Lawrie, ISCA 1987 | 热点地址分散策略，解释为何"分段/分槽"能提升可伸缩性 |
| Linearizability: A Correctness Condition for Concurrent Objects | Herlihy & Wing, TOPLAS 12(3), 1990 | 判定 `put/get` 线性化、以及 `size()` 为何不满足线性化的依据 |
| Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms | Michael & Scott, PODC 1996 | 迁移/帮助（helping）与惰性更新的经典技巧，协作扩容精神相通 |
| Software Transactional Memory | Shavit & Touitou, PODC 1995 | 另一条路线：`computeIfAbsent` 这种"原子复合更新"在 STM 中由事务承担 |
| The Art of Multiprocessor Programming | Herlihy & Shavit, 2008 / 2012 | 教材第 13 章专讲并发哈希表与天然并行性 |
| The Java Memory Model | Manson, Pugh & Adve, POPL 2005 | `table`、`Node.val`、`next` 的 volatile 语义与 happens-before |

## 五、近年研究与工业界实践

**同行评审论文**
- NVTraverse（Friedman 等，PPoPP 2021）：NVRAM 上"只保证到达终态"的遍历策略，为持久化哈希表/计数结构提供新思路。
- RefinedRust（Gäher 等，2024）：用类型系统 + 分离逻辑自动验证并发数据结构，分片哈希表是常见案例。
- Understanding Real-World Concurrency Bugs in Go（Tu 等，ASPLOS 2019）：统计显示并发 map 访问（尤其是"检查后再写入"的复合操作）是高频缺陷，对应 Java 侧应当用 `computeIfAbsent`/`merge` 而非 `get` + `put`。

**工业界资料**
- OpenJDK：`src/java.base/share/classes/java/util/concurrent/ConcurrentHashMap.java` — https://github.com/openjdk/jdk
- JCTools — https://github.com/JCTools/JCTools ：提供 `NonBlockingHashMap` 等替代实现，可用于对比不同并发策略
- JMH — https://github.com/openjdk/jmh （吞吐基准）；jcstress — https://github.com/openjdk/jcstress （验证 `size()` 弱一致与 `computeIfAbsent` 语义）
- Netty — https://github.com/netty/netty ：大量使用 CHM 管理 Channel 与配置，是真实压测场景的参考
- Chronicle-Queue — https://github.com/OpenHFT/Chronicle-Queue ：堆外持久化队列，代表"绕开堆内哈希表"的另一条工程路线

## 六、常见误区 + 跨语言对照

**常见误区**
1. "CHM 完全无锁"——JDK 8 起冲突桶用的是 `synchronized`，只有空桶插入、计数和状态位切换用 CAS。
2. "`size()` 是精确值"——求和遍历无快照，并发下是估计值；要规模用 `mappingCount()`。
3. "链表超过 8 就树化"——还要求 `table.length >= 64`，否则优先扩容。
4. "`computeIfAbsent` 里可以递归建值"——同一键递归更新在 JDK 8 会死锁/行为未定义，JDK 9+ 抛 `IllegalStateException: Recursive update`；映射函数必须是纯函数式的。
5. "CHM 允许 null"——不允许 null key 与 null value，因为 `get` 返回 null 要能明确表示"不存在"。
6. "`get` + `put` 组合就够了"——不是原子操作；用 `putIfAbsent`/`computeIfAbsent`/`merge`。
7. "`concurrencyLevel` 还能调并发度"——JDK 8 里它只作为初始容量的提示，不再决定锁数量。
8. "迭代时会抛 `ConcurrentModificationException`"——CHM 迭代器是**弱一致**的，不抛异常，但可能看不到迭代期间的更新。

**跨语言对照**

| 语言 | 对应设施 | 关键差异 |
| --- | --- | --- |
| Java | `ConcurrentHashMap`（桶级锁 + 树化 + 散布计数） | 单键原子 + 复合更新 API 齐全；`size()` 弱一致 |
| C++ | 标准库无并发哈希表；常用 `folly::ConcurrentHashMap`（Java 8 CHM 的 C++ 移植）或 libcuckoo | 需自行处理内存回收（hazard pointer / RCU），无 GC 兜底 |
| Rust | 无标准实现；社区用 `dashmap`（分片 `RwLock`）或 `scc::HashMap` | 借助所有权模型防止数据竞争，多靠分片锁而非树化 |
| Go | `sync.Map`（只读副本 + dirty map + misses 提升，Go 1.9 起） | 针对"读多写少、键集合稳定"优化；通用高写场景仍需分片 map + RWMutex |
| Erlang | `ets` 表（`public`/`protected`，可设 `write_concurrency`、`read_concurrency`） | 运行时代为分片与原子化，行级/表级锁由 OTP 管理 |
| Python | 无并发 map；`dict` 在 GIL 下单操作安全，复合操作需 `threading.Lock` | GIL 提供的是"操作级"安全而非"事务级"原子性 |
