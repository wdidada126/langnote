# 第 3 章（下） CAP 定理、一致性模型与隔离级别

> 本章笔记覆盖原书 **第 3 章 3.3 CAP 定理、3.4 一致性模型、3.5 隔离级别、3.6 一致性和隔离级别的对比、3.7 小结**。
> 分区与复制在 [03-数据分区与复制.md](03-数据分区与复制.md)。
> **本章地图**：本书这半章的任务是**厘清术语**——「一致性」这个词在分布式系统里被复用得太厉害：
> 共识（consensus）、强一致（linearizability）、事务一致性（C/I of ACID）、副本收敛（eventual consistency）指的根本不是一件事。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 3.3 CAP 定理 | C=线性一致性、A=非失败节点有限时间响应、P=容忍网络分区 | CAP 只在**网络分区发生时**强迫你在 C 与 A 之间二选一；无分区时它什么都不禁止 |
| 3.3.1 PACELC 定理 | 分区时 A/C 取舍；无分区时延迟/一致性取舍（Else） | **PACELC 才是日常系统设计的真正框架**：平时我们付的是延迟代价，不是可用性代价 |
| 3.3.2 BASE | Basically Available / Soft state / Eventual consistency | BASE 与 ACID 不是对立口号，而是「另一侧的取舍语言」 |
| 3.4.1 线性一致性 | 所有操作看起来像在某一瞬间原子生效，且尊重实时顺序 | 最强、**可组合**的一致性模型；「对单个对象」的强一致，不是事务隔离 |
| 3.4.2 实现线性一致性 | 全序广播 / 共识 + 状态机复制 | 每步操作都要过多数派 ⇒ 代价是一次 RTT 级别的延迟 |
| 3.4.3 线性一致性的代价 | 与可用性在分区下的冲突；延迟下限 | 「强一致」不是免费的：它换来的是正确性推理的简单化 |
| 3.4.4 顺序一致性 | 尊重每进程的程序顺序，但不要求实时顺序 | 比线性一致弱；内存可见性场景更常用 |
| 3.4.5 因果一致性 | 只保因果相关的顺序；并发可任意序 | 因果一致是「**不牺牲可用性情况下能做到的最强**」模型之一，也是 CRDT 的基石 |
| 3.4.6 最终一致性 | 停止写入后副本趋于一致 | 「最终」没有时间界限，实际工程要看**收敛时间与违约窗口** |
| 3.4.7 以客户端为中心的一致性 | 读写保证/单调读/单调写/读其所写 | 从客户端视角补画模型，常比「服务端强一致」便宜得多 |
| 3.5–3.6 隔离级别 vs 一致性模型 | ANSI SQL 隔离级别（脏读…可串行化）对事务；一致性模型对单个对象 | 两者是**正交的两个维度**：一个类比也不成立；混淆它们是分布式里最常犯的错误 |

## 核心精讲

### 3.3 CAP：一句话与三个澄清

> 在一个可能丢失任意消息的异步网络里，不可能同时实现「线性一致性」和「对每个非失败节点都可用」。

**澄清一**：CAP 里的 **C 是线性一致性**（linearizability），不是 ACID 的 C（那个 C 通常指「事务不违反业务不变式」），也不是「副本一致」。

**澄清二**：**P 不是可选项**。现实网络一定会分区，所以「CA 系统」在分布式里没有意义；真正的选择是
**分区发生时**：要么牺牲可用性（CP：少数派拒绝服务），要么牺牲一致性（AP：两边都继续写，之后合并）。

**澄清三**：没有分区的时候 CAP 什么也不禁止，此时真正限制你的是 **延迟**——这正是 PACELC 要表达的。

### 3.3.1 PACELC

PACELC 的读法是把一句话拆成两半（`Else` 分支）：

```text
if Partitioned:   tradeoff between Availability and Consistency (A vs C)
else:             tradeoff between Latency and Consistency (L vs C)
```

由此可以给常见系统贴标签（标签是相对**默认配置**的，所有系统几乎都可配）：

| 系统 | 默认倾向 | 备注 |
| --- | --- | --- |
| Spanner（外部一致性） | PC/EC | 强一致优先，延迟靠 TrueTime + 2PC 优化 |
| Dynamo / Cassandra（默认 CL） | PA/EL | 可用性优先，冲突交应用层 |
| MySQL 半同步 + 读主 | PC/EC | 经典 CP：主不可用即不可写 |
| Cassandra（QUORUM 读写） | PC/EL-ish | 提高一致性级别即向 C 移动，代价是延迟与可用性 |

### 3.4 一致性模型谱系（强 → 弱）

