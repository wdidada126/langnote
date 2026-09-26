# 第 10 章 Fast Paxos——C/S 架构的福音

> 覆盖原书第 8 章（第 3 篇「Paxos变种算法集合」，P242–254）：
> 8.1 Fast Paxos简介（背景介绍 / 基本概念）；8.2 算法详述（算法设计 / Fast Paxos模拟 / Learn阶段）；
> 8.3 Quorum推导（决策条件 / 计算Quorum）；8.4 Classic Round简介（提案冲突 / 选择提案值的规则 / 证明）；
> 8.5 提案恢复（基于协调者的恢复 / 基于非协调者的恢复）；8.6 本章小结。

## 本章地图

本章回答一个非常具体的工程问题：**能不能少一个消息延迟？**

```
经典 Paxos（C/S 架构下）：Client → Coordinator(Leader) → Acceptor → Learner/Client
                           = 3 个消息延迟（客户端视角）
Fast Paxos：               Client/Acceptor 直接收提案并响应
                           = 2 个消息延迟（省掉 Coordinator 那一跳）
代价：quorum 变大 + 节点数变多，且「冲突」时要回退，反而更慢
```

- **8.1**：背景（客户端直连 acceptor 的动机）与概念（**fast round / classic round**、coordinator 与 proposer 的区分、`Any` 消息）；
- **8.2**：算法设计与消息流、Learn 阶段；
- **8.3**：quorum 推导——本章最硬的一节：为什么「快」必须付出更大的 quorum；
- **8.4**：冲突（collision）发生时回退到 classic round 的规则与证明；
- **8.5**：两种恢复路径（由谁来完成恢复）。

## 核心精讲

### 8.1.1 背景：省掉 Coordinator 那一跳

在 C/S 架构中，客户端的写请求通常先到 Leader（coordinator），由 Leader 跑 Phase 2。若客户端能**直接把值发给所有 acceptor**，就能省掉这一跳网络往返。

代价是：**没有 Leader 来「统一选值」**，于是多个客户端可能同时向 acceptor 提出**不同的值** → 冲突。

### 8.1.2 基本概念

| 概念 | 含义 |
| --- | --- |
| **Classic round** | 与经典 Paxos 相同：coordinator 收集 Phase 1 结果后**亲自选值**再广播 |
| **Fast round** | coordinator 在 Phase 1 后发 `Any` 消息（表示「我不指定值」），**任何 proposer（客户端）都可以直接把值发给 acceptor**，acceptor 像对待普通 accept 一样处理 |
| **Coordinator** | 完成 Phase 1、拿到写权限的那个 proposer（本轮的组织者） |
| **Proposer** | 任何提出值的人（fast round 下可以是客户端本身） |
| **Collision（冲突）** | 快路径上出现了两个不同的值，导致无法仅凭本轮结果判定 |

```text
// 教学示意：经典轮 vs 快轮（不参与构建、不编译、不运行）
// --- Classic round（3 个消息延迟）---
//   Client → Coordinator: v
//   Coordinator → Acceptors: Accept(n, v)
//   Acceptors → Learner/Client: Accepted(n, v)

// --- Fast round（2 个消息延迟）---
//   Coordinator → Acceptors: Prepare(n) → Promise，然后发 Any(n)
//   Client → Acceptors: Accept(n, v)     // 客户端直投
//   Acceptors → Learner/Client: Accepted(n, v)
```

### 8.3 Quorum 推导：为什么「快」要更大的 quorum

设 $N$ 为 acceptor 总数，$f$ 为可容忍故障数，$e$ 为「仍能两步决定」所允许的故障数（$e \le f$）。

| 配置 | 经典 Paxos | Fast Paxos（典型配置） |
| --- | --- | --- |
| acceptor 总数 $N$ | $2f+1$ | 需 **$3f+1$**（工程综述中常见的取值） |
| 普通（classic）quorum | $f+1$（多数派） | — |
| **fast quorum** | — | **$2f+1$** |
| 客户端视角延迟 | 3 个消息延迟 | 2 个消息延迟 |

