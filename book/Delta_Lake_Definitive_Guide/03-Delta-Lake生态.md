# 第 4 章 深入 Delta Lake 生态

> 原书第 4 章「Diving into the Delta Lake Ecosystem」。本文件按「**引擎 × Catalog × 接入器 × 跨格式**」
> 四个象限整理生态图景，并标注 2026 年的口径变化（UC 开源、Iceberg REST 蚕食 catalog 层）。
> 所有配置/代码为**自拟教学示意，非书中原文**。机制口径参照 delta.io connectors 文档与各引擎官方文档。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 4.1 引擎象限 | Spark/Databricks 本位 + Trino/Presto/Flink/Hive 旁路 | 读生态成熟，写生态以 Spark/Databricks 为主 |
| 4.2 Catalog 象限 | HMS/Glue/UC/Polaris 等 | 表格式与 catalog 是两层，选型别混 |
| 4.3 接入器 | Kafka Connect sink、Airbyte、Fivetran/Debezium 路线 | 「CDC 进湖」的管道清单 |
| 4.4 UniForm | 一份数据同时暴露 Delta/Iceberg/Hudi 元数据 | 化解「格式站队」的折中 |
| 4.5 云厂商发行版 | EMR/Dataproc/Synapse/阿里云 EMR 支持度 | Delta 已不只是 Databricks 的 |
| 4.6 delta-rs 与社区 | Rust 原生实现、Python 绑定、Kernel | 非 JVM 世界的入口（衔接第 6 章） |

## 核心精讲

### 4.1 引擎象限：谁能读、谁能写

| 引擎 | 读 | 写 | 机制要点 |
| --- | --- | --- | --- |
| Spark/Databricks | ✅ 全功能 | ✅ 全功能 | delta-spark 一等公民 |
| Trino/Presto | ✅ | ✅（INSERT/UPDATE/DELETE/MERGE 受版本限制） | delta-connector 按 commit 重建快照；DV 需较新版本 |
| Flink | ✅ | ✅（append/upsert 经 sink v2） | 由 delta-connector-flink 维护，流式语义见其文档；成熟度弱于 Spark |
| Hive | ✅ 只读（LLAP 时代遗产） | ⚠️ 不建议 | Hive input format 直读 parquet + 日志解析，DDL 能力弱 |
| Impala/StarRocks/Doris/ClickHouse | 部分 ✅ | ❌/旁路 | 各自以外部表/catalog 方式接入，能力子集 |

- **心智模型**：Delta 的能力 = 协议（PROTOCOL.md）+ 各引擎实现的支持矩阵。
  用非 Spark 引擎前，先查该引擎文档的「Delta Lake 支持级别」表——**协议允许 ≠ 连接器已实现**。
- DV、column mapping、CDF 这类新 writer feature 会**提升 minReaderVersion/minWriterVersion**，
  旧连接器遇到高协议版本直接拒读——生态兼容的真正机制是 protocol negotiation。

### 4.2 Catalog 象限

```text
表格式（Delta 日志）解决「一张表内部的事务」
catalog 解决「有哪些表、表在哪、schema 快照」
```

| Catalog | 形态 | 备注 |
| --- | --- | --- |
| Hive Metastore | OSS 事实标准 | Delta 默认 `org.apache.spark.sql.hive...` 兼容路径 |
| AWS Glue | 云托管 | EMR/Databricks 均可作 catalog backend |
| Unity Catalog | Databricks → 🔧 2024-06 开源（含 REST） | 治理下沉到 catalog 层（第 12 章） |
| Polaris/Gravitino | Iceberg REST 阵营 | 与 Delta 互操作依赖 UniForm/REST 扩展 |

⚠️ 2024 书稿的口径是「UC=商业治理平台」；2026 年 UC 开源 + Iceberg REST 成为跨格式 catalog 接口事实标准，
catalog 层之争比表格式层更激烈——读本章时把「生态」理解为「格式协议 + catalog 协议」双栈。

### 4.3 接入器：数据如何进湖（衔接 CDC 章）

- **Kafka Connect Delta Lake sink**（databrickslabs 开源）：把 topic 按微批写入 Delta，
  自带 schema 演化、` MERGE` 模式（可配 primary key 去重）——低代码 CDC 入口。
