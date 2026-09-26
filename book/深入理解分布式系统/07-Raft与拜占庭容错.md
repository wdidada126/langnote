# 第 4 章（下） Raft 与拜占庭容错

> 本章笔记覆盖原书 **第 4 章 4.8 Raft 算法、4.9 Paxos vs Raft、4.10 拜占庭容错和 PBFT 算法、4.11 小结**。
> Paxos 家族见 [06-Paxos与Multi-Paxos及其变体.md](06-Paxos与Multi-Paxos及其变体.md)。
> **本章地图**：Raft 是「为了让人看懂并写对」而重新设计的共识算法：**子问题分解**（leader election / log replication / safety）
> + 强 leader，使正确性可以被五条不变量说完。最后把它与 Paxos 对照，并跨到节点会作恶的世界（PBFT）。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 4.8.1 系统模型 | 服务器为状态机；持久化日志 + 持久化{currentTerm, votedFor}；commitIndex、lastApplied | 「持久化什么」决定 crash-recovery 下是否安全；Raft 把它说得很死 |
| 4.8.2 基本概念 | Leader/Follower/Candidate、任期（term）、日志项（term + index + cmd） | 任期号是全局逻辑时钟，也是拒绝过期 leader 的唯一手段 |
| 4.8.3 领导者选举 | 心跳、选举超时随机化、RequestVote 的两条投票条件、投票持久化 | 随机化退避是 Raft 绕开 FLP 的具体做法 |
| 4.8.4 日志复制 | AppendEntries 一致性检查（prevLogIndex/prevLogTerm）、多数派后提交 | 「日志匹配特性」让回溯只需退 nextIndex |
| 4.8.5–4.8.6 领导者更替 | 新 leader 必须拥有全部已提交日志（up-to-date 检查） | 选举限制 = Raft 安全性的一半：不是「最新当选」而是「日志最全才可能被选」 |
| 4.8.7 延迟提交前任日志 | 只用当前 term 的多数派复位 commitIndex | 这是论文 Figure 8 讲的坑：直接用 replica 计数提交前任日志会丢已提交数据 |
| 4.8.8 清理不一致日志 | follower 冲突日志被覆盖；nextIndex 回退（可带优化） | 「以 leader 为准」让不一致的收敛非常简单，代价是 leader 要能删 follower 的日志 |
| 4.8.9 处理旧领导者 | 任期号比较 ⇒ 立即降级为 follower | 网络分区恢复时靠 term 把「僵尸 leader」一次性杀掉 |
| 4.8.10–4.8.11 客户端协议与线性一致 | 请求去重（clientId + seq）、只读 optimized path（readIndex / leader lease） | 只读如果不特殊处理，可能在新 leader 刚上任时返回陈旧值 |
| 4.8.12–4.8.13 配置变更 | joint consensus（C_old,new 阶段）及其 Bug | 成员变更是 Raft 里最容易写错的部分；必须走日志、必须避免双 leader 多数派 |
| 4.8.14 极端的活性问题 | 成员/日志进度不均导致的反复选举；被隔离节点不断发起选举打乱集群 | 论文之后的实现补丁（PreVote / CheckQuorum）都是为**活性**加的，不是为安全 |
| 4.8.15–4.8.18 日志压缩与性能优化 | 快照（内存状态机 vs 磁盘状态机）、InstallSnapshot、流水线/批处理/并行 | 工程化的大头：快照 + 异步 apply + batch disk write |
| 4.9 Paxos vs Raft | 强 leader vs 多提案者；可理解性；提交规则 | 两者同宗；差别在「怎么让工程实现真的写对」 |
| 4.10 PBFT | 三阶段（pre-prepare/prepare/commit）、视图更替、f < n/3 | 拜占庭世界里 leader 也可能撒谎，因此需要「多一轮确认 + 视图变更」 |

## 核心精讲

### 4.8.2–4.8.4 Raft 的五条核心不变量

| 性质 | 表述 |
| --- | --- |
| Election Safety | 任一 term 内最多一个 leader |
| Leader Append-Only | leader 只追加，不删改自己的日志 |
| Log Matching | 两日志若在 (index, term) 相同，则其之前所有项完全相同 |
| Leader Completeness | 若某日志项在某 term 被提交，则之后所有 leader 的日志里都有它 |
| State Machine Safety | 任一服务器 apply 到某个 index 的内容，与其他服务器在该 index 的内容相同 |

### 教学示意：AppendEntries 的一致性检查

