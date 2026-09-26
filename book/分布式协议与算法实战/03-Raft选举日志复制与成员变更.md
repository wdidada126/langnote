# 第 4 章 Raft 算法（选举 / 日志复制 / 成员变更）

> 覆盖原书：第 4 章「Raft算法」。
> 4.1 如何选举领导者、4.2 如何复制日志、4.3 如何解决成员变更问题、4.4 Raft 与一致性、4.5 小结。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 4.1.1 成员身份 | Leader / Follower / Candidate | 任一时刻最多一个合法 Leader；**任期（term）**是逻辑时钟 |
| 4.1.2 选举过程 | 心跳超时 → 自增 term → 请求投票 → 多数派 | 随机化选举超时是**避免分裂投票**的关键工程技巧 |
| 4.1.3 选举过程四连问 | 任期/日志新旧/超时/分裂票 | 「日志至少跟我一样新」这一条是安全性的核心约束 |
| 4.2.1–4.2.2 日志与复制 | 日志项 = (term, index, 指令) | 复制 = 追加 + 多数派确认后提交 |
| 4.2.3 日志一致性 | 前一条匹配则本条匹配（归纳） | **日志匹配特性**让 Leader 能靠「回退重试」对齐 follower |
| 4.3 成员变更 | 单节点变更 | 一次只增删一个节点，**新旧两个多数派必相交**，无需联合共识 |
| 4.4 Raft 与一致性 | 线性一致性的读路径 | 直接读 Leader **不够**——需要 Read Index / Lease Read 等机制 |

## 核心精讲

### 4.1 选举：任期 + 随机超时

```
教学示意，不参与构建
// 每个节点维护
state       : FOLLOWER | CANDIDATE | LEADER
currentTerm : int             // 逻辑时钟，单调递增
votedFor    : nodeID | null
log[]       : [(term, index, cmd)]
commitIndex : int
// FOLLOWER 侧
on electionTimeout:                    // 随机区间，如 150~300ms
    state = CANDIDATE
    currentTerm += 1
    votedFor = self
    send RequestVote(currentTerm, lastLogIndex, lastLogTerm) to all
// 投票方（每个 term 只能投一票、先到先得）
on RequestVote(t, lastIdx, lastTerm):
    if t < currentTerm:  reject
    if (votedFor == null or votedFor == candidate) and
       候选人的日志至少跟我一样新:        // (lastTerm, lastIdx) 字典序比较
        votedFor = candidate; grant
    else: reject
// CANDIDATE 侧
if 收到多数派 grant:  state = LEADER; 立即发心跳宣誓
if 收到更高 term 的消息: state = FOLLOWER; 更新 currentTerm
if 超时未决: 重新选举（新 term，超时值再次随机）
```

**为什么随机超时**：若所有节点同时超时，谁都拿不到多数派，选举反复失败。
随机化让「某个节点先超时」成为高概率事件，从而快速收敛。这是 Raft 少有的**概率性**设计。

### 4.1.3 四连问里的关键一条

> 「日志至少跟我一样新」的判定：先比 `lastLogTerm`，相同再比 `lastLogIndex`。

这一条保证了**日志完整性特性（Leader Completeness）**：
因为一条日志只有被多数派写入才算可能提交，而新 Leader 必须拿到多数派选票，
两个多数派必相交，所以**新 Leader 一定持有所有已提交的日志**。
这是 Raft 不需要像 Paxos 那样「Learner 反向补齐」的根本原因。

### 4.2 日志复制与一致性

```
教学示意，不参与构建
// LEADER 侧
on client cmd:
    log.append((currentTerm, nextIndex, cmd))
    send AppendEntries(prevIndex, prevTerm, entries[], leaderCommit) to all   // 心跳复用此 RPC
on 多数派返回成功:
    commitIndex = 该日志项的 index
    apply 到状态机; 回复客户端
// FOLLOWER 侧
on AppendEntries(prevIndex, prevTerm, ...):
    if prevIndex 处不存在或 term 不匹配:  return false   // 一致性检查失败
    删除冲突项; 追加 entries; commitIndex = min(leaderCommit, 本地最后 index)
    return true
// LEADER 收到 false:  nextIndex -= 1; 重试（可批量回退以加速）
```

**日志匹配特性**（Log Matching Property）：若两个日志在某一 index 上的 (term, index) 相同，
则**该 index 之前的所有日志项都相同**。由「AppendEntries 只在前一条匹配时才追加」这一条归纳可得。
它让「对齐 follower」退化成一个简单的**回退重试**循环，而不需要传输完整日志。

### 4.3 成员变更：为什么单节点变更就够了

联合共识（joint consensus，论文原方案）需要两阶段、中间态复杂。
单节点变更（single-server change）的正确性论证只有一句话：

