# 05 Synapse Notebook 与 Spark 数据工程 — Data Transformation and Processing with Synapse Notebooks（原书第 5 章）

> 章题 ✅ Packt 官方 ColorImages PDF 文本层实抓；配方级小节 ⚠️ 推定（一手旁证 = 官方仓库
> `chapter 5/code` 仅 chapter5.txt 一文件 + README 特性句「Perform exploratory data
> analytics using Apache Spark」「Read and write DataFrames into Parquet files using
> PySpark」）。机制 = Microsoft Learn 转述 ⚠️ + ✅ URL（2026-10-02 `curl -sI` 200）；
> Azure 不可实测 ⚠️；🔧 类比标注**非 Synapse 行为**；pyspark 本机不可装（波6 先例沿用），
> 概念面以 DuckDB/SQLite 类比。

## 5.1 Notebook = Synapse 的通用工作台

✅ `azure/synapse-analytics/spark/apache-spark-development-using-notebooks` ⚠️ 转述：
工作区笔记本挂 Spark 池，单元格混编 PySpark/Scala/SQL（`%%sql` 魔法打到 SQL 端点）；
内联/链接笔记本复用；`get_context()` 取会话。README 软件清单（Azure 订阅+SSMS+Power BI
Desktop+Pathway）不含本地 Spark——一切算力在云上 ⚠️。

**Spark 池供给侧** ✅ `spark/apache-spark-pool-configurations`：节点数/VM 规格/动态执行
器、Spark 3.x 版本线、Apache Arrow 加速 ⚠️；性能配方 ✅ `spark/apache-spark-performance`
（文件布局/分区数/缓存/广播小表）。

## 5.2 探索-转换-落湖主配方（对位 README 特性句 ⚠️）

1. **读**：`spark.read.parquet/csv/orc` 直读 ADLS（湖优先）；
2. **探**：`display()`/`df.printSchema()/summary()` 数据画像；
3. **转**：列运算/窗口/UDF；写回 `df.write.parquet(path, mode="overwrite")`——
   README 明示「Read and write DataFrames into Parquet files using PySpark」✅ 特性句实抓；
4. **供**：产出物供服务器端点外部表（03 章 3.7）与专用池 CTAS（01 章）双消费——
   **「一次加工、两处查询」的湖仓中枢**。

🔧**E4（主类比，非 Synapse）**：DuckDB 写 5M 行 Parquet（84.6MB）后按列读取——
只取 (k,v) 两列时压缩字节 60.0M vs 全列 84.6M（省 29%）；带谓词过滤查询 1.9ms。
演示「Parquet 列裁剪 + 谓词剪枝」是笔记本落湖格式选择的根本理由（落 Delta 另有事务面 ⚠️）。

🔧**E2 侧证**：转换时把 join 键相同的表按同键重分区（`repartition(n, key)`）≈
SQLite 分片实验里 HASH 共置 vs 跨片的 2.2× 差距（34.2ms vs 73.8ms，非 Synapse）——
「shuffle 是分布式第一大税」跨引擎成立。

## 5.3 会话、单元与依赖管理

⚠️ 转述：笔记本会话=独占 Spark 上下文，`maven/PyPI` 包可池级或会话级注入；
单元格并行执行（依赖标注）；导入笔记本=函数库复用。工程守则（编者归纳 ⚠️）：
笔记本要能被管道活动无头执行（02 章 Notebook 活动 ✅ `synapse-notebook-activity`），
故避免交互式状态依赖、参数走 `mssparkutils.notebook.run` 传参 ⚠️。

## 5.4 与 SQL 端点的双向门

- `%%sql` 单元格 → 专用池/服务器端点跑 T-SQL（把 Spark 编排与 SQL 加工缝在同一笔记本）⚠️；
- Spark 表 ↔ 外部表：Spark 写的 Parquet 目录可被服务器端点 `CREATE EXTERNAL TABLE`
  指认（✅ `sql/develop-tables-external-tables`；两侧 schema 声明重复是已知摩擦 ⚠️）；
- `spark.write` 直入专用池走 synapse 连接器（内部=批量装载引擎，01/02 章同源）⚠️。

## 5.5 探索分析到 ML 的桥（本章 → 06 章）

✅ `spark/apache-spark-machine-learning-mllib-notebook`：MLlib 管道（特征→训练→评估）
在笔记本内闭环；README 特性句「Work with notebooks for various tasks, including ML」✅
实抓——06 章 AutoML 把这条线接管到 Azure ML 服务面。

## 5.6 笔记本工程检查单（编者归纳 ⚠️）

1. 输出布局按查询谓词分区目录了吗（`dt=.../region=...`）？
2. 小文件合并（`repartition/coalesce`）做了吗？
3. 包依赖固定版本、可无头重放吗？
4. 落湖格式选型记录了吗（Parquet 简单/Delta 事务）⚠️？
5. 消费方（服务器端点/专用池/Power BI）的 schema 契约测试了吗？

