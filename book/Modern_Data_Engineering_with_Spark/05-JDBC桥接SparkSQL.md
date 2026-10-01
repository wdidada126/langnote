# 05 — JDBC 桥接 Spark SQL（Bridging Spark SQL with JDBC）

> 《Modern Data Engineering with Apache Spark》第 5 章 · Apress 2022 · Scott Haines
> 章题与章序 ✅ Crossref DOI `10.1007/978-1-4842-7452-1_5` 实抓；**章内小节结构 ⚠️ 推定**（依据章题与 Spark SQL/JDBC 官方文档主题域反推），非原书小节文本。
> 三态标记：✅ 实抓 / ⚠️ 推定或转述 / 🔧 本机实测类比（非本书 Spark 平台行为）。

## 1. 本章定位

Spark 与「存量关系库世界」的接缝章：读入用 `df.read.jdbc`，写出用 `df.write.jdbc`，中间是谓词下推与并行分片的艺术。数据工程师的日常里 JDBC 面往往比文件系统面更脏（锁、限流、方言、时区），所以本章的工程浓度高于 API 浓度——这也是它区别于 TDG「数据源概览」一节带过的地方。

## 2. 读侧：一次「远程表」的解剖（⚠️ 按章题域重构）

- 入口三参：`url`（含驱动方言）、`dbtable`（表或**子查询**——后者是下推失败时的手工兜底）、`properties`（user/password/fetchsize）。
- **并行分片三件套**：`partitionColumn` + `lowerBound` + `upperBound` + `numPartitions`；不 partitionColumn 则单连接全表——入门事故第一名。
- 边界值语义：lower/upper **只定分片范围不过滤数据**，`"< lowerBound"` 归入第一片、`">= upperBound"` 归入最后一片（官方文档 ✅ https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html 明载，本波实测 200）。
- `predicates` 手动分片：日期/枚举列无均匀数值分布时的替代方案。
- `pushDownPredicate`（`dbtable` 生成时的 WHERE 注入）与 `pushDownAggregate`（3.2 起，⚠️ 本书是否已展开未证实）。

## 3. 写侧：从「能写」到「写得体面」

- `mode` 复用第 3 章四态；`truncate` vs `isolationLevel` 的权衡（可恢复写需事务隔离支持，官方列出四档隔离级别，⚠️ 细节以文档为准）。
- `batchsize` 决定 round-trip 数——与 fetchsize 成对出现的两侧性能钮。
- `createTableOptions`/`createTableColumnTypes`：方言建表控制。
- **upsert 无原生**（2022 语境）：JDBC V2 的事务性多分区写与 later 版本的能力在演进节补；书中工程方案大概率是 staging 表 + 手工 MERGE（⚠️ 推定）。

## 4. 下推语义的工程账（本章的隐形主线，⚠️ 重构）

| 下推项 | 生效条件 | 常见失效 |
|--------|----------|----------|
| 列裁剪 | SELECT 列在编译期已知 | UDF 吃整行 `*` |
| WHERE | 表达式可翻译成方言 SQL | 函数/正则方言不认 |
| LIMIT | 直译为方言 LIMIT | 下推后再 filter 使语义走样 |
| AGGREGATE | 3.2+ 部分函数白名单 | 非确定函数不下推 |

- 校核手段：`df.explain()` 看 V2 节点是否带 pushedDownFilters；数据库侧看执行日志——工程册的标准动作（⚠️ 重构）。

## 5. 🔧 实测·概念类比：下推前后的「拉取量」差异（SQLite 类比，非 Spark 行为）

```python
import sqlite3, time
s = sqlite3.connect(":memory:")
s.execute("CREATE TABLE big(id INTEGER PRIMARY KEY, k INT, pad TEXT)")
s.executemany("INSERT INTO big VALUES(?,?,?)",
              [(i, i % 97, 'x'*60) for i in range(1, 500001)])
# 「不下推」：全表拉回再过滤（模拟单连接 SELECT * 后 Spark 端 filter）
t0=time.perf_counter(); rows = s.execute("SELECT * FROM big").fetchall()
r1 = [r for r in rows if r[1] == 5]; naive=time.perf_counter()-t0
# 「下推」：谓词交给 SQLite，仅回传命中行
t0=time.perf_counter(); r2 = s.execute("SELECT * FROM big WHERE k=5").fetchall(); push=time.perf_counter()-t0
print(len(rows), len(r1), r1==r2, naive, push)
```

