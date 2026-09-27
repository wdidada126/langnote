# 01 · 湖仓崛起与 Delta 定位（⚠️ 推定主题章）

> 章题为精读重构组织（非书中原文，见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 取证台账）。
> 本章回答"Up and Running 的第一问"：在装任何东西之前，先弄清楚 Delta Lake 到底解决谁的问题。
> 全章机制口径以 delta.io 协议与官方文档为锚（✅ 文档级），Spark/Databricks 行为一律 ⚠️ 转述——
> **本册 Delta 不装不跑、pyspark 不装**（任务红线）。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 1 | 数据湖的三大痛点 | schema-on-read 的便宜是有利息的 |
| 2 | 湖仓（Lakehouse）概念的来历 | 仓的治理 + 湖的成本，medallion 是操作化 |
| 3 | Delta Lake 的价值主张 | 在对象存储的"仅追加文件"上加一层事务日志 |
| 4 | 出身与耦合度 | Databricks 开源，OSS 可用但与 DBR 特性分级 |
| 5 | "跑起来"前的版本地图 | 2023 书基线（Delta 1.x/2.x）→ 2026 现状（4.x） |

## 1. 数据湖三大痛点（⚠️ 文档转述，配 DG 对照）

裸数据湖 = 对象存储 + Parquet/ORC 文件目录（文件布局基线见
[../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)）。三大经典痛点：

1. **无原子提交**：一批 1000 个 parquet 写到一半失败，下游读到"半批"；
   重试又造成重复。对象存储只有"单对象 put 原子"，没有"一组文件原子"。
2. **无行级更新**：改一行 = 重写整个文件；删一行 = 要么重写要么不删。
   于是 CDC/维表迟到修正这类数仓日常在湖里无处安放。
3. **无一致性读**：查询横跨文件列表刷新，同一查询两次扫描看到不同数据；
   更别提并发写者的互相覆盖。

教科书坐标：这三条分别对应 ACID 的 A/C（或 D）、隔离级、恢复——湖把数据库
六十年前解决的问题又丢了一遍（对照 [../数据库系统概念6/15-并发控制.md](../数据库系统概念6/15-并发控制.md)、
[16-恢复系统.md](../数据库系统概念6/16-恢复系统.md)）。

## 2. 湖仓：从论文口径到 medallion

"Databricks/伯克利"路线的叙事（✅ Databricks 文档页存在性实抓）：湖仓不是产品，
是"用开放存储 + 表格式 + 治理层重建数仓语义"的架构。其操作化形态即 **medallion**：

```text
bronze(原始追加) → silver(清洗+MERGE 对齐) → gold(业务聚合)
每层都是同一张事务日志表；层间靠流式增量推进
```

概念源头可再上溯 [../The_Data_Lakehouse/00-总览与阅读地图.md](../The_Data_Lakehouse/00-总览与阅读地图.md)
（Zikopoulos 一系的"湖仓"用语）；平台中立视角的完整架构学
[../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md)；
DG 的架构章在 [../Delta_Lake_Definitive_Guide/08-湖仓架构-Medallion.md](../Delta_Lake_Definitive_Guide/08-湖仓架构-Medallion.md)（参考纵深密度），本册只取"上手够用"的密度。

## 3. Delta 的核心手法：一层日志 + 文件名即版本

Delta 表 = `数据文件目录/_delta_log/`。提交 = 追加一个
`{version:020}.json`，内容是"本次新增/删除了哪些文件"（不是数据本身）；
读 = 从日志算出当前版本的文件列表再去扫 parquet。**"把变更当作一系列对
不可变文件列表的原子提交"** 是 Delta/Iceberg/Hudi/Paimon 四家共享的公理，
差异全在日志结构与提交协议（本册 02 章专讲，横向总论见
[../Engineering_Lakehouses_with_Open_Table_Formats/02-开放表格式的元数据布局总论.md](../Engineering_Lakehouses_with_Open_Table_Formats/02-开放表格式的元数据布局总论.md)）。

引擎侧坐标（⚠️ 转述，出自 DG 同款取证链）：Delta 生于 2019 年 Spark 社区，
GitHub 仓库 delta-io/delta（✅ URL 实抓 200）；"Delta Lake 湖仓格式"的说法
在 2024 年后官方措辞里已让位于"开放表格式"竞争叙事——四格式的引擎生态
对照在 [../Apache_Paimon_Streaming_Lakehouse/12-多引擎生态与四大湖格式对比.md](../Apache_Paimon_Streaming_Lakehouse/12-多引擎生态与四大湖格式对比.md)。

## 4. 出身与 Databricks 耦合度（两书分工的关键变量）

| 层 | OSS Delta（delta.io） | Databricks 平台增强 | 书内处理 |
| --- | --- | --- | --- |
| 协议/事务日志 | ✅ 完全开放（PROTOCOL.md 实抓 200） | 同源 | 本册 02/03 章主战场 |
| OPTIMIZE/Z-ORDER | ✅ 有 | 自动 OPTIMIZE、Predictive IO | ⚠️ 平台侧转述 |
| CDF/Deletion Vectors | ✅（3.x 后） | 更早以 Delta 引擎特性亮相 | 05 章，标注版本线 |
| Unity Catalog/Delta Sharing | OSS UC 存在（2024-06 开源） | 深度绑定托管版 | 06 章摘要，纵深让给 DG 11/12 章 |
| DLT、Serverless | ✗ | 商业专有 | 一律 ⚠️，不展开 |

