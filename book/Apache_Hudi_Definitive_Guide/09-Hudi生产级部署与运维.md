# 第 9 章 Hudi 的生产级部署与运维

> 原书章题（译系列核实）：Hudi 的生产级部署与运维。小节地图：认识 CLI（Getting to Know the CLI）→ 执行表级操作（Performing Table Operations）→ 与目录服务同步（Syncing with Catalogs）→ 触发 Post-Commit 回调（Triggering Post-Commit Callbacks）→ 接入监控系统（Wiring Up Monitoring Systems）→ 集成进平台（Integrating into the Platform）→ 性能调优（写入/读取/存储布局/表服务四类）→ 小结。
> 机制口径以官方文档 Operating on the Table / AdminDocs / Monitoring / Tuning 各页为准。

## 本章地图

> 一句话：**生产级 Hudi = 三件事常做常新：元数据一致（CLI/表操作/catalog 同步）、事件外发（post-commit callback）、账本清楚（指标 + 四类调优旋钮）。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 9.1 CLI 与操作入口 | Spark SQL 过程 / hudi CLI / Java 工具类三件套 | 入口多，语义同源（都走 table service API） |
| 9.2 表级操作 | rollback、savepoint/restore、delete partition、clustering/compaction 手动挡、metadata 修复、fsview | 事故手册的正文 |
| 9.3 Catalog 同步 | Hive/Glue/ZK/JDBC 同步；自动 vs 手动 | "查不到新分区"的根因治理 |
| 9.4 Post-Commit 回调 | 提交成功后挂扩展：同步、webhook、质量校验 | 让副作用进入事务边界 |
| 9.5 监控体系 | Dropwizard → JMX/Prometheus/CloudWatch/Datadog；关键指标清单 | 湖仓 SRE 的仪表盘 |
| 9.6 平台集成 | 编排调度、多租户、权限、schema 治理 | Hudi 只当存储事务层，别的交给平台 |
| 9.7 性能调优 | 写 / 读 / 布局 / 表服务四张旋钮表 | 每章机制的运维投影 |

## 核心精讲

> **教学示意，不参与构建。**

### 9.1 认识 CLI：三个入口怎么选

| 入口 | 形态 | 典型命令 |
| --- | --- | --- |
| Spark SQL 扩展 | `CALL hudi.system_conn.run_compaction(...)` 类存储过程 | 交互式运维、调度器里的 SQL 步骤 |
| hudi CLI（hudi-cli.sh） | 独立 shell，连表路径 | `commits show`、`compactions schedule/run`、`cleaner_runs show`、`rollback`、`savepoint` |
| Java 工具类 | SparkJob / Flink 作业 main：`HoodieCompactionJob`、`HoodieCleanerJob`、`HoodieRollbackJob`、元数据校验/复制工具（类名以官方 AdminDocs 为准） | 批调度平台里的"一个任务一个 main" |

- 1.x 文档把"过程 + 独立 job"作为主线；旧版 `hudi-cli` 部分功能已迁移——书中"认识 CLI"一节按此口径展开。

### 9.2 表级操作：事故与日常

```sql
-- 教学示意，不参与构建（Spark SQL）
CALL hudi_system.run_compaction(table => 'db.orders');            -- 手动挡压缩
CALL hudi_system.run_clustering(table => 'db.orders',
     order => 'ts');                                              -- 排序聚簇
CALL hudi_system.savepoint(table => 'db.orders', commit_time => '20260925...');
CALL hudi_system.restore(table => 'db.orders', savepoint_time => '20260925...'); -- 版本钉住/回滚
CALL hudi_system.rollback_to_instant(table => 'db.orders', instant_time => '...');
CALL hudi_system.delete_partitions(...);                           -- 分区硬删（合规/纠错）
CALL hudi_system.run_clean(...); run_archive(...)                  -- 手动清偿元数据债
```

- **rollback 两类场景**：清悬挂 inflight（03 章自动化的手动兜底）；撤销一次已提交但业务错误的事务（第 10 章数据韧性）。
- **savepoint vs restore**：savepoint 把某 instant 标为"cleaner 不许碰"；restore 把当前表状态指回该 savepoint。审计/月度报表要钉版本，靠这两个而不是"调大保留窗口"。
- **metadata 表修复**：`init metadata table` / 重建 record_index / 校验工具（名称以官方为准）；metadata 漂移的典型诱因：外部直接删文件、混用非 Hudi 写者、存储一致性窗口。

### 9.3 与目录服务同步

| 方式 | 触发 | 适用 |
| --- | --- | --- |
| Streamer `--hive-sync` | 每次提交后（9.4 回调实现） | Streamer 管线 |
| Spark/Flink 表选项 | 写提交时自动（`hoodie.datasource.hive_sync.*` / Flink `metastore` + `sync.enable`） | 自管写作业 |
| 独立 HiveSyncTool | 定时批 | 多写者集中治理、glue/多 catalog |

- 同步的是**表存在性、schema、分区清单**；不同步数据版本——目录永远不会"落后于事务"，只会"落后于同步动作"。

