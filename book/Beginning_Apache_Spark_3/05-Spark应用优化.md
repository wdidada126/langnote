# 05 Optimizing Spark Applications（Spark 应用优化）

> 原书 Ch5，pp.183–219（37 页）。入门册的「优化」章注定是清单式的：分区、缓存、shuffle、内存、GC——每样给一个旋钮和一句原理，深度让位给 Ch4 的计划面。二级小节未实抓 ⚠️，主题簇按章题与官方 tuning 文档骨架推定；属**精读重构**。

## 5.1 优化的第一性：数据移动与重复计算 ⚠️

- 本章世界观（重构）：Spark 性能 = 少动数据（下推/裁剪/广播）+ 少算第二遍（缓存/物化复用）+ 别让一个任务干全组的活（分区均衡）。三条对应三节下文。
- 官方锚点：https://spark.apache.org/docs/latest/tuning.html（✅ curl 200）——本册该章可视为此文档的教学化压缩 ⚠️（对应关系推定）。

## 5.2 分区与倾斜 ⚠️

- 输入分区数由 split 规则决定（文件切片/`parallelism` 参数）；`repartition(n)` 全量洗牌、`coalesce(n)` 免 shuffle 缩分区——两个动作的代价差一个数量级，是入门者最常被烧的旋钮。
- 倾斜诊断面：stage 内 task 时长图「一根长尾」；处方面：加盐（salting）二次聚合、热点键单独广播处理、AQE 倾斜拆分（回读 `04`）。
- 对照盘上：倾斜与 shuffle 的中文教材展开在 [../bigdata/03-Shuffle与宽依赖.md](../bigdata/03-Shuffle与宽依赖.md)；权威版在 [../Spark_The_Definitive_Guide/10-生产部署与性能调优.md](../Spark_The_Definitive_Guide/10-生产部署与性能调优.md)——本册只给到「认识症状」层。

## 5.3 缓存与物化 ⚠️

- `cache()/persist(StorageLevel)`：MEMORY_ONLY 默认，序列化级别（MEMORY_AND_DISK_SER）换 CPU 换内存；`checkpoint()` 切断血缘换重算免疫——本册把 checkpoint 归入流式容错预备（Ch7 收费）⚠️。
- 判断标准只有一条：**这个中间结果会被读两次以上吗？** 一次性读取缓存 = 纯内存浪费；本册练习特意安排两种形态对照体验。
- 表格式层的兴起（Delta OPTIMIZE/Z-Order）已把「布局级优化」从会话内缓存挪到存储层 ⚠️ 演进见文末。

## 5.4 shuffle 面：数与形 ⚠️ + 🔧 E4

- 经验参数群（转述清单）：`spark.sql.shuffle.partitions`（默认 200，小数据场景 200×executor 的空 task 风暴）、`spark.shuffle.compress`、`spark.sql.adaptive.coalescePartitions.enabled`（AQE 兜底）——本册教「先调 partitions 再看 AQE」。
- 🔧 **实验 E4**（**非本书 Spark 引擎行为**；DuckDB 1.5.5 + SQLite 3.45.3）：同一形态的聚合问题（200k 行、97 个分组键值的 count+sum）——
  - SQLite：44.0ms，其查询计划为**排序聚合**形态（VDBE 指令面可见 `SorterOpen/SorterInsert/SorterSort`，即物化排序后流式分组）；
  - DuckDB：1.4ms，EXPLAIN 显示 `PERFECT_HASH_GROUP_BY`（分组基数已知小时直接开数组哈希）。
  - 同题 30 倍差，机制差异可迁移的直觉：**聚合算法选型（排序 vs 哈希）决定同题成本量级**——Spark 的 sort-based shuffle（写侧排序+读侧归并）与哈希聚合的组合，正落在同一设计空间里 ⚠️（Spark 侧 shuffle 机制转述官方文档，未本机测）。
  - 边界声明：两个单机引擎都没有网络层与 disk spill 压力面，本数字不可与 Spark shuffle 指标对比。

## 5.5 内存、序列化与 GC ⚠️

