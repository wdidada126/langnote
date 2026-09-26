# 第 3 章 Paxos 算法（Basic Paxos 与 Multi-Paxos）

> 覆盖原书：第 3 章「Paxos算法」。
> 3.1 Basic Paxos（三种角色 / 如何达成共识）、3.2 Multi-Paxos（兰伯特的思考 / Chubby 的实现）、3.3 小结。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 3.1.1 三种角色 | Proposer / Acceptor / Learner | 角色是**逻辑角色**，一个进程可同时扮演三个；工程实现几乎都三者合一 |
| 3.1.2 如何达成共识 | Prepare 阶段 + Accept 阶段 | 两阶段的本质是「**抢号（争当提议权）+ 定值（让多数派记住同一个值）**」 |
| 3.2.1 兰伯特关于 Multi-Paxos 的思考 | 选出 Leader、省掉 Prepare | Multi-Paxos **不是一个算法而是统称**：凡是「一次选举 + 多次只跑 Accept」的做法都算 |
| 3.2.2 Chubby 如何实现 Multi-Paxos | 租约选主、Master 续租 | 工程上的 Paxos = Multi-Paxos + 一堆补丁（成员变更、日志压缩、快照） |
| 3.3 小结 | 特点与适用场景 | 理解 Paxos 的最大价值不是「实现它」，而是读懂 Raft/ZAB 的设计动机 |

## 核心精讲

### 3.1.1 三种角色

| 角色 | 职责 | 现实对应 |
| --- | --- | --- |
| **Proposer（提议者）** | 提出提案（编号 n + 值 v），驱动两阶段 | 客户端接入的那个节点 / Leader |
| **Acceptor（接受者）** | 对提案投票，持久化「已承诺编号」与「已接受值」 | Raft 中「持有日志的 follower」的抽象 |
| **Learner（学习者）** | 读取已被选定的值，不参与投票 | 只读副本 / 备份节点 |

> 本书强调「你需要了解的 3 种角色」。要注意：**角色 ≠ 进程**。
> 真实系统中同一台机器既是 Proposer 又是 Acceptor 又是 Learner。

### 3.1.2 两阶段：抢号 + 定值

**阶段一 Prepare（抢号）**

```
教学示意，不参与构建
Proposer(n):                        // n 全局唯一且递增
    send Prepare(n) to all Acceptors
Acceptor on Prepare(n):
    if n > minProposal:
        minProposal = n            // 承诺：不再接受编号 < n 的提案
        reply Promise(n, acceptedN, acceptedV)   // 带上「我已接受过的最大编号提案」
    else:
        reply Nack                 // 或直接忽略
```

**阶段二 Accept（定值）**

```
教学示意，不参与构建
Proposer(n, v):
    if 收到多数派 Promise:
        v = 所有 Promise 中 acceptedN 最大的那个 acceptedV     // 关键！
        if 没有任何 Promise 带回值:
            v = 自己想提的值                                   // 可以自由选值
        send Accept(n, v) to all Acceptors
Acceptor on Accept(n, v):
    if n >= minProposal:
        acceptedN = n; acceptedV = v
        reply Accepted(n, v)       // Learner 据此学习
    else:
        reply Nack
```

**为什么「带回最大编号的值」是安全性的关键**：
一旦某个值 v 已被多数派接受，后续任何 Proposer 在 Prepare 阶段都会从多数派中**至少碰到一个**接受过 v 的 Acceptor，
于是被迫改提 v。这就是「**多数派必相交**」这一唯一数学事实的全部用途。

```
教学示意，不参与构建
// 活锁（liveness 问题）
P1: Prepare(1) -> ok -> Accept(1, v1) 期间
P2: Prepare(2) -> 让 Acceptor 提升 minProposal -> P1 的 Accept(1) 被拒
P1: Prepare(3) -> 又让 P2 的 Accept(2) 被拒
... 两个 Proposer 互相踩 -> 永不收敛
// 工程解法：只让一个 Leader 当 Proposer（这就是 Multi-Paxos）
```

### 3.2.1 兰伯特的思考：Multi-Paxos 不是算法

Lamport 的观察：如果**先选出一个稳定的 Leader**，并且 Leader 的提案编号一直最大，
那么 Prepare 阶段对**后续所有提案**都可以省略——只跑 Accept 阶段，一次 RTT 就完成一次共识。

于是「Multi-Paxos」在工程上变成一个**统称**，各家实现各不相同：

| 实现 | 选主方式 | 特点 |
| --- | --- | --- |
| Chubby（Google） | 租约 + Master 续租 | 本书 3.2.2 详述；Paxos Made Live 记录了它的工程坑 |
| PhxPaxos（微信） | 类 Raft 选举 | 国内落地最广的开源 C++ 实现 |
| 各类自研 | 外部协调服务选主 | 选主与共识分离，实现简单但引入外部依赖 |

