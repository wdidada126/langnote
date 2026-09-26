# 第 6 章 ZAB 协议与 ZooKeeper

> 覆盖原书：第 6 章「ZAB协议」。
> 6.1 如何实现操作的顺序性、6.2 主节点崩溃了怎么办、6.3 如何从故障中恢复、6.4 如何处理读写请求、6.5 ZAB 与 Raft、6.6 小结。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 6.1.1 为什么 Multi-Paxos 无法保证顺序性 | 提案乱序 + 空洞 | Multi-Paxos 只保证「某个值被选定」，**不保证「按提交顺序被选定」** |
| 6.1.2 ZAB 如何保证顺序性 | 主节点排序 + 严格 FIFO 广播 | 顺序性来自「**只有一个节点给事务编号**」 |
| 6.2 主节点崩溃 / 选举 | ZAB 选举 vs ZooKeeper 选举 | 选举必须挑出**拥有最新历史**的节点，否则会丢已提交事务 |
| 6.3 故障恢复 | 发现（Discovery）→ 同步（Synchronization）→ 广播（Broadcast） | 恢复阶段先「对齐历史」再「开始广播」，这是 ZAB 与 Raft 形状上的最大差别 |
| 6.4 读写请求 | Leader 处理写、Follower 可处理读 | 读可能**陈旧**（ZooKeeper 默认不保证线性一致读） |
| 6.5 ZAB vs Raft | 主备广播 vs 复制状态机 | 两者都是「强 Leader + 多数派」，差别在日志模型与恢复流程 |

## 核心精讲

### 6.1.1 Multi-Paxos 为什么给不了顺序性

Multi-Paxos 里每个日志槽位（instance）是**独立跑一次 Paxos**的。这意味着：

1. **可以乱序选定**：instance 10 可能先于 instance 9 被选定，形成「空洞」；
2. **可以并行提交**：不同 instance 之间没有先后约束；
3. **需要额外机制补齐**：Leader 必须自己保证按序填充，并处理前任留下的空洞。

对「给你一个锁、一个配置」这类**复制状态机**场景，光有「每个槽位最终定值」不够，
还要求「**第 n 条指令在所有副本上都是同一条**且**顺序相同**」。这正是 ZAB 设计要直给的东西。

### 6.1.2 ZAB 的顺序性从哪来

ZAB（ZooKeeper Atomic Broadcast）的核心约束只有一句：

```
教学示意，不参与构建
// 所有事务都由「主节点（primary / leader）」分配单调递增的 zxid
zxid = (epoch << 32) | counter        // 高 32 位是纪元，低 32 位是纪元内计数
// 广播采用严格 FIFO 通道：
//   若事务 A 在事务 B 之前被主节点提交，则 A 必须在 B 之前被所有副本交付（deliver）
// -> 顺序性不是「协商」出来的，而是「主节点编号 + FIFO 通道」 enforced 出来的
```

对比：

| 协议 | 顺序性来源 | 是否需要处理空洞 |
| --- | --- | --- |
| Multi-Paxos | 无内建顺序性，靠 Leader 自律补齐 | 需要 |
| **ZAB** | 主节点编号 zxid + FIFO 广播 | 不需要（广播期是连续的） |
| **Raft** | 日志 index 连续 + 前一条匹配才追加 | 不需要（靠回退重试对齐） |

### 6.2 选举：为什么要挑「历史最新」的节点

```
教学示意，不参与构建
// 选举时的比较规则（ZooKeeper Fast Leader Election 使用的三元组）
//   依次比较 (epoch / zxid / myid)，大者胜
// 直觉：
//   一个节点若持有最大的 zxid，它最可能持有「所有已提交的事务」
//   选它做 Leader，恢复阶段只需「别人向它对齐」，不需要反向补齐
```

> 本书 6.2.1 讲 ZAB 的选举，6.2.2 讲 ZooKeeper 的实际实现（Fast Leader Election）。
> 二者的分野值得注意：**协议层的选举规则**与**工程实现的选举算法**不是一回事，
> 后者还要处理「选票传播」「选票统计」「looking/following/leading 状态机」。

### 6.3 故障恢复：三阶段不是两阶段

ZAB 的一个完整生命周期是 **四个阶段**（进入广播前的两个是恢复）：

```
教学示意，不参与构建
Phase 0: Election（选举）      -> 选出准 Leader，拿到 Epoch
Phase 1: Discovery（成员发现） -> 准 Leader 收集各 Follower 的 lastZxid，选出历史最新的历史作为「初始历史」
Phase 2: Synchronization（同步）-> 把初始历史补齐/截断到各 Follower，多数派确认后准 Leader 转正
Phase 3: Broadcast（广播）     -> 正常的两阶段提交式广播（Proposal -> ACK -> Commit）
// 关键：只有过了 Phase 2 才允许处理新写请求 —— 这是「先对齐，再服务」的原则
```

**为什么不能直接广播**：若 Follower 还留着「未被前任 Leader 提交的事务」，
必须先**截断**掉，否则同一 zxid 位置会出现两个不同的事务，违反顺序一致性。

### 6.3 补充：为什么「先对齐再服务」不能省

