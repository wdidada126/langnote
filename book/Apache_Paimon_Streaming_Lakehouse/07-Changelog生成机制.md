# 07 Changelog 生成机制：让湖表说出完整的流语义

> 《Apache Paimon 官方文档与源码精读》第 7 章。主源：文档 Primary-Key Table / Changelog Production 板块。
> 这是全系列最核心的一章：changelog 是"湖"与"流"之间的翻译层，也是 Paimon 区别于其他三种表格式的
> 立身之本。理解本章，才理解为什么下游 Flink 作业敢直接"流读湖"。

## 核心概念速览（中英对照）

- **变更日志** — Changelog：与表变更一一对应的 +I/-U/+U/-D 完整事件序列文件，流读的直接数据源。
- **changelog 生产者** — Changelog Producer：表参数，决定由谁、在哪一步、花多少代价把旧值（-U）记下来：none / input / lookup / full-compaction。
- **none 模式** — 无显式 changelog：只靠数据文件推导；流读时由读侧 normalize/合并补旧值，成本转嫁下游。
- **input 模式** — 直抄上游：要求输入本身是完整成对 changelog（如 CDC），写入时原样落 changelog 文件，零额外计算。
- **lookup 模式** — 合并时点查：flush/compaction 前对每条新记录在旧层级点查前值，当场补出 -U 🔧。
- **full-compaction 模式** — 全量对比：每次全量 compaction 时对比新旧两代数据生成 changelog，节拍=全量合并间隔。
- **变更归一化** — Changelog Normalization：流读侧对不规整输入（producer=none 或跨桶）做旧值补偿的 Flink 算子。
- **非成对变更** — Non-paired Changes：-U 缺失/+U 落单，会让下游 sum 等聚合算错——producer 存在的根本动机。
- **changelog 清单** — changelogManifestList：快照中指向本批 changelog 文件的账本（第 04 章）。
- **保留窗口错配** — Retention Mismatch：快照/changelog 过期快于下游消费速度 → 流读断链，需 consumer-id/tag 锚定。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 7.1 | 为什么湖上的"新快照"不等于"流" | 流要的是差集，合并把差集碾碎了 |
| 7.2 | 四种 producer 逐一拆解 | 一张对比表定选型 |
| 7.3 | input：CDC 链路的白送午餐 | 上游完整就别自己造 |
| 7.4 | lookup 与 full-compaction 的对决 | 新鲜度/成本/回撤顺序三角权衡 |
| 7.5 | 消费侧兜底与断链修复 | normalize、consumer-id、从快照全量起流 |

## 精讲

### 7.1 差集问题：合并即失忆

Flink 聚合作业 `SELECT shop, sum(amt) FROM orders GROUP BY shop` 以流读方式消费湖表：

- 湖表只存"最新状态"：order#1 的 amt 从 10 改成 20，表里只剩一行 20；
- 下游需要收到 `-U(10), +U(20)` 才能把 sum 修正（只给 +U(20) 会多算 10；只给新快照差分更无从谈起）；
- 旧值 10 物理上躺在**上一代 sorted run** 里，LSM 一合并就灰飞烟灭。

所以 changelog 必须在**合并发生之前/之时**被显式抓取并持久化——这不是 connector 层的巧思，
而是格式层的存储设计：快照里多了一本 changelogManifestList 账、桶目录里多了一类 changelog 文件。
对照：Delta 的 CDF 在优化事务时记旧版本、Iceberg 靠删文件差分（-U 语义不完整）、Hudi CDC 模式记 preImage；
**Paimon 的差异在于把"谁负责抓、什么时候抓"做成了用户可选的四档开关**，让成本显式化。

### 7.2 四档 producer 总览

| 模式 | 旧值来源 | 额外代价 | changelog 完整时刻 | 典型场景 |
| --- | --- | --- | --- | --- |
| none（默认） | 不产；读侧兜底 | 表侧零，下游大 | 取决于下游 normalize | 只有批读/追加流读的内部表 |
| input | 上游自带，直拷落盘 | 几乎零 | 写入即可用 | CDC 入湖（上游是完整变更流）|
| lookup | 每次 flush/小合并时点查旧层 | 中：点查+本地 RocksDB 状态 🔧 | 提交即较完整 | 回撤流打宽/agg 后仍需 changelog 的中间层 |
| full-compaction | 全量合并时新旧代对比 | 高：周期性全量重读 | 仅在全量合并后成批出现 | 更新率适中、能容忍节拍、不想养 lookup 状态的表 |

选型三问：① 上游是成对 CDC 吗？是 → input。② 下游流读要多快的新鲜度？秒/分钟 → lookup；
能吃"全量合并节拍" → full-compaction。③ 有人只批读？那这张表的 producer 可以 none 省成本——但别让它出现在任何流读下游。

### 7.3 input：与 Flink CDC 的天然锁死

`changelog-producer = 'input'` 假设输入流**每个变更事件都已带对方的影子**（-U 紧邻 +U、同键同批出现），
典型来源：MySQL CDC（debezium 事件序）、Kafka 上的 changelog topic、以及"Flink 作业的成对输出"。
写作业原样把 +I/-U/+U/-D 落到 changelog 文件，代价≈0。两个隐含纪律：

