# L11 Dynamo：高可用 key-store 的设计

> 阅读：DeCandia et al., *Dynamo: Amazon's Highly Available Key-value Store*, SOSP 2007
> 主线：本课"AP 阵营"的代表作——为了可用性主动放弃线性一致（对照 L10）。

## 1. 核心问题

- 场景：亚马逊购物车/结账等** always-on 服务**——拒绝写入的商业代价
  远大于"读到稍旧数据"的代价。这决定了全篇取向：**可用性 > 一致性**。
- 需求画像：读多写少、简单 key-value、可容忍最终一致、
  数据量到必须分区、运营要求"零停机 + 增量扩容 + 商用硬件"。
- 与 Raft/Spanner（CP）的分野：**Dynamo 明确选择分区时少数派仍可读写**。

## 2. 设计与取舍

### 2.1 去中心化：一致性哈希 + Vector Clock
- **一致性哈希（consistent hashing）**：把 key 空间哈希到环上，
  每个节点负责一段——**扩容只影响相邻节点，数据迁移量 O(1/N)**
  （对照 L23 DHT 的 Chord，思想同源）。虚拟节点（vnode）抹平负载倾斜。
- 每个 key 复制 N 份（默认 3），由环上顺时针 N 个协调者负责。
- **向量时钟（vector clock，L07）**：给每次写打上
  `{node: counter}` 向量，读时合并多个副本的版本 → 
  能**检测**并发写（分叉），交给上层调和（siblings），**不自动解决**。

### 2.2 读写协议：R + W > N 的 quorum
- 写：W 个副本确认即返回；读：R 个副本，取向量时钟最大版本。
- `R + W > N` → 读写集合必相交 → **大概率读到最新（但不保证线性一致**，
  因为并发写交错的写集/读集相交规则只保证"因果序不乱"）。
- 允许 W=1/N：牺牲持久性换写延迟（亚马逊配置成"宁可多副本异步补齐"）。

### 2.3 副本同步三板斧
- **Read Repair**：读时发现有旧版本副本 → 后台异步写回最新（读顺带修复）。
- **Merkle 树反熵（anti-entropy）**：节点周期性比对哈希树找差异补数据
  （对照 L19 链式复制的反熵、比特币区块头 L24）。
- **Sloppy Quorum + Hinted Handoff**：目标节点宕机时先写给"替补"节点并留 hint，
  原节点恢复后送回 → 把"N 台里挂 1 台就拒绝写"变成"几乎总能写"
  ——**这是 Dynamo 可用性魔法的核心一招**。

### 2.4 对象存储与失效
- 值大 → 用 **MySQL/Berkeley DB 式的对象存储 + tombstone 处理删除**
  （LSM 血统，与 L04 呼应；删除必须靠墓碑等 compaction）。

## 3. 论文间脉络

- 对 L10：Dynamo 是"最终一致 + 会话保证（读己之写、单调读）"的工业样板。
- 对 L05-L08：没有共识 → 无法在并发写时裁定唯一胜者 → 只能把冲突抛给应用。
- 对 L23：一致性哈希与 DHT 属同一去中心化定位技术；Dynamo 中心是"协调者"而非纯 P2P。
- 主线：本讲把"一致性—可用性"权衡做成可调旋钮（R/W/N），
  是三角权衡最具体的工程呈现。

## 4. 跨课程联系

- **15-445/15-721**：quorum 读写 ↔ 数据库多数派复制；向量时钟 ↔ MVCC 版本依赖图；
  read repair ↔ 复制日志的追赶（catch-up）。
- **CS149**：一致性哈希环 = 数据的分布式寻址结构，与并行程序里
  哈希分布/负载均衡一脉。
- **自顶向下网络**：DHT/一致性哈希与 CDN、P2P 内容定位共享"去中心化路由"思想。
- **6.S081**：tombstone + compaction 与文件系统延迟删除/日志回收同构。

## 5. 开源项目中的应用

- **Cassandra / ScyllaDB / Riak / DynamoDB**：Dynamo 的直系后代，
  Cassandra 直接把"一致性哈希 + vnode + quorum + read repair + hinted handoff"全套继承。
- **Voldemort / Project Voldemort**：LinkedIn 的开源复刻。
- **Redis Cluster**：用哈希槽（slot）替代哈希环做分区，仍是 quorum + 异步复制谱系。
- **TiKV（PD 调度）/ CockroachDB Rebalancer**：range 迁移借鉴"增量扩容少搬数据"。
- 冲突调和：现代 API 的 CRDT（如 Riak 的 OR-set、Ant Farm）是"自动解决 siblings"
  对 Dynamo"交给应用"的回应（延伸阅读）。

## 6. 延伸阅读

- Voids: *DynamoDB 单表设计* 与 AWS "Consistency Models" 文档（强一致/最终一致开关即本讲）。
- Shapiro et al., *Conflict-free Replicated Data Types* (CRDT, 2011)——自动调和分叉。
- Cassandra 官方文档 "About lightweight transactions (Paxos)"——AP 系统里嵌一个 CP 通道的现实案例。
- 课内对照题：Dynamo 的 R+W>N 为什么给不了线性一致？画一个违反实时序的历史。
