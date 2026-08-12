# starrocks

https://github.com/StarRocks/starrocks

linux基金会的项目

华为的

抄袭 百度 Apache Doris
如何评价StarRocks开源？
https://www.zhihu.com/question/485718919/answer/2967555685?utm_psn=1704150981976231938

Linux基金会项目StarRocks是新一代极速全场景MPP数据库，遵循Apache 2.0开源协议。
面世三年来，StarRocks致力于帮助企业构建极速统一的湖仓分析新范式，是实现数字化转型和降本增效的关键基础设施。目前，全球380家以上市值超过70亿元人民币的顶尖企业选择用StarRocks来构建新一代数据分析能力，这些企业包括腾讯、携程、平安银行、中原银行、中信建投、招商证券、大润发、百草味、顺丰、京东物流、TCL、OPPO等。StarRocks也已经和全球云计算领导者亚马逊云、阿里云、腾讯云等达成战略合作关系。
StarRocks全球开源社区也正飞速成长。目前，StarRocks的GitHub star数已达8200，吸引了超过350位贡献者和数十家国内外行业头部企业参与共建，用户社区也有过万人的规模。凭借其卓越的表现，StarRocks荣获了全球著名科技媒体InfoWorld颁发的2023BOSSIEAward最佳开源软件奖项。

## StarRocks 综合笔记（截至 2026-08）

### 定位与版本边界

StarRocks 是面向实时分析、交互式 OLAP、湖仓查询和高并发报表的 MPP 列式分析数据库，兼容 MySQL 协议并支持 SQL。它适合大规模明细、宽表、聚合、多维筛选和复杂 Join；不应直接替代 MySQL/PostgreSQL 等 OLTP 主库来承载单行强事务订单系统。

截至 2026-08-12，官方文档 Latest 为 4.1，4.1.1 发布于 2026-05-29。生产环境应使用目标版本最新补丁，不能把“大版本最新”直接等同于可直接升级：官方说明容器环境不要使用存在启动问题的 4.1.0，应使用 4.1.1；升级到 4.1 后不能回退至低于 4.0.6 的版本。

| 需求 | 适配性 | 关键前提 |
| --- | --- | --- |
| 实时看板、用户画像、指标查询 | 高 | 合理分区/分桶，控制 Join shuffle 和高基数聚合。 |
| Kafka/Flink CDC 实时数仓 | 高 | 明确主键、乱序/删除、幂等、checkpoint 和对账。 |
| Hive/Iceberg/Hudi/Delta/Paimon 湖上分析 | 高 | 外部 Catalog、元数据刷新、文件布局与缓存需要治理。 |
| 订单、支付等 OLTP 主库 | 低 | 需要复杂事务/外键/细粒度冲突处理时优先 OLTP。 |
| 向量召回 | 试验性 | 向量索引仍为 Beta，先验证召回率、成本与部署限制。 |

官方入口：

- 架构：https://docs.starrocks.io/docs/introduction/Architecture/
- 4.1 发布说明：https://docs.starrocks.io/releasenotes/release-4.1/
- GitHub 发布页：https://github.com/StarRocks/starrocks/releases

### 架构：FE、BE、CN 与两种部署模式

FE（Frontend）负责连接、元数据、SQL 解析、优化、计划和调度。存算一体模式使用 BE（Backend）执行查询并保存本地数据；存算分离模式以 CN（Compute Node）替代 BE，CN 只负责计算和热点缓存，数据放在对象存储或 HDFS。

```text
MySQL/JDBC/BI/Flink/Kafka
            |
            v
FE: 元数据、优化器、调度、认证
            |
     MPP fragments / Exchange
            |
  +---------+----------------+
  |                          |
  v                          v
BE: 本地存储 + 计算       CN: 计算 + 本地缓存
shared-nothing            shared-data + 对象存储/HDFS
```

| 模式 | 组成 | 优点 | 主要代价 |
| --- | --- | --- | --- |
| 存算一体（shared-nothing） | FE + BE | 本地数据路径短，热数据低延迟，多副本可用 | 扩缩容通常涉及数据均衡和副本管理。 |
| 存算分离（shared-data） | FE + CN + 对象存储/HDFS | 存储低成本、计算弹性、CN 增减无需搬迁主数据 | 冷数据受远端存储、文件布局和缓存命中影响。 |

存算分离并非没有本地盘：CN 使用内存和本地磁盘作为多级缓存，缓存命中时性能可接近存算一体。对象存储带宽、请求费用、跨地域网络、缓存预热和生命周期策略都应进入容量与成本模型。

FE 高可用依赖元数据复制和选主：Leader 处理元数据写，Follower 参与选主，Observer 可扩展查询服务但不参与选主。生产应按多数派规划 Follower 的数量和跨可用区部署；不要单 FE 后再谈 HA。两种部署模式不支持原地互转，架构选择要在迁移方案中明确。

