# 14 · 附录 C/D：The Apache Iceberg specification 与后记（v1–v4、REST、Puffin 与迁移）

> 覆盖原书附录 C 与附录 D（后记并入本章末节）。目录来源：✅ Manning 官方 TOC 实抓：C.1 Understanding
> the Iceberg specification（规范是什么/为何形式化/版本化原则与兼容）/ C.2 Iceberg table format
> versions（v1 基础、v2 行级删除与更严写入、v3 扩展类型与进阶能力、**v4 性能/可移/实时就绪**）/
> C.3 Snapshot management and table metadata（元数据文件/快照与清单列表/序列号与乐观并发）/
> C.4 The REST Catalog specification（概览/配置与默认端点/命名空间表视图/注册指标事务/**OAuth2 安全**/
> **scan-planning 端点**）/ C.5 Puffin file format specification（是什么/列级指标与自定义索引/与表
> 元数据的集成）/ C.6 Compatibility and migration（跨版本读写/升级路径/向后兼容实务）；
> 附录 D afterword（后记，并入本章末节）。
> ⚠️ 全章为规范骨架的架构师视角重构；字段级权威文本 → iceberg.apache.org/spec/（✅ 200 实抓）。

## 本章地图

| 小节 | 内容 | 结论（一句话） |
| --- | --- | --- |
| C.1 | 规范的角色 | 表行为被形式化成文档——多引擎实现"同一张表"的前提 |
| C.2 | 版本线 v1→v4 | v1 分析表地基；v2 行级删除+写纪律；v3 新类型/DV/row lineage；v4 面向性能与可移 |
| C.3 | 元数据结构 | metadata JSON/快照/清单/序列号四件套——乐观并发的文件侧定义 |
| C.4 | REST Catalog 规范 | 目录从实现升格为协议：端点族/OAuth2/扫描规划 |
| C.5 | Puffin | 专存"非数据"的索引/统计文件容器（DV、删除向量、列指标） |
| C.6 | 兼容与迁移 | format-version 单向升级；跨版本读写矩阵按引擎核对 |

## C.2 版本线精读（本书附录里最有"时间戳"的一节）

| 版本 | 关键引入 | 盘上深读位 |
| --- | --- | --- |
| v1 | 元数据树+快照+隐藏分区的完整地基（纯 append/overwrite） | [../Apache_Iceberg活用入門/02-元数据三层结构.md](../Apache_Iceberg活用入門/02-元数据三层结构.md) |
| v2 | **delete files**（position/equality）→ 行级 UPDATE/DELETE/MERGE 与 MoR | [../Apache_Iceberg活用入門/05-行级删除与删除文件.md](../Apache_Iceberg活用入門/05-行级删除与删除文件.md) |
| v3 | 新类型（nanosecond/variant/geo 等）、列默认值、row lineage、**deletion vector（Puffin 承载）** | 规范页在册 ✅；细节以当期 spec 为准 ⚠️ |
| v4 | 章旨：性能、可移性、实时就绪（书成时的最新规范动响 ⚠️ 特性清单未逐条核实，勿照抄任何二手总结） | 规范页导航已见 "Version 4: Metadata Structure and Representation" ✅ 实抓 |

- 架构读法：**format-version 是"表级"属性**——同库可不同版本、升级单向不可逆（C.6.2）；
  把"全库一步升 v3/v4"当 KPI 是误区，按消费引擎最短板走（C.6.1 的矩阵先摸清）。

## C.3 元数据结构（与 02 章 🔧 演示的对应关系）

- metadata JSON（编号递增不可改）、快照对象（id/parent/manifest-list/summary）、清单列表/清单文件
  的 avro 模式、**序列号（sequence number）给删除文件定序匹配**——乐观并发的"谁可见谁"由版本号裁决。
- 🔧 本机对应物：演示脚本产出的 `mini_iceberg/v3.json`（快照数组+current-snapshot-id 指针）是
  C.3.1 的手抄简化版；D1a/D1b 的可见集切换复现了"按快照+序列语义过滤清单"的骨架
  （文件：`D:\develops\tmp\dbwave_w3_icearch\demo_mini_iceberg.py`，DuckDB 1.5.5 实跑；
  **教学模仿非规范实现**，字段名不可当规范用）。
