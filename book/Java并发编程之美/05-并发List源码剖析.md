# 第 5 章 Java 并发包中并发 List 源码剖析（原书 pp.105-114）

> 主角：`java.util.concurrent.CopyOnWriteArrayList`（本书讲的"并发 List"其实是它）
> 相关：`CopyOnWriteArraySet`、`Collections.synchronizedList`、`Vector`、`ConcurrentLinkedQueue`
> 延伸：[concepts/并发模型跨语言对比.md](concepts/并发模型跨语言对比.md)

## 一、本章地图

| 小节 | 主题 | 页码 |
| --- | --- | --- |
| 5.1 | 介绍 | 105 |
| 5.2 | 主要方法源码解析（初始化 / 添加 / 获取 / 修改 / 删除 / 弱一致迭代器） | 106-113 |
| 5.3 | 总结 | 114 |

## 二、核心精讲

### 5.1 为什么是 Copy-On-Write

并发 List 有三种路线，本书选了最"读友好"的一条：

| 方案 | 读 | 写 | 适用 |
| --- | --- | --- | --- |
| `Vector` / `Collections.synchronizedList` | 加锁 | 加锁 | 几乎已被淘汰（读写都串行） |
| `CopyOnWriteArrayList` | **完全无锁** | 加锁 + 复制整个数组 | **读多写极少的集合**（监听器列表、配置白名单） |
| `ConcurrentLinkedQueue` / `LinkedBlockingQueue` | 无锁/双锁 | 无锁/双锁 | 队列场景（第 7 章），不支持随机访问 |

```
核心结构：
private transient volatile Object[] array;      // volatile：保证读线程立刻看到新数组
final transient ReentrantLock lock = new ReentrantLock();
```

### 5.2 源码逐节

**(1) 初始化**

```java
public CopyOnWriteArrayList() { setArray(new Object[0]); }     // 空数组起步
public CopyOnWriteArrayList(E[] toCopyIn) { setArray(Arrays.copyOf(toCopyIn, toCopyIn.length, Object[].class)); }
```
注意：**它自己也 copy 一份**（构造 `CopyOnWriteArrayList(list)` 时复制传入集合），避免外部改动影响内部。

**(2) 添加元素 add**

```java
public boolean add(E e) {
    final ReentrantLock lock = this.lock;
    lock.lock();
    try {
        Object[] es = getArray();
        int len = es.length;
        es = Arrays.copyOf(es, len + 1);      // ★ 复制：O(n) 时间与 O(n) 临时内存
        es[len] = e;
        setArray(es);                          // volatile 写：后续读立刻可见
        return true;
    } finally { lock.unlock(); }
}
```
关键：`setArray` 是 **volatile 写**，利用了 JMM 的 happens-before（见 [concepts/JMM与happens-before.md](concepts/JMM与happens-before.md)）—— 读线程不需要加锁，只需要一次 volatile 读。

**(3) 获取指定位置 get**

```java
@SuppressWarnings("unchecked")
private E elementAt(Object[] a, int index) { return (E) a[index]; }
public E get(int index) { return elementAt(getArray(), index); }
```
无锁、无 CAS、单次数组访问 —— **读性能接近普通 ArrayList**，这是它最大的价值。

**(4) 修改 / 删除**

```java
public E set(int index, E element) {
    final ReentrantLock lock = this.lock;
    lock.lock();
    try {
        Object[] es = getArray();
        E oldValue = elementAt(es, index);
        if (oldValue != element) {
            es = es.clone();                     // 即使只改一个元素也要整体复制
            es[index] = element;
            setArray(es);
        }
        return oldValue;
    } finally { lock.unlock(); }
}
```
> **注意 `set` 中的 `setArray` 即使值相同也不更新的优化**：JDK 8+ 加了 `if (oldValue != element)` 判断，避免无谓的 volatile 写 —— 因为 volatile 写有 store barrier 成本。这是本书没提到但很值得记的细节。

**(5) 弱一致性的迭代器 COWIterator**

```java
public Iterator<E> iterator() {
    return new COWIterator<E>(getArray(), 0);   // ★ 快照：指向迭代器创建那一刻的数组
}
```
因此：
- 迭代期间其他线程的**增/删不会被看到**，也不会抛 `ConcurrentModificationException`（这点与 `ArrayList` 完全不同）；
- 迭代器**不支持 `remove()`**（会抛 `UnsupportedOperationException`）—— 因为它作用在不可变的旧快照上。

