# 第 3 章 共识（理论篇）

> **本章地图**：共识 ≠ 一致性（3.1）→ 拜占庭将军问题（3.2）→ 容错性分级：CFT / BFT（3.3）
> → 共识算法总览（3.4）→ **Paxos**（3.5：提出与证明 / 内容 / 实现分析 / 理解与示例）
> → **Raft**（3.6：内容 / 保证 / 总结分析）→ 引出实践篇的锁与事务。

## 本章地图

- 位置：理论篇第 3 章，紧接第 2 章的「一致性」。
  - 3.1 先把 **consensus（共识）**与 [02](02-一致性的概念与强弱.md) 讲的 **consistency（一致性）**分开；
  - 3.2–3.3 给出**故障模型**（节点会怎么坏）与**容错门限**（要多少台机器才够）；
  - 3.4–3.6 讲两个具体算法：Paxos 与 Raft。
- 主线（一条因果链）：
  1. 共识要解决的原始问题：**多个节点对一个值达成一致，且这个决定不可反悔**；
  2. 节点可能「撒谎/乱发」→ 拜占庭将军问题 → 需要 `3f+1` 台机器；
  3. 节点只会「停机」→ 崩溃故障 → 只需 `2f+1` 台；
  4. 异步模型下 FLP 说「不可能」→ 实际系统用**超时 + 部分同步**绕开；
  5. Paxos 给出最经典的解，Raft 给出最易实现的解。
- 🔧 本章讲完，读者应能回答三个工程问题：
  **选主怎么做**（Raft election）、**日志怎么复制**（log replication）、**读能不能拿到最新值**（读路径，本书未讲，2026 必补）。

## 核心精讲

（以下伪代码与示意图均为**教学示意，不参与构建**。）

### 3.1 共识与一致性：两个词，两件事

| 维度 | **一致性 Consistency**（第 2 章） | **共识 Consensus**（本章） |
| --- | --- | --- |
| 问题 | 副本「看起来是不是一样」 | 多个节点「**对一个值**达成一致」 |
| 对象 | 通常是**多个数据项**、持续的状态 | **一次决定**（一个值、一条日志、一个提案） |
| 性质 | 是一组**正确性条件**（线性/顺序/因果/最终） | 是一个**算法问题**，有明确的安全性与活性定义 |
| 关系 | 一致性通常**由**共识实现 | 共识是**手段** |

- **共识的四个形式性质**（本书 3.1.1 会给出类似表述）：
  - **协定性（Agreement）**：所有正确节点决定同一个值；
  - **有效性（Validity）**：被决定的值一定是某个节点**提出过**的值（不能凭空产生）；
  - **终止性（Termination）**：所有正确节点最终都会做出决定；
  - **完整性 / 不可反悔（Integrity）**：一个值一旦被决定，就不会再被改成别的值。
- 🔧 「再论一致性」的要点：
  **共识是实现线性一致的通用机器**——把共识用在「日志复制」上，日志顺序全局唯一，
  各节点按同一顺序重放日志，就得到**状态机复制（State Machine Replication, SMR）**；
  这是 etcd、ZooKeeper、TiKV、CockroachDB 的共同骨架。

### 3.2 拜占庭将军问题（3.2）

- 原始表述（Lamport, Shostak, Pease, TOPLAS 1982）：
  几位将军围城，需要通过信使达成一致（一起进攻或一起撤退），
  但**其中可能有叛徒**：叛徒会向不同将军发送不同消息，甚至伪造消息。
- 结论：
  - **口头消息**（无法验证签名）：只有叛徒数 `f < n/3`（即 `n ≥ 3f+1`）时才可解；
  - **签名消息**（不可伪造）：可以做到 `n ≥ f+2`，代价是签名与证书体系。
- 🔧 为什么是 3f+1：
  忠诚将军必须能「**压过**」叛徒制造的分歧——即使 f 个节点全都沉默或都说假话，
  剩下的 `n−f` 个节点里，忠诚者仍须构成多数，于是要求 `n−f > f`，即 `n ≥ 2f+1`；
  但这只解决「沉默」。当叛徒**主动分裂意见**时，需要消息在两个诚实集合间交叉验证，门限提高到 `3f+1`。

### 3.3 容错性：CFT 与 BFT

