# 18-XML对象关系与NoSQL（Part VI 导言 p.521 ✅；Ch26 XML Support, pp.523–541 ✅；Ch27 Object-Relational Databases, pp.543–584 ✅；Ch28 Relational Databases and “Big Data”: The Alternative of a NoSQL Solution, pp.585–596 ✅）

> 三态：✅ 书页 TOC/Crossref 页码实抓 · ⚠️ 转述/推定展开 · 🔧 本机 SQLite/DuckDB 实测（**非本书引擎/示范行为**）。
> Part VI 是全书 28 章的收官「后关系巡礼」（19+42+12 页）：Ch26 XML 是 2000s 企业集成的余晖，Ch27 对象关系是 SQL:1999 OR 遗产的完整复述，Ch28 NoSQL 是作者对大数据异端的 2016 年定性。三章共持一个隐性论题——**关系模型有边界，但每次「越界」的尝试最终都被关系主流收编**。本文件是本册与盘上 NoSQL/图/检索引擎纵深线的总汇合点。

## 一、精读札记（官方二级小节 ✅ 逐条）

**Part VI 导言（p.521）**：作者给出「超越关系」的三件套框架——文档数据（XML）、复杂对象（OR）、超大规模水平扩展（NoSQL）；⚠️ 框架措辞系推定，三章结构本身 ✅。

**Ch26（523–541）**
- XML Basics —— 元素/属性/良构/嵌套层次（小节题 ✅；展开 ⚠️）。
- SQL/XML —— 关系↔树的双向序列化标准层（⚠️）。
- The XML Data Type —— DBMS 把 XML 当一等类型存储与查询（⚠️）。

**Ch27（543–584）**
- Getting Started: Object-Orientation without Computing —— 不用计算机讲 OO 的教学开场（⚠️ 标题 ✅）。
- Basic OO Concepts —— 类/继承/封装/多态四件套。
- Benefits of Object-Orientation / Limitations of Pure Object-Oriented DBMSs —— 正反双节：纯 OO DBMS 的市场败局（⚠️）。
- The Object-Relational Data Model —— 关系为底、对象为翼的折中模型。
- SQL Support for the OR Data Model —— SQL:1999 血统的规范叙述（⚠️）。
- An Additional Sample Database —— OR 专章例库换装（⚠️）。
- SQL Data Types for Object-Relational Support / User-Defined Data Types and Typed Tables —— UDT、有类型表、引用类型（⚠️）。
- Methods —— DBMS 内封装行为；2026 对位是 UDF/UDAF（⚠️）。

**Ch28（585–596）**
- Types of NoSQL Databases —— 键值/文档/列族/图四分类（⚠️ 展开，分类学为通说）。
- Other Differences Between NoSQL Databases and Relational Databases —— schema 弹性、水平扩展、一致性档位（⚠️）。
- Benefits of NoSQL Databases —— scale-out、开发速度、半结构化贴合。
- Problems with NoSQL Databases —— 一致性税、二级查询生态、运维与人才储备（⚠️）。
- Open Source NoSQL Products —— 2016 产品切片（⚠️）。

## 二、主题深读

### 2.1 三章共同弧线：「异质模型→被关系收编」（评注 ⚠️）
Ch26 的 XML 集成热在 2010 后降温为「交换格式而非存储引擎」；Ch27 的 SQL:1999 OR 特性只在商业库以方言碎片存活（PostgreSQL 的组合类型、Oracle UDT 是幸存者 ⚠️），真正的继承者是 JSON/数组类型；Ch28 的 NoSQL 在 2016 后反而被关系界面回摄（DynamoDB 的 PartiQL、MongoDB 的查询语言趋 SQL、Cassandra 的 CQL 借 SQL 语法——盘上整书纵深见 §五）。教材把三章放进「Beyond」Part 的编排=精确的历史定位：它们是关系模型的前沿哨所，不是替代政权。

### 2.2 Ch26 与 1NF 的余震：JSON 把原子性战场重新炸开
Ch26 维护的 1NF 原子值假设，十年后被 JSON 从关系阵营内部重新击穿。🔧 载体观察（非本书示范行为）：本机 SQLite 内置 JSON1 扩展（sqlite.org/json1.html ✅ 已验页），json_each 可把一列 JSON 展平成关系行；DuckDB 的 LIST/STRUCT 直接存嵌套值——这正是 06 §2.4 登记的 1NF 现代两难的两个极端站姿。XML 章的教训在 2026 重演：**嵌套永远被重新引入，然后被再次规范化**——原子性是螺旋不是直线。

