# 02 实例配置与内存、TempDB 管理（目录版 · 精读重构）

> ⚠️ 主题重构章（取证降级见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第三节）。SQL Server 不可本机实测：全章"转述 + ⚠️"，准绳为 ✅ Learn 验真 URL；跨引擎通用机制类比见文末与 03/04/08 章 🔧。

## 本章地图

1. "高级选项"总闸面：sp_configure 的世界
2. 内存：max server memory 与min 的博弈
3. tempdb：一个库养活全实例的耗材经济学
4. MAXDOP/成本阈值/优化器高级配置的常规三件套
5. 配置变更的运维纪律（改什么、怎么改、怎么退）

## 一、sp_configure：实例的仪表盘与旋钮

- 官方"服务器配置选项"总表（约 40+ 个选项、默认值/动态性/生效方式）✅ https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/server-configuration-options-sql-server
- 管理员高频旋钮 ⚠️ 转述：`max server memory (MB)`、`min server memory`、`max degree of parallelism`、`cost threshold for parallelism`、`show advanced options`（先开它才能看见多数旋钮）、`scan for startup proc`、`lightweight pooling`（禁用勿碰）。
- 读法惯例：`sp_configure 'option'` 看运行值 vs 配置值两列——**RECONFIGURE 后两列不一致**就是"这个选项要重启才生效"的信号灯 ⚠️。
- `optimize for ad hoc work`：缓存即弃查询的瘦身开关，OLTP 混杂 workload 的常规开项 ⚠️；机理（计划缓存条目结构）见 [../Pro_SQL_Server_Internals/14-查询优化执行与计划缓存.md](../Pro_SQL_Server_Internals/14-查询优化执行与计划缓存.md)。

## 二、内存：把操作系统当合伙人

- SQL Server 默认**贪婪**吃内存（max 无上限时逼近物理内存），与 OS/其他进程争 RAM 是"服务器越跑越慢"的经典剧本 ⚠️——设 `max server memory` 是第一安装后动作。
- 容量规划口径 ⚠️ 转述：留基线（OS+监控代理+连接开销）→ 留缓冲池目标（热数据 working set）→ 留 CLR/列存压缩/哈希连接 spill 的弹性；多实例同机先分额度再谈超卖。
- 内存压制的表现面：page life expectancy 跳水、lazy writer 忙、backup/大数据量 ETL 时段 OOM 杀进程（Linux 侧 systemd-oom）⚠️；观测入口在 08 章 DMV 线。
- In-Memory OLTP（内存优化表）是"另一套内存账本"：HEAP/INDEX 两类、 DURABILITY 可降级、与缓冲池分池记账 ⚠️；官方入门 ✅ https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/introduction-to-memory-optimized-tables；其内核史见 [../SQL_Server_2012_Internals/01-体系结构与SQLOS.md](../SQL_Server_2012_Internals/01-体系结构与SQLOS.md)（SQLOS 内存管理）。

## 三、tempdb：多文件、争用与版本存储

- 官方 tempdb 专页（配置要点、多文件均衡、8032/trace flag 历史包袱）✅ https://learn.microsoft.com/en-us/sql/relational-databases/databases/tempdb-database
- tempdb 承担四类活 ⚠️：显式临时表/表变量、排序/hash spill、游标工作区、**行版本存储**（RCSI/快照隔离/MARS/触发器 undo 版本都写这里）——最后一个最常被容量规划遗忘。
- 经典处方 ⚠️ 转述：按 CPU 核数配 N 个等大盘文件（起步 4/8，PFS/GAM 争用实测再调）、独立快卷、重启不丢但要重建（tempdb 每次实例启动重播 model 库模板）。
- 版本存储失控的连锁：长事务 + RCSI → tempdb 暴涨 → 日志链受累 → 备份窗口爆掉；与 04/05 章的日志与副本话题同一条因果链 ⚠️。
- 🔧 通用机制注：SQLite 无 tempdb 概念，其临时对象在 `PRAGMA temp_store` 与 `-wal` 旁路文件里发生；"版本空间要算容量"这一课在 MVCC 引擎（InnoDB undo、PG 死元组、SQL Server version store）三处同构——对照 [../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md) 的 undo 段（若该文件涉及 undo 章，其 00 可作入口）。

## 四、并行度三件套与优化器配置

