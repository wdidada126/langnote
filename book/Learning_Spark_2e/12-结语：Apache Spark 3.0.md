# 12 · 结语：Apache Spark 3.0（及向 4.x 的桥）

> 原书第 12 章（Conclusion: Apache Spark 3.0）。章骨架 ✅ 按 ApacheCN 全译镜像实抓还原：Spark Core 与 Spark SQL（动态分区裁剪／自适应查询执行 AQE：AQE 框架、SQL 连接提示、SMJ/BHJ/SHJ/洗牌复制 NLJ 四家族）／Catalog 插件 API 与 DataSourceV2／加速器感知调度器／结构化流（新触发/状态面）／PySpark、Pandas UDF 与 Pandas 函数 API（类型提示重设计、迭代器支持、新 Pandas 函数）／功能与语言变更（支持/弃用语言清单）／DataFrame/Dataset API 变更／explain 命令增强／发布公告。Spark 行为 = ⚠️ 转述 + 官方文档。本章是 2e 的"版本宣言"：前面 11 章讲 2.4 教学基线，这里把 3.0 的新武器逐一挂名。

## 12.1 AQE：本章的主角（回收第 7 章全部伏笔）

⚠️ 转述（官方 sql-performance-tuning 页 ✅ curl 200；AQE 总开关 `spark.sql.adaptive.enabled`，3.2 起默认开）：

- **动态合分区**：shuffle 后按真实数据量合并小分区——第 7 章"shuffle.partitions=200 魔法数"的终结者；
- **自动倾斜处理**：`skewJoin` 检测大分区并拆分复制——第 7 章"加盐三板斧"的托管化；
- **运行时改选 join**：统计到位后 BHJ/SMJ/SHJ 现场切换，`coalescePartitions` 与 join 策略联动；
- **SQL 连接提示**：`/* BROADCAST(t) */` 等 SQL 侧 hint——第 7 章 DataFrame hint 的 SQL 分身；
- **DPP（动态分区裁剪）**：用一侧的实际过滤值现场裁剪另一侧分区——第 5 章静态分区裁剪的进阶态。

## 12.2 接口面：Catalog 插件、DSv2、explain

- **Catalog Plugin API**：`spark.sql.catalog.*` 可插拔外部元数据（Iceberg REST/Delta 各取所需）——第 9 章"表格式之争"未来走向 catalog 化的种子；
- **DataSourceV2 批流双人格**：连接器同一实现既批读又流读（第 5/8 章回收）；
- **explain 增强**：`EXPLAIN FORMATTED/COST` 与 `spark.sql.explain...` 输出可读性升级（第 7 章调试回收）。

## 12.3 Python 与流的换代件

- **Pandas UDF 重设计**：类型提示 + `Iterator[pandas.DataFrame]`（分组 mapInPandas 的流式化）——第 5/11 章 Python 性能线的完全体；
- **新 Pandas 函数 API**：`applyInPandas` 家族在 Dataset/DataFrame 语义对齐；
- **Structured Streaming**：3.0 的 `foreachBatch`（第 8/9/11 三章的枢纽件）、Kafka 批读同源、状态 API 演进预告（Arbitrary State 实验线，4.0 转正 v2）。

## 12.4 语言与 API 的断舍离（书时代公告）

- R（SparkR）进入弃用通道；Python 2 支持终止（2.0 已断）；Java 8/11 与 Scala 2.12 为当时基线——**"版本宣言章"的另一半是老化预告**：这些基线在 2026 全部过期（见演进节），本章是全书时效衰减最快的一章，恰是其"教学册"身份的代价。

## 12.5 从 3.0 到 4.0：本章内容的时间轴外推（✅ 官方 Release Notes 实抓）

https://spark.apache.org/releases/spark-release-4-0-0.html（curl 200）要点：4.x 首版、5100+ ticket、390+ 贡献者；**Spark Connect 转正面**（`pyspark-client` 1.5MB、Connect 默认发行包、`spark.api.mode`、Java 客户端 API 对齐、ML on Connect、Swift 客户端）；**SQL 面**（VARIANT 类型、SQL UDF、session variables、pipe 语法、collation）；**PySpark 面**（原生绘图 API、Python Data Source API、Python UDTF、UDF 统一 profiling）；**流面**（Arbitrary State API v2、State Data Source 调试通道）。本章 12.1–12.3 的每一节都能在 4.0 找到直系续命——教学结论：**读 2e 学词表，读 4.x release notes 校准实现。**

🔧 **计划自适应的单机对照（非本书 Spark 引擎行为）**：DuckDB `EXPLAIN` 的 HASH_JOIN/HASH_GROUP_BY 选择是编译期定死（meas.txt G4 组）——拿它反衬 AQE 的本质"运行时统计再规划"：单机引擎无 shuffle，也就无"运行时才知道分区大小"这回事。**AQE 行为本身不可本机实测，全节 ⚠️ 转述。**

## 12.6 全书收束（重构观点)

12 章走完的地图是：统一叙事（1–2）→ 结构化内核（3–6）→ 性能（7）→ 流（8）→ 湖（9）→ ML 与生产（10–11）→ 版本宣言（12）。作为教学册，它的完成度标尺是"词表是否跨版本保值"——Job/Stage/Task、UnsafeRow/Encoder、BHJ/SMJ、watermark/state、事务日志/merge、Pipeline/Tracking：这些在 2026 依然现役；而安装、语言基线、手动调优仪式已经翻篇。用这本书的正确方式：**把它当 2020 年的快照，把官方文档当实时源，把本目录当两者间的翻译层。**

