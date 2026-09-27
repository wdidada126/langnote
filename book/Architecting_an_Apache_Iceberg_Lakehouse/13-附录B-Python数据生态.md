# 13 · 附录 B：Python for Apache Iceberg（七件 Python 生态武器与选型小结）

> 覆盖原书附录 B。目录来源：✅ Manning 官方 TOC 实抓：B.1 PyIceberg / B.2 Polars / B.3 DuckDB /
> B.4 Daft / B.5 Dremio / B.6 Bauplan / B.7 Spice AI / B.8 Summary and best practices。
> ⚠️ 除 DuckDB 1.5.5 可本机核验的部分外，其余库不安装不运行（Iceberg 面一律不实测），行为全部
> 转述官方文档。

## 本章地图

| 库（TOC 实抓） | 生态位 | 一句话判词 |
| --- | --- | --- |
| PyIceberg（B.1） | Iceberg 官方 Python 原生实现 | 不经 JVM 读写表元数据/仲裁/维护过程——Python 侧的"规范化身" |
| Polars（B.2） | Rust 核 DataFrame 引擎 | 内存计算件；接 Iceberg 经 PyIceberg/SQL 上下文组合（形态 ⚠️ 以当期文档为准） |
| DuckDB（B.3） | 单机分析 SQL 引擎 + 扩展生态 | 湖仓消费面的"轻装探针"——iceberg 扩展在册（本章 🔧 核验） |
| Daft（B.4） | Rust 核分布式 Python DataFrame | 面向多模态/AI 负载的查询引擎，Iceberg 为一等源 |
| Dremio（B.5） | 联邦引擎（08 章主角） | Python 经其 JDBC/Flight SQL/REST API 消费面进场 |
| Bauplan（B.6） | Python 原生湖仓开发框架 | "把管道写成纯 Python"的早期旗手；近况与活跃度要按仓库当期核对 ⚠️ |
| Spice AI（B.7） | AI 原生数据虚拟化（8.6.2 回环） | 为 LLM/agent 供数的加速运行时，Iceberg 为源 |
| B.8 小结 | 最佳实践 | 按负载分层：轻量直查/重 ETL/AI 管道各选其器 |

## B.1 PyIceberg 精读（⚠️ API 名以官方文档为准，本章不运行）

- 定位：Iceberg 项目内的**纯 Python 表实现**——catalog 客户端（REST/Hive/Glue 等后端）、schema/
  partition 演化 API、表扫描（谓词下推产出文件集）与写入、维护动作（expire/rewrite 部分过程）；
- 与"经 PySpark 的 Python"的分野：PySpark 走 JVM 引擎全家桶，PyIceberg 直连对象存储与目录——
  **轻量、无集群、但计算重活要交给别人**（读出的 Arrow/文件集转 DuckDB/Daft/Polars 计算）；
- 典型组合拳（书旨重构）：`PyIceberg 规划与提交 + Arrow 交换 + DuckDB/Daft 执行`——
  附录 B 的真实主题其实是"**Python 时代的读写分离**"：表的真相管理（catalog/元数据）与计算解耦后，
  Python 系引擎都能上桌。

## B.2–B.4 三型执行器对照（⚠️ 集成形态按当期文档）

| 型 | 代表 | 接 Iceberg 的方式 | 甜点位 |
| --- | --- | --- | --- |
| 单机内存 | Polars | 文件级（Parquet）或经 SQL 上下文/扩展 ⚠️ | ETL 中件、笔记本规模 |
| 单机 SQL | DuckDB | **iceberg 扩展（catalog ATTACH 路线）** + 直接 read_parquet 文件路线 | 探针/轻量消费/教学 |
| 分布式 | Daft | 原生 Iceberg 数据源 | 多模态（图像/文本列）与 AI 管道 |

### 🔧 核验：DuckDB 1.5.5 iceberg 扩展在册状态（本机实测，复用 DUAR09 口径不重复安装）

