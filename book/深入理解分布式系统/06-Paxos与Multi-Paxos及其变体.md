# 第 4 章（中） Paxos、Multi-Paxos 及其变体

> 本章笔记覆盖原书 **第 4 章 4.4 Paxos、4.5 Go 语言实现 Paxos 实验、4.6 Multi-Paxos、4.7 其他 Paxos 变体**。
> 共识的定义与 FLP 在 [05-共识的地基与不可能定理.md](05-共识的地基与不可能定理.md)，
> Raft 与拜占庭容错在 [07-Raft与拜占庭容错.md](07-Raft与拜占庭容错.md)。
> **本章地图**：从「一次只能决定一个值」的 Basic Paxos，一路走到「决定一个无限长日志」的 Multi-Paxos，
> 再由七个变体说明：**同一个 safety 内核，可以在不同场景下用不同的 quorum / leader 策略重排。**

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 4.4.1 基本概念 | Proposer / Acceptor / Learner；提案号（ballot）；多数派 quorum | Paxos 的角色划分决定了它「看起来复杂」：每个角色只做很少的事 |
| 4.4.2 问题描述 | 选择一个值，并保证后续不会被推翻 | 核心是 **P2c**：被选中的值必须在更大的提案里被「追认」 |
| 4.4.3 算法流程 | Prepare/Promise（阶段一）+ Accept/Accepted（阶段二） | 阶段一「占坑并发誓」，阶段二「用誓言守住已有选择」 |
| 4.4.4 案例 | 两个提案者竞争、旧提案失效但仍安全的执行轨迹 | 安全性来源于「先知期（promise）」，不是来源于「谁更强」 |
| 4.4.5 活锁 | 两个提案者交替打断 ⇒ 无人能被选中 | 工程解法：选出一个稳定的 leader（distinguished proposer） |
| 4.5 实验：Go 实现 Paxos | 结构体、消息、流程、学习提案、单元测试 | **本书最有价值的章节之一**：从零写一遍能暴露所有纸面推导的省略处 |
| 4.6 Multi-Paxos | 日志索引、leader 选举、减少 Prepare、副本完整性、配置变更 | Multi-Paxos = Basic Paxos + 稳态 leader + 跳过 Prepare 的优化 |
| 4.7 Paxos 变体 | Disk / Cheap / Fast / Mencius / EPaxos / Flexible / WPaxos / CASPaxos | 变体只改三件事：**谁是 leader、quorum 怎么交叉、几轮往返** |

## 核心精讲

### 4.4.2–4.4.3 Basic Paxos：两个阶段与一条关键的证明线

**角色**

| 角色 | 职责 |
| --- | --- |
| Proposer（提案者） | 提出 ⟨提案号 n, 值 v⟩，负责推动两个阶段 |
| Acceptor（接受者） | 对提案做出 promise 或 accept，是「 quorum 的原子不可回滚单位」 |
| Learner（学习者） | 读取被选定的值（多数实现里角色由 Proposer 顺带承担） |

**阶段一（Prepare / Promise）**：Proposer(n) → 全体 Acceptor

- Acceptor 若 `n > minProposal` 则承诺：① 不再接受号小于 n 的提案；② 返回自己**已接受过的最大号提案**（若有）。

**阶段二（Accept / Accepted）**：

- Proposer 收到多数 Promise 后，必须选取「**Promise 返回值中提案号最大者**」的值（若所有返回都为空，则自选值 v）；
- 发送 Accept(n, v)；Acceptor 若 `n >= minProposal` 则接受并记录。

安全性真正的不变量（P2c）：

```text
P2c: 若 ⟨n, v⟩ 被提出，则存在一个多数派集合 S，使得：
     (a) S 中无人接受过号小于 n 的提案，或
     (b) v 是 S 中已接受的、号小于 n 的提案中号最大的那个提案的值。
```

P2c 是为什么 Paxos 能「追认旧值」的全部秘密：**一旦某个值被多数派接受，任何更大的提案都必须搬运这个值**，
因此不可能出现两个不同的值都「被选中」。

### 教学示意：Acceptor 的状态机

```go
// 教学示意，不参与构建
type Acceptor struct {
    minProposal int   // 已 promise 的最高提案号
    acceptedN   int   // 已接受提案的提案号，0 表示未接受
    acceptedV   string
}

// 阶段一：Prepare(n) → Promise
func (a *Acceptor) Prepare(n int) (promised bool, accN int, accV string) {
    if n > a.minProposal {
        a.minProposal = n                 // 誓言：不再接受更小号的提案
        return true, a.acceptedN, a.acceptedV
    }
    return false, a.acceptedN, a.acceptedV // 拒绝：已经有更大的提案被 promise
}

// 阶段二：Accept(n, v) → Accepted
func (a *Acceptor) Accept(n int, v string) bool {
    if n >= a.minProposal {
        a.acceptedN, a.acceptedV = n, v
        return true
    }
    return false
}

// Proposer 侧：从多数派的 Promise 中「挑出可能被选定的值」
func pickValue(promises []Promise) string {
    best, bestV := -1, ""
    for _, p := range promises {
        if p.AccN > best {
            best, bestV = p.AccN, p.AccV
        }
    }
    return bestV // 为空则调用方可自选提议值
}
```

