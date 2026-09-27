# 第 11–12 章 · XML 与临时表（XML / Temporary Tables）

> 原书位置：Part 2 · Chapter 11（页 209–232）+ Chapter 12（页 233–254）（✅ Crossref 子 DOI ..._11 / ..._12）。
> 小节标题逐字官方（✅ front-matter 实抓）；正文为精读重构转述；机制结论一律 ⚠️。

## 本章地图

| 官方小节（✅） | 章 | 转述要点 | 一句话结论 |
| --- | --- | --- | --- |
| To Use or Not to Use XML? | 11 | 三选一：EAV、宽表/稀疏列、XML——按"结构稳定 vs 属性未知"决策；XML 当"影子关系表"看 | 先问形状再选载体 ⚠️ |
| XML Data Type | 11 | 类型化（schema collection，XML 校验器）vs 非类型化；document vs content；存储为拆分的二进制森林 + LOB 树（接 01） | XML 不是字符串 ⚠️ |
| Working with XML Data（value/exists/query/nodes/modify） | 11 | 五方法各有代价：nodes() 做行展开（shredding）、存在性用 exists()、取标量用 value()、原地改 modify() | 用错方法=整树重解析 ⚠️ |
| OPENXML | 11 | 旧的行集物化接口（xml document + 映射），逐步被 nodes() 取代 | 兼容层 ⚠️ |
| FOR XML | 11 | RAW/PATH/AUTO/EXPLICIT/BINARY 模式序列化查询为 XML | 出方向工具 ⚠️ |
| Temporary Tables | 12 | #本地/##全局；建在 tempdb、按会话命名后缀；支持索引/统计/参与事务与编译复用 | 临时表=有统计的小表 ⚠️ |
| Table Variables | 12 | @tv 内存对象语义：无统计、日志少（只在销毁时）、不参与编译级联——书中告诫"大结果集别用它" | 便利但估算失明 ⚠️ |
| User-Defined Table Types / TVP | 12 | 表作为参数批量入存储过程：替代逐行调用与 IN 列表 | 批量接口正解 ⚠️ |
| Regular Tables in tempdb | 12 | tempdb 内普通表跨会话共享：比持久表便宜但无统计优化红利 ⚠️ | 第三形态 ⚠️ |
| Optimizing tempdb Performance | 12 | 多文件均摊分配、按 CPU 配 1:1 文件（当时建议 ⚠️）、-T1118 混合区策略、内存优化临时对象（2016+）| tempdb 是隐形瓶颈 ⚠️ |

## 核心精讲（转述 + ⚠️）

### XML 的存储与索引双层
书中把 XML 拆成三层讲：物理（LOB 树 + 二进制森林/节点表形态 ⚠️ 转述）、逻辑（document/content、类型化挂 XSD）、访问（主 XML 索引=把影子关系表物化；次级索引 PATH/VALUE/PROPERTY 三种各有适用查询形态）。工程结论（转述）：查询集中在少数热点列时才值得索引；否则"解析全树"仍是主成本 ⚠️。

### shredding 与"影子表"思维
`CROSS APPLY col.nodes('/X/Y')` 把 XML 展成行集再 join——等价于隐式 EAV 查询。书的立场：如果 XML 里某字段被高频过滤，就"提取成持久化计算列 + 索引"（接 04），让 XML 只承担装填 ⚠️。

### 临时对象三种形态的选择函数（第 12 章主线）
- 行数少（几十）+ 会话内：表变量（无统计但无重编译风暴——2005 时代旧账，书中对比 ⚠️）。
- 行数大/需要索引统计/复杂计划：#临时表。
- 跨会话缓冲 + 高吞吐装载：tempdb 普通表（如 ETL 中转）。
- 批量入参：TVP（消灭逐行 RPC 与长 IN 列表）。
书中给出 tempdb 热点页（PFS/GAM/SGAM，接 01）在高并发临时表场景的争用画像与多文件对策 ⚠️。

### XML 索引三件套的适用查询形态（转述 ⚠️）
主 XML 索引物化全部节点后，次级索引按查询形态分三种：**PATH**（`/a/b/text()` 这类路径定位+属性存在性）、**VALUE**（`//b[@x=1]` 这类只认值不认路径）、**PROPERTY**（已知元素/属性名取标量的等值）。书给的选择函数：查询含完整路径→PATH；跨路径找值→VALUE；混合高频取列→PROPERTY。都建=存储翻倍；不建主索引=次级索引无从谈起 ⚠️。