```text
线性一致性 Linearizability
    ↓ （不再要求实时顺序）
顺序一致性 Sequential consistency
    ↓ （不再要求全局单一顺序）
因果一致性 Causal consistency   ←— 常常是「可用性可保全的最强档」
    ↓ （连因果也不保，只保最后收敛）
最终一致性 Eventual consistency
```

**线性一致性的三种等价说法**：

1. 每个操作看起来在其调用与响应之间的**某个瞬间**原子生效；
2. 一旦某个写完成，之后的所有读都必须看到它（或更后写的值）；
3. 存在一个与**实时顺序**（real-time order）相容的操作全序。

**顺序一致性**只要求「存在一个与每个进程程序序相容的全序」，不要求它尊重墙上时钟先后。

**因果一致性**：只保证「可能具有因果关系」的操作可见顺序一致。Lamport 的 happens-before 是它的数学形式（第 6 章）。

### 教学示意：线性一致性的「违反判定」骨架

```go
// 教学示意，不参与构建
// 一个历史 history 是若干操作的调用/响应区间；判定「是否存在与实时顺序相容的全序」
type Op struct {
    Proc  int
    Type  string // "read" | "write"
    Key   string
    Val   string
    // 区间的端点（逻辑时间戳，只在教学里用）
    Invoke, Response int
}

// Linearizable：尝试把尚未「定序」的操作逐个挑出来，模拟执行，看能否把全部操作排完。
// 这里的 searching 展示的是「检查 = 搜索一个合法全序」这个核心观念，不是可用的判定器。
func Linearizable(h []Op) bool {
    pending := append([]Op(nil), h...)
    // state: key -> value
    state := map[string]string{}
    for len(pending) > 0 {
        progressed := false
        for i, op := range pending {
            // 若存在另一个已"完成"（Response < op.Invoke）的操作排在它前面，
            // 则该 op 不能在这一轮被挑出 —— 这是实时顺序的约束。
            if blockedByRealTime(pending, op) {
                continue
            }
            if ok := apply(state, op); ok {
                pending = removeAt(pending, i)
                progressed = true
                break
            }
        }
        if !progressed {
            return false // 卡住 ⇒ 不能排完 ⇒ 非线性一致
        }
    }
    return true
}
```

这段代码的重点不在跑出结果，而在于：**线性一致性 = 「找一个与实时相容的全序」**，
因此判定它是搜索问题（Jepsen 的 Knossos 就是做这件事的生产级实现，用 WGL 算法避免暴力搜索）。

### 3.5–3.6 隔离级别 vs 一致性模型：一张对照表

| 维度 | 一致性模型（3.4） | 隔离级别（3.5） |
| --- | --- | --- |
| 作用对象 | **单个对象的多个副本 / 单个读写的可见性** | **包含多个操作的事务之间** |
| 代表术语 | 线性一致、顺序、因果、最终一致 | 读未提交、读已提交、可重复读、快照隔离、可串行化 |
| 语义来源 | 分布式 / 共享内存理论 | ANSI SQL 标准（及 Berenson 1995 的批判与 Adya 的重定义） |
| 组合性 | 线性一致天然可组合（对全局推理友好） | 一般需要 **ISI/SSI** 级别的额外保护才能跨对象成立 |

**最容易踩的坑**：把「可串行化」当「强一致」，把「线性一致」当「事务原子」。
前者不保证多分区副本的新鲜度，后者不保证多对象操作的原子性。真正想要两者，需要的是
**「可串行化 + 线性一致」⇒ 严格可串行化（strict serializability）**，这正是 Spanner「外部一致性」的实质。

## 版本演进

- **本书 2022 年第一版**，本章内容所属理论全部早于成书（最晚的 survey 是 2016 年），因此「版本演进」体现为**术语口径的收敛**：
  - **2015 之前**：「最终一致 vs 强一致」二分法流行；
  - **2016–2020**：Viotti & Vukolić 的综述（ACM Computing Surveys 2016）之后，社区开始明确区分
    **数据一致性（data-centric）** 与 **客户端一致性（client-centric）**，以及各自的强弱偏序；
  - **2020 之后**：生产系统普遍提供「可调一致性级别 + 会话/快照读 API」，把选择权交给调用方；
  - **2022（本书出版年）→ 2026**：CRDT 从「论文 Demo」走到协同编辑产品；Jepsen 报告让厂商在文档里
    开始区分「理论模型」与「默认配置下的实际保证」。
- **本书特有的时代烙印**：本章对 CRDT 只是一笔带过（甚至未独立成节），而 2026 年的工程现实是 CRDT 已经成了
  离线优先 / 协同编辑 / 多端同步领域的事实解法——见 🔧 补丁。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Lamport《How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs》 | IEEE Transactions on Computers，1979 | **顺序一致性**的原始定义 |
