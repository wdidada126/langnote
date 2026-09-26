# 第 7 章　Spanner 深度探索

> 原书第 7 章是典型案例篇的首章，也是**分量最重**的一章：Spanner 是「从零设计分布式数据库」的范式。
> 7.1 从 Spanner 的两篇重点论文（OSDI 2012 + SIGMOD 2012 配套 TrueTime 论文）说起；
> 7.2 架构；7.3 事务处理模型（TrueTime + 外部一致性）；7.4 Spanner 与 CAP。
> 这一章把前六章的「原理」全部在 Spanner 上落地了一次。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 7.1 从 Spanner 的两篇重点论文说起 | OSDI 2012 主论文 + SIGMOD 2012 TrueTime 论文 | Spanner = 架构论文 + 时钟论文「双拼」 |
| 7.2 Spanner 的架构 | universe/zone/spanserver、tablet、directory、Paxos 组 | 数据按 directory 分片，每片一个 Paxos 组跨 zone 复制 |
| 7.3 Spanner 的事务处理模型 | TrueTime、commit wait、2PL + MVCC、外部一致性 | 用硬件时钟换「全球一致的外部一致性」 |
| 7.4 Spanner 与 CAP | Spanner 在分区时选 CP，但通常同时高可用 | 实践中用 TrueTime 把「一致性代价」压到可用范围内 |

## 核心精讲

（以下为教学性梳理，伪代码/示意均**教学示意，不参与构建**。）

### 7.2 架构

- **层级**：universe（全球部署）→ zone（数据中心单元）→ spanserver（服务 100~1000 个 tablet）→ tablet（key→值的多版本映射）→ directory（一组连续 key，复制与放置的基本单位）。
- **每个 directory 一个 Paxos 组**：组跨 zone 复制，组内强一致；跨 directory 事务用 2PC。

```text
# 教学示意，不参与构建：Spanner 层级
universe
└── zone (数据中心)
    ├── zonemaster: 分配 tablet 给 spanserver
    ├── location proxy: 帮客户端定位 tablet
    └── spanserver: 服务 tablet, 每个 directory 一个 Paxos 组
```

### 7.3 事务模型：TrueTime 换外部一致性

- **TrueTime**：每个数据中心配 GPS + 原子钟（两种失效模式不同的时钟），`TT.now()` 返回区间 `[earliest, latest]`，真实时间落在区间内，半宽 ε≈几毫秒。
- **commit wait**：事务提交时间戳 `s` 必须等到 `TT.now().earliest > s` 才可见 → 保证「之后发生的读一定看到这次提交」。
- **外部一致性**：按真实时间顺序发生的提交，其可见顺序与之严格一致（比可串行化更强）。

```text
# 教学示意，不参与构建：commit wait
1. T1 提交, 取 s = TT.now().latest
2. 等待直到 TT.now().earliest > s   (约等 ε, 几毫秒)
3. 此后任意 T2 时间戳必 > s -> T2 必见 T1 写入 -> 外部一致性
```

- **并发控制**：读写事务用 2PL + wound-wait 死锁预防；只读事务无锁快照读（MVCC + 时间戳由 TrueTime 保证不读未完成事务）。

### 7.4 Spanner 与 CAP

- 网络分区时 Spanner 选 **CP**（牺牲部分可用、保证一致）；但因 TrueTime 让提交延迟仅多 ε，平时可用性极高，所以「实际体验接近 CA」。

## 版本演进

- **本书无第二版**；本节写 2021 年口径 → 2026 年视角的变化。
- **Spanner 成为范式输出者**：催生 CockroachDB（9 章）、YugabyteDB、TiDB（部分思想）、OceanBase。本书判断贯穿第 7–9 章。
- 🔧 **TrueTime 不可替代 → 通用系统走 TSO/HLC**：TSO（OB 的 GTS、TiDB 的 PD）或 HLC（CockroachDB），见 [03-一致性问题的解法.md](03-一致性问题的解法.md) 3.4 与 [09-CockroachDB深度探索.md](09-CockroachDB深度探索.md)。
- 🔧 **Google Cloud Spanner 持续演进**：增加 PostgreSQL 接口等（具体功能集本目录未逐条核实），对外仍是托管服务。
- 🔧 **国产数据库继承 Spanner 思想**：OceanBase（Paxos+2PC+单机分布式一体化）、TiDB（分片复制 + Percolator 事务），见 [09-CockroachDB深度探索.md](09-CockroachDB深度探索.md) 与 [08-Percolator事务处理模型.md](08-Percolator事务处理模型.md)。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Corbett et al.《Spanner: Google's Globally-Distributed Database》 | **OSDI 2012** | 本章 7.2/7.3 主论文：架构、Paxos 组、外部一致性 |
| Baker et al.《Megastore: Providing Scalable, Highly Available Storage for Interactive Services》 | CIDR 2011 | Spanner 前身（半关系层），见 [../大规模分布式存储系统/06-分布式表格系统.md](../大规模分布式存储系统/06-分布式表格系统.md) |
| Shute et al.《F1: A Distributed SQL Database That Scales》 | VLDB 2013 | 建在 Spanner 之上的 OLTP 系统，验证其用法 |
| Lamport《The Part-Time Parliament》（Paxos） | ACM TOCS 1998 | 复制层 Paxos（→ 7.2） |
| Gray, Lamport《Consensus on Transaction Commit》 | ACM TODS 2006 | Paxos + 2PC（→ 7.3） |

