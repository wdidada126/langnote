# 第 8 章 Quorum NWR 算法

> 覆盖原书：第 8 章「Quorum NWR算法」。
> 8.1 Quorum NWR 的三要素、8.2 如何实现 Quorum NWR、8.3 小结。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 8.1 三要素 | N（副本数）/ W（写成功数）/ R（读成功数） | 只要 **W + R > N**，读集合与写集合必相交，就不会读到「全旧」的副本 |
| 8.2 如何实现 | 写时多副本并发、版本/时间戳、读时取最新并**读修复** | NWR 是**可调旋钮**：W=N 时强一致慢，W=1 时快但可能丢 |
| 8.3 小结 | 适用场景 | 用「读写 quorum 的配置」把一致性变成**业务可选**，而不是系统固定 |

## 核心精讲

### 8.1 三要素与 W+R>N

```
教学示意，不参与构建
N = 数据的副本总数（通常在 3 左右）
W = 一次写操作必须成功写入的副本数（才算写成功）
R = 一次读操作必须成功读取的副本数（才用结果应答）

// 相交论证（Dynamo 的核心论证）
// 若 W + R > N，则「任意 W 个副本的集合」与「任意 R 个副本的集合」必相交
// 于是：读到的 R 个副本里，至少有一个持有最新写
// -> 客户端比较版本号/时间戳后能拿到最新值
```

常见配置与其含义：

| N | W | R | W+R>N | 语义 | 代价 |
| --- | --- | --- | --- | --- | --- |
| 3 | 3 | 1 | ✅ | 写强、读快 | 写一个副本慢/挂就写失败（可用性低） |
| 3 | 1 | 3 | ✅ | 写快、读要问全部 | 读慢；且 W=1 时若副本挂了可能丢写 |
| 3 | 2 | 2 | ✅ | **读写均衡**（最常用） | 容忍 1 个副本故障 |
| 3 | 1 | 1 | ❌ | 弱一致（可能读到旧值） | 最快，但读可能拿不到最新值 |
| 3 | 2 | 1 | ❌ | 仍可能读到旧值 | 注意：满足不了 W+R>N 就是弱一致 |

> **W+R>N 是「保证读到最新值」的充分条件，不是「保证线性一致」的充分条件**。
> 这一点是本章最大的隐性陷阱，见「常见误区」。

### 8.2 实现：写并发、版本比较、读修复

```
教学示意，不参与构建
// 写路径
func put(key, value):
    v = (value, version = logicalTimestamp())    // 或版本向量
    results = parallelWriteToPreferenceList(key, v, N)
    if count(success in results) >= W:
        return OK
    else:
        return FAIL            // 客户端可见的写失败，但部分副本已写入！

// 读路径
func get(key):
    replies = parallelReadFromPreferenceList(key, R)
    if count(success) < R: return FAIL
    latest = maxByVersion(replies)
    // 读修复：把最新值回写给那些落后的副本
    asyncWriteBack(latest, replicasWithStaleValues)
    return latest.value

// 冲突：当出现「并发写」且版本不可比（版本向量分叉）时
//   last-write-wins：按时间戳取最大 -> 静默丢数据
//   版本向量 + 返回多版本交给应用层 -> 不丢，但业务要会合并
```

**关键实现细节**：

1. **偏好列表（preference list）**：Dynamo 用一致哈希算出 key 应该落在哪 N 个节点（含环上后继），
   这与本书第 5 章一致哈希直接衔接。
2. **W < N 时的写失败语义**：写返回失败但数据**已经在部分副本上**，后续读仍可能读到它。
   客户端不能把「写失败」理解为「数据没写进去」。
3. **读修复（read repair）**与**反熵（anti-entropy）**互补：前者是**读时顺手修**，后者是**周期性全量修**（本书第 7 章）。

### 8.2 补充：sloppy quorum 与 hinted handoff

```
教学示意，不参与构建
// 严格 quorum（strict quorum）：必须写到 preference list 里那 W 个**指定**节点
//   节点挂了 -> 写失败 -> 可用性下降
// 松散 quorum（sloppy quorum）：写不进去时，先写到环上的**下一个**节点并记 hint
//   目标节点恢复后回放（hinted handoff） -> 可用性提高
// 代价：读的时候也要把 hint 节点算进去，否则可能读不到刚写的值
//   -> 这就是本书第 13 章 InfluxDB DATA 节点 13.3.2 的做法
```

> NWR 的「N」到底是哪些节点，取决于是否启用 sloppy quorum。
> 这是从论文读不出来的细节，但在 Dynamo 系系统里是默认行为。

