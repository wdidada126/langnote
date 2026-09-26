# 第 4 章　Ehcache 与 Guava Cache

> 进入框架篇之前的「本地缓存」一章。Ehcache 偏企业级（支持集群、磁盘层），Guava Cache 偏
> 轻量进程内缓存。两者都是「不依赖外部服务」的本地缓存，和后面的分布式缓存形成对照。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 4.1 Ehcache 特性与集群 | 缓存管理器、TTL/TTI、堆内/堆外/磁盘三级存储、Terracotta 集群 | 适合需要持久层与集群的企业 Java 应用 |
| 4.2 Ehcache 存储层 | 堆内（on-heap）/ 堆外（off-heap）/ 磁盘（disk）分层 | 分层让容量远超 JVM 堆，且减少 GC 压力 |
| 4.3 Guava Cache 本地内存缓存 | LoadingCache、自动加载、过期、弱引用、统计 | 轻量、无依赖，适合单体或进程内热点缓存 |

## 核心精讲

（以下为教学性梳理，伪代码/SQL 均**教学示意，不参与构建**。）

### 4.3 Guava Cache 最小示意

```java
// 教学示意，不参与构建
LoadingCache<String, User> cache = CacheBuilder.newBuilder()
    .maximumSize(10_000)                 // 容量上限（近似 LRU 淘汰）
    .expireAfterWrite(10, TimeUnit.MINUTES)   // 写后 10 分钟过期
    .recordStats()                       // 记录命中率
    .build(new CacheLoader<String, User>() {
        public User load(String key) { return userDao.load(key); }  // 自动回填（Cache-Aside 的自动版）
    });
User u = cache.get("uid-123");           // 未命中自动调用 load
```

- 对比 [01-缓存为王.md](01-缓存为王.md) 1.6：Guava 的 `CacheLoader` 让「Cache-Aside 的回填」自动化，
  接近于 Read-Through；`expireAfterWrite` 对应 3.3 的 TTL。

### 4.1 Ehcache 分层存储示意

```text
# 教学示意，不参与构建：Ehcache 三级层级
L1 堆内   (fast, limited, GC pressure)
L2 堆外   (off-heap, bigger, no GC of cached objects)
L3 磁盘   (largest, persistent-ish, slow)
读取：先 L1 -> 未命中 L2 -> 未命中 L3 -> 回源 DB
写入：按策略写穿到各层
```

## 版本演进

- **本书无第二版**；本节写 2017 年口径 → 2026 年视角的变化。
- **Caffeine 取代 Guava Cache**：2026 年 Java 本地缓存事实标准是 **Caffeine**（ben-manes/caffeine，**17878★**），
  API 与 Guava 相似但命中率（W-TinyLFU）与并发远胜；新项目几乎不再用 Guava Cache（见 [01-缓存为王.md](01-缓存为王.md) 补丁）。
- **Ehcache 现状**：Ehcache 3.x 仍在维护（ehcache/ehcache3，**2088★**），但定位和 Caffeine + 外部存储不同，
  企业里更多用 Caffeine（本地）+ Redis/Tair（分布式）组合替代「Ehcache 集群」。
- **堆外/磁盘分层被 redis 化**：进程内三级存储的需求，很多被「本地 Caffeine + 远端 Redis」多级方案替代，
  因为远端缓存可跨进程共享、易扩容。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Gil Einat, Friedman《TinyLFU: A Highly Efficient Cache Admission Policy》 | POMACS / SOSP 2015 (poster) | **W-TinyLFU**，Caffeine 的理论底座（见第 1 章 1.5） |
| 各缓存官方文档 | Ehcache 官方文档、Guava Cache 官方 Wiki | 本章配置与 API 的一手出处（工程文档而非论文） |

> 说明：Ehcache/Guava 是工程库，理论贡献在「淘汰算法」而非库本身；算法文献见第 1 章。

## 近年研究与工业界开源实践（2015–2026）

- **实测 star（2026-09，`gh api` 实测）**：

| 项目 | 定位 | star |
| --- | --- | --- |
| `ben-manes/caffeine` | Java 本地缓存，W-TinyLFU（Guava Cache 的现代替代） | 17878 |
| `google/guava` | 含 Guava Cache（本章 4.3 主角） | 51912 |
| `ehcache/ehcache3` | Ehcache 3.x（本章 4.1/4.2 主角） | 2088 |

- **Caffeine 的 W-TinyLFU** 让本地缓存命中率显著提升，是 2015 年后本地缓存领域最重要的实践进展；
  Spring Boot 的 `@Cacheable` 默认桥接 Caffeine/Redis。
- **多级缓存组合**：`Caffeine（本地） + Redis（分布式）` 成为 Java 后端标配，
  比单用 Ehcache 集群更灵活、扩容更容易。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「本地缓存不会拖慢 JVM」 | 堆内缓存过大加重 GC；应上堆外/分层或改用 Caffeine + Redis |
| 2 | 「Ehcache 集群 = 分布式缓存」 | Ehcache 集群偏进程间同步，规模和弹性不如 Redis/Tair 集群 |
| 3 | 🔧 本书主推 Guava Cache | 2026 年本地缓存事实标准是 **Caffeine（W-TinyLFU）**，命中率与并发更优，应补 |
| 4 | 🔧 本书未提「本地+分布式」多级 | 2026 年主流是 Caffeine + Redis 两级；单级 Ehcache 集群已非首选 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 4.3 Guava → [01-缓存为王.md](01-缓存为王.md) 1.5（LRU）/ 1.6（Cache-Aside 自动回填）；
  - 4.2 分层 → [03-动手写缓存.md](03-动手写缓存.md) 3.3（过期清理的工程化）；
  - 4.x 本地缓存 → 后面 [05-](05-从Memcached开始了解集中式缓存.md) 起的分布式缓存（对照「共享 vs 不共享」）。
- [../大规模分布式存储系统/02-单机存储系统.md](../大规模分布式存储系统/02-单机存储系统.md)
  ——堆内/堆外/磁盘分层与「存储层次架构（2.1.5）」同构。
- [../设计数据密集型应用/](../设计数据密集型应用/) DDIA 对「应用层缓存」的讲法，与本章直接对读。
