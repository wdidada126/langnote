# 第 9–10 章 MySQL XA 与 TCC（分布式事务的两种两阶段）

> 覆盖原书：第 9 章「MySQL XA」（9.1 什么是XA规范 / 9.2 如何通过MySQL XA实现分布式事务 / 9.3 小结）
> + 第 10 章「TCC」（10.1 什么是TCC / 10.2 如何通过TCC实现指令执行的原子性 / 10.3 小结）。
> 两章合并的理由：它们都是「把原子性做到跨资源」，只是一个在**数据库层**、一个在**业务层**。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 9.1 什么是 XA 规范 | X/Open DTP 模型：AP / TM / RM | XA 是**接口规范**不是协议实现；它把 2PC 标准化为 `xa_start/end/prepare/commit/rollback` |
| 9.2 MySQL XA 实现 | 外部 XA vs 内部 XA | MySQL 的 XA 参与方是**数据库实例**；真正的难点在 **binlog 与 redo 的两阶段一致性** |
| 10.1 什么是 TCC | Try / Confirm / Cancel | 把两阶段搬到业务层：Try 预留资源，Confirm/Cancel 二选一 |
| 10.2 TCC 的原子性 | 幂等 / 空回滚 / 防悬挂 三大坑 | TCC 的「原子性」靠**业务代码正确性**保证，框架只给编排 |
| 两章小结 | 何时用哪个 | 短事务、数据库内 → XA；跨服务、长事务、非数据库资源 → TCC/SAGA |

## 核心精讲

### 9.1 X/Open DTP 模型与 XA 接口

```
教学示意，不参与构建
// 三个角色
AP (Application Program)  : 业务程序，定义事务边界
TM (Transaction Manager)  : 事务管理器，负责全局事务 ID 与二阶段驱动
RM (Resource Manager)     : 资源管理器（数据库、MQ），负责本地分支事务
// XA 接口（TM 调用 RM）
xa_start(xid)             : 开启分支事务
xa_end(xid)               : 结束分支的 SQL 执行
xa_prepare(xid)           : 第一阶段：写 prepare 日志、锁住资源、返回「能否提交」
xa_commit(xid) / xa_rollback(xid) : 第二阶段
xa_recover()              : 崩溃重启后枚举处于 prepared 状态的分支
```

**XA 的关键承诺**：`xa_prepare` 成功后，RM 必须保证「**之后无论发生什么，都能按 TM 的指令提交或回滚**」——
这要求 prepare 时把 undo/redo 都**落盘**，并持有锁。

### 9.2 MySQL XA：外部与内部

```
教学示意，不参与构建
-- 外部 XA：MySQL 作为 RM，由外部 TM（应用/框架）驱动
XA START 'gtrid','bqual';     -- xid = gtrid + bqual + formatID
UPDATE account SET balance = balance - 100 WHERE id = 1;
XA END 'gtrid','bqual';
XA PREPARE 'gtrid','bqual';   -- 写 prepare 记录，崩溃后可恢复
XA COMMIT 'gtrid','bqual';    -- 或 XA ROLLBACK ...
-- 崩溃恢复
XA RECOVER;                   -- 列出所有 prepared 分支，由 TM 决定去向
```

**内部 XA**：MySQL 内部的 **binlog（server 层）与 redo（InnoDB 层）**之间也需要两阶段，
否则崩溃后会出现「redo 提交了但 binlog 没有」——主从不一致。
MySQL 5.6 曾存在「prepared 事务未写入 binlog 即崩溃导致数据丢失」的问题，
后续版本把 binlog 的 flush 纳入了 prepare 阶段。

**XA 的三个硬伤**（2026 年仍然成立）：

1. **阻塞**：TM 在 prepare 之后宕机，所有 RM 的锁一直持有，无人能推进；
2. **性能**：两阶段需要 **2 次落盘 + 2 次网络往返**，且锁持有时间跨整个事务；
3. **协调者单点**：TM 必须自己把「决定」持久化，否则恢复后不知道该提交还是回滚。

### 10.1 TCC：把两阶段搬到业务层

```
教学示意，不参与构建
// Try：预留资源（不是真正执行，是「冻结」）
func try(orderID, amount):
    freezeBalance(amount)          // 余额 -> 冻结金额
    createOrder(orderID, state=TRYING)
// Confirm：确认执行（Try 成功且全局决定提交）
func confirm(orderID, amount):
    deductFromFrozen(amount)       // 冻结 -> 实际扣减
    setOrderState(orderID, CONFIRMED)
// Cancel：补偿（Try 成功但全局决定回滚）
func cancel(orderID, amount):
    unfreezeBalance(amount)
    setOrderState(orderID, CANCELED)
// 幂等：Confirm/Cancel 都可能被重试 -> 必须先查状态再执行
// 空回滚：Try 没执行（网络丢包），Cancel 却先到了 -> 不能报错，要「记一笔空回滚」
// 防悬挂：Cancel 先到、Try 后到 -> Try 必须拒绝执行（否则资源永久冻结）
```