1. **上游违约无检查**：给 input 表灌一条只有 +U 没有 -U 的流，changelog 就永久残缺、下游静默算错——
   input 是"信任声明"不是"校验保证"；
2. **deduplicate 引擎下的删除**：-D 同样入 changelog；想屏蔽删除看 ignore-delete（第 06 章）。

### 7.4 lookup vs full-compaction：新鲜度三角

**lookup（1.x 推荐的主路）**：在 flush/compaction 前，用桶内"层间点查"（本地 RocksDB 维护小层
键索引，🔧 文档称 lookup changelog producer 借 deletion-vector 同款点查设施）为每条 upsert 找到前值：
找到 → 补 -U；找不到 → 说明是首次出现，记 +I。产出的 changelog 随每次提交（检查点）可用，
新鲜度 = 提交节拍，且**顺序天然规整**。代价：每次 flush/小合并多做一轮点查 + 状态维护，写放大上升；
桶内存/CPU 预算要留够。

**full-compaction**：平时不产 changelog；每隔 `full-compaction.delta-commits` 次提交强制一次
**全层级归并**，归并时新旧两代键对比，产出这一窗口内的完整变更集。特征互补：

- 优点：无点查状态、写放大集中在合并本身；更新少/键基数小的表非常省。
- 缺点：changelog **成批迟到**（两次全量合并之间下游流读无事可读/或走读侧兜底）；
  全量合并=重读整桶，大桶上的抖动明显；期间上游多次改同键只能折叠成"净变更"（非逐步变更）——
  下游 sum 类聚合结果对，但中间值轨迹丢失（"changelog 质量降级"）。

> 一个高频面试/排障点：**partial-update / aggregation 表的流读为什么不许 producer=input？**
> 因为合并语义（多列独立更新、列折叠）使"逐条上游变更"在表侧不可逆推——-U 的"部分更新前整行"
> 在 input 里根本没有出现过。必须让 lookup/full-compaction 在合并现场把整行前像抓下来。

### 7.5 消费侧兜底：producer=none 也能流读，但代价换人付

不配 producer 的表被流读时，Flink 读端会进入"读数据文件当 changelog"的模式：新文件里的记录按
键与更早数据比较（必要时 normalize 算子补 -U），正确但把合并/比较的账搬到下游，且下游状态大、
恢复慢。工程铁律：

- **producer 解决"有没有"，consumer-id 解决"断不断"**：流读断链的头号原因是快照过期
  （`snapshot.time-to-live`）把 changelog 清了。修复：consumer-id 钉进度（第 08 章）或 tag 保留节点（第 10 章）。
- 切换 producer（none→lookup）不回溯历史：流读起点必须选在新 producer 生效之后的快照，
  否则"半截 changelog"照样错账——变更表要 `FROM-SNAPSHOT` 全量重放或换表重建。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "主键表天然就有 changelog，设了主键流读就有 -U" | 默认 producer=none，下游走 normalize 兜底或拿不到完整变更；"能流读"≠"有 changelog" |
| "input 模式会校验上游是不是完整 changelog" | 不校验（7.3）；错配只会在下游 sum 对不上时暴露 |
| "full-compaction 产出的 changelog 和 input 一样逐步" | 它是窗口净变更，同键多次修改被折叠（7.4）|
| "changelog 文件会一直占空间要单独清" | 与快照同生命周期：随快照过期一并回收（第 10 章）|
| "配了 lookup 下游就能任意慢消费" | producer 管生产，不管理保留；保留靠 consumer-id/tag（7.5）|

## 与其他章 / 其他笔记的联系

- 合并现场即 changelog 现场：LSM 结构 → 02；compaction 触发 → 09；lookup 设施与删除向量共用 → 09。
- 快照/账本结构 → [04-元数据层快照与清单.md](04-元数据层快照与清单.md)（changelogManifestList）。
- 流读位点与消费者管理 → [08-读路径批流一体读取.md](08-读路径批流一体读取.md)。
- 上游从哪来：CDC 链路 → [11-Flink集成与CDC入湖实践.md](11-Flink集成与CDC入湖实践.md)。
- Flink changelog 流/撤回语义基线 → [../基于Apache_Flink的流处理.md](../基于Apache_Flink的流处理.md)、
  [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)。
- Hudi CDC 模式对照 → [../Apache_Hudi_Definitive_Guide/04-从Hudi读.md](../Apache_Hudi_Definitive_Guide/04-从Hudi读.md)；
  Delta CDF 对照 → [../Delta_Lake_Definitive_Guide/07-高级特性-DV与CDF.md](../Delta_Lake_Definitive_Guide/07-高级特性-DV与CDF.md)；
  Iceberg 删除文件差分的局限 → [../Apache_Iceberg活用入門/05-行级删除与删除文件.md](../Apache_Iceberg活用入門/05-行级删除与删除文件.md)。

## 本章记忆桩

```text
一句话：合并会碾碎旧值，changelog producer 就是在碾碎前把旧值抄一份。
选型：上游完整→input；要新鲜→lookup；省状态能忍→full-compaction；没人流读→none。
双闸：producer 管"产不产"，consumer/tag 管"留不留"——只开一闸必断链。
```
