# 05 并发锁与UNDO调优 — Oracle Performance Tuning, 2e（精读重构）

> ⚠️ 主题重组口径（[00-总览与阅读地图.md](00-总览与阅读地图.md) §3/§8）。闩、锁、ITL/块竞争与 undo 的 9i/10g 病理学；
> Oracle 行为 ⚠️ 转述；🔧 用 SQLite 写冲突/UNDO 计时做机制类比（非 Oracle 行为）。

## 1. 三种"等"的谱系：闩 / 锁 / 行争用（⚠️ 通说）

| 层 | 保护对象 | 语义 | 代表等待 |
|---|---|---|---|
| Latch 闩 | SGA 内部结构（链、池） | 无死锁检测、get/release、spin+sleep | `latch: cache buffers chains`、`latch: shared pool` |
| Enqueue 锁 | 对象生命周期（表/行/字典） | 模式化、有死锁检测（ORA-60） | `enq: TX - row lock contention` |
| 块内争用 | 同一数据块内并行度 | ITL/freelist/百分比 | `buffer busy waits`、`ITX` 类 |

- 闩算法 ⚠️：先立即试（immediate）→ 自旋 N 次（`latch_misses` 统计自旋/睡眠比）→ 睡眠排队；10g 的"延迟释放"（nowait 模式）改写了部分等待曲线。
- 锁模式教学模型 ⚠️：DML 自动成对——表级 **TM**（意向锁，挡 DDL）+ 行级 **TX**（真正锁行）；`V$LOCK` 的 LMODE/BLOCK 读法至今不变；`SELECT FOR UPDATE` 的 NOWAIT/WAIT n 是应用侧第一道闸。

## 2. 行锁病理：谁堵谁，怎么治（⚠️ 通说）

- 经典分类（TX 等待的 reason 码，10g `V$SESSION` 前夜/11g 起 `BLOCKING_SESSION*` 列成熟 ⚠️）：
  1. 未提交长事务持行（业务逻辑/忘记提交）——唯一解是缩短事务，不靠调参。
  2. **热行队列化**（计数器/序列/账户余额单行高频更新）——治法谱系：应用分片（sharding key 拆分行）、`SELECT FOR UPDATE NOWAIT` + 重试、序列缓存放大；12c 身份列/缓存序列是后续代际的官方解（本册时代以应用改造为主 ⚠️）。
  3. 外键无索引 → 子表检查锁父表行（经典事故，`06` 章索引话题与约束语义的交点 ⚠️）。
- 死锁 ORA-60：trace 文件锁图读法（持有者/请求者双环）⚠️——与 `02` 章 10046/trace 工具链同一条线（✅ 深版对读 [../Troubleshooting_Oracle_Performance_2e/03-可复现问题的分析.md](../Troubleshooting_Oracle_Performance_2e/03-可复现问题的分析.md)）。

## 3. ITL 与 freelist：块级并发的地基（⚠️ 通说）

- **ITL（Interested Transaction List）**：块头事务槽，`INITRANS/MAXTRANS` 控制；槽尽 → `ITL 等待/块内串行` ⚠️。10g 后 ASSM（系统管理段）用位图块替代 freelist 组，把"段头竞争"消灭在结构层（`PCTUSED`/`FREELISTS/FREELIST GROUPS` 退位 ⚠️）——本册 2e 恰逢 ASSM 前夜，通说仍以 freelist 条带化为主课（⚠️ 推定）。
- **PCTFREE 调优语义**：预留更新空间防**行迁移（migrated rows）**——行迁移让一次逻辑读变两次（链接追块），账本上表现为 `db file sequential read` 小峰 ⚠️（TOP 2e 物理设计章同款结论，✅ [../Troubleshooting_Oracle_Performance_2e/16-优化物理设计.md](../Troubleshooting_Oracle_Performance_2e/16-优化物理设计.md)）。
- RAC 语境的"块在多实例缓存的复制"（Cache Fusion）在本册按通说仅有预告性段落 ⚠️；精读让位《Oracle编程艺术》与 RAC 专著线。

### 🔧 类比 D4-EXT：一次 UPDATE 的 UNDO 账（SQLite，非 Oracle）

`demo_out.txt` 的 WRITE+UNDO-类比项：对 20 万行表 `UPDATE big SET pad=pad WHERE a=3`（命中 1 万行）后 **ROLLBACK**，计时 **14.369 ms**，占三操作总账 25.185 ms 的 **57.1%**——"改了又撤销"仍要付全价：写 undo、再按 undo 反放。Oracle 账本对应物：undo 生成量（`V$TRANSACTION`）、`UNDO TABLESPACE` 增长、回滚等待。验证的结论同构：**回滚不是免费的，长事务+大 UPDATE 是 undo 空间与一致性读的双料炸弹** ⚠️。

