# 第 4 章 Trino架构（Trino Architecture ⚠️ 英题推定）

> 全书机制心脏。二级节标题 ✅ 实抓自 [oreilly.com.cn 官方页](http://www.oreilly.com.cn/index.php?func=book&isbn=978-7-111-73160-3)。图示与 SQL 为教学示意。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 4.1 集群中的协调器和工作节点 | coordinator：解析/优化/调度；worker：切分 task 执行 fragment | 进程同构、角色配置化，worker 无状态 |
| 4.2 基于连接器的架构 | connector SPI：元数据 + 分片 + 读写三大接口面 | 「一个引擎 N 种存储」全靠 SPI 薄 |
| 4.3 catalog、schema和表 | 三级命名空间 = connector 实例 → 库 → 表 | 名字即路由：`catalog.schema.table` |
| 4.4 查询执行模型 | stage→fragment→task→pipeline→driver；MPP 拉取式 exchange | 一切算子都在 driver 线程里被 push/pull |
| 4.5 查询计划 | 解析→逻辑计划→优化→物理/分布式计划 | EXPLAIN 三连看的是同一条流水线 |
| 4.6 优化规则 | RBO 规则库：谓词下推/列裁剪/常量折叠/聚合下推… | 规则驱动、代价无关的部分最先发生 |
| 4.7 实现规则 | 逻辑算子 → 分布式物理算子（分片、复制、exchange 选型） | 「怎么跑」的选择：partitioned/replicated/broadcast |
| 4.8 基于代价的优化器 | CBO：统计驱动的 join 顺序与分发策略选择 | 没统计的 CBO 近似瞎子，先 ANALYZE |
| 4.9 使用表统计信息 | connector 统计表 + ANALYZE + 自动采集 ⚠️ 书稿口径 | 统计是 CBO 的口粮，Hive/Iceberg 路径各异 |
| 4.10 小结 | — | 带着这张「解剖图」去 05/12 章运维 |

## 核心精讲

### 1. 两阶段式「MPP + 拉取」执行模型（4.1/4.4）

```
SQL → Parser(ANTLR4) → Analyzed AST → Logical Plan
    → 优化器(RBO 规则反复应用 → [CBO 代价决策]) 
    → 分布式 Plan: Fragment(STAGE) × N
    → coordinator 把 fragment 按分片调度到 worker = Task
    → Task 内并行的 Driver 流水线（算子链），跨 stage 用 Exchange 拉取
```

- **coordinator**：查询解析、优化、分片枚举（向 connector 要 splits）、task 调度、结果汇聚；自身默认不参与计算。
- **worker**：通用算子运行时 + connector 插件；对上层「不知道对方是谁」，靠 exchange 传页（固定大小 page）。
- stage 之间是**流水线化**的（非 Hive 式落盘阶段），因此内存与网络背压成为核心变量——12 章的 spill/并发/调度全部围绕这条线。
- 概念对照：Presto 论文 ICDE'19 描述的就是这套 fragment/exchange 架构（论文条目引用 ⚠️ 未过 CrossRef 核验，仅题录转述）；理论坐标见 [../Readings_in_Database_Systems/00-总览与阅读地图.md](../Readings_in_Database_Systems/00-总览与阅读地图.md) 与 [../../db/db.md](../../db/db.md)。

### 2. Connector SPI：架构的第一性（4.2/4.3）

一个 connector 对引擎回答四类问题（✅ [developer 文档口径，release 483 docs 导航含 Developer guide](https://trino.io/docs/current/release/release-483.html)；SPI 细节以官方 Developer guide 为准 ⚠️ 具体小节未逐抓）：

| 接口面 | 回答的问题 | 影响 |
| --- | --- | --- |
| Metadata | 有哪些 schema/table/列/分区/统计？ | 优化器视野与 plan cache |
| Split/分片枚举 | 这表的数据切成哪些可并行单元？ | 并行度与数据本地性 |
| RecordCursor/PageSource | 按分片把行/页交出来 | 扫描吞吐（谓词能否下推在此兑现） |
| 写侧（insert/CTAS/MV） | 能不能写、怎么写、事务语义 | 06/08 章 DML 能力的天花板 |

catalog = connector 具名实例：`SHOW CATALOGS` 看到的每个名字背后是一个 properties 文件 + 一组 SPI 实现。三级名 `catalog.schema.table` 里，Trino 的 schema 多数时候就是**对端系统的库/目录概念映射**，别指望引擎内建新 schema 改变存储。

### 3. 计划三看（4.5–4.8 的动手版）

```sql
-- 教学示意：同一查询的三个镜头
EXPLAIN SELECT s, count(*) FROM lineitem WHERE l_shipdate > date '1995-01-01' GROUP BY s;
EXPLAIN (TYPE DISTRIBUTED) SELECT ... ;   -- 看 fragment 与 exchange 类型
EXPLAIN (TYPE VALIDATE) ...;               -- 只验语法/语义
```

- RBO（4.6）：TopN 下推、LIMIT 穿透 join、半/反连接改写、聚合拆 partial/final、投影/谓词下推到 connector scan——这些**不依赖统计**。
- 实现规则（4.7）：join 分布方式选择——小表 broadcast（replicated）vs 双方按 key 重分布（partitioned）。书稿 392 时代已含 **bucket pruning**（Hive 分桶表）等 connector 特化。
- CBO（4.8）：以行数/NDV/统计区间估算代价，决定 join order（多表 join 时是最大杠杆）与是否物化 broadcast。开关与代价模型细节（`join-reordering-strategy=AUTOMATIC` 一类属性 ⚠️ 属性名以 483 文档 administration 章为准）。

### 4. 统计信息（4.9）：书稿 vs 483 差异最密集的一节

- 392 时代：列级统计主要靠 `ANALYZE` 写入（Hive connector 写 metastore 表级/列级统计），部分 connector 无统计可采。
- 483 现状 ✅（[optimizer/statistics.html](https://trino.io/docs/current/optimizer/statistics.html)）：统计框架持续扩展，Iceberg 等新 native connector 自带统计面（Puffin 类）接入更顺；「connector 支持不支持 ANALYZE」成为查表手册式问题——**用前看对应 connector 页**（06 章）。
- 误区链：没统计 → join 顺序拍脑袋 → 广播了大表 → OOM/超时 → 「Trino 不稳」，实际是第一行 `ANALYZE` 没跑。

### 5. 一条 SQL 的全链路账单（本章整合）

以 4.5 的分布式 EXPLAIN 为账本，一条湖上 join 的成本被拆成四行账：

| 账行 | 决定者 | 可干预点 |
| --- | --- | --- |
| 扫描字节 | connector 下推 + 分区/桶裁剪 + 文件格式 | 8.11 谓词写法、06 章表设计 |
| shuffle（exchange）字节 | join 分发选型 | 统计（4.9）、hint/改写（08 章） |
| 中间驻留内存 | 聚合/join 构建侧大小 | 预聚合、广播阈值（12.3） |
| 落盘与否 | spill/FTQ 策略 | 12.6 双模式 |

架构章的终局读数：**性能问题最终都落回这四行账里的一行**——这就是 04 与 12 的分界线。

## 常见误区

- 「worker 会缓存数据」：worker 无状态，重复查询的加速来自 connector 端/缓存层（RubiX 类，11 章）而非引擎。
- 「coordinator 也是 worker」：可以配（学习集群），生产不配；coordinator 被大 query 压垮会连坐全集群（12 章）。
- 把 exchange 当 shuffle：Trino 是**拉取式** exchange + 流水线 stage，不是 MR 式落盘 shuffle——所以它对低延迟友好，对「超大中间结果」脆弱，需要 spill/分区裁剪来补短板。
- 以为统计自动存在：多数 connector 需手动 `ANALYZE`（483 起部分自动采集在推进 ⚠️ 未逐 connector 核）。

## 与其他章/其他书的联系

- 4.1 的拓扑 → [05-生产环境部署.md](05-生产环境部署.md)（节点/JVM）与 [12-生产环境中的Trino.md](12-生产环境中的Trino.md)（背压与 spill）。
- 4.2 的 SPI → [06-连接器.md](06-连接器.md)（常用 connector 逐一过）与 [07-高级连接器示例.md](07-高级连接器示例.md)。
- 4.8/4.9 → Volcano/Cascades 理论在 [../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md) 与 [../../db/db.md](../../db/db.md) 论文线的对应条目。
- Spark SQL Catalyst 与 Trino 优化器的对照表：[../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md) + [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)。

## 核心概念速览（中英对照）

1. **协调器** — coordinator：解析/优化/调度/汇聚的中心节点进程。
2. **工作节点** — worker：执行 task 的无状态计算节点。
3. **连接器 SPI** — connector SPI：元数据、分片、读页、写入四组扩展接口。
4. **命名空间三级** — catalog/schema/table：`catalog.schema.table` 名字即路由。
5. **分片** — split：并行的最小数据单元，由 connector 枚举。
6. **阶段** — stage/fragment：计划的分布式切分单元，跨 stage 用 exchange。
7. **任务** — task：fragment 在某 worker 上的实例化。
8. **驱动** — driver：task 内并行执行算子链的流水线单元。
9. **交换** — exchange：stage 间拉取式数据流（≠落盘 shuffle）。
10. **规则优化** — RBO optimizer：谓词下推、列裁剪、TopN 穿透等代价无关改写。
11. **实现规则** — implementation rules：逻辑算子到分布式物理算子的选型（含 join 分布）。
12. **代价优化器** — CBO：统计驱动的 join 顺序/分发决策。
13. **表统计** — table statistics：行数/NDV/取值分布，`ANALYZE` 生产。
14. **广播连接** — broadcast/replicated join：小表复制到各端，省重分布。
15. **分桶裁剪** — bucket pruning：借 Hive 分桶元数据跳过无关桶 ⚠️ 书稿特色节。

## 最新演进与工业实践

- **483 文档导航仍是本章骨架** ✅：Overview/Query optimizer/Administration/Connectors 分区与本章一一对应（[docs current](https://trino.io/docs/current/overview/concepts.html)）。
- **优化器持续加码**：392→483 的 release notes 中「Query optimizer」「plan caching」「dynamic filtering」高频出现（✅ [release-483.html](https://trino.io/docs/current/release/release-483.html) 索引页可回溯逐版）；动态过滤默认开且增强（✅ [admin/dynamic-filtering.html](https://trino.io/docs/current/admin/dynamic-filtering.html)），书里 8 章（1e）/练习中手动 `JOIN_FILTER` 时代的坑已过时。
- **FTQ（容错执行）**：本模型是流水线、失败即重跑整 query；483 已提供 fault-tolerant execution（external exchange + spooling，牺牲延迟换大 ETL 韧性）✅ [admin/fault-tolerant-execution.html](https://trino.io/docs/current/admin/fault-tolerant-execution.html)——书成稿时该特性尚年轻，工程上「交互式不 FTQ、批量开 FTQ」是当下共识（转述自官方文档定位句 ✅）。
- **统计与 CBO**：connector 统计支持矩阵继续扩张，Iceberg/Delta/Hive 路径各异（✅ 各 connector 页，06 章互链）；生产上「join 慢先 ANALYZE + EXPLAIN (TYPE DISTRIBUTED)」仍是黄金两板斧（工程口径 ⚠️）。
- **代码坐标** ✅：引擎源码 [github.com/trinodb/trino](https://github.com/trinodb/trino/releases)（releases 页实抓可达；主干即文档站「Trino 483」）。
