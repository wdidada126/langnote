# 章文件 01 · 体系结构与 SQLOS（原书第 1–2 章）

> 原书位置：Chapter 1 "SQL Server 2012 Architecture and Configuration" + Chapter 2 "The SQLOS"（章题 ✅ LoC 内容附注逐字）。
> 正文为精读重构转述；SQL Server 不可本机实测，机制结论一律 ⚠️ 并配 ✅ 官方文档准绳。本册 00 的取证/辨析/实验总表见 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 本章地图

| 主题块（转述提纲） | 一句话要旨 | 标注 |
| --- | --- | --- |
| 产品分层：关系引擎 vs 存储引擎 | 查询处理器与存储引擎以行流(OQPTR/行序化接口)为界，两半各走各的优化世界 | ⚠️ 转述 |
| 版本与配置 | 2012 各版本(Enterprise/BI/Standard…)在内存上限、并行度、特性(列存/镜像)上的配额差异是架构决策第一约束 | ⚠️ 转述，配额数字 ⚠️ 未逐条核验 |
| 进程模型 | 单进程多线程 + 数据库引擎作为 Windows 服务；DAC 专用管理员连接兜底 | ⚠️ 转述 |
| SQLOS 定位 | 在 Windows 之上再造一层"小型操作系统"：内存、调度、IO、异常四大子系统归口管理 | ⚠️ 转述 |
| 内存管理 | 内存 broker 按需在各 clerk 间调配；缓冲池(数据页缓存)为最大用户；NUMA 节点感知(2012 把 NUMA 提升为调度一等公民) | ⚠️ 转述 |
| 调度器与等待 | 协作式调度(scheduler/worker/task 三级)、非让出(suspect)检测；等待类型体系是排障语料库 | ⚠️ 转述，✅ 见 wait_stats 文档 |
| IO 子系统 | 异步 IO 完成端口、条带与交错(stripe/interleave)假设、8KB 页对齐 | ⚠️ 转述 |
| 异常与崩溃恢复入口 | 系统异常→mini-dump→恢复流程从 error log/尾部记录读起 | ⚠️ 转述 |

## 核心精讲（转述 + ⚠️）

### 1. 一张图分两半：关系引擎与存储引擎
书中把 SQL Server 切成"查询处理器(SQL 解析→标准化→优化→执行)"与"存储引擎(缓冲池→页→索引→日志)"两半，交界处是**火山式行流**：执行算子每次向上吐一行(或批)。这个分层是全书各章的目录学——第 6/7 章向下钻存储，第 10–12 章向上钻查询，SQLOS(第 2 章)则是两半共同的地基 ⚠️。同一分法在 [../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md) 的 MySQL"Server 层 vs 引擎层"里能找到几乎同构的对位，区别是 InnoDB 没有自建 SQLOS 层、直接吃 OS ⚠️。

### 2. SQLOS：为什么微软要在 OS 上再造 OS
Windows 不认识的三件事：(a) 缓冲池里每页属于哪个数据库对象；(b) 任务在等锁还是在等 IO；(c) 内存紧张时该牺牲哪个 clerk。SQLOS 的答案：内存 broker 记账 + 协作式调度器(每个 scheduler 绑定一个 CPU) + 统一异步 IO 栈 + 等待统计。工程含义：**SQL Server 的排障语言是"等待类型"**（PAGEIOLATCH_*、LCK_M_*、WRITELOG…），这在 [../Pro_SQL_Server_Internals/15-系统排查与扩展事件.md](../Pro_SQL_Server_Internals/15-系统排查与扩展事件.md) 是操作面，在本章是原理面 ⚠️。✅ 现代准绳：sys.dm_os_wait_stats 官方文档 https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-os-wait-stats-transact-sql 。

### 3. 内存拓扑与 NUMA（2012 时代分水岭）
2012 把 NUMA 节点做成调度与内存分配的一等对象：worker 亲和到节点、缓冲池按节点分桶、跨节点访问计入"异步内存池"等待。书中(推测口径 ⚠️)提醒：虚拟机 vNUMA 配置失真是 2012 时代性能玄学的第一来源。2016+ 的"软 NUMA"(Soft-NUMA) 把这条线工程化为可配置对象 ⚠️（演进节续讲）。内存目标/最小内存钳制选项的官方现代文档 ✅（Learn "server memory options" 系列页，本册未逐条 curl，标 ⚠️ 不引用 URL）。

### 4. 调度：协作式与"非让出"
worker 必须在协作点主动让出，否则 SQLOS 标记 scheduler "yield 超时/非让出可疑(suspect)"，写进 system_health 会话的 sp_server_diagnostics 组件。这套自诊断在 2012 是新面孔，其思想与"看门狗+心跳"通用机制同构 ⚠️。

