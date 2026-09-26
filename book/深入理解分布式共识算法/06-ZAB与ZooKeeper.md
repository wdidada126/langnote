# 第 6 章 ZAB——ZooKeeper 技术核心

> 覆盖原书第 5 章（第 2 篇，P101–163）：5.1 Chubby简介（是什么 / 为什么选择锁服务 / 需求分析 / 集群架构）；
> 5.2 ZooKeeper的简单应用（是什么 / 数据节点 / Watch机制 / ACL权限控制 / 会话 / 读请求处理）；
> 5.3 ZAB设计（背景分析 / 为什么不直接用Paxos / ZAB简介 / 事务标识符 / 多数派机制 / Leader周期）；
> 5.4 ZAB描述（选举 / 成员发现 / 数据同步 / 消息广播 / 算法小结）；
> 5.5 ZooKeeper中的ZAB实现（选举 / 发现 / 同步 / 广播 / 小结 / 算法模拟 / 提案的安全性）；
> 5.6 ZooKeeper成员变更（变更过程 / 并行变更）；5.7 ZooKeeper源码实战（启动 / 选举 / 初始化 / 发现 / 同步 / 广播）。

## 本章地图

本章是全书**唯一一个「为某个具体系统定制的共识协议」**章节，主线是血缘与取舍：

```
Chubby（Google，锁服务，Paxos 内核，OSDI 2006）
   │  开源世界需要一个等价物
   ▼
ZooKeeper（Yahoo!，wait-free 协调，ATC 2010）
   │  为什么不直接用 Paxos？（5.3.2）
   ▼
ZAB（ZooKeeper Atomic Broadcast，DSN 2011）：为主备顺序广播定制
   │
   ▼
四阶段：Leader 选举 → 成员发现（Discovery）→ 数据同步（Sync）→ 消息广播（Broadcast）
```

- **5.1–5.2**：先把「为什么需要协调服务」讲清楚（锁服务 vs 共识库、znode 树、watch、session、读路径）；
- **5.3**：ZAB 的设计动机——**主序（primary order）**：所有写都经由 primary，primary 提出的顺序即全局顺序，换主时保证「已 deliver 的事务前缀不丢」；
- **5.4–5.5**：协议描述与 ZooKeeper 的实现（Fast Leader Election、zxid、epoch）；
- **5.6–5.7**：成员变更与源码路径。

## 核心精讲

### 5.1 Chubby：为什么是「锁服务」而不是「共识库」

Burrows（OSDI 2006）给出的理由至今成立：

- 共识库要求**每个开发者都懂共识**才能用对；锁服务把复杂性收进服务端，客户端只调 `Open/Lock/GetContents`；
- 「粗粒度锁」（持有数小时）比「细粒度锁」更契合数据中心场景，容量压力小；
- 顺便提供**名字服务**（小文件存储 + 目录），这成为 Chubby/ZooKeeper 后来最广泛的用法；
- 架构：一个 Chubby cell = 约 5 台机器，用 Paxos 选 master 并复制数据库；客户端经 master 读写，非 master 只做转发。

### 5.2 ZooKeeper 的数据模型与读路径

| 概念 | 含义 | 工程注意 |
| --- | --- | --- |
| znode | 层级命名空间中的节点（持久 / 临时 / 顺序节点） | 临时节点（EPHEMERAL）与 session 绑定，是「存活探测」的实现基础 |
| Watch | 一次性触发器 | **一次性**——触发后需重新注册，否则会漏事件（经典坑） |
| ACL | 基于 `scheme:id:permission` 的访问控制 | 与 UNIX 权限不同：znode 的 ACL **不继承** |
| Session | 客户端与服务器的会话，带超时与心跳 | session 过期 → 临时节点被删除、watch 丢失 |
| 读请求处理 | 由客户端所连服务器**本地处理** | 默认读**不保证读到最新**；需要更强保证要调 `sync()`（🔧 见「常见误区」） |

### 5.3.2 为什么 ZooKeeper 不直接使用 Paxos

这是本章最有价值的一节，结论有三条（与 Junqueira 等的 DSN 2011 论文口径一致）：

