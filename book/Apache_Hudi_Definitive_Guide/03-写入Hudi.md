# 第 3 章 写入 Hudi

> 原书章题（译系列核实）：写入 Hudi。小节地图：拆解写入流程（Start Commit → Prepare Records → 记录分桶 → 写入存储 → 提交变更）→ 探索写入操作（表属性、INSERT INTO、MERGE INTO 部分合并、删除、覆盖分区/整表）→ 亮点功能（Key Generators、Merge Modes、写时模式演进、引导导入）→ 小结。
> 机制口径以官方文档 Spark Writer / Flink Writer 页与 1.x 源码行为为准。

## 本章地图

> 一句话：**一次 upsert = 打收据（分配 instant）→ 贴标签（索引定位 file group）→ 分篮子（partitioner 分组到 task）→ 写文件（COW 重写 / MOR 追加 log）→ 盖章发布（写 commit 元数据 + 冲突检测）。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 3.1 Start Commit | 分配 instant time；先回收悬挂 inflight（自动 rollback） | 写入器自己修复上次事故 |
| 3.2 Prepare Records（tagging） | 用索引把每条记录标上 fileID + instant | upsert 的核心开销在这里（第 5 章） |
| 3.3 记录分桶（partitioning） | Spark 侧把同 file group 的记录送进同一 task | 避免并发写者互踩，决定并行度 |
| 3.4 写入存储 | COW：read-merge-write；MOR：append log block | 两种表类型在此分叉 |
| 3.5 Commit Changes | 额外元数据（文件清单/统计）→ 冲突解决 → completed | 可见性原子点；OCC 战场（第 7 章） |
| 3.6 写操作全家福 | INSERT/MERGE/DELETE/OVERWRITE/BULK_INSERT | 语义与代价各不同 |
| 3.7 Key Generator | record key 与 partition path 如何从输入派生 | 复杂键/时间键/非核心键 |
| 3.8 Merge Modes | 批内 + 跨批谁赢：COMMIT_TIME/CUSTOM/OVERWRITE_WITH_LATEST | preCombine 字段的舞台 |
| 3.9 Schema Evolution on Write | 写时自动加列/改名映射（1.x 能力） | 上游加字段不再断流 🔧 |
| 3.10 Bootstrap | 把既有 Hive/Parquet 数据集原地收编为 Hudi 表 | 迁移不改数据文件 |

## 核心精讲

> **教学示意，不参与构建。**

### 3.1–3.5 Upsert 五步拆解（Spark 写路径）

```text
① Start Commit
   timeline 上写 <t>.commit.requested → <t>.commit.inflight
   顺手检查：若有更老的 inflight（上次崩溃），生成 rollback 并清理其孤儿文件
② Prepare Records（tagging）
   输入每条记录带 HoodieKey(recordKey, partitionPath)
   查索引："这个 key 现在住在哪个 file group？" → 打上 fileID 与所属 slice
   命中 = UPDATE 语义；未命中 = INSERT 进新/现有 file group
③ 记录分桶（upsert partitioner）
   把 (partitionPath, fileID) 相同或相近的记录聚到同一 Spark task；
   按 file group 大小估算均衡 task 负载（小文件处理策略也在这一步选择落点）
④ 写入存储
   COW：每个 task 读旧 base file + merge 新记录 → 写 version+1 的 base file
   MOR：往目标 file group 的 log 文件追加 block（updates → compacted/delta block）
⑤ Commit Changes
   驱动端汇总：各 task 的文件清单 → 写 <t>.commit（含每个 file group 的 added/removed、
   记录数、字节数、统计、schema、冲突解决元数据）→ 原子可见
```

- **tagging 为什么贵**：全量输入 × 索引查找。bloom index 要扫候选文件的 column stats；record index 走 metadata 表一次 KV 查询（第 5 章）。
- **delete 的特殊性**：带 delete 标记的记录（delete key / Flink CDC 的 op=d）在 COW 中被 merge 剔除；在 MOR 中写 delete block，且默认要等 compaction 才物理消失。开启"仅凭 key 字段删除"（无需携带整行 payload）后，Debezium tombstone 也能直接落地（选项名以官方 Write Operation 文档为准）。

