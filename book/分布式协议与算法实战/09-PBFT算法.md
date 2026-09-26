# 第 11 章 PBFT 算法

> 覆盖原书：第 11 章「PBFT算法」。
> 11.1 口信消息型拜占庭问题之解的局限、11.2 PBFT 是如何达成共识的、11.3 如何替换作恶的主节点、
> 11.4 PBFT 的局限、解决办法和应用、11.5 小结。
> 本章是本书第 1 章「拜占庭将军问题」的正式答案。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 11.1 口信消息解的局限 | OM(m) 的消息复杂度 O(n^(m+1))、领袖无法确定 | 理论可行但**不可工程化**，需要多项式复杂度 + 不需要确定叛徒是谁 |
| 11.2 PBFT 三阶段 | pre-prepare / prepare / commit | 3f+1 副本、**两轮所有节点广播**，在**异步但弱同步假设**下保证安全与活性 |
| 11.3 视图更换 | view change + new-view | 主节点作恶只是「不推进」而非「不安全」——**活性**靠视图更换修复 |
| 11.4 局限与应用 | O(n²) 消息、n 到几十就吃力 | 适合**联盟链/小规模许可网络**，不适合大规模公网 |
| 11.5 小结 | 与 CFT 的选型边界 | 只有「节点由互不信任方运维」才值得付 BFT 的代价 |

## 核心精讲

### 11.1 从 OM(m) 到 PBFT：解决了什么

| 维度 | 口信消息型（本书 1.2） | PBFT |
| --- | --- | --- |
| 消息复杂度 | 指数级 O(n^(m+1)) | **O(n²)**（多项式） |
| 是否需要「知道谁是叛徒」 | 需要递归比对 | 不需要，只要求**诚实节点行为一致** |
| 网络假设 | 同步（Lamport 原始模型） | **异步**，活性依赖弱同步（weak synchrony） |
| 是否需要签名 | 否（口信）/ 是（签名型） | 用 **MAC（消息认证码）**即可，比公钥签名快得多 |
| 容错阈值 | 3f+1 | 3f+1 |

### 11.2 三阶段协议

```
教学示意，不参与构建
// 角色：一个主节点 primary（视图 v 内），其余为备份节点 backup
// 状态：每个节点维护 view 号、已接受的消息日志

// 阶段 1: PRE-PREPARE（主节点 -> 所有备份）
primary on 收到 client 请求 m:
    分配序号 n（在同一个 view 内递增）
    broadcast PRE-PREPARE(v, n, digest(m))  // 只发摘要，不发全量
// 备份校验：view 正确、n 在可接受窗口内、摘要未被用过 -> 接受，进入 PREPARE

// 阶段 2: PREPARE（所有节点 -> 所有节点）
backup i on 接受 PRE-PREPARE:
    broadcast PREPARE(v, n, digest(m), i)
// 节点收到 2f 个（含自己）匹配的 PREPARE -> 进入 prepared 状态
//   prepared 的含义：「全网诚实节点已就 (v, n, m) 达成一致排序」

// 阶段 3: COMMIT（所有节点 -> 所有节点）
node on prepared:
    broadcast COMMIT(v, n, digest(m), i)
// 节点收到 2f+1 个匹配的 COMMIT -> 进入 committed-local，可以执行 m 并回复客户端
//   客户端等 f+1 个**相同结果**即认为完成（因为最多 f 个是作恶节点）
```

**为什么是 2f+1 而不是多数派**：
CFT 只要 2f+1 个节点里「多数派（f+1）」即可，因为崩溃节点不说话；
BFT 里 f 个节点可能**说假话**，所以必须从 **3f+1** 个节点中收集到 **2f+1** 个一致回复，
才能保证「其中至少 f+1 个是诚实的」，从而压过 f 个作恶者的干扰。

**为什么需要 commit 阶段**（这是最常被问的问题）：

- `prepared` 只在**当前 view** 内有意义；
- 视图更换时，新主节点必须能证明「某个序号确实已被全网准备好」；
- 只有收到 2f+1 个 COMMIT，才能确保**跨 view 也成立**——即 `committed-local` 具有跨视图的稳定性。

### 11.3 视图更换：修复的是活性而非安全性

