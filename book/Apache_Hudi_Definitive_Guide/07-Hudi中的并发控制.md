# 第 7 章 Hudi 中的并发控制

> 原书章题（译系列核实）：Hudi 中的并发控制。小节地图：并发控制技术（多写入场景：为何需要多写者、OCC/NBCC/MVCC 各自适用的场景；简单默认：单写入+表服务）→ Hudi 如何处理并发控制（基础、三阶段提交、冲突检测与解决、加锁机制、多写系统挑战）→ 在 Hudi 中使用多写入支持（启用、配置锁、Streamer/Spark DataSource 用法、单写多服务、关闭）→ 小贴士与最佳实践 → 总结。
> 机制口径以官方文档 Concurrency Control 章节为准。**这是全书机制密度最高的一章。**

## 本章地图

> 一句话：**Hudi 的默认世界观是"一张表一个写者"；多写者靠乐观并发控制（OCC）——每个事务带着自己的"文件清单"提交，提交前沿 timeline 回放检测是否与他人触碰同一 file group，冲突则按解析器裁决；锁提供者（lock provider）只在 instant time 分配等狭窄临界区里提供保护。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 7.1 并发控制技术谱系 | 锁/Wound-Wait、MVCC、OCC、NBCC | 湖仓选 OCC 的物理原因 |
| 7.2 单写者默认模型 | 写者 + 表服务是"特权写" | 大多数事故源于误解此默认 |
| 7.3 三阶段提交流程 | preCommit → 数据写入 → commit 时冲突检测 | 检测在盖章前最后一刻 |
| 7.4 冲突检测 | 直接读 vs 元数据回放；粒度= file group | 两事务改同一 file group 才算冲突 |
| 7.5 冲突解决 | bloom / record index / simple 解析器；部分成功（partial write） | 不是"全输重跑"，能救多少救多少 |
| 7.6 Lock providers | 内建进程内锁（Spark 作业间安全）vs ZK/文件系统/JDBC/Hive 锁 | 没有外部锁 = 单机内安全而已 |
| 7.7 多写者的现实挑战 | 读放大、重复数据、长尾重试 | 书中"挑战"清单 |
| 7.8 运维旋钮 | 启用/关闭多写、早期检测、异步表服务、分区隔离 | 最佳实践收敛 |

## 核心精讲

> **教学示意，不参与构建。**

### 7.1 为什么是 OCC 而不是锁或 MVCC

- 对象存储没有可靠的共享锁与页级并发（01 章三约束）；跨 Spark/Flink 作业持锁 = 把互斥成本放在最贵的协调面上。
- Hudi 的元数据形态（**每次提交 = 受影响 file slice 的完整清单**）恰好是 OCC 的理想输入：提交时只需比较清单交集。
- 技术谱系对照（书中"并发控制技术"段）：
  - 悲观锁/NBCC：适合短事务高频互斥（OLTP）；湖仓事务以分钟计，不适用。
  - MVCC：Hudi 文件天然多版本，但**写写冲突仍要额外机制裁决**——Hudi 用 timeline + OCC 而不是可见性快照。
  - OCC：读不加锁、写提交时检测——默认选择。Flink 多写者场景另有 NBCC/MVCC 变体的讨论（书中"适用于 NBCC 与 MVCC 的多写入场景"）。

### 7.2 默认模型：单写者

```text
一张表 = 一个写者（一个 Spark 作业 / 一个 Flink 作业 / 一个 Streamer）
        + 若干表服务执行体（可独立进程）
同引擎并发的多个 SQL？—— 由引擎内建串行（InProcessLockProvider 只保护同一 JVM）
```

- 官方反复强调：**没开多写者时，两个独立作业同时写一张表不保证正确性**（可能丢提交、读到半发布）。
- 这就是"简单默认：单写入 + 表服务"一节的现实意义：能用单写者解决就别开多写。

### 7.3 三阶段提交（写事务视角）

```text
阶段一 preCommit（开始提交前）：
  在外部锁保护下分配 instant time，写 <t>.commit.requested/.inflight
  （ZK/文件系统/JDBC 锁的粒度：整个 preCommit 或仅 instant time 分配）
阶段二 写数据：
  各 task 写 base/log 文件；驱动端收集清单；此期间不阻塞任何人
阶段三 commit：
  1) 读 timeline：列出与我并发（inflight 更早、或完成时刻交叠）的事务集合
  2) 冲突检测：把每个并发事务的清单按时间顺序"回放"到当前（direct read 或 metadata replay）
  3) 冲突解决：对命中的 file group 做裁决（7.5）
  4) 写 <t>.commit（完成态）→ 原子可见
```

### 7.4 冲突检测细节

- **粒度**：(partitionPath, fileId) —— 同一 file group 被两个事务改写才算真冲突；不同分区/不同文件互不相干。
- **两种检测方式**（官方文档称检测模式，参数口径以 Configs 页为准）：
  - DIRECT_READ：读并发事务已写的文件清单（元数据），精确但要求元数据可读。
  - SOURCE：按数据源重放（用于 Flink 两阶段提交恢复等场景）。
- **planner constraint**：限制"你不应与哪些未完成动作并存"（如：存在 pending clustering 时拒绝普通写，或反之），防止结构类操作与数据写互相拆台。

