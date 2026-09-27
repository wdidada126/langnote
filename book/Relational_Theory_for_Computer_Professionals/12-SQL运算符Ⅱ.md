# 第 12 章　SQL 运算符Ⅱ（SQL Operators II ⚠️ 回译）

> 译本 p157–167｜小节（✅ 实抓）：12.1 MATCHING 与 NOT MATCHING / 12.2 EXTEND / 12.3 映像关系 / 12.4 聚集和归纳（12.4.1 归纳、12.4.2「通用的限制」）/ 12.5 练习 / 12.6 答案。
> 这一章的结论最"扫兴"：第 5 章的四个算子里，SQL 有一个勉强能模拟、一个语法化了一半、一个完全没有。**缺的不是语法，是关系值层次的表达力。**

## 本章地图

| 小节 | 模型算子 | SQL 有没有 | 结论 |
| --- | --- | --- | --- |
| 12.1 | `MATCHING` / `NOT MATCHING (BY)` | 无算子，有 `EXISTS` / `NOT EXISTS` 谓词 | 语义可达，但**结果不是可操作的关系**（只能待在 WHERE 里） |
| 12.2 | `EXTEND` | SELECT 列表表达式 | 位置错了：派生列在最末尾求值，不能用于 WHERE/GROUP BY（11.8 的顺序） |
| 12.3 | 映像关系（子关系） | 无 | SQL 没有"某组的子关系"这个值；只能用相关子查询重算 |
| 12.4 | `SUMMARIZE` + 聚集 | `GROUP BY` + 聚合 | 语法可用，但聚集的定义域问题（空组）与不可组合性暴露 |
| 12.4.2 | 广义约束（用聚集表达断言） | 只能塞进 `HAVING` / 触发器 | 断言层缺失（→ 第 6 章 🔧、第 13 章） |

## 核心精讲

### 1. MATCHING / NOT MATCHING：可达，但不可组合（12.1）

🔧 实测（D5b/D5c，SQLite 3.45.3）：

```sql
SELECT * FROM S WHERE EXISTS (SELECT 1 FROM SP WHERE SP.SN = S.SN AND SP.QTY > 250);
-- -> [('S1', 20, 'Paris'), ('S2', 10, 'Rome')]
SELECT * FROM S WHERE NOT EXISTS (SELECT 1 FROM SP WHERE SP.SN = S.SN);
-- -> [('S3', 40, 'Athens')]
```

注意两点：① 这两条与 Tutorial D 的 `S MATCHING (SP ...)` / `S NOT MATCHING BY {SNO} (SP)` **语义等价**；② 但 SQL 里的"匹配结果"不能直接当一个关系继续操作——想对结果再投影，就要把 EXISTS 整段重写进子查询里（或者套 CTE，代价是把谓词搬到 FROM 层）。

这就是"表达力"的准确含义：**不是能不能算出答案，而是答案能不能作为一等值继续参与代数。** 🔧 除法那一例（D5d/D5e）是同一个问题的极端版：

```sql
-- 正确：DISTINCT + 双重否定（Tutorial D: SP{SN,PN} ÷ P）
SELECT DISTINCT SN FROM SP AS x
WHERE NOT EXISTS (SELECT * FROM P AS p
                  WHERE p.PN NOT IN (SELECT PN FROM SP AS y WHERE y.SN = x.SN));
-- -> [('S4',)]
-- 忘记 DISTINCT 的同一查询 -> [('S4',), ('S4',), ('S4',)]
```

### 2. EXTEND：SQL 把算子降级成了"选择列表位置"（12.2）

模型里 `EXTEND S : { ANNOS := ... }` 的结果是一个**新关系**（度 +1），可以立即参与 σ/π/⋈/GROUP BY。SQL 的对应物只存在于 SELECT 列表，而 SELECT 在求值顺序的最后（11.8）⇒ 派生列不能用于 WHERE/GROUP BY/HAVING（除少数产品的扩展语法，如 PostgreSQL 允许 `GROUP BY` 别名、MySQL 允许 `HAVING` 引用别名 ⚠️ 转述）。后果就是真实项目里的两种脏写法：表达式写两遍，或者多套一层子查询。

🔧 顺带一个 SQLite 特有的坑：允许"裸列"（D10c）让某些人把派生值与分组混写，结果不定义：

```sql
SELECT SN, PN, COUNT(*) AS n FROM SP GROUP BY SN;
-- -> [('S1','P1',2), ('S2','P2',1), ('S4','P1',3)]   -- PN 取组内任意元组的值
```

### 3. 映像关系：本章真正的缺口（12.3）

第 5 章的映像（image）= 分组对应的**子关系**。SQL 里没有任何表达式求值出一个子关系；只有两处"隐式"用到它（聚合函数的输入、相关子查询的内部作用域），且**都不把它当值**。因此：

