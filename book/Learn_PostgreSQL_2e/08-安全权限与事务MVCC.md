# 08 · 安全权限与事务、MVCC、WAL（原书第 10–11 章合并）

> 对应原书 Ch10 *Users, Roles and Database Security* + Ch11 *Transactions, MVCC, WALs and Checkpoints*（✅ 章题；两章同归"服务器内核治理"档，映射见 00）。
> 实证 ✅：docker `chapter_10/init/002-create-tablespaces.sh`（安全章含表空间演示）。
> 本章是全书技术脊柱：权限模型 + 事务语义 + WAL 机制三线并置。

## 1. 权限矩阵：对象 ACL 到行级安全（Ch10 ⚠️+✅）

- 三层防线（书的心智模型 ⚠️）：
  1. **连接层**：pg_hba——见 [02-用户与连接管理.md](02-用户与连接管理.md)；
  2. **库/对象层 ACL**：`GRANT/REVOKE` 矩阵（✅ https://www.postgresql.org/docs/current/sql-grant.html ）；
  3. **行层 RLS**：`CREATE POLICY`+`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`（✅ https://www.postgresql.org/docs/current/ddl-rowsecurity.html ）——多租户的库内正解。
- 默认公地陷阱 ⚠️+✅：`public` schema 历史上人人可建表；**PG 15 起默认收回创建权**（release 15 口径；中文社区译文佐证如 modb 转载《PostgreSQL 15: public schema权限的变化》）——本书 16 基线已在新默认下行文。
- 预置角色族 ⚠️+✅（docs 预定义角色页，族 ⚠️）：`pg_read_all_stats`、`pg_monitor` 等"岗位角色"——审计/监控授权不再发超管。
- 表空间（✅ 代码实证）：`CREATE TABLESPACE` 需超管+OS 目录属主双闸（⚠️+✅ sql-createtabletablespace 族）。
- 对象属主与 `ALTER ... OWNER TO`：与 SECURITY DEFINER 联动（[06 号文件](06-服务端编程_PLPGSQL.md)）。

## 2. 事务与隔离级别（Ch11 上半 ⚠️+✅）

- PG 三档实现（✅ https://www.postgresql.org/docs/current/mvcc.html ）：
  - **Read Committed（默认）**：每语句新快照；
  - **Repeatable Read**：语句批次级快照=快照隔离，冲突报 `could not serialize access due to concurrent update`；
  - **Serializable**：SSI 谓词/写依赖环检测，报 `serialization_failure` ⇒ **应用必须带重试**（✅ 同页 Serializable 节）。
- 无 Read Uncommitted：映射为 RC ⚠️+✅。
- 写偏斜（write skew）为 RC 不可防、RR/SSI 才防的经典例（社区标准案例 ⚠️）。
- 事务包裹纪律 ⚠️+✅：
  - `VACUUM`/`CREATE INDEX CONCURRENTLY`/`DROP DATABASE ... (PG 13+ 可带进度)` 等**不可进事务块**（✅ https://www.postgresql.org/docs/current/sql-vacuum.html ）；
  - `PREPARE TRANSACTION` 两阶段提交存在但生态罕用 ⚠️。
- 长事务三害：膨胀（死元组堆积）、槽锁 WAL、vacuum 停滞——Ch11→Ch13/16 的因果链 ⚠️+✅（routine-vacuuming https://www.postgresql.org/docs/current/routine-vacuuming.html ）。

## 3. MVCC 物理面：xmin/xmax 与膨胀（⚠️+✅）

- 行头三元组 `xmin/xmax/cid` 决定可见性（✅ https://www.postgresql.org/docs/current/storage-page-layout.html ）；
- UPDATE=插新行+标旧行 xmax ⇒ **死元组** ⇒ VACUUM/autovacuum 回收、`freeze` 防 32 位 XID 回卷（✅ sql-vacuum/routine-vacuuming）；
- HOT update（页内链）与 fillfactor 是膨胀调节阀 ⚠️+✅；
- 观测：`pg_stat_user_tables.n_dead_tup/last_autovacuum`（✅ https://www.postgresql.org/docs/current/monitoring-stats.html ）→ [11-日志备份与监控.md](11-日志备份与监控.md)。

## 4. WAL、检查点与归档（⚠️+✅）

- WAL 三职责：**崩溃恢复 / 复制 / PITR**（✅ https://www.postgresql.org/docs/current/wal-internals.html ）；
- `wal_level=replica` 为默认（✅ 官方勘误订正书中 p610 "mininal" 误说——见 00 勘误清单第 5 条）；升到 `logical` 才有解码（→ [12-物理复制与逻辑复制.md](12-物理复制与逻辑复制.md)）。
- 检查点=脏页批量刷盘+恢复起点前移：`checkpoint_timeout`/`max_wal_size` 定节奏，`log_checkpoints` 定观测（⚠️+✅ https://www.postgresql.org/docs/current/runtime-config-wal.html ）。
- 低层热备 API：`pg_backup_start()/pg_backup_stop()`（旧名 pg_start/stop_backup）+ 归档 `archive_mode=on` ⇒ PITR（✅ https://www.postgresql.org/docs/current/continuous-archiving.html 、backup-dump https://www.postgresql.org/docs/current/backup-dump.html ）。