**直觉解释**：经典 Paxos 里，coordinator 保证了「本轮只有一个值被提出」，于是任意两个 quorum 相交（$2(f+1) > 2f+1$）就足够安全。快路径下**可能同时出现两个值**，为了让「后来者能看到先前的值」，快路径 quorum 必须**大到足以与之前的快路径 quorum 在足够多的节点上相交**——于是 fast quorum 从 $f+1$ 涨到 $2f+1$，总节点数从 $2f+1$ 涨到 $3f+1$。

- 理论下界：Lamport 给出「可扩展到 $e \le f$ 场景」的两步共识需要至少 $\max\{2e+f+1,\; 2f+1\}$ 个进程，Fast Paxos 达到该下界；
- 出处提示：上述 $3f+1$ / fast quorum $=2f+1$ 的常见表述见 Lamport 的 *Fast Paxos* 与工程综述（如 Petrov《Database Internals》第 14 章，其引用标注为 Junqueira 等的工作）。**本书 8.3 的具体推导过程未能核实原文**（大纲只给小节名），上表属于该主题的公认结论。

### 8.4 冲突与回退：Classic Round 的价值

**冲突（8.4.1）**：快路径上有两个不同的值 $v_1, v_2$ 分别被部分 acceptor 接受，且都**未达到 fast quorum** → 无法判断谁被选定。

**8.4.2 选择提案值的规则**（恢复时 coordinator 该选谁）：

- 若快路径已有一个值达到 fast quorum → 该值已被选定，只能复用；
- 否则 coordinator 按「**被接受的最大的 ballot/轮次**」或论文给出的排序规则挑一个值，用 **classic round** 重新广播；
- 由于 fast quorum 与 classic quorum 相交，coordinator 在 Phase 1 一定能「看到」可能已被选定的值，从而不会选错。

```text
// 教学示意：冲突后的恢复（不参与构建、不编译、不运行）
fn coordinatorRecover(round n):
    promises = Prepare(n+1)                        // 重新跑 Phase 1
    seen = collectAcceptedValues(promises)         // 收集各 acceptor 已接受的值
    if exists v with count(v) >= fastQuorumSize:   // 已被快路径选定
        return Accept(n+1, v)                      // 只能复用
    else:
        return Accept(n+1, pickByRule(seen))       // 按论文规则选一个（classic round）
```

> **这就是 Fast Paxos 的代价曲线**：无冲突时快 1 个延迟；一旦冲突，需要**额外的恢复轮**，总延迟可能**高于**经典 Paxos。

### 8.5 两种恢复路径

| 恢复方式 | 由谁做 | 特点 |
| --- | --- | --- |
| **基于协调者（8.5.1）** | 由当前轮的 coordinator 发起新轮恢复 | 最常用；coordinator 本来就有写权限，直接跑 classic round |
| **基于非协调者（8.5.2）** | 由其他节点（如 learner 或后续 proposer）发起 | 用于 coordinator 也故障的情形；需要先用更高 ballot 抢占 |

### 8.2.3 Learn 阶段

被选定的值需要让 Learner 知道。常见做法：acceptor 在 accepted 后通知一组 learner，或由 coordinator 汇总后广播。**消息量与 learner 数量成正比**，大规模部署时通常用 learner 组播树或只通知 coordinator 再转发。

## 版本演进