| 类型 | 故障行为 | 门限 | 典型算法 | 典型场景 |
| --- | --- | --- | --- | --- |
| **崩溃故障容错 CFT**（非拜占庭，3.3.1） | 节点停机、重启、网络丢包；**不会发出矛盾消息** | `2f+1` 台容忍 `f` 台故障 | Paxos、Raft、ZAB | 数据中心内部、企业集群（本书主线） |
| **拜占庭容错 BFT**（3.3.2） | 节点可能**任意行为**：撒谎、串谋、伪造、选择性响应 | `3f+1` 台容忍 `f` 台恶意 | PBFT、PoW/PoS、Tendermint | 区块链、多方可信计算 |

- 🔧 工程判断：**绝大多数后端系统只需要 CFT**。
  数据中心内的机器不会「故意撒谎」，引入 BFT 只会带来三倍以上的机器成本与复杂度。
  只有跨组织/开放网络（公链、联邦）才需要 BFT。
- 🔧 一条常被忽略的边界：**CFT 协议假设节点不会「复活后带着旧身份作乱」**。
  Raft 的 `term`、ZAB 的 `epoch` 就是为了防止旧主复辟（脑裂双主）。

### 3.4–3.5 Paxos

- **三个角色**：Proposer（提案者）、Acceptor（接受者）、Learner（学习者）；实际系统中一个进程常兼三职。
- **两阶段**：
  - **Prepare/Promise**：Proposer 选一个**全局递增**的提案号 `n` 广播 `Prepare(n)`；
    Acceptor 承诺「不再接受编号 < n 的提案」，并回复自己已接受的最高编号提案（若有）。
  - **Accept/Accepted**：Proposer 收到多数派 Promise 后，若发现已有被接受的提案值，
    **必须沿用那个值**（这是安全性的关键），否则用自己的值，广播 `Accept(n, v)`；
    多数派接受后，值 `v` 被**选定（chosen）**。
- **安全性直觉**：
  任意一个值一旦被多数派接受，之后任何提案在 Prepare 阶段**必然会看到它**并被强制沿用 → 不会反悔。
- **Multi-Paxos**：
  单轮 Paxos 只决定**一个值**。要复制一整条日志，需要对每个位置跑一次 Paxos；
  优化办法是**选出一个稳定的 Leader**，由它跳过 Prepare 阶段直接 Accept（后续位置只跑一阶段）→ 这就是 Multi-Paxos。
- 🔧 读 Paxos 最容易卡住的三点（对照本书 3.5.3「算法实现分析」）：
  1. **提案号必须全局唯一且递增**（通常用 `(round, node_id)` 编码）；
  2. **「沿用已接受的值」不是优化，是正确性要求**；
  3. **活锁**：两个 Proposer 交替打断对方的 Prepare → 工程上靠「选主 + 随机退避」解决，这已经是 Raft 的思路了。

### 3.6 Raft：把共识拆成三个子问题

| 子问题 | 机制 | 关键不变量 |
| --- | --- | --- |
| **领导选举（Leader election）** | 任期 `term` 递增；Follower 超时未收心跳 → 变 Candidate → 请求投票；获多数票者成为 Leader | **每个 term 至多一个 Leader**（一任最多投一票 + 多数派交集） |
| **日志复制（Log replication）** | Leader 追加日志并广播 `AppendEntries`，多数派确认后**提交（commit）**，再应用到状态机 | **日志匹配特性**：相同 `(index, term)` 的日志条目必然相同；且之前的日志也相同 |
| **安全性（Safety）** | 选举时**只把票投给日志至少和自己一样新的 Candidate**（比较 `lastTerm/lastIndex`） | **已提交的日志条目在未来的 Leader 上必然存在**（状态机安全） |

- **Raft 的五个保证**（本书 3.6.2 会逐条给出）：
  选举安全、Leader 只追加、日志匹配、Leader 完整性（Completeness）、状态机安全。
- 🔧 **Raft vs Paxos 的关系**：
  **Raft 不是「更强的 Paxos」，而是「更易实现、更易教学的等价物」**（都解同一个问题，都是 CFT、2f+1）。
  Raft 的核心贡献是**强 Leader 模型 + 可理解性**：把「多轮提案竞争」收敛成「一个 Leader 定序」，
  工程上更容易实现成员变更、日志压缩与读路径优化。
