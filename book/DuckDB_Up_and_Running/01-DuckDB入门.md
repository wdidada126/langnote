# 01 · Getting Started with DuckDB（DuckDB 入门）

> 覆盖原书第 1 章。目录来源：✅ 官方示例文件 `Chapter_1.ipynb` 标题实抓。本章是全书的"十分钟心智模型"：连一个库、造一张表、插一条记录、查一遍、聚合一次、JOIN 一次、直接读 pandas，最后用速度与内存两个尺子收束。

## 内容规格（小节地图，✅ 实抓自官方示例 notebook）

- **Chapter 1. Getting Started with DuckDB**
  - **A Quick Look at DuckDB**：DuckDB 定位（进程内 OLAP）、`import duckdb` + `duckdb.connect()` 两形态——新库文件 `test.db` 与内存库 `:memory:`；notebook 里以注释并排给出两种连接写法（✅ 示例代码实抓）。
  - **Loading Data into DuckDB**：`CREATE TABLE` DDL 建表 → 后续以 `INSERT` 与直接从文件加载双路径（与第 2 章衔接）。
  - **Inserting a Record**：`INSERT INTO … VALUES` 单行/多行；参数位 `execute(sql, params)`。
  - **Querying a Table**：`SELECT … WHERE` 基础查询；结果出口 `fetchall()/df()`。
  - **Performing Aggregation**：`GROUP BY/HAVING` 第一次见列存引擎的聚合速度。
  - **Joining Tables**：两表 JOIN（第 5 章会放大到 580 万行航班×机场实测口径）。
  - **Reading Data from pandas**：替换扫描（replacement scan）——`SELECT * FROM df` 直接命中内存里的同名 DataFrame，零导入。
  - **Execution Speed**：与 pandas 直觉口径的快慢对比（本章给结论，[04 章](04-DuckDB与Polars.md)/[05 章](05-用DuckDB做探索性数据分析.md)给数字）。
  - **Memory Usage**：进程内引擎的内存画像：默认 `memory_limit` 与 `threads`。

## 核心技术清单

- 连接对象即线程安全入口：`duckdb.connect(path, read_only=…, config=…)`；`path=None/":memory:"` 两种内存态。
- 三类执行面：`execute()`（DBAPI，带参数）、`sql()`（关系/查询面）、`con.register()`（将宿主对象挂成视图）。
- 结果出口四件套：`fetchall()`/`fetchdf()`/`fetchdf(chunk)`/`arrow()`（1.5 线 `.arrow()` 返回 RecordBatchReader，见 DIA 06 实测）。
- 替换扫描是本草章的"魔法"：DataFrame、（1.5.5 实测）Polars DataFrame、Arrow Table 都能被 `FROM 变量名` 直接吃掉。
- 设置面：`duckdb_settings()` 目录 + `SET memory_limit='…'`/`SET threads=N`；等价地，`connect(path, config={'threads': N, 'memory_limit': '…'})` 可在建连时注入（配置项与 SET 同集）。
- 文件即表语法糖的两种身份：查询期临时表 vs `CREATE TABLE AS` 物化——本章示例只做前者，落库动作在第 2 章。
- 连接四姿势：`connect()`（内存）/`connect('test.db')`（文件）/`read_only=True`（只读）/`config={…}`（画像覆写）——本章 notebook 只出现前两种。
- 方言初触点：`FROM 'file.parquet'` 文件即表（第 2/5 章主菜，此处只露一角）。

## 🔧 实测（1.5.5；官方默认画像 + 最小闭环）

1. 环境画像 ✅：`SELECT name,value FROM duckdb_settings() WHERE name IN('memory_limit','threads')` → `memory_limit=25.0 GiB`、`threads=16`（本机 16 核，默认吃满；`enable_progress_bar=false` 在无 TTY 环境）。
2. 建库/建表/插值/查/聚合/JOIN 全链路 ✅：与 notebook 同型代码在 1.5.5 全部原样可跑（无报错、无行为差异）——本章是"成书代码到 1.5.5 零改动"的部分。
3. 替换扫描直查 10M 行 pandas DataFrame（2 列，`g` 分组求 `sum(v)` 取 Top-3）：**0.03 s**，且结果与 pandas 原生（0.11 s）、Polars（0.06 s）逐值一致；10M×2 列 DataFrame 全程未落盘、未导入。
4. 同题文件面：`SELECT count(*) FROM 'flights2015.parquet' WHERE AIRLINE='UA'`（5.8M 行 5 列谓词）**0.01 s**——"Execution Speed"一节的现代量化：过滤/聚合类查询已是毫秒级，瓶颈在网络与 IO，不在 SQL。
5. **内存→文件闭环** ✅：`:memory:` 里 CTAS 造表后查询正常；换进程重开同一 `.db` 文件数据仍在——"内存库练手、文件库交作业"的最小心智，与 notebook 的 `test.db` 路线互证。
6. **只读姿势**：`READ_ONLY` 挂载/连接下查询照常（09 章 sqlite 只读 ATTACH 后 count 0.09 s ✅），写路径被拒（机制转述）——本章练习期先别加只读，交作业时再收。
7. 版本漂移点（影响本章示例）：`con.sql(sql, [参数])` 位置参数在 1.5.5 直接 TypeError，须 `params=` 或 `execute`；`duckdb_extensions()` 的 `extension_type` 列消失（见 00 漂移清单 1/2）。

