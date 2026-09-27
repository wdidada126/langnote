# 03 · Hands-on with Apache Iceberg（动手实践：从 Spark 写入到 BI 看板的最小组合）

> 覆盖原书第 3 章。目录来源：✅ Manning 官方 TOC 实抓：3.1 Our example / 3.2 Setting up an Apache
> Iceberg environment（Docker 前置、Docker Compose 文件、运行、访问服务）/ 3.3 Creating Iceberg tables
> in Spark（PostgreSQL 灌数→启 Spark→配置 Iceberg→装载→MinIO 验证）/ 3.4 Reading Iceberg tables with
> Dremio（启 Dremio→连 Nessie 目录→查询）/ 3.5 Creating a BI dashboard（Superset→连 Dremio→建
> dataset→图表与看板）。
> ⚠️ **本目录不搭不跑该环境**（Iceberg/Spark/Dremio/Nessie/Superset 一律不安装不启动）：以下是对
> 链路结构与配置要点的转述性重构 + 官方文档核对，凡行为断言均标 ⚠️。

## 本章地图

| 小节 | 内容 | 结论（一句话） |
| --- | --- | --- |
| 3.1 | 示例数据集与目标 | 一条"关系库→湖→看板"的最小Vertical Slice，五层各用一个开源件 |
| 3.2 | Docker Compose 环境 | 一个 compose 起 Spark/Nessie/MinIO/Dremio/Superset(+PostgreSQL 源库)全家 |
| 3.3 | Spark 建表装载 | JDBC 读 PostgreSQL → `writeTo` 落 Iceberg（Nessie catalog、MinIO 存储）→ 客户端看桶验证 |
| 3.4 | Dremio 读 | Dremio 挂同一 Nessie 目录，零拷贝直查湖上 Iceberg 表 |
| 3.5 | Superset 看板 | BI 不碰 Iceberg——经 Dremio 的 JDBC/ODBC 接口消费（联邦层的价值演示） |

## 3.1–3.2 环境拓扑（✅ 结构来自官方 TOC 与本书 Docker Compose 叙事框架；参数细节 ⚠️）

```text
docker compose 拉起的六件套（教学拓扑）：
  PostgreSQL      —— 模拟业务源库（3.3.1 灌样例数据）
  MinIO           —— S3 API 兼容对象存储（存储层的本地替身）
  Nessie          —— Git 式 Iceberg Catalog（catalog 层的演示件）
  Spark(THrift/JDBC server + Iceberg runtime jar) —— 摄入/DDL 引擎
  Dremio          —— 联邦查询引擎 + BI 语义层
  Superset        —— 消费层 BI
  读法：五层模型（02 章 2.7）在一张 compose 里各给一个"最便宜的可跑替身"——
  这正是本章的教材意图：选型前先摸到每层的接缝在哪。
```

- 为什么 demo catalog 选 **Nessie** 而非 Polaris/Lakekeeper（07 章才全景比较）：Nessie 单容器、
  零外部依赖即可跑 REST catalog，且其"分支"概念与 3.4 Dremio 连 Nessie 的叙事天然衔接 ⚠️（转述）。
- MinIO 承担"验证数据真的落在桶里"的角色（3.3.5）：`aws s3 ls`/mc 客户端肉眼确认
  `warehouse/…/metadata/*.json` 与 `data/*.parquet` 树形存在——**湖仓第一次摸到实体**。

## 3.3 Spark 建表装载（配置要点核对到 iceberg.apache.org Spark 文档；命令形态 ⚠️ 示意，未本机执行）

Spark 侧三要素（语法与
[../Use_Iceberg_with_Spark/02-Catalog配置与接入.md](../Use_Iceberg_with_Spark/02-Catalog配置与接入.md)
同口径，那里有逐参数深读）：