### 9.4 🔧 Post-Commit 回调：事务边界的扩展点

```text
提交成功后（原子点之后）依次执行注册的 callback：
  HiveSyncCallBack / JdbcSyncCallBack / ZKSyncCallBack / GlueSyncCallBack / 自定义 webhook 类回调
  （官方 Callbacks 文档列出的插件族）
用途：通知下游、触发质量校验、把表元数据推给平台、记录审计日志
```

- 设计要点：**回滚不触发**；callback 失败不回滚事务——副作用系统要么幂等要么告警，别指望 exactly-once 外呼。
- 这是第 8 章"提交后推进位点"同一机制的通用化。

### 9.5 接入监控系统

- 框架：Dropwizard Metrics → reporter：JMX / Prometheus / CloudWatch / Datadog / Graphite / Console（配置 `hoodie.metrics.*` 家族，官方 Monitoring 文档口径）。
- 值得先建的仪表盘（书中要点 + 官方指标名整理）：

| 组 | 指标（示例名） | 告警含义 |
| --- | --- | --- |
| 写入 | duration / total_upsert_records_written / total_update_insert... | 写吞吐与延迟突变 |
| 读 | file scan 相关、timeline 规划耗时 | 小文件/元数据债 |
| 表服务 | compaction elapsed & failed、cleaner files_deleted、clustering 时长 | 还债速度是否跟上欠债 |
| 元数据 | metadata 表操作耗时、timeline server 响应 | metadata 漂移前兆 |
| Streamer | 每批 fetch/transform/write 计时、checkpoint lag | 端到端新鲜度 |

- 新鲜度 SLO 的正解：`最老未消费 instant 与当前 instant 的差`（增量读端 lag）+ compaction lag（第 6 章）两个数。

### 9.6 集成进平台

- 调度：Spark operator/Airflow/DolphinScheduler 拉起 Streamer 与表服务作业；Hudi 自身无编排。
- 权限与多租户：依赖存储层（ Ranger/S3 bucket policy）+ catalog；Hudi 1.x 无内置行级权限（书与文档一致口径）。
- 与查询平台：Trino/Presto 做交互式层（第 10 章），Spark 做加工层，避免一个引擎包打。

### 9.7 性能调优四张表（全书机制的运维投影）

| 方向 | 旋钮（书→章回链） | 一句话 |
| --- | --- | --- |
| 写入 | 索引选型（05）、小文件策略与并行度（03）、批量大小、MOR log 块格式（06） | 先让 tagging 便宜，再谈并行 |
| 读取 | 查询类型选择（04）、谓词列排序（06 clustering）、data skipping 有效性（05）、timeline server/视图缓存 | 读慢九成是布局问题 |
| 存储布局 | 分区粒度、file group 目标大小、桶数、clustering 节奏 | "分区太碎、文件太小"是湖仓两大绝症 |
| 表服务 | inline/async/standalone 模式（06）、compaction 预算策略、cleaning 窗口 | 还债节奏决定 SLO 上限 |

## 版本演进

| 项 | 0.1x | 1.x（本书基线） |
| --- | --- | --- |
| 操作入口 | hudi-cli 为主 | Spark 存储过程 + Java jobs + Flink action 三轨 |
| 回调 | 仅 hive sync 硬编码 | post-commit callback 插件化 🔧 |
| 元数据运维 | 手工删 .hoodie（危险） | init/rebuild/validate metadata |
| 监控 | 日志 + metrics reporter 基础 | 指标面扩充（timeline server、metadata、clustering） |

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "Hive 看不到新数据 = Hudi bug" | 先查 sync 是否启用、再查分区注册方式；数据早已在表里 |
| "savepoint 等于备份" | 只防 cleaner；数据被删/存储故障仍要快照/异地备份体系 |
| "metrics 接上了就万事大吉" | 没有 lag 类衍生指标（checkpoint lag、compaction lag）的湖仓监控等于只有心电图 |
| "调优 = 调并行度" | 本书口径：并行度排最后；先做索引/布局/表服务模式的结构性选择 |
| "rollback 之后还能继续读旧数据" | rollback 撤销的是 inflight/指定事务；其"未受保留窗口保护的旧 slice"可能已被 cleaning——恢复预案要带保留窗口计算（第 10 章韧性案例） |

## 与其他章 / 其他笔记的联系

- 9.2 每个操作都是 02 章 timeline instant 家族的一员；9.4 与 [08-基于HudiStreamer构建数据湖仓.md](08-基于HudiStreamer构建数据湖仓.md) 的位点推进同构。
- 9.5 的新鲜度告警阈值要按 [06-维护与优化Hudi表.md](06-维护与优化Hudi表.md) 的服务节奏设定。
- SRE 视角对照：《SRE》与仓库内 [../bigdata/11-调度资源与运维.md](../bigdata/11-调度资源与运维.md)、[../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md)。
- 事务语义对照：savepoint/restore ≈ 数据库闪回（[../../db/db.md](../../db/db.md)、[../数据库系统概念6/16-恢复系统.md](../数据库系统概念6/16-恢复系统.md)）。
