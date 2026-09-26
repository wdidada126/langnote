# 第 7 章 Raft——共识算法的宠儿（6.1–6.5）

> 覆盖原书第 6 章前五节（第 2 篇，P164–191）：6.1 Raft简介（诞生的背景 / 可理解性 / 基本概念）；
> 6.2 Raft算法描述（Leader选举 / 日志复制 / 日志对齐 / 幽灵日志 / 安全性 / Raft小结）；
> 6.3 算法模拟（Leader选举 / 日志复制 / 日志对齐）；6.4 成员变更（联合共识 / 工程实践 / 单个成员变更）；
> 6.5 日志压缩。
> 后半章（网络分区、非事务请求、Parallel Raft、SOFAJRaft 源码）见 [08-Raft工程实践与SOFAJRaft.md](08-Raft工程实践与SOFAJRaft.md)。

## 本章地图

本章是全书篇幅最大、也是工程价值最高的一章。Raft 的设计哲学是**把「可理解性」当作与「正确性」同等级的目标**：

```
Paxos 的问题：难理解、难实现 → 系统会「照着论文写，但写错」
   │
   ▼  Raft 的两把刀
   ① 问题分解：Leader 选举 / 日志复制 / 安全性 三个子问题分开讲
   ② 状态空间压缩：强 Leader + 日志连续性，减少可能的状态组合
```

- **6.1**：背景（Paxos 理解成本高）与「可理解性」的方法论；基本概念：**term、三种角色、两类 RPC**；
- **6.2**：算法主体——选举（随机化超时）、日志复制（多数派确认即提交）、日志对齐（一致性检查回退）、幽灵日志、**安全性**（选举限制 + 只提交当前 term 的日志）；
- **6.3**：三个场景的算法模拟（本书的特色：用具体时序把算法跑一遍）；
- **6.4**：成员变更——**联合共识（joint consensus）** 与单成员变更；
- **6.5**：日志压缩（快照）。

## 核心精讲

### 6.1.3 基本概念

| 概念 | 含义 |
| --- | --- |
| **term（任期）** | 逻辑时间单位，单调递增；每个 term 至多一个 Leader。term 是 Raft 的「epoch」，作用等同于 ZAB 的 epoch、Paxos 的 ballot |
| **角色** | Leader（唯一，处理所有写）/ Follower（被动）/ Candidate（选举中的临时状态） |
| **AppendEntries RPC** | Leader 用于日志复制 + 心跳（空条目） |
| **RequestVote RPC** | Candidate 用于拉票 |
| **Commit Index** | 已被多数派复制的最高日志索引；可被状态机应用 |

**三条持久状态**（必须落盘）：`currentTerm`、`votedFor`、`log[]`；
**两条易失状态**：`commitIndex`、`lastApplied`；
**Leader 专有易失状态**：`nextIndex[]`、`matchIndex[]`。

### 6.2.1 Leader 选举

```text
// 教学示意：Raft 选举（不参与构建、不编译、不运行）
// 所有节点启动时是 Follower，持有随机化选举超时（论文示例 150–300ms）
on electionTimeoutElapsed():
    currentTerm++; votedFor = self; state = CANDIDATE
    votes = 1
    for p in peers: async p.RequestVote(currentTerm, selfId, lastLogIndex, lastLogTerm)
    // 投票规则（6.2.5 安全性的一部分）：
    //   - term 更小 → 拒；
    //   - 已投给别人 → 拒；
    //   - 候选人日志不如我新（比较 (lastLogTerm, lastLogIndex)）→ 拒
    if votes > n/2: state = LEADER; sendHeartbeats()
on receive AppendEntries from leader with term >= currentTerm:
    state = FOLLOWER; resetElectionTimer()
```

- **随机化选举超时的作用**：让「同时超时 → 选票瓜分 → 再来一轮」的概率降到极低。这是 Raft 解决选举活锁的方式，也是它与 Paxos「选主」的最大区别（Paxos 用 ballot 抢号，Raft 用随机超时 + 任期）。
- **选举限制**：只有**日志足够新**的节点能当选——这保证了「已提交的日志不会丢」，是安全性的第一块基石。

### 6.2.2 日志复制

1. 客户端请求 → Leader 追加到本地日志（**先 fsync**）；
2. 并行发 `AppendEntries` 给所有 Follower（携带 `prevLogIndex`、`prevLogTerm`、`entries[]`、`leaderCommit`）；
3. 多数派成功 → Leader 推进 `commitIndex` 并应用状态机 → 返回客户端；
4. 后续 `AppendEntries`（含心跳）携带 `leaderCommit`，Follower 据此推进自己的 `commitIndex`。