### 8.2 补充：写冲突的两种结局

| 做法 | 机制 | 后果 |
| --- | --- | --- |
| **LWW（最后写入者赢）** | 按时间戳取最大 | 实现简单，但**并发写会静默丢数据** |
| **版本向量** | 每个副本维护 (node, counter) 向量，分叉时返回**多版本** | 不丢数据，但**业务必须会合并** |
| **CRDT** | 数据类型自带可交换/幂等的合并规则 | 自动收敛，但**数据类型受限**（计数器、集合、映射等） |

本书第 8 章只给了「取版本号最大」这一条路，读者需要知道它等价于 LWW，
在高价值数据上应改用版本向量或 CRDT。

### 8.3 为什么 NWR 是「AP 的高级形态」

与前几章对比：

| 方案 | 一致性强度 | 可用性 | 需要 Leader 吗 |
| --- | --- | --- | --- |
| Raft / ZAB（本书 4、6 章） | 线性一致（配 Read Index） | 多数派挂就不可用 | **需要** |
| **Quorum NWR** | 可调（W+R>N 保「读到最新」） | 只要能凑够 W 或 R 就能服务 | **不需要** |
| Gossip 反熵（本书 7 章） | 最终一致 | 极高 | 不需要 |

NWR 的价值在于：**不用 Leader、不用共识，也能给出可证明的读新鲜度保证**。
代价是把冲突处理推给了业务（版本向量/CRDT/应用层合并）。

## 版本演进

- **1979**：Gifford 在 SOSP 发表《Weighted Voting for Replicated Data》，
  提出**加权投票**：不同副本可以有不同的票重（例如机房 A 的副本权重更高），
  quorum 是「票数过半」而非「节点数过半」。这是 NWR 的真正源头。
- **2007**：Amazon Dynamo（SOSP 2007）把 N/W/R 变成公开的工程模板，并提出**可调一致性（tunable consistency）**一词。
- **2010s**：Cassandra、Riak、Voldemort 沿用；Riak 明确把 N/W/R 暴露为**每个请求可覆盖**的参数。
- **2022（本书）**：第 8 章（3 节）把 NWR 讲成一个「自定义一致性旋钮」，定位准确。
- **2026 视角**：
  - NWR 仍广泛存在（Cassandra、ScyllaDB、InfluxDB Enterprise、Riak 系），
    但**新系统更倾向于「Raft 保证元信息强一致 + 数据分片用主副本复制」**；
  - 「W+R>N 就线性一致」这个**常见误解**已被反复澄清（见 Jepsen 的 `knossos` 与多篇分析）：
    它只保证「读到某个最新写」，不保证**实时顺序**；
  - **读修复的时序漏洞**（写返回成功后立即读，读修复尚未完成，仍可能读到旧值）在实际系统中存在，
    需要配合 `quorum read` + 版本比较 + 同步读修复。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Gifford《Weighted Voting for Replicated Data》 | ACM SOSP 1979 | 加权投票 quorum，NWR 的源头 |
| DeCandia et al.《Dynamo: Amazon's Highly Available Key-value Store》 | ACM SOSP 2007 | 可调一致性 N/W/R、向量时钟、读修复、hinted handoff |
| Lakshman & Malik《Cassandra: A Decentralized Structured Storage System》 | ACM SIGOPS OSR 2010 | NWR 的开源大规模落地 |
| Thomas《A Majority Consensus Approach to Concurrency Control for Multiple Copy Databases》 | ACM TODS 1979 | 多数派方法的早期形式化 |
| Herlihy & Wing《Linearizability: A Correctness Condition for Concurrent Objects》 | ACM TOPLAS 1990 | 线性一致性的正式定义；判断 NWR 是否达标的标尺 |
| Shapiro, Preguiça, Baquero, Zawirski《Conflict-free Replicated Data Types》 | INRIA Tech Report / SSS 2011 | NWR 冲突的自动合并解法（本书未涉及） |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **Flexible Quorum**：Cassandra 2.0+ 支持把 quorum 从「读/写多数派」改为**可调的非对称 quorum**，
    思路与 Howard & Mortier 的 Flexible Paxos（OPODIS 2016）一致——只要读写 quorum 相交即可；
  - **有界陈旧度（bounded staleness）**：Azure Cosmos DB 把「最终一致」细分为
    **强 / 有界陈旧 / 会话 / 一致前缀 / 最终** 五档，是「把一致性变成产品选项」最完整的工业实践；
  - **CRDT 与 NWR 的结合**：Riak 的 CRDT 类型与 Cassandra 的 LWW 形成对照，
    说明「quorum 只解决读新鲜度，冲突语义仍需数据类型层解决」。