## 5. 🔧 类比实测 A：checkpoint 同词三义（sq1.out / duck.out 🔧）

```text
SQLite 3.50.6:  PRAGMA journal_mode=WAL;            -> 'wal'
                PRAGMA wal_checkpoint(TRUNCATE);    -> 0|0|0  (busy,log,checkpointed)
                # 语义：把 WAL 内容折回主库文件并截边文件
DuckDB 1.5.5:   CHECKPOINT                           -> 语句执行通过（WAL 回灌主文件）
PostgreSQL:     CHECKPOINT                           -> 全库脏页刷盘+恢复点前移
                # WAL 段不因此删除：归档/复制按 retention 自主回收 ⚠️+✅
```

- 前两行为本机实测（**非 PostgreSQL 行为**）；PG 行以 runtime-config-wal/wal-internals 文档为据 ⚠️+✅；
- 概念对位：嵌入式"checkpoint≈合并日志回主文件"，PG"checkpoint≈一致性快照推进"——词义迁移是 DBA 新人第一坑；管理册参数语境对位 [../PostgreSQL_10_High_Performance_3e/06-配置参数语境与生效方式.md](../PostgreSQL_10_High_Performance_3e/06-配置参数语境与生效方式.md)。

## 6. 🔧 类比实测 B：物化视图——只有服务器引擎才有的"手动刷新对象"（sq3.out / duck.out 🔧）

```text
SQLite 3.50.6:  CREATE MATERIALIZED VIEW mv AS SELECT 1 x;
                Parse error: near "MATERIALIZED": syntax error
DuckDB 1.5.5:   同语句 -> Parser Error: syntax error at or near "MATERIALIZED"
```

- 两家只有普通视图（每次展开重算）；PG 的 MV 是**存储对象**：
  - `REFRESH MATERIALIZED VIEW` 全量重灌 / `CONCURRENTLY` 增量差量（需唯一索引；走 MVCC 不外泄中间态）✅ https://www.postgresql.org/docs/current/sql-creatematerializedview.html ；
  - 刷新产生 WAL/膨胀——本章 Ch11 知识的应用题 ⚠️。
- 替代姿势 ⚠️：SQLite=汇总表+触发器（[07 号文件](07-触发器规则与分区.md)第 5 节已实测触发器 🔧）；DuckDB=CTAS/ATTACH 增量。
- freshness vs 一致性的三角权衡三表达（**非 PostgreSQL 行为**）。

## 7. 与其他册分工

- 权限/RLS 配方：[../PostgreSQL_16_Administration_Cookbook/03-安全与权限.md](../PostgreSQL_16_Administration_Cookbook/03-安全与权限.md)；并发/膨胀运维：[../PostgreSQL_16_Administration_Cookbook/05-性能与并发.md](../PostgreSQL_16_Administration_Cookbook/05-性能与并发.md)。
- MVCC/VACUUM 性能纵深：[../PostgreSQL_10_High_Performance_3e/07-MVCC与Vacuum与表膨胀.md](../PostgreSQL_10_High_Performance_3e/07-MVCC与Vacuum与表膨胀.md)；存储结构内幕：[../Mastering_PostgreSQL_Administration/03-物理存储结构.md](../Mastering_PostgreSQL_Administration/03-物理存储结构.md)。
- 中文内核视角：[../PostgreSQL数据库内核分析.md](../PostgreSQL数据库内核分析.md)；事务理论后台：[../事务处理原理.md](../事务处理原理.md)、[../事务处理概念与技术.md](../事务处理概念与技术.md)（盘上实名 ✅）。
- 承上启下：扩展补安全（pgAudit）→ [09-扩展生态.md](09-扩展生态.md) 与 [11-日志备份与监控.md](11-日志备份与监控.md)。

## 8. 本章自测（重构版；题目自拟 ⚠️）

1. **问**：PG 支持四种标准隔离级别吗？**答**：只三档（RU 映射为 RC）。
2. **问**：RR 下更新冲突怎么办？**答**：`could not serialize...` 中止当前事务，重试该事务（RC 只中止语句）⚠️。
3. **问**：为什么 autovacuum 停摆后 WAL 可能暴涨？**答**：老快照钉住行/或叠加失活槽 ⚠️。
4. **问**：REFRESH ... CONCURRENTLY 的前提？**答**：唯一索引+非空（✅ 文档）。
5. **问**：wal_level 默认值？**答**：replica（✅ 官方勘误口径）。