### 3.2.2 Chubby 的实现：把 Paxos 变成「带日志的服务」

Chubby（Burrows, OSDI 2006）的关键工程决策：

1. **选主用租约**：Master 持有一个有限期租约，到期前续租；租约过期则重新选举。
   租约把「Leader 是否还活着」变成**时间上的约定**，避免依赖精确失败检测。
2. **日志 = 一组 Paxos Instance**：每个日志槽位（instance）跑一次 Paxos；
   Leader 连任期间这些 instance 共用同一个 Prepare 结果，只跑 Accept。
3. **必须有成员变更与快照**：论文没写、但线上必须有的部分。Google 在《Paxos Made Live》（Chandra et al., PODC 2007）
   里明确说：从论文到可用系统，他们**补了大量论文里没有的东西**——磁盘损坏处理、成员变更、快照、以及一个能把「测试通过」变成「确实正确」的机制。

## 版本演进

- **1990 / 1998**：Lamport 写出《The Part-Time Parliament》，被审稿人嫌「用希腊议会做比喻太难懂」，压了八年才发表在 ACM TOCS 1998。
- **2001**：Lamport 补发《Paxos Made Simple》，去掉比喻、只讲算法，成为绝大多数人（包括本书）的实际来源。
- **2006**：Chubby 论文（OSDI）与 **2007**《Paxos Made Live》（PODC）把 Paxos 从「理论可行」推到「工程可用」。
- **2013**：Raft 出现——**它的设计动机就是「Paxos 太难教、太难实现」**。Raft 论文明确说它把 Paxos 的单条目共识改成了连续日志 + 强 Leader。
- **2022（本书）**：第 3 章的定位是「读懂即可，不必手写」。书中把 Multi-Paxos 明确定性为「统称」——这一点比很多中文材料都准确。
- **2026 视角**：
  - 今天**新系统几乎都直接选 Raft**（etcd/TiKV/Consul/SOFAJRaft/braft），Paxos 主要出现在**老系统**（Chubby、Spanner 的 Paxos 组、Ceph 的 mon）与**研究型变种**（EPaxos、Fast Paxos）里；
  - 「Multi-Paxos」这个词在 2026 年的语境里，更常见的说法是「**Leader-based consensus with log**」，也就是 Raft 的同义词族；
  - Spanner 之后，**Paxos 组 + 分片（Multi-Raft / Multi-Paxos Group）**成为水平扩展的标准形态，这一点本书第 3 章完全没有展开。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Lamport《The Part-Time Parliament》 | ACM TOCS 1998 | Paxos 原始论文（希腊议会比喻版） |
| Lamport《Paxos Made Simple》 | ACM SIGACT News 2001 | 去比喻版，本书与绝大多数教材的实际来源 |
| Burrows《The Chubby lock service for loosely-coupled distributed systems》 | USENIX OSDI 2006 | 本书 3.2.2 的主角：租约选主 + Paxos 复制日志 |
| Chandra, Griesemer, Redstone《Paxos Made Live: An Engineering Perspective》 | PODC 2007 | 「论文到系统之间缺了什么」的第一手记录 |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | Raft：为可理解性重新设计，本书第 4 章 |
| Chandra & Toueg《Unreliable Failure Detectors for Reliable Distributed Systems》 | JACM 1996 | 失败检测器的形式化；租约选主的理论背景 |
| Gray & Cheriton《Leases: An Efficient Fault-Tolerant Mechanism for Distributed File Cache Consistency》 | SOSP 1989 | 租约机制的原始论文，Chubby 选主与 etcd lease 的共同源头 |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **EPaxos（Moraru, Andersen, Kaminsky, SOSP 2013）**：去中心化，无依赖的提案走快路径（1 RTT），有依赖的走慢路径。
    是「能不能不要 Leader」这一问题的代表性答案。
  - **Flexible Paxos（Howard & Mortier, OPODIS 2016）**：指出「所有 quorum 都必须相交」是过强的要求——
    只要 **Prepare 阶段的 quorum 与 Accept 阶段的 quorum 相交**即可。这一结论极大简化了「多数派」的工程配置。
  - **WPaxos / Multi-Raft 分组**：把单组共识扩展到多组分片，是 2018 年后的主流工程形态。
- **工业界开源**（star 数 2026-09 `gh api` 实测）：
  - `etcd-io/etcd`（**52310★**）：Raft 实现，且内置 **lease（租约）**、watch、revision 等 Chubby 一脉的能力，是本书 3.2.2 「租约选主」思想在 2026 年的最主流形态。
  - `hashicorp/raft`（**9136★**）：Go 的 Raft 库，本书第 14 章主角（见 [12-Hashicorp-Raft与分布式KV系统实战](12-Hashicorp-Raft与分布式KV系统实战.md)）。
  - `sofastack/sofa-jraft`（**3824★**）：蚂蚁的 Java Raft 实现，生产级（含快照、读优化、成员变更）。
  - `baidu/braft`（**4227★**）：百度 C++ Raft 实现（braft 现托管于该仓库；`apache/brpc` **17620★** 为其常见宿主项目）。
  - `tikv/tikv`（**16878★**）：**Multi-Raft 分组**的最大规模开源落地（每个 Region 一个 Raft 组 + PD 调度）。
  - `pingcap/tidb`（**40590★**）：在 Multi-Raft 之上叠加分布式事务（Percolator 模型）。
