# 08 SQL 数据操纵语句（原书第 12 章）

> 书目：《Database Systems: A Pragmatic Approach》，Elvis C. Foster & Shripad V. GodBole，Apress 2014，章 DOI `10.1007/978-1-4842-0877-9_12`（pp.219–258，40 页）。
> 证据级：章题/页码/DOI ✅；章首段 ✅ 摘要逐字；语句清单细节 ⚠️ 重构；🔧 为 SQLite/DuckDB 实测，**非本书引擎（Oracle 10g）行为**。

## 1 本章定位与摘要逐字锚

DML 主场章。首段是全书对 SELECT/INSERT/UPDATE/DELETE 最干净的定性（✅ 逐字）：

> "There are four core DML statements in SQL, namely INSERT, UPDATE, DELETE, and SELECT. These statements apply to base tables and views (views will be discussed in the next chapter). The chapter proceeds under the following subheadings:"（列表截断 ⚠️）

注意两点一手信息：**四核心语句**的名录（不含 MERGE——SQL:2003 才有，2014 教材按 Oracle 口径常单列 ⚠️）；**DML 同样作用于视图**的预告（衔接 ch13）。

## 2 内容主讲（⚠️ 按 40 页体量+Oracle 10g 课堂口径重构）

- **INSERT**：单行 VALUES、多语句脚本式批量、`INSERT INTO … SELECT`（派生/装载的主力）、子查询作源；序列对象喂主键（回收 ch11 的 SEQUENCE ⚠️）。
- **UPDATE / DELETE**：WHERE 谓词+相关子查询定位；"没有 WHERE 的 UPDATE=事故"式的工程告诫（⚠️ 教材惯例）。
- **SELECT 全集**：投影/别名、WHERE、GROUP BY+HAVING、ORDER BY、多表连接（等值/外连接——Oracle 旧式 `(+)` 外连接语法与 ANSI JOIN 并存于 2014 教材 ⚠️）、集合运算 UNION/INTERSECT/MINUS、嵌套查询（IN/EXISTS/标量子查询）、聚合与 NULL 的纠缠。
- ⚠️ 可能含 cursors/embedded SQL 小节（同作者《Databases Demystified》有此配置）——本册无逐字证据，不下断言。

## 3 🔧 双引擎 DML 实测（非本书行为）

- **RETURNING 子句**：SQLite 3.45.3 ✅（E3：`UPDATE emp SET salary=salary*1.1 WHERE did=10 RETURNING eid, salary` → `[(1,110.0…),(2,132.0…)]`）；DuckDB ✅ 同款并回 `Decimal('110.00')`——本书年代这属于"扩展方言"（Oracle 仅 PL/SQL 内 DML RETURNING ⚠️），2026 已是开源双雄标配。
- **UPDATE…FROM 跨表更新**：**两引擎都支持**（E3b：SQLite 3.33+ `UPDATE emp SET salary=salary*1.2 FROM dept WHERE emp.did=dept.did AND dept.dname='Eng'` → 120/144 生效；DuckDB 同构）。Oracle 10g 需相关子查询写法——方言代差 sample 1（⚠️ 转述）。
- **事务性 DML**：E3 `BEGIN; UPDATE; ROLLBACK` 保 90.0——DML 与事务的绑定在 SQLite（库级锁）与 DuckDB（快照隔离语义简化版）都即时可感；本书 DML 章不讲事务（无专章 ⚠️ 全书缺口，见 00 §5）。
- **CTE 即查询管线**（E3/E7）：`WITH RECURSIVE n(i)…` 造 50 万行事实表、`WITH t AS (…avg…) JOIN t` 做"高于均值"过滤——SQL:1999 递归 CTE 是 ch15"程序性局限"的解药之一（E7 用它替游标）。
- **窗口函数**（E3）：DuckDB `rank() OVER (PARTITION BY did ORDER BY salary DESC)` → `[(1,2),(2,1),(3,1)]`；SQLite 3.25+ 亦备——本书 SQL 部类止于 GROUP BY（⚠️ 教材年代），此处补 2026 必修件。

## 4 与本书其他章的接线