> **注意**：Raft 的「提交」是**靠 Leader 计数多数派**判定的，且 6.2.5 有一条关键限制——**Leader 只能直接提交当前 term 的日志**（详见下）。

### 6.2.3 日志对齐

Follower 日志与 Leader 不一致时，`AppendEntries` 的一致性检查（`prevLogIndex/prevLogTerm` 是否匹配）失败，Leader 递减 `nextIndex` 重试，直到找到匹配点再覆盖后续条目。

- 朴素实现：一次退一条（日志差异大时很慢）；
- 工程优化：Follower 在拒绝时回带**冲突 term 与其首条索引**，让 Leader 一次跳过整个 term（Ongaro 论文已提及，etcd/HashiCorp 均有实现）。

### 6.2.4 幽灵日志（Raft 语境）

与 [05](05-Multi-Paxos与PhxPaxos工程实现.md) 中 Paxos 的同名问题一致：旧 Leader 写入但未提交的条目，在新 Leader 上任后若被「复活」，客户端会看到一条它认为失败的写。**Raft 的通用工程解法**：新 Leader 上任后**立即提交一条 no-op 空日志**，把之前所有未决条目一次性封住（同时也顺带推进了 commitIndex），之后才对外服务。

### 6.2.5 安全性：两条关键规则

1. **选举限制（Leader Completeness）**：候选人的日志必须「不比投票者的旧」才能得到选票 → 任何已提交的条目必然出现在新 Leader 的日志中。
2. **只提交当前 term 的日志**：Leader 不能仅凭「某条**旧 term** 的日志已被多数派复制」就提交它。经典反例（论文图 8）：旧 term 的条目被多数派复制但未提交，换主后新 Leader 若复制了自己的新条目使多数派达成，再回头提交旧条目——若此时再次换主，那条旧条目可能被覆盖。
   - 正确做法：**提交当前 term 的条目时，之前的所有条目随一同被提交**（因为日志连续 + 前缀匹配）。

```text
// 教学示意：提交判定（不参与构建、不编译、不运行）
fn advanceCommitIndex():
    // 只统计「当前 term」的条目在多少个节点上已复制
    for i in (commitIndex+1 .. lastLogIndex):
        if log[i].term == currentTerm and countReplicated(i) > n/2:
            commitIndex = i          // 因日志连续，i 之前的所有条目一并提交
```

### 6.4 成员变更

**联合共识（Joint Consensus，6.4.1）**：变更分两步走，中间存在一个同时包含新旧配置的过渡配置 $C_{old,new}$：

| 阶段 | 配置 | 要求 |
| --- | --- | --- |
| 1 | Leader 收到变更，写入 $C_{old,new}$ 并复制 | 决议需要 **$C_{old}$ 的多数派 + $C_{new}$ 的多数派**都同意 |
| 2 | $C_{old,new}$ 提交后，写入 $C_{new}$ 并复制 | 只需 $C_{new}$ 的多数派 |

任何时刻都不存在「两个配置各自选出 Leader 且互不知情」的窗口——因为过渡期两个配置的多数派必须相交。

**单个成员变更（6.4.3）**：一次只加/减一个节点。在 $n \to n+1$ 与 $n \to n-1$ 两种情形下，新旧 quorum 必然相交，因此**无需联合共识**。

> 🔧 **单步变更的工程前提**：必须保证**同一时刻只有一个在途变更**，且**变更条目提交后才能开始下一个**。若并发变更或变更提交前又提出新变更，仍可能构造出双 Leader。etcd 等实现对此有严格串行化约束（参见 [08-Raft工程实践与SOFAJRaft.md](08-Raft工程实践与SOFAJRaft.md)）。

**6.4.2 工程实践**（成员变更中真正麻烦的部分）：
- 新加入节点的**日志追赶**：先作为 Learner 复制日志（不参与投票），追上后再纳入投票集合；
- 移除节点时 Leader 可能**是被移除者**，需要「移交 Leader」再退出；
- 变更期间的**分区处理**（见本书 6.6）。

### 6.5 日志压缩

- 长期运行的日志不可能无限增长 → 定期做**快照（snapshot）**：把状态机的当前状态序列化落盘，丢弃已应用的日志前缀；
- 落后太多的 Follower 无法用 `AppendEntries` 补齐（其所需日志已被截断）→ Leader 发 **InstallSnapshot RPC**（论文中列出该 RPC）；
- 快照的代价：STW 或 Copy-on-Write（工程上多用 COW/分块快照避免阻塞写入）。

