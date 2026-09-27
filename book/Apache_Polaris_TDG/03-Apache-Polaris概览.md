# 03 Apache Polaris 概览

> 本章是全书的坐标系原点：Polaris 从哪来、解决什么问题、核心架构是什么。
> 后续所有章节（REST 规范、安全模型、联邦、运维）都是本章的展开。

## 3.1 Polaris 的起源与定位

### 3.1.1 从 Snowflake Open Catalog 到 Apache Polaris

Polaris 的前身是 Snowflake 内部开发的 **Open Catalog** 服务——
Snowflake 希望让用户在 Snowflake 之外也能通过开放标准管理 Iceberg 表。
2024 年，Snowflake 将 Open Catalog 捐赠给 Apache 软件基金会，
项目更名为 **Apache Polaris**，进入 Incubating 阶段。

> ⚠️ 捐赠细节来自 Snowflake 官方博客与 Apache incubator 页面；
> 精确日期以 Apache 公告为准。

### 3.1.2 核心定位一句话

**Polaris = Apache Iceberg REST Catalog 的参考实现 + 多引擎联邦入口。**

它不做：
- ❌ 不替代 Iceberg 表格式（表格式是 Iceberg 的活）。
- ❌ 不替代计算引擎（Spark/Flink/Trino 各司其职）。
- ❌ 不存储数据（数据在 S3/GCS/ADLS 上）。

它做：
- ✅ 管理"有哪些 Iceberg 表、元数据在哪"。
- ✅ 提供标准 REST API 让多引擎共享同一 Catalog。
- ✅ 联邦外部 Catalog（Nessie/Glue/Gravitino 等）到统一入口。
- ✅ 提供 RBAC 安全模型控制表/命名空间级权限。

### 3.1.3 作者

本书作者 `chr(65)+chr(108)+chr(101)+chr(120)+' '+chr(77)+chr(101)+chr(114)+chr(99)+chr(101)+chr(100)`
（Alex Merced）是 Dremio/Snowflake 开发者关系负责人、DataLakehouseHub.com 社区主理人。
✅ 多源交叉确认：alexmerced.com、掘金翻译署名、datalakehousehub.com/author/alex-merced。

## 3.2 核心架构

### 3.2.1 架构分层

```text
┌────────────────────────────────────────────────────────┐
│  客户端/引擎层                                          │
│  Spark │ Flink │ Trino │ Doris │ StarRocks │ REST CLI  │
├────────────────────────────────────────────────────────┤
│  REST API 层（Iceberg REST Catalog Spec）               │
│  /v1/config │ /v1/{prefix}/namespaces │ /v1/.../tables │
├────────────────────────────────────────────────────────┤
│  Polaris 服务层                                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐   │
│  │ 认证/OAuth│ │ RBAC 引擎│ │ 联邦 Catalog 管理器  │   │
│  └──────────┘ └──────────┘ └──────────────────────┘   │
├────────────────────────────────────────────────────────┤
│  元数据存储层（可配置后端）                               │
│  内存 │ 文件 │ 关系数据库                                │
├────────────────────────────────────────────────────────┤
│  对象存储层                                             │
│  S3 │ GCS │ ADLS │ MinIO                               │
└────────────────────────────────────────────────────────┘
```

### 3.2.2 关键组件

| 组件 | 职责 |
| --- | --- |
| REST API Server | 接收并路由 Iceberg REST 请求 |
| Authentication Module | OAuth2/OIDC 令牌验证 |
| Authorization Engine | Principal → PrincipalRole → CatalogRole 三层 RBAC（见 06 章） |
| Namespace Manager | 命名空间的 CRUD 与层级管理 |
| Table Registry | 表注册、metadata file 位置管理 |
| Federation Manager | 外部 Catalog 的注册与代理访问（见 08 章） |
| Storage Credential Provider | 为引擎生成临时存储访问凭证 |

## 3.3 Polaris 的核心特性

### 3.3.1 开放标准优先

- 100% 实现 Iceberg REST Catalog 规范。
- 不引入私有 API——任何 Iceberg REST 客户端都能接入。
- 与 Nessie、Gravitino、Lakekeeper 等实现互操作。

