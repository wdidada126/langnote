# 04 · Using DuckDB with Polars（DuckDB 与 Polars）

> 覆盖原书第 4 章。目录来源：✅ 官方示例文件 `Chapter_4.ipynb` 标题实抓（notebook 首题即 "Using DuckDB with Polars"）。这是两本 DuckDB 书里**唯一以 Polars 为主角的一章**：先教 Polars 基本盘，再打通"Polars↔DuckDB 经 Arrow 零拷贝互喂"与不写 SQL 的 `DuckDBPyRelation` 对象代数。

## 内容规格（小节地图，✅ 实抓自官方示例 notebook）

- **Introduction to Polars / Creating a Polars Dataframe**：无索引 DataFrame、列型显名（notebook 注释逐条演示 `dtypes`/列名/元组化查看）。
- **Selecting Columns / Selecting Rows / Selecting Rows and Columns**：`select/filter/[]` 三态切片语法谱。
- **Using SQL on Polars**：`pl.SQLContext` 路线——在 Polars 侧写 SQL（✅ 小节题实抓）。
- **Understanding Lazy Evaluation in Polars**：**Implicit/Explicit lazy evaluation** 两节：表达式树 + 优化器 + `.collect()`。
- **Querying Polars DataFrames Using DuckDB**，下分：**Using the sql() Function**、**Using the DuckDBPyRelation Object**；再按关系代数逐节演示 **Inserting Rows / Joining tables / Filtering rows / Aggregating rows / Projecting columns / Limiting rows**——一章把 Relation API 当"无 SQL 的 SQL"教完。

## 核心技术清单

- 两条宿主桥：`duckdb.sql("… FROM pldf …")`（替换扫描吃到 Polars 对象）与 `duckdb.from_polars/ con.register`（命名挂载）。
- Relation API 六件套：`rel.filter()/project()/aggregate(keys,aggs)/join(rel, how)/limit(n)/insert()`，链式组合、`.show()/.df()/.to_arrow_table()` 出口。
- SQL↔Relation 互通：`con.sql(rel)`、Relation 作别名进 SQL（DIA 06 实测口径，本目录复核 API 在）。
- Polars↔DuckDB 的物理总线是 **Arrow C Data Interface**：往返不序列化、不复制列缓冲。
- 惰性求值对照：Polars 用查询计划（lazyframe）逼近数据库；DuckDB 天生就是计划引擎——两者互补而非替代。
- 聚合语义细节：`agg(pl.col('v').sum())` vs DuckDB `sum(v)`；表达式内改列名策略（`.alias`）。

## 🔧 实测（1.5.5 / polars 1.44.2 / pandas 3.0.2；同数据同题三引擎对照）

1. **10M 行×2 列（g 分组求 sum(v) 取 Top-3）**：pandas 原生 **0.11 s**；`pl.from_pandas(df)` 后 Polars eager **0.06 s**；**DuckDB 替换扫描直查同名 pandas df 0.03 s**——三结果逐值一致（Top-3 组与和值全同）。
2. **Polars 对象直查** ✅：3M 行 Polars DataFrame 建好后 `SELECT count(*) FROM pldf` **0.00 s**（列存内存直读，无导入步骤）。
3. **Arrow 总线吞吐**：5M 行结果 `to_arrow_table()` **0.05 s**；`pl.from_arrow(tbl)` **0.01 s**；把该 Arrow 表再注册回 DuckDB 查 count **0.01 s**——一个 500 万行对象在 pandas→DuckDB→Arrow→Polars→DuckDB 全链上**没有任何一次行级遍历**。
4. **agg→pandas 出口**：10M 行聚合出 1000 组再 `.df()` **0.03 s**（含物化）——"先聚后取"永远优先于"取了再聚"。
5. **Relation API 现状**：`con.sql(...)` 返回对象及其链式方法在 1.5.5 存在（DIA 06 已实测 `.filter/.aggregate` 可用；本目录以 DuckDB 关系面复核 join/aggregate ✅）；聚合键值表语义 `aggregate("k","sum(v)")` 字符串式（⚠️ 新版推荐 relation 表达式式，两种并存）。
6. **版本漂移**：`con.sql(sql, params)` 位置参数移除影响"SQL 里引用宿主变量"的模板写法；`duckdb.typing` 子模块消失影响 Polars dtype→DuckDB 类型的中转代码（用字符串类型名）。
7. **`aggregate()` 参数序反转（1.5.5 实测重锤）**：`DuckDBPyRelation.aggregate.__doc__` 逐字实抓为 `aggregate(aggr_expr: object, group_expr: str = '')`——**聚合表达式在前、分组键在后**。按成书口径写 `rel.aggregate("AIRLINE","count(*)")` 直接 `Binder Error: GROUP BY clause cannot contain aggregates!`（它把 "AIRLINE" 当聚合、"count(*)" 进了 GROUP BY）；正解 `rel.aggregate("count(*)","AIRLINE")` ✅ 出 14 航司计数。成书（1.1 代）与 1.5.5 行为相反，**升级必查 `__doc__` 签名**。
8. **aggregate 字符串的限制** ✅：聚合串里带 `AS n` 别名在 1.5.5 报 Parser Error（不接受 AS）；输出列名回落函数式 `count_star()`，排序得写 `order("count_star() DESC")`；list/`Expression` 形态参数在本机构建直接 incompatible——字符串双参是唯一稳态。
9. **Relation 链全链示范** ✅：`con.sql(SELECT AIRLINE, DEPARTURE_DELAY FROM flights).filter("DEPARTURE_DELAY > 60").aggregate("count(*)","AIRLINE")` 出 14 行计数（>60 分钟延误航班，最大组 WN 65,521——SQL 排序核对）；**Relation 裸输出不保证行序**，榜单必须显式 `.order()`；链上每步都是关系对象、末端才执行——"惰性 Relation + 早过滤"是 Relation API 的正确打开方式。