## 9. 行级安全（RLS）实战模式（⚠️+✅）

- **启用骨架**（✅ https://www.postgresql.org/docs/current/ddl-rowsecurity.html ）：

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.tenant_id')::int);
-- 属主默认豁免 RLS——应用角色需显式受约束
ALTER TABLE orders FORCE ROW LEVEL SECURITY FOR app_user;
```

- **两方向策略** ⚠️+✅：`USING`（读过滤）与 `WITH CHECK`（写校验）可分别定义——读可见行 ≠ 可写行。
- **性能注意** ⚠️：RLS 谓词在每行上求值——复杂表达式会拖慢全表扫描；保持谓词简单+索引友好。
- **排障**：`SET row_security = off;`（超管默认 off ⚠️）可临时关闭以便调试；`pg_policies` 视图查看当前策略 ✅。
- 🔧 对照：SQLite/DuckDB 均无 RLS 等价物（🔧 非 PostgreSQL 行为）——多租户隔离在嵌入式引擎只能靠应用层 WHERE 或视图。

## 10. 死锁与锁监控（⚠️+✅）

- **锁模式速查**（✅ https://www.postgresql.org/docs/current/explicit-locking.html ）：
  - `AccessShareLock`（SELECT）/ `RowShareLock`（SELECT FOR UPDATE）/ `RowExclusiveLock`（INSERT/UPDATE/DELETE）/ `ShareLock`（CREATE INDEX）/ `AccessExclusiveLock`（ALTER TABLE/DROP）；
  - 冲突矩阵：轻锁互不阻塞、重锁阻塞轻锁——`AccessExclusiveLock` 阻塞一切 ⚠️。
- **死锁检测** ⚠️+✅：`deadlock_timeout`（默认 1s）到期后检测环依赖，牺牲一个事务报 `deadlock detected`。
- **观测**（✅ monitoring-stats 页）：

```sql
SELECT pid, mode, granted, waitstart, query
FROM pg_locks l JOIN pg_stat_activity a USING (pid)
WHERE NOT granted;   -- 正在等待锁的会话
```

- **缓解** ⚠️：保持事务短小、统一加锁顺序（按表名/主键排序获取锁）、`LOCK TABLE ... IN ... MODE` 显式声明意图。

## 核心概念速览（中英对照）

1. **ACL** — 访问控制列表：GRANT/REVOKE 的账本。
2. **RLS** — 行级安全：POLICY+角色作用域。
3. **预定义角色** — predefined roles：pg_monitor 岗位模板 ⚠️+✅。
4. **表空间** — tablespace：逻辑→OS 路径映射，双闸权限 ✅ 实证。
5. **隔离级别** — isolation levels：RC/RR/Serializable。
6. **快照隔离** — snapshot isolation：RR 的语句级一致读。
7. **SSI** — 可串行化快照隔离：serialization_failure 重试契约。
8. **死元组** — dead tuple：MVCC 版本残留。
9. **冻结** — freeze：XID 回卷防御。
10. **WAL** — 预写日志：恢复/复制/PITR 三位一体（默认 replica ✅ 勘误）。
11. **检查点** — checkpoint：刷脏+推进恢复起点（🔧 三引擎词义辨析）。
12. **PITR** — 时间点恢复：basebackup+归档重放。
13. **物化视图** — materialized view：手动 REFRESH 的存储查询（🔧 否证对照）。

## 最新演进与工业实践

- **PG 15 安全分水岭**：public schema 默认收权（✅ release-15 族 https://www.postgresql.org/docs/current/release-15.html 未单验 ⚠️；中文社区广泛译文佐证）——读旧教程必对齐此线。
- **PG 17/18**（✅ https://www.postgresql.org/docs/release/17.0/ 、https://www.postgresql.org/docs/release/18.0/ ）：17 权限收紧的延续（如 ALTER TABLE SET STATISTICS 需属主/权限 ⚠️）、vacuum 改进；18 **OAuth 认证**、异步 I/O 重塑 WAL 刷写与 checkpoint 行为——本章参数经验值到 18 需重估 ⚠️。
- **审计合规** ⚠️：pgAudit（外部扩展，核心无此页——docs/current/pgaudit.html 实测 404 已登记）承担语句级审计；云托管的 log 管道直达 SIEM。
- **多租户工程**：RLS+连接会话 `SET app.tenant_id` 组合是 Supabase 等平台的设计底座 ⚠️——本书 Ch10 知识点的 2020s 工业放大版。
- **文档锚点**（✅ 全部 200 已验）：mvcc / wal-internals / runtime-config-wal / continuous-archiving / sql-grant / ddl-rowsecurity / sql-creatematerializedview / monitoring-stats。
