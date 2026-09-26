# 第 8 章 Raft 工程实践与 SOFAJRaft（6.6–6.10）

> 覆盖原书第 6 章后五节（第 2 篇，P192–225）：6.6 网络分区（成员变更中的分区 / 对称网络分区 / 非对称网络分区）；
> 6.7 非事务请求（线性一致性 / Leader Read / Raft Log Read / Read Index / Lease Read）；
> 6.8 Parallel Raft并行协商（乱序协商 / Merge阶段）；
> 6.9 Raft源码实战——SOFAJRaft（简介 / Leader选举 / 日志复制 / 非事务请求 / 成员变更）；
> 6.10 本章小结（Raft与Paxos的异同 / Raft与ZAB的异同）。
> 前半章（6.1–6.5）见 [07-Raft.md](07-Raft.md)。

## 本章地图

如果说 [07-Raft.md](07-Raft.md) 讲的是「**Raft 论文写了什么**」，本章讲的是「**论文没写、但生产必须解决的**」——这也是本章 🔧 补丁最密集的原因：

```
6.6 网络分区   ── 对称 / 非对称；分区会放大成员变更的风险
6.7 非事务请求 ── 五种读方案，逐级用「时钟假设」换「延迟」
6.8 ParallelRaft ── 打破日志严格顺序以换取吞吐（专用场景的激进优化）
6.9 SOFAJRaft  ── 把上面所有议题落成 Java 代码
6.10 横向对比  ── Raft vs Paxos、Raft vs ZAB
```

## 核心精讲

### 6.6 网络分区

**对称分区**：分区两侧**互相**不可达。多数派侧可正常选主与服务；少数派侧收不到心跳而反复超时、自增 term、发起选举但永远拿不到多数票。

| 分区类型 | 特征 | 风险 |
| --- | --- | --- |
| 对称 | A↔B 双向不通 | 少数派侧 term 无意义增长（扰动） |
| 非对称 | A→B 通、B→A 不通（单向可达） | 可能出现「B 能发出投票请求、但收不到回复」或「B 能收到更高 term 的投票请求而 step down」，导致**集群反复换主、term 飙升** |
| 成员变更中的分区 | 变更进行中被分区 | 新旧配置的多数派可能落在两侧 → 若变更未串行化会双 Leader |

**两个工程对策**（论文正文未重点强调、但所有实现都有）：

- **PreVote（预投票）**：节点发起真实选举前，先问一圈「如果我发起选举，你会投我吗」，拿不到多数意向就不自增 term。作用是**防止被隔离的节点用高 term 污染集群**（它恢复后会带着超高 term 出现，迫使现任 Leader 下台）。
- **CheckQuorum（Leader 主动检查）**：Leader 若在选举超时内未收到多数派的心跳响应，主动退位，避免「僵尸 Leader」继续对外服务。

```text
// 教学示意：PreVote + CheckQuorum（不参与构建、不编译、不运行）
on electionTimeoutElapsed():
    // 先预投票：不自增 term
    if count(peers.askPreVote(currentTerm + 1)) > n/2:
        currentTerm++; startRealElection()      // 才有资格真的增 term
    else:
        resetElectionTimer()                    // 被隔离的节点安静下来

on leaderTick():
    if now - lastQuorumHeartbeatAck > electionTimeout:
        stepDown()                              // CheckQuorum：主动让位
```

### 6.7 非事务请求（读路径）

**6.7.1 线性一致性**：读必须能看到「读开始之前已完成的最后一次写」。共识只保证日志一致，**不自动给读请求这个保证**——五种方案逐级取舍：

| 方案 | 机制 | 是否线性一致 | 代价 / 假设 |
| --- | --- | --- | --- |
| **Raft Log Read**（6.7.3） | 读请求也走一遍日志复制，等它提交后按状态机读出 | 是 | 一次完整共识（一次 fsync + 一轮 RPC），最慢 |
| **Leader Read**（6.7.2） | Leader 直接读本地状态机 | **否** | 若该 Leader 已被新 Leader 取代（网络分区），会读到旧值 |
| **Read Index**（6.7.4） | ①Leader 记录当前 `commitIndex`；②向多数派发心跳确认自己仍是 Leader；③等状态机 `lastApplied` 追上该 index；④本地读 | 是 | 一轮 RPC（发心跳即可，不写日志）；**不依赖时钟** |
| **Lease Read**（6.7.5） | Leader 持租约，租期内直接本地读 | 是（**依赖时钟假设**） | 零 RPC，最快；假设「时钟漂移有上界」 |