```
教学示意，不参与构建
// 反例：跳过 Synchronization 直接广播
//   旧 Leader L1 广播了事务 (epoch=1, counter=7) 给 A，但没发给 B、C
//   L1 宕机；B 被选为新 Leader（epoch=2）
//   若 B 直接开始广播 (epoch=2, counter=1)，而 A 仍持有 (1,7) 这条未提交事务
//   -> 客户端从 A 读会看到 (1,7)，从 B 读看不到 -> 顺序一致性被破坏
// 正解：B 必须先让 A 截断掉 (1,7)，把三者历史对齐到同一点，再开始广播
//   这就是 Phase 1/2 存在的全部理由
```

> 这个反例也解释了为什么 ZooKeeper 在 Leader 故障后**有一段明确的不可服务窗口**：
> 共识协议要求「先消除分歧，再接受新写」，这段时间无论如何都省不掉。

### 6.4 读写请求：读不一定线性一致

```
教学示意，不参与构建
// 写请求
client -> 任意节点；若是 Follower，转发给 Leader
Leader: 生成 zxid -> Proposal 广播 -> 等多数派 ACK -> Commit -> 应用
// 读请求
client -> 任意节点；节点**直接读本地内存数据库**返回（ZooKeeper 的 DataTree 全在内存）
// 后果：Follower 可能还没收到最新 Commit -> 读到旧值
// 这就是 ZooKeeper 的 "sequential consistency"（同一客户端的写后读可见），
// 而不是线性一致性（linearizability）
// 需要强读时：调用 sync()（一次「空写」走完 Leader 流程）再读
```

ZooKeeper 的 `sync()` 与 Raft 的 **Read Index** 是同一问题的两种答案——
本书没有把它们放在一起讲，但读者应当自行对照（见 [03-Raft选举日志复制与成员变更](03-Raft选举日志复制与成员变更.md) 4.4）。

### 6.5 ZAB 与 Raft 的差别

| 维度 | ZAB | Raft |
| --- | --- | --- |
| 设计目标 | **主备（primary-backup）广播**：所有副本最终执行同一序列 | 复制状态机，强调可理解性 |
| 日志模型 | 事务 + zxid（epoch.counter） | 日志项 + (term, index) |
| 恢复流程 | 显式的 Discovery → Synchronization 阶段 | 用 `nextIndex` 回退重试隐式对齐 |
| 选举比较 | (epoch, zxid, id) | (lastLogTerm, lastLogIndex) |
| 读一致性 | 默认 sequential，`sync()` 加强 | Read Index / Lease Read 加强 |
| 顺序性 | 由主节点编号强保证 | 由日志连续性天然保证 |

## 版本演进

- **2007–2010**：ZooKeeper 从 Yahoo! 的 Chubby 开源替代起步（Hunt et al., USENIX ATC 2010）。
- **2011**：Junqueira、Reed、Serafini 在 DSN 发表《Zab: High-performance broadcast for primary-backup systems》，
  第一次把 ZooKeeper 内部使用的协议**独立成文**并给出论证。
- **2022（本书）**：第 6 章是全书中**篇幅最大、最接近源码**的一章（6.4.2 直接给代码实现），
  也体现了作者的工程取向：ZAB 是「讲得最透」的那个协议。
- **2026 视角**：
  - ZooKeeper 已从「新项目的默认选择」退为**存量系统**：新项目优先 etcd/Consul/K8s 原生机制；
  - ZooKeeper 在 2023 年发布 **3.9.0**，引入了对 **Admin Server、只读模式**等能力的增强，但**架构未变**；
  - Curator（`apache/curator`，**3172★**）仍是 JVM 生态的事实标准客户端，其 `LeaderLatch`、`InterProcessMutex` 被广泛使用；
  - **服务发现从 ZooKeeper 迁往 etcd/Consul/K8s Service** 是 2018–2026 最明显的迁移潮流，
    动因是 K8s 生态绑定、运维复杂度与 etcd 的 watch/revision 模型更适合声明式配置。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Junqueira, Reed, Serafini《Zab: High-performance broadcast for primary-backup systems》 | IEEE DSN 2011 | ZAB 协议的正式论文（本书第 6 章的源头） |
| Hunt, Konar, Junqueira, Reed《ZooKeeper: Wait-free coordination for Internet-scale systems》 | USENIX ATC 2010 | ZooKeeper 的系统论文，含数据模型与 API |
| Burrows《The Chubby lock service for loosely-coupled distributed systems》 | USENIX OSDI 2006 | ZooKeeper 的设计原型 |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | 本书 6.5 的对照物 |
| Lamport《Paxos Made Simple》 | ACM SIGACT News 2001 | 本书 6.1.1「Multi-Paxos 无顺序性」的论证背景 |
| Gray & Cheriton《Leases: An Efficient Fault-Tolerant Mechanism for Distributed File Cache Consistency》 | SOSP 1989 | ZooKeeper 会话/ ephemeral 节点时间语义的源头之一 |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - ZAB 本身的研究热度在 2015 年后显著下降，研究重心转向 Raft 及其变体；
  - 关于「**协调服务到底要不要线性一致读**」的讨论持续存在：etcd 用 revision + Read Index 直接给出线性一致读，
    而 ZooKeeper 需要 `sync()`，这一差异在 2026 年仍是选型理由之一；
  - **ZooKeeper 的内存数据模型限制**（DataTree 全内存、单 Leader 写）使其天然不适合作为大规模配置/元数据存储，
    这是迁往 etcd 的技术动因。
