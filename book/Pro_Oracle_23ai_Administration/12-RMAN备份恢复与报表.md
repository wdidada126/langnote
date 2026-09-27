# 12 · RMAN 备份、恢复与报表（原书 Ch.13+14 合并, pp.379-458）

> 合并声明：原书 Ch.13 "RMAN Backups and Reporting"（✅ …_13, pp.379-413）与 Ch.14 "RMAN Restore and Recovery"（✅ …_14, pp.415-458）同属 RMAN 主题域，按 [00-总览与阅读地图.md](00-总览与阅读地图.md) §三合并。章内小节自拟 ⚠️；Oracle 行为一律 ⚠️ 转述；RMAN 参考册深链在 /26/ 重排后不可稳定命中（口径 00 §2.4），概念取证走 Concepts ✅ …/23/cncpt/index.html 。含 🔧 类比 1 组（非本书引擎行为）。

## 12.1 RMAN 架构与三本账

- **目标库**（target：控制文件里的物理结构账+被备份对象）、**恢复目录**（catalog：可选的元数据富库，脚本/持久设置/多库账本）、**通道**（server process：真正干 I/O 的会话）⚠️；
- 元数据双账：控制文件（自动备份 piece `c-...` 保命根）+ 目录（保留窗口策略的执行者）——`crosscheck`/`report schema` 的差别就在问哪本账 ⚠️；
- 快闪恢复区（FRA，04 章）是备份/归档/控制文件自动备份的默认聚宝盆：配额=容量规划+告警线（"归档爆盘"案的两 half 都在此）⚠️。

## 12.2 备份语义学（本章第一地图 ⚠️）

| 轴 | 选项 | 决策问句 |
|---|---|---|
| 物理形态 | backupset（RMAN 专属打包，可压缩/加密/多卷）vs image copy（文件级镜像，秒 restore/可 swap） | 要恢复速度还是要空间/校验红利 |
| 逻辑档位 | FULL / LEVEL0（基）/ LEVEL1 差异（differential vs cumulative）| 窗口与链深的平衡 |
| 对象粒度 | 库/表空间/数据文件/**PDB**/归档/控制文件/口令文件/spfile | 容器化后的备份单位重学 |
| 内容策略 | 增量+`backup as compressed backupset`、`plus archivelog`、不备只读表空间 | 窗口内做不完的都是设计错 |
| 生命周期 | `retention policy to recovery window of N days/redundancy k` + `delete obsolete` | 保留政策即合规文档 |

- 增量扫描账：块变更跟踪（block change tracking，状态视图 `v$block_change_tracking`）让 level1 免全读 ⚠️；
- **NOLOGGING 契约**（07/10 章两度预告的清算）：NOLOGGING 产物可能不在增量里留痕，备后 `recover ... nologging`/全备兜底或干脆对生产禁用 ⚠️。

## 12.3 Reporting：备份子系统的可观测面（Ch.13 后半 ⚠️）

`list backup summary` / `report need backup`（按保留政策答"现在丢了要不要命"）/ `report unrecoverable`（NOLOGGING 受害名单）/ `v$rman_status` 与 `v$rman_output`（作业历史与 channel 回声）——Pro 立场：**恢复演练的剧本从 report 长出来**，不是从记忆长出来 ⚠️。

## 12.4 恢复四境（Ch.14 主干 ⚠️）

1. **介质失败、库还开着**：离线单文件 `restore/recover datafile`，业务无感（online 表空间粒度）；
2. **全库崩溃（DB 关、数据文件坏）**：`startup mount → restore database → recover database → alter database open resetlogs?`（仅当不完全恢复/控制文件重建才 resetlogs，04 章分叉语义）；
3. **到时间点（PITR）**：`run { set until time/scn/log_sequence ...; restore; recover }` + `catalog/increment` 联动——"把昨天 14:32 的库还回来"的原子流程；闪回数据库（`flashback database to timestamp/scn`，依赖闪回日志保留窗口）是其快捷同义 ⚠️（04 章 UNDO/闪回区账）；
4. **表级手术**：`recover table ... until time`（RMAN 自动建辅助实例、抽表回插——11g+ 的"免全库回滚"王牌，代价：临时空间+归档需求）⚠️；PDB 级同理按容器（`restore pluggable database`）⚠️（→11 章）。

