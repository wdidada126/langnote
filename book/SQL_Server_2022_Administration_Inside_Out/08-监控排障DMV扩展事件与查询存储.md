# 08 监控排障：DMV、扩展事件与查询存储（目录版 · 精读重构）

> ⚠️ 主题重构章（取证降级见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第三节）。SQL Server 不可本机实测：引擎口径"转述 + ⚠️"；🔧 E4 用本机 SQLite 3.45.3 演示锁等待/超时**通用机制**，标注非本书引擎行为。

## 本章地图

1. 观测三支柱：快照（DMV）、事件（XEvents）、历史（QS/DC）
2. DMV 巡礼：等待统计、请求会话、操作系统内存三条主线
3. Extended Events：会话架构、模板与"低开销"边界
4. Query Store：计划历史的行车记录仪与强制回放
5. Data Collector：官方慢变量仓库
6. 阻塞链与死锁：从现象到处置的剧本
7. 🔧 E4：锁等待与超时的可测同构

## 一、观测三支柱的分工

- 快照类（DMV/DMF）：读"现在"——便宜但过时即失，采样节奏决定你能否抓住鬼影 ⚠️ ✅ 总览 https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/system-dynamic-management-views。
- 事件类（XEvents）：订"发生"——定向捕获、低开销、可扩展到文件/环表 ⚠️ ✅ https://learn.microsoft.com/en-us/sql/relational-databases/extended-events/extended-events。
- 历史类（Query Store / Data Collector）：存"趋势"——为"昨天 3 点为什么慢"留档 ✅ https://learn.microsoft.com/en-us/sql/relational-databases/performance/monitoring-performance-by-using-the-query-store、https://learn.microsoft.com/en-us/sql/relational-databases/data-collection/data-collection。
- 排障心法 ⚠️（管理册观点）：先定"现象坐标"（哪个库/哪类查询/什么时段），再选支柱——拿 DMV 扫历史是徒劳，拿 QS 看阻塞是错器。

## 二、DMV 巡礼：三条主线

- **等待统计**：`sys.dm_os_wait_stats` 是引擎自述"我们在等什么"——CXPACKET/LCK_M_*/PAGEIOLATCH_*/WRITELOG/PAGELATCH_EX（tempdb）等高频等待的语义与第一反应处方 ⚠️ 转述（数值因机而异，不给阈值教条）。
- **会话与请求**：`sys.dm_exec_sessions/requests`+`sys.dm_exec_sql_text/query_plan` 三视图连坐——当前在跑什么、什么语句、什么计划 ⚠️；社区封装 sp_WhoIsActive（Adam Machanic）/First Responder Kit（Brent Ozar）已成事实标准 ⚠️（指路 github: adam-machanic/sp_whoisactive、BrentOzar/SQLServerFirstResponderKit，未经逐 commit 核验）。
- **OS 资源面**：`sys.dm_os_memory_clerks`（谁吃了内存，接 02 章）、`sys.dm_os_schedulers`（并行压力）、`sys.dm_io_virtual_file_stats`（按文件 IO 画像，接 03 章容量账）。
- DMV 自身的观察者效应 ⚠️：高频全量扫 DMV 也有成本，巡检脚本要限列/限速；#36 的排查章口径见 [../Pro_SQL_Server_Internals/15-系统排查与扩展事件.md](../Pro_SQL_Server_Internals/15-系统排查与扩展事件.md)。

## 三、Extended Events：把探针插进引擎

- 架构三件 ⚠️：Event（事件）/ Predicate（谓词过滤）/ Target（ring_buffer、event_file、配对打包）；系统健康会话（system_health）默认常在，先读它再造轮子 ⚠️。
- 高频用法 ⚠️ 转述：死锁图（xml_deadlock_report）、超时与错误（attention/rpc_completed 系）、存储过程级追踪过滤（定向采样代替 SQL Trace）；Profiler 已入废弃轨道，新代码一律 XEvents ⚠️。
- 开销边界：事件风暴（每秒数十万 rpc 全量捕获）会反噬生产——谓词前置+抽样+文件目标滚动是三条安全带 ⚠️；与 SQL Trace 的对比结论见 #56 册 [../SQL_Server_2012_Internals/08-事务并发与DBCC内部机制.md](../SQL_Server_2012_Internals/08-事务并发与DBCC内部机制.md) 所引官方口径 ⚠️。
- 管理面：会话启停纳入 10 章作业日历（如夜间批量时段临时开写死锁采样）⚠️。

## 四、Query Store：计划回归的保险箱

- 官方语义 ✅（query-store 页，见第一节 URL）：按库启用，存 runtime stats+query plans+等待统计（2022 增强等待维度 ⚠️ 转述）；两模式（读写/只读）与清理策略（stale 数据/最大存储）。
- 三大用例 ⚠️：找回归（同查询计划变化+耗时跳升）、强制旧计划（`sp_query_store_force_plan`）、升级体检（01 章切兼容级别前后对照基线）。
- QS 与自动调优的接口：自动调优的"强制回归计划"动作以 QS 为数据底座 → [09-查询性能智能查询处理与自动调优.md](09-查询性能智能查询处理与自动调优.md) ✅ https://learn.microsoft.com/en-us/sql/relational-databases/automatic-tuning/automatic-tuning。
- 运维注 ⚠️：QS 自身占库内文件（PRIMARY 或专 FG），容量预算里给它一列；只读副本/AG 环境的 QS 行为有版本细节 ⚠️ 以文档为准。

