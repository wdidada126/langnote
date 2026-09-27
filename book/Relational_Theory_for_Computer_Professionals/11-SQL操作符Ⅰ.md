# 第 11 章　SQL 操作符Ⅰ（SQL Operators I ⚠️ 回译）

> 译本 p141–155｜小节（✅ 实抓）：11.1 限制 / 11.2 投影 / 11.3 并、交、差 / 11.4 更名 / 11.5–11.6 练习Ⅰ与答案Ⅰ / 11.7 联接（11.7.1 另一种格式、11.7.2 规范特性、11.7.3 笛卡儿乘积）/ 11.8 基本表表达式的求值 / 11.9 表的比较 / 11.10 显示结果 / 11.11–11.12 练习Ⅱ与答案Ⅱ。
> 本章逐条把第 4 章的算子映射到 SQL 语法，并给出一条统摄性判据：**这个 SQL 构造求值的是一张表还是一个关系？**

## 本章地图

| 小节 | Tutorial D | SQL | 偏离要点 |
| --- | --- | --- | --- |
| 11.1 限制 | `S WHERE CITY = 'Paris'` | `SELECT * FROM S WHERE CITY = 'Paris'` | WHERE 丢弃 UNKNOWN 行（🔧）；`SELECT *` 又引入列序 |
| 11.2 投影 | `S { SNO, CITY }` | `SELECT DISTINCT SNO, CITY FROM S` | 必须写 DISTINCT；投影**不是**"选列列表" |
| 11.3 并/交/差 | `UNION` / `INTERSECT` / `MINUS`（同头要求） | `UNION`/`INTERSECT`/`EXCEPT`（+ `ALL` 变体） | 按**位置**对齐、默认去重、`ALL` 回到袋 |
| 11.4 更名 | `RENAME CITY AS C` | `AS`（列别名/表别名） | 别名只在当层可见，不能据此凑"同头" |
| 11.7 联接 | `⋈`（自然）、`*_`（θ）、`×`（乘积） | `NATURAL JOIN` / `JOIN ... ON` / `JOIN ... USING` / `CROSS JOIN` / 老式逗号 + WHERE | 外联接把关系变成"带 NULL 填充的表" |
| 11.8 求值 | 表达式自内向外求值，结果恒为关系 | `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY` | 语法顺序 ≠ 逻辑顺序，别名可见性由此而来 |
| 11.9 表的比较 | `r1 = r2` 直接可写 | 没有（只能双向 EXCEPT 绕） | 🔧 D10e |
| 11.10 显示结果 | 展示不是查询的一部分 | `ORDER BY` 属于查询语法，结果仍是表 | 🔧 D10/D10b |

## 核心精讲

### 1. 限制（σ）与 WHERE 的三值后果

`WHERE` 的语义不是"返回谓词为真的行"，而是"**返回谓词为 TRUE 的行**；FALSE 与 UNKNOWN 一起丢掉"。🔧 实测（D8b，SQLite 3.45.3）：

```sql
SELECT 1 WHERE NULL = 3;           -- -> []
SELECT 1 WHERE NOT (NULL = 3);     -- -> []
```

于是"正问"和"反问"都不返回同一行，互补谓词不再划分关系（D8c：`WHERE ST = 20` 2 行、`WHERE NOT (ST = 20)` 1 行，而总行数 4）。作者的处方（→ 第 14 章清单）：**要么列 NOT NULL，要么在取反处显式 `OR col IS NULL`**。

🔧 正确补集的写法（D8e）：

```sql
SELECT COUNT(*) FROM T8 WHERE ST = 20;                    -- -> [(2,)]
SELECT COUNT(*) FROM T8 WHERE ST <> 20 OR ST IS NULL;     -- -> [(2,)]  这才是补集（2+2=4）
SELECT COUNT(*) FROM T8 WHERE NOT (ST = 20);              -- -> [(1,)]  这个"NOT"不是补集
```