### 5. IO：8KB 页是一切的原罪
缓冲池按页工作，日志按扇区(512B)单位写、按虚拟日志块(VLF)管理——第 03 章细讲；数据文件增长、交错写策略都要回到"页 + 分配单元"的世界观(02/04 章) ⚠️。✅ 现代准绳：Pages and Extents Architecture Guide https://learn.microsoft.com/en-us/sql/relational-databases/pages-and-extents-architecture-guide 。

## 🔧 类比实验（本章无独立实验）

本章为"总纲+地基"性质，类比实验落在下游文件：页与文件头见 [02-数据库与数据库文件.md](02-数据库与数据库文件.md) 的 E1；等待/资源竞争语义无法用 SQLite/DuckDB 诚实类比（两者无服务器调度器/内存 broker 概念），如实留 ⚠️（共通规范"不能类比如实 ⚠️"条款）。

## 本章结论速记

- 关系引擎/存储引擎二分 + 火山行流是全书目录学。
- SQLOS 存在的理由：对象感知内存、协作式调度、统一 IO/等待记账。
- 排障从等待类型入手：那是 SQLOS 给 DBA 的"系统调用号表"。
- NUMA 敏感是 2012 起的部署第一课；虚拟化层要如实呈报拓扑。
- 8KB 页假设贯穿存储、日志、备份、索引一切下游章节。

## 常见误区（转述 ⚠️）

| 误区 | 事实 |
| --- | --- |
| "SQL Server 就是跑在 Windows 上的单体" | 其上有自管内存/调度/IO 的 SQLOS 层，OS 视角看到的往往"不准" |
| "内存吃满=泄漏" | 缓冲池按设计"闲置内存即浪费"，先看 PLE/目标内存再看进程 RSS |
| "等待统计=病因" | 等待是症状，需汇聚到资源(内存/CPU/IO/锁)四象限再下结论 ⚠️ |
| "并行总更快" | Exchange 算子与调度开销在短查询上净亏(07 章呼应) ⚠️ |
| "vNUMA 无所谓" | 2012+ 拓扑盲从会放大跨节点内存访问 ⚠️ |

## 与其他章/其他笔记的联系

- 上承：本册 [00-总览与阅读地图.md](00-总览与阅读地图.md) 谱系与辨析声明。
- 下启：页/扩展区 → [04-表存储.md](04-表存储.md)；缓冲池脏页与检查点 → [03-日志与恢复.md](03-日志与恢复.md)；内存授予 → [07-查询执行优化与计划缓存.md](07-查询执行优化与计划缓存.md)。
- 横向：#36 的 [../Pro_SQL_Server_Internals/00-总览与阅读地图.md](../Pro_SQL_Server_Internals/00-总览与阅读地图.md) 无 SQLOS 专章（工程向略过），两家互补；通用内核视角(单进程/线程池/缓冲管理)对照 [../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md) 与 [../数据库系统概念6.md](../数据库系统概念6.md) 存储管理章。

## 转述扩写：SQLOS 四大子系统细目（⚠️ 转述，非作者口径）

### 内存子系统的"单位经济学"
- 分配粒度：内存以 8KB 页为对象、以 64KB 大块(extent 对齐)为单位向 OS 伸手——与数据页/扩展区同构，SQLOS 把"页哲学"用到了 RAM 上 ⚠️。
- clerk 视角：缓冲池、执行计划缓存、锁管理器、句柄表……每个消费方登记自己的"账房"，broker 在压力下按"用页多者先出血"谈判；目标内存每几分钟重算 ⚠️。
- 两个极端旋钮：min/max server memory 决定谈判底线；低内存时最先遭殃的往往是计划缓存(07 章的"缓存驱逐"伏笔) ⚠️。
- eager writer：后台把日志改脏的页尽快刷回，防止"检查点风暴"——它同时是 03 章恢复时间预算的隐藏变量 ⚠️。

### 调度子系统的"三级账"
- scheduler(绑定逻辑 CPU)→worker(执行上下文)→task(一次请求)：请求在队列里等的是 worker，worker 在 scheduler 上等的是让出点 ⚠️。
- 非让出检测三档(suspect/severe)：sp_scheduler 心跳 + dump 生成；这是"SQL 卡死但服务没挂"事故的第一现场 ⚠️。
- 并行 worker 预算：max worker count 与"每个并行查询预扣线程"的账——2012 时代"线程饥饿 RESOURCE_SEMAPHORE_QUERY_COMPI"类等待的根源层 ⚠️。

### IO 子系统的"页对齐洁癖"
- 所有读写按 8KB 页、日志按 512B 扇区(当时硬件口径)——torn page 风险由此不对称产生(03 章呼应) ⚠️。
- 异步 IO 经完成端口收敛到 SQLOS：一次 IO 的一生=等待类型 PAGEIOLATCH_SH/EX 的一生 ⚠️。
- 交错单元 256KB：文件跨盘条带化时"每文件一个逻辑盘"的假设——书中给 SAN 布局的告诫(数字细节 ⚠️ 转述)。