## 4. Undo/Rollback：一致性读的代价体系（⚠️ 通说）

- 双职责 ⚠️：**回滚**（原子性）+ **读一致性**（CR 块重建——查询沿 undo 链回溯到 SCNs 可见版本）。
- 9i 代际：回滚段手工条带（`rollback_segments`、按热段分组防争用）→ **自动 undo 管理**（`UNDO_MANAGEMENT=AUTO`、`UNDO_TABLESPACE`、区级自动扩展）⚠️——本册 2e 正处过渡期，通说两种管法并列讲（⚠️ 推定）。
- **ORA-01555 snapshot too old**：读侧经典——长查询 + 快覆盖 undo 的组合病；对策清单 ⚠️：加大 undo 保留（`undo_retention` + 10g RETENTION GUARANTEE 表空间）、给读事务建"稳定快照"（拆分/物化/复制读）、装载期用 `NOLOGGING`+分批防覆盖风暴。
- 段头竞争（segment header）：高频小插入在块位图/区间管理上的串行点 ⚠️——与 `02` 章 `buffer busy waits` 互证。

## 5. 并发调优决策树（⚠️ 收口）

```
等待出现 → 是 latch/enq/buffer busy?
├─ latch：定位父闩子闩号 → 关联 SGA 域（03 章）→ 先修结构饥饿再谈自旋参数
├─ enq TX：查持锁者（V$LOCK/V$SESSION）→ 应用事务边界/热行分片，不调参
├─ buffer busy：段头 or 热块 or 单块读风暴 → ASSM/PCTFREE/缓存策略
└─ 01555/快照类：undo 保留 + 读路径改造
```

（该树是本目录对"结构派并发章"的重构，非原书流程图 ⚠️。）

## 6. repo 对读

- 机理正典：[../Oracle编程艺术：深入理解数据库体系结构（第3版）.md](../Oracle编程艺术：深入理解数据库体系结构（第3版）.md)（块头/ITL/undo 逐字节级）。
- 诊断工程化：[../Troubleshooting_Oracle_Performance_2e/04-不可复现问题的实时分析.md](../Troubleshooting_Oracle_Performance_2e/04-不可复现问题的实时分析.md)（锁与闩的现行视图读法）。
- 教材速览：[../Oracle12c数据库应用与开发/04-事务与redo-undo-归档.md](../Oracle12c数据库应用与开发/04-事务与redo-undo-归档.md)、[../Oracle12c数据库应用与开发/05-索引与约束.md](../Oracle12c数据库应用与开发/05-索引与约束.md)。
- 跨引擎锁语义对照：[../The_Definitive_Guide_to_SQLite_2e/00-总览与阅读地图.md](../The_Definitive_Guide_to_SQLite_2e/00-总览与阅读地图.md)（整库锁→WAL 的行级化史）。

## 6.1 补充：锁模式compat矩阵（教学版 ⚠️，TM 语义）

| 请求\持有 | NULL | SS(RS) | SX(RX) | S | SIX | X |
|---|---|---|---|---|---|---|
| SS | ok | ok | ok | ok | ok | 冲突 |
| SX | ok | ok | ok | 冲突 | 冲突 | 冲突 |
| S | ok | ok | 冲突 | ok | 冲突 | 冲突 |
| SIX | ok | ok | ok | 冲突 | 冲突 | 冲突 |
| X | 冲突 | 冲突 | 冲突 | 冲突 | 冲突 | 冲突 |

- 读法 ⚠️：普通 DML=RX（SX）：彼此相容、只挡 S/X（=挡读表/挡 DDL 的"意向"本义）；`LOCK TABLE ... IN EXCLUSIVE MODE` 的滥用是"人肉串行化"反模式。
- 查案 SQL 形状 ⚠️：`V$LOCK` 自联接（BLOCK=1 行给"谁挡谁"），11g+ 用 `V$SESSION.BLOCKING_SESSION` 直读（✅ 26/19 文档主链，见文末锚）。

## 6.2 ITL/事务槽预算速算（⚠️ 通说教学）

```
块内并发需求 ≈ 该块所在段的并发热度假设
  INITRANS 起步：OLTP 索引/热表 8（默认 2 常不够 ⚠️）
  判据：ITL 等待/块串行现象 + 块dump（受控环境 ALTER SYSTEM DUMP ...）
  ASSM 时代：freelist 病 → 位图块争用，另一张图
```

- 与 `03` 章热块问题的分界：**同一块被同事务群改 → ITL/freelist；被跨会话读风暴钉 → cache buffers chains**。处置不同（改段参数 vs 散列数据）。
- PCTFREE 与更新放大 ⚠️：UPDATE 若使行长超出块空余即行迁移（`05` 病灶之一）；"先全删重插"的批处理伪装调优其实是块重组。

