# 第 12 章 生产环境中的Trino（Trino in Production ⚠️ 英题推定）

> 全书运维压舱石。二级节标题 ✅ 实抓自 [oreilly.com.cn 官方页](http://www.oreilly.com.cn/index.php?func=book&isbn=978-7-111-73160-3)。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 12.1 使用Trino Web UI进行监控 | 查询列表→stage 树→driver 级细节的三层放大镜 | 先看形态（卡在哪 stage），再动参数 |
| 12.2 Trino SQL查询调优 | 统计/物化视图/下推改写四大杠杆 | 查询调优的 80% 是「让引擎看见数据」 |
| 12.3 内存管理 | 池模型：general/reserved/system + spill | 三类 OOM 报错对应三种处方 |
| 12.4 任务并发性 | task.concurrency 与 driver/页缓冲的乘数效应 | 并发×内存=吞吐/稳定性的交换汇率 |
| 12.5 工作节点调度 | split 调度均衡、拓扑亲和、挂起保护 | 调度不均 = 快节点等慢节点 |
| 12.6 网络数据交换 | exchange 类型与缓冲；FTQ 的外置换存储 | 网络是流水线的血管，也最先堵 |
| 12.7 JVM调优 | GC 停顿/堆布局/容器内存对齐 | GC 日志不读，调优等于蒙眼 |
| 12.8 资源组 | 队列/并发/内存按用户维度准入控制 | 483 起新实现取代 legacy（见文末，大事） |
| 12.9 小结 | — | 「监控→定位→杠杆→护栏」闭环 |

## 核心精讲

### 1. 三层放大镜（12.1）

Web UI（03 章入口）→ 查询详情：stage DAG + 各 stage 的 input/output rows & bytes + 算子耗时 → JSON plan 下载离线看。经验读法（与 4.4 模型对表）：

- **输入量异常大的 stage** → 下推没生效（8.11 的 sargable 违规、分区谓词被函数包裹）；
- **两 stage 行数几乎不变但字节暴涨** → 广播了不该广播的表（缺统计，4.9）；
- **某 task 远慢于兄弟 task** → split 不均/热点分区/慢节点（12.5）；
- 命令行替代通道：`system.runtime.queries/queries`（8.2）与 JMX connector（6.7）——UI 被 10 章关掉的场景就靠它们。

### 2. 内存三池与 spill（12.3）

```properties
# 教学示意：护栏三件套 + 落盘泄压
query.max-memory=100GB            # 集群级，所有查询用户池总和
query.max-memory-per-node=16GB    # 单查询单节点上限
experimental.spill-enabled=true   # 属性名以 483 spill 文档为准 ⚠️
experimental.spill-prefix=/data/trino-spill
```

- **内存池模型（书稿 392）**：general pool（算子内存）/reserved pool（聚合超支续命）/system pool（引擎自身）；三类典型失败：`Exceeded pooled memory`（改查询或加节点）、`worker too many memory reservations`（调度问题）、system 池爆（连接/元数据侧）。483 属性字典 ✅ [properties-resource-management.html](https://trino.io/docs/current/admin/properties-resource-management.html)。
- **spill**：聚合/join/sort 中间态落盘，以吞吐换存活，默认关；FTQ 用 external spool 更进一步（✅ [spill.html](https://trino.io/docs/current/admin/spill.html)、[fault-tolerant-execution.html](https://trino.io/docs/current/admin/fault-tolerant-execution.html)）。
- 第一处方永远是：**分区裁剪/谓词早置/统计到位**，内存参数是第二顺位。

### 3. 并发与调度（12.4/12.5）

- `task.concurrency`：每 task 的 driver 并行度——**驱动级并行**与 split 级并行相乘决定单查询吃几成集群（默认值=核数口径 ⚠️ 以 properties 文档为准）；高并发 BI 场景常需调低。
- worker 调度：coordinator 按「已调度字节」均衡发 split；拓扑亲和（同机架/同区）与「挂起 worker 保护（slow node warning/removal）」是 483 现文重点 ✅ [properties-task.html](https://trino.io/docs/current/admin/properties-task.html)。
- 动态过滤（✅ [dynamic-filtering.html](https://trino.io/docs/current/admin/dynamic-filtering.html)）：build 侧完成前向 probe 侧回推过滤值，join 场景默认收益——书稿时点它刚转正几年，今天基本当「免费」用（个别形态回退仍要 EXPLAIN 验证）。

### 4. 资源组：准入控制的语义（12.8）

```text
# 教学示意：legacy 模型的概念形态（483 已换新实现，见文末！）
group root.bi soft-memory-limit=20GB hard-concurrency-limit=10 ...
group root.etl ...
```

维度：排队上限、并发数、内存份额、按用户/来源路由；目标是「小查询不死、大查询排队」。392 书稿的 file-based legacy 资源组在 483 时代被**数据库支撑的新资源管理器**取代（语义/迁移成本见文末）——这是全书与现状偏差最大的一节。

### 5. 调优剧本（章末整合）

`UI 定位 stage → EXPLAIN (TYPE DISTRIBUTED) 看分发/下推 → ANALYZE 补统计 → 分区/裁剪改写 → 需要才动并发/spill → 资源组限流兜底 → FTQ 救大管道`（顺序即优先级）。

### 6. 故障→处方对照表（本章的「急诊手册」形态）

| 现场症状 | 第一嫌疑 | 确认手段 | 处置顺位 |
| --- | --- | --- | --- |
| 看板整体变慢、UI 排队 | 某大查询占满 general pool | 12.1 stage 树 + queries 系统表 | 资源组限额 → kill → 查改写 |
| 首包快、结果慢 | 客户端拉取/网络瓶颈或终 stage 汇聚单点 | UI stage 字节数 vs 网络计数 | 投影裁剪 → CTAS 落表 → 分页取 |
| `Query exceeded reserved memory limit` | 高基数聚合/join 倾斜 | EXPLAIN 看行数字节比 | 改写预聚合 → 扩节点 → spill |
| 同 SQL 时快时慢 | split 不均/慢节点/缓存冷热 | 12.5 task 时长分布 | 调度参数 → 文件 compaction（06） |
| worker 频死、GC 长停顿 | 堆配置与并发乘数失控 | GC 日志 + 12.4 | 调 task.concurrency → 重算堆预算 |
| 大 ETL 一失败全重来 | 流水线模式无断点 | 查询时长与重试记录 | FTQ + external spool（12.6） |
| 联邦查询打挂线上库 | 源端无限流 | 源端监控 | 只读副本 + connector 池 + 资源组 |

用法：症状行对到「机制节」（括号内 12.x），再回到该节剧本；表中处置顺位刻意保守——引擎参数永远是最后一档，SQL 与数据布局永远是第一档。

### 7. 例行维护日历（预防面）

`ANALYZE 关键表（日/周）· MV REFRESH 编排（Airflow，11.3）· 小文件 compaction（按 connector，06）· 证书/凭据轮换（10）· 版本灰度（release notes 连接器节逐版读，06 演进）· 慢查询 TopN 复盘（系统表周报）`。

## 常见误区

- 见 OOM 就加 -Xmx：reserved/system 池的爆法不同，堆大小不解决倾斜与缺统计（12.3 先判池）。
- spill 开成默认策略：交互式查询 spill 即慢，宁可让它快速失败排队；ETL 才谈落盘（FTQ 更优）。
- coordinator 参与调度但资源不设防：`include-coordinator` 忘关的存量集群，worker 一忙 UI 就假死（5.2 同款）。
- 资源组规则当 SQL 权限（10.2 管数据面，12.8 管容量面，两本账）。
- 用 `kill` 治慢查询而不留 plan：`EXPLAIN ANALYZE`/JSON plan 先下载再 kill，现场即证据。

## 与其他章/其他书的联系

- 本章是 4.4 执行模型的「运维镜像」；参数分层在 [05-生产环境部署.md](05-生产环境部署.md) 已埋；UI/系统表入口在 [03-使用Trino.md](03-使用Trino.md)。
- 通用调优方法论（基线→剖面→干预）对照 [../数据库性能调优.md](../数据库性能调优.md)；Spark 侧的 shuffle/内存对位问题：[../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)（含 [../bigdata/03-Shuffle与宽依赖.md](../bigdata/03-Shuffle与宽依赖.md) 的对比：落盘 shuffle vs 流水线 exchange）。
- GC/JVM 深水区：[../深入理解Java虚拟机3.md](../深入理解Java虚拟机3.md) 式阅读法迁移到 Trino jvm.config。

## 核心概念速览（中英对照）

1. **阶段树** — stage tree：UI 里的执行 DAG，三层放大镜第一层。
2. **JSON plan** — 分布式计划序列化：离线复盘的完整现场（3.5/4.5）。
3. **general pool** — 通用内存池：算子内存的主战场。
4. **reserved pool** — 预留池：聚合等可续命操作的缓冲池。
5. **spill** — 溢写：join/agg/sort 中间态落盘（✅ spill 页）。
6. **task.concurrency** — 任务并发：driver 并行度旋钮。
7. **split 调度** — split scheduling：按字节均衡 + 拓扑亲和。
8. **慢节点处理** — slow node warning/removal：挂起节点保护。
9. **exchange 缓冲** — exchange buffer：跨 stage 拉取的内存背压面。
10. **动态过滤** — dynamic filtering：build→probe 的运行期谓词回推 ✅。
11. **资源组** — resource groups：查询准入与容量配额（483 新实现见文末）。
12. **排队上限** — queue limits：突发流量的削峰阀。
13. **GC 停顿** — GC pause：流水线引擎的隐性长尾来源。
14. **FTQ** — fault-tolerant execution：以 spool 落盘换 ETL 韧性的模式 ✅。
15. **调优优先级** — optimization order：裁剪/统计先行，参数与扩容殿后（剧本）。

## 最新演进与工业实践

- **资源组换心（重磅）**：Trino 461+ 引入**基于数据库表的新资源管理器**（配置即表、支持动态修改/加权公平队列等），legacy 文件规则进入退场轨道——书稿 12.8 需整体重读 ✅（新管理器的文档属性面见 [properties-resource-management.html](https://trino.io/docs/current/admin/properties-resource-management.html) 与逐版 release notes；生效版本号按 release-483 索引回溯 [release-483.html](https://trino.io/docs/current/release/release-483.html)，本次未逐条定位 ⚠️）。
- **自适应与自动调优**：plan caching、自适应聚合/连接（adaptive filter/optimizations）在 392→483 间持续增强（✅ release notes 高频项）；「参数越少越好」是明确产品方向（官方 Vision 页口径 ⚠️ 未逐抓）。
- **FTQ 生产化**：external exchange/spooling（✅ [fault-tolerant-execution.html](https://trino.io/docs/current/admin/fault-tolerant-execution.html)）让 Trino 吃到「湖上批量 ETL 可恢复」的场景——与 Spark 正面竞争的关键补丁；「交互默认、批量 FTQ」成双模式共识。
- **可观测栈**：事件监听 + 系统表 + Prometheus 生态 exporter（社区）组成生产标配；慢查询画像与成本归因走查询事件仓库（工程实践 ⚠️）。
- **与 DuckDB/ClickHouse 的分层**：单机亚秒层（DuckDB ✅ [duckdb.org](https://duckdb.org/)）— 预聚合/OLAP 库（数仓书群）— 湖上联邦（Trino）三层各司其职，「全用 Trino 硬扛高频小查询」被生产反复证伪（选型口径 ⚠️ 转述）。
