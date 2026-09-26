# 第 5 章 Multi-Paxos 与 PhxPaxos 工程实现（4.5–4.7）

> 覆盖原书第 4 章后三节（第 2 篇，P64–100）：4.5 Multi Paxos详解（简介 / Leader选举）；
> 4.6 工程实现（一些优化 / 对读请求进行优化 / 并行协商 / Instance的重确认 / 幽灵日志）；
> 4.7 Paxos在PhxPaxos中的应用（分析 / 初始化 / 协商提案 / 数据同步 / Master选举 / 成员变更）。
> 前半章（Basic Paxos）见 [04-Paxos.md](04-Paxos.md)。

## 本章地图

如果说第 4 章前半段给出的是「**数学上正确的单值共识**」，本章给出的是「**能跑在生产上的连续共识**」：

```
Basic Paxos（每值两轮通信、会活锁）
   │  选出一个长期 Leader，把 Phase 1 摊掉
   ▼
Multi-Paxos（一轮通信定一个值；一串 instance 组成复制日志）
   │  但论文到此为止，工程上的坑才刚开始
   ▼
4.6 工程实现：读优化 / 并行协商 / 重确认 / 幽灵日志
   │
   ▼
4.7 PhxPaxos：把这些全部落成一个可直接嵌入的 C++ 库
```

- **4.5**：Multi-Paxos 的核心想法极简——**Leader 稳定后，Phase 1 只做一次**，之后每个日志槽（instance）直接跑 Phase 2；
- **4.6**：五个工程议题，每一个都是论文不写、但实现者必须回答的问题；
- **4.7**：PhxPaxos 作为「可运行的 Multi-Paxos」样本，把 4.5–4.6 全部落地。

## 核心精讲

### 4.5.1 Multi-Paxos：从「一次共识」到「一串共识」

**复制日志 = 一串独立的 Paxos 实例**。第 $i$ 个槽位（instance $i$）的值就是第 $i$ 条命令。

```text
// 教学示意：Multi-Paxos 的稳态路径（不参与构建、不编译、不运行）
// 一次性成本：Leader 上任时对整个 instance 区间做一次 Phase 1（Prepare）
fn onBecomeLeader():
    for i in (lastExecuted+1 .. plusInfinity):
        // 只需要拿到多数派 Promise；区间可以合并成一条消息
        promise = broadcastPrepare(ballot = B, instanceRange = [i, +inf))
        if not quorum(promise): return STEP_DOWN
    ready = true                // 之后每个槽位只跑 Phase 2

// 稳态：每个写请求一轮通信
fn replicate(cmd):
    i = nextIndex++
    acks = broadcastAccept(instance = i, ballot = B, value = cmd)
    if quorum(acks): commitIndex = i; apply(cmd)
    else:            return STEP_DOWN      // 失去多数派 → 退位
```

**为什么这样就够了**：Phase 1 的语义是「封死更小编号的提案」。Leader 用同一个 ballot $B$ 对**整个区间**做完 Prepare 后，在它仍是 Leader 的期间，再没有别人能用更大的 ballot 抢走（除非换主），于是每个新槽位直接 Accept 即可。

### 4.5.2 Leader 选举：三种常见做法

| 做法 | 机制 | 评价 |
| --- | --- | --- |
| 用 Paxos 本身选主 | 把「谁是 Leader」当作一个值去跑 Basic Paxos | 自洽、无需额外组件；本书思路 |
| Lease（租约） | Leader 定期续租，租期内保证无人争抢 | 依赖**时钟漂移上界**；工程常见但假设要写清楚 |
| 外部故障检测器 | 用 ◇W 一类的故障检测器触发选主 | Chandra & Toueg 的理论保证：最弱的「最终弱」检测器即可解共识 |

> 理论要点：Chandra & Toueg（JACM 1996）证明，**在异步系统中，共识可解的充要条件是存在一个足够强的故障检测器**（◇W「最终弱」是解共识的最弱类别）。这条结论解释了为什么「选主」在所有共识实现里都无法避免，也解释了为什么纯异步下 FLP 的悲观结论成立。

### 4.6.1 一些优化

- **批量（batching）**：多条命令合成一个 instance，摊薄 fsync 与网络开销；
- **流水线（pipelining）**：不等待前一条 commit 就发下一条，用滑动窗口控制未决数量；
- **Leader 粘性**：Leader 稳定时不重新 Prepare，减少消息量；
- **消息合并**：把 `Promise` / `Accepted` 与心跳合并，减少 RPC 数；
- **Learner 传播**：由 Leader 直接推给 Learner，或在 Learner 数量大时用「Learner 组播树」。

