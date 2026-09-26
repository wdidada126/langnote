# 第 13 章 InfluxDB 企业版一致性实现剖析

> 覆盖原书：第 13 章「InfluxDB企业版一致性实现剖析」。
> 13.1 什么是时序数据库、13.2 如何实现 META 节点一致性、13.3 如何实现 DATA 节点一致性
> （13.3.1 自定义副本数 / 13.3.2 Hinted-handoff / 13.3.3 反熵 / 13.3.4 Quorum NWR）、13.4 小结。
> 本章是全书**最有价值的一章**：它展示了「同一个系统里同时使用 CP 与 AP 两套路径」的真实设计。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 13.1 什么是时序数据库 | 写多读少、按时间范围查询、数据可过期 | 负载特征决定了「元信息」与「时序数据」可以采用**不同的一致性策略** |
| 13.2 META 节点一致性 | 元信息（库/表/保留策略/分片归属）用**强一致** | 元信息量小、变更少、错了就全错 → 走共识（CP） |
| 13.3.1 自定义副本数 | 每个 retention policy 可配副本数 | 用**副本数**而非全局配置来调一致性与成本 |
| 13.3.2 Hinted-handoff | 目标节点短暂不可用时，先写在别处并记 hint | 只补偿**短暂**故障，超过窗口必须靠反熵 |
| 13.3.3 反熵 | 周期性比对并补齐 | 兜底修复，保证**最终**一致 |
| 13.3.4 Quorum NWR | 用 N/W/R 配置读写 | 把一致性变成**可配置档位**（AP 侧） |
| 13.4 小结 | 混合架构 | **META 用 CP、DATA 用 AP** —— 这是本章最值得带走的模式 |

## 核心精讲

### 13.1 时序数据的负载特征

| 特征 | 含义 | 对一致性的影响 |
| --- | --- | --- |
| 写多读少、追加写 | 极少更新已有时间点 | 冲突少 → 最终一致的代价低 |
| 按时间范围扫描 | 查询常跨大量点 | 单点陈旧影响小 |
| 数据有 TTL | 保留策略（retention policy）自动过期 | 丢少量近期点的代价可接受 |
| 指标可容忍微小误差 | 监控/趋势场景 | 不需要分布式事务 |

**结论**：时序数据天然适合 AP 侧；但**元信息**（哪个分片在哪台机器、有哪些库表）不能含糊，必须 CP。

### 13.2 META 节点：为什么必须强一致

```
教学示意，不参与构建
// META 节点保存的是「集群的目录」：
//   database / retention policy / shard group / shard -> 哪些 DATA 节点
//   连续查询（continuous query）的进度、用户与权限
// 这些信息的特点：
//   1. 体量小（可以全放内存）
//   2. 变更频率低（建库、建表、分片分裂）
//   3. 一旦不一致，后果严重（写错节点、数据丢失、双写）
// -> 用共识（Raft / 类 Paxos）保证强一致，代价完全可接受
```

META 与 DATA 的分工：

| 维度 | META 节点 | DATA 节点 |
| --- | --- | --- |
| 数据 | 元信息（小、少变） | 时序数据（大、高频写） |
| 一致性 | **CP**（共识强一致） | **AP**（最终一致 + 可调） |
| 写入量 | 低 | 极高 |
| 故障影响 | 全局不可用 | 只影响部分分片 |

### 13.3 DATA 节点的四件套

```
教学示意，不参与构建
// 1) 自定义副本数（13.3.1）
//    每个 retention policy 指定 replication factor
//    副本分布在 DATA 节点上（按分片分布策略）
CREATE RETENTION POLICY "rp_7d" ON "metrics"
    DURATION 7d REPLICATION 3 SHARD DURATION 1d
//    副本数 N 直接决定后续 N/W/R 的可选范围

// 2) Hinted-handoff（13.3.2）
on writeTo(node, points):
    if node is unavailable and failure is transient:
        writeToLocalHintedQueue(node, points)   // 先存本地，带目标地址
    // 节点恢复后回放；队列有容量/时间窗口，超限则丢弃并等待反熵
//    定位：补偿「秒级~分钟级」的短暂故障，不是持久方案

// 3) 反熵（13.3.3）
every T:
    for each shard:
        compareWithPeers(shard)      // 常用 Merkle 树/摘要比对
        repairMissingRanges()        // 补齐缺失的时间段
//    定位：兜底。没有它，hint 超窗口后就是永久丢失

// 4) Quorum NWR（13.3.4）
//    写：至少 W 个副本确认才算成功；读：至少读 R 个副本取最新并读修复
//    W + R > N  -> 保证能读到最新写（见第 8 章）
```

