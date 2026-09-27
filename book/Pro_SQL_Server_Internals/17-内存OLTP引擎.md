# 第 32–33 章 · 内存 OLTP 引擎：Hekaton 内核与编程面（In-Memory OLTP Internals / Programmability）

> 原书位置：Chapter 32 "In-Memory OLTP Internals"（页 649–688，官方目录排 Part 7）+ Chapter 33 "In-Memory OLTP Programmability"（页 691–707，官方目录排 Part 8 题头之后 ⚠️ 目录排版怪癖已在 00 注明）（✅ Crossref 子 DOI ..._32 / ..._33）。
> 小节标题逐字官方（✅ front-matter 实抓）；正文为精读重构转述；SQL Server 本机不可运行，机制结论一律「转述 + ⚠️」，全章零 🔧。
> 论文层原理见 [../../db/Hekaton.md](../../db/Hekaton.md)（Diduri 等人的 VLDB 2014 论文笔记），本章文件是它的工程化对照。

## 本章地图

| 官方小节（✅） | 章 | 转述要点 | 一句话结论 |
| --- | --- | --- | --- |
| Why Hekaton? | 32 | 磁盘引擎的三重税：闩锁（页）、锁（行）、日志（每改必录）；内存引擎以"无页无锁+编译执行"拆税 | 为 OLTP 热循环重写引擎 ⚠️ |
| Engine Architecture and Data Structures | 32 | 总览：容器（container）+桶数组索引+行指针；无 B 树无页 | 一切皆内存结构 ⚠️ |
| Memory-Optimized Tables | 32 | SCHEMA_AND_DATA / SCHEMA_ONLY 持久档；无聚簇概念，索引全 NONCLUSTERED 内存型 | 先定 durability ⚠️ |
| High-Availability Technology Support | 32 | 内存表随库备份/镜像/AG 走的边界（书载 2014 限制清单 ⚠️） | HA 面有暗礁 ⚠️ |
| Data Row Structure | 32 | 行=定长槽+变长列尾指针；行不迁移、更新即新行（MVCC）；无页对齐开销 | 行住在堆里 ⚠️ |
| Hash Indexes | 32 | 定长桶数组、等值命中、桶链长统计（bucket_count 估算与 REBUILD 演化 ⚠️ 书演示） | 无 ORDER、快等值 ⚠️ |
| Range Indexes | 32 | 跳表（skiplist）多指针塔结构：范围+有序扫描+等值；写入成本高于 hash | 有序靠跳表 ⚠️ |
| Statistics on Memory-Optimized Tables | 32 | 内存优化表统计由引擎自动维护（默认采样行为 ⚠️ 转述） | 优化器也要吃内存账 ⚠️ |
| Garbage Collection | 32 | 版本不可见后入回收队列、gc 线程后台复用；长事务拖住 gc（接 13 版本存类比）⚠️ | 内存的 VACUUM ⚠️ |
| Transactions and Concurrency | 32/33 | 无锁：时间戳+版本可见性判定；隔离仅限 RC/SI/SERIALIZABLE 三档（SI 为快照语义但实现不同 ⚠️）；写写冲突直接牺牲 | 锁没了，规则换了 ⚠️ |
| Cross-Container Transactions | 32 | 内存表×磁盘表混合事务：日志双轨、边界条件清单（书中列升级/死锁不可测等限制 ⚠️） | 跨容器有税 ⚠️ |
| Data Access, Modifications, and Transaction Lifetime | 32 | 时间戳分配、提交序列、可见性判定的完整流程（书以时序图 ⚠️ 转述） | 提交=盖章 ⚠️ |
| Transaction Logging | 32 | 只有提交时合并日志流（无 undo、逐语句日志）；checkpoint 文件+日志再重建（接 16 恢复叙事）⚠️ | 日志变精简 ⚠️ |
| Data Durability and Recovery | 32 | 重启沿日志重放+索引重建；SCHEMA_ONLY 走快线但崩即丢 ⚠️ | 内存也能 crash-consistent ⚠️ |
| Memory Usage Considerations | 32 | 内存表占多核/行开销/索引额外 8B 指针量级；容量规划与"别超卖"警告 ⚠️ | 预算制 ⚠️ |
| Native Compilation | 33 | natively compiled 模块：T-SQL→C→机器码；无解释开销、无行上下文切换 | 编译执行 ⚠️ |
| Natively-Compiled Stored Procedures | 33 | 两代形态（900ms 类书载限制/不支持特性清单 ⚠️）+优化（迭代/集合限制） | 快但有语法牢笼 ⚠️ |
| — Supported T-SQL Features / Execution Statistics | 33 | 支持面清单与 sys.dm_db_xtp_* 执行统计取证（书以 DMV 为工具箱 ⚠️） | 可观测配套 ⚠️ |
| Interpreted T-SQL and Memory-Optimized Tables | 33 | 混合执行：解释 T-SQL 访问内存表（2014 可用但代价=跨引擎边界 ⚠️）；后续版本"互操作编译"演进 | 不必全编译 ⚠️ |
| Memory-Optimized Table Types and Variables | 33 | 内存优化 TVP/表变量：tempdb 争用的正交解法（接 08/13 版本存 ⚠️） | tempdb 进内存 ⚠️ |
| In-Memory OLTP: Implementation Considerations | 33 | 落地清单：选表（热/短事务/无 FK 深链）、改写（游标/动态 SQL 雷区）、灰度与回退 | 迁移是手术 ⚠️ |