```text
// 教学示意：ReadIndex（不参与构建、不编译、不运行）
fn linearizableRead(key):
    if state != LEADER: return FORWARD_TO_LEADER
    idx = commitIndex                          // ① 记录读索引
    ok  = heartbeatToQuorum()                  // ② 确认仍是 Leader（多数派响应）
    if not ok: return NOT_LEADER
    waitUntil(lastApplied >= idx)              // ③ 等状态机追上
    return stateMachine.read(key)              // ④ 本地读，不写日志
```

> 🔧 **Lease Read 的真正风险在时钟**：租约的判定是「本地时钟未超过租约到期时间」。若发生 **NTP 跳变、虚拟机迁移/暂停、长时间 GC 停顿**，旧 Leader 可能在租约实际已失效时仍认为自己有效 → 返回旧值 → **破坏线性一致性**。etcd 默认用 ReadIndex，把 Lease Read 作为可选项，正是出于这一顾虑。

### 6.8 Parallel Raft（并行协商）

**动机**：Raft 要求日志严格按序提交，一条日志的 fsync/网络延迟会阻塞后面所有日志 → 吞吐受限。

**思路（公开资料中 PolarDB 一脉的 ParallelRaft）**：

1. **乱序协商**：允许 Leader 并行下发多条日志，Follower 可以不按顺序确认；
2. **Merge 阶段**：提交前把「空洞」补齐/合并，恢复出一个可安全应用的顺序前缀。

```text
// 教学示意：ParallelRaft 的两段式（不参与构建、不编译、不运行）
// 阶段一 乱序协商：Leader 并行发 log[5..9]，Follower 可回 ACK(5),ACK(7),ACK(9)
// 阶段二 Merge：Leader 用一个后台线程/阶段把空洞（6、8）补写、
//               并把「可安全应用的前缀」向前推进
fn onAck(i):
    acked[i] = true
    // 不要求 nextIndex 严格连续；空洞交给 merge 处理
fn mergeLoop():
    while true:
        fillHolesFromLeaderLog()              // 补空洞
        advanceAppliedPrefix()                // 推进可应用前缀
```

> 🔧 **ParallelRaft 不是「更快的通用 Raft」**：它放松了 Raft 的日志连续性这一核心约束，安全性论证必须重做（空洞如何表示、恢复期如何处理、与状态机应用的接口如何定义）。它面向的是**共享存储/专用存储引擎**这类场景（底层已有更强的数据可靠性保证）。**不建议把普通 Raft 系统直接改成 ParallelRaft**。

### 6.9 SOFAJRaft 源码实战

`sofastack/sofa-jraft`（**3,824★**，蚂蚁开源，Java）：

| 小节 | 源码关注点 |
| --- | --- |
| 6.9.2 Leader 选举 | 选举定时器、PreVote、`RequestVote` 的投票判定与 ballot 箱（BallotBox） |
| 6.9.3 日志复制 | 日志存储抽象（`LogManager` + `LogStorage`）、批量与流水线、`AppendEntries` 的一致性检查与回退 |
| 6.9.4 非事务请求 | ReadIndex 的实现（读索引队列 + 心跳确认）、Lease Read 开关 |
| 6.9.5 成员变更 | 一次一个节点的变更、`addPeer/removePeer` 的串行化、Learner 追赶 |

工程价值：它是**中文社区最完整的 Java Raft 实现之一**，且与本书章节一一对应，适合作为「读论文 → 读代码」的桥梁。

### 6.10 横向对比（本书小结）

