# 第 23 章 XML

> **本章地图**：XML 数据模型（元素、属性、**命名空间**、ID/IDREF、良构 vs 有效）→ **DTD / XML Schema（XSD）** → **查询与转换**：**XPath**（路径表达式与轴）、**XQuery**（FLWOR）、**XSLT** → **XML 存储**（原生 XML 数据库 vs 映射到关系表）→ **SQL/XML**（`XML` 类型、`XMLTABLE`、`XMLELEMENT` 等）→ XML 应用（SOAP/Web Service、配置文件、OOXML/ODF）→ 现实：**JSON 取代了 XML 作为数据交换格式**，XML 退守配置文件与企业集成领域。

## 二、核心精讲

### 23.1 XML 数据模型
- **元素（element）**、**属性（attribute）**、文本内容、**命名空间**（`xmlns:ns="URI"` 消除同名冲突）、**ID / IDREF(S)**（XML 内部的引用机制，类似外键）、**CDATA / 实体引用**。
- **良构（well-formed）**：语法正确；**有效（valid）**：符合某个 DTD 或 Schema。
- 🔧 XML 是**有序、层次化**的半结构化模型，与关系的无序集合模型根本不同 —— 顺序的保留是 XML 映射到关系表时最麻烦的点。

### 23.2 DTD 与 XML Schema
- **DTD**：`<!ELEMENT>`、`<!ATTLIST>`，语法非 XML、类型系统弱（几乎只有 `#PCDATA`）。
- **XML Schema（XSD）**：本身是 XML，提供**强类型**（`xs:int`、`xs:date`）、复杂类型、继承/扩展（`extension` / `restriction`）、`key` / `keyref` 约束。
- 🔧 对照第 8 章：XSD ≈ XML 世界的「模式定义 + 完整性约束」；`key`/`keyref` 对应主键/外键。现代对照：**JSON Schema**（Draft 2020-12）承担同样角色，且被 OpenAPI/Swagger 广泛采用。

### 23.3 查询：XPath / XQuery / XSLT
- **XPath**：路径表达式 `/bookstore/book[price>30]/title`，支持**轴**（`child::`、`parent::`、`descendant::`、`following-sibling::`…）、谓词、函数。XPath 是 XQuery 与 XSLT 的共同基础。
- **XQuery**：**FLWOR** 表达式（`for / let / where / order by / return`）—— 与 SQL 的 `SELECT ... FROM ... WHERE ... ORDER BY` 高度对应，是理解「声明式查询可以脱离关系模型」的最佳例子：
  ```xquery
  for $b in /bookstore/book
  where $b/price > 30
  order by $b/title
  return $b/title
  ```
- **XSLT**：把 XML 转成 HTML/其他 XML 的**声明式转换语言**（模板驱动，函数式风格）。
- 🔧 现代对照：**JSONPath / JMESPath / jq** 之于 JSON，就是 XPath/XQuery 之于 XML；**SQL 的 JSON 函数**（`jsonb_path_query` in PG、JSON_TABLE in MySQL 8）把两者统一起来了。

### 23.4 XML 存储：原生 vs 关系映射
- **原生 XML 数据库**（eXist-db、BaseX、MarkLogic）：直接存 DOM 树，保留顺序与结构，用专用索引加速 XPath/XQuery。
- **映射到关系表的三种策略**：
  1. **边表 / 通用表**（`Edge(parent, child, label)`）——通用但查询爆炸；
  2. **按 Schema 分解**（shredding，每个复杂类型一张表）——查询快但依赖 schema；
  3. **整篇存为 CLOB + XML 索引**（Oracle XML DB、SQL Server `xml` 类型）——折中方案。
- 🔧 现实：**Shredding 的思路被 JSON 继承**（MongoDB 的 WiredTiger 存 BSON；PG 的 jsonb 是分解后的二进制树结构，支持 GIN 索引）；而「通用边表」的教训直接化为**NoSQL 反模式警告**。

### 23.5 SQL/XML
- SQL:2003 引入 `XML` 类型与一组函数：`XMLELEMENT`、`XMLATTRIBUTES`、`XMLAGG`、`XMLTABLE`（**把 XML 拆解为关系行**，最实用）、`XMLQUERY`、`XMLEXISTS`。
- 🔧 工程价值：`XMLTABLE` 是批量导入 XML/UBL 发票、SOAP 响应的最简洁方式；Oracle/DB2/SQL Server 均支持良好，PostgreSQL 用 `xpath()`/`xmltable` 近似（PostgreSQL 10+ 有 `xmltable`）。