### 4.6.2 对读请求进行优化

读请求若也走一遍 Paxos，代价与写相同。三种逐级放松的做法（本书第 6 章 6.7 在 Raft 语境下给了五方案，可对照）：

| 方案 | 做法 | 保证 | 代价 |
| --- | --- | --- | --- |
| Log Read（走日志） | 读请求也提交成一条日志 | 线性一致 | 一次完整共识，最慢 |
| Read Index | Leader 记下当前 commitIndex，向多数派确认自己仍是 Leader，等状态机追上该 index 后本地读 | 线性一致 | 一次 RPC 往返（不发日志） |
| Lease Read | Leader 持租约，租期内直接本地读 | 线性一致（**依赖时钟假设**） | 零 RPC，最快 |

> 🔧 **Lease Read 的安全性依赖「时钟漂移有上界」这一假设**。若发生时钟跳变（NTP 校正、虚拟机迁移、GC 停顿导致租约判断滞后），可能出现「旧 Leader 仍认为自己在租期内」→ 返回旧值 → 破坏线性一致性。etcd 默认走 **ReadIndex**，把 Lease Read 作为可选项，正是出于这一顾虑。

### 4.6.3 并行协商

多个 instance 同时推进（滑动窗口），关键约束是**应用顺序仍必须按槽位递增**。并行提升的是**吞吐**而非**单条延迟**；窗口大小需要与「fsync 吞吐 / 网络 RTT」匹配，过大会在换主时产生大量未决 instance 需要重确认。

### 4.6.4 Instance 的重确认

新 Leader 上任时，区间内可能存在**未决 instance**：某些槽位可能已被多数派接受（值已确定但未广播），也可能只在少数派上（值未确定）。新 Leader 必须：

1. 对区间做一次 Prepare（Phase 1），收集每个 instance 的 `acceptedV`；
2. 对**已确定值的 instance** 重新广播该值（重确认），确保多数派都知道；
3. 对**值未确定的 instance**，安全做法是**填 no-op**（避免「幽灵复现」，见下）。

### 4.6.5 幽灵日志（幽灵复现）

**现象**：旧 Leader 收到客户端写请求 $W$，在本地与部分副本上写入了 instance $i$，但**未达成多数派**就宕机/失联；客户端也未收到成功响应（视为失败）。新 Leader 上任后做重确认时，若把 instance $i$ 的值「复活」并提交，客户端就会看到一条**它以为写失败了、实际却生效了**的记录——这就是**幽灵日志**。

**危害**：破坏「客户端可见的成功/失败语义」，对**非幂等写**（如余额扣减后重试）尤其致命。

**通用解法**：新 Leader 在开始服务前，先把所有「不确定性」封住——
- 对已确认有值的槽位重确认；
- 对无值或不确定的槽位**显式提交 no-op**（让它不可能再被复活）；
- 做完这一步再响应客户端。

```text
// 教学示意：换主时封住幽灵日志（不参与构建、不编译、不运行）
fn onBecomeLeader():
    for i in (lastExecuted+1 .. maxKnownInstance):
        v = prepareCollect(i)                 // 收集该 instance 的 acceptedV
        if v != nil and wasAcceptedByQuorum(i): broadcastAccept(i, v)   // 重确认
        else:                                   broadcastAccept(i, NOOP) // 主动封死
    commitNoopBoundary()                      // 提交一条边界日志
    readyToServe = true
```

> ⚠️ PhxPaxos 处理幽灵日志的**具体代码路径**（如是否在 `InitAndStartMaster` 中提交 no-op 边界）未在本次核实，**未能核实原文，存疑**；上面给出的是该问题的通用工程解法。

### 4.7 PhxPaxos：一个可嵌入的 Multi-Paxos 库

- **定位**：微信（腾讯）开源的 C++ Paxos 库（`Tencent/phxpaxos`，**3,379★**），把 Multi-Paxos + 状态机封装成库，业务只需实现状态机的 `Execute`。
- **4.7.1 分析要点**：分层（Paxos 算法层 / 实例层 / 状态机层）、多 Group 支持（不同数据分片可用不同 Paxos 组，即「分组 Paxos」的雏形）、网络与存储可插拔。
- **4.7.2 初始化**：读取本机已持久化的 instance 状态，构造 Paxos Node 与 Group，进入 Follower。
- **4.7.3 协商提案**：即上文 Multi-Paxos 稳态路径，含批量与流水线。
- **4.7.4 数据同步**：落后副本从 Leader 拉取缺失 instance（类似 Raft 的日志对齐，但 Paxos 允许「槽位空洞」，需要逐槽补齐）。
- **4.7.5 Master 选举**：基于 Paxos 的选主，配租约与续约。
- **4.7.6 成员变更**：基于「成员组本身也是一个被共识的值」的思路（Lamport 的 *Reconfiguring a State Machine* 一脉）。