> 本书 10.1 用「如何实现指令执行的原子性」表述，强调的是**指令（业务动作）**而非数据库行——
> 这正是 TCC 与 XA 的分野。

### 三大坑的形式化

| 坑 | 触发场景 | 正确做法 |
| --- | --- | --- |
| **幂等** | Confirm/Cancel 网络超时被重试 | 用**全局事务 ID + 分支事务 ID** 做去重表；先查状态再执行 |
| **空回滚** | Try 请求丢失，TM 超时后直接发 Cancel | Cancel 时若无 Try 记录，**插入一条回滚记录**并返回成功 |
| **防悬挂** | Cancel 先到（空回滚），Try 请求随后到达 | Try 时发现已有回滚记录，**直接返回失败**不再预留 |

### 什么时候用哪个

| 维度 | XA / 2PC | TCC | SAGA |
| --- | --- | --- | --- |
| 资源类型 | 数据库（支持 XA 的 RM） | 任意（含非数据库） | 任意 |
| 隔离性 | 强（锁持有到提交） | 弱（Try 阶段只是预留，业务可见中间态） | 最弱（无预留，靠补偿） |
| 业务侵入 | 低（框架驱动） | **高**（每个业务写三段代码） | 中（写补偿动作） |
| 适用时长 | 短事务（毫秒~百毫秒） | 中（秒级） | 长事务（分钟以上） |
| 典型实现 | MySQL XA、JTA/Atomikos | Seata TCC、Hmily | Seata Saga、Camunda |

## 版本演进

- **1978**：Gray 在《Notes on Database Operating Systems》系统化 2PC 与 WAL，是所有原子提交的源头。
- **1991 前后**：X/Open 发布 **XA 规范**，把 2PC 接口标准化（`xa_*`），本书第 9 章的正式出处。
- **2000s**：JTA/JTS 与 Atomikos、Bitronix 让 XA 进入 J2EE 主流；MySQL 自 5.0 起支持 XA。
- **2007**：Pat Helland《Life beyond Distributed Transactions》指出**跨服务分布式事务不可扩展**，
  提出「实体 + 消息 + 幂等」的模型，是 TCC 与 SAGA 的思想源头（本书第 10 章的正式出处）。
- **2010s**：**Percolator（Google, OSDI 2010）**给出「客户端协调的 2PC + 快照隔离」，
  TiDB 直接实现它；Seata（阿里，2019）提供 AT/TCC/Saga 三种模式。
- **2022（本书）**：第 9、10 章定位是「两种落地姿势」，对 XA 的 MySQL 实现与 TCC 的三段代码都给了实操细节。
- **2026 视角**：
  - **XA 在新系统里已明显退潮**：微服务化后跨库 XA 的锁持有时间不可接受；
    主流做法是 **「本地事务 + 可靠消息（事务消息/Outbox）+ 幂等消费」**这一最终一致方案；
  - **TCC 仍活跃**但主要靠框架（Seata `apache/incubator-seata`，**26012★**）提供幂等/空回滚/防悬挂的样板；
  - **Spanner/TiDB/CockroachDB**证明了「分布式数据库内部可以用 2PC + TrueTime/HLC 做到外部一致的可串行化」——
    这是与 XA 完全不同的路线（**数据库内部**的 2PC，不跨异构系统）。

## 经典论文与原始文献

| 论文/规范 | 出处 | 贡献 |
| --- | --- | --- |
| Gray《Notes on Database Operating Systems》 | 1978（Operating Systems: An Advanced Course） | 2PC 与 WAL 的系统化 |
| X/Open《Distributed Transaction Processing: The XA Specification》 | X/Open 1991 | XA 接口规范，本书第 9 章的源头 |
| Helland《Life beyond Distributed Transactions: an Apostate's Opinion》 | CIDR 2007 | TCC / SAGA 的思想源头 |
| Peng & Dabek《Large-scale Incremental Processing Using Distributed Transactions and Notifications》（Percolator） | USENIX OSDI 2010 | 客户端协调的 2PC + SI，TiDB 的实现依据 |
| Corbett et al.《Spanner: Google's Globally-Distributed Database》 | USENIX OSDI 2012 | TrueTime + 2PC 实现**外部一致**的分布式事务 |
| Thomson et al.《Calvin: Fast Distributed Transactions for Partitioned Database Systems》 | ACM SIGMOD 2012 | 确定性事务：先定序再执行，绕开 2PC 的不确定性 |
| Lampson & Sturgis《Crash Recovery in a Distributed Data Storage System》 | 1976（技术报告） | 原子提交的早期形式化 |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **确定性数据库**（Calvin SIGMOD 2012；Bohm、Aria VLDB 2020）用「先定序、后执行」消除 2PC 的协调开销，是近年研究热点；
  - **Sundial（CIDR 2021 / VLDB 2022）**用**逻辑租约**降低 OCC 重启率，是「租约」思想进入事务层的代表；
  - **HLC（混合逻辑时钟）**在 CockroachDB 落地，配合写意图实现**无特殊硬件**的串行化快照——
    这是 Spanner TrueTime 路线的「平民化」版本。
