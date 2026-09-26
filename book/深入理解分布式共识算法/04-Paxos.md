# 第 4 章 Paxos——分布式共识算法（4.1–4.4）

> 覆盖原书第 4 章前四节（第 2 篇，P48–63）：4.1 Paxos的诞生；4.2 初探Paxos（基本概念 / 角色 / 阶段）；
> 4.3 Paxos详解（模拟 / Prepare 阶段 / Accept 阶段 / 活锁 / 提案编号选定）；4.4 Paxos的推导过程（推导 / 多数派的本质）。
> 后半章（Multi Paxos、工程实现、PhxPaxos）见 [05-Multi-Paxos与PhxPaxos工程实现.md](05-Multi-Paxos与PhxPaxos工程实现.md)。

## 本章地图

本章是全书的算法主峰，也是最难读的一章。它讲 **Basic Paxos（单值共识，single-decree Paxos）**：

```
4.1 诞生  ── Lamport 1989 投稿、1998 才发表（Part-Time Parliament 的虚构考古叙事）
4.2 初探  ── 提案 / 三种角色 / 两个阶段：把「达成一致」拆成「抢号」+「定值」
4.3 详解  ── Prepare(Promise) 与 Accept(Accepted) 的完整消息流、活锁、编号怎么选
4.4 推导  ── 从「必须选某个人提议的值」反推出 P1/P2/P2a/P2b/P2c，落到多数派相交
```

**一句话概括 Basic Paxos**：先用一轮 Prepare **把旧的提案封死**（承诺不再接受更小编号），再用一轮 Accept **把值写进多数派**；一旦某个值被多数派接受，任何后续 Prepare 都会「看见」它并只能复用它——这就是安全性来源。

## 核心精讲

### 4.2.1 基本概念与角色

- **提案（proposal）**：`(编号 n, 值 v)`，编号全局可比且单调递增，值才是真正要共识的内容。
- **角色（4.2.2）**：

| 角色 | 职责 | 现实映射 |
| --- | --- | --- |
| Proposer（提案者） | 提出提案、驱动两阶段 | 接收写请求的节点 |
| Acceptor（接受者） | 对提案投票、记住承诺与已接受值 | 「投票箱」，是安全性的载体 |
| Learner（学习者） | 得知被选定的值 | 其余副本/观察者 |

> 一个进程可以**同时扮演多个角色**，这是 Paxos 与 Raft（角色互斥的 Server 状态机）在工程理解上的一大差异。

### 4.2.3 阶段：一次成功的消息时序

| 步骤 | 消息 | 发送方 → 接收方 | 接收方状态变化 |
| --- | --- | --- | --- |
| 1 | `Prepare(n)` | Proposer → Acceptors | 若 `n > maxPrepared` 则更新 `maxPrepared`（**落盘**） |
| 2 | `Promise(n, acceptedN, acceptedV)` | Acceptors → Proposer | 承诺不再接受编号 $< n$ 的提案 |
| 3 | （Proposer 选值） | — | 无 `acceptedV` 则用自己的值；否则用 `acceptedN` 最大的那个值 |
| 4 | `Accept(n, v)` | Proposer → Acceptors | 若 `n >= maxPrepared` 则接受并**落盘** `(n, v)` |
| 5 | `Accepted(n, v)` | Acceptors → Proposer / Learners | 达到多数派 → 值被 **chosen** |

> 两点工程注记：
> ① 步骤 1 与 4 的接收方都必须 **fsync 后再回复**，否则宕机重启会「忘记承诺」；
> ⑤ 的 Learner 通知可以是「每个 Acceptor 通知所有 Learner」（消息量 $O(n^2)$），也可以先汇总到**一个 distinguished learner** 再转发（消息量 $O(n)$，但多一跳且该 learner 成为单点——实践中通常选多个 learner 做冗余）。

### 4.2.3 / 4.3.2–4.3.3 两阶段的完整消息流

**Phase 1 —— Prepare / Promise（抢号 + 封旧）**

1. Proposer 选一个新编号 `n`，向 Acceptor 集合广播 `Prepare(n)`；
2. Acceptor 收到 `Prepare(n)`：
   - 若 `n <= maxPrepared`（已承诺过的最大编号）→ **拒绝或忽略**；
   - 否则令 `maxPrepared = n`（**持久化！**），回复 `Promise(n, acceptedN, acceptedV)`——「我承诺不再接受编号 < n 的提案；另外我最近一次接受的是 `(acceptedN, acceptedV)`」。