## 版本演进

- **1998–2001**：Lamport 在论文里**只用一两段话**提到「选一个 Leader 就能省掉 Phase 1」——Multi-Paxos 从来没有被 Lamport 写成一份完整规格，这是后来一切混乱的源头；
- **2007**：《Paxos Made Live》（PODC 2007）首次系统披露「论文没写的部分」：磁盘损坏、成员变更、快照、master lease；
- **2010**：Lamport、Malkhi、Zhou《Reconfiguring a State Machine》（SIGOPS OSR）给出成员变更的规范化思路；
- **2014**：Ongaro & Ousterhout 的 Raft 干脆把 **Leader 选举、日志复制、安全性、成员变更、日志压缩**全部写进论文——这正是 Raft 对 Paxos 生态最大的改进（不是算法更优，而是**规格完整**）；
- **2017 前后**：phxpaxos 开源（微信），中文互联网获得一个可读、可跑、带测试的 Paxos 实现；
- **2023（本书）**：选择 phxpaxos 作为 Paxos 的源码载体，是本书相对多数中文材料的**差异化价值**；
- **2026 视角**：共识库的竞争已从「算法」转到「**工程完整度与生态**」——快照、成员变更、读优化、可观测性、混沌测试，以及是否有 Jepsen 级别的第三方验证。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Lamport《Paxos Made Simple》 | ACM SIGACT News 2001 | Multi-Paxos（选主后只跑 Phase 2）的原始表述 |
| Chandra & Toueg《Unreliable Failure Detectors for Reliable Distributed Systems》 | JACM 1996 | 故障检测器与共识可解性；◇W 是解共识的最弱检测器 |
| Chandra, Griesemer, Redstone《Paxos Made Live – An Engineering Perspective》 | PODC 2007 | 「论文到实现」的坑清单 |
| Lamport, Malkhi, Zhou《Reconfiguring a State Machine》 | ACM SIGOPS OSR 2010 | 成员变更（reconfiguration）的规范思路 |
| Lamport《Cheap Paxos》 | DSN 2004 | 用辅助节点降低成本（本目录 [09-Paxos变种算法的发展史.md](09-Paxos变种算法的发展史.md)） |
| Ongaro《Consensus: Bridging Theory and Practice》（博士论文） | Stanford 2014 | 系统讨论 Multi-Paxos 与 Raft 的工程差异 |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | Raft：把 Paxos 论文未写之处补全 |

## 近年研究与工业界开源实践（2015–2026）

> star 数均为 2026-09 用 `gh api repos/OWNER/REPO --jq '.stargazers_count'` 实测。

- `Tencent/phxpaxos`（**3,379★**）：本章 4.7 的主角。价值在于「**可读的 Multi-Paxos 完整实现**」——含选主、重确认、成员变更、多 Group，且自带确定性测试框架（可用于验证幽灵日志等边界行为）。
- `etcd-io/etcd`（**52,310★**）：读优化的对照样本——默认 **ReadIndex**，Lease Read 可选；`etcd-io/raft`（**1,128★**）把 Raft 拆成独立库，与 phxpaxos 的角色类似但生态更大。
- `sofastack/sofa-jraft`（**3,824★**）：Java 侧对应物（本书第 6 章 6.9 的主角），工程议题（快照/成员变更/读路径）与 phxpaxos 一一对应，适合横向比较。
- `baidu/braft`（**4,227★**）：C++ Raft 实现，与 phxpaxos 同语言同量级，可直接对照两者在**日志存储、快照、成员变更**上的取舍。
- `jepsen-io/jepsen`（**7,504★**）：第三方一致性验证；共识库是否「真的线性一致」要用它说话。
- **近年研究**：
  - **Flexible Paxos**（Howard, Malkhi, Spiegelman，OPODIS 2016）在 Multi-Paxos 语境下最有价值：把 Phase-1 与 Phase-2 的 quorum 解耦，可以缩小热路径 quorum 以换取延迟；
  - **确定性模拟测试**（FoundationDB 一脉的做法）成为共识库的质量门槛；
  - **Multi-Raft 分组**（TiKV/CockroachDB）把「一个共识组」扩展到成千上万个组，带来了**组间负载均衡与分裂合并**的新议题，这是单组 Paxos 时代没有的问题。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Multi-Paxos 是 Lamport 正式提出的算法，有标准规格」 | Lamport 只简单提及「选主后可省 Phase 1」；**没有完整规格**，成员变更/快照/日志对齐都靠各实现自行发挥（🔧） |
