# 第 8 章：RMAN 备份恢复最佳实践

> ⚠️ 文档转述（章题取自中译本逐字目录 ✅，章内小节自拟 ⚠️；Oracle/RMAN 行为均为 11gR2–12cR1 口径转述，无 Oracle 实测）。本章 🔧 组为 SQLite backup API + WAL checkpoint 类比，**非 Oracle/RMAN 行为**。

## 本章定位

第 8 章是全书"能不能活下来"的底牌章：前面 1–7 章的所有高危操作（NOLOGGING、坏段隔离、MOVE）都默认这里的安全网存在；后面迁移章（13–14）也复用它的数据搬移原语（增量前滚）。

## 8.1 备份架构决策（⚠️ 转述）

- **备份策略三参数**：保留策略（RECOVERY WINDOW vs REDUNDANCY）、是否开归档、是否用快速恢复区（FRA）。最佳实践口径：生产=归档模式+FRA+保留窗口 7–30 天起步。
- **增量分级**：L0（基线）+L1 差异/累积滚动；累积 L1 越大越慢是误解——10g 起用块变更跟踪（Block Change Tracking）后，L1 只读变更位图，TB 库窗口从小时级压到分钟级。
- **压缩/多路/并行**：`BACKUP AS COMPRESSED BACKUPSET` + `SECTION SIZE` 分段并行（对应 SBT 磁带或多通道磁盘）；控制文件自动备份 `CONFIGURE CONTROLFILE AUTOBACKUP ON` 是"最后一条命"。

## 8.2 恢复矩阵与诊断（⚠️ 转述）

| 故障形态 | 恢复路径 | 关键点 |
|---|---|---|
| 数据文件丢失、归档连续 | RESTORE+RECOVER 全自动 | RMAN 按 SCN 自决所需归档，无需人工指定 |
| 归档缺口 | 不完全恢复到 RESETLOGS 点 | 立刻重开 L0：incarnation 分裂的坑 |
| UNDO 文件级损坏 | 换 undo 表空间或介质恢复 | 回看第 2 章分诊 |
| 控制文件全毁 | AUTOBACKUP 重建+catalog 同步 | 无 autobackup 时手工恢复最脆 |
| 库整体要搬 | DUPLICATE FOR RECOVERY / TRANSPORT TABLESPACE | 与第 14 章快速迁移同源 |

- 验证常态化：`RESTORE ... VALIDATE`、`BACKUP ... VALIDATE`、`LIST BACKUP SUMMARY` 三件套；"从未验证的备份=没有备份"是本章第一军规。
- 交叉检查卫生：`CROSSCHECK` 与 `DELETE EXPIRED/OBSOLETE` 的误用会把可用备份标掉——变更存储布局（NFS→ASM→云）时尤其小心 ⚠️。

## 8.3 与第 6/7 章的协议（⚠️ 转述）

1. NOLOGGING 变更 → 紧随其后的对象级备份（否则 ORA-01578 出现在"以为有备份"的文件上——第 2 章的 DBV 确诊在此复用）。
2. 大库窗口不够 → 增量滚动（周一 L0、每日累积 L1）+ 归档压缩；闪回保证区（guarantee）单列为"人为错误"防线，不算备份替代。
3. 统计/DDL 变更的"逻辑回退"靠导出统计+SPM 基线快照；RMAN 只能回"物理"，这一课在每次误 DROP 时重讲。

## 8.4 目录与保留细节（⚠️ 转述）

- Catalog DB vs 仅控制文件自动备份：目录端才谈得上持久脚本、stored script、跨检查报表；无 catalog 的小库路线可用，但大库账本（谁覆盖了谁）会糊。
- 保留策略只决定"什么时候可以删"，`DELETE OBSOLETE` 仍需排班执行——FRA 撑满引发的"备份自困"是最常见事故形态。
- 归档删除策略 `CONFIGURE ARCHIVELOG DELETION POLICY TO BACKED UP 2 TIMES TO DEVICE TYPE SBT`：不配就等于"归档无限堆积直到把写路径憋死"。
- 备份窗口与 L0 日历：周一 L0、周二至周日累积 L1 的滚动表要与统计收集/DBMS_SCHEDULER 任务错峰（第 7 章窗口重算清单）。