- 深读 → [../Engineering_Lakehouses_with_Open_Table_Formats/02-开放表格式的元数据布局总论.md](../Engineering_Lakehouses_with_Open_Table_Formats/02-开放表格式的元数据布局总论.md)。

## C.4 REST Catalog 规范（07 章选型题的协议底账）

- 端点族（TOC 实抓）：配置与默认端点、namespace/table/view 三类资源、表注册/指标上报/事务；
- **OAuth2**（C.4.5）：目录作为认证授权边界的标准化——07.6 访问控制的协议根；
- **scan-planning 端点**（C.4.6）：把"给查询算文件清单"从客户端下沉目录服务——规划成本与
  12 章客户端 `files` 视图的长期演化方向 ⚠️（各服务端支持子集不一，按 OpenAPI yaml 逐端点验收；
  yaml 在册 ✅ https://github.com/apache/iceberg/blob/main/open-api/rest-catalog-open-api.yaml ）。

## C.5 Puffin 规范（三种信息的新容器）

- **是什么**：面向"表附件"的容器格式（blob 族：统计、删除向量、自定义索引），与数据文件分开管理；
- 与 v3 deletion vector 的关系：DV 以 Puffin blob 承载（05/10 章 MoR 成本线的新算子）；
- 集成点：表元数据里登记引用——expire/orphan 逻辑要把 Puffin 文件计入管辖对象（10 章清理面的延伸）⚠️。

## C.6 兼容与迁移 + 附录 D 后记要点

- **跨版本读写**（C.6.1）：读端向后兼容是原则（新引擎读老表），写端升级后老引擎拒读——
  迁移窗口的检查顺序：先全消费方引擎版本清单，再动 `upgrade`；
- **升级实务**（C.6.2–3）：`format-version` 属性变更经一次元数据提交完成；回滚不在规范承诺内 ⚠️；
- **附录 D（后记）书旨重构**：收束"开放表格式=长期主义"——标准、社区、多引擎三件套胜过任何
  单平台便利；编者注：与 01 章"反锁定"首尾呼应，全书的立场句。

## 常见误区

| 误区 | 纠偏 |
| --- | --- |
| "规范=某引擎行为文档" | 规范是语言中立文本，实现（Java/Python/Go/Rust）各有特性子集——差异以 issue 追，不以传言补 |
| "v2 表能随便用 v3 特性" | format-version 决定特性门（DV/新类型属 v3+）；"混着开"会在弱实现引擎上静默降级或报错 ⚠️ |
| "REST 规范=所有端点都得支持" | 实现按子集声明（配置端点里可协商）；验收照 yaml 逐路径打勾，别按博文（07 章陷阱重述） |
| "Puffin 又是数据文件格式" | 它是**附件**容器：统计/索引/DV，不参与扫描产出——05 章 Parquet 的位置不可被它替换 |
| "升级测试=读通就行" | 要按 C.6.1 矩阵覆盖"老引擎×新表/新引擎×老表"两向；下游 BI/流任务一并入测试面 |

## 与其他章 / 其他书的联系

- 本册内：版本特性落到运维 → [10-湖仓维护.md](10-湖仓维护.md)、[11-运维化-编排审计与容灾.md](11-运维化-编排审计与容灾.md)；
  REST 端点落到选型 → [07-Catalog层实现.md](07-Catalog层实现.md)；元数据表 →
  [12-附录A-元数据表.md](12-附录A-元数据表.md)；Python 实现 → [13-附录B-Python数据生态.md](13-附录B-Python数据生态.md)。
