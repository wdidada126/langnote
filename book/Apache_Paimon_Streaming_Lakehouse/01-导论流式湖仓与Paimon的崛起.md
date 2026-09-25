# 01 导论：流式湖仓的兴起与 Paimon 的定位

> 本笔记为《Apache Paimon 官方文档与源码精读》系列第 1 章。**不存在对应的出版专著**（考证见
> [00-总览与阅读地图.md](00-总览与阅读地图.md)）。内容依据 paimon.apache.org 文档 Concepts/Overview
> 与公开演讲/博客（Alibaba Cloud "Apache Paimon: Streaming Lakehouse is Coming" 等），标 🔧 处为文档示例仿写。

## 核心概念速览（中英对照）

- **数据湖** — Data Lake：对象存储/HDFS 上以开放文件格式（Parquet/ORC）存原始数据的低成本存储层。
- **湖仓一体** — Lakehouse：在数据湖上补齐 ACID、schema、时间旅行等数仓能力（Databridge 论文系概念）。
- **流式湖仓** — Streaming Lakehouse：湖的数据新鲜度从"小时级批"压缩到"分钟/秒级流"，流是一等公民。
- **湖流一体** — Unified Stream & Batch Storage：同一份 Paimon 表同时充当批表和流队列，替代"Kafka+湖"双写。
- **开放表格式** — Open Table Format：在文件之上定义事务与元数据层的格式（Delta/Iceberg/Hudi/Paimon）。
- **更新流** — Changelog / Update Stream：携带 +I/-U/+U/-D 四种行变更事件的流。
- **批流一体计算** — Unified Batch & Streaming：同一引擎同一表定义既能全量批跑又能增量流跑。
- **检查点** — Checkpoint：Flink 分布式快照机制；Paimon 以检查点为湖提交的节拍。
- **新鲜度-成本权衡** — Freshness vs Cost：提交越频繁小文件越多，湖上"实时"本质是这笔账的精细化。
- **Flink Table Store** — Paimon 的前身，2023 年捐赠进入 ASF 孵化后更名为 Apache Paimon 🔧。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 1.1 | 大数据存储的三次摆动：数仓→湖→湖仓 | 湖赢了成本，输了时效与事务 |
| 1.2 | 表格式战国：为什么 Delta/Iceberg/Hudi 之后还要 Paimon | 前三者以"批表"为默认用户，流式更新是补丁 |
| 1.3 | Paimon 的三条设计公理 | LSM 入湖、changelog 显式化、Flink 原生 |
| 1.4 | 典型架构：流式湖仓长什么样 | ODS→DWD→DWS 全部落湖，级联流作业 |
| 1.5 | 边界与代价 | 不是所有场景都该上 Paimon |

## 精讲

### 1.1 三次摆动与"分钟级"空窗

第一代答案（数仓）解决事务与查询，但存不动日志/半结构化且成本失控；第二代（Hadoop 湖 + Parquet）
解决成本，但"目录即表"没有 ACID，一个 `INSERT OVERWRITE` 就能让下游读到半写状态。第三代（湖仓）由
Delta Lake（2019 论文，Spark 事务日志）、Iceberg（Netflix，快照式元数据）、Hudi（Uber，增量管线）
各自补上事务层——但它们的**默认用户是批作业**：提交节拍是"一个 Spark 作业结束"，新鲜度天然落在
几十分钟到小时级。Hudi 用 timeline + 异步表服务把新鲜度往分钟压，代价是表服务复杂度；
Delta 靠 Structured Streaming 轮询事务日志；Iceberg 靠 incremental 查询两快照差分。
三者在 2023 年前后都还回答不了同一个问题：**下游是一个 Flink 流作业、需要带 -U 的更新流时，湖能给吗？**

### 1.2 Paimon 的直接答案：把 Flink 的状态思想搬到湖上

Paimon 前身 Flink Table Store 的立项逻辑（FLIP 阶段公开文档可查）：Flink 流作业内部早就有
"高频更新 + 定期快照 + 状态后端"的完整体系，为什么不把这棵树（LSM）直接种到对象存储上，
让**湖表本身**成为可流读流写的存储？于是得到三条设计公理：

1. **LSM 树入湖**（第 02 章）：行级 upsert 不再重写整个数据文件，而是追加到 sorted run，后台归并。
   高频小提交从"湖格式的原罪"变成"LSM 的日常"。
2. **Changelog 显式化**（第 07 章）：更新流的"旧值"（-U）必须在合并前被抓出来持久化，湖上流读才有
   正确语义。Paimon 提供 input/lookup/full-compaction 三种 changelog producer，把选择权交给用户。
3. **Flink 原生绑定**（第 11 章）：commit on checkpoint、两阶段提交、撤回流处理、Lookup Join 维表、
   CDC 整库入湖 YAML——这些不是 connector 层的适配，而是格式层的能力（快照协议按 Flink 节拍设计）。

🔧 一句话验证定位（官方文档原文口径）：Paimon 自称 "a streaming data lake storage"，
核心能力列表第一条即 "real-time streaming lakehouse"。

### 1.3 湖流一体：Kafka 的两种角色变化

传统实时数仓：`CDC → Kafka(ODS) → Flink → Kafka(DWD) → Flink → 湖/OLAP`。Kafka 既当传输总线又当
"最近 N 天的物化视图"，topic 副本存储成本高、保留期外的历史要靠湖再存一份——**同一条流被存了两遍**。
Paimon 主张的"湖流一体"（官方称 log duplication 架构演进）有两种落地：