## 8.5 案例演练：介质故障当夜的恢复时序（⚠️ 按章主题结构化）

1. 症状：打开库报 ORA-01157/01110，`v$recover_file` 点名文件号——先确认是单文件而非磁盘组整体（后者走第 11 章）。
2. 定性：归档连续性预判——`RESTORE` 前用 `LIST BACKUP OF DATAFILE n` 看最近 L0/L1 链与归档覆盖点。
3. 执行：`RESTORE DATAFILE 7; RECOVER DATAFILE 7;`；大文件加并行、需要改位置时 SET NEWNAME+SWITCH。
4. 决策点：若归档缺口补不上→评估不完全恢复+RESETLOGS 的后果，**当场重开 L0**（8.2 矩阵第二行）。
5. 善后：表空间 ONLINE；告警与 alert 日志归档留存；故障盘按 ASM failure group 记录换盘工单。
6. 复盘：把恢复用时与"备份可读性证明"（RESTORE VALIDATE 排班是否存在空窗）写进复盘——复盘产出就是下一版验证排班。

## 8.6 常见误区（⚠️ 社区口径）

- "FRA 自动管理=备份不用管"——删除策略未配时，自动管理只会"自动把空间耗光"。
- "压缩备份拖窗口"——CPU 换 IO 在多数盘上净赚；只有 CPU-bound 库才先亏。
- "验证一次就够"——L0/L1/归档三类产物都要覆盖进周期抽样验证。
- "autobackup 有控制文件就够了"——无 catalog 时 RMAN 元数据依赖它，删改前想清楚账本在哪。

## 🔧 实验 G6 · 在线一致性备份与 checkpoint 语义（非 Oracle；Python 3.13 / SQLite 3.45.3）

```text
### G6 online backup / migration (Data Pump / RMAN analogy vs backup API + WAL checkpoint)
journal_mode -> wal
backup steps=1, last=(101, 0, 11)
backup rows -> 5000 | integrity -> ok
wal_checkpoint(TRUNCATE) -> [(0, 0, 0)]
wal_checkpoint return (busy,log,checkpointed): [(0, 0, 0)]
```

- 方法：WAL 模式下写入 5000 行，边有事务活动边用 `Connection.backup()` 在线复制到目标库（progress 回调报 11 页步数、结束时 remaining=0），对副本 `integrity_check` 通过。
- 对照 RMAN：backup API 的"页步进+最终一致"对应 backupset 的 SCN 对齐；`wal_checkpoint(TRUNCATE)` 返回 `(busy, log, checkpointed)=(0,0,0)` 对应"归档已可截断/应用位点已前移"的干净状态。**备份的目标态永远用一次独立校验来证明**（这里是 integrity_check，RMAN 里是 VALIDATE）——同一纪律，两个引擎。

## 8.7 常用命令骨架（⚠️ 通用形态示意，非原书清单）

```text
CONFIGURE CONTROLFILE AUTOBACKUP ON;
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 14 DAYS;
CONFIGURE ARCHIVELOG DELETION POLICY TO BACKED UP 2 TIMES;
BACKUP INCREMENTAL LEVEL 0 FOR RECOVER OF COPY ... TAG 'L0_W1';
BACKUP AS COMPRESSED BACKUPSET DATABASE PLUS ARCHIVELOG;
RESTORE DATABASE VALIDATE;            -- 验证排班入口
CROSSCHECK BACKUP OF DATABASE;        -- 先对账再谈删除
LIST BACKUP SUMMARY;
```

## 症状 → 动作速查表