- **成员变更**：单步变更节点集合会有「两个多数派不相交」的风险 → 用**联合共识（joint consensus）**或**单节点变更**（一次只加/减一台）保证安全。

### 教学示意：Raft 日志复制与 Paxos 一轮提案

```python
# 教学示意：Raft Leader 的日志复制循环；不参与构建，不运行。
class RaftLeader:
    def append(self, cmd):
        self.log.append(Entry(term=self.term, cmd=cmd))
        acks = 1                                   # 自己这一票
        for f in self.followers:
            if f.append_entries(self.log, self.commit_index):
                acks += 1
        if acks > len(self.cluster) // 2:          # 多数派确认
            self.commit_index = len(self.log) - 1  # 提交
            self.apply_to_state_machine_up_to(self.commit_index)
            return "committed"
        return "not committed（不告诉客户端成功）"

class RaftFollower:
    def on_append_entries(self, prev_index, prev_term, entries, leader_commit):
        # 一致性检查：只有 prev 匹配才接受，否则让 Leader 回退重发
        if not self.log.matches(prev_index, prev_term):
            return False
        self.log.truncate_from(prev_index + 1); self.log.extend(entries)
        self.commit_index = min(leader_commit, len(self.log) - 1)
        return True
```

```python
# 教学示意：Paxos 的 Proposer 一轮；不参与构建，不运行。
class Proposer:
    def run(self, value, acceptors):
        n = self.next_ballot()                     # 全局唯一递增
        promises = [a.prepare(n) for a in acceptors]
        if len(promises) <= len(acceptors) // 2:
            return "no quorum"                     # 可能活锁：改用随机退避重试
        highest = max((p.accepted for p in promises if p.accepted), default=None)
        v = highest.value if highest else value    # ★ 安全性关键：沿用已接受的值
        accepted = [a.accept(n, v) for a in acceptors]
        if len(accepted) > len(acceptors) // 2:
            return f"chosen: {v}"
        return "no quorum"
```

```text
# 教学示意：CFT 与 BFT 的门限（文本图，不参与构建）
CFT  n = 2f+1   容忍 f 台停机     （3 台容忍 1 台，5 台容忍 2 台）
BFT  n = 3f+1   容忍 f 台任意作恶 （4 台容忍 1 台，7 台容忍 2 台）
异步 + 一个崩溃进程 → FLP：不存在既安全又必然终止的确定性共识算法
务实解法：引入超时（部分同步 / 随机化）→ 牺牲「必然终止」的严格性换工程可用
```

## 版本演进

- **版本情况**：本书第 1 版（2022-01）；**第 2 版未核实到，标注「待核验」**。以下记录共识领域的演进。
- **共识的三个时代**：
  1. **1978–1985（奠基与不可能）**：Lamport 的逻辑时钟（CACM 1978）、拜占庭将军问题（TOPLAS 1982）、
      oral messages 的 3f+1 门限、FLP 不可能（JACM 1985）——**先把边界画清楚**；
  2. **1988–2001（可解性）**：Dwork/Lynch/Stockmeyer 的**部分同步**模型（JACM 1988）指出「只要系统最终会稳定下来就能解」，
     Chandra & Toueg 的**不可靠故障检测器**（JACM 1996）给出绕开 FLP 的标准路径；Lamport 的 Part-Time Parliament（TOCS 1998）与 Paxos Made Simple（2001）给出算法；
  3. **2006–2014（工程化）**：Chubby（OSDI 2006）、ZooKeeper（ATC 2010）、ZAB（DSN 2011）、
     Raft（USENIX ATC 2014）——共识从论文变成可运维的组件。
- 🔧 **2022 → 2026**：
  - **Multi-Raft 成为存储层标配**：把数据分片，每个分片一个 Raft 组（TiKV、CockroachDB、PolarDB 等），
    解决「单个 Raft 组吞吐有上限」的问题；
  - **Kafka 用 KRaft 取代 ZooKeeper**（3.3 起生产可用，4.0 起不再依赖 ZK），是「共识内置化」的标志性事件；
  - **读路径被正式纳入协议讨论**：本书 3.6 讲了写路径，但 2026 年必须补 **ReadIndex / Lease Read / follower read**——
    否则「强一致系统」的读完全可能返回旧值（详见 [12](12-ZooKeeper详解与再论分布式系统.md)）。

