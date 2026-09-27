# 02 · Importing Data into DuckDB（数据导入 DuckDB）

> 覆盖原书第 2 章。目录来源：✅ 官方示例文件 `Chapter_2.ipynb` 标题实抓。本章是"数据进得来、出得去"：CSV/Parquet/Excel/MySQL 四类格式的加载与导出双向通道，外加 `register()` 免导入路线。

## 内容规格（小节地图，✅ 实抓自官方示例 notebook）

- **Chapter 2. Importing Data into DuckDB**
  - **Creating DuckDB Databases**：`.db`/`.duckdb` 文件即库；建库参数（含 `read_only`）。
  - **Loading Data from Different Data Sources and Formats**
    - **Working with CSV Files**：两条路——**SQL 查询法**（`read_csv_auto()`，notebook 原注"SELECT 子句可省"）与 **`register()` 法**（挂视图零拷贝）；**Exporting a table to CSV**（`COPY … TO … (FORMAT CSV)`）。
    - **Working with Parquet Files**：Loading/Exporting 双向；`read_parquet()` 与 `COPY … TO (FORMAT PARQUET)`。
    - **Working with Excel Files**：Loading Excel files（excel 扩展）+ **Export tables to Excel**。
  - **Working with MySQL**：`mysql_scanner` 路线 ATTACH MySQL → 抽表入 DuckDB（本机无 MySQL 服务器 ⚠️ 未实证）。

### 本章数据底座与连接形态（实测口径）

- 主数据：Kaggle **2015 Flight Delays**（`usdot/flight-delays`，第三方笔记仓库明记本书用此数据 ✅）——官方示例已预转为 `datasets/flights/year=2015/month=XX/flights.parquet` 12 文件（✅ 仓库树实抓），另有 `airports.parquet`（322 行子集）/`airlines.parquet`/对应 CSV 与 `airports_and_airlines.xlsx`。
- 本目录对应物：HTTPS 冷拉 12 文件物化为 `flights2015.parquet`（5,819,079 行/144 MB，拉取过程见 [08 章](08-用DuckDB访问远程数据.md)实测 4）；SQLite 镜像 `flights2.db`（140 MB，09 章实测一）。
- 建库形态：`duckdb.connect('my.db')` 即本章第一节 "Creating DuckDB Databases" 的全部——库=单文件，不存在独立服务地址/端口概念。

## 核心技术清单

- 四格式 × 双向矩阵：CSV/Parquet/Excel/MySQL 各有"读入口"和 `COPY TO` 出口；Parquet↔DuckDB 原生最顺，CSV 需类型推断（`read_csv_auto`），Excel 走 community/core 扩展，MySQL 走 scanner 扩展。
- 加载双路径心智：**先 register/直查（零落库）→ 满意后 CTAS 落库**——notebook 的"SELECT 子句可省"原注就是鼓励第一路径。
- 读函数参数三件套：`header`/`columns`（或 `names+types`）/`sample_size`——嗅探翻车时的三板斧（CSV/JSON/Parquet 通用命名习惯）。
- `register()`：零拷贝把文件/DataFrame 挂成临时视图——"探索期不建表"的关键姿势。
- `read_csv()` 的 `header=true`、`sample_size`、列类型覆写；`read_json_auto` 见 [06 章](06-DuckDB与JSON文件.md)。
- 文件即表语法：`FROM 'x.parquet'`/`FROM 'x.csv'`（替换扫描的文件形态）。
- Hive 分区目录直读：`year=2015/month=01/…` 配 `hive_partitioning=1`（本书数据即此布局；HTTP 场景有坑，见 08 章）。
- `COPY (SELECT …) TO 'f' (FORMAT …, HEADER true)` 是统一的"导出总线"，顺带承担落盘缓存职责。
- `COPY … TO 'dir/' (FORMAT PARQUET, PARTITION_BY (k))` 分片落盘（机制在册；本目录未逐测 ⚠️）——本书数据的官方月度分区布局即这类导出的产物形态。
- SQLite 文件直读：`sqlite_scan(db, '表')` / `ATTACH (TYPE sqlite)` 两条路（scanner 家族与 MySQL 同构；本目录在 09 章把 sqlite 路线跑出了实数，可平移理解本节 MySQL）。

## 🔧 实测（1.5.5；本书航班数据上的格式往返）