## 易错点与陷阱

- **内存库不是免费午餐**：`:memory:` 库随连接对象销毁；notebook 重启 = 数据蒸发。练习期建议一开始就落文件（书中 `test.db` 路线）。
- **替换扫描的名字遮蔽规则**：库内已有同名表/视图时，`FROM df` 命中的是表不是变量——先 `DROP VIEW` 或 `unregister()`。
- **`fetchdf()` 全量物化**：把千万行结果直接 `.df()` 是内存炸弹的起点（07 章实测：经 duckdb-engine 拉 2M 行要 14.4 s，原生 3.38 s——先选出口再谈大小）。
- **默认线程=全部核**：笔记本上跑 `SET threads` 前先想清楚是否要给别的进程留核；多进程各自开 DuckDB 时尤其。
- **`read_only=True` 与替换扫描共存**：只读连接里 `register()` 仍可用，但 `CREATE TABLE` 会炸——练习时先别加只读。
- **成书与 1.5.5 的 API 面**：`duckdb.typing.DOUBLE` 一类类型别名在 1.5 已移除，UDF 类型用字符串 `"DOUBLE"`（同 DIA 06 实测）。
- **`.db` 不是 SQLite**：DuckDB 默认数据库文件扩展常被写成 `.db`（书中 `test.db`），但文件页是 DuckDB 自有格式——SQLite 打不开；跨到 SQLite 页要走 `sqlite_scanner`（02/09 章实测口径）。
- **进程内 = 锁在文件系统层**：多进程同时开同一库文件会撞锁（并发叙事见 [../DuckDB_in_Action/09-构建与部署数据应用.md](../DuckDB_in_Action/09-构建与部署数据应用.md)），本章单进程世界感受不到，第 7 章起 notebook+脚本并行时会撞到。
- **`con.sql()` 是惰性出口**：不 `.show()/.df()` 就不会真正执行——给"Execution Speed"一节计时时把 execute 与 collect 分开看，否则会把物化时间错记成查询时间。

## 关键 API 速查（1.5.5 实测注记）

| API | 用途 | 注记 |
| --- | --- | --- |
| `duckdb.connect(path)` | 入口 | ✅ 文件/`:memory:` |
| `con.execute(sql, params)` | 参数化执行 | ✅ 用 `execute` 传位置参数 |
| `con.sql(sql)` | 查询/关系面 | ⚠️ 位置 params 已移除 |
| `con.register(name, obj)` | 挂宿主对象 | ✅ df/Polars/Arrow 通吃（1.5.5 实测 Polars 直查 0.00s/3M） |
| `duckdb_settings()` | 画像 | ✅ |
| `FROM 'file.parquet'` | 文件即表 | ✅ 本章预告，02/05 章主用 |
| `connect(..., config={'threads':…})` | 建连注入画像 | ✅ 与 `SET threads` 同集 |

## 最小闭环练习清单（对照 notebook，✅ 全部在 1.5.5 原样可跑）

| # | 动作 | 命令骨架 | 复核锚点 |
| --- | --- | --- | --- |
| 1 | 建库/建表 | `connect('test.db')` + `CREATE TABLE` | 实测 2 |
| 2 | 插入 | `INSERT INTO … VALUES`，参数走 `execute(sql, params)` | 漂移清单 1 |
| 3 | 查询 | `SELECT … WHERE` → `fetchall()/df()` | 实测 2 |
| 4 | 聚合 | `GROUP BY` + `count(*)` | 实测 4 |
| 5 | JOIN | 两表 `JOIN USING` | 放大版见 05 实测 1 |
| 6 | 直查 DataFrame | `SELECT … FROM df`（替换扫描） | 实测 3（0.03 s/10M） |
| 7 | 画像 | `SELECT * FROM duckdb_settings()` | 实测 1（25 GiB/16 线程） |

## 自测判分（三问全对再进 02 章）

- 三引擎同题（10M group-by）各耗时多少？→ 0.11/0.06/0.03 s（实测 3）。
- `FROM df` 何时不命中你的 DataFrame？→ 库内同名表/视图优先（陷阱 2）。
- 本章两个"尺子"设置叫什么、默认多少？→ `memory_limit=25.0 GiB`、`threads=16`（实测 1）。

## 常见报错对照（1.5.5 实测原文）

| 现象/写法 | 报错（截断） | 正解 |
| --- | --- | --- |
| `con.sql(sql, [1])` | TypeError: sql(): incompatible function arguments | 走 `con.execute(sql, [1])` 或 `params=`（漂移清单 1） |
| `FROM df` 查出陌生 schema | 无报错——命中库内同名表 | `SHOW TABLES` 核对；`DROP VIEW`/`unregister()` 后重来 |
| SQLite 工具打开 `test.db` | file is not a database | DuckDB 自有页格式；跨库走 `sqlite_scanner`（02/09 章） |
| UDF 里 `duckdb.typing.DOUBLE` | ModuleNotFoundError: duckdb.typing | 类型名用字符串 `"DOUBLE"`（漂移清单 8） |

