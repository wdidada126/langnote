# 专篇：ConcurrentHashMap 三代演进 —— 从分段锁到 CAS + 红黑树

> 对应本书第 5 章（并发 List）与第 7 章（并发队列）之间的**空白地带**。
> 本书成书于 JDK 8 时代，但只讲了 `CopyOnWriteArrayList` 与队列，
> **对 Java 并发容器里最重要的 ConcurrentHashMap 着墨不多**。
> 而 CHM 恰恰是理解"JDK 8 并发思想转向"的最佳样本：
> **从"锁分片"转向"乐观 CAS + 细粒度 synchronized + 协助扩容"**。

## 一、本章地图

```
JDK 5/6：Segment[] 分段锁（16 段，ReentrantLock）
   ↓  瓶颈：段内串行、扩容只能整段、读要 volatile 两次跳转
JDK 7：Segment 惰性初始化 + 内部优化（架构不变）
   ↓
JDK 8：推倒重写 —— CAS 插空桶 / synchronized 锁桶头 / 链表转红黑树 / 多线程协助扩容
   ↓
JDK 9+：VarHandle 替换 Unsafe、computeIfAbsent 递归检测、并行聚合操作
   ↓
JDK 21+：虚拟线程 + JEP 491 解决 synchronized 钉住问题
```

## 二、JDK 5/6/7：分段锁（Segment）

```java
// JDK 7 结构（简化）
final Segment<K,V>[] segments;      // 默认 16 段，不可扩容
static final class Segment<K,V> extends ReentrantLock {
    transient volatile HashEntry<K,V>[] table;   // 段内的小哈希表
    transient int count;                          // 段内元素数
}
```

| 特性 | 说明 |
| --- | --- |
| `concurrencyLevel` | 构造参数，默认 16 → 决定 Segment 数（向上取 2 的幂） |
| 写操作 | 先按 `hash` 高位定位 Segment，**仅锁该段** |
| 读操作 | **全程无锁**：`HashEntry.value` 是 `volatile`，`next` 是 final（JDK 7） |
| 扩容 | **只扩段内数组**，各段独立，不互相阻塞 |
| `size()` | 先两次无锁求和，不一致则**锁住所有段**再求和（很重） |

**为什么被淘汰**：

1. 段数固定 → 热点 key 集中在一段时退化为串行；段数太多则内存浪费（每段一个 `ReentrantLock` + 数组头）。
2. 定位要**两次哈希**（先找段、再找桶），多一次内存跳转。
3. `size()` 的"锁全表"路径是隐藏炸弹。
4. 链表过长仍会退化成 O(n) 查找（JDK 7 没有树化）。

## 三、JDK 8：重写后的核心结构

```
   table[]（长度恒为 2 的幂）
   ┌────┬────┬────┬────┬────┬────┐
   │null│Node│Moved│TreeBin│Reserv│...
   └────┴────┴────┴────┴────┴────┘
           │     │      │      │
           │     │      │      └─ ReservationNode（hash = -3）computeIfAbsent 占位
           │     │      └─ TreeBin（hash = -2）红黑树，内部持有读写锁状态
           │     └─ ForwardingNode（hash = -1 / MOVED）扩容中标记
           └─ 普通链表头（hash >= 0）
```

### 3.1 `sizeCtl` 一个字段的四种含义

| `sizeCtl` 值 | 含义 |
| --- | --- |
| `0` | 表未初始化 |
| `> 0` | 未初始化时 = 初始容量；已初始化后 = **扩容阈值**（0.75 × n） |
| `-1` | **正在初始化**（`CAS` 抢到锁的线程） |
| `< -1` | **正在扩容**：`-N` 表示有 `N-1` 个线程在协助 transfer |

> 这是 JDK 源码里"用位模式压缩状态"的经典手法，与 `ThreadPoolExecutor` 的 `ctl`
> 异曲同工（见本书第 8 章笔记）。