1. **parquet→CSV**：5 列 × 5,819,079 行 `COPY … TO 'fl.csv' (FORMAT CSV, HEADER true)` **0.17 s**，得 107 MB（源 parquet 中该 5 列占比约 31 MB 级）。
2. **CSV→parquet 回灌**：`COPY (SELECT * FROM read_csv('fl.csv', header=true)) TO 'fl.parquet'` **0.54 s**，得 **31 MB**——同一份数据 **CSV/parquet ≈ 107/31 = 3.5 倍体积差**。
3. **查询代价对照**：`WHERE DISTANCE>2000`（同为 373,982 行结果）CSV **0.14 s** vs parquet **0.007 s** ≈ **20 倍**——本章"用 Parquet 存中间结果"的最硬理由。
4. **Excel 读**（`airports_and_airlines.xlsx`，34 KB）：`read_xlsx(file, sheet:='airports')` → **322 行 0.01 s**；`sheet:='airlines'` → 13 行。⚠️ 漂移：该 build 无 `excel_tables()` 列 sheet 函数（报 Catalog Error），openpyxl 读该文件 sheetnames 亦返 []（样板文件元数据奇异）——列 sheet 名请用其他工具或问扩展。
5. **Hive 分区目录直读（本地）**：`read_parquet('datasets/flights/year=2015/month=*/*.parquet', hive_partitioning=1)` 得 5,819,079 行并附 `year/month` 伪列 ✅（同一 glob 走 HTTP 会 404，见 [08 章](08-用DuckDB访问远程数据.md)实测）。
6. **MySQL/ scanners**：`mysql_scanner`、`postgres_scanner` 均可 install（13.3 s/7.8 s，✅）；无本地服务器，ATTACH 查询 **⚠️ 未实证**（scanner 用法转述自官方扩展索引 https://duckdb.org/community_extensions/ ✅，引根目录不深链）。
7. **SQLite 桥同型可跑**：与 MySQL 同族的 scanner 路线在本目录已被完整实证——`ATTACH 'flights2.db' (TYPE sqlite, READ_ONLY)` 后 count **0.09 s**、sqlite×parquet 跨源 join **0.19 s**（数字与场景详见 [09 章](09-云端DuckDB与MotherDuck.md)实测一）；scanner 家族的读姿势同构，可放心平移。
8. **分片导出实测定型**：`COPY (SELECT * FROM 'flights2015.parquet') TO 'pout/' (FORMAT PARQUET, PARTITION_BY (AIRLINE))` **3.14 s** 落 **14 个 `AIRLINE=XX/` 目录**；`read_parquet('pout/*/*.parquet', hive_partitioning=1)` 回读 **5,819,079 行 / 0.02 s**——此前标 ⚠️ 的 PARTITION_BY 分片落盘由本条转 🔧 ✅，官方"月度分区"布局的生成端在本目录同机复现。
9. **`sample_size` 只管推断不管扫描**：`read_csv('fl.csv', header=true, sample_size=1000)` 对 107 MB/580 万行全量计数 **0.13 s**——该参数只缩类型推断的取样窗，不是扫描上限；嗅探翻车调它，"慢"不是它的锅。

## 易错点与陷阱

- **`register()` 不是导入**：视图不持久、不统计（ANALYZE 不可用）、重名即隐；反复 JOIN 的大表最终仍建议 `CREATE TABLE AS SELECT`（CTAS）落库，10M 行内存 CTAS 约半秒级（DIA 实测 0.55 s，口径可平移：[../DuckDB_in_Action/10-大数据集性能考量.md](../DuckDB_in_Action/10-大数据集性能考量.md)）。
- **CSV 类型推断翻车**：邮编/电话被推成数值、日期格式混排 → `read_csv(..., columns={…}, all_varchar=true)` 先粗后细。
- **Excel 是三条路**：excel 扩展 `read_xlsx`（快、命名参数 sheet）、spatial 扩展 `st_read`（读 ogr 图层）、以及导出侧的 `st_write`——版本漂移集中在前者的函数集（实测 `excel_tables` 不存在）。
- **多 sheet 工作簿**：一个 xlsx 多 sheet 要逐个 `read_xlsx(sheet:=…)`，没有"整簿入库"原生函数——别指望像 CSV 一样一把 glob。
- **导出不如导入多样**：`COPY TO` 原生只有 CSV/Parquet/JSON；Excel 写出在该版本不存在原生 copy function（"Export tables to Excel" ⚠️ 原书或经 pandas/openpyxl 中转——以 notebook 代码为准的推定）。
- **MySQL ATTACH 是拉取式**：远端表以视图形态出现，过滤是否下推决定成败；大表搬运先 `CREATE TABLE AS SELECT` 落地再分析。
- **`.db` 后缀不是格式承诺**：本目录把 DuckDB 库与 SQLite 库分别记作 `flights2.db`（SQLite 页，经 ATTACH TYPE sqlite 读写）与默认 DuckDB 文件——同名扩展、两种格式，工具链（DBeaver/SQLite CLI）打开前先确认 TYPE，别拿错钥匙。
- **导出即快照**：`COPY TO` 出去的 CSV/Parquet 是时点副本，不是活视图；要"湖+真相"双份就配 09 章 DuckLake 的快照语义，别对着导出文件查增量。

