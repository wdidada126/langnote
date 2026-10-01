# 07 · AWS 生态协同：Redshift、S3 与大数据管道

> 章题 ⚠️ 推定（重构依据：✅ 官方导读句「Work closely with AWS services such as Redshift, S3, and MapReduce so they collaborate with DynamoDB efficiently」，见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §2/§6）。三态：✅ 实证 / ⚠️ 转述推定 / 🔧 本机类比实测（**非 DynamoDB 行为**）。

## 1. 章定位：单键库如何嵌入数据栈

- DynamoDB 官方自我定位「NoSQL 快速 KV，不适合分析扫描」✅（Introduction.html 明言其面向事务性 KV 访问 ⚠️ 措辞转述）。
- 因此生态协同承担三件事 ⚠️：归档/成本下沉、OLAP 查询补位、管道触发。
- 导读点名三服务=2014 数据栈三件套：**Redshift（仓）/ S3（湖）/ MapReduce（EMR 计算）** ✅ 在场。
- 谱系对位（写前 ls 验名 ✅ 在盘）：湖仓现状见 `book/Data_Lakehouse_in_Action` 等目录版（波8-9 产物）——本章 2014 视角 vs 波次湖仓视角互读。

## 2. 三条经典通道（2014 面 ⚠️ → 2026 面 ✅/⚠️）

### 2.1 导出侧（DynamoDB → 分析层）

- 2014：EMRDynamoDBInputFormat 直接以表作 mapper 输入；或 Scan 全表自写落 S3 ⚠️（本书「MapReduce」句 ✅ 概念在场）。
- 2014→2015 过渡：Data Pipeline 的 DynamoDB→S3 备份导出 ⚠️。
- 2026 ✅：原生**导出到 S3**（S3DataImport.html 同族页）；湖仓模式=导出落 lake→Athena/Redshift Spectrum 查询 ⚠️ 转述。
- EMR Hive/Pig DynamoDB 存储处理器：**已废弃** ⚠️（文档横幅口径，curl 200 ✅ 见文末锚）。

### 2.2 载入侧（数据 → DynamoDB）

- 2014：EMR 作业写回、自写批量灌入器、Data Pipeline ⚠️。
- 2026 ✅：原生**从 S3 导入** ✅（S3DataImport.html）——把本书时代「百万次 BatchWrite」的容量灾难变成对象存储批作业 ⚠️ 定性。

### 2.3 触发侧（变更 → 下游）

- 2014 前史：Scan+时间戳轮询 ⚠️。
- 2013 出生、本书成书窗口内：**Streams** ✅（Streams.html）——变更日志流；Lambda 触发（2014-11 发布，恰在书出版前后 ⚠️ 覆盖存疑）。
- 2017 ✅：**KDA/Kinesis Data Analytics 直连 Streams** 查询（kda.html）⚠️ 用途口径转述；2023 后该产品线收缩 ⚠️。
- EventBridge 管道、零 ETL 同步至 Redshift/SageMaker Lakehouse ✅ 页存在（2023/2024 ⚠️ 年代）。

## 3. Streams 专段（本章的「本书未尽之言」⚠️）

- 流视图四种（NEW_IMAGE/OLD_IMAGE/NEW_AND_OLD_IMAGES/KEYS_ONLY）⚠️→✅ 口径。
- 保留 24h、分片继承分区键 ⚠️。
- 消费端职责：checkpoint、分片分裂遍历、乱序容忍 ⚠️——「变更捕获语义靠消费者」是本章最工程化的告诫 ⚠️。

## 4. 成本与一致性边界 ⚠️+✅

- 跨系统一致性=异步+对账，无分布式事务 ⚠️（事务 API 也仅限 DynamoDB 域内 ✅ transactions.html）。
- Scan 导出与在线流量抢配额 → 错峰/导出通道 ✅（S3 导出旁路扫描）。
- 湖侧 schema 演化交给列式文件与外部表 ⚠️（联动 `book/Data_Lakehouse_in_Action` 谱系）。

## 5. 🔧 本机类比实验（SQLite 3.45.3 / DuckDB 1.5.5；**非 DynamoDB 行为**）

| 组 | 实验与真实输出 | 类比点 |
|---|---|---|
| T3 | 触发器审计表捕获 INSERT：`streamlog=[('INSERT','o3#c3',ts)]` | Streams 变更日志形状（本机以触发器替 ⚠️） |
| D17 | 表→CSV→DuckDB `read_csv_auto` 读回；`COPY TO 'd17.parquet'`（450B，回读 3 行） | 导出到 S3→湖/仓管道 |
| D2 | `UNNEST(STRUCT{tags:[…]})` 数组展开 | 分析侧 flatten 与文档型源的衔接 |
| D19 | 过期行按谓词排除（exp>now→仅 'fresh'） | TTL 的本机替身（真 TTL ✅ 页存在） |

## 6. 2014 数据栈三件套的 2026 结局（考古表 ⚠️，锚 ✅）

| 2014 | 2026 |
|---|---|
| EMR + MapReduce 直读表 | EMR 仍在，DynamoDB 存储处理器废弃 ⚠️；批分析让位 S3 导出+查询引擎 ⚠️ |
| Redshift 为唯一「仓」 | Redshift 存续+零 ETL 直连 ✅（zero-etl URL）；Athena/Glue 补湖侧 ⚠️ |
| Data Pipeline | 退役 ⚠️ |
| 手工归档 | TTL 原生删除 ✅（ttl.html） |
| 轮询消费 | Streams+Lambda/EventBridge/KDA ✅ 页存 |