| 维度 | Raft | Multi-Paxos | ZAB |
| --- | --- | --- | --- |
| 时代标识 | term | ballot（编号） | epoch（zxid 高位） |
| Leader | 强 Leader，唯一 | 允许短暂无主/多主（靠编号仲裁） | 强 Leader（primary） |
| 日志连续性 | **强制连续**（核心约束） | 允许空洞 | 主序 + 前缀属性 |
| 换主时的收敛 | 日志对齐（nextIndex 回退） | 逐 instance 重确认 | 独立的同步阶段 |
| 读路径 | 论文未写 → ReadIndex/Lease | 论文未写 → 同上思路 | 本地读 + `sync()` |
| 规格完整度 | **最高**（成员变更、日志压缩都在论文里） | 最低（Multi-Paxos 无正式规格） | 中（DSN 2011 论文 + 系统文档） |

## 版本演进

- **2014**：Raft 论文发表；论文已包含成员变更与日志压缩，但**未包含**读路径优化、PreVote/CheckQuorum（这些在 Ongaro 博士论文与工程实现中）；
- **2015–2017**：etcd v3、Consul 等把 ReadIndex / Lease Read / PreVote 变成事实标准；共享存储型数据库开始探索**乱序提交**（ParallelRaft 一脉）；
- **2018–2020**：Multi-Raft 分组（TiKV/CockroachDB）成熟；国产数据库形成各自的共识选型；
- **2023（本书）**：把「分区 / 读优化 / 并行协商 / 源码」四块集中讲，是本章相对一般中文材料的**最大增量**；
- **2026 视角**：读路径与成员变更已高度标准化（ReadIndex 为默认、PreVote 为标配）；**多组调度**与**可观测性/混沌测试**成为新的竞争点。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | Raft 主论文（本章 6.6–6.7 的问题均在此论文边界之外） |
| Ongaro《Consensus: Bridging Theory and Practice》 | Stanford 博士论文，2014 | **PreVote、CheckQuorum、客户端会话与线性一致读**等工程细节的出处 |
| Herlihy & Wing《Linearizability: A Correctness Condition for Concurrent Objects》 | ACM TOPLAS 1990 | 6.7.1 线性一致性的形式化定义 |
| Junqueira, Reed, Serafini《Zab: High-performance broadcast for primary-backup systems》 | DSN 2011 | 6.10.2 的对照物 |
| Lamport《Paxos Made Simple》 | ACM SIGACT News 2001 | 6.10.1 的对照物 |
| Howard《Raft Refloated: Do We Have Consensus?》 | ACM SIGOPS OSR 2015 | 对 Raft 简化表述与成员变更边界的再讨论 |

## 近年研究与工业界开源实践（2015–2026）

> star 数均为 2026-09 用 `gh api repos/OWNER/REPO --jq '.stargazers_count'` 实测。

- `etcd-io/etcd`（**52,310★**）/ `etcd-io/raft`（**1,128★**）：读默认 **ReadIndex**（不依赖时钟），成员变更**一次一个**并串行化，支持 **Learner**，实现了 PreVote。是「保守但可验证」的样板。
- `hashicorp/raft`（**9,136★**）：把存储抽象为 `LogStore/StableStore`，快照策略与 etcd 不同；同一份 Raft 论文下的**不同工程取舍**，值得逐项对照。
- `sofastack/sofa-jraft`（**3,824★**）：本章 6.9 主角；Java 生态里工程议题覆盖最全的实现之一。
- `tikv/tikv`（**16,878★**）/ `cockroachdb/cockroach`（**32,508★**）：Multi-Raft 分组 + 集中调度（PD）；把「一个组」的议题（选举、变更、快照）放大到「成千上万个组」的**调度与运维**议题。
- `jepsen-io/jepsen`（**7,504★**）：Jepsen 对 etcd、CockroachDB、TiDB 均有公开测试报告（按版本查阅 jepsen.io 的 analyses 列表）。
  - 对本章最有价值的结论：**读路径与客户端语义是偏差高发区**。etcd 的线性一致读、CockroachDB 的可串行化宣称、TiDB 的默认快照隔离，在故障注入下都出现过需要修复的偏差——但**根因几乎都不在 Raft 日志层**。
- **近年研究**：
  - **读路径**：ReadIndex 成为默认；Lease Read 只在能证明时钟漂移上界的受控环境中启用；
  - **分区韧性**：PreVote/CheckQuorum 已成为实现标配；非对称分区的处理进入常规测试集；
  - **可观测性与混沌测试**：Raft 组的 leader 分布、commit 延迟直方图、确定性模拟测试成为交付门槛。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Leader Read 是线性一致的」 | 不是。若该节点已不是真正 Leader（分区导致），会读到旧值；需要 ReadIndex 或 Lease |