```
教学示意，不参与构建
// 触发：备份节点的定时器在收到合法请求后超时未执行 -> 怀疑主节点作恶/卡住
backup i: view += 1; broadcast VIEW-CHANGE(v+1, n, P, Q, i)
//   P = 本地 prepared 的消息集合证明；Q = pre-prepare 证明
// 新主节点（编号 = (v+1) mod N）收集 2f+1 个 VIEW-CHANGE
new primary:
    构造 NEW-VIEW(v+1, V, O)：
      V  = 各 VIEW-CHANGE 的证明集合
      O  = 新的 pre-prepare 集合
        - 对 V 中「已 committed」的序号：沿用原请求（不能改！）
        - 对 V 中最高 prepared 序号之后、且无人 prepared 的：可填 null（空操作）
    broadcast NEW-VIEW
// 关键安全性约束：一旦某序号在旧 view 中 committed，新 view 必须沿用同一请求
```

> **安全性与活性的分工**：PBFT 的安全性（不会有两个不同请求在同一序号上被提交）
> **不依赖主节点诚实**；主节点作恶只会造成**不推进（活性受损）**，由视图更换修复。
> 这是本书 11.3 最重要的结论。

### 11.4 局限

| 局限 | 表现 | 常见缓解 |
| --- | --- | --- |
| 消息复杂度 O(n²) | n=100 时一次共识广播上万条消息 | 委员会/分片、聚合签名（BLS） |
| 视图更换昂贵 | 换主需要传所有 prepared 证明 | 流水线化、checkpoint 截断日志 |
| 无法抵御 Sybil 攻击 | 「节点」身份必须事先授权 | 许可网络（联盟链）+ PKI |
| 客户端也要容错 | 需等 f+1 个一致回复 | 客户端库封装 |

## 版本演进

- **1982**：Lamport/Shostak/Pease 提出拜占庭将军问题（本书第 1 章）。
- **1999**：Castro & Liskov 在 OSDI 发表《Practical Byzantine Fault Tolerance》，
  第一次让 BFT 在**异步网络**里达到接近非拜占庭系统的性能（相对于理论方案是数量级改进）。
- **2000s**：PBFT 长期停留在研究圈；直到区块链兴起才被大规模关注。
- **2016**：**Tendermint**（Kwon, 2014 白皮书；Buchman et al. 2018 论文）把 PBFT 简化为
  **propose / prevote / precommit** 两轮投票 + 锁定机制，成为 Cosmos 生态的共识核心。
- **2019**：**HotStuff**（Yin et al., PODC 2019）实现**线性视图更换**（O(n) 消息复杂度），
  被 Libra/Diem 采用，是 PBFT 的里程碑式改良。
- **2022（本书）**：第 11 章按「口信解的局限 → 三阶段 → 视图更换 → 局限」组织，结构清晰。
- **2026 视角**：
  - **HotStuff 系已成为工程主流**（含其变体 Chained HotStuff、Jolteon、Bullshark 等 DAG-BFT）；
  - **DAG-based BFT**（如 Narwhal & Tullahi、Bullshark、Sui 的 Mysticeti）把**数据传播与共识排序解耦**，
    显著提升吞吐，是 2022 年之后最重要的新形态；
  - 联盟链侧，`hyperledger/fabric`（**16732★**）从早期 PBFT 走向 **Raft（CFT）+ 可插拔 BFT**，
    说明**许可链里 CFT 常常就够**——这一点值得与本书 11.4 的应用建议对照。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Lamport, Shostak, Pease《The Byzantine Generals Problem》 | ACM TOPLAS 1982 | 拜占庭问题与下界（本书 1.2 / 11.1） |
| Castro & Liskov《Practical Byzantine Fault Tolerance》 | USENIX OSDI 1999 | PBFT 原始论文，本书第 11 章的正式出处 |
| Castro & Liskov《Practical Byzantine Fault Tolerance and Proactive Recovery》 | ACM TOCS 2002 | PBFT 期刊版，含主动恢复 |
| Yin, Malkhi, Reiter, Gueta, Abraham《HotStuff: BFT Consensus with Linearity and Responsiveness》 | ACM PODC 2019 | 线性视图更换，PBFT 的里程碑改良（本书未涉及） |
| Buchman, Kwon《Tendermint》相关论文《The latest gossip on BFT consensus》 | arXiv 2018 | Tendermint 共识的形式化（本书未涉及） |
| Kwon《Tendermint: Consensus without Mining》 | 2014 白皮书 | Tendermint 原始设计（本书未涉及） |
| Danezis et al.《Narwhal and Tullahi: DAG-based Mempool and Efficient BFT Consensus》 | EuroSys 2022 | DAG-BFT，2022 后的主流新形态（本书未涉及） |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **HotStuff 系**（2019 起）把视图更换降到线性复杂度，并支持**流水线化（chained）**；
  - **DAG-BFT / 异步共识**：Narwhal-Tullahi（EuroSys 2022）、Bullshark、Mysticeti，
    把「传播」与「排序」解耦，吞吐上一个台阶；
  - **聚合签名（BLS）与委员会**把 PBFT 的 O(n²) 消息降到可接受范围，使 n 可达数百；
  - **BFT 与 CFT 的边界再讨论**：许可链（联盟链）中节点由已知机构运维，**CFT + 审计**通常更划算。