⚠️ 但要注意本章的层次：**在关系模型里根本不该有这个讨论**——模型的谓词是二值的（真/假），"缺失值"是第 6 章讨论过的、作者主张用 Placeholder（域内的特定值）而不是 NULL 来表达的问题（对照 [../SQL_and_Relational_Theory/07-缺失值的真实语义-42与2与Placeholder.md](../SQL_and_Relational_Theory/07-缺失值的真实语义-42与2与Placeholder.md)）。

### 2. 投影（π）：一个必须写 DISTINCT 的操作

模型的 `π_{SNO}(SP)` 返回**关系**（重复自动消失）；SQL 的 `SELECT SNO FROM SP` 返回**袋**（🔧 D4 的第二段：数据恰好没有产生重复时看不出差别，因此它是潜伏 bug）。作者的立场：投影的"去掉属性"必然引起"合并元组"，SQL 把合并后的重复留给你自己处理，等于把语义责任推给使用者。

另一处偏离：**投影是"去掉属性"，不是"选择表达式"**。`SELECT SNO, STATUS*2 FROM S` 其实是 投影 ∘ 扩展（EXTEND），SQL 把两件事挤在一个位置里 ⇒ 于是派生列在 WHERE 里不可用（第 5 章 EXTEND 的对照）。

### 3. 并/交/差：名字不参与、顺序参与

🔧 实测（D2 + 列名核验）：

```sql
WITH A(x, y) AS (VALUES (1, 2)), B(y, x) AS (VALUES (3, 4))
SELECT * FROM A UNION ALL SELECT * FROM B;
-- 值 -> [(1, 2), (3, 4)]；结果列名 -> ['x', 'y']
SELECT 1 AS one, 2 UNION SELECT 3, 4;   -- 列名 -> ['one', '2']（第一支决定名字）
```

三条结论：① 复合查询按**位置**对齐；② 结果列名取自**第一支**；③ `UNION` 默认去重（回到关系语义），`UNION ALL` 是袋（`EXCEPT ALL` 在 🔧 的 SQLite 3.45.3 里甚至不被支持）。

模型观点下，"并"要求两操作数**同头**（属性名+类型一致，头是无序集合）。SQL 放宽成"同度数 + 对应位置类型可兼容"——这是最容易把错数据并到一起的地方。作者的实用建议 ⚠️ 重构：写复合查询时显式列出列名并保证同名同序，或干脆用 CTE 把两侧写成"具名视图"再并。

### 4. 更名（ρ）与 `AS`：作用域不同

Tutorial D 的 `RENAME` 产生**新的关系值**（头真的变了），可以拿去满足并/自然联接的同头条件。SQL 的 `AS` 只给列/表起一个当层可见的标签，**不改变"头的相等性判断"**（因为 SQL 压根按位置判断）。所以：

```sql
-- ⚠️ 示意：想让两侧"同头"，SQL 里只能靠列名+列序都写对
WITH s AS (SELECT SNO, CITY FROM S), p AS (SELECT PNO, CITY FROM P)
SELECT * FROM s UNION SELECT * FROM p;    -- 位置对齐即可，名字并不强制
```

### 5. 联接（11.7）：三种格式与一个"规范特性"

- 11.7.1「另一种格式」= 老式 `FROM S, SP WHERE S.SNO = SP.SNO`（逗号 = 乘积 + 限定）。作者的批评一贯：连接条件与筛选条件混写在一起，**漏写条件就退化成乘积**（🔧 D4b：本例 `S CROSS JOIN SP` = 9 = 3×3），而显式 `JOIN ... ON` 至少让漏写在语法上可见。
- 11.7.2「规范特性」= `USING` / `NATURAL` 与"同名同型公共属性"的关系：自然联接在模型里定义干净（相等 + 去重列），在 SQL 里遇 NULL 就不干净——`NULL = NULL` 是 UNKNOWN ⇒ 两个 NULL 的外码值**不会匹配**（→ 🔧 D8h：LEFT JOIN 的 NULL 与真实 NULL 无法区分）。
- 11.7.3「笛卡儿乘积」：`CROSS JOIN` 是 SQL 里唯一保持闭包且与模型完全一致的联接形式（袋语义下基数仍是乘积）。

