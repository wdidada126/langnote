# 02 · Apache Iceberg and the lakehouse（表格式定义与五层组件模型）

> 覆盖原书第 2 章。目录来源：✅ Manning 官方 TOC 实抓：2.1 What does it mean that Iceberg is a table
> format / 2.2 Why you need a table format / 2.3 How Apache Iceberg manages metadata / 2.4 Key features
> （2.6.1 ACID transactions、2.6.2 How tables evolve、2.6.3 Time travel and snapshot-based queries、
> 2.6.4 Hidden partitioning、2.6.5 Cost efficiency and query performance）/ 2.7 lakehouse components
> （2.7.1 Storage / 2.7.2 Ingestion / 2.7.3 Catalog / 2.7.4 Federation / 2.7.5 Consumption 五个子节）。
> **2.7 的五层模型是全书骨架**，05–09 章按它逐层展开。

## 本章地图

| 小节 | 内容 | 结论（一句话） |
| --- | --- | --- |
| 2.1–2.2 | 表格式是什么、为什么需要 | 表格式=用文件定义的"表真相"契约；没有它，目录与数据各说各话 |
| 2.3 | 元数据管理 | metadata JSON→snapshot→manifest list→manifest file 四层树，指针即事务 |
| 2.4/2.6 | 六大特性 | ACID、演化、时间旅行、隐藏分区、性能、成本——全部派生自元数据树 |
| 2.7 | 湖仓五层组件 | 存储/摄入/Catalog/联邦/消费——本书的选型坐标系 |

## 2.1–2.3 机制坐标（架构视角；字段级深读回姊妹册）

Iceberg 把一张表描述成一棵**纯文件构成的元数据树**（⚠️ 转述官方规范结构，非实测）：

```text
metadata/vN.json（table metadata：schema、spec、snapshots 列表、current-snapshot-id 指针）
  └─ snapshot（一次提交=一个表版本；parent 链 + summary）
      └─ manifest list（avro：本快照由哪些 manifest 组成，各带 added/existing/deleted 计数与分区范围）
          └─ manifest file（avro：逐数据文件记录 partition、record_count、file_size_in_bytes、列级 min/max）
              └─ data files（Parquet/ORC/Avro 实际文件，躺在对象存储）
```

- **提交 = 写新文件 + 原子换指针**：`metadata/v(N+1).json` 完整写出后，Catalog 里
  compare-and-swap `current-snapshot-id`；失败重读重试（乐观并发）。旧文件一个字节不动——
  这就是 ACID、时间旅行、回滚、零成本演化的共同来源。
- 与 Hive 表的关键差别：Hive metastore 记"路径约定"（目录名即分区值，改路径=改表），Iceberg 记
  "文件清单"（manifest 才是真相，路径随便挪）。病灶案例 →
  [../Apache_Iceberg活用入門/01-Iceberg与数据湖表格式入门.md](../Apache_Iceberg活用入門/01-Iceberg与数据湖表格式入门.md)。

### 🔧 演示一：手写迷你"快照清单"看时间旅行（DuckDB 1.5.5，本机真实跑过）

方法：`D:\develops\tmp\dbwave_w3_icearch\demo_mini_iceberg.py` 用两张 DuckDB 表模仿 manifest_entry
（status∈{ADDED,EXISTING,DELETED}）与 manifest_list，构造三个快照 1001(append)→1002(MoR delete)→
1003(CoW rewrite)，"读某快照"= `snapshot_id<=S 且未被 DELETED` 的文件集。实测输出：

- 读 1001 可见文件 = `001.parquet + 002.parquet`（2 个）；
- 读 1003 可见文件 = `002.parquet + 001b.parquet`（`001` 被 `001b` 取代）——**同一张表，两个时刻两套
  文件清单**，时间旅行的本质就是按快照过滤清单；
- `meta/pos-del-1002.avro` 在 1002 可见、1003 起隐身——delete 文件也是清单里的一等公民。

