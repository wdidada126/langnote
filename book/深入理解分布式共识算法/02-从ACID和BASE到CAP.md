# 第 2 章 从 ACID 和 BASE 到 CAP

> 覆盖原书第 2 章（第 1 篇「分布式相关概念与定理」，P11–16）。
> 小节照抄大纲：2.1 ACID——追求一致性；2.2 BASE 理论——追求可用性（三个方面 / 应用）；
> 2.3 CAP——分布式系统的 PH 试纸（定理 / 为什么 C、A、P 三者不可兼得 / 应用）；2.4 本章小结。

## 本章地图

本章是全书的理论前厅，任务是给后面所有算法立一个「取舍坐标系」：

```
ACID（单机事务，追求一致性）
   │  分布式化后：跨节点原子提交代价高、阻塞风险大
   ▼
BASE（放松一致性换可用性：Basically Available / Soft state / Eventually consistent）
   │  但「放松到什么程度」没有刻度
   ▼
CAP（给出刻度：网络分区 P 无法避免时，只能在 C 与 A 之间二选一）
```

- **2.1 ACID**：Atomicity / Consistency / Isolation / Durability。注意 **这里的 C（事务一致性）与 CAP 的 C（线性一致性）不是同一件事**——这是中文材料里最高频的混淆点。
- **2.2 BASE**：由 Fox & Brewer 在 HOTOS 1999 提出，本质上是「**承认中间状态存在、承认最终会收敛**」的设计立场。
- **2.3 CAP**：Brewer 2000 年在 PODC 的猜想，Gilbert & Lynch 2002 给出形式化证明（限定为**原子/线性一致性**与**任意非故障节点可响应**）。
- **2.3.3 CAP 的应用**：把系统按 CA / CP / AP 归类（本书的典型用法）。

## 核心精讲

### 2.1 ACID：一致性是有代价的

| 字母 | 含义 | 分布式化后的麻烦 |
| --- | --- | --- |
| A 原子性 | 事务要么全做要么全不做 | 跨节点要靠 2PC（见 [03-2PC与3PC分布式事务.md](03-2PC与3PC分布式事务.md)），协调者单点会造成阻塞 |
| C 一致性 | 事务前后**满足应用定义的约束**（不变量） | 这一条**主要由应用保证**，数据库只提供 A/I/D 三个工具 |
| I 隔离性 | 并发事务互不干扰 | 分布式下需要全局定序/全局时钟（TrueTime / HLC / TSO） |
| D 持久性 | 提交后不丢 | 依赖 WAL 落盘与多副本确认；「多副本确认」这一步就走到了共识 |

> 关键认识：**ACID 是单机语义**。把它搬到多节点，需要两个额外的机制——**原子提交**（第 3 章）与**共识**（第 4–6 章）。

### 2.2 BASE：BASE 不是「反 ACID」，而是「换一种失败语义」

- **Basically Available（基本可用）**：允许降级（读旧数据、限流、功能裁剪），但不整体不可用；
- **Soft state（软状态）**：允许副本间存在**中间不一致状态**，且该状态不需要被立刻消除；
- **Eventually consistent（最终一致）**：若停止写入，副本**最终**会收敛到同一状态。

**BASE 的三个词分别对应一个工程决定**：

| 词 | 要回答的工程问题 | 常见手段 |
| --- | --- | --- |
| Basically Available | 降级到什么程度仍算「可用」？ | 只读副本、熔断、限流、返回兜底数据 |
| Soft state | 中间状态允许存在多久？ | TTL、异步复制队列、重试队列 |
| Eventually consistent | 「最终」是多久？冲突怎么消解？ | LWW、向量时钟、CRDT、人工介入 |

```text
// 教学示意：BASE 下的最终一致（不参与构建、不编译、不运行）
fn write(x, v):
    writeLocal(x, v)                // 本地先收，立即返回成功（高可用）
    async replicateToPeers(x, v)    // 异步扩散，期间副本不一致 = 软状态

fn read(x):
    return readLocal(x)             // 可能读到旧值（最终一致，不是线性一致）

// 分区恢复后的收敛：必须定义「谁赢」
fn resolveConflict(a, b):
    // ① LWW：时间戳大者赢（简单但可能丢写）
    // ② 向量时钟：能检测并发写，交给应用层合并
    // ③ CRDT：用可交换的数据结构，保证任意顺序合并都收敛
```