## 5.7 与 repo 其他章/册的联系

- 被编排 → [02-数据管道与转换编排.md](02-数据管道与转换编排.md)；
- 供 SQL 消费 → [03-多节点最优处理与专用池调优.md](03-多节点最优处理与专用池调优.md)、
  [01-数据装载方法选型与落地.md](01-数据装载方法选型与落地.md)；
- ML 延伸 → [06-AzureMLAutoML回归数据增强.md](06-AzureMLAutoML回归数据增强.md)；
- 实时数据源 → [04-SynapseLink与Cosmos实时分析.md](04-SynapseLink与Cosmos实时分析.md)；
- 湖仓理论（跨波实链 ✅ 验名）：[../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md)（表格式/事务层纵深）、[../Amazon_Redshift_Cookbook_2e/06-半结构化与外部数据.md](../Amazon_Redshift_Cookbook_2e/06-半结构化与外部数据.md)（半结构化处理对照）。

## 5.8 笔记本-管道-仓库三角工作流（⚠️ 编者归纳）

```
        开发态(人)                运行态(机器)              消费态(查询)
   Synapse 笔记本 --参数化--> 管道 Notebook 活动 --调度--> 湖上 Parquet / 内表
        ^                                                       |
        +---------------- 画像/调试回路 <----------------------+
```

- 开发态：小样本（如 NYCTripSmall.parquet ✅ 仓库文件实抓）快速迭代；
- 运行态：`mssparkutils` 传参 + 无头执行（5.3），失败进管道重试面（02 章）；
- 消费态：产出物双出口——服务器端点外部表（03 章 3.7）或专用池 CTAS（01 章）；
- 回路：查询侧发现的脏数据/新字段回笔记本画像，形成闭环 ⚠️。

## 5.9 常见故障与对策表（⚠️ 编者归纳，对位 apache-spark-performance 主题域）

| 症状 | 根因 | 对策 ⚠️ |
| --- | --- | --- |
| 首单元格分钟级等待 | 会话冷启动+库加载 | 池常驻/内联笔记本复用（✅ pool-configurations） |
| shuffle 阶段倾斜 OOM | join 键热点 | 广播小表/加盐重分区（✅ apache-spark-performance） |
| 写出海量小文件 | 并行度×分区误配 | `repartition/coalesce` 目标文件尺寸（5.6 项 2） |
| 端点读同目录报 schema 不一致 | 漂移列 | 显式列定义+版本目录（5.4 摩擦项） |
| 包版本冲突 | 会话/池双源注入 | 单一声明源+锁版本（5.3） |

🔧 侧证补强：E4 的「谓词组剪枝=0」如实登记（03 章 3.7 同注）——布局不匹配时
Parquet 剪枝无戏可唱，上表第 3 行的文件布局纪律因此是**剪枝收益的前提**。

## 核心概念速览（中英对照）

- **Synapse 笔记本** — Synapse notebook：多语言单元格工作台，挂 Spark 池 ⚠️（✅ development-using-notebooks）。
- **Spark 池** — Spark pool：节点数×VM 规格的工作区算力，动态执行器 ⚠️（✅ pool-configurations）。
- **`%%sql` 魔法** — 笔记本内直达 SQL 端点 ⚠️。
- **落湖配方** — DataFrame→Parquet on ADLS：一次加工两处消费 ⚠️（README 特性句 ✅）。
- **列裁剪** — Column pruning：Parquet 按列读取的 IO/成本红利 ⚠️（🔧E4 量化）。
- **会话包管理** — Session/pool libraries：maven/PyPI 注入与版本固定 ⚠️。
- **无头执行** — Notebook run by pipeline：参数化、可调度是工程底线 ⚠️。
- **MLlib 管道** — Spark ML pipeline：特征→训练→评估笔记本闭环 ⚠️（✅ mllib-notebook）。

## 最新演进与工业实践

2022→2026（URL 均 ✅ 200；状态 ⚠️ 转述）：

- **Spark 池版本线推进**：本书时代以 Spark 2.4/3.1 为主，现行池支持 Spark 3.3/3.4/3.5
  多版本可选（✅ apache-spark-pool-configurations 现行版）；GPU 池已标注弃用
  （✅ toc 实抓 apache-spark-gpu-concept 标 deprecated——引用本书 GPU 内容先核对）。
- **Delta 默认化**：官方最佳实践把笔记本产出物导向 Delta/开放格式 + 统一 catalog 语义；
  Fabric 侧对应物为 Lakehouse（#218/#191 波内登记不链）。
- **工业实践**：「笔记本产线化」= 检查单 5.6 的制度化——小文件、分区布局、依赖固定三项
  最常见事故源；与 [../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md) 的表格式治理经验互认。
- 🔧 数字口径：E4/E2 为 DuckDB 1.5.5/SQLite 3.45.3 本机实测，只证列裁剪与 shuffle 代价
  的普适算术，**非 Synapse Spark 行为**；pyspark 本机不可装（零新装红线），未做伪实测。
