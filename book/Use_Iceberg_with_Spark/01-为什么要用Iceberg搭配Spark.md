# 01 为什么要用 Iceberg 搭配 Spark

> 章题为推断（原书 TOC 未能核实，见 [00 总览](00-总览与阅读地图.md) 的声明段）。
> 本章对应 short report 的导言职能：先讲清「Spark 自带表管理已经很能打，为什么还要一层 Iceberg」。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 1.1 | Spark 原生 Hive 表的三宗罪 | 分区即目录、无 ACID、演化几乎不可做 |
| 1.2 | 表格式（table format）在栈中的位置 | 文件层（Parquet）之上、引擎层（Spark）之下的元数据层 |
| 1.3 | Iceberg 规范能力速览 | ACID、快照、隐藏分区、演化、多引擎平权 |
| 1.4 | 三大表格式对比 | Iceberg/Delta/Hudi 的选型坐标系 |
| 1.5 | Spark-Iceberg connector 的分层 | catalog → 规划/执行 → 提交，一条写路径看懂职责 |

## 核心精讲

> 以下示例均为**教学示意，不参与构建**。

### 1.1 Spark 原生 Hive 表的三宗罪

在没有表格式的年代，Spark 管一批 Parquet 文件靠的是 **Hive Metastore + 目录约定**：

```sql
-- 教学示意：Spark 原生（Hive 风格）分区表
CREATE TABLE orders_p (
  order_id BIGINT,
  amount   DECIMAL(10,2)
) USING parquet
PARTITIONED BY (dt STRING, region STRING);   -- 分区 = 物理目录 dt=.../region=...
```

痛点（后续章节会逐个回收）：

1. **分区是物理布局，不是逻辑属性**。查询必须「知道」分区列并显式过滤
   `WHERE dt = '2025-01-01'`；如果业务列是事件时间戳 `ts`，你得手动造一个冗余的 `dt` 列写入。
   改分区方案（如按天改按小时）= 重写全表 + 通知所有下游改 SQL。
2. **没有 ACID**。`INSERT OVERWRITE` 期间的目录状态可被读到（半成品）；多写者并发直接互相踩踏；
   失败的任务留下脏数据且无法回滚。
3. **schema 变更脆弱**。Hive 的 `ALTER TABLE ADD COLUMNS` 只能加在末尾；改类型靠重建表；
   旧文件的 SerDe/列序对不上时表现为静默读出错值。

对照阅读：[../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md) 讲了 Parquet 层的自描述 schema
——但它只描述**单文件**，跨文件的表级 schema/分区一致性无人负责，这正是表格式补的位。

### 1.2 表格式在栈中的位置

```
引擎：   Spark / Flink / Trino / Spark Structured Streaming ...
          │  通过 connector 读写
表格式：  Apache Iceberg —— metadata.json → manifest list → manifest files
          │  定义「一张表是什么」：schema、分区规范、当前快照、文件清单
文件层：  Parquet / ORC / Avro（+ 删除文件：position / equality deletes）
存储层：  HDFS / S3 / GCS / ...（FileIO 抽象）
```

