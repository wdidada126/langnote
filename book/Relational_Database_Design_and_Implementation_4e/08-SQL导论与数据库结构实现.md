# 08-SQL导论与数据库结构实现（Part III 导言 p.181 ✅；Ch10 Introduction to SQL, pp.183–190 ✅；Ch11 Using SQL to Implement a Relational Design, pp.191–213 ✅）

> 三态：✅ 书页 TOC/Crossref 页码实抓 · ⚠️ 转述/推定展开 · 🔧 本机 SQLite/DuckDB 实测（**非本书示范行为**）。
> 设计篇（Part II）到此结束，实践篇开场：Ch10 给 SQL 的历史与 conformace 等级地图，Ch11 把 ER/规范化产出物写成 DDL——数据库结构层级、SCHEMA、DOMAIN、TABLE、ALTER/DROP。本章是 🔧 E2 约束矩阵的主战场。

## 一、精读札记（官方二级小节 ✅ 逐条）

**Ch10 Introduction to SQL（183–190）**
- A Bit of SQL History —— IBM System R/SEQUEL 血统，ANSI-89 起点 ⚠️ 通说。
- Conformance Levels —— Full/Core/Entry 三级（SQL-92 遗产框架）；「完全兼容」的营销话术与现实的裂缝。
- SQL Environments —— 模块式（主机语言+SQLDA）vs 交互式（命令行即席）——2016 版仍以此二分 ⚠️。
- Elements of a SQL Statement —— 动词表：SELECT/INSERT/UPDATE/DELETE + DDL 族。

**Ch11 Using SQL to Implement a Relational Design（191–213）**
- Database Structure Catalog/Schemas → 层级：CATALOG→SCHEMA→TABLE/COLUMN/DOMAIN。
- Domains —— CREATE DOMAIN：命名域+默认值+CHECK（本书用 SQL 标准语义；方言支持度见 §2.2）。
- Tables —— CREATE TABLE 全要素：列定义、PK/UNIQUE/FK/CHECK 四约束语法位 ⚠️（页内例句不可达）。
- Modifying Database Elements —— ALTER TABLE 族（加列/改类型/挂约束）。
- Deleting Database Elements —— DROP 与级联（RESTRICT/CASCADE 语义）。

## 二、主题深读

### 2.1 🔧 E2 实测：DDL 四约束的方言执法矩阵（非本书示范行为）
demos.txt 完整实录（SQLite 3.45.3 + DuckDB 1.5.5）：
```
SQLite: FK pragma OFF 孤儿 1 行不拦；【陷阱】事务中 PRAGMA foreign_keys=ON 是 no-op
        → 提交后再 ON：FOREIGN KEY constraint failed；UNIQUE constraint failed: u.a
DuckDB: FK「Violates foreign key constraint because key "id: 9" does not exist...」（即插即拦）
        UNIQUE「duplicate key "1"」/ CHECK「CHECK constraint failed on table ck with expression CHECK((a > 0))」
        复合 PK「duplicate key "1, 1"」
```
教科书把「约束」当标准语句，工程要回答的是「谁执法、何时执法、怎么开关」。Ch11 的 DDL 语法面在 SQLite 上**部分住着而不执法**（FK），在 DuckDB 上**全部执法**（与 2016 教材默认的商业 DBMS 行为一致——这一条 2026 实测反而推翻了「分析引擎松约束」的旧印象）。

### 2.2 DOMAIN 与 ALTER TABLE 的方言落差
- SQL 标准 DOMAIN=可复用类型对象；🔧 本机两载体均不支持 CREATE DOMAIN ⚠️→用 CHECK+列定义模拟；PostgreSQL 支持但工业采用率低。
- ALTER TABLE 族在 SQLite 的残缺（不能 DROP COLUMN 老版本/不能改类型）是 2016 教材不讲的痛；SQLite 官方改造手册（12-step ALTER）✅ https://www.sqlite.org/lang_altertable.html（实查）是本章「修改数据库元素」小节的当代必读附页。
- DROP 级联语义（CASCADE/RESTRICT）SQLite 在 FK 上下文生效（依赖 foreign_keys 开关，E2 已证）——「声明-执法-开关」三层结构在删除方向同样成立。

### 2.3 结构层级：CATALOG/SCHEMA 的教材遗产 vs 工业现实
书内三层目录树（catalog→schema→table）是 SQL-92 模型；2026 工业的三向变形：SQLite/DuckDB 的「文件=库+ATTACH 挂载多目录」轻量形（🔧 盘上 Using_SQLite 有 ATTACH 实验 ✅ 在册可纵读）、云仓的「catalog-schema-table 三层回归+按量计费命名空间」（波10 云仓线）、湖仓的「Iceberg namespace 映射」（在册 Apache_Iceberg活用入門 ✅）。同一层级树，三种物理化。