- **工业界开源**（star 数 2026-09 `gh api` 实测）：
  - `apache/incubator-seata`（**26012★**）：AT / TCC / Saga / XA 四种模式，本书第 10 章 TCC 的工业化形态。
  - `pingcap/tidb`（**40590★**）：Percolator 模型（乐观 + 悲观）；5.0 起默认**悲观事务 + 分布式死锁检测**；TiDB 7.x 起提供一阶段提交（1PC）优化。
  - `cockroachdb/cockroach`（**32508★**）：**HLC + 串行化快照**，是「不用 TrueTime 也能可串行化」的样本。
  - `apache/rocketmq`（**22621★**）：**事务消息**（半消息 + 回查），是「本地事务 + 可靠消息」这一替代路线的代表实现。
  - `redis/redis`（**76485★**）：Redis 事务是**弱原子**的（MULTI/EXEC 无回滚语义），常被误当作分布式事务组件，值得对照。
- **Jepsen 实测**（`jepsen-io/jepsen`，**7504★**）：TiDB 与 CockroachDB 均有专项报告，
  讨论集中在**时钟与隔离级别**（如 TiDB 早期 SI 的写偏斜问题、CockroachDB 时钟偏移上限）——
  这类实测结论是 2026 年评估分布式事务的唯一可靠依据。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「XA 能保证隔离性」 | XA 只保证**原子提交**；隔离性由各 RM 自己的锁/MVCC 决定，且跨 RM 的全局隔离通常做不到 |
| 2 | 「TCC 的 Confirm 一定成功」 | 不一定。Confirm 也可能失败，需要**重试 + 幂等**；长时间失败需人工介入 |
| 3 | 「有了 TCC 框架就不用管幂等」 | 框架只做编排；**幂等、空回滚、防悬挂**必须由业务代码落实 |
| 4 | 「分布式事务首选 XA」 | 2026 年跨服务场景首选「**本地事务 + 可靠消息 + 幂等**」；XA 只适合同构、短事务、锁代价可接受的场景 |
| 5 | 🔧 2026 补丁：本书未讲「协调者必须持久化决定」 | 第 9 章讲 XA 恢复时未强调：TM 在发出 commit 之前必须**先把全局决定落盘**，否则崩溃后无法判断该提交还是回滚。这是 2PC 唯一的「不可自动恢复点」 |
| 6 | 🔧 2026 补丁：未区分「跨异构系统 2PC」与「分布式数据库内部 2PC」 | Spanner/TiDB/CockroachDB 的 2PC 运行在**单一数据库内部**，有统一的时钟与并发控制，能做到外部一致/可串行化；XA 跨异构系统做不到这点。本书把两者混在同一章语境里，容易误导 |
| 7 | 🔧 2026 补丁：TCC 的隔离性缺失应显式说明 | TCC 在 Try 之后、Confirm 之前，其他事务能看到「冻结中」的中间态。本书未提这一隔离性缺口，而它正是 TCC 无法替代数据库事务的根本原因 |
| 8 | 🔧 2026 补丁：缺 SAGA 与事务消息两条路线 | 本书只给 XA 与 TCC。2026 年长事务的主流是 **SAGA**（补偿链）与 **事务消息/Outbox**（RocketMQ 半消息），两者业务侵入更低。本章表格已补，建议读者一并了解 |

## 与其他章 / 其他书的联系

- **本目录内**：
  - 本章的原子性问题陈述来自 [01-拜占庭将军问题与CAP-ACID-BASE](01-拜占庭将军问题与CAP-ACID-BASE.md) 2.2（ACID 与 2PC）；
  - 本章与 [02-Paxos与Multi-Paxos](02-Paxos与Multi-Paxos.md) 的关键区分是：**2PC 是原子提交，不是共识**——2PC 中只要有一个参与者挂了就阻塞，而共识要求多数派可用；
  - TCC 的补偿思想在 [11-InfluxDB企业版一致性实现剖析](11-InfluxDB企业版一致性实现剖析.md) 的 hinted handoff 里能见到同构思路（事后补）。
- **跨书**：
  - [../深入理解分布式共识算法/03-2PC与3PC分布式事务.md](../深入理解分布式共识算法/03-2PC与3PC分布式事务.md)——2PC/3PC 与 Seata AT 模式，含**空回滚/防悬挂**，与本章 10.2 完全对口；
  - [../深入理解分布式系统/08-分布式事务.md](../深入理解分布式系统/08-分布式事务.md)——分布式事务的系统书口径；
  - [../数据库系统概念6/26-高级事务处理.md](../数据库系统概念6/26-高级事务处理.md)——教科书对 2PC、XA、事务补偿的标准化表述；
  - [../软件架构设计/10-事务一致性.md](../软件架构设计/10-事务一致性.md)——架构视角的事务一致性决策；
  - [../分布式数据库入门进阶与实战/](../分布式数据库入门进阶与实战/00-总览与阅读地图.md) 第 14 章「分布式事务」——Spanner/Calvin/客户端事务框架，是本章的进阶版。
