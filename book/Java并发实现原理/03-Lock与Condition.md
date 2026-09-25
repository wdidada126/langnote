# 第 3 章 Lock与Condition（原书 pp.49-82）

> **本书最体现"手写"价值的章节**：从零实现一个简化版 AQS（`MyLock` + `MyCondition`），再据此实现 `ReentrantLock`/`ReentrantReadWriteLock`/`StampedLock` 思路。与《艺术》5 章源码 + 《之美》`concepts/AQS抽象同步队列.md` 互补——本书是"自己写一遍"，另两本是"读 JDK 源码"。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| 手写 AQS | `state` + FIFO 等待队列 + `LockSupport.park/unpark` + CAS 入队 |
| `ReentrantLock` | 公平/非公平；可重入计数；可中断/超时 |
| `ReentrantReadWriteLock` | 读写分离；高 16 读 / 低 16 写 |
| `Condition` | 手写条件队列 + `await/signal` |
| `StampedLock` | 🔧 乐观读思路（本书 JDK 8 版可能在后续补） |

## 二、核心精讲

### 2.1 手写 AQS（MyLock）
- **`state`**：`volatile int`，用 CAS 抢（0→1 表示拿到锁）。
- **等待队列**：抢不到的线程封装成 Node，CAS 挂到队列尾（`tail`），然后 `LockSupport.park()` 挂起。
- **释放**：`unpark` 队列头节点（手写版可简单 unpark head；JDK 真实从 tail 反向遍历，因 `next` 不可靠，见《之美》AQS 专篇）。
- **可重入**：`state` 累加；释放递减至 0 才真正释放。
- 公平 vs 非公平：公平版 `tryAcquire` 先查队列有无前驱。

### 2.2 `ReentrantReadWriteLock` 手写
- `state` 32 位拆分：高 16 位读计数，低 16 位写持有。
- 写锁：CAS 抢低 16 位（且高 16 为 0）；读锁：`CAS` 高 16 位 +1（写锁空闲时）。
- 写→读可降级（持写时拿读再放写）；读→写不可（死锁）。

### 2.3 `Condition` 手写
- 每个 `MyCondition` 一个条件队列（链表）；`await()`：释放锁 → 入条件队列 → `park`；`signal()`：把条件队列头节点移回 AQS 同步队列 → `unpark`。
- 优势：一个 `Lock` 多 `Condition`（如 `ArrayBlockingQueue` 的 notEmpty/notFull），`wait/notify` 做不到。

### 2.4 `StampedLock`（🔧 补充）
- 本书 JDK 8 基线手写多停在读写锁；**`StampedLock`（JDK 8）** 提供**乐观读**：`tryOptimisticRead()` 拿戳 → 读 → `validate(stamp)` 校验期间有无写 → 无则免锁读，有则升级读锁。读多写极少时远快于读写锁（见《艺术》5 章 / 《之美》锁讨论）。

## 三、版本演进

- **JDK 5**：`Lock`/AQS 引入（Doug Lea），本书手写对象的官方原版。
- **JDK 8**：`StampedLock`（非 AQS，CLH 变体 + 乐观读）。
- **JDK 9+**：AQS 内部 `Unsafe`→`VarHandle`。
- **JDK 21+**：AQS 等待不 pin 虚拟线程（对比 `synchronized`）。

## 四、经典论文 / 原始文献

- **Doug Lea, "The java.util.concurrent Synchronizer Framework" (SCIENCE 2004)**——AQS 权威（手写对照官方）。
- **Craig (1993) / Magnussen et al. (IPPS 1994)**——CLH/MCS 队列锁。
- **Hoare, "Monitors" (CACM 1974)**——Condition 语义。

## 五、工业界前沿

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **openjdk/jdk** | 23.4k | `AQS`/`ReentrantLock`/`ReentrantReadWriteLock`/`StampedLock`/`Condition` |
| **JCTools/JCTools** | 3.9k | 手写无锁同步器，绕开 AQS |
| **LMAX-Exchange/disruptor** | 18.5k | 自研 `Sequence` 同步协议，无 AQS |
| **ben-manes/caffeine** | 17.9k | 读写锁 + 分段 + 无锁混合 |

## 六、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "手写 AQS 用 unpark head 即可" | JDK 真实从 tail 反向遍历（`next` 不可靠） |
| 2 | "读写锁读多必快" | 写频繁/写饥饿更慢；考虑 StampedLock 🔧 |
| 3 | "读锁可升级写锁" | 死锁；仅写→读降级 |
| 4 | "AQS 万能" | StampedLock、无锁结构刻意不用 AQS |
| 5 | "手写用 Unsafe" | 🔧 JDK 21+ 废弃；改 VarHandle |