- 读法：本章三通道里**两条（原生 S3 导入导出、零 ETL）在本书出版后十年出现**——精读时应以 ⚠️ 标注「本书不可能写到」，以免把演进物误归原书。

## 7. 与波次湖仓谱系的接口

- `book/Data_Lakehouse_in_Action`、`book/Practical_Lakehouse_Architecture`、`book/The_Data_Lakehouse`（波8-9 在盘，写前 ls 已验名 ✅）承接「导出之后」的湖侧故事。
- 盘上 DynamoDB 侧纵深：[../Amazon_DynamoDB_TDG/00-总览与阅读地图.md](../Amazon_DynamoDB_TDG/00-总览与阅读地图.md) 07/08 章（Streams 集成、Global Tables，2022 API 版，✅ 实链）。
- 本册生态章与 #113 生态章共同回答「单键库的数据去向」——2014 答 EMR/Redshift，2026 答 S3 原生/零 ETL ⚠️。

## 8. 挂点

- 前置 [04-分片与容量规划.md](04-分片与容量规划.md)（抢配额问题）、[06-API集成与数据格式.md](06-API集成与数据格式.md)（格式交换底座）。
- 全书收束：本册主线「访问模式→键→索引→容量→读写→集成→生态」止于此。

## 9. 通道选择决策清单（2026 版 ⚠️+✅）

1. 一次性全量进湖 → 原生导出 S3 ✅（免烧 Scan 配额）。
2. 历史数据回灌 → 原生导入 S3 ✅（免烧 WCU）。
3. 近实时进仓 → 零 ETL 集成 ✅/⚠️ 年代。
4. 变更驱动微批 → Streams+Lambda/EventBridge ✅ 页存。
5. 窗口聚合流分析 → kda 线 ✅ 存在/⚠️ 2026 现状存疑登记。
6. 超 400KB 对象 → S3 主存+DynamoDB 元数据索引 ⚠️ 标准模式。
7. 过期清理 → TTL ✅。
8. 跨区读就近 → Global Tables ✅。
9. 全键都答不了的临时分析 → 别 Scan 生产表，导出去湖侧跑 ⚠️。
10. 拿不准 → 默认「批导出」而不是「在线扫」⚠️。

## 10. 本章三态小结

- ✅：Streams/kda/S3 导入导出/GlobalTables/零 ETL/EventBridge/TTL 七组官方页 curl 200（台账 §7）。
- ⚠️：EMR 存储处理器废弃、Data Pipeline 退役、KDA 线收缩、各能力年代。
- 🔧：D17 导出-读回链、T3 触发审计、D2 flatten、D19 TTL 替身——四组全部标注**非 DynamoDB 行为**。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
|---|---|---|
| 变更数据流 | DynamoDB Streams | 24h 变更日志，视图四档 ⚠️→✅ |
| 流消费 | stream shard iterator | 分片遍历+checkpoint 自理 ⚠️ |
| 触发分析 | Kinesis Data Analytics for DynamoDB Streams | 服务端 SQL 消费 ✅ kda.html |
| 湖仓导出 | DynamoDB export to S3 | 原生批量导出 ✅ 2022 ⚠️ 年代 |
| 批量载入 | DynamoDB import from S3 | 免烧 WCU 的入口 ✅ S3DataImport.html |
| 零 ETL | zero-ETL integration | 到 Redshift/SageMaker 近实时 ✅/⚠️ 2023-24 |
| 事件总线 | EventBridge pipe | 轮询替代品 ✅/⚠️ 2019 |
| TTL 归档 | time to live (TTL) | 原生过期删除 ✅ |
| 全局多活复制 | global tables | 跨区最终一致 ✅（→ [00-总览与阅读地图.md](00-总览与阅读地图.md) §8） |
| 湖侧 schema | columnar external table | Parquet/Glue Catalog 接管 ⚠️ |

## 最新演进与工业实践

- 文档锚 ✅（curl 200，台账 [00-总览与阅读地图.md](00-总览与阅读地图.md) §7）：
  - `https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html`
  - `https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/kda.html`
  - `https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/S3DataImport.html`
  - `https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html`
- 产品考古 ⚠️：EMR Hive/Pig DynamoDB 存储处理器已废弃（文档横幅口径）；Data Pipeline 退役；Streams 之上 Lambda（2014-11）与 EventBridge（2019）先后成为默认消费者 ⚠️ 年代。
- 原生批量面 ⚠️+✅：S3 导入/导出（2022）、零 ETL→Redshift（2023）/→SageMaker Lakehouse（2024）、IVT 表间复制（2024）——本章三通道在十年后被官方「批+流」双轨接管。
- 工业实践 ⚠️：热数据 DynamoDB+冷数据 S3 湖+仓侧联邦查询的三层标准布局；归档以 TTL+导出组合替代自建轮询作业；跨系统一致性靠幂等键+对账而非分布式事务（与 [06-API集成与数据格式.md](06-API集成与数据格式.md) 联动）。
