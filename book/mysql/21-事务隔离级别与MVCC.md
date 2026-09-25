# 第 21 章 一条记录的多副面孔——事务隔离级别与 MVCC

> 原书说明：标题为「一条记录的多副面孔——事务隔离级别和MVCC」，基于 MySQL 5.7.22 撰写。本文件按其思路展开 **read view、trx_id / roll_pointer、RC 与 RR 的差异**，并补齐 5.7/8.0 的演进与 2020 年之后必须补的**8.0 read view 优化、trx_id 复用陷阱**。

## 本章地图

> 一句话：**同一行记录在磁盘上只有一个最新版本，但在不同事务眼里它是「多副面孔」——这个「面孔」由 `read view`（快照）+ `trx_id`（版本时间戳）+ `roll_pointer`（版本链）三者共同决定。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 21.1 四个隔离级别 | Read Uncommitted / Read Committed / Repeatable Read / Serializable | 标准是「读不到未提交」，RR 额外靠 next-key 锁补幻读 |
| 21.2 行里的两个隐藏列 | `trx_id`(6B) + `roll_ptr`(7B) | 版本链的锚点 |
| 21.3 undo 版本链 | 已提交版本的存放位置 | 一致性读顺着链往前找 |
| 21.4 read view（一致性读视图） | creator trx_id、活跃事务集合、上/下界 | **RC 每次语句建视图，RR 第一次读建视图并复用** |
| 21.5 可见性判断规则 | 一次「沿链找可见版本」的算法 | 规则只有 4 条，慢的是链长 |
| 21.6 RC 与 RR 的核心差异 | 视图创建时机 | 一个「每句一快照」，一个「事务一快照」 |
| 21.7 幻读与 Next-Key Lock | RR 下靠 `next-key` 锁消除幻读 | 标准定义的 RR 有幻读，InnoDB 的 RR 没有 |
| 21.8 当前读 vs 快照读 | `SELECT` 走 MVCC；`UPDATE`/`FOR UPDATE` 走锁 | 混用两者是数据不一致的经典来源 |
| 21.9 🔧 2026 视角 | 8.0 的 read view 优化、trx_id 复用陷阱、写偏斜 | 原书的 RC 也有「奇怪现象」 |

## 核心精讲

> **教学示意，不参与构建。** 下文结构与 `--` 片段仅用于说明可见性判断语义，**未在本机编译、未连接任何 MySQL 实例执行**。

### 21.1 四个隔离级别

| 隔离级别 | 脏读 | 不可重复读 | 幻读 | InnoDB 下实现 |
| --- | --- | --- | --- | --- |
| `READ UNCOMMITTED` | 可能 | 可能 | 可能 | 几乎不用（读不加锁，一致性最差） |
| `READ COMMITTED`（RC） | 不会 | 可能 | 可能 | 语句级 read view |
| `REPEATABLE READ`（RR，默认） | 不会 | **不会** | **不会**（靠 next-key 锁） | 事务级 read view + next-key 锁 |
| `SERIALIZABLE` | 不会 | 不会 | 不会 | RR + 全表锁读（`SELECT ... FOR SHARE`） |
- **标准（ANSI SQL）的 RR 允许幻读**，而 **InnoDB 的 RR 不允许** —— 这是面试高频陷阱，原因见 21.7。
- 默认值：`transaction_isolation`（8.0 起的参数名，5.7 为 `tx_isolation`）默认 `REPEATABLE-READ`。
- 可以设置全局/会话/下一个事务三个层级；🔧 8.0 支持 `SET PERSIST` 持久化。

### 21.2 行里的两个隐藏列

- 每条记录（聚簇索引里）带：`DB_TRX_ID`(6B) 与 `DB_ROLL_PTR`(7B)，另有可选的 `DB_ROW_ID`(6B)（无主键时）。
- **只有聚簇索引行带这两个列**；二级索引行**不带 trx_id** —— 这是理解「为什么有时二级索引查询要回表判断可见性」的关键。

### 21.3 版本链：多副面孔的物理存放

```text
当前行（trx_id = 100，roll_ptr → U_n）
   │
   ▼
U_n：最后一次 UPDATE 之前的镜像（trx_id = 88）
   │
   ▼
U_{n-1}：更早的镜像（trx_id = 54）
   │
   ▼
...（一直串到 INSERT 那条 undo，U_0 的 roll_ptr 为 NULL）
```
- 历史版本全部在 **undo 段**里；purge 线程在「最老 read view 之后」才能回收它们（见 `20-undo日志.md` 20.7）。
- 🔧 **推论**：长事务会让版本链变长 → 一致性读变慢 → purge 变慢 → undo 膨胀。三者是同一个根因。

