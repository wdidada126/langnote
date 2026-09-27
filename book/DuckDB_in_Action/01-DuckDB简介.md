# 01 · An introduction to DuckDB（DuckDB 简介）

> 覆盖原书第 1 章。目录来源：✅ Manning 官方 TOC 实抓（product id 3153）。本章是全书立论：**DuckDB 是什么、为谁而造、何时用/何时不用**。

## 内容规格（这章在讲什么）

- **1.1 是什么**：进程内（in-process）嵌入式**分析**数据库——像 SQLite 一样零运维、单文件、无服务进程，但引擎为 OLAP 重写：列式存储格式、向量化执行、并行扫描、自动并行 join/聚合。（重构自 Manning About the book："a modern embedded analytics database that runs locally, efficiently processing and querying gigabytes of data… without requiring a server"。）
- **1.2 为什么值得关注**：分析师/数据工程师被"小数据要起集群、大数据要导数据库"的两头折磨；DuckDB 让笔记本上 GB 级分析成为一行代码的事；MIT 协议、社区驱动。
- **1.3 何时用**：本地/边缘的 ad-hoc 分析、ETL 中间层、数据科学笔记本、应用内嵌分析、文件即数据库、CI 里的查询测试。
- **1.4 何时不用**：高并发多写 OLTP（那是 PostgreSQL/MySQL 的活）、作为中心化的多用户查询服务（进程内模型决定它没有 server 端用户/权限模型——云短板由 MotherDuck 补，见第 7 章）、超大集群级算力需求。
- **1.5 用例**：书中以能源统计、Stack Overflow 倾倒数据、纽约出租车为主菜（10 章）。
- **1.6 生态位**：与 pandas/Duck 式"笔记本工具"和 ClickHouse/Snowflake 式"分析仓库"之间的一条新缝：**嵌入式 OLAP**。与 SQLite（嵌入式 OLTP）构成"嵌入式双子星"互补。
- **1.7 数据处理流程五步**：格式与来源（CSV/JSON/Parquet/数据库）→ 数据结构（表/DataFrame/视图）→ 写 SQL → 执行 → 使用/加工结果（导出、可视化、下游应用）。全书各章即按这条流水线展开。

## 核心技术清单

- 进程内架构：无守护进程、库直接链接进宿主（Python/C/Java/Wasm）。
- 列式 + 向量化：按列压缩存放、以向量批（典型 2048 值）推进表达式，CPU cache 友好。
- 并行执行：默认吃满逻辑核（`threads` 设置，实测本机 =16）。
- 单文件持久化：`my_db.duckdb` + WAL（`my_db.duckdb.wal`），拷贝即备份。
- "无服务器 ≠ 无云"：MotherDuck 把同一引擎接上云协同（第 7 章主题）。
- SQL-first：完整关系代数 + 半结构化类型（LIST/STRUCT/MAP），不是 NoSQL 查询语言。

## 🔧 实测（本机数字，方法可复跑）

**环境**：Windows 11 / 16 核 / Python 3.13.2 / duckdb 1.5.5（`pip install duckdb` 一次成功）。

1. 引擎身份与默认并行度：
   ```sql
   SELECT version();                          -- v1.5.5
   SELECT current_setting('threads');         -- 16（=逻辑核数）
   SELECT current_setting('memory_limit');    -- 25.0 GiB
   ```
2. "GB 级分析一行代码"验证：内存表 CTAS 造 1000 万行（`FROM range(10000000)` + random）用时 **0.55 s**；随后 `GROUP BY g ORDER BY s DESC` 全表聚合 **0.04 s**、`count(*) WHERE v>0.5` 热扫描 **0.011 s**。量级结论：千万行 = 毫秒级响应，与第 1 章"笔记本即数仓"的立论一致。
3. 持久化代价：同量数据写进数据库文件 CTAS **3.31 s**、文件 77.3 MB（含一个 VARCHAR 列）；说明"内存即抛"与"落盘"的成本差近 6 倍，用 `SELECT` 直查文件（第 5 章）常比落库更划算。
4. ⚠️ CLI 本机未装（`duckdb` 不在 PATH）；以上用 Python API 等价完成。官方安装页 https://duckdb.org/install/ ✅ 可达（含 CLI 一键下载）。