- **工业界开源**（star 数 2026-09 `gh api` 实测）：
  - `apache/zookeeper`（**12811★**）：本书第 6 章主角；仍在 Kafka、Hadoop、HBase、Dubbo 等生态中广泛使用。
  - `apache/curator`（**3172★**）：ZooKeeper 的 JVM 客户端与「配方（recipes）」库（锁、选主、屏障）。
  - `etcd-io/etcd`（**52310★**）：2026 年新建系统的主流替代，线性一致读 + lease + watch。
  - `hashicorp/consul`（**30085★**）：服务发现的另一替代路径（Raft + Serf Gossip 混合）。
  - `kubernetes/kubernetes`（**128012★**）：其内置服务发现/配置（Service、ConfigMap、Lease API）取代了大量 ZooKeeper 用例。
  - `apache/rocketmq`（**22621★**）：其 NameServer 走的是**无共识**的最终一致路由，是「协调服务可以不用共识」的反例样本。
- **Jepsen 实测**（`jepsen-io/jepsen`，**7504★**）：ZooKeeper 有专门报告；
  其结论与本书 6.4 一致——**默认读不是线性一致的**，需要额外机制。同时也指出其分布式锁配方在某些故障下的问题。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「ZooKeeper 读是线性一致的」 | **不是**。默认只能保证同一客户端的 sequential consistency；强读要 `sync()` |
| 2 | 「ZAB 就是 Paxos 换了个名字」 | 不是。ZAB 是**主备广播协议**，目标是顺序交付；Paxos 是单值共识 |
| 3 | 「Follower 也能处理写」 | 不能。所有写必须过 Leader（Follower 只做转发） |
| 4 | 「zxid 就是一个自增 ID」 | 它是 `(epoch, counter)` 二元组；epoch 变化时 counter 归零，用于识别「新旧 Leader 的日志」 |
| 5 | 🔧 2026 补丁：本书未充分强调「先对齐再服务」的代价 | 6.3 的 Discovery→Synchronization 阶段意味着 **Leader 故障后有一段不可服务时间**。2026 年的系统常把这段时间的 SLA 明确写出来（etcd 通常数秒内恢复），本书未给量化 |
| 6 | 🔧 2026 补丁：服务发现迁移潮本书未涉及 | 书成书时 ZooKeeper 仍是主流协调服务。2026 年新建系统多直接选 **etcd / Consul / K8s 原生机制**，ZooKeeper 主要在 Kafka/Hadoop/HBase 等存量生态中。读者应把第 6 章当作「读懂存量系统」而非「新建项目的首选」 |
| 7 | 🔧 2026 补丁：ZooKeeper 的锁配方不等于分布式锁的正确答案 | Curator 的 `InterProcessMutex` 依赖 ZooKeeper 会话与 ephemeral 节点；**会话超时不等于业务持有结束**（GC 停顿、网络抖动会造成「锁丢失但业务还在跑」）。这是所有基于会话/TTL 的锁的共性风险，也是 Redlock 争议的同一类问题 |
| 8 | 🔧 2026 补丁：缺少与 Raft Read Index 的对照表 | 本书 6.5 只比了协议结构，没有把「ZooKeeper `sync()` vs Raft Read Index vs Lease Read」放到一张表里。建议与 [03-Raft选举日志复制与成员变更](03-Raft选举日志复制与成员变更.md) 4.4 合并阅读 |

## 与其他章 / 其他书的联系

- **本目录内**：
  - 6.1.1 的问题陈述来自 [02-Paxos与Multi-Paxos](02-Paxos与Multi-Paxos.md)，两章必须连读；
  - 6.5 的对比表要与 [03-Raft选举日志复制与成员变更](03-Raft选举日志复制与成员变更.md) 对读；
  - 6.4 的读语义在 [07-Quorum-NWR](07-Quorum-NWR.md) 里能看到「另一种放弃线性一致」的做法。
- **跨书**：
  - [../深入理解分布式共识算法/06-ZAB与ZooKeeper.md](../深入理解分布式共识算法/06-ZAB与ZooKeeper.md)——Chubby 血缘 + ZAB 四阶段 + 成员变更 + 源码实战，与本章同源且更深；
  - [../深入理解分布式共识算法/07-Raft.md](../深入理解分布式共识算法/07-Raft.md)——6.5 对照的另一半；
  - [../深入理解分布式系统/10-案例研究文件系统与协调服务.md](../深入理解分布式系统/10-案例研究文件系统与协调服务.md)——协调服务的案例视角；
  - [../分布式算法/06-网络共识与选举.md](../分布式算法/06-网络共识与选举.md)——选举的算法级形式化；
  - [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)——何时该用协调服务而非自研共识。
