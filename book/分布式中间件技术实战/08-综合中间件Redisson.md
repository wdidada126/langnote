# 第 8 章　综合中间件 Redisson

> 原书第 8 章是**Redisson 的理论章**：Redisson 是「基于 Redis 的 Java 驻内存数据网格 / 分布式对象框架」，
> 它把分布式锁、并发集合、信号量、闭锁等 Java 并发原语「分布式化」。这一章先讲 Redisson 是什么、
> 常用组件怎么用，再聚焦「分布式锁实战」——本质是**第 7 章 7.3 手写 Redis 锁的工业级封装**。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 8.1 Redisson 概述 | 基于 Redis 的 Java 分布式对象/服务框架 | 让 Redis 变身「分布式 Java 并发工具箱」 |
| 8.2 常见功能组件实战 | RMap/ RList/ RSet/ RAtomicLong/ RBucket 等 | 把 JUC 集合映射成分布式集合 |
| 8.3 分布式锁实战 | RLock 可重入锁、公平锁、读写锁、红锁、看门狗续期 | 第 7.3 手搓锁的工程化答案 |
| 8.4 总结 | 收束 Redisson 理论章 | 下一章用「高性能点赞」落地 |

## 核心精讲

（以下为教学性梳理，代码均**教学示意，不参与构建**。）

### 8.1 Redisson 是什么

- 它**不是 Redis 客户端的另一种**（那叫 Jedis/Lettuce），而是在 Redis 之上**封装了一层
  分布式 Java 对象与并发原语**：`RLock`、`RSemaphore`、`RCountDownLatch`、`RReadWriteLock`、
  `RAtomicLong`、`RMap` 等，API 长得像 JUC（`java.util.concurrent`），但状态在 Redis 集群里共享。
- 价值：把第 7 章要手写的「`SET NX` + Lua + 看门狗」全部内置，业务只写 `lock()`/`unlock()`。

### 8.2 常用组件（教学示意）

```java
// 教学示意，不参与构建：分布式对象映射
RMap<String, String> map = redissonClient.getMap("shared:config");
map.put("k", "v");                       // 像用 HashMap，但跨进程共享

RAtomicLong counter = redissonClient.getAtomicLong("like:count:1");
counter.incrementAndGet();                // 分布式原子计数器（第 9 章点赞用）

RSemaphore sem = redissonClient.getSemaphore("slot");
sem.trySetPermits(10); sem.acquire();     // 分布式信号量（限流/配额）
```

### 8.3 分布式锁实战（本章重点，教学示意）

```java
// 教学示意，不参与构建：RLock 可重入锁 + 自动看门狗
RLock lock = redissonClient.getLock("book:lock:1");
lock.lock();                 // 拿锁；未指定 lease 时会启动「看门狗」每 10s 续期
try {
    // 临界区：扣库存等
} finally {
    lock.unlock();           // 可重入计数归零 + 取消看门狗
}
```

- **看门狗（Watchdog）**：Redisson 默认锁 30s 过期，但若业务没执行完，后台线程每 10s 把 TTL 续到 30s，
  直到 `unlock`——正好补上第 7.3「业务超时锁失效」的坑。
- **读写锁 / 公平锁 / 红锁（RedLock）**：`getReadWriteLock`（读共享写互斥）、
  `getFairLock`（按申请顺序）、`getRedLock`（多 Redis 实例联合加锁）。
  红锁的争议见第 7 章「近年研究」段。

## 版本演进

- **本书基于 Redisson 3.x**；到 2026 年 Redisson 已支持 Redis 6/7 的 ACL、TLS、Cluster、哨兵、云 Redis。
- **🔧 与 Redis 7 / 云 Redis 适配**：2026 年 Redisson 需配对的 Redis 版本注意 RESP 协议与集群拓扑；
  云 Redis（如阿里云）对某些命令（如 `KEYS`、多 key 事务）有限制，Redisson 的批量操作需注意。
- **🔧 看门狗与「锁自动延期」是 2026 默认预期**：手写锁时代（第 7 章）最易错的就是续期，
  Redisson 把这事标准化了；但也要注意 `lock(leaseTime)` 显式设了租约后**不会**走看门狗。
- **🔧 Reactive / 异步 API**：Redisson 提供 `RLockAsync` 等异步接口，适配 WebFlux/响应式，本书未覆盖。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Redisson 官方文档（redisson.org） | redisson.org | 本章所有 `R*` 组件的权威出处 |
| Redis 官方文档：SET NX / Lua / 发布订阅 | redis.io | Redisson 底层依赖的命令底座 |
| （RedLock 争议）Kleppmann《How to do distributed locking》博客 2016 | martin.kleppmann.com | 对 Redis 分布式锁安全假设的质疑 |

> 第 8 章是工程实战章，原书不引论文；上表补官方文档与 RedLock 争议出处。

## 近年研究与工业界开源实践（2015–2026）

- **实测 star（2026-09，`gh api` 实测）**：

| 项目 | 定位 | star |
| --- | --- | --- |
| `redisson/redisson` | 本章全部组件的本体 | 24403 |
| `redis/redis` | Redisson 的存储底座 | 76498 |
| `lettuce-io/lettuce` | 可与 Redisson 并存的另一 Redis 客户端 | 5779 |

- **Redisson 是 Java 侧「Redis 即并发框架」的事实标准**：大量公司的分布式锁、限流、排行榜直接建在它之上；
  它与 Spring Boot 通过 `redisson-spring-boot-starter` 集成。
- **与 Curator 对照**：Redisson 管「基于 Redis 的分布式对象」，Curator 管「基于 ZK 的协调原语」；
  两者定位相似（把并发原语分布式化），底座不同（Redis vs ZK）。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Redisson 就是另一个 Redis 客户端」 | 它是**基于 Redis 的分布式对象/锁框架**，与 Jedis/Lettuce 定位不同 |
| 2 | 「`lock()` 后永远安全」 | 显式 `lock(leaseTime)` 不设看门狗，到期仍会失效；需 `unlock` 配对 |
| 3 | 「RLock 不用关」 | 必须 `try/finally unlock`，否则看门狗一直续期 → 死锁 |
| 4 | 「红锁一定比单实例锁安全」 | 红锁依赖时钟假设，有争议；多数场景单实例锁 + 兜底足够 |
| 5 | 🔧 本书基于 Redisson 3.x | 2026 需注意与 Redis 7 / 云 Redis 的兼容与命令限制 |
| 6 | 🔧 本书未提异步/响应式 API | 2026 年 Redisson 提供 `RLockAsync` 等，适配响应式栈 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 8.3 RLock → [07-分布式锁实战.md](07-分布式锁实战.md)（7.3 手搓 Redis 锁的封装版）；
  - 8.2 RAtomicLong/RMap → [09-Redisson典型应用场景实战之高性能点赞.md](09-Redisson典型应用场景实战之高性能点赞.md)（计数器/排行榜）；
  - 8.1 基座 → [03-缓存中间件Redis.md](03-缓存中间件Redis.md)（Redis 连接）。
- [../Redis深度历险.md](../Redis深度历险.md)——分布式锁系统讲法，含 RedLock 讨论，与 8.3 对读。
- [../ZooKeeper-分布式过程协同技术详解.md](../ZooKeeper-分布式过程协同技术详解.md)
  ——对照「基于 ZK 的协调原语（Curator）」与 Redisson 的设计哲学差异。
- [../深入理解高并发编程/](../深入理解高并发编程/)——JUC 并发原语（Redisson 的 API 灵感来源）。
