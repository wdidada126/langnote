# 第 06 讲 Fault Tolerance: Raft (1)：选举、日志复制与安全性

> 官方标题：**Fault Tolerance: Raft (1)**（LEC 6，主讲 fk）
> 指定必读：**Raft (extended) (2014)，读到 §5 结束**（即：Raft 核心协议，不含 §6 成员变更）
> 对应：**Lab 2: Raft**（2A 选举 / 2B 日志复制 / 2C 持久化）

## 本章地图

本讲是 Raft 正文的第一半，覆盖论文 §1–§5：

```
§1–§3  Raft 的基本机制：状态、任期、两个 RPC
§5.1   Raft 基础（三种状态、term、选举）
§5.2   领导选举（随机化超时、选举限制）
§5.3   日志复制（AppendEntries、一致性检查、提交）
§5.4   安全性（选举限制、提交上一任期条目的陷阱、安全性论证）
```

主线：为什么是「强领导」→ 任期如何当逻辑时钟 → 选举如何不分裂 → 日志如何保证一致 →
**为什么不能靠「数副本」提交上一任期的条目** → 安全性论证的形状。

## 核心精讲

### 6.1 强领导：Raft 的核心简化

- 日志**只从 leader 流向 follower**，follower 之间不互相复制；
- leader 决定「什么时候可以提交」，follower 只是被动接受 + 转发冲突信息；
- 代价：所有写都经过 leader，leader 成为吞吐瓶颈与故障切换点；
  收益：状态空间大幅减少，「谁说了算」永远是明确的。

### 6.2 三种状态与任期

| 状态 | 行为 |
| --- | --- |
| **follower** | 被动，只响应 RPC；超时未收到心跳则转为 candidate |
| **candidate** | 发起选举（自增 term、投自己、发 RequestVote） |
| **leader** | 定期发心跳（空的 AppendEntries）压制选举；处理客户端请求 |

**任期（term）** 是单调递增的逻辑时钟，用来「识别过期信息」：

- 每个 RPC 都带 term；收到**更高** term → 立即退回到 follower 并更新自己的 term；
- 收到**更低** term 的 RPC → 直接拒绝（对方已经过期）；
- 一个 term 内**最多**一个 leader（也可能一个都没有，即选举失败）。

### 6.3 领导选举

```
follower 的选举计时器超时（每个节点随机化，避免同时超时）
  → term++，转为 candidate，投自己一票
  → 并行向所有节点发 RequestVote(term, candidateId, lastLogIndex, lastLogTerm)
  → 三种结果：
     (a) 拿到多数票      → 成为 leader，立刻发心跳
     (b) 收到合法 leader 的 AppendEntries（term >= 自己）→ 退回 follower
     (c) 超时（没人拿到多数，分裂选举）→ 开启新一轮选举（term 再 ++）
```

**为什么必须随机化超时**：若所有节点同时超时，谁也拿不到多数，会反复分裂。
随机化让「某个节点先超时」成为高概率事件。论文给出的时间不等式是：

> 广播时间（broadcastTime） ≪ 选举超时（electionTimeout） ≪ 平均故障间隔（MTBF）

**选举限制（election restriction）** 是安全性的关键：

> 投票方只在「候选人的日志至少跟我一样新」时才投票。
> 比较规则：先比**最后一条日志的 term**，term 大的更新；term 相同则**索引更长**的更新。

这条保证了：**当选的 leader 一定持有所有已提交的日志条目**（Leader Completeness）。

### 6.4 日志复制

日志条目形如 `(term, index, command)`。流程：

1. client 请求 → leader 把命令追加到本地日志（未提交）；
2. leader 并行发 `AppendEntries(term, leaderId, prevLogIndex, prevLogTerm, entries[], leaderCommit)`；
3. follower 做**一致性检查**：若自己日志中 `prevLogIndex` 处的 term 与 `prevLogTerm` 不符 → 拒绝；
4. leader 收到多数成功 → **提交**（应用到状态机，回复 client）；
   leader 在后续的 AppendEntries/心跳里带上 `leaderCommit`，follower 据此提交自己的日志；
5. follower 拒绝 → leader 把该 follower 的 `nextIndex` **回退**并重试，直到找到匹配点，然后补齐后续日志。

**日志匹配性质（Log Matching Property）**：若两条日志在同一索引上条目相同（同 index 同 term），
则它们在此之前的所有条目都相同。它由「一致性检查 + 只由 leader 追加」归纳得出，
是 Raft 全部安全性论证的基石。

### 6.5 提交规则的陷阱（论文 Figure 8）

> **规则：Raft 绝不通过「数副本」来提交上一任期的日志条目；
> 只通过数副本来提交「当前任期」的条目。当前任期的条目一旦提交，
> 由日志匹配性质，它之前的所有条目也随之被间接提交。**

为什么？反例的形状：

