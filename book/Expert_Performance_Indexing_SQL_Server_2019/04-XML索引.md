# 04 · XML 索引（XML Indexes）

> 原书 Chapter 4 "XML Indexes"，pp.163–176（✅ Crossref，DOI …_4）。短章（14 页）：
> 特化索引四连（XML/空间/内存/全文）的第一站。⚠️ 叙事重构，引擎口径以 Learn ✅ 锚定。

## 本章主线

XML 类型列本质是文档容器，默认**不可用普通 B+ 树索引加速路径查询**；SQL Server 用
"主 XML 索引 + 次要 XML 索引"的两级结构把文档拆解为可索引的关系化中间表示。本章讲
何时值得为 XML 建索引、以及索引自身的存储/维护代价。⚠️

## 4.1 主 XML 索引：shredded B+ 树 ⚠️ 转述 + ✅ 概念

- 前置条件：列上有 XML 类型 + 存在可空/非空约束语义下才谈索引；必须先建**主 XML 索引**，
  它把文档"粉碎"（shredding）为 (节点值, 路径, 文档内节点号) 三元组的内部表并全量索引。
  ✅ 官方：https://learn.microsoft.com/en-us/sql/relational-databases/xml/xml-indexes-sql-server
- PRIMARY … FOR PATH 的三种 SECONDARY 变体：VALUE / PATH / PROPERTY，分别服务
  `.exist()` 按值、按路径、按属性名+值定位的查询形态——选型依据 = XQuery 谓词形态。⚠️/✅
- 限制面：主索引随表数据复制体积（文档膨胀率）、DML 需同步重粉碎、单表 XML 列数量与
  索引组合受版本/兼容级别约束 ⚠️。

## 4.2 何时不该用 XML 存储 ⚠️ 重构论证

1. 查询模式稳定 → 应拍平为关系列 + 常规索引（schema-first 优先）；
2. 文档半结构且整存整取 → XML 无索引裸存即可，索引纯增负担；
3. 只有"确实按路径/值检索"且**无法拍平**时才上 XML 索引——本书把 XML 索引定位为
   "遗留/集成场景的补救"，与第 15 章方法论一致。⚠️ 判断
- 对照现实：JSON 在 SQL Server 长期只是"带校验的 nvarchar"，2025/17.x 才引入原生
  JSON 类型与 JSON 索引方向（演进节给 ✅ URL）——**这正是本章在 2019 的痛点**。⚠️/✅

## 4.3 选择性评估与空间/全文章的接口 ⚠️

- XML 路径选择性无统计直方图可依赖（第 03 章的工具在此失效），需按业务采样估算——
  这一"特化索引各自为政的观测盲区"在空间（§5）与全文（§7）章重复出现，构成
  第 13 章监控章的例外清单。⚠️

## 4.4 维护与体积 ⚠️

- XML 列更新=内部表重建局部，成本远高于标量列 UPDATE；批量导入场景建议**后建索引**。
- 压缩选项：主 XML 索引支持与常规索引一致的 DATA_COMPRESSION 语义 ⚠️ 转述，
  ✅ 概念口径并见 Create XML Index 官方页（xml-indexes-sql-server 同上 URL）。

## 4.5 🔧 类比说明（诚实登记：无对位实验）

- XML  shredding/次要索引为 SQL Server 特有结构，SQLite 无原生 XML 类型（其 XML 需应用层
  解析）、DuckDB 以嵌套类型+半结构化读取处理——**本册不为 XML 造玩具类比**，按波纪律记
  ⚠️ 不可类比。可用的最近邻观察：SQLite 的 JSON1 扩展把 JSON 路径当"伪 shredding"消费
  （`json_extract` 无索引=全行扫），若本机内核带 JSON1 可自验（本册未跑，不作 🔧 登记）。

## 4.6 章内互链

- 通用索引不可用场景的补救谱系 → [05-空间索引.md](05-空间索引.md) /
  [07-全文索引.md](07-全文索引.md)
- "先拍平再索引"的存储立场 → [02-索引存储基础.md](02-索引存储基础.md)
- 后建索引/批量导入维护 → [09-索引维护.md](09-索引维护.md)
- 特化索引监控盲区 → [13-索引监控.md](13-索引监控.md)

## 4.7 关联笔记（盘上实链）

- XML/半结构化在别引擎的索引化（JSON/嵌套）：
  [../DuckDB_in_Action/00-总览与阅读地图.md](../DuckDB_in_Action/00-总览与阅读地图.md)（半结构化读取面）
- 物理设计视角"该不该反范式/嵌套存"：
  [../Physical_Database_Design/00-总览与阅读地图.md](../Physical_Database_Design/00-总览与阅读地图.md)
- SS 内核侧大值类型处理对照：[../Pro_SQL_Server_Internals/00-总览与阅读地图.md](../Pro_SQL_Server_Internals/00-总览与阅读地图.md)
- MySQL 半结构化（无 XML 索引，有 JSON）对照：[../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md)