## 核心精讲（转述 + ⚠️）

### 无锁并发的机制本质
书中解释 Hekaton 事务靠**行内时间戳+全局提交序列**做可见性判定（转述 ⚠️）：每行带创建/删除事务戳，读者按快照戳扫版本链——这替代了锁与版本存储两件事。冲突检测只剩"写写"一类；牺牲者在写冲突时直接收到错误而非排队。SERIALIZABLE 依赖谓词范围记录（与磁盘引擎的 KEY-Range 实现不同 ⚠️）。第 13 章的"转换等待死锁"在内存表上结构性消失——这正是书给它的宣传点 ⚠️。

### 索引即内存结构
Hash 索引=桶数组+单向行链：等值 O(1)、无排序、删除后桶链不自动收缩——书中演示 bucket_count 估低导致长链、以及 ALTER REBUILD 改桶数（转述 ⚠️）。Range（跳表）：多层前向指针塔，查找 O(log n) 近似、支持范围与有序，但每插入要动多指针。两型皆 NONCLUSTERED（书特别澄清"非聚簇"在 Hekaton 里只是"附加索引"的历史命名 ⚠️），主键必须有一个内存索引（hash 或 range）兜底。

### GC 与"长事务债"
被更新/删除的旧版本在"没有任何未来快照可能看见"后进入垃圾队列，由后台 GC 线程按依赖（索引→表）顺序回收（转述 ⚠️）。一个挂起的打开事务/泄漏连接=版本滞留=内存只涨不跌——13 章"保留线"叙事的内存翻版。书给的观测工具：dm_db_xtp_gc_* 队列深度 ⚠️。

### 日志与恢复的反直觉
内存表的日志**只在提交时写合并记录**（无 undo、无逐语句 redo 单元），恢复=按序重放提交记录重建行+重建索引；checkpoint 把重放起点前移（书中机制 ⚠️，与 [../../db/ARIES.md](../../db/ARIES.md) 的 ARIES 对照：Hekaton 干脆绕开了 redo/undo 范式）。SCHEMA_ONLY 表完全不写数据日志——ETL 暂存新贵、崩了就丢 ⚠️。