## 易错点与陷阱

- 把 DuckDB 当 SQLite 的"分析版替身"塞进高并发 Web 后端：**跨进程只有一个连接持有数据库文件**（实测：另一进程 `read_only=True` 也被 IOException 拒绝），它不是"谁都能连的服务"。
- 用 `memory_limit`/`threads` 默认值跑共享机器：默认吃满全部核与 80% 内存，笔记本风扇起飞、容器 OOM——生产要先 `SET`。
- 以为"列存 = 一切快"：点查单行、小表高频写仍是行存强项；1.4 节的"何时不用"要照抄进选型 checklist。
- 行转列思维：DuckDB 里 `INSERT` 逐行喂是反模式，批量 `APPEND`/`COPY`/CTAS 才是正门（附录 A.4 主题）。

## 关键参数与对象速查

| 参数/对象 | 默认值（1.5.5 实测） | 一句话 |
| --- | --- | --- |
| `threads` | 16（=逻辑核） | 单查询并行度；共享机器先降 |
| `memory_limit` | 25.0 GiB（≈80% RAM） | 超出即溢盘/报错 |
| `max_temp_directory_size` | 90% 磁盘 | 溢盘配额 |
| `database_path` | `:memory:` | connect 首参决定落不落盘 |
| `access_mode` | read_write | 只读挂载用 read_only |
| `preserve_insertion_order` | true | 大 COPY 吞吐开关 |
| `.duckdb` 文件 | 单文件 | 库 = 1 文件 + `.wal` |
| WAL | 自动 | 崩溃恢复日志，CHECKPOINT 收敛 |
| `extension_directory` | `~/.duckdb/extensions` | 扩展按 os_arch+版本分目录 |
| 许可 | MIT | 内核与主客户端均 MIT |

## 本章实测复现（临时脚本，repo 零产物）

```python
# D:\develops\tmp\dbwave_duckdb\b1_engine.py（要点摘录）
import duckdb, time, os, multiprocessing
con = duckdb.connect()
print(con.sql("SELECT version()").fetchone())            # ('v1.5.5',)
print(con.sql("SELECT current_setting('threads')").fetchone(), multiprocessing.cpu_count())  # (16,) 16
print(con.sql("SELECT current_setting('memory_limit')").fetchone())  # ('25.0 GiB',)

t0=time.time()
con.sql("CREATE TABLE t AS SELECT i id, random() v, (i%997)::int g FROM range(10000000) tbl(i)")
print(f"CTAS 10M: {time.time()-t0:.2f}s")                 # 0.55s
print(f"groupby cold: ", end="")
t0=time.time(); con.sql("SELECT g,sum(v) FROM t GROUP BY g ORDER BY 2 DESC").fetchall()
print(f"{time.time()-t0:.2f}s")                           # 0.04s

# 持久化对照
p = duckdb.connect("bench.duckdb")
t0=time.time(); p.execute("CREATE TABLE big AS SELECT ... FROM range(10000000)")
print(f"persistent CTAS: {time.time()-t0:.2f}s")          # 3.31s
# 关闭后 os.path.getsize("bench.duckdb") → 77.3 MB
```

## 与其他章/本书的互链

- 方言语法细节 → [03-执行SQL查询.md](03-执行SQL查询.md)、[04-高级聚合与数据分析.md](04-高级聚合与数据分析.md)
- "不导库查文件" → [05-无持久化的数据探索.md](05-无持久化的数据探索.md)
- Python 宿主细节 → [06-融入Python生态.md](06-融入Python生态.md)
- 云协作补强 → [07-云端DuckDB与MotherDuck.md](07-云端DuckDB与MotherDuck.md)
- 并发一言 → [12-附录A-客户端API.md](12-附录A-客户端API.md)
- 内核原理（列存/向量化出处）→ [../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md)