| 症状 | 第一动作 | 关联 |
|---|---|---|
| ORA-01157/01110 打开库缺文件 | 先 RESTORE 该文件再 RECOVER，勿动 RESETLOGS | 8.2 |
| 恢复报缺归档、链断了 | 评估不完全恢复+重开 L0 | 8.2 |
| L1 增量慢 | 开块变更跟踪；检查位图文件在 ASM | 8.1 |
| LIST EXPIRED 一片 | CROSSCHECK 先分清"物理在否"再删 | 8.2 |
| NOLOGGING 后报坏块 | 该对象立即重备份；DBV 定位坏块 | 8.3/Ch.2 |
| 想证明备份可用 | RESTORE VALIDATE 排班进周任务 | 8.2 |

## 自测题

1. RECOVERY WINDOW 与 REDUNDANCY 两种保留策略各自的适用场景？
2. 块变更跟踪为什么能把 L1 变成"读位图"？没有它时 L1 在做什么？
3. 控制文件自动备份为什么被称为"最后一条命"？
4. NOLOGGING 与备份协议的两条规则是什么？违反后症状出现在何时？
5. incarnation/RESETLOGS 之后必须做什么，否则下次全库恢复会踩什么坑？
6. 🔧G6 里 backup 完成后为什么还要对副本跑 integrity_check？对应 RMAN 的哪个命令？
7. 案例演练第 4 步：为什么 RESETLOGS 之后必须立刻重开 L0？不重开会在下次恢复时踩什么坑？
8. 归档删除策略 BACKED UP n TIMES 保护的是哪条链？它和保留策略的分工是什么？

## 核心概念速览（中英对照）

- **归档模式** — ARCHIVELOG：REDO 归档保留，支持在线备份与时间点恢复（PITR） ⚠️
- **备份集** — Backup Set：RMAN 专有打包格式，支持压缩/多路复用 ⚠️
- **图片副本** — Image Copy：文件级 1:1 副本，可 SWITCH 秒用 ⚠️
- **增量 L0/L1** — Incremental Levels：基线与差异/累积层 ⚠️
- **块变更跟踪** — Block Change Tracking：位图化加速增量 ⚠️
- **保留策略** — Retention Policy：窗口式或冗余式过期判定 ⚠️
- **快速恢复区** — FRA：备份+归档+闪回统一存储配额面 ⚠️
- **闪回保证区** — Flashback Guarantee：长期闪回保留，防逻辑错 ⚠️
- **验证备份** — VALIDATE：不还原证明可读（RESTORE/BACKUP VALIDATE） ⚠️
- **交叉检查** — Crosscheck：目录与物理介质对账 ⚠️
- **INCARNATION** — Database Incarnation：RESETLOGS 造成的时间线分支 ⚠️
- **在线页步进备份** — Online Page-Step Backup：🔧 SQLite backup() 的逐步一致复制（非 Oracle）

## 最新演进与工业实践

- **19c 口径**：FRA/归档压缩、备份加密（`SET ENCRYPTION` 与密钥管理集成 KMS 化）、SBT 云直连（ZDK/OSS 类）为标配；RMAN 仍是 23ai 文档推荐的主备份面（docs.oracle.com Database Backup and Recovery Reference ✅ 域名可达，页内容未直读 ⚠️）。
- **Dbum 社区工程**：RMAN 编排脚本生态（DBA 社区）延续本章"滚动 L0+验证排班"思路自动化；跨平台迁移仍以 RMAN CONVERT/传输表空间为主脊（衔接第 14 章）。
- **备份即演练**：2020s 工业界将"自动化恢复演练"纳入安全合规（如不可变存储+定期全链路恢复测试），本章 8.2 的"从未验证=没有备份"成为通用 SRE 规则，与云厂商 DB 备份的 PITR 演练同构 ⚠️ 转述。
- **跨引擎镜像**：PostgreSQL 的 `pg_basebackup`+WAL 归档、MySQL 的 XtraBackup、SQLite 的 🔧G6——"在线页步进+日志重放达成一致"的备份数学完全一致，只是目录/编目层各有系统表（⚠️ 各家文档口径）。
