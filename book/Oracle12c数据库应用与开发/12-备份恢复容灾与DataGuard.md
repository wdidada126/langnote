# 12 · 备份恢复、容灾与 Data Guard

> **本章地图**：**备份策略的三种组合**（RMAN full + archivelog / 增量 / 归档 + 闪回）→ **RMAN 的核心命令**（`BACKUP` / `RESTORE` / `RECOVER` / `LIST` / `REPORT`）→ **增量备份与块介质恢复（BMR）**→ **不完全恢复**（`UNTIL TIME` / `UNTIL SCN` / `UNTIL SEQUENCE`）→ **恢复目录（Recovery Catalog）**→ **Data Guard 的三种形态**（物理 standby / 逻辑 standby / 快照 standby）→ **日志应用方式**（Redo Apply vs SQL Apply）→ **Switchover 与 Failover**→ **延迟应用（Delay）与 Active Data Guard**→ **RAC / CDB 下的备份粒度**→ **容灾演练与运维纪律**。

## 一、核心精讲

> 以下 SQL/DDL 均为**教学示意，不参与构建**，不可也不必在真实实例上执行。

### 1.1 先想清楚：备份到底是为了回答什么问题

| 你想回答的问题 | 手段 |
| --- | --- |
| 硬盘坏了，数据文件丢了，要能恢复 | **物理备份（RMAN）+ 归档日志** |
| 用户误删了一张表 / 误改了数据 | **不完全恢复**（时间点恢复）或 **Flashback Table** |
| 想恢复**单个坏块** | **块介质恢复（BMR）**——只恢复那一个块，代价极小 |
| 需要"保留一年前的状态"以便合规审计 | **Flashback Data Archive（FDA）** |
| 主库挂了，要有备用 | **Data Guard** |
| 想"回到 5 分钟前" | **Flashback Database**（依赖 Flashback Log，且库不能 open 过） |

### 1.2 RMAN 核心命令（教学示意，不参与构建）

```bash
rman target /

# 0 级全备 + 归档 + 之后每天 1 级增量（经典策略，教学示意，不参与构建）
RMAN> BACKUP INCREMENTAL LEVEL 0 DATABASE PLUS ARCHIVELOG DELETE INPUT;
RMAN> BACKUP INCREMENTAL LEVEL 1 CUMULATIVE DATABASE PLUS ARCHIVELOG DELETE INPUT;

# 看备份里有什么
RMAN> LIST BACKUP SUMMARY;
RMAN> LIST ARCHIVELOG ALL;
RMAN> REPORT NEED BACKUP;
RMAN> REPORT SCHEMA;

# 恢复：先 restore 再 recover
RMAN> RESTORE DATABASE;
RMAN> RECOVER DATABASE;

# 时间点恢复（不完全恢复，必须之后 OPEN RESETLOGS）
RMAN> RUN {
  SET UNTIL TIME '2026-09-01 12:00:00';
  RESTORE DATABASE;
  RECOVER DATABASE;
  ALTER DATABASE OPEN RESETLOGS;
}
```

**RMAN 的三条设计哲学**（理解了就不容易出错）：

1. **RMAN 读控制文件（或恢复目录）来决定"备份里有什么"**，所以**控制文件本身也需要备份**（`CONFIGURE CONTROLFILE AUTOBACKUP ON`）——否则控制文件丢了，恢复就没了地图；
2. **归档日志是"增量恢复的燃料"**：没有归档，`RECOVER` 无从下手；
3. **`DELETE INPUT` 要小心**：它删的是已备份的归档，`FAILURE` 场景下容易造成归档缺失，建议搭配保留策略一起看（`CONFIGURE RETENTION POLICY`）。

```sql
-- 保留策略与自动备份（教学示意，不参与构建）
RMAN> CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 30 DAYS;
RMAN> CONFIGURE CONTROLFILE AUTOBACKUP ON;
RMAN> CONFIGURE BACKUP OPTIMIZATION ON;
```

### 1.3 块介质恢复（BMR）：最被低估的能力

- **场景**：`v$database_block_corruption` 里发现坏块，或 ORA-01578（块损坏）；
- **做法**：`BLOCKRECOVER DATAFILE 5 BLOCK 1234;`（RMAN 从最近的备份里取该块，再用归档恢复）；
- **代价**：**不恢复整个文件、不停机、不重建**，代价接近零；
- **前提**：必须开启 **块跟踪（block change tracking）** 才能让增量备份只读变化块（否则 RMAN 仍会读全量数据文件）——这是"增量备份很慢"最常见的解释。

