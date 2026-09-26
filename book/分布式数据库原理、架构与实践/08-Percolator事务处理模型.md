# 第 8 章　Percolator 事务处理模型

> 原书第 8 章是典型案例篇的第二例：**Percolator**——Google 的「去中心化分布式事务」模型。
> 它没有 TrueTime 硬件，而是用 **Bigtable + 两列时间戳（lock/write）+ 中心化授时（TSO）**
> 实现跨行、跨表的 ACID 事务。8.1 架构；8.2 事务处理。
> 这个模型是 **TiDB 事务的直接原型**，工业影响极大。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 8.1 Percolator 的架构 | 基于 Bigtable、加 lock 列/write 列、中心 TSO 授时 | 不依赖专用硬件，用「多版本 + 锁 + 中心时间戳」做事务 |
| 8.2 Percolator 的事务处理 | 读写事务（2PC + 行级锁）、快照读、清理机制 | 乐观模型：提交期才冲突检测，靠锁保证原子性 |

## 核心精讲

（以下为教学性梳理，伪代码/示意均**教学示意，不参与构建**。）

### 8.1 架构：三列模型

- 在 Bigtable 的 key-value 上为每个数据单元加三列：**data**（值）、**lock**（事务锁）、**write**（指向某版本 data 的提交指针）。
- **中心化授时 TSO**：全局单调递增时间戳由单一服务分配（Percolator 原始设计如此；TiDB 用 PD 做 TSO）。

### 8.2 事务处理：乐观 2PC

- **快照读**：读时用 TSO 给的 `start_ts`，读 `write` 列中 `version <= start_ts` 的最大版本对应 data。
- **写事务（乐观）**：
  1. 预写（buffer）：改 data 列（新版本 `start_ts`），并在**首个写入行（primary）**加 lock；
  2. 提交：取 `commit_ts`，先提交 primary（写 write 列 + 清 lock），再提交其余（secondary）；
  3. 冲突检测：若某行已有他人 lock → 冲突，回滚。

```text
# 教学示意，不参与构建：Percolator 写事务
start_ts = TSO()
写: data[new_start_ts] = v; lock[primary] = 标记
提交: commit_ts = TSO()
  primary: write = (commit_ts -> new_start_ts); 删 lock[primary]
  secondary(各): write = (commit_ts -> new_start_ts); 删 lock
# 若 primary 提交成功 -> 事务整体可见 (secondary 失败可由他人/后台清理)
```

- **清理机制**：若客户端崩溃留下孤儿 lock，后续事务据 `write` 列判断该事务是否已提交，代为清理（滚前/补后）。

> Percolator 的关键优势：**无 TrueTime 硬件**、**去中心化数据节点**（只 TSO 是中心），且天然 MVCC 快照读。代价：中心 TSO 可能成瓶颈、secondary 提交需逐个写。

## 版本演进

- **本书无第二版**；本节写 2021 年口径 → 2026 年视角的变化。
- **Percolator 是 TiDB 事务的直接原型**：TiDB/TiKV 的 Percolator 行格式 + PD 授时，几乎照此实现。本书 8 章的工程价值在 2026 年极高。
- 🔧 **TSO 单点优化**：TiDB 用 PD 集群 + 批量授时（预分配时间窗口）缓解 TSO 瓶颈；2026 年「TSO 能否去中心化」仍有 HLC 路线之争（见 [09-CockroachDB深度探索.md](09-CockroachDB深度探索.md)）。
- 🔧 **Percolator 的悲观扩展**：TiDB 后来加悲观事务（pessimistic）降低冲突重试，弥补原始乐观模型高冲突痛点（本书 2021 述乐观为主，需补悲观演进）。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Peng, Dabek《Large-scale Incremental Processing Using Distributed Transactions and Notifications》（Percolator） | **OSDI 2010** | 本章原始论文：去中心化分布式事务模型 |
| Chang et al.《Bigtable: A Distributed Storage System for Structured Data》 | OSDI 2006 | Percolator 的存储底座 |
| Corbett et al.《Spanner》 | OSDI 2012 | 对照：用 TrueTime 而非 TSO（→ 第 7 章） |
| Huang et al.《TiDB: A Raft-based HTAP Database》（及 TiKV 论文） | VLDB 2020 | Percolator 模型的工业落地（→ TiDB/TiKV） |

## 近年研究与工业界开源实践（2015–2026）

- **star 数（2026-09，`gh api` 实测）**：Percolator 最直接的开源继承者：

| 项目 | 定位 | star |
| --- | --- | --- |
| `pingcap/tidb` | NewSQL，事务模型 = Percolator + TSO | 40591 |
| `tikv/tikv` | TiDB 的存储层，Percolator 行格式 + Multi-Raft | 16878 |
| `cockroachdb/cockroach` | 走 HLC 而非 Percolator（对照路线） | 32509 |

- 🔧 **TiDB 悲观事务（2019–）**：补原始乐观模型的高冲突短板，是 Percolator 在 2026 年的主流形态。
- 🔧 **TSO 的规模化**：PD 预分配时间窗口、多 TSO 分片，是 2026 年缓解单点的工程手段（本书未专述）。
- 原始 Percolator 代码未作为独立开源仓库发布（Google 内部系统），故无对应 GitHub star 数；本目录不杜撰该数字。

## 常见误区与本书需修正之处

| 误区 | 事实 | 书目 |
| --- | --- | --- |
| 「Percolator 需要 TrueTime」 | 不需要；用中心 TSO + MVCC 实现，无专用硬件 | 8.1 |
| 「Percolator 是悲观锁」 | 原始模型是乐观（提交期才检测冲突），高冲突会重试 | 8.2 |
| 「Percolator 没用 2PC」 | 它本质是两阶段（预写锁 + 提交 primary/secondary） | 8.2 |
| 🔧 本书未提 TiDB 是 Percolator 的直接落地 | 2026 年 TiDB/TiKV 是最广为人知的 Percolator 实现，需补 | 8.1/8.2（🔧 补） |
| 🔧 本书未讲 TiDB 悲观事务演进 | 2019 后 TiDB 加悲观模式，是工业现实，需补 | 8.2（🔧 补） |
| 🔧 本书未对比 TSO(Percolator) vs HLC(CockroachDB) | 这是 2026 年两条主流去中心化事务路线，需补 | 8.2（🔧 见第9章） |

## 与其他章 / 其他书的联系

- **本书内**：
  - 8.1 TSO → [03-一致性问题的解法.md](03-一致性问题的解法.md)（TSO 是无中心 HLC 的对照路线，🔧）；
  - 8.2 MVCC → [04-分布式事务原理.md](04-分布式事务原理.md) 4.4；
  - 8.2 2PC 思想 → [04-分布式事务原理.md](04-分布式事务原理.md) 4.6；
  - 8.x 整体 → [07-Spanner深度探索.md](07-Spanner深度探索.md)（TrueTime 对照）、[09-CockroachDB深度探索.md](09-CockroachDB深度探索.md)（HLC 对照）。
- [../分布式数据库入门进阶与实战/06-事务基础与分布式事务.md](../分布式数据库入门进阶与实战/06-事务基础与分布式事务.md)——Percolator 的现代中文讲法。
- [../数据库系统概念6/26-高级事务处理.md](../数据库系统概念6/26-高级事务处理.md)——分布式事务教科书底座。
- [../设计数据密集型应用/07-事务.md](../设计数据密集型应用/07-事务.md)——快照隔离与 MVCC 的延伸。