## 本章结论速记

- XML 是被低估的"引擎内半结构化列存"；用不好就是解析税。
- 主 XML 索引=影子表物化；热点字段应提取为列。
- 临时对象按"行数 × 是否需要统计 × 生命周期"三轴选型。
- TVP 是 ORM 与批量装载的标准接口。
- tempdb 文件数与混合区策略是 2014 运维第一课。

## 工程模式与常见误区

| 误区 | 事实（转述 ⚠️） |
| --- | --- |
| "XML 列=存字符串" | 类型化 XML 带 XSD 校验与二进制森林，直接 CAST 比较无意义 ⚠️ |
| "exists() 慢用 query()" | 存在性用 exists 最省；query 拉整片段 ⚠️ |
| "表变量无日志所以快" | 无统计的估算失真在联查时更致命 ⚠️ |
| "临时表用完自动没事" | 会话池复用（连接池）让清理滞后；显式 DROP 是好风味 ⚠️ |
| "tempdb 默认 1 文件够用" | 并发下分配映射页争用；按芯加文件（当年口径 ⚠️） |
| "TVP 可当索引随便建" | 只读入参，不能建索引（限制细节 ⚠️ 以官方为准） |
| "tempdb 只在开发用" | 它同时服务临时对象/版本存储/排序溢出三条线，容量与延迟是全局账 ⚠️ |
| "nodes() 会改原列" | 查询方法只读；原地更新只有 modify()，且它按引用改内部树 ⚠️ |

## 机制链条

```
XML 列 ──写入──▶ XSD 校验（类型化）──▶ 二进制森林/LOB 树
   │主索引=节点全物化──▶ PATH/VALUE/PROPERTY 次级索引按查询形态补
查询：value()/exists() 标量与存在性 | query() 片段 | nodes() 展平 join | modify() 原地
临时对象：#表(tempdb, 有统计) | @tv(无统计, 轻日志) | TVP(只读批参) | tempdb 普通表(跨会话)
   └──高并发创建/销毁──▶ tempdb 分配图页(PFS/GAM/SGAM)争用 ──▶ 多文件均摊 ⚠️
```

## 延伸转述：书中判断力小题（转述 + ⚠️，非原书逐字）

1. **问**：取一个标量用 query() 还是 value()？
   **答**：value()——返回 SQL 标量且单值保证；query() 返回 XML 片段还得再拆 ⚠️。
2. **问**：判断存在性怎么写最省？
   **答**：exists() 短路求值；别用 query().exist 之外的"取出来再判空" ⚠️。
3. **问**：XML 列能直接进 JOIN 吗？
   **答**：可以但按二进制序列化比较，几乎从不是你想要的语义——正确姿势是 shredding 或提取列 ⚠️。
4. **问**：临时表为什么可能引发计划重编译风暴？
   **答**：每会话各建各的、统计各异，共享计划反复失效（书的时代分析 ⚠️；对象定义变化触发重编译机制）。
5. **问**：表变量何时反而比 # 表稳？
   **答**：极小行数+避免重编译抖动时"估算失明"无伤大雅；大行数控件下统计压倒一切 ⚠️。
6. **问**：TVP 传 10 万行会发生什么？
   **答**：入参只读、无统计→下游估算按默认值；书中路线是超阈值先落 # 表再 join ⚠️。
7. **问**：tempdb 里建普通表何时合理？
   **答**：跨会话共享的 ETL 中转/全局暂存；要自担清理与并发命名冲突 ⚠️。
8. **问**：-T1118 与多文件谁先上？
   **答**：先多文件均摊（书中 1:1 CPU 起步口径 ⚠️ 后时代收敛为 4+8 经验），1118 视争用画像再加。
9. **问**：# 表加索引值得吗？
   **答**：行数大+被反复查询时值得；它同样吃 tempdb IO 与统计维护 ⚠️。
10. **问**：临时表和表变量谁写日志？
    **答**：都写（undo/redo 都有），"表变量少日志"是误解其销毁时机语义——书专门纠偏 ⚠️。
11. **问**：XML 能当文档数据库用吗？
    **答**：能存能查，但事务与索引粒度和今天 JSON/外部文档库不可同日而语（演进见下节 ⚠️）。

