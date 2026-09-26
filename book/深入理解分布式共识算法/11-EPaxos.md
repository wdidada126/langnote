# 第 11 章 EPaxos——去中心化共识

> 覆盖原书第 9 章（第 3 篇「Paxos变种算法集合」，P255–288）：
> 9.1 EPaxos简介（共识算法对比 / 认识EPaxos算法 / 基本概念）；
> 9.2 协商协议（Prepare / PreAccept / Paxos-Accept / Commit / 特殊的Quorum）；
> 9.3 执行协议（互相依赖 / 执行过程 / 拓扑排序 / 寻找强连通分量 / EPaxos排序）；
> 9.4 算法证明（执行的一致性 / 执行的顺序性）；9.5 Optimized-EPaxos简介（Prepare阶段 / 论证QuorumFast）；
> 9.6 算法模拟（协商协议 / Prepare阶段）；9.7 成员变更；9.8 工程优化（巨大的消息体 / 读请求处理）；
> 9.9 本章小结（与Paxos的异同 / 与Raft、ZAB、Multi Paxos的异同）；9.10 练习题。

## 本章地图

本章是全书「第 3 篇」的技术顶点：EPaxos（Egalitarian Paxos，SOSP 2013）要解决的问题是——**能不能既不要 Leader，又能一步提交？**

```
Leader-based（Paxos/Raft/ZAB）：所有写都绕经 Leader
   ├─ 优点：定序简单（Leader 说了算）
   └─ 缺点：远端客户端延迟高、Leader 是瓶颈、换主期间不可用

EPaxos：任何副本都能当「本次命令的 leader」（command leader）
   ├─ 无冲突命令：PreAccept 一轮即可提交（fast path）
   ├─ 有冲突命令：用「依赖」记录顺序，走 Paxos-Accept（slow path）
   └─ 执行阶段：按依赖图做拓扑排序 + 强连通分量内按 seq 排序
```

- **9.1–9.2**：协商协议（PreAccept / Paxos-Accept / Commit）与特殊的 quorum 取值；
- **9.3**：**执行协议**——本章最独特的部分：共识时不直接定全序，而是在**执行时**按依赖图定序；
- **9.4–9.5**：正确性论证与 Optimized-EPaxos（缩小快路径 quorum）；
- **9.7–9.8**：成员变更与两个真实工程痛点（消息体膨胀、读请求处理）。

## 核心精讲

### 9.1 认识 EPaxos

**核心想法**：把「**全局定序**」换成「**记录冲突依赖**」。

- 两条**不冲突**（操作不同的 key）的命令，谁先谁后无所谓 → 各自一步提交；
- 两条**冲突**（操作同一个 key）的命令，必须定序 → 用 `deps`（依赖集）记录「我依赖于谁」，执行时再定序。

**基本概念**：

| 概念 | 含义 |
| --- | --- |
| **instance** | 每个副本上的命令槽位，用 `(replicaId, instanceId)` 标识 |
| **command leader** | 某条命令的发起副本——**只对这条命令负责**，不是全局 Leader |
| **deps（依赖集）** | 与该命令**冲突**、且已知的其他命令集合 |
| **seq（序列号）** | 用于打破依赖环：`seq = max(deps 中的 seq) + 1` |
| **attributes** | `(deps, seq, status)`，命令的三元组属性；协商的对象就是它 |

### 9.2 协商协议

```text
// 教学示意：EPaxos 的两条路径（不参与构建、不编译、不运行）
// 设 N = 2F+1（F = 可容忍故障数）
//   fast-path quorum  = F + floor((F+1)/2)   （含 command leader；N=5 时为 3）
//   slow-path quorum  = F + 1                （简单多数；N=5 时为 3）

fn replicate(cmd):                            // 本副本作为 command leader
    deps, seq = localScanConflicts(cmd)       // 本地扫描已知冲突命令
    replies = sendPreAccept(fastQuorum, cmd, deps, seq)
    // 快路径条件：所有回复的 (deps, seq) 完全一致
    if allIdentical(replies):
        commit(cmd, deps, seq)                // fast path：一步提交
    else:
        deps = union(all deps); seq = max(all seq)
        ok = sendPaxosAccept(majority, cmd, deps, seq)   // slow path
        commit(cmd, deps, seq)
```