| 需要映像才能干净表达的需求 | SQL 的现实写法 | 症状 |
| --- | --- | --- |
| 组内极值对应的整行（top-1 per group） | 相关子查询 / 窗口函数 `ROW_NUMBER()` | 窗口函数是 2003 年才补上的"绕道"，且要把结果包成派生表再筛 |
| 组内自定义聚集（如"组内中位数"、"首末值差"） | `STRING_AGG` 后外部解析，或写聚合 UDF | 聚集不再是"关系→标量"的开放体系 |
| 二次聚集（先按 A 分组聚集，再按 B 聚集结果） | 两层子查询 | 语义正确但可读性/复用性差 |

🔧 本目录的空聚集实测（补充演示）：`SELECT MIN(QTY), COUNT(*) FROM SP WHERE 0;` → `[(None, 0)]`，`SUM` 同样返回 `None`。**没有子关系这个值，就没有"该函数在这个输入上无定义"这种可检查的错误**——SQL 只能给 NULL。这正是第 7 章类型公设（7.2/7.3）想解决的问题：聚集应当声明**初值/类型下限**（Tutorial D 的 `ITERATE MIN` 之类的写法 ⚠️ 依作者一贯口径转述）。

### 4. 聚集和归纳（12.4）

- 12.4.1「归纳」（SQL 侧的聚合语法）：`COUNT(*)` vs `COUNT(列)`（🔧 D8g：`[(3, 2, 1)]`，三者语义不同）、`SUM/AVG` 忽略 NULL、`MIN/MAX` 忽略 NULL、`GROUP BY` 与 `HAVING` 的作用层次（🔧 D9/D9b 用了聚合后比较基数）。
- 作者特别指出 `COUNT(*)` 不是"数行数"而是"数元组"——在没有 NULL、没有重复行的关系里两者相同，在 SQL 里不是。
- `DISTINCT` 在聚合里是"回到关系"的开关：`COUNT(DISTINCT CITY)`（🔧 D8g → 1）。

### 5.「通用的限制」（12.4.2，直译自 generalized restriction/constraint）

这一小节把第 5 章的"广义约束"落到 SQL：想表达"每个城市供应商数不超过 2"这类**跨元组**规则，SQL 里能用的只有：

1. `CHECK` —— 不允许子查询（🔧 第 6 章实测：`subqueries prohibited in CHECK constraints`）；
2. `HAVING` —— 只能在查询里，不能声明；
3. 触发器 —— 过程式（🔧 第 6 章 D7c）；
4. 断言 —— 语法不存在（🔧 第 6 章：`near "ASSERTION": syntax error`）。

于是"通用的限制"在 SQL 里的真实形态是：**把规则写成一条查询，然后在应用/调度里定期执行它**。这正是第 6 章批评的"程序系统回潮"，也是本章作为第 14 章清单的前奏。

⚠️ 现代产品的部分补洞（转述）：PostgreSQL 的可延后外键（🔧 本目录实测 SQLite 也有：非法值在 `COMMIT` 时才报错）、`EXCLUDE USING gist`（表达"区间不重叠"这类跨元组约束）、物化视图 + 唯一索引、生成列。这些是**约束家族**的扩充，但都不是"任意谓词 + 关系层次"的断言。

## 常见误区

| 误区 | 纠正 |
| --- | --- |
| 「有 EXISTS 就不需要 MATCHING」 | 语义够，**层次**不够：MATCHING 的结果是关系，可继续参与代数；EXISTS 是谓词 |
| 「SELECT 里加表达式列就能到处引用它」 | 求值顺序决定它最后才存在（11.8/12.2） |
| 「窗口函数 = 映像关系」 | 窗口函数每次仍是对行的计算，不产生"子关系"这个值；组内需要复杂统计时立刻显出差距 |
| 「空组的 MIN 返回 NULL 很合理」 | 数学上无定义；NULL 把类型问题伪装成缺失值问题（→ 第 13 章） |
| 「`COUNT(*)` 会慢，改 `COUNT(1)`」 | 两者语义相同（🔧 都是数元组），性能 Myth；真正的语义坑在 `COUNT(列)` 忽略 NULL |
| 「跨元组规则用 HAVING 就行」 | HAVING 属于查询，不属于数据库定义；规则不会被强制（12.4.2） |

## 与其他章 / 其他书的联系

