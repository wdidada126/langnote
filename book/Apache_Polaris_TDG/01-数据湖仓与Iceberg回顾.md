# 01 数据湖仓与 Iceberg 回顾

> Polaris 要解决的问题域：湖仓架构为什么需要 Catalog？Iceberg 表格式如何改变了数据管理？
> 本章为全书建立背景——不重复 Iceberg 表格式机制细节（那是
> [Architecting_an_Apache_Iceberg_Lakehouse](../Architecting_an_Apache_Iceberg_Lakehouse/) 的活），
> 而是聚焦 **Catalog 层为何成为瓶颈**。

## 1.1 从数据湖到湖仓的演进

### 1.1.1 数据湖的初心与困境

数据湖（Data Lake）的初心是"先存下来，以后再分析"——把原始数据以文件形式
dump 到对象存储（S3/HDFS/GCS），用 Spark/Hive 按需查询。这个模式解决了
**存储成本** 问题，但带来了三个结构性困境：

1. **无 ACID 事务**：并发写入导致数据不一致，读者可能看到半写状态的文件集。
2. **无 Schema 演进**：列变更需要重写全部文件或维护脆弱的 ETL 管道。
3. **无时间旅行**：无法回溯到某个历史版本，审计与回滚无从谈起。

### 1.1.2 表格式（Table Format）的救赎

Apache Iceberg / Apache Hudi / Apache Paimon（原 Flink Table Store）
三个项目分别提出了"在文件之上加一层元数据"的方案。它们的核心思想一致：

- 数据仍然是对象存储上的文件（Parquet/ORC）。
- 元数据层记录"哪些文件属于哪张表、当前版本是哪个、快照链如何连接"。
- 通过元数据原子切换实现乐观并发控制。

> 🔧 **类比**：就像 SQLite 的 `sqlite_master` 表记录了所有表结构——
> Iceberg 的 metadata.json 就是"分布式版 sqlite_master"。
> ⚠️ 非本书引擎行为——这是 Iceberg 表格式的通用设计，非 Polaris 特有。

### 1.1.3 湖仓（Lakehouse）的定义

湖仓 = 数据湖的低成本存储 + 数据仓库的 ACID 保证与 Schema 管理。
关键特征：

| 特征 | 数据湖 | 湖仓 |
| --- | --- | --- |
| ACID | 无 | ✅ 表级/快照级 |
| Schema 演进 | 手动 ETL | ✅ 列增/列删/列重命名 |
| 时间旅行 | 无 | ✅ 快照 ID 回溯 |
| 引擎耦合 | 高（Hive 专属） | 低（多引擎通过 Catalog 接入） |

## 1.2 Apache Iceberg 表格式核心机制

### 1.2.1 三层元数据结构

Iceberg 的元数据分三层，理解这三层是理解 Catalog 角色的前提：

```text
metadata file (metadata.json)
  └── snapshot (快照 = 一个完整表状态的时间点)
        └── manifest list (清单列表 = 本次快照涉及哪些 manifest)
              └── manifest file (清单 = 一批数据文件的路径+分区+统计)
                    └── data file (Parquet/ORC 实际数据)
```

- **metadata file**：记录所有快照、当前快照 ID、表 schema、分区规范。
- **snapshot**：指向一个 manifest list，代表表在某一时刻的完整内容。
- **manifest list**：列出本次快照包含的所有 manifest 文件。
- **manifest file**：列出数据文件路径及其分区值、列级统计（min/max/null count）。

### 1.2.2 乐观并发与原子提交

Iceberg 的写入不依赖分布式锁：
1. Writer 读取当前 metadata file，基于当前 snapshot 创建新 snapshot。
2. Writer 尝试将 metadata file 原子切换为新版本（CAS 操作）。
3. 如果切换失败（其他 writer 已提交），则重试。

> 🔧 **类比**：类似 Git 的 rebase——两人同时改同一文件，后提交者需要 rebase 再 push。
> ⚠️ 非本书引擎行为——这是 Iceberg 的通用并发模型。