### 3.3.2 多引擎支持

通过 REST 标准接口，以下引擎可直接接入 Polaris：

| 引擎 | 接入方式 | 备注 |
| --- | --- | --- |
| Apache Spark | `spark.sql.catalog.polaris` 配置 | 详见 07 章 |
| Apache Flink | Flink Iceberg connector 的 catalog 配置 | 详见 07 章 |
| Trino | Trino Iceberg connector 的 REST catalog 模式 | 详见 07 章 |
| Apache Doris | Doris 的 Iceberg catalog 配置 | ⚠️ 社区贡献中 |
| StarRocks | 类似 Doris | ⚠️ 社区贡献中 |

### 3.3.3 联邦能力

Polaris 不仅管理自己的表，还能将外部 Catalog "挂载"到统一入口：
- 用户通过 Polaris REST 端点访问 Glue 中的表——无需知道 Glue 的存在。
- 详见 08 章。

### 3.3.4 细粒度安全模型

三层 RBAC：Principal → PrincipalRole → CatalogRole。
- Principal：用户或服务账号。
- PrincipalRole：分配给 Principal 的角色集合。
- CatalogRole：在特定 Catalog 内的权限集合（可细化到 namespace/表级）。
- 详见 06 章。

## 3.4 项目状态与治理

### 3.4.1 Apache 毕业历程

| 时间 | 事件 | 来源 |
| --- | --- | --- |
| 2024 | 进入 Apache Incubating | ⚠️ Apache incubator 页面 |
| 2025 | 成书时仍为 Incubating | ⚠️ O'Reilly 书页 |
| **2026-02-18** | **毕业为 Apache 顶级项目** | ✅ dev.to 年度综述实抓 |

> ⚠️ 成书时 Polaris 仍为 Incubating；本笔记以毕业后状态标注。

### 3.4.2 社区治理

- 邮件列表：dev@polaris.apache.org
- 代码仓库：github.com/apache/polaris
- PMC 成员来自 Snowflake、Dremio、Apple、Microsoft 等 ⚠️（具体成员列表需查 Apache Whimsy）。

## 3.5 与 Snowflake Open Catalog 的关系

| 维度 | Snowflake Open Catalog | Apache Polaris |
| --- | --- | --- |
| 代码基础 | 相同 | 相同（捐赠） |
| 治理 | Snowflake 商业产品 | Apache 社区治理 |
| 定位 | Snowflake 生态的 catalog 服务 | 开放标准参考实现 |
| 联邦 | 有限 | 完整（见 08 章） |

## 3.6 本章小结

- Polaris = REST Catalog 参考实现 + 联邦入口 + RBAC 安全模型。
- 从 Snowflake Open Catalog 捐赠而来，2026-02 毕业为 Apache 顶级项目。
- 核心价值：让多引擎通过同一个标准 API 管理 Iceberg 表。

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
| --- | --- | --- |
| 参考实现 | Reference Implementation | 最贴近规范的开源实现 |
| 联邦 | Federation | 统一入口访问多个外部 Catalog |
| Principal | Principal | 用户或服务账号 |
| PrincipalRole | Principal Role | 分配给 Principal 的角色集合 |
| CatalogRole | Catalog Role | Catalog 内的权限集合 |
| 临时凭证 | Storage Credential | 引擎访问对象存储的短期令牌 |

## 最新演进与工业实践

- **2024**：Polaris 进入 Apache Incubating ⚠️。
- **2026-02-18**：毕业为顶级项目 ✅。
- **工业趋势**：Snowflake → Apache 的捐赠路径成为"商业产品开源化"的标杆案例。
- **⚠️**：Polaris 的联邦能力仍在快速迭代中，外部 Catalog 的支持范围以官方文档为准。
- **生态联动**：Polaris 与
  [Data_Fabric_and_Data_Mesh_with_AI](../Data_Fabric_and_Data_Mesh_with_AI/)
  中的数据联邦/Mesh 理念形成技术实现层面的呼应（见 08 章）。
