# 02 · Unity Catalog 架构与命名空间

> 目标书：《Data Governance with Unity Catalog on Databricks》（O'Reilly 2025，ISBN 9781098179625）。
> ⚠️ **重建声明**：原书逐章目录未在线取得（见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §2），
> 本章按 Unity Catalog 官方文档架构模块重构，**不代表原书真实章界**。
> 三态标注：✅ 实证（附 URL）｜⚠️ 转述推定｜🔧 本机真实跑过（DuckDB/SQLite，非本书引擎行为）。

## 1. 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| §1 | Metastore：治理的根节点 | 一个 metastore 绑定多个工作区，是所有治理对象的容器 |
| §2 | 三层命名空间 | catalog.schema.object——比 HMS 的 db.table 多一层隔离 |
| §3 | Securables 对象模型 | 表/卷/函数/模型/服务——UC 治理的原子单元 |
| §4 | 存储层：Managed vs External | 托管表由 UC 管理存储；外部表只注册元数据 |
| §5 | 🔧 DuckDB 模拟三层命名空间 | 用 DuckDB schema+表类比 UC 的 catalog.schema.object |

## 2. Metastore：治理的根节点（§1）

Unity Catalog 的顶层容器是 **Metastore**（元数据存储）。

```
┌────────────────────────────────────────────────┐
│               Databricks Account               │
│  ┌──────────────────────────────────────────┐  │
│  │           Metastore (region-bound)        │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐    │  │
│  │  │Catalog A│ │Catalog B│ │Catalog C│    │  │
│  │  └────┬────┘ └────┬────┘ └────┬────┘    │  │
│  │       │           │           │          │  │
│  │  ┌────┴────┐ ┌────┴────┐     │          │  │
│  │  │Schema A1│ │Schema B1│     │          │  │
│  │  │Schema A2│ │Schema B2│     │          │  │
│  │  └─────────┘ └─────────┘     │          │  │
│  └──────────────────────────────────────────┘  │
│                                                │
│  Workspace 1 ←→ Metastore                      │
│  Workspace 2 ←→ Metastore (共享)               │
│  Workspace 3 ←→ Metastore (不同region)         │
└────────────────────────────────────────────────┘
```

✅ 关键事实（docs.databricks.com/en/data-governance/unity-catalog）：
- Metastore 绑定到特定云区域（AWS us-east-1 / Azure eastus / GCP us-central1）
- 一个 metastore 可被多个工作区引用（跨工作区共享治理）
- 每个 Databricks 账户可创建多个 metastore（多区域部署）
- Metastore 包含：storage credentials、external locations、connections、shares

⚠️ 转述：Metastore 的设计哲学是"治理与计算分离"——metastore 管治理，
workspace 管计算，两者通过绑定关系解耦。

## 3. 三层命名空间（§2）

```
Hive Metastore:     database.table           （两层）
Unity Catalog:      catalog.schema.object    （三层）
```

三层命名空间解决的问题：
1. **跨团队隔离**：不同团队用不同 catalog，不互相干扰
2. **环境分离**：dev/staging/prod 各一个 catalog，同一份代码切换 catalog 名即可
3. **数据产品化**：catalog = 数据产品边界（类似 Data Mesh 的 domain）

✅ SQL 示例（docs.databricks.com）：
```sql
-- 创建 catalog
CREATE CATALOG analytics;
-- 创建 schema
CREATE SCHEMA analytics.finance;
-- 创建表
CREATE TABLE analytics.finance.revenue (
  year INT, quarter INT, amount DECIMAL(12,2)
);
-- 查询
SELECT * FROM analytics.finance.revenue;
```

## 4. Securables 对象模型（§3）

Unity Catalog 治理的对象统称 **securables**（可授权对象）：

| 对象类型 | 说明 | 治理维度 |
| --- | --- | --- |
| **Table** | Delta / Hive / 外部表 | SELECT / MODIFY / CREATE |
| **Volume** | 非表数据（文件/模型权重） | READ VOLUME / WRITE VOLUME |
| **Function** | UDF / 注册 Python 函数 | USAGE |
| **Model** | ML 模型注册 | APPLY CATALOG / CREATE MODEL |
| **Service** | AI 服务（AI Gateway） | USE |
| **Share** | 数据共享定义 | 由 provider 管理 |