### 异常与自诊断
- 引擎内 try/except 包装非托管代码；崩溃路径写 mini-dump + error log 双证据 ⚠️。
- sp_server_diagnostics + query_processing 等组件：2012 起"系统自己的 XE 会话"思想成形(细节 ⚠️)。

## 排障视角速查（等待四象限，⚠️ 转述 + ✅ 文档）

| 象限 | 代表等待 | 本章对应子系统 |
| --- | --- | --- |
| CPU | SOS_SCHEDULER_YIELD | 调度(让出/线程压力) |
| 内存 | RESOURCE_SEMAPHORE(_QUERY_COMPILES) | broker/clerk/计划缓存 |
| IO | PAGEIOLATCH_* / WRITELOG | 缓冲池/IO 栈/日志 |
| 锁/其他 | LCK_M_* / CXPACKET | 08 章/07 章并行 |

✅ 现代准绳：sys.dm_os_wait_stats https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-os-wait-stats-transact-sql 。

## 核心概念速览（中英对照）

1. **关系引擎** — Relational Engine：解析/优化/执行查询的一半，与存储引擎以行流接口为界 ⚠️。
2. **存储引擎** — Storage Engine：页、索引、日志、缓冲池的世界，本册 02–06 章的主题 ⚠️。
3. **SQLOS** — SQL Server Operating System：内嵌的内存/调度/IO 资源管理层 ⚠️。
4. **内存代理** — Memory Broker：按 clerk 记账并动态调配内存的组件 ⚠️。
5. **缓冲池** — Buffer Pool：数据页的内存副本缓存，脏页等待检查点/日志机制处理 ⚠️。
6. **NUMA** — Non-Uniform Memory Access：远近内存延迟差异；2012 起一等调度对象 ⚠️。
7. **协作式调度** — Cooperative Scheduling：worker 主动让出 CPU，配合非让出检测 ⚠️。
8. **等待类型** — Wait Type：SQLOS 对"任务卡在哪"的标准化词表 ✅(dm_os_wait_stats 文档)。
9. **DAC** — Dedicated Admin Connection：资源耗尽时的兜底诊断连接 ⚠️。
10. **system_health** — 系统健康会话：常驻 Extended Events 会话，收录调度异常等 ⚠️。
11. **页与扩展区** — Pages and Extents：8KB 页、64 页扩展区的分配原语 ✅(Learn 架构指南)。
12. **火山模型** — Volcano/Iterator Model：算子逐行拉取的执行范式，本册 07 章对比列存批处理 ⚠️。
13. **mini-dump** — 小型转储：崩溃/可疑状态的轻量现场记录 ⚠️。
14. **条带与交错** — Striping and Interleaving：多文件平行摆放 extent 以摊薄 IO 热点 ⚠️。

## 最新演进与工业实践

- **2012→2019**：内存粒度从 8KB 页走向"Hekaton 无页表"(✅ 文档 https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/overview-and-usage-scenarios ，论文线 [../../db/Hekaton.md](../../db/Hekaton.md) )；缓冲池扩展(BCPE)2014 短暂上线后 2019 移除 ⚠️ 转述。
- **Linux 化 = SQLOS 的第二生命（重大演进）**：2017 SQL Server on Linux GA 把 SQLOS 的调度/内存/IO 语义移植到 Ubuntu/RHEL 内核上（"sqlservr paldumper" 等痕迹），页仍是 8KB——✅ 概览 https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-overview 。本章"再造 OS"的论证在 Linux 版上获得最强实证：同一层抽象换了宿主 OS。
- **2025 现状**：SQL Server 2025（官方 what's new ✅ https://learn.microsoft.com/en-us/sql/sql-server/what-s-new-in-sql-server-2025 ）头版特性即**容器/Kubernetes 部署（预览路线）**与向量检索——SQLOS 话题进化为"资源治理与容器 CPU/内存配额如何映射到内存 broker"⚠️ 转述；学习版/Azure SQL 的弹性伸缩把"配额是架构第一约束"变成云侧计费现实。
- **工业实践口径**：现代排障仍以等待统计为第一入口（dm_os_wait_stats + sp_WhoLock/blitz 系开源工具 ⚠️ 点名不引数据）；虚拟化部署 checklist 仍含 vNUMA 如实透传——2012 时代结论未被推翻。
- **系列对位**：本章的"引擎分层+OS 层"叙事与 [../DuckDB_in_Action/00-总览与阅读地图.md](../DuckDB_in_Action/00-总览与阅读地图.md)（嵌入式、无 SQLOS 对应物、单进程内全自管）互为镜像——嵌入式与服务器式资源模型的对照是本册给系列读者的思考题。
