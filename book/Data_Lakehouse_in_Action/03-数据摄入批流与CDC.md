# 03 · 数据摄入：批、流与 CDC

> 目标书：《Data Lakehouse in Action》（Pradeep Menon，Packt，2022-03）。
> ⚠️ 重建声明：章界推定（见 00）；"ingest"为官方简介六动词之首（✅ 简介原文），
> 本章按 2022 年 Azure 语境 + 通用摄入工程重构，平台细节标 ⚠️。

## 1. 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| §1 | 摄入模式四分法 | 文件批、数据库复制、事件流、API 拉取，四条管道三种幂等难题 |
| §2 | 批摄入的工程骨架 | 清单表 + 分区落位 + 重放窗口 |
| §3 | CDC：把 UPDATE 搬进不可变文件 | 日志挖掘 vs 查询式，去重键是灵魂 |
| §4 | 流摄入与新鲜度预算 | exactly-once 的三段责任划分 |
| §5 | 落到湖仓表 | 追加、MERGE、分区覆盖三种写法的选择 |
| §6 | 本书语境的 Azure 摄入件（⚠️） | ADF/Synapse Pipelines/Event Hub/IoT Hub 一览 |

## 2. 摄入模式四分法（§1）

```
 源系统                传输                落湖姿势
┌──────────┐   ┌──────────────┐   ┌────────────────────┐
│ 业务DB   │→ │ 快照导出(全/增)│→ │ 文件→Bronze 分区   │  批
│ 业务DB   │→ │ CDC日志挖掘    │→ │ MERGE→Silver 主键表│  准实时
│ 事件/日志│→ │ Kafka/EventHub │→ │ 流式追加/小文件治理│  流
│ SaaS API │→ │ 轮询拉取       │→ │ 增量水位+去重      │  批
└──────────┘   └──────────────┘   └────────────────────┘
```

| 模式 | 幂等靠什么 | 典型事故 |
| --- | --- | --- |
| 全量快照 | 分区级覆盖（overwrite by partition） | 快照不原子的"半份数据" |
| 增量批次 | 批次号水位表 + 主键去重 | 时钟漂移导致水位漏采 |
| CDC | 主键 + 版本号/LSN 排序合并 | 乱序更新回写旧值 |
| 事件流 | 事件 ID 去重 + 提交原语 | 小文件风暴（→ 04 章 🔧E5） |

## 3. CDC 机制速览（§3，✅ 各官方文档口径）

- **日志挖掘**（Debezium/GoldenGate 类）：读事务日志，对源库零压力，拿到事务内有序变更；
  难点是 DDL 漂移与日志保留窗口。
- **查询式**（时间戳/自增列轮询）：实现简单，但抓不到物理删除、对源库有读压。
- **落湖侧承接**：Hudi 把 CDC 做成一级公民（`_hoodie_commit_seqno` 排序合并 ✅
  <https://hudi.apache.org/docs/next/concepts>）；Paimon 以 LSM 主键表原生承接 Flink
  CDC 流（✅ <https://paimon.apache.org/docs/master/primary-key-table/table-mode/>）。
- 盘上纵深（互链）：
  [../Apache_Hudi_Definitive_Guide/03-写入Hudi.md](../Apache_Hudi_Definitive_Guide/03-写入Hudi.md)、
  [../Apache_Paimon_Streaming_Lakehouse/11-Flink集成与CDC入湖实践.md](../Apache_Paimon_Streaming_Lakehouse/11-Flink集成与CDC入湖实践.md)、
  [../Engineering_Lakehouses_with_Open_Table_Formats/10-增量管线与CDC.md](../Engineering_Lakehouses_with_Open_Table_Formats/10-增量管线与CDC.md)、
  [../Introduction_to_Apache_Flink/00-总览与阅读地图.md](../Introduction_to_Apache_Flink/00-总览与阅读地图.md)（流式语义的理论底座）。

## 4. exactly-once 的三段责任（§4）

端到端"不重不丢"不是某组件的属性，而是三段各自履约的合取：

1. **源→传输**：可重放日志（Kafka/Event Hub offset 语义）——消费位点由谁存？
2. **传输→湖**：微批/流式提交与检查点原子对齐（Flink checkpoint ↔ Delta/Iceberg 提交协议
   的两阶段耦合 ⚠️ 各家实现细节转述）。
3. **湖内**：即使上游重放，MERGE 去重键兜底（§3 排序合并）——"传输层保证不重，
   存储层保证重放无害"是双保险设计。

- 教学示意：重放风暴下，第 2 段失败退化为 at-least-once，第 3 段决定最终一致性——
  **去重键质量 > 传输承诺**。
- 盘上对位：[../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)、
  [../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md)
  （Wave-1 已在盘的流处理理论册——exactly-once 章给出两阶段提交的完整证明视角）。

## 5. 落湖三写法与选择（§5，⚠️ Spark SQL 语法形态为文档口径，本机未跑）

| 写法 | SQL 形态（示意） | 适用 | 代价 |
| --- | --- | --- | --- |
| 追加 | `INSERT INTO bronze PARTITION(dt) SELECT …` | 事件/日志类只增表 | 无界增长→ compaction 压力 |
| 分区覆盖 | `INSERT OVERWRITE … partitionOverwriteMode=dynamic` | 日批回刷幂等 | 整分区重写放大 IO |
| 合并 | `MERGE INTO silver USING batch ON key WHEN MATCHED …` | 主键表 CDC/SCD1 | 冲突语义与排序依赖（→ 02 章 🔧） |

```
选择树：有业务主键？ ─否→ 追加
              │是
      更新会迟到/乱序？ ─否→ 简单 MERGE
              │是
      按(主键,版本)排序合并（Hudi/Paimon 内建；Delta/Iceberg 靠 MERGE 条件手写）
```

