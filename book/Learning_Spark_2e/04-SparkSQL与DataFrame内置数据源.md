# 04 · Spark SQL 与 DataFrame：内置数据源

> 原书第 4 章（Spark SQL and DataFrames, Part 1：内置数据源）。章骨架 ✅ 按 ApacheCN 全译镜像实抓还原；Spark 行为 = ⚠️ 转述 + 官方文档实链。对位：[bigdata 04 SparkSQL 与结构化数据](../bigdata/04-SparkSQL与结构化数据.md)、[bigdata 09 存储与文件格式](../bigdata/09-存储与文件格式.md)、[TDG 06 SparkSQL 与 Dataset](../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md)、[TDG 04 聚合与复杂类型](../Spark_The_Definitive_Guide/04-聚合与复杂数据类型.md)。

## 4.1 在应用中用 Spark SQL

- `spark.sql("SELECT ...")` 返回 DataFrame——SQL 与 API 双语互写是 2e 的核心教学承诺；
- **表与视图**：`df.createOrReplaceTempView("t")`（会话级）、`createGlobalTempView`（跨会话，`global_temp` 库）、`createTempView`（防覆盖变体）；托管/非托管表概念经 Catalog/Hive Metastore 进入；
- **SQL 数据库与表**：`CREATE DATABASE`/`CREATE TABLE [USING parquet]`；managed（数据归 Spark 管，DROP 连数据删）vs external（`LOCATION` 指外部路径，DROP 只删元数据）——数据工程的第一道所有权边界；
- **元数据查看**：`SHOW DATABASES/TABLES/COLUMNS`、`DESCRIBE`、`spark.catalog.*`；
- **缓存 SQL 表**：`CACHE TABLE`（物化）vs `CACHE LAZY TABLE`（用时才物化）；与 DataFrame `persist` 的关系在词表上打通。

## 4.2 内置数据源：Parquet / JSON / CSV / ORC / Text

- **DataFrameReader/Writer 对称 API**：`spark.read.parquet(p)` / `df.write.parquet(p)`；JSON/CSV 带选项族（`header`、`inferSchema`、`delimiter`、`multiLine`、`mode/PERMISSIVE`…）；
- **Parquet**：列式 + 嵌套友好 + 压缩（snappy 默认口径）；谓词与列裁剪下推是默认红利；**Spark 生态事实标准落盘格式**；
- **JSON**：半结构化直读；嵌套列展开（`from_json`/`schema_of_json` 用法 ⚠️ 转述）；
- **CSV**：类型全靠推断或显式 schema——生产口径"永远给显式 schema"（社区共识，书中同调）；
- **读写矩阵**：同一数据可"读成 DataFrame→注册视图→SQL 查→再写 Parquet"，本章端到端示例走完整环。

## 4.3 🔧 实测类比组（非本书 Spark 引擎行为）

用 DuckDB 1.5.5 做"DataFrameReader 的单机替身"（meas.txt G1 组，临时件 `D:\develops\tmp\dbwave_w8_lkspark\g1.csv`）：

1. 三行混合类型 CSV（含空值、日期）→ `read_csv()` 自动推断出 `BIGINT/VARCHAR/DOUBLE/DATE`——对应 Spark `inferSchema=true` 的行为直觉：**推断是把列全扫一遍的代价**；
2. `count(score)=2 / count(*)=3`、`avg=8.375`：空值参与聚合的口径与 Spark `avg` 忽略 null 一致（概念类比，非引擎同源保证）；
3. CSV→`COPY TO parquet`→回读 `WHERE score>8` 命中 1 行：列式文件谓词过滤的最小闭环，对应本章"Parquet 读回即带下推"的教学点。

结论口径：schema 推断、null 语义、下推三件事在单机列式引擎里同样成立——Spark 的差异在于这些动作发生在**分区 × executor** 的尺度上（⚠️ 转述）。

## 4.4 写侧细节（⚠️ 转述 + 官方文档）

- `df.write.mode("overwrite|append|ignore|error")` 四态；
- `partitionBy("year","month")` 产出 Hive 风格目录 `year=2024/month=1/...`——本章埋点、第 5 章外部数据源展开；
- `bucketBy`（仅托管表可用）、sortBy、`option("compression")`；
- 写出即多任务并行：文件数≈分区数——"小文件问题"的第一成因（第 7 章回收）。

## 4.5 工程判断（重构观点）

- SQL 与 DataFrame 不是"两种写法选一种"，而是**同一计划树的两种拼写**：可组合、可互相嵌入（`df.sql` 里引用视图、SQL 结果继续 API 链）。2e 比 TDG 更早把这个"双语教学"做成结构（第 4/5/6 三章反复用双语对照同一任务）。
- "内置 vs 外部"的分界线是**要不要带依赖**：内置零 jar、外部要 `--packages`——读者的运维直觉应从 API 直接映射到 classpath。

## 4.6 章小节骨架总览（✅ 镜像实抓逐节对账）