- **完全替代**：CDC 直接入 Paimon（带 changelog 的主键表），下游 Flink 流读 Paimon。
  延迟从秒级变成分钟级（检查点节拍），换来了历史可回溯、批流同表、OLAP 直读。
- **双写过渡**：Kafka 继续服务秒级作业，Paimon 承接分钟级作业与批分析；避免一次性推翻存量链路。

选择判据：下游能容忍多高的延迟？官方文档与实践博客一致——**分钟级可接受就入湖，秒级刚需留在 Kafka**。

### 附：项目沿革速览（🔧 以官方 Release/公告为准）

```text
2022     Flink Table Store 作为 Flink 社区子项目启动（FLIP 驱动，目标"给 Flink 一个湖上表存储"）
2023-12  以 Apache Paimon 之名进入 ASF 孵化器
2024     毕业为 Apache 顶级项目；国内云厂商全面产品化（阿里云 Flink+Paimon 流式湖仓方案）
2025+    1.x 系列：Deletion Vector、lookup changelog、postpone bucket、多模态/Blob、REST Catalog 等密集落地
```

沿革决定气质：Paimon 的默认接口、提交协议、类型系统处处可见 Flink 印记；它不是"通用表格式顺便支持流"，
而是"流存储下沉到湖"。后文各章遇到"为什么这样设计"的问题，回到这句找答案。

### 1.4 典型拓扑

```text
MySQL CDC ──┐                    ┌─ 流读 changelog ─→ Flink DWD 作业 ─→ Paimon(DWD 主键表)
Kafka 日志 ──┼→ Paimon(ODS 表) ──┤
日志文件  ──┘                    └─ 批读快照 ───────→ Spark/Trino/StarRocks ad-hoc 与报表
```

每一层都是同一张 Paimon 表：批读走最新快照（合并读），流读走 changelog（第 08 章）。
层间串联从"Flink state + Kafka topic"变成"Paimon 表 + 消费者 ID"（第 11 章级联作业）。

### 1.5 边界：什么时候**不**该选 Paimon

| 场景 | 更合适的选择 | 原因 |
| --- | --- | --- |
| 纯 append 日志分析、无更新 | Iceberg/Delta | 不需要 LSM 与 changelog，避开 compaction 税 |
| 以 Spark/Trino 为主、几乎无流写 | Iceberg | 生态中立性与引擎成熟度占优 |
| 秒级（<1min）端到端延迟 | Kafka + Flink state | Paimon 提交节拍受检查点限制 |
| 超高并发点查服务 | KV 存储/OLAP | 湖格式非 serving 层（Paimon 有 index 但不承诺毫秒点查）|
| 已有重 Hudi/Spark 体系且稳定 | 维持现状 | 迁移成本 > 流式收益时不值得（第 12 章有迁移路径 🔧）|

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "Paimon 是又一个表格式，和 Iceberg 互为替代品，选一个就行" | 默认负载不同：Paimon 默认用户是**持续写的流作业 + 持续读的流作业**；Iceberg 默认是批表。混批流负载时才需要 Paimon 的能力面 |
| "有了 Paimon 就可以删掉 Kafka" | 只在分钟级延迟可接受的全链路成立；秒级链路 Kafka 仍在（1.3 双写模式正是为此保留）|
| "Paimon 实时性 = Flink 实时性" | 湖上提交的可见性以快照为单位，最快也是检查点间隔 + compaction 滞后，与 Flink state 内秒级不是一个数量级 |
| "任何表设了主键就有 changelog" | 默认 changelog-producer=none，不配置则流读会被迫走"合并读"或由 normalize 节点兜底（第 07 章）|

## 与其他章 / 其他笔记的联系

- LSM 如何承载主键表 → [02-核心数据结构LSM树与主键表.md](02-核心数据结构LSM树与主键表.md)；
  changelog 三 producer → 07；Flink 绑定细节 → 11。
- 湖仓概念史与论文出处 → [../bigdata/01-大数据技术全景.md](../bigdata/01-大数据技术全景.md)。
- Flink 检查点与撤回流语义基线 → [../基于Apache_Flink的流处理.md](../基于Apache_Flink的流处理.md)、
  [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)。
- Hudi 的 timeline 解法对照 → [../Apache_Hudi_Definitive_Guide/04-从Hudi读.md](../Apache_Hudi_Definitive_Guide/04-从Hudi读.md)；
  Iceberg 元数据解法 → [../Apache_Iceberg活用入門/02-元数据三层结构.md](../Apache_Iceberg活用入門/02-元数据三层结构.md)；
  四格式横向总论 → [../Engineering_Lakehouses_with_Open_Table_Formats/02-开放表格式的元数据布局总论.md](../Engineering_Lakehouses_with_Open_Table_Formats/02-开放表格式的元数据布局总论.md)。
- 格式选型思维 → [../Engineering_Lakehouses_with_Open_Table_Formats/12-格式选型与迁移.md](../Engineering_Lakehouses_with_Open_Table_Formats/12-格式选型与迁移.md)。

## 本章记忆桩

```text
湖仓三代：能事务(19) → 能增量(21) → 能流动(23+)。
Paimon 三公理：LSM 入湖、changelog 显式化、Flink 原生。
入湖判据一句话：下游是流就要 -U；要 -U 就问 changelog-producer 谁来生产。
```
