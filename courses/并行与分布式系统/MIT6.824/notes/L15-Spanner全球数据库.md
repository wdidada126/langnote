# L15 Spanner：可扩展的全球数据库

> 阅读：Corbett et al., *Spanner: Google's Globally-Distributed Database*, OSDI 2012 / TOCS 2013
> 主线：把 L07 时间、L08 共识、L14 事务合成一个"地球规模的 ACID 数据库"。

## 1. 核心问题

- 目标：一个数据库同时满足——
  **跨大洲复制、外部一致性（external consistency = 真实时间序）、
  事务 + 丰富 SQL、读扩展、数千台机、99.999% 可用**——此前被认为不可能兼得。
- 关键赌注：**TrueTime**——用 GPS + 原子钟把全球时钟同步到
  "已知误差区间 `[t-ε, t+ε]`"。这是本讲的题眼（L07 谱系里的硬件派）。

## 2. 数据布局与复制

- 数据按行 key 有序 → 切成 **directory（对应其他系统的 tablet/region）**。
- 每个 directory 是一个 **Paxos 复制组**（默认 5 副本跨多数据中心）：
  一个 leader 处理读写，多数派持久化才返回 → directory 级细粒度共识（L08）。
- 分裂/合并/迁移实现自动负载均衡（对接 L13 Ark、L11 一致性哈希的分区思想）。
- Layers：paxos record log → 复制状态机（Multi-Paxos）→ 数据管理（目录/事务）→ GFS 存储。

## 3. TrueTime 与外部一致性提交

- API：`TT.now() -> [earliest, latest]`（一个区间）+ `TT.after(t)`（等到绝对晚于 t）。
- 读：只要"过去某时刻的值"——用时间戳版本（MVCC，L04/L14）读某个快照。
- **写提交 = 2PC + commit-wait**：
  事务提交时间戳 `s = TT.latest()`（区间上界）；
  提交前 **等待到 `TT.earliest() > s`**（即"全地球任何一台机器的时钟都已越过 s"）
  → 保证任何后续事务看到的 s 都在其"之前" → **外部一致性（真实时间序 = 序列化序）**。
- 这就是"用等待换因果/真实序"——ε 越大，提交延迟越高（时钟质量直接换成性能）。
- 对照：CockroachDB 用 HLC + 不确定性窗口（L07）达到类似性质而无须原子钟；
  代价是把模糊性暴露给上层重试。

## 4. 其他工程亮点

- **无 2PC 阻塞**：leader 崩溃 → 组内新 leader 从 Paxos 日志恢复决定
  （L08 + L14："共识解决原子提交的阻塞"，Spanner 是官方示范）。
- **读扩展**：follower 可服务"历史快照读"（不必回 leader）；
  leader 租约读（lease read）避免每次读一个 RTT（L06 linearizable read 同源）。
- **均匀延迟**：把事务分片按 key 分布到不同 directory → 网络可并行；
  热点用"把热行分到多 directory"（split by key range）。
- **Schema + 交错表**：把"通常一起访问"的数据物理邻近（减少跨 directory 事务）。

## 5. 论文间脉络

- 集大成：时间（L07）× 共识（L08/L05）× 事务（L14）× 存储分层（L03/L04/L13）。
- 对照 L11 Dynamo：Spanner 站 CP/强一致极，Dynamo 站 AP/最终一致极；
  两者是"一致性—可用性"光谱的两端锚点。
- 下游：L22 FaRM（内存 + RDMA 上重做 OCC）、NewSQL 全家（TiDB/CockroachDB/YugabyteDB）
  都是"Spanner 思想 + 开源可及硬件"的重构。

## 6. 跨课程联系

- **15-721（高级数据库）**：Spanner 是"分布式 MVCC + 2PC + 外部一致性"的标准案例；
  commit-wait 与 HLC 的取舍、TrueTime 的误差模型是常见考题。
- **体系结构/DDCA**：原子钟/GPS 授时、跨洋 RTT（光速下界 ~ms/千公里）
  决定 ε 与等待 → 物理定律第一次成为数据库设计参数。
- **自顶向下网络**：跨 DC 复制的带宽/延迟预算直接决定 ε 与吞吐。
- **6.S081**：MVCC 版本 + 快照读与内核的 copy-on-write/RCU 读侧无锁同构。

## 7. 开源项目中的应用

- **CockroachDB / TiDB / YugabyteDB / Google Cloud Spanner（托管版）**：
  Spanner 论文是其共同的"原始蓝图"。
- **TiKV**：Multi-Raft（Raft 替 Paxos，L05）+ PD 中心化 TSO（放弃 TrueTime 用单点授时换简单）。
- **PostgreSQL 生态 Citus / Greenplum**：分片 + 2PC，但没有共识/外部一致性——
  对照读能理解 Spanner 难在哪。
- **AWS Aurora / DSQL**：把存储层共识化 + 无协调器事务，走另一条"Spanner 目标、
  不同架构"的路。

## 8. 延伸阅读

- *Spanner: Becoming a SQL System* (SIGMOD 2017)——加入复杂 SQL 的后续。
- *HighAvailability Web-Scale Transactions: The Extended Details*（Michael Baron）——
  commit-wait/2PC 细节最好的第三方讲解。
- 对照精读 CockroachDB "Live and Consistent"（HLC 路线 vs TrueTime 路线）。
- Malicevic & Zeller, *Using Logical Physical Clocks for Consistent Snapshots*（把 HLC 与分布式快照缝合，L07/L15 交叉）。