## 思考题（合上笔记再答）

1. 为什么说"DuckDB = 分析界的 SQLite"既是好类比又是坏类比？（好：嵌入形态/单文件/零运维；坏：负载模型与并发模型完全相反——见 1.4 与实测锁行为）
2. 你手上 2 GB 的月 CSV 报表，按本章五步流程给出最短方案，并说明是否需要落库。（参考答案方向：read_csv 直查 + PIVOT 出报表，不建库；周期性再转 Parquet）
3. 什么信号出现时你该从 DuckDB 迁去 ClickHouse/数仓？（并发多写、常驻服务、PB 级共享、需要细粒度权限/审计）

## 2026 视角补注

- 本章"何时不用"清单在今天仍然成立，但每条都有了官方泄压阀：并发共享→MotherDuck/DuckLake，超大算力→集群版数仓，点查服务→仍建议正牌 OLTP。
- 原书未提的 `lightweight storage migrations`（1.4 起）让跨版本文件兼容压力前移到工具链，选型时"锁大版本 + 升级演练"仍是铁律。
- 教学角度：本章五步流程是全书最好的"给老板看的 15 分钟"，实操对应 demo 即 05 章三行 SQL。

## 核心概念速览（中英对照）

- **嵌入式数据库** — Embedded database：以库形式链接进宿主进程、无独立服务端的数据库形态。
- **分析型/OLAP** — Online Analytical Processing：以扫描+聚合为主的负载，区别于事务型 OLTP。
- **列式存储** — Columnar storage：按列连续存放，利于压缩与只读所需列。
- **向量化执行** — Vectorized execution：解释执行的算子按定长向量批处理，摊薄解释开销、吃满 SIMD。
- **进程内并行** — Intra-process parallelism：单查询自动切分任务到 `threads` 个 worker。
- **单文件数据库** — Single-file database：整个库落在一个 `.duckdb` 文件（+WAL）里。
- **替换扫描** — Replacement scan：SQL 里直接引用宿主语言变量名（如 DataFrame）当表用（第 6 章）。
- **零拷贝** — Zero-copy：与 Arrow/pandas 共享内存布局而非序列化为字节。
- ** MotherDuck** — 与 DuckDB 无缝对接的云数据仓库（第 7 章）。
- **MIT 许可证** — MIT License：DuckDB 的宽松开源协议，商用友好。

## 最新演进与工业实践

- **版本现状（2026-09）**：成书基于 0.10/1.0，现最新稳定线 **v1.5.5（2026-07-22）**，1.x 自 2024-06-03（v1.0.0）已发 63 个 release（GitHub releases API 实抓 ✅）；存储兼容性按大版本承诺，读旧文件持续可用。https://github.com/duckdb/duckdb/releases/tag/v1.0.0 ✅
- **与 SQLite 的分工定调更新**：SQLite 官方 "when to use" 页（✅ https://sqlite.org/whentouse.html）明确推荐"应用内嵌分析用 DuckDB"，"嵌入式双子星"叙事已成官方口径。
- **与 ClickHouse 的定位之争**：ClickHouse（✅ https://github.com/ClickHouse/ClickHouse）仍是"中心化服务 + 高吞吐实时"路线，DuckDB 是"进程内 + 文件直查"路线；2025–2026 年 ClickHouse 也推本地单机模式/`clickhouse local`，两者在"笔记本分析"场景摩擦增多——选型的判别标准不变：是否需要多写并发与常驻服务。
- **工业采用**：DuckDB 基金会（荷兰 Stichting 非营利）治理，MotherDuck 公司提供商业云；被 DBeaver/DataGrip 之外的现代栈广泛集成：dbt-duckdb、dlt、Dagster、Datasette 生态、Quack 类客户端/服务端实验（社区报道，⚠️ 未官方定版）。
- **论文线**：向量化执行的学理源头（MonetDB/X100、C-Store 列存）见 [../../db/db.md](../../db/db.md) 论文索引；原理纵深另参 [../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md)。
