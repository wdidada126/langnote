# 第 09 讲 More Replication, CRAQ：把读扩散到整条链

> 官方标题：**More Replication, CRAQ**（LEC 9，主讲 rtm）
> 指定必读：**CRAQ (2009)**
> 布置：**Lab 3: KV Raft**

## 本章地图

本讲把「复制」这个主题从三种已知方案（主从 / 共识多数派 / GFS 式弱一致）扩展到第四种拓扑：

```
主从/FT（L4）     ：主定序，备不服务读
共识 Raft/Paxos   ：多数派定序，读默认走 leader
GFS（L3）         ：弱一致，读随便走
链式复制（本讲）  ：写入从头到尾，读在尾 —— 强一致且结构简单
CRAQ（本讲）      ：读可以在链上任意节点 —— 读多数场景下读吞吐随链长线性扩展
```

主线：链式复制的基本协议 → 失效处理（为什么必须有个外部「配置管理器」）→
**CRAQ 的 dirty/clean 版本机制** → 与多数派方案的定量对比 → 适用边界。

## 核心精讲

### 9.1 链式复制（Chain Replication, CR）

节点排成一条链：`head → n1 → ... → tail`。

- **写**：client 把写发给 **head**，沿链向后传播，每个节点按顺序应用；
- **提交点**：**tail 应用后，由 tail 回复 client**——因此「已被 client 看到的写」必然已在 tail 上；
- **读**：client 把读发给 **tail**——因为 tail 持有所有已提交的写，读 tail = 线性一致。

优点非常诱人：**不需要多数派投票就能得到强一致**，而且实现极简（只有一条链）。

### 9.2 失效处理：为什么必须有外部配置管理器

链的成员变更不能由链自己决定（否则又回到共识问题）。CR 的做法是引入一个**主配置服务（master / configuration service）**，
通常由 Paxos/ZooKeeper 这类共识系统实现，它负责：检测节点失效、决定新链、广播新配置。

三种失效情形的安全性：

| 失效位置 | 处理 | 安全性 |
| --- | --- | --- |
| **head 挂了** | 第二个节点成为新 head | ⚠️ 麻烦：head 可能已经收到写但还没往下传 → 这些写**没有被提交**（没人回复过 client），可以安全丢弃；但 client 需要重新提交 |
| **tail 挂了** | 前一个节点成为新 tail | 安全：tail 回复过的写，其前驱必然也已应用（沿链传播），新 tail 持有全部已提交写 |
| **中间节点挂了** | 把它从链中摘掉，前驱重发未完成的写 | 安全：只要前驱还持有未传播完的写 |

**关键洞察**：安全性靠「**提交点是 tail**」这一条保证——
所有已确认的写都在 tail 及更早的节点上，所以「删掉链上任意一段」不会丢已确认的数据。

### 9.3 CRAQ：让任意节点都能服务读

CR 的问题是**所有读都打在 tail 上**，读吞吐无法扩展。CRAQ 的解法：

- 每个对象在每个节点上有**版本号**和一个 **clean / dirty 标记**；
- **写入传播（向下）**：head 收到写 → 本地记为 `dirty(v+1)` → 沿链向后传，每个节点都记为 `dirty(v+1)`；
  到达 tail 时，tail 把它**提交**并标记为 `clean(v+1)`；
- **确认传播（向上）**：tail 提交后，沿链**反向**发回一个 ACK，把沿途节点上的该对象标记为 `clean(v+1)`；
- **读**：
  - 若本地该对象是 **clean** → **直接本地返回**（零跳）；
  - 若是 **dirty** → 说明本地版本可能还没提交 → 向 **tail** 查询「该对象最后已提交的版本」并返回那个版本。

于是：**读多数（read-mostly）负载下，绝大多数读是 clean 的本地读 → 读吞吐随链长线性增长**。
而写仍然要穿过整条链（向下 + 向上），写吞吐不随链长增长——这是个明确的取舍。

### 9.4 教学示意：读路径的判定

> **教学示意，不参与构建**——只表达 CRAQ 读的分支逻辑。

```go
// 教学示意，不参与构建
type Versioned struct {
    Value    []byte
    Version  int
    Dirty    bool // true = 已写入本地但尚未被 tail 提交
}

// 在链上任意节点处理读
func (n *Node) read(key string) ([]byte, error) {
    local := n.store[key]

    if !local.Dirty {
        return local.Value, nil // 快速路径：本地 clean，直接返回
    }
    // 慢路径：本地是脏版本，必须问 tail 拿到「最后已提交版本」
    committed, err := n.askTail(key)
    if err != nil {
        return nil, err
    }
    return committed.Value, nil
}

// tail 提交后沿链反向清理
func (n *Node) onCommitAck(key string, version int) {
    if n.store[key].Version == version {
        n.store[key].Dirty = false // 变 clean，之后可读本地
    }
}
```