- **2005**：Lamport 提出 Fast Paxos（MSR-TR-2005-112；期刊版 *Distributed Computing* 19(2), 2006）；同年提出 Generalized Paxos（[09-Paxos变种算法的发展史.md](09-Paxos变种算法的发展史.md) 7.3）；
- **2007 前后**：经验性结论出现——由于 acceptor 数量从 $2f+1$ 增至 $3f+1$，消息总数上升，**高冲突率下 Fast Paxos 的延迟反而高于经典 Paxos**；
- **2013**：EPaxos（SOSP 2013）用「依赖图」在**更少节点**下实现两步提交，绕开了「必须 $3f+1$」的直觉（见 [11-EPaxos.md](11-EPaxos.md)）；
- **2025**：**Revisiting Lower Bounds for Two-Step Consensus**（PODC 2025）重新审视 Lamport 的两步共识下界，指出 EPaxos 之所以能用更少的进程达成两步决定，是因为「快」的定义在实践里可以放宽（只要求某个进程快，而非所有进程快）；
- **2023（本书）**：把 quorum 推导与恢复流程完整讲一遍，是本章的价值所在；
- **2026 视角**：Fast Paxos 仍然**极少被直接实现**；「降低延迟」的主流工程手段是 **Multi-Raft 分组 + 就近 Leader / follower read / ReadIndex**，而不是增大 quorum 换一个消息延迟。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Lamport《Fast Paxos》 | MSR-TR-2005-112, 2005；*Distributed Computing* 19(2):79–103, 2006 | 快路径与两步共识 |
| Lamport《Generalized Consensus and Paxos》 | MSR-TR-2005-33, 2005 | 命令可交换性（[09](09-Paxos变种算法的发展史.md) 7.3） |
| Lamport《The Part-Time Parliament》 | ACM TOCS 1998 | 被比较的经典版本 |
| Moraru, Andersen, Kaminsky《There Is More Consensus in Egalitarian Parliaments》 | SOSP 2013 | EPaxos：用更少节点达成两步决定 |
| Ryabinin, Gotsman, Sutra《Revisiting Lower Bounds for Two-Step Consensus》 | PODC 2025 | 重新审视两步共识的进程数下界 |
| Howard, Malkhi, Spiegelman《Flexible Paxos: Quorum Intersection Revisited》 | OPODIS 2016 | quorum 相交条件的一般化 |
| Petrov《Database Internals》第 14 章 | O'Reilly, 2019 | 工程综述口径的 Fast Paxos 与 quorum 数值 |

## 近年研究与工业界开源实践（2015–2026）

> star 数均为 2026-09 用 `gh api repos/OWNER/REPO --jq '.stargazers_count'` 实测。

- **落地情况**：Fast Paxos 与 [09](09-Paxos变种算法的发展史.md) 的六个变种一样，**没有主流开源生产实现**。生产系统的共识层几乎全部落在 Raft / Multi-Paxos / Multi-Raft 上：

| 系统 / 库 | star | 说明 |
| --- | --- | --- |
| `etcd-io/etcd` | 52,310★ | Raft；降低延迟靠 ReadIndex 与本地读，不靠快路径 |
| `etcd-io/raft` | 1,128★ | Raft 库 |
| `hashicorp/raft` | 9,136★ | Raft 库 |
| `sofastack/sofa-jraft` | 3,824★ | Java Raft |
| `Tencent/phxpaxos` | 3,379★ | Multi-Paxos（非 Fast Paxos） |
| `tikv/tikv` | 16,878★ | Multi-Raft 分组 + PD 调度 |
| `cockroachdb/cockroach` | 32,508★ | Multi-Raft 分组 |

- **为什么没落地（工程判断）**：
  1. **节点成本**：从 $2f+1$ 涨到 $3f+1$，意味着容忍 1 个故障要从 3 台变 4 台；多出来的机器成本与运维成本通常高于省下的一个 RTT；
  2. **收益有限**：同一数据中心内 RTT 常在亚毫秒级，省一跳**绝对值很小**；
  3. **风险不对称**：无冲突才有收益，冲突时**更慢**；而冲突率会随写入并发上升；
  4. **有更简单的替代**：ReadIndex / 本地读降低的是**读**延迟（读通常占绝大多数），且实现简单得多；Multi-Raft 分组则把 Leader 放到离客户端近的地方。
- **近年研究**：
  - **EPaxos**（SOSP 2013）与 **Optimized EPaxos** 证实用 $2f+1$ 个节点也能在多数场景两步决定（代价是依赖图与恢复复杂度）；
  - **PODC 2025** 的工作从理论上下解释了这个矛盾（「快」的定义差异），并给出更贴近实践的下界；
  - **广域网场景**的主流解法已经是**分区 + 就近 Leader**（CockroachDB 的 geo-partitioning、TiKV 的 Placement Rules），而不是协议内的快路径。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Fast Paxos 只是把 Leader 去掉」 | 它保留 coordinator（负责 Phase 1 与恢复），只把 **Phase 2 的值选择权**交给 proposer |