- **工业界开源**（star 数 2026-09 `gh api` 实测）：
  - `influxdata/influxdb`（**31759★**）：本书第 13 章主角，DATA 节点用 **自定义副本数 + Quorum NWR**（13.3.1 / 13.3.4）。
  - `apache/cassandra`（star 未核验）：NWR 最知名的开源实现（本次未取到 star）。
  - `etcd-io/etcd`（**52310★**）：**反例**——它不用 NWR，用 Raft 全量一致，说明「可调一致性」不是唯一答案。
  - `tikv/tikv`（**16878★**）：Raft 组 + 每个 Region 一个组，是 NWR 的**替代路线**（共识而非 quorum 读写）。
  - `hashicorp/consul`（**30085★**）：Consul 的 KV 在 Raft 之上提供 `stale`/`consistent` 两种读模式，是「一致性档位」的另一种呈现。
- **Jepsen 实测**（`jepsen-io/jepsen`，**7504★**）：对 Cassandra/Riak 的报告明确指出——
  **W+R>N ≠ 线性一致**；在时钟/会话/读修复时序问题下仍能观察到违反。这是本章最该补的一手证据。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「W+R>N 就是线性一致」 | **不成立**。它保证「读到至少一个最新写」，但**不保证实时顺序**；线性一致需要 Herlihy-Wing 定义的可串行化到实时序 |
| 2 | 「写失败 = 没写进去」 | W<N 时写失败**部分副本已落盘**，后续读可能读到；必须视为「结果未知」 |
| 3 | 「读修复能保证下一次读一定新」 | 异步读修复有窗口；若要求强保证，需**同步**修复或提高 R |
| 4 | 「NWR 不需要冲突处理」 | 需要。LWW 会静默丢数据；正确做法是**版本向量**或 **CRDT** |
| 5 | 🔧 2026 补丁：本书未区分「读到最新」与「线性一致」 | 第 8 章把 W+R>N 讲成强一致的充分条件。2026 年公认结论是：它只是**读新鲜度**保证。要线性一致仍需共识或额外的顺序机制（租约/序号服务） |
| 6 | 🔧 2026 补丁：未提加权 quorum 与 Flexible Quorum | Gifford 1979 原始论文就是**加权**投票；Cassandra 的 Flexible Quorum 与 Flexible Paxos（2016）都说明「读写 quorum 相交即可」。本书只讲了等权版本 |
| 7 | 🔧 2026 补丁：一致性档位化本书未涉及 | 2026 年主流云产品（Cosmos DB 五档、Consul stale/consistent、etcd 的 revision 读）把一致性做成**可选档位**。本书只给 N/W/R 三个数，读者需自行补上「档位化」产品形态 |
| 8 | 🔧 2026 补丁：缺 Jepsen 实测证据 | 本章结论「W+R>N 就安全」应配合 Jepsen 对 Cassandra/Riak 的报告阅读——实测中**时钟与读修复时序**会造成可观察异常 |

## 与其他章 / 其他书的联系

- **本目录内**：
  - 本章的副本列表来自 [04-一致哈希算法](04-一致哈希算法.md)（偏好列表 = 哈希环上的后继节点）；
  - 本章的「读修复」与 [06-Gossip协议与反熵](06-Gossip协议与反熵.md) 的反熵是**两种修复手段**；
  - 本章在 [11-InfluxDB企业版一致性实现剖析](11-InfluxDB企业版一致性实现剖析.md) 13.3.1 / 13.3.4 有真实落地。
- **跨书**：
  - [../深入理解分布式系统/03-数据分区与复制.md](../深入理解分布式系统/03-数据分区与复制.md)——复制策略的系统书口径，含 quorum 的一般化；
  - [../深入理解分布式系统/04-CAP定理与一致性模型与隔离级别.md](../深入理解分布式系统/04-CAP定理与一致性模型与隔离级别.md)——把 NWR 放进一致性模型谱系；
  - [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)——架构师视角的「quorum 还是共识」决策；
  - [../数据库系统概念6/26-高级事务处理.md](../数据库系统概念6/26-高级事务处理.md)——教科书对副本控制（多数派、读一写全）的口径；
  - [../分布式数据库入门进阶与实战/09-共识算法.md](../分布式数据库入门进阶与实战/09-共识算法.md)——同为「多副本怎么达成一致」，但走共识路线，可与本章对照。