## 版本演进

- **1988**：Oki & Liskov 的 **Viewstamped Replication（VR，PODC 1988）** 已经用了「主副本 + quorum + 视图变更」，与 Raft 思路高度相近；
- **2013–2014**：Ongaro & Ousterhout 在设计教学中发现 Paxos 难以教学与实现，遂以可理解性为目标重构，发表《In Search of an Understandable Consensus Algorithm》（USENIX ATC 2014）；Ongaro 的斯坦福博士论文（2014）补充了大量论文未写的工程细节（客户端交互、成员变更细节、性能优化）；
- **2014–2016**：etcd（CoreOS）、Consul（HashiCorp）相继采用，Raft 迅速成为事实标准；
- **2016–2020**：**Multi-Raft 分组**成为分布式数据库的标配（TiKV、CockroachDB），共识从「一个组」走向「成千上万个组 + 调度器」；
- **2023（本书）**：用「算法模拟 + SOFAJRaft 源码」讲 Raft，是中文材料中少见的「能落地」的讲法；
- **2026 视角**：Raft 的地位已稳固，争议点转移到了**读路径语义、成员变更的自动化、快照/压缩策略、多组调度**等论文未覆盖的工程议题。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Oki & Liskov《Viewstamped Replication: A New Primary Copy Method to Support Highly-Available Distributed Systems》 | PODC 1988 | VR：与 Raft 同构思想的早期工作 |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | **Raft 主论文**：选举、日志复制、安全性、成员变更、日志压缩 |
| Ongaro《Consensus: Bridging Theory and Practice》 | Stanford 博士论文，2014 | 论文未覆盖的工程细节（客户端会话、线性一致读、性能优化、变更细节） |
| Lamport《Paxos Made Simple》 | ACM SIGACT News 2001 | 对照物：Raft 的设计动机来源 |
| Howard《Raft Refloated: Do We Have Consensus?》 | ACM SIGOPS OSR 2015 | 对 Raft 简化表述的澄清与 quorum 视角的再讨论 |
| Howard, Malkhi, Spiegelman《Flexible Paxos: Quorum Intersection Revisited》 | OPODIS 2016 | 把 quorum 视角推广，也适用于 Raft 的 quorum 配置 |
| Chandra & Toueg《Unreliable Failure Detectors for Reliable Distributed Systems》 | JACM 1996 | 选主/超时机制的理论背景 |

## 近年研究与工业界开源实践（2015–2026）

> star 数均为 2026-09 用 `gh api repos/OWNER/REPO --jq '.stargazers_count'` 实测。

- **`etcd-io/etcd`（52,310★）与 `etcd-io/raft`（1,128★）**：Raft 生态最大的实现（Kubernetes 依赖 etcd）。特点：Raft 被拆成独立可复用库；读默认 **ReadIndex**（线性一致）；成员变更一次一个、严格串行；有 Learner 角色。
- **`hashicorp/raft`（9,136★）**：Consul/Nomad/Vault 使用的 Go 库。与 etcd-io/raft 的差异在读路径、快照策略、成员变更约束与可插拔存储（LogStore/StableStore 抽象）上——**两者都不是「照抄论文」**。
- **`sofastack/sofa-jraft`（3,824★）**：蚂蚁开源、本书 6.9 主角。Java 实现，工程议题（快照、读优化、成员变更、批量与流水线）覆盖完整。
- **`tikv/tikv`（16,878★）、`cockroachdb/cockroach`（32,508★）**：**Multi-Raft 分组**的两个代表——按 Range/Region 切分成成千上万个 Raft 组，配合集中调度（PD）做副本放置、分裂合并与负载均衡。这是论文完全没写、却是 2026 年共识最重要的工程形态。
- **`jepsen-io/jepsen`（7,504★）**：第三方一致性验证。Jepsen 对 etcd、CockroachDB、TiDB 均有公开测试报告（按版本在 jepsen.io 的 analyses 列表查阅）。共同结论是：**偏差多出在读路径、时钟依赖、默认隔离级别与客户端重试语义，而非 Raft 算法本身**——这条结论对本章尤其重要，因为它界定了「Raft 保证了什么、没保证什么」。
- **近年研究**：
  - **读路径**：ReadIndex / Lease Read 成为标配，代价与时钟假设是核心权衡（详见 [08](08-Raft工程实践与SOFAJRaft.md)）；
  - **成员变更自动化**：自动 rebalance、Learner 追赶、Leader 移交，从「人工操作」走向「调度器自动完成」；
  - **形式化验证**：Raft 的 TLA+ 规格与确定性模拟测试成为实现的质量门槛。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「被多数派复制就等于提交」 | Leader **只能直接提交当前 term 的条目**；旧 term 条目要等当前 term 的条目提交后被「顺带」提交（论文图 8 的反例） |
