# 第 1 章 数据湖仓与 Apache Hudi 导论

> ⚠️ 诚实声明：本章的**英文章题与小节目录未逐字核实**（掘金翻译系列未单独翻译第 1 章）。
> 本章主题依据第 2 章开篇对第 1 章的转述（数据湖演进为湖仓、Hudi 生态位、架构总览与核心能力）+ 豆瓣内容简介重建；
> 机制内容全部以 hudi.apache.org 官方文档为准，不伪造书中原文。

## 本章地图

> 一句话：**数据湖解决了"存得下"，没解决"改得动、查得准"；Hudi 把数据库的事务语义（ACID、record 级 upsert、时间旅行）下沉到对象存储上的 Parquet 文件群之上，形成开放湖仓。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 1.1 数据湖的困境 | 裸 Parquet/ORC 表：不可变、无事务、小文件、难 UPDATE | "lake 只能 append，业务需要 change" |
| 1.2 湖仓的兴起 | Lakehouse = 湖的成本 + 仓的语义；开放表格式三件套 | 表格式（table format）是湖仓的地基 |
| 1.3 Hudi 的生态位 | 增量管线 + 变更数据集管理，源自 Uber 2015 | "Hudi = Hadoop Upserts Deletes and Incrementals" |
| 1.4 架构总览 | timeline / 文件布局 / 索引 / 表服务 / 引擎集成五层 | 一切能力都是 timeline 事务的推论 |
| 1.5 核心能力清单 | ACID、upsert、增量查询、CDC、表服务、多引擎 | 每项能力对应后面一章 |
| 1.6 竞品坐标 | vs Hive 表、vs Iceberg、vs Delta Lake | 差异在"索引 + 表服务 + Streamer" |

## 核心精讲

> **教学示意，不参与构建。** 本节不搭真实 Hudi 集群，SQL/配置仅供理解。

### 1.1 数据湖的困境：为什么裸文件不够

典型的数据湖（HDFS/S3 上的 Hive 表）有四座大山：

1. **不可变假设**：Hive 表只有 INSERT OVERWRITE 整分区这一种"更新"。改 1 亿行里的 1 万行 = 重写 1 亿行。
2. **无原子性**：Spark 作业写一半失败，目录里就是一半脏文件；下游读到的分区可能永远不完整。
3. **读放大与写放大并存**：查询侧没有可靠的 min/max 统计利用约定（分区裁剪之外）；写入侧每天几百个 task 各写几个 KB 级文件。
4. **没有"自昨天以来变了什么"的答案**：全量快照对比（diff 两张 10TB 表）是最常见也最昂贵的 ETL 原语。

```text
裸湖的更新 = 重写全分区：
  partition=2026-09-01/  part-000.parquet (3GB)
  → INSERT OVERWRITE 读 3GB、算、写 3GB，中途失败则分区损坏
```

### 1.2 湖仓：在对象存储上重新发明数据库的一小截

Lakehouse 的定义性特征（业界共识，官方文档同样按此叙事）：

- **开放格式**：数据仍是 Parquet/ORC/Avro，表格式只加**元数据层**，引擎可绕开 Hudi 直接读文件（只是丢事务视图）。
- **ACID on blob store**：多引擎并发读写下不出现"半提交"。Hudi 的实现 = 不可变文件 + 原子发布（timeline）。
- **BI + ML + 流** 统一：同一份数据支持交互式 SQL、批 ETL、增量消费和（第 10 章的）特征/知识库。

对象存储的三条物理约束决定了所有表格式的设计空间：
`list 慢且最终一致`、`rename 非原子（S3）`、`无文件级锁`。
Hudi 的对策：元数据全部集中在 `.hoodie/` 下的**小文件集合（timeline）**，发布事务 = 写一个 completed instant 文件 + 原子可见性靠"最后一次写入"（详见 02 章与 07 章）。

### 1.3 Hudi 的生态位与历史

- 2015 年生于 Uber（工程博客《Uber's Big Data Modernization》脉络），名字即能力清单：**H**adoop **U**pserts **D**eletes and **I**ncrementals。
- 2019 年 ASF 孵化毕业为顶级项目；Onehouse（2021，由 Hudi 创始团队创立）是主要商业推力，本书作者三位来自 Onehouse/Uber 的 PMC。
- 1.0.0（2024-12 正式发布）是本书的版本基线：metadata table 默认开启、record index 成为推荐索引、hudi-rs/hudi-python 进入官方能力面。🔧

两个使用面（官方文档同样二分为 "pipelines" 与 "analytics"）：

| 使用面 | 诉求 | Hudi 对应特性 |
| --- | --- | --- |
| 增量管线 | 低延迟 upsert、断点续传、分层加工 | Streamer、incremental query、CDC mode |
| 分析湖仓 | 即席查询、时间旅行、回滚 | 快照/优化查询、clustering、data skipping |

### 1.4 架构总览：五层看 Hudi

