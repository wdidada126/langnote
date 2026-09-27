# 第 1 章　ZooKeeper 核心理论

> 原书第 1 章是全书的理论底座：数据模型、Watch、角色、选举、ZAB、节点类型、简单 API。
> 但它是**最需要 2026 年补丁**的一章：1.5 把 Paxos 与 ZAB 混在一起只做「简介」，
> 而 ZAB 与 Paxos 的关系、1.7「奇数台」的底层数学、以及 ZK 在超大规模下的瓶颈，
> 本书都没讲透；Triple 协议所需的「协调服务」视角也完全没延伸到 Dubbo 3。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 1.1 ZooKeeper 的介绍 | ZK 是什么（分布式协调服务）、定位 | ZK 不是数据库，是**协调服务**（锁/配置/命名/选主） |
| 1.2 数据模型和 Watch | 树形 znode、Watcher 一次性触发 | 数据模型 = 精简文件系统；Watch 是**一次性**观察者 |
| 1.3 角色 Leader/Follower | 集群角色划分 | 写经由 Leader，Follower 提供读与投票 |
| 1.4 为什么要选举 | 单点不可靠 → 需选主 | 选主是为了**高可用**，不是为性能 |
| 1.5 Paxos 与 ZAB 简介 | 两个共识/原子广播协议的概念 | ZAB 是 ZK 专用原子广播，≠ 通用 Paxos |
| 1.6 选举算法 | 快速选举（Fast Leader Election） | 比早期 LeaderElection 更快收敛 |
| 1.7 为什么奇数台 | 容错公式 2N+1 | 奇数台在「同等容错下」最省机器 |
| 1.8 ZooKeeper 的特点 | 顺序一致、原子、可靠、实时（最终） | 顺序是 ZK 一切保证的源头 |
| 1.9 使用架构 | Client/Server、集群部署形态 | 客户端连任意节点，写统一走 Leader |
| 1.10 znode 节点类型 | 持久/临时、顺序/非顺序四种组合 | 临时节点是**会话绑定**，是分布式锁基础 |
| 1.11 运用场景 | 配置管理、命名、分布式锁、选主、队列 | 本质是「小规模元数据 + 协调」 |
| 1.12 五点保证 | 顺序一致、原子性、单系统镜像、可靠、及时 | 这五点定义了 ZK 的一致性边界 |
| 1.13 简单的 API | create/delete/exists/get/set/getChildren/sync | API 极简，复杂语义靠组合 |

## 核心精讲

（以下为教学性梳理，伪代码/Java 均**教学示意，不参与构建**。） 

### 1.2 数据模型与 Watch：树 + 一次性观察者

- ZK 的数据像一棵精简的文件系统：**znode** 是树上的节点，可挂数据（默认上限 1MB）和子节点。
- **Watcher 机制**是 ZK 实现「变更通知」的核心，但有两个坑：
  1. **一次性**：触发一次后即失效，想持续监听必须**重新注册**；
  2. **弱实时**：通知是**最终**到达，不保证网络分区恢复前一定收到。

```text
# 教学示意，不参与构建：Watch 的一次性语义
client 在 /config 上注册 Watcher
server 数据变更 -> 向 client 推送一个 WatcherEvent
client 收到后：Watcher 已失效
若想继续监听 -> client 必须再次 exists/getData/getChildren 并重新注册 Watcher
（这就是本书 4.20「自实现递归 watch」要解决的痛点）
```

### 1.3 / 1.4 角色与选举动机

- **角色**：Leader（唯一可写、提议者）、Follower（投票 + 提供读）、Observer（只提供读，不参与投票，扩展读吞吐）。
- **为什么选举**：单台 ZK 挂掉 → 整个协调服务不可用；多台组成 ensemble，靠**选主**保证
  即使挂掉部分节点仍有多数派可用。选主保证的是**可用性**，不是性能。

### 1.5 ZAB 与 Paxos（本章最易混淆点）

- **ZAB（ZooKeeper Atomic Broadcast）** 是 ZK 专用的**原子广播/崩溃恢复**协议，目标是
  「所有节点以相同顺序应用事务」。它和 Paxos 解决的问题相同（共识），但**设计不同**：
  ZAB 强调**主备（primary-order）**的有序广播，Paxos/Multi-Paxos 是更通用的提案共识。
