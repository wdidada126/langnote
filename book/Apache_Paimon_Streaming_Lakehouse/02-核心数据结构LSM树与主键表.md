# 02 核心数据结构：LSM 树与主键表

> 《Apache Paimon 官方文档与源码精读》第 2 章。主源：Paimon 文档 "Primary-Key Table" 板块
> （Data Layout / Bucket / Sequence Field / Merge Engine 入口）。机制以源码行为为准，🔧 标文档示例。

## 核心概念速览（中英对照）

- **主键表** — Primary Key Table：`PRIMARY KEY (...) NOT ENFORCED` 声明的表，支持行级 upsert 与删除。
- **LSM 树** — Log-Structured Merge Tree：写先落内存表/level-0 小文件，后台逐层归并的存储结构；Paimon 中**一个桶内一棵 LSM**。
- **分桶** — Bucket：分区内数据的哈希分片单位；同键必然同桶，是并行写入与冲突隔离的粒度。
- **固定桶** — Fixed Bucket：`bucket = num`（>0），按键 `hash(key) % num` 定位；经典模式。
- **动态桶** — Dynamic Bucket：`bucket = -1`，key→bucket 映射存于哈希索引，支持跨分区更新与免选桶数。
- **延迟桶** — Postpone Bucket：`bucket = -2`，新数据先进临时桶、由 compaction 作业重分布 🔧。
- **桶键** — Bucket Key：固定桶下可指定少于主键列的哈希键，控制数据倾斜分布。
- **有序段** — Sorted Run：一段按键有序的文件集合；level-0 每个文件即一个 sorted run，更高层整层为一个。
- **层级** — Level（L0..Ln）：LSM 的分层；越深层数据越旧越大，由 compaction 逐层下沉（第 09 章）。
- **序列字段** — Sequence Field：同键记录的"谁新谁旧"比较列（如更新时间/版本号），乱序保护的闸门。
- **键组/值列** — Key Columns vs Value Columns：主键列+序列列存于 key 侧，其余列为 value 侧；合并时按 key 对齐。
- **归并读** — Merge Read：读时对覆盖同键的多个 sorted run 做堆合并取最新，是主键表读放大来源。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 2.1 | 为什么湖上更新非 LSM 不可 | 只追加文件系统里，"改一行"=重写整个文件；LSM 把重写摊到后台 |
| 2.2 | 表→分区→桶→LSM 的四级布局 | 桶是原子单位：单写者、单棵树、单堆合并读 |
| 2.3 | 固定桶/动态桶/延迟桶三选一 | 桶数决策贯穿表生命周期，选错代价极高 |
| 2.4 | 序列字段与乱序 | 无序列字段则按到达顺序裁决更新，CDC 乱序会旧胜新 |
| 2.5 | 写入缓冲与 flush | 内存排序缓冲满 → 生成 level-0 文件 → 触发合并检查 |

## 精讲

### 2.1 湖上 upsert 的死结与 LSM 的解法

对象存储/HDFS 的 Parquet 文件**不可改**（append-only 介质 + 列式编码整体压缩）。要在这样的湖上支持
`UPDATE t SET amt=... WHERE user_id=...`，只有三条路：

1. **重写整个文件/分区**（Iceberg/MOR 之前的批式做法，Delta 无 DV 时的 UPDATE）——更新越密代价越爆炸；
2. **删除文件 + 读时过滤**（Iceberg MOW position delete、Delta DV、Hudi 的 delete 记录）——把成本转嫁给读侧与"清理重写"；
3. **追加"带键的补丁文件"，后台归并**——即 LSM。Hudi MOR 的 log block 是它的表格式化变体；
   Paimon 则直接以 LSM 为**第一公民**：level 结构、sorted run、compaction 全部一等建模。