### 21.4 read view：快照到底是什么

read view（一致性读视图）的四个要素（教学示意，不参与构建）：

| 字段 | 含义 |
| --- | --- |
| `creator_trx_id` | 创建这个视图的事务 ID（只读事务为 0） |
| `m_trx_ids` | 创建时刻**尚未提交**的活跃事务 ID 列表 |
| `m_up_limit_id` | 活跃事务中**最小的** trx_id |
| `m_low_limit_id` | 创建时刻**下一个将要分配**的 trx_id（即「上界」） |

于是「一条记录该不该被本事务看到」简化成：**它最后一次被修改的 `trx_id` 落在哪个区间**。

- **RC**：**每条语句**开始时新建一个 read view。
- **RR**：**第一个**一致性读（快照读）时建一个 read view，之后整个事务复用。
  ```text
  RR 事务 T：  SELECT ① → 建 read view（m_low_limit_id = 200）
              另一个事务 U 提交（trx_id 150）
              SELECT ② → 复用同一个 read view → 仍看不到 150 的改动 ✅
  ```
- 🔧 **8.0 的 read view 优化**：为避免每次语句都构造/维护 read view 带来的开销（尤其 RC 下每句都建），8.0 改用了更高效的实现（红黑树结构 + 减少全局互斥）。**结果层面的语义没变，但性能表现变了** —— 这是 2020 年之后 RC 才「突然变得便宜」的原因。

### 21.5 可见性判断：一次沿链查找

给定 read view 与一条记录，判断它是否可见（教学示意，不参与构建）：

```text
while (当前版本存在):
    trx_id = 该版本的 DB_TRX_ID
    if trx_id == creator_trx_id:            → 看得见（自己改的）
    else if trx_id < m_up_limit_id:         → 看得见（创建视图时已提交）
    else if trx_id in m_trx_ids:            → 看不见（创建时还没提交），往前翻
    else if trx_id >= m_low_limit_id:       → 看不见（比视图还晚开始），往前翻
    else:                                   → 看得见
    顺着 roll_pointer 找下一个版本
返回：第一个可见的版本，或「不可见」（返回 NULL / 跳过该行）
```

- 三条工程含义：
  1. **链越长，判断越慢** → 所以长事务 + 频繁更新 = 查询变慢。
  2. **RR 下「看不到」不等于「不存在」** —— 也许它在你之前被提交，只是你那一刻开始得太早。
  3. **RC 下同一条记录在同一事务内两次读可能不同** —— 这不是 bug，是 RC 的定义。

### 21.6 RC 与 RR 的核心差异：只有「快照时机」不同

| 场景 | RC 的结果 | RR 的结果 |
| --- | --- | --- |
| 事务开始时他人提交 | **看得到** | 看不到 |
| 事务内两次读同一行 | 可能不同 | 始终相同 |
| 语句看到的是 | **语句开始时刻**的快照 | **事务开始时刻**的快照 |
| `SELECT ... FOR UPDATE` 的结果 | 与快照不同，是**最新已提交 + 加锁** | 同左（当前读不受快照限制） |
- 🔧 **RC 下的两个常见「意外」**：
  1. **RC 下依然存在「不可重复读」** —— 这是定义如此，很多团队把它误认为 bug；
  2. **RC 下「半边更新」现象**：一个事务 `UPDATE` 了 A 行未提交，另一个事务读 B 行照常；但如果业务层依赖「读到 A 的旧值并据此更新」，RC 下就可能读到「中间状态」—— 因此 **RC + 应用层「先读后写」不是原子的**，必须 `FOR UPDATE` 或乐观锁。

### 21.7 幻读与 Next-Key Lock：为什么 InnoDB 的 RR 没有幻读

- **幻读**：同一事务两次范围查询，另一事务**插入**了满足条件的新行。
- 纯 MVCC **无法**解决幻读（看不到别人已提交的插入，但也拦不住别人插入）。
- InnoDB 的解法：**在 RR 下，当前读（`UPDATE` / `DELETE` / `SELECT ... FOR UPDATE`）会对索引做 **next-key lock**（记录锁 + 间隙锁）**（详见 `22-锁.md`）。于是「你要插到我锁住的区间里？先排队」—— 幻读从「看不见」变成「插不进来」。
- 所以结论是：
  - **标准 RR** 允许幻读；
  - **InnoDB RR**（默认隔离级别）**不允许幻读**，代价是多出了间隙锁的并发开销。
