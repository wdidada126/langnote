# 第 4 章 Apache Hudi 表格式机制

> ⚠️ 章题为**推定**（见 [00-总览与阅读地图.md](00-总览与阅读地图.md)）。
> 事实来源：Hudi 官方文档（Core Concepts/Timeline/Data Models/Metadata Table/Index）、HUDI RFC。SQL/配置为教学示意。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 4.1 | Timeline：Hudi 的第一抽象 | 一切可见性、回滚、表服务都挂在 instant 状态机上 |
| 4.2 | COW vs MOR：同一个 file group 的两种历史 | 读放大/写放大的旋钮，不是二选一的表类型标签 |
| 4.3 | 记录级语义：record key、precombine、payload | Hudi 是"表里有主键概念"的格式 |
| 4.4 | 索引体系 | upsert 性能的决定因素 |
| 4.5 | 内部元数据表（MDT） | 把"表索引"做成一张表内小表 |
| 4.6 | 表服务：compaction/cleaning/clustering | 异步流水线与它的时间约束 |

## 核心精讲

### 4.1 Timeline 与 instant 状态机

`.hoodie/` 目录下的每个动作是一个 **instant**，文件名
`<instanttime>_<action>[.<partitionpath>].<state>`：

```text
instanttime：Unix 毫秒（2.x 起加纪元前缀）
action：  commit(COW写) | deltacommit(MOR写) | compaction | cleaner |
         rollback | savepoint | replacecommit(表服务/clustering产物)
state：  requested → inflight → completed（文件名后缀变化 = 状态推进）
```

三条规则解释 Hudi 90% 的行为：

1. **读端只认 completed**：可见性边界 = 最新 completed commit/inflight 之前的完成集；
   "requested/inflight 存在"即意味着有未完成作业，恢复器据此回滚或续做；
2. **回滚 = 反向 instant**：写失败时把 inflight 文件转成 `rollback`，
   由回滚器删除该 instant 产生的新文件（对比 ARIES undo，见 02 章 2.2）；
3. **表服务是"挂在时间线上的普通动作"**：compaction 请求由写端在跨过阈值时
   自动产生 `.requested`，由独立服务捡走执行——**这决定了"写快但读暂时背着旧 delta"的语义**。

多写者并发：instant 的 requested→completed 推进需要原子 rename（HDFS 天然、
S3 靠条件写🔧/DynamoDB 时间线服务）；**Hudi 的并发控制仲裁点是 Timeline + MDT**，
第 6 章细讲。

### 4.2 COW / MOR：file group 的两种演化方式

```text
partition → file groups (按 file id 组织)
COW:  一次 upsert → 重写受影响 base file（新 version 的文件），旧版留给 cleaner
MOR:  一次 upsert → 追加 log file 的 block：
        insert/append-block(Colon) | update-block | compact-block | deletion-block(DV)
      读端 = base file ⊕ log blocks 在线合并（read-optimized 则只读 base/已 compact）
```

- **COW**：读快、写放大随记录命中面积放大 → 适合"大批低频更正"；
- **MOR**：写快（顺序 append）、读要合并 → 适合流式高频 upsert；
  `compaction` 就是把 log blocks 物化成新 base file 的物化点；
- 🔧 **deletion vector 模式**（1.x 起）：用 roaring 位图标记删除行，
  大幅缓解"删除也要重写整文件"——机制与 Iceberg DV、Delta DV 三家趋同（第 8 章对照）。

关键配置的心智模型：`hoodie.datasource.write.operation` =
upsert/insert/bulk_insert/delete；`precombine` 决定同批内同 key 谁胜出；
`record key + partition path` 的哈希/映射决定落哪个 file group。

### 4.3 记录级语义

Hudi 是三格式中唯一把"**主键 + 组合时间 + 载荷语义**"写进表属性
（`hoodie.table.recordkey.fields / partitionfields / precombine.field`）的格式：

- upsert = 按 record key 定位 file group → 写 update block 或重写 base；
- 这使 **CDC 入湖是"表原生能力"**而非外部作业逻辑（第 10 章）；
- 代价：表属性耦合写入路径，且**record key 不可演化**——改键 = 重建表。

### 4.4 索引体系：key → file group 的映射器

| 索引 | 原理 | 适用 / 痛点 |
| --- | --- | --- |
| Bloom Index（默认遗留） | 在 base 文件 footer 里存 key 布隆过滤器 | 免外部状态；更新文件即"换指纹"，大表慢 |
| Global Bloom | 跨分区查找 | 键可能改分区时唯一可用，代价更高 |
| Simple Partition-level | 按分区裁剪后的布隆 | 键稳定在分区内的常规场景 |
| Bucket Index (Murmur3/Native) | hash(key)%N → file group，N 建表定死 | O(1) 定位、写放大可控；**桶数难改**（2.x 起支持动态桶调整） |
| Record Index | 从文件路径编码的分区+键范围反推 | bulk 友好、特定数据分布 |
| Metadata-based (MDT 的 record_index) | 直接查 `.hoodie/metadata` 里的索引表 | 大表正解；强依赖 MDT |
| Fallback / 二级索引 | 组合多种 + 表达式索引 | 覆盖"既要桶又要全局"的杂糅需求 |