- 内存地图（3.x 口径）：统一内存管理下 execution/storage 互相借用，user memory 在顶；OOM 的三种死法：driver collect 过大、executor 执行内存爆、metaspace 代码生成类泄漏——本册各给一个反例 ⚠️ 主题簇推定。
- 序列化：Kryo 配置在 RDD 线仍有教、SQL 线基本免调（Tungsten 内存格式自带）；Python worker 的 Arrow 转换面（`spark.sql.execution.arrow.pyspark.enabled`）是 PySpark 用户唯一的「序列化优化」作业 ⚠️。
- GC：G1 默认后的时代修正——2021 教材还在讲 CMS 调参的部分今已作废，回读任何 GC 参数建议先对版本 ⚠️。

## 5.6 观测先行：UI/事件日志/度量 ⚠️

- 顺序教条：先看 stage/task 图 → 再看 SQL 页签的物理计划与 metrics（scan size、shuffle bytes）→ 最后才动参数。入门者反着来的居多。
- `spark.eventLog.enabled` + History Server 的离线回看；工业界 2024–2026 已普遍叠外部画像（云厂商托管 UI/OpenLineage）⚠️。
- 对照盘上可观测册：[../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md](../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md)。

## 5.7 本章练习视角（重构）⚠️

五连自查：① 同一 group-by 分别用 200 与 8 个 shuffle 分区跑，记录空 task 占比；② 缓存/不缓存复用型查询 A/B；③ 把 broadcast 阈值调到 1B 强制 SortMerge，观察 Exchange 数变化；④ 人为造一个热点键，验证加盐二次聚合；⑤ `collect()` 一张大表看 driver OOM 现场（本地小数据模拟，⚠️ 非集群实测）。

## 5.8 优化决策树（重构 ⚠️）

- 第一步永远是定位：哪个 stage 慢？它的时间花在 扫描 / shuffle / 计算 / GC 哪一块？（UI 的 task metric 四分法）
- 扫描慢 → 检查谓词/列裁剪是否生效（回 `03/04`）→ 文件格式与分区布局 → 小文件合并（回 `03` 缺口 → 表格式）。
- shuffle 慢 → 分区数是否 200×空转 → join 能否改广播 → 聚合能否两阶段（partial+final）→ 倾斜加盐。
- 计算慢 → UDF 审查（`04` E2）→ codegen 是否被打断（看 `*(n)` 段数）→ 数据是否被反序列化成对象（存储级别误用）。
- GC 慢 → 内存占比与存储级别 → 缓存滥用（5.3 的「两次以上」标准）→ executor 内存碎片化（K8s 场景另议）。
- 全都不显著 → 资源本身小了，加 executor 重跑对照——「先加钱验证假设，再花力气优化」。

## 5.9 参数速查卡（本册涉及的旋钮 ⚠️ 语义转述官方文档）

| 参数 | 管什么 | 常见误调 |
| --- | --- | --- |
| spark.sql.shuffle.partitions | 聚合/连接后并行度 | 无脑调大制造空 task |
| spark.sql.autoBroadcastJoinThreshold | 广播 join 尺寸上限 | 调到 0 等于自废 |
| spark.sql.adaptive.enabled | AQE 总开关 | 关掉再手调退回 2018 |
| spark.memory.fraction | 统一内存可借区占比 | 微操无益先动它 |
| spark.executor.memoryOverhead | 堆外/开销预算 | 不设导致 K8s OOMKill |
| spark.sql.files.maxPartitionBytes | 输入切片尺寸 | 小文件场景调它治标 |
| spark.eventLog.enabled | 历史回看数据底座 | 生产关闭等于裸奔 |

- 读法：本表是「旋钮语义」不是「旋钮取值」——取值永远是实验题；本目录因 Spark 不可装，不提供任何取值结论（红线）。

## 5.10 优化叙事的时代修正（重构 ⚠️）

- 本册优化章 = 会话内视角（2021）；2026 工业视角多了两层：
  - 存储层：表格式接管布局优化（小文件/聚簇/统计），作业内只做计算优化；
  - 平台层：自动调优（云厂商 advisor/autotuning）把 5.9 大半参数藏进产品——入门者学参数的意义变成「知道黑盒在调什么」。
