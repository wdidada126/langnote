# 第 13–14 章 · CLR 集成与自定义类型（CLR / CLR Types）

> 原书位置：Part 2 · Chapter 13 "CLR"（页 255–273）+ Chapter 14 "CLR Types"（页 275–300）（✅ Crossref 子 DOI ..._13 / ..._14）。
> 小节标题逐字官方（✅ front-matter 实抓）；正文为精读重构转述；SQL Server 本机不可运行，机制结论一律「转述 + ⚠️」，全章零 🔧。

## 本章地图

| 官方小节（✅） | 章 | 转述要点 | 一句话结论 |
| --- | --- | --- | --- |
| CLR Integration Overview | 13 | 引擎内托管宿主：程序集注册（CREATE ASSEMBLY）→ T-SQL 对象映射（过程/函数/触发器/UDT/聚合）；三种信任集 | CLR=把 .NET 缝进进程内 ⚠️ |
| Security Considerations | 13 | SAFE / EXTERNAL_ACCESS / UNSAFE 三档权限集；SAFE 仍需 db_owner 以上批准（sa/dbo 权限面 ⚠️ 转述）；UNC 路径与证书签名两条外访问路线 | 信任级先于性能想 ⚠️ |
| Performance Considerations | 13 | 首次调用冷启动（AppDomain 装载）、解释调用与 T-SQL↔CLR  marshal 成本、内存占用不归 BP 管辖；聚合/字符串处理是甜点，行级 OLTP 热路径是雷区 | 托管优势只在计算密集处 ⚠️ |
| User-Defined CLR Types | 14 | UDT=最大 8060 字节的结构化工件：属性/方法/序列化（Binary 或 Native）；可建持久化计算列与索引 | 类型也能编程 ⚠️ |
| Spatial Data Types | 14 | geometry（平面）与 geography（椭球）即内置 CLR 类型的官方示范；空间索引走网格（Grid/Tiles）切分 | 空间=UDT 的样板房 ⚠️ |
| HierarchyId | 14 | 变长二进制编码的树路径（如 /1/3/1/），GetDescendant 写、IsDescendant 读；深度与键宽成反比博弈 | 树形数据的引擎内编码 ⚠️ |
| Summary | 13/14 | 两章收口：CLR 是"能用但慎能"的扩展面，默认关闭（clr enabled=0） | 默认关=官方态度 ⚠️ |

## 核心精讲（转述 + ⚠️）

### CLR 宿主的生命周期（第 13 章主线）
书中把 CLR 集成拆成四拍（转述 ⚠️）：① 编译 .NET 程序集 → ② `CREATE ASSEMBLY` 把 DLL 字节流存进数据库（程序集本体是数据库对象，随备份走）→ ③ `CREATE PROCEDURE/FUNCTION/TRIGGER/TYPE ... EXTERNAL NAME` 建壳 → ④ 首次调用时宿主在 SQL Server 进程内建 AppDomain 并 JIT。关键工程后果：**代码版本与壳对象解耦**——更新程序集要 DROP/ALTER ASSEMBLY 且可能级联失效依赖对象，书中把这列为运维痛点 ⚠️。

### 安全三档的真实边界
- SAFE：只允许计算与内部 API，禁文件/网络/注册表/非托管互操作。
- EXTERNAL_ACCESS：可触达外部资源，书中演示了文件读写与网络调用两条路线（转述 ⚠️）；2005 时代要求数据库 TRUSTWORTHY 或证书+非对称密钥授权，后者才是可迁移的正路。
- UNSAFE：可做任何事，包括调非托管代码——等于把沙箱删掉；书的立场是仅内置对象（如空间类型）配得 ⚠️。
配套细节：`clr enabled` 面配置默认 0；sp_configure 打开是安装后动作而非运行时动作 ⚠️。

### 性能账本（书中实验的描述性转述 ⚠️）
CLR 赢在：循环密集的字符串解析、正则、位运算、加解密、跨行聚合（用户定义聚合 UDA）。CLR 输在：
1. 首次调用的装载/编译延迟（书中建议部署后预热，转述 ⚠️）；
2. 每行调用的 T-SQL↔CLR 类型编组成本，行级热路径被放大；
3. SQL Server 内存管理（BP）管不到 CLR 堆——极端场景可把实例推到 OS 换页 ⚠️；
4. 托管异常需转译回 SQL 错误，SqlContext.Pipe 是唯一回吐结果集通道，破坏并行性（书中演示 ⚠️ 转述）。

### UDT 序列化与索引联动（第 14 章）
UDT 两种序列化形态（转述 ⚠️）：Native（按字段布局二进制直存，快但布局一变数据即废）与 Binary 自管（实现 IBinarySerialize，可版本演进）。定序 UDT 上可建索引——但索引只认"字节序"，若自然序与字节序不一致（书中以多维/半结构类型举例 ⚠️），范围查询就失真。这解释了为什么 hierarchyid 要精心设计成"字典序≈树先序"。