1. **Paxos 允许「空洞」与「乱序选定」**：Basic/Multi-Paxos 的每个 instance 独立选值，换主时可能出现「后面的槽位已选定、前面的还没有」；而状态机应用需要**按序**。ZooKeeper 想要的是**主序（primary order）**：primary 提出事务的顺序就是 deliver 的顺序。
2. **需要「前缀属性（prefix property）」**：若事务 $m$ 被 deliver，那么 primary 在 $m$ 之前提出的**所有事务**都已被 deliver。这条保证让「新 leader 上任时先把已提交前缀补齐」成为自然流程，也让客户端的 watch 语义可预测。
3. **恢复优先于服务**：ZooKeeper 要求新 primary 在对外服务前，先把已提交前缀推给 quorum；Paxos 没有这一强制阶段。

### 5.3.4 事务标识符 zxid 与 5.3.6 Leader 周期（epoch）

- **zxid = (epoch, counter)**：高 32 位是 epoch（leader 周期），低 32 位是该周期内的单调计数；
- **epoch 的作用**：每次换主 epoch 递增，用于**区分不同 leader 时代**的提案，防止旧 leader 的残留提案被误认为有效。

```text
// 教学示意：ZAB 的 zxid 与四阶段骨架（不参与构建、不编译、不运行）
struct Zxid { epoch: u32, counter: u32 }     // 比较：先比 epoch，再比 counter

// 阶段 1 选举：选「日志最新」的候选 —— 比较 (epoch, zxid, sid)，取最大者
// 阶段 2 发现：收集 quorum 的 lastZxid，据此生成 newEpoch 并广播
// 阶段 3 同步：把新 Leader 的已提交前缀推给 Follower，补齐/截断差异
// 阶段 4 广播：类 2PC —— Proposal → Ack → Commit，zxid 严格递增

fn broadcast(cmd):                           // 阶段 4
    zxid = Zxid(currentEpoch, ++counter)
    writeLocalLog(zxid, cmd); fsync()
    broadcast(PROPOSE, zxid, cmd)
    wait quorum(ACK(zxid))                   // 多数派 ack 即可提交，不需全体
    broadcast(COMMIT, zxid)
    deliver(cmd)                             // 严格按 zxid 顺序应用到状态机
```

> 注意 ZAB 的广播阶段**类 2PC 但不需要全部参与者响应**：只要多数派 ack 就 commit，且 follower 不需要显式回复「commit 完成」。这与 Raft 的「多数派写入即 commit、后续消息携带 commitIndex」效果相似、机制不同。

### 5.4 四阶段的作用分工

| 阶段 | 目的 | 关键动作 |
| --- | --- | --- |
| Leader 选举 | 选出一个**日志足够新**的节点 | Fast Leader Election：比较 `(epoch, zxid, sid)` 取最大 |
| 成员发现 | 让准 Leader 与 quorum 就「新 epoch」达成一致 | 收集 follower 的 `lastZxid`，生成并广播 `newEpoch` |
| 数据同步 | 消除副本差异，保证前缀属性 | 由 Leader 决定同步方式（增量 / 截断 / 全量快照），follower 按指令补齐 |
| 消息广播 | 稳态下复制新事务 | Proposal → Ack → Commit |

### 5.5.7 提案的安全性

ZAB 的安全性依赖两条：

1. **quorum 相交**：任何两个 quorum 有公共节点，保证「已 commit 的事务」必然出现在新 Leader 的日志里，从而被同步阶段带到 quorum；
2. **epoch 单调且只在 quorum 上建立**：新 epoch 必须在 quorum 上确认，旧 epoch 的提案不可能在新 epoch 中复活——这正是 ZAB 版本的「幽灵日志」防御（对照 [05-Multi-Paxos与PhxPaxos工程实现.md](05-Multi-Paxos与PhxPaxos工程实现.md)）。

### 5.6 成员变更

- **变更过程**：ZooKeeper 3.5 起提供**动态重配置**（`reconfig`），集群成员本身作为一个被 ZAB 复制的配置；变更需要**两类 quorum 都响应**：当前配置的多数派 + 新配置的多数派（与 Raft 联合共识同源）。
- **并行变更**：多笔变更必须串行化，否则会出现「中间配置无人拥有多数派」的窗口；实践中由 Leader 串行下发，并要求新配置同样满足多数派可达。

> ⚠️ 本书 5.6 的具体变更步骤**未能核实原文**（大纲只给小节名）；上面是「双 quorum、串行变更」这一公认思路的表述。