- 读数：源表 499999 行；两条路径**结果集完全一致**（r1==r2 为 True），但传输/物化行数从 50 万降到约 5 千——这就是下推的全部经济学。
- 类比边界：Spark 的 JDBC 下推发生在异构方言翻译层，还有 `fetchsize` 游标维度；SQLite 单机内存库无网络成本，比例失真（🔧 仅证「谁执行过滤」的量级差）。

## 6. 关系库在湖仓时代的位置（本书写于转折期）

- 2022 年本书把 JDBC 定位为「摄取源 + 消费汇」两头；中间态大数据一律落文件/表——此判断在 2024–2026 依然成立，只是「中间态」从裸文件换成了湖表：[../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md)、[../Apache_Paimon_Streaming_Lakehouse/01-导论流式湖仓与Paimon的崛起.md](../Apache_Paimon_Streaming_Lakehouse/01-导论流式湖仓与Paimon的崛起.md)。
- CDC 替代批量 JDBC 轮询成为主流摄取形态（→ 演进节；盘上 Paimon 的 CDC 入湖章节为纵深）。
- 与第 11 章对读：**Kafka 之于流式摄取 ≈ JDBC 之于批量摄取**，2022 年后二者边界被 CDC-to-Kafka（Debezium 类）打通（⚠️ 生态常识，非本书内容）。

## 7. 校读清单

- 作者用的关系库是 PostgreSQL/MySQL/SQL Server 哪种？——方言与隔离级别讨论的适配面。
- 是否演示 `dbtable` 包子查询的列别名强制写法？——实战高频坑。
- 写出是否触及「分区数=库连接数」的限流讨论？——工程成熟度的标志。

## 9. 下推排障决策树（本章的运维件，⚠️ 重构）

1. 读得慢？→ `df.explain()` 找 `PushedFilters` 是否为空。
2. 空则查三源：UDF/表达式不可译？列类型与谓词不匹配（隐式转换杀死索引）？优化开关被关（`pushDownPredicate=false` 遗留）？
3. 仍无解 → `dbtable` 手工包子查询（把 WHERE 写进字符串，注意**必须起别名** `(... ) AS t`，✅ 文档惯例）。
4. 聚合慢 → 3.2+ `pushDownAggregateEnabled` 白名单核对；不满足则库侧物化视图兜底。
5. 库被打挂 → 降 `numPartitions`、错峰、限流：JDBC 并发的道德上限由 DBA 决定而非 Spark 决定（工程册的人情世故，⚠️ 重构语气）。

## 10. 本章实验卡（⚠️ 非原书代码，Postgres/任意库可替）

1. 百万行表：单连接 `SELECT *` 读入 vs 四分片 `partitionColumn` 读入，对比墙钟与库侧连接数曲线。
2. 时间列分片：用 `predicates=[..LIKE '2022-01-%', ..]` 手写月度切片，体会「无均匀数值列」时的自由度。
3. 写出三击：`append` 后 `overwrite`（库侧 TRUNCATE 语义差异）→ `truncate` 对照 → 隔离级别参数实验（⚠️ 本地库先行）。
4. `fetchsize` 从 1000 到 100000 的梯度：观察 driver 内存与 round-trip 的镜像曲线。
5. 上下界哨兵实验：故意 lowerBound 设错，确认「边界外行仍被全数收入」的文档语义（2 章 §2 的实证位）。

## 11. 校读问答（五问五答）

