# 04 使用 Kafka Streams 进行查询（Querying with Kafka Streams）

> 书目 #157 第 4 章 ｜ 主题：Kafka Streams 是什么、Quarkus 承载服务、运行与查询 HTTP 端点、Kafka Streams 的局限性。
> 精读重构（目录 ✅，展开 ⚠️），非原书文本。

## 本章任务

- 掌握"把 Kafka Streams 当嵌入式查询引擎用"的最小形态：消费→聚合→本地状态→HTTP 暴露；
- 理解 Quarkus 在本册的角色（JVM 原生云框架，承载 Streams 应用与 REST 层）；
- 重点吃透 4.6：**Kafka Streams 局限性清单**——它是全书转向 Pinot 的正式理由。

## 4.1 什么是 Kafka Streams（What Is Kafka Streams）

- 定义：跑在应用进程内的**流处理库**（不是集群产品）——无独立 master/TaskManager，部署面=普通微服务；
- 核心抽象：`KStream`（记录流）/`KTable`（变更流折叠成的键状态视图），`group_by + windowed aggregation + reduce/aggregate` 构成分析原语；
- 状态存储：本地 RocksDB/内存 state store + changelog topic 恢复（"本地 KV + 日志重建"架构）；
- 与理论层对齐：流表二象性与窗口语义见 [../Streaming_Systems/08-流式SQL.md](../Streaming_Systems/08-流式SQL.md) 及 06 章；Streams 的 KTable 就是"折叠后的流"。
- ⚠️ 具体 DSL 方法名与版本行为以官方文档为准：https://kafka.apache.org/documentation/streams/ ✅（curl 200）。

## 4.2 什么是 Quarkus（What Is Quarkus）

- Red Hat 系的"Kubernetes 原生 Java 栈"：启动快（GraalVM 原生镜像可选）、内存小，把 MicroProfile/RESTEasy 与扩展生态打包；
- 本册用途：`quarkus-kafka-streams` 扩展把 Streams 生命周期托管给应用框架，聚合结果写入本地 store，REST 端点查询该 store；
- 选型语义：**处理器+服务层+API 层合体为单应用**——小规模实时分析的最低运维形态（官方站 ✅ https://quarkus.io/ curl 200）。

## 4.3 Quarkus 应用程序（The Quarkus Application）

目录级重构的组件切分（⚠️ 类名/配置不转述）：

- **生产者**：模拟订单事件向 Kafka 注入（AATD 下单流量）；
- **Streams 拓扑**：`orders` 流 → 按 `restaurant_id`（或品类）key 重分区 → 滚动/滑动窗口计数与金额聚合 → 结果 KTable；
- **查询面**：聚合 KTable 桥接为内存缓存/CDI Bean，REST Resource 暴露 `/restaurants/{id}/order-count` 型端点；
- 心法：端点查询的是**本实例状态分片**，这决定了 4.6 的第一条局限。

## 4.4 运行应用程序（Running the Application）

- dev 模式 + 本地 Kafka（Docker）+ `mvn quarkus:dev` 型工作流（⚠️ 命令组合为通识重构，非书照抄）；
- 观察点：启动回放（ Streams 的持久化 vs 重启全量重放语义）、多实例下分区再均衡（rebalance）对查询完整性的影响；
- 诚实提示：这一节全书最"版本敏感"，笔记只留观察方法不留命令。

## 4.5 查询 HTTP 端点（Querying the HTTP Endpoint）

- 单实例：延迟=进程内 KV 读，微秒~毫秒级，新鲜度=消费滞后（ms~s）——A 类需求达标；
- 多实例：客户端必须知道 key→实例路由（或每端点扇出+合并），否则"半张报表"；
- 这正是"处理器兼任服务层"的边界：**状态按分区散布，查询按业务键汇聚**，两个坐标天然错位。

## 4.6 Kafka Streams 的局限性（Limitations of Kafka Streams）

本册的枢纽结论（重构为五条）：

