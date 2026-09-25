# 09 Compaction 与删除向量：LSM 的另一张账单

> 《Apache Paimon 官方文档与源码精读》第 9 章。主源：文档 Primary-Key Table / Compaction 板块与
> Maintenance（Dedicated Compaction、Manage Rows、OOM 调优）相关页。第 02 章说 LSM 把随机更新
> 变成顺序追加，本章说它如何为"摊平"付费——compaction 是 Paimon 集群里第一号运维对象。

## 核心概念速览（中英对照）

- **压实/合并** — Compaction：把多个 sorted run 归并成更少更大、键不重叠的层级文件的后台过程。
- **触发线** — num-sorted-run.compaction-trigger：sorted run 数超过阈值即安排合并（默认 5 量级 🔧）。
- **停写线** — num-sorted-run.stop-trigger：超过则写入暂停等合并（write-async/同步模式的差别）。
- **通用策略** — Universal Compaction / Sorted Run 计数策略：按 run 数而非层大小触发，写放大可控。
- **异步合并** — Async Compaction：合并与 flush 解耦，在检查点间隙/独立线程执行，降低提交延迟。
- **专用合并作业** — Dedicated Compaction Job：`compact` action，把合并从写作业剥离成独立 Flink 作业 🔧。
- **full-compaction** — 全量合并：把整桶所有层重写成单层，changelog(full-compaction 模式)与部分运维依赖它。
- **sort-compact** — 排序压实：按指定列对（追加表的）文件重排归并 🔧，服务读局部性。
- **删除向量** — Deletion Vector (DV)：位图标记 base 文件中已失效行，让主键表免合并直读 🔧。
- **lookup 合并** — Lookup 触发方式：小合并时顺带点查维护 DV/changelog 的执行路径（与 07 章同源）。
- **资源外溢** — 内存与堆：写缓冲、合并堆、lookup RocksDB 都在作业堆/盘上，OOM 多与 compaction 相关。
- **新鲜度税** — Freshness Tax：合并节拍决定 ro 表/直读引擎能看到多新的数据。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 9.1 | 触发模型：run 计数与两线机制 | 读放大、写放大、空间放大三角的手动挡 |
| 9.2 | 在哪跑：写作业内 vs 专用作业 | 官方推荐：生产上写/合并分离 |
| 9.3 | 删除向量：读路径的解放 | 牺牲一点合并复杂度换免合并读与 OLAP 直读 |
| 9.4 | 追加表的 compaction | 无键合并也要物理归并 |
| 9.5 | 运维视角：观测、调优、OOM | 从 $files 的 level 分布读起 |

## 精讲

### 9.1 触发模型：两线夹一个节拍

Paimon 的 LSM 不照搬 RocksDB 的 level 大小比策略，而以 **sorted run 计数**为核心：

- 每次 flush 给 level-0 加一个 run（键范围可与其它 L0 文件重叠）；更高层整层天然是一个不重叠 run；
- **compaction-trigger**：run 总数越线 → 挑选最小代价的一批 run 归并（universal 风格：优先合并
  相近大小的 run，控制写放大倍数）；
- **stop-trigger**：继续堆积越过第二线 → 写作业反压/暂停该桶，直到合并追上。两线间距就是突发缓冲。

参数直觉（🔧 具体键名/默认值以文档为准）：trigger 越大 → 读放大越高、写放大越低、
查询合并越贵；反之合并越勤、存储与 CPU 越贵、读越爽。默认值偏保守，**高更新表要主动调**。

异步化选项：合并可放 flush 线程内（同步，节拍简单但提交慢）或异步线程（利用检查点间空隙，
吞吐高但瞬时文件/状态更多）。full-compaction 周期（`full-compaction.delta-commits`）另计：
即使 run 数未越线，也周期性把所有层压平成单层——为 changelog(full-compaction) 与 DV 维护提供节拍。

### 9.2 在哪跑：三形态与选型

| 形态 | 配置 | 优点 | 代价 |
| --- | --- | --- | --- |
| 写作业内合并（默认） | 普通 streaming write job | 链路短，无额外部署 | 计算资源混用，合并抖动拖慢检查点 |
| 写侧只写 + 独立压缩作业 | 写作业 `write-only=true` + `compact` action 常驻 🔧 | 互不干扰；压缩可独立扩缩容、错峰 | 多一套作业与桶分配协调；新鲜度=压缩节拍 |
| 手工/调度触发 | 批式 `compact` action（定时全量或按分区） | 适合回灌、迁移、救火 | 人力/调度成本 |

`compact` action 的两种角色值得单记：
① **流式常驻**：订阅 APPEND 快照持续合并（专用压缩作业）；
② **批式重写**：对历史分区一次性整理（迁移、rescale、追平落后的冷分区）。
写作业与压缩作业同桶并跑是被设计支持的（这正是 5.4 表格里唯一允许的同桶双作业）。

**桶数演进的正解也在这一节**：固定桶改数量不能原地生效——新数据走新桶数、旧分区维持旧桶，
用 `compact` action（+ 按分区/整体）重写旧桶，即官方 rescale 流程 🔧（延迟桶 postpone 模式正是把这条路产品化）。

### 9.3 删除向量：给 OLAP 直读开的后门

传统 LSM 读必须堆合并（base 文件里躺着已删/已更的行）。**deletion vector** 模式
（`deletion-vectors.enabled=true` 🔧）让合并/lookup 时顺带为每个数据文件产出一张 RoaringBitmap：
"第 3、77、908 行已失效"。收益：