### 6. 求值顺序（11.8）：语法顺序 ≠ 逻辑顺序

逻辑顺序（⚠️ 通行教材口径）：

```
FROM / JOIN → WHERE → GROUP BY → HAVING → SELECT(表达式/别名) → ORDER BY → LIMIT
```

由此解释三件日常现象：

1. `WHERE` 里不能用 `SELECT` 定义的别名（还没求值）；
2. `GROUP BY` 里能否用别名，各家不同（MySQL 允许、PostgreSQL 标准口径不允许）⚠️ 转述；
3. SQLite 的"裸列"扩展直接把这条顺序变成"任取一行"（🔧 D10c）。

### 7. 表的比较（11.9）与显示结果（11.10）

- 比较：模型里 `r1 = r2` 是扩展相等（第 4 章 4.11）；SQL 没有这个运算符，只能"双向 EXCEPT 皆空"（🔧 D10e → `[(1,)]`）。含 NULL 时更麻烦：`EXCEPT` 把 NULL 视为可比较（NULL 之间算相等），于是 SQL 的"相等"在不同构造里行为不一致（第 14 章清单收这条）。
- 显示：`ORDER BY` 出现在查询语法里，但**它不属于查询的语义**（查询返回关系，展示才需要顺序）。🔧 支持证据：D10（无 ORDER BY 时顺序是实现细节）、D10b（`LIMIT` 无 ORDER BY ⇒ 非确定结果）。作者的规则 ⚠️ 重构：把 ORDER BY 当作"客户端渲染指令"，除"分页/TOP-N 语义"外不要在查询里依赖它。

## 常见误区

| 误区 | 纠正 |
| --- | --- |
| 「SELECT 列表就是投影」 | 它是 投影 + 扩展 + 表达式求值的混合位置；真投影必须配 DISTINCT |
| 「NOT (p) 就是补集」 | 3VL 下不是（🔧 D8c/D8e）；要么 NOT NULL 约束，要么显式 IS NULL |
| 「UNION 会帮我对齐列名」 | 它按位置对齐、按第一支命名（🔧）；名字不同也能"成功" |
| 「NATURAL JOIN 最贴近模型，随便用」 | NULL 参与时行为不干净；且公共属性集合一变，联接条件跟着变 |
| 「逗号连接和 JOIN ON 只是风格差异」 | 漏写条件的失效模式不同：逗号版静默变乘积，ON 版语法上更难漏 |
| 「ORDER BY 结果顺序稳定，下游按位置取列没事」 | 顺序与列序都是实现细节（🔧 D10/D10f），按名字取列是最低要求 |

## 与其他章 / 其他书的联系

- 算子的模型定义：[04-关系运算符Ⅰ.md](04-关系运算符Ⅰ.md)；半联接/EXTEND/SUMMARIZE 的缺位：[12-SQL运算符Ⅱ.md](12-SQL运算符Ⅱ.md)。
- 3VL 的真值表与"取反"：[../SQL_and_Relational_Theory/06-NULL与三值逻辑3VL.md](../SQL_and_Relational_Theory/06-NULL与三值逻辑3VL.md)、AND/OR/NOT 的唯一操作符论证 [../SQL_and_Relational_Theory/05-AND-OR-NOT唯一的逻辑操作符.md](../SQL_and_Relational_Theory/05-AND-OR-NOT唯一的逻辑操作符.md)。
- 投影/DISTINCT/袋语义的可操作版：[../SQL_and_Relational_Theory/09-重复行DISTINCT与集合语义.md](../SQL_and_Relational_Theory/09-重复行DISTINCT与集合语义.md)、[../SQL_and_Relational_Theory/02-关系代数与封闭性.md](../SQL_and_Relational_Theory/02-关系代数与封闭性.md)。
- 求值顺序的工程后果（优化器怎么改顺序）：[../mysql/14-基于规则的优化.md](../mysql/14-基于规则的优化.md)、[../mysql/15-连接查询.md](../mysql/15-连接查询.md)、[../数据库系统概念6/05-高级SQL.md](../数据库系统概念6/05-高级SQL.md)。
- 偏离的总结与"SQL 到底关系不关系"：[14-SQL与关系模型.md](14-SQL与关系模型.md)。