## 导入/导出决策表

| 目标 | 入口 | 出口 | 实测注记 |
| --- | --- | --- | --- |
| CSV | `read_csv_auto`/`read_csv` | `COPY TO (FORMAT CSV)` | 0.17s/5.8M；体积 3.5× |
| Parquet | `read_parquet`（glob/Hive 可用） | `COPY TO (FORMAT PARQUET)` | 0.54s/5.8M；扫描 20× 于 CSV |
| Excel | `read_xlsx(f, sheet:='…')` | ⚠️ 经 pandas | 322 行 0.01s |
| MySQL | ATTACH (TYPE mysql) + scanner | 同左反向（INSERT 回写） | ⚠️ 无服务器未证 |
| DataFrame | 替换扫描/`register()` | `.df()`/`to_arrow_table()` | 零拷贝见 04 章 |
| JSON | `read_json_auto` 族 | `COPY TO (FORMAT JSON, ARRAY true)` | 详见 [06 章](06-DuckDB与JSON文件.md) |
| SQLite | `ATTACH (TYPE sqlite)`/`sqlite_scan` | ATTACH 后 `CREATE TABLE AS` | 读 0.09 s/写 3.16 s（09 章实测） |
| 远程 HTTP 文件 | `read_*('https://…')`（httpfs） | 先 `COPY TO` 本地化再谈复用 | 冷 23.68 s→本地 0.01 s 级（08 章） |

## 常用导入命令速查（本目录实测注记）

```sql
SELECT * FROM 'f.csv';  -- 文件即表（CSV 自动嗅探）
SELECT * FROM read_csv('f.csv', header=true, columns={'zip':'VARCHAR'});
COPY (SELECT * FROM t) TO 'out.parquet' (FORMAT PARQUET);  -- 实测同型：CSV→parquet 5.8M 行 0.54 s/31 MB
SELECT * FROM read_parquet('dir/year=2015/month=*/*.parquet', hive_partitioning=1);  -- ✅ 本地 5,819,079 行
SELECT * FROM read_xlsx('w.xlsx', sheet:='airports');  -- ✅ 322 行；sheet 必须命名参数
ATTACH 'x.db' AS s (TYPE sqlite, READ_ONLY);  -- ✅ scanner 家族样板（09 章全实测）
INSTALL mysql_scanner; LOAD mysql_scanner;  -- ✅ 13.3 s（连接路径 ⚠️ 未实证）
```

## 一页导入/导出流水线（实测命令串联）

```sql
-- ① 原始 CSV → 本地 parquet（实测 2：5.8M 行 0.54 s / 31 MB）
COPY (SELECT * FROM read_csv('raw.csv', header=true)) TO 'stg.parquet' (FORMAT PARQUET);
-- ② 事实表按业务键分片（实测 8：3.14 s → 14 目录，下游按 Hive 湖读）
COPY (SELECT * FROM 'stg.parquet') TO 'pout/' (FORMAT PARQUET, PARTITION_BY (AIRLINE));
-- ③ 报表出口：ND JSON 一行一对象给流式下游（06 章实测 7 同型）
COPY (SELECT AIRLINE, count(*) n FROM 'stg.parquet' GROUP BY 1) TO 'agg.json' (FORMAT JSON);
```

- 三步覆盖"交换格式进 → 存算格式驻 → 分片/文档格式出"，命令全部在 1.5.5 本机跑过；行式镜像（SQLite）作第四站见 [09 章](09-云端DuckDB与MotherDuck.md) 实测一。

## 与其他章/书的互链

