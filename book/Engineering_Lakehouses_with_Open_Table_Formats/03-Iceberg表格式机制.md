# 第 3 章 Apache Iceberg 表格式机制

> ⚠️ 章题为**推定**（见 [00-总览与阅读地图.md](00-总览与阅读地图.md)）。
> 事实来源：Iceberg Table Spec（spec v1/v2/v3）、iceberg.apache.org 文档。SQL 均为教学示意。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 3.1 | metadata.json：表的"constitution" | 一切历史都在这一份文件里版本化 |
| 3.2 | snapshot / manifest-list / manifest | 三层清单的字段与用途 |
| 3.3 | 隐藏分区与 transform | 分区是元数据概念，不是目录概念 |
| 3.4 | 行级删除与 v2 | position/equality delete、deletion vector |
| 3.5 | 表排序与元数据整理 | sort order、RewriteManifests、ExpireSnapshots |
| 3.6 | spec 版本演进 v1→v2→v3 | 每次升版动了哪块元数据 |

## 核心精讲

### 3.1 metadata.json：单文件承载全部表历史

Iceberg 表当前状态的入口是一份 Avro/JSON 元数据文件（约定 `<uuid>-<version>.metadata.json`
或 `v<N>.metadata.json`），关键字段（Spec 术语）：

```text
format-version            1 | 2 | 3
table-uuid, location
last-sequence-number      v2+：全表单调序列号发号器
last-column-id            schema 演化用的高水位
schemas[] + current-schema-id        schema 全历史
partition-specs[] + default-spec-id  分区 spec 全历史（不可变）
sort-orders[] + default-sort-order-id
snapshots[]                          快照数组（含 parent-snapshot-id 链）
snapshot-log / metadata-log          审计时间线
refs{}                               main 分支 + branch/tag（含保留策略）
properties                             表属性
```

设计要点：**"历史内嵌于当前"**——读旧版本不需要翻目录，指针一跳直达。
代价是 metadata.json 会随提交线性膨胀，因此有周期式
`RewriteTableMetadata`/压缩实践（🔧 v3 时代多轮小提交的表尤需关注）。

### 3.2 三层清单的字段级视角

```text
snapshot {
  snapshot-id, parent-snapshot-id, sequence-number,
  manifest-list -> List<ManifestFile>
}
ManifestFile {
  path, length, partition-spec-id, content(0=data/1=deletes),
  sequence-number, min-sequence-number,
  added/existing/deleted-files-count,
  partitions[]: { 每分区字段: contains_null, lower_bound, upper_bound, column_size }
}
ManifestEntry {
  status: EXISTING|ADDED|DELETED, snapshot-id, sequence-number,
  DataFile { content(data/position-deletes/equality-deletes/deletion-vectors),
             file_path, file_format, partition(值元组), record_count,
             column-sizes, value-counts, null-value-counts,
             lower-bounds, upper-bounds }
}
```

三个高频误读，值得掰开：

- **sequence-number 决定"谁删除谁"**：v2 里 manifest entry 的有效性
  靠 sequence number 与 delete file 的 `sequence_number/referenced_*` 对齐，
  而不是靠文件时间；这也是"改写数据文件时保留 delete 语义"的基础。
- **manifest 是 Avro 文件**：列存、可流式读；规划器读它等价于一次小查询。
- **partition-field summaries 在 manifest-list 上**：所以裁剪第一刀
  只花一跳一文件，跳过 90% 的 manifest 才花第二跳。

### 3.3 隐藏分区：transform 而非目录

分区 spec 由 `(source-id, transform, name)` 三元组列表构成，transform 是纯函数：

```text
identity | bucket[N] | truncate[W] | year/month/day/hour
```

写入时引擎按 spec 计算分区值（写入文件的 `partition` 元组），
**目录布局完全由格式自由决定（如按 UUID 散列存放）**。查询时：

```sql
-- 教学示意：谓词 day(ts)=... 能被规划器改写为对分区列的等值约束
SELECT * FROM events WHERE ts >= TIMESTAMP '2026-09-30 00:00:00';
```

由此获得两项独门能力（第 7 章展开）：**分区演化**（换 spec 不动旧文件）
与**谓词到分区的自动映射**（用户不必知道分区列名，引擎投影出
`partitions.day(ts)` 供 BI 使用）。

### 3.4 v2 行级删除：MOR 的最小实现

Iceberg v2 把"行级修改"定义为 **附加 delete file、不改 data file**：