**四件套的关系**：

```
教学示意，不参与构建
// 时间轴视角
//   写入瞬间：Quorum NWR 决定「这次写算不算成功」
//   秒~分钟  ：目标节点短暂故障 -> Hinted-handoff 补偿
//   分钟以上 ：hint 队列超限 / 长时故障 -> 反熵兜底修复
//   读时    ：读顺手修复（read repair，本书第 8 章）
// 副本数 N 是这一切的「预算」：N 越大，能容忍的故障越多，成本越高
```

### 13.4 带走这个模式

> **META 用 CP、DATA 用 AP** 是一种可复用的架构模式，不只在时序库里有：

| 系统 | CP 部分 | AP 部分 |
| --- | --- | --- |
| InfluxDB Enterprise | META 节点（共识） | DATA 节点（NWR + 反熵） |
| Consul | 服务目录（Raft） | 成员/故障检测（Serf Gossip） |
| Kubernetes | etcd（所有对象） | 各节点的 kubelet 本地状态（最终收敛） |
| TiDB | PD + Region 元信息（Raft） | 数据 Region（Multi-Raft，每组分片各自一致） |
| 大数据平台 | NameNode / Catalog | 数据块副本（后台修复） |

## 版本演进

- **2013–2015**：InfluxDB 0.x/1.x 出现；**集群与企业版（META/DATA 分离）**是闭源商业特性，
  社区版长期没有集群能力。作者韩健发起 **FreeTSDB**，被介绍为「补齐 InfluxDB 分布式能力的开源时序数据库」——
  这是本章写作视角的直接来源。
- **2019–2021**：InfluxDB 2.x 转向 **Flux + TICK 统一**，OSS 版**仍不带集群**；
  企业版维持 META/DATA 架构。
- **2022（本书）**：第 13 章是全书实战篇的第一案，核心价值在「CP + AP 混用」这一架构判断。
- **2026 视角（重要）**：
  - **InfluxDB 3.x**（2023 起）用 **Rust 重写**，架构与 1.x/2.x 企业版**不再相同**：
    引入 **InfluxDB 3 Core（开源）/ Enterprise**，存储层改用 **Apache Arrow / Parquet + 对象存储**，
    计算与存储进一步分离；
  - 因此本书 13.2/13.3 描述的 **META 节点 + DATA 节点 + hinted handoff + 反熵** 这一套，
    主要对应 **1.x/2.x 企业版**。读本章时应把它当作**一个经典架构样本**，
    而不是 InfluxDB 3.x 的现状描述；
  - 与此同时，**「元信息强一致 + 数据最终一致」这个模式本身没有过时**，
    它在 TiDB、Consul、K8s、各类存算分离系统中反复出现。

## 经典论文与原始文献

| 论文/文献 | 出处 | 贡献 |
| --- | --- | --- |
| DeCandia et al.《Dynamo: Amazon's Highly Available Key-value Store》 | ACM SOSP 2007 | 本章 13.3 四件套（副本数/hinted handoff/反熵/NWR）的**共同源头** |
| Lakshman & Malik《Cassandra: A Decentralized Structured Storage System》 | ACM SIGOPS OSR 2010 | hinted handoff + Merkle 反熵 + NWR 的开源实现参考 |
| Demers et al.《Epidemic Algorithms for Replicated Database Maintenance》 | ACM PODC 1987 | 反熵（本书第 7 章） |
| Gifford《Weighted Voting for Replicated Data》 | ACM SOSP 1979 | Quorum NWR（本书第 8 章） |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | META 节点强一致的算法基础 |
| Jensen, Pedersen, Thomsen《Time Series Management Systems: A Survey》 | IEEE TKDE 2017 | 时序数据库系统的综述（本章 13.1 的学术背景） |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **存算分离 + 对象存储**成为时序/分析型系统的主流形态（InfluxDB 3.x、各类 lakehouse），
    一致性问题从「副本同步」变为「**元数据 + 对象存储清单（manifest）**」的提交原子性；
  - **Arrow / Parquet + 列式**使时序数据的修复粒度从「分片」变为「文件」，反熵的代价显著下降；
  - **时序基准**（如 TSBS）成为评估写入吞吐与查询时延的标准工具。