| Herlihy & Wing《Linearizability: A Correctness Condition for Concurrent Objects》 | ACM TOPLAS 1990 | **线性一致性**的原始定义与「可组合性（compositionality）」的证明 |
| Fox & Brewer《Harvest, Yield, and Scalable Tolerant Systems》 | HotOS 1999 | BASE/收获率-yield 权衡的源头之一 |
| Brewer《Towards Robust Distributed Systems》 | PODC 2000（特邀报告） | CAP 猜想的首次公开表述 |
| Gilbert & Lynch《Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services》 | ACM SIGACT News 2002（后又将其体系化） | CAP 的**形式化证明** |
| Terry et al.《Session Guarantees for Weakly Consistent Replicated Data》 | PDIS 1994 | 以客户端为中心一致性的四种会话保证 |
| Saito & Shapiro《Optimistic Replication》 | ACM Computing Surveys 2005 | 乐观复制与最终收敛的系统化 |
| Vogels《Eventually Consistent》 | CACM 2009 | 「最终一致」一词在大众语境中的普及 |
| Berenson et al.《A Critique of ANSI SQL Isolation Levels》 | SIGMOD 1995 | 指出 SQL 标准隔离级别定义的缺陷，提出快照隔离 |
| Adya《Weak Consistency: A Generalized Theory and Optimistic Implementations for Distributed Transactions》 | MIT 博士学位论文，1999 | 用冲突图重定义隔离级别（PL-1…PL-3），今天的教科书口径 |
| Abadi《Consistency Tradeoffs in Modern Distributed Database System Design》 | IEEE Computer 2012 | **PACELC** 的原始表述 |
| Shapiro, Preguiça, Baquero, Zawirski《A Comprehensive Study of Convergent and Commutative Replicated Data Types》 | INRIA 技术报告 RR-7506，2011 | CRDT 的系统化定义（CmRDT / CvRDT） |
| Kleppmann & Beresford《A Conflict-Free Replicated JSON Datatype》 | IEEE TPDS 2017 | CRDT 走向产品级数据结构的一步 |
| Viotti & Vukolić《Consistency in Non-Transactional Distributed Storage Systems》 | ACM Computing Surveys 2016 | 2016 年前后的权威综述，低成本建立整体地图的最佳读物 |
| Corbett et al.《Spanner: Google's Globally Distributed Database》 | OSDI 2012 | 「外部一致性 = 严格可串行化」的实际范例 |

## 近年研究与工业界开源实践（2015–2026）

- **研究**：一致性的「谱系化」基本完成；近年的空隙在**验证**与**组合语义**：
  轻量形式化验证（TLA+/P）、随机化容错测试（Jepsen 类）、以及 Python/Go 里的线性一致性判定器。
- **Jepsen 的实践影响**（2026 视角必须补的一课）：
  jepsen.io 系列公开评测把大量「文档声称强一致」的系统拉回到可证伪的地面。典型收获是三条通用教训：
  ① **默认配置 ≠ 文档宣称**（很多系统的「默认」是最弱档）；
  ② **「quorum 足够」不等于线性一致**（时钟、成员视图、lease 的实现细节会破功）；
  ③ **「隔离级别」这个词在不同系统里有不同的历史语义**（如 PostgreSQL 的 SI/SSI、以及各家 MongoDB 默认读关注的话术差异）。
  具体每一份报告的结论请以 jepsen.io/analyses 原文为准，本目录不转述个案结论。
- **CRDT 落地**：协同编辑/离线优先场景（文档、白板、多人编辑）。国内常见组合是在服务端用 OT/ CRDT + 版本向量。
- **工业界开源**（star 数均为 2026-09-26 用 `gh api repos/OWNER/REPO --jq '.stargazers_count'` 实测）：