1. **查询形态窄**：state store 只支持键点查/前缀查，无 ad-hoc 多维过滤、无 SQL、无任意 group by；
2. **路由负担外置**：聚合散布在各实例分区上，横向扩展查询面要自建路由/复制层；
3. **高并发服务非所长**：为吞吐消费优化的进程同时服务大量用户查询会互相挤压；
4. **多维分析成本**：每新增一个维度组合=新增一条拓扑+一个 store（对比 OLAP 引擎"存原始明细，查询时再聚合"）；
5. **重放与回填慢**：改口径要重放历史 topic，计算与数据同生命周期管理成本高。

→ 结论：**Kafka Streams 是优秀的处理器，是勉强的服务层**。第 5 章把"服务查询"卸载给 Pinot，Kafka Streams 回归纯加工位。

## 🔧 实测 E2：增量聚合 vs 全量重算（非本书引擎行为）

用 DuckDB（1.5.5，**非 Kafka Streams**）复刻"状态存储维护聚合"的思想实验：

- 数据：200 万订单事件（1000 个键），时间跨 100 小时；以 T0='2024-01-04 22:00' 为界；
- 对照组：**全量重算** `GROUP BY key`：0.005s；
- 实验组：**增量维护**——先物化 state(key,s,c,wm)@T0，尾部新事件预聚合后 `UPDATE ... FROM inc + INSERT WHERE NOT IN`，测后 `sum(s)`；0.005s；
- 一致性：两组总额/行数**逐位一致**（exact match: True）；
- 解读（概念级）：列式向量化引擎上，百万级"暴力重算"与增量同毫秒——**增量聚合的价值不在小数据的时延，而在成本随新增量而非历史增长**：历史十亿行、或每 5s 触发一次的持续查询时，全量重算不可持续，state store 型增量才有意义。这与 Kafka Streams 以 state store 换"每条 O(1) 摊销"的动机同源。
- 脚本/输出：`D:\develops\tmp\dbwave_w8_brtas\exp.py / results.txt`；聚合语义可再参照 [../DuckDB_in_Action/04-高级聚合与数据分析.md](../DuckDB_in_Action/04-高级聚合与数据分析.md)。

## 与其他册的关系

- Flink 对照（DataStream API/状态后端差异）：[../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md)、[../Introduction_to_Apache_Flink/00-总览与阅读地图.md](../Introduction_to_Apache_Flink/00-总览与阅读地图.md)；
- 精确一次与副作用（Streams EOS 语义讨论的理论底）：[../Streaming_Systems/05-精确一次与副作用.md](../Streaming_Systems/05-精确一次与副作用.md)；
- Kafka 分区/重平衡机制：[../Kafka权威指南.md](../Kafka权威指南.md)。

## 拓扑拆解练习（重构：把 4.3 画成 DAG）

一个"餐厅分钟单量"拓扑的最小分解（⚠️ 方法名以官方 DSL 文档为准）：

- source：`streamsBuilder.stream("orders")` → 反序列化 + 时间戳提取；
- select-key：按 `restaurant_id` 重分区（内部 republish topic，命名带 `.repartition` 痕迹 ⚠️）；
- groupWindow：`groupBy(...).window(TumblingWindows.of(Duration.ofMinutes(1)))`；
- aggregate：`count()` 产出窗口 KTable；
- suppress/materialize：发射策略决定"每分钟一条"还是"随时更新"（⚠️ 语义细节属官方文档面）；
- 桥接：`interactive queries`/本地 store 读 → CDI Bean → REST Resource。

心智要点：**每一步都会产生中间 topic 或本地状态**——运维看到的"莫名 topic"多来自隐式 republish/changelog；这是 11 章容量清单（state 大小）与本课的接口。

## Streams vs Flink 快答（选型面）