- JSON 专题 → [06-DuckDB与JSON文件.md](06-DuckDB与JSON文件.md)；远程直读与 glob 坑 → [08-用DuckDB访问远程数据.md](08-用DuckDB访问远程数据.md)
- 落库后的查询姿势 → [03-SQL速成与CLI.md](03-SQL速成与CLI.md)、[05-用DuckDB做探索性数据分析.md](05-用DuckDB做探索性数据分析.md)
- "无持久化探索"的系统化讲法 → [../DuckDB_in_Action/05-无持久化的数据探索.md](../DuckDB_in_Action/05-无持久化的数据探索.md)（同主题、更重 SQLite/Excel 对照）
- 湖仓视角：Parquet 作为事实标准存储 → [../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md)

## 思考题（合上笔记再答）

1. 同一份 580 万行数据，为什么"存 parquet、只在对账时导 CSV"？给出你机上的体积与扫描倍数。（3.5×体积、20×过滤扫描——本目录实测）
2. `register()` 与 `CREATE TABLE AS` 怎么选？（一次性探索 vs 反复使用/需统计；CTAS 半秒级不心疼）
3. Excel 多 sheet 工作簿入库的最小可行流程？（列 sheet→逐 sheet `read_xlsx(sheet:=)`→CTAS 入 DuckDB；列 sheet 名工具外部解决）
4. 把 580 万行"Kaggle 原始 CSV→本目录 parquet→SQLite 镜像"两跳的实测耗时与体积报出来。（CSV→parquet 0.54 s/31 MB；DuckDB→SQLite 3.16 s/140 MB——行存落盘体积反超列存 4.5 倍）

## 2026 视角补注

- 2024–2026 社区扩展治理后，excel/spatial 等已进统一安装通道（本目录实测全部 `install_extension` 成功，版本以 commit 号示之，如 excel `f4c72b5`）；"扩展即格式适配器"的格局稳固。
- CSV 仍是交换格式、Parquet 是存算格式的分层共识在两本 DuckDB 书里同口径；DuckLake（09 章）进一步把"Parquet + 元数据"变成带 ACID 的湖仓格式。

## 核心概念速览（中英对照）

- **自动嗅探** — read_*_auto：抽样推断列名/类型/分隔符的加载函数族。
- **注册视图** — register()：零拷贝把对象挂为临时视图。
- **CTAS** — Create Table As Select：物化落库的唯一正道。
- **Hive 分区** — hive_partitioning：目录 `k=v` 升格为列。
- **COPY 总线** — COPY TO/FROM：统一导出（CSV/Parquet/JSON）。
- **Scanner 扩展** — Scanner extension：mysql/postgres/sqlite 外部库桥接。
- **谓词下推** — Predicate pushdown：过滤送进远端/文件 footer 减扫描量。
- **行组裁剪** — Row-group pruning：Parquet min/max 统计跳过整组。
- **类型覆写** — columns/all_varchar：先粗读后 CAST 的防翻车策略。
- **交换格式 vs 存算格式** — CSV for exchange, Parquet for storage：体积 3.5×/扫描 20× 的实证分工。

## 最新演进与工业实践

- **格式生态现状**：1.5.5 原生读写 CSV/Parquet/JSON，扩展补 Excel/AVRO（`avro` 在装列表 ✅）/delta 类（⚠️ `deltalake` 已不在 1.5.5 仓库清单，delta 支持路径转介社区/ducklake 侧——装前必查 `duckdb_extensions()`）。
- **文档口径**：数据导入官方指南族（https://duckdb.org/docs/stable/ 下 data ingestion 板块，✅ 站点可达）与本章结构几乎一一对应，可作英文对照读物。
- **工业实践**：ETL 中间层"一律 Parquet、报错留 CSV"已是默认习惯；本书示例把 2015 Kaggle CSV 预转成按月分区 parquet（官方示例仓库实测即此布局），2026 视角看是标准动作而非可选优化。
- **互读**：行式数据库导入导出的对位口径（含 appender 高速写）见 [../DuckDB_in_Action/12-附录A-客户端API.md](../DuckDB_in_Action/12-附录A-客户端API.md)；SQLite 单机库的导入叙事见 [../Using_SQLite/00-总览与阅读地图.md](../Using_SQLite/00-总览与阅读地图.md)（#87 已落盘：其 `.import`/CLI 路线与本章 ATTACH 路线互为"导入 vs 挂载"两解）。
