# 02 Iceberg Catalog 的角色

> Catalog 是 Iceberg 架构中最容易被忽视、却最关键的一层。
> 本章展开 Catalog 从 Hive Metastore 到 REST 规范的演进，
> 解释为什么"Catalog 标准化"是湖仓多引擎互操作的前提。

## 2.1 Catalog 到底管什么

### 2.1.1 Catalog 的三重职责

Iceberg Catalog 承担三个核心职责：

1. **命名空间管理（Namespace Management）**：组织表的层级结构（如 `db.schema.table`）。
2. **表注册（Table Registration）**：记录"有哪些表"以及"每张表的 metadata file 在哪里"。
3. **元数据版本协调（Metadata Versioning）**：在创建/删除/更新表时，保证元数据的一致性。

> 🔧 **类比**：SQLite 的 `sqlite_master` 系统表记录了所有用户表的名称、类型和 SQL 定义。
> Iceberg Catalog 就是"分布式版 sqlite_master"——但它是远程 HTTP 服务，不是本地文件。
> ⚠️ 非本书引擎行为——类比仅用于理解概念。

### 2.1.2 Catalog 不做什么

同样重要的是理解 Catalog **不**做什么：

- ❌ 不存储数据文件（数据在对象存储上）。
- ❌ 不管理 Iceberg 快照链（快照在 metadata file 里）。
- ❌ 不执行查询（查询由引擎完成）。
- ❌ 不缓存数据（Catalog 只缓存元数据）。

## 2.2 从 Hive Metastore 到 REST Catalog

### 2.2.1 Hive Metastore（HMS）的问题

Hive Metastore 是 Hadoop 时代的 Catalog 标准，但它有结构性缺陷：

| 问题 | 说明 |
| --- | --- |
| 强耦合 Hadoop | 依赖 HDFS + Thrift RPC，云原生环境部署困难 |
| 单点故障 | 传统 HMS 是单节点，需要额外 HA 配置 |
| 引擎绑定 | Spark/Flink/Trino 各自维护 HMS 连接，版本兼容性矩阵复杂 |
| 非标准 API | Thrift 接口非 HTTP，难以跨语言/跨网络调用 |
| 安全模型原始 | 基于 Hadoop 的 proxy user，缺乏细粒度 RBAC |

### 2.2.2 云原生 Catalog 的尝试

AWS Glue、Google BigQuery Metastore 等云厂商提供了托管 Catalog 服务：
- ✅ 免运维、高可用。
- ❌ 厂商锁定——API 非标准，迁移成本高。
- ❌ 跨云不可用——Glue Catalog 只能在 AWS 生态内使用。

### 2.2.3 REST Catalog 规范的诞生

2023 年，Iceberg 社区在 REST Catalog 规范上达成共识：
- 基于 HTTP/JSON 的标准 API。
- 引擎无关——任何实现了 Iceberg REST 客户端的引擎都能接入。
- Catalog 实现可替换——Polaris、Nessie、Gravitino、Lakekeeper 都是 REST catalog 的实现。

> 🔧 **类比**：HMS → REST Catalog 的演进，类似 JDBC → ODBC 的标准化——
> 从"每个数据库有自己的协议"到"大家都说同一种语言"。
> ⚠️ 非本书引擎行为——概念类比。

## 2.3 REST Catalog 的核心设计原则

### 2.3.1 引擎无关性（Engine Agnostic）

REST catalog 的核心价值：**一个 Catalog，多个引擎**。

```text
Spark ──┐
Flink ──┤
Trino ──┼── REST API (HTTP/JSON) ── Polaris Catalog
Doris ──┤
StarRocks┘
```

所有引擎通过同一个 REST 端点访问同一组表——不需要为每个引擎配置不同的 Catalog 连接。

### 2.3.2 实现可替换性（Implementation Replaceable）