- 不变的部分：定位优先（5.8 第一步）、数据移动第一性、倾斜与空 task 的形态识别——这三件是引擎代际间稳定的知识，也是本章真正的读值。
- 对照盘上：中文教材的优化章 [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md) 与本册同层；权威纵深 [../Spark_The_Definitive_Guide/10-生产部署与性能调优.md](../Spark_The_Definitive_Guide/10-生产部署与性能调优.md)；「单机镜像」语境见 [../DuckDB_in_Action/00-总览与阅读地图.md](../DuckDB_in_Action/00-总览与阅读地图.md)。

## 5.11 速自检与一行卡（答案在上文）

1. 优化第一性的三句话是什么？
2. repartition 与 coalesce 的代价差来自哪里？
3. 倾斜的「诊断-处方」两步各一句？
4. 缓存判断标准一句话？
5. checkpoint 与 cache 各自对付什么故障模型？
6. shuffle.partitions 默认值与空 task 风暴的关系？
7. 🔧 E4 中 SQLite 用什么算法做 group-by、DuckDB 用什么？倍数差多少？
8. E4 的结论能不能写成 Spark 数值？为什么？
9. 统一内存下哪两块可以互相借用？
10. 「先看 UI 再动参数」的三步顺序是什么？
11. 一行卡：`explain` 里的 `Exchange` = shuffle 边界；`*(n)` = codegen 段；`Coalesce`(AQE) = 运行期并区。
12. 一行卡：优化改动必须带对照组重跑，无对照的数字一律作废（本目录红线）。

## 5.12 优化黑话小词典（语境卡 ⚠️）

- 长尾（long tail）：stage 内个别 task 远慢于其余——倾斜的 UI 形态。
- 空转 task：无数据可读的调度单元，分区数过大的税。
- spill：执行内存放不下后落磁盘，OOM 与慢的双重前兆。
- 全表扫（full scan）：谓词没裁到文件/row group，`03` 裁剪机制失效的同义词。
- 小文件：分区×任务写出碎片，读端元数据开销爆炸——表格式 OPTIMIZE 的对象。
- 内存借调：unified memory 里 execution/storage 的互让规则。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 分区数 | Number of Partitions | 并行度与空 task 成本的双刃 |
| 重分区 | Repartition | 带全量 shuffle 的分区数/分布重排 |
| 并区 | Coalesce | 免 shuffle 的分区收缩 |
| 数据倾斜 | Data Skew | 键分布不均导致长尾 task |
| 加盐 | Salting | 热点键加随机前缀二次聚合 |
| 存储级别 | Storage Level | 缓存的内存/磁盘/序列化档位 |
| 检查点 | Checkpoint | 物化并切断血缘的容错手段 |
| 洗牌分区数 | shuffle.partitions | SQL 聚合/连接的默认并行度旋钮 |
| 统一内存管理 | Unified Memory Management | execution/storage 动态借用 |
| 空 task 风暴 | Task Overhead / Empty Task | 分区数远超数据量的纯调度浪费 |
| 事件日志 | Event Log | History Server 回看的数据底座 |
| AQE | Adaptive Query Execution | 运行期统计驱动的分区/计划自适应 |

## 最新演进与工业实践

- **AQE 吃掉半章旋钮（2021→2026）**：本册教的 shuffle.partitions 手调、倾斜 join 手工加盐，3.x+ AQE 已自动化大半（coalesce、skew join、运行时 join 转换）——2026 的优化教学序倒转为「先开 AQE 观测，再手工补刀」⚠️（官方文档口径）。
- **存储层优化接管布局问题**：小文件/聚簇/统计维护从会话内移交表格式：Delta `OPTIMIZE`+Z-Order、Iceberg 分区演化/`rewrite_table_files`（官方 https://docs.delta.io/latest/index.html ✅ 200）；盘上对位：[../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md)、[../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)。
- **成本治理新维度**：云按秒计费让「优化=省钱」成为 2024–2026 主轴（spot 实例、autoscaling、serverless Spark 如 Databricks Serverless/EMR Serverless ⚠️ 产品口径非实测）；本册的会话内调参叙事需要这层改写才合今日语境。
- **单机镜像实验的可迁移性**：本目录 🔧 E4 说明「聚合算法决定成本量级」这类机制直觉可以用 DuckDB/SQLite 免费建立；但 spill、网络、推测执行这些 Spark 特有代价，单机类比**系统性缺席**，须以 ⚠️ 官方文档补课。