```
教学示意，不参与构建
// 旧集群 N 个节点 -> N+1 个节点（一次只加一个）
旧多数派大小 = floor(N/2) + 1
新多数派大小 = floor((N+1)/2) + 1
任意「旧多数派」与「新多数派」必有交集  -> 不会同时选出两个 Leader
// 例：N=3 -> 4，旧多数派 2，新多数派 3，交集 >= 1
```

> 本书 4.3.2 讲的正是这一条。需要注意的前提：**一次只能变更一个节点**，
> 且必须等上一个变更**提交后**才能开始下一个——否则交集性质不再成立。

### 4.4 Raft 与一致性：写一致 ≠ 读一致

Raft 保证的是**日志项顺序一致**（复制状态机的安全性），但**直接读 Leader 的本地状态机并不安全**：
网络分区后旧 Leader 可能仍以为自己是 Leader，读到的就是陈旧数据。

四种读方案（2026 年工程语境，本书 4.4 只给了概念）：

| 方案 | 做法 | 代价 |
| --- | --- | --- |
| Leader Read（不安全） | 直接读本地 | 可能读陈旧数据（stale read） |
| Log Read | 把读也当成一条日志走一遍 | 安全但每次读都要写日志、落盘 |
| **Read Index** | Leader 记录当前 commitIndex，发一轮心跳确认自己仍是 Leader，再等状态机追上该 index | 一次 RTT（可用心跳合并），无落盘 |
| **Lease Read** | 基于租约：租约期内不可能有新 Leader，直接读本地 | **依赖时钟**，时钟漂移会破安全性 |

## 版本演进

- **2014**：Ongaro & Ousterhout 在 USENIX ATC 发表 Raft 论文，明确以「**可理解性**」为设计目标，
  并把实现细节（成员变更、日志压缩、客户端交互）写进**扩展版（dissertation）**而非主论文。
- **2015–2016**：CoreOS 的 etcd、HashiCorp 的 Consul 先后采用 Raft；`hashicorp/raft` 成为 Go 生态事实标准库。
- **2019–2021**：国内 SOFAJRaft（蚂蚁）、braft（百度）成熟；TiKV 把 Multi-Raft 推到大规模生产。
- **2022（本书）**：第 4 章按「选举 → 日志 → 成员变更 → 一致性」组织，与论文结构一致，
  且**选择了单节点变更而非联合共识**——这是工程派写法，本书的一大优点。
- **2026 视角**：
  - Raft 已经**赢了共识算法的工程战争**：etcd / Consul / TiKV / CockroachDB / SOFAJRaft / braft 全是 Raft；
  - 「Raft 论文的 20 页」只是开始，**生产级实现 = 论文 + 成员变更 + 快照/压缩 + 读优化 + 流量控制 + 磁盘故障处理**；
  - 论文里的 Leader 选举在 2026 年常被换成 **Leader 租约 + 外部选主服务**（尤其在托管 K8s / 云环境里）。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | Raft 主论文：强 Leader、日志连续、成员变更 |
| Ongaro《Consensus: Bridging Theory and Practice》 | PhD dissertation, Stanford 2014 | 论文未覆盖的工程细节（日志压缩、客户端会话、性能） |
| Lamport《Paxos Made Simple》 | ACM SIGACT News 2001 | Raft 的对照物与设计动机 |
| Chandra & Toueg《Unreliable Failure Detectors for Reliable Distributed Systems》 | JACM 1996 | 失败检测器；解释了为什么 Raft 必须用超时 |
| Gray & Cheriton《Leases: An Efficient Fault-Tolerant Mechanism for Distributed File Cache Consistency》 | SOSP 1989 | Lease Read 的源头；也解释 Read Index 为何更安全 |
| Fischer, Lynch, Paterson《Impossibility of Distributed Consensus with One Faulty Process》 | JACM 1985 | FLP：Raft 之所以引入随机超时的理论原因 |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **Multi-Raft 分组 / Parallel Raft**：单组 Raft 的吞吐受限于单个 Leader，工程上按 key range 分多组；
    PolarFS（Aliyun, 2018）提出的 **Parallel Raft** 允许乱序确认 + 空隙合并，是 Raft 面向 NVMe 的改良。
  - **Raft 的形式化验证**：2015 年后出现多个 TLA+/Coq 的 Raft 安全性证明（含 etcd 对成员变更的 TLA+ 规格），
    说明「论文 20 页」确实不足以覆盖真实实现。
  - **租约读的时钟风险**：多方（含 etcd 官方）明确指出 **Lease Read 依赖时钟漂移上界**，
    云环境 VM 暂停/时钟跳变会破坏它，因此 etcd 默认走 **Read Index** 而非 Lease Read。