```sql
-- 开启块跟踪（教学示意，不参与构建）
ALTER DATABASE ENABLE BLOCK CHANGE TRACKING
  USING FILE '/u01/oradata/ORCL/changetracking.f' REUSE;
```

### 1.4 Data Guard 的三种形态

| 形态 | 日志应用方式 | 能否读 | 用途 |
| --- | --- | --- | --- |
| **物理 standby（物理 DG）** | **Redo Apply**：物理复制块，**字节级一致** | `OPEN READ ONLY`（11g 起 **Active Data Guard** 可 `READ ONLY + APPLY` 同时） | 默认、最常用；介质恢复、备份可放备库 |
| **逻辑 standby（逻辑 DG）** | **SQL Apply**：把 redo 转成 SQL 在备库执行 | 可 `OPEN READ WRITE`（应用时 `READ ONLY` 限制） | 备库可跑报表；**对 DDL 与数据类型有要求** |
| **快照 standby（snapshot DG）** | **不应用**日志，可 `READ WRITE` | 可写 | **临时把备库当"生产沙箱"做升级前验证**（12c 起） |

**选择矩阵**：

```
                  要"几乎零数据丢失 + 快速切换"  → 物理 DG（ + Fast-Start Failover）
                  要"备库跑报表/写数据"           → 逻辑 DG 或快照 DG
                  要"最小停机升级"                 → 物理 DG → 逻辑 DG 的滚动升级（见下）
```

🔧 **一个仍然有效的实用技巧**（DBA 攻坚指南专门讲过）：**把物理 Data Guard 转成逻辑 Data Guard 来做滚动升级**——利用"备库可以转成逻辑备库、主备各自升级、再切换"的方式，把停机时间从"几小时"压到"分钟级"。这条路径在 12c/19c 仍然是标准升级手法之一。

### 1.5 Switchover 与 Failover

| 动作 | 方向 | 数据丢失 | 是否可逆回原主 |
| --- | --- | --- | --- |
| **Switchover** | 主 → 备，且**原主变成新备** | **无（或极少）** | ✅ 是（可来回切） |
| **Failover** | 主挂 → 备接管 | **可能有丢失**（取决于 `sync`/`async` 与是否启用 FFO） | ❌ 通常需要重建 |

保护模式的权衡（这是容灾设计的核心选择题）：

| 保护模式 | 含义 | 代价 |
| --- | --- | --- |
| **Maximum Performance**（默认） | 主库提交不等备库确认 | 备库断了主库照跑，可能丢少量数据 |
| **Maximum Availability** | 优先可用性，同步但有超时降级 | 极端情况下退化为 Maximum Performance |
| **Maximum Protection** | 零数据丢失，主库必须等备库 | **备库不可用时主库会挂**（这是要接受的代价） |

```sql
-- 观察（教学示意，不参与构建）
SELECT database_role, open_mode, protection_mode, protection_level,
       standby_role, active_standby, switchover_status
FROM v$database;

-- 切主（教学示意，不参与构建；先切备，再切主）
-- 在备库： ALTER DATABASE COMMIT TO SWITCHOVER TO PHYSICAL STANDBY;
-- 在旧主： ALTER DATABASE COMMIT TO SWITCHOVER TO PRIMARY;
```

> **`Maximum Protection` 下"主库随备库一起挂掉"是最反直觉也最需要提前说清的一条**：它不是 bug，是设计。很多容灾方案在这里翻车，因为业务方以为"同步复制 = 主库永远活着"。

### 1.6 延迟应用（Delay）与 CDC 的一致性读

- **`DELAY`**：创建 standby 日志应用时可以设延迟（如 3600 秒），给"误操作"留一个回滚窗口；
- **逻辑 standby 的 `SKIP` 规则**：可以跳过某些 schema/表的日志应用（把备库用作"部分数据的报表库"）；
- **`Active Data Guard`（11g 起）**：备库在 `READ ONLY` 状态下**继续应用 redo**，可在备库跑报表/备份，代价是 **额外的 Active Data Guard 许可**——这是实施时最容易被忽略的成本项。

### 1.7 CDB / RAC 下的备份粒度

| 对象 | RMAN 语法粒度 |
| --- | --- |
| **整个 CDB** | `BACKUP DATABASE ROOT` + `BACKUP PLUGGABLE DATABASE ALL`（备份全部 PDB） |
| **单个 PDB** | `BACKUP PLUGGABLE DATABASE PDBSHOP;`——**12c 起支持，且只在 PDB 打开时可用** |
| **PDB 的表空间** | `BACKUP TABLESPACE ...` 需先 `ALTER SESSION SET CONTAINER` |
| **RAC** | 多节点并行 `BACKUP`（`CONFIGURE DEVICE TYPE DISK PARALLELISM 4`），并用 **catastrophic recovery area** 防止单节点丢失恢复数据 |

