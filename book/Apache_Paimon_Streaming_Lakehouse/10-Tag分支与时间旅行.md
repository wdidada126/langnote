# 10 Tag、分支与时间旅行：给湖表装上版本管理

> 《Apache Paimon 官方文档与源码精读》第 10 章。主源：文档 Maintenance（Tag / Branch / Manage
> Snapshots / Partition 生命周期）板块。快照只解决"能回看"，本章解决"值得回看的东西怎么留住、
> 怎么在留住的同时不破产"。

## 核心概念速览（中英对照）

- **时间旅行** — Time Travel：按快照号/时间戳/tag 读取历史版本表状态。
- **标签** — Tag：给某个快照起的持久名字，脱离快照过期策略独立存活。
- **自动打标** — Tag Automatic Creation：按 daily/hourly 周期自动为窗口末端快照打 tag 🔧。
- **标签退休** — Tag Retention/Expiration：自动 tag 按保留时长批量退役。
- **分支** — Branch：从某 tag/快照分裂出的独立版本线，读写均可指向分支，`表$branches` 观测。
- **回滚** — Rollback：把主分支指针重置到历史快照/tag，一步撤销一批提交。
- **快照过期** — Snapshot Expiration：保留 N 个/时长外的旧快照连同其独占文件清单被清除。
- **分区过期** — Partition Expiration：按时间或值自动删除整个分区（数据+元数据）。
- **孤儿清理** — Orphan Files Cleanup：remove_orphan_files 扫无引用文件物理删除 🔧。
- **冻结/归档语义** — 批处理锚点：用 tag 固定"昨天分区终态"给下游批作业，读写互不踩踏。
- **写隔离试验** — Branch 试跑：模式变更/backfill 在分支验证后 fast-forward 回主线的实践 🔧。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 10.1 | 快照保留窗口：默认即遗忘 | 过期是常态，不配置=只保最近几个 |
| 10.2 | tag：把易失快照变版本 | 批流读的共同锚点，schema 快照同名演进 |
| 10.3 | branch：存储层的 git 分支 | 同名表不同线，A/B 发布与回滚 |
| 10.4 | 分区生命周期 | 热-温-冷与过期删除的自动化 |
| 10.5 | 组合拳：湖仓版本管理 SOP | 打标→消费→过期→清理 一条闭环 |

## 精讲

### 10.1 默认世界：快照会烂掉

`snapshot.num-retained.min/max`、`snapshot.time-to-live`（默认小时级 🔧）决定表只"记得"最近几个状态。
过期的连锁回收：快照消失 → 其独占的 manifest/数据文件失去引用 → 异步 clean（含 4.3 讲的
"DELETE 条目落地"）。**一切时间旅行与流读回溯能力都以'快照还活着'为前提**——
这就是第 07/08 章反复强调"保留窗口错配"的根源。想让某天永在，请打标。

### 10.2 Tag：命名即永存

```sql
-- 手工：给快照起名字（Flink/Spark 过程调用，语法口径以文档为准 🔧）
CALL sys.create_tag('db.my_table', 'release-2026-09', 12345);
SELECT * FROM my_table /*+ OPTIONS('scan.tag-name'='release-2026-09') */;  -- 时间旅行到 tag
CALL sys.delete_tag('db.my_table', 'release-2026-09');
```

- tag 是**独立的元数据条目**（tag 目录），快照过期不会动它引用的文件——tag 把"版本"从
  "易失窗口"升级为"命名资产"；
- **自动打标**：`tag.automatic-creation = daily | hourly` + 时区 + `tag.num-retained-max` 退休策略——
  天级 tag 就是湖仓版"日终快照"，批作业、审计、报表全部锚定 `dt=...` 对应 tag，
  彻底解决"批读时分区还在被流写入追加尾巴"的经典撕裂问题（**批流一致的锚点**）；
- 与 consumer-id（8.4）分工：consumer 钉"消费进度"（流语义），tag 钉"业务版本"（批语义）。

### 10.3 Branch：同一张表的平行宇宙

```sql
CALL sys.create_branch('db.my_table', 'staging', 'release-2026-01');  -- 从 tag 分裂 🔧
INSERT INTO `my_table$branch_staging` ...;   -- 写分支（Flink/Spark 均支持，语法见文档）
SELECT * FROM my_table /*+ OPTIONS('branch'='staging') */;
CALL sys.fast_forward('db.my_table', 'staging');  -- 分支转正：main 指向分支头部
```

要点（🔧 文档行为口径）：

