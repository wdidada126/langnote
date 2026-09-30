# 09 事务与 ACID

> 单元性质：⚠️ 主题重构。对应教材通行"Transactions"单元。深度对照：[../数据库系统概念6/14-事务.md](../数据库系统概念6/14-事务.md)；中文对照：../数据库系统概论.md 第 13 章（恢复）与并发篇；事务专著：../数据库事务处理的艺术.md；论文线：[../../db/db.md](../../db/db.md)。

## 1. 事务=应用正确性的合约单位

定义：不可分割的读写操作序列，BEGIN…COMMIT/ROLLBACK 定界；**COMMIT 之后改变永久，ROLLBACK 之后世界如未发生**。教材经典例：转账（T1 扣 A 加 B），失败必须整体撤销——原子性+一致性的最小演示。概念6 的"一致性=DB 状态满足完整性约束"口径在此延用：03 章约束是"一致性"的形式内容。

## 2. ACID 逐词拆

- **A 原子性**：全做或全不做；机制在 11 章（日志回滚）。
- **C 一致性**：约束守恒（事务作者的责任+引擎辅助）。
- **I 隔离性**：并发事务互不见中间态；**注意**隔离强度是光谱不是开关（10 章隔离级别）。
- **D 持久性**：提交扛得住崩溃；机制=日志先写+介质假设。
教学口径：A/I/D 是引擎机制承诺，C 是应用语义责任——四字并排常被误读为"四个同级功能"。

## 3. SQL 事务控制语法

`START TRANSACTION/BEGIN`、`COMMIT`、`ROLLBACK`、`SAVEPOINT sp / ROLLBACK TO sp`（部分回滚）、`SET TRANSACTION ISOLATION LEVEL ...`、隐式提交（DDL 自动提交是 MySQL 家传统 ⚠️ 方言点，SQLite 的 DDL 也在事务包裹上 behave 特殊）。**autocommit 模式**：每条语句自成一事务——DB-API 的 isolation_level=None 即其显式形态。

## 4. 🔧 exp3/exp5 事务实测语料（SQLite 3.45.3 + DuckDB 1.5.5）

| 实验点 | 🔧 实测 |
|---|---|
| BEGIN→UPDATE v=999→ROLLBACK | 读回 v=10，未泄漏 |
| BEGIN IMMEDIATE + SAVEPOINT sp1→DELETE→ROLLBACK TO sp1→COMMIT | DELETE 被撤销，v=20 保住（部分回滚成立） |
| 双连接写冲突 | a 持 `BEGIN IMMEDIATE` 写锁，b `BEGIN IMMEDIATE` 报 `database is locked`（busy timeout=0.1s 生效）——SQLite 读者不挡写者（WAL 语境），写写互斥 |
| DuckDB 转账 BEGIN→双向 UPDATE→ROLLBACK | 余额回到 (100.00, 0.00)；COMMIT 版本 (70, 30) |
| 未提交即断连（隐式事务） | exp5：连接 close 未 commit，重开只见 1 行——**客户端异常断连=自动回滚**，D 只保护已提交的世界 |

复现：`dbwave_w7_dbill\exp3_transactions.py`、`exp5_wal_duckdb_nosql.py`。

## 5. 异常处理与应用侧模式

教材给嵌入式 SQL 的 SQLSTATE/指示器；现代对应 Python try/except + `conn.rollback()` 包裹、"单元工作模式"（one transaction per logical unit）、**幂等重试**（提交结果未知时的 idempotency key——13 章分布式会重新需要它）。事务边界放在服务方法层而非 DAO 层，是把教材概念翻译成工程的第一课。

## 6. 只读事务与长事务之罪

`START TRANSACTION READ ONLY` 给优化器/复制以额外自由度；**长事务**在引擎侧钉住旧版本/膨胀 undo 日志/阻回收——SQLite WAL 的 checkpoint 同理受阻。教材常漏这条工程铁律，本目录在此补写。

## 7. 与相邻章节的接缝

- 03：C 的约束来源；05：事务内语句的求值语义（快照读 vs 当前读在 10 章展开）。
- 10：I 从"承诺"变"级别菜单"；11：A/D 的日志机制实现；13：D 在复制环境的弱化（异步副本可能丢已提交数据 ⚠️ 云实践注记）。
- BASE 阵营（14 章）以"放弃 I 与强 D 换可用性"为口号，ACID 的教学价值恰在对照中显形。

## 8. 常见错误清单

1. 忘 COMMIT 就断连，以为数据已存（exp3 反例实测）。
2. 在循环里逐条 autocommit 批量导入（exp4 用 executemany+单事务是数量级差）。
3. 把 ROLLBACK 当"撤销一切"的后悔药——已 COMMIT 段力不从心（用 SAVEPOINT 分段，exp3 实测）。
4. 以为 DDL 可回滚（跨引擎行为不一 ⚠️ 用 exp1 场景自行验证：SQLite DDL 事务包裹语义特殊）。
5. 依赖隔离"默认级别"不显式声明（10 章第一异常来源）。

## 9. 小结

事务把"多语句一个对错"钉为合约单位，ACID 给四维承诺并各归其主。下一章追问承诺里最含糊的 I：并发交错下什么异常能发生、级别菜单如何分级堵住。