- **工业界开源**（star 数 2026-09 `gh api` 实测）：
  - `etcd-io/etcd`（**52310★**）：Go 实现，Read Index 默认、lease 机制、watch 机制齐全；K8s 的元数据存储。
  - `hashicorp/raft`（**9136★**）：本书第 14 章主角，被 Consul、InfluxDB Enterprise 等使用。
  - `sofastack/sofa-jraft`（**3824★**）：Java 生产级实现，含 **Read Index / Lease Read / 日志压缩 / 成员变更**完整矩阵。
  - `baidu/braft`（**4227★**）：C++ 实现，配合 `apache/brpc`（**17620★**）使用。
  - `tikv/tikv`（**16878★**）：Multi-Raft 分组 + PD 调度，是「Raft 如何支撑 PB 级数据」的最佳样本。
  - `hashicorp/consul`（**30085★**）：Raft 用于服务目录 + Serf（Gossip）用于成员/故障检测的**混合架构**。
- **Jepsen 实测**（`jepsen-io/jepsen`，**7504★**）：etcd 与 Consul 均有专项报告。
  共识层本身安全性良好，报告的典型问题集中在**读路径、会话/锁语义与时钟假设**上——正好对应本章 4.4。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「拿到多数派选票就能当 Leader」 | 还必须**日志足够新**；否则会把已提交日志丢掉 |
| 2 | 「Leader 提交了 = 客户端可见」 | 必须等 `commitIndex` 被**本地状态机 apply** 后才能读；否则读到旧状态 |
| 3 | 「成员变更一次改多个节点更快」 | 单节点变更靠「新旧多数派必相交」保证安全；一次改多个会破坏该性质 |
| 4 | 「Raft 读 Leader 就是线性一致」 | **不成立**。旧 Leader 在分区后仍会自认为 Leader；需 Read Index 等机制 |
| 5 | 🔧 2026 补丁：Lease Read 的时钟依赖要讲清 | 本书 4.4 提到与一致性相关的问题，但若读者直接上 Lease Read，须知它**依赖时钟漂移上界**。etcd 默认 Read Index；braft/SOFAJRaft 的 lease read 也要求配置时钟漂移阈值。云环境 VM 暂停会造成严重时钟跳变 |
| 6 | 🔧 2026 补丁：未涉及 Multi-Raft 分组 | 单组 Raft 无法水平扩展数据容量。2026 年标准做法是**按 range 分多组**（TiKV/CockroachDB），并配 PD/调度器做 rebalance 与成员变更编排。本书 4.3 只讲单组成员变更 |
| 7 | 🔧 2026 补丁：Leader 租约 vs 客户端租约要分清 | 本书讲 Raft 时没有区分**「Raft 内部的 Leader 租约」**与**「etcd 给客户端用的 lease（TTL key）」**。后者不是共识机制，而是服务端 TTL + 续租；用客户端 lease 实现分布式锁在 etcd 里是可行的，但**不能等价于 Redlock 类客户端锁**。详见 [12-Hashicorp-Raft与分布式KV系统实战](12-Hashicorp-Raft与分布式KV系统实战.md) |
| 8 | 🔧 2026 补丁：缺少 Jepsen 视角 | 本书按「算法应该正确」讲，但 2026 年的正确做法是**用 Jepsen/故障注入实测**。SOFAJRaft 与 etcd 都内置混沌测试；只靠「读论文觉得对」在生产上是不够的 |

## 与其他章 / 其他书的联系

- **本目录内**：
  - 本章与 [02-Paxos与Multi-Paxos](02-Paxos与Multi-Paxos.md) 是同一问题的两种解法，建议**对照读**；
  - 本章 4.2 的「顺序性」由 Raft 天然保证，而 [05-ZAB协议与ZooKeeper](05-ZAB协议与ZooKeeper.md) 6.1.1 会告诉你「为什么 Multi-Paxos 保证不了」；
  - 本章的代码落地在 [12-Hashicorp-Raft与分布式KV系统实战](12-Hashicorp-Raft与分布式KV系统实战.md)；
  - 本章 4.3 的成员变更在 [11-InfluxDB企业版一致性实现剖析](11-InfluxDB企业版一致性实现剖析.md) 里有真实系统的对应物。
- **跨书**：
  - [../深入理解分布式共识算法/07-Raft.md](../深入理解分布式共识算法/07-Raft.md)——Raft 论文的逐节重述，本章的工程化补充；
  - [../深入理解分布式共识算法/08-Raft工程实践与SOFAJRaft.md](../深入理解分布式共识算法/08-Raft工程实践与SOFAJRaft.md)——**五种读方案 + Parallel Raft + 源码**，是本章 4.4 的直接延伸；
  - [../深入理解分布式系统/07-Raft与拜占庭容错.md](../深入理解分布式系统/07-Raft与拜占庭容错.md)——Raft + BFT 并列视角；
  - [../分布式算法/06-网络共识与选举.md](../分布式算法/06-网络共识与选举.md)——选举的算法级形式化；
  - [../分布式数据库入门进阶与实战/09-共识算法.md](../分布式数据库入门进阶与实战/09-共识算法.md)——数据库视角的 Raft/Paxos 用法；
  - [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)——判断何时该用 Raft、何时用 Quorum NWR。