- 分支共享历史文件的元数据引用，**分叉后的新写才产新文件**——比 fork 一张新表便宜得多；
- 读写入口：表路径/SQL 的 `branch` 选项、系统表 `表$branch` 语法族；catalog 不感知也可用；
- 典型场景：① schema 演进/参数调整的灰度验证；② 年度回刷/backfill 在分支跑，验证后 fast-forward，
  主链路零污染；③ A/B 数据实验（两分支两套 compaction 策略）。
- 边界：**分支无合并（merge）语义**——不是 git，两条线不能三方合并；转正=指针切换，旧线被显式处理。
- 回滚的另一半：`sys.rollback_to(快照号/tag)` 把主分支回退（数据文件按引用回收），
  与"下游流读从回滚点重新对齐"需人工协调（consumer-id 可能要先 reset）。

### 10.4 分区生命周期：温度的自动化

```text
dt=2026-05-01（30 天前）→ partition.expiration-time='30 d' 命中 → 整分区标记过期
  → 快照不再引用 → 后台物理删除 + manifest 收缩
```

- 双策略：按时间（时间分区通用）与按值（`partition.mark-done-action` 等辅助，🔧）；
- 过期动作可挂钩下游：done 标记文件通知批调度（对照 Hudi savepoint/ Hive partition _drop_）；
- 与 tag 的关系：分区过期是"删"，tag 是"钉"——**同分区可以同时被过期策略和 tag 引用**，
  tag 引用的快照存续期间分区数据不得物理消失；顺序与范围要一起设计，否则要么提前失血要么永不过期。

### 10.5 SOP：一套可抄的保留策略

| 层 | 手段 | 目的 |
| --- | --- | --- |
| 秒/分钟 | 快照保留窗口（默认）| 流读容错、短窗排障 |
| 小时/天 | `tag.automatic-creation=daily` + 保留 90 天 | 批锚点、日级回溯 |
| 月/季 | 手工 tag（版本发布/审计点） | 命名资产、报表复现 |
| 消费端 | 每个流下游一个 consumer-id + lag 监控 | 防断链、防钉死 |
| 回收 | `remove_orphan_files` 定期批任务 🔧 | 清失败提交残留 |
| 试验 | branch + fast_forward | 变更灰度 |

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "time-to-live 设大点省心" | 保留=文件不清=对象存储账单 + list 变慢 + 快照枚举变深；过期策略要与最慢消费者对齐（consumer 监控）|
| "tag 只是个字符串别名，删了无感" | 删 tag 即释放引用，其独占文件可能被过期回收——先确认下游批作业不再引用该 tag |
| "分支能合并" | 无 merge（10.3）；分支是读/写指针与隔离写入，不是版本控制系统 |
| "回滚后流下游自动跟着重来" | 快照回退≠消费进度回退；不 reset consumer-id 会表现为"下游静默漏数"，排障地狱 |
| "打了 daily tag 就不用管快照过期" | daily tag 之间的窗口内，流读回溯仍受快照保留限制；长断链的流作业需要额外 tag 或 from-snapshot-full 起流 |

## 与其他章 / 其他笔记的联系

- 被 tag/branch 操作的元数据结构 → [04-元数据层快照与清单.md](04-元数据层快照与清单.md)；
  流读保留依赖 → [07-Changelog生成机制.md](07-Changelog生成机制.md)、[08-读路径批流一体读取.md](08-读路径批流一体读取.md)；
  schema 历史文件 → [02-核心数据结构LSM树与主键表.md](02-核心数据结构LSM树与主键表.md)（4.4 演进规则）。
- Delta 时间旅行/VACUUM 对照 → [../Delta_Lake_Definitive_Guide/04-表维护-时间旅行与VACUUM.md](../Delta_Lake_Definitive_Guide/04-表维护-时间旅行与VACUUM.md)；
  Hudi savepoint/restore 对照 → [../Apache_Hudi_Definitive_Guide/09-Hudi生产级部署与运维.md](../Apache_Hudi_Definitive_Guide/09-Hudi生产级部署与运维.md)；
  Iceberg 分支/标签（Spark Procedure 族）对照 → [../Apache_Iceberg活用入門/08-表维护操作.md](../Apache_Iceberg活用入門/08-表维护操作.md)。
- 横向：四格式 schema 与演化 → [../Engineering_Lakehouses_with_Open_Table_Formats/07-Schema与分区演化.md](../Engineering_Lakehouses_with_Open_Table_Formats/07-Schema与分区演化.md)。
- 数据质量/批流一致性讨论 → [../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md)。

## 本章记忆桩

```text
易失与永存：快照是 RAM，tag 是硬盘——批流锚点、回滚基线、审计资产全靠钉。
branch 三用：灰度 schema、隔离 backfill、A/B 实验；转正用 fast-forward，没有 merge 别硬合。
保留四件套：窗口（短）+ 自动 tag（天）+ 手工 tag（版本）+ consumer 监控（人）。
```
