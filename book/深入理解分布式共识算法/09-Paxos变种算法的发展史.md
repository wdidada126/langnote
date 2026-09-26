# 第 9 章 Paxos 变种算法的发展史

> 覆盖原书第 7 章（第 3 篇「Paxos变种算法集合」，P228–240）：
> 7.1 Disk Paxos简介（算法描述 / 小结）；7.2 Cheap Paxos简介（算法描述 / 小结）；7.3 Generalized Paxos简介；
> 7.4 Stoppable Paxos简介；7.5 Mencius简介；7.6 Vertical Paxos简介（算法描述 / 算法模拟 / 小结）；7.7 本章小结。

## 本章地图

本章是全书**最像「论文导读」的一章**：六个变种，每一个都针对「经典 Paxos 的某一个具体痛点」提出改造。

| 变种 | 想解决的痛点 | 核心手段 |
| --- | --- | --- |
| **Disk Paxos**（7.1） | 处理器数量不足以做 quorum | 把 acceptor 角色交给**共享磁盘**，容错从处理器转移到磁盘 |
| **Cheap Paxos**（7.2） | 要凑 $2f+1$ 个「真节点」太贵 | 稳态只用 $f+1$ 个主节点 + $f$ 个**廉价辅助节点**（故障时启用） |
| **Generalized Paxos**（7.3） | 所有命令被迫全序，太保守 | 利用命令**可交换性**：不冲突的命令可乱序，只记录依赖 |
| **Stoppable Paxos**（7.4） | 一个慢/故障 proposer 占住 ballot 会卡住整轮 | 允许 coordinator **主动停止**未完成的一轮并重开 |
| **Mencius**（7.5） | 单 Leader 在广域网下成为瓶颈与延迟源 | **轮转 Leader**：每个节点负责一部分 instance |
| **Vertical Paxos**（7.6） | 成员变更（换配置/换主）流程笨重 | 把「配置变更」外包给**配置管理器**，常规共识只面对当前配置 |

读法建议：本章**不要按算法细节背**，而应按「**它放宽/替换了经典 Paxos 的哪一条假设**」来记——这是理解第 8、9 章（Fast Paxos、EPaxos）的前提。

## 核心精讲

### 7.1 Disk Paxos：把 acceptor 换成磁盘

- **场景**：处理器只有 2 个（不够 $2f+1$），但磁盘有 ≥3 个（Gafni & Lamport 在论文里说明需求来自 DEC 存储部门）。
- **做法**：处理器（proposer/learner）通过**共享磁盘网络**通信；磁盘充当 acceptor，用「磁盘块」记录 ballot 与已接受值。
- **性质**：只要**多数磁盘可用**，即使只剩一个处理器存活，系统仍能推进。
- **代价**：对磁盘的读写有「部分失败」语义（写一半掉电），需要额外的磁盘块协议处理；论文后来被 Jaskelioff 用 Isabelle/HOL 机械验证并发现了若干小错误（Lamport 本人在其主页上提及此事，并把 Disk Paxos 作为「并发算法机械验证的测试样例」保留未改）。

```text
// 教学示意：Disk Paxos 的角色映射（不参与构建、不编译、不运行）
// 经典 Paxos:   proposer=进程, acceptor=进程, learner=进程
// Disk Paxos:   proposer=处理器(进程), acceptor=磁盘(共享存储), learner=处理器
// 容错来源：不再依赖「多数处理器存活」，而依赖「多数磁盘可访问」
```

### 7.2 Cheap Paxos：用廉价节点凑容错

- **配置**：$f+1$ 个**主 acceptor**（参与稳态）+ $f$ 个**辅助 acceptor**（只在主 acceptor 故障时启用），总数仍是 $2f+1$。
- **典型例子**：$f=1$ 时，2 个主节点 + 1 个辅助节点。稳态只需 2 个节点参与；其中一个挂了，才唤醒辅助节点补齐 quorum。
- **辅助节点可以很便宜**：不存完整数据、只记录 ballot/值，甚至可以是一台小虚拟机或专用见证服务。
- **思想遗产**：现代系统里的 **witness / tiebreaker / arbiter 副本**（只投票不存数据的第三副本）就是这一思路的直系后代。

### 7.3 Generalized Paxos：利用「命令可交换」

经典 Paxos 对所有命令强制**全序**，但有些命令之间其实**无冲突**（如修改不同 key 的两条写），顺序无关紧要。