| 2 | 「任期 term 就是时间」 | term 是**逻辑时钟**，只在选举时递增；空闲集群 term 不变 |
| 3 | 「日志对齐就是 Leader 把日志全量发给 Follower」 | 通过 `prevLogIndex/prevLogTerm` 做一致性检查回退，只发缺失部分；差异过大才走 InstallSnapshot |
| 4 | 「成员变更随时可做」 | 需要 quorum 相交保证；单步变更也必须**串行且等前一条变更提交**，否则仍可能双 Leader |
| 5 | 「快照只是省空间」 | 快照还会改变**落后的 Follower 的补齐方式**（必须走 InstallSnapshot），并引入 STW/COW 的取舍 |
| 6 | 🔧 Raft 论文**没有**覆盖读路径优化 | 论文只保证「日志一致性」，**不含** ReadIndex / Lease Read。这两者是工程实现的关键差异点（etcd 默认 ReadIndex，Lease Read 可选）。详见 [08-Raft工程实践与SOFAJRaft.md](08-Raft工程实践与SOFAJRaft.md) |
| 7 | 🔧 本书未点明 Multi-Raft 分组这一主流形态 | 单组 Raft 的吞吐受 Leader 限制；生产系统靠**按 Range/Region 切分成千上万个 Raft 组 + 集中调度**（TiKV **16,878★**、CockroachDB **32,508★**）实现水平扩展。论文与本书都停留在「一个组」的视角 |
| 8 | 🔧 本书未给出 etcd 与 HashiCorp Raft 的实现差异 | 两者在**读路径、快照策略、成员变更约束、存储抽象（etcd 自带 WAL+bolt；HashiCorp 抽象出 LogStore/StableStore）**上差异明显；选库时要按这些工程属性比对，而非「都实现了 Raft」 |
| 9 | 🔧 「用了 Raft 就是线性一致」需加限定 | Jepsen（**7,504★**）对 etcd/CockroachDB/TiDB 的测试显示，端到端保证还会被**读路径、默认隔离级别、时钟与客户端重试**削弱。Raft 保证的是**日志层**的一致，应用层的一致性要另外论证 |
| 10 | 🔧 本书未讨论 Raft 的国产化选型对照 | 公开资料口径：**TiDB/TiKV 用 Multi-Raft**；**OceanBase 以 Multi-Paxos 为核心**；**PolarDB 相关设计采用 ParallelRaft 一类并行共识**。差异来自分片粒度与存储形态，不是算法家族之争 |

## 与其他章 / 其他书的联系

**本目录内**

- [08-Raft工程实践与SOFAJRaft.md](08-Raft工程实践与SOFAJRaft.md)：本章的直接续篇（分区、读优化五方案、Parallel Raft、源码、与 Paxos/ZAB 对比）。
- [04-Paxos.md](04-Paxos.md) / [05-Multi-Paxos与PhxPaxos工程实现.md](05-Multi-Paxos与PhxPaxos工程实现.md)：term ↔ ballot；日志连续性是 Raft 相对 Paxos 的**额外约束**，换来可理解性。
- [06-ZAB与ZooKeeper.md](06-ZAB与ZooKeeper.md)：epoch ↔ term；ZAB 的同步阶段 ↔ Raft 的日志对齐。
- [12-FLP不可能定理.md](12-FLP不可能定理.md)：随机化选举超时正是「绕开 FLP」的随机化手段之一。

**跨书**

- [../深入理解分布式系统/07-Raft与拜占庭容错.md](../深入理解分布式系统/07-Raft与拜占庭容错.md)：Raft 的另一份中文讲法 + BFT 对照，与本章互补。
- [../分布式算法/06-网络共识与选举.md](../分布式算法/06-网络共识与选举.md)：选举与共识的算法级严格处理。
- [../分布式算法导论/06-选举算法.md](../分布式算法导论/06-选举算法.md)：从图算法视角看「选主」，与 6.2.1 对照。
- [../分布式数据库入门进阶与实战/09-共识算法.md](../分布式数据库入门进阶与实战/09-共识算法.md)：工程口径的 Raft，读它可快速判断「要不要自己实现」。
</content>