### 5.7 源码实战的阅读路径

| 阶段 | 关注点 |
| --- | --- |
| 启动 | 加载 `currentEpoch` / `acceptedEpoch` / `lastLoggedZxid`，进入 LOOKING |
| Leader 选举 | Fast Leader Election 的选票结构 `(epoch, zxid, sid)` 与选票仲裁 |
| Follower/Leader 初始化 | 建连、QuorumCnxManager 的双向连接管理 |
| 成员发现 | `newEpoch` 的协商与 follower 的 ack |
| 数据同步 | 同步方式的判定分支与 follower 的落盘 |
| 消息广播 | Proposal 的持久化、ack 计数、commit 下发与状态机应用 |

## 版本演进

- **2006**：Chubby（OSDI 2006）确立「锁服务」范式，并公开其内部使用 Paxos；
- **2008**：Reed & Junqueira 在 LADIS 提出《A simple totally ordered broadcast protocol》，ZAB 雏形；
- **2010**：ZooKeeper 论文（USENIX ATC 2010）落地，提出 wait-free 协调与「写线性化 + 每客户端 FIFO」的目标；
- **2011**：Junqueira, Reed, Serafini 的 DSN 论文正式描述 ZAB（primary-backup 顺序广播）；
- **2013–2015**：ZooKeeper 3.5 引入动态重配置；同期 etcd/Raft（2014）出现，开始分流新系统；
- **2021–2022**：**Kafka 通过 KIP-500 引入 KRaft（Kafka Raft metadata mode）**，用内置 Raft quorum 替代 ZooKeeper 保存元数据；自 Kafka 3.3（2022）起官方将其标记为生产可用，并在后续版本中移除对 ZooKeeper 的依赖——**这是对 ZAB/ZooKeeper 生态影响最大的一次迁移**；
- **2023（本书）**：仍把 ZooKeeper/ZAB 作为协调服务的默认范本讲述（合理，因为存量系统极多）；
- **2026 视角**：新系统首选 etcd（Kubernetes 生态），ZooKeeper 主要出现在 Hadoop/Kafka 存量集群与老中间件中；「协调服务」这一范式本身被保留下来。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Burrows《The Chubby lock service for loosely-coupled distributed systems》 | OSDI 2006 | 锁服务范式，ZooKeeper 的思想源头 |
| Reed & Junqueira《A simple totally ordered broadcast protocol》 | LADIS 2008 | ZAB 雏形 |
| Hunt et al.《ZooKeeper: Wait-free coordination for Internet-scale systems》 | USENIX ATC 2010 | ZooKeeper 系统论文 |
| Junqueira, Reed, Serafini《Zab: High-performance broadcast for primary-backup systems》 | DSN 2011 | **ZAB 正式论文** |
| Lamport《Paxos Made Simple》 | ACM SIGACT News 2001 | 5.3.2「为什么不直接用 Paxos」的对照物 |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | Raft：与 ZAB 同为强 Leader，但规格更完整 |
| Apache Kafka 社区《KIP-500: Replace ZooKeeper with a Self-Managed Metadata Quorum》 | Apache Kafka 设计文档 | KRaft 的设计来源 |

## 近年研究与工业界开源实践（2015–2026）

> star 数均为 2026-09 用 `gh api repos/OWNER/REPO --jq '.stargazers_count'` 实测。

- `apache/zookeeper`（**12,811★**）：本章主角，ZAB 的参考实现。存量极广（Hadoop、HBase、Kafka 旧版本、Dubbo 等注册中心依赖它）；3.5 起支持动态重配置。
- `etcd-io/etcd`（**52,310★**）：Raft 实现的协调服务，Kubernetes 默认元数据存储。与 ZooKeeper 的对照是本书缺失但对选型最重要的一节（🔧 见下）。
- `jepsen-io/jepsen`（**7,504★**）：Jepsen 对 ZooKeeper 有公开测试报告，是协调服务一致性宣称的第三方校验来源。
- **近年工业实践**：
  - **KRaft**（Kafka KIP-500）：Kafka 用自带 Raft quorum 管理元数据，**去掉 ZooKeeper 部署依赖**。这是 ZAB 生态最大的一次流失，也说明「共识层内嵌」已成趋势；
  - **共识内嵌化**：新系统倾向把 Raft 作为库内嵌（etcd-io/raft、hashicorp/raft、sofa-jraft），而不是部署一个独立协调服务；
  - **成员变更工程化**：ZooKeeper 动态重配置与 Raft 联合共识本质都是「双 quorum 交集」，工程重点是**变更串行化与可回滚**。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「ZooKeeper 读是线性一致的」 | 读由**客户端所连节点本地处理**，默认可能读到旧值；要读最新需先调 `sync()`。ZooKeeper 提供的是**写线性化 + 每客户端 FIFO 序**，读需显式加强 |