## 4.8 判读 FAQ

- **Q：XML 列不建索引完全不能查吗？**
  A：能查（全行粉碎后谓词评估），只是无加速——XML 索引是性能件不是功能件，功能正确性零依赖。
- **Q：主索引能跳过吗？**
  A：不能，次要三种全部以主索引为前置——顺序是强制的，这也是“先拍平后索引”立场（§4.2）的程序性依据。
- **Q：三种次要索引能全建吗？**
  A：技术可、经济亏：每多一型≈再存一份粉碎行集；按 XQuery 形态只选一型是默认答案。⚠️
- **Q：exist() 和 value() 谁吃索引？**
  A：exist 谓词类受益最直接；value 抽取常仍回文档原值——计划里“有索引却全扫”多为此形态。
- **Q：XML 列能进普通复合索引吗？**
  A：不能作键列（大值类型限制，§2.1 账本）；普通索引只能覆盖其同表的标量列。
- **Q：和 JSON 扩展性怎么选？**
  A：2019 现实：两者都是“字符串/文档列+外置索引思路”；新项目选 JSON（生态向 2025 原生方向倾斜），XML 留给存量。⚠️/✅
- **Q：文档大小有上限吗？**
  A：列上限 2GB（varbinary 同族），实践上千 KB 级文档的粉碎/重建成本已需专项评估。⚠️ 口径
- **Q：命名空间影响索引吗？**
  A：影响路径写法与次要索引命中形态，不影响结构；默认命名空间是 XQuery 判读事故高发点。
- **Q：本章在 2026 还要精读吗？**
  A：作为“特化索引如何被关系引擎消化”的样本仍值得：同样的两段式/盲区结构将在向量索引叙事里重演。

XML 章的最大误读是把“支持 XML”读成“推荐 XML”——本章实为劝退学。

## 核心概念速览（中英对照）

1. **XML 类型** — xml data type：以实例存储的半结构化列类型，非二进制 XML 文档直存 ⚠️/✅。
2. **粉碎** — shredding：把文档拆为 (值,路径,节点号) 关系化内部表示的主索引构建过程。
3. **主 XML 索引** — primary XML index：全量索引 shredded 行集，次要索引的前置。
4. **次要 XML 索引** — secondary XML index：VALUE/PATH/PROPERTY 三型，按查询形态选配。
5. **XQuery 方法** — query/value/exist/nodes：命中不同次要索引形态的访问入口。
6. **路径** — path (.pathname)：节点在文档树中的定位串，索引键的第一维。
7. **文档膨胀** — XML index size blow-up：主索引内部表数倍于源文档体积的现象。⚠️
8. **后建索引** — build-after-load：批量导入完成后再创建 XML 索引的降载手法。
9. **无统计可依赖** — statistics-blind：特化索引不进入常规直方图体系的观测盲区。
10. **schema collection** — XML schema collection：类型化的 XSD 约束集，影响校验与索引可用性 ⚠️。
11. **JSON 原生缺位（2019）** — 2019 时代 JSON 仅为字符串列+约束，非引擎级类型 ⚠️/✅。
12. **DATA_COMPRESSION** — data compression：XML 索引同样适用的页/行压缩开关。

## 最新演进与工业实践

- 官方 XML 索引文档（主/次索引、限制与设计建议）：
  https://learn.microsoft.com/en-us/sql/relational-databases/xml/xml-indexes-sql-server ✅
- 半结构化重心的迁移：2024–2025 起 SQL Server 2025（17.x）引入原生 JSON 支持方向
  （JSON 类型/索引相关文档已进入 Learn；本册核到 200 的向量侧证据见下条，JSON 专页
  以官方检索为准 ⚠️ 标注）——"XML 索引章"在新一代版本中正在被"JSON 索引章"替换。⚠️/✅
- 向量检索作为新的特化索引家族成员（与 XML/空间/全文并列的第五路）：
  https://learn.microsoft.com/en-us/sql/relational-databases/vectors/vectors-sql-server ✅、
  https://learn.microsoft.com/en-us/sql/t-sql/data-types/vector-data-type ✅
- 工业实践：新增系统普遍 schema-first + JSON 列存原文备查；遗留集成（ESB/文档库）仍按
  本章"主+次"模型治理 XML 索引；评估口径"查询形态→索引形态"未过时。⚠️ 判断
- 半结构化的工业共识迁移：event-sourcing/文档表混存回关系列，XML 列仅保留审计原文；
  治理动作与本章劝退学一致——先拍平、后索引、索引是补救。⚠️ 判断
- 跨引擎：PostgreSQL 的 jsonpath/GIN-on-JSONB 是同类问题的另一解法谱系，对读
  [../PostgreSQL数据库内核分析.md](../PostgreSQL数据库内核分析.md)。