### 编程面的得与失（33 章主线）
原生编译过程：循环/分支/聚合编译为机器码，书中转述基准"热循环 10–30 倍"（⚠️ 书载口径，非本机实测）。代价：2014 支持面窄（无 OFFSET/FETCH、无 TRY/CATCH 细节差异、集合语句限制等清单 ⚠️ 以书列为准）、变更需重编译部署、调试弱。书的务实路线：只编译热点写入路径（事件摄取/库存扣减），其余留解释 T-SQL+内存表 ⚠️。内存优化表变量/TVP 直击 08 章 tempdb 热点：参数传递零日志、销毁即回收 ⚠️。

## 本章结论速记

- Hekaton=对闩锁/锁/日志三重税的重写：内存结构+时间戳 MVCC+编译执行。
- Hash 快等值、Range 管有序；桶数是唯一要养的参数。
- 无锁不等于无冲突：写写直接牺牲，隔离只剩三档。
- GC 的保留线由最老快照决定——长事务仍是一切之敌。
- 日志只记提交，恢复靠重放；SCHEMA_ONLY 换速度弃持久。
- 编程面：只编译最热的，混用是常态不是妥协。
- 内存索引选型只有两个问题：这查询是等值还是范围、桶链现在多长。

## 工程模式与常见误区

| 误区 | 事实（转述 ⚠️） |
| --- | --- |
| "内存表=把所有表搬进内存" | 容量/恢复/GC 预算只对热循环划算；书的筛选标准：高频短事务+索引等值为主 ⚠️ |
| "hash 桶一次定终身" | 估低=长链退化；书演示带数据迁移的 REBUILD 修正 ⚠️ |
| "无锁=无阻塞" | 写写冲突以报错形式现世；重试逻辑要换错误号 ⚠️ |
| "natively compiled 一律快 30 倍" | 收益集中在循环内；IO-bound 语句编译了也白编译 ⚠️ |
| "SCHEMA_ONLY 可当缓存随便用" | 崩溃/故障转移即清空；语义=易失缓存要设计失陷路径 ⚠️ |
| "FK/触发器照旧" | 内存表约束面 2014 有缺项（书列 ⚠️），迁移前先过检查清单 |
| "索引数按磁盘表习惯三五条起步" | 每条内存索引都是写路径上的桶/链维护；书的选型极简：等值 hash、范围 range，主键一条兜底通常够 ⚠️ |
| "natively compiled 里 TRY/CATCH 照写" | 2014 支持面残缺（书列错误处理清单 ⚠️）需退回返回码老式；后续版本逐年放宽，跨版本迁移要重查官方清单 |

## 机制链条

```
DML（natively compiled proc）
   ▼
行分配（内存堆）+ 时间戳盖戳 ──▶ 索引入链（hash 桶 / 跳表）
   ▼
提交：取全局戳 → 合并日志记录落盘（无逐语句日志 ⚠️）
   ▼
旧版本不可见 → GC 队列 → 后台回收复用
   ▼
崩溃恢复：checkpoint + 日志重放 → 行与索引全重建（SCHEMA_AND_DATA）
```

## 与其他章 / 其他笔记的联系

- 锁/版本存储/隔离的"旧世界"对照：[12-锁类型阻塞与死锁.md](12-锁类型阻塞与死锁.md)、[13-乐观并发应用锁与模式锁.md](13-乐观并发应用锁与模式锁.md)。
- tempdb 版本存与内存优化表变量的替代关系：[08-XML与临时表.md](08-XML与临时表.md)。
- 日志/恢复模型对照（WAL 精简版）：[16-事务日志备份与高可用.md](16-事务日志备份与高可用.md)。
- 编译执行 vs 火山/批模式：[14-查询优化执行与计划缓存.md](14-查询优化执行与计划缓存.md)；列存批模式并列第三路线：[18-列存储索引.md](18-列存储索引.md)。
- 论文原理与工业实现对照：[../../db/Hekaton.md](../../db/Hekaton.md)、[../../db/db.md](../../db/db.md)；同代内存数据库谱系（H-Store/HyPer 一系）见 [../../db/HyPer.md](../../db/HyPer.md)。
- MVCC 可见性判定的跨引擎对照（PG 行内 xmin/xmax 路线，与本版"时间戳+提交序列"互读）：[../../db/mvcc.md](../../db/mvcc.md)。
- 同谱系深化：Expert SQL Server In-Memory OLTP（2015/2017，DOI 见 [00 版本史](00-总览与阅读地图.md)）。