> 应用形态：缓存、异步主从复制、DNS、消息队列的 at-least-once、读写分离的只读副本——**它们都是 BASE 的具体实例**。
> 重要提醒：选择了 BASE 就要**明确回答上表三行**，否则「最终一致」只是一个没写清楚的承诺。

### 2.3 CAP 到底在说什么

Gilbert & Lynch 证明的版本（**这是唯一有严格证明的口径**）：

- **C** = **线性一致性（linearizability）**：每个读都能看到「最近的已完成写」；
- **A** = **每个非故障节点收到的每个请求最终都能得到响应**（注意：**不要求有限的时间界**，这是最容易被误读的一点）；
- **P** = 网络允许**丢失任意消息**（分区）。

结论：在异步网络且允许消息丢失的模型下，**不存在既能保证线性一致性、又能保证每个非故障节点都能响应的算法**。

```text
// 教学示意：CAP 在分区下的两难（不参与构建、不编译、不运行）
// 两个副本 R1、R2 被网络分区隔开，客户端分别连到两边
fn onWrite(x, v):
    if config == CP:
        // 只有多数派侧能凑出 quorum，少数派侧拒绝写入 → 牺牲 A
        if not hasQuorum(): return REJECT("unavailable")
        return replicateToQuorum(x, v)      // 走共识：安全，但少数派侧不可用
    else:  // AP
        return writeLocal(x, v)             // 本地先收：两边都可用，但产生分叉
        // 分区恢复后需要冲突消解（LWW / 向量时钟 / CRDT / 人工介入）

fn onRead(x):
    if config == CP: return readThroughConsensus(x)   // 线性一致，可能拒绝服务
    else:            return readLocal(x)              // 可能读到旧值（最终一致）
```

**为什么「不可兼得」的直觉成立**（对应 2.3.2）：分区期间，若少数派侧也响应写请求，那么它写入的值无法被多数派侧知道；等分区恢复，两侧已各写各的，若要维持线性一致性就必须有一侧的写入被作废——即那侧的写请求当时就不该被「成功响应」。所以：**要线性一致就必须让一侧不可用**。

> ⚠️ **本书 2.3.2 的具体论证方式未能核实原文**（大纲只给小节名）。上面给出的是 Gilbert & Lynch 证明的标准直觉，属于公认知识，不作为对本书原文的转述。

### 2.3.3 CAP 的应用：分类法

| 类别 | 分区时的选择 | 典型系统（公开资料口径） |
| --- | --- | --- |
| CP | 宁可不可用，不返回旧/冲突数据 | etcd、ZooKeeper、TiKV、CockroachDB（共识层） |
| AP | 继续服务，接受暂时的不一致 | Cassandra（可调一致性）、Dynamo 一脉、DNS |
| CA | 不分区时同时满足 C 与 A | **仅在「不存在分区」时成立**，分布式系统里不是一个可承诺的类别 |

**把三个概念排成一排看**（这张表是本章最实用的一张）：

| 维度 | ACID | BASE | CAP |
| --- | --- | --- | --- |
| 适用场景 | 单机事务 | 大规模、可降级的服务 | 分布式系统的取舍框架 |
| 追求 | 一致性 | 可用性 | 给出「分区时怎么选」的刻度 |
| 对中间态 | 不允许（原子 + 隔离） | 允许（软状态） | 不表态 |
| 失败语义 | 事务回滚 | 收敛（可能丢写/需合并） | 分区侧不可用（CP）或分叉（AP） |
| 典型代价 | 吞吐、可用性 | 一致性延迟 | 分区时必失其一 |

## 版本演进