| 维度 | Kafka Streams（本册） | Flink（盘上两册） |
|---|---|---|
| 部署形态 | 库，随应用进程 | 独立集群 |
| 状态恢复 | changelog 重放 | savepoint 引导 |
| SQL 支持 | 弱（DSL 为主 ⚠️ 新版 Table API 现状不转述） | 一等公民 |
| 精确一次 | 幂等+事务 EOS（范围内） | 端到端 checkpoint 叙事 |
| 适用团队 | 已有 Kafka、Java 微服务栈 | 专职流平台 |
| 升级痛 | 拓扑变更=重建态 | savepoint 兼容管理 |

- 结论不是"谁优"，而是**组织形态决定引擎形态**（与 02 章"运维面"判据一致）；
- 理论纵深（水位线/窗口/状态函数）Flink 册覆盖更全：见"与其他册的关系"。

## 局限复验法（读完 4.6 后能自己证伪）

1. 试着加一个"按品类×按小时"的新切片 → 需新拓扑新 store → 维度组合爆炸实证；
2. 压测 REST 端点并发 → 消费吞吐随查询 QPS 下降 → 服务非所长实证；
3. 双实例查同一 key → 一端 404/空值 → 路由负担实证；
4. 改聚合口径重放 1 小时数据 → 计时 → 回填慢实证；
（演练基于架构原理重构 ⚠️，非书实验清单。）

## 核心概念速览（中英对照）

- **流处理库** — Stream Processing Library：嵌入应用进程的处理器形态（对位集群式）。
- **KStream/KTable** — Streams DSL 双流/变更表抽象，流表二象性的 API 化身。
- **状态存储** — State Store：处理器本地 KV（RocksDB），聚合结果的物化载体。
- **变更日志主题** — Changelog Topic：状态恢复的日志备份，故障后重建 KV。
- **再均衡** — Rebalance：分区在实例间重新分配，波及查询路由。
- **键点查** — Key Lookup：state store 原生只支持的访问形态。
- **窗口聚合** — Windowed Aggregation：滚动/滑动/会话窗口上的 count/sum。
- **Quarkus** — Quarkus：Kubernetes 原生 Java 框架，托管 Streams 生命周期+REST。
- **原生镜像** — Native Image：GraalVM AOT，Quarkus 冷启动优势来源（⚠️ 通识）。
- **服务层错位** — Serving Mismatch：状态散布坐标≠查询汇聚坐标的结构性矛盾。
- **维度组合爆炸** — Dimensionality Explosion：每维度组合需新拓扑的维护成本。
- **重放回填** — Replay/Backfill：改口径时从日志头部重算的过程。
- **增量 vs 重算** — Incremental vs Full Recompute：成本随新增量或随历史增长的权衡（🔧E2）。

## 最新演进与工业实践

- Kafka Streams 4.x：亚拓扑级线程模型与 metrics 持续演进，官方文档线 ✅ https://kafka.apache.org/documentation/streams/ （curl 200）；本册基于 3.x 早期行为，API 兼容需逐版对照 ⚠️。
- Quarkus 3.x 与 Kafka Streams 扩展仍是"轻量实时"的常见组合 ⚠️ 转述；官方 https://quarkus.io/ ✅200。
- 工业边界共识："Streams 做加工、专用引擎做服务"与 Confluent 自身的表格式产品路线（Tableflow/Flink SQL Gateway 等 ⚠️ 名称未经逐一实证，只作趋势提及）同向。
- 盘上镜像叙事：流式 SQL 如何缓解"查询形态窄"（把 KTable 查询暴露为 push/pull query）见 [../Streaming_Databases/05-流式数据库导论.md](../Streaming_Databases/05-流式数据库导论.md)。
- DuckDB 类比补充（🔧 非本书引擎）：E2 中 `state` 表即手工物化视图；DuckDB 无 MV 语法（E1），增量链需外部编排（cron/dbt 型），这正是"管道即物化视图"的嵌入式实现路径，见 [../DuckDB_in_Action/08-构建数据管道.md](../DuckDB_in_Action/08-构建数据管道.md)。
- 中译对应：机工版第 4 章《使用 Kafka Streams 进行查询》（✅ QQ 读书实抓）。