关键认知：**Iceberg 不搬数据、不做计算**。它是一组合规的元数据文件 + 一套规范
（[spec.md](https://iceberg.apache.org/spec/)），Spark 读表时仍然自己去扫 Parquet——只是「读哪些文件、
按什么 schema 解释」改由 Iceberg 元数据回答。

### 1.3 Iceberg 规范能力 → Spark 侧的落点

| Iceberg 能力 | 在 Spark 里长什么样 | 本目录章节 |
| --- | --- | --- |
| 原子快照提交 | `MERGE INTO` 成功即产生新快照，失败无痕 | 03 |
| 时间旅行 | `VERSION AS OF` / `TIMESTAMP AS OF` | 04 |
| schema evolution | `ALTER TABLE ... ADD/AFTER/DROP/RENAME`，不重写数据 | 05 |
| 隐藏分区 + partition evolution | 按 `days(ts)` 分区但查询只写 `ts`；换分区法不回填 | 05 |
| 独立于引擎的 catalog | 同一张表可被 Spark/Flink/Trino 共同读写 | 02 |
| 平台可维护性 | `CALL ...rewrite_data_files/expire_snapshots` | 06 |

### 1.4 三大表格式对比（选型坐标系）

| 维度 | Iceberg | Delta Lake | Hudi |
| --- | --- | --- | --- |
| 出身 | Netflix → Apache 顶级项目（2020 毕业） | Databricks（2019 开源） | Uber（2017），主打 upsert 管道 |
| 规范开放度 | 引擎中立规范最彻底；REST Catalog 成事实接口 | 协议开源但深度绑定 Databricks 生态（UniForm 在弥合） | 表内维护组件较重 |
| 元数据 | 多层 Avro manifest + 快照树（支持分支/标签） | `_delta_log` 事务日志（JSON+checkpoint） | timeline + commit |
| 隐藏分区 | ✅ transform（days/bucket/truncate…） | ❌ 生成列近似 | 部分（record key 模型） |
| partition evolution | ✅ 无回填 | ❌ | 受限 |
| Spark 集成 | `iceberg-spark-runtime`（本目录主线） | delta connector，版本随 DB 发行 | hudi-spark-bundle |

> 「Iceberg vs Delta」的完整论述超出本 report 范围；若后续建
> `book/Delta_Lake_Definitive_Guide/`，两目录在「upsert、时间旅行、优化维护」三处互为对照。

### 1.5 connector 分层：一次写操作的职责链

Spark 侧的 `iceberg-spark-runtime` 干三件事：

1. **Catalog 层**：把 `prod.db.orders` 解析成一张 Iceberg `Table` 对象（走 REST/Hive/Hadoop catalog），
   见第 02 章。
2. **规划/执行层**：作为 Spark DataSource V2 实现，向 Catalyst 提供文件切片与分区统计，把
   `WHERE ts >= ...` 翻译成 Iceberg 表达式做文件级 pruning，见第 05 章。
3. **提交层**：作业结束后通过 catalog 做**可串行化提交**（compare-and-swap 元数据指针），
   冲突则重试或报错，见第 03、06 章。

一句话总结本章：**Spark 解决「怎么算」，Iceberg 解决「算什么、算完怎么安全落地」；
connector 是两者的契约粘合层。**

## 版本与兼容性

- 写作基线：Apache Iceberg **1.11.x**（2026 年在支版本；`format-version=2` 自 1.4+ 起成为建表默认），
  Spark **3.5 / 4.x** 双主流。runtime jar 按 `iceberg-spark-runtime-<major>_<scala>` 矩阵选择，
  以 [iceberg.apache.org/releases](https://iceberg.apache.org/releases/) 为唯一权威。
- Iceberg 1.9/1.10 起提供 Spark 4.x（Scala 2.13）runtime；Spark 3.4 及更早版本已脱离支持窗口。
- 本 report（2025 出版）内容大概率基于 Iceberg 1.5–1.7 + Spark 3.5 时代；本目录示例统一标注新版本差异。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| 「Iceberg 是一种文件格式」 | 文件仍是 Parquet/ORC；Iceberg 只管表级元数据与协议 |
| 「用了 Iceberg 就不用管小文件」 | 快照隔离让写更自由，但小文件/元数据膨胀仍要定期 `rewrite_data_files`（06 章） |
| 「Iceberg 表只能被 Spark 读写」 | 表格式引擎中立；正因如此 schema/分区变更要按「多引擎消费者」纪律管理 |
| 「DELETE 语句 = 立刻物理删数据」 | MoR 模式下先写 delete file，物理清除靠后续 compaction（03/06 章） |
| 「时间旅行会永久保留数据」 | 快照会被 `expire_snapshots` 过期，旅行窗口是运维策略决定的（04/06 章） |

## 与其他章 / 其他书的联系

- 1.1 的分区痛点 → 第 05 章「隐藏分区」给出完整解法；`dt` 冗余列的写法即 [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md) 中讨论的传统分区。
- 1.2 文件层 → [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)。
- 1.5 提交层并发问题 → 数据库视角的快照隔离见 [../../db/db.md](../../db/db.md)。
- 下一站：[02-Catalog配置与接入.md](02-Catalog配置与接入.md)，先把能跑起来的环境讲完。