**索引选择即表设计**：同一份数据，bucket index 与 bloom index 的
upsert 吞吐可差一个数量级。它与 MDT 一起构成 Hudi "为管线优化"的护城河。

### 4.5 内部元数据表（MDT）

`.hoodie/metadata` 是一张 **MOR 小表**，列族化的表内表：

```text
files        每个 base/log 文件的路径、大小、分区、写入 instant
column_stats 文件级列统计（裁剪 + 布隆辅助）
record_index record key → (partition, file group)  ← 支撑 record-level upsert
txn          事务元数据（写锁/并发控制辅助，配合 Timeline）
clean/compaction/requested 队列  ← 表服务的工作队列本身也存这里
```

MDT 把"列目录 + 读 footer"变成"查一张索引表"，规划成本从 O(文件数)
降到近似 O(命中文件数)；**代价是元数据一致性从"目录真相"变成"表内真相"**，
MDT 损坏/落后需要 `regen` 工具修复——生产事故高发点。

### 4.6 表服务与它的调度形状

```text
写入（deltacommit）→ 超阈值产生 compaction.requested
                 → 超保留产生 clean.requested / clustering / rollback_sync
   ↑ 由 inline（同 Spark 任务）或 standalone service 消费
```

- **compaction** 的执行者是"第二个写者"，它产生 `replacecommit`，
  原子地把文件组指向新 base（第 6 章冲突矩阵里这是唯一"读旧写新"的交错热点）；
- **cleaner** 保留 `hoodie.cleaner.commits.retained` 个 instant 的历史，
  savepoint 可钉住特定 instant（如发布快照）；
- **clustering** = 离线重排文件布局（sort columns 声明"聚簇意图"，
  由 layout strategy 执行，第 8 章与 Z-order 对照）。

## 例子：一条 CDC update 的完整旅程（MOR）

```text
Debezium 事件 {key=42, op=u, ts=...}
→ 写端算 record index → 定位 partition p1 / file group fg7
→ 追加 update block 到 fg7 的 <instant>.log.v1
→ deltacommit completed：42 的"最新态"此刻存在于 base⊕log 合并视图
→ 阈值到 → compaction 把 fg7 重写为新 base（旧 base 等 clean）
→ cleaner 保留期内：as.of.instant 仍能读到 42 的旧版本
```

这条链解释了为什么 Hudi 强调 **"写即时、读最终、历史靠时间线"**。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "COW/MOR 是建表时的永久选择" | MOR 表靠 compaction 把 file group 逐步变回'近似 COW'；两种模式共享 timeline 机制 |
| "MOR 的实时读等于快照读" | realtime query 合并 log blocks，隔离语义与"读已 compact 数据"（read-optimized）差一个 compaction 延迟 |
| "MDT 只是加速索引" | 并发控制（txn）、表服务队列也依赖它；关 MDT 时这些能力降级到 Timeline 文件 |
| "bucket 数可以随便调" | 改桶 = 重哈希/reshuffle，有专属工具且代价接近重建，容量规划时要算够 |

## 与其他章的联系

- 4.1 → 第 6 章（OCC 的仲裁点：Timeline + txn 表）；
- 4.2/4.6 → 第 8 章 compaction 三格式对照；
- 4.3/4.4 + 4.1 → 第 10 章 CDC 入湖管线的机制底座；
- MDT 与 Iceberg manifest 的"元数据即文件"路线差异 → 02 章 2.5 对照表；
- 更深的索引/表服务专题 → 待建档的姊妹笔记（Apache Hudi 单格式指南，见 00 章分工表）。

## 思考题

1. Timeline 的 instant 文件名即状态机——推导：为什么这个设计在 HDFS 上优雅、
   在裸 S3（无条件写时代）上麻烦？Hudi 给的两种补救（timeline server/元数据表）
   各牺牲了什么？
2. Bucket index + MOR：桶数 N 选小了与选大了分别先在哪一环爆掉
   （写端/读端/维护端）？给一个容量估算公式草案。
3. MDT 的 `record_index` 落后于数据（异步写）时会发生什么错误行为？
   读 Hudi 文档确认其一致性约束，与你设计的修复顺序比较。
4. 对比 Iceberg equality delete：Hudi 的 update block 把"待合并"状态放在
   **数据侧文件**，Iceberg 放在**清单侧条目**。两种选择在
   "规划器复杂度、compaction 必要性、time travel 粒度"上各产生什么差异？