> 正确性来源：**「dirty」意味着「这个版本可能还没被提交」，所以不敢直接给客户端**；
> 一旦 tail 提交了并回传 ACK，就变成 clean，本地读安全。
> 换句话说，CRAQ 把「线性一致读」的成本从「每次都问 tail」降到了「**只在对象刚被写过的一小段窗口内问 tail**」。

### 9.5 与多数派方案的对比（本讲最有价值的部分）

| 维度 | 链式复制 / CRAQ | Raft / Paxos（多数派） |
| --- | --- | --- |
| 定序者 | 链本身（head 定序，tail 提交） | leader（经多数派授权） |
| 写延迟 | 穿过整条链（**受最慢节点拖累**） | 只需多数派响应（**可跳过慢节点**） |
| 读吞吐（读多写少） | **随链长线性扩展**（CRAQ） | 需 leader + ReadIndex，或额外机制（follower read/lease） |
| 对慢节点的敏感 | 高（慢节点在链上会拖慢所有写） | 低（多数派即可） |
| 成员变更 | **依赖外部配置管理器**（本身要共识） | 协议内置（Raft §6） |
| 可容忍故障 | 只要有配置管理器，可容忍到只剩一个节点 | 需多数派存活（N=2f+1 容忍 f） |

一句话总结这个对比：**链式复制用「更长的写路径」换「可以扩散的读」；
多数派用「更短的写路径」换「读集中在 leader」**。选哪个取决于读写比与慢节点分布。

### 9.6 现实中的链式结构

- **HDFS 的写入流水线**就是链式的：client 把 block 沿 datanode 链依次推送，
  与 CR 的「沿链传播」形状一致（但 HDFS 的确认与一致性语义与 CR 不同，不能等同）；
- 一些 KV 存储（如学术研究中的 FAWN-KV 一类系统）采用链式复制来在大量弱节点上获得强一致；
- 需要外部配置管理器的模式已经很常见：**元数据走共识、数据走复制**（TiKV 的 PD、各类控制面/数据面分离架构）。

## 版本演进

- **2004**：van Renesse & Schneider《Chain Replication for Supporting High Throughput and Availability》（OSDI 2004）
  提出链式复制（**6.5840 2026 schedule 已把它单列为独立一讲，读 CR (2004)；2020 年读的是 CRAQ (2009)**）。
- **2009**：Terrace & Freedman《Object Storage on CRAQ: High-throughput chain replication for read-mostly workloads》（USENIX ATC 2009）
  把读扩散到整条链。
- **2010s**：链式结构多用于存储系统的写入流水线与特定 KV 系统；
  通用共识实现（Raft）的普及使「多数派 + leader」成为默认。
- **2020（本讲）**：课程把 CRAQ 作为「**复制拓扑还有别的可能**」的反例教材——
  提醒学生不要以为「复制 = Raft」。
- **2026**：CRAQ 的直接部署不多，但它的两个思想被继承：
  - **读扩散**（follower read / lease read / 本地读 + 版本校验）已是 Raft 系系统的标配优化；
  - **控制面/数据面分离**（元数据走共识、数据走复制拓扑）成为主流架构。

## 经典论文与原始文献

| 论文 | 出处 | 本讲为何读它 |
| --- | --- | --- |
| Terrace & Freedman《Object Storage on CRAQ: High-throughput chain replication for read-mostly workloads》 | **USENIX ATC 2009** | L9 **指定必读**（课程站点 `craq.pdf`，另有 craq-faq） |
| （基础，**非本讲指定**）van Renesse & Schneider《Chain Replication for Supporting High Throughput and Availability》 | OSDI 2004 | CRAQ 的前身；6.5840 2026 把它单列一讲（CR 2004） |
| （对照）Ongaro & Ousterhout《Raft》 | USENIX ATC 2014 | 多数派路线的对照物（[06-容错Raft一.md](06-容错Raft一.md)） |
| （对照，非本讲指定）Andersen et al.《FAWN: A Fast Array of Wimpy Nodes》 | SOSP 2009 | 链式复制在真实系统中的一个著名用例（FAWN-KV） |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **灵活法定数（flexible quorums）**：Howard & Mortier 等工作表明「读法定数与写法定数可非对称配置」，
    在读写比变化时动态切换——与 CRAQ「按负载调整读策略」是同一思路的不同实现；
  - **租约读 / follower read**：让 Raft 的 follower 也能服务线性一致读
    （etcd 的 ReadIndex、TiKV 的 follower read / lease read），本质是把 CRAQ 的「读扩散」搬进多数派系统；
  - **可重配置复制（reconfigurable replication）**：SmartMerge、Raft 成员变更等，
    解决的正是本讲「配置管理器必须可信」这一环节。