- 另外：**快照读（`SELECT`）在 RR 下依然可能看到「别人后来插入的行」吗？** 不会 —— 因为 read view 是事务开始时建的，插入行的 `trx_id` 通常 ≥ 上界，所以不可见。**但 `SELECT` 本身不加锁，拦不住别人插入**；只有当前读才拦。

### 21.8 当前读 vs 快照读：最容易踩的两类写法

| 类型 | 典型语句 | 走什么机制 |
| --- | --- | --- |
| 快照读（一致性读） | 普通 `SELECT` | MVCC，**不加锁** |
| 当前读 | `SELECT ... FOR UPDATE` / `FOR SHARE`、`UPDATE`、`DELETE`、`INSERT`（唯一键冲突检查时） | **加锁**（行锁 / next-key 锁） |

- 经典错误（教学示意，不参与构建）：
  ```sql
  -- 意图：避免超卖。但 SELECT 是快照读，两个事务可能同时读到「剩 1」
  BEGIN;
  SELECT stock FROM t WHERE id=1;          -- 快照读，不加锁
  UPDATE t SET stock = stock - 1 WHERE id=1;  -- 当前读，加锁
  COMMIT;
  ```
  正确写法：把 `SELECT` 改成 `SELECT ... FOR UPDATE`（当前读，锁住该行），或直接用 `UPDATE t SET stock = stock - 1 WHERE id = 1 AND stock > 0` 并校验影响行数。
- 另一类错误：**在同一个事务里混用快照读与当前读**，导致「我看到的库存和我改的库存不是同一个数字」。
- 注意：`REPEATABLE READ` 下**当前读总是读最新已提交版本**，不受 read view 限制 —— 这是理解「为什么 RR 下 `UPDATE` 会覆盖别人已提交的修改」的关键。

### 21.9 🔧 2026 视角：8.0 的 MVCC 与 trx_id 复用陷阱

- **read view 实现的重构（8.0）**：RC 下每句都要建视图，8.0 用更高效的数据结构与更少的全局同步；RR 下则明确在事务首个快照读时创建并**全程复用**。语义不变，成本下降。
- 🔧 **`innodb_max_trx_id` 与 trx_id 复用陷阱**：trx_id 是 48 位，用尽后系统会在「更小的 ID 范围」上继续分配。若此时还有**很老的 read view** 在比较 trx_id，理论上可能得出错误的可见性结论（历史上出现过「已提交事务却读不到」的诡异现象）。
  - 运维含义：**极其老旧的长事务（甚至跨版本备份事务）风险更大**；升级到 8.0 后务必复核「最老活跃事务」的时长监控。
  - 这不是「你一定会遇到」，而是「长事务 + 8.0 升级」组合下的已知风险面。
- 🔧 **MySQL 仍然没有 SSI**：InnoDB 的 RR 消除了读写幻读，但**没有消除「写偏斜（write skew）」**。快照隔离的经典反例（两个医生同时请假导致没人值班）在 MySQL RR 下**依然会发生** —— 需要应用层用 `SELECT ... FOR UPDATE` 或唯一约束兜底。
  - 对照：`postgresql/postgres` 有 SSI（可串行化快照隔离），这是两者语义上最实质的差距。
- 🔧 **并行复制下的 MVCC 语义**：RC/ROW 模式下从库回放顺序可能与主库不同（依赖 writeset 判定），「最终看到的状态」与主库逐个事务略不同 —— 涉及「先读后写」逻辑时要用 `slave_preserve_commit_order` 或业务层幂等。

## 版本演进