教学示意，不参与构建：

```sql
-- 只备份一个 PDB（教学示意，不参与构建）
RMAN> ALTER SESSION SET CONTAINER = PDBSHOP;
RMAN> BACKUP PLUGGABLE DATABASE PDBSHOP;

-- 备份 CDB 根 + 全部 PDB（教学示意，不参与构建）
RMAN> BACKUP DATABASE ROOT PLUGGABLE DATABASE ALL;
```

## 二、版本演进

| 版本 | 备份 / 容灾相关变化 |
| --- | --- |
| 10g | "**备份放到备库做**"成为最佳实践；`OMF`；ADM 引入 |
| 11g | **Active Data Guard**（备库可读 + 应用）、**Fast-Start Failover**、Backup on standby、ADR |
| 12.1 | 12.1.0.2 起 **deferred redo**（备库上的块恢复）、快照 standby、`RECOVER ... UNTIL` 增强 |
| 12.2 | **物理 DG → 逻辑 DG 的自动转换工具**更好用；多租户下的 DG 支持更完整 |
| 19c | **持续 PRC** 影响备库的重做行为；**Autonomous Recovery**；ADG 的延迟应用与聚合更快 |
| 23c | 自治运维；与云备份（Backup on OCI Object Storage）深度整合 |

🔧 **2026 年必须补的四条**：
1. **"备份在备库做 / 云对象存储作为备份目标"已是默认做法**，本书时代的本地磁盘备份目录（`$ORACLE_BASE/flashback`）只适合教学；
2. **应急恢复的演练纪律**：**"没演练过的备份等于没有备份"**——定期做一次真实的 `RESTORE` + `RECOVER` 演练（或至少 `RESTORE ... VALIDATE` / `RECOVER ... TEST`）；
3. **许可边界**：**Active Data Guard** 需要单独的 ADG 许可；**Oracle 的备份与容错管理包（Backup and Recovery Manager 本身通常含在 enterprise 版里，但 ADG、Advanced Compression、Diagnostics Pack 常常不含）**——实施前要核实合同；
4. **PDB 的备份粒度与 12c 限制**：PDB 备份**要求 PDB 处于 open 状态**，这让"CDB 级备份"与"PDB 级备份"的运维策略需要分开设计（见 [`01`](01-Oracle12c体系结构与CDB-PDB.md)）。

## 三、经典论文与原始文献

| 文献 | 出处 | 与本主题的关系 |
| --- | --- | --- |
| Haerder & Reuter《Principles of Transaction-Oriented Database Recovery》 | ACM Computing Surveys 15(4), 1983 | **通用理论，非 Oracle 专属**：恢复算法的设计空间、检查点与日志 |
| Mohan 等《ARIES: A Serializability-Preserving Recovery Algorithm With Repeating History》 | SIGMOD 1992 | **通用理论，非 Oracle 专属**：前滚/后滚、重复历史，与 RMAN 的恢复流程同构 |
| Bernstein, Hadzilacos & Goodman《Concurrency Control and Recovery in Database Systems》 | Addison-Wesley, 1987（书） | **通用理论，非 Oracle 专属**：分布式环境下的恢复与副本管理 |
| Oracle《Oracle Database Backup and Recovery User's Guide》 | Oracle 官方文档（非论文） | RMAN 命令与恢复流程的权威描述 |
| Oracle《Oracle Data Guard Concepts and Administration》 | Oracle 官方文档（非论文） | Data Guard 三种形态、保护模式、switchover/failover 的权威描述 |

> 说明：备份恢复是**通用数据库理论**，DG 与 RMAN 是**产品实现**。上述均为**通用理论或官方文档**，明确**不是 Oracle 专属论文**。

## 四、近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **备份的"不可变/防篡改"**（immutable backup、WORM 存储、备份与勒索软件对抗）在 2020 年代成为研究热点：RANSOM 攻击会先删除备份，所以**离线/异地/不可变副本**是现代备份策略的第一原则；
  - **备份即数据湖**（备份到对象存储 + Parquet 化分析），以及 **备份的可验证性（verifyability）**；
  - **存算分离下的备份**：Aurora（SIGMOD 2017）把日志作为持久性载体，重新定义了"备份"的边界。
