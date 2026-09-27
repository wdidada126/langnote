# 04 Presto 的架构

> 原书第 4 章（中译本 p.39–64）。全书硬核：组件拓扑、执行模型、优化器三段式与 CBO。
> 书评公认"第 4 章讲原理，受用"（豆瓣短评语境）——本文件按节重构其推理链。
> 返回 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 4.1 协调器与工作节点 | 单协调器规划、多 worker 执行的对等数据面 | 协调器是"大脑+邮局"，worker 是"流水线工人" |
| 4.2 协调器 | 解析→分析→规划→优化→调度；管理查询状态 | 一条 SQL 的五次形态转换 |
| 4.3 节点发现服务 | worker 心跳注册、协调器感知拓扑（内嵌/外置 etcd ⚠️ 版本差异） | 无中心元数据的最终一致 |
| 4.4 工作节点 | Task→Pipeline→Driver→Operator 层级 | 执行单元的四级嵌套 |
| 4.5–4.6 连接器架构与命名空间 | catalog/schema/表三层映射到外部系统 | Connector 是元数据+Split+记录读写的总 SPI |
| 4.7 查询执行模型 | Stage 树、Exchange、分布式 DAG | 流水线不物化，交互式低延迟之本 |
| 4.8 查询优化：解析分析+初始计划 | AST→逻辑计划→规范化的第一步 | 语法正确≠能跑，分析器还要问连接器"表存在吗" |
| 4.9 优化规则 | 谓词下推/Cross Join 消除/TopN/局部聚合 | RBO 四板斧 |
| 4.10 实现规则 | Lateral Join/Semi-join 去关联化 | 相关子查询改写为非相关 |
| 4.11 基于代价的优化器 | 代价模型（CPU/内存/网络）、Join 代价、统计信息、Join 枚举、广播 vs 分区 | CBO 的朴素样本：统计缺失时退化为启发式 |
| 4.12 表统计信息 | ANALYZE 命令族、写入时收集、Hive ANALYZE、查看统计 | 统计是 CBO 的燃料 |

## 精讲

### 1. 一次查询的形态学（4.2+4.7 合并读法）
```text
SQL 文本 → Parser(AST) → Analyzer(语义校验, 元数据解析) → 初始逻辑计划
   → Optimizer(规则改写 + 代价选择) → 分布式计划(SPlan)
   → 拆成 Stage 树(按 Exchange 边界) → 调度到 worker 成 Task
   → Task 内 Pipeline→Driver 流水线 → Operator 算子间 Page(列式小批) 流动
```
关键不变量：
- **Stage 间以 Exchange 隔开发**：上游 OUTPUT 算子序列化 Page，下游通过 HTTP/内部交换拉取——shuffle 是"拉式流水线"，不是 Hive 式落盘（早期 HttpExchange，Netty 交换为可选路线 ⚠️ 版本相关）；
- **Driver 并行度 = splits 并发**：CPU 密集算子链在 worker 内以 `task.max-worker-threads` 并转（12.4 的参数在此埋下）；
- **Page 列式微批**（数千行）摊薄虚函数与序列化成本，但**不是向量化**——这是与 Velox/ClickHouse 的本质差距（文末演进节展开）。

### 2. 优化四板斧的"为什么"（4.9）
- **谓词下推**：把 `WHERE` 尽量交给连接器（Hive 分区剪裁、JDBC 翻译 SQL、ES 转查询 DSL）——省的是网络与解码；
- **Cross Join 消除**：`ON 1=1` 的显式笛卡尔或无关联条件 JOIN，识别后可退化为可分片的嵌套结构，避免单点爆炸；
- **TopN**：`ORDER BY x LIMIT k` 沿计划树把"全局排序"逐段降级为"各支保 k 条"；
- **局部聚合**：两阶段聚合（partial→final），Exchange 前先 `COUNT→SUM(partial_count)` 化简，把 shuffle 行数压到 NDV 量级。
这四条对任何 MPP/聚合下推型引擎都成立，通用版本参见 [../大数据SQL优化.md](../大数据SQL优化.md)。