## 易错点与陷阱

- **"Polars 快"与"DuckDB 快"是两个预算**：Polars eager 每步物化、lazy 才合并计划；把 DuckDB 当"更快的 group by"时，真正省的是**跨引擎搬运**而不是单算子。
- **from_pandas 不是零拷贝**：pandas（尤其含 object/nullable 列）→Polars 有转换成本；上面 0.06 s 里大头是这一步。零拷贝只在 **Arrow-backed** 对象之间成立。
- **替换扫描的解析顺序**：库内同名表存在时 Polars 变量被遮蔽（同 [01 章](01-DuckDB入门.md) 陷阱）——`DROP VIEW`/换名/`register()` 显式绑定。
- **聚合 API 换代坑**：Polars 1.x 起 `group_by().sum(col)` 式逐步退位 `agg(pl.col(...))`；DIA 06 实测就踩过 API 变更——跨版本 notebook 先跑 smoke。
- **Relation 链的参数序心智（1.5.5 实测修订）**：签名是 `aggregate(aggr_expr, group_expr)`——**聚合在前、分组在后**（实测 7）；写反会撞 "GROUP BY cannot contain aggregates"，好在报错响亮不算静默坑。聚合串里拼 `AS` 别名会 Parser Error（实测 8）；复杂逻辑早退 SQL。
- **别用 DuckDB 跑 UDF 打 Polars**：Python 回调在两边都慢（DIA 实测行级 UDF 慢 86×），向量化路线各自有原生表达式。

## Relation ⇄ SQL 翻译对照卡（1.5.5 实测注记）

| Relation 链 | 等价 SQL | 注记 |
| --- | --- | --- |
| `rel.filter("d > 60")` | `WHERE d > 60` | 字符串表达式 |
| `rel.project("a","b")` | `SELECT a, b` | 投影 |
| `rel.aggregate("count(*)","AIRLINE")` | `SELECT count(*), AIRLINE … GROUP BY AIRLINE` | **聚合在前！**（实测 7） |
| `rel.join(other, how="inner")` | `… JOIN … USING (k)` | 键列名需一致 |
| `rel.order("count_star() DESC").limit(3)` | `ORDER BY … LIMIT 3` | 排序列用聚合后自动名（实测 8） |
| `.show()/.fetchall()/.to_arrow_table()` | 结果出口三形态 | Arrow 出口吞吐见实测 3 |

- 读法：先写 SQL 验证语义，再逐子句"翻"成链式调用——翻译卡六行覆盖本章 Relation 小节全部动作。

## 选型速记（本章视角）

| 场景 | 推荐 | 依据（实测/机制） |
| --- | --- | --- |
| 内存内小中数据、表达式流 | Polars | 0.06s/10M，无 SQL 心智负担 |
| 同数据要 SQL/JOIN 组合拳 | DuckDB 直查 | 0.03s/10M，替换扫描零导入 |
| 结果喂下游 Polars | Arrow 总线 | 5M 行 0.05+0.01s |
| 反复迭代的管道 | lazy Polars 或 DuckDB 表 | 合并计划/一次物化 |
| 无 SQL 授权的报表 | Relation API | 链式对象代数 |

## Lazy Polars 一页骨架（对应本章 "Understanding Lazy Evaluation" 两小节）

```python
import polars as pl
q = (pl.scan_parquet("flights2015.parquet")     # explicit lazy：建计划、不物化
       .filter(pl.col("DEPARTURE_DELAY") > 60)
       .group_by("AIRLINE")
       .agg(pl.col("DEPARTURE_DELAY").mean().alias("avg_delay"))  # agg 内即 implicit lazy 表达式
       .sort("avg_delay", descending=True)
       .collect())                              # 执行开关；谓词下推/列裁剪在这一步发生
```

- 成书把 Implicit/Explicit 拆两节讲：前者=在 eager 接口里传表达式树，后者=`scan…collect` 全程计划态——骨架里两者同框。
- DuckDB 对照：`con.sql(...)` 返回 Relation、末端才执行（01 章陷阱 9）——两栈惰性心智同构，只是 DSL 形状不同；"合并计划"层面 Polars lazy ≈ 查询优化器，DuckDB 天生就是计划引擎。