三处最容易写错的地方（本书 4.5 的小节正是在教这个）：

1. **`minProposal` 必须持久化**：崩溃重起后忘记誓言 ⇒ 可能接受旧提案 ⇒ 破坏安全；
2. **阶段二必须用 `>=` 而不是 `>`**（对自己刚 promise 的同一提案号要保持接受）；
3. **Promise 返回值必须带「已接受的提案」**，否则 Proposer 会用新值覆盖一个可能已被选定的旧值。

### 4.4.5 活锁与 Leader

两个 Proposer 交替提升提案号，互相在对方的阶段二之前插入新的 Prepare ⇒ 谁也选不上。
这是**活性**问题而非安全问题：算法永不选错值，只是可能选不出来。

本书在这之后的解法与工程一致：**选出一个 leader（distinguished proposer）**，
只有 leader 提议；leader 更换时再由新 leader 用大提案号重新走一轮 Prepare 补齐日志。

### 4.6 Multi-Paxos：从「选一个值」到「复制一个日志」

| 机制 | 说明 |
| --- | --- |
| 日志索引 | 每个日志槽位 i 跑一次独立的 Paxos 实例（Instance per index） |
| leader 选举 | 稳态只有一个 leader，负责所有槽位的提案 |
| 减少请求 | leader 稳定后**跳过 Prepare 阶段**（在一个任期内， quorum 的 promise 可以被「继承」），每次写只需一轮 RTT |
| 副本完整性 | 新 leader 要为每一个未确认的槽位补跑 Prepare，回填可能已选定的值 |
| 客户端协议 | 请求带 clientId + 序列号去重；只有 leader 能响应写 |
| 配置变更 | 成员变化时 quorum 定义会变 ⇒ 必须与日志槽位绑定（α 到 α+k 期间新旧 quorum 同时满足） |

```text
稳态一次写：client → leader → (Accept 广播) → 多数派 ACK → 提交 → 应用状态机 → 回 client
                              ↑ 一轮 RTT（Prepare 已被省略）
```

**新 leader 的代价（最容易忽略的一节）**：它不是「从最新 position 接手」，
而是要保证对于**每一个**槽位，要么知道自己上任时被选定的值，要么补齐它。
这就是为什么 Multi-Paxos 的实现里总有 `no-op` specific entries 或显式的「补齐」步骤。

### 4.7 变体速查

| 变体 | 改了什么 | 适用场景 |
| --- | --- | --- |
| Disk Paxos | Acceptor 用共享磁盘而非持久化本地状态 | 有共享存储的一组「无状态 acceptor」 |
| Cheap Paxos | 用少量辅助（auxiliary）节点代替 f+1 个全量副本 | 降低从节点成本，牺牲容错度换取成本 |
| Fast Paxos | 允许 Proposer 直接让 Acceptor 接收值，一轮搞定 | 冲突少时延迟减半；冲突时退化并需要更大 quorum |
| Mencius | 轮流坐庄（每个槽位有一个默认 leader） | WAN 下避免每次都跨地域访问同一个 leader |
| EPaxos | 无 leader，只在冲突时排序；依赖的依赖跟踪 | 广域多主、冲突稀疏的写负载 |
| Flexible Paxos | 放松「阶段一与阶段二 quorum 必须都是多数派」的经典假设 | 提升**写的 quorum**可以**减小阶段一 quorum**；反过来不可 |
| WPaxos | 把「(object group) 的 quorum」与「leader locality」解耦 | 多区域但每个对象有明确归属区域 |
| CASPaxos | 不复制日志，直接对寄存器做 CAS 式的共识 | 需要 key-value 语义而不必复制全部历史时 |

## 版本演进