### 2.4 Ch10 conformance 话语的今日用法
「支持 SQL:2016/2023」的市场话术仍对应 Core/Entry 现实：SQLite 官方自述遵循 SQL-92 核心+扩展方言 ⚠️（转述），DuckDB 走「PostgreSQL 方言超集+分析扩展」路线——教学结论不变：**conformance level 是采购审查项，不是信仰条款**。

### 2.5 SQL 标准线年表（补 Ch10 Conformance 小节的时代坐标，⚠️ 通识）
书内 Conformance Levels（✅ 节题）用的是 Entry/Intermediate/Full 旧语；标准线此后走过 SQL:1999（窗口函数与 UDT 入库——后者即 Ch27 的正文）、SQL:2003（MERGE 与正则）、SQL:2011（时态语义——17 数仓时变特征的语法化）、SQL:2016/2023（JSON 关系化——18 §2.2 的收编法律文本）。教材不写版本流水（依小节清单 ⚠️），本册登记一句：**conformance 是谈判面不是及格线**——每代标准件都有「先实现后改名」的方言史，MERGE 是书内 2016 就近可见的标本（13 §2.2 已开）。

### 2.6 Ch11 实施三事：DOMAIN / ALTER / DROP 的方言账
- Domains（✅ 节题）：标准把「域」升格为独立对象——本机两载体均不提供可建 DOMAIN（⚠️ 依两引擎公开文档面；替代物=CHECK+列注解，🔧 E2 实录 CHECK 执法在 DuckDB/SQLite 均生效，非本书示范行为）。03 §2.6 给语义面，本节给语法面。
- Modifying Database Elements（✅）：SQLite 的 ALTER 是裁剪面（官方 lang_altertable 页 ✅ 在 00 取证链；重建舞=备份→新表→搬运→改名十二步量级 ⚠️ 文档转述）——「结构修改」在弱 DDL 方言里是数据迁移项目。
- Deleting Database Elements（✅）：DROP 的依赖处置（CASCADE/RESTRICT）是 E2 FK 执法矩阵的反向半张；先删子后删父的手序错误=约束在替你排队（🔧 载体常识注）。

### 2.7 SQL Environments 一节的 2026 谱系（08 §2.4 续）
Ch10 的三形态（interactive/embedded/module，✅ 节题）今日对位：交互→CLI+笔记本+网页控制台；嵌入→驱动游标范式（19 §2.2，ESQL 是其祖先）；模块→存储过程与 UDF。教材没预见的第四形态=**远端 SQL**：查询网关、HTTP 端点、LLM 作为 SQL 的新宿主语言。三分类不过时，只是长出了新头——环境节的真正教义是：**SQL 是被宿主语境定义的协议**。

## 三、原书 → 2026 对位

| 书内论点 (2016) | 2026 现状 |
|---|---|
| 模块式 vs 交互式环境 | ORM/查询生成器成「模块式」主流形态；交互式由 notebook 接管 |
| DDL 一次成型、小心 ALTER | schema 迁移工具链（版本化 SQL/expand-contract 模式）把 ALTER 变例行公事 |
| DOMAIN 复用约束 | 工业替身=共享 CHECK 模板/dbt tests/数据契约枚举 |
| DROP 谨慎 | 软删除+审计列（deleted_at）成默认；物理 DROP 留给分区生命周期 |

## 四、阅读自测
1. 画出 E2 的「声明-执法-开关」三层，并标注 SQLite/DuckDB 各在哪层缺件。
2. FK 孤儿行在 SQLite 里出现需要什么条件组合？（提示：pragma+事务态）
3. CREATE DOMAIN 与「列+CHECK+默认值」的表达力差在哪里？
4. ALTER 加 NOT NULL 列到 500 万行表的两步安全舞是什么？
5. 为什么 Ch10 的 conformance 三级框架至今仍是 RFP 审查模板？

## 五、互链
- 上游：06（分解结果交 DDL）、07（Rule 5/10 的语言面）。
- 下游：14（结构对象续建）、16（Rule 12 与安全）、10（案例 DDL 全文位）。
- 谱系：[../Using_SQLite/00-总览与阅读地图.md](../Using_SQLite/00-总览与阅读地图.md)、[../DuckDB_Up_and_Running/00-总览与阅读地图.md](../DuckDB_Up_and_Running/00-总览与阅读地图.md)、[../Relational_Theory_for_Computer_Professionals/13-SQL约束.md](../Relational_Theory_for_Computer_Professionals/13-SQL约束.md)、[../Databases_Illuminated_4e/00-总览与阅读地图.md](../Databases_Illuminated_4e/00-总览与阅读地图.md)。