1. `--packages org.apache.iceberg:iceberg-spark-runtime-<scala>:<ver>`（运行时 jar 版本必须锁死组合 ⚠️）；
2. catalog 三参数指 Nessie：`catalog-impl=org.apache.iceberg.nessie.NessieCatalog`、
   `uri=http://nessie:19120/api/v2`、`warehouse=<桶根>`；
3. 写入：`df.writeTo("db.tgt").create()` / `append()`，或 JDBC 读 PostgreSQL 后同型装载 ⚠️。

- **验证闭环（3.3.5）**：MinIO 控制台列桶 → 看到 metadata/ 与 data/ 两族文件 → 回到 02 章的元数据树
  实物对照。演示语义可用本目录 🔧 迷你清单（见 02 章演示一）在纯 SQL 侧预演，无需真环境。

## 3.4 Dremio 读、3.5 Superset 看板（链路断言均 ⚠️ 转述）

| 步骤 | 动作 | 暴露的架构知识点 |
| --- | --- | --- |
| 3.4.2 | Dremio 添加 Iceberg source，指向 Nessie | **同一 catalog = 同一表真相**：换引擎不换数据、不重复注册 |
| 3.4.3 | Dremio SQL 编辑器直查 | 联邦层的读优化（列剪裁下推 + 加速缓存 reflection ⚠️ 特性名以当期文档为准） |
| 3.5.2 | Superset 经 Dremio（ODBC/JDBC 系）建连接 | 消费层与表格式**解耦**：BI 只需要 SQL 接口，不需要懂 Iceberg |
| 3.5.3–4 | dataset→chart→dashboard | 端到端"湖仓价值 30 分钟演示"完成——第 8/9 章的选型讨论由此起锚 |

- 链路读法：`PostgreSQL →(Spark/Nessie 写)→ MinIO(Iceberg 文件) →(Dremio/Nessie 读)→ Superset`。
  写入侧引擎与读取侧引擎**只共享两样东西：对象存储上的文件 + Catalog 里的指针**——这就是 1.6
  "两全其美"的工程显形。

## 常见误区

| 误区 | 纠偏 |
| --- | --- |
| "demo 里 Dremio 也写 Iceberg" | 本章 Dremio 只读；写路径归 Spark（摄入层职责边界，06 章）。读引擎写湖表要另查其 INSERT/DDL 支持矩阵 ⚠️ |
| "Nessie 只是 demo 玩具" | Nessie 的分支/合并语义是生产可用的治理特性（07 章/11 章分支审计复用该概念）⚠️ |
| "Superset 直连 MinIO 更快" | BI 直读 parquet 绕过 catalog=绕过快照隔离与权限——湖仓反模式；经联邦层是本章立的范 |
| "compose 起得来=架构成立" | 单机 compose 无并发写者、无小文件压力、无凭据体系——生产差距由 04–11 章逐层补齐 |
| 把 3.2 的镜像版本组合当长期依赖 | Manning 书内 compose 版本随年久失修 ⚠️；落地前核 iceberg-spark-runtime/Spark/Nessie 三方兼容表 |

## 与其他章 / 其他书的联系

- 本章每层组件的"选型展开"：存储→[05-存储层选型.md](05-存储层选型.md)、摄入→
  [06-摄入层架构.md](06-摄入层架构.md)、Nessie/catalog→[07-Catalog层实现.md](07-Catalog层实现.md)、
  Dremio/Trino→[08-联邦层设计.md](08-联邦层设计.md)、Superset 类 BI→[09-消费层与开放接口.md](09-消费层与开放接口.md)。
- Spark-Iceberg 逐参数深读（本书不重复）→ [../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)。
- Dremio 之外的联邦引擎（Trino）系统讨论 → [../Trino_The_Definitive_Guide_2e/00-总览与阅读地图.md](../Trino_The_Definitive_Guide_2e/00-总览与阅读地图.md)。
- Docker 全家桶 vs 云上托管替身（S3 Tables/Glue/Athena 一步到位）的取舍 →
  [../Practical_Lakehouse_Architecture/08-现实世界中的湖仓.md](../Practical_Lakehouse_Architecture/08-现实世界中的湖仓.md)。