- `max degree of parallelism (MAXDOP)`：单查询可用线程顶棚；OLTP 常用小值、数仓常用核数整组 ⚠️ 转述（无万能公式，NUMA/超线程需分别定）。
- `cost threshold for parallelism`：多少估算成本才配并行；默认值在 2022 时代"偏低"是社区长期共识，升级后先测 workload 直方图再动 ⚠️。
- 数据库级 `AUTO_UPDATE_STATISTICS`/延迟持久化等选项、`READ_COMMITTED_SNAPSHOT`：实例级与库级开关的作用域别混 ⚠️；统计信息内核口径见 [../Pro_SQL_Server_Internals/03-统计信息.md](../Pro_SQL_Server_Internals/03-统计信息.md)。
- 配置审计面：`sys.server_configurations` 留快照、变更走工单——"这台机器为什么和那张不一样"是排障第一问 ⚠️。

## 五、变更纪律：改-验-退三步

1. 改前：当前配置存档（`sys.sp_configure` 输出+截图）；标注是否需重启。
2. 改后：动态项 RECONFIGURE 立即回读运行值；重启项安排维护窗口，衔接 01 章升级窗口管理。
3. 回退预案：任何内存/并行/临时库改动都要有"恢复默认"的一步式脚本，纳入 10 章作业化。

## 六、与其他章/其他笔记的联系

- 装完第一件事清单 → [01-2022产品全景与安装升级.md](01-2022产品全景与安装升级.md)；tempdb 卷规划依赖存储章的盘策略 → [03-数据库存储与文件组管理.md](03-数据库存储与文件组管理.md)。
- 版本存储与并发语义 → [08-监控排障DMV扩展事件与查询存储.md](08-监控排障DMV扩展事件与查询存储.md)（阻塞链里 tempdb 常当嫌疑人）。
- 内存压力对计划缓存的清洗效应 → [../SQL_Server_2012_Internals/07-查询执行优化与计划缓存.md](../SQL_Server_2012_Internals/07-查询执行优化与计划缓存.md)。
- 跨引擎"实例总闸"对照：MySQL `innodb_buffer_pool_size` 与 `tmp_table_size` → [../MySQL_8_Administrators_Guide/00-总览与阅读地图.md](../MySQL_8_Administrators_Guide/00-总览与阅读地图.md)；PG `shared_buffers`/`work_mem` → [../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md](../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md)。

## 七、常见坑清单（⚠️ 转述整理，非原书条文）

1. **max memory 不设**：OS 与其他进程被挤到 OOM，故障表象却在"随机慢"——第一安装后动作 ⚠️。
2. **min=max 同值**：内存锁死后其他 clerk 饿死（列存/CLR 场景尤甚）⚠️。
3. **tempdb 单文件大增长**：PFS 争用表现为 PAGELATCH_EX 等待堆积，重启才发现"原来一直慢" ⚠️。
4. **把 model 库当摆设**：新建库默认大小/恢复模型/兼容级全继承自 model——批量建库前改 model 是杠杆点 ⚠️。
5. **MAXDOP 一刀切**：按"核数模板"抄值，不看 NUMA 边界与 workload 形态；升级后并行等待暴增 ⚠️。
6. **配置改了没 RECONFIGURE/没重启**：运行值与配置值两列不一致时误判"改了没用" ⚠️。
7. **多实例不分额度**：同机三实例都设 max=物理-2G，合计超卖，谁先吃谁赢 ⚠️。

## 八、实操速查卡（⚠️ 社区通行写法示意，非本书实测）

```sql
EXEC sp_configure 'show advanced options',1; RECONFIGURE;
EXEC sp_configure 'max server memory (MB)';   -- 看运行/配置两列
SELECT * FROM sys.databases WHERE name='tempdb';
SELECT file_id, name, size, growth, is_percent_growth FROM sys.master_files WHERE database_id=2;
DBCC SQLPERF(LOGSPACE);                        -- 各库日志使用率快照
```

- 用途：交班前"五连看"——内存顶棚、tempdb 文件、增长策略、日志空间、兼容级（把 01 章体检并入）⚠️。

## 九、本章回看自测

- sp_configure 哪两列不一致说明要重启？（一）
- tempdb 承担的四类活里最易被容量规划遗忘的是哪个？（三）
- max memory 与"吵闹邻居"的关系？（二/六·7）
- RCSI 开启后哪张库先感受到压力？（三·版本存储）
- 配置变更三步纪律是什么？（五）