- 本书把两者并列为「简介」容易让人以为 ZAB = Paxos，实际上 ZAB 是**为 ZK 定制的原子广播**，
  与 Raft 的「leader-based log replication」思路更接近（见下方版本演进补丁）。

### 1.6 / 1.7 快速选举与「奇数台」

- **Fast Leader Election**：节点间互发选票（epoch + zxid + myid），比较 (zxid, myid) 收敛出 Leader。
- **为什么奇数台**：容错需要「多数派存活」。N 台集群允许挂 ⌊N/2⌋ 台。
  - 3 台允许挂 1 台，4 台也只允许挂 1 台 → **4 台比 3 台多花一台机器却没多容错**；
  - 所以「2N+1 奇数」在同等容错下机器最省。注意：这**不意味着偶数不能跑**，只是性价比低。

### 1.10 znode 节点类型（四种组合）

| 类型 | 是否持久 | 是否顺序 | 典型用途 |
| --- | --- | --- | --- |
| 持久（PERSISTENT） | 是 | 否 | 配置、命名 |
| 持久顺序（PERSISTENT_SEQUENTIAL） | 是 | 是 | 公平队列、全局有序 ID |
| 临时（EPHEMERAL） | 否（会话结束即删） | 否 | **分布式锁、服务注册（本书 7.3 的临时节点注册）** |
| 临时顺序（EPHEMERAL_SEQUENTIAL） | 否 | 是 | **非公平锁转公平锁**（最小序号者获锁） |

> 临时节点是「服务注册」和「分布式锁」的物理基础：服务会话断开 → 节点自动消失 → 自动下线。

### 1.12 五点保证（ZK 的一致性契约）

1. **顺序一致**：客户端的更新按发送顺序生效；
2. **原子性**：更新要么全成功要么全失败；
3. **单系统镜像**：客户端无论连哪个节点，看到的数据视图一致（同一时刻）；
4. **可靠**：一旦更新成功，持续有效直到被覆盖；
5. **及时（最终）**：客户端在一定时间窗口内看到最新数据（非强实时）。

## 版本演进

- **本书无第二版**；本节写 2022 年口径 → 2026 年视角的变化。
- **1.5 必须补 Raft 视角**：ZAB 与 Raft 同属「leader-based 有序日志复制」，今天要理解 ZAB，
  用 Raft 对照反而更直观（etcd/OB/TiKV 全用 Raft）。本书成书时 Raft 已流行 8 年却未提及，是明显短板。
- **1.7「奇数台」需补下限与写瓶颈**：ZK 的写吞吐受限于**单一 Leader**；ensemble 大了读可加 Observer 扩展，
  但写不会随节点数线性增长。超大规模注册场景下 ZK 的写成为瓶颈（→ 见 06/07 的「应用级服务发现」补丁）。
- **1.2 Watch 的一次性痛点**：本书 4.20 自己实现了「递归 watch」，但 2026 年正确做法是
  用 **Curator 的 CuratorCache / TreeCache**（见 04）或客户端缓存，而非手写递归注册。
- **ZK 会话（session）风暴**：本书未讲「大量客户端重连导致 session 过期风暴」这一生产级事故模式；
  这是 ZK 做大规模注册中心时最经典的坑。
- **ZK 与 etcd 对照**：etcd（Raft、gRPC 接口、MVCC）在云原生时代大量替代 ZK 做协调/注册，
  本书把 ZK 当唯一真理，未给对照。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Hunt, Konar, Junqueira, Reed《ZooKeeper: Wait-free Coordination for Internet-scale Systems》 | USENIX ATC 2010 | **ZK 原始论文**，提出 ZAB 与 wait-free 协调原语 |
