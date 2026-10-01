# 07 · Spark 应用优化与调优

> 原书第 7 章（Optimizing and Tuning Spark Applications）。章骨架 ✅ 按 ApacheCN 全译镜像实抓还原：查看/设置配置／为大规模负载扩展 Spark（静态 vs 动态资源分配、executor 内存与 shuffle service）／最大化并行度／缓存与持久化（cache()/persist()、何时缓存、何时别缓存）／Spark 连接家族（广播哈希连接及其适用、洗牌排序合并连接及其优化与适用）／Spark UI 各页签之旅（Jobs/Stages、Executors、Storage、SQL、Environment）／调试 Spark 应用。Spark 行为 = ⚠️ 转述 + 官方文档（https://spark.apache.org/docs/latest/tuning.html ✅、https://spark.apache.org/docs/latest/configuration.html ✅、https://spark.apache.org/docs/latest/sql-performance-tuning.html ✅ 均 curl 200）。调优是本书"把第 2 章 UI 前置"的兑现章。

## 7.1 资源面：分配模型与内存布局

- **静态 vs 动态分配**：`spark.dynamicAllocation.enabled`（需 shuffle service 配合，executor 随积压扩缩）；YARN 时代默认叙事；
- **executor 规格口诀**（书中取向）：少而大 vs 多而小的权衡——内存池利用、GC 停顿、HDFS 客户端数三变量的折中；`--executor-memory/--executor-cores` 与堆内（执行/存储/用户缓存三区）+ 堆外开销（⚠️ unified memory 模型转述，细节以官方 configuration 页为准）；
- **External Shuffle Service**：动态分配下 shuffle 数据外置的生命线。

## 7.2 并行度：分区是第一变量

- 目标粒度：每分区约 100–200MB 社区口径（⚠️ 转述）；
- 入口三把刀：读源并行度（文件切片/JDBC 四件套）、`repartition(n)`（全量重洗）、`coalesce(n)`（收窄不下 shuffle）；
- **小文件与过度分区**是并行度滥用的两个对称病灶（回收第 4/5 章预埋）；
- `spark.sql.shuffle.partitions`（默认 200，3.x 前被吐槽最多的魔法数）。

## 7.3 缓存与持久化：cache/persist 的经济学

- `df.cache()`=MEMORY_AND_DISK 简写；`persist(StorageLevel...)` 全谱（MEMORY_ONLY/_AND_SER/_DISK_ONLY/OFFHEAP，⚠️ 官方 rdd 页词表）；
- **何时缓存**：多次复用、探索期脏活、join 热点侧；**何时别缓存**：只用一次、写后不再读（action 只是 sink）、内存挤压引发 spill 连锁——书用专门小节泼冷水；
- `unpersist` 与 Storage 页签的落盘核对；
- 与 AQE 关系：3.0 后部分"为 join 手动 cache"的旧仪式失效（演进节）。

🔧 **物化 vs 惰性实测类比（非本书 Spark 引擎行为，meas.txt G6 组）**：DuckDB 300 万行表 `GROUP BY` 结果：视图路径首读现场算 17.8ms；物化路径建表 391ms、复读 0.63ms——"缓存=一次性物化成本换多次复读收益"的盈亏平衡 ≈ 复读 25 次。把 `persist` 决策变成算术，是本目录给的替代直觉。**Spark 的 StorageLevel/内存外溢行为不可本机实测，全部 ⚠️ 转述。**

## 7.4 连接家族（本章技术心脏）

⚠️ 转述（官方 sql-performance-tuning 页同族）：

| 策略 | 机制 | 适用/失效边界 |
| --- | --- | --- |
| Broadcast Hash Join (BHJ) | 小表整发上广播，零 shuffle | 小侧超 `autoBroadcastJoinThreshold`（默认 10MB）即退化；广播本身打满 driver 内存是经典事故 |
| Shuffle Sort Merge Join (SMJ) | 双侧重分区+排序+归并 | 大×大的默认主力；倾斜键炸（单 reducer 过载）；`spark.sql.shuffle.partitions` 影响其成本 |
| Sort Merge Bucket Join | 双方按同桶键预排 | 需两表同分桶（第 5 章 bucketBy 回收） |
| Shuffle-and-Replicate NLJ | 小表复制交叉 | 兜底，几乎总是坏消息 |

