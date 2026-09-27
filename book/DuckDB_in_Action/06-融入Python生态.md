# 06 · Integrating with the Python ecosystem（融入 Python 生态）

> 覆盖原书第 6 章。目录来源：✅ Manning 官方 TOC 实抓。本章讲 DuckDB 作为"Python 进程里的第二台引擎"：pip 安装、连接对象、关系 API、直接查 DataFrame、UDF、Arrow/Polars 零拷贝互操作。

## 内容规格（小节地图，✅ 实抓）

- **6.1 Getting started**：6.1.1 `pip install duckdb`（wheel 全平台）；6.1.2 `duckdb.connect()` 三种形态：内存 `:memory:`、文件 `path.db`、`read_only=True`；连接即线程安全对象、每连接一个事务上下文。
- **6.2 Using the relational API**：不写 SQL 的链式对象代数——`duckdb.read_csv('x.csv') .filter() .aggregate() .project() .order()`；6.2.1 摄取 CSV；6.2.2 组合查询（Relation 可 `.to_sql()`/互相 JOIN）；6.2.3 SQL 与 Relation 混用（`con.sql(rel)`、`rel.query("SQL", alias=rel)`）。
- **6.3 Querying pandas DataFrames**：替换扫描（replacement scan）让 `SELECT * FROM my_df` 直接命中内存里的 DataFrame；`register/unregister` 显式命名；`.df()` 取回 DataFrame。
- **6.4 User-defined functions**：`con.create_function(name, fn, [args], ret[, type=numpy/arrow])` 注册标量 UDF；向量化 UDF（`null_between` 等选项）；UDF 走 Python 回调、**破坏流水线优化**。
- **6.5 Interoperability with Apache Arrow and Polars**：`con.from_arrow_table`/`duckdb.filter`、`fetch_arrow_table()`、Relation/Polars 与 Arrow stream 互喂；Arrow 是"进程间零拷贝总线"。

## 核心技术清单

- API 层次：DBAPI2（execute/fetch*）+ cursor + `sql()`/`relation()`/`from_df`/`to_df` 双轨。
- 结果出口：`fetchall/fetchnumpy/fetchdf/df()/arrow()/to_arrow_table()`。
- 参数化：`execute("... WHERE x=?", [v])`——防注入 + 计划复用。
- `appender`：批量行写入 API，比 executemany INSERT 快一个量级。
- 替换扫描的查找顺序：注册对象 → Python 变量名（DataFrame/Arrow/数组）。
- 与 Polars：经 Arrow 互转零拷贝，`pl.from_arrow(duck_result)` 常见。
- 多线程：一连接多 cursor 并行查询；`con.cursor()` 隔离事务。

## 🔧 实测（pandas 3.0.2 / polars 1.44.2 / pyarrow / 1.5.5；10M 行 groupby 同数据对照）

| 方案（`g` 分组求 `sum(v)` 取 Top-3） | 耗时 |
| --- | --- |
| pandas 原生 `df.groupby('g')['v'].sum()` | **0.13 s** |
| polars `pl.from_pandas(df).group_by('g').agg(...)` | **0.05 s** |
| **DuckDB 直查同名 DataFrame**（零注册、替换扫描） | **0.03 s** |

1. 替换扫描 ✅：`con.sql("SELECT ... FROM df ...")` 直接吃 `df` 变量；Top-3 结果与 pandas 一致。
2. Arrow 出口行为变化（1.5.5）：`con.sql(...).arrow()` 返回 **RecordBatchReader**（流式，不再是 Table）；要 Table 用 `to_arrow_table()`——`fetch_arrow_table()` 已 **DeprecationWarning** ⚠️→✅ 实测两版差异。
3. Python 标量 UDF 的代价：`classify(v)`（if/else）注册后对 10M 行执行 **2.57 s**——是同一查询纯 SQL 版（0.03 s）的 **~86 倍**；UDF 能把"表达不了的逻辑"塞进计划，但每行一次 GIL 回调。
4. `create_function` 签名坑（1.5.5 实测）：类型用**字符串** `"DOUBLE"` 可用；`duckdb.typing.DOUBLE` 直接 `AttributeError`（该子模块在 1.5 移除）——成书代码到新版要改。
5. `register()`/`unregister()` ✅；`con.execute("... WHERE g=?", [7])` 参数化 ✅。

## 易错点与陷阱

- **替换扫描只认"还没被当变量解析前"的名字冲突**：库里已有同名表时 SQL 优先命中表，DataFrame 被遮蔽——先 `DROP VIEW`/换名。
- **pandas→DuckDB 的类型往返**：pandas 3.0 的 string dtype/Arrow backed 列与 DuckDB VARCHAR 转换偶发 `TypeError`（本工程 polars `group_by().sum('v')` API 变更就踩了一脚）——跨版本迁移先跑 smoke。
- **UDF 三宗罪**：丢并行优化、丢 null 传播心智、丢类型推断；能用 `CASE/list_transform/宏` 表达的别上 UDF；真要上，用 `type='arrow'` 向量化批量传参。
- **GIL 与多进程幻想**：Python UDF 在多线程共享一个连接时不会加速（回调串行化）；横向扩展要换 MotherDuck/多进程各自读 Parquet。
- **DBAPI 的 `%` 参数与 LIKE 冲突**：`execute("... LIKE '%x%'")` 会被当占位符解析报错——用参数位或转义 `%%`。
- `df()` 全量物化到 pandas 是常见内存炸弹——大结果走 `to_arrow_table()` 分批或直接 `COPY TO parquet`。

## 核心概念速览（中英对照）

- **替换扫描** — Replacement scan：SQL 标识符回落到宿主语言对象的解析机制。
- **关系 API** — Relational API：无 SQL 的代数对象链（scan/filter/project/aggregate）。
- **标量 UDF** — Scalar user-defined function：逐行/逐批回调宿主语言函数。
- **向量化 UDF** — Vectorized UDF：以整批（numpy/Arrow）为单位的 UDF。
- **零拷贝** — Zero-copy（via Arrow）：共享列式缓冲区避免序列化。
- **DBAPI 2.0** — Python 数据库接口规范：execute/fetch/cursor 约定。
- **appender** — Appender API：批量行级高速写入器。
- **参数化查询** — Parameterized query：占位符绑定值，防注入。
- **RecordBatchReader** — Arrow 流读取器：DuckDB `.arrow()` 当前返回的流式对象。
- **游标隔离** — Cursor isolation：`con.cursor()` 独立事务/参数上下文。

## 最新演进与工业实践

- **Python 客户端 ABI 策略**：DuckDB 对 Python 提供全平台 wheel 且承诺稳定（版本线 ✅ GitHub releases：1.5.5/2026-07-22）；`pyproject` 生态把 duckdb 当作"默认分析后端"（DuckDB + pandas + Polars 三件套已是数据工程课标配）。
- **Polars 协作关系**：两者共享 Arrow 内存标准，Polars 1.x 已把默认后端切到 Arrow，DuckDB↔Polars 往返真零拷贝（官方 https://pola.rs 未逐页 curl ⚠️；社区实践定性）。
- **客户端概览权威入口**：https://duckdb.org/docs/stable/clients/overview ✅（列 Python/R/Java/Node/Wasm 全矩阵）。
- **工业教训**：多起公开博客报告"Python UDF 把 DuckDB 变成比 pandas 更慢的 pandas"——本目录 2.57 s vs 0.03 s 的 86 倍差距即量化佐证（🔧 本工程自测，非原书数据）。