配套件：控制文件/SPFILE/口令文件的恢复三部曲（从自动备份 piece 起，`restore controlfile from autobackup`→mount→recover）、`switch datafile ... to copy`（image copy 秒切+`recover from service` 备库拉增量）⚠️。

## 12.5 校验与"备份可信"工程（⚠️ 管理纵深）

- `backup validate database` / `restore ... validate`：只读验块不写文件——把"备份作业绿勾"升级为"介质真可恢复"；
- 坏块族：`v$database_block_corruption`（备份时物理/逻辑坏块检测），介质恢复（block media recovery）只修坏块不滚全文件；`dbv` 工具离线核文件 ⚠️；
- 加密备份：口令模式/Wallet 模式（05 章钱包联动），**密钥丢了备份=砖**写进变更单模板；
- 演练制度：季度恢复到隔离主机+`check restore`+业务抽样验数；备份邮件绿≠资产安全 ⚠️——Ch.13/14 合并阅读的真正收口。

**🔧 类比（非本书引擎行为）——"快照+日志续档"的最小身**：SQLite WAL 模式下无 RMAN，但概念对子齐全：整件拷贝式快照 ↔ image copy；WAL 帧序 ↔ 归档日志流。本机 sqlite 3.45.3 实跑：

```
$ python - <<'EOF'
import sqlite3, os
p1 = sqlite3.connect('pdb1.db')          # WAL 模式的既有库
p1.execute("vacuum into 'pdb1_snap.db'") # 一致性快照(不锁读)
print(os.path.getsize('pdb1_snap.db'), os.path.getsize('pdb1.db'))  # 8192 8192
print(p1.execute('pragma wal_checkpoint(truncate)').fetchone())     # (0, 0, 0)
EOF
8192 8192
(0, 0, 0)
```

对照点：`vacuum into` ↔ image copy/热备快照（"运行中取一致副本"）；`wal_checkpoint(truncate)` ↔ 日志截断/推进检查点（把 WAL 折回主件、缩短"恢复重放距离"）；checkpoint 返回三元组（busy, log, checkpointed）≈ RMAN 报告里"做到哪了"的状态位。**差异**：SQLite 无保留政策/无 catalog/无按时间点到任意库级恢复（缺"归档续档+元数据账本"两件套），故只能"整件快照+顺放日志"，Oracle 的四境恢复在类比端只剩第 1 境的影。演示于 tmp/dbwave_w4_ora23，非本书引擎行为。

## 12.6 备份域运维清单（⚠️ 综合两章操作位）

1. 策略先行：保留窗口×备份档位×压缩/加密矩阵落纸（合规附件）；
2. FRA/备份盘双水位告警（归档与备份互为挤兑方）；
3. 每次大变更（06 move/07 rebuild NOLOGGING/11 插拔/16 补丁）后备份链语境复位：全量基线重起或 `recover ... nologging` 清账；
4. 控制文件自动备份常开（spfile 入备份件）；
5. 演练产出《恢复时长实测表》——MTTR 是备份设计的唯一验收指标。

## 12.7 RMAN 命令速查（⚠️ 示意，target=/连接语境省略）

```rman
-- 备: 全库+归档+压缩+标签(控制文件自动备份走 configure 策略, 见下)
run { allocate channel c1 device type disk;
      backup as compressed backupset database plus archivelog
        tag 'DLY_FULL' format '/fra/%d_FULL_%U'; }
configure controlfile autobackup on;
configure device type disk parallel 2;
-- 查: 三 report 与两 list
report need backup;  report unrecoverable;  list backup summary;  list copy of database;
crosscheck backup; delete noprompt obsolete of recovery window of 14 days;
-- 恢: 四境骨架(12.4 的展开形)
restore database check restore;                -- 只验不落的"纸上恢复"(12.5)
run { set until time "to_date('2025-01-31 14:32:00','yyyy-mm-dd hh24:mi:ss')";
      restore database; recover database; }    -- PITR 半章; 收尾 resetlogs 决策(04 章)
restore controlfile from autobackup;           -- 控制文件丢失剧本第一拍
recover table hr.employees until time
  "to_date('2025-01-31 14:32:00','yyyy-mm-dd hh24:mi:ss')"
  auxiliary destination '/fra/aux';            -- 表级微创(12.4 第 4 境)
-- PDB 粒度(11 章联动的容器备份账)
restore pluggable database pdb_app; recover pluggable database pdb_app;
```