| Junqueira, Reed《Zab: High-performance Broadcast for Primary-backup Systems》 | DSN 2011 | **ZAB 协议**正式描述（原子广播） |
| Lamport《The Part-Time Parliament》 | ACM TOCS 16(2), 1998 | Paxos 原始论文（本书 1.5 提到的 Paxos） |
| Lamport《Paxos Made Simple》 | ACM SIGACT News 2001 | Paxos 通俗重述 |
| Ongaro, Ousterhout《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | Raft（理解 ZAB 的最佳对照） |
| Fischer, Lynch, Paterson《Impossibility of Distributed Consensus with One Faulty Process》（FLP） | JACM 1985 | 异步共识不可能性，所有共识协议的理论天花板 |
| Gilbert, Lynch《Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services》 | ACM SIGACT News 2002 | CAP 形式化（与本书 5.6 呼应） |

## 近年研究与工业界开源实践（2015–2026）

- **apache/zookeeper（12811★，2026-09 实测）**：仍大量服役于存量 Hadoop/Dubbo/HBase 系统，
  但新项目多转向 etcd / 专用注册中心。
- **apache/curator（3173★）**：ZK 的 Java 客户端事实标准封装，提供分布式锁、Leader 选举、
  缓存（Cache）、重试策略——是本书 04 章「自实现递归 watch」应替换为的工程化方案。
- **etcd-io/etcd（52310★ 量级）**：Raft + gRPC + MVCC，云原生协调/注册首选，是 ZK 的现代对照物。
- **alibaba/nacos（33419★）**：集注册中心 + 配置中心于一体，国产生态主流，本书 7.11–7.14 已引入。
- **一致性/协调的中文系统材料**：仓库 `../深入理解分布式共识算法/00-总览与阅读地图.md`
  有 Paxos/Multi-Paxos/ZAB/Raft/EPaxos 的逐算法推导，是本章 1.5 的必配对读材料。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「ZK 是数据库」 | ZK 是**协调服务**，单节点 1MB 上限、不适合存业务数据 |
| 2 | 「Watch 是持久订阅」 | Watch **一次性**，触发后需重新注册；想持续监听用 Curator Cache |
| 3 | 「ZAB = Paxos」 | ZAB 是 ZK 定制的**原子广播**协议，与 Paxos 设计不同、与 Raft 思路更接近 |
| 4 | 「偶数台不能部署」 | 偶数能跑，只是同等容错下比奇数多花机器，**性价比低**而非不能 |
| 5 | 「临时节点跨会话存在」 | 临时节点**绑定会话**，会话断开即删，是锁/注册的基础语义 |
| 6 | 「ZK 写能随节点数扩展」 | 写受**单一 Leader**限制，节点多了只扩展读（Observer） |
| 7 | 🔧 1.5 完全未提 Raft | Raft（ATC 2014）是理解 ZAB 的最佳现代对照，本书成书时已流行 8 年却缺位 |
| 8 | 🔧 1.2/4.20 手写递归 watch | 2026 年应直接用 Curator 的 Cache 体系，手写易漏注册导致「丢失通知」 |
| 9 | 🔧 未讲 ZK 会话风暴与容量瓶颈 | 大规模注册场景下 ZK 的 session 风暴、写瓶颈是生产级事故源，本书只讲「能跑」 |
| 10 | 🔧 未对照 etcd | 云原生时代 etcd 大量替代 ZK 做协调/注册，本书把 ZK 当唯一真理 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 1.10 临时节点 → [07-Dubbo实战技能.md](07-Dubbo实战技能.md)（7.3 用临时节点做服务注册下线）；
  - 1.5/1.6 选举 → [03-搭建ZooKeeper主从运行环境.md](03-搭建ZooKeeper主从运行环境.md)（集群选主落地）；
  - 1.2 Watch → [04-ZooKeeper常见命令和Curator的使用.md](04-ZooKeeper常见命令和Curator的使用.md)（watch 命令与 Curator）；
  - 1.7 容错 → [08-Dubbo高级技能.md](08-Dubbo高级技能.md)（集群容错的思想源头）。
- [../深入理解分布式共识算法/00-总览与阅读地图.md](../深入理解分布式共识算法/00-总览与阅读地图.md)
  ——本章 1.5 只给 ZAB/Paxos 轮廓，那里有 ZAB/Raft/Paxos 的完整推导，是**必配**材料。
- [../设计数据密集型应用/09-一致性与共识.md](../设计数据密集型应用/09-一致性与共识.md)
  ——DDIA 对线性一致性、顺序保证的现代讲法，与本章 1.8/1.12 直接对读。