### 3.6 写操作全家福（Spark）

```sql
-- INSERT INTO：纯追加，不查索引，最快但会产生重复 key（官方明确警告）
INSERT INTO customers SELECT * FROM stg.day1;

-- MERGE INTO：可控 upsert；支持部分列更新 + 条件分支
MERGE INTO customers t USING stg.changes s ON t.id = s.key
WHEN MATCHED AND s.op = 'd' THEN DELETE
WHEN MATCHED AND s.op = 'u' THEN UPDATE SET t.email = s.email, t.ts = s.ts
WHEN NOT MATCHED THEN INSERT (id, email, ts, dt) VALUES (s.key, s.email, s.ts, s.dt);

-- UPDATE/DELETE 非键列：可行，代价 = 索引反查（第 5 章 column stats / expression index）
-- OVERWRITE：整表/整分区替换，产生一个 replacecommit 风格的快照切换
INSERT OVERWRITE customers PARTITION (dt='2026-09-25') SELECT ... ;
-- bulk_insert（DataSource 选项 operation=bulk_insert）：跳过索引与合并，按输入直接切文件
```

| 操作 | 走索引 | 去重 | 典型场景 |
| --- | --- | --- | --- |
| insert | 否 | 否 | 只追加事实表 |
| upsert | 是 | 是 | CDC/维表更新 |
| bulk_insert | 否 | 否（仅文件切分优化） | 历史回填 |
| insert_overwrite | 否 | — | 分区级快照替换 |
| delete（key） | 是 | — | 软/硬删除 |

### 3.7 Key Generators：输入没有干净主键怎么办

官方四类（Spark `hoodie.datasource.write.keygenerator.class`）：

| Generator | record key | partition path | 场景 |
| --- | --- | --- | --- |
| SimpleKeyGenerator | 单列 | 单列 | 常规 |
| ComplexKeyGenerator | 多列拼接 | 多列拼接 | 复合自然键 |
| TimestampBasedKeyGenerator | 可省略（用默认） | 由时间列格式化派生 | 按 `yyyy-MM-dd` 自动分区 |
| NonCoreRecordGenerator（input 无 meta 字段） | 从业务列派生 | 从业务列派生 | 摄取非 Hudi 结构流 |

- Flink 侧对应 `partition.fields.`/`recordkey.fields` + `complex.key.column.drop.value`。
- ⚠️ 分区键含时间戳的陷阱：**同一行晚到的更新若落入另一分区 → 变成"旧分区删除 + 新分区插入"**，跨分区 upsert 一致性靠 GLOBAL 索引兜底（第 5 章 global vs local）。

### 3.8 Merge Modes：版本裁决规则

- **COMMIT_TIME_ORDERING（默认）**：后一事务赢；同事务内用 preCombine 列裁决。
- **CUSTOM**：指定列（默认 `_hoodie_record_seq`）逐条比较；配合自定义 `payload clazz` 可实现"部分列合并"——第 2 章 MERGE 语义的底层机制。
- **OVERWRITE_WITH_LATEST**：最后一条直接覆盖，适合"记录本身是部分列 patch"的事件溯源式 upsert。
- preCombine 选择建议（书中口径=官方建议）：用**不可变单调列**（updated_at / CDC binlog ts），不要用 ingest 墙钟，否则乱序会回退版本。

### 3.9 🔧 Schema Evolution on Write