### 空间类型与 hierarchyid 的定位
- geometry/geography 是微软自家 CLR 应用：点线面 WKT/WKB 互转、缓冲/交并/距离；空间索引=四级网格切片，选择性靠边界框重叠（细节 ⚠️ 转述，接 15 章等待画像中的空间查询案例）。
- hierarchyid：编码树路径的 UDT，`GetAncestor/GetDescendant/IsDescendant` 家族 + 深度优先可定序；书中对比邻接表/路径枚举/闭包表后推荐它处理"深而稳"的层级（组织树/分类目录），但警告：父节点重排时 GetDescendant 生成的新键可能连锁改子树 ⚠️。

## 本章结论速记

- CLR 程序集是数据库内对象：随备份走、随 TRUSTWORTHY/证书谈安全。
- 默认 `clr enabled=0`：微软与书同款的"非拒用、但劝退"。
- 计算密集用 CLR，行级 OLTP 热路径远离 CLR。
- UDT=可索引的 8060 字节结构工件；字节序即索引序，设计时锁死。
- 空间/hierarchyid 是 CLR 类型的官方样板间，也是本章在今天仍活着的部分。

## 工程模式与常见误区

| 误区 | 事实（转述 ⚠️） |
| --- | --- |
| "CLR 过程比 T-SQL 游标快，所以到处换 CLR" | 冷启动+编组+管道串行化常在联机短查询上倒亏；收益区是解析/加密/字符串密集 ⚠️ |
| "SAFE 就绝对安全" | SAFE 仍占非托管堆、可跑死循环；资源治理不在权限集内 ⚠️ |
| "TRUSTWORTHY ON 最省事" | 把整个库变成外访问跳板；证书签名路线才可控 ⚠️ |
| "UDT 改字段布局无所谓" | Native 序列化下旧数据直接不可解；要演进就用自管二进制+版本号 ⚠️ |
| "hierarchyid 万能树方案" | 深树重排代价、键宽随深度增长；浅而大的树用邻接表+CTE 未必输 ⚠️ |
| "空间索引像 B 树一样随便建" | 网格层级不调好=海量重叠 tile，回表过滤吃掉收益 ⚠️ |

## 机制链条

```
.NET DLL ──CREATE ASSEMBLY──▶ 数据库内程序集 ──EXTERNAL NAME──▶ T-SQL 壳对象
   │                                   │
 首次调用                       备份/还原带走字节流
   ▼
AppDomain 装载 → JIT →（每行调用：类型编组 ⇄ SqlPipe）
   ▼
内存落在 CLR 堆（不受 BP 管理 ⚠️）→ 极端时实例整体内存画像失真
```

## 延伸转述：书中判断力小题（转述 + ⚠️，非原书逐字）

1. **问**：CLR 程序集存在文件系统里吗？
   **答**：字节流存在数据库内（程序集对象），随备份迁移；磁盘上的 DLL 只是来源 ⚠️。
2. **问**：SAFE 程序集能不能读文件？
   **答**：不能——文件/网络/环境访问属 EXTERNAL_ACCESS 起步；试图越界在首次触碰时抛权限异常 ⚠️。
3. **问**：TRUSTWORTHY ON 和证书签名选哪个？
   **答**：证书+非对称密钥授权是可迁移正路；TRUSTWORTHY 把整库变跳板（书中安全课 ⚠️）。
4. **问**：CLR 过程第一次调用为什么慢？
   **答**：AppDomain 装载+JIT 冷启动；部署后预热是书给的标准动作 ⚠️。
5. **问**：UDT 能进索引吗？
   **答**：能，按字节序；自然序≠字节序时范围查询失真——定序要在编码期设计 ⚠️。
6. **问**：Native 序列化和自管二进制怎么选？
   **答**：前者快但布局冻结；后者带版本号可演进——长期在线系统选自管（书中告诫 ⚠️）。
7. **问**：hierarchyid 相比路径字符串强在哪？
   **答**：变长二进制+可定序+引擎方法族（祖先/后代/深度），宽度和比较成本都低 ⚠️。
8. **问**：什么树不适合 hierarchyid？
   **答**：频繁整体重排/超深树——新键生成可能要求子树连锁改写 ⚠️。
9. **问**：geometry 和 geography 的本质区别？
   **答**：平面欧氏 vs 椭球测地（面积/距离算法不同）；坐标系（SRID）错配=结果全错 ⚠️。
10. **问**：空间索引为什么需要"重组"？
    **答**：对象移动使 tile 登记过期；书中给 ALTER INDEX REBUILD/重组织节奏 ⚠️。
11. **问**：CLR 聚合能并行执行吗？
    **答**：分片累积+终并的形态决定收益；含 SqlContext.Pipe 输出的过程会串行化（书例 ⚠️）。