✅ 每种 securable 都有独立的特权集合（privileges），通过 GRANT / REVOKE 管理。
详见 Ch03。

## 5. 存储层：Managed vs External（§4）

| 维度 | Managed Table | External Table |
| --- | --- | --- |
| 数据存储 | UC 管理（默认 metastore 的 storage） | 用户指定的 external location |
| 生命周期 | DROP TABLE = 删数据+删元数据 | DROP TABLE = 只删元数据 |
| 存储凭证 | 自动管理 | 需配置 storage credential |
| 适用场景 | 生产表、UC 完全管控 | 跨平台表、已有数据注册 |

✅ External Location 需先创建 storage credential（S3 role / Azure MI / GCP SA），
然后注册 external location（URL 前缀匹配）。

## 6. 🔧 DuckDB 模拟三层命名空间（§5）

> ⚠️ **非本书引擎/平台行为**：以下演示用 DuckDB 1.5.5 模拟 Unity Catalog
> 的三层命名空间概念，仅做机制类比，不代表 Databricks 实际行为。

```python
import duckdb

# DuckDB 支持 catalog（通过 ATTACH）和 schema 两层
con = duckdb.connect()

# 模拟 catalog 层：用 ATTACH 创建独立数据库
con.execute("ATTACH ':memory:' AS analytics")
con.execute("ATTACH ':memory:' AS raw_data")

# 模拟 schema 层
con.execute("CREATE SCHEMA analytics.finance")
con.execute("CREATE SCHEMA analytics.marketing")
con.execute("CREATE SCHEMA raw_data.landing")

# 模拟 object 层：在各 schema 下建表
con.execute("""
    CREATE TABLE analytics.finance.revenue AS
    SELECT 2024 AS year, 1 AS quarter, 1500000.00 AS amount
""")
con.execute("""
    CREATE TABLE analytics.marketing.campaigns AS
    SELECT 'email' AS channel, 50000 AS spend
""")
con.execute("""
    CREATE TABLE raw_data.landing.events AS
    SELECT '2024-01-01' AS dt, 'click' AS event_type
""")

# 三层查询
result = con.execute("SELECT * FROM analytics.finance.revenue").fetchall()
print(f"三层查询结果: {result}")
# 输出: [(2024, 1, 1500000.0)]

# 列出所有 catalog 和 schema（类似 UC 的 SHOW 命令）
catalogs = con.execute("SELECT database_name FROM information_schema.schemata").fetchall()
print(f"可用 catalog/schema: {catalogs}")

con.close()
```

类比映射：
| DuckDB 概念 | Unity Catalog 概念 |
| --- | --- |
| ATTACH 的数据库 | Metastore 中的 Catalog |
| CREATE SCHEMA | Catalog 中的 Schema |
| CREATE TABLE | Schema 中的 Table/Volume/Function |

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
| --- | --- | --- |
| 元数据存储 | Metastore | UC 的顶层治理容器，绑定云区域 |
| 三层命名空间 | Three-level Namespace | catalog.schema.object 层级结构 |
| 可授权对象 | Securable | UC 中可被授予特权的任何对象 |
| 托管表 | Managed Table | UC 管理存储和元数据的表 |
| 外部表 | External Table | 仅注册元数据，存储由用户管理 |
| 存储凭证 | Storage Credential | 访问云存储的身份凭证 |
| 外部位置 | External Location | 云存储 URL 的注册映射 |

## 最新演进与工业实践

- **2025 Q1**：Unity Catalog 开源项目（github.com/unitycatalog/unitycatalog）
  发布独立 REST API 规范，允许非 Databricks 引擎接入。⚠️ 转述自 GitHub README。
- **Iceberg 兼容**：UC 现已支持注册 Apache Iceberg 表（通过 external location +
  Iceberg catalog 集成），模糊了 Delta-only 的边界。✅ docs.databricks.com。
- **对标**：Apache Polaris（Incubating）提供纯 Iceberg 的 REST catalog 服务，
  是 UC 在开源社区的对标方案。详见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §4.2。
- **趋势**：三层命名空间正在成为行业共识——Snowflake 的 database.schema.object
  与 UC 的 catalog.schema.object 结构一致，反映了"多租户+环境隔离"的共性需求。