- **Q：为什么本章单独成章而 TDG 一节带过？** A：工程册的读者要处理的是「库侧同事的抗议」——限流/方言/时区是工作不是 API。
- **Q：写侧 upsert 到底谁负责？** A：2022：手工 staging+MERGE；2026：湖表 MERGE/库原生 upsert 语法（✅ SQLite 示例见 🔧 与 13 章同源）。
- **Q：本章会讲 DataSource V2 吗？** A：⚠️ 存目概率高、展开概率低——展开与否直接决定读侧事务讨论的深度，校读时留意。
- **Q：和 6 章接口？** A：JDBC 表 `createExternalTable` 注册进 catalog 后即为「可发现对象」——两章合写摄取+发现闭环。
- **Q：和 11 章分工？** A：批量拉（本章）⇄ 变更推（11 章）；同一条数据生命线的上下游（§6 表）。

## 12. 章末锚点卡（速记三线，⚠️ 目录制）

- 一条主线：JDBC 读写的全部工程=「谁执行了多少过滤/传输了多少行」的博弈史。
- 一条警戒线：连接数即库侧政治资源——`numPartitions` 的每个数字背后都有一位 DBA 的血压（⚠️ 工程幽默但真实）。
- 一条接口线：读入接 3/4 章的管道，写出接 10/13 章的幂等 sink；CDC 线接 11 章——本章是三条线的枢纽。
- 记忆钩：「分区列三件套+边界不过滤」；哨兵值实验（卡 5）治终身遗忘。
- 平台观：库是「旧世界的文件」，湖是「新世界的库」——本书 2022 的过渡态写法，读 5/6/12 章时心里换轴即可。

## 观读三复（复核小记）

- 复核点一：§9 决策树与卡 5 哨兵实验互为表里——树是流程，卡是证据。
- 复核点二：下推白名单随版本漂移，引用前查 ✅ sql-data-sources-jdbc.html 当期措辞（本波实测 200）。
- 复核点三：本章「库的连接是有预算的公共品」立场贯穿 §9/§11/锚点卡——工程册的人情线，非 API 线。
- 与 03 分工再确认：格式在 3、库在 5、注册在 6——三章各守一个 I/O 面，勿混读。

## 核心概念速览（中英对照）

- **JDBC 数据源** — JDBC Data Source：以连接串+方言读远程表的数据源。
- **分区列分片** — Partition Column Sharding：lower/upper/num 生成并行 `BETWEEN` 切片。
- **dbtable 子查询** — Inline Subquery：把投影/过滤手工交给库执行的逃生门。
- **谓词下推** — Predicate Pushdown：WHERE 翻译进 dbtable；失败则全量搬运。
- **聚合下推** — Aggregate Pushdown：3.2 起部分算子可下发（⚠️ 白名单制）。
- **fetchsize/batchsize** — 游标/批量尺寸：读写两侧的 round-trip 旋钮。
- **truncate 选项** — Truncate Option：复用表结构清空而非 DROP 重建。
- **isolationLevel** — 事务隔离级别：可恢复多分区写的前提能力。
- **方言** — Dialect：类型/函数/引号规则的库间差异层。
- **CDC** — Change Data Capture：以变更流替代轮询的摄取范式（→ 演进）。

## 最新演进与工业实践

- **DataSource V2 JDBC 事务写**：Spark 3.x 后期 `jdbc` 支持基于 V2 的多分区事务写（⚠️ 转述；校核入口 ✅ https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html）。
- **JDBC 连接器生态**：Databricks 的 JDBC/DBTX 系连接器把「upsert/方言适配」产品化；开源侧 Spark 原生 jdbc 保持朴素（⚠️ 观察性陈述）。
- **CDC 摄取成为默认**：Debezium/Kafka Connect → Kafka → Spark Structured Streaming 的组合替代了大批「JDBC 定时轮询全表」的老管道；盘上对应流式读法见第 11 章与 [../Streaming_Systems/02-数据处理的来龙去脉.md](../Streaming_Systems/02-数据处理的来龙去脉.md)（变更日志叙事线）。
- **仓库联动新形态**：2024–2026 湖仓直连 OLTP 的「零 ETL」（如 DLF/托管镜像类服务）蚕食 JDBC 手工层——本书技能转为「理解其原理以治理遗留管道」（⚠️ 观察性陈述，不做厂商背书）。
- **驱动安全**：JDBC 供应链漏洞（如 log4j 之外的驱动 CVE）使「驱动版本白名单」进入数据工程 checklist（⚠️ 行业惯例）。