### 3. 去关联化（4.10）
Lateral Join、`IN (SELECT ...)` 等相关子查询在 Presto 被改写为 Join/半结构算子：
`x IN (SELECT y FROM t WHERE ...)` → 去重后的 SemiJoin，避免逐行重执行子查询。
这是"声明式 SQL 能跑出过程式效率"的核心机制之一；Spark SQL 的对应叙事见
[../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)（AQE 一节有当代对比）。

### 4. CBO 的朴素样本（4.11–4.12）
- 代价三元组：**CPU 时间 + 网络传输 + 内存驻留**，计划枚举取和最小；
- 统计面：行数/NDV/列 min-max/NULL 率；`ANALYZE table FOR COLUMNS ... WITH (histogram=FDL)` 产直方图
  ⚠️ 直方图类型名（FDL 等）按发行版核对；
- **Join 顺序枚举**为贪心/受限搜索而非全动态规划（书中强调实用主义）；
- **广播 vs 分区 Join**：小表（< `join-distribution-type` 阈值）广播到各 worker 避免两侧 shuffle；
- 没有 ANALYZE 的表：统计缺失 → CBO 回退启发式 → 大表被误广播的翻车是社区经典 issue 题材。
工业对照：Snowflake/BigQuery 全自动统计 vs Presto 手动 ANALYZE，恰是"开源引擎以运维纪律换控制力"的取舍。

### 5. 节点发现的故障语义（4.3）
worker 失联→协调器视拓扑收缩→在途查询失败而非重调度（查询是"尽力而为的一次性编排"）。
这解释了为什么交互式 SLA 靠**多集群+路由**（美团/B 站 Dispatcher 的动机）而不是单集群容错。

## 常见误区

| 误区 | 现实 |
| --- | --- |
| "Presto 有 shuffle 落盘，像 Spark" | Stage 间是内存+HTTP 交换流；内存/网络缓冲打满直接挤兑失败（12.6），不是背压重试到磁盘 |
| "协调器只是负载均衡" | 它还持有全查询生命周期状态机；单协调器是扩展性讨论的中心（13.2） |
| "优化器总是选对计划" | 无统计=猜；书中演示过同查询因统计变化切换 Broadcast/Partitioned 的对照 |
| "列式 = 向量化" | Presto Java 执行按 Page 行迭代式处理，向量化执行属 Velox/原生路线（文末演进） |

## 与其他章/其他笔记的联系
- 参数落地面 → [05-生产环境部署.md](05-生产环境部署.md)、[12-生产环境中的Presto.md](12-生产环境中的Presto.md)；
- 连接器 SPI 的样板解读 → [06-连接器.md](06-连接器.md)；
- 统计与直方图函数面 → [09-高级SQL特性.md](09-高级SQL特性.md)（approx_* 一族与统计学的呼应）；
- 通用优化叙事 → [../大数据SQL优化.md](../大数据SQL优化.md)、Spark 对照 → [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)。

## 本章小结与行动清单

三句话带走：
1. 形态链"SQL→AST→逻辑计划→优化计划→Stage 树→Task→Driver→Operator"是全书查询行为解释器；
   能默写这条链，性能问题就都有了提问框架；
2. RBO 四板斧+去关联化解决"能不能跑"，CBO+统计解决"跑得好不好"——**统计是燃料**，ANALYZE 应进建表默认动作；
3. 拉式流水线 shuffle 不落盘：低延迟与"尖峰内存/网络压力"是同一枚硬币的两面（12.3/12.6 是它的账单）。