```text
┌ 引擎层    Spark / Flink / Trino / Hive / Kafka Connect / hudi-rs …
├ 表服务层  compaction · clustering · cleaning · archival · indexing（第 6 章）
├ 索引层    record/bloom/simple/bucket/partition + metadata table（第 5 章）
├ 事务层    timeline：requested → inflight → completed（第 2、7 章）
└ 存储层    分区目录 + file group（base file + log files）（第 2 章）
```

- **事务层是脊柱**：rollback、savepoint、增量查询、并发控制，全部是 timeline 上 instant 序列的不同读法。
- **索引层是写侧咽喉**：upsert 快不快，只取决于"这条 key 属于哪个 file group"这个查找问题（第 5 章展开）。
- **表服务层是读侧还债**：MOR 的 log 文件、小文件、过期快照，都由后台任务偿还（第 6 章）。

### 1.5 核心能力 → 章节索引

| 能力 | 机制一句话 | 对应章 |
| --- | --- | --- |
| 记录级 upsert/delete | 索引定位 file group + merge 重写或追加 log | 03 |
| 快照读 | 每个 commit instant 绑定一组文件的"清单" | 02、04 |
| 时光回溯 | 按 instant time / date 选历史快照 | 04 |
| 增量查询 / CDC | 两个 instant 区间内的差分文件清单（+ log 合并） | 04 |
| 并发写 | OCC 三阶段提交 + lock provider | 07 |
| 端到端摄取 | Hudi Streamer：checkpoint 驱动的微批 | 08 |
| 布局治理 | 小文件合并、排序聚簇、清理、归档 | 06 |
| 运维 | CLI / 表操作 / catalog sync / 指标 | 09 |

### 1.6 竞品坐标（对照记忆，勿当优劣结论）

- **vs Iceberg**：Iceberg 以"隐藏分区 + 演进型分区 + 规范"见长，元数据是完整文件树清单（manifest），读规划极快；Hudi 以**写侧索引 + 内置表服务 + Streamer**见长，upsert/CDC 管线开箱即用。
- **vs Delta Lake**：Delta 事务日志 `_delta_log` 每版本一个 JSON，与 Spark 生态耦合最深；Hudi 的 timeline 是"动作"模型（commit/compaction/clean…各有生命周期），设计上更贴近数据库的日志-动作语义。
- **vs 裸 Hive + 手工增量列**：那是"没有事务的快照对比"，延迟和正确性都差一个量级。

## 版本演进

| 时期 | 关键变化 |
| --- | --- |
| 0.5–0.9 | COW/MOR 成型；DeltaStreamer；Spark 为主引擎 |
| 0.10–0.12 | metadata table 进入主线；Flink 写路径成熟；时间线 Server |
| 0.13 | **OCC 冲突解决重写**（record index 作为解析器）；表服务 async 化 |
| 1.0（2024-12） | 宣告稳定 API；hudi-rs/hudi-python；functional index；clustering 布局优化策略扩展 🔧 |
| 1.x（2025→） | 元数据表 partition 类型继续扩充；多 catalog 集成；性能与云对象存储兼容性修复 |

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "Hudi 是一种新的文件格式" | 数据仍是 Parquet/ORC（base）+ Avro/Parquet block（log）；Hudi 是**表格式 + 事务层 + 服务层** |
| "有了 Hudi 就不需要 ETL 了" | Hudi 提供的是管线原语（upsert/增量读/去重），分层业务逻辑仍要自己写（第 8、10 章的 Bronze→Silver→Gold） |
| "湖仓 = 存算分离的数据库" | Hudi 湖仓没有常驻计算节点；查询延迟受文件规划与对象存储 list 制约，这是 05/06 章大量篇幅存在的原因 |
| "upsert 一定比 insert 慢" | 慢的不是 merge 本身，而是**索引查找**与**小文件放大**；record index + metadata table 可把 upsert 做到接近 append-only |
| 第 1 章章题 | ⚠️ 本目录第 1 章标题为依据第 2 章转述的重建，非逐字核实 |

## 与其他章 / 其他笔记的联系

- 本章 1.4 的五层模型 = 全书目录的空间展开：**02 存储层+事务层 → 03 写 → 04 读 → 05 索引 → 06 表服务 → 07 并发 → 08 管线 → 09 运维 → 10 案例**。
- 事务语义对照：[../../db/db.md](../../db/db.md)（OLTP 的 WAL/锁 vs 湖仓的 timeline/OCC——同一个 ACID，两种物理实现）。
- 生态位对照：[../bigdata/01-大数据技术全景.md](../bigdata/01-大数据技术全景.md)、[../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)。
- 姊妹书文字对照：《Designing Data-Intensive Applications》第 3 章（存储与编码）与第 11 章（流批一体）是本章叙事的教科书版；Iceberg/Delta 的 Definitive Guide 若本仓库后续建目录再换链接。