Paimon 选 3 的深层原因：它假设写者是**秒/分钟级持续 upsert 的流**。这个频率下方案 1 完全不可行，
方案 2 会让每次查询都背上合并税；只有 LSM 的"顺序追加 + 后台摊平"能把高频小提交变成常态。
代价写在脸上：必须有 compaction（第 09 章），且点查/批读要跨 sorted run 归并（2.6）。

### 2.2 四级布局：catalog → 表 → 分区 → 桶（=一棵 LSM）

```text
warehouse/db.db/my_table/
├── snapshot/        # 快照序列（第 04 章）
├── schema/          # schema 历史
├── manifest/        # 清单文件（第 04 章）
├── dt=20260901/
│   ├── bucket-0/    # ← 一棵 LSM：level-0 小文件们 + L1..Ln 归并后的文件
│   ├── bucket-1/
│   └── ...
└── index/           # 动态桶的 hash 索引 / 删除向量等 🔧
```

- 一个桶 = 一个 LSM = 同一时刻**至多一个写者** = 无锁并行单位。写吞吐上限 ≈ 桶数 × 单桶写速。
- 主键必须**包含全部分区列**（固定桶模式的约束），否则同键可能落两分区，"改一行"就不知道去哪找旧行；
  想跨分区更新（分区列不在主键里）只能走**动态桶**（2.3）。
- 读取一个主键：定位分区 → `hash(key)%num` 定位桶 → 在该桶的 LSM 上跨 sorted run 归并找最新值。

🔧 建表示例（Flink SQL，官方文档口径仿写）：

```sql
CREATE TABLE orders (
  order_id BIGINT,
  user_id  BIGINT,
  amount   DECIMAL(10,2),
  update_time TIMESTAMP(3),
  dt STRING,
  PRIMARY KEY (order_id, dt) NOT ENFORCED   -- 分区列必须进主键（固定桶）
) PARTITIONED BY (dt) WITH (
  'bucket' = '8',
  'sequence.field' = 'update_time'
);
```

### 2.3 三种桶模式：一个决策树

| 模式 | 取值 | 定位方式 | 适用 | 痛点 |
| --- | --- | --- | --- | --- |
| 固定桶 | bucket>0 | hash(桶键)%num，**无状态** | 桶数可估、吞吐可控的主链路 | 桶数选小写不动、选太大读碎；改桶数需 rescale/重写 🔧 |
| 动态桶 | bucket=-1 | 查 key→bucket 哈希索引（Flink state + index 文件） | 无法预估规模、**跨分区更新**、多作业并发不同桶 | 索引只在写作业 state 里——多写者并发改同键危险；扩桶需 rebuild 🔧 |
| 延迟桶 | bucket=-2 | 先写"延迟区"，专用 compaction 作业决定最终桶数 | 接入期规模未知、希望自动分桶 🔧（1.x 引入） | 必须常伴 rescale 型压缩作业，链路多一个角色 |

决策顺序建议：**默认固定桶 + 按压测流量定桶数**（经验式：单桶 200MB~1GB 归并后大小、
每桶稳定 1~2 个写并行）；确认存在"主键不含分区列"的跨分区更新才用动态桶；
规模完全不可测的新湖仓用延迟桶过渡（🔧 该模式文档与参数名迭代较快，以当前 master 文档为准）。

动态桶的成本要讲透：写作业 state 里维护全量 key→bucket 映射（本质是一台嵌在 Flink 状态里的
哈希索引），state 大小与表基数同阶——**Checkpoint/恢复时间与状态后端容量都要按表规模预算**。

### 2.4 序列字段：谁新谁旧的裁决权

同键两条记录并发到达，谁覆盖谁？默认按**进入 LSM 的先后**（内部自增序列号）。但 CDC 经 Kafka 多分区
转发后到达顺序≠业务顺序，会出现"旧快照覆盖新变更"。`sequence.field`（可用逗号多列逐级比较）把裁决权
交给业务列（如 `update_time`、binlog offset）：合并时序列小者败。

