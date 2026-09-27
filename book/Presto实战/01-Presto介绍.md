# 01 Presto 介绍

> 原书第 1 章（中译本 p.3–15）。定位：全书的"为什么"——Presto 解决什么问题、不解决什么问题。
> 返回 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 1.1 大数据带来的问题 | 数据量爆炸 + 存储多样化，Hive 批式延迟无法满足交互分析 | "数据在湖里，问题在分钟内" |
| 1.2 Presto 来救场 | 为性能和规模而生 / SQL-on-Anything / 存储与计算分离 | 三条设计支柱 |
| 1.3 使用场景（10 小节） | 单一 SQL 访问点、数仓访问点、SQL 化一切、联邦查询、语义层、湖查询引擎、ETL 转换、快速响应、ML/AI 供数 | 场景清单即选型依据 |
| 1.4 资源 | 官网/文档/社区/源码许可版本/本书示例数据集（鸢尾花、航班） | 学习路径入口 |
| 1.5 Presto 简史 | Facebook 2012 起步 → 2013 开源 → 2019 Presto Foundation → 2020-12 更名分叉（PrestoSQL→Trino） | 一段历史 = 两团火焰 |

## 精讲

### 1. SQL-on-Anything 的三层含义
1. **语法面**：标准 SQL（ANSI 语义为主），BI 工具与工程师都无需学新 DSL；
2. **存储面**：HDFS/S3/Cassandra/MySQL/Kafka/ES……凡有连接器皆可 JOIN，计算向数据移动而非数据搬家；
3. **规模面**：MPP 全内存流水线执行，毫秒~分钟级响应，介于"单机 DuckDB"与"批重器 Spark/Hive"之间。
这层定位在 repo 的全景表里对应"交互分析 OLAP"一格，见
[../bigdata/01-大数据技术全景.md](../bigdata/01-大数据技术全景.md)。

### 2. 存储与计算分离不是口号
- Presto 进程**不拥有数据**：无副本、无本地格式转换、无导入导出；
- 由此得到的性质：弹性扩缩（节点无状态）、多租户共享同一份湖、故障域小；
- 由此付出的代价：**远端 IO 是性能天花板**，第 6 章 Hive 连接器的文件剪裁、第 11.2 节 RubiX 缓存、第 12 章网络交换调优，全是为这个代价打的补丁。
与"存储计算分离是云原生默认形态"的当代论点互证，见
[../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)。

### 3. 联邦查询：杀手场景（1.3.4）
一条 SQL 同时查 MySQL 维表 + Hive 事实表 + Kafka 流式事件，传统架构需要 ETL 汇聚，
Presto 用连接器 + 分布式 Join 当场完成（详见第 7.6 节）。边界要记牢：
- 适合：**读侧聚合**、中小结果集点查与探索；
- 不适合：重写侧事务（无 ACID 跨源）、超大 Shuffle（网络交换非为 TB 级重排设计——第 12 章会给参数边界）。

### 4. 简史补注（书中 1.5 的当代延长线）
- 2012–2013 Facebook 内部 Dapper 时代遗留 → Scribe/Presto；2013 开源；
- 2019-09 Facebook/Uber/Airbnb 等成立 **Presto Foundation**（捐给 Linux Foundation 体系内运作）；
- 2020-12 社区分叉：**PrestoSQL 改名 Trino**（独立路线），prestodb 留在基金会（Meta 主导）——
  本书写作时（2020–2021 MEAP 期）正是分叉前后，故书中连接器/UI 截图多为 34x 版 Presto；
- 2025–2026 两线继续各自演进（见文末"最新演进"）。
⚠️ 早期历史细节（Dapper 前史等）以社区公开回忆文为准，原书仅给梗概。

## 常见误区

| 误区 | 现实 |
| --- | --- |
| "Presto 是新一代 Hive 替代" | 它替代的是**交互查询**这一段；深度 ETL/大 Shuffle 仍是 Spark/Hive 的地盘（书中 1.3.7 把 ETL 列为场景之一，工业上通常只做轻转换） |
| "有了 Presto 就不需要数仓" | 书中"虚拟数仓语义层"场景（1.3.5）恰恰说明它是访问层，不是存储层 |
| "Presto 支持事务" | 连接器决定一切；多数开源连接器无跨语句事务，写侧能力 2021 前后主要限于 Hive/Iceberg 的有限 DML |
| "版本 3xx = 稳定 API" | 连接器 SPI、REST 内部协议均快速漂移，升级即回归测试 |

## 与其他章/其他笔记的联系
- 设计支柱的机制展开 → [04-Presto的架构.md](04-Presto的架构.md)；
- "SQL-on-Anything" 的落地件 → [06-连接器.md](06-连接器.md)、[07-高级连接器实例.md](07-高级连接器实例.md)；
- 与 Spark SQL 的引擎路线对比 → [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)；
- 优化通用心法（本书仅 Presto 视角）→ [../大数据SQL优化.md](../大数据SQL优化.md)。

## 本章小结与行动清单

三句话带走：
1. Presto 的不可替代性="**湖上交互式联邦 SQL**"这一个十字；其余场景它都能被替代或替代别人；
2. 选型时先对 1.3 的十个场景打勾，再对 4 条"不适合"打叉——打叉项有实权重时，别用 Presto 当主引擎；
3. 2020-12 的分叉决定了今天读这本书的姿势：**先问发行线（prestodb/Trino），再问版本号**。

