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

## 关键 API 对象速查

| API | 用途 | 版本注记（1.5.5 实测） |
| --- | --- | --- |
| `duckdb.connect(path, read_only, config)` | 入口 | ✅ |
| `con.execute(sql, params)` / `con.sql(sql)` | DBAPI/关系双轨 | ✅ |
| `con.cursor()` | 独立事务上下文 | 未点验 ⚠️ |
| `rel = con.sql(...); rel.filter().aggregate()` | Relation 链 | 未点验 ⚠️（API 在） |
| `con.register(name, obj)` / `unregister` | 显式替换扫描注册 | ✅ |
| `con.create_function(n, f, [types], ret)` | 标量 UDF | ✅；类型串 `"DOUBLE"`，`duckdb.typing` 已移除 |
| `df = con.sql(...).df()` | 取回 pandas | ✅ |
| `.arrow()` | 取 Arrow | ⚠️ 返回 **RecordBatchReader**（流） |
| `.to_arrow_table()` | 取 Arrow Table | ✅ 新名；`fetch_arrow_table` 已弃用 |
| `duckdb.connect()` + `rel.to_table()` 等 | polars 互喂 | 经 Arrow，✅ |
| `con.append("t", df)` | DataFrame 直灌 | ✅ 0.12s/1M 行 |
| `con.install_extension/load_extension` | 扩展 | ✅ |

## 本章实测复现（临时脚本，repo 零产物）

```python
# D:\develops\tmp\dbwave_duckdb\ 下执行（数字均为本机真实输出）
import duckdb, time, numpy as np, pandas as pd, polars as pl
df = pd.DataFrame({"g": np.random.randint(0,1000,10_000_000), "v": np.random.rand(10_000_000)})
con = duckdb.connect()
# 三引擎同题对照（10M 行 group by 求和取 Top-3）：
t0=time.time(); df.groupby("g")["v"].sum().sort_values(ascending=False).head(3)
print(f"pandas  {time.time()-t0:.2f}s")     # 0.13s
t0=time.time(); pl.from_pandas(df).group_by("g").agg(pl.col("v").sum().alias("s")).sort("s",descending=True)
print(f"polars  {time.time()-t0:.2f}s")     # 0.05s
t0=time.time(); con.sql("SELECT g,sum(v) s FROM df GROUP BY g ORDER BY s DESC LIMIT 3").fetchall()
print(f"duckdb  {time.time()-t0:.2f}s")     # 0.03s（df 即替换扫描，零注册）
# Arrow 出口行为：
print(type(con.sql("SELECT g,sum(v) FROM df GROUP BY g").arrow()))   # RecordBatchReader
print(con.sql("SELECT g,sum(v) FROM df GROUP BY g").to_arrow_table().num_rows)  # 1000
# UDF 代价：
con.create_function("classify", lambda x: "hi" if x>0.5 else "lo", ["DOUBLE"], "VARCHAR")
t0=time.time(); con.sql("SELECT classify(v), count(*) FROM df GROUP BY 1").fetchall()
print(f"row-wise UDF {time.time()-t0:.2f}s")  # 2.57s ≈ 纯 SQL 的 86 倍
```

## 与其他章/本书的互链

- SQL 方言里这些对象怎么组合 → [03-执行SQL查询.md](03-执行SQL查询.md)、[04-高级聚合与数据分析.md](04-高级聚合与数据分析.md)
- 替换扫描/导入姿势的量化底线 → [12-附录A-客户端API.md](12-附录A-客户端API.md)
- 管道化 Python 侧（dlt 也是 Python-first）→ [08-构建数据管道.md](08-构建数据管道.md)

## 思考题（合上笔记再答）

1. 替换扫描的查找顺序是什么？什么情况下 `FROM df` 命中的不是你的 DataFrame？（先注册对象/库内表，再回落宿主变量；同名表存在时表优先——见陷阱）
2. 为什么官方建议"能缓存就别 UDF"？给出本目录实测比值。（行级回调 2.57 s vs 纯 SQL 0.03 s ≈ 86×，且丢向量化/并行）
3. 100 万行结果要喂给下游 pandas，写出你最省内存的出口链路。（`COPY TO parquet` 落盘分片读，或 `to_arrow_table`+`df()` 分批；避免一次 fetchall 三份拷贝）

## 2026 视角补注

- Python 包发布节奏跟 core release 完全同步（1.5.5 wheel 本机 `pip install` 即得 ✅），`duckdb` 已是 PyPI 分析类目头部依赖。
- Arrow 接口从 Table 默认转向流式 RecordBatchReader 是 1.5 线的重要行为变更（实测 DeprecationWarning 路径），大结果集链路应尽早切 `to_arrow_table()`/流式消费。
- 与 Polars 的关系从"竞品叙事"走向"同总线叙事"（共享 Arrow 内存），选型判据变成"SQL-first 还是表达式-first"。

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