## 十、配置变更工单模板（⚠️ 示意）

| 字段 | 内容要点 |
| --- | --- |
| 变更对象 | 实例名 + sp_configure 选项或 ALTER DATABASE 选项 |
| 当前值/目标值 | 运行值与配置值两列都记录（一·读法惯例） |
| 生效方式 | RECONFIGURE 即效 / 需重启（排维护窗口，接 01 章） |
| 回退一步 | 恢复原值的现成语句 |
| 验证钩子 | 变更后 24h 观察指标（等待统计/作业成败，接 08 章） |

- 用途：把第四节"改-验-退"纪律落成可审计单据；批量实例走 CMS 扇出执行（10 章）。

## 十一、复现与延伸（可选自修）

- 🔧 复现"版本存储吃空间"的通用直觉（SQLite 3.45.3，非本书引擎行为）：开 `journal_mode=wal` 后连续更新同一行 5000 次不 checkpoint，观察 `-wal` 随未冻结读快照膨胀——SQL Server 侧对应 tempdb version store 在长事务+RCSI 下的同一物理压力。
- 阅读动线：先本册 02 → #56 的 SQLOS 内存章 [../SQL_Server_2012_Internals/01-体系结构与SQLOS.md](../SQL_Server_2012_Internals/01-体系结构与SQLOS.md) → #36 的排查章 [../Pro_SQL_Server_Internals/15-系统排查与扩展事件.md](../Pro_SQL_Server_Internals/15-系统排查与扩展事件.md)。
- 术语回填：min/max server memory、clerk、PFS 的官方定义都在 ✅ server-configuration-options / tempdb-database 两页（见第一节 URL），转述与文档冲突时以文档为准。

## 核心概念速览（中英对照）

- **服务器配置选项** — Server Configuration Options (sp_configure)：实例级旋钮总表，动态/静态两态。
- **最大服务器内存** — max server memory：缓冲池顶棚，防 OS 挤压的第一开关。
- **缓冲池** — Buffer Pool：数据页的内存映射区，命中率的母体。
- **tempdb** — tempdb：全实例共用的工作/版本临时库，重启重建。
- **版本存储** — Version Store：tempdb 里的行版本链，RCSI/快照隔离的燃料。
- **MAXDOP** — max degree of parallelism：单查询并行线程顶棚。
- **并行成本阈值** — cost threshold for parallelism：触发并行的估算成本门槛。
- **NUMA** — Non-Uniform Memory Access：多插槽服务器的内存拓扑，调度与 MAXDOP 的地形。
- **内存优化表** — Memory-Optimized Table (Hekaton)：独立内存账本+无闩锁索引的 OLTP 快车道。
- **PFS 页** — Page Free Space / GAM 系列：tempdb 多文件缓解的元数据争用点。
- **延迟持久化** — Delayed Durability：库级"提交先记账后落盘"换吞吐的取舍开关。
- **RECONFIGURE** — RECONFIGURE：让非重启型配置即刻生效的确认动作。

## 最新演进与工业实践

- 2022 的"配置友好度"延续：tempdb 与内存选项仍走 sp_configure+ALTER DATABASE 双层 ✅（server-configuration-options、tempdb-database 两页均 200 验真）。
- 云对照：Azure SQL 用"弹性/vCore 配额"替代手动内存额度——理解 max server memory 后才看得懂云上的"配置被托管" ⚠️ 转述，衔接 [10-自动化作业与混合云运维.md](10-自动化作业与混合云运维.md)。
- 社区基准：MAXDOP/CTFP 调优的公开方法论（如用 `sys.dm_exec_query_stats` 直方图定阈值的脚本化流程）已成巡检标配 ⚠️；本册只登记方法论存在，不代跑数。
- 开源同构：PG 16/MySQL 8 的临时空间与缓冲池治理与本章一一对位（temp 表空间、buffer pool），跨引擎 DBA 可平移心智 → 参考 [../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md](../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md)、[../MySQL_8_Administrators_Guide/00-总览与阅读地图.md](../MySQL_8_Administrators_Guide/00-总览与阅读地图.md)。
- 风险实践：多实例共享 max memory 的"吵闹邻居"治理（cgroup/容器限额在 Linux 路线的应用）是 2024–2026 混合负载常态 ⚠️ ✅ Linux 总览 https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-overview。