`SELECT extension_name, installed, loaded, extension_version FROM duckdb_extensions() WHERE
extension_name='iceberg'` 实跑输出：`('iceberg', installed=True, loaded=False, version='45163a28')`；
`LOAD iceberg` 成功。与姊妹册取证**逐值一致**（扩展版本串 45163a28；"可装、默认不载、load 无碍"）；
真实 `ATTACH (TYPE ICEBERG …)` 查询路径本机无公共仓库凭据，维持 ⚠️ 未实证——完整口径与安装史：
[../DuckDB_Up_and_Running/09-云端DuckDB与MotherDuck.md](../DuckDB_Up_and_Running/09-云端DuckDB与MotherDuck.md)。
官方扩展文档 ✅ 200：https://duckdb.org/docs/stable/core_extensions/iceberg/overview.html 。

**诚实边界**：扩展"在册可读元数据/规划"的能力面（版本 45163a28 支持 v2 delete？REST 认证方式？）
本机未验证 ⚠️——本目录只证"注册表里有、能 LOAD"，不证"能查你的生产表"。

## B.5–B.7 服务面与框架（⚠️ 转述）

- **Dremio（B.5）**：Python 消费其结果面（JDBC/REST；Flight SQL 支持度 ⚠️ 按版核）——09 章三接口
  在服务端一侧的兑现者；
- **Bauplan（B.6）**：以 Python 装饰器/配置把"管道即代码"做到湖仓上，含 catalog 交互——
  活跃度与后继状态请以 GitHub 当期为准 ⚠️（编者注：7 件名单里最"历史切片"的一件，读作 2024–2025
  Python 湖仓框架 wave 的标本）；
- **Spice AI（B.7）**：AI 运行时的检索加速面（8.6.2 回环）；与 09 章 MCP 消费同趋势。
- **B.8 选型条（书旨重构）**：轻量分析→DuckDB/Polars；直连表管理与维护→PyIceberg；
  AI/多模态管道→Daft；治理化共享→经 Dremio/联邦层；agent 供数→Spice 类新物种——
  "能用接口解决就不要用引擎解决，能单机解决就不要上分布式"。

## 常见误区

| 误区 | 纠偏 |
| --- | --- |
| "Python 写 Iceberg 必须 PySpark" | PyIceberg 覆盖轻写入与元数据管理；重计算才回 JVM/分布式引擎（B.8 的分层） |
| "DuckDB iceberg 扩展=能查一切 Iceberg 表" | 可装≠可查≠可查你的凭据/目录/格式版本组合——三态分账（本册 🔧 只到第二态） |
| "Daft/Polars 读 parquet 就是读 Iceberg 表" | 绕过 catalog 的裸文件读=看不见快照边界与删除记账——时间旅行/隔离全失效 |
| "PyIceberg 性能≈引擎" | 它的强项在规划/维护/轻读写；大扫描+复杂聚合仍应交给引擎面（各库执行内核不同代）⚠️ |
| 附录 B 当安装教程 | 库际兼容矩阵（pyiceberg×pyarrow×对象存储 SDK）年抛——装前核当期依赖 |

## 与其他章 / 其他书的联系

- Python 生态的盘上主库：DuckDB 两册 →
  [../DuckDB_Up_and_Running/00-总览与阅读地图.md](../DuckDB_Up_and_Running/00-总览与阅读地图.md)、
  [../DuckDB_in_Action/06-融入Python生态.md](../DuckDB_in_Action/06-融入Python生态.md)；
  Polars 在 UAR 的专章 → [../DuckDB_Up_and_Running/04-DuckDB与Polars.md](../DuckDB_Up_and_Running/04-DuckDB与Polars.md)。
- Iceberg 的元数据语义（裸文件读为什么不够）→ [02-Iceberg表格式与湖仓五层.md](02-Iceberg表格式与湖仓五层.md)；
  REST 目录对接 → [07-Catalog层实现.md](07-Catalog层实现.md)；维护过程的 Python 化 →
  [10-湖仓维护.md](10-湖仓维护.md)。