### 3.2 写路径：三步走

```java
// putVal 核心（JDK 8+，极度简化）
if (tab == null)                  initTable();          // CAS sizeCtl = -1 抢占
else if ((f = tabAt(tab, i)) == null) {
    if (casTabAt(tab, i, null, new Node(...))) break;   // ① 空桶：纯 CAS，无锁
}
else if (f.hash == MOVED)         helpTransfer(...);    // ② 遇到搬运节点：帮忙扩容
else {
    synchronized (f) {                                  // ③ 非空桶：只锁桶头
        if (binCount >= TREEIFY_THRESHOLD) treeifyBin(tab, i);
    }
}
```

**为什么是 `synchronized` 而不是 `ReentrantLock`？**

- 锁住的是**一个桶**，粒度极小，竞争概率低；
- `synchronized` 有 **偏向锁/轻量锁/自适应自旋**（JDK 6+），在这种"极短临界区 + 低争用"场景下比 `ReentrantLock` 更省（少一个 AQS 节点对象）；
- 省内存：不需要每个桶一个 Lock 对象。

> **JDK 15 (JEP 374) 起偏向锁被默认禁用并在后续版本移除**——
> 因为现代负载下偏向锁的撤销成本 > 收益。但轻量锁/膨胀锁路径仍在，`synchronized` 依然廉价。

### 3.3 树化（treeify）的三个阈值

| 常量 | 值 | 含义 |
| --- | --- | --- |
| `TREEIFY_THRESHOLD` | 8 | 链表长度 ≥ 8 **且**满足下条时转红黑树 |
| `MIN_TREEIFY_CAPACITY` | 64 | 表长度 < 64 时**优先扩容**而不是树化（扩容更划算） |
| `UNTREEIFY_THRESHOLD` | 6 | 扩容/删除后树节点 ≤ 6 时**退回链表** |

> 8 这个数字来自**泊松分布**：默认负载因子 0.75 下，桶中元素数服从 λ≈0.5 的泊松分布，
> 长度达到 8 的概率约 **千万分之六**——说明发生树化几乎一定是哈希函数被攻击或 key 的 `hashCode()` 写得极差。

**`TreeBin` 的读写锁状态**：`TreeBin` 不直接用 `ReentrantReadWriteLock`，而是自己用
`lockState`（`volatile int` + CAS）实现：无锁读（lockState ≥ 0 走链表遍历），写操作才锁。
**读操作在红黑树上也是无锁的**。

### 3.4 扩容：多线程协助 transfer（最精彩的部分）

```
触发线程：CAS sizeCtl → (rs << RESIZE_STAMP_SHIFT) + 2，开始搬运
其他线程：put 时遇到 MOVED 桶 → sizeCtl < 0 → 自愿加入，各领一段 stride 去搬
```

| 机制 | 说明 |
| --- | --- |
| `stride` | 每个线程一次领 `MIN_TRANSFER_STRIDE = 16` 个桶，从**尾部往前**领（`--i`） |
| `ForwardingNode` | 搬完的桶放一个 `hash = MOVED` 的节点，告诉后来者"这里搬走了，去 nextTable 找" |
| `nextTable` | 扩容中的新表；完成后 `table = nextTable`，`sizeCtl = 0.75 × 2n` |
| `transferIndex` | 用 `volatile int` + CAS 做"领取进度"，无中心协调 |

**为什么扩容线程数有上限**：`sizeCtl` 低 16 位记录协助线程数，`MAX_RESIZERS = 65535`；
且超过一定数量后不再扩容表本身（避免大表下线程过多）。

### 3.5 `size()` 与 `mappingCount()`

`baseCount + sum(CounterCell[])` —— **和 LongAdder 完全同构**（见本目录《LongAdder与分段累加》）。
**并发下 `size()` 不是精确值**，且 `int` 可能溢出 → **请用 `mappingCount()`（返回 `long`）**。