- **工业界开源**（star 数 2026-09 `gh api` 实测）：
  - `hyperledger/fabric`（**16732★**）：联盟链主流；其排序服务从早期的 BFT 方案演进为 **Raft（CFT）为默认 + 可插拔共识**，是本章 11.4 「应用场景」的现实对照。
  - `bitcoin/bitcoin`（**90251★**）：**非 PBFT** 路线（PoW），是本书第 12 章的主角，与本章形成「许可 vs 无许可」的对照。
  - `etcd-io/etcd`（**52310★**）：CFT（Raft）代表，提示读者「绝大多数业务根本不需要 BFT」。
  - `apache/zookeeper`（**12811★**）：同为 CFT 代表。
- **Jepsen 实测**（`jepsen-io/jepsen`，**7504★**）：Jepsen 主要针对**数据库与协调服务**做一致性测试，
  **不覆盖区块链共识**；评估 BFT 系统应参考其公开的形式化证明与故障注入测试报告，而非 Jepsen。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「PBFT 的主节点作恶会导致不一致」 | 不会。主节点作恶只影响**活性**（不推进）；安全性由 prepare/commit 两轮 quorum 保证 |
| 2 | 「PBFT 只要 2f+1 个节点」 | 节点总数必须 **3f+1**；2f+1 是**要收集的一致回复数**，两件事别混 |
| 3 | 「PBFT 是同步协议」 | 安全性在**异步**下成立；**活性**需要弱同步假设（消息延迟的增长慢于超时） |
| 4 | 「PBFT 用了数字签名」 | 原论文主要用 **MAC**（对称）以获得性能；只有视图更换等处才用公钥签名 |
| 5 | 🔧 2026 补丁：缺 HotStuff 与线性视图更换 | 本书 11.3 的视图更换是 PBFT 原版（O(n²) 消息）。2019 年 **HotStuff** 已把视图更换降为**线性复杂度 + 响应性**，是工程实现的实际选择 |
| 6 | 🔧 2026 补丁：缺 DAG-BFT 这一新形态 | 2022 年后 **Narwhal/Tullahi、Bullshark、Mysticeti** 把数据传播与共识解耦，吞吐显著提升。本书 11.4 的「O(n²) 吃力」结论需要配合这些进展重新评估 |
| 7 | 🔧 2026 补丁：联盟链的真实选择常是 CFT | 本书 11.4 讲 BFT 的应用，但现实里 `hyperledger/fabric` 的**默认排序服务是 Raft（CFT）**。许可网络中「节点身份已知 + 有审计」时，BFT 的额外成本常常不划算 |
| 8 | 🔧 2026 补丁：未区分「共识安全」与「应用正确」 | BFT 保证的是**排序一致**，不保证**智能合约/业务逻辑正确**，也不解决**身份与准入**。区块链场景的多数事故出在这一层，与共识算法无关 |

## 与其他章 / 其他书的联系

- **本目录内**：
  - 本章是 [01-拜占庭将军问题与CAP-ACID-BASE](01-拜占庭将军问题与CAP-ACID-BASE.md) 1.2/1.3（口信与签名消息）的**直接答案**，两章必须连读；
  - 本章的「许可网络 BFT」与 [10-PoW算法与区块链](10-PoW算法与区块链.md) 的「无许可网络 PoW」是**同一问题的两种体制**，对比价值最大；
  - 本章的视图更换与 [03-Raft选举日志复制与成员变更](03-Raft选举日志复制与成员变更.md) 的 Leader 选举都是「换主」，但安全约束完全不同。
- **跨书**：
  - [../分布式算法/08-拜占庭与容错共识.md](../分布式算法/08-拜占庭与容错共识.md)——拜占庭共识的严格化处理，本章的形式化底座；
  - [../深入理解分布式系统/07-Raft与拜占庭容错.md](../深入理解分布式系统/07-Raft与拜占庭容错.md)——CFT 与 BFT 并列对比；
  - [../深入理解分布式共识算法/01-分布式共识算法概述.md](../深入理解分布式共识算法/01-分布式共识算法概述.md)——拜占庭与非拜占庭的分野；
  - [../分布式算法/03-FLP与不可能性.md](../分布式算法/03-FLP与不可能性.md)——解释为什么 BFT 也需要弱同步假设。