## 12.7 章小节骨架总览（✅ 镜像实抓逐节对账）

| 原书小节（回译） | 本文件对应 |
| --- | --- |
| Spark Core 和 Spark SQL（总起） | 12.1 |
| 动态分区裁剪（DPP） | 12.1 末条 |
| 自适应查询执行：AQE 框架／SQL 连接提示 | 12.1 首两条 |
| 洗牌排序合并连接（SMJ）／广播哈希连接（BHJ）／洗牌哈希连接（SHJ）／洗牌并复制嵌套循环连接（SNLJ） | 12.1 表位、07 章对照 |
| 目录插件 API 和 DataSourceV2 | 12.2 |
| 加速器感知调度器 | 12.4 注（GPU 线，演进节回收） |
| 结构化流（3.0 新件） | 12.3 末段 |
| PySpark、Pandas UDF 和 Pandas 函数 API：类型提示重设计／迭代器支持／新的 Pandas 函数 API | 12.3 前两枪 |
| 功能变更／支持的语言和已弃用的语言 | 12.4 |
| DataFrame 和 Dataset APIs 的变更 | 12.4 末、12.2 |
| DataFrame 和 SQL Explain 命令 | 12.2 末条 |
| 公告（3.0 发布节奏） | 12.5 |

## 12.8 重建示例：AQE 开关面板（本目录重做；⚠️ 参数语义转述官方 sql-performance-tuning ✅）

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")                    # 总闸（3.2+ 默认）
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true") # 动态合分区
spark.conf.set("spark.sql.adaptive.coalescePartitions.minPartitionSize", "64MB")
spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "128MB")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")           # 自动拆倾斜
spark.sql("SELECT /*+ BROADCAST(dim) */ * FROM f JOIN dim ON f.k=dim.k")# SQL 侧 hint
# 验收动作：SQL tab 对比开/关 AQE 的 plan 差异——本章给 07 章手活写"退休通知书"
```

## 12.9 课堂问题（答不出回本文件）

1. AQE 三件套各替代第 7 章哪件手活？
2. DPP 与静态分区裁剪的时机差在哪个阶段（对照 3.5 四阶段）？
3. 3.0 join 提示族（SMJ/BHJ/SHJ/SNLJ）里哪种永远该被怀疑？
4. "语言断舍离"公告里 R 与 Python 2 的下场说明教材的什么问题？
5. foreachBatch 为什么同时出现在 8/9/11 三章的回收位？
6. 用哪一条官方实据校准"3.0→4.0"的版本线（12.5）？

## 核心概念速览（中英对照）

- **AQE** — 自适应查询执行：运行时统计驱动的再规划。
- **动态合分区** — Coalesce Shuffle Partitions：小分区合并。
- **自动倾斜 join** — Skew Join Handling：大分区拆分复制。
- **DPP** — 动态分区裁剪：运行时值现场裁另一侧。
- **SQL Join Hints** — BROADCAST 等 SQL 侧计划干预。
- **SHJ/SNLJ** — 洗牌哈希/洗牌复制嵌套循环：join 家族补全。
- **Catalog Plugin** — 外部元数据可插拔接口。
- **DataSource V2 批流同体** — 一套连接器两种消费。
- **EXPLAIN FORMATTED/COST** — 可读计划输出升级。
- **Iterator[Pandas] UDF** — 类型提示化批式 Python UDF。
- **foreachBatch** — 微批落库/打分枢纽（跨章回收件）。
- **Arbitrary State API** — 细粒度自定义流状态（v2 于 4.0）。
- **Spark Connect** — 客户端/服务端协议化解耦（4.0 主线）。
- **VARIANT** — 半结构化类型入 SQL（4.0）。

## 最新演进与工业实践

- **3.0→4.x 版本线**（✅ https://spark.apache.org/releases/ 同族与 4.0.0 页）：3.1–3.5（2021–2024）交付 ANSI 兼容模式、materialized view 预告件、UTF-8 布局等；4.0（2025）交付 Connect/VARIANT/Python DSv2/State v2——本章"宣言"的所有续集在官方 release notes 可逐条对号；4.1 及后续 ⚠️ 未核验不写。
- **Java/Scala 基线更替**：4.0 需 Java 17 运行时线（⚠️ 转述发行说明），书时代的 JDK 8/11 公告整体过期——印证 12.4"版本宣言=老化预告"的判断。
- **Connect 生态**：JDBC/ODBC/REST 多语言客户端与 `spark.api.mode` 让"IDE/笔记本直连远端集群"成 2024–2026 教学与开发默认；本章 12.2 的接口化种子已长成主干。
- **湖仓/catalog 化**：12.2 Catalog Plugin + 第 9 章格式之争合流为 Polaris/Unity/Glue 的 REST Catalog 大战（⚠️ 转述产品线，盘上相邻书目在 [00 谱系表](00-总览与阅读地图.md) 已登记对位）。
- **中文引擎演进叙事**：批流合流与"计算引擎的演进"主题在盘上有专章讨论，读 [../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md) 可补国产视角；与本章互为"官方宣言/行业回声"。