**四个阶段（对应 9.2.1–9.2.4）**：

| 阶段 | 作用 |
| --- | --- |
| **PreAccept**（9.2.2） | 探测冲突：各副本回复「我这边还有哪些冲突命令」，command leader 汇总 |
| **Paxos-Accept**（9.2.3） | 快路径失败时的慢路径：用多数派（$F+1$）确认合并后的 `(deps, seq)` |
| **Commit**（9.2.4） | 广播最终 `(deps, seq)` |
| **Prepare**（9.2.1） | 恢复阶段：某条命令的 command leader 故障后，由其他副本重新协商其属性 |

**9.2.5 特殊的 Quorum**：EPaxos 的快路径 quorum 是
$\;F + \lfloor (F+1)/2 \rfloor\;$（含 command leader），慢路径 quorum 是 $\;F+1\;$。
以 $N=5$（$F=2$）为例：**快路径 quorum = 3，与简单多数相同**——这正是 EPaxos 相对 Fast Paxos（需要 $3f+1$ 个节点）的关键优势。

> ⚠️ 本书 9.2.5 / 9.5.2 给出的具体推导步骤**未能核实原文**（大纲只给小节名）。上面的取值来自 EPaxos 论文与技术报告（CMU-PDL-13-111）中给出的公式，属于该论文的原始结论。

### 9.3 执行协议：依赖图 → 拓扑排序 → 强连通分量

这是 EPaxos 最有辨识度的部分：

1. **9.3.1 互相依赖**：命令 A 依赖 B、B 又依赖 A 是可能的（并发冲突），形成环；
2. **9.3.2 执行过程**：副本本地已有所有命令的 `(deps, seq)`，据此构造**依赖图**；
3. **9.3.3 拓扑排序**：先按依赖图做拓扑排序；
4. **9.3.4 寻找强连通分量（SCC）**：环上的命令属于同一个 SCC，无法用拓扑排序分开；
5. **9.3.5 EPaxos 排序**：**SCC 之间**按逆拓扑序执行；**SCC 内部**按 `seq` 排序（`seq` 相同则按 instance id 之类的确定性 tie-break）。

```text
// 教学示意：EPaxos 执行算法（不参与构建、不编译、不运行）
fn execute(cmd):
    visited = {}
    buildDependencyGraph(cmd, visited)          // 递归展开 deps，构造有向图
    sccs = tarjan(visited)                      // 求强连通分量
    for comp in reverseTopologicalOrder(sccs):  // 分量间按逆拓扑序
        for c in sortBy(comp, key = seq):       // 分量内按 seq（再按 id 打破平局）
            apply(c)
```

> **为什么要 SCC**：如果依赖图无环，拓扑排序足以给出执行顺序；一旦出现环（并发冲突互相依赖），必须把环上的命令当作一个**整体**处理，并在内部用 `seq` 定序——所有副本只要按同一规则，就会得到**相同的执行顺序**。这正是 9.4「执行的一致性/顺序性」要证明的东西。

### 9.5 Optimized-EPaxos

**动机**：基本版 EPaxos 把 PreAccept 发给所有副本（non-thrifty），消息量大。

**优化（9.5.1）**：

- **thrifty 模式**：只发给一个快路径 quorum（含自己）；
- 由此可以把快路径 quorum 从 $2F$ 降到 $\;F + \lfloor (F+1)/2 \rfloor\;$（9.5.2 论证）；
- 附加条件 **FP-deps-committed**：快路径提交时，要求 `deps` 里的每条命令已至少被 quorum 中某个副本标记为 committed，以保证 `seq` 不再变化；
- 另一种变体（$N \le 7$ 时）用 **Accept-Deps**（在 Accept/AcceptReply 上附带更新后的依赖列表）替代该条件，且**不影响快路径命中率**。

> 来源说明：以上细节出自 EPaxos 的正确性证明技术报告（CMU-PDL-13-111）；本书 9.5 的具体表述未能核实，存疑。

### 9.7–9.8 成员变更与工程优化