| delete 类型 | 语义 | 主要使用者 |
| --- | --- | --- |
| position delete | (path, pos)：删指定文件的指定行 | Spark MERGE、Flink |
| equality delete | (col=value[, ...])：删匹配键的所有行（含未来文件） | Flink 流式 upsert 的核心 |
| deletion vector（🔧 v2 扩展/v3 转正） | 文件级 roaring 位图，标记已删行号 | 替代海量 position delete，规划 O(1) |

查询 = data files ∧ 反连接匹配的 delete files；维护 = compaction 把 delete
"烘焙"进新 data file（`RewriteDataFiles`，第 8 章）。**equality delete 是 Flink
无状态流式 upsert 的命脉，也是"读放大"的头号来源**——未 compaction 前，
每个读端都要在线执行 delete 关联。

### 3.5 运维三件套（规划视角）

- `RewriteDataFiles`：bin-pack/sort（按 sort order）合并小文件、烘焙 delete；
- `RewriteManifests`：把碎 manifest 重打包（小提交风暴后必做，
  目标尺寸默认 8MB 量级、1000+ 文件/manifest 上限）；
- `ExpireSnapshots` + `remove_orphan_files`：快照链截短（受 refs 保留策略约束）、
  清理"写了没提交"的孤儿（默认 older_than 数天，防并发写误删）。

### 3.6 spec 版本演进一句话

| 版本 | 关键增量 |
| --- | --- |
| v1 | 分析型 append 表：manifest 树 + 隐藏分区 + schema/partition 演化 |
| v2 | 行级删除（delete files）、sequence number、内容类型（data/eq/pos deletes）、row-level 更新 |
| v3 | 🔧 deletion vectors、row lineage（`_event_time/_data_sequence_number/_change_ordinal/_operation`）、default values、嵌套 schema 演化、geospatial/variant 等新类型 |

## 例子：读一张表的"当前文件清单"到底发生了什么

```text
1) catalog 返回 metadata.json 位置        （一次 HTTP/Thrift）
2) 读 metadata.json，取 current-snapshot  （一次 GET，几 KB～几 MB）
3) 读 snapshot 指向的 manifest-list       （一次 GET + 解析 Avro）
4) 用谓词对 partitions[] 摘要裁剪          → 得到要打开的 manifest 集
5) 读这些 manifest                        → DataFile 级 min/max 再裁
6) 下发扫描任务                            总计约 3+N 次元数据读、零目录 LIST
```

这条链是 Iceberg 全部优点（可规划、可并发）与全部成本（元数据读延迟、
manifest 膨胀）的来源。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "分区列必须在 schema 里" | 分区是 source 列上的 transform 结果，可分区 `bucket(id,16)`，表里无需 id 之外的列 |
| "snapshot-id 可以按时间排序" | 它是生成序（v1 是毫秒时间戳，后续是雪花式），分支/tag 场景下时间序 ≠ 提交序 |
| "有了 v2 更新就不需要 compaction" | equality/position delete 只增读放大，不增正确性成本；不 compaction 的表读性能会雪崩 |
| "metadata.json 坏了表就没了" | 历史 metadata 路径可从旧 snapshot 链/备份恢复；生产必须开启 catalog 侧版本保护 |

## 与其他章的联系

- 3.1/3.2 → 第 6 章：commit = CAS 替换 metadata.json，冲突校验发生在追加 snapshot 时；
- 3.3 → 第 7 章 partition evolution 全量展开；
- 3.4 → 第 8 章 compaction 的"烘焙 delete"职责；
- 3.5 → 第 11 章各引擎动作名（procedure/DDL）对照；
- 生态位讨论 → [../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)。

## 思考题

1. 为什么 v2 引入 `sequence-number` 后，manifest entry 不再必须携带
  `snapshot-id` 语义？用"改写数据文件时 delete 如何继续生效"解释。
2. 一张高频提交（每分钟）的流表，manifest 数 3 天涨到 5 万。
   给出诊断路径（看哪两个元数据指标）与两种补救操作，说明各自停写与否。
3. equality delete 让 Flink 实现无状态 upsert，但把状态转移给了谁？
   从读端、维护端、表大小三个角度各答一条。
4. 对比 [../数据库系统概念6/15-并发控制.md](../数据库系统概念6/15-并发控制.md)：
   Iceberg 的 CAS-on-catalog 是严格可串行化还是仅快照隔离？
   丢更新（lost update）在什么操作组合下仍可能发生？
