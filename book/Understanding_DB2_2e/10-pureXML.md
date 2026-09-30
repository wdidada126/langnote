# 10 pureXML（原书第 10 章 Mastering the DB2 pureXML Support ✅ 题逐字）

> 本章为精读重构：pureXML 行为「⚠️ 转述」。9.5 的招牌功能章——也是本册与其余 LUW 引擎书差异最大的一章。

## 章图与图描述（视觉向开场）

- **图 10-A「拍平 vs 原生」**（描述，本章立场图）：左栏"关系建模派"把 XML 拆成多表多列（箭头乱、重构难），右栏 pureXML 整文档入列+索引加速（文档树原形保真）——"为什么需要原生 XML"一图解忧。
- **图 10-B「XML 存储内部格式」**（描述）：文档被切成数据行/片段，标注"shredding（碎片化存储）+ 结构索引/路径索引"两类加速件；这是图 8-A 套娃在 XML 世界的分身。
- **图 10-C「XQuery FLWOR 流水线」**（描述）：FOR-LET-WHERE-ORDER-BY-RETURN 五段各配小箭头，把"XML 里的 for 循环"讲成可视管道。
- **图 10-D「混查示意」**（描述）：一条 SQL 里关系谓词与 XMLQUERY() 列函数并排、结果网格混合列——"关系+XML 一个引擎"的产品叙事图。

## 原书章骨架 → 本文件对位（⚠️ 推定主题域）

| 推定主题域 | 本文件小节 |
| --- | --- |
| XML 列与文档完整性 | 精讲 1 |
| XML 索引体系 | 精讲 2 |
| XQuery 语法族 | 精讲 3 |
| SQL↔XML 桥函数 | 精讲 4 |
| 装载与编程接口 | 精讲 5 |
| 何时该用/不该用 | 精讲 6 |

## 核心精讲

### 1. XML 型列：整文档公民（⚠️ 转述）
`CREATE TABLE ... (doc XML)`——文档按 well-formed（9.5 默认校验良构；**schema-based 与 annotated XDS 是 9.7 补的课 ⚠️ 版本分界**）；容量口径与 LOB 同量级（2G–4G ⚠️ 具体上限以版本手册为准）。文档进列即"原生形态存储+版本可追溯（XDS 前代用 LOB/表设计自管 ⚠️）"。

### 2. XML 索引三件（⚠️ 转述）
- **路径/模式索引**（XMLPATTERN/INCLUDE 指定 pathterms）：给热点路径建"目录高速公路"；
- **元素/属性值索引**：等值谓词加速；
- **嵌套路径索引（NXPATH）**：9.5 时代主打，多路径组合一次命中（⚠️ 索引名称/组合规则随版本演进，以现行文档为准）。
【注】索引不是越全越好——XML 索引维护成本随写入放大，本章 Tip 反复强调"按访问模式建索引"。

### 3. XQuery：XML 的 SELECT（⚠️ 转述）
FLWOR 五件套+谓词+构造（XMLTEXT/XMLELEMENT 回关系侧）；DB2 提供 **XMLQUERY()/XSQ** 把 XQuery 嵌入 SQL 标量位置，db2ex 或 CLP 亦可试跑；全文检索与上下文谓词是加分项（⚠️ 具体函数名以版本为准）。

### 4. SQL↔XML 桥（⚠️ 转述）
XMLPARSE/XMLSERIALIZE/XMLVALIDATE 三件套；**XMLTABLE（把 XML 拆回关系行列）是 9.7 后话**——9.5 读者的等价物是 XQuery+视图自组（⚠️ 版本分界声明，读现代 Db2 文档时 XMLTABLE 已司空见惯）。

### 5. 装载与编程接口（⚠️ 转述）
INSERT/LOAD 直灌 XML 列（9.5 对 XML 列的 LOAD/IMPORT 支持细节 ⚠️）；CLI/JDBC/XQJ（IBM 的 XQuery for Java 谱系）三条应用通道；XML 文档与关系数据的混合抽取供 BI。

### 6. 选型判断（本章工程观）
适合：文档形态异构、层级深、模式演进快、需要整文档原子存取（报文/表单/配置）；不适合：以窄表聚合分析为主——拍平关系模型仍是王道。这条"混合数据管理"的边界论，是 DB2 当年对抗 NoSQL 潮的产品哲学（呼应 [01](01-DB2入门与视觉学习法.md) 混合叙事）。

## 常见误区

1. "XML 列=存字符串"——原生内部格式+碎片化索引才是 pureXML 的本体（图 10-B）。
2. "XQuery 取代 SQL"——两语族靠函数桥互相调用，不是替代关系。
3. "上 schema 校验越早越好"——9.5 仅良构校验，schema-based 属 9.7+（版本错位是本章最易引错处 ⚠️）。
4. "全文索引=XML 索引"——两族索引各有分工，混查计划里各走各位（[15](15-性能与问题诊断.md) 语境）。

【微讲堂】一屏混查示意（⚠️ 语法转述，非实测）：

```text
SELECT id, XMLQUERY('$d/order/customer/text()' PASSING doc AS "d") AS cust
FROM orders_xml
WHERE XML_EXISTS('fn:contains($d/order/item/@type,"rush")' PASSING doc AS "d");
```