## 五、Data Collector：官方的慢变量仓库

- 官方机制 ✅（data-collection 页，见第一节 URL）：SSIS 包驱动的采集流水线（collect set→上传进 MDW 仓库库），预置 Disk Usage/Query Stats/Perfmon counters 三仓 ⚠️ 转述。
- 适用画像 ⚠️：容量趋势与"每周报告"友好，秒级排障不友好（采集粒度粗）——与自研轻采样（sp_Blitz 类）互补而非互斥。
- MDW 报表面与 SSMS 集成是"报告给管理层"的官方通道 ⚠️。

## 六、阻塞链与死锁处置剧本

1. 现场三拍 ⚠️：抓 `sys.dm_exec_requests.blocking_session_id` 链→定位头阻塞者的语句与等待→判断"等锁/等 IO/长运行"三分。
2. 处置分级 ⚠️：催办应用提交/回滚＞KILL 头阻塞（回滚代价先算——大事务 KILL 后 undo 更痛）＞结构性改造（加 NOLOCK 是饮鸩，快照隔离 RCSI 是正解之一，代价见 tempdb 章）。
3. 死锁：读 XEvents 死锁图定"互锁对象+持锁顺序"，处方优先改访问顺序/加合适索引缩小锁面 ⚠️；内核锁模式谱见 [../Pro_SQL_Server_Internals/12-锁类型阻塞与死锁.md](../Pro_SQL_Server_Internals/12-锁类型阻塞与死锁.md) 与 [../SQL_Server_2012_Internals/08-事务并发与DBCC内部机制.md](../SQL_Server_2012_Internals/08-事务并发与DBCC内部机制.md)。
- 🔧 **实验 E4（SQLite 3.45.3，非本书引擎行为）**：连接 A 持写事务（`BEGIN IMMEDIATE`+INSERT 未提交）；连接 B `timeout=1ms` 时尝试开写事务，0.008s 即报 `database is locked`（≈SQL Server"锁等待超时/立即失败"策略）；B 设 `PRAGMA busy_timeout=3000` 后同场景**实等 3.298s** 仍失败——阻塞时长=对方持锁时长，超时只决定"我陪你等多久"。类比管理概念：`LOCK_TIMEOUT`/查询超时/阻塞链排查同此理——**先找头阻塞者，再谈超时参数** ⚠️。仅通用机制演示。

## 七、与其他章/其他笔记的联系

- 内存/并行观测口径 → [02-实例配置与内存TempDB管理.md](02-实例配置与内存TempDB管理.md)；文件 IO 画像回扣存储账 → [03-数据库存储与文件组管理.md](03-数据库存储与文件组管理.md)。
- AG 健康 DMV 族 → [05-高可用与灾难恢复AlwaysOn.md](05-高可用与灾难恢复AlwaysOn.md)；安全审计事件（login/permission 类 XEvent）→ [06-安全主体与权限体系.md](06-安全主体与权限体系.md)。
- 波内分工：#68《SQL Server Advanced Troubleshooting》目录版落盘后是本链"深水区"下一站（只登记不链，波尾主代理闭链）。
- 开源同构：PG 的 `pg_stat_statements`/等待事件、MySQL 的 performance_schema → [../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md](../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md)、[../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md)。

## 八、常见坑清单（⚠️ 转述整理，非原书条文）

1. **重启前不抓等待统计**：`dm_os_wait_stats` 随实例重启清零——基线采集要在变更前 ⚠️。
2. **XEvents 全量 rpc 风暴**：谓词没前置，追踪自己成为头号等待 ⚠️（三·开销边界）。
3. **QS 只开不查**：留档没人复盘，回归在第三周才爆发——周报挂 QS Top-N 是开它的全部理由 ⚠️。
4. **死锁当报错处理**：应用对 1205 无重试逻辑，锁竞争演成业务投诉 ⚠️。
5. **拿 profiler 老习惯抓包**：SQL Trace 系工具在高吞吐下开销显著，迁 XEvents 是路线正确性 ⚠️。
6. **KILL 大事务不估回滚**：杀掉一时爽，undo 火葬场——KILL 前先查该会话已写事务量 ⚠️（六·2）。
7. **告警只配错误号不配"无数据"**：采集器停摆静默失联——观测面自身要有心跳告警 ⚠️（运维通识）。

## 九、排障路径速查卡（⚠️ 示意流程）

- "慢"字诀：QS 定位查询 → 计划与运行统计对照 → 等待类型归因（IO/锁/内存授予/并行）→ 处方回 02/09 章对应节。
- "锁"字诀：请求 DMV 拉阻塞树 → 头阻塞者语句现形 → XEvents 死锁图补结构 → 处置分级（六）。
- "崩"字诀：错误日志+system_health 会话 → 内存 clerk/IO 子系统快照 → 备份还原演练兜底（04）。
- "诡"字诀（间歇鬼影）：ring_buffer 常驻+错误号警报+按计划启停的定向会话——低成本钓鱼 ⚠️。