- 批读/交互查询**跳过合并**：扫文件 + 查位图过滤即可，Trino/StarRocks/Doris 直读主键表的延迟断崖式下降；
- 与 read-optimized 路线（8.6）互补：DV 让"新鲜数据"也能免合并读；
- 代价：每次合并多一步 DV 生成与位图 IO；bucket 更新密集时位图膨胀，需要合并重写文件回收。

> 这一能力解释了 Paimon 与 OLAP 引擎的"合体"趋势（第 12 章）：湖侧把合并成本预付一次，
> 查询侧不再每次交易——对高并发短查询是根本性改善。对照：Iceberg/Delta/Hudi 的 position-delete/DV
> 思路相同，差别在 Paimon 的 DV 由 LSM 合并顺带维护、与 changelog/lookup 共享一条流水线。

### 9.4 追加表：没有键也要整理

追加表无 sorted run 概念，compaction 退化为**物理小文件归并**：
`compaction.max-file-num / min-file-num` 类阈值按分区+桶攒够碎文件就合并 🔧。
两个专属工具：

- **异步合并作业**（同上，追加表同样支持独立 compact，避免写入端 list/小文件恶化）；
- **sort-compaction / 增量聚类**：合并时按指定列排序重写（如按 user_id），把"谁在未来会被一起扫"
  的数据摆在一起——服务谓词扫描与列编码双重收益（对照 Iceberg 的 sort、Delta 的 Z-ORDER，见互链）。

### 9.5 运维视角

观测入口（🔧 系统表口径，第 04 章）：

```sql
SELECT `level`, COUNT(*), SUM(file_size_in_bytes) FROM my_table$files
WHERE bucket = 0 AND partition='dt=20260901' GROUP BY `level`;
-- 健康态：level-0 少量、高层占绝对体积；病态：level-0 几十上百 = 合并饿死
```

常见病灶与药方：

| 症状 | 根因 | 处方 |
| --- | --- | --- |
| 提交超时/检查点拉长 | 同桶合并抖动抢 CPU/IO | 剥离专用压缩作业；异步合并 |
| 读 P99 毛刺 | level-0 堆积 → 归并读很深 | 降 trigger 或补 full-compaction 周期 |
| 存储膨胀 | run 碎 + 旧文件未过期 | 查快照过期（第 10 章）与 DV 位图大小 |
| 写作业 OOM | 写缓冲×桶数 + 合并堆 + lookup 状态同堆竞争 | 降 sink 并行度/桶数、加 managed memory、lookup 换磁盘 RocksDB（参数组合以文档 OOM 指南为准 🔧）|
| 桶数想改 | 固定桶先天刚性 | rescale：改表参数 + compact 重写旧分区 🔧 |

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "compaction 是后台小事，默认配置就够" | 默认值面向通用场景；高更新主键表不调 compaction ≈ 实时数仓不给 GC，必然演化成读慢/OOM |
| "write-only=true 就能关掉合并" | 它只是把合并职责**移交**专用作业；没人接 = level-0 无限堆积 = 停写 |
| "删除向量让 compaction 不再需要" | DV 本身由合并流程维护；它优化的是**读**，不是取消合并 |
| "full-compaction 越频繁越好" | 每次都是整桶重读重写，频率与桶大小相乘就是账单；changelog 质量需求决定节拍下限即可 |
| "专用压缩作业和写作业桶划分可以随便改" | 两者按同一桶集合工作，并行度/桶数错配会导致空转或漏桶（🔧 按文档分配规则部署）|

## 与其他章 / 其他笔记的联系

- 被合并的对象（LSM/level/run）→ [02-核心数据结构LSM树与主键表.md](02-核心数据结构LSM树与主键表.md)；
  changelog 由合并顺带产出 → [07-Changelog生成机制.md](07-Changelog生成机制.md)；
  ro 表/直读受益方 → [08-读路径批流一体读取.md](08-读路径批流一体读取.md)；
  旧文件物理回收 → [10-Tag分支与时间旅行.md](10-Tag分支与时间旅行.md)。
- 表服务对照：Hudi 四服务（含 compaction/clustering）→ [../Apache_Hudi_Definitive_Guide/06-维护与优化Hudi表.md](../Apache_Hudi_Definitive_Guide/06-维护与优化Hudi表.md)；
  Iceberg 维护操作 → [../Apache_Iceberg活用入門/08-表维护操作.md](../Apache_Iceberg活用入門/08-表维护操作.md)；
  Delta OPTIMIZE/Z-ORDER → [../Delta_Lake_Definitive_Guide/09-性能调优.md](../Delta_Lake_Definitive_Guide/09-性能调优.md)。
- 横向总论：四格式 compaction 哲学 → [../Engineering_Lakehouses_with_Open_Table_Formats/08-Compaction与表维护.md](../Engineering_Lakehouses_with_Open_Table_Formats/08-Compaction与表维护.md)。
- 文件格式层统计与行组 → [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)。

## 本章记忆桩

```text
LSM 三放大三角：读放大=run 数、写放大=合并次数、空间放大=旧版本滞留；trigger 两线是手动挡。
生产形态：写只写（write-only），压单独跑（compact 常驻）——资源解耦是第一原则。
DV 一句话：把合并税从每次查询预付成每次合并，换来 OLAP 直读自由。
```