```
(a) S1 是 term 2 的 leader，把条目复制到 S1、S2，还没提交就崩了
(b) S5 成为 term 3 的 leader（靠 S3、S4 的票），写了自己的条目，也崩了
(c) S1 重新成为 term 4 的 leader，继续复制 term 2 的那条到多数派
    —— 此时它在多数派上了，但 S1 不能就此认为它已提交！
(d) 若 S1 又崩了，S5 可能再次当选（它的日志在 term 3 更新），
    然后用自己 term 3 的条目覆盖掉那条 term 2 的条目 → 已「提交」的条目被改写
(e) 正确做法：S1 在 term 4 上任后先提交一条**当前任期**的条目，
    一旦成功，term 2 的那条才被间接确认
```

这条规则是 Lab 2 中最隐蔽的 bug 源：**只判断「多数派已复制」就推进 commitIndex 是不安全的**，
必须同时要求 `entries[i].Term == currentTerm`。

### 6.6 教学示意：选举与回退的判断逻辑

> **教学示意，不参与构建**——只给出判定条件，不构成可运行实现。

```go
// 教学示意，不参与构建

// 1) 是否给该候选人投票（§5.4.1 选举限制）
func shouldVote(myTerm, candTerm int, votedFor *int,
    candLastIdx, candLastTerm, myLastIdx, myLastTerm int) bool {

    if candTerm < myTerm {
        return false // 过期候选人
    }
    if candTerm == myTerm && votedFor != nil {
        return false // 本任期已投过
    }
    // 日志新鲜度：先比 term，再比 index
    if candLastTerm < myLastTerm {
        return false
    }
    if candLastTerm == myLastTerm && candLastIdx < myLastIdx {
        return false
    }
    return true
}

// 2) AppendEntries 的一致性检查（§5.3）
func consistencyCheck(log []Entry, prevIdx, prevTerm int) bool {
    if prevIdx >= len(log) {
        return false // 我根本没有这么长的日志
    }
    return log[prevIdx].Term == prevTerm
}

// 3) 提交条件（§5.4.2）：必须是「当前任期的条目」且已在多数派上
func canCommit(entry Term, matchCount, clusterSize, currentTerm int) bool {
    return entry == currentTerm && matchCount > clusterSize/2
}
```

> 这三段判断就是 Lab 2A/2B 的全部核心逻辑；剩下的都是「什么时候调用它们、用什么并发保护」的工程问题。
> 本目录只给判定条件，不给实现骨架。

### 6.7 安全性论证的形状（不写完整证明）

结论：**状态机安全性（State Machine Safety）**——任一索引上的条目一旦被提交，
后续任何 leader 在该索引上都是同一个条目。

论证骨架（反证法）：

1. 假设条目在 term T 被提交（即 T 的 leader 把它放到了多数派上）；
2. 假设之后某个 term U > T 的 leader 没有这条条目；
3. 由选举限制，该 leader 当选时必然有某个多数派的成员投了票，而这个成员一定持有该条目
   （因为两个多数派必有交集）；
4. 再由「日志只从 leader 流向 follower（leader 从不删除/覆盖自己的日志）」，
   推出该 leader 的日志必然包含该条目 → 矛盾。

## 版本演进

- **1998**：Paxos（Lamport，《The Part-Time Parliament》，TOCS 1998）；Paxos Made Simple 2001。
- **2014**：Raft 论文（USENIX ATC 2014）+ 扩展版（含成员变更、日志压缩、客户端交互）。
- **2014–2016**：大量实现出现：etcd/raft、Consul 的 hashicorp/raft、LogCabin 等；
  社区陆续发现并修正了论文未写清的工程细节（见 [07-容错Raft二.md](07-容错Raft二.md)）。
- **2020（本讲）**：课程把 Raft 讲两讲，并**明确跳过 §6（成员变更）**——
  但工程上它极其重要，本目录在 07 号文件补一节（会标注「非本讲指定阅读」）。
- **2026**：Raft 已是「共识的事实标准接口」：etcd/raft、hashicorp/raft、raft-rs、braft 等；
  研究焦点转向 WAN 下的延迟优化、无主共识，以及**如何验证实现正确**。

## 经典论文与原始文献

| 论文 | 出处 | 本讲为何读它 |
| --- | --- | --- |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm》（Raft extended） | **USENIX ATC 2014** | L6 **指定必读：§1–§5**（课程站点 `raft-extended.pdf`，另有 raft-faq） |
| （背景）Lamport《The Part-Time Parliament》/《Paxos Made Simple》 | TOCS 1998 / 2001 | Raft 的对照物；2020 课表中 Paxos 是 L7 的**选读** |
| （背景）Lamport《Time, Clocks, and the Ordering of Events》 | CACM 1978 | term 作为逻辑时钟的思想来源 |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **无主/多主共识**：EPaxos（SOSP 2013）、Flexible Paxos（OPODIS 2016）、WPaxos、Tempo——
    针对「强领导在跨地域部署下延迟高」的痛点；
  - **形式化验证**：用 TLA+/Coq 验证 Raft 的安全属性，以及 **IronFleet**（SOSP 2015，把协议与实现一起证明）；
    6.5840 2026 schedule 已把 IronFleet 单列一讲；
  - **确定性仿真测试**：把 Raft 跑进确定性模拟器，暴力搜索调度顺序，复现极小概率的时序 bug。
