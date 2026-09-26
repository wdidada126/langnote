# 第 9 章　CockroachDB 深度探索

> 原书第 9 章是典型案例篇的第三例：**CockroachDB**——Spanner 的「开源精神继承者」。
> 它**没有 TrueTime 硬件**，改用 **HLC（混合逻辑时钟）+ Raft** 实现「类 Spanner」的强一致与分布式事务。
> 9.1 架构；9.2 事务处理模型；9.3 分布式一致性实现原理。
> 这一章是第 3 章（HLC/Raft）与第 7 章（Spanner）的「开源落地版」。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 9.1 CockroachDB 的架构 | 分层（SQL/KV/存储）、Range 分片、每个 Range 一个 Raft 组（Multi-Raft） | 用 Raft 复制 + Range 自动分裂/再均衡做到去中心化水平扩展 |
| 9.2 CockroachDB 事务处理模型 | HLC 时间戳、串行化快照隔离 SSI、2PC（分布式提交） | 用 HLC 近似 TrueTime 的外部一致性，SSI 拿可串行化 |
| 9.3 分布式一致性实现原理 | HLC 生成、读时间戳、冲突与读重启 | 无中心时钟下，靠 HLC + 因果序 + 读重启保证正确 |

## 核心精讲

（以下为教学性梳理，伪代码/示意均**教学示意，不参与构建**。）

### 9.1 架构：Range + Multi-Raft

- **数据分片为 Range**（连续 key 区间），每个 Range 默认 3 副本，组成**一个 Raft 组**；多个 Range 各自独立 Raft 组 = **Multi-Raft**。
- Range 自动分裂（过大）与再均衡（负载不均），实现 5.5 的「弹性可扩展」。

```text
# 教学示意，不参与构建：CockroachDB 分层 + Multi-Raft
SQL 层 (无状态, 可水平扩)
  -> KV 层 (路由到对应 Range)
      -> 每个 Range: Raft 组(3 副本) -> 一个 Leader 服务读写
# 不同 Range 的 Leader 可在不同节点 -> 负载自然分散
```

### 9.2 事务模型：HLC + SSI

- **时间戳用 HLC**：每个事务取 `timestamp = HLC.now()`，既接近真实时间又能排因果（见 [03-一致性问题的解法.md](03-一致性问题的解法.md) 3.4）。
- **SSI（可串行化快照隔离）**：在 MVCC 基础上检测「危险结构」（读写冲突环）以拦截写倾斜，拿到真正可串行化，而免 2PL 的锁开销。

```text
# 教学示意，不参与构建：读重启 (read refresh / restart)
T1 (ts=100) 读 x
T2 (ts=110) 写 x 并提交
T1 再读 x 时发现 x 已在其快照后被改 -> 重启 T1 (取新 ts) 重跑
# 用 "读写冲突则重启" 代替锁, 保证可串行化
```

### 9.3 一致性实现原理

- **无中心时钟**：不依赖 TSO 也不依赖 TrueTime；HLC 在时间戳里编码「物理时间 + 逻辑计数」，跨节点只需偶尔同步物理时间（NTP 级即可）。
- **读重启保证正确**：当读遇到「晚于本事务快照的写」时，重启该事务取更大时间戳，避免读到不一致的中间态。

## 版本演进

- **本书无第二版**；本节写 2021 年口径 → 2026 年视角的变化。
- **CockroachDB 持续演进**：22.x/23.x 强化多地域、向量化执行、与 PostgreSQL 协议兼容度；具体版本功能集本目录未逐条核实。
- 🔧 **HLC 路线的代表地位巩固**：CockroachDB/YugabyteDB 用 HLC 证明「无 TrueTime 硬件也能做类 Spanner」；与 TSO（OB/TiDB-PD）形成 2026 年两大路线（见 [08-Percolator事务处理模型.md](08-Percolator事务处理模型.md)）。
- 🔧 **Raft 已是事实标准（本书 3.6 已体现）**：CockroachDB 的 Multi-Raft 是 Raft 在数据库的工程样板。
- 🔧 **SSI 默认强隔离**：CockroachDB 默认 SSI，印证 [04-分布式事务原理.md](04-分布式事务原理.md) 4.7 的演进方向。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Corbett et al.《Spanner》 | OSDI 2012 | CockroachDB 的范式来源（→ 第 7 章） |
| Kulkarni et al.《Logical Physical Clocks and Consistent Snapshots in Globally Distributed Databases》（HLC） | 2014（版本较多，本目录只标年份） | CockroachDB 时间戳基础（→ 9.2/9.3） |
| Ongaro, Ousterhout《In Search of an Understandable Consensus Algorithm》（Raft） | USENIX ATC 2014 | Range 的 Raft 复制（→ 9.1） |
| Cahill et al.《Serializable Isolation for Snapshot Isolation》（SSI） | SIGMOD 2008 | CockroachDB 默认隔离级别（→ 9.2） |
| CockroachDB 官方论文 / 文档（社区版开源） | 2010s–2020s | 架构与事务的工程细节（版本较多，本目录未逐条核实） |