## 本章链路速查卡

- 六容器对五层：PostgreSQL(源)/MinIO(存)/Nessie(目)/Spark(摄)/Dremio(联)/Superset(消)。
- 一条主线：PG →(Spark 写)→ MinIO 上的 Iceberg 文件 →(Dremio 经 Nessie 读)→ Superset 看板。
- 两个共享：读写引擎只共享"对象存储文件 + catalog 指针"——1.6"两全其美"的工程显形。
- 三个验证动作：桶里肉眼确认 metadata/data 树；Dremio 直查零重复注册；BI 不碰 parquet 只走 JDBC。
- 不跑声明：以上为 ✅ TOC 实抓结构 + 官方文档 ⚠️ 转述；复现请自行核对 compose 三件版本兼容表。
- 读法提示：本章是"接缝认知"教材——每层先摸到接口，05–09 章再谈选型。

## 核心概念速览（中英对照）

- **Vertical Slice** — 纵切样例：每层各取一个组件打通的最小端到端链路。
- **Docker Compose** — 单机多容器编排：本章六件套（PG/MinIO/Nessie/Spark/Dremio/Superset）的载体。
- **Nessie** — Git 式 Iceberg Catalog：分支/合并/REST 协议实现（07 章全景比较）。
- **MinIO** — S3 API 兼容开源对象存储：存储层的本地替身。
- **iceberg-spark-runtime** — Spark 侧 Iceberg connector 的运行时 fat jar。
- **writeTo / createOrReplace** — Spark Dataset 写 Iceberg 的入口 API（深读在 Use_Iceberg_with_Spark 03）。
- **Reflection（Dremio）** — Dremio 对源表自动维护的加速副本 ⚠️ 特性名以当期文档为准。
- **零拷贝接入** — 引擎经 catalog 直读既有文件，不导数据不重复注册。
- **BI 经联邦层** — Superset→Dremio→Iceberg 的三段式：消费层与表格式解耦的示范路径。
- **warehouse（catalog 参数）** — 表数据在对象存储上的根路径命名空间。
- **桶验证（3.3.5）** — 用 S3 客户端肉眼确认 metadata/data 文件树的教学动作——湖仓"实体化"时刻。

## 最新演进与工业实践

- **本章技术栈的 2026 坐标（✅ URL 核验）**：Nessie 最新 release `nessie-0.108.8`（2026-09-09，
  `https://api.github.com/repos/projectnessie/nessie/releases/latest`）；Dremio 持续主推 Iceberg 原生
  （作者任职处，见 00 章作者条）；iceberg 规范页 https://iceberg.apache.org/spec/ ✅ 200。
- **REST catalog 收敛（⚠️ 定性）**：demo 中"Nessie 承载 REST"的模式已是社区默认——老式 Hive catalog
  直连教程在新文档中淡出，选型细节见本册 07 章与
  [../Engineering_Lakehouses_with_Open_Table_Formats/09-Catalog与互操作.md](../Engineering_Lakehouses_with_Open_Table_Formats/09-Catalog与互操作.md)。
- **本地体验的低成本替代（🔧 边界提示）**：不想起六容器时，DuckDB iceberg 扩展可"装+load"但真实 ATTACH
  查询本机未实证 ⚠️——取证与口径见 [../DuckDB_Up_and_Running/09-云端DuckDB与MotherDuck.md](../DuckDB_Up_and_Running/09-云端DuckDB与MotherDuck.md)
  （扩展版本 45163a28，2026-09 实测在册）。
- **工业化注脚**：作者 2026-06 的 catalog 生态综述 ✅
  https://dev.to/alexmercedcoder/the-state-of-apache-iceberg-catalogs-in-june-2026-265e ——可当作本章
  demo 组件"毕业去向"的公开近况。