**Phase 2 —— Accept / Accepted（定值 + 传播）**

3. Proposer 收到**多数派**的 Promise：
   - 若所有回复里的 `acceptedV` 都为空 → **可以自由选自己的值** `v`；
   - 否则必须**选用回复中 `acceptedN` 最大的那个 `acceptedV`**（这是安全性的关键约束）；
4. 广播 `Accept(n, v)`；Acceptor 若 `n >= maxPrepared` 则接受，持久化 `(n, v)`，回复 `Accepted(n, v)`（并通知 Learner）；
5. 收到多数派 `Accepted` → 值 `v` **被选定（chosen）**。

```text
// 教学示意：Basic Paxos 两阶段（不参与构建、不编译、不运行）
// --- Proposer ---
fn propose(v):
    n = nextBallot()                      // 全局唯一、单调增，见 4.3.5
    promises = broadcastPrepare(n)        // Phase 1
    if len(promises) < majority: return RETRY     // 未凑够 quorum，重来（可能活锁）
    picked = max(promises, key = p -> p.acceptedN).acceptedV
    value  = (picked == nil) ? v : picked         // 「已有值就复用」= 安全性核心
    acks = broadcastAccept(n, value)              // Phase 2
    if len(acks) < majority: return RETRY
    return CHOSEN(value)

// --- Acceptor（状态必须落盘：maxPrepared / acceptedN / acceptedV）---
on Prepare(n):
    if n <= maxPrepared: return NACK(maxPrepared)
    maxPrepared = n; fsync()
    return PROMISE(n, acceptedN, acceptedV)

on Accept(n, v):
    if n < maxPrepared: return NACK(maxPrepared)
    (acceptedN, acceptedV) = (n, v); fsync()
    return ACCEPTED(n, v)
```

**为什么「复用已接受的最大值」能保证安全**（4.4 推导的直觉）：
设值 `v` 已被选定，即存在一个多数派 $Q_1$ 接受了 `(n, v)`。此后任何新提案 `n' > n` 的 Phase 1 也必须拿到某个多数派 $Q_2$ 的 Promise；由于**任意两个多数派必相交**，$Q_2$ 中至少有一个 Acceptor 属于 $Q_1$，它会在 Promise 里带上 `(n, v)`。因为 `v` 对应的 `n` 是它在 $Q_2$ 回复中能看到的最大编号之一，Proposer 只能选 `v`。**归纳下去，所有被选定的值都相同**。

### 4.3.4 活锁（dueling proposers）

两个 Proposer 交替抢号：P1 用 `n=1` 完成 Phase 1，P2 用 `n=2` 抢先，使 P1 的 Accept 被拒；P1 改用 `n=3`，又打断 P2……**谁也无法走完两阶段**。

- 注意：**活锁只破坏活性（liveness），不破坏安全性**——不会选出两个不同的值；
- 教科书解法：**选出一个唯一的 Proposer（Leader）**，只有 Leader 提案（这也正是 Multi-Paxos 的起点，见 [05](05-Multi-Paxos与PhxPaxos工程实现.md)）；
- 备选：随机退避（只能降低概率，不能根除）。

### 4.3.5 提案编号的选定

工程上的通用做法是把编号做成**二元组 `(round, serverId)`** 并按字典序比较：

- `round` 单调递增（本地持久化的计数器 + 每次选举递增）；
- `serverId` 保证同一 round 内不同 Proposer 的编号不冲突；
- **必须持久化**：Acceptor 重启后若「忘记」自己的 `maxPrepared`，会接受一个已经承诺过不再接受的旧编号提案，安全性直接崩塌（这是 Paxos 实现里最经典的 bug）。

### 4.4.2 多数派的本质

「多数派」不是魔法，它只是**满足「任意两个 quorum 相交」这个性质的一种取法**。更一般的说法：

- 安全性只需要 **quorum 相交性**：$\forall Q_1, Q_2: Q_1 \cap Q_2 \ne \emptyset$；
- 可用性只需要 **能容忍 f 个故障**：存在与任意故障集不相交的 quorum；
- 于是 $n = 2f+1$、$|Q| = f+1$ 是**最省节点**的一组解，不是唯一解。

## 版本演进

