# 09 SQL 视图与系统安全（原书第 13 章）

> 书目：《Database Systems: A Pragmatic Approach》，Elvis C. Foster & Shripad V. GodBole，Apress 2014，章 DOI `10.1007/978-1-4842-0877-9_13`（pp.259–278）。
> 证据级：章题/页码/DOI ✅；章首段 ✅ 摘要逐字；小节展开 ⚠️ 重构；🔧 为 SQLite/DuckDB 实测，**非本书引擎（Oracle 10g）行为**。

## 1 本章定位与摘要逐字锚

一章双主题、且作者亲自说明为何同章（✅ 逐字）：

> "Two very powerful and important features of SQL are the facility to create and manage logical views, and the capability to manage security issues of a database. This chapter discusses these two related issues. The chapter proceeds under the following subtopics:"（列表截断 ⚠️）

"related"一词点题：**视图是安全的第一实现载体**——行列裁剪靠视图，授权对象靠视图，本册把两者焊在同章是刻意的教学设计。

## 2 内容主讲（⚠️ 按视图×安全双轨重构）

**视图轨**：

- 逻辑（虚）视图定义 `CREATE VIEW v AS SELECT…`；视图即"存进目录的查询"（→ch14 回收，✅ ch14 摘要确证目录职能）。
- 用途三件套：简化复杂查询（把 JOIN 封装成"每系工资榜"）、**定制用户数据视图**（回收 ch6 UI：不同角色看不同切面）、安全隔离（只暴露列/行子集）。
- 可更新视图条件：单表/键保留（⚠️ 教材通行说法）；WITH CHECK OPTION 防"隔墙改牛"。

**安全轨**（2014 Oracle 10g 语境，⚠️ 转述）：

- 系统权限（CREATE SESSION/CREATE TABLE…）vs 对象权限（SELECT/INSERT/EXECUTE ON 具体对象）——Oracle 权限二分法。
- `GRANT/REVOKE` 语法、WITH GRANT OPTION 传播链；角色 ROLE 作授权包（ch11"用户/概要文件"对象的策略面）。
- 视图作为授权载体：把"表级全量"降为"视图级切片"发放。

## 3 🔧 视图行为实测（非本书行为）

- **SQLite 3.45.3（E5/E6）**：一切视图**不可直接写**——`INSERT INTO v1` 报 `cannot modify v1 because it is a view`（无论单表还是 JOIN 视图）；开写入的正道是 **INSTEAD OF 触发器**：`CREATE TRIGGER vi INSTEAD OF INSERT ON vv BEGIN INSERT INTO t VALUES(new.x); END` → 插入成功 `(7,)`。视图定义原文完整存于 `sqlite_master.sql` 列（E6）——"视图=存起来的查询"的字面证据。
- **DuckDB 1.5.5（E6d）**：视图 INSERT 报 `Catalog Error: v2 is not an table`（原文如此）；可写性整体让位于"视图=分析抽象"定位；`duckdb_views()` 目录可查（E6）。
- ⚠️ Oracle（本书）允许简单视图 updatable（key-preserved 规则），与本册"INSTEAD OF 兜底"的叙事在 SQLite 上只能演示触发器半边——差异登记。
- 🔧 安全的最小可行类比（非本书引擎）：SQLite 无 GRANT/ROLE 体系，权限=文件权限+URI `mode=ro`；DuckDB 同理。"把 SELECT 列裁剪封装成视图再暴露"仍是 2026 嵌入式场景唯一现实的"视图即安全"手法（本工作区可跑，属工程实践非引擎特性）。

## 4 与本书其他章的接线

- ←ch6（用户切面）、←ch11（视图=六对象之一 ✅ 摘要）、←ch12（DML 可用于视图的预告 ✅）；→ch14（视图定义入目录）、→ch21（DBA 的授权职责）、→ch22（分布式视图 ⚠️ 推测）。

## 5 对位阅读（实链，已验名）

- [../Databases_Illuminated_4e/12-安全与权限.md](../Databases_Illuminated_4e/12-安全与权限.md)：同代教材把安全独立成章（还含注入/加密——本册全书无专节 ⚠️ 缺口对照）。
- [../Pro_SQL_Server_Internals/07-视图与用户定义函数.md](../Pro_SQL_Server_Internals/07-视图与用户定义函数.md)：索引视图/分区视图的内幕层，视图性能叙事的上限样本。
- [../Understanding_DB2_2e/11-安全实现.md](../Understanding_DB2_2e/11-安全实现.md)：DB2 权限模型对照（本册 ch17 概览的深化版）。
- [../Using_SQLite/10-扩展虚拟表与时间旅行.md](../Using_SQLite/10-扩展虚拟表与时间旅行.md)：SQLite 虚拟表=另一种"查询即对象"的设计谱系（E5 的语境续读）。

## 6 教学与实操要点

1. 视图三问：暴露什么列？限定什么行？谁来写它？——第三问在 SQLite 的答案永远是"触发器代写"（E5）。
2. 授权设计口径：按角色发包（ROLE）而不是按人逐 GRANT；REVOKE 传播链要画依赖图——本章是全书最接近"治理"的 SQL 章。
3. 安全缺口自查（本书级）：无 SQL 注入/最小权限工程/审计专节——2026 面试口径请另行补现代安全读物；本工作区已验名的最近替代是 D-I 12 与 SQL Server 内幕卷的权限章节。

## 7 深挖与自测

