# L19 链式复制与 CRAQ：读扩展的一致性复制

> 阅读：van Renesse et al., *Chain Replication for Supporting High Throughput and Availability*, OSDI 2004；
> 辅读：Terrace & Freedman, *Object Storage on CRAQ: High-throughput Strengthened Consistency*, ATC 2009
> 主线：在"主从（太脆）/ 共识（太贵）"之外的第三条复制路线——用链换吞吐与线性一致读。

## 1. 核心问题

- 主从异步复制（L04 Bigtable 早期）：读任意副本可能读到旧值；
  主挂 → 数据丢失/分叉风险。
- 共识（L05/L08）：写要多数派往返，**读也要走 leader** → 读无法像副本数那样线性扩展。
- 链式复制的问题意识：**能否用"固定顺序的转发链"同时拿到：
  写的强一致、读的任意副本扩展、故障时近乎无损切换？**

## 2. Chain Replication（CR, 2004）

- 拓扑：对每个对象集（storage unit）构造一条**严格排序的副本链**：
  head（接收写）→ middle → tail（唯一提交者）。
- **写协议**：客户端 → head；每个副本"本地持久化未提交版本 → 转发后继"；
  **tail 提交并回执**，ACK 沿链回传。
  → 天然全序（同一条链、同一 head），**无需投票/选举即可线性一致**——共识被"拓扑"替代。
- **读协议（原版）**：只能在 tail 读（它是唯一"干净"副本）→ 读扩展不佳，引出 CRAQ。
- **管理**：由 **reconfiguration daemon（链管理器）**负责增删节点、重组链；
  视图（view）带单调 epoch（又是 fencing token，L05/L03 lease 一脉）。
- 容错：链断裂期间新配置装入前拒绝请求——可用性不如主从，
  但**比共识便宜**：写吞吐 = 单条链顺序 + 流水线。

## 3. CRAQ：读 anywhere 的强化版

- 引入**版本号 + dirty 标记**：写沿链打脏（携带新值+版本）；
  中间副本允许"**快照读（snapshot read）**"：
  - 本地干净 → 直接返回；
  - 脏 → 向下游询问"这条目提交了吗？值多少？"（tail 一定干净）→
    仍不需要 leader/共识，**读扩展 = 副本数**。
- **批量写**：写按版本区间打包转发，摊薄往返 → 论文实测写吞吐优于
  Dynamo/主从（同延迟下），读吞吐远超"读主"方案。
- 删除 = 特殊值；反熵（anti-entropy）修补缺失版本区间（对照 L11 Dynamo 的 Merkle 树）。
- **CRAQ 的线性一致读**证明是 L10 的绝佳应用题：快照读 + 下游确认
  如何保证"不读旧值"。

## 4. 工程影响与后续

- **Redis RAFT / RedisRaft、Aerospike（XP 协议思想近亲）、WDP/MemC3、
  FoundationDB（paxos 系但链式 log 思想浓）**：CR 家族的商业化散见。
- **直接后代**：微软 Azure Storage（**Stamp Service 的链式复制**是教科书案例：
  extent node 链 + stream 链），论文 *Azure Storage: A Highly Available Cloud Storage Service* (SOSP 2011) 必读——L13 S3 的"对象"在 Azure 用链式复制实现。
- **Cassandra 的 "lightweight transactions"（Paxos 区）** 与链式方案对照：
  同为"在最终一致底座上加一条强一致快车道"。
- 现代回响：TiKV/CockroachDB 的 **Follower Read + ReadIndex/LeaseRead**
  本质上是在共识系统里重获 CRAQ 式"读扩展"（L06 §4 的伏笔在此回收）。

## 5. 论文间脉络

- 谱系位置：主从（L04 原型）→ 链式（本讲：顺序换共识）→ 共识（L05/L08：多数派换灵活性）。
- 与 L13：Azure 链式 vs S3 quorum/EC——云存储两大复制路线对照。
- 与 L10：CR/CRAQ 给线性一致却不用共识 → 不违反 FLP？
  因为**链管理器仍是一个（需容错的）共识式组件**——"天下没有免费的线性一致"。

## 6. 跨课程联系

- **自顶向下网络**：链式转发 = store-and-forward 流水线；批量与延迟权衡同网络设计。
- **15-445**：链式写提交序 = 事务提交序的唯一化；
  对照数据库"同步复制"的 primary-standby → chain → quorum 三种复制拓扑演化。
- **CS149**：链上"未提交版本流水线传播" = 数据在算子间流动，与 Lightning 流水线神似。
- **6.S081**：视图 epoch / fencing ↔ 内核代际计数器（generation counter）。

## 7. 开源项目与应用场景

- 复现学习：**CRAQ 的 MinIO 分支讨论、链式 K/V 实验项目（如 chainstore）**。
- 概念输出：Raft 库普遍支持 **Learner 追链**；**Kafka ISR 的"追上即入链"**思想近似。
- 生产案例：Azure Storage 各代（SOSP'11/'17）、HDFS EC+链式写管道
  （**DataNode write pipeline 就是链式复制**：客户端→DN1→DN2→DN3 顺序转发，值得重读 L03 对照）。
- CAHA（OSDI 2020，本课讲义提过）：**混合部署共识组（consensus-as-a-service）**，
  在 CR/共识之间做资源弹性折中——延伸阅读首选。

## 8. 延伸阅读

- SOSP 2011 Azure Storage 论文（链式复制工业最大规模应用）。
- *Chain Replication for Storage Systems with High Water-Marks* 等 CR 变体论文（读扩展改进）。
- CAHA: Flexible and Cost-Efficient Consensus Using Shared Replication Groups (OSDI 2020)。
- 本目录 notes/L03/L05/L10 交叉：亲手推导"CRAQ 快照读为什么线性一致"。