自测（学完本目录后再回答）：
- [ ] 说出"存算分离"给 Presto 带来的三个性质与两个代价（代价分别在哪几章被治理？）
- [ ] 联邦查询的三类典型事故（源库过载/计划爆炸/口径漂移）对应本目录哪些节的解法？
- [ ] Presto Foundation（2019）与 PrestoSQL→Trino 更名（2020-12）各自解决了什么矛盾？

延伸动作：
- 打开 [../bigdata/01-大数据技术全景.md](../bigdata/01-大数据技术全景.md) 的 OLAP 象限表，
  把 Presto/Trino/ClickHouse/Doris 四格各自的"甜蜜区"抄成一张对比卡（这是第 13 章选型讨论的预习）。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 交互式分析 | Interactive Analytics | 秒级反馈的人机探索式查询负载 |
| 联邦查询 | Federated Query | 一条 SQL 跨多个异构数据源联表 |
| SQL-on-Anything | SQL-on-Anything | 以标准 SQL 访问任意存储系统的口号 |
| 存算分离 | Separation of Storage and Compute | 引擎不拥有数据，计算层可独立伸缩 |
| MPP | Massively Parallel Processing | 多节点并行执行同一查询的架构族 |
| 数据孤岛 | Data Silo | 标准不一的存储系统造成的割裂 |
| 连接器 | Connector | Presto 访问外部数据源的插件 SPI |
| 湖仓 | Lakehouse | 对象存储 + 开放表格式 + SQL 引擎的新形态（2021 后成为 Presto 主战场） |
| 语义层 | Semantic Layer | BI 与引擎之间统一的业务口径定义层 |
| Presto Foundation | Presto Foundation | 2019 年成立的厂商中立治理组织 |
| Trino 更名 | Trino Rebrand | 2020-12 PrestoSQL 社区改名 Trino 的分叉事件 |
| 流水线执行 | Pipelined Execution | 算子间流式传递数据、不等物化，交互式低延迟的来源 |
| 节点无状态 | Stateless Workers | 工作节点可随时增减，数据在远端存储 |
| 查询下推 | Pushdown | 把过滤/投影交给数据源先做，减少搬运（下章预告） |

## 最新演进与工业实践

（链接均经 curl 验证可达，抓取日 2026-09；403 者注明）

- **社区分裂的当下（2024–2026）**：
  - prestodb 线：GitHub 主仓库持续高活跃，Releases 已到 **0.299**（2026-08）——
    [github.com/prestodb/presto](https://github.com/prestodb/presto)、
    [github.com/prestodb/presto/releases](https://github.com/prestodb/presto/releases)（✅ 200 实抓）；
    Presto 官网 [prestodb.io](https://prestodb.io/) ⚠️ 实抓 403（反爬），以 GitHub 为事实入口；
  - Trino 线：版本已至 **483**（trino.io 当前文档实抓）——
    [trino.io](https://trino.io/)、[trino.io/docs/current/overview.html](https://trino.io/docs/current/overview.html)、
    [github.com/trinodb/trino](https://github.com/trinodb/trino)（✅ 200）；
  - 分叉沿革报道：《PrestoSQL 项目更名为 Trino，彻底和 PrestoDB 分家》
    [sohu.com/a/441573139_315839](https://www.sohu.com/a/441573139_315839)（✅ 200）；
    Presto Foundation 成立报道（2019-09）[new.qq.com/rain/a/TEC2019092400060000](https://new.qq.com/rain/a/TEC2019092400060000)（✅ 200）。
- **湖仓 connector 成为主战场**：Iceberg 已是两家交互式分析的默认表格式——
  [iceberg.apache.org](https://iceberg.apache.org/)、[Trino Iceberg connector 官方文档](https://trino.io/docs/current/connector/iceberg.html)（✅ 200）；
  repo 湖格式三书对应：[../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md)、
  [../Apache_Paimon_Streaming_Lakehouse/12-多引擎生态与四大湖格式对比.md](../Apache_Paimon_Streaming_Lakehouse/12-多引擎生态与四大湖格式对比.md)、
  [../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md](../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md)。
- **经典论文**：Ramesh et al., *Presto: SQL on Everything*, IEEE ICDE 2019,
  DOI [10.1109/icde.2019.00196](https://doi.org/10.1109/icde.2019.00196)（✅ Crossref 200 校验）——
  本章"三条支柱"的学术表述版；论文线索引见 [../../db/db.md](../../db/db.md)。
- **国内采用公开资料**：美团技术团队早期即引入 Presto——
  [《Presto实现原理和美团的使用实践》tech.meituan.com/2014-06-16/presto.html](https://tech.meituan.com/2014-06-16/presto.html)（✅ 200）；
  B 站离线平台三引擎（Presto/Spark/Hive）路由实践——
  [dbaplus《相比Spark和Hive，选Presto做查询简直不要太香！》](https://dbaplus.cn/news-73-4481-1.html)（✅ 200）；
  小红书在线查询场景中 Presto 承担 Ad-hoc 交互式查询（厂商案例转述）——
  [腾讯云开发者社区 EMR 支撑小红书](https://cloud.tencent.com/developer/article/2704655)（✅ 200；⚠️ 云厂商转述，非小红书一手发布）。
- **工业提醒**：2024 后选型必写清"prestodb 还是 Trino"——两家的 Iceberg 版本支持、DML 能力、原生执行（Velox）路线已不同名同义（参
  [../Apache_Iceberg活用入門/09-Spark_Flink_Trino实战.md](../Apache_Iceberg活用入門/09-Spark_Flink_Trino实战.md) 的分叉告诫）。
