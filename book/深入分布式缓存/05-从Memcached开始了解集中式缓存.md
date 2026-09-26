# 第 5 章　从 Memcached 开始了解集中式缓存

> 框架篇第一章，也是最「集中式」的一个：Memcached 本身无集群、无持久化、无副本，所有分布式
> 能力都放在**客户端**。理解 Memcached 能帮我们看清「集中式缓存」的边界，也为后面 Redis/Tair 的
> 分布式方案提供对照。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 5.1 架构与多线程模型 | 多 worker 线程 + 主线程 accept；每个连接由一个线程处理 | Memcached 用**多线程**吃满多核，与 Redis 单线程形成对照 |
| 5.2 libevent 事件驱动 | 基于 libevent 的 Reactor 事件循环 | 高并发网络层的经典实现 |
| 5.3 slab 内存分配器 | 按 chunk size 分 slab class，预分配页，避免碎片 | slab 是 Memcached 内存高效的关键 |
| 5.4 客户端一致性哈希 | 分布式完全靠客户端：key 哈希到某台机器 | 扩容需客户端重算，迁移靠业务侧 |
| 5.5 Twemcache / Twemproxy | Twitter 的 Memcached 分支（Twemcache）与代理（Twemproxy） | 代理把分片/路由从客户端上收，屏蔽后端拓扑 |

## 核心精讲

（以下为教学性梳理，伪代码/SQL 均**教学示意，不参与构建**。）

### 5.3 slab 分配器（为什么 Memcached 不怕内存碎片）

```text
# 教学示意，不参与构建：slab class 分级
slab class 1: chunk = 96B    预分配若干页，每页切成 N 个 96B chunk
slab class 2: chunk = 120B   （按 1.25 因子递增）
...
set(key, value):
    size = len(value)
    cls  = 找到 >= size 的最小 slab class
    if 该 class 有空闲 chunk: 放入
    else: 申请新页并切片 -> 放入
淘汰: 该 slab class 满且无空闲 -> LRU 淘汰该 class 内最久未用 item
```

- 关键限制：**value 大小有上限**（默认 1MB），且同一 slab class 的 chunk 固定大小会导致「内部碎片」（96B 的 value 占 120B chunk）。

### 5.4 客户端一致性哈希（分布式能力的承担者）

```text
# 教学示意，不参与构建：客户端路由
servers = [s1, s2, s3]
ring    = consistent_hash(servers)           # 见 02 章 2.3
get(k):  s = ring.node_for(k); s.get(k)
set(k,v): s = ring.node_for(k); s.set(k,v)
# 扩容加机器: 客户端 ring 重算 -> 约 1/新机器数的 key 需迁移（由业务/代理处理）
```

- Memcached 服务端**不知道**集群拓扑；扩缩容、故障转移的「责任」全在客户端或代理（Twemproxy）。

## 版本演进

- **本书无第二版**；本节写 2017 年口径 → 2026 年视角的变化。
- **Memcached 仍是稳定基础设施**：`memcached/memcached` 持续维护（**14285★**），但对新业务而言份额被 Redis 蚕食；
  它仍在需要纯 KV、多线程、大并发读的场景（如缓存 HTML 片段、Session）里吃得开。
- **Twemproxy 仍是事实标准代理**：`twitter/twemproxy`（**12339★**）被广泛用于 Memcached/Redis 的前端分片；
  但 2026 年新项目更多直接用 Redis Cluster（服务端分片），减少对代理的依赖。
- **代理形态进化**：除 Twemproxy 外，bilibili 开源的 `bilibili/overlord`（**2247★**，Go 写的 memcache/redis 代理与集群管理）
  代表了「自动化高可用缓存服务」方向，本书成书后才有。
- **多线程对照**：Memcached 的多线程天然吃多核；Redis 直到 🔧 6.0 才引入多线程 **网络 I/O**（命令执行仍单线程），见 [07-Redis探秘.md](07-Redis探秘.md)。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Fitzpatrick《distributed caching with memcached》 | 工程实践（2004，LiveJournal） | **Memcached 的原始设计**与「客户端分片」思想 |
| Karger et al.《Consistent Hashing and Random Trees》 | STOC 1997 | 客户端一致性哈希的理论底座（见第 2 章 2.3） |
| libevent / GNU 相关事件库文档 | — | 5.2 的 Reactor 实现基础 |
| Provos et al.《libevent: an event notification library》 | USENIX 2000（相关） | 事件驱动网络库的设计 |

> 说明：Memcached 偏工程系统，权威出处是作者博客/官方 wiki 与一致性哈希论文，无单篇「Memcached 论文」。

## 近年研究与工业界开源实践（2015–2026）

- **实测 star（2026-09，`gh api` 实测）**：

| 项目 | 定位 | star |
| --- | --- | --- |
| `memcached/memcached` | 集中式多线程 KV 缓存（本章主角） | 14285 |
| `twitter/twemproxy` | Memcached/Redis 代理，客户端分片上收 | 12339 |
| `bilibili/overlord` | Go 写的 memcache/redis 代理 + 集群管理（自动化高可用） | 2247 |
| `redis/redis` | 分布式缓存事实标准（对比对象） | 76487 |

- **「集中式 vs 分布式」的边界在模糊**：Twemproxy/Overlord 把 Memcached 的「客户端分片」上收为代理分片；
  Redis Cluster 把分片放进服务端，Memcached 自身仍坚持无状态服务端。
- **内存效率研究**：slab 的「固定 chunk」带来的内部碎片，催生了可调整 factor、或改用 jemalloc 的优化，
  但 Memcached 的核心分配哲学未变。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Memcached 是分布式缓存」 | 它本身**无集群/无副本**，分布式全靠客户端或代理；真正的分布能力在 Redis Cluster/Tair |
| 2 | 「Memcached 和 Redis 差不多」 | Memcached 只 KV、多线程、无持久化；Redis 多数据结构、单线程、有持久化（见第 7 章） |
| 3 | 「slab 不会内存浪费」 | 固定 chunk 有**内部碎片**；value 远小于 chunk 时浪费明显 |
| 4 | 「加机器零成本」 | 客户端一致性哈希下，扩容要重算 ring 并迁移约 1/N 的 key，需业务配合 |
| 5 | 🔧 本书未提 Twemproxy 以外的现代代理 | 🔧 `bilibili/overlord`（2247★，2018 后）代表自动化高可用缓存方向，应补 |
| 6 | 🔧 本书未对比 Redis 多线程化 | 🔧 Redis 6.0 已引入多线程 IO，与 Memcached 多线程的对照需更新（见第 7 章） |

## 与其他章 / 其他书的联系

- **本书内**：
  - 5.4 客户端一致性哈希 → [02-分布式系统理论.md](02-分布式系统理论.md) 2.3（一致性哈希理论）；
  - 5.5 Twemproxy → [08-分布式Redis.md](08-分布式Redis.md) 8.3（Redis Cluster 服务端分片对照）；
  - 5.3 slab → [07-Redis探秘.md](07-Redis探秘.md) 7.4（Redis 内存管理对照）。
- [../大规模分布式存储系统/05-分布式键值系统.md](../大规模分布式存储系统/05-分布式键值系统.md)
  ——Tair 的「桶」与 Memcached 客户端哈希是同一分布式思想的两种承担方（服务端 vs 客户端）。
- [../深入分布式缓存.md](../深入分布式缓存.md)——大纲版提到「推特开源 Twemcache 代理 Memcached/redis」「缓存热点问题」。