```go
// 教学示意，不参与构建
type AppendEntries struct {
    Term         int
    PrevLogIndex int
    PrevLogTerm  int
    Entries      []Entry
    LeaderCommit int
}

func (r *RaftNode) handleAppend(a AppendEntries) bool {
    if a.Term < r.currentTerm {
        return false // 旧 leader：拒绝（4.8.9）
    }
    r.stepDownToFollower(a.Term)
    r.resetElectionTimer()

    // 一致性检查：本地必须已有 PrevLogIndex 且 term 相同
    if a.PrevLogIndex >= len(r.log) ||
        (a.PrevLogIndex >= 0 && r.log[a.PrevLogIndex].Term != a.PrevLogTerm) {
        return false // 触发 leader 递减 nextIndex（4.8.8）
    }
    // 截断冲突部分后追加
    r.log = append(r.log[:a.PrevLogIndex+1], a.Entries...)

    if a.LeaderCommit > r.commitIndex {
        // 提交：只能推进到「本地已存在的最后一项」与 leaderCommit 的较小值
        r.commitIndex = min(a.LeaderCommit, len(r.log)-1)
    }
    return true
}
```

**Leader 侧提交规则（论文里的关键例外）**：

```go
// 教学示意，不参与构建
func (r *RaftNode) advanceCommitIndex(acked int) {
    // 只能直接用 replica 计数提交「当前任期」的日志项
    if r.log[acked].Term != r.currentTerm {
        return // 前任的日志项只能由后续「当前任期的提交」顺带推进
    }
    if majorityReplicated(acked) {
        r.commitIndex = acked
    }
}
```

### 4.8.7 为什么不能直接用副本数提交前任日志（论文 Figure 8）

场景：leader S1 把 ⟨term 2, index 2⟩ 复制到多数派（含 S3）后崩溃；
若允许「用副本计数提交前任日志」，S5 可能通过 term 3 当选并覆盖 index 2 —— 于是已被 S1 认为提交的项丢失。
Raft 的做法是：**leader 只在自己任期内的日志项达到多数派时才直接推进 commitIndex**，
前任留下的日志项随之后一项的提交而「顺带」被提交。

> 补充一点文献事实：Raft 论文发表后有讨论（如 Howard & Mortier《Raft Refloated》，SIGOPS OSR 2016）
> 指出这个「延迟」不是唯一的修法——另一种做法是保证新 leader 上任时知道前任最后一条日志的提交状态。
> 本书沿用的是论文原文的做法。

### 4.8.12–4.8.13 成员变更与它的坑

- **joint consensus**：先切换到 `C_old,new`（此时选举与提交都需要**同时得到两边的多数派**），
  再切换到 `C_new`，期间成员可以在两 config 中自由切换而不破坏安全性；
- **单节点变更**：在只允许一次增删一个节点的约束下可以省掉联合协商，
  但论文后续也承认：若引入一次性加入多个节点，或者把成员变更与其他日志交错处理不当，会产生多数派不交叉的窗口；
- **必须注意的另一个坑**：成员变更项本身也是日志项，
  因此也要受「多数派」约束；把 config 当成「单独的配置项存在另一处」的实现通常是错的。

### 4.10 PBFT：把「错误假设」升级为「节点会撒谎」

PBFT 的三阶段：

```text
client → primary(request)
primary → backups(pre-prepare: seq + view + digest)
backups ↔ backups(prepare: 同意序号)
backups ↔ all(commit: 确认已收到足够 prepare)
all → client(reply: 收到 f+1 条匹配回复则接受)
```

两关键点：

1. **为什么需要 prepare 阶段**：保证在同一 view 内，所有正常副本对一个请求的**序号**达成一致（即使主节点作恶）；
2. **为什么要收到 f+1 条回复就接受**：保证至少有一个正常副本已经持久化了结果，后续试图改变会被发现。

**视图更替（view change）**：当副本怀疑 primary 作恶或超时，就广播 VIEW-CHANGE 并收集 2f+1 条以组成 NEW-VIEW 证明；
PBFT 用其中的 **P / Q 集合**保证「已被客户端接受的请求」不会在新视图里被丢失。

## 版本演进