## 核心概念速览（中英对照）
| 中文 | 英文 | 出处/一句话 |
|---|---|---|
| 一致性等级 | conformance levels | Ch10 Full/Core/Entry |
| 模块式/交互式环境 | module/interactive environment | Ch10 使用面二分 |
| 数据库层级 | database structure hierarchy | Ch11 catalog→schema→table |
| 模式 | schema | Ch11 命名空间 |
| 域 | domain | Ch11 可复用类型对象 |
| 建表 | CREATE TABLE | Ch11 约束四件套宿主 |
| 主键约束 | primary key constraint | E2 两引擎均执法 |
| 外键约束 | foreign key constraint | E2 SQLite 开关/DuckDB 执法 |
| 检查约束 | CHECK constraint | E2 DuckDB 报错原文可读 |
| 唯一约束 | UNIQUE constraint | E2 执法矩阵成员 |
| 修改元素 | ALTER 族 | Ch11 + SQLite 12-step 附页 |
| 级联删除 | DROP ... CASCADE | Ch11 依赖方向执法 |
| conformance 语史 | conformance levels | §2.5 旧三级语言 ✅ |
| SQL:1999 | SQL-99 | §2.5 窗口/UDT 入库 |
| SQL:2003 | SQL-03 | §2.5 MERGE 出处 |
| SQL:2011 | SQL-11 | §2.5 时态语法→17 |
| SQL:2016/2023 | SQL-16/23 | §2.5 JSON 关系化→18 |
| 谈判面读法 | conformance-as-negotiation | §2.5 不及格线论 |
| 域对象空缺 | DOMAIN absence | §2.6 两载体不建域 |
| ALTER 裁剪面 | ALTER subset | §2.6 重建舞出处 ✅ 文档页 |
| DROP 依赖序 | drop-order discipline | §2.6 CASCADE 反账 |
| 远端 SQL | remote SQL | §2.7 第四形态 |
| 查询网关 | query gateway | §2.7 现代宿主 |
| LLM 宿主语言 | LLM as host | §2.7 新头 ⚠️ |
| 语句构成 | elements of a SQL statement | Ch10 节 ✅ |
| 环境协议论 | protocol view | §2.7 SQL 被语境定义 |
| 执法矩阵 | enforcement matrix | 🔧 E2 四格（非本书示范） |

## 最新演进与工业实践
- SQLite ALTER 官方规程实查 200：https://www.sqlite.org/lang_altertable.html ✅（2026-10-02）——「表重建十二步」仍是嵌入式现场最可靠的改表手册；DuckDB 约束文档 ✅ https://duckdb.org/docs/stable/sql/constraints 记录全约束执法现状（E2 实测与之相符）。
- 迁移工程化：expand-contract（先加后删双写窗口）+ 版本目录迁移脚本已是团队标配；教学 DDL 章的 2026 增补重点不是语法而是**迁移编排** ⚠️ 通说。
- 与波内教材线对位：#1《Database Systems: A Pragmatic Approach》（Apress，同波待建，00 §七登记）的 SQL 章组织亦走「标准语义+单一工程方言」路线；本目录 E2 的双方言矩阵法是同题的更廉价实验设计。
- 标准年表给教材补「此后十年」附录位——conformance 话语是 1990s 化石（§2.5）。
- Ch11 实施章身份：02/03/04/06 纸面规则在此变 DDL——落地层全册索引。
- 方言账三节均有 🔧/✅ 双轨：CHECK 执法（E2）、altertable 页、FK 反序（demos；非本书示范）。
- 云仓 DDL（聚簇键/生命周期）已超标准——conformance 话语继续贬值（⚠️）。
- 毕业判据：画「书内标准态 vs 两载体实测态」四约束对照并指两处分歧。
- SQL Environments 三分类（§2.7）与 19 AppB 互文：形态史即宿主史。
- 「生成物必须过人审」从 09 codegen 延到 08 迁移脚本——同一工程红线。
- 先删父的报错是约束替你排队（§2.6 注；demos 可复跑，非本书示范）。
- 文档 URL 账：constraints/altertable 等页在 00 取证链 ✅（2026-10-02 口径）。
- 结构层级（§2.3）CATALOG 话语遗产：三段式命名+湖仓 catalog 分层（⚠️）。
- 与 13 接缝：建表→改数=表生命周期两半（13 §2.7 对位）。
- 载体提醒：方言体验=两栈切换（demos 头注）——教材不做的对照本册补。
- 波内登记：#1 兄弟 SQL 章互链义务在其侧落链（00 §七）。