- ←ch4（改数据不得破约束——E1/E2 执法面）、←ch7/8（代数算子的 SQL 同构）、←ch11（可写对象先由 DDL 定义）；→ch13（视图可 DML 化的条件）、→ch14（DML 计划/统计入目录）、→ch15（复杂操纵的无力感）。

## 5 对位阅读（实链，已验名）

- [../Databases_Illuminated_4e/05-SQL进阶-连接子查询与视图.md](../Databases_Illuminated_4e/05-SQL进阶-连接子查询与视图.md)：连接/子查询的教材级进阶面（含优化视角）。
- [../Using_SQLite/08-事务锁与变更.md](../Using_SQLite/08-事务锁与变更.md)：SQLite 事务性 DML 的专册章（E3 的回声）。
- [../Database_Administration_2e/08-应用性能与SQL调优.md](../Database_Administration_2e/08-应用性能与SQL调优.md)：把"写得出 SELECT"升级为"写得快"的 DBA 章。
- [../设计数据密集型应用/02-数据模型与查询语言.md](../设计数据密集型应用/02-数据模型与查询语言.md)：声明式查询语言的当代定位总论。

## 6 教学与实操要点

1. 四核心语句的**方向性**记忆：INSERT 管进门、SELECT 管出门、UPDATE/DELETE 管改杀；一切"装载/回滚/审计"话题都归队到这四个门。
2. 教学顺序建议：先教 `INSERT…SELECT`（数据生成器）再教子查询——E7 的百万行造数靠这一招。
3. 无 WHERE 的 UPDATE/DELETE 练习必须配 E3 的 BEGIN/ROLLBACK 习惯；生产 SQLite 上再加 changes() 自检。
4. 方言代差三口井：外连接（ANSI vs `(+)`）、集合差（EXCEPT vs MINUS）、跨表更新（UPDATE…FROM vs 相关子查询）——面试与读老代码双向防身。

## 7 深挖与自测

### 概念辨析十问
1. 四核心（✅ 摘要）里 SELECT 为何最特殊？——演算的直接投影；其余三个改状态。
2. INSERT…SELECT 与 COPY/装载工具分界？——行级语义 vs 批量字节流；仓库场景后者胜（ch24）。
3. UPDATE 自引用读新值还是旧值？——旧值：同语句声明式并行安全，不靠书写顺序。
4. 相关子查询何时劣于 JOIN？——语义=逐行循环；多数引擎可去相关但手改 JOIN 常提速（⚠️ 引擎而异）。
5. 清空全表三写法成本序？——DELETE 无 WHERE（逐行日志）>TRUNCATE（页级）>>DROP+建（本册是否辨析 ⚠️）。
6. 视图上的 DML 边界？——三引擎三答案：Oracle 简单视图可（⚠️ 本书口径）/SQLite 全否+触发器（E5）/DuckDB 否（E6d）。
7. HAVING 与 WHERE 本质差？——执行序（分组前后）+可用表达式（聚合有无）。
8. NULL 在聚合中的蒸发规则？——COUNT(*) 数行、其余数非 NULL——AVG 陷阱题之源。
9. 集合运算谁最方言？——差集：EXCEPT（标准/开源）vs MINUS（Oracle/DB2 旧口径 ⚠️）。
10. RETURNING 属四核心吗？——是 DML 的"结果回执"扩展（SQL:2003 血统；🔧E3 双引擎标配）。

### 常见误区六条
- UPDATE 不带 WHERE 就敢跑——BEGIN/ROLLBACK 先行（E3）+影响行数自检。
- 游标思维写 SQL——先集合式（CTE/窗口），游标作最后手段（ch15 论战工程版）。
- 以为 `<>` 自动排除 NULL——NOT IN 遇 NULL 全灭（三值逻辑恒考点）。
- 子查询三层起步——可读性债；CTE 命名化（E3/E7 范式）。
- DISTINCT 无感知税——每次=一个去重算子（EXPLAIN 可见）。
- 把 UPDATE…FROM 当到处可写——Oracle 10g 无此语法（⚠️ E3b 代差标本）。