- **做法**：把「选一个值」改成「**选一组可交换的命令 + 记录它们之间的依赖**」；acceptor 可以接受不同的**命令序列**，只要这些序列在「不可交换的命令」上保持一致。
- **结果**：无冲突的命令可以在**一轮**内提交（类似快路径），有冲突的才需要额外的协调轮。
- **历史地位**：**EPaxos（本目录 [11-EPaxos.md](11-EPaxos.md)）就是 Generalized Paxos 思想的实现**——EPaxos 论文自称是 Generalized Paxos 的一个实例化。

### 7.4 Stoppable Paxos：能「停掉」一轮

- **痛点**：经典 Paxos 中，一个 proposer 用高 ballot 开了轮次后若变慢或崩溃，其他 proposer 必须等它（或用更高 ballot 抢占，但已发出的 accept 消息仍可能在后续造成干扰）。
- **做法**：引入 **Stop 消息**：coordinator 可以主动宣布「这一轮作废」，让所有 acceptor 回到一个干净状态，再由新的 proposer 用新 ballot 重开。
- **收益**：避免单个故障 proposer 长期占据 ballot 导致的吞吐塌陷。

### 7.5 Mencius：广域网下的轮转 Leader

- **痛点**：单 Leader 模式下，跨地域部署时**所有写都要绕经 Leader**，远端客户端延迟高、Leader 带宽成为瓶颈。
- **做法**：把 instance 编号**静态分配**给各节点（例如按 $i \bmod n$），每个节点是自己那部分 instance 的 Leader；无写入时用「跳过（skip）」消息宣布放弃自己的槽位，避免阻塞。
- **代价**：
  - 需要额外的 skip 消息，空闲时也有开销；
  - **慢节点会拖累整体**（它的槽位必须被 skip 或被抢占才能推进），论文设计了「laggard 处理」机制；
  - 实际吞吐对负载分布敏感。

### 7.6 Vertical Paxos：把重配置变成一等公民

- **痛点**：成员变更（增/删副本、换主）在经典 Paxos 里要经历复杂且低效的过程。
- **做法**：引入一个**配置管理器（configuration master / reconfiguration master）**：
  - 常规共识只在「当前配置」内进行， ballot 与 instance 的推进不关心变更；
  - 变更由配置管理器发起，把「旧配置 → 新配置」的切换本身作为一次**跨配置的共识**（需要新旧两个 quorum 参与一次交接）；
  - 交接完成后，新配置独立运行。
- **直觉**：把「横向（一次一个值）」的共识与「纵向（一次换配置）」的共识分开——这也是 *Vertical* 名字的由来。

```text
// 教学示意：Vertical Paxos 的两个维度（不参与构建、不编译、不运行）
// 横向：config_k 内部，对 instance i 的值做共识（普通 Paxos）
// 纵向：config_k -> config_{k+1} 的切换，由 configuration master 驱动，
//       需要 old-quorum 与 new-quorum 同时确认「交接点」
```

### 六个变种的「假设对照」一览

读本章的正确姿势是看**每个变种改了哪一条假设**，而不是记算法细节：

| 变种 | 放宽/替换的假设 | quorum 或节点数变化 | 主要代价 |
| --- | --- | --- | --- |
| Disk Paxos | 「acceptor 必须是进程」→ 换成磁盘 | 容错依赖**多数磁盘**而非多数处理器 | 需要处理磁盘的「部分写」语义 |
| Cheap Paxos | 「所有 acceptor 等价」→ 主/辅不对称 | 总数仍 $2f+1$，稳态只需 $f+1$ 个主节点参与 | 主节点故障时要唤醒辅助节点，恢复变慢 |
| Generalized Paxos | 「所有命令必须全序」→ 只给冲突命令定序 | 不变（$2f+1$） | 需要维护依赖信息，协议复杂度上升 |
| Stoppable Paxos | 「一轮一旦开启就必须走完」→ 可中止 | 不变 | 引入 Stop 消息与轮次管理 |
| Mencius | 「必须有一个 Leader」→ 轮转 Leader | 不变 | skip 消息开销；慢节点拖累 |
| Vertical Paxos | 「配置固定」→ 重配置外包给配置管理器 | 变更时需新旧两个 quorum 参与交接 | 引入配置管理器这一新组件 |

> 一句话总结：这六个变种**没有一个是「全面更强」**，它们都是「在某一种特定约束下更合适」。这也是它们未能成为通用标准的原因。

## 版本演进

