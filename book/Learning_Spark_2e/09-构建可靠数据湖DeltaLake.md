# 09 · 用 Apache Spark 构建可靠数据湖（Delta Lake）

> 原书第 9 章（Building Reliable Data Lakes with Apache Spark）。章骨架 ✅ 按 ApacheCN 全译镜像实抓还原：优化存储方案的重要性（数据库简介/读写/限制 → 数据湖简介/读写/局限）→ 湖仓（Lakehouse）是演进下一步（Apache Hudi／Apache Iceberg／Delta Lake）→ 用 Spark+Delta 构建湖仓（配置、批加载、流加载、写入时模式强制、模式演化、存量转换、update 修错、delete 合规删除、merge 处理 CDC、insert-only merge 去重、操作历史审计、时间旅行查快照）。Spark/Delta 行为 = ⚠️ 转述 + 官方文档。本章是 2e 相对 1e 的**全新章**，也是 2026 年回看最"应时代"的一章。对位：[Use Iceberg with Spark](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)、[Apache Hudi 权威指南](../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md)、[Apache Paimon 流式湖仓](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)。

## 9.1 存储三分法（章前半的论证结构）

- **数据库**：ACID/事务强，但规模与开放度受限；Spark 读写 DB（第 5 章 JDBC 回收）"能连不能靠"；
- **数据湖**：对象存储 + 开放格式（Parquet），规模便宜开放，但**没有事务、没有 schema 强制、并发写互踩、"湖变沼泽"**；
- **湖仓（Lakehouse）**：在湖的存储上补齐事务表语义——书给出三候选：Hudi（upsert 流式入湖先行者）、Iceberg（中立表格式）、**Delta（Spark 亲儿子、本书主推）**。
- 重构注脚：三格式之争在 2024–2026 已演化（统一/catalog 化/互操作），本册只在演进节登记现状，立场按原文"Delta 视角"标注为厂商相关。

## 9.2 Delta 机制词表（⚠️ 转述，口径 https://delta.io/ ✅ curl 200）

- **事务日志**：表目录 `_delta_log` 的 JSON commit + checkpoint；写=原子登记新文件清单，读=按版本拼快照——ACID 的实现根基；
- **配置接入**：`spark.sql.extensions=DeltaSparkSessionExtension` + catalog 替换（`.format("delta")` / `USING delta` 建表）；
- **批加载**：`df.write.format("delta").mode(overwrite/append)`；
- **流加载**：`readStream...writeStream.format("delta")`——与第 8 章 checkpoint/幂等合成交付"流进湖"正路；
- **模式治理**：写入时 schema 强制（拒腐）、`schemaOf_ + mergeSchema` 演化（可控变）；
- **数据维护**：`UPDATE`/`DELETE` 修错与合规删除（GDPR 叙事）、`convertToDelta` 存量转换；
- **MERGE（本章王牌）**：`DeltaTable.merge(...).whenMatchedUpdate().whenNotMatchedInsert()`——CDC 一行入湖的 upsert 原语；insert-only merge 做幂等去重；
- **审计与回溯**：`history(n)` 操作历史、`VERSION AS OF`/`TIMESTAMP AS OF` 时间旅行。

🔧 **概念类比：快照与增量（非本书 Spark/Delta 引擎行为）**：DuckDB 侧把第 5 章的分区 parquet 集当"湖"，用视图+目录约定手工搭"版本感"：`CREATE VIEW v2024 AS SELECT * FROM read_parquet('pq/yr=2024/*.parquet')` 读回 500 行（meas.txt G3 复用）；SQLite 侧用 WAL（meas.txt G5 组：`g5.db-wal/-shm` 伴生文件实测在场）观察"主文件+附属日志"的结构——**两例只给"数据与变更日志分离、按日志重放状态"的直觉**；Delta 的 MVCC/日志压缩/小文件 OPTIMIZE 均 ⚠️ 转述，不可由类比背书。

## 9.3 教学史位置（重构观点）

- 1e（2015）无此章；TDG（2018）也尚未把湖仓写进正文——**2e 是主流教学书里第一批把"表格式"升为主章的**（2020-07 成书，早于 Iceberg 热潮主流化）；
- 代价：本章=Delta 广告浓度最高的一章（作者 Databricks 身份，第 1 章已预警滤镜）；工程判断：学"机制词表"（事务日志/merge/时间旅行），**不学"唯一解"姿态**；
- merge 语义在 SQL 标准（MERGE INTO）与各格式间已趋同——概念一次学会，到处迁移。

## 9.4 盘上三角对位

- Iceberg 视角（中立格式/多引擎/catalog）：[../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)；
- Hudi 视角（upsert 时间线/记录级索引）：[../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md](../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md)；
- Paimon 视角（流式湖仓/LSM 原生）：[../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)；
- 论文/工程线补充：湖仓开山论文（Armbrust et al., *Data Lakehouse: A Ten-Year Overview*, IEEE Data Eng. Bull. 2021——无 DOI 挂靠，⚠️ 按标题+刊物+年份引用）。

## 9.5 章小节骨架总览（✅ 镜像实抓逐节对账）