```java
CopyOnWriteArrayList<String> l = new CopyOnWriteArrayList<>(List.of("a", "b"));
for (String s : l) {
    l.add("c");        // ✅ 不抛 CME，但本次循环看不到 "c"
}
```

### 5.3 总结：什么时候用 / 不用

✅ **适合**：监听器/回调列表、Spring 的 `ApplicationListener`、路由表、黑白名单、权限配置 —— 典型特征是"**几百个元素 + 几乎不写**"。
❌ **不适合**：元素多（>1000）或写频繁 —— 每次 add 都要复制整个数组 + 产生一次垃圾；**内存占用峰值翻倍**。

## 三、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 5 | `CopyOnWriteArrayList`/`CopyOnWriteArraySet` 引入 |
| JDK 8 | `CopyOnWriteArrayList` 内部改用 `COWIterator`，加入 `spliterator()`；`set` 加 `oldValue != element` 短路优化 |
| JDK 9+ | 使用 `VarHandle` 访问 `array` 字段（替代 `Unsafe`），并随 JEP 403（JDK 17）成为内部实现细节 —— **API 与语义没变** |
| JDK 11 | `toArray(size -> new String[size])` 等改进（Collection 接口新增默认方法） |
| JDK 21+ | `CopyOnWriteArrayList` 的读路径**对虚拟线程完全无害**（无锁）；但**写依然加 ReentrantLock**，虚拟线程在锁内阻塞在 JDK 24 前会钉住 carrier，参考 [concepts/虚拟线程Loom.md](concepts/虚拟线程Loom.md) |

> 🔴 **JDK 21 的一个重要提醒**：不要把 COW 列表当作"虚拟线程友好"的结构 —— 大量虚拟线程**写**它时会全部串行在 `ReentrantLock` 上。替代思路：`ConcurrentHashMap.newKeySet()`、不可变集合 + `AtomicReference` 整体替换（这其实是手写 COW 的升级版：把"复制整个数组"换成"引用整体替换"，读只需一次 `get`）。

```java
// 手写 COW（读多写少 + 元素大时的更省 utils 做法）
private final AtomicReference<Map<String, Route>> routes = new AtomicReference<>(Map.of());
void put(String k, Route r) {
    Map<String, Route> next = new HashMap<>(routes.get());  // 先在外部复制
    next.put(k, r);
    routes.set(next);                                        // 一次引用替换 = 发布
}
Route get(String k) { return routes.get().get(k); }         // 完全无锁
```

## 四、经典论文 / 原始文献

| 主题 | 文献 | 出处 |
| --- | --- | --- |
| **持久化数据结构的理论基础** | Driscoll, Sarnak, Sleator & Tarjan, *Making Data Structures Persistent* | J. Comput. Syst. Sci. 38(1), 1989 —— COW 是 "partially persistent" 的最简单特例 |
| 纯函数式数据结构 | Okasaki, *Purely Functional Data Structures* | 1998（Cambridge，§2.x lazy evaluation / amortized persistence） |
| **并发容器的核心语义** | Herlihy & Wing, *Linearizability: A Correctness Condition for Concurrent Objects* | TOPLAS 12(3), 1990 —— 用于论证 Iterator 的"弱一致性"是线性一致还是 sequential weak 语义 |
| 快照与 MVCC 源头 | Bernstein & Hadzilacos & Goodman, *Concurrency Control and Recovery in Database Systems* | 1987 |
| 并发写时复制树 | Kung & Lehman, *Concurrent Manipulation of Binary Search Trees* | ACM TODS 5(3), 1980 |

> **本书没讲但重要的区分**：JDK 的并发容器统称 *weakly consistent* —— Javadoc 明确写了迭代器不抛 CME、也不保证马上看到更新。这与 MVCC 的"快照读"是同一思想体系。

## 五、近年研究与工业界前沿（2020-2026）

**同行评审论文**