- **工业界**：
  - **Oracle 侧**：`RESTORE ... VALIDATE`、`RECOVER ... TEST` 让"备份可用性"可被周期性验证；云备份（OCI Object Storage）与 S3 兼容目标；
  - 🔧 **CDC 与"逻辑备份"的融合**：`debezium/debezium`（star 实测 ≈13152）让"从 Oracle 取变更"不再依赖逻辑 DG；而 **逻辑 DG 的 SKIP 规则**与 CDC 的过滤规则正在收敛；
  - 🔧 **国产替代下的"容灾重构"**：从 Oracle DG 迁到 OceanBase/PolarDB/TiDB 时，"三副本 + Raft/Paxos"把 DG 的职责吸收进内核，**不再需要单独搭一套 DG**，但**跨地域容灾（城市级）的方案需要重新设计**（OB 的三地五中心、TiDB 的 DR 方案各有侧重）；
  - 🔧 **演练工具化**：很多企业把"切换演练"做成**定期自动演练**（如每季度一次 switchover 并观察业务），把"演练"变成流程的一部分，而不是事故后的应急。

## 五、常见误区与本书需修正之处

| # | 误区 | 修正 | 书目 |
| --- | --- | --- | --- |
| 1 | "备份成功就等于能恢复" | 要定期做**恢复演练**（`RESTORE ... VALIDATE` / 完整 restore 到隔离环境） | 全部 9 本 |
| 2 | "归档日志让它自动删就行" | 归档目标满会导致**实例挂起**；删除策略要匹配恢复目标（RPO） | DBA 攻坚指南（运维章）有流程，其余书偏设置 |
| 3 | "逻辑 DG 比物理 DG 高级" | 物理 DG 是默认首选；逻辑 DG 有数据类型/DDL 限制且 SQL Apply 慢 | 12c 教材第 15–16 章只讲 RMAN，未涉及 DG |
| 4 | "`Maximum Protection` 只是更安全的选项" | 备库不可用**主库会停**——这是必须提前对齐业务预期的代价 | 全部 9 本 |
| 5 | "Failover 之后原主可以自动回来" | 通常要**重建**（`Flashback to SCN` 只在少数场景可行），否则重新搭 DG | DBA 攻坚指南有案例 |
| 6 | "PDB 可以用和整库一样的方式备份" | **PDB 备份要求 PDB 处于 open 状态**，运维策略要分开设计 | 12c 教材第 15 章未提 PDB 粒度的限制 |
| 7 | "RMAN 增量备份很快，因为只备份变化块" | 前提是先开**块跟踪**（block change tracking），否则仍读全量 | 全部 9 本 |
| 8 | 🔧 "DG 是容灾的终局方案" | 在国产化替代中，"多副本共识"把 DG 的职责吸收进了内核；DG 的角色从"唯一方案"变成"可选增强" | 🔧 高并发 Oracle 书（DG 部分）与全部 9 本未覆盖国产替代 |
| 9 | 🔧 "Active Data Guard 会自动启用" | 它是**额外许可**；备库要在 `READ ONLY` 下继续应用日志，需要确认合同是否包含 ADG | 🔧 全部 9 本未提许可边界 |
| 10 | 🔧 "绝对不能做不完全恢复" | 恰恰相反：**误删表之后的正确动作是不完全恢复到删除前**，配合 Flashback 与 FDA 形成分层 | 🔧 12c 教材第 16 章的闪回与 RMAN 章节彼此割裂，未形成分层策略 |

## 六、与其他章 / 其他书的联系

- **上一章**：[`11-RAC与高可用.md`](11-RAC与高可用.md)（GI 管实例存活、DG 管数据副本，二者常一起部署）
- **下一章**：[`13-高并发系统的架构与设计.md`](13-高并发系统的架构与设计.md)（容灾是高并发架构的组成部分；读写分离与备份的互补）
- **强相关**：[`04-事务与redo-undo-归档.md`](04-事务与redo-undo-归档.md)（归档模式是本章的前提；redo 是恢复的燃料）
- **强相关**：[`07-SQL性能诊断与调优实践.md`](07-SQL性能诊断与调优实践.md)（备份期间的 I/O 争用会污染 AWR）
- **强相关**：[`01-Oracle12c体系结构与CDB-PDB.md`](01-Oracle12c体系结构与CDB-PDB.md)（CDB/RAC 下的备份粒度）
- **理论对照**：[`数据库系统概念6/16-恢复系统.md`](../数据库系统概念6/16-恢复系统.md)（ARIES、检查点、恢复算法的完整理论版）；[`软件架构设计/09-高可用与稳定性.md`](../软件架构设计/09-高可用与稳定性.md)（高可用指标体系与演练纪律）
- **其他书**：《DBA攻坚指南》第 1–4 章（Oracle 运维）里有"物理 DG 转逻辑 DG 滚动升级"与"数据泵迁移"的实操步骤，是本章 1.4 的实战版；《高并发 Oracle 数据库系统的架构与设计》最后从容灾与高并发角度讲 Data Guard 的妙用。