由于 API 是标准化的，Catalog 后端可以替换：
- 开发环境用本地文件 Catalog → 生产环境切换到 Polaris。
- 从 AWS Glue 迁移到 Polaris → 只需改 REST 端点 URL。

### 2.3.3 安全解耦（Security Decoupled）

REST catalog 将认证/授权从 Catalog 实现中解耦：
- 认证：OAuth2 / OIDC 标准协议。
- 授权：Catalog 实现自行定义 RBAC 模型（Polaris 用三层 RBAC，见 06 章）。

## 2.4 Catalog 生态全景

截至 2025 年，Iceberg REST catalog 的主要实现：

| 实现 | 维护方 | 特征 | 状态 |
| --- | --- | --- | --- |
| **Apache Polaris** | Apache（原 Snowflake 捐赠） | 参考实现 + 联邦入口 | ✅ 2026-02 毕业为顶级项目 |
| Apache Gravitino | Apache | 多引擎元数据管理平台 | ⚠️ Incubating |
| Lakekeeper | 社区 | Rust 实现的轻量 REST catalog | ⚠️ 早期阶段 |
| AWS Glue | AWS | 云托管，非完全 REST 标准 | ✅ GA |
| Tabular | Tabular Inc. | 商业托管 Iceberg catalog | ⚠️ 商业服务 |

> 与 [Architecting_an_Apache_Iceberg_Lakehouse/07-Catalog层实现.md](../Architecting_an_Apache_Iceberg_Lakehouse/07-Catalog层实现.md)
> 的十一款 catalog 生态互为补充——那里是广度选型，本册是 Polaris 深度。

## 2.5 Polaris 与其他 Catalog 实现的区别

Polaris 的独特定位：
1. **REST 规范的参考实现**：最贴近 Iceberg REST spec 的开源实现。
2. **联邦入口**：不仅管理自己的表，还能联邦外部 catalog（见 08 章）。
3. **Apache 顶级项目**：社区治理、厂商中立。

与 Paimon 的对照：
- [Apache_Paimon_Streaming_Lakehouse](../Apache_Paimon_Streaming_Lakehouse/) 中的 Paimon
  使用自身的 catalog 机制，而非 Iceberg REST catalog。
- 这反映了流式湖仓与批式湖仓在 Catalog 需求上的差异——Paimon 的 catalog 更侧重流式一致性。

## 2.6 本章小结

- Catalog 管"有哪些表、元数据在哪"，不存储数据、不执行查询。
- HMS → REST Catalog 的演进 = 从引擎绑定到引擎无关、从厂商锁定到标准开放。
- Polaris 是 REST catalog 的 Apache 级参考实现，独特价值在于联邦能力。

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
| --- | --- | --- |
| 命名空间 | Namespace | Catalog 内的表层级组织 |
| 表注册 | Table Registration | 记录表名到 metadata file 的映射 |
| Hive Metastore | Hive Metastore (HMS) | Hadoop 时代的 Catalog 标准 |
| REST Catalog | REST Catalog | 基于 HTTP/JSON 的标准 Catalog API |
| 引擎无关 | Engine Agnostic | 任何引擎通过同一 API 接入 |
| 联邦 | Federation | 通过统一入口访问多个外部 Catalog |

## 最新演进与工业实践

- **2023**：Iceberg REST Catalog 规范在 Apache Iceberg 社区达成共识 ✅。
- **2024**：Snowflake 将 Open Catalog 捐赠给 Apache，更名为 Polaris ⚠️（捐赠公告来自 Snowflake 博客）。
- **2025**：多引擎互操作成为湖仓标配——Trino、Spark、Flink 均原生支持 REST catalog ✅。
- **工业趋势**：企业从"一个引擎一个 Catalog"向"一个 Catalog 多引擎共享"迁移，
  减少元数据孤岛和重复配置。
- **⚠️**：Lakekeeper 等新兴实现的成熟度仍在演进中，选型时需评估社区活跃度。