## 经典论文与原始文献

| 论文 / 文献 | 出处 | 与本章关系 |
| --- | --- | --- |
| Pease, Shostak, Lamport, 《Reaching Agreement in the Presence of Faults》 | JACM 27(2), 1980 | 容错一致的早期形式化 |
| Lamport, Shostak, Pease, 《The Byzantine Generals Problem》 | ACM TOPLAS 4(3), 1982 | 3.2 的原始出处，3f+1 门限的证明 |
| Fischer, Lynch, Paterson, 《Impossibility of Distributed Consensus with One Faulty Process》 | JACM 32(2), 1985 | **FLP**：本章所有算法为何都要靠超时续命（3.3 的理论底） |
| Dwork, Lynch, Stockmeyer, 《Consensus in the Presence of Partial Synchrony》 | JACM 35(2), 1988 | 部分同步模型：务实系统的理论依据 |
| Chandra & Toueg, 《Unreliable Failure Detectors for Reliable Distributed Systems》 | JACM 43(2), 1996 | 故障检测器分类（◇S、◇P 等），绕开 FLP 的标准路径 |
| Lamport, 《The Part-Time Parliament》 | ACM TOCS 16(2), 1998 | **Paxos** 原始论文（3.5） |
| Lamport, 《Paxos Made Simple》 | ACM SIGACT News 32(4), 2001 | Paxos 的可读版重述 |
| Lamport, 《Fast Paxos》 | Distributed Computing 19(2), 2006 | 把提交延迟从两轮降到一轮（优化线代表） |
| Castro & Liskov, 《Practical Byzantine Fault Tolerance》 | OSDI 1999 | **PBFT**：3.3.2 的工程算法（本书未展开推导） |
| Burrows, 《The Chubby Lock Service for Loosely-Coupled Distributed Systems》 | OSDI 2006 | 共识的工业先行者：锁服务 + 名字服务 |
| Reed & Junqueira, 《A Simple Totally Ordered Broadcast Protocol》 | LADIS 2008 | ZAB 的早期表述 |
| Hunt 等, 《ZooKeeper: Wait-free Coordination for Internet-scale Systems》 | USENIX ATC 2010 | 共识的工程形态（第 12 章主角） |
| Junqueira, Reed, Serafini, 《Zab: High-performance broadcast for primary-backup systems》 | DSN 2011 | ZAB 协议论文 |
| Ongaro & Ousterhout, 《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | **Raft** 原始论文（3.6） |
| Ongaro, 《Consensus: Bridging Theory and Practice》 | Stanford 博士论文, 2014 | Raft 的完整细节（成员变更、日志压缩） |

## 近年研究与工业界开源实践（2015–2026）

- **Raft 的主流实现（star 均为 2026-09 `gh api` 实测）**：
  - `etcd-io/etcd`（≈52.3k★）：Kubernetes 的存储底座，Raft 实现见 `raft/` 目录，
    支持 **ReadIndex** 线性读、prevote、learner 节点；
  - `sofastack/sofa-jraft`（≈3.8k★）：Java 版 Raft 工业实现，带完整文档与线性读、快照；
  - `baidu/braft`（≈4.2k★）：百度 C++ 版 Raft，支撑 bRPC 生态；
  - `hashicorp/consul`（≈30.1k★）：内部使用 Hashicorp Raft 库（另有独立仓库，star 未核验）。
- 🔧 **Multi-Raft（分片 + 每片一个 Raft 组）**：
  - `tikv/tikv`（≈16.9k★，实测）：Multi-Raft + PD 调度，是「共识用于分片存储」的代表实现；
  - `cockroachdb/cockroach`（≈32.5k★，实测）：Range 为单位的 Raft 组，自动分裂/合并/再平衡；
  - 这条路线是本书 3.6 之后最该补的工程知识：**单 Raft 组有吞吐上限，水平扩展必须分片**。
- 🔧 **KRaft：共识内置化**：
  - `apache/kafka`（≈33.8k★，实测）自 3.3 起提供生产可用的 KRaft（内置 Raft 替代 ZooKeeper），
    4.0 起完全移除对 ZooKeeper 的依赖；
  - 意义：2015 年时「共识组件 = 外部 ZooKeeper」是标准答案，2026 年标准答案是**内置 Raft**。