- **1970s–1980s**：ACID 成型（Gray 1981 的《The Transaction Concept》；Haerder & Reuter 1983 归纳出 ACID 缩写）；
- **1999–2000**：BASE（HOTOS 1999）与 CAP 猜想（PODC 2000 keynote）相继出现，背景是大规模 Web 服务对可用性的强需求；
- **2002**：Gilbert & Lynch 把 CAP 变成定理；此后 CAP 成为分布式系统的入门词汇，也开始被滥用；
- **2012**：Brewer 本人写《CAP Twelve Years Later》澄清「三选二」的误读；同年 Abadi 提出 **PACELC**，指出**没有分区时也要在延迟（L）与一致性（C）之间取舍**；
- **2015–2026**：Kleppmann 等人对 CAP 提出批评（认为其模型过窄，无法表达真实系统的取舍）；工程界的实际语言转向「**具体一致性模型 + 具体延迟/可用性 SLO**」，并用 **Jepsen** 风格的故障注入实测来检验宣称；
- **2023（本书）**：仍采用「CAP 是 PH 试纸」的经典表述——**这一表述本身没错，但它是粗刻度**，需要 2026 补丁（见下）。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Gray《The Transaction Concept: Virtues and Limitations》 | VLDB 1981 | 事务概念的权威表述 |
| Haerder & Reuter《Principles of Transaction-Oriented Database Recovery》 | ACM Computing Surveys 1983 | 归纳出 ACID 缩写 |
| Herlihy & Wing《Linearizability: A Correctness Condition for Concurrent Objects》 | ACM TOPLAS 1990 | **线性一致性**的形式化定义（CAP 中 C 的严格含义） |
| Fox & Brewer《Harvest, Yield, and Scalable Tolerant Systems》 | HOTOS 1999 | BASE 的来源 |
| Brewer《Towards Robust Distributed Systems》 | PODC 2000 keynote | CAP 猜想 |
| Gilbert & Lynch《Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services》 | ACM SIGACT News 2002 | CAP 的形式化证明 |
| Brewer《CAP Twelve Years Later: How the "Rules" Have Changed》 | IEEE Computer 2012 | 作者对 CAP 的澄清与反思 |
| Abadi《Consistency Tradeoffs in Modern Distributed Database System Design》 | IEEE Computer 2012 | **PACELC**：无分区时 E（延迟）与 C 仍然对立 |
| Kleppmann《A Critique of the CAP Theorem》 | arXiv:1509.05393 | 对 CAP 模型表达力的批评 |

## 近年研究与工业界开源实践（2015–2026）

> star 数均为 2026-09 用 `gh api repos/OWNER/REPO --jq '.stargazers_count'` 实测。

- `etcd-io/etcd`（**52,310★**）：etcd 是**典型的 CP 系统**——分区时少数派侧拒绝读写；它提供线性一致（默认）与可串行化的 KV 语义，是 Kubernetes 把「CP」作为控制面默认选择的直接原因。
- `apache/zookeeper`（**12,811★**）：CP；写走 ZAB 全序广播，读默认可能是**本地读**（需要 `sync()` 才能获得更强的读保证），这一点是 ZooKeeper 使用中的经典坑（详见 [06-ZAB与ZooKeeper.md](06-ZAB与ZooKeeper.md)）。
- `cockroachdb/cockroach`（**32,508★**）：对外宣称**可串行化（serializable）**，用 Raft + HLC 实现；这是「CAP 之下把 C 做到很强、用工程手段压低 A 的损失」的样本。
- `pingcap/tidb`（**40,590★**）：TiDB 的默认隔离级别是 **快照隔离（SI）**（文档表述为 Repeatable Read），而不是可串行化——**这是「宣称」与「模型」必须对齐的地方**，SI 允许写偏斜。
- `jepsen-io/jepsen`（**7,504★**）：Jepsen 用故障注入检验上述宣称，是本段最重要的方法论工具。
  - **Jepsen 实测的共同结论（概括，不逐条复述具体报告编号以避免误引）**：
    1. etcd / CockroachDB / TiDB 都有 Jepsen 公开测试报告（见 jepsen.io 的 analyses 列表，按版本查阅）；
    2. 测试中发现的偏差大多**不是共识算法本身错**，而是**读路径优化、时钟依赖、默认隔离级别、客户端重试语义**削弱了端到端保证；
    3. 因此「用了 Raft」≠「应用层获得线性一致性」——这一点是本章与 [07-Raft.md](07-Raft.md)、[08-Raft工程实践与SOFAJRaft.md](08-Raft工程实践与SOFAJRaft.md) 共同的落脚点。