- 消费层的 Python/AI 位 → [09-消费层与开放接口.md](09-消费层与开放接口.md)；
  波内兄弟 #124 Vector_Databases（写作时未落盘）与本附录的检索负载对照，挂点登记 00。

## 本章速查卡

- 分工图：PyIceberg 管表真相（规划/提交/轻读写维护），Polars/DuckDB/Daft 管计算，Dremio/Spice 管供数面。
- 组合拳：规划 + Arrow 交换 + 引擎执行——附录 B 的暗线是"Python 读写分离"。
- 三型选型：单机内存 Polars / 单机 SQL DuckDB / 分布式多模态 Daft。
- 🔧 三态记账口径：installed → loaded → queryable——本目录实证前两态（45163a28），第三态按凭据/版本逐案验收。
- 反模式警示：裸 read_parquet ≠ 读 Iceberg 表；绕目录即绕过快照隔离与删除记账。
- 装载顺序建议：先 PyIceberg 注册与演化实验，再谈引擎并发写——元数据事故比查询慢更贵。

## 核心概念速览（中英对照）

- **PyIceberg** — Iceberg 官方 Python 原生实现：catalog/元数据/读写/部分维护不经 JVM。
- **规划与执行分离** — Planning vs Execution：元数据管理归 PyIceberg，计算交引擎的分工模式。
- **Polars** — Rust 核单机 DataFrame：与 Iceberg 经文件/SQL 上下文组合使用 ⚠️。
- **DuckDB iceberg 扩展** — 核心扩展生态里的外湖桥：ATTACH catalog 路线（本目录证"在册"）。
- **Daft** — Rust 核分布式 Python DataFrame：多模态/AI 负载向，Iceberg 一等源。
- **Flight SQL（Dremio 面）** — Arrow 传输 + SQL 语义的 Python 消费通道之一 ⚠️ 支持度按版核。
- **Bauplan** — Python 原生湖仓管道框架：wave 标本位，活跃度以仓库当期为准 ⚠️。
- **Spice AI** — AI 原生数据虚拟化/加速运行时：agent 供数面（8.6.2/9.3.3 的生态呼应）。
- **裸文件读** — Bypassing the Catalog：直接 read_parquet 绕过快照/删除——湖仓反模式。
- **Arrow 交换层** — 各库间零拷贝数据面的通用货币（B.8 组合拳的黏合剂）。
- **三态记账** — installed/loaded/queryable：扩展能力验收的诚实分层（本章 🔧 的方法论）。

## 最新演进与工业实践

- **PyIceberg 线（⚠️ 定性）**：随 Iceberg 1.11.x 推进其 v2/v3 特性面（deletion vector 读、
  新增 REST 认证）持续补全；版本号与能力矩阵以官方 py-iceberg 文档当期页为准
  （入口同 https://iceberg.apache.org/ 文档树 ✅ 200 群）。
- **DuckDB 扩展生态（✅ 本机 2026-09-27 实抓）**：iceberg 扩展 `45163a28`（installed=True/loaded=False，
  LOAD 成功）与 DUAR09 记录一致；duckdb 1.5.5 同环境另含 ducklake/motherduck 扩展生态
  （函数族 21 个在册的取证在同源文件）。
- **Daft/Polars 竞争面**：2025–2026 两库都在向"湖仓原生 + AI 多模态"渗透，功能重叠扩大——
  选型按团队栈亲和而非功能清单 ⚠️（定性）。
- **工业化注脚**：本附录的"Python 读写分离"叙事与 07 章 REST catalog 化是同一件事的两面——
  目录服务标准化后，任意语言客户端才可能轻装上桌（作者综述同源 ✅
  https://dev.to/alexmercedcoder/the-state-of-apache-iceberg-catalogs-in-june-2026-265e）。