## 近年研究与工业界开源实践（2015–2026）

- **star 数（2026-09，`gh api` 实测）**：Spanner 本身不开源，但其精神继承者：

| 项目 | 定位 | star |
| --- | --- | --- |
| `cockroachdb/cockroach` | Spanner 开源精神继承者：Raft + HLC（无 TrueTime 硬件） | 32509 |
| `pingcap/tidb` | NewSQL：Multi-Raft + Percolator 事务 + TSO | 40591 |
| `oceanbase/oceanbase` | 国产原生分布式，Paxos + 2PC + TSO | 10291 |

- 🔧 **Spanner 范式三条落地分支**（见 [09-CockroachDB深度探索.md](09-CockroachDB深度探索.md)）：TSO+Raft（OB/TiDB）、HLC+Raft（CockroachDB）、共享存储一写多读（PolarDB/Aurora）。
- 🔧 **TrueTime 的两条无硬件替代**（HLC 2014、TSO）：CockroachDB 用 HLC 做到「无中心时钟的外部一致性近似」，是 2026 年通用系统的现实路径。

## 常见误区与本书需修正之处

| 误区 | 事实 | 书目 |
| --- | --- | --- |
| 「Spanner 是 CA 系统」 | 分区时仍选 CP；只是 TrueTime 把一致代价压低，体验接近 CA | 7.4 |
| 「外部一致性 = 可串行化」 | 外部一致性要求提交顺序符合真实时间，比可串行化更强 | 7.3 |
| 「TrueTime 可直接照搬」 | 依赖 GPS+原子钟硬件，通用系统只能走 TSO/HLC | 7.3 |
| 「commit wait 无所谓」 | 它把延迟抬高约 ε（毫秒级），是「延迟换一致」的显式代价 | 7.3 |
| 🔧 本书未强调「TrueTime 不可复制 → 通用走 TSO/HLC」 | 2026 年这是选型第一课，需补 | 7.3（🔧 补，见第3/9章） |
| 🔧 本书未把 Spanner 与国产数据库（OB/TiDB）对照 | 2026 年国产第一梯队继承 Spanner 思想，需补 | 7.2/7.3（🔧 补） |

## 与其他章 / 其他书的联系

- **本书内**：
  - 7.2 Paxos 组 → [03-一致性问题的解法.md](03-一致性问题的解法.md) 3.5；
  - 7.3 外部一致性 → [02-深入研究一致性.md](02-深入研究一致性.md) 2.3.1（线性一致 + 真实时间）；
  - 7.3 2PC → [04-分布式事务原理.md](04-分布式事务原理.md) 4.6；
  - 7.3 MVCC 快照读 → [04-分布式事务原理.md](04-分布式事务原理.md) 4.4；
  - 7.x 整体 → [08-Percolator事务处理模型.md](08-Percolator事务处理模型.md)（另一类去中心化事务）、[09-CockroachDB深度探索.md](09-CockroachDB深度探索.md)（Spanner 开源版）。
- [../大规模分布式存储系统/06-分布式表格系统.md](../大规模分布式存储系统/06-分布式表格系统.md)——Megastore 是 Spanner 前身。
- [../设计数据密集型应用/09-一致性与共识.md](../设计数据密集型应用/09-一致性与共识.md)——线性一致与共识，理解外部一致性的前置。
- [../深入理解分布式共识算法/04-Paxos.md](../深入理解分布式共识算法/04-Paxos.md)——7.2 Paxos 组的深度推导。
