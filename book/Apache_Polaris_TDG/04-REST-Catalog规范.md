# 04 REST Catalog 规范

> Iceberg REST Catalog 规范是 Polaris 的实现基础。
> 本章拆解规范的 API 契约、端点设计与语义——理解规范才能理解 Polaris 的设计决策。

## 4.1 规范的设计目标

Iceberg REST Catalog 规范（REST Catalog Spec）的设计目标：

1. **引擎无关**：任何语言/引擎通过 HTTP 客户端即可接入。
2. **实现可替换**：后端从 Glue 切到 Polaris，只需改 URL。
3. **安全标准化**：认证用 OAuth2/OIDC，不依赖特定协议。
4. **原子语义**：表创建/更新/删除操作具有原子性保证。

> 🔧 **类比**：REST Catalog 规范之于 Catalog 实现，类似 JDBC 之于数据库驱动——
> 定义了"怎么说话"，不规定"怎么实现"。
> ⚠️ 非本书引擎行为——这是 Iceberg 社区规范。

## 4.2 核心端点一览

### 4.2.1 配置端点

| 端点 | 方法 | 用途 |
| --- | --- | --- |
| `/v1/config` | GET | 获取 Catalog 配置（默认属性、支持的特性等） |

引擎启动时首先调用此端点，获取 Catalog 的全局配置。

### 4.2.2 命名空间端点

| 端点 | 方法 | 用途 |
| --- | --- | --- |
| `/v1/{prefix}/namespaces` | GET | 列出所有命名空间 |
| `/v1/{prefix}/namespaces` | POST | 创建命名空间 |
| `/v1/{prefix}/namespaces/{ns}` | GET | 获取命名空间详情 |
| `/v1/{prefix}/namespaces/{ns}` | DELETE | 删除命名空间 |
| `/v1/{prefix}/namespaces/{ns}/properties` | POST | 更新命名空间属性 |

> 🔧 **类比**：SQLite 的 `CREATE SCHEMA` / DuckDB 的 `ATTACH DATABASE`——
> 命名空间是 Catalog 内的逻辑分区。
> 🔧 差异：SQLite schema 是文件内逻辑分区；REST namespace 可跨存储位置、跨云。
> ⚠️ 非本书引擎行为。

### 4.2.3 表端点

| 端点 | 方法 | 用途 |
| --- | --- | --- |
| `/v1/{prefix}/namespaces/{ns}/tables` | GET | 列出命名空间内的表 |
| `/v1/{prefix}/namespaces/{ns}/tables` | POST | 创建表 |
| `/v1/{prefix}/namespaces/{ns}/tables/{table}` | GET | 获取表元数据 |
| `/v1/{prefix}/namespaces/{ns}/tables/{table}` | POST | 更新表（提交新快照） |
| `/v1/{prefix}/namespaces/{ns}/tables/{table}` | DELETE | 删除表 |

### 4.2.4 视图端点（Views）

| 端点 | 方法 | 用途 |
| --- | --- | --- |
| `/v1/{prefix}/namespaces/{ns}/views` | GET/POST | 列出/创建视图 |
| `/v1/{prefix}/namespaces/{ns}/views/{view}` | GET/POST/DELETE | 获取/更新/删除视图 |

### 4.2.5 凭证端点

| 端点 | 方法 | 用途 |
| --- | --- | --- |
| `/v1/{prefix}/namespaces/{ns}/tables/{table}/credentials` | GET | 获取表的临时存储凭证 |

引擎在读写数据前调用此端点获取临时凭证（如 S3 STS token），
避免长期存储凭证。

## 4.3 请求与响应格式

### 4.3.1 创建表请求示例

```json
{
  "name": "events",
  "schema": {
    "type": "struct",
    "fields": [
      {"id": 1, "name": "event_id", "required": true, "type": "long"},
      {"id": 2, "name": "event_type", "required": false, "type": "string"},
      {"id": 3, "name": "created_at", "required": true, "type": "timestamptz"}
    ]
  },
  "partition-spec": {
    "fields": [
      {"source-id": 3, "field-id": 1000, "transform": "day", "name": "created_at_day"}
    ]
  },
  "location": "s3://bucket/warehouse/db/events"
}
```

### 4.3.2 响应结构