- **Debezium/Flink-CDC → Kafka → sink** 与 **直连 MERGE** 是两条路线，对比见 `10` 文件。
- **Airbyte/Fivetran**：SaaS 抽取 → Delta staging；书中 medallion 的 bronze 层常见来源。
- **delta-kafka / Spark Structured Streaming 的 Kafka source**：更灵活但要自己管 offset/乱序（第 7 章）。

### 4.4 UniForm（Universal Format）

```text
                 ┌─ _delta_log/         （Delta 引擎读）
一份 parquet 数据 ┼─ ICEBERG_METADATA/   （Iceberg 引擎读）
                 └─ HUDI_METADATA/       （Hudi 引擎读）
```

- 原理：写入仍是 Delta 事务，提交时**顺带生成 Iceberg/Hudi 元数据镜像**
  （`delta.universal.formats.enabled` 类选项，OSS 3.1+ 预览、🔧 4.0 GA 方向）。
- 意义：数据物理只存一份，「消费方引擎要 Iceberg」不再逼迫重写管道；
  限制：早期不支持 DV/某些 writer feature（被镜像的语义子集较小），以 delta.io UniForm 文档为准。
- 与 Hudi OneHoodie、Iceberg「多查询引擎」路线同向：**格式战争正在以元数据互读收场**。

### 4.5 云厂商发行版（2024→2026 口径）

- **EMR**：Delta 作为 attach 组件；**Dataproc**: image 内置可选；**Azure Synapse**: 原生 Delta 支持较深（含内部格式兼容）。
- **阿里云 EMR Serverless Spark** 等也提供使用 Delta 的官方用例（help.aliyun.com 用例文档可查）。
- Databricks 仍是功能首发地（liquid、DV、managed table 都是先 DBR 后 OSS）。

### 4.6 delta-rs 与社区实现

- **delta-rs**：Rust 原生读（写能力逐步完善），Python 绑定 `deltalake` PyPI——
  Polaris/DuckDB/自定义引擎经它访问 Delta；checkpoint 处理、时间旅行 API 都有。
- **Delta Kernel**（Java/C）：官方「引擎构建件」，把协议解析做成库——第 6 章主场。
- 生态判断：**协议文档化 + 多语言实现 = 表格式活了；私有库 + 单引擎 = 产品**。Delta 走的是前者。

## 版本演进

| 时间 | 事件 |
| --- | --- |
| 2021 | Trino/Presto 连接器进 delta 仓库（原 standalone 项目收编） |
| 2022–2023 | Kafka Connect sink、Flink connector 活跃；UniForm 预览（3.1） |
| 🔧 2024-06 | Unity Catalog 开源（含 REST catalog） |
| 🔧 2025 | Delta 4.0：统一元数据让 UniForm 转正式能力 |

## 文献与文档

- delta.io「Delta Lake Connectors / UniForm」文档页。
- Trino docs「Delta Lake connector」；Apache Flink Delta Connector 仓库 README。
- Kafka Connect Delta Lake sink：databrickslabs/delta-connect GitHub。
- Unity Catalog 开源公告（databricks.com blog, 2024-06）。
- delta-rs：github.com/delta-io/delta-rs。

## 常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「协议支持 = 所有引擎都能读写」 | 连接器能力是协议子集；DV/column mapping 会抬高 reader 要求 |
| 2 | 「catalog 和表格式是一回事」 | 两层解耦（4.2）；「我用了 UC」不代表「我用了 Delta」 |
| 3 | 「用 UniForm 就无损」 | UniForm 镜像的 writer 特性子集有限；跨格式消费前核对支持表 |
| 4 | 🔧 「Delta 只能在 Databricks 跑」 | EMR/Dataproc/Synapse/自建 Spark + delta-rs/Trino 组成完整非 Databricks 栈 |

## 与其他章 / 其他书的联系

- ← `01`：1.4 竞品坐标的展开。
- → `05`：Kernel/delta-rs 从「生态组件」升级为「构建材料」。
- → `11`：catalog 之争的治理面（UC/血缘）。
- → [../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)：Kafka/Debezium 管道上游。
- → [../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)：多引擎并存的由来。
- → 《Engineering Lakehouses with Open Table Formats》精读：**待建**（该书主题即本章的多格式生态）。