| 2 | 「Multi-Paxos 保证日志连续」 | 不保证。Paxos 的 instance 之间**允许空洞**，需要逐槽补齐；Raft 才强制日志连续（这是两者工程差异的关键） |
| 3 | 「读走 Leader 就一定是线性一致」 | 若 Leader 已失联但仍自认是 Leader（旧 Leader 读），会返回旧值 → 需要 ReadIndex / Lease Read 之类的确认机制 |
| 4 | 「Lease Read 和 ReadIndex 一样安全」 | Lease Read 依赖**时钟漂移上界**；时钟跳变/GC 停顿会破坏它（🔧） |
| 5 | 「幽灵日志是 Paxos 独有的问题」 | 换主导致的「未决日志复活」在 Raft 中同样存在（用**上任先提交 no-op 边界日志**解决）；只是 Raft 因日志连续而更好定位 |
| 6 | 🔧 本书用 phxpaxos 代表 Paxos 工程实现，需补生态对比 | 2026 年共识库的事实标准是 **Raft 生态**（etcd-io/raft **1,128★**、hashicorp/raft **9,136★**、sofa-jraft **3,824★**、braft **4,227★**），phxpaxos（**3,379★**）是 Paxos 侧最重要的中文开源实现但生态较小。选型时应说明「**生态与可维护性**往往比算法家族更重要」 |
| 7 | 🔧 本书未覆盖 Multi-Raft 分组这一主流形态 | 补：TiKV（`tikv/tikv` **16,878★**）与 CockroachDB（`cockroachdb/cockroach` **32,508★**）用**成千上万个 Raft 组**（Region/Range）+ 集中调度（PD）实现水平扩展；单组 Paxos/Raft 的性能已不是瓶颈，**分组与调度**才是。本书停留在单组视角 |
| 8 | 🔧 国产化选型对照未给出 | 公开资料口径：**OceanBase** 以 **Multi-Paxos** 作为副本一致性核心；**TiDB/TiKV** 用 **Multi-Raft**；**PolarDB** 相关设计采用 **ParallelRaft** 一类并行共识（见 [08-Raft工程实践与SOFAJRaft.md](08-Raft工程实践与SOFAJRaft.md)）。三者共同点是**都不是单组共识**，而是分组/并行化；差异来自分片粒度与存储形态，而非算法家族 |
| 9 | 🔧 「重确认」的正确性依赖持久化的 ballot | 若 Acceptor 重启后丢失 `maxPrepared`（未 fsync），重确认会接受旧编号提案 → 安全性崩塌；实现必须把 ballot 与 instance 状态一起落盘，并用 TLA+/确定性测试覆盖该路径 |

## 与其他章 / 其他书的联系

**本目录内**

- [04-Paxos.md](04-Paxos.md)：本章的 Multi-Paxos 直接复用前章的两阶段与 quorum 相交论证。
- [07-Raft.md](07-Raft.md) / [08-Raft工程实践与SOFAJRaft.md](08-Raft工程实践与SOFAJRaft.md)：工程议题（读优化 / 幽灵日志 / 成员变更）逐条对照；Raft 论文把它们写进了规格，Paxos 没有。
- [09-Paxos变种算法的发展史.md](09-Paxos变种算法的发展史.md)：Vertical Paxos 讨论的就是「换成员 + 换配置」，是本章成员变更的延伸。
- [11-EPaxos.md](11-EPaxos.md)：EPaxos 正是要去掉本章的「Leader 瓶颈」，代价是依赖图复杂度。

**跨书**

- [../深入理解分布式系统/06-Paxos与Multi-Paxos及其变体.md](../深入理解分布式系统/06-Paxos与Multi-Paxos及其变体.md)：Multi-Paxos 的另一份中文讲法，可与本章对读。
- [../分布式算法/06-网络共识与选举.md](../分布式算法/06-网络共识与选举.md)：故障检测器与选主的严格化处理（Chandra-Toueg 的理论背景）。
- [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)：从架构角度解释为什么生产系统要分组、要调度。
- [../分布式数据库入门进阶与实战/09-共识算法.md](../分布式数据库入门进阶与实战/09-共识算法.md)：把 Multi-Paxos/Raft 放回数据库复制的语境。
</content>
