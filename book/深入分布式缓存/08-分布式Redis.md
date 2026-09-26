# 第 8 章　分布式 Redis

> 第 7 章讲单机内核，本章讲 Redis 的**分布式形态**：主从复制、Sentinel 故障转移、Redis Cluster
> （16384 槽），以及 Java 客户端。这是把 Redis 从「单机缓存」变成「分布式缓存」的关键。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 8.1 主从复制 | 全量 RDB 同步 + 增量命令传播；从节点只读 | 复制提供读扩展与冷备，但写仍在主 |
| 8.2 哨兵 Sentinel | 监控、通知、自动故障转移、配置提供 | Sentinel 解决「主挂了谁来顶」的 2.8 问题 |
| 8.3 Redis Cluster | 16384 槽（hash slot），服务端分片，Gossip 维护拓扑 | 槽 = 「一致性哈希」的离散化落地，天然支持扩缩容 |
| 8.4 客户端（Jedis 等） | 客户端感知槽分布、重定向（MOVED/ASK） | 客户端需理解集群拓扑才能高效路由 |

## 核心精讲

（以下为教学性梳理，伪代码/SQL 均**教学示意，不参与构建**。）

### 8.1 主从复制流程

```text
# 教学示意，不参与构建
slave 启动 -> 发 SYNC 给 master
master: fork 子进程 dump RDB -> 传给 slave -> slave 载入
        之后 master 把每个写命令异步传播给 slave (增量)
读: 可打到 slave（读扩展）；写: 只走 master
```

- 注意：复制默认**异步**，主宕且未同步的写会丢；需要更强保证要用 WAIT 或换共识方案。

### 8.3 Redis Cluster 的槽（slot）

```text
# 教学示意，不参与构建：16384 槽 = 离散版一致性哈希
slot = CRC16(key) % 16384
每个 master 负责一段连续的槽；槽可在 master 间迁移
key 不在本节点 -> 返回 MOVED <slot> <host:port> -> 客户端重定向
扩容: 把部分槽从旧 master 迁到新 master（迁移期间用 ASK 重定向，保证不丢）
```

- 这与 [02-分布式系统理论.md](02-分布式系统理论.md) 2.3 一致性哈希、[09-Tair探秘.md](09-Tair探秘.md) 9.3「桶」、[05-](05-从Memcached开始了解集中式缓存.md) 客户端哈希是**同一思想三种实现**：
  都是「把 key 空间切成可迁移的最小单位」。

## 版本演进

- **本书无第二版**；本节写 2017 年口径（Redis 3.x Cluster 已出）→ 2026 年视角的变化。
- **🔧 客户端缓存贯通 Cluster**：Redis 6.0 的 client-side caching（tracking）在集群下也适用，
  客户端缓存槽对应 key 的失效，进一步降低读放大。
- **🔧 多线程 IO（6.0）让大集群吞吐更高**：单实例不再是 CPU 瓶颈，集群规模的经济性更好。
- **🔧 Valkey 成为 Cluster 替代实现**：Valkey（valkey-io/valkey，**27297★**）兼容 Redis Cluster 协议，
  2026 年许多云托管 Redis 集群实为 Valkey；本书只讲 Redis Cluster 一家，需补。
- **🔧 官方 Redis 7/8 的 Cluster 增强**：更顺滑的槽迁移、更稳的 Gossip、Sharded Pub/Sub，
  运维复杂度下降。
- **🔧 代理层仍活跃**：Codis（CodisLabs/codis，**13222★**）作为「预 Cluster 时代」方案仍在部分老系统，
  新系统多用原生 Cluster 或 Valkey。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Redis 官方 Replication / Cluster 规范（antirez 文档） | redis.io | 8.1/8.3 一手出处 |
| Karger et al.《Consistent Hashing and Random Trees》 | STOC 1997 | 槽/桶/哈希的同一理论底座 |
| Ongaro, Ousterhout《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | Sentinel 选主背后的共识思想（补 8.2） |
| Hunt et al.《ZooKeeper》 | USENIX ATC 2010 | 协调/选主服务的工业标准（与 Sentinel 同类思路） |

## 近年研究与工业界开源实践（2015–2026）

- **实测 star（2026-09，`gh api` 实测）**：

| 项目 | 定位 | star |
| --- | --- | --- |
| `redis/redis` | Redis 本体 + Cluster（本章主角） | 76487 |
| `valkey-io/valkey` | Redis Cluster 协议兼容的 2024 分叉 | 27297 |
| `CodisLabs/codis` | Redis 集群代理方案（预 Cluster 时代，已少维护） | 13222 |
| `redisson/redisson` | Java Redis 客户端 + 分布式锁/对象 | 24403 |
| `redis/lettuce` | 异步响应式 Java 客户端 | 5779 |

- **Cluster 的「槽」已成为分布式缓存的事实分片范式**：Tair 桶、Dynamo 虚拟节点、Cassandra vnode 同构，
  只是单位叫法不同。
- **客户端智能化**：Lettuce/Redisson 自动维护槽映射、处理 MOVED/ASK、支持 Cluster 拓扑刷新，
  让 8.4 的「客户端感知拓扑」在 2026 年开箱即用。
- **Redis 托管服务**：AWS ElastiCache、阿里云 Tair（托管 Redis 兼容）、腾讯云 Redis——
  把 8.2/8.3 的运维下沉给云，本书讲自建视角需补托管选项。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「主从复制保证不丢数据」 | 默认异步复制，主宕可能丢未同步写；强一致需 WAIT 或共识方案 |
| 2 | 「Cluster 下所有 key 自动均衡」 | 需合理设计 key；大 key / 热 key 仍会打爆单槽/单节点 |
| 3 | 「槽迁移零影响」 | 迁移期间 ASK 重定向、带宽占用，需低峰操作 |
| 4 | 「Sentinel 万能」 | Sentinel 只管故障转移，不解决数据分片；分片要靠 Cluster |
| 5 | 🔧 本书未提 Valkey 作为 Cluster 替代 | 2026 年云托管集群多为 Valkey，应补 |
| 6 | 🔧 本书客户端只提 Jedis | 🔧 Lettuce/Redisson 处理 Cluster 拓扑更现代，应补 |
| 7 | 🔧 本书未提托管 Redis 服务 | AWS ElastiCache / 阿里云 Tair 等把运维下沉，应补 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 8.3 槽 → [02-分布式系统理论.md](02-分布式系统理论.md) 2.3（一致性哈希）、[09-Tair探秘.md](09-Tair探秘.md) 9.3（桶）；
  - 8.1 复制 → [07-Redis探秘.md](07-Redis探秘.md) 7.3（RDB 用于全量同步）；
  - 8.2 Sentinel → [02-分布式系统理论.md](02-分布式系统理论.md) 2.8（故障转移）。
- [../大规模分布式存储系统/05-分布式键值系统.md](../大规模分布式存储系统/05-分布式键值系统.md)
  ——Tair 的 Config Server + 桶 与 Redis Cluster 槽是「中心化 vs 去中心化」两种分片哲学。
- [../深入理解分布式共识算法/07-Raft.md](../深入理解分布式共识算法/07-Raft.md)
  ——Sentinel 选主 2026 年常由 Raft 类机制承担。
- [../深入分布式缓存.md](../深入分布式缓存.md)——大纲版提到「第8章 分布式Redis 故障转移（failover）」。