## 十、本章回看自测

- 观测三支柱各答哪类问题？（一）
- sp_WhoIsActive 们解决 DMV 的什么痛点？（二）
- system_health 为何要"先读再造"？（三）
- 🔧E4 中 busy_timeout=3000 实等 3.298s 说明了什么本质？（六·E4）
- QS 与自动调优的数据底座关系在哪章展开？（→09 章）

## 十一、复现与延伸（可选自修）

- 🔧 复现 E4（SQLite 3.45.3，非本书引擎行为）：两个连接交替 `BEGIN IMMEDIATE`，分别在 `busy_timeout=0/3000` 下计时报错（本机实测 0.008s 与 3.298s）；把"头阻塞者持锁时长决定一切、超时只决定陪等多久"写成一句话贴在你的排障卡片上。
- 延伸阅读：四大观测面官方页 ✅（第一节四 URL：DMV/XEvents/QS/DC）；社区工具 sp_WhoIsActive/FRK 仓库地址见第二节注 ⚠️ 指路；内核锁与并发内幕 [../Pro_SQL_Server_Internals/12-锁类型阻塞与死锁.md](../Pro_SQL_Server_Internals/12-锁类型阻塞与死锁.md)。
- 自修题三则：① "重启后等待统计清零"给基线工程带来的约束如何解（→八·1）；② 用 QS 三视图设计一张"回归周报"字段表（→四节）；③ system_health 里能挖出哪些默认已存的故障证据（→三节，开放题）。

## 核心概念速览（中英对照）

- **DMV** — Dynamic Management View：引擎运行态的透视窗（快照型）。
- **等待统计** — Wait Statistics：引擎对"瓶颈在哪类资源"的自我陈述。
- **扩展事件** — Extended Events：事件+谓词+目标三段式的轻量追踪框架。
- **system_health** — 系统健康会话：出厂常开的兜底探针。
- **死锁图** — Deadlock Graph (xml_deadlock_report)：两持有者互等的结构画像。
- **查询存储** — Query Store：计划与运行统计的历史仓库+强制回放保险箱。
- **计划回归** — Plan Regression：同查询换计划导致性能倒退的头号事故型。
- **Data Collector/MDW** — 数据收集器与管理数据仓库：官方趋势留档管道。
- **头阻塞者** — Head Blocker：阻塞链根部会话，处置优先级第一。
- **busy_timeout** — SQLite 锁重试预算（🔧E4）：等得起≠等得到，超时报错同 SQL Server 锁超时语义。
- **RCSI** — Read-Committed Snapshot Isolation：用 tempdb 版本链换"读不堵写"的库级开关。
- **sp_WhoIsActive** — 社区旗舰诊断过程：Adam Machanic 作品，排障标配 ⚠️。
- **基线采集** — Baseline Collection：变更前留存的指标快照，重启清零约束下的对抗手段。
- **心跳告警** — Watchdog Alert：对观测面自身停摆的元监控，"沉默即事故"的防线。
- **目标服务器** — Target Servers：一作业分发多实例的 Agent 扇出机制（接 10 章）。

## 最新演进与工业实践

- Query Store 在 2022 成为"默认开"的推荐基线（新库模板/迁移检查表常含），并作为自动调优数据面持续增值 ✅ https://learn.microsoft.com/en-us/sql/relational-databases/automatic-tuning/automatic-tuning。
- 等待统计维度入 QS（2022 起）让"计划回归+等待迁移"同屏诊断成为新版卖点 ⚠️ 转述（QS 官方页 ✅ 口径）。
- 可观测性栈融合：Prometheus/Grafana+metrics 导出器、OpenTelemetry 链路把 SQL Server 纳入统一平台监控是 2024–2026 大厂常态；XEvents 仍是引擎内第一现场 ✅ 概念 https://learn.microsoft.com/en-us/sql/relational-databases/extended-events/extended-events ⚠️ 集成细节转述。
- 社区工具线：First Responder Kit / sp_WhoIsActive（github: BrentOzar/SQLServerFirstResponderKit、adam-machanic/sp_whoisactive）持续维护至 2025+ ⚠️ 指路未逐 commit 核验。
- 排错方法论跨引擎互读：等待事件驱动的排错在 PG（waits/pg_stat_statements）与 MySQL（performance_schema）各有对应物 → [../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md](../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md)、[../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md)；同波 Oracle 排错册（#66）与 #68 深水区册落盘后由主代理闭链（此处只登记不链）。
- AI 辅助排错：自然语言问日志/生成诊断脚本的 Copilot 类工作流进入 2024–2026 运维台面，但"现场三拍"的结构化流程仍是提示工程的地基 ⚠️ 观点。
- 留档纪律：任何一次成功排障都要沉淀"现象→证据链→处方→验证"四段卡片，DMV 快照会过期，卡片不会 ⚠️ 观点句（管理册立场）。