| 2 | 「ZAB 就是 Paxos 改名」 | ZAB 为**主备顺序广播**定制：强调主序与前缀属性，换主必先同步；Paxos 允许乱序选定与空洞 |
| 3 | 「Watch 是持久订阅」 | Watch **一次性触发**；触发后必须重新注册，期间事件会漏 |
| 4 | 「临时节点在连接断开时立即消失」 | 与 **session** 绑定，只有 session 超时才删除；网络闪断但 session 未过期时不会消失 |
| 5 | 「zxid 只是一个自增号」 | zxid = `(epoch, counter)`；epoch 用于隔离不同 leader 时代的提案，是安全性关键 |
| 6 | 🔧 本书以 ZooKeeper 为协调服务默认范本，需补 2026 生态事实 | 新系统主流已转为 **etcd**（`etcd-io/etcd` **52,310★**，K8s 生态）；ZooKeeper（**12,811★**）主要服务存量集群。选型应按「是否在 K8s 生态 / 是否已有 ZK 运维体系」判断，而非算法优劣 |
| 7 | 🔧 本书未覆盖 KRaft 对 ZooKeeper 的替代 | 补：**Kafka 通过 KIP-500 引入 KRaft**（内置 Raft 元数据 quorum），自 **Kafka 3.3（2022）** 起官方标记生产可用并逐步移除 ZooKeeper 依赖。这直接削弱了「ZooKeeper 是新系统标配」的前提，本书 2023 出版未能反映 |
| 8 | 🔧 本书未给出 ZK vs etcd 的读语义对照 | 补：ZooKeeper 读默认本地读、`sync()` 强化；etcd 默认**线性一致读**（ReadIndex），也提供串行读（更快但可能旧）。两者「默认档位」不同，迁移时最易踩坑 |
| 9 | 🔧 成员变更的「双 quorum」本质未点明 | 补：ZK 动态重配置与 Raft 联合共识都要求**新旧两个配置的多数派都响应**，否则会出现「旧/新配置下各有一个 leader」的窗口；因此变更必须串行化（本书 5.6.2 的「并行变更」正是要防这个） |

## 与其他章 / 其他书的联系

**本目录内**

- [04-Paxos.md](04-Paxos.md) / [05-Multi-Paxos与PhxPaxos工程实现.md](05-Multi-Paxos与PhxPaxos工程实现.md)：5.3.2 的「为什么不直接用 Paxos」必须读完前两章才成立。
- [07-Raft.md](07-Raft.md)：ZAB 的 epoch ↔ Raft 的 term；ZAB 的数据同步 ↔ Raft 的日志对齐；两者都是强 Leader，但 ZAB 靠同步阶段保证前缀属性，Raft 靠日志匹配 + 选举限制。
- [08-Raft工程实践与SOFAJRaft.md](08-Raft工程实践与SOFAJRaft.md)：本书 6.10.2「Raft 与 ZAB 的异同」的展开版。
- [02-从ACID和BASE到CAP.md](02-从ACID和BASE到CAP.md)：ZooKeeper 是典型 CP 系统；读路径决定了它对外的 C 档位。

**跨书**

- [../深入理解分布式系统/10-案例研究文件系统与协调服务.md](../深入理解分布式系统/10-案例研究文件系统与协调服务.md)：协调服务的案例视角，与本章系统论文互补。
- [../分布式系统概念与设计/10-协调与协定.md](../分布式系统概念与设计/10-协调与协定.md)：共识与协调服务的教科书口径。
- [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)：架构视角下「要不要引入协调服务」的判据。
- [../分布式数据库入门进阶与实战/09-共识算法.md](../分布式数据库入门进阶与实战/09-共识算法.md)：把 ZAB 放回「原子广播 vs 共识」的工程语境。
</content>
