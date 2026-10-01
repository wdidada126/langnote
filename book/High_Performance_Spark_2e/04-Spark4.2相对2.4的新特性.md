# 04 Spark4.2相对2.4的新特性（Ch4: What's New in Spark 4.2 Since 2.4）

> 章题取证 ✅（终版目录第 4 章，2e **新增章**，草案无对应）；章内小节未获公开取证：⚠️ 本节清单为"按官方文档主题重建"，每条挂已验 200 的官方 URL 或标 ⚠️ 转述；不引未经 api.crossref.org 校验的 DOI。

## 0. 本章主线

这是一章**版本压缩饼干**：把 2.4（2018 末）到 4.2（取证时 2026-10 官方 latest＝4.2.0，✅ 实抓）之间约七年的性能相关增量，按"调优者需要知道的"切片。

- 读法三问（对每条新特性）：
  1. 默认开没开？（决定你是否已经在用它）
  2. 省的是哪类成本？（内存/IO/网络/CPU/人力）
  3. 把哪类老技巧作废了？（决定你该忘掉什么）
- 本章与 [03-Spark升级与迁移](03-Spark升级与迁移.md) 互为表里：那边讲"怎么安全过去"，这边讲"过去了得到什么"。

## 4.1 优化器与执行（作废手工技巧最多的区）

- **AQE（3.0 引入，后续默认开）**：
  - 运行时统计合并过多 shuffle 分区（治"默认 200 不适配"）；
  - 统计修正 Join 策略（小表误判不再一路错到底）；
  - 倾斜热分区自动拆分并行化；⚠️＋ https://spark.apache.org/docs/latest/sql-performance-tuning.html ✅
  - 作废技巧：手调 `spark.sql.shuffle.partitions` 一把梭。
  - 🔧 概念锚：E6（SQLite ANALYZE 前后计划翻转 39.9ms→0.0ms，**非 Spark**，详 [05-DataFrame与SparkSQL](05-DataFrame与SparkSQL.md)）。
- **whole-stage codegen 持续扩张**：算子覆盖与生成质量逐年提升；UDF 仍是打断代码生成的头号成本源。⚠️
- **Join Hint 家族**：BROADCAST/MERGE/SHUFFLE_HASH/SKEW 提示词——给"优化器不知道"的场景留后门，AQE 时代仍有席位。⚠️＋同上官方页 ✅
- **自动两阶段聚合、limit 下推、distinct 改写**：Catalyst 规则逐年加厚，手写技巧的存活空间持续收缩。⚠️

## 4.2 数据源与格式（IO 成本重分配区）

- **DSv2（Data Sources API v2）成熟**：
  - 新格式（Paimon/Iceberg/Delta 连接器）绕过 Hive 老接口接入；
  - 谓词/列/分区三级下推标准化——"分区裁剪"从目录约定升级为接口契约。⚠️
  - 湖仓侧展开：../Use_Iceberg_with_Spark/05-演化与隐藏分区.md。
- **Variant 类型（4.0+）**：半结构化数据的二进制列式表示，替代"JSON 字符串＋解析 UDF"的高成本套路；schema-on-read 第一次有了引擎级一等公民。⚠️
- **压缩编解码扩展（zstd 等）与 CSV/JSON 读写优化**：落盘与 shuffle 的"压缩比×CPU"再平衡。⚠️＋ https://spark.apache.org/docs/latest/tuning.html ✅
- **Parquet/ORC 向量化读持续调优**：列式批读＋延迟物化是 SQL 吞吐基本盘。🔧 单机已见 24 倍（E4，非 Spark）。
- 中文格式谱系互证：../bigdata/09-存储与文件格式.md。

## 4.3 资源与部署

- **K8s 从实验到成熟**：executor pod 模板、driver-on-K8s、动态分配组合拳。⚠️＋ https://spark.apache.org/docs/latest/running-on-kubernetes.html ✅
- **语言运行时门槛整体上移**：Scala 2.12→2.13 双支持再到默认、JDK 11/17 线、Python 3.x 收敛——升级章的姊妹事实，逐项以 https://spark.apache.org/downloads.html ✅ 的当版说明为准。⚠️
- 小文件/元数据治理并入表格式维护作业（非引擎主线，见 Iceberg 线目录）。

## 4.4 编程面与生态