> 诚实边界：这是**语义模仿**（SQL 手搓），不是任何 Iceberg 实现；真实 spec 字段与匹配规则见
> [../Apache_Iceberg活用入門/02-元数据三层结构.md](../Apache_Iceberg活用入門/02-元数据三层结构.md)。

## 2.4/2.6 六大特性逐条（各给"选型时的追问"）

| 特性（TOC 实抓小节） | 机制一句话 | 架构师追问（通向的章） |
| --- | --- | --- |
| 2.6.1 ACID transactions | 原子指针替换 + 乐观并发校验 | 谁做 CAS？→ Catalog 的并发实现质量（07 章） |
| 2.6.2 How tables evolve | field-id/spec-id 解耦名字与数据 | 哪些演化免费、哪些要重写？→ 活用入門 04 |
| 2.6.3 Time travel / snapshot queries | 快照链保留=历史可查 | 保留多久、花多少钱？→ 10 章 expire 与 11 章留存政策 |
| 2.6.4 Hidden partitioning | transform（days/bucket/truncate/identity）写进元数据 | 选错 transform 的代价与分区演化（05 章存储布局、活用入門 03） |
| 2.6.5 Cost efficiency & query performance | manifest min/max 剪枝 + 引擎并行规划 | 剪枝效果取决于 compaction 质量（10 章） |
| （2.5 开源标准） | 规范公开、多引擎实现 | 引擎特性矩阵按最短板（08/09 章） |

### 🔧 演示二：清单剪枝（同脚本，D2）

谓词 `partition_day='2026-05-02'` 时 planner 只需扫 **1 个文件**（清单里当天文件恰 1 个）——
剪枝的"账本"就是 manifest；文件与分区错位摆放（poorly colocated）时同一查询会扫一把文件，
这正是 10 章 `rewrite_data_files` 的动机之一。列级 min/max 的更细剪枝（ts 谓词）在真实 spec 里
由 manifest 的列统计承担，机制 → [../Engineering_Lakehouses_with_Open_Table_Formats/03-Iceberg表格式机制.md](../Engineering_Lakehouses_with_Open_Table_Formats/03-Iceberg表格式机制.md)。

## 2.7 五层组件模型（全书主纲，务必背下每层的"契约"）

| 层 | 官方小节名（实抓） | 职责契约 | 本书展开章 |
| --- | --- | --- | --- |
| Storage | Foundation of your lakehouse | 对象存储 + Parquet + S3 API 事实标准 | 05 |
| Ingestion | Feeding data into Iceberg tables | 写语义/提交协议的执行者（Spark/Flink/…） | 06 |
| Catalog | **Your entry point to the lakehouse** | 表名→metadata 位置的注册/发现/授权服务 | 07 |
| Federation | Modeling and accelerating data | 跨源建模与查询加速（Dremio/Trino） | 08 |
| Consumption | Delivering business value | BI/笔记本/AI 经开放接口消费 | 09 |

- 记法：**存-摄-目-联-消**，数据从下往上流，请求从上往下打，Catalog 是两侧的交汇闸口——
  所以书里叫它 entry point 而不是 metadata store。
- 该分层与 Practical_Lakehouse_Architecture 的切法（存储/目录/计算/治理）正交互补：
  它按"平台职能"切，本册按"数据在 Iceberg 视角的流经路径"切 →
  [../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md)。

## 常见误区

| 误区 | 纠偏 |
| --- | --- |
| "Iceberg 是存储格式（像 Parquet）" | 它不规定字节怎么写进文件，只规定**表的真相怎么写进元数据**；文件层是 Parquet/ORC（2.1 的题眼） |
| "manifest list 可有可无" | 快照的文件爆炸防护层：查询先读 list 粗筛 manifest，再读选中的 manifest——跳过它等于每查询全表清单扫描 |
| "有了快照就不用备份" | 快照只覆盖"被跟踪的文件"；孤儿清理误删/桶级删除不在快照保护圈（11 章灾备） |
| "五层=五个必装产品" | 层是**职责**不是采购单：MinIO 可以同时当存储与（小环境里）事实目录宿主；Dremio 一身兼联邦+部分 Catalog |
| "隐藏分区=性能免费" | transform 选择不当反而放大小文件与倾斜（10 章 compaction 买单） |

