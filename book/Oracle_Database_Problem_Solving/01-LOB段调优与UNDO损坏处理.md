# 第 1–2 章：LOB 段性能的诊断与调优 · 处理 UNDO 表空间损坏

> ⚠️ 文档转述（章题取自中译本逐字目录 ✅，章内小节为本目录按主题自拟 ⚠️，Oracle 不可本机实测，无一条 Oracle 🔧）。本文件的 🔧 实验是 SQLite 类比，明确标注**非 Oracle 行为**。

## 本文件定位

原书前两章都落在"存储对象出毛病"这一层：第 1 章是**性能型**故障（LOB 段访问慢、高水位膨胀、空间不回吐），第 2 章是**损坏型**故障（UNDO 表空间坏了，实例起不来或事务悬挂）。两章合起来示范本书体例：先认症状（等待事件/报错号），再进诊断视图，最后给处置与预防。

## 第 1 章 LOB段性能的诊断与调优

### 1.1 症状面（⚠️ 转述）

- 含大字段（CLOB/BLOB/NCLOB）的表查询、插入、更新显著变慢；应用报 `ORA-22924`（快照过期的 LOB 版本）或 `ORA-01555 snapshot too old`。
- AWR 里 `buffer busy waits`、`read by other session` 集中出现在 LOBSEGMENT/LOBINDEX 对象上；`db file sequential read` 次数异常放大（LOB chunk 链式读取）。
- `dba_lobs` 指向的段实际块数远大于理论占用——高水位不降，全表扫 LOB 段成本虚高。

### 1.2 诊断路径（⚠️ 转述，11gR2–12cR1 口径）

1. 确认存储形态：BasicFiles LOB 还是 SecureFiles（`dba_lobs.retention` / securefile 列）。SecureFiles 支持压缩/去重/加密，行为差异大。
2. 定位热点块：`v$session_wait` 中 p1/p2 翻译出 file#/block#，对照 `dba_extents` 找到是 LOB 段头、chunk 还是 LOBINDEX 在争。
3. 空间账：`segment_high_water_mark` 对 `sum(dbms_lob.getlength)`，判断"垃圾占比"。
4. 读放大账：单次取 LOB 触发的 chunk 数（默认 chunk 8K），与 SQL trace 里的等待事件分布对齐。

### 1.3 处置与预防（⚠️ 转述）

- 迁移到 SecureFiles（`ALTER TABLE ... MOVE LOB(...) STORE AS SECUREFILE`），按需开 COMPRESSION/DEDUPLICATE；12c 起 SecureFiles 为默认。
- 空间回吐：`ALTER TABLE ... MODIFY LOB (...) (RETENTION ...)` 调 UNDO 依赖窗口；配合分区做生命周期管理（老分区整段 DROP 是"大 LOB 库"最省事的回收手段，与第 7 章衔接）。
- 读写模式：不要把 LOB 列混进高频窄查询的 SELECT 列表；用 DBMS_LOB 按 offset/amount 分段读写（对应下面 🔧G4 演示的"整取 vs 增量读"差异）。
- 应用侧：LOB 定位器（locator）与旧值拷贝的语义要一致，长事务读 LOB 是 ORA-01555/22924 的常见根因（UNDO 保留与第 2 章问题同源，可互相触发）。

## 第 2 章 处理UNDO表空间损坏

### 2.1 症状面（⚠️ 转述）

- 实例启动挂在 `SMON` 回滚阶段，告警日志出现 `ORA-00600/ORA-00607` 带 undo 相关参数，或 `ORA-01595`（freelist 扩展失败）、`ORA-00120`（UNDO 表空间缺省）类报错。
- 某 UNDO 数据文件介质损坏：`ORA-01110/ORA-01173`；未提交事务的回滚记录不可读，会话报 `ORA-00600 [2663]` 一类。

### 2.2 诊断路径（⚠️ 转述）