- 本书 2022 年第一版，本章内容属于「2000 年代就基本定稿」的经典；
  **2022 → 2026 的变化全部发生在工程落地层面**：
  - **KRaft 取代 ZooKeeper**：Apache Kafka 的元数据面从「外部协调服务」改成「自身把 Raft 用于元数据」，
    KIP-500 方向上自 Kafka 3.3（2022）起始标记为生产可用，后续版本在完成去 ZooKeeper 化。
    这是「本书出版时正发生、2026 已成定局」的最大变化。
  - **Multi-Raft 成为存储层常态**：TiKV/CockroachDB 一系把 consensus group 按 Range 切分，
    每个 Range 一套 Paxos/Raft 实例，由中心调度器管理成员与迁移。
  - **可嵌入库成熟**：etcd-io/raft、HashiCorp Raft 让「不必自己写共识」成为默认选择；
    本书 4.5 的「从零写一个 Paxos」在今天更像一次**价值极高的教学练习**，而不是生产路径。
  - **形式化验证常态化**：TLA+/P 与 Jepsen 成为发布前的门槛，而不是论文附带的证明。
- **本书特有的处理**：4.5 节的 Go 实现 + 单元测试是同类书里少见的「手写能跑的最小 Paxos」。
  阅读时建议把它与 [07-Raft与拜占庭容错.md](07-Raft与拜占庭容错.md) 的 Raft 工程清单对照，观察两者的取数差别。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Lamport《The Part-Time Parliament》 | ACM TOCS 1998 | Paxos 的原始发表（希腊议会寓言） |
| Lamport《Paxos Made Simple》 | ACM SIGACT News 2001 | 去掉寓言、只留算法的标准版本 |
| Chandra, Griesemer, Redstone《Paxos Made Live – An Engineering Perspective》 | PODC 2007 | 从论文到 Chubby 之间「全部没写在论文里的改动」 |
| van Renesse & Altinbuken《Paxos Made Moderately Complex》 | ACM Computing Surveys 2015 | Multi-Paxos 完整实现的现代教程 |
| Gray & Lamport《Consensus on Transaction Commit》 | ACM TOCS 2006 | Paxos Commit（本书 5.2.3 的理论来源） |
| Gafni & Lamport《Disk Paxos》 | Distributed Computing 2003 | 用共享磁盘作为 acceptor 存储 |
| Lamport & Massa《Cheap Paxos》 | DSN 2004 | 用辅助节点降低成本 |
| Lamport《Fast Paxos》 | Distributed Computing 2006 | 一轮提交与冲突退化 |
| Mao, Junqueira, Marzullo《Mencius: Building Efficient Replicated State Machines for WANs》 | OSDI 2008 | 轮换 leader 的 WAN 优化 |
| Moraru, Andersen, Kaminsky《There Is More Consensus in Egalitarian Parliaments》 | SOSP 2013 | **EPaxos**：leaderless、投机执行、冲突排序 |
| Howard, Malkhi, Spiegelman《Flexible Paxos: Quorum Intersection Revisited》 | OPODIS 2016 | 经典 quorum 假设的放松与重新表述 |
| Ailijiang & Demirbas《WPaxos: Ruling the Archipelago with Fast Consensus》 | arXiv，2017 | 对象归属 + 多区域 fast path |
| Rystsov《CASPaxos: Replicated State Machines without logs》 | arXiv，2018 | 基于 CAS 的寄存器式共识 |
| Junqueira, Reed, Serafini《Zab: High-performance broadcast for primary-backup systems》 | DSN 2011 | ZooKeeper 使用的主序广播协议（常与 Paxos 对照） |

> 说明：上表中 arXiv 条目为预印本；本目录只陈述其存在与年份，不对其后续正式发表情况做断言。

## 近年研究与工业界开源实践（2015–2026）

- **研究与评测**：近年最有实用价值的工作是 **Flexible Paxos**（改变了 quorum 默认是「多数派」的心智，
  使得「写 quorum 与阶段一 quorum 可以不同规模」成为调优手段）与 **leaderless 路线的工程评测**
  （EPaxos 在真负载下的表现依赖冲突率）。
- **共识「不再手写」**：共识库与托管服务成为常态，2026 年一个新的存储系统通常是**选一个共识库并把它用对**。
- **Multi-Raft**：这是 2015 年后最大的形态变化，也带来新问题：跨 Range 事务、跨组成员变更、成员分布与 lease 协同。
- **工业界开源**（star 数均为 2026-09-26 用 `gh api repos/OWNER/REPO --jq '.stargazers_count'` 实测）：