### MPP 执行与性能思维

MPP 将 SQL 拆为多个 fragment，在多个节点并行扫描、过滤、局部聚合、Join，再经 Exchange 重分布或汇总。列式存储、向量化、Pipeline 执行和 CBO 共同服务于分析查询，但是否高效主要取决于读取量和网络交换量。

| 操作 | 高效条件 | 常见风险 |
| --- | --- | --- |
| 扫描/过滤 | 分区裁剪、谓词下推、只读取必要列 | 低选择性条件、读取大 JSON、统计信息失真。 |
| 聚合 | 先局部聚合，再合并 | 高基数 `GROUP BY` 放大中间状态。 |
| Join | colocate 或小表广播 | 大表 shuffle、倾斜、误广播大维表。 |
| 排序/窗口 | 局部排序后合并 | 全局排序、深分页、单分区热点。 |

排查 SQL 不要只看耗时：用 `EXPLAIN`/`EXPLAIN VERBOSE` 看分区裁剪、Join 分发和 Exchange，用 `EXPLAIN ANALYZE`/profile 对照估算和实际扫描行数、内存、spill、网络数据量。优化优先级是减少扫描和重分布，其次才是扩机器。

### 数据建模：表模型、分区、分桶、排序

| 表模型 | 主要语义 | 合适场景 | 注意事项 |
| --- | --- | --- | --- |
| Duplicate Key | 保留重复明细，不做键约束 | 日志、行为事件、可回放原始数据 | 去重语义需由查询或上游明确。 |
| Primary Key | 主键唯一非空，支持实时 Upsert/Delete/部分更新 | 实时状态表、维表、CDC 宽表 | 更新热点、主键宽度和 compaction 必须压测。 |
| Unique Key | 键唯一，Merge-On-Read | 低频更新、读时去重 | 查询可能承担合并代价。 |
| Aggregate Key | 同 Key 的指标按聚合类型预聚合 | 固定维度的汇总指标 | 更省查询成本，但维度演进不灵活。 |

Primary Key 表的更新路径与 Unique Key/Aggregate Key 的 Merge-On-Read 不同，适合更强实时更新需求，但不是“无限免费更新”。高频更新、单热点 key、无界小批写入都会放大主键索引、版本和 compaction 压力。

建模顺序：先定义一行数据的事实粒度，再选表模型；按时间范围分区以支持裁剪、TTL 和增量刷新；按均匀且常用的 Join/聚合键分桶，避免低基数和热点租户；再选择 `ORDER BY` 排序键，最后才针对明确工作负载评估索引或物化视图。不要把每个查询字段都放进排序键或每列都建索引。

索引是以存储、写入和 compaction 成本换查询性能。排序/前缀索引、Bitmap、Bloom Filter、倒排索引和向量索引目标不同。倒排索引可覆盖部分文本/过滤检索，不等同于搜索引擎的完整相关性与生态能力。

向量索引截至该时间点仍为 Beta，仅支持 shared-nothing 的 v3.4+，支持 HNSW 和 IVFPQ，且每表仅一个向量索引。它适合“向量相似度 + 结构化过滤”的 POC；需独立评估召回率、索引构建、内存/磁盘、更新成本和过滤选择性，不应直接承诺核心生产 SLA。

官方参考：

- 表模型：https://docs.starrocks.io/docs/table_design/StarRocks_table_design/
- Primary Key：https://docs.starrocks.io/docs/table_design/table_types/primary_key_table/
- 向量索引：https://docs.starrocks.io/docs/table_design/indexes/vector_index/

### 实时导入、CDC 与事务边界

| 方式 | 场景 | 实践重点 |
| --- | --- | --- |
| Stream Load | 应用/API 推送小中批数据 | 使用 label 跟踪和幂等，控制批次大小与并发。 |
| Routine Load | 持续消费 Kafka | 长运行 load job 切分为 task；官方提供 exactly-once 载入语义。 |
| Flink Connector | 流计算与 CDC | 对齐 checkpoint、sink 语义、主键表与 schema 演进。 |
| Broker/对象存储/HDFS 导入 | 离线文件批量装载 | 检查文件大小、格式、分区和失败重跑。 |
| `INSERT`/CTAS | ELT、湖表转内表 | 与交互式 BI 做资源隔离。 |

Routine Load 的 exactly-once 只覆盖该加载作业进入 StarRocks 的目标语义。端到端是否 exactly-once 还取决于 CDC 事务边界、Kafka offset、Flink checkpoint、乱序/重复事件、DDL 变更和下游消费。CDC 写入 Primary Key 表时，必须提前定义 update-before/update-after、delete、重放和事件顺序的映射规则。