## 🔧 类比说明（本章无等价实验）
SQLite/DuckDB 无原生 XML 类型与 XQuery（SQLite 可存 TEXT+自解析、DuckDB 强项是 JSON——均**非对位机制**）；本章不硬凑实验，保持"不可类比即如实声明"的纪律。JSON 半结构化的现代对位体验可用 DuckDB json 函数一瞥（方法自便，结论不外推 DB2）。

## 与其他章/其他笔记的联系

- 上游：对象与列类型 → [07](07-数据库对象.md)；存储对象行 → [08](08-存储模型.md)。
- 下游：索引与计划 → [15](15-性能与问题诊断.md)；装载与 REORG → [12](12-并发锁与数据维护.md)。
- 异厂/同代对照：XML 在 Oracle 系的对应叙事 → [../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md)（本书 XMLDB 语境旁支）；半结构化现代主流（JSON/parquet）→ [../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md)、[../DuckDB_in_Action/00-总览与阅读地图.md](../DuckDB_in_Action/00-总览与阅读地图.md)；NoSQL 全景中的 XML DB 位 → [../nosql精粹.md](../nosql精粹.md)（盘上单文件）。

## 章末自查（对位原书复习题的"看图作答"法）

1. 图 10-A 的两栏各举一个真实业务形态。
2. 9.5 的文档校验层级是什么？schema-based 哪年补的？
3. XML 索引三件分别加速什么谓词形态？
4. FLWOR 五段用一句话串起来。
5. SQL 与 XML 桥三件套各自方向？XMLTABLE 为何是"后话"？
6. LOAD XML 列的支持面（⚠️）与拍平方案的对比一句话。
7. 选型判断：合同条款库与订单聚合报表各适不适合 XML 列？

## 版本分界速查（读现代文档先打补丁）

| 能力 | 9.5 本册 | 9.7+ |
| --- | --- | --- |
| schema 校验/annotated XDS | 无（良构 only） | 有 |
| XMLTABLE | 无 | 有 |
| 嵌套路径索引 | 主打 | 演进 |

## 本章黑话三句

- "整文档公民" = XML 列按原形存。
- "切碎" = shredding 内部存储。
- "高速公路" = 路径索引。
- "新旧同屋" = 关系与 XML 共库共表。

【注】本章无 🔧 组：SQLite/DuckDB 均无对等的原生 XML 列模型，硬凑 JSON 实验会误导版本分界，宁缺毋滥（纪律见 00 第九节）。

【注】版本分界一句话：9.5 买"存与查"，9.7 补"拆与注解"（XMLTABLE/XDS，⚠️ 转述）。

## 核心概念速览（中英对照）

1. **pureXML** — 原生 XML 支持: 文档内部格式存储+索引。
2. **XML 列** — XML Type Column: 整文档为单元的关系列。
3. **良构** — Well-formed: 9.5 的默认文档完整性校验层级。
4. **Shredding** — 碎片化存储: 文档拆内部行以加速存取。
5. **pathterms** — 路径项: 模式/路径索引的索引对象。
6. **嵌套路径索引** — Nested Path Index: 9.5 主打的组合路径加速（⚠️ 名称以版本为准）。
7. **XQuery** — XML 查询语族: FLWOR 管道式导航/构造。
8. **FLWOR** — FOR/LET/WHERE/ORDER/RETURN: XQuery 五段式。
9. **XMLQUERY/XML_EXISTS** — SQL→XQuery 桥函数（⚠️ 具体名以版本为准）。
10. **XMLPARSE/SERIALIZE/VALIDATE** — 转换三件套: 字符串↔文档↔校验。
11. **XMLTABLE** — 拆回关系: 9.7 后补的位（9.5 无，版本分界）。
12. **XDS** — XML Document Storage 注解: schema-based 存储（9.7+，⚠️）。
13. **XQJ** — XQuery for Java: Java 侧 XQuery API 谱系。
14. **混合数据管理** — Mixed Data: 关系+XML 一引擎的产品叙事。

## 最新演进与工业实践

- **XML 一脉存续但收缩**：Db2 11.5 保留 pureXML/XML 列与 XQuery（官方文档入口 https://www.ibm.com/docs/en/db2 curl 200 ✅），但新工作负载的半结构化主角已是 JSON——Db2 后续补上 SQL/JSON 函数族（JSON_TABLE 等）接棒（⚠️ 转述）。
- **标准风向**：SQL:2016 收 JSON 表函数、SQL:2023 收 JSON 算子（ISO 文书本环境无法逐号取证，标 ⚠️ 只记年份不贴 DOI）；XML 阵营整体进入"存量维护期"。
- **工业现场**：报文类行业（银行 ISO 8583/XML、政务交换、保险单证）仍有大量 DB2 XML 存量资产，迁移策略多为"保留列+网关转 JSON"——本册这章的实用价值恰在读懂这批老库（⚠️ 行业观察二手口径）。
- **对照实验提醒**：想体感"原生 vs 拍平"，可用 DuckDB 读 JSON vs 手工拆表对比开发成本（结论**非 DB2 行为**）。
- **三册线**：#76 认证考纲对 XML 比重已下降、#77 DBA 卷偏存储维护——XML 的概念地形以本册为最全（[00](00-总览与阅读地图.md) 分工表）。