### 1.2.3 Catalog 在 Iceberg 中的位置

**关键洞察**：Iceberg 表格式本身 **不管理** "有哪些表"——它只管理"一张表的内容"。
"catalog 里有哪些表、每张表的 metadata file 在哪里"这个映射关系，
需要由 **Catalog 服务** 来维护。这就是 Polaris 要解决的问题。

## 1.3 Catalog 的演进简史

| 阶段 | 代表 | 特征 | 痛点 |
| --- | --- | --- | --- |
| Hive Metastore | Hive + Hadoop | Thrift RPC，强耦合 Hadoop | 单点故障、难扩展、引擎绑定 |
| AWS Glue | AWS 托管 | 云原生、免运维 | 厂商锁定、API 非标准 |
| Nessie | Project Nessie | Git-like 版本控制 | 社区分裂（已并入其他项目） |
| REST Catalog | Iceberg 规范 | HTTP 端点、引擎无关 | 需要实现服务——Polaris 填补此位 |

> 详见 02 章展开。

## 1.4 Polaris 在生态中的位置

Polaris 不替代 Iceberg 表格式，而是在其之上提供 **Catalog 服务层**：

```text
┌─────────────────────────────────────────────┐
│  引擎层：Spark / Flink / Trino / Doris      │
├─────────────────────────────────────────────┤
│  Catalog 层：Apache Polaris (REST Catalog)  │  ← 本册主角
├─────────────────────────────────────────────┤
│  表格式层：Apache Iceberg                    │
├─────────────────────────────────────────────┤
│  存储层：S3 / GCS / ADLS / MinIO            │
└─────────────────────────────────────────────┘
```

与姊妹册的关系：
- [Architecting_an_Apache_Iceberg_Lakehouse/07-Catalog层实现.md](../Architecting_an_Apache_Iceberg_Lakehouse/07-Catalog层实现.md)
  是上游——十一款 catalog 生态选型在本册展开为 Polaris 深度。
- [Engineering_Lakehouses_with_Open_Table_Formats/](../Engineering_Lakehouses_with_Open_Table_Formats/)
  提供三格式横评中的 Catalog 层对比视角。

## 1.5 本章小结

- 湖仓 = 湖的成本 + 仓的规矩；Iceberg 提供了"规矩"的表格式基础。
- Iceberg 表格式管"一张表的内容"，Catalog 管"有哪些表、在哪里"。
- Catalog 从 Hive Metastore 演进到 REST 规范——Polaris 是 REST catalog 的 Apache 级参考实现。

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
| --- | --- | --- |
| 数据湖 | Data Lake | 原始数据的低成本存储池 |
| 湖仓 | Lakehouse | 湖的存储 + 仓的 ACID |
| 表格式 | Table Format | 文件之上的元数据层（Iceberg/Hudi/Paimon） |
| 快照 | Snapshot | 表在某一时刻的完整状态 |
| 清单文件 | Manifest File | 记录数据文件路径与统计的元数据文件 |
| 乐观并发 | Optimistic Concurrency | 无锁写入，CAS 原子切换 |
| Catalog | Catalog | 管理"有哪些表、元数据在哪"的服务层 |

## 最新演进与工业实践

- **2024**：Apache Polaris 作为 Incubating 项目进入 Apache 软件基金会 ⚠️（官方 incubator 页面确认）。
- **2025**：O'Reilly 出版 Alex Merced 所著 *Apache Polaris: The Definitive Guide* ⚠️（书页 403，搜索页可达）。
- **2026-02-18**：Apache Polaris 毕业为顶级项目 ✅（dev.to 年度综述实抓）。
- **工业趋势**：Snowflake Open Catalog（Polaris 的商业前身）→ Apache 开源的路径，
  反映了"开放标准优先于厂商锁定"的行业共识。
- **⚠️**：成书时 Polaris 仍为 Incubating；本笔记以毕业后状态标注，章内区分"成书时"与"当前"。