- 本书 2022 年第一版。Raft 论文发表于 2014，PBFT 于 1999；本节的理论部分在 2026 年无需任何修订。
- **2022 → 2026 的现实变化**：
  - **共识组数量爆炸**：Multi-Raft 成为存储层标准形态（TiKV/CockroachDB），
    本书描述的「一个集群一个组」在今天很像单 Range 的内部视角。
  - **成员/角色扩展**：工程实现增加了论文没写的角色与机制（Learner/Witness/CheckQuorum/PreVote），
    这些是从**活性与运维**角度加的，不是新算法。
  - **BFT 的重新民用化**：permissioned/permissionless 链让 PBFT 一系（PBFT → Tendermint → HotStuff）
    成为「日常能被部署的东西」；HotStuff 的线性视图更替简化了 PBFT 最复杂的部分。
  - **Kafka KRaft**：把 ZooKeeper 依赖去掉后，Raft 进入了「消息系统元数据」这一新的主力场景。
- **本书的处理特点**：4.8 是全书最细的章节（19 个小节），几乎逐条对应 Raft 论文的 Section；
  这使得本书在这一节的可稿性非常高，也是本目录唯一几乎不需要修正的一节——除了下面几条工程补丁。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | **Raft 论文**，本书 4.8 的唯一正式来源 |
| Ongaro《Consensus: Bridging Theory and Practice》 | Stanford 博士学位论文，2014 | 论文的扩展版：配置变更的坑、活性问题的补充讨论 |
| Howard & Mortier《Raft Refloated: Do We Have Consensus?》 | ACM SIGOPS Operating Systems Review，2016 | 对 Raft 论文的评述与若干可选修法 |
> 说明：本表只保留能确认会议/期刊/年份的文献；出处无法确认的条目不列入，不做填补。
| Castro & Liskov《Practical Byzantine Fault Tolerance》 | OSDI 1999 | PBFT，本书 4.10 的来源 |
| Castro & Liskov《Practical Byzantine Fault Tolerance and Proactive Recovery》 | ACM TOCS 2002 | 加入主动恢复与更完整的证明 |
| Kotla, Alvisi, Dahlin, Clement, Wong《Zyzzyva: Speculative Byzantine Fault Tolerance》 | SOSP 2007 | 投机执行降低 BFT 延迟 |
| Yin, Malkhi, Reiter, Gueta, Abraham《HotStuff: BFT Consensus with Linearity and Responsiveness》 | PODC 2019 | 线性视图更替；后续被 Libra/Diem 一系采用 |
| Buchman《Tendermint: Byzantine Fault Tolerance in the Age of Blockchains》 | 硕士学位论文，University of Guelph，2016 | 部分同步下的轮次 BFT |
| Nakamoto《Bitcoin: A Peer-to-Peer Electronic Cash System》 | 白皮书，2008 | 开放成员下的随机化（PoW）路线 |
| Lamport, Shostak, Pease《The Byzantine Generals Problem》 | ACM TOPLAS 1982 | 3f+1 下界的出处 |

> 说明：本表只保留能确认会议/期刊/年份的文献；无法确认出处的条目已显式标注不列入，不做填补。

## 近年研究与工业界开源实践（2015–2026）

- **研究**：近年有价值的方向是 **Raft 的工程边界**——Leader Lease 与 readIndex 的正确性边界、
  日志压缩/快照在磁盘状态机上的处理，以及成员角色的扩展（Learner / Witness 等非投票角色）。
  另一条线是 **BFT 的工程化简化**（HotStuff 之后的一批改进）。
- **工程**：Raft 库化已经完成；2026 年新系统更多是在**用好一个库**（何时做快照、如何给 Learner 布置、
  如何限速、如何处理跨组分片），而不是从头实现。
- **工业界开源**（star 数均为 2026-09-26 用 `gh api repos/OWNER/REPO --jq '.stargazers_count'` 实测）：