- **工业界开源（star 数 2026-09-26 `gh api` 实测）**：
  - `apache/hadoop`（**15669★**）：HDFS 的写入流水线是链式结构最广为人知的工业实例
    （语义与 CR/CRAQ 不同，但拓扑相同，可用来体会「沿链传播」的优缺点）。
  - `scylladb/scylladb`（**15772★**）：Dynamo 式可调 quorum 的代表，是本讲「链式 vs 多数派」对照的现役样本。
  - `redpanda-data/redpanda`（**12572★**）：用 Raft 做分区复制的日志系统，
    可与「链式流水线」对比延迟模型（多数派只需 f+1 个响应）。
  - `tikv/tikv`（**16878★**）：PD（控制面）+ 多 Raft group（数据面）的分离架构，
    是「元数据走共识、数据走复制」的 2026 主流形态。

## 常见误区与本课程需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「链式复制不需要共识」 | 它需要**外部配置管理器**做成员变更，而这个管理器本身必须容错（通常用 Paxos/ZK） |
| 2 | 「CRAQ 的读一定是本地零跳」 | **只有 clean 的读**是本地；刚写过、本地还 dirty 的对象必须问 tail（慢路径） |
| 3 | 「链式复制的写更快」 | 写要穿过整条链，**受最慢节点拖累**；多数派可跳过慢节点，这是链的劣势 |
| 4 | 「CRAQ 适合写多读少」 | 恰恰相反：它是为 **read-mostly** 设计的；写多的负载下 dirty 比例高，慢路径占比大 |
| 5 | 「HDFS 的流水线 = 链式复制」 | 拓扑相同，**语义不同**（确认点、失败处理、一致性保证都不一样），不可等同 |
| 6 | 🔧 2020 课程未覆盖 | **读扩散在 Raft 系系统里已成标配**：etcd ReadIndex、TiKV follower read/lease read；CRAQ 的思想被吸收进了多数派系统 |
| 7 | 🔧 2020 课程未覆盖 | **慢节点（gray failure / 降速故障）**：链对慢节点最敏感；2026 必须补「降速故障检测 + 主动摘除」这一层 |
| 8 | 🔧 2020 课程未覆盖 | **跨地域链**：链长 = 延迟叠加，跨 AZ/跨 region 部署几乎不可用；这是链式复制没能普及的现实原因 |
| 9 | 🔧 课程本身演进 | 6.5840 2026 把 **Chain Replication (CR 2004)** 单列一讲；2020 只读 CRAQ。两条文献都应知道 |

## 与其他章 / 其他书的联系

- **本目录内**：
  - [06-容错Raft一.md](06-容错Raft一.md)、[07-容错Raft二.md](07-容错Raft二.md)——多数派路线的完整形态，与本讲对照；
  - [08-ZooKeeper.md](08-ZooKeeper.md)——ZK 常被用作本讲所需的「外部配置管理器」；
  - [04-主从复制与VMwareFT.md](04-主从复制与VMwareFT.md)——同样是「主定序」，但备不服务读，本讲解决了这一点；
  - [10-Aurora与Frangipani.md](10-Aurora与Frangipani.md)——Aurora 的法定数是本讲「灵活/非对称 quorum」思路的工业版本。
- **跨书**：
  - [../设计数据密集型应用/05-复制.md](../设计数据密集型应用/05-复制.md)——复制三种路线（主从/多主/无主）与 quorum 的工程口径；
  - [../分布式系统/07-复制与一致性.md](../分布式系统/07-复制与一致性.md)——教材口径的一致性协议分类；
  - [../深入理解分布式共识算法/09-Paxos变种算法的发展史.md](../深入理解分布式共识算法/09-Paxos变种算法的发展史.md)——灵活法定数等变种。

> **一句话总结本讲**：复制拓扑的选择，本质是「**定序权给谁、提交点在何处、读能扩散到哪**」三个问题的组合。
> 链式复制给了第三个问题一个漂亮的答案，代价是第二个问题变慢。