| 2 | 「ReadIndex 和 Lease Read 一样安全」 | ReadIndex **不依赖时钟**（靠心跳确认 Leader 身份）；Lease Read **依赖时钟漂移上界**（🔧） |
| 3 | 「读也要 fsync」 | ReadIndex 不写日志、不 fsync；它只需要确认 Leader 身份 + 等状态机追上 |
| 4 | 「非对称分区只是『网络不好』」 | 它会让 term 无意义地飙升、集群反复换主；PreVote 正是为此设计 |
| 5 | 「ParallelRaft 是 Raft 的升级版」 | 它放松了 Raft 的核心约束（日志连续），安全性需重新论证，且面向专用存储场景（🔧） |
| 6 | 🔧 本书 6.7 未强调 Lease Read 的时钟假设 | 补：NTP 跳变、VM 迁移/暂停、长 GC 都可能导致旧 Leader 在租约失效后仍自认有效 → 返回旧值。生产建议**默认 ReadIndex**，把 Lease Read 限定在能证明漂移上界的环境 |
| 7 | 🔧 本书未把「多组调度」纳入工程实践 | 补：TiKV（**16,878★**）/CockroachDB（**32,508★**）的 Multi-Raft 把本章的每个议题（选举、变更、快照、读）都乘以「组数」，并新增了**分裂/合并、副本放置、热点调度**。2026 年 Raft 工程的主要复杂度在这里，不在单组算法 |
| 8 | 🔧 本书未给出 etcd 与 HashiCorp Raft 的对照 | 补：etcd 读默认 ReadIndex、变更一次一个、有 Learner；HashiCorp 用可插拔 `LogStore/StableStore`、快照与读路径策略不同。两者都实现了 PreVote。**选库要比对这些工程属性**，而不是「都实现了 Raft」 |
| 9 | 🔧 本书未给出 Jepsen 视角的边界 | 补：Raft 保证的是**日志层一致**；端到端线性一致还会被读路径、默认隔离级别、客户端重试削弱。`jepsen-io/jepsen`（**7,504★**）是验证手段，宣称一致性前应做故障注入测试 |
| 10 | 🔧 国产化选型对照缺失 | 补（公开资料口径）：**TiDB/TiKV → Multi-Raft**；**OceanBase → Multi-Paxos**；**PolarDB 相关设计 → ParallelRaft 一类并行共识**。差异源于分片粒度与存储形态；不要按「哪个算法更先进」选型，要按**生态、运维与验证充分性**选型 |

## 与其他章 / 其他书的联系

**本目录内**

- [07-Raft.md](07-Raft.md)：本章的问题（读路径、分区、成员变更）全部建立在 07 的算法基础上。
- [05-Multi-Paxos与PhxPaxos工程实现.md](05-Multi-Paxos与PhxPaxos工程实现.md)：Paxos 侧的读优化与重确认，与本章 6.7 逐条对照。
- [06-ZAB与ZooKeeper.md](06-ZAB与ZooKeeper.md)：6.10.2「Raft 与 ZAB 异同」的详细展开；ZooKeeper 的 `sync()` 与 Raft 的 ReadIndex 是同一问题的两种答案。
- [01-分布式共识算法概述.md](01-分布式共识算法概述.md)：本章所有读方案最终都是为了兑现第 1 章定义的「一致性」档位。

**跨书**

- [../深入理解分布式系统/07-Raft与拜占庭容错.md](../深入理解分布式系统/07-Raft与拜占庭容错.md)：Raft 与 BFT 的对照，可补本章未涉及的拜占庭场景。
- [../分布式算法/06-网络共识与选举.md](../分布式算法/06-网络共识与选举.md)：分区、选举与故障检测器的严格化处理。
- [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)：从架构视角判断读路径与一致性档位该如何选。
- [../分布式数据库入门进阶与实战/09-共识算法.md](../分布式数据库入门进阶与实战/09-共识算法.md)：把 Raft 放回数据库复制与事务的语境。
</content>