| 项目 | star | 与本章的对应 |
| --- | --- | --- |
| `etcd-io/raft` | 1128 | Raft 参考实现；论文之外的 PreVote / CheckQuorum / 租约读等扩展在此可见 |
| `hashicorp/raft` | 9136 | 另一主流 Raft 库，快照/单节点变更的实践参考 |
| `etcd-io/etcd` | 52310 | 默认线性一致读；其 `readIndex` 与 leader lease 的实现是最常被引用的样本 |
| `tikv/tikv` | 16877 | Multi-Raft 的代表把本章的「一个组」放大到 Range 级大量组 |
| `pingcap/tidb` | 40589 | PD + TiKV：组内共识 + 跨组的在线调度与事务 |
| `apache/kafka` | 33847 | KRaft：用 Raft 承载元数据面，替代外部协调服务 |
| `cockroachdb/cockroach` | 32508 | Raft 组 + Range 迁移 + 追随者读/租约读多种读路径 |

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Raft 只需要理解 term 就够了」 | 关键是**五条不变量**；term 只是实现手段 |
| 2 | 「日志项的提交可以直接按副本计数推进」 | 只有当前任期的日志项可以这样做；这是论文 Figure 8 的核心警示 |
| 3 | 「follower 日志与 leader 不一致时应该让 follower 保存」 | 以 leader 为准覆盖（由 Log Matching 保证安全） |
| 4 | 「leader 收到多数派响应就可以返回结果」 | 必须先更新 commitIndex（并等到它被 apply），否则读不到自己刚写的 |
| 5 | 「Raft 的 leader 读天然线性一致」 | 不一定：网络分区后旧 leader 可能还以为自己是 leader。必须走 **readIndex / leader lease**，或者干脆走日志 |
| 6 | 「成员变更只是改一下配置」 | 必须作为日志项提交、必须避免新旧多数派不交叉； joint consensus 或受约束的单节点变更是仅有的规范做法 |
| 7 | 「PBFT 的 prepare 阶段可省」 | 省掉就不能保证同 view 内序号一致；这是主节点作恶的情形下的关键一步 |
| 8 | 「PBFT 也要 f+1 轮换」 | PBFT 常态为三阶段；**视图更替**才是代价最大的部分（HotStuff 的改进点正在这里） |
| 9 | 「BFT 只需要 2f+1」 | 拜占庭需要 **3f+1**；2f+1 只在非拜占庭（crash）模型下成立 |
| 10 | 🔧 本书按论文讲配置变更，但缺少今天的**工程补丁**清单 | 2026 的现实：生产实现（如 etcd）额外提供 **PreVote**（避免网络隔离节点反复发起选举打乱集群）、**CheckQuorum**（leader 若失去多数派心跳主动降级）、**Learner 角色**（新副本先追数据再参与投票）。这些都不是为了安全，而是为了**活性与运维** |
| 11 | 🔧 本书以「一个共识组」为视角，未讨论 Multi-Raft | 2026 的现实：一个集群往往有成千上万个 Raft 组，每个组独立选举与快照；此时真正的难题变成 **组级别的均衡、成员分布、心跳放大、以及跨组事务**。本书读者要把「组 × N」这一层自己补上 |
| 12 | 🔧 本书未覆盖 **Raft 库化后的集成陷阱** | 2026 的现实：正确地「用」一个 raft 库包括——**先写 WAL 再向 raft 层返回成功**、异步 apply 必须保证持久化与 apply 的顺序分离、以及大 value 的处理（分块或外置存储）。这些比算法本身更容易出错 |
| 13 | 🔧 本书对 **BFT 的现代形态**只站在 1999 年 PBFT | 2026 的现实：HotStuff（PODC 2019）把视图更替线性化，Tendermint 把部分同步 BFT 产品化，更多的 permissioned 链把 PBFT 一系变成了「每天都在跑的东西」。读本节时应把 PBFT 当作这一族的起点而不是终点 |

## 与其他章 / 其他书的联系

**本目录内**

- [05-共识的地基与不可能定理.md](05-共识的地基与不可能定理.md)：随机选举超时 = 那里 4.2.4 随机化的落地。
- [06-Paxos与Multi-Paxos及其变体.md](06-Paxos与Multi-Paxos及其变体.md)：4.9 节 Paxos vs Raft 的直接对读对象。
- [10-案例研究文件系统与协调服务.md](10-案例研究文件系统与协调服务.md)：ZooKeeper/etcd 是对 Raft/Zab 的两种工程回答。
- [08-分布式事务.md](08-分布式事务.md)：跨多组分片的事务要在 Raft 之上再叠加 2PC（这也是 Multi-Raft 的现实形态）。

**跨书互链**

- [../深入理解分布式共识算法.md](../深入理解分布式共识算法.md)：Raft/Paxos 的完整推导谱系。
- [../MIT 6.824 Distributed Systems.md](../MIT 6.824 Distributed Systems.md)：6.824 的 Raft 实验（含 Figure 8 与 snapshot）是本节最好的动手材料。
- [../分布式系统/08-容错.md](../分布式系统/08-容错.md)：教科书对 Raft/Zab/提交的定位。
- [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)：「要不要共识 / 要几个副本」的决策视角。
- [../分布式数据库入门进阶与实战/09-共识算法.md](../分布式数据库入门进阶与实战/09-共识算法.md)：工程书对同一批算法的取舍语言。
