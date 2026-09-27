# 08 附录：NoSQL 概览（NoSQL Overview）

> 对应原书附录（中译本页码 164–178；英文通行名 *NoSQL Overview*，⚠️ 以原书为准）。附录无编号二级目录（豆瓣实抓目录仅列“附录 NoSQL 概览”一条），本文件按通行内容线重构：分类学 → 各范式要点 → CAP/BASE → 与图的关系。
> 本章文件为**精读重构**，非原书文本。定位：给第 2 章的“逐一检视 NoSQL 缺联系”补一张全景地图，也是本书与《NoSQL 精粹》的天然接口。

## 附录内容线（重构）

### A. NoSQL 分类学

书中沿用业界四分类（与 Sadalage & Fowler《NoSQL 精粹》同源口径）：

1. **键值（key-value）**：不透明值 + 哈希键；伸缩性极好，查询能力=键设计能力。代表（2015 语境）：Redis、Voldemort、Dynamo 系。
2. **文档（document）**：半结构化自描述文档 + 域查询；聚合一致性边界。代表：MongoDB、CouchDB。
3. **列族/宽列（column family / wide-column）**：按列族稀疏排序存储；为“列裁剪 + 写吞吐”优化。代表：Cassandra、HBase。
4. **聚合/事件溯源（aggregate/event sourcing）**：不可变事件流重建状态；时间维度的“关系”。

本书的独特动作：在第四类之外把**图数据库单列**为第五类（或者说“关系范式”的独立代表），并用第 2 章论证为什么前四类没有把“联系”当一等公民。

### B. CAP 与 BASE

- **CAP**：分区容错在分布式里近乎必选，工程选择发生在 C/A 之间；书中提醒——“选择”只在**分区发生时**才被迫二选一，正常期两者可兼得（这一辨析至今常被误读）。
- **BASE**（Basically Available / Soft state / Eventually consistent）：对 ACID 的松绑； Dynamo/Cassandra 血统的最终一致读（读写向量、读修复、读己之写的补丁手段）。
- 本书立场：图数据库（Neo4j 代表）明确站 ACID 一侧——第 6 章 6.4 的“事务/可恢复性”与此呼应；附录承认代价是**扩展性形态受限**（当时无通用分片）。

### C. 与图数据库的关系收束

- 多语言持久化（polyglot persistence）：图负责关联查询，其他引擎负责各自最擅长的形态；集成方式回到第 4 章（REST/Bolt 服务器模式天然适合异构栈）。
- 分类学不是选型终点：**查询形态（沿关系扩散 vs 聚合扫描 vs 键取回）才是**——附录把第 2 章的批判升格为一般方法。

## 精读札记

- 附录写于 2015 年 NoSQL 论战尾声，语气是“分类与和解”而非“布道”；今天回看最有生命力的恰是 B 节那句 CAP 辨析。
- “四分类 + 图”的框架后来被“多模（multi-model）数据库”打乱：单一引擎内置多种模型（见最新演进），分类学从“选引擎”退化为“选引擎内的表征收用哪种视图”。

## repo 互链

- 本附录的“正书版”分类学：[../nosql精粹.md](../nosql精粹.md)（NoSQL 精粹——本书附录主题的单行本原著）。
- 教材口径的 NoSQL/NewSQL 章（第 7 版扩充）：[../数据库系统概念7.md](../数据库系统概念7.md)。
- Redis（键值代表）两册：[../Redis设计与实现.md](../Redis设计与实现.md)、[../Redis实战.md](../Redis实战.md)。
- Cassandra（宽列代表）：[../cassandra实战.md](../cassandra实战.md)。
- 复制/一致性总框架：[../设计数据密集型应用.md](../设计数据密集型应用.md)；论文线：[../../db/db.md](../../db/db.md)。
- 正文中的对应批判章：[./02-关联数据的存储选择.md](./02-关联数据的存储选择.md)；ACID 立场章：[./06-图数据库的内部结构.md](./06-图数据库的内部结构.md)。

## 核心概念速览（中英对照）

- **键值存储** — key-value store：不透明值 + 键哈希，伸缩优先。
- **文档存储** — document store：自描述半结构化文档，聚合边界。
- **聚合** — aggregate：一致性/事务边界的领域单元。
- **列族** — column family：稀疏有序列簇，宽列存储的核心结构。
- **事件溯源** — event sourcing：以不可变事件流为真相源的状态重建。
- **多语言持久化** — polyglot persistence：按负载选存储的架构观。
- **CAP** — CAP：一致性/可用性在分区时的取舍定理。
- **BASE** — BASE：基本可用 + 软状态 + 最终一致的松绑纲领。
- **最终一致** — eventual consistency：无全局时序的收敛保证。
- **读修复/反熵** — read repair / anti-entropy：副本收敛机制两形态。
- **ACID 立场** — ACID stance：本书/Neo4j 的 OLTP 承诺。
- **多模数据库** — multi-model database：单引擎内置多种数据模型（分类学的当代融合）。

## 最新演进与工业实践

- **量化全景**：DB-Engines 按“graph DBMS”等分类给出月度流行度排名，是附录分类学的活数据入口：https://db-engines.com/en/ranking/graph+dbms （curl 200 ✅；名次随月变动，引用时现取）。
- **文档/宽列阵营的“补图”**：MongoDB（Graph 通过 $graphLookup 有限支持）、Cassandra（SAI 索引替代物化索引路线）、DynamoDB（TransactWrite 增强一致性）——各家都在补“关系能力”，但都未把邻接做成存储原语，2.2/附录的判断仍立得住（⚠️ 各家特性版本口径请以官方文档现核）。
- **BASE 阵营的“补 ACID”**：附录对译的当代版本是“分布式事务回归”（CockroachDB/YDBC 系），与本系列分布式/湖仓书目相邻：[../分布式数据库入门进阶与实战/00-总览与阅读地图.md](../分布式数据库入门进阶与实战/00-总览与阅读地图.md)。
- **多模融合的代表**：Microsoft Fabric 在仓内同时提供 Graph/向量/关系视图（https://learn.microsoft.com/en-us/fabric/graph/gql-conformance ，curl 200 ✅）；Memgraph/Neo4j 内置向量索引（见 `./06-图数据库的内部结构.md` 链接）——“四分类+图”正在收敛成“一个引擎、多种索引、一种查询语言（GQL）”。
- **GQL 标准对分类学的定调**：ISO/IEC 39075:2024 以“属性图 + 模式匹配语言”为对象（ISO 官方页 https://www.iso.org/standard/76120.html ⚠️ 403 反爬，核证双源见 `./02-关联数据的存储选择.md` 最新演进）——图从“NoSQL 的一类”升格为“与 SQL 并列的标准模型”，附录的从属视角需要更新。
- **NoSQL 精粹的续作**：《NoSQL Distilled》无第二版正式出版信息（⚠️ 未核到官方续订声明），本附录+《NoSQL 精粹》仍是该分类学最短路径；进阶可直接读 LDBC 基准定义了解“负载驱动选型”的现代方法：https://ldbcouncil.org/ （curl 200 ✅）。