- 前三行在 1.5.5 原文可复现（🔧 本目录复核）——"报错文本是比教程更快的老师"，本章撞墙记录全部登记进 00 漂移清单。

## 与其他章/书的互链

- 导入全家桶（CSV/Parquet/Excel/MySQL）→ [02-数据导入DuckDB.md](02-数据导入DuckDB.md)
- SQL 方言与 CLI → [03-SQL速成与CLI.md](03-SQL速成与CLI.md)
- 替换扫描与 Polars/Arrow 零拷贝深水区 → [04-DuckDB与Polars.md](04-DuckDB与Polars.md)
- 同题的更细方言/UDF 实测 → [../DuckDB_in_Action/03-执行SQL查询.md](../DuckDB_in_Action/03-执行SQL查询.md)、[../DuckDB_in_Action/06-融入Python生态.md](../DuckDB_in_Action/06-融入Python生态.md)
- 嵌入式**行存**对位（SQLite）→ [../Using_SQLite/00-总览与阅读地图.md](../Using_SQLite/00-总览与阅读地图.md)（#87 已落盘，"行/列单机对位"锚点两册互设）；并发与部署叙事 → [../DuckDB_in_Action/09-构建与部署数据应用.md](../DuckDB_in_Action/09-构建与部署数据应用.md)。

## 思考题（合上笔记再答）

1. 替换扫描的命中顺序是什么？什么时候 `FROM df` 拿到的不是你的 DataFrame？（先注册对象/库内表后宿主变量；同名表遮蔽——见陷阱）
2. 为什么本章把 Execution Speed 与 Memory Usage 并成两节？给出你机器上 `memory_limit/threads` 的默认值与含义。（25.0 GiB/16；进程内引擎无服务端，配额即宿主配额）
3. 用一行 SQL 在 580 万行航班 parquet 上求 p90 延误并按航司分组，估耗时。（实测全组 0.06 s：`SELECT AIRLINE, quantile_cont(DEPARTURE_DELAY,0.9) FROM … GROUP BY 1`）
4. 本章 notebook 的 `test.db` 路线与 `:memory:` 路线，各自的"数据蒸发时刻"是什么？（文件库=DROP/换库；内存库=连接对象销毁/内核重启——实测 5）

## 2026 视角补注

- "分析界的 SQLite"官方口径仍是选型第一课（SQLite 官网 whentouse 页明确把分析负载让给 DuckDB——DIA 00 已引，两书共用该结论）。
- 1.x 的 API 稳定承诺让 2024 年的 notebook 到 1.5.5 仍能整跑，但**Python 客户端层**（参数传递、扩展清单列、Arrow 出口形态）是漂移集中区——升级时先跑 00 漂移清单八条。

## 核心概念速览（中英对照）

- **进程内数据库** — In-process database：以库形式嵌入宿主语言、无独立服务进程。
- **列式存储引擎** — Columnar engine：按列存/扫/聚合，OLAP 快的根因。
- **替换扫描** — Replacement scan：SQL 标识符回落到宿主内存对象的解析机制。
- **内存数据库** — In-memory database：`:memory:` 连接，生命周期=连接对象。
- **DBAPI 参数化** — Parameterized query：占位符绑定值，防注入。
- **关系 API** — Relational API：`con.sql()` 返回的链式关系对象。
- **memory_limit** — 内存上限设置：默认按宿主可用内存自适应（实测 25.0 GiB）。
- **threads** — 并行度设置：默认=逻辑核数（实测 16）。
- **文件即表** — Direct querying files：`FROM 'x.parquet'` 零导入扫描。
- **Arrow 流式出口** — RecordBatchReader：1.5 线 `.arrow()` 的返回形态。

## 最新演进与工业实践

- **1.x 版本线**（GitHub releases 实抓）：1.0（2024-06）→ 1.1（2024-09，本书写作期）→ 1.2/1.3/1.4 → **1.5.5（2026-07-22，最新）**；PyPI 同步发 wheel（https://pypi.org/project/duckdb/ ✅），"pip 装一个分析引擎"已是数据栈常识。
- **客户端矩阵**：Python 之外 R/Node/Wasm/JDBC 全线维护（https://duckdb.org/docs/stable/clients/overview ✅）；本目录的 1.5.5 漂移清单同样适用于 R/Node 用户（扩展清单/参数签名类变更）。
- **工业实践**：数据分析教学与面试题库已把"直查 DataFrame + 直查 Parquet"当作 DuckDB 第一课（与本书第 1 章同构）；生产上强调"先估算 `df()` 体量、大结果走 Arrow/Parquet 落盘"。
- **对照读物**：DIA 第 2 章从 CLI/扩展切入的"上手"叙事与本章 notebook 叙事互补——两种入门路径都跑通才算真上手：[../DuckDB_in_Action/02-快速上手CLI与扩展系统.md](../DuckDB_in_Action/02-快速上手CLI与扩展系统.md)。