### 2.3 Ch27 是全书最「考古」的一章（42 页，本 Part 最长）
42 页献给一个没有赢的模型——作者的意图显然不在教 OR DBMS，而在用 OO 概念打磨读者的模型迁移力。2026 转译读法：「User-Defined Data Types and Typed Tables」对位 Postgres 组合类型/域与现代 OLAP 的 AggregateFunction 类（⚠️）；「Methods」对位 UDF 注册；「继承」的真正幸存者不是有类型表，而是星型模式里的共享维度与子类表设计（接 03/10 的建模线）。本章与 Ch28 的篇幅比（42:12）本身就是 2016 年教材对两种异端的历史判断——事后看判错了方向但判对了性质。

### 2.4 Ch28 的 12 页：教材克制与工业喧嚣的对照
NoSQL 只给 12 页，却完成四分类+收益+问题+开源产品的完整三角评述——2016 年多数出版物还在「大数据传教」文体里，本章的「Problems with NoSQL Databases」一节是少见的冷水阀（⚠️ 评价）。2026 复核：作者的克制大体被历史兑现——NoSQL 未取代关系，而是多模分化：键值线归托管服务（DynamoDB）、列族线归 Cassandra 系、图线归 Neo4j 系、检索线归 Elasticsearch 系，四条线全部有盘上整书（§五实链），本册读者从这里跳板即可。

### 2.5 CAP/BASE 缺席：本章的理论缺口（⚠️ 评注）
Ch28 小节列表（✅）不含一致性理论专节——CAP 与 BASE 语汇在本章是空缺的（依小节清单推定）。本册补最小骨架：CAP=分区容忍下一致性/可用性二选一；BASE=基本可用+软状态+最终一致，是工程对一致性的折价采购。两词应从盘上 DynamoDB/Cassandra 册的 00 学习而非本章——但教材立场值得复述：**没有一致性理论的 NoSQL 叙述，等于没有 FD 的规范化叙述**——都是可操作而无判据。

### 2.6 多模合流 2026：三个「超越」的归宿（综合 ⚠️）
Postgres 一库集 JSONB+数组+全文+图扩展；SQL Server 的 XML 类型仍在且加 JSON；Snowflake/Databricks 的半结构化列（variant 类 ⚠️）由湖仓承接——Ch26/27/28 的清单被关系阵营逐项收编：XML→JSON 类型、UDT→嵌套类型、NoSQL→多模引擎+开放表格式。Part VI 标题的 2026 终审答案可能是：**模型边界是海岸线，侵蚀方向始终是向心**。

## 三、原书 → 2026 对位

| 书内论点 (2016) | 2026 现状 |
|---|---|
| XML 是一等数据类型（Ch26） | 降为交换格式；JSON 接管「嵌套存储」职务 |
| OR 模型的 UDT/有类型表（Ch27） | 方言碎片存活；精神继承者是嵌套类型+UDF |
| NoSQL 四分类+利弊（Ch28） | 多模+湖仓双轨：引擎专业化、界面 SQL 化 |
| 关系是默认，超越是例外 | 仍成立；「例外」各自长出独立产业与整书文献 |

## 四、阅读自测
1. Ch26/27/28 的共同论题一句话（「被收编的边疆」展开说）。
2. 1NF 的两代再战场：XML 与 JSON 各在哪一侧击穿原子性？
3. Ch27 的 Methods/UDT 两节各给一个 2026 方言对位。
4. Ch28「Problems」节的代价清单，从 2026 平台团队视角挑三条最痛的并说明理由。
5. 用盘上 DynamoDB/Cassandra/Graph 三册补本章的 CAP/BASE 缺件，各一句话。

## 五、互链
- 上游：06（1NF 与 JSON 战场 §2.4）、04（关系公理=越界的度量衡）、07（Codd 规则=被「超越」的宪法正文）、17（数仓是大数据的关系侧收编）。
- 兄弟：14（二级索引/视图≈NoSQL 查询能力缺件的补偿清单）、15（并发与一致性词汇在 NoSQL 侧的镜像）。
- 盘上纵深（全部 ls 验名 ✅ 实链）：[../Amazon_DynamoDB_TDG/00-总览与阅读地图.md](../Amazon_DynamoDB_TDG/00-总览与阅读地图.md)、[../Graph_Databases_2e/00-总览与阅读地图.md](../Graph_Databases_2e/00-总览与阅读地图.md)、[../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md](../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md)、[../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md](../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md)。
- 00 账：谱系表 NoSQL 行、取证链均见 [00-总览与阅读地图](00-总览与阅读地图.md) §七。