实操检查单（有任一可跑实例时）：
- [ ] 对典型查询跑 `EXPLAIN`，找出计划里的 Exchange 边界（LOCAL/GATHER/REPARTITION/REPLICATE 类型与 4.7 的对应）；
- [ ] 执行前 `ANALYZE` 与不执行各跑一次，对比 Join 分布形态变化（CBO 燃料的直观课）；
- [ ] 写一个 `ORDER BY x LIMIT 10`，在 EXPLAIN 里同时找到 TopN 与局部聚合两板斧的痕迹；
- [ ] 写一个含 `IN (SELECT ...)` 的谓词，观察 SemiJoin 的去关联化产物。

自测：
- [ ] 协调器重启对在途查询的影响 vs worker 重启？（4.3 故障语义）
- [ ] 为什么 Page 列式微批≠向量化？差距在哪层被补上？（Velox，文末演进）

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 协调器 | Coordinator | 解析规划调度并汇收结果的中央节点 |
| 工作节点 | Worker | 执行 Task 的对等计算节点 |
| 节点发现 | Node Discovery | 心跳式拓扑感知机制 |
| Stage | Stage | 按 Exchange 切分的计划片段，形成树 |
| Task | Task | Stage 在某 worker 上的实例 |
| Pipeline/Driver | Pipeline / Driver | worker 内算子链与其实例化执行线程单元 |
| Operator | Operator | 物理算子（Scan/Filter/Agg/Join…） |
| Page | Page | 算子间流转的列式微批（数千行） |
| Exchange | Exchange | Stage 间数据重分布通道 |
| 谓词下推 | Predicate Pushdown | 过滤条件移交数据源先执行 |
| 局部聚合 | Partial Aggregation | 两阶段聚合的第一段 |
| 去关联化 | Decorrelation | 相关子查询改写为非相关计划 |
| CBO | Cost-Based Optimization | 以统计与代价模型选计划 |
| Join 枚举 | Join Enumeration | 连接顺序/结合律的搜索过程 |
| 广播 Join | Broadcast Join | 小表全量复制到各节点免重分布 |
| ANALYZE 命令 | ANALYZE Statement | 采集列统计/直方图供 CBO 使用 |

## 最新演进与工业实践

- **执行层换代——Velox 原生执行**：Meta 开源的统一向量化执行库 **Velox**
  （[github.com/facebookincubator/velox](https://github.com/facebookincubator/velox) ✅ 200）成为 Presto C++/原生执行的内核，
  论文 *Velox: Meta's Unified Execution Engine*, VLDB 2022，DOI [10.14778/3554821.3554829](https://doi.org/10.14778/3554821.3554829)
  （✅ Crossref 200 校验）；条目亦见 [../../db/db.md](../../db/db.md) 与
  [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)（Velox star 计数处）。
  本章"Page 行迭代"的 Java 执行模型正被"向量化 + SIMD"路线部分替换（两家进度不同 ⚠️ 以 Release Notes 为准）。
- **优化器持续演进**：2024–2026 两条线均在 CBO（统计自动采集、动态过滤 runtime filter）上加码；
  Trino 的动态过滤与分布式执行器改造见官方文档 [trino.io/docs/current/overview.html](https://trino.io/docs/current/overview.html) ✅ 的
  Query optimizer 章节；prestodb 侧变更日志见 [github.com/prestodb/presto/releases](https://github.com/prestodb/presto/releases) ✅。
- **延迟量化研究**：社区论文 *Presto® Express: Speeding up Query Processing with Minimal Resources*（PVLDB 2023）
  专门优化交互式尾延迟（⚠️ DOI 未通过 Crossref 校验，仅给标题+会议+年份）；
  架构总纲仍是 *Presto: SQL on Everything*（ICDE 2019, DOI [10.1109/icde.2019.00196](https://doi.org/10.1109/icde.2019.00196) ✅）。
- **工业印证**：美团 2014 年即基于本章同类架构做使用实践与改造（[tech.meituan.com Presto 实践](https://tech.meituan.com/2014-06-16/presto.html) ✅）；
  B 站 Dispatcher 的"按语法特征+数据量+负载选引擎"本质是把这些架构性质当成路由特征工程（[dbaplus 原文](https://dbaplus.cn/news-73-4481-1.html) ✅）。