| 项目 | star | 与本章的对应 |
| --- | --- | --- |
| `etcd-io/raft` | 1128 | Raft 的 Go 参考实现；大量项目内嵌它做 Multi-Raft 组 |
| `hashicorp/raft` | 9136 | 另一条被广泛采用的共识库，Consul/Nomad 系的基础 |
| `apache/zookeeper` | 12811 | Zab 的经典实现；与 Multi-Paxos 的对比样本 |
| `apache/kafka` | 33847 | KRaft：把元数据面从外部协调服务搬进自身的 Raft 组 |
| `tikv/tikv` | 16877 | Range 级 Multi-Raft；把本章的「日志复制」放大一万倍 |
| `apple/foundationdb` | 16731 | 自主实现的 Paxos 系副本（含日志角色分离），并用确定性模拟测试验证 |

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Paxos 一次只能决定一个值」 | Basic Paxos 是一个实例；Multi-Paxos 用「每槽一个实例 + 稳态 leader」来复制日志 |
| 2 | 「每次写都要走两阶段」 | leader 稳定后，阶段一的 promise 可以在整个任期内复用，稳态写是一轮 RTT |
| 3 | 「提案号相同也没关系」 | 提案号必须全局全序且可比较（通常 `(round, serverId)`），否则誓言无法区分先后 |
| 4 | 「Acceptor 可以不持久化」 | crash-recovery 下忘记 `minProposal`/`acceptedN,V` 就会破坏安全（本书 4.5 的代码也正是要持久化） |
| 5 | 「Proposer 在二阶段可以选自己喜欢的值」 | 若 Promise 返回中已有被接受的值，必须用**号最大者**的值，否则可能推翻一个已选定的值 |
| 6 | 「活锁说明 Paxos 不安全」 | 活锁是活性问题：不会出现两个不同的值，只是可能一直不终止；解法是 leader + 随机退避 |
| 7 | 「Flexible Paxos 说 quorum 不用交叉」 | 它放松的是**「两个阶段都必须是多数派」的对称性**：两阶段的 quorum **仍然必须相交** |
| 8 | 「Fast Paxos 一定更快」 | 它在高冲突下会退化且需要更大的 quorum，实际收益取决于冲突率 |
| 9 | 🔧 本书 4.5 的 Go 实验给的是「最小可运行」，但不构成生产实现 | 2026 的现实：生产路径是**选一个成熟共识库**并做正确的集成；本书实验的价值是教学而不是工程输出。补齐参考清单：只读查询的线性一致读（readIndex / lease read）、
  快照与日志压缩、成员变更、以及网络丢包/重复/乱序与磁盘故障注入，都在此次最小实验的覆盖之外 |
| 10 | 🔧 本书未把 **Multi-Raft** 作为工程主线来讲 | 2026 的现实：绝大多数生产系统运行的并不是「一个集群一个共识组」，而是**成千上万个共识组**，每个组独立选主/迁移/平衡。本书以「一个集群一个组」为主，读者需要自己把「跨组」这一层补上 |
| 11 | 🔧 本书对 **KRaft / Zab 的现代定位**只能在 2022 年的语境下理解 | 2026 的现实：Kafka 已完成去 ZooKeeper 化的过程；ZooKeeper 在新系统里的份额下降。读本书这一节时应把「ZooKeeper 是元数据面标配」视为 2022 年的陈述 |
| 12 | 🔧 本书缺少 **形式化/故障注入验证**这一节 | 2026 的现实：Paxos/Raft 实现默认要过 TLA+ 建模或 Jepsen 式随机故障测试；
  只有覆盖了消息丢失/重复/乱序与磁盘故障的注入测试，才算「实现完成」 |

## 与其他章 / 其他书的联系

**本目录内**

- [05-共识的地基与不可能定理.md](05-共识的地基与不可能定理.md)：本章的 leader 与随机退避正是对那里 FLP/◊P 的工程回应。
- [07-Raft与拜占庭容错.md](07-Raft与拜占庭容错.md)：Multi-Paxos 与 Raft 的对照；4.9 节「Paxos vs Raft」就在那里讨论。
- [08-分布式事务.md](08-分布式事务.md)：Paxos Commit（5.2.3）直接用本章的 prepare/accept 做提交决定。
- [10-案例研究文件系统与协调服务.md](10-案例研究文件系统与协调服务.md)：ZooKeeper（Zab）是 Multi-Paxos 之外的另一条主序路线。
- [11-案例研究分布式存储与数据库.md](11-案例研究分布式存储与数据库.md)：Spanner 的 Paxos 组、Cassandra 的 Paxos LWT。

**跨书互链**

- [../深入理解分布式共识算法.md](../深入理解分布式共识算法.md)：Paxos 变体谱系与推导的专门笔记。
- [../分布式系统/08-容错.md](../分布式系统/08-容错.md)：教科书对 Paxos/Raft 的定位与用途说明。
- [../分布式系统概念与设计/10-协调与协定.md](../分布式系统概念与设计/10-协调与协定.md)：同样的 consensus 定义和容错美度。
- [../分布式数据库入门进阶与实战/09-共识算法.md](../分布式数据库入门进阶与实战/09-共识算法.md)：工程书对同一批算法的取舍语言。
- [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)：何时用共识、何时用无主 quorum。