## 与其他章 / 其他书的联系

- 本章是 05–09 章的目录页：每层的机制细节在本册对应章；规范细节统一转
  [../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md)。
- 元数据树 vs Paimon 的 snapshot/manifest：同构命名、不同内容（LSM 层）→
  [../Apache_Paimon_Streaming_Lakehouse/04-元数据层快照与清单.md](../Apache_Paimon_Streaming_Lakehouse/04-元数据层快照与清单.md)。
- 提交协议与冲突矩阵的三格式横评 →
  [../Engineering_Lakehouses_with_Open_Table_Formats/06-事务与并发写.md](../Engineering_Lakehouses_with_Open_Table_Formats/06-事务与并发写.md)。
- Spark 侧怎么写这份清单 → [../Use_Iceberg_with_Spark/03-数据读写与MERGE-INTO.md](../Use_Iceberg_with_Spark/03-数据读写与MERGE-INTO.md)。

## 核心概念速览（中英对照）

- **表格式** — Table Format：以文件元数据定义表真相（schema/分区/快照）的规范层。
- **表元数据文件** — Table Metadata File（metadata JSON）：schema、spec、快照列表与当前指针的根。
- **快照** — Snapshot：一次提交的全表状态版本，时间旅行与回滚的锚点。
- **清单列表** — Manifest List：快照级 manifest 目录，带各 manifest 的新增/存续/删除计数与分区范围。
- **清单文件** — Manifest File：逐数据文件的分区、行数、字节数与列级 min/max 统计。
- **原子指针替换** — Atomic Pointer Swap：提交协议本质——写完新元数据才换 current 指针。
- **乐观并发** — Optimistic Concurrency：CAS 失败则重读重试，不重写数据文件。
- **隐藏分区** — Hidden Partitioning：分区值由 transform 从列推导并记入元数据，用户无需感知分区列。
- **transform** — 分区变换函数：identity/bucket/truncate/days 等，决定剪枝与写入布局。
- **五层模型** — Storage/Ingestion/Catalog/Federation/Consumption：本书的架构坐标系（2.7）。
- **入口点** — Entry Point：Catalog 的角色定义——引擎与治理在此相遇。
- **数据文件** — Data File：Parquet/ORC/Avro 实体文件，Iceberg 只登记不改造。

## 最新演进与工业实践

- **规范版本线（✅ 实抓）**：iceberg.apache.org/spec/（200，2026-09-27 核验）导航已列
  "Version 4: Metadata Structure and Representation"——本书附录 C（本册 14 章）讨论的 v4 已成规范在册文本；
  实现线 `apache-iceberg-1.11.0`（2026-05-20，GitHub Releases API ✅）。
- **元数据层工程化**：v3 的 deletion vector（Puffin 格式承载）与 v4 的方向是"少写清单、快规划"——
  细节以规范页为准 ⚠️，勿按 2024 年前的博客抄配置。
- **消费侧接口扩张**：Arrow Flight SQL 与 MCP 被本册 09 章/原书 9.3 并列——2025–2026 "AI 直连湖仓"
  的接口层正在把目录/查询服务变成 MCP server（定性 ⚠️，实现各异）。
- **本机可核验的接入现状**：DuckDB 1.5.5 iceberg 扩展 install+load ✅（版本 45163a28）、真实仓库查询
  无凭据未实证 ⚠️——取证复用 [../DuckDB_Up_and_Running/09-云端DuckDB与MotherDuck.md](../DuckDB_Up_and_Running/09-云端DuckDB与MotherDuck.md)，
  官方扩展文档 https://duckdb.org/docs/stable/core_extensions/iceberg/overview.html ✅ 200。