1. 先分性质：**文件级损坏**（能 RMAN 恢复，转第 8 章）还是**内容级损坏**（文件在、回滚段坏）。
2. `v$undo_extents`/`v$rollname`/告警日志三角定位受损回滚段；`o2overs`/BBED 类工具读块头确认（⚠️ 内部工具，社区口径）。
3. 判断受影响事务是否仍在回滚：`v$fast_start_transactions`。

### 2.3 处置阶梯（⚠️ 转述，风险自高而低逐级尝试）

- 正规路径：文件级损坏走 `RMAN restore/recover`（第 8 章），UNDO 表空间可即时替换：新建 undo tbs → `ALTER SYSTEM SET undo_tablespace=...` → 旧的 DROP。
- 内容级损坏的隔离：参数 `_offline_rollback_segments`/`_corrupted_rollback_segments` 列出坏段名，让实例跳过其回滚——**代价是坏段上未提交事务的数据一致性由人工兜底**，官方仅支持在 Oracle 指导下使用。
- 极端路径：切换 `_smu_debug_mode` 调试语义、或 allow_resetlogs 式不完全恢复（会丢该事务的未提交改动的"另一半"），属于最后一档。
- 预防：undo_retention 与 `maxsize` 自动扩展、闪回区容量核对（与第 7 章大库口径一致）；长批处理改分段提交，别把 UNDO 当工作区。

### 2.4 两章的共同教训

LOB 与 UNDO 在 11g/12c 是**同一条读一致性链**的两端：读 LOB 靠 UNDO  reconstruct 旧版本（`read consistency for LOBs` ⚠️）。UNDO 保留窗口不够 → LOB 报 ORA-22924；UNDO 坏 → 一切依赖它的读路径连锁失效。排错时永远先看 UNDO 面（retention/使用率/坏段），再看对象面。

## 🔧 SQLite 类比实验（非 Oracle 行为；脚本 `D:\develops\tmp\dbwave_w7_oraps\exp.py`，Python 3.13 + SQLite 3.45.3）

### G2 · 内容级损坏的诊断输出（类比 2.2 的"块级确诊"）

构造 200 行表后，直接把文件页 2 的若干字节改写为 `0xFF`，再跑诊断 pragma：

```text
quick_check -> ['*** in database main *** | Tree 2 page 2 cell 8: Offset 65535 out of
range 2333..4092 | Tree 2 page 2 cell 7: Offset 65535 out of range ...',
'database disk image is malformed']
integrity_check -> 同上（诊断行 + 'database disk image is malformed'）
```

- 要点：**轻损坏时诊断命令"报告而非崩溃"**，逐条给出"树/页/槽位"坐标——这就是 Oracle 世界 `DBV`/`RMAN VALIDATE` 干的事；重损坏时同一命令直接抛 `SQLITE_CORRUPT`（本实验另一轮观察到）。"报告坐标 → 决定隔离还是恢复"的分诊逻辑与 2.2 完全同构。

### G4 · LOB 整行取 vs 增量读（类比 1.3 的 DBMS_LOB 分段读）

对 2MB BLOB 列分别整行 SELECT 与增量 `blobopen().read(1MB)`：

```text
full row fetch len=2097152 ms=1.4
incremental blobread 1MB len=1048576 ms=0.5
page_size*page_count -> 2105344
```

- 只取一半字节，耗时减半量级——"按 chunk 取"的收益在任何引擎都是真的；Oracle 的差异在于 chunk 链式寻址带来的**多次单块读**（⚠️ 转述），所以收益比 SQLite 更悬殊。

## 症状 → 动作速查表

| 症状 | 第一动作 | 章节 |
|---|---|---|
| LOB 表查询慢 + buffer busy waits | p1/p2 翻译定位 LOB 段头/LOBINDEX 热点块 | Ch.1 |
| LOB 段高水位虚高 | 分区 DROP 或 MOVE + SecureFiles 迁移 | Ch.1 |
| 读 LOB 报 ORA-22924 | 查 undo_retention 与长事务 | Ch.1/2 |
| 实例卡在启动回滚 | 告警日志 + v$fast_start_transactions 分诊 | Ch.2 |
| UNDO 文件介质损坏 | 走 RMAN（转 Ch.8），换 undo 表空间 | Ch.2/8 |
| 坏回滚段隔离 | _corrupted_rollback_segments（需 Oracle 指导） | Ch.2 |