- 算子的模型定义与映像概念：[05-关系运算符Ⅱ.md](05-关系运算符Ⅱ.md)；除法的代数位置：[04-关系运算符Ⅰ.md](04-关系运算符Ⅰ.md)。
- 约束层次的完整论证：[06-约束和断言.md](06-约束和断言.md)；SQL 约束的支持面：[13-SQL约束.md](13-SQL约束.md)。
- 类型/定义域问题（空聚集、初值）：[07-关系模型.md](07-关系模型.md)。
- SQL 侧的可操作版本（GROUP BY 陷阱、外连接误用、DISTINCT 处方）：[../SQL_and_Relational_Theory/09-重复行DISTINCT与集合语义.md](../SQL_and_Relational_Theory/09-重复行DISTINCT与集合语义.md)、[../SQL_and_Relational_Theory/13-全书常见误区与关系论清单.md](../SQL_and_Relational_Theory/13-全书常见误区与关系论清单.md)、语言对照 [../SQL_and_Relational_Theory/12-语言教程TutorialDees与SQL对照.md](../SQL_and_Relational_Theory/12-语言教程TutorialDees与SQL对照.md)。
- 聚集与索引/执行（top-1 per group 的成本）：[../mysql/15-连接查询.md](../mysql/15-连接查询.md)、[../数据库系统概念6/05-高级SQL.md](../数据库系统概念6/05-高级SQL.md)。
- NULL/3VL 的 deeper：[../SQL_and_Relational_Theory/06-NULL与三值逻辑3VL.md](../SQL_and_Relational_Theory/06-NULL与三值逻辑3VL.md)、[../SQL_and_Relational_Theory/07-缺失值的真实语义-42与2与Placeholder.md](../SQL_and_Relational_Theory/07-缺失值的真实语义-42与2与Placeholder.md)。

## 核心概念速览（中英对照）

- **匹配 / 非匹配的 SQL 替身** — `EXISTS` / `NOT EXISTS`：语义等价、层次不同（谓词 vs 算子）
- **相关子查询** — correlated subquery：SQL 里最接近"按组重算子关系"的手段
- **EXTEND 的降级** — select-list only：派生列在求值顺序末尾，不能上移复用
- **映像关系** — image relation：分组对应的子关系；SQL 中无对应值
- **窗口函数** — OLAP window function：SQL 对"组内计算"的补丁（SQL:2003），仍不产生关系值
- **聚合** — aggregate（SQL 侧称呼）：`COUNT/SUM/AVG/MIN/MAX`，忽略 NULL
- **`COUNT(*)` vs `COUNT(列)`** — 数元组 vs 数非空值：语义不同 🔧 D8g
- **空组定义域** — aggregation over empty input：`MIN/SUM` 返回 NULL 即"无定义"的伪装 🔧
- **通用限制 / 广义约束** — generalized constraint：用聚集 + 关系比较表达的规则，SQL 无法声明
- **`HAVING`** — 查询级过滤：能算出违规，不能阻止违规
- **可延后约束** — deferrable constraint：SQL 里唯一"事务边界求值"的正式机制（🔧 实测 SQLite 有效）

## 最新演进与工业实践

- **SQL:2003 窗口函数 + SQL:1999 聚合改进**（⚠️ 转述）：工业界用窗口函数、`FILTER (WHERE ...)`、`WITHIN GROUP`（有序聚集，如 `percentile_cont`）、`GROUPING SETS/CUBE/ROLLUP` 部分回应了本章缺口——它们让"组内计算"能写，但仍**不把子关系当值**。SQLite 侧 `FILTER` 已可用（🔧 实测：`COUNT(*) FILTER (WHERE STATUS > 15)` 与旧式 `SUM(CASE WHEN ...)` 结果一致 → `[('Athens',1),('Paris',2),('Rome',0)]`）。
- **半联接/反半联接已被产品语法化**（🔧/文档）：DuckDB 有 `SEMI JOIN` / `ANTI JOIN` 一等语法（https://duckdb.org/docs/sql/query_syntax/select ✅）——这等于承认 12.1 的批评方向；PostgreSQL/MySQL 仍以 `NOT EXISTS`/`NOT IN` + 优化器改写实现（⚠️ 未在本目录测执行计划）。
- **"SQL 里写不了断言"的当代外移**：数据契约与断言型测试（dbt tests 的 `unique`/`not_null`/自定义 SQL 测试、Great Expectation/Soda 类期望，⚠️ 工具名仅作生态说明）承担了 12.4.2 的"通用限制"。区别在于**检查发生在写入之后**，与本书"由 DBMS 在状态转移时强制"仍然不同——这条差异正是第 14 章要总结的。
- **顶层实践提示**：需要"组内极值整行 / top-K"时，优先显式窗口函数 + CTE，并把"映像"的语义在注释里写清（哪个属性集定义组、聚集作用在哪个子关系上）；不要依赖裸列扩展（🔧 D10c）。⚠️ 性能未在本目录实测。
- **深浅分工**：本章只做"缺什么"的盘点；**在 SQL 里怎么把这些问题写对**（外连接误用、聚合陷阱的处方）在 [../SQL_and_Relational_Theory/00-总览与阅读地图.md](../SQL_and_Relational_Theory/00-总览与阅读地图.md) 的 06/07/09 章；**约束的可实现子集**在 [13-SQL约束.md](13-SQL约束.md)。