### 🔧 加餐：DML 手感三跑（非本书行为）
- E3 RETURNING + BEGIN/ROLLBACK 保 90.0，60 秒。
- E3b SQLite 也支持 UPDATE…FROM——"开源=落后"错觉的标本级反驳。
- E7 递归 CTE 造数+JOIN 装载宽表=一条流水线三考点。

### 一分钟版
- 四个动词进门（✅ 摘要"four core DML statements"）。
- 视图可 DML 是本章埋的引子，下一章接火（✅ "views will be discussed in the next chapter"）。
- 手感三件套：事务先行、集合式优先、NULL 常备怀疑。

## 8 术语快卡与跨书对位

| 术语 | EN | 一句话定位 |
|---|---|---|
| INSERT/UPDATE/DELETE | 数据操纵 | 写路径三件套 |
| 相关子查询 | Correlated Subquery | 逐行引用外层值的子查询 |
| 聚集函数 | Aggregate | COUNT/SUM/AVG/MIN/MAX |
| GROUP BY/HAVING | 分组与过滤 | 先分组再筛组 |
| 连接写法 | Join Syntax | FROM 逗号式 vs 显式 JOIN |

**跨书对位（盘上已验证目录）**：
- 参 [SQL_and_Relational_Theory]：子查询等价改写的理论纵深（盘上登记，不链）。
**速测**：合上书，口述一条 UPDATE 违约参照完整性时引擎该报什么。

**速测**：合上书，用一句话向同事讲清本册最难的概念；讲不清就回到 §7 误区清单重读。

**快验证问答（补）**

- Q：INSERT INTO…SELECT 的用途？A：跨表批量搬运/临时表。
- Q：HAVING 为何不能替代 WHERE？A：WHERE 在分组前过滤，HAVING 在分组后筛组。
- Q：相关子查询慢在哪？A：外层每行都可能重跑一遍。
- Q：无 WHERE 的 UPDATE 风险？A：全表改写；生产先跑同条件 SELECT 验数。
- Q：显式 JOIN 的血脉？A：代数 ×+σ，工程上换成可读的连接语法。

**一句**：写路径先想回滚，读路径先想索引。

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|---|---|---|
| 数据操纵语言 | Data Manipulation Language (DML) | 四核心语句的总称（✅ 摘要） |
| 插入-查询式 | INSERT INTO … SELECT | 装载与派生的主力 |
| 相关子查询 | correlated subquery | 逐行参照外层的谓词 |
| EXISTS/IN | EXISTS / IN | 半连接双写法 |
| 分组过滤 | GROUP BY / HAVING | 聚合前后各一刀 |
| 集合运算 | UNION/INTERSECT/MINUS(EXCEPT) | 关系并交差入语法 |
| 返回子句 | RETURNING | 🔧 双引擎标配（非本书） |
| 游标/嵌入式 SQL | cursors/embedded SQL | ⚠️ 本册可能涉及，未取证 |

## 最新演进与工业实践

- **MERGE 成为第一公民**：SQL:2003 的 MERGE 已进 MySQL 8.4/Oracle/PG（upsert 变体）与湖仓格式（Delta `MERGE INTO` 带 CDF）——本册"四核心"扩为五核的现在时；✅ https://dev.mysql.com/doc/refman/8.4/en/（200）。
- **管道层接管 DML**：dbt incremental model/Spark Structured Streaming 的 append/merge 语义替代手写 `INSERT…SELECT`，盘上续读 [../Analytics_Engineering_with_SQL_and_dbt/02-SQL数据建模.md](../Analytics_Engineering_with_SQL_and_dbt/02-SQL数据建模.md)（grep 验名）。
- **DuckDB 批量 DML 实测感**：`INSERT INTO big SELECT range… FROM range(1000000)` 一行造百万行（E4，秒级）——2026 分析侧 DML 的性能叙事已从"索引"转向"向量化+行组统计"。
- ⚠️ Oracle 侧事务/DML 内幕续读盘上 [../Oracle_Essentials_5e/01-关系模型与SQL基础.md](../Oracle_Essentials_5e/01-关系模型与SQL基础.md)。