- **1999–2000**：Disk Paxos（DISC 2000）——「谁来当 acceptor」第一次被抽象掉；
- **2004**：Cheap Paxos（DSN 2004）——「副本可以不对称」；
- **2005**：Generalized Paxos（MSR-TR）——「命令不必全序」；同年 Fast Paxos（本目录 [10-Fast-Paxos.md](10-Fast-Paxos.md)）提出「省一个消息延迟」；
- **2008**：Stoppable Paxos（MSR-TR）与 Mencius（OSDI 2008）——分别处理「慢 proposer」与「单 Leader 瓶颈」；
- **2009–2010**：Vertical Paxos（PODC 2009）与 Reconfiguring a State Machine（SIGOPS OSR 2010）——重配置被系统化；
- **2013**：EPaxos（SOSP 2013）把 Generalized Paxos 落地；
- **2016**：Flexible Paxos（OPODIS 2016）给出更一般的 quorum 相交条件，是这一族**最近一次有影响力的理论推进**；
- **2023（本书）**：把这六个变种串成一条「变种史」，是中文材料中少见的整理；
- **2026 视角**：这些变种**几乎没有直接的生产落地**，但它们的思想（witness 副本、命令可交换性、重配置与常规共识分离、quorum 可调）已经**渗入**主流系统。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Gafni & Lamport《Disk Paxos》 | DISC 2000（LNCS 1914, 330–344）；期刊版 *Distributed Computing* 16(1):1–20, 2003 | 用共享磁盘做 acceptor |
| Lamport & Massa《Cheap Paxos》 | DSN 2004 | 主 acceptor + 廉价辅助 acceptor |
| Lamport《Generalized Consensus and Paxos》 | MSR-TR-2005-33, 2005 | 命令可交换性与依赖图 |
| Lamport《Fast Paxos》 | MSR-TR-2005-112；*Distributed Computing* 19(2), 2006 | 快路径（[10-Fast-Paxos.md](10-Fast-Paxos.md)） |
| Lamport《Stoppable Paxos》 | MSR-TR-2008-46, 2008 | 可中止的轮次 |
| Mao, Chen, Vadhat《Mencius: Building Efficient Replicated State Machines for WANs》 | OSDI 2008 | 广域网下的轮转 Leader |
| Lamport, Malkhi, Zhou《Vertical Paxos and Primary-Backup Replication》 | PODC 2009 | 重配置与常规共识分离 |
| Lamport, Malkhi, Zhou《Reconfiguring a State Machine》 | ACM SIGOPS OSR 2010 | 重配置的规范思路 |
| Howard, Malkhi, Spiegelman《Flexible Paxos: Quorum Intersection Revisited》 | OPODIS 2016 | quorum 相交条件可以放宽 |
| Moraru, Andersen, Kaminsky《There Is More Consensus in Egalitarian Parliaments》 | SOSP 2013 | EPaxos（[11-EPaxos.md](11-EPaxos.md)） |

## 近年研究与工业界开源实践（2015–2026）

> star 数均为 2026-09 用 `gh api repos/OWNER/REPO --jq '.stargazers_count'` 实测。

- **这一章最诚实的一句话**：上述六个变种**没有对应的主流开源实现**。2026 年在生产里跑的共识，几乎全部是 **Raft 生态**或 **Multi-Paxos 的工程变体**，加上少量 BFT：

| 系统 / 库 | star | 与本章的关系 |
| --- | --- | --- |
| `etcd-io/etcd` | 52,310★ | Raft 生态核心；无变种算法落地 |
| `etcd-io/raft` | 1,128★ | Raft 库 |
| `hashicorp/raft` | 9,136★ | Raft 库 |
| `sofastack/sofa-jraft` | 3,824★ | Java Raft |
| `Tencent/phxpaxos` | 3,379★ | Multi-Paxos（非本章变种） |
| `baidu/braft` | 4,227★ | C++ Raft |
| `tikv/tikv` / `cockroachdb/cockroach` | 16,878★ / 32,508★ | Multi-Raft 分组 |

- **思想遗产的落地位置**（这些变种「活着」的地方）：
  - **Cheap Paxos → witness/tiebreaker 副本**：只投票不存数据的第三副本，在许多分布式存储与数据库里以「仲裁副本 / 轻量副本」形式出现；
  - **Generalized Paxos → EPaxos → 依赖图思想**：虽未大规模落地，但「无冲突命令可并行提交」成为后续研究（含 BFT 侧）的常用思路；
  - **Vertical Paxos → 重配置独立化**：现代系统的「成员变更作为一条特殊日志 + 双 quorum 交集」与之一脉相承；
  - **Disk Paxos → 共享存储架构**：其「容错不再依赖多数处理器」的思想，与云原生的**存算分离**（共享存储 + 多计算节点）在架构动机上呼应；
  - **Flexible Paxos → quorum 可调**：把 Phase-1/Phase-2 quorum 解耦，是这一族近十年最有工程潜力的理论结果。