速查纪律：**每段命令先在心里过"备份链语境"**——谁使此前 piece 作废（resetlogs）、谁欠下补备（NOLOGGING/新 PDB 插入）⚠️。

## 12.8 恢复演练日历模板（⚠️ 制度件）

| 频率 | 演练 | 验收物 |
|---|---|---|
| 每周 | `restore ... validate`/check restore 全量 | 无坏块报告+时长趋势 |
| 每月 | 抽 1 PDB 恢复到隔离实例+开库验数 | 《MTTR 实测表》逐月 |
| 每季 | 全库 PITR 到指定分钟+控制文件丢失剧本 | 归档连续性+resetlogs 认知 |
| 每半年 | 跨主机/跨版本（升级后）恢复+加密口令件重验 | 备份件可移植报告 |
| 每次大变更 | 变更后立即基线+抽查恢复 | 变更单附件 |

## 自测（能默写=过关）

- backupset vs image copy 的恢复经济学；level0/1 与变更跟踪的关系。
- 恢复四境各自的命令骨架与业务影响面。
- report need backup 与 validate 各回答什么信任问题。
- NOLOGGING 在备份域的两处清算路径。

## 核心概念速览（中英对照）

- **RMAN** — Recovery Manager：官方备份/恢复/校验子系统与 DSL。
- **恢复目录** — recovery catalog：可选元数据库，扩保留策略与脚本库。
- **通道** — channel：执行备份/恢复 I/O 的目标库会话。
- **备份集** — backupset：RMAN 打包格式，支持压缩/加密/多卷。
- **镜像副本** — image copy：文件级精确拷贝，可秒切/交换恢复。
- **增量基** — level 0/1：以 0 为基的差异链；cumulative 差分二选一。
- **块变更跟踪** — block change tracking：增量备份免全读的位图账。
- **保留政策** — retention policy：recovery window/redundancy 两种过期法。
- **交叉检查** — crosscheck：物理件与账本的相符性核对。
- **不完全恢复** — incomplete/PITR：恢复到指定时间/SCN/日志序列后 resetlogs。
- **闪回数据库** — flashback database：整库时间机器，依赖闪回日志窗口。
- **表级恢复** — table recovery：RMAN 辅助实例抽表回插的微创术。
- **介质恢复** — media recovery：restore+apply redolog 使文件追平一致性点。

## 最新演进与工业实践

- **备份即数据的第二生命周期**：23ai 线继续强化"自动备份到 FRA/Cloud Object Store"的两级出口（DBMS_CLOUD Object Store 备份件生态 ⚠️ 转述），云侧 ATP 全自动（✅ adbsb：自动级联备份+64 天内任意点恢复/`restore restore point` 时间机器），本章人工件在托管世界逐项清零 ⚠️。
- **勒索语境下的不可变备份**：2024+ 工业实践把"保留政策"升维为 WORM/不可变存储+隔离账户双闸（Oracle 官方备份白皮书方向 ⚠️ 通说）；`delete obsolete` 的执行身份与备份账户分离是新审计点。
- **验证自动化**：`backup validate`+定期自动恢复沙箱（Docker/K8s 起临时库验片）成为大厂标配 ⚠️；对位开源思想：整件快照+重放验证在 PG 生态（pgBackRest 的 check）同构——对照 ../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md。
- **盘上延伸**：恢复的等待事件与诊断学（为何 recover 慢：并行/归档预取/检查点）见 [../Troubleshooting_Oracle_Performance_2e/00-总览与阅读地图.md](../Troubleshooting_Oracle_Performance_2e/00-总览与阅读地图.md)；引擎无关的备份/DR 框架叙事（快照/复制/连续数据保护谱系）在 ../Database_Administration_2e/00-总览与阅读地图.md 第 12-13 章；12c 中文操作对照在 ../Oracle12c数据库应用与开发/12-备份恢复容灾与DataGuard.md（RMAN 口径较旧，容器恢复缺位 ⚠️）。