- 纵深：[../Delta_Lake_Up_and_Running/03-表操作与数据变更.md](../Delta_Lake_Up_and_Running/03-表操作与数据变更.md)
  （MERGE 歧义的 sqlite 迷你复现）、
  [../Use_Iceberg_with_Spark/03-数据读写与MERGE-INTO.md](../Use_Iceberg_with_Spark/03-数据读写与MERGE-INTO.md)。
- SCD2（拉链）作为 CDC 落湖的高频下游模式 →
  [../Delta_Lake_Definitive_Guide/10-设计模式-CDC与SCD.md](../Delta_Lake_Definitive_Guide/10-设计模式-CDC与SCD.md)。

## 6. 本书语境的 Azure 摄入件（§6，⚠️ 2022 快照，全部未实测）

| 组件 | 角色 | 2026 状态（⚠️ 转述） |
| --- | --- | --- |
| Azure Data Factory | 编排式复制/映射数据流 | 仍在，被 Fabric Dataflows 分流 |
| Synapse Pipelines | ADF 内嵌于 Synapse 的形态 | 随 Synapse 叙事降温（→ 11 章） |
| Event Hub / IoT Hub | 高吞吐事件接入（Kafka 协议兼容） | 稳定 |
| Stream Analytics | 轻量流加工入湖 | 稳定 |
| Synapse Spark | 落湖主力引擎 | → 05/09 章 |

✅ Azure 平台总口径（湖仓视角）：<https://learn.microsoft.com/en-us/azure/databricks/lakehouse/>。
注：本节产品矩阵在 2026 已由 Microsoft Fabric 重排，盘上实况见
[../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md](../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md)——
读本书第 9 章前先对表，避免按 2022 SKU 做 2026 选型。

## 7. 常见误区

| 误区 | 修正 |
| --- | --- |
| "上了 Kafka 就 exactly-once" | 三段缺一即降级（§4）；湖侧无去重键则重放必脏 |
| "CDC 抓删除只能靠日志挖掘" | 查询式可用软删标记/定期对账补漏（⚠️ 实务通识） |
| "Bronze 层也要 MERGE 清洗" | Bronze 只追加原样存；清洗下沉 Silver（§5 表，medallion 纪律） |
| "小文件是存储问题" | 是摄入节拍问题：提交频率×并行度=文件数（→ 04 章 🔧E5 的量化） |
| "API 拉取不需要水位表" | 无水位=每轮全量；SaaS 限速场景直接不可用 |
| "摄入管道出事先查代码" | 先查清单表/水位表/批次号——三表定责快于读逻辑 |

## 与其他章 / 其他书的联系

- 摄入节拍的存储端代价 → [04-存储层对象存储文件格式与分区.md](04-存储层对象存储文件格式与分区.md)
- 流式语义理论 → [../Introduction_to_Apache_Flink/00-总览与阅读地图.md](../Introduction_to_Apache_Flink/00-总览与阅读地图.md)、
  [../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md)
- 湖内事务与冲突 → [02-湖仓核心模式与分层.md](02-湖仓核心模式与分层.md)
- 摄入的质量闸门 → [06-湖仓治理元数据血缘与质量.md](06-湖仓治理元数据血缘与质量.md)

## 核心概念速览（中英对照）

- **摄入** — Ingestion：把源数据搬进湖仓的管道总称（本书六动词之首 ✅）。
- **CDC** — Change Data Capture：捕获插入/更新/删除的变更流。
- **日志挖掘** — Log Mining：读事务日志的无损 CDC 路线 ✅ Hudi/Debezium 口径。
- **幂等** — Idempotent：重放不改变终态；分区覆盖与 MERGE 是两大实现。
- **水位表** — Watermark/Cursor Table：记录"取到哪"的元数据表。
- **exactly-once** — 精确一次：端到端三段责任合成的承诺（§4）。
- **MERGE INTO** — 合并写：按连接键分匹配合入的声明式更新（⚠️ 语法形态）。
- **分区覆盖** — Partition Overwrite：以分区为单位的原子替换（dynamic 模式）。
- **排序合并** — Precombine：按版本号取最新再落表（Hudi 语义 ✅）。
- **小文件风暴** — Small-file Problem：高频提交的文件数爆炸（→ 04 章）。

## 最新演进与工业实践

- **专用 CDC 入湖栈成型的延续**：2022 年"Debezium+Kafka+表格式"三件套，2026 已部分
  让位于一体化产品（Flink CDC 3.x 整库同步、Paimon 原生 CDC 存储 ✅
  <https://paimon.apache.org/docs/master/>）；本书手工拼装章的历史价值大于实用价值。
- **零 ETL 叙事**：SaaS→湖仓的"托管实时复制"（Fivetran/dlt/各云原生）把 §1 的
  第四条管道产品化；开源侧 dlt 已在盘上有实测册——
  [../Engineering_Lakehouses_with_Open_Table_Formats/10-增量管线与CDC.md](../Engineering_Lakehouses_with_Open_Table_Formats/10-增量管线与CDC.md) 的 🔧 dlt 真跑。
- **Iceberg 流式写入语义收敛**：增量读写（incremental appending/scans）进入 spec 与
  多引擎实现 ✅ <https://iceberg.apache.org/docs/latest/>——2022 书里"批为主"的摄入
  默认值在 2026 已改写为"流批同构"。
- **合规驱动的来源端改造**：GDPR/个保法使"原样入 Bronze"需要法务评审（删除权回溯），
  摄入设计从纯技术问题变政策问题（→ 07 章与 #186 册对读：
  [../Data_Governance_Elsevier/00-总览与阅读地图.md](../Data_Governance_Elsevier/00-总览与阅读地图.md)）。