## 核心概念速览（中英对照）
| 中文 | 英文 | 出处/一句话 |
|---|---|---|
| 可扩展标记语言 | XML | Ch26 文档数据载体 |
| SQL/XML | SQL/XML | Ch26 关系↔树标准映射层 |
| XML 数据类型 | XML data type | Ch26 一等存储类型 |
| 良构/有效性 | well-formedness/validation | Ch26 语法两关（⚠️） |
| 对象-关系模型 | object-relational data model | Ch27 关系+对象折中 |
| 继承 | inheritance | Ch27 OO 概念 |
| 封装 | encapsulation | Ch27 OO 概念 |
| 多态 | polymorphism | Ch27 OO 概念 |
| 用户定义类型 | user-defined type (UDT) | Ch27 方言遗产 |
| 有类型表 | typed table | Ch27 少存活特性 |
| 方法 | method | Ch27 → 今 UDF/UDAF |
| NoSQL | NoSQL | Ch28 异端总称 |
| 键值存储 | key-value store | Ch28 四分类之一 |
| 文档数据库 | document database | Ch28 四分类之一 |
| 列族存储 | column-family store | Ch28 四分类之一 |
| 图数据库 | graph database | Ch28 四分类之一（纵深在盘上） |
| 水平扩展 | scale-out | Ch28 核心卖点（⚠️） |
| 基本可用软状态最终一致 | BASE | 本册补件（书内缺，2.5） |
| SQL/XML | SQL/XML | ✅ 节题：关系↔树映射层 |
| XML 数据类型 | XML data type | ✅ 节题：存储侧一等类型 |
| 用户定义类型 | user-defined type | Ch27 UDT 方言幸存 |
| 有类型表 | typed table | Ch27 少存活特性 |
| 方法 | method | Ch27→今 UDF/UDAF（§2.3） |
| 键值/文档/列族/图 | four NoSQL families | §2.4 四分类线 |
| BASE | BASE | §2.5 本册补件（书内缺 ⚠️） |
| CAP | CAP theorem | §2.5 缺件账（本章未展开） |
| 多模合流 | multi-model convergence | §2.6 关系收编 |
| 嵌套螺旋 | nesting spiral | §2.2 原子性再引入 |
| 水平扩展 | scale-out | Ch28 核心卖点 ⚠️ |
| 一致性折价采购 | consistency tradeoff | §2.5 BASE 一句话定义 |
| 模型海岸线 | model coastline | §2.6 向心侵蚀论 |

## 最新演进与工业实践
- 「被收编的边疆」是 2026 定局：多模合流（Postgres JSONB、SQL Server XML 健在+JSON、Oracle JSON 表 API 替代原生 XML DB ⚠️）；湖仓（object storage+开放表格式）接管了 XML/NoSQL 当年的文档/blob 存储职务——schema-on-read 是 Ch28「灵活性」一节的宏大转正（接 17 §2.2 与盘上湖仓群实链）。
- 🔧 载体注（非本书示范行为）：本波实验栈 SQLite 3.45.3 的 JSON1 ✅ 文档页与 DuckDB 1.5.5 的半结构化类型正是 Ch26–28 三大「超越」的最小当代复现——单机内即可体验「嵌套↔规范化」螺旋，06/18 双文件互证。
- NoSQL 一致性理论补件义务移交盘上整书：DynamoDB/Cassandra/Graph 三册的 00 各带 CAP/BASE/最终一致纵深（§五实链）；本册读者的正确姿势是以 Ch28 的利弊清单为提纲、以三册为讲义。
- 波尾申报：本文件 18 登记为「本册→NoSQL/图/检索线」的总汇合点；波内兄弟 #1《Database Systems: A Pragmatic Approach》的 NoSQL 章互链义务待其成书后由其侧落链（00 §七只登记）。
- Part VI 终审 all in：XML→JSON、UDT→嵌套类型、NoSQL→多模+湖仓（§2.6/§2.1 账目回顾）。
- 🔧 载体双栈（JSON1 ✅ 文档页/DuckDB 嵌套类型）是 Ch26–28 的当代最小复现——非本书示范。
- CAP/BASE 缺件义务移交 DynamoDB/Cassandra/Graph 三册 00（§2.5/§五实链登记）。
- Ch27:Ch28 页比 42:12=2016 对两异端的历史判断——§2.3 判词：方向判错、性质判对。
- schema-on-read 转正（文末注）：对象存储+表格式接 XML/NoSQL 旧职——Ch28 灵活性节对位。
- NoSQL 四线全有盘上整书（§五 ✅）——本册只任索引章跳板。
- Ch26 读法=对 06 §2.4 双文件互证：原子性螺旋（教材代答案 vs 现代答案同战场）。
- OO 概念四件套（§一）今日成面试基础词——Ch27 的第二教学产出（文末注在册）。
- 有类型表在 struct 类型的复活属登记未实测件——波尾候选（🔧 未跑）。
- 「被收编边疆」论与湖仓群互链（17 §2.2/§五）——Part VI 的关系侧总账在 17。
- 波尾申报：NoSQL 线汇合点登记与 #1 兄弟互链义务见 00 §七。