| 2 | 「Fast Paxos 用同样的 $2f+1$ 个节点」 | 快路径需要更大的 fast quorum，典型配置下总数升到 **$3f+1$** |
| 3 | 「快路径命中失败就退化成经典 Paxos」 | 不是简单退化，而是要走**恢复流程**（新轮 + 选值规则），延迟可能**高于**经典 Paxos |
| 4 | 「冲突概率很低，可以忽略」 | 冲突率随并发写上升；写密集场景下快路径命中率会显著下降 |
| 5 | 「省一个消息延迟一定值」 | 同机房 RTT 亚毫秒，收益小；节点从 3 台变 4 台的成本是确定的 |
| 6 | 🔧 本书以「C/S 架构的福音」定位 Fast Paxos，需补工业结论 | 补：2026 年 Fast Paxos **无主流开源生产实现**。降低延迟的主流做法是 **Multi-Raft 分组 + 就近 Leader**（TiKV **16,878★**、CockroachDB **32,508★**）与 **ReadIndex 本地读**（etcd **52,310★**）。本章应作为「延迟—quorum 取舍」的思路训练，而非选型依据 |
| 7 | 🔧 本书未说明「冲突恢复」的代价曲线 | 补：Fast Paxos 的延迟是**双峰**的——无冲突 2 步、冲突时 ≥ 3 步且需额外恢复轮。工程上要看 **P99 延迟**，而不仅是「最好情况快一跳」 |
| 8 | 🔧 本书未给出 EPaxos 对 Fast Paxos 的超越 | 补：EPaxos（SOSP 2013）用 $2f+1$ 个节点就能在多数场景两步决定，靠的是**依赖图 + 冲突检测**而非更大 quorum；但它的恢复路径更复杂，且 **EPaxos Revisited（NSDI 2021）**发现了原协议恢复流程的正确性问题 |
| 9 | 🔧 本书未给出 2025 年的理论更新 | 补：**Revisiting Lower Bounds for Two-Step Consensus（PODC 2025）**指出 Lamport 的经典下界 $\max\{2e+f+1, 2f+1\}$ 与实际协议（EPaxos）之间的差距源于「快」的定义；论文给出了更贴近实践的下界（作为对象时为 $\max\{2e+f-1, 2f+1\}$）。这是本章议题的最新进展 |

## 与其他章 / 其他书的联系

**本目录内**

- [04-Paxos.md](04-Paxos.md)：本章是它的「延迟优化版」，quorum 相交的论证直接沿用。
- [09-Paxos变种算法的发展史.md](09-Paxos变种算法的发展史.md)：Generalized Paxos 与 Fast Paxos 同年提出，两者常被一起引用；本章与 7.3 对读最佳。
- [11-EPaxos.md](11-EPaxos.md)：EPaxos 是对「$3f+1$ 太贵」的回应，是本章的直接续篇。
- [08-Raft工程实践与SOFAJRaft.md](08-Raft工程实践与SOFAJRaft.md)：ReadIndex/Lease Read 是 2026 年「降低延迟」的实际答案，与本章形成「协议内优化 vs 系统层优化」的对照。

**跨书**

- [../深入理解分布式系统/06-Paxos与Multi-Paxos及其变体.md](../深入理解分布式系统/06-Paxos与Multi-Paxos及其变体.md)：Paxos 变体的另一份中文整理。
- [../分布式算法/06-网络共识与选举.md](../分布式算法/06-网络共识与选举.md)：共识下界与消息复杂度的理论视角。
- [../分布式数据库入门进阶与实战/09-共识算法.md](../分布式数据库入门进阶与实战/09-共识算法.md)：工程视角判断「要不要为延迟改协议」。
- [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)：把「就近访问/分区放置」放回架构设计语境。
</content>