| 项目 | star | 与本章的对应 |
| --- | --- | --- |
| `jepsen-io/jepsen` | 7504 | 一致性宣称的可证伪工具；`knossos` 实现线性一致性判定 |
| `cockroachdb/cockroach` | 32508 | 对外主打串行化隔离 + 线性一致；其 HLC 时间戳与写意图机制是理解这套保证的关键 |
| `apache/cassandra` | 10102 | 可调一致性级别（ONE/QUORUM/ALL）+ LWT 是「同一系统里既 PA 又 PC」的活教材 |
| `etcd-io/etcd` | 52310 | 默认线性一致读（quorum read / readIndex），是「怎样把强一致做对」的参考实现 |
| `y-crdt/y-crdt` | 2165 | CRDT 引擎（Yjs 的 Rust 内核），协同编辑的当前主流底座 |
| `pingcap/tidb` | 40589 | 乐观/悲观事务各自对应不同隔离保证，是 3.5/3.6 的现实样本 |

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「CAP 的 C = ACID 的 C」 | CAP 的 C 是**线性一致性**；ACID 的 C 通常指事务不破坏业务不变式，两者无关 |
| 2 | 「可以选 CA」 | P 不能放弃；所谓「CA」只在单机或永不分区的网络里才有意义 |
| 3 | 「CAP 是三选二」 | 更准确的说法是：**分区发生时，C 与 A 二选一**；平时根本没有这个选择 |
| 4 | 「线性一致性 = 可串行化」 | 前者是对**单对象**的实时顺序保证，后者是对**多对象事务**的隔离保证；两者都要则是「严格可串行化」 |
| 5 | 「最终一致 = 一定会短时间统一」 | 「最终」没有时间上限；工程上真正关心的是**收敛时长分布**与**冲突解决成本** |
| 6 | 「加了 quorum 读就一定是线性一致」 | 还要看是否做了 leider read/readIndex/lease 或者是否诚实仲裁递延；否则陈旧副本可以回答 stale 值 |
| 7 | 「因果一致不需要任何元数据」 | 需要向量时钟或类似机制记录依赖关系，成本随参与者数量增长 |
| 8 | 「隔离级别描述的是副本新鲜度」 | 不是。隔离级别说事务之间怎么互相干扰（脏读/不可重复读/幻读/写偏斜），与副本陈旧与否是两个维度 |
| 9 | 「BASE 与 ACID 对立」 | 二者是两个正交取舍语言；同一系统常常对不同数据用不同策略（账本强一致，推荐列表最终一致） |
| 10 | 🔧 本章对 **CRDT** 的处理偏薄 | 2026 的现实：CRDT 已是离线优先/协同编辑（文档、白板、多人图表）的**默认解法**，Yjs/Automerge 这类库把它工程化。合并语义（ convergent items 的收敛证明、删除/墓碑处理，以及「本该由用户决定合并结果」的场景）应补进「最终一致性」这一节来读 |
| 11 | 🔧 本章缺少 **Jepsen 式证伪方法**的引介 | 2026 的现实：读产品文档不如读一致性评测报告。「先看默认配置、再看声明模型、最后看第三方评测」应成为标准三步；本书以模型介绍为主，没有给出「怎么证伪一个宣称」的路径 |
| 12 | 🔧 本章的 CAP 表述未涵盖 **Brewer 本人后来的修正** | Brewer 在 CAP 十二年后补充说明：集群实际是在**分区态与正常态之间来回切换**，
  关注点应是「如何最小化分区恢复期的数据分歧与 torn writes」，而不是一次性地 C/A 二选一。补上这段能让本章结论更贴近运维现实 |
| 13 | 🔧 本章未区分「理论模型」与「API 契约」 | 2026 的现实：同一个系统对不同 API 给出不同保证（如 follower read vs leader read、stale read vs causal read）。「系统是什么模型」在今天通常是一个**按 API 分层的答案**，而不是一个名词 |

## 与其他章 / 其他书的联系

**本目录内**

- [03-数据分区与复制.md](03-数据分区与复制.md)：数据怎么放 ← 那里；数据对外承诺什么 ← 本章。
- [05-共识的地基与不可能定理.md](05-共识的地基与不可能定理.md)：线性一致性的实现要「全序」，全序要靠共识。
- [07-Raft与拜占庭容错.md](07-Raft与拜占庭容错.md)：Raft 的 4.8.11 节「实现线性一致性」与本章 3.4.2 是一回事。
- [09-时间和事件顺序.md](09-时间和事件顺序.md)：因果一致性的形式化基础（happens-before）。
- [11-案例研究分布式存储与数据库.md](11-案例研究分布式存储与数据库.md)：Spanner 的外部一致性 = 严格可串行化的落地形态。

**跨书互链**

- [../分布式系统/07-复制与一致性.md](../分布式系统/07-复制与一致性.md)：van Steen 3rd 对数据中心一致性 vs 客户端一致性的二分，与本章 3.4.7 对应。
- [../分布式系统概念与设计/13-复制.md](../分布式系统概念与设计/13-复制.md)：线性一致/顺序一致的教科书推导。
- [../数据库系统概念6/15-并发控制.md](../数据库系统概念6/15-并发控制.md)：隔离级别在数据库内部的完整谱系（SI/SSI、写偏斜）。
- [../数据库系统概念6/26-高级事务处理.md](../数据库系统概念6/26-高级事务处理.md)：事务二维保证与本章 3.6 对照。
- [../分布式数据库入门进阶与实战/05-BASE与CAP及分布式一致性模型.md](../分布式数据库入门进阶与实战/05-BASE与CAP及分布式一致性模型.md)：同一组术语的另一本工程书讲法。
- [../分布式系统/07-复制与一致性.md](../分布式系统/07-复制与一致性.md)：van Steen 3rd 的模型地图。