- **9.7 成员变更**：需要同时保证「新旧配置的 quorum 相交」与「依赖图的完整性」（变更期间命令可能引用旧配置的 instance），比 leader-based 协议更复杂。
- **9.8.1 巨大的消息体**：`deps` 集合随并发冲突数增长 → PreAccept 消息体会**不断膨胀**。这是 EPaxos 在高冲突负载下的核心工程痛点。
- **9.8.2 读请求处理**：读也要考虑依赖——一个读必须等它依赖的所有命令执行完，且要保证读到一致的状态。相比「Leader 直接本地读 + ReadIndex」，EPaxos 的读路径明显更绕。

## 版本演进

- **2013**：Moraru、Andersen、Kaminsky 在 SOSP 2013 发表《There Is More Consensus in Egalitarian Parliaments》，提出 EPaxos；同期技术报告（CMU-PDL-13-111）给出正确性证明与 Optimized-EPaxos；
- **2014**：后续分析指出原始 EPaxos 的**完整恢复协议并未写在 SOSP 论文里，而在技术报告中**——这本身就是复杂度的信号；
- **2021**：**《EPaxos Revisited》（NSDI 2021）**系统审查 EPaxos，指出其**恢复流程存在长期未被发现的正确性问题**，并给出修正；
- **2023（本书）**：把协商/执行两段协议与证明脉络完整讲一遍，是中文材料中少见的系统介绍；
- **2025**：PODC 2025 的《Revisiting Lower Bounds for Two-Step Consensus》从理论上解释「为什么 EPaxos 能用 $2f+1$ 个节点达成两步决定」（放宽了「快」的定义）；
- **2026 视角**：EPaxos 仍**无主流开源生产实现**；「避免 Leader 瓶颈」的需求在工程上用 **Multi-Raft 分组 + 就近 Leader** 解决，而不是用去中心化协议。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Moraru, Andersen, Kaminsky《There Is More Consensus in Egalitarian Parliaments》 | SOSP 2013 | **EPaxos 主论文** |
| Moraru, Andersen, Kaminsky《A Proof of Correctness for Egalitarian Paxos》 | CMU-PDL-13-111（技术报告） | 正确性证明、恢复协议、Optimized-EPaxos |
| Lamport《Generalized Consensus and Paxos》 | MSR-TR-2005-33, 2005 | 命令可交换性（EPaxos 的思想源头） |
| Lamport《Fast Paxos》 | MSR-TR-2005-112；*Distributed Computing* 19(2), 2006 | 两步共识的下界（[10-Fast-Paxos.md](10-Fast-Paxos.md)） |
| Tollman, Park, Ousterhout《EPaxos Revisited》 | NSDI 2021 | 指出原 EPaxos 恢复流程的正确性问题并修正 |
| Ryabinin, Gotsman, Sutra《Revisiting Lower Bounds for Two-Step Consensus》 | PODC 2025 | 重新解释 EPaxos 与经典下界的差距 |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | 对照物：Leader-based 路线的代表 |

## 近年研究与工业界开源实践（2015–2026）

> star 数均为 2026-09 用 `gh api repos/OWNER/REPO --jq '.stargazers_count'` 实测。

- **落地情况（诚实结论）**：EPaxos **没有主流开源生产实现**。2026 年生产系统的共识层仍然是 Leader-based 阵营：

| 系统 / 库 | star | 说明 |
| --- | --- | --- |
| `etcd-io/etcd` | 52,310★ | Raft 生态核心 |
| `etcd-io/raft` | 1,128★ | Raft 库 |
| `hashicorp/raft` | 9,136★ | Raft 库 |
| `sofastack/sofa-jraft` | 3,824★ | Java Raft |
| `tikv/tikv` | 16,878★ | Multi-Raft 分组 + PD 调度 |
| `cockroachdb/cockroach` | 32,508★ | Multi-Raft + 地理分区（geo-partitioning） |
| `Tencent/phxpaxos` | 3,379★ | Multi-Paxos（Leader-based） |

- **为什么「换个 Leader 就能解决」**：EPaxos 想解决的痛点是「远端客户端必须绕经固定 Leader」。工程上更便宜的解法是
  **Multi-Raft 分组 + 把 Leader 调度到离客户端近的位置**（CockroachDB 的 geo-partitioning、TiKV 的 Placement Rules）——
  它保留了 Leader-based 的简洁性，同时达到了「就近提交」的效果。这是 EPaxos 未被大规模采用的根本原因。