- 手动干预三件套：`BROADCAST()` hint（书时代）、`REPARTITION` hint、cache+bucket；3.0 后让位 AQE（第 12 章）；
- 倾斜三板斧：加盐打散热点键、热点单独广播、`skewJoin`（3.0 自动，书稿收尾时刚出生——2e 的"-preview2"注脚）。

## 7.5 Spark UI 页签之旅 + 调试

- **Jobs/Stages**：找最长 Stage、看 task 时长分布（倾斜的直观指纹）；**Executors**：各 executor GC 时间/内存水位不均=数据倾斜或坏节点；**Storage**：缓存是否真落地、剩余内存；**SQL 页签**：逻辑/物理计划树 + 节点级指标（本书把 SQL tab 单独成节是 2e 特色）；**Environment**：生效配置对账（"你以为的默认值"坟场）；
- 调试节给的清单：`explain()` 三种模式（cost/formatted/extended）、eventLog/History Server、异常栈的 driver/executor 两侧定位、`spark.sql.adaptive.enabled` 开与关的 A/B 习惯（3.0 语境）。

🔧 **物理计划对照实测类比（非本书 Spark 引擎行为，meas.txt G4 组）**：DuckDB 对 join+group 查询 `EXPLAIN` 输出 `HASH_JOIN → HASH_GROUP_BY → SEQ_SCAN`——与 Spark SMJ 对照可见**同问题不同解**：单机选择 hash 全家桶（内存充裕无网络），Spark 必须回答"数据在哪些分区、要不要洗"（shuffle 是它的税）。用 DuckDB 计划树练"读执行计划"的手感，再迁移到 Spark SQL tab（⚠️ Spark 侧仅文档转述）。

## 7.6 工程判断（重构观点）

本章把调优从"玄学参数表"拉回**三问结构**：数据怎么分区？重分布（shuffle）能不能免？结果值不值得物化？——2026 年 AQE/向量化吃掉了大量手活，但三问仍是面试与事故复盘的骨架。书里"何时别缓存"的克制与"UI 先行"的取证习惯，是它比同期资料更像教材的地方。

## 7.7 章小节骨架总览（✅ 镜像实抓逐节对账）

| 原书小节（回译） | 本文件对应 |
| --- | --- |
| 优化和调整 Spark 的效率（总起） | 7.6 三问结构 |
| 查看和设置 Apache Spark 配置 | 7.1 + Environment 页签 7.5 |
| 为大规模工作负载扩展 Spark：静态与动态资源分配／配置执行器内存和洗牌服务 | 7.1 |
| 最大化 Spark 的并行性 | 7.2 |
| 数据的缓存和持久化：DataFrame.cache()／DataFrame.persist()／何时缓存和持久化／何时不要 | 7.3 |
| Spark 连接家族：广播哈希连接（及其何时使用）／洗牌排序合并连接（优化／何时使用） | 7.4 表 |
| 检查 Spark UI：通过页签的旅程（作业与阶段／执行者／存储／SQL／环境） | 7.5 |
| 调试 Spark 应用程序 | 7.5 末段 |

## 7.8 重建示例：调优取证清单（本目录重做；⚠️ 参数名以官方 configuration/sql-perf 页为准）

```text
事故复盘五步（每步先看数再动手）：
1 哪类作业慢？        SQL tab 看计划树最长的节点（scan? exchange? agg?）
2 慢在数据量还是分布？ task 时长分布 p50/p95/p99——p99>>p50 ⇒ 倾斜
3 shuffle 多大？       Stage Metrics 的 shuffle read/write bytes；分区数够否
4 广播划算吗？         小侧行数×行宽 vs autoBroadcastJoinThreshold(10MB 默认)
5 物化值不值？         复读次数 ≥ 2 且内存有余 ⇒ cache；否则让 AQE 合区
```

```python
# 三个最常改的旋钮（示例仅语义存档，零执行）
spark.conf.set("spark.sql.shuffle.partitions", 400)     # 手动时代（<3.0 默认叙事）
spark.conf.set("spark.sql.adaptive.enabled", "true")     # AQE 总闸（3.2+ 默认开）
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
df = df.repartition(64, "country")                        # 只在大表 join 前显式重分布
```