- **近年研究**：
  - **EPaxos Revisited**（NSDI 2021）指出原始 EPaxos 的**恢复流程存在长期未被发现的正确性问题**——这提醒本章读者：**「去中心化」类协议的复杂度主要在恢复路径**；
  - **Revisiting Lower Bounds for Two-Step Consensus**（PODC 2025）重新审视了「两步共识所需进程数」的下界，指出 Lamport 的经典下界与实际协议（如 EPaxos）之间的差距来自「快」的定义——这是本章涉及的 Fast/EPaxos 议题在 2025 年的最新进展。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Disk Paxos 是把日志写到磁盘的 Paxos」 | 磁盘是 **acceptor（投票者）**，不是存储介质；容错来源从「多数处理器」变为「多数磁盘」 |
| 2 | 「Cheap Paxos 只需 $f+1$ 个节点就能容忍 $f$ 个故障」 | 总数仍是 $2f+1$；$f$ 个辅助节点**只在主节点故障时参与**，稳态不参与 |
| 3 | 「Generalized Paxos 放弃了顺序保证」 | 它放弃的是「**所有**命令全序」；不可交换（冲突）的命令之间仍必须定序 |
| 4 | 「Mencius 解决了广域网延迟」 | 它降低了「远端写必须绕 Leader」的延迟，但引入 skip 开销与**慢节点拖累**问题 |
| 5 | 「Vertical Paxos 是一种全新的共识」 | 它是对**重配置流程**的重构；常规路径仍是 Paxos |
| 6 | 🔧 本书按「变种史」讲授，需明确给出工业落地情况 | 补：这六个变种**都没有主流开源生产实现**。2026 年的事实标准是 Raft 生态（etcd **52,310★**、hashicorp/raft **9,136★**、sofa-jraft **3,824★**）与 Multi-Raft 分组（TiKV **16,878★**、CockroachDB **32,508★**）。本章的正确读法是**当作设计空间地图**，不是选型清单 |
| 7 | 🔧 本书未提及这一族在 2016 年后的理论推进 | 补：**Flexible Paxos**（Howard, Malkhi, Spiegelman，OPODIS 2016）证明「所有 quorum 两两相交」是过强要求，只需 Phase-1 与 Phase-2 quorum 相交；这直接给了工程上「缩小热路径 quorum、放大换主 quorum」的自由度 |
| 8 | 🔧 Generalized Paxos 的下游（EPaxos）存在正确性争议 | 补：**EPaxos Revisited（NSDI 2021）**发现原 EPaxos 的恢复协议存在长期未被发现的问题；因此「去中心化共识」类协议在采用前应重点审查**恢复路径**，并要求形式化规格或模型检查证据 |
| 9 | 🔧 本书未给出「如何验证变种实现」 | 补：Disk Paxos 的论文就曾被人用 Isabelle/HOL 机械验证后发现小错误（Lamport 本人在其公开主页上说明了此事）。这提示：**越是小众变种，越需要机械验证**；生产采用需有 TLA+/模型检查证据 |

## 与其他章 / 其他书的联系

**本目录内**

- [04-Paxos.md](04-Paxos.md) / [05-Multi-Paxos与PhxPaxos工程实现.md](05-Multi-Paxos与PhxPaxos工程实现.md)：本章的每个变种都是对前两章「经典 Paxos 假设」的放宽。
- [10-Fast-Paxos.md](10-Fast-Paxos.md)：与本章同年（2005）提出的「省一个消息延迟」方案，常与 Generalized Paxos 一起被引用。
- [11-EPaxos.md](11-EPaxos.md)：Generalized Paxos 的直接实现；本章 7.3 是它的理论前传。
- [08-Raft工程实践与SOFAJRaft.md](08-Raft工程实践与SOFAJRaft.md)：Mencius 想解决的「单 Leader 瓶颈」，在 2026 年是用 **Multi-Raft 分组**解决的，而不是轮转 Leader。

**跨书**

- [../深入理解分布式系统/06-Paxos与Multi-Paxos及其变体.md](../深入理解分布式系统/06-Paxos与Multi-Paxos及其变体.md)：同主题的另一份中文整理，可与本章对读。
- [../分布式算法/06-网络共识与选举.md](../分布式算法/06-网络共识与选举.md)：从算法理论角度给出共识问题的下界与变体分类。
- [../分布式数据库入门进阶与实战/09-共识算法.md](../分布式数据库入门进阶与实战/09-共识算法.md)：工程视角判断「这些变种值不值得用」。
- [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)：把「witness 副本」「重配置」等放回架构选型语境。
</content>