| 原书小节（回译） | 本文件对应 |
| --- | --- |
| 在 Spark 应用程序中使用 Spark SQL／基本查询示例 | 4.1 |
| SQL 表和视图／托管与非托管表 | 4.1 表条目 |
| 创建 SQL 数据库和表（创建托管表／创建非托管表） | 4.1 |
| 创建视图／临时视图与全局临时视图 | 4.1 视图条目 |
| 查看元数据 | 4.1 元数据条目 |
| 缓存 SQL 表 | 4.1 CACHE 条目（07 章回收） |
| 将表读取到 DataFrames 中／DataFrames 和 SQL 表的数据源 | 4.2 |
| DataFrameReader／DataFrameWriter | 4.2、4.4 |
| Parquet（读入 DataFrame／读入 SQL 表／写出 DataFrame／写出 SQL 表） | 4.2 Parquet 条 |
| JSON（读入 DataFrame／读入 SQL 表／写出／JSON 数据源选项） | 4.2 JSON 条 |
| CSV（读入 DataFrame／读入 SQL 表／写出…） | 4.2 CSV 条 |
| ORC／文本／save 全家（load/save 组合模式） | 4.2 读写矩阵段 |

## 4.7 重建示例：双语一个环（本目录重做；⚠️ 语义转述官方 SQL 文档线）

```sql
-- 路径直读 → 注册视图 → SQL 查 → 写成分区 Parquet（本章教学闭环）
CREATE OR REPLACE TEMP VIEW sales AS
  SELECT * FROM parquet.`data/sales/*.parquet`;

SELECT region, year, sum(amount) AS total
FROM sales
WHERE year >= 2024 AND amount IS NOT NULL
GROUP BY region, year
ORDER BY year, region;
```

```python
(spark.sql("SELECT * FROM sales WHERE region='APAC'")
   .write.mode("overwrite")
   .partitionBy("year")          # 落盘即 Hive 目录：year=2024/...
   .parquet("out/apac"))
# == ⚠️ 未执行；行为口径见 sql-data-sources-load-save-functions.html ✅ curl 200
```

🔧 侧证：G1 组（同目录 `g1.csv→g1.parquet`）验证了"推断→落列式→过滤回读"三环在单机引擎同样成立；本目录用它替代 Spark 实操完成手感训练（非本书 Spark 引擎行为）。

## 4.8 课堂问题（答不出回本文件）

1. DROP 一张 managed 表与一张 external 表，磁盘上分别发生什么？
2. global temp view 的命名空间前缀是什么、可见域到哪为止？
3. `CACHE TABLE` 与 `CACHE LAZY TABLE` 的差别与 07 章 `persist` 的对应？
4. CSV 为什么必须显式 schema？给两个事故场景。
5. 写出文件数≈什么？由此引出哪个运维问题（4.4→07）？
6. "同一计划树两种拼写"在 API 层怎么互嵌（4.5）？

## 核心概念速览（中英对照）

- **spark.sql** — SQL 字符串入口：返回 DataFrame。
- **TempView / GlobalTempView** — 会话级/全局级注册视图（`global_temp` 库）。
- **Managed / External Table** — 托管表（数据随表亡）/外部表（只亡元数据）。
- **Spark Catalog** — 库表函数注册中心：`spark.catalog`。
- **CACHE TABLE / LAZY** — SQL 侧物化缓存与惰性缓存。
- **DataFrameReader / Writer** — 读源/写源对称 DSL。
- **inferSchema** — 扫一遍换类型推断：便利即成本。
- **Parquet** — 列式嵌套格式：默认下推红利。
- **ORC** — 列式（Hive 系）：与 Parquet 同类选项。
- **mode(append/overwrite…)** — 写四态：落盘行为开关。
- **partitionBy** — 写出 Hive 风格目录分区。
- **bucketBy** — 仅托管表的分桶：join/agg 加速布局。
- **PERMISSIVE/mode(JSON)** — 坏记录处理策略族。
- **小文件问题** — 分区×并行度乘积的副产物（预埋）。

## 最新演进与工业实践

- **SQL 语法面扩张**：3.x→4.0 新增 pipe 语法（`|>`）、session variables、collation、VARIANT 类型（✅ Spark 4.0.0 Release Notes 实抓，https://spark.apache.org/releases/spark-release-4-0-0.html）——本章"SQL 双语"的教学面比成书时宽得多。
- **格式面**：Variant/半结构化直读是 2024–2026 热点（⚠️ 转述，Databricks/Spark 双侧宣传）；社区对"JSON 慢、Parquet 为王"的判断依旧成立；CSV 显式 schema 仍是生产铁律（官方文档持续强调 ✅ https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html）。
- **湖仓衔接**：托管/外部表 + `USING delta` 的第三选项在成书同年出现（第 9 章），2026 年回看：表格式层（Delta/Iceberg）正在吸收"managed 表"的职能，元数据服务化（Polaris/Unity/Glue）成为新战场。
- **单机对照**：DuckDB `read_csv/read_parquet` + `COPY TO` 与本章 Reader/Writer 一一对应（🔧 G1），教学上可用 DuckDB 先建"下推/推断"直觉再上 Spark——本目录的实操替代方案。
- **对照互链**：中文实战的 SQL 侧细节坑（数据源版本、UDF 注册）见 [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)。