### 概念辨析十问
1. 视图存的是数据还是文本？——查询定义文本（E6 sqlite_master 逐字在册）；"物化视图"才是另一物件。
2. 为什么作者把视图与安全放同章？——视图行列裁剪=最小权限的 SQL 表达（✅ "two related issues"）。
3. 可更新视图的通行判定式？——单表+保键+无聚合/DISTINCT/分组（⚠️ 本册口径；SQLite 一律拒绝，E5）。
4. WITH CHECK OPTION 防什么？——防"借视图改出不属于视图的行"（写入谓词逃逸）。
5. 系统权限与对象权限的分界句？——"能不能干这类事" vs "对这个物件能不能干"（Oracle 二分法）。
6. GRANT ... WITH GRANT OPTION 的风险？——授权传播链失控；REVOKE 不必然收回转授（⚠️ 级联口径）。
7. 角色何时优于逐人授权？——岗位=权限包；人动角色不动（回收 ch21 运营面）。
8. 视图能当安全边界的全部吗？——否：元数据泄露/间接推断/性能旁路；需配合引擎权限层。
9. 嵌入式引擎（无 GRANT）如何做"视图即安全"？——裁剪后的视图/API 只读暴露（🔧E5/E6 语境实践）。
10. 本章与 ch14 目录的接口？——视图定义、授权记录都是目录内容；查目录即审计第一步。

### 常见误区六条
- 以为建视图零成本——每次引用都要展开重写（E5 时代 Oracle/开源皆尔）。
- 把视图当物化快照——本书语境无物化视图展开 ⚠️；混淆者等数据"新"来打脸。
- 借视图 UPDATE 不看可更性——三引擎三答案（E5/E6d 实测：只有触发器是 SQLite 正道）。
- 用表名隐藏代替权限控制——改名不是安全；GRANT 面才是。
- 全库 DBA 一票授权到底——最小权限原则从视图开始练习。
- 审计=查登录日志——对象权限/视图定义变更史（目录）更重要。

### 🔧 加餐：视图行为速查（非本书行为）
- SQLite：一切视图只读；INSTEAD OF 触发器开写入→(7,)（E5/E6e）。
- DuckDB：视图 INSERT→Catalog Error "v2 is not an table"（E6d 原文）。
- 定义可查：sqlite_master / duckdb_views()（E6）——审计脚本两行起步。

### 一分钟版
- 一章两轨：视图（怎么藏）×安全（给谁看）。
- "related"是钥匙词：视图是权限的最小实施面。
- 带走模板：角色→对象权限→视图裁剪→目录审计四步闭环。

## 8 术语快卡与跨书对位

| 术语 | EN | 一句话定位 |
|---|---|---|
| 视图 | View | 命名的虚表，存查询不存数据 |
| WITH CHECK OPTION | 视图检查项 | 经视图写入不得逃逸视图条件 |
| GRANT/REVOKE | 授权/收权 | DCL 双子星 |
| 特权 | Privilege | 对象级许可（SELECT/INSERT/…） |
| 角色 | Role | 2026 主流安全单元，本书未及 |
| 授权子语言 | Authorization Sublanguage | SQL 第三层（DCL） |

**跨书对位（盘上已验证目录）**：
- 参 [Databases Illuminated 4e](../Databases_Illuminated_4e/00-总览与阅读地图.md)：视图可更新条件讨论可对照。
- 🔧：E7/E8 实测了视图与权限面（SQLite 无 DCL，DuckDB 1.5.5 有角色雏形）。

**速测**：合上书，用一句话向同事讲清本册最难的概念；讲不清就回到 §7 误区清单重读。

**快验证问答（补）**

- Q：视图何时不可更新？A：含聚集/连接组等构造时（本书口径）。
- Q：WITH CHECK OPTION 防什么？A：防经视图写入"逃逸出"视图条件。
- Q：授权给 PUBLIC 后剩什么课题？A：回收粒度与最小权限审计。

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|---|---|---|
| 逻辑视图 | logical view | 存起来的查询，无独立数据 |
| 可更新视图 | updatable view | 单表键保留才可直写（⚠️ 本册口径） |
| WITH CHECK OPTION | with check option | 经视图写入不得逃逸谓词 |
| 系统权限 | system privilege | 能不能干这类事 |
| 对象权限 | object privilege | 对这个对象能不能干 |
| GRANT/REVOKE | grant/revoke | 授权与撤权（传播链注意） |
| 角色 | role | 权限包，DBA 的手柄 |
| INSTEAD OF 触发器 | INSTEAD OF trigger | 🔧 SQLite 视图写入唯一正道（非本书） |

## 最新演进与工业实践

- **行列级安全产品化**：云仓原生 RLS/列掩码（Snowflake row access policy + data masking；PG `ROW SECURITY`）把本章"视图代偿"方案下沉为引擎一等公民——✅ https://docs.snowflake.com/en/user-guide/intro-key-concepts（200，站内 security 域）。
- ✅ SQL Server 角色体系文档锚点（本册 GRANT/ROLE 叙事的现代版）：https://learn.microsoft.com/en-us/sql/relational-databases/security/authentication-access/database-level-roles（200 验真）。
- **API 层接管视图**：GraphQL/语义层把"每角色看每切面"移出资深 BI 的 SQL 视图实现——概念不变、宿主漂移。
- **嵌入式安全现实**：SQLite 的 URI `mode=ro`+SQLCipher 生态与 DuckDB 只读 ATTACH 是 2026 端侧"最小权限"的两张真牌（🔧 本工作区可测性有限，登记为工程实践）。