| 版本 | MVCC / 隔离级别相关变化 |
| --- | --- |
| 5.5 | RR 为默认隔离级别；undo 与版本链成型 |
| 5.6 | read view 实现改进；`innodb_max_trx_id` 冲突处理更规范 |
| 5.7 | `innodb_max_trx_id` 相关行为稳定；参数名 `transaction_isolation` 过渡 |
| 8.0 | 参数改名为 `transaction_isolation`；**read view 优化**；只读优化（`READ ONLY`） |
| 🔧 8.0.x | trx_id 复用范围与老 read view 的交互被反复修正，需关注 release notes |

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Berenson et al., *A Critique of ANSI SQL Isolation Levels* | SIGMOD 1995 | 指出标准隔离级别定义漏洞，提出**快照隔离（SI）**与写偏斜异常 |
| Fekete et al., *Making Snapshot Isolation Serializable* | ACM TODS 2005 | 写偏斜的完整刻画与 SI 的正确性边界 |
| Cahill, Röhm, Fekete, *Serializable Isolation for Snapshot Databases* | SIGMOD 2008 | **SSI** 方案 |
| Ports & Grittner, *Serializable Snapshot Isolation in PostgreSQL* | PVLDB 2012 | SSI 的工程落地 |
| Bernstein, Hadzilacos & Goodman, *Concurrency Control in Distributed Database Systems* | ACM Computing Surveys 13(2), 1981 | 多版本并发控制协议的分类学 |
| MySQL 官方文档：innodb-max-trx-id / Read Views / Isolation Levels | dev.mysql.com | trx_id 位数、read view 字段、隔离级别语义的权威口径 |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：**快照隔离的边界与加固**——SSI、可串行化的低成本实现（*Fast Serializable Snapshot Isolation for Read-Only Transactions*, VLDB 2021；*Determining Serializability for Snapshot Isolation*, TODS 2020）；**无锁 read view / 低开销快照**（CockroachDB 的 `Read Timestamp Cache`、FoundationDB 的只读快照无需全局协调）；**HTAP 下的一致性读**（TiFlash 用「先读后写冲突检测」保证 MVCC 语义跨引擎一致）。
- **工业界开源**（star 数 2026-09-25 通过 `gh api` 实测）：
  - `mysql/mysql-server`（≈12.4k★）：read view 实现 `storage/innobase/read/read0read.cc`；可见性判断 `read0read.cc` 的 `trx_visible_to` 系列函数；`trx_id` 分配在 `trx0trx.cc`。
  - `postgres/postgres`（≈22.2k★）：**唯一实现 SSI** 的开源关系库（`src/backend/storage/lmgr/predicate.c`），是理解「MySQL RR 还剩什么洞」的必读代码。
  - `pingcap/tidb`（≈40.6k★）：MVCC + Percolator 快照时间戳，把 read view 的概念扩展到分布式。
  - `cockroachdb/cockroach`（≈32.5k★）：使用 HLC 作为快照时间戳，`read timestamp cache` 避免了全局 read view。
  - `mariadb/server`（≈8.3k★）：隔离级别与 MVCC 实现细节与 MySQL 保持兼容但有分支差异。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「RC 会让 MySQL 出问题，所以全用 RR」 | 选级别要看业务：RC 下「先读后写」不安全，RR 下写偏斜仍在；都需 `FOR UPDATE` 兜底 |
| 2 | 「RR 下 `SELECT` 能看到别人新插入的行吗？」 | 快照读看不到（trx_id 在上界之外）；但 `SELECT` **不加锁拦不住**别人插入 |
| 3 | 「InnoDB 的 RR 就是标准 RR」 | 标准 RR 允许幻读，**InnoDB 靠 next-key 锁消除了幻读** |
| 4 | 「RR 下 `UPDATE` 用的是事务开始时的数据」 | 当前读读的是**最新已提交版本**，不受 read view 限制 |
| 5 | 「RR 就完全可串行化了」 | 只消除幻读；**写偏斜**依然存在 |
| 6 | 🔧 **本书未覆盖** | 原书基于 5.7.22，**没有** 8.0 的 read view 优化实现细节，也**没有** **`innodb_max_trx_id` / trx_id 复用导致的可见性陷阱** |
| 7 | 🔧 **本书未覆盖** | 原书把 RC 描述成「问题较少」，但**没讲清 RC 下「先读后写」同样不安全**，也没有** MySQL 没有 SSI 这一致命对照**（PostgreSQL 有） |

## 与其他章 / 其他书的联系

- → `20-undo日志.md`：版本链的物理载体就是 undo；purge 的限制来自最老 read view。
- → `22-锁.md`：next-key 锁是「消除幻读」的另一半；当前读与快照读的分界在此。
- → `19-redo日志.md`：`trx_id` 也是 redo 与 MVCC 之间的桥梁。
- → `18-事务的庐山真面目.md`：隔离性是事务四特性之一。
- → `X2-日志系统专题.md`：RC/RR 的差异也决定了 binlog 组提交与并行复制的安全边界。
- → [15-并发控制.md](../数据库系统概念6/15-并发控制.md)：MVTO / MV2PL / 快照隔离 / SSI 的通用理论，以及 PostgreSQL 的落地。
- → [26-高级事务处理.md](../数据库系统概念6/26-高级事务处理.md)：写偏斜与 SI 的工业解法。