- **1989→1998**：Lamport 以「Paxos 岛兼职议会」的虚构考古故事写成论文，因叙事晦涩被拖延多年才发表（TOCS 1998）；
- **2001**：被逼出《Paxos Made Simple》——同一算法、去掉叙事、只保留推导；今天绝大多数人从这里入门；
- **2006–2007**：Google 的 Chubby（OSDI 2006）与《Paxos Made Live》（PODC 2007）把 Paxos 推到工程台前，同时坦白「从论文到实现之间有一大堆坑」；
- **2013–2014**：Raft（ATC 2014）以「可理解性」为第一目标重构同样的问题，事实上取代了 Paxos 作为**教学与新建系统**的默认选择；
- **2016**：Flexible Paxos（OPODIS 2016）指出「所有 quorum 两两相交」过强，只需 Phase-1 quorum 与 Phase-2 quorum 相交，打开了 quorum 配置空间；
- **2023（本书）**：保留了「推导脉络 + 算法模拟 + 源码解析」的写法，是中文材料里少见的、愿意讲「为什么是这样」的一章；
- **2026 视角**：工业界几乎不存在「裸的 Basic Paxos」——所有生产系统都是 **Multi-Paxos / Raft / ZAB**；Basic Paxos 的价值在于它是**安全性证明的最小模型**。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Lamport《The Part-Time Parliament》 | ACM TOCS 1998 | Paxos 原始论文 |
| Lamport《Paxos Made Simple》 | ACM SIGACT News 2001 | 去掉叙事的通俗重述 |
| Lamport《Fast Paxos》 | MSR-TR-2005-112 / Distributed Computing 2006 | 快路径（本目录 [10-Fast-Paxos.md](10-Fast-Paxos.md)） |
| Chandra, Griesemer, Redstone《Paxos Made Live – An Engineering Perspective》 | PODC 2007 | Google Chubby 的 Paxos 工程经验（「论文到实现」的坑清单） |
| Fischer, Lynch, Paterson《Impossibility of Distributed Consensus with One Faulty Process》 | JACM 1985 | 为什么 Paxos 必须在活性上让步（本书第 10 章） |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | Raft：以可理解性重构同类问题 |
| Howard, Malkhi, Spiegelman《Flexible Paxos: Quorum Intersection Revisited》 | OPODIS 2016 | quorum 相交条件可以放宽 |
| Oki & Liskov《Viewstamped Replication》 | PODC 1988 | 与 Paxos 同源的主副本复制方案 |

## 近年研究与工业界开源实践（2015–2026）

> star 数均为 2026-09 用 `gh api repos/OWNER/REPO --jq '.stargazers_count'` 实测。

- **直接实现 Paxos 的开源库**（数量明显少于 Raft，本身就是一种结论）：
  - `Tencent/phxpaxos`（**3,379★**）：微信开源的 Paxos 库，是本书 4.7 的主角（详见 [05-Multi-Paxos与PhxPaxos工程实现.md](05-Multi-Paxos与PhxPaxos工程实现.md)）。它把「Multi-Paxos + 状态机」做成可直接嵌入 C++ 服务的库。
  - `baidu/braft`（**4,227★**）：百度开源的 Raft 实现（C++），虽然不是 Paxos，但它与 phxpaxos 常被视为「中文互联网两大共识库」，工程取舍（快照/成员变更/读优化）高度可比。
- **Raft 阵营**（承接 Paxos 的工程化成果）：
  - `etcd-io/raft`（**1,128★**）/ `etcd-io/etcd`（**52,310★**）、`hashicorp/raft`（**9,136★**）、`sofastack/sofa-jraft`（**3,824★**）。
- **共识 + 分组的工程化**：`tikv/tikv`（**16,878★**）与 `cockroachdb/cockroach`（**32,508★**）用 Multi-Raft 把「一个 Paxos/Raft 实例」扩展到成千上万个 Region/Range。
- **近年研究**：
  - **Flexible Paxos**（OPODIS 2016）把 quorum 变成可调旋钮：把热路径的 Phase-2 quorum 缩小、Phase-1 quorum 放大；
  - **形式化验证**成为共识实现的标配方法（TLA+ / Jepsen），PhxPaxos、Raft 等实现都引入了确定性模拟测试；
  - **Paxos vs Raft 的争论已平息**：Raft 赢在可理解性与生态，Paxos 赢在灵活性与 quorum 可调；两者在安全性结构上同构（都是 quorum 相交 + 二阶段）。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Paxos 一次就能决定一个值，可以直接当复制日志用」 | Basic Paxos 是 **single-decree**（只决定一个值）；复制日志需要跑一串实例 → Multi-Paxos（本章未覆盖，见 [05](05-Multi-Paxos与PhxPaxos工程实现.md)） |