- 依赖 metadata 表中的 schema 历史（第 5 章）；1.x 中写路径（DataSource/MERGE）遇到输入新增列时自动为表演进 schema（增列、类型放宽），删除/丢列类演进受守护参数控制（如 `hoodie.datasource.write.schema.allow.auto.evolution.column.drop`，口径以官方 Configurations 页为准）。
- 列改名（rename）在 Spark `MERGE`/`ALTER` 路径下可被识别并映射。
- Flink 写路径同样支持在写入时演进表 schema（以官方 Flink Writer 文档的相应选项为准，本目录不背参数名）。
- 意义：**上游 MySQL 加一列，湖仓管道不断流**——第 8 章 Streamer 的异构数据整合直接引用本节。

### 3.10 Bootstrap：引导导入

```text
hudi.bootstrap.mode: 把既有数据集（Hive 分区表/裸 parquet）原地登记：
  - 原文件成为各 file group 的 base file（copy-on-write 表）
  - 不重写数据，只生成一次 bootstrap instant 的清单
  - 之后按分区可开启 delete/partition 演化
Flink 侧：bootstrap.source.partition / parallelism 参数化分片扫描
```

- 对照：Iceberg `add_files` / Delta `convert` 是同类能力；Hudi 的差别是 bootstrap 后立刻可用 upsert（因为 tag 与索引体系照常运转）。

## 版本演进

| 行为 | 旧版（≤0.12） | 1.x（本书基线） |
| --- | --- | --- |
| 并发写语义 | 简单 OCC/无冲突解决（多写者易脏） | 三阶段冲突检测 + 可插拔解析器（第 7 章） |
| 写入器小文件控制 | 手写 fileID 上限参数 | `hoodie.*` 自动按记录估算大小滚动（`hoodie.parquet.max.file.size`/`small.file.limit`） |
| MERGE INTO | 仅 SQL 扩展 | Spark Catalog 原生（支持 DELETE/UPDATE 语句翻译） |
| Schema on write | 手工 `ALTER` | 写时自动演进（增列/映射），破坏性演进受守护参数控制 🔧 |
| payload 类 API | deprecated | 新 PartialUpdateHandle 推荐 |

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "insert 也会自动去重" | 官方明确：insert 不做记录级去重；重跑会产生重复 key。幂等摄取应使用 upsert + 稳定 record key，或依赖 Streamer 的 checkpoint/dedup（第 8 章） |
| "preCombine 随便挑个时间列" | 必须单调且不可被业务改写；用可更新时间戳会被"迟到旧数据"覆盖新值 |
| "MOR 更新写 log = 顺序写所以无限快" | log block 滚动 + 读侧 merge 债务 + compaction 资源都要算账；写便宜是把账单推给第 6 章 |
| "tagging 在 executor 本地做" | tagging 需要索引全局视图（metadata 表/驱动端广播），它是 Spark 作业的一个独立 stage，常是瓶颈 stage |
| "bootstrap 会复制数据" | 不复制；登记现有文件。代价是第一次 compaction/cleaning 前布局不受控 |

## 与其他章 / 其他笔记的联系

- 3.2 tagging 的索引查找 → [05-索引与元数据表.md](05-索引与元数据表.md)；3.5 的冲突解决 → [07-Hudi中的并发控制.md](07-Hudi中的并发控制.md)。
- 3.4 的 log block → [06-维护与优化Hudi表.md](06-维护与优化Hudi表.md) compaction 的对象；[04-从Hudi读.md](04-从Hudi读.md) snapshot 读的 merge 成本。
- 3.7/3.8 直接服务于 [08-基于HudiStreamer构建数据湖仓.md](08-基于HudiStreamer构建数据湖仓.md) 的摄取语义（ordering field、payload）。
- OLTP 对照：⑤ commit 前收集"受影响文件清单"≈ MySQL 提交时写 binlog event；回滚孤儿文件 ≈ undo purge（[../../db/db.md](../../db/db.md)）。
- Spark 执行层背景：[../bigdata/02-Spark核心与RDD模型.md](../bigdata/02-Spark核心与RDD模型.md)、[../bigdata/03-Shuffle与宽依赖.md](../bigdata/03-Shuffle与宽依赖.md)（3.3 的 partitioner 本质是一次带业务语义的 shuffle）。