### 23.6 XML 的应用与衰退
- 曾被广泛期待的方向：**Web Service（SOAP/WSDL/UDDI）**、**配置文件**（Ant、Maven `pom.xml`、Spring 的 `applicationContext.xml`）、**文档格式**（OOXML、ODF）、**行业数据交换**（UBL、HL7、FpML）。
- 🔧 现实判断（重要）：
  - **数据交换**：JSON 胜出（HTTP API、NoSQL、浏览器原生）。XML 仍占主导的是 **企业级/强 schema 场景**（金融报文、航空、医保 HL7 v3、UBL 发票、Android 布局、Maven/Spring 配置）。
  - **Web Service**：REST/JSON + gRPC/Protobuf 取代 SOAP；但 **WSDL/SOAP 在银行与电信老系统中仍大量存在**。
  - **XML 的安全教训**：**XXE（XML External Entity）注入**、**十亿笑攻击（billion laughs，实体展开 DoS）**——OWASP 长期列为高危；Java 的 `DocumentBuilderFactory` 必须禁用外部实体。这是本章在现代安全语境下最该记住的实用点。

## 三、经典论文与原始文献

| 论文/标准 | 出处 | 贡献 |
| --- | --- | --- |
| W3C《Extensible Markup Language (XML) 1.0》 | W3C Recommendation 1998 | 语法标准 |
| W3C《XML Schema Part 0/1/2》 | W3C 2001 | XSD 类型系统 |
| W3C《XPath 1.0 / 3.1》《XQuery 1.0 / 3.1》 | W3C 1999 / 2017 | 查询语言 |
| 《SQL/XML》（SQL:2003 Part 14） | ISO/IEC 9075-14 | XML 与 SQL 的桥 |
| Florescu & Kossmann《Storing and Querying XML Data using an RDMBS》 | IEEE Data Eng. Bull. 1999 | 关系映射路线的奠基讨论 |
| Shanmugasundaram et al.《Relational Databases for Querying XML Documents: Limitations and Opportunities》 | VLDB 1999 | shredding 方案 |
| Al-Khalifa et al.《Structural Joins: A Primitive for Efficient XML Query Pattern Matching》 | ICDE 2002 | XML 结构连接 |

## 四、近年研究与工业界开源实践

- **近年研究**：**JSON 半结构化的存储与查询优化**（`jsonb` 的 GIN 索引、DuckDB/Presto 的 JSON 函数下推）；**多模数据库**（PostgreSQL 同时支持关系/JSON/XML/向量）；**XML 流式处理的性能**（StAX / SAX vs DOM）；**XML 安全**（XXE 防御自动化检测）。
- **工业界开源**（star 数 2026-09 实测）：
  - `BaseXdb/basex`、`eXist-db/exist`（轻量原生 XML 数据库）：XQuery 3.1 的完整开源实现，是练习本章内容的最佳工具。
  - `postgresql/postgres`（≈17k★）：`xml` 类型 + `xpath()` + `xmltable`；`src/backend/utils/adt/xml.c`。
  - `mysql/mysql-server`：`ExtractValue()` / `UpdateXML()`（基于 libxml2）。
  - `apache/xerces-c`、`FasterXML/jackson-xml`、`javax.xml`（JDK 内置 JAXP）：解析器生态；**JDK 的 JAXP 默认已禁用外部实体**（JDK 8u 起逐步加固），但仍应显式配置。
  - `protocolbuffers/protobuf`（≈67k★）、`grpc/grpc-java`（≈11k★）：XML/SOAP 的现代替代品。

## 五、常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "XML 会成为下一代通用数据格式" | **JSON 才是**（2010 年后已见分晓）；XML 退守企业集成与配置 |
| 2 | "XQuery 会取代 SQL" | 不会；SQL 通过 **JSON/XML 函数**吸收了半结构化查询能力 |
| 3 | "XML 属性与元素可随意互换" | 属性不可重复、无顺序、不能嵌套；建模时需区分（属性=元数据，子元素=结构） |
| 4 | "解析 XML 很安全" | **XXE / billion laughs** 是真实高危漏洞，必须禁用外部实体与 DTD |
| 5 | 🔧 本书定位 | 本章在 2020 年代主要价值是**理解半结构化模型的理论问题**（顺序、路径查询、schema 校验），具体技术应迁移到 **JSON/JSON Schema/JSONPath** |