## 关联阅读

- 机制原理（undo/读一致性为什么这样设计）：[../Oracle编程艺术：深入理解数据库体系结构（第3版）.md](../Oracle编程艺术：深入理解数据库体系结构（第3版）.md)
- 恢复章全文：[04-RMAN备份恢复最佳实践.md](04-RMAN备份恢复最佳实践.md)；大库分区回收：[03-DDL优化与大型数据库.md](03-DDL优化与大型数据库.md)
- 等待事件面方法论对照：[../Troubleshooting_Oracle_Performance_2e/00-总览与阅读地图.md](../Troubleshooting_Oracle_Performance_2e/00-总览与阅读地图.md)

## 自测题

1. 为什么"垃圾占比"要用高水位对 `getlength` 总和来算？
2. BasicFiles 与 SecureFiles 在排错上最先影响哪一步判断？
3. ORA-22924 与 ORA-01555 的因果链里，共享的那个资源是什么？
4. 分诊"文件级损坏 vs 内容级损坏"各走哪条处置线？
5. `_corrupted_rollback_segments` 的代价是什么，为什么只能官方指导下用？
6. 🔧G2 里"报告坐标"与"直接抛错"两种损坏形态各对应 Oracle 处置阶梯的哪一档？

## 核心概念速览（中英对照）

- **大对象段** — LOB Segment：大字段独立存储段，含段头/chunk/LOBINDEX 三类争用点
- **安全文件** — SecureFiles：11g+ 的 LOB 新存储形态，支持压缩/去重/加密
- **基本文件** — BasicFiles：老式 LOB 存储，chunk 链式寻址
- **高水位膨胀** — HWM Bloat：删除不回吐导致扫描成本虚高
- **定位器** — LOB Locator：指向 LOB 值的指针，读写语义有别于普通列
- **回滚段** — Rollback/Undo Segment：读一致性与事务回滚双职责的载体
- **快照过期** — Snapshot Too Old (ORA-01555)：UNDO 覆盖导致一致性读失败
- **LOB 版本过期** — ORA-22924：读 LOB 旧版本时 UNDO 已不可用
- **坏段隔离** — Corrupted Rollback Segment Isolation：用隐含参数跳过坏回滚段
- **快速回滚监控** — V$FAST_START_TRANSACTIONS：判断实例卡在回滚的对象面
- **块校验** — Block Validation (DBV/RMAN VALIDATE)：内容级损坏的坐标化确诊 ⚠️
- **介质损坏** — Media Failure：文件不可读级故障，走备份恢复线

## 最新演进与工业实践

- **SecureFiles 全面默认**：12c 起 LOB 默认 SecureFiles；23ai/19c 文档口径下 BasicFiles 已进入维护语义（官方文档 Database SecureFiles 存储指南，https://docs.oracle.com/en/database/oracle/oracle-database/ 系列 ✅ 域名可达，具体页面未直读 ⚠️）。
- **JSON 取代一半 LOB 场景**：23ai 的 JSON 关系视图/原生 JSON 类型把"文档进数据库"的主流载体从 BLOB+CLOB 迁到类型化列，传统 LOB 段调优问题面收窄 ⚠️ 转述。
- **UNDO 治理自动化**：RMAN VALIDATE、V$DIAG_ALERT_EXTEND（ADR 体系）把 2.2 的分诊做成可查询事件流；自动 UNDO 调优（undo_retention guarantee 结合闪回保留）是 19c+ 常见基线 ⚠️ 转述。
- **跨引擎镜像**：SQLite 的 `PRAGMA integrity_check` 已成为工业界"内容级损坏坐标化报告"的标准范式（SQLite FAQ 官方文档 ✅）；本书 2015-18 年用 DBV 手工做的事，现在各引擎普遍有 SQL 级一键体检。