- **持久内存（PMEM）上的持久并发数据结构** 是 2020 年后最活跃的方向之一，代表工作：
  - Friedman, Ben-David, Wei, Blelloch & Petrank, *NVTraverse: In NVRAM Data Structures, the Traversal is Half the Battle*, **PPoPP 2021** —— 指出遍历路径（而非仅修改点）才是持久化的开销来源，对"整棵树/整表 COW"的成本分析很有启发。
  - Correia, Felber & Ramalhete, *Romulus: Efficient Algorithms for Persistent Transactional Memory*, SPAA 2018（后续 2020+ 有扩展）—— 用"两份副本交替"的方式做持久更新，**本质上就是全局版的 copy-on-write**。
- **Linux/文件系统侧的 COW** 也在同期持续演进：Btrfs/ZFS、overlayfs、reflink copy —— 与第 5 章是同一思想在存储层的落地（都是"延迟复制 + 原子地替换引用"的变体）。

**工业界资料（非同行评审）**

- 使用案例：Spring Framework 的 `AbstractApplicationContext` 监听器列表、Guava / Caffeine 的某些 listener 集合、Netty 的部分 handler map。搜索技巧：`grep -rn "CopyOnWriteArrayList" --include=*.java` 在任一框架源码里都能找到。
- 反面教材：把 COW list 用作**事件总线**（高频 add/remove + 遍历）会导致 GC 压力与 O(n²) 复制开销，实践中应换成 `ConcurrentHashMap.newKeySet()` 或 CopyOnWrite 的分段版本。

## 六、常见误区 / 本书需修正之处

1. ❌ **"`CopyOnWriteArrayList` 是线程安全的 ArrayList，可以到处替换 ArrayList"** —— 错误：写操作 O(n) 且有双倍内存峰值，仅适合读多写极少的小集合。
2. ❌ **"迭代器能看到实时修改"** —— 不，迭代器是**创建时刻的快照**（弱一致），且不支持 `remove()`。
3. ❌ **`size()` + `get(i)` 循环是原子的** —— 不，两次独立调用之间集合可能变化；要遍历请用 `iterator()`/for-each（拿到快照）或加锁。
4. ⚠️ **本书没提 `CopyOnWriteArraySet`** —— 它就是 `CopyOnWriteArrayList` 包一层 `al.contains(e)` 判重，**写成本随元素数量线性增长**，超小集合才用；正确替代是 `ConcurrentHashMap.newKeySet()`。
5. ⚠️ **本书写"并发 List"容易让人以为有更多选择** —— 实际上 JDK 的并发 List 只有 COW 一种（有随机访问需求时）；其余场景应该用队列（第 7 章）或 `ConcurrentHashMap` 派生结构。

## 七、跨语言对照

| 语言 | COW / 不可变读方案的等价物 | 备注 |
| --- | --- | --- |
| Java（本书） | `CopyOnWriteArrayList`（volatile 数组 + ReentrantLock 写） | 只能整体复制，写是 O(n) |
| C++ | `std::shared_ptr<const std::vector<T>>` + `atomic_load/store`（俗称 RCU / atomic shared_ptr，**C++20 起 `std::atomic<std::shared_ptr<T>>` 可用**） | 这是 COW 的更优形式：只替换指针；缺点是旧副本要等最后一个读者离开才释放（GC vs 引用计数） |
| Rust | `Arc<RwLock<Vec<T>>>`；追求无锁读用 **`arc-swap`** crate 的 `ArcSwap`，或专注于读多写少的 `evmap` | Rust 的所有权让"发布后不可变"能被编译器检查，难以被误修改 |
| Go | 惯例：`atomic.Value` 存 `[]T` 快照；或每次写时 copy 一份 slice 再整体替换 | Go 1.18 引入泛型后写法更干净（此前需 `interface{}` 装箱） |
| Erlang/OTP | 语言级别不可变数据结构 + `ets` 表（读写锁粒度可调） | 由于进程间不共享可变状态，很多场景下根本不需要 COW |
| Clojure | **持久化数据结构（HAMT / persistent vector，Okasaki 系的落地）** | 注意：COW 是 O(n) 全复制，持久化结构是**结构共享 + O(log n) 部分复制**，是更高阶的版本 |

> 一句话总结跨语言：**"读多写极少的集合" 的通用解法是"不可变快照 + 原子地替换引用"**，Java 的 COW list 是最朴素的一版，Clojure 的持久化向量是进化版，C++20 的 `atomic<shared_ptr>` / Rust 的 `arc-swap` 是手动版。