- **BFT 的回归**：区块链场景推动 PBFT 系（Tendermint、HotStuff）重新活跃；
  HotStuff（PODC 2019）把 BFT 的通信复杂度降到线性并支持流水线化，是近年最重要的 BFT 进展之一（本书未覆盖）。
- **共识的可测试性**：`jepsen-io/jepsen`（≈7.5k★）对 etcd/ZooKeeper/Consul 的共识实现做过公开测试，
  推动了「leader lease」「读路径」等细节的公开讨论。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「共识就是一致性」 | 共识是**就一个值达成一致**的算法问题；一致性是**副本状态应满足的条件**；共识通常被用来实现线性一致 |
| 2 | 「Paxos 只决定一个值，所以不能复制日志」 | 对日志每个槽位跑一次 Paxos 即可；稳定 Leader + 跳过 Prepare 就是 **Multi-Paxos** |
| 3 | 「Raft 比 Paxos 更强 / 更安全」 | 二者等价（解同一问题、同为 CFT、同为 2f+1）；Raft 胜在**可理解性与可实现性** |
| 4 | 「5 台机器能容忍 2 台任意作恶」 | 5 台只能容忍 2 台**停机**（2f+1）；容忍 2 台**拜占庭**需要 7 台（3f+1） |
| 5 | 「多数派确认了就一定能读到」 | 多数派确认的是**写**；读若走任意节点且不经 ReadIndex/租约/同步，仍可能读到旧值 |
| 6 | 「共识算法保证一定会出结果」 | FLP 说明异步下不可能同时保证安全与终止；实际系统靠**超时 + 部分同步假设** |
| 7 | 「选主不需要任期号」 | 必须有 `term`/`epoch`：否则旧 Leader 恢复后会双主（脑裂），这是工程事故高发点 |
| 8 | 🔧 本书需 2026 补丁 | 3.6 未覆盖 **读路径**：ReadIndex、Lease Read、follower read 与 stale read 的取舍必须补 |
| 9 | 🔧 本书需 2026 补丁 | 3.4–3.6 未覆盖 **Multi-Raft**：单组 Raft 的吞吐上限决定了必须分片，这是存储层的默认架构 |
| 10 | 🔧 本书需 2026 补丁 | 本书未覆盖 **成员变更的安全做法**（joint consensus / 单节点变更）与**日志压缩（快照）**：这两项是 Raft 落地必备 |

## 与其他章 / 其他书的联系

- ← **[02-一致性的概念与强弱.md](02-一致性的概念与强弱.md)**：线性一致性的定义来自那一章；共识是它的实现手段。
- ← **[03-两阶段提交与三阶段提交.md](03-两阶段提交与三阶段提交.md)**：FLP 与「2PC 不是共识」在那里提出，本章给正解。
- → **[06-分布式锁.md](06-分布式锁.md)**：锁的「一致性实现」本质是把锁状态交给共识组件（ZK/etcd）托管。
- → **[12-ZooKeeper详解与再论分布式系统.md](12-ZooKeeper详解与再论分布式系统.md)**：ZAB 与 ZK 的一致性级别是本章的工程案例。
- ↔ [../深入理解分布式共识算法/04-Paxos.md](../深入理解分布式共识算法/04-Paxos.md) 与 [../深入理解分布式共识算法/07-Raft.md](../深入理解分布式共识算法/07-Raft.md)：算法级推导，本书第 3 章的最佳配套。
- ↔ [../深入理解分布式系统/06-Paxos与Multi-Paxos及其变体.md](../深入理解分布式系统/06-Paxos与Multi-Paxos及其变体.md) 与 [07-Raft与拜占庭容错.md](../深入理解分布式系统/07-Raft与拜占庭容错.md)：中文原创书的图示版，直观性好。
- ↔ [../分布式协议与算法实战/02-Paxos与Multi-Paxos.md](../分布式协议与算法实战/02-Paxos与Multi-Paxos.md) 与 [03-Raft选举日志复制与成员变更.md](../分布式协议与算法实战/03-Raft选举日志复制与成员变更.md)：工程落地视角，成员变更一节正好补本书缺口。
- ↔ [../分布式系统/06-协调.md](../分布式系统/06-协调.md)：van Steen 教材中「共识的动机」（选举/互斥）与本章互补。
- ↔ [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)：把共识放进架构选型的语言里讨论。