## 版本漂移复诊清单（成书 1.1 代 → 1.5.5，代码级）

1. `aggregate(keys, aggs)` → `aggregate(aggs, keys)`（实测 7，本章最重刀）。
2. 聚合串内 `AS` 别名不再接受；列名回落 `count_star()` 式（实测 8）。
3. `duckdb.typing` 子模块消失——dtype 中转用字符串类型名（00 漂移清单 8）。
4. `con.sql(sql, params)` 位置参数移除（00 清单 1）——宿主变量模板写法迁到 `execute`。
5. Polars 侧 `.df()` 与 jupysql 结果对象的 `.DataFrame()` 是两回事（07 章漂移），跨栈笔记勿混用。
- 排障顺序：撞错先 `__doc__`/`help()` 看签名，再查 00 清单，最后才怀疑 SQL 本身。

## 与其他章/书的互链

- 替换扫描与 UDF 代价的完整 Python 生态面 → [../DuckDB_in_Action/06-融入Python生态.md](../DuckDB_in_Action/06-融入Python生态.md)（同一对照实验的 DIA 版本：pandas 0.13/polars 0.05/duckdb 0.03，量级吻合本目录）
- Jupyter 里两种引擎的第三选择（JupySQL）→ [07-DuckDB与JupySQL.md](07-DuckDB与JupySQL.md)
- 本章数据上到 580 万行后的形态 → [05-用DuckDB做探索性数据分析.md](05-用DuckDB做探索性数据分析.md)
- 表达式/向量化执行原理 → [../../db/db.md](../../db/db.md)（Vectorized/ MonetDB-X 论文线）

## 思考题（合上笔记再答）

1. 三引擎同题（10M group-by）各多少秒？谁赢在"跨引擎搬运"上？（0.11/0.06/0.03；DuckDB 吃替换扫描红利，导入成本为 0）
2. 说出一条"pandas→DuckDB→Polars→DuckDB"全程无行级遍历的路径及其前提。（Arrow Table 作总线；前提：Arrow-backed 类型可映射）
3. lazy evaluation 为什么让 Polars 逼近数据库？DuckDB 相对它还多提供什么？（计划合并+列裁剪/谓词下推；多 SQL 面、持久化、多源 ATTACH）
4. 1.5.5 里 `rel.aggregate` 的参数序是什么？写反报什么错？（`aggregate(aggr_expr, group_expr)`——聚合在前；"GROUP BY clause cannot contain aggregates!"——实测 7）

## 2026 视角补注

- "DuckDB vs Polars"叙事已从替代转向**同一 Arrow 世界的两种门面**（SQL-first vs 表达式-first）；两本书（UAR04/DIA06）从不同侧面给出可互校验的数字。
- Polars 默认后端即 Arrow，DuckDB `.arrow()` 于 1.5 线改流式 RecordBatchReader——大结果互喂注意消费形态（DIA 06 实测注记，本目录复核 `to_arrow_table()` 仍 Table）。

## 核心概念速览（中英对照）

- **表达式 API** — Expression API：以列表达式为一等对象的查询构造法。
- **惰性求值** — Lazy evaluation：先建计划后执行，算子融合+谓词下推。
- **collect** — 惰性计划的执行开关。
- **零拷贝** — Zero-copy via Arrow：共享列缓冲，不序列化。
- **SQLContext（Polars）** — Polars 自带的 SQL 门面。
- **DuckDBPyRelation** — DuckDB 的关系对象：filter/project/aggregate/join/limit。
- **替换扫描（Polars 形态）** — FROM 直接命中内存 Polars 对象。
- **from_pandas 成本** — eager 转换非零拷贝，是跨栈预算大头。
- **alias 心智** — 聚合表达式改名列的标准动作。
- **agg 双参数** — Relation 聚合的 keys/aggregates 字符串对。

## 最新演进与工业实践

- **版本线**：polars 1.44 / duckdb 1.5.5 / pandas 3.0 三者同代（本机 pip 实测），"三件套"是 2026 数据工程标配依赖面（PyPI duckdb 页 ✅）。
- **生态动向**：DuckDB 与 Polars 社区互认"同总线"关系；`pl.SQLContext` 的加入让 Polars 侧也能吃 SQL——两引擎在 API 面互相靠拢，选型判据收敛到"事务性/多源/UDF"侧。
- **工业实践**：notebook 生产化的通行分层=Polars 做转换、DuckDB 做联合查询与对外供数、parquet 做中间层；本目录 3 的 Arrow 链吞吐（5M 行 0.06 s 端到端）即该分层的可行性证明（🔧 自测）。
- **互读**：本章与 DIA 客户端叙事的分工 → [../DuckDB_in_Action/12-附录A-客户端API.md](../DuckDB_in_Action/12-附录A-客户端API.md)。