## 近年研究与工业界开源实践（2015–2026）

- **star 数（2026-09，`gh api` 实测）**：CockroachDB 自身及其对照系统：

| 项目 | 定位 | star |
| --- | --- | --- |
| `cockroachdb/cockroach` | Spanner 开源精神继承者：Raft + HLC + SSI | 32509 |
| `pingcap/tidb` | 对照：走 TSO + Percolator 而非 HLC | 40591 |
| `oceanbase/oceanbase` | 对照：走 Paxos + TSO | 10291 |

- 🔧 **YugabyteDB** 同为 HLC + Raft 的 Spanner 系开源（具体 star 本书未实测，未杜撰）。
- 🔧 **HLC vs TSO 之争持续**：CockroachDB（HLC，无中心）vs TiDB/OB（TSO，中心授时）；2026 年两者都大规模生产，无绝对胜负。
- CockroachDB 社区版开源（BSL 许可，近年许可政策有调整，具体条款本目录未逐条核实），因此 GitHub 可见其源码仓库。

## 常见误区与本书需修正之处

| 误区 | 事实 | 书目 |
| --- | --- | --- |
| 「CockroachDB 是 Spanner 的复刻」 | 思想继承（Paxos/Raft+2PC+外部一致），但用 HLC 替代 TrueTime，无硬件依赖 | 9.1/9.3 |
| 「HLC 就是物理时间」 | HLC = 物理时间 + 逻辑计数，仍可判因果，且不需 GPS/原子钟 | 9.3 |
| 「SSI 需要加锁」 | CockroachDB 用 SSI 在 MVCC 上靠冲突检测拿可串行化，免 2PL 锁 | 9.2 |
| 🔧 本书未把 CockroachDB(HLC) 与 TiDB(TSO) 并列为两大路线 | 2026 年这是选型核心对照，需补 | 9.2/9.3（🔧 见第8章） |
| 🔧 本书未强调 Multi-Raft 是水平扩展关键 | 每 Range 一 Raft 组是 CockroachDB 扩展性的底座，需补 | 9.1（🔧 见第3章） |
| 🔧 本书未提 CockroachDB 许可变化 | 其开源许可（BSL）近年有调整，引用时应注意「开源」的具体含义 | 9.1（🔧 注） |

## 与其他章 / 其他书的联系

- **本书内**：
  - 9.1 Multi-Raft → [03-一致性问题的解法.md](03-一致性问题的解法.md) 3.6（Raft）；
  - 9.2/9.3 HLC → [03-一致性问题的解法.md](03-一致性问题的解法.md) 3.4；
  - 9.2 SSI → [04-分布式事务原理.md](04-分布式事务原理.md) 4.7；
  - 9.x 整体 → [07-Spanner深度探索.md](07-Spanner深度探索.md)（被继承的范式）、[08-Percolator事务处理模型.md](08-Percolator事务处理模型.md)（对照的 TSO 路线）。
- [../深入理解分布式共识算法/00-总览与阅读地图.md](../深入理解分布式共识算法/00-总览与阅读地图.md)——Raft 深度推导，补 9.1。
- [../设计数据密集型应用/09-一致性与共识.md](../设计数据密集型应用/09-一致性与共识.md)——线性一致与 HLC 的关系，补 9.3。
- [../数据库系统概念6/15-并发控制.md](../数据库系统概念6/15-并发控制.md)——SSI 与隔离级别的教科书底座。