- **规范深读的盘上主库**（本册刻意不重复）：
  [../Apache_Iceberg活用入門/02-元数据三层结构.md](../Apache_Iceberg活用入門/02-元数据三层结构.md)、
  [../Apache_Iceberg活用入門/05-行级删除与删除文件.md](../Apache_Iceberg活用入門/05-行级删除与删除文件.md)、
  [../Apache_Iceberg活用入門/06-ACID与乐观并发控制.md](../Apache_Iceberg活用入門/06-ACID与乐观并发控制.md)；
  三格式规范总论 → [../Engineering_Lakehouses_with_Open_Table_Formats/03-Iceberg表格式机制.md](../Engineering_Lakehouses_with_Open_Table_Formats/03-Iceberg表格式机制.md)。
- Paimon 的 Iceberg 兼容元数据生产（反向互操作）→
  [../Apache_Paimon_Streaming_Lakehouse/12-多引擎生态与四大湖格式对比.md](../Apache_Paimon_Streaming_Lakehouse/12-多引擎生态与四大湖格式对比.md)。

## 本章速查卡

- 版本门速记：v1 地基 / v2 删除文件 / v3 DV+新类型+行血缘 / v4 性能与可移（章旨）。
- 升级律：format-version 单向；迁移先摸"引擎×版本"矩阵再动 upgrade；回滚不在规范承诺内。
- REST=目录的协议化：端点按 OpenAPI yaml 逐路径验收；scan-planning 是规划下沉的服务化方向。
- Puffin 三件套记法：统计、索引、删除向量——数据文件之外的"表附件"统一容器。

## 核心概念速览（中英对照）

- **表格式规范** — Table Format Specification：以文档定义表行为契约、供多实现遵循的标准文本。
- **format-version** — 表级版本属性：v1/v2/v3/v4 特性门的开关，升级单向。
- **表元数据文件** — Metadata File：schema/spec/快照列表/当前指针的 JSON 根（编号递增不可改）。
- **序列号** — Sequence Number：给数据/删除文件定序匹配的并发可见性裁决轴。
- **Deletion Vector** — 删除向量：v3 起以位图标记被删行的机制，Puffin 承载。
- **Puffin** — 附件容器格式：列指标/自定义索引/DV 的文件族。
- **Row Lineage** — 行血缘：v3 引入的行级来源追踪（跨改写保身份）⚠️ 名目以规范为准。
- **Scan Planning 端点** — REST 规范中由目录服务代做文件规划的高阶端点族。
- **OAuth2（catalog）** — 目录服务的标准授权框架接口：07.6 权限的协议根。
- **声明式提交** — Declarative Commit（requirements 断言）：把"我以为的当前状态"写进提交请求。
- **跨版本读写矩阵** — Compatibility Matrix：迁移测试的覆盖清单（老×新双向）。
- **长期主义** — 后记主旨：标准+社区+多引擎的开放栈对抗平台便利的诱惑。

## 最新演进与工业实践

- **规范与实现的当期坐标（✅ 2026-09-27 实抓）**：spec 页含 v4 条目（https://iceberg.apache.org/spec/ ）；
  参考实现 apache-iceberg-1.11.0（2026-05-20，GitHub Releases API）；REST OpenAPI 文本在
  `open-api/rest-catalog-open-api.yaml` 在册（GitHub 200）。
- **v3/v4 的支持扩散（⚠️ 定性）**：DV/variant 在 Spark/Flink/Trino/DuckDB 各线的读写成熟度不齐，
  以各家当期 release notes 核对——本册 07/08/09 章"最短板引擎"原则的规范侧投影。
- **多语言实现生态**：PyIceberg（13 章）、Rust/Go 客户端与独立 catalog 服务（Polaris/Lakekeeper，
  07 章版本实抓）都在跟随规范演进——"规范文本→多实现"的健康度是 2025–2026 湖仓选型可依赖 Iceberg
  的核心论据（后记主旨的现实注脚）。
- **盘上取证复用声明**：DuckDB iceberg 扩展三态（installed/loaded/queryable）口径引
  [../DuckDB_Up_and_Running/09-云端DuckDB与MotherDuck.md](../DuckDB_Up_and_Running/09-云端DuckDB与MotherDuck.md)
  与本册 13 章 🔧；迷你元数据演示不替代任何规范验收。