## 核心概念速览（中英对照）

1. **内存优化表** — Memory-Optimized Table：无页容器常驻内存的表族。
2. **容器** — Container：行分配池（与文件组绑定）。
3. **桶数** — Bucket Count：哈希索引数组长度，需按行数量级估计。
4. **跳表** — Range Index/Skiplist：多指针塔有序内存结构。
5. **时间戳 MVCC** — 无锁并发：以版本可见性替代锁排队。
6. **写写冲突** — Write-Write Conflict：内存表的唯一阻塞形态（直接报错）。
7. **垃圾回收** — GC：不可见版本异步回收，依赖链排序。
8. **SCHEMA_AND_DATA / SCHEMA_ONLY** — 两档持久性。
9. **合并日志** — Logging at Commit：只记提交记录，恢复靠重放。
10. **原生编译** — Native Compilation：T-SQL→机器码模块。
11. **互操作（interop）** — 解释 T-SQL 访问内存表的边界路径。
12. **内存优化表变量/TVP** — tempdb 的内存替代。
13. **跨容器事务** — Cross-Container：内存×磁盘混合事务。
14. **谓词范围记录** — Hekaton 的 SERIALIZABLE 防幻读实现面（与磁盘引擎 KEY-Range 不同路 ⚠️）。
15. **双轨提交** — 跨容器事务的两套日志路径与两阶段收口（书载限制与代价 ⚠️）。

## 最新演进与工业实践

- **持久化内存（PMEM）路线兴衰**：2017/2019 曾提供内存表驻留 PMEM 的 fast-durability 选项；2024+ Optane 停产、该线收缩——"纯 DRAM+日志重放"仍是主形态 ⚠️（趋势性描述，[内存优化表简介](https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/introduction-to-memory-optimized-tables) ✅）。
- **限制面持续收窄**：2016 放宽列宽/索引数/FK 与触发器支持、2017 起互操作自动本机化（interop natively compiled）、原生编译限制清单逐年缩短（[事务与内存优化表](https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/transactions-with-memory-optimized-tables) ✅、[本机编译存储过程](https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/natively-compiled-stored-procedures) ✅ 各页含版本注记）。
- **Azure 侧的镜像**：Azure SQL 的 In-Memory OLTP 曾长期缺席、后部分回归（记忆优化表可用面 ⚠️ 以官方版次矩阵为准）；Hyperscale 用架构手段（内存化页缓存）达成类似"热数据在内存"目标，路线分化 ⚠️。
- **工业现状**：2024–2026 的部署热点=事件摄取/高频账务/会话存储的"窄表+编译过程"三件套；本书 33 章的"只编译最热路径"策略仍是主流剧本（模式性描述 ⚠️）。
- **作者后续书**：Korotkevitch《Expert SQL Server In-Memory OLTP》（2015/2017，✅ Crossref，DOI 见 [00 版本史](00-总览与阅读地图.md)）把这两章拆成整卷，深入 GC/索引/迁移案例——本章文件是其"目录版前传"。
- **GC 专页缺口声明（二轮）**：官方"内存优化 OLTP 的垃圾回收"专页候选路径本轮 curl 实测 404（疑随 PMEM 文档线重组）——GC 依赖链与队列观测的口径继续以书+同谱系 Expert 卷转述为准 ⚠️，勿引二手博客。
- **隔离与冲突错误号现行页**：Hekaton 三档隔离、写写冲突错误面的官方文本复用已验证页 [事务与内存优化表](https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/transactions-with-memory-optimized-tables) ✅；2025 侧互操作自动本机化的默认行为 ⚠️ 以版本发布页为准（[2025 新特性](https://learn.microsoft.com/en-us/sql/sql-server/what-s-new-in-sql-server-2025) ✅）。