- 序列字段是**读/合并时比较**，不是写入去重——乱序的旧记录照样落 level-0，只是归并时被压住（写放大仍在）。
- 与部分更新/聚合引擎组合时的行为见第 06 章（序列组）。
- 想要"数值大的赢"以外的自定义裁决，需要 UDF 级 merge function（聚合引擎路径，第 06 章）。

### 2.5 写入的一生：缓冲 → level-0 → 触发合并

```text
upsert 记录 → 桶内内存写缓冲（红黑/跳表按键排序，默认 256MB 量级 🔧 'write-buffer-size'）
  → 满则 flush：缓冲整体排序落盘为一个 level-0 文件（内部有序）
  → 检查 sorted run 数是否越过 compaction 触发线（第 09 章）
  → 未越过：返回继续收；越过：该桶写入暂停或异步化，先归并再收
```

level-0 文件间键范围可以重叠（都装"最近改动"），L1 以下整层不重叠——这是 LSM 经典不变式，
决定了 2.6 的读策略。快照提交时机在别处（第 05 章）：flush 产生文件 ≠ 可见，可见以 snapshot 为准。

### 2.6 读侧：归并读与它的三笔优化债

主键表批读 = 对该桶所有 sorted run 做 k 路归并（键堆），同键取序列最大者。读放大 = 一个键被更新的
次数在归并中被重放的体现。Paimon 给的三笔债的偿还手段分别在：

1. **compaction 摊平**（09）——run 数越少归并越浅；
2. **删除向量**（09）——把"逻辑删除"物化成位图，base 文件可直接跳过合并；
3. **统计裁剪**（04）——manifest 里的 min/max key、value 统计让不相关文件根本不进堆。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "主键表像 OLTP 主键一样全局唯一约束" | 唯一性只在**同桶同键的合并语义**下成立；Paimon 不做约束校验，乱序/多写者破坏唯一性时报错不会来，坏数据会来 |
| "动态桶免选桶数所以更好" | 它把桶数决策换成了 state 索引维护成本，且并发写者与恢复行为复杂；官方文档默认推荐仍是固定桶 |
| "bucket 就是分区" | 分区是**目录级裁剪单位**（按 dt 等），桶是**哈希并行单位**；先分区后桶 |
| "设了 sequence.field 就不怕乱序" | 结果正确但 level-0 里旧数据仍占空间、仍参与合并；乱序窗口过大还会拖慢收敛 |
| "一个桶可以被两个作业同时写" | 同桶并发写无事务保护（各自 flush 的 LSM 结构会互相看不见），必须单写者；多作业并写要靠**不同桶/不同分区**划分 🔧 |

## 与其他章 / 其他笔记的联系

- 桶文件的元数据登记与统计裁剪 → [04-元数据层快照与清单.md](04-元数据层快照与清单.md)；
  合并引擎如何消费 key/value 布局 → [06-合并引擎.md](06-合并引擎.md)；compaction 细节 → [09-Compaction与删除向量.md](09-Compaction与删除向量.md)。
- LSM 树单机原理（LevelDB/RocksDB）→ [../精通LevelDB.md](../精通LevelDB.md)；Paimon 可视为"湖上分布式版 RocksDB + 快照协议"。
- Hudi 的 log block 对照 → [../Apache_Hudi_Definitive_Guide/02-Hudi快速入门.md](../Apache_Hudi_Definitive_Guide/02-Hudi快速入门.md)（COW/MOR）；
  Iceberg 的 MOW 对照 → [../Apache_Iceberg活用入門/05-行级删除与删除文件.md](../Apache_Iceberg活用入門/05-行级删除与删除文件.md)。
- 检查点节拍 → [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)。

## 本章记忆桩

```text
四级布局：表 → 分区（目录裁剪）→ 桶（哈希并行）→ LSM（sorted runs）。
桶三态：固定=算得快、动态=查得到、延迟=以后再说。
乱序三件套：sequence.field 定胜负，level-0 存旧账，compaction 平烂账。
```