StarRocks 支持 SQL Transaction，可在内部原子提交多条 DML 和多表 DML；Stream Load transaction interface 自 v2.4 支持面向 Flink/Kafka 的 2PC 接口，自 v4.0 支持同一数据库多表事务加载。4.1 中 SQL Transaction 默认受会话变量 `enable_sql_transaction` 控制。这些能力只保证 StarRocks 内部写入，不自动覆盖外部 MySQL、消息、HTTP 或跨服务流程；仍需 outbox、业务唯一键、幂等消费、对账和补偿。

建议把“原始 CDC 事件表”和“实体最新状态表”分开：前者可回放、对账，后者使用 Primary Key 加速查询。持续小批写入会造成小 rowset 和 compaction 积压，应监控导入延迟、失败重试、Kafka lag、版本发布、compaction、磁盘/对象存储和主键热点。

官方参考：

- 导入：https://docs.starrocks.io/docs/loading/
- Routine Load：https://docs.starrocks.io/docs/loading/RoutineLoad/
- Stream Load 事务：https://docs.starrocks.io/docs/loading/Stream_Load_transaction_interface/

### 异步物化视图：查询加速与数据新鲜度

同步 MV（Rollup）主要面向单表有限聚合的加载时维护；异步 MV（ASYNC MV）更通用，可基于内部表、部分外部表、已有 MV 或视图构建，支持自动/定时/手动刷新和透明查询改写。

适用场景：高频重复聚合、多张宽表反复 Join 后的指标层、湖上固定报表预计算、近期热分区与历史基表的热冷分层。MV 不是“建完必然加速”：优化器只在结果一致性、新鲜度和查询形状满足条件时改写，刷新本身也消耗计算与 I/O。

| 场景 | 建模建议 | 验证项 |
| --- | --- | --- |
| 内部表指标 | 基表与 MV 按时间分区，增量刷新 | `EXPLAIN` 是否命中、刷新延迟、分区 TTL。 |
| 湖上固定报表 | 外部 Catalog MV | 元数据刷新、成本、数据新鲜度和回退路径。 |
| 复杂 SQL | 先看计划，再尝试 SPJG 或文本匹配改写 | 不能只因 MV 存在就假设会改写。 |
| 不容忍陈旧读 | 直接查基表或严格配置一致性 | 不要默认接受 staleness。 |

内部原生表的透明改写会排除与基表不一致的 MV，以保证改写结果一致；外部 Catalog 的数据变化无法总被 StarRocks 感知，不能默认有同样保证。JDBC 和 Hudi 外部表上的 MV 有特定改写限制，升级和建模前要查当前 Feature Support。

用 `SHOW MATERIALIZED VIEWS`、`SHOW CREATE MATERIALIZED VIEW`、`information_schema.materialized_views`、tasks/task_runs 观察定义、刷新和失败；为 MV 刷新指定资源组，避免 ETL 影响看板。

官方参考：

- 异步 MV：https://docs.starrocks.io/docs/using_starrocks/async_mv/Materialized_view/
- 查询改写：https://docs.starrocks.io/docs/using_starrocks/async_mv/use_cases/query_rewrite_with_materialized_views/

### 湖仓、Catalog 与联邦查询

External Catalog 可用于 Hive、Iceberg、Hudi、Delta Lake、Paimon、JDBC、Elasticsearch 等外部源；数据通常位于 HDFS/对象存储，元数据来自 HMS、Glue 或对应 catalog。Unified Catalog 自 v3.2 引入，官方标记为 Beta，用于将多种湖表格式作为统一数据源访问。

```text
对象存储/HDFS + Hive Metastore/Glue/Catalog
        |
        v
StarRocks External Catalog
  +-- 直接查询（不导入）
  +-- INSERT INTO/CTAS 导入内表
  +-- 异步 MV 预计算加速
```

少搬数据不等于没有数据治理。跨源 Join 可能拉取大量数据并重分布，性能和费用不同于内表 Join。设计时必须明确：事实源在湖还是 StarRocks 内表；catalog/partition 的可见延迟；Parquet/ORC 文件大小和小文件问题；对象存储、metastore、KMS 的最小权限；哪些查询直读湖、哪些经 MV 或导入内表，以及缓存失效/湖表故障的降级路径。

官方参考：

- 湖仓：https://docs.starrocks.io/docs/integrations/data_lakes/
- Unified Catalog：https://docs.starrocks.io/docs/data_source/catalog/unified_catalog/
- External Catalog：https://docs.starrocks.io/docs/sql-reference/sql-statements/Catalog/CREATE_EXTERNAL_CATALOG/

### 资源隔离、运维与升级