- **PySpark 成为主力入口**：pandas API on Spark（批量 Arrow 通道）、Koalas 收编——语言税大幅下降但 UDF 仍是坑（09 章算总账）。⚠️
- **Spark Connect（4.0+）**：客户端/服务端 gRPC 协议，进程与版本解耦，多语言与云托管的地基。⚠️
- **Structured Streaming 增量演进**：watermark/状态语义与恢复能力改进、流式入湖成熟；详版 API 在 ../Spark_The_Definitive_Guide/09-结构化流处理.md。⚠️＋ https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html ✅
- **ML 管道统一**：RDD 路线 MLlib 进入退场通道（[11-MLlib与机器学习管道](11-MLlib与机器学习管道.md)）。⚠️＋ https://spark.apache.org/docs/latest/ml-guide.html ✅

## 4.5 关于 4.1/4.2 的诚实边界（重要）

- 本章题点名"4.2"，但 **4.1/4.2 的逐条 changelog 本轮取证未成功**：官方 releases 专页抓取 404/网络受限；`docs/latest` 页头仅能确认当前版本号 **4.2.0**（✅）。
- 故 4.x 小版本增量只给方向性登记（AQE 打磨、Connect/Variant 完善、ML 函数面扩张）——**不作逐条断言、不臆写清单**；请以 https://spark.apache.org/downloads.html ✅ 与官方 release notes 为唯一权威。
- 同理，草案中译（2022 年基线）与终版（4.2 基线）之间必然存在本清单未覆盖的新条目，⚠️ 属取证缺口而非内容遗漏。

## 4.6 特性→作废技巧 对照表

| 新特性 | 作废/降权的 2.4 时代技巧 | 残留适用场景 |
|---|---|---|
| AQE 分区合并 | 手调 shuffle.partitions | 极窄作业固定并行度 |
| AQE 策略切换 | 猜大小设广播阈值 | 统计长期失真的外表 |
| SKEW hint | 手工 salting | 超热键+广播兜底 |
| DSv2 下推 | 预过滤中间表 | 非 pushdown-safe 函数 |
| Variant | JSON 字符串列＋get_json_object UDF | 强 schema 化场景转列 |
| pandas API | 全量 toPandas 单机玩 | 真·单机小样本 |

## 4.7 小结自检

1. AQE 三件套各自替代了哪个 2.4 时代手工参数？
2. DSv2 为什么是湖仓格式爆发的技术前提？
3. Variant 取代的是哪种"土办法"，省掉的钱花在哪？

## 核心概念速览（中英对照）

- **AQE** — Adaptive Query Execution：运行时统计驱动的合并/换策略/拆倾斜三件套，3.x 默认化的优化分水岭。
- **DSv2** — Data Source API v2：三级下推标准化的数据源接口，湖仓格式的现代入场券。
- **向量化读** — Vectorized reader：Parquet/ORC 列式批读路径，吞吐基本盘。
- **Variant** — 半结构化二进制类型：4.0+ 的 schema-on-read 一等公民，替代 JSON 字符串＋解析。
- **whole-stage codegen** — 全阶段代码生成：算子融合成单 JVM 循环，UDF 打断它。
- **Join hints** — 连接提示：BROADCAST/SKEW 等后门，优化器信息不足时人工补位。
- **pandas API on Spark** — PySpark 列式通道：Arrow/批式执行缩小 Python 语言税。
- **Spark Connect** — 客户端-服务端架构：gRPC 解耦客户端语言与引擎版本。
- **zstd** — 通用压缩编解码：shuffle/落盘压缩选项扩展代表。
- **watermark** — 事件时间水位线：流式状态清理与迟到容忍的节拍器。
- **pushdown** — 谓词下推：DSv2 契约化的过滤前置，E3 裁剪的上层叙事。

## 最新演进与工业实践

- **版本锚点**：本册取证（2026-10）`docs/latest`＝ **Spark 4.2.0**（✅）；4.x 系列处于"Connect/Variant/ML 函数"新范式铺开期。⚠️（逐条以官方 release notes 为准，见 §4.5 边界声明）
- **工业现状**：在产集群主力分布 3.x 中后期至 4.0 早期；"2.4 存量"仍是教材级市场——本章与 03 章共同解释 2e 的时代价值。⚠️ 行业观察。
- **Photon 类原生引擎潮流**：商业发行版以原生向量化引擎替换 JVM 路径，开源主线以 codegen＋向量化读跟进；Photon 相关论文/博客本轮 Crossref 检索与 URL 验证未获正果，⚠️ 只作系统名叙述不引文献。
- **可复现锚**：本章四条 ⚠️ 转述均有官方文档 URL 兜底（sql-performance-tuning / running-on-kubernetes / ml-guide / structured-streaming-programming-guide / downloads 五页本轮 200 ✅）。
- **文献锚（过 Crossref 200）**：Spark SQL（SIGMOD 2015，DOI 10.1145/2723372.2742797 ✅）——自动化优化器路线的宣言书；2.4→4.2 的全部演进都是这条路线的延长线。