分工表（[00-总览与阅读地图.md](00-总览与阅读地图.md)）里"耦合度差异"一行在此落地：
入门实操册先把 OSS 层跑通，平台特性是"升级路径"而非"起跑线"。
同名 Haelen/Davis 书（辨析一）从第 2 章就绑 DBR 集群 notebook——那是另一种写法，
注意别按那条路径理解本册（其仓库地址见 00，✅ 200 已验）。

## 5. 版本地图：2023 书基线 → 2026 现状

- **书基线（⚠️ 推定）**：2023 年 5 月前后对应 Delta OSS 1.x/2.x（2.0 引入 row
  tracking/type widening；2.3 前后 CDF 可用）——具体随附版本无官方 TOC 可证，标 ⚠️。
- **现状（✅ delta.io 博客 URL 实抓）**：Delta 3.0（2024，DV 转正、UniForm 叙事）、
  3.3；**4.0 于 2025-09-25 发布博文**（本目录 00 勘误④：与 DG 00"4.0=2025-01"存在
  预览/正式之差）；4.1（2026-03）、4.2（2026-04）、4.3（2026-06）。
- **上手建议**：新表直接按 4.x 文档走（docs.delta.io ✅ 301→https://docs.delta.io/index.html），
  遇到旧教程里的 2.x 行为差异回本册各章"最新演进"节对表。

## 6. 常见误区

| 误区 | 修正 |
| --- | --- |
| "Delta 就是 Databricks 的私有格式" | 协议开放、多引擎（Trino/Flink/delta-rs/Kernel）可读；商业增值在平台层 |
| "有事务日志就不用管小文件" | 日志解决正确性，不解决性能：高频提交照样需要 OPTIMIZE（04 章） |
| "湖仓 = 换了个文件夹" | 换的是提交协议与一致性语义；没有日志的目录永远只是文件堆 |
| "入门书=浅" | 本册按"上手骨架+机制锚点"取舍，纵深（Kernel/血缘/Sharing 协议）明确让给 DG 与格式三角目录 |

## 与其他章/其他书的联系

- 提交协议的机制细节与 🔧 手写演示 → [02-事务日志与提交协议.md](02-事务日志与提交协议.md)
- 概念总纲与两书分工 → [00-总览与阅读地图.md](00-总览与阅读地图.md)
- 全面参考纵深（安装章）→ [../Delta_Lake_Definitive_Guide/01-湖仓格式入门与安装.md](../Delta_Lake_Definitive_Guide/01-湖仓格式入门与安装.md)
- 引擎演进的长河视角 → [../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)；权衡总纲 → [../设计数据密集型应用.md](../设计数据密集型应用.md)

## 核心概念速览（中英对照）

- **数据湖** — Data Lake：对象存储上以开放文件格式存原始数据的仓库。
- **湖仓** — Lakehouse：湖成本 + 仓语义（ACID/治理/BI）的参考架构。
- **奖牌架构** — Medallion (Bronze/Silver/Gold)：分层数据精炼的湖仓操作化模式。
- **表格式** — Table Format：在文件之上定义事务/元数据协议的一层（Delta/Iceberg/Hudi/Paimon）。
- **事务日志** — Transaction Log：`_delta_log` 中按版本号的提交序列，Delta 的真相主体。
- **仅追加** — Append-only：对象存储文件不可改，一切"更新"都是新文件 + 日志重指向。
- **原子提交** — Atomic Commit：多文件变更以单个日志条目一次性生效。
- **schema-on-read** — 读模式：湖默认不校验 schema，Delta 以 enforcement 补课（03 章）。
- **OSS 与平台分层** — Delta Lake OSS vs Databricks Runtime：同内核不同商业面。
- **书基线/现状差** — 2023 书稿 vs 2026 Delta 4.x：本册每章"最新演进"节专职弥合。
- **四格式三角** — 本仓库对 Iceberg/Hudi/Paimon/Delta 姊妹目录的互认坐标网。

## 最新演进与工业实践

- **协议与实现**：Delta Protocol（✅ https://github.com/delta-io/delta/blob/master/PROTOCOL.md）、
  delta.io 文档站（✅ https://docs.delta.io/index.html）、主仓库（✅ https://github.com/delta-io/delta）。
- **版本线**：4.0 发布博（✅ https://delta.io/blog/2025-09-25-delta-lake-40/）、
  4.3 博（✅ https://delta.io/blog/2026-06-22-delta-4-3-release/）；3.0 博
  （✅ https://delta.io/blog/delta-lake-3-0/）。
- **2026 动向**："Delta grows up"博文（✅ https://delta.io/blog/2026-05-06-delta-grows-up-writes-time-travel-and-unity-catalog/）
  概括了写入/时间旅行/UC 的收敛方向；Delta Kernel + UC REST APIs 的开源化叙事持续推进
  （✅ https://delta.io/blog/2026-08-20-simplifying-your-open-lakehouse-with-the-delta-kernel-and-the-uc-delta-apis/）。
- **工业实践**：选型语境已从"Delta vs Iceberg"转为"UC/Polaris 等 catalog 中立层之下多格式并存"——
  本册 06 章与 [../Engineering_Lakehouses_with_Open_Table_Formats/00-总览与阅读地图.md](../Engineering_Lakehouses_with_Open_Table_Formats/00-总览与阅读地图.md) 选型章对读；
  Azure Databricks 文档（✅ https://learn.microsoft.com/en-us/azure/databricks/delta/）是平台侧最完整的公开镜像。
