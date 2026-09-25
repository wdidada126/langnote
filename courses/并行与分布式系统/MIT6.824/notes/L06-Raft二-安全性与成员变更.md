# L06 Raft（二）：安全性、持久化与成员变更

> 阅读：Ongaro & Ousterhout ATC 2014（后半）+ Ongaro 博士论文 §5.4/§6
> 对应 Lab：pg3（持久化 + 快照）。本讲把 Raft 从"算法"变成"可部署的系统"。

## 1. 安全性（Safety）四条性质

Raft 的"活法"很多（超时随机、流水线含糊），但**绝不允许**出现：
1. **选举安全性**：一个 term 至多一个 leader（投票一次 + 多数派）。
2. **Leader 追加性**：leader 只追加自己的日志，从不删除/覆盖已提交条目。
3. **日志匹配性**：若两条日志在某副本上 term.index 相同，则此前所有条目相同
   （由 AppendEntries 一致性检查 + 强制回退归纳证明）。
4. **状态机安全性**：任一副本应用到状态机的条目，其他副本一旦应用必同序同内容。

### 4.1 危险案例与对策（面试高频）
- **旧 leader 用大任期偷覆盖未提交日志** → 对策：**禁止基于"日志里存在"就 commit**，
  只统计当前 term 条目的多数派（图 4.3 反例）；更早 term 的条目**间接提交**。
- **已提交条目可能被选不上/被覆盖** → 对策：**选举限制**（L05）保证 leader 日志
  包含全部已提交条目；follower 端 AppendEntries 仍可能短暂缺失 → 
  leader 必须**暴力回退补齐**（nextMatch 递减重试），不允许"跳过空洞"。
- **重启后失忆**（忘了自己投过谁/commit 到哪）→ 持久化 `currentTerm, votedFor, log`
  三件套必须先落盘再动作，重启重放（pg3 的全部工作量）。

## 2. 快照与日志压缩（pg3 核心）

- 日志无界增长 → 定期对状态机做 **snapshot**（LSM 的 compaction 视角：
  把"历史"折叠成"当前状态 + 截断点"）。
- **包含 lastIncludedIndex/Term 的快照**让 Raft 逻辑透明跨过截断区：
  选举比较、AppendEntries 匹配都用它替代真日志头。
- InstallSnapshot RPC + 速率限制：落后太多的 follower 不再逐条重放。
- **直传快照的陷阱**：快照与 leader 后续 AppendEntries 竞态 → 快照里含配置项，
  到达后若截断点已被超越要丢弃（lab 里最常见的 bug 源）。
- 与 L04 呼应：LSM = "用不断 compact 的有序结构近似状态机"；
  Raft 快照 = "用状态机当前值近似日志"。同一思想：**折叠历史，保留可续推的现在**。

## 3. 成员变更（Membership / Joint Consensus）

### 3.1 为什么危险
直接换配置 → 新旧两拨人各按自己的多数派**同时选出两个 leader**
（C_old={S1,S2,S3}，C_new={S2,S3,S4,S5}，S1 选 L1，S4/S5 选 L2）→ 脑裂。

### 3.2 两阶段联合共识
`C_old → C_old,new（双方多数派都同意才提交）→ C_new`。
任何时刻只有一个配置处于"活跃投票"状态，且其多数派与另一阶段相交 → 不可能双决。

### 3.3 工程现实：single-step change
实践中（etcd/TiKV/CockroachDB）**每次只加/减一个节点**：
此时新旧多数派必相交，无需联合配置——用"运维纪律"换算法简化。
配套问题：新节点追日志（Learner 状态）、旧节点何时停服
（"离开集群前要先观察到新配置提交"防退役 leader 幽灵）。

## 4. 客户端协议（linearizable read 伏笔）

- 命令带 clientID + requestID **去重** → 把 RPC 的 at-most-once 语义凑齐
  （重试安全；对照 L01）。
- 读请求走 Raft 代价大（一个 RTT + 多数派）→ 
  **Lease Read / ReadIndex / 线性izable read**：leader 用"我的心跳证明了多数派
  还认我"来直接服务读。正确性依赖时钟上界假设——与 L07 HLC、L15 TrueTime 一脉相承。

## 5. 论文间脉络

- L05 给了机制，L06 给机制**加上"绝不出错"的证明义务**；
  L08 Paxos 展示同一问题的另一解，L10 线性一致性给出"正确"的形式化定义。
- L09 把 Raft 装进 KV 状态机；L12 ZAB 是"Raft 之前的工业近亲"。

## 6. 跨课程联系

- **15-445**：快照/截断 ↔ checkpoint + WAL truncate；成员变更 ↔ 数据库在线扩容
  （rebalancing）；Lease Read ↔ 主从复制里"读主"的线性一致性论证。
- **6.S081**：先落盘再动作 = fsck 前的 WAL 纪律；"重启丢内存"= 崩溃恢复模型。
- **MLC/分布式训练**：PS 架构里 meta/调度一致性也常用 Raft（如 TiKV 支撑的
  分布式训练参数存储）；成员变更 ↔ 弹性伸缩的节点上下线。

## 7. 开源项目中的应用

- **etcd**：`ConfChangeV2` 支持批量变更（内部实现联合共识变体）；
  `Progress` 的 `Match/Next` 即 log matching 的工程形态。
- **TiKV**：Raft Learner + `region merge/split` + hibernate（省心跳）；
  Follower Read（ReadIndex 变体）。
- **CockroachDB**：Leaseholder 机制把"谁是 leader"缓存到 client，
  配合 250ms clock offset 上界做不确定性区间读（L07/L15 的落地）。
- **Kafka KRaft / RabbitMQ Quorum Queue / MinIO（Raft 管元数据）**。

## 8. 延伸阅读

- raft.es 网站 "RAFT: consensus made easy" 动画 + 论文图 4.3/4.4 反例亲手推一遍。
- Diego Ongaro 博客 "Raft 安全性证明" 系列（transient log loss 的讨论）。
- 对照阅读 etcd RFC "linearizable reads" 与 CockroachDB 的 leaseholder 文档。
