# 第 10 章　EVCache 探秘

> 框架篇的第三个系统，Netflix 基于 **Memcached** 构建的缓存。它最有特点的不是单实例，而是
> **跨区域（cross-region）复制**——这是前几章都没展开的「多机房/多区域」维度。与 [05-](05-从Memcached开始了解集中式缓存.md)
> 的集中式 Memcached 相比，EVCache 把 Memcached 用在了全球规模。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 10.1 Netflix 基于 Memcached 的缓存 | EVCache = Ephemeral + Memcached；为每个区域部署独立 Memcached 集群 | 每个区域本地读，低延迟 |
| 10.2 跨区域复制 | 写本区域后，通过消息/复制通道同步到其他区域 | 跨区读可命中本地副本，避免跨洋往返 |
| 10.3 弹性缓存 | 随流量自动扩缩、与云基础设施集成 | 缓存成为弹性基础设施的一部分 |

## 核心精讲

（以下为教学性梳理，伪代码/SQL 均**教学示意，不参与构建**。）

### 10.2 跨区域复制示意

```text
# 教学示意，不参与构建
Region-A: App -> Memcached-A  (写)
                     |
                     |  复制通道 (异步, 如 Kafka/定制中继)
                     v
Region-B: Memcached-B  (被更新)
Region-B: App 读本地 Memcached-B  -> 命中，无需跨洋访问 Region-A 的 DB

代价: 跨区域是异步复制 -> 短暂不一致；某区域写入后另一区域可能短暂读旧值
```

- 这里 EVCache 复用 Memcached 的「无状态服务端 + 客户端分片」，再加一层「区域间复制」，
  与 [02-分布式系统理论.md](02-分布式系统理论.md) 2.2 的「最终一致（BASE）」一致。

### 10.1/10.3 与 Memcached 的关系

- EVCache 的单区域部分就是第 5 章的 Memcached（多线程、slab、客户端哈希）；
- 区别在**编排层**：Netflix 把多区域、复制、弹性扩缩、与 AWS 集成做进了 EVCache 体系，
  而非单纯跑一个 Memcached。

## 版本演进

- **本书无第二版**；本节写 2017 年口径 → 2026 年视角的变化。
- **🔧 EVCache 开源与现状**：Netflix 开源 `netflix/evcache`（**2223★**，2026-09 实测），但 2026 年其角色已部分
  被**云托管多区域缓存**（AWS ElastiCache Global Datastore、阿里云全球多活 Tair）承接。
- **🔧 跨区复制成为云能力**：本书把跨区复制当作 EVCache 的独门绝技；2026 年 Redis（Active-Active via CRDT /
  Valkey 的类似能力）、DynamoDB 全局表都已内建跨区复制，概念下沉到托管服务。
- **🔧 CRDT 用于跨区一致**：跨区复制的「冲突」可由 CRDT（见 [大规模分布式存储系统/05](../大规模分布式存储系统/05-分布式键值系统.md)）数学消歧，
  比 EVCache 的「后写覆盖」更优雅，是 2026 年 Active-Active 的主流思路。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Netflix Tech Blog: EVCache 系列工程文章 | Netflix 技术博客 | **EVCache 设计与跨区域复制**的一手工程记录 |
| Fitzpatrick《distributed caching with memcached》 | 2004 | EVCache 单区域层的底座（第 5 章同出处） |
| Shapiro et al.《Conflict-Free Replicated Data Types》 | SSS 2011 | 跨区冲突的数学解法（补 10.2 的「后写覆盖」局限） |

## 近年研究与工业界开源实践（2015–2026）

- **实测 star（2026-09，`gh api` 实测）**：

| 项目 | 定位 | star |
| --- | --- | --- |
| `netflix/evcache` | Netflix 基于 Memcached 的跨区缓存（本章主角） | 2223 |
| `memcached/memcached` | EVCache 单区域层底座 | 14285 |
| `redis/redis` | 跨区复制的对照对象（Redis 全球表/Active-Active） | 76487 |
| `valkey-io/valkey` | Redis 分叉，兼容跨区复制能力 | 27297 |

- **跨区复制下沉为云能力**：AWS ElastiCache Global Datastore、阿里云 Tair 全球多活，把 EVCache 的独门能力产品化。
- **Active-Active 缓存**：Redis Enterprise / Valkey 生态的 CRDT 复制，让多区域可同时写，
  优于 EVCache 的「单写区域 + 异步广播」模型。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「EVCache 是一个独立缓存内核」 | 它基于 **Memcached**，跨区复制与编排才是其增量 |
| 2 | 「跨区复制保证强一致」 | 跨区域是异步复制，存在短暂不一致窗口 |
| 3 | 「单区域缓存和 EVCache 一样」 | 单区域 Memcached 无跨区层；EVCache 价值在跨区域复制与弹性编排 |
| 4 | 🔧 本书未提跨区复制已云产品化 | 2026 年 AWS/阿里云的 Global Datastore/全球多活已内建，应补 |
| 5 | 🔧 本书未提 CRDT 解决跨区冲突 | 🔧 Active-Active + CRDT 是 2026 年更优解，应补 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 10.1 单区域层 → [05-从Memcached开始了解集中式缓存.md](05-从Memcached开始了解集中式缓存.md)（Memcached 底座）；
  - 10.2 跨区复制 → [02-分布式系统理论.md](02-分布式系统理论.md) 2.2（BASE 最终一致）。
- [../大规模分布式存储系统/03-分布式系统.md](../大规模分布式存储系统/03-分布式系统.md) 3.8（跨机房部署）
  ——EVCache 的跨区复制是「跨机房部署」在缓存领域的具体实现。
- [../大规模分布式存储系统/05-分布式键值系统.md](../大规模分布式存储系统/05-分布式键值系统.md)
  ——Dynamo 的 hinted handoff / 反熵与跨区复制目标相似（容错同步）。
- [../深入分布式缓存.md](../深入分布式缓存.md)——大纲版提到「EVCache 探秘 netflix 开源」。