## 核心概念速览（中英对照）

- **限制 / WHERE** — restriction：谓词为 TRUE 才保留；UNKNOWN 与 FALSE 一并丢弃 🔧
- **投影 / SELECT DISTINCT** — projection：去属性必然合并元组；SQL 要手写 DISTINCT
- **复合查询** — compound query（UNION / INTERSECT / EXCEPT）：按位置对齐、默认去重、`ALL` 回到袋
- **同头 / 并兼容** — union compatibility：模型要求名字与类型对应；SQL 只要求度数与位置
- **更名 / AS** — rename：模型的 RENAME 产出新头；SQL 的别名只有作用域没有语义
- **θ-联接 / 自然联接** — theta join / natural join：`ON` 显式条件 vs `NATURAL`/`USING` 按同名属性
- **外联接** — outer join：用 NULL 填充未匹配行，破坏"结果仍是关系"的干净性 🔧 D8h
- **求值顺序** — logical order of evaluation：FROM→WHERE→GROUP BY→HAVING→SELECT→ORDER BY
- **表的比较** — table comparison：SQL 无关系相等运算符，需双向 EXCEPT 🔧 D10e
- **显示层** — presentation：ORDER BY/LIMIT 属于展示，不属于查询语义
- **裸列扩展** — bare-column extension：SQLite 允许的非分组列，取值不定义 🔧 D10c
- **`IS` / `IS NOT DISTINCT FROM`** — null-safe equality：把 UNKNOWN 折成真的相等判定

## 最新演进与工业实践

- **本章的"求值顺序"知识在 2024–2026 年仍是最有用的 SQL 心智模型**：各家文档都以逻辑顺序解释别名可见性与 `GROUP BY` 限制。PostgreSQL 与 SQLite 都提供 `IS NOT DISTINCT FROM`（SQLite 写作 `IS`，🔧 已实测）与 `FILTER (WHERE ...)` 聚合（🔧 已实测可用）。DuckDB 语法文档：https://duckdb.org/docs/sql/query_syntax/select ✅
- **复合查询的袋语义在分析引擎里更贵**：`UNION ALL` + 向量化执行是常规写法（保留重复以省一次去重），而"要正确就要 DISTINCT"的代价在列式引擎上更高 ⚠️ 转述，本目录未做性能测量。
- **`NATURAL JOIN` 的现实地位**：主流风格指南仍建议避免（隐式条件 + 模式漂移风险），`USING` 被视为可接受的中间态 ⚠️ 转述；这与本章"模型定义干净但 SQL 实现不干净"的判断一致。
- **查询等价性测试**：把本章的判据变成 CI 断言（🔧 自拟示意，非书中原文）：

```sql
-- 🔧 断言"正问 + 反问 = 全集"，失败即说明该列存在 NULL 且谓词用了 NOT
SELECT (SELECT COUNT(*) FROM T) =
       (SELECT COUNT(*) FROM T WHERE  P ) +
       (SELECT COUNT(*) FROM T WHERE NOT P ) AS excluded_middle_ok;
```

- **深浅分工**：那本 SQL 书（[../SQL_and_Relational_Theory/00-总览与阅读地图.md](../SQL_and_Relational_Theory/00-总览与阅读地图.md)）给的是"同样这些偏离，SQL 该怎么写对"；本直给"偏离为什么必然存在"。性能取向的写法（联接顺序、谓词下推）见 [../mysql/15-连接查询.md](../mysql/15-连接查询.md) 与 [#45](../Efficient_MySQL_Performance/00-总览与阅读地图.md)/[#23](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md)（均已落盘，波尾闭环）。