一套集群往往同时运行看板短查询、Ad Hoc、ETL/ELT、导入和 MV 刷新。资源组、查询队列、内存管理与 spill 用于避免大查询耗尽 CPU/内存：

| 能力 | 作用 | 原则 |
| --- | --- | --- |
| Resource Group | 按用户/角色/库/IP/查询类型分配 CPU、内存、并发 | BI、ETL、MV 刷新分组并设置上限。 |
| Query Queue | 资源或并发达到阈值时排队 | 设置队列超时并告警，不能无限排队。 |
| Big Query 限制 | 限制扫描行数、CPU 时间、内存 | 基于审计日志分位数设置，而不是拍脑袋。 |
| Spill | 中间结果落磁盘/对象存储以避免 OOM | 是保护措施，持续 spill 要回查 Join/聚合。 |

Resource Group 自 v3.1 默认启用，v3.3.5 起支持 CPU 硬限制；4.1 中 `query_queue_v2` 默认开启。可根据审计日志的 CPU 时间、内存、扫描行数、并发和错误率反推配置，生产前必须压测。

4.1 重点包括 shared-data 的范围分布与 Tablet 自动 split/merge，用于缓解热点和倾斜；大容量 Tablet 的并行导入、Primary Key 更新与 compaction；Fast Schema Evolution V2；默认优化的 ETL 执行模式。升级前要在近似数据分布的环境比较计划、P95/P99、内存、spill、compaction、缓存命中、导入延迟和 Connector 行为，并准备符合版本回退边界的备份/恢复预案。

排障顺序：

1. 看板慢：运行中查询、资源组/队列、缓存、热点分区、MV 是否命中。
2. OOM/spill：Join 分发、聚合基数、单查询内存和并发，不要只加内存。
3. 导入积压：load job、Kafka lag、版本发布、compaction、小批写入和主键热点。
4. shared-data 冷查询慢：缓存命中、对象存储延迟/带宽、文件布局、跨地域网络。
5. 数据倾斜：分桶/分区键、租户热点、Tablet 大小和范围分布。

日常应监控 FE 选主和节点健康、BE/CN 磁盘、导入成功率/延迟、查询 QPS/P95/P99/错误率、资源组队列、内存/spill、compaction backlog、缓存命中、对象存储错误、MV 刷新和外部 catalog 状态。关键报表应保留 SQL、基线计划与时延，升级或模型变更后自动对比。

官方参考：https://docs.starrocks.io/docs/administration/management/resource_management/resource_group/

### POC、面试与学习路径

POC 不能只跑单表 `COUNT(*)`。应使用真实数据倾斜和真实并发，至少验证：

1. Duplicate Key 明细、Primary Key 当前状态、分区异步 MV 指标层三种模型。
2. CDC 的重复、乱序、删除、重放、断点恢复和与源库对账。
3. 多表 Join、窗口函数、Top N、深分页、湖表查询及 BI 并发下的 Exchange、scan、spill、缓存命中。
4. 导入、查询、MV 刷新同时运行时的资源隔离。
5. FE leader、BE/CN、对象存储、Kafka、metastore 故障后的 RPO/RTO、告警和恢复。
6. 存算一体 SSD/副本成本，与 CN+对象存储+缓存的网络、请求、备份和运维成本。

常见问答要点：

- **FE/BE/CN？** FE 管元数据/优化/调度；BE 在存算一体中存储并执行；CN 在存算分离中执行并缓存。
- **Primary Key vs Unique Key？** 前者面向实时更新和部分更新，后者 Merge-On-Read；按更新频率、查询延迟和 compaction 代价选。
- **实时数仓？** 不能只答“Flink CDC -> StarRocks”，还要说明事件语义、主键、幂等、乱序、MV、资源隔离和对账。
- **MV 未命中？** 看查询形状、分区映射、刷新状态、一致性条件，用 `EXPLAIN` 验证。
- **存算分离为何仍要缓存？** 对象存储提供容量和弹性，本地缓存降低热点远端 I/O；缓存命中决定实际性能与成本。

学习顺序：先读 [MPP架构](MPP架构.md)、[Doris](doris.md) 了解共同背景；完成官方 shared-data Quick Start，再实现一个导入任务和异步 MV；结合 [数据仓库与OLAP实践教程](../book/数据仓库与OLAP实践教程.md) 与 [数据库综合笔记](../db/db.md) 补齐维度建模、事务和分布式一致性；最后选择 Primary Key + CDC、Iceberg 湖查询加速、资源组多租户或 shared-data 缓存成本中的一个专项深入。

最终应能写出可运行设计，而不是只记功能列表：数据从哪里来、哪张表是事实源、怎样去重/更新、哪些查询使用 MV、资源怎样隔离、故障后如何恢复和对账。