## 6.3 undo 容量估算式（⚠️ 时代配方）

```
UNDO 空间 ≈ 峰值（每秒重做生成率中"被 undo 记录的部分"） × 最长查询(或长事务)时间 × 安全系数
（10g 顾问化：V$UNDOSTAT 的 UNDOTUNE/最大保留时长直读 ⚠️）
```

- `undo_retention` 语义 ⚠️：目标保留秒数（RETENTION GUARANTEE 前是"尽力"）；01555 的另一半解在读侧——**给报表建快照（物化/复制/后来的 Data Guard 备库读）**是 2006 年即成熟的好答案。
- 长事务三宗罪 ⚠️：undo 膨胀（空间）、回收站式清不掉（V$TRANSACTION 常驻）、备库/同步链路延迟（10g 后新增维度，`04` 章 standby 线）。

## 6.4 一页记忆卡（⚠️ 自测）

1. latch 与 enqueue 的死锁待遇差异？——前者不检测（超时/自旋/睡眠纪律），后者 ORA-60 检测并牺牲 ⚠️。
2. `SELECT FOR UPDATE` 何时不该用？——能用乐观列版本（版本列/`ON DUPLICATE` 语义）替代悲观持锁的交互路径 ⚠️。
3. ASSM 消灭了什么、留下了什么？——消灭 freelist 组条带课；留下 ITL 与热块链。
4. 01555 的读侧解排序？——快照设施（物化/备库读）> 拆查询 > 加 retention > 加 undo 空间。
5. undo 生成的账在哪三章都出现？——`04`（redo 伴随）、`05`（本章）、`07`（逐行提交放大）。

## 核心概念速览（中英对照）

- **闩** — Latch：SGA 内部结构的轻量自锁，无死锁检测、spin+sleep 获取。
- **enq 队列锁** — Enqueue：模式化通用锁框架（TM/TX 由它派生）。
- **TM/TX 锁** — Table/Row DML 锁对：意向表锁 + 行锁双保险 ⚠️。
- **SELECT FOR UPDATE** — 显式行锁 API：NOWAIT/WAIT n 控制等待语义。
- **死锁** — Deadlock（ORA-00060）：环等待被检测、牺牲一方并出 trace 图。
- **ITL** — Interested Transaction List：块头事务槽（INITRANS/MAXTRANS）。
- **FREELIST 组** — 空闲列表组：RAC 时代段内并发的老条带手段 ⚠️。
- **ASSM** — Automatic Segment Space Management：10g 位图块替代 freelist。
- **行迁移/行链接** — Migrated/Chained Rows：块放不下致一次逻辑读变两次。
- **UNDO** — 回滚/一致性数据：回滚 + CR 重建双职责（ORA-01555 = 读侧饥饿）。
- **CR 块** — Consistent Read clone：沿 undo 链重建的查询快照副本 ⚠️。

## 最新演进与工业实践

- **文档锚 ✅（2026-09-28 curl 200）**：并发与一致性内容现行于 Tuning Guide 26 根页 https://docs.oracle.com/en/database/oracle/oracle-database/26/tgdba/index.html ；事务模型在 Concepts 文档族（未逐页校验 ⚠️）。19 版镜像 https://docs.oracle.com/en/database/oracle/oracle-database/19/tgdba/index.html 同构。
- **闩的退场** ⚠️：10g 延迟释放 → 11g **mutex/原子操作**替换热点闩（library cache 全量）、细粒度子闩哈希——今天 AWR 里 latch 段占比已边缘化，但 `cache buffers chains` 子闩在超热块场景仍会探头。
- **锁的现代面孔** ⚠️：12c 起 `V$SESSION` 阻塞链列（BLOCKING_SESSION + SQL_ID + 会话诊断仓 ADR/`v$diag_*`）；**23ai** 新增 `SELECT FOR UPDATE NOWAIT` 的语义扩展与 JSON 关系双模下的行版本化（细节以 26ai 文档为准 ⚠️）；闪回事务（Flashback Transaction）让"找谁改了这行"从考古变查询。
- **Undo 侧** ⚠️：undo 表空间自动扩展 + UNDO 保留顾问化；**闪回数据归档（FDA）**与长保留把 01555 的"读一致性预算"产品化为可配置的保留策略。
- **工业实践**：OLTP 反模式清单今天仍成立——短事务、幂等重试、避免热点行（事件溯源/分片计数替代）、外键建索引；SQLite 类比给出的"回滚不免费"结论在 MVCC 家族（PG/MySQL）同型：WAL/undo 生成量都是硬账（跨引擎互见 [../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md) undo 线、[../PostgreSQL_10_High_Performance_3e/00-总览与阅读地图.md](../PostgreSQL_10_High_Performance_3e/00-总览与阅读地图.md)）。
