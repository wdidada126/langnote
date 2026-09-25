# 02 Catalog 配置与 Spark 接入

> 章题为推断（见 [00 总览](00-总览与阅读地图.md) 声明段）。本章对应 report 的「getting started /
> connecting」职能：从 spark-sql 命令行到生产 catalog 选型。语法以
> [iceberg.apache.org Spark Configuration](https://iceberg.apache.org/docs/latest/spark-configuration/) 为准。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 2.1 | 引入 runtime jar | 一个 `--packages` 坐标搞定 connector |
| 2.2 | SparkCatalog 三种后端 | hadoop（文件即元数据）/ hive（共享 Metastore）/ REST（新默认方向） |
| 2.3 | 会话配置全集 | extensions、时区、覆盖行为等关键开关 |
| 2.4 | Catalog 选型决策 | 为什么 2025 年后新项目首选 REST Catalog |
| 2.5 | 无 catalog 的读法 | `spark.read.format("iceberg").load(path)` 的救急通道 |

## 核心精讲

> 以下配置均为**教学示意，不参与构建**；版本号为示意，以 releases 页矩阵为准。

### 2.1 引入 runtime jar

Iceberg 对 Spark 的集成物是一个 **shade 过的 runtime**（内含 core/api/parquet 与对 Spark DataSource V2 的实现）：

```bash
# 教学示意：本地起一个 spark-sql
bin/spark-sql \
  --packages org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.11.0 \
  --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions
```

- 坐标规则：`iceberg-spark-runtime-<Spark大版本>_<Scala版本>`（Spark 4.x 用 `4.0_2.13` 形态）。
- **不要在同一个 session 混装多个大版本的 runtime**；也不要再单独引 `iceberg-spark-3.5`，runtime 已含。

### 2.2 SparkCatalog：一种实现，多种后端

`org.apache.iceberg.spark.SparkCatalog` 把「表名字空间 → Iceberg Table 对象」的解析完全交给
可插拔的 **catalog 实现**。catalog 用 `spark.sql.catalog.<name>` 前缀声明，`<name>` 即 SQL 里的库前缀：

```properties
# 教学示意：hadoop 后端 —— 元数据存在仓库目录里，零外部依赖，适合本地/测试
spark.sql.catalog.local                = org.apache.iceberg.spark.SparkCatalog
spark.sql.catalog.local.type           = hadoop
spark.sql.catalog.local.warehouse      = s3://my-bucket/warehouse/
# hadoop catalog 需要把 Hadoop 配置透传时用前缀：
spark.sql.catalog.local.hadoop.fs.s3a.aws.access_key_id = ...
```

```properties
# 教学示意：hive 后端 —— 表登记进 Hive Metastore，供 Hive/老查询引擎发现
spark.sql.catalog.hive_prod            = org.apache.iceberg.spark.SparkCatalog
spark.sql.catalog.hive_prod.type       = hive
spark.sql.catalog.hive_prod.uri        = thrift://hive-metastore:9083
```

```properties
# 教学示意：REST 后端 —— 对接 Lakehouse 目录服务（Polaris / Gravitino / OneCatalog / Project Lighthouse 等）
spark.sql.catalog.rest_prod            = org.apache.iceberg.spark.SparkCatalog
spark.sql.catalog.rest_prod.type       = rest
spark.sql.catalog.rest_prod.uri        = https://polaris.example.com/api/catalog
spark.sql.catalog.rest_prod.warehouse  = my_warehouse
# 认证（示例，具体键名随所接 REST 服务）：
spark.sql.catalog.rest_prod.credential = <key>:<secret>
spark.sql.catalog.rest_prod.scope      = catalog:all
```

配好后 SQL 直接用三段名：`rest_prod.sales.orders`。此外还有 `jdbc`、各云厂商
`glue/snowflake/bigquery/dynamo` catalog 以及自定义 `catalog-impl`（直接给
`org.apache.iceberg.Catalog` 实现类，替代 `type`）。

### 2.3 会话配置全集（高频项）

| 配置 | 作用 | 备注 |
| --- | --- | --- |
| `spark.sql.extensions=...IcebergSparkSessionExtensions` | 开启 Iceberg SQL 扩展 | **必开项**：不开则没有 `CALL` 过程、增强的 `MERGE`（通配列等）、分支/标签时间旅行语法 |
| `spark.sql.catalog.<name>.cache-enabled` | catalog 层表对象缓存 | 排障「读到老 schema」时可临时关闭 |
| `spark.sql.iceberg.handle-timestamp-without-timezone` | TIMESTAMP 无时区解释策略 | 与 Spark 3 时区修复联动，跨引擎对数时重点核对 |
| `spark.sql.sources.partitionOverwriteMode` | `INSERT OVERWRITE` 是静态还是动态分区覆盖 | `dynamic` = 只覆盖数据里出现的分区，Iceberg 强烈建议（03 章 3.4） |
| `spark.sql.catalog.<name>.write.distribution-mode` | catalog 级写分布模式 | `none/hash/range`，影响小文件与 MoR 删除文件数（03 章） |

> 注：官方 `spark-configuration.md` 中 catalog 属性以
> `spark.sql.catalog.<name>.type|uri|warehouse|catalog-impl` 一组为核心；
> 属性名前缀规则（catalog 名嵌在 key 里）是 Spark 侧约定，不是 Iceberg Java API。

### 2.4 Catalog 选型决策

```
需要被 Hive/遗留查询引擎看见？ ── 是 ─→ hive catalog
        │否
元数据要进 Git / 做表级分支审批？ ── 是 ─→ Nessie（catalog-impl）
        │否
多引擎多云、要细粒度权限与凭证置换？ ── 是 ─→ REST catalog（Polaris/Gravitino/云托管…）
        │否
测试 / 单机 / 不想部署任何服务？ ── 是 ─→ hadoop catalog
        │否
                                  ─→ jdbc catalog（轻量共享元数据）
```

趋势判断：2025 年后新项目基本收敛到 **REST Catalog**——它把「目录服务」变成语言中立的 HTTP API
（规范见 [rest-catalog-spec](https://iceberg.apache.org/rest-catalog-spec/)），Spark/Flink/Trino 用同一种方式接入，
权限、凭证、审计都在服务端统一。hadoop catalog 则长期保留「本地实验零成本」地位。

### 2.5 无 catalog 的读法

```python
# 教学示意：PySpark 直接按路径读一张离线拷贝的表（只读）
df = spark.read.format("iceberg").load("s3://bucket/warehouse/db/orders")
```

按路径读不需要 catalog 登记，常用于备份验证与跨云搬运后的抽查；**写入不走这条路**
（没有提交协议，会产生并发事故）。

## 版本与兼容性

- 旧配置键 `spark.sql.catalog.impl.*`、`catalog-impl` 直挂式写法已统一为 `type` 简写；
  老 report 时代（Iceberg ≤1.4）示例可能仍用 `catalog-impl=org.apache.iceberg.hive.HiveCatalog` 全类名，二者等价。
- `format-version=2` 自 1.4 起为 Spark 建表默认（可用 `spark.sql.catalog.<c>.format-version=1` 或
  建表 `TBLPROPERTIES` 覆盖）；v1 表不支持行级删除，新项目无理由选 v1。
- REST catalog 客户端自 Iceberg 1.3 进入主干，1.4+ 键名稳定（`type=rest`）。
- Spark 3.3 以下 + Iceberg 1.x 新 runtime 的组合不支持。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| 没配 `spark.sql.extensions` 就抱怨 `CALL`/`MERGE ... *` 语法报错 | 这些是扩展语法，不是 Spark 内建；extensions 是必开项 |
| 把 `warehouse` 与 `warehouse-location` 混用 | `type=hadoop/hive` 时代常见两个键并存：`warehouse`（Spark catalog 前缀用）语义是表数据根路径；以当前版本文档为准 |
| hadoop catalog 指向团队共享目录图省事 | 元数据指针是文件级 CAS，无锁服务；高并发写易提交冲突，生产请用带服务的 catalog |
| 以为 catalog 管数据访问权限 | catalog 只管「表名→路径/凭证」的注册与发现；数据读权限在存储层/RBAC（REST catalog 服务端可代管凭证置换） |
| 一个 `--conf spark.sql.catalog.x=...` 名字里带点漏写 | 前缀必须精确为 `spark.sql.catalog.<name>`，`<name>` 才对应 SQL 里的一段名 |

## 与其他章 / 其他书的联系

- catalog 就位后第一次读写 → [03-数据读写与MERGE-INTO.md](03-数据读写与MERGE-INTO.md)。
- extensions 提供的 `VERSION AS OF 'branch'` 语法 → [04-时间旅行与元数据表.md](04-时间旅行与元数据表.md)。
- Spark 版本/扩展机制背景 → [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)。
- 「多引擎对等共享元数据」的平台视角（待建）Apache_Iceberg活用入門 的核心章题。