- **Jepsen 实测**（`jepsen-io/jepsen`，**7504★**）：etcd、Consul、TiDB 等均有专门报告；
  共识层本身极少出错，**出问题几乎都在「如何使用共识」这一层**（读路径、租约假设、时钟漂移）。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Paxos 一次共识只定一个值，所以没用」 | 单个值是**一个日志槽位**；连续跑就是复制状态机。Multi-Paxos 正是这个意思 |
| 2 | 「Prepare 阶段可以省掉」 | 只有**同一个 Leader 连续任期内**能省；新 Leader 上任必须先跑一次 Prepare 补齐空白 |
| 3 | 「多数派是指超过一半的节点都同意了某个值」 | 更准确的用法是「**任意两个多数派必相交**」。安全性来自交集，不来自「人数过半」这个数字 |
| 4 | 「Paxos 是 Leaderless 所以更容错」 | Basic Paxos 无 Leader 会**活锁**；所有实用系统都有 Leader（或 Leader 租约） |
| 5 | 🔧 2026 补丁：本书未讲 FLP 与失败检测器 | 第 3 章讲了「怎么做」但没解释「为什么必须这样做」。没有 FLP（JACM 1985）与 Chandra-Toueg（JACM 1996）失败检测器理论，读者无法理解「为什么要选主 + 超时」。补：[../分布式算法/03-FLP与不可能性.md](../分布式算法/03-FLP与不可能性.md) |
| 6 | 🔧 2026 补丁：缺 Flexible Paxos 的 quorum 视角 | 本书讲「多数派」，但 2016 年 Howard & Mortier 已证明**只要两阶段 quorum 相交**即可（不必都是多数派）。这一结论直接影响工程上的 quorum 配置与跨机房部署 |
| 7 | 🔧 2026 补丁：Multi-Paxos 的现代说法 | 2026 年工程语境里，「Multi-Paxos」几乎等同于「Leader-based 复制状态机」，且与 Raft 同族。本书按 2022 口径讲 Chubby，读者应知道 etcd/TiKV/Consul 走的是 Raft 而非 Paxos |
| 8 | 🔧 2026 补丁：未涉及 Multi-Raft 分组 | 单组 Paxos/Raft 无法水平扩展数据。2026 年的标准做法是**按 key range 分成多个 Raft 组**（TiKV/CockroachDB/Spanner），并配一个 Placement Driver 做调度。本书第 3 章完全没有这一层 |

## 与其他章 / 其他书的联系

- **本目录内**：
  - 本章的「两阶段 + 多数派相交」是 [03-Raft选举日志复制与成员变更](03-Raft选举日志复制与成员变更.md) 与 [05-ZAB协议与ZooKeeper](05-ZAB协议与ZooKeeper.md) 的共同底盘；
  - 本章「Multi-Paxos 无法保证操作顺序性」这一点，是第 6 章 6.1.1 的引子——见 [05-ZAB协议与ZooKeeper](05-ZAB协议与ZooKeeper.md)；
  - 本章的租约思想在 [12-Hashicorp-Raft与分布式KV系统实战](12-Hashicorp-Raft与分布式KV系统实战.md) 中落到 etcd lease。
- **跨书**：
  - [../深入理解分布式共识算法/04-Paxos.md](../深入理解分布式共识算法/04-Paxos.md)——同一算法的**推导式**重述，本章偏「读懂」，那边偏「论证」；
  - [../深入理解分布式共识算法/05-Multi-Paxos与PhxPaxos工程实现.md](../深入理解分布式共识算法/05-Multi-Paxos与PhxPaxos工程实现.md)——本书 3.2 的深化版（含幽灵日志、读优化）；
  - [../深入理解分布式系统/06-Paxos与Multi-Paxos及其变体.md](../深入理解分布式系统/06-Paxos与Multi-Paxos及其变体.md)——Paxos 家族综述，含 EPaxos/Fast Paxos 等本章未提的分支；
  - [../分布式算法/06-网络共识与选举.md](../分布式算法/06-网络共识与选举.md)——网络模型下的算法级对照；
  - [../分布式数据库入门进阶与实战/09-共识算法.md](../分布式数据库入门进阶与实战/09-共识算法.md)——数据库视角的「用」，与本章「懂」互为对照；
  - [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)——判断「这里到底需不需要共识」。