## 10. 补充：exp3 时间线逐帧图（文字版）

双连接 a/b 的交错（🔧 实录时序）：

```
a: BEGIN IMMEDIATE      -- a 拿到库级写锁
a: UPDATE t SET v=30
b: BEGIN IMMEDIATE      -- 等待 0.1s（busy timeout）
b: → OperationalError: database is locked
a: COMMIT               -- 锁释放
b: BEGIN IMMEDIATE（重试成功）
b: UPDATE ... v=40; COMMIT
读回 v=40 —— 串行化结果与"b 从未插队"的直觉一致
```

教学要点：① "locked 即隔离的粗粒度形态"——SQLite 用忙错替代排队，应用必须写重试（与 05 章计划外异常处理、本节幂等姿势同源）；② timeout=0.1 是我们刻意设小以便当场看见，默认 timeout=5s 时 b 会先等再错——**隔离性强度与等待策略是两个独立旋钮**。

## 11. 补充讨论：事务边界的架构位置

- 单服务：方法级边界（ORM unit-of-work）；
- 跨服务：无全局事务→Saga 编排/编舞（10 章末），补偿语义写进接口契约；
- 跨存储（DB+消息队列）："提交后发送"的 outbox 模式（同库表事务+后台搬运）——**用同库 ACID 冒充分布式原子性**，是本册知识最锋利的工业应用。
- 只读副本上的"读自己刚写的"（read-your-writes）需要会话一致性协议 ⚠️ 转述：13 章复制延迟的应用面。

## 12. 自测四问

1. ROLLBACK 能撤销已 COMMIT 的段吗？（不能；SAVEPOINT 只覆盖未 COMMIT 区间——exp3 分段实验。）
2. "提交后进程崩溃"数据丢吗？"提交前"呢？（前者已 fsync 日志段，恢复重做；后者恢复撤销——exp5 断连即样本。）
3. 为什么事务里放 HTTP 调用是反模式？（网络延迟拉长持锁时间→并发崩塌；外部副作用不可回滚→用 outbox/异步。）
4. SQLite `BEGIN DEFERRED` 与 `IMMEDIATE` 的隔离差异？（DEFERRED 读时才拿锁，写锁可能晚到引发 SQLITE_BUSY 于 UPDATE 中；IMMEDIATE 开局占写锁——边界提前是工程偏好。）

## 13. ACID 故障映射表（每字母对应哪种"坏日子"）

| 字母 | 防的事故 | 机制所在 | 现场实验 |
|---|---|---|---|
| A | 半途而废（转账扣了没加） | 日志 undo/回滚 | 🔧 exp3 ROLLBACK 保 v=10 |
| C | 约束被跨语句组合违反 | 约束执法+应用逻辑 | 🔧 exp1 三类违约报错 |
| I | 交错污染（10 章异常谱） | 锁/快照/级别 | 🔧 exp3 写写互斥 locked |
| D | 崩溃抹掉已提交 | WAL+fsync+恢复 | 🔧 exp5 断连回滚（反面：未提交本就不该存） |

这张表是 09–11 三章的"总目录"：面试被问 ACID 时按行展开=自带结构的答案。

## 核心概念速览（中英对照）

- **transaction** — 事务：不可分割的语句序列
- **BEGIN / COMMIT / ROLLBACK** — 提交/回滚：时间两态的界碑
- **SAVEPOINT** — 保存点：部分回滚（🔧 exp3 实测 DELETE 撤销）
- **autocommit** — 自动提交：单语句即事务的缺省形态
- **ACID** — 原子/一致/隔离/持久：机制与责任的分工表
- **atomicity** — 原子性：全有或全无
- **durability** — 持久性：提交扛崩溃；未提交断连=回滚（🔧 exp5）
- **read-only transaction** — 只读事务：额外优化的声明式许可
- **long-running transaction** — 长事务：版本钉住与回收阻碍之罪
- **unit of work** — 工作单元：应用侧事务边界粒度
- **idempotent retry** — 幂等重试：结果未知场景的安全重放
- **implicit commit on DDL** — DDL 隐式提交：方言雷区 ⚠️

## 最新演进与工业实践

- **JDBC/ORM 层事务抽象成熟**：Spring `@Transactional` 传播语义、SQLAlchemy session 单位工作模式是教材概念的工业转写；2024–2026 教程普遍以 ORM 为主入口，但排错仍需回到裸 BEGIN/COMMIT 心智（本目录 exp3 即排错底图）。
- **托管事务的持久性再分级**：云数据库用"多副本 quorum 提交"重定义 D（RPO 谈判点），单副本承诺与跨可用区承诺差价明显 ⚠️ 各服务口径以其白皮书为准。
- **嵌入式引擎事务边界**：SQLite WAL 提供"读者不阻写"的高并发事务形态；DuckDB 单写者模型适合分析批任务——"事务 OLTP/批处理 OLAP"分工在 Python 栈里即两包并存的日常（../DuckDB_in_Action/06-融入Python生态.md）。
- **无服务器/NewSQL 的分布式事务**：TiDB/CockroachDB/YugabyteDB 以 Percolator/Raft 复刻 ACID 于分片间——教材单机叙事的外延，衔接 13 章。