## 四、JDK 9 → 21 的增量

| 版本 | 变化 |
| --- | --- |
| JDK 9 | `Unsafe` → **VarHandle**；`computeIfAbsent` 加入**递归更新检测**（JDK 8 里递归更新会死循环/数据错乱，JDK 9 起抛 `IllegalStateException: Recursive update`） |
| JDK 9 | 新增 `forEach/search/reduce/mappingCount/reduceEntries...` 带 `parallelismThreshold` 的**并行批量操作** |
| JDK 11+ | 持续的优化（如 `compute` 系列的锁行为修正） |
| JDK 21 | 虚拟线程：`synchronized` 在 JDK 21-23 会**钉住（pin）载体线程**，CHM 写操作是隐性风险点 |
| JDK 24 | **JEP 491: Synchronize Virtual Threads without Pinning** —— `synchronized` 不再 pin，CHM + 虚拟线程的组合终于安全 |

> 这条演进链值得记：本书（JDK 8）时期的 CHM 在虚拟线程环境下是**有坑的**，
> 直到 JDK 24 才彻底解决。

## 五、经典论文 / 原始文献

| 文献 | 贡献 |
| --- | --- |
| **Shalev, O. & Shavit, N. 2006. "Split-Ordered Lists: Lock-Free Extensible Hash Tables." JACM 53(3): 379-405.** | 用"虚拟节点 + 递归拆分桶"实现**无锁且可增量扩容**的哈希表。Java CHM 并未采用，但它是"在线扩容"这一支的奠基作 |
| **Michael, M. M. 2002. "High Performance Dynamic Lock-Free Hash Tables and List-Based Sets." SPAA '02.** | 无锁链式哈希表的实用化；讨论了删除标记 + 内存回收 |
| **Triplett, J., McKenney, P. E., Walpole, J. 2011. "Resizable, Scalable, Concurrent Hash Tables via Relativistic Programming." USENIX ATC '11.** | **"读者与写者并发扩容"的核心思路**——与 CHM 的"协助扩容 + forwarding 节点"是同一问题的两种解法；Linux 内核 rhashtable 的基础 |
| **Pagh, R. & Rodler, F. F. 2004. "Cuckoo Hashing." Journal of Algorithms 51(2).** | 另一种解决冲突/扩容的思路；O(1) 最坏查找 |
| **Fan, B., Andersen, D. G., Kaminsky, M. 2013. "MemC3: Compact and Concurrent MemCache with Dumber Caching and Smarter Hashing." NSDI '13.** | Cuckoo + 并发的工程化；`efficient/libcuckoo` 的理论基础 |
| **Maier, T., Sanders, P., Dementiev, R. "Concurrent Hash Tables: Fast and General?(?)" PPoPP '18.** | 近年对 CHM 类实现的系统评测；指出通用 CHM 与专用实现（如 `libcuckoo`）的性能差 |
| **Einziger, G., Friedman, R., Kassner, B. 2015. "TinyLFU: A Highly Efficient Cache Admission Policy." EuroSys '15 / TOCS.** | 与 CHM 组合成高性能缓存（Caffeine 的 W-TinyLFU 即基于此） |
| **Doug Lea 的 `ConcurrentHashMap.java` 类注释** | **CHM 没有论文**。Lea 在源码里写了几百行设计说明（含"为什么是 8"、"为什么用 synchronized"），是唯一权威文档 |

## 六、近年研究与工业界前沿

### 近年研究（2018-2025）

- **持久内存（PMem）哈希表**：`Dash: Scalable Hashing on Persistent Memory`（VLDB 2020）、`CCEH`、`Level Hashing` —— 在 Optane 类设备上重做哈希表的扩容与一致性模型。虽然 Intel 已退出 Optane 产品线，但这一支研究的"指纹（fingerprint）+ 桶分片"技巧已回流到内存哈希表设计。
- **学习式索引**：Kraska et al. "The Case for Learned Index Structures"（SIGMOD 2018）把哈希表的"槽位计算"换成模型预测，近年已有与并发控制结合的后续工作。
- **GPU / 异构哈希**：面向 SIMD 与 GPU 的大规模并发哈希（如 `warpcore`），强调"无锁 + 批量探测"。
- **弱内存模型验证**：用 `jcstress` / 模型检测验证 CHM 的线性一致性（与 JMM 篇呼应）。

