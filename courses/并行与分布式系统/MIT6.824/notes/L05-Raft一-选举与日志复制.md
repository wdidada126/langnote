# L05 Raft（一）：Leader 选举与日志复制

> 阅读：Ongaro & Ousterhout, *In Search of an Understandable Consensus Algorithm*, ATC 2014（前半）
> 对应 Lab：pg2/pg3。全课技术核心：共识 = 复制状态机的可行性证明。

## 1. 核心问题

- 场景：一台机器上的状态机（如 KV 的 Put/Get）不可靠 → **复制状态机（RSM）**：
  多份相同副本 + 相同的命令日志 + 按相同顺序执行 = 各副本状态必然一致。
  于是问题归约为：**共识（consensus）**——让集群对"日志条目的顺序"达成一致，
  且多数派持久化后才算提交。
- 前史：Paxos（L08 专讲）难以理解、难以工程化、单命令提案啰嗦。
  Raft 的目标是**可理解性**：分解为 leader 选举 / 日志复制 / 安全性三个相对独立的子问题。
- 关键前提：**crash-stop 故障模型 + 多数派（majority）**。
  网络分区时少数派不可用（CP），这正是与 Dynamo（AP，L11）的分水岭。

## 2. 设计与取舍

### 2.1 三种角色与任期
Follower / Candidate / Leader；**term（任期号）= 逻辑时钟 + fencing token**。
任一瞬间至多一个 leader（由"每 term 选举至多一票"保证）。
任何 RPC 里带上 term，收到更大 term 立刻臣服 → 过期 leader 自然退位（防脑裂）。

### 2.2 Leader 选举
- Follower 在 election timeout（150–300ms 随机）内没听到心跳 → 变 Candidate，
  term+1，向所有人 RequestVote。
- 投票规则（安全性第一道闸）：只投给"日志至少和我一样新"的候选人
  （先比最后条目 term，再比长度）→ **选举限制保证新 leader 一定包含所有已提交条目**。
- 拿到多数票 → 上位，立刻发心跳压制其他候选人。
- 随机超时 = 用随机性打破对称，避免票被瓜分；这是"以概率换确定性"的极简案例。

### 2.3 日志复制
- Leader 收客户端命令 → 追加到本地日志（带 term.index）→ AppendEntries 并行发给
  所有 follower；**多数派落盘 → commit → 应用到状态机 → 返回客户端**。
- 一致性检查：AppendEntries 携带 `prevLogTerm/prevLogIndex`，follower 不匹配则拒绝，
  leader 回退重试（log matching property 保证收敛）→ 这就是"日志修复"。
- 心跳即空 AppendEntries：兼做 leader 权威广播与 commit 推进。

### 2.4 为什么是多数派
两个多数派必相交 → 交集节点不会同时答应两个冲突决定；
相交节点上的 term 单调性把"决定不可推翻"传递到全集群。
**多数派 = 可用性（容忍少数故障）与安全性（防双主决断）的最小代价**（Quorum 数学：f+1 of 2f+1）。

## 3. 本讲实现要点（对接 pg2 与本项目 P2）

- RPC 处理必须**异步化**（Go 每连接一个 goroutine），否则死锁于
  "A 给 B 发 RPC 而 B 也在给 A 发"（Lab 2A 的经典坑）。
- 每个 RPC 处理函数**先检查 term 再动状态**；任何"我发现我该下台"的时刻
  都要立即停止当前工作返回（不可半途提交）。
- **状态变更与持久化解耦**：选举/复制逻辑先跑通（内存版），再插盘（pg3）。
- 测试哲学：用"每 10ms 随机重启一个节点"的 chaos 测试检验安全性不变量
  （对任意两副本，已提交前缀必须一致）——IronFleet（L22）把这种测试升级为证明。

## 4. 论文间脉络

- 收束 L01–L03 的伏笔：RPC 是通信语法；GFS 的"单 master + 操作日志 + lease"
  是手写共识，Raft 把它变成可复用的算法。
- 续篇 L06：安全性细则（投票限制为何够、成员变更为什么危险）与 Joint Consensus。
- 下游：L09 用 Raft 做 KV；L12 ZooKeeper/ZAB、L15 Spanner 的多 Raft/Paxos 组，
  都是本讲的规模化。

## 5. 跨课程联系

- **6.S081**：Raft 的持久化 = 文件系统 WAL（写-ahead log）思想——"先写日志再动手"，
  崩溃恢复 = 重放日志；pg3 与 xv6 日志文件系统机制同构。
- **15-445**：Raft commit index ↔ 数据库 WAL flush LSN；"多数派持久化"
  对应主从复制的 synchronous/semi-sync 级别；Raft 保证的是**复制**的顺序一致，
  事务隔离（MVCC/2PL）仍要在状态机里另做（见 P3 讨论）。
- **CS149/自顶向下**：term 是"逻辑时钟"，与 TCP 序列号防旧包、L07 Lamport 时钟同一谱系。

## 6. 开源项目中的应用

- **etcd**：Go + Raft 的事实标准（Kubernetes 的脑）；raft library 后独立为
  `hashicorp/raft`、`tikv/raft-rs`、`etcd-io/raft`。
- **TiKV / CockroachDB**：Multi-Raft（每个 region/range 一个 Raft 组）+
  Raft Learner + PreVote + Lease Read 等工程扩展。
- **Kafka（KRaft 模式）**：2024 年起用 Raft 取代 ZooKeeper 管理元数据。
- **RethinkDB / Neo4j causal cluster / MongoDB（复制协议非 Raft 但同族）**。

## 7. 延伸阅读

- Raft 可视化（raft.github.io / will.thesanem.com 的 In Search of an Understandable Consensus 动画）。
- Ongaro 博士论文 *Consensus: Bridging Theory and Practice*（2014）——安全性证明完整版。
- 本目录 `projects/p2_raft/`：单进程内 5 节点 + channel transport 的最小 Raft。