### 7.5 冲突解决：解析器与部分成功

- 解析器（官方提供 `RECORD_INDEX` / `BLOOM_FILTER` / `SIMPLE` 三种 resolver）：
  - 核心思想：对冲突 file group，**比较两事务各自写入的 key 集合**——只有真交集才判冲突。
  - 两事务写了同 file group 的不同 key → 本事务只重写"自己碰过的 key"，保留对方的（**partial write success**）：重算受影响的 slice，合并双方结果。
- 失败路径：若交集非空 → 本事务对该 file group 的修改丢弃或整体重试（行为由 conflict resolution 配置族决定，口径以文档为准），**而不是回滚对方**。
- 对照 MySQL：MySQL 的写写冲突 = 死锁检测 + 回滚一方；Hudi = 提交时文件级 diff + 尽量都活。乐观的代价是"部分提交"带来的语义要业务自己确认（幂等/最终一致）。

### 7.6 Lock Providers

| Provider | 协调面 | 依赖 | 备注 |
| --- | --- | --- | --- |
| InProcessLockProvider | 单 JVM | 无 | Spark 默认；跨作业不安全 |
| ZookeeperBasedLockProvider | ZK 临时节点 | ZK | 经典选择；含心跳防死锁 |
| FileSystemBasedLockProvider | 存储上锁文件 | 原子 create 语义 | **S3 等不支持原子 rename 的存储慎用**（官方警告） |
| JDBCBasedLockProvider | 数据库表锁/租约 | 关系库 | 已有元数据库时最省事 |
| HiveLockProvider | Hive metastore 锁 | HMS | 与 Hive ACID 同设施 |

- 配置面：`hoodie.write.lock.provider` + `...client.class` + `...timeout` 等（口径：官方 Lock Providers 页）。
- **Flink 多写者**：各写并行、以 checkpoint 驱动提交，需要外部锁保证 instant 分配与提交串行化（书中"适用于 NBCC 与 MVCC 的多写入场景"一节讨论的正是 Flink 侧的取舍；参数以官方 Flink Writer 文档为准）。

### 7.7–7.8 多写者的代价与调法（书中最佳实践浓缩）

| 实践 | 理由 |
| --- | --- |
| 按业务域分表/分区隔离写者 | 不重叠的文件集合 = 零冲突；比任何调参都有效 |
| 启用早期冲突检测（early conflict detection） | 写前先探测明显重叠，减少"干完活才发现白干" |
| 表服务与数据写分离（async/standalone） | 结构类 instant 与数据类 instant 解耦，planner constraint 更稳 |
| 控制重试成本：缩短单事务时长、减小批 | OCC 的世界里，大事务 = 高冲突面 = 高重做成本 |
| 多写者 + 无外部锁 = 事故 | 回到单写者（不开 OCC 模式、不配外部锁）才是安全默认；书与官方都建议能单写就不多写 |
| 防重复数据：写者间统一 record key 生成与 ordering | 两写者各自插同一新 key 时，索引+preCombine 决定终值 |

## 版本演进

| 项 | ≤0.12 | 0.13+ / 1.x（本书基线） |
| --- | --- | --- |
| 冲突解决 | 简单"后提交者整体失败" | 完整 OCC：检测+解决+部分成功（PR 系列即书中主角） |
| 默认 resolver | — | RECORD_INDEX（依赖 metadata 表） |
| 多引擎多写 | Spark 勉强 | Flink/Spark 混合写者可用（需外部锁） |
| 与表服务协同 | 粗 | planner constraint + pending_* instant 细化 |

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "Spark 默认有锁，多作业并发写一张表安全" | 默认 InProcess 锁只在一个 JVM 内有效；跨作业必须外部锁 + `write.tasks` 相关并发开关 |
| "OCC 冲突 = 一方全丢" | 解析器支持部分成功：不同 key 落在同一文件也能各留各的 |
| "锁粒度越粗越安全" | 粗锁把提交路径串行化，吞吐塌方；Hudi 只在 preCommit/commit 的窄缝用锁 |
| "开了多写者性能就线性扩展" | 冲突面随写者数平方增长；书与官方都建议"逻辑上单写、物理上分区隔离" |
| "commit 时看不到 inflight" | 并发 inflight 正是检测对象：清单会按 instant time 全序回放 |

## 与其他章 / 其他笔记的联系

- 7.3 阶段三的回放对象 = [02-Hudi快速入门.md](02-Hudi快速入门.md) 2.3 的三态 timeline；7.5 的 key 集合比较依赖 [05-索引与元数据表.md](05-索引与元数据表.md) record_index/column_stats。
- 7.4 planner constraint 管的是 [06-维护与优化Hudi表.md](06-维护与优化Hudi表.md) 的结构类 instant（clustering/compaction）。
- Flink 侧两阶段提交与 Hudi 提交的握手 → [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)。
- OLTP 对照（本章最值得互文）：Wound-Wait/死锁回滚 vs OCC 部分成功；MySQL 的"提交 = 写 binlog" vs Hudi 的"提交 = 回放并发清单后盖章"——见 [../../db/db.md](../../db/db.md) 与 [../数据库系统概念6/15-并发控制.md](../数据库系统概念6/15-并发控制.md)。