| 2 | 「Acceptor 的状态可以不落盘」 | `maxPrepared / acceptedN / acceptedV` **必须 fsync**；重启失忆会接受旧编号提案，直接破坏安全性 |
| 3 | 「活锁会导致选出两个值」 | 活锁只破坏**活性**；安全性由 quorum 相交保证，与活锁无关 |
| 4 | 「活锁靠随机退避解决」 | 工程解是**选唯一 Leader**（Multi-Paxos/Raft 的做法）；退避只降概率 |
| 5 | 「提案编号随便自增就行」 | 需要 `(round, serverId)` 二元组保证并发 Proposer 不撞号，且 round 要持久化 |
| 6 | 「多数派是硬性要求」 | 硬性要求只是 **quorum 相交**；多数派是 $2f+1$ 配置下的最省解，Flexible Paxos 允许非对称 quorum |
| 7 | 🔧 本书把「Paxos」作为默认工程选型，需要补一句现实 | 2026 年新建系统**绝大多数选 Raft**（etcd/HashiCorp/SOFAJRaft/TiKV/CockroachDB 全在 Raft 生态）；Paxos 主要在**存量系统**（Chubby/Spanner 一脉）与少数库（phxpaxos）中出现。这不是算法优劣，而是**生态与可理解性**的结论（🔧） |
| 8 | 🔧 本书未把 Paxos 与 Raft 做「结构同构」的对照 | 补：Raft 的 term ≈ Paxos 的 ballot；Raft 的「日志连续性 + 强 Leader」是**用额外约束换可理解性**，代价是成员变更与日志对齐更复杂（详见 [07-Raft.md](07-Raft.md) 与 [08-Raft工程实践与SOFAJRaft.md](08-Raft工程实践与SOFAJRaft.md)） |
| 9 | 🔧 本书未给出「如何验证实现正确」 | 补：共识实现应配 **TLA+ 规格 + 确定性模拟测试 + Jepsen 风格故障注入**；`jepsen-io/jepsen`（**7,504★**）是公开可查的第三方校验工具。`Tencent/phxpaxos`（**3,379★**）自带确定性测试框架，是该方向的开源样本 |
| 10 | 🔧 「Paxos Made Simple 就够了」的阅读建议不完整 | 入门读 Paxos Made Simple；但要写实现必须读 **《Paxos Made Live》（PODC 2007）**——它列了论文不写而工程必需的坑（磁盘损坏、成员变更、快照、master lease） |

## 与其他章 / 其他书的联系

**本目录内**

- [05-Multi-Paxos与PhxPaxos工程实现.md](05-Multi-Paxos与PhxPaxos工程实现.md)：本章的直接续篇——Leader 选举把「活锁」变成「选主」，工程优化处理幽灵日志与读路径。
- [07-Raft.md](07-Raft.md)：同问题的另一解法；建议读完本章立即对照 Raft 的 term/日志连续性。
- [09-Paxos变种算法的发展史.md](09-Paxos变种算法的发展史.md) / [10-Fast-Paxos.md](10-Fast-Paxos.md) / [11-EPaxos.md](11-EPaxos.md)：本章的 quorum 与二阶段是理解所有变种的前提。
- [12-FLP不可能定理.md](12-FLP不可能定理.md)：解释为什么本章的「活锁」不是 bug，而是异步模型的固有代价。

**跨书**

- [../深入理解分布式系统/06-Paxos与Multi-Paxos及其变体.md](../深入理解分布式系统/06-Paxos与Multi-Paxos及其变体.md)：同主题的另一种讲法，适合作为本章的对照阅读。
- [../分布式算法/06-网络共识与选举.md](../分布式算法/06-网络共识与选举.md)：Lynch 教材对共识的算法级处理，比本章严格。
- [../分布式数据库入门进阶与实战/09-共识算法.md](../分布式数据库入门进阶与实战/09-共识算法.md)：工程口径的 Paxos 概述，读它可快速判断「我到底要不要自己实现」。
- [../分布式系统概念与设计/10-协调与协定.md](../分布式系统概念与设计/10-协调与协定.md)：教科书对共识与相关问题的分章口径。
</content>