## 与其他章 / 其他笔记的联系

- LOB 物理层与溢出页：[01-数据页与数据存储内部结构.md](01-数据页与数据存储内部结构.md)。
- 计算列提取热点：[04-特殊索引与存储特性.md](04-特殊索引与存储特性.md)。
- tempdb 争用等待画像：[15-系统排查与扩展事件.md](15-系统排查与扩展事件.md)、[12-锁类型阻塞与死锁.md](12-锁类型阻塞与死锁.md)。
- 版本存储也用 tempdb（行版本化）：[13-乐观并发应用锁与模式锁.md](13-乐观并发应用锁与模式锁.md)。
- 数据装载与 ORM 批处理语境：[11-系统设计考量.md](11-系统设计考量.md)。
- 跨引擎对照：MySQL 临时表/temptable 引擎（[../MySQL技术内幕_InnoDB存储引擎2.md](../MySQL技术内幕_InnoDB存储引擎2.md)、[../高性能mysql.md](../高性能mysql.md)）、PG TemporalTables 与 TOAST 的半结构化对照（[../PostgreSQL数据库内核分析.md](../PostgreSQL数据库内核分析.md)）。

## 核心概念速览（中英对照）

1. **EAV** — Entity-Attribute-Value：竖表建模法，XML 的竞争形态之一。
2. **类型化 XML** — Typed XML：绑定 XML schema collection、写入即校验。
3. **文档/内容** — Document / Content：单根 vs 片段两种实例形态。
4. **二进制森林** — Binary Forest：XML 拆成的关系式节点表。
5. **主 XML 索引** — Primary XML Index：全节点物化（影子表）。
6. **次级 XML 索引** — Secondary XML Index：PATH / VALUE / PROPERTY 三型。
7. **展平** — Shredding：nodes() 把树变行集。
8. **FOR XML** — 序列化模式：RAW/PATH/AUTO/EXPLICIT/BINARY。
9. **本地临时表** — Local Temp Table (#)：会话私有、tempdb 物化、带统计。
10. **表变量** — Table Variable (@)：轻量表对象，无统计。
11. **表值参数** — TVP / UDTT：批量入参的用户定义表类型。
12. **tempdb 多文件** — Multiple tempdb Files：均摊 GAM/SGAM/PFS 争用。
13. **XQuery** — XML 查询语言族：FLWOR 式路径表达式（value/query/exists 的底层）。
14. **延迟清理** — Deferred Drop：临时对象随会话/池复用的滞后消失现象 ⚠️。

## 最新演进与工业实践

- **JSON 全面上位**：SQL Server 2016 引入 JSON、2017 OPENJSON 索引友好；2024–2026 的现实是"半结构化列默认 JSON，XML 守存量集成（SSIS/ADO.NET 遗留面）"（[2022 新特性](https://learn.microsoft.com/en-us/sql/sql-server/what-s-new-in-sql-server-2022) ✅；2025 的 JSON 增强条目名 ⚠️ 逐字未录）。
- **tempdb 智能化**：SQL Server 2016 起安装默认按芯配 tempdb 文件、-T1118 默认化；2019+ 提供**内存优化临时表**（MEMORY_OPTIMIZED=ON，消除日志与闩锁热点）——本章运维建议大半已被产品内置（[tempdb 数据库](https://learn.microsoft.com/en-us/sql/relational-databases/databases/tempdb-database) ✅）。
- **表变量估算修复**：2019 的表变量延迟编译（TVM delayed table variable）+ 内联家族（IQP）显著削弱本章"表变量禁忌" ⚠️ 兼容级相关（[IQP](https://learn.microsoft.com/en-us/sql/relational-databases/performance/intelligent-query-processing) ✅）。
- **TVP 的后继面**：批量写入更多走 SqlBulkCopy/ADF/Pollyfill 之外的 REST/Parquet 通道；TVP 仍是存储过程批处理的标准姿势 ⚠️（共识性描述）。
- **tempdb 的云上终局**：Azure SQL 中 tempdb 本地 SSD 托管、自动配文件，本章运维项对 SaaS 化用户基本消失（[Hyperscale 架构](https://learn.microsoft.com/en-us/azure/azure-sql/database/hyperscale-architecture) ✅）。