### 工业界开源实现（2026-09 核验）

| 项目 | Stars | 说明 |
| --- | --- | --- |
| **openjdk/jdk** | 23.4k | `ConcurrentHashMap.java`（JDK 8 版约 6000+ 行，注释占比极高）、`ConcurrentSkipListMap.java` |
| **ben-manes/caffeine** | 17.9k | Java 高性能缓存事实标准；**W-TinyLFU** 淘汰策略 + 基于 CHM 的写缓冲；Spring Boot 默认缓存之一 |
| **efficient/libcuckoo** | 1.7k | 高并发 Cuckoo 哈希表（C++），学术成果落地工程的样板 |
| **crossbeam-rs/crossbeam** | 8.6k | Rust 并发工具集；`crossbeam-skiplist` 与无锁结构 |
| Go `sync.Map` | — | Go 的"读多写少"并发 map：读写分离 + dirty map 提升，思路与 CHM 不同（适合 cache 场景，不适合通用写） |
| Rust `dashmap` | — | 分片 RwLock 的并发 map，等价于"JDK 7 分段锁"思路的 Rust 复刻 |

## 七、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "CHM 的读也要加锁" | **读全程无锁**（`Node.val` volatile + `TreeBin.lockState` 判断）；树化后读走链表遍历，也无锁 |
| 2 | "JDK 8 的 CHM 还是分段锁" | JDK 8 **彻底移除 Segment**，改为 Node 数组 + CAS + 桶头 synchronized |
| 3 | "链表超过 8 就树化" | 还必须 `table.length >= 64`，否则**优先扩容** |
| 4 | "`put` 时只锁自己的桶，扩容就不影响了" | 遇到 `MOVED` 桶，**put 线程会停下来帮忙扩容**——这是 CHM 高吞吐的关键，也是"put 偶尔变慢"的原因 |
| 5 | "`size()` 是精确值" | 并发下是**估计值**；用 `mappingCount()`（long） |
| 6 | "`computeIfAbsent` 里可以再操作同一个 map" | **递归更新**：JDK 8 下可能死循环/数据丢失，JDK 9+ 抛 `IllegalStateException` |
| 7 | "CHM 保证复合操作的原子性" | `get` 后 `put` 不是原子的；必须用 `computeIfAbsent` / `merge` / `putIfAbsent` |
| 8 | "CHM 的 key/value 可以是 null" | **不允许 null**（`HashMap` 允许）。原因：`map.get(k) == null` 无法区分"不存在"与"值为 null"，在并发语义下是致命歧义 |
| 9 | "迭代器会抛 `ConcurrentModificationException`" | 不会；CHM 迭代器是**弱一致性**的，反映创建时或迭代中的某个状态 |
| 10 | "虚拟线程 + CHM 没问题" | **JDK 21-23 有 pin 风险**（synchronized 钉住载体线程），**JDK 24（JEP 491）才彻底解决** |
| 11 | "并发度高就该调大 `concurrencyLevel`" | JDK 8 起该参数**已被忽略**（仅保留兼容性），分区由 table 长度决定 |

> **本书补充定位**：本书第 5 章只讲了 `CopyOnWriteArrayList`（写时复制，适合读多写极少），
> 读者很容易误以为并发 Map 也是类似思路。这一篇讲清 CHM 是完全不同的路线，
> 并把 JDK 24 的 pinning 修复接上。


---

<!-- ===== 以下为 gitlab 端合并保留版本（2026-09-25 merge） ===== -->

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