- **近年研究**：对 CAP 的替代表达（PACELC、一致性模型谱系、SLO 化描述）已基本取代「三选二」的粗分类；HLC/TrueTime 一类时钟方案把「外部一致性」变成可度量的工程目标。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「ACID 的 C = CAP 的 C」 | ACID 的 C 是**应用不变量**（转账前后总额不变）；CAP 的 C 是**线性一致性**。两者同名不同义 |
| 2 | 「CAP 是三选二，所以可以选 CA」 | P 是**网络属性不是选项**；无分区时 C 与 A 可同时满足，分区时必须放弃其一。「CA」不是分布式系统可承诺的类别 |
| 3 | 「CAP 的 A = 高可用（几个 9）」 | Gilbert & Lynch 的 A 是「每个非故障节点对每个请求都能响应」，**与可用性百分比、与 SLA 不是一回事** |
| 4 | 「BASE 就是不保证一致性」 | BASE 是一种**设计立场**（接受软状态 + 最终收敛），仍需明确「最终」多久、冲突如何消解 |
| 5 | 「选了 CP 就自动获得线性一致」 | 还要看**读路径**：ZooKeeper 本地读、etcd 的串行/线性读选项、TiDB 的 SI 默认级别都会削弱端到端保证 |
| 6 | 「共识算法保证的是 ACID」 | 共识只保证**副本间的日志全序**；原子提交（2PC）与隔离级别是另外两件事（见 [03-2PC与3PC分布式事务.md](03-2PC与3PC分布式事务.md)） |
| 7 | 🔧 本书「CAP 是 PH 试纸」的表述需要加刻度 | 2026 年工程界的通用语言是 **PACELC + 具体一致性模型 + SLO**：无分区时仍有 E/L（延迟）与 C 的取舍，分区时才有 C/A 取舍。只读「三选二」会推不出「为什么很多系统平时不分区也在牺牲一致性」 |
| 8 | 🔧 本书未给出「宣称 vs 实测」的校验方法 | 补：应以 `jepsen-io/jepsen`（**7,504★**）一类故障注入测试检验一致性宣称；Jepsen 对 etcd / CockroachDB / TiDB 均有公开报告，偏差多出在读路径与默认隔离级别而非共识本身 |
| 9 | 🔧 本书未把「CAP 的 C」与「可串行化」区分 | 线性一致性是**单对象、实时序**的保证；可串行化是**多对象事务**的保证。CockroachDB 宣称可串行化、TiDB 默认 SI，二者不是同一档位；选型时不能只问「是不是 CP」 |

## 与其他章 / 其他书的联系

**本目录内**

- [01-分布式共识算法概述.md](01-分布式共识算法概述.md)：本章的「一致性」在那里被定义为客户端可见性保证；两章合起来才完整。
- [03-2PC与3PC分布式事务.md](03-2PC与3PC分布式事务.md)：ACID 的 A 在分布式下的实现，也是「共识不是原子提交」的分界点。
- [08-Raft工程实践与SOFAJRaft.md](08-Raft工程实践与SOFAJRaft.md)：读路径（ReadIndex / Lease Read）直接决定了一个 Raft 系统对外宣称的 C 是哪个档位。
- [12-FLP不可能定理.md](12-FLP不可能定理.md)：CAP 与 FLP 是「同一个悲观结论的两种表述」——一个从分区/可用性角度，一个从异步/终止性角度。

**跨书**

- [../分布式数据库入门进阶与实战/05-BASE与CAP及分布式一致性模型.md](../分布式数据库入门进阶与实战/05-BASE与CAP及分布式一致性模型.md)：国产书的同主题章，与本目录 02 对读可看两种口径差异。
- [../深入理解分布式系统/04-CAP定理与一致性模型与隔离级别.md](../深入理解分布式系统/04-CAP定理与一致性模型与隔离级别.md)：把 CAP、一致性模型、隔离级别放在一起讲，正好补本章缺的「隔离级别」那一维。
- [../数据库系统概念6/26-高级事务处理.md](../数据库系统概念6/26-高级事务处理.md)：ACID/隔离级别的教科书口径。
- [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)：从架构角度给出「什么时候可以不要强一致」的判据。
</content>