| 原书小节（回译） | 本文件对应 |
| --- | --- |
| 优化存储解决方案的重要性 | 9.1 首段 |
| 数据库：数据库简介／使用 Spark 读写数据库／数据库的限制 | 9.1 数据库条 |
| 数据湖：简介／使用 Spark 读写数据湖／数据湖的局限性 | 9.1 数据湖条 |
| 湖岸（Lakehouse）：存储解决方案演进的下一步骤 | 9.1 湖仓条 |
| Apache Hudi／Apache Iceberg／Delta Lake | 9.1 三候选、9.4 三角 |
| 使用 Apache Spark 和 Delta Lake 构建 Lakehouse／配置 Delta Lake | 9.2 配置条 |
| 加载数据到 Delta Lake 表格中（批） | 9.2 批加载 |
| 将数据流加载到 Delta Lake 表格中（流） | 9.2 流加载 |
| 写入时强制执行模式以防止数据损坏 | 9.2 模式强制 |
| 适应变化数据的演进模式 | 9.2 模式演化 |
| 转换现有数据（convertToDelta） | 9.2 转换条 |
| 更新数据以修复错误（UPDATE）／删除与用户相关的数据（DELETE） | 9.2 维护条 |
| 使用 merge() 向表中插入变更数据（CDC）／使用仅插入合并去重数据 | 9.2 MERGE 条 |
| 通过操作历史审核数据更改（history）／使用时间旅行查询表的先前快照 | 9.2 末条 |

## 9.6 重建示例：CDC 一行入湖 + 时间旅行（本目录重做；⚠️ 语义转述 delta.io 文档）

```python
(deltaTable.alias("t")
   .merge(cdc_df.alias("s"), "t.pk = s.pk")
   .whenMatchedUpdate(set={"v": "s.v", "op": "s.op"})
   .whenMatched(s.col("op") == "D").delete()
   .whenNotMatchedInsert(values={"pk": "s.pk", "v": "s.v", "op": "s.op"})
   .execute())                     # == MERGE INTO 的 DataFrame 拼写（第 6 章双生语）

# 流式入库（第 8 章 foreachBatch 回收）：
(spark.readStream.format("kafka").option("topic", "cdc").load()
  .writeStream.format("delta").option("checkpointLocation", "ck/cdc")
  .foreachBatch(lambda b, i: b.write.format("delta").mode("append").save(path)).start())

# 审计与回溯：
spark.sql("SELECT * FROM delta.`%s` VERSION AS OF 7 WHERE pk=42" % path)  # 时间旅行
spark.sql("DESCRIBE HISTORY delta.`%s`" % path)                           # 操作历史
```

- 读法提示：三截代码是本章三个"王牌小节"（MERGE/流加载/时间旅行）的最小骨架；**零执行，`DESCRIBE HISTORY`/`VERSION AS OF` 语法以官方 Delta 文档为准**。

## 9.7 课堂问题（答不出回本文件）

1. 数据库/数据湖/湖仓各解什么问题、留什么问题（9.1 三分法）？
2. Delta 的"写=登记、读=拼快照"两句话各自的文件证据？
3. schema 强制与演化同时存在怎么配置才不打架？
4. insert-only merge 的去重语义与 `dropDuplicates` 的差别？
5. 时间旅行对"合规删除（GDPR）"的悖论怎么解（提示：VACUUM/墓碑语义 ⚠️）？
6. 本章三格式在 2026 的现实排位？依据哪个口径（9.1 重构注脚/演进节）？

## 核心概念速览（中英对照）

- **数据湖** — Data Lake：对象存储+开放格式的低价规模仓。
- **沼泽化** — Data Swamp：无治理湖的退化态。
- **湖仓** — Lakehouse：湖存储+仓语义的合题。
- **表格式** — Table Format：在文件之上定义事务表的规范层。
- **_delta_log** — Delta 事务日志：commit 序列即历史。
- **MVCC/快照隔离** — 多版本并发读+原子写（⚠️ 转述）。
- **Schema Enforcement/Evolution** — 写入拒腐与可控变列。
- **MERGE/UPSERT** — 匹配更新+未匹配插入：CDC 入湖原语。
- **Insert-only Merge** — 只插不更的幂等去重。
- **Time Travel** — VERSION/TIMESTAMP AS OF 快照查询。
- **History Audit** — 操作历史审计链。
- **convertToDelta** — 存量 Parquet 目录收编。
- **OPTIMIZE/Z-ORDER** — 小文件合并与聚簇（书浅、演进节补）。

## 最新演进与工业实践

- **Delta Lake 4.0 与开放化**：Delta 2019 开源后入 LF，2024–2025 推进 UniForm 多格式互读（Parquet/Iceberg/Hudi 元数据统一，⚠️ 转述未逐页核验）、Variant 类型随 Spark 4.0 落地（✅ https://spark.apache.org/releases/spark-release-4-0-0.html）；delta.io ✅ 为权威口径。
- **格式竞争收敛**：Iceberg 凭 REST catalog（Apache Polaris）+ 多引擎支持成 2024–2026 中立默认；Databricks 亦收购 Tabular 后双押（⚠️ 商业事实按公开公告转述）——本章"三选一"框架过时，现实是"按 catalog 与引擎生态选"。
- **流式入库标准姿势**：Structured Streaming + merge（第 8 章 foreachBatch 回收）仍是湖仓摄入主流；Paimon 在 Flink 侧、Iceberg 在 Kafka 侧各有原生解。
- **治理接口**：本章内容在 2026 与治理线（Unity/Polaris/Glue）拼接——目录版互链建议顺读 Data Fabric 系（波 6 在盘）与第 12 章 catalog 插件一节。
- **对照阅读**：盘上三本格式专书 00 文件已实链（9.4 节），本册角色=在 Spark 教学线内"第一次给表格式以正章地位"。