- **近年研究**：
  - **EPaxos Revisited（NSDI 2021）**：发现原协议恢复流程的正确性问题，并给出修正版本；
  - **依赖图 + 冲突检测**的思想被移植到 BFT 与高吞吐复制研究中；
  - **PODC 2025** 的下界重估，把「EPaxos 为何能用更少进程」从「违反下界」变成「定义差异」的清晰解释。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「EPaxos 完全没有 Leader」 | 每条命令有一个 **command leader**（发起该命令的副本），只是它不是全局 Leader、也不需要选举 |
| 2 | 「快路径一定快」 | 快路径要求所有 quorum 成员返回的 `(deps, seq)` **完全一致**；冲突一多就命中不了，退化为慢路径 |
| 3 | 「快路径 quorum 与多数派一样大，所以一定命中」 | quorum 大小只决定「能否一步提交」的门槛；命中率取决于**冲突率** |
| 4 | 「依赖图有环就没法执行」 | 有环时用 **SCC（强连通分量）** 打包，分量内按 `seq` 定序；所有副本按同一规则得到同一顺序 |
| 5 | 「EPaxos 的复杂度在协商阶段」 | 主要在**恢复阶段**——恢复要重建命令属性，且原协议在此处被发现过问题（🔧 见下） |
| 6 | 🔧 本书未说明 EPaxos 的落地现状与正确性争议 | 补：**EPaxos 至今无主流开源生产实现**；且 **《EPaxos Revisited》（NSDI 2021）**指出原协议**恢复流程存在长期未被发现的正确性问题**。采用前应要求形式化规格或模型检查结果（EPaxos 有公开的 TLA+ 规格可作为起点） |
| 7 | 🔧 本书未说明「去中心化」的工程替代方案 | 补：2026 年解决「Leader 瓶颈/远端延迟」的主流做法是 **Multi-Raft 分组 + 就近 Leader**（TiKV **16,878★**、CockroachDB **32,508★**），复杂度远低于依赖图；本章应作为思路训练而非选型依据 |
| 8 | 🔧 本书 9.8.1「巨大的消息体」需要给出量级判断 | 补：`deps` 随并发冲突数线性增长，PreAccept 消息体会**随负载膨胀**——这使得 EPaxos 在**高冲突**工作负载下比 Leader-based 更差。它的适用场景是**低冲突 + 地理分布**，而不是通用高吞吐 |
| 9 | 🔧 本书未覆盖 EPaxos 的读路径难题 | 补：读也要处理依赖（必须等依赖命令执行完），比「ReadIndex 本地读」复杂得多。这正是 Leader-based 协议在工程上更受欢迎的原因之一 |

## 与其他章 / 其他书的联系

**本目录内**

- [09-Paxos变种算法的发展史.md](09-Paxos变种算法的发展史.md)：7.3 Generalized Paxos 是本章的直接理论前传——EPaxos 论文自称是它的实例化。
- [10-Fast-Paxos.md](10-Fast-Paxos.md)：两者都在追求「两步决定」；Fast Paxos 用更大的 quorum（$3f+1$），EPaxos 用依赖图（$2f+1$）。**本章与第 10 章必须连读**。
- [04-Paxos.md](04-Paxos.md) / [05-Multi-Paxos与PhxPaxos工程实现.md](05-Multi-Paxos与PhxPaxos工程实现.md)：9.9.1「EPaxos 与 Paxos 的异同」的基础。
- [07-Raft.md](07-Raft.md) / [08-Raft工程实践与SOFAJRaft.md](08-Raft工程实践与SOFAJRaft.md)：9.9.2「与 Raft、ZAB、Multi-Paxos 的异同」的对照对象；也是「去中心化 vs 分组就近」的选型对照。

**跨书**

- [../深入理解分布式系统/06-Paxos与Multi-Paxos及其变体.md](../深入理解分布式系统/06-Paxos与Multi-Paxos及其变体.md)：Paxos 变体的另一份中文整理，含 EPaxos。
- [../分布式算法/06-网络共识与选举.md](../分布式算法/06-网络共识与选举.md)：共识的算法级分类与下界。
- [../分布式数据库入门进阶与实战/09-共识算法.md](../分布式数据库入门进阶与实战/09-共识算法.md)：工程视角判断「要不要引入去中心化共识」。
- [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)：把「分组 + 就近放置」放回架构设计语境。
</content>