- **工业界开源（star 数 2026-09-26 `gh api` 实测）**：
  - `etcd-io/etcd`（**52310★**）：生产级 Raft 实现（Kubernetes 的元数据存储）。
  - `hashicorp/raft`（**9136★**）：Go 生态另一个 widely-used Raft 库。
  - `tikv/tikv`（**16878★**）+ `tikv/raft-rs`（**3401★**）：Rust 生态的 Multi-Raft 实践（见 [07-容错Raft二.md](07-容错Raft二.md)）。
  - `baidu/braft`（**4227★**）：百度开源的 C++ Raft 实现，工业级工程细节齐全。
  - `madsim-rs/madsim`（**1161★**）：确定性仿真器，用于把 Raft 类系统跑成可复现测试。

## 常见误区与本课程需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「多数派已复制 = 已提交」 | 还需 `entry.Term == currentTerm`（Figure 8 陷阱），否则可能提交后被覆盖 |
| 2 | 「选举只看谁先超时」 | 必须施加**选举限制**（日志新鲜度），否则会选出缺日志的 leader |
| 3 | 「term 大的 leader 一定日志更新」 | term 只表示「选举轮次」；日志新鲜度要用 lastLogTerm/lastLogIndex 比 |
| 4 | 「follower 冲突就删掉自己的日志」 | Raft 里 follower **不主动截断**，由 leader 的 AppendEntries 带 entries 覆盖（follower 只在收到冲突条目时按要求截断到匹配点之后） |
| 5 | 「心跳就是普通的空 RPC」 | 心跳 = 空 entries 的 AppendEntries，它同时承担压制选举与推进 `leaderCommit` |
| 6 | 🔧 2020 课程未覆盖 | **PreVote / CheckQuorum**：论文里没有，但生产实现几乎必加——防止「被隔离的节点反复自增 term 又落选」造成 term 爆炸与可用性抖动 |
| 7 | 🔧 2020 课程未覆盖 | **Leader Stickiness 与 Leader Transfer**：运维上常需要「不要因为一次网络抖动就换 leader」，以及「计划内迁移 leader」（论文把这些放到了实现/运维讨论里） |
| 8 | 🔧 2020 课程未覆盖 | **任期内追加 no-op 条目**：新 leader 上任后先写一条空条目以快速收敛多数派，是常见工程做法，不在 §1–§5 正文里 |
| 9 | 🔧 2020 课程未覆盖 | **论文的超时数值是数据中心量级**（百毫秒级）；跨地域部署必须重新标定，否则选举频繁触发 |

## 与其他章 / 其他书的联系

- **本目录内**：
  - [05-Go线程与Raft导论.md](05-Go线程与Raft导论.md)——本讲的前导（Raft 词汇 + Go 并发纪律）；
  - [07-容错Raft二.md](07-容错Raft二.md)——§7 之后：快照、成员变更、线性一致读、持久化；
  - [04-主从复制与VMwareFT.md](04-主从复制与VMwareFT.md)——同样追求「一致的日志」，但用共享磁盘仲裁；Raft 用多数派取代它；
  - [08-ZooKeeper.md](08-ZooKeeper.md)——Raft 之上的 KV 服务与「重复请求处理」。
- **跨书**：
  - [../深入理解分布式共识算法/07-Raft.md](../深入理解分布式共识算法/07-Raft.md)——中文推导版，与本讲逐节对读；
  - [../深入理解分布式共识算法/04-Paxos.md](../深入理解分布式共识算法/04-Paxos.md)——补 Paxos（2020 课表只作选读）；
  - [../深入理解分布式共识算法/12-FLP不可能定理.md](../深入理解分布式共识算法/12-FLP不可能定理.md)——解释「为什么 Raft 必须用超时 + 随机化」；
  - [../分布式算法/06-网络共识与选举.md](../分布式算法/06-网络共识与选举.md)——理论口径的选举与共识下界。

> **Lab 提示（思路，不给代码）**：Lab 2 的三个部分恰好对应本讲的三个层次——
> 2A 只做选举（先把「term + 投票 + 心跳压制」跑通）、
> 2B 加日志复制与提交（重点在一致性检查与回退）、
> 2C 加持久化（见 [07-容错Raft二.md](07-容错Raft二.md)）。
> 本目录不提供、也不链接任何公开解答仓库。