创建表成功后返回完整的 `LoadTableResult`，包含：
- `metadata-location`：metadata file 的存储路径。
- `metadata`：完整的表元数据（schema、partition spec、snapshots 等）。
- `config`：引擎访问数据时需要的额外配置（如存储凭证）。

## 4.4 原子提交语义

### 4.4.1 乐观并发模型

REST Catalog 的表更新使用 **乐观并发控制**：

1. 引擎读取当前表元数据（包含当前 snapshot ID）。
2. 引擎在本地计算新快照。
3. 引擎提交更新请求，携带 `current-snapshot-id`（期望的当前版本）。
4. Catalog 检查 `current-snapshot-id` 是否匹配——匹配则原子更新，不匹配则返回 409 Conflict。

> 🔧 **类比**：类似 Git 的 push with `--force-with-lease`——
> 你期望远端在某个 commit，如果已被别人推进则拒绝。
> 🔧 差异：Git 用文件锁/引用锁；REST catalog 用元数据原子切换实现无锁并发。
> ⚠️ 非本书引擎行为。

### 4.4.2 冲突处理

当提交冲突时（409 Conflict），引擎需要：
1. 重新读取最新表元数据。
2. 基于新快照重新计算变更。
3. 重试提交。

## 4.5 认证与安全

### 4.5.1 OAuth2 认证流程

REST Catalog 规范定义了标准的 OAuth2 认证：

```text
引擎 → POST /v1/oauth/tokens (client_id + client_secret)
     ← 200 OK (access_token + expires_in)
引擎 → GET /v1/config (Authorization: Bearer <token>)
```

### 4.5.2 令牌传递

所有后续请求通过 `Authorization: Bearer <token>` 头传递令牌。
Catalog 实现负责验证令牌并映射到权限模型。

## 4.6 规范与 Polaris 的映射

| 规范要求 | Polaris 实现 | 备注 |
| --- | --- | --- |
| REST 端点 | ✅ 完整实现 | 所有标准端点均支持 |
| OAuth2 认证 | ✅ 内置 OAuth2 服务器 | 也支持外部 OIDC |
| 原子提交 | ✅ CAS 语义 | 基于元数据存储的原子操作 |
| 命名空间层级 | ✅ 支持多级 | 如 `db.schema` |
| 临时凭证 | ✅ STS 集成 | S3/GCS/ADLS 均支持 |
| 视图 | ✅ 支持 | Iceberg View spec 实现 |

## 4.7 与姊妹册的关联

- [Architecting_an_Apache_Iceberg_Lakehouse/07-Catalog层实现.md](../Architecting_an_Apache_Iceberg_Lakehouse/07-Catalog层实现.md)
  中的 Catalog 层是本章的上游——那里讲十一款 catalog 的选型，本章讲 REST 规范本身。
- [Engineering_Lakehouses_with_Open_Table_Formats/](../Engineering_Lakehouses_with_Open_Table_Formats/)
  中的三格式横评也涉及 Catalog 层对比——Hudi 和 Paimon 各有自己的 catalog 机制。

## 4.8 本章小结

- REST Catalog 规范定义了 Catalog 的 HTTP API 契约。
- 核心端点：config、namespaces、tables、views、credentials。
- 原子提交基于乐观并发（CAS），冲突时返回 409。
- Polaris 是规范的最完整开源实现。

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
| --- | --- | --- |
| REST 端点 | REST Endpoint | Catalog API 的 HTTP 入口 |
| 命名空间 | Namespace | Catalog 内的逻辑分区 |
| 原子提交 | Atomic Commit | CAS 语义的元数据更新 |
| 乐观并发 | Optimistic Concurrency | 无锁写入，冲突重试 |
| 临时凭证 | Storage Credential | 短期存储访问令牌 |
| 冲突 | Conflict (409) | 并发提交时的版本不匹配 |

## 最新演进与工业实践

- **2023**：REST Catalog 规范在 Iceberg 社区定稿 ✅。
- **2024-2025**：Polaris、Lakekeeper、Gravitino 等实现陆续跟进 ✅。
- **工业趋势**：REST catalog 正在成为湖仓 Catalog 的"事实标准"——
  即使非 Iceberg 生态（如 Paimon）也在探索 REST 接口兼容。
- **⚠️**：规范仍在演进中，部分端点（如 views）的实现成熟度因 Catalog 而异。
- **参考**：Iceberg REST spec 源码在 `apache/iceberg` 仓库的 `open-api/rest-catalog-open-api.yaml`。