- **工业界开源**（star 数 2026-09 `gh api` 实测）：
  - `influxdata/influxdb`（**31759★**）：本书第 13 章主角。注意 **3.x 已用 Rust 重写**，与本章描述的 1.x/2.x 企业版架构不同。
  - `etcd-io/etcd`（**52310★**）：本章 13.2「META 节点强一致」在 2026 年的典型实现选择。
  - `tikv/tikv`（**16878★**）+ `pingcap/tidb`（**40590★**）：**「元信息强一致 + 数据分片各自一致」**在分布式数据库里的对应形态（PD + Multi-Raft）。
  - `hashicorp/consul`（**30085★**）：同为「CP 目录 + AP 成员层」混合架构，与本章 13.4 的模式高度同构。
  - `apache/rocketmq`（**22621★**）：其 NameServer 是「元信息**也不强一致**」的反例，可用来对照本章 13.2 的必要性论证。
- **Jepsen 实测**（`jepsen-io/jepsen`，**7504★**）：Jepsen 未对 InfluxDB 企业版（闭源）做专项公开测试；
  读者若需评估类似架构，可参考其对 Cassandra（同为 hinted handoff + 反熵 + NWR）的报告。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「一个系统只能选 CP 或 AP」 | 错。本章的价值正在于**按数据性质分而治之**：元信息 CP、数据 AP |
| 2 | 「hinted handoff 能兜住所有故障」 | 它只补偿**短暂**故障，队列有容量与时间窗口；长时故障必须靠反熵 |
| 3 | 「有了反熵就不需要副本数规划」 | 反熵只修「已存在的副本」；若 N 个副本同时失效，数据就没了 |
| 4 | 「META 节点用最终一致也行」 | 不行。分片归属一旦不一致就会**双写/写到错节点**，恢复成本极高 |
| 5 | 🔧 2026 补丁：InfluxDB 3.x 已重写架构 | 本书描述的是 **1.x/2.x 企业版**的 META/DATA + hinted handoff + 反熵。2023 起 **InfluxDB 3.x 用 Rust 重写**，转向 Arrow/Parquet + 对象存储 + 存算分离。读本章应把它当**架构样本**，而非产品现状 |
| 6 | 🔧 2026 补丁：META 层的实现已换成 etcd/Raft 生态 | 本书 13.2 讲「META 节点一致性」偏原理。2026 年新建系统几乎直接采用 **etcd**（或 Raft 库）承载元信息，而不是自研一套元信息共识。见 [12-Hashicorp-Raft与分布式KV系统实战](12-Hashicorp-Raft与分布式KV系统实战.md) |
| 7 | 🔧 2026 补丁：对象存储改变了修复粒度 | 存算分离后，数据以**不可变文件（Parquet）**落在对象存储上，"反熵"变成**清单（manifest）比对 + 文件级补齐**，远比副本级比对便宜。本书 13.3.3 的副本级反熵模型在 2026 年已被部分取代 |
| 8 | 🔧 2026 补丁：TTL/保留策略与云原生的关系未展开 | 本章 13.1 讲 TTL，但未联系云原生：2026 年 TTL 与**对象存储生命周期策略**、**K8s 的 lease/TTL 机制**、**etcd lease** 是同一思想在不同层的落地，读者可自行打通 |

## 与其他章 / 其他书的联系

- **本目录内**：
  - 13.2 的 CP 部分对应 [03-Raft选举日志复制与成员变更](03-Raft选举日志复制与成员变更.md)；
  - 13.3.3 反熵对应 [06-Gossip协议与反熵](06-Gossip协议与反熵.md)；
  - 13.3.4 NWR 对应 [07-Quorum-NWR](07-Quorum-NWR.md)；
  - 分片归属的寻址对应 [04-一致哈希算法](04-一致哈希算法.md)；
  - 13.4 的模式在 [12-Hashicorp-Raft与分布式KV系统实战](12-Hashicorp-Raft与分布式KV系统实战.md) 里被亲手实现一遍。
- **跨书**：
  - [../深入理解分布式系统/10-案例研究文件系统与协调服务.md](../深入理解分布式系统/10-案例研究文件系统与协调服务.md)——协调服务与元信息管理的案例视角；
  - [../深入理解分布式系统/11-案例研究分布式存储与数据库.md](../深入理解分布式系统/11-案例研究分布式存储与数据库.md)——存储系统的案例对照；
  - [../深入理解分布式系统/03-数据分区与复制.md](../深入理解分布式系统/03-数据分区与复制.md)——分区与复制的系统书口径，是本章 13.3 的理论背景；
  - [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)——把「CP/AP 分而治之」翻译成架构决策；
  - [../分布式数据库入门进阶与实战/](../分布式数据库入门进阶与实战/00-总览与阅读地图.md) 第 22 章「特殊用途的分布式数据库」——含**时序数据库**一节，与本章 13.1 直接对口。