12. **问**：怎么升级一个被 200 个对象引用的程序集？
    **答**：ALTER ASSEMBLY WITH DROP_DESCRIPTORS/先壳后芯/蓝绿库——书中列了痛点和路线，结论是"少而稳的 CLR 面" ⚠️。
13. **问**：新项目今天还要写 CLR 吗？
    **答**：多数动机已被内置 T-SQL/外部服务取代（STRING_SPLIT、JSON、加密函数）；存量空间/层级类型继续用 ⚠️（见下节）。

## 与其他章 / 其他笔记的联系

- EAV/宽表/稀疏列与 CLR 类型的选型对照：[04-特殊索引与存储特性.md](04-特殊索引与存储特性.md)；XML 也是"半结构装进引擎"的竞品：[08-XML与临时表.md](08-XML与临时表.md)。
- 字符串拆行（fn_Split 类 CLR TVF）在查询端的计划代价，接标量 UDF 不可内联旧账：[07-视图与用户定义函数.md](07-视图与用户定义函数.md)、[14-查询优化执行与计划缓存.md](14-查询优化执行与计划缓存.md)。
- CLR 聚合在数仓场景被批处理列存取代：[18-列存储索引.md](18-列存储索引.md)。
- 客户端侧批量交互（比 CLR 更常用的扩展面）：[11-系统设计考量.md](11-系统设计考量.md)。
- 跨引擎谱系：MySQL 无进程内托管扩展（UDF 走原生 so/dll）、PG extension 生态走 C+可信语言沙箱（plv8 等），对照 [../PostgreSQL数据库内核分析.md](../PostgreSQL数据库内核分析.md)、[../MySQL技术内幕_InnoDB存储引擎2.md](../MySQL技术内幕_InnoDB存储引擎2.md)。

## 核心概念速览（中英对照）

1. **CLR 集成** — CLR Integration：SQL Server 进程内托管宿主，2005 引入。
2. **程序集** — Assembly：注册进数据库的 .NET 单元，随备份迁移。
3. **外部名称** — EXTERNAL NAME：T-SQL 壳对象与 CLR 方法的绑定语法。
4. **权限集** — Permission Set：SAFE / EXTERNAL_ACCESS / UNSAFE 三档信任。
5. **可信数据库** — TRUSTWORTHY：允许程序集借库身份获得外部访问的开关。
6. **数据编组** — Marshaling：T-SQL 与托管类型逐行互转的隐性成本。
7. **用户定义聚合** — UDA：CLR 实现的跨行聚合器。
8. **UDT 序列化** — UDT Serialization：Native 布局直存 vs IBinarySerialize 自管。
9. **geometry / geography** — 平面/椭球两套内置空间 CLR 类型。
10. **空间索引** — Spatial Index：基于网格 tile 重叠的粗筛索引。
11. **hierarchyid** — 变长二进制路径编码的树型 UDT。
12. **GetDescendant** — hierarchyid 的核心写方法：在父子槽位间生成新键。
13. **clr enabled** — 实例级面配置，默认关闭。

## 最新演进与工业实践

- **官方定调（2024–2026）**：SQL Server 的 Azure SQL Database 与托管实例不支持用户 CLR；微软明确建议以数据库引擎外部服务/T-SQL 新功能替代——SQL Server 本地版仍可用户 CLR 但已属"冻结演进"面（[CLR 集成概述](https://learn.microsoft.com/en-us/sql/relational-databases/clr-integration/common-language-runtime-integration-overview) ✅ curl 200）。
- **本章明星功能的内置化**：字符串拆分有 `STRING_SPLIT`（2016）、JSON 有 `OPENJSON`/JSON 类型路线（2016/2024 增强）、加密与哈希大量下沉为 T-SQL 函数——当年写 CLR 的头号动机（拆行）已消失（[2022 新特性](https://learn.microsoft.com/en-us/sql/sql-server/what-s-new-in-sql-server-2022) ✅）。
- **hierarchyid 的真实战场收窄**：组织/目录树更多用"邻接表+递归 CTE+物化路径"或应用层图结构；hierarchyid 仍在但新项目引用率下降 ⚠️（趋势性描述，无单一权威统计）。
- **空间栈继续活着**：geometry/geography 仍是本地版空间数据主路线，并与 Azure SQL 兼容；2022+ 有 WGS84 深度增强与 OpenGeo 系生态互动（概称 ⚠️，逐条特性名以官方 release notes 为准）。
- **扩展语言的新答案**：Microsoft 转向在引擎外做"托管扩展"——BIG DATA CLUSTERS（已官宣退役 ⚠️ 口径以微软停用公告为准）、Azure Synapse 的 PolyBase/外部表，以及 2025 的向量检索面（[2025 新特性](https://learn.microsoft.com/en-us/sql/sql-server/what-s-new-in-sql-server-2025) ✅）；"进程内跑用户代码"这条路线整体上被"数据出去、算力进来"取代。
- 作者后续公开文章可作旁证：[aboutsqlserver.com](https://aboutsqlserver.com/) ✅。