🔧 侧证三组（全部"非本书 Spark 引擎行为"）：G6 缓存盈亏算术（7.3）、G4 计划树对照（7.5 末）、G1 "推断=全扫成本"（第 4 章，与 7.2 读并行度联动）。

## 7.9 课堂问题（答不出回本文件）

1. 动态分配为什么必须配 external shuffle service？
2. coalesce(1) 救小文件的代价是什么？何时反而该 repartition？
3. BHJ 的"小表"由谁判定？3.0 后判定权移交给谁（12 章回收）？
4. SMJ 倾斜炸的指纹在 UI 哪一页、哪个指标？
5. "何时别缓存"三条各举一反例。
6. explain 三模式分别给谁看（调试对象：人/优化器/成本）？

### 调优清单（速记）

- 先看 UI 的 Stage DAG 与 task 时长分布，再决定改分区数还是改 join 策略。
- shuffle 是多数瓶颈的来源：广播阈值、加盐、map-side combine 都围绕它展开。
- 小文件问题优先于算子问题：读侧 merge 与写侧 coalesce 是两个不同动作。
- 缓存要算内存账：MEMORY_AND_DISK 与 MEMORY_ONLY 的差别在溢出行为。
- AQE 相关开关在 3.0 前不存在；本章按 2.4/3.0-preview 口径转述（⚠️ 未本机验证）。
- 倾斜 key 先采样定位（如 count 按 key 分布），再决定广播或加盐。

## 核心概念速览（中英对照）

- **动态资源分配** — Dynamic Allocation：按积压扩缩 executor，依赖 shuffle service。
- **统一内存模型** — Unified Memory Management：执行/存储区互借（⚠️ 转述）。
- **repartition / coalesce** — 全量重洗 / 无 shuffle 收窄。
- **shuffle.partitions** — 聚合后并行度默认 200 的旋钮。
- **persist / StorageLevel** — 物化缓存与级别全谱。
- **BHJ** — 广播哈希连接：小表复制、零 shuffle。
- **SMJ** — 洗牌排序合并连接：大表 join 主力。
- **数据倾斜** — Skew：单键过载；加盐/单独广播/自动 skewJoin 三治。
- **BROADCAST hint** — 计划干预：强制广播。
- **explain** — 三模式计划打印（extended/cost/formatted）。
- **Spark UI SQL tab** — 计划树 + 节点指标取证面。
- **eventLog/History Server** — 事后取证链路。

## 最新演进与工业实践

- **AQE 成为默认**：Spark 3.0 引入自适应执行（动态合分区、自动倾斜处理、join 策略运行时改选——第 12 章主场），**3.2 起默认开启**、3.5/4.0 持续增强（⚠️ 转述 + https://spark.apache.org/docs/latest/sql-performance-tuning.html ✅）；本章手动 hint 学大半退休，"小文件合并"由 `advisoryPartitionSizeInBytes` 接管。
- **向量化/代码生成**：Parquet 向量化读（3.0 起）与整段 codegen 是开源侧主力；商业 Photon（SIGMOD 2022，DOI `10.1145/3514221.3526054` ✅ Crossref，论文线挂 [../../db/db.md](../../db/db.md)）把表达式执行搬进原生向量化引擎。
- **观测升级**：Spark UI 在 3.3+/4.x 重做（新 SQL 页签火焰图式视图，⚠️ 转述未逐屏核验）；Prometheus sink + OpenTelemetry 路线成为生产标配（官方 monitoring 文档线）。
- **K8s 弹性**：executor 动态分配在 K8s 有原生对应（Spark Operator 的 dynamic allocation，⚠️ 转述）。
- **对读**：shuffle 机制与宽依赖的底层叙述见 [../bigdata/03-Shuffle与宽依赖.md](../bigdata/03-Shuffle与宽依赖.md)；中文调优实战坑录见 [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)；TDG 的部署调优纵深见 [../Spark_The_Definitive_Guide/10-生产部署与性能调优.md](../Spark_The_Definitive_Guide/10-生产部署与性能调优.md)。
