# 05 · Cypher 查询调优与执行计划（Ch.5，章题为 ⚠️ 逆推重构）

> 取证锚点（✅ 实抓配套仓库 chapter05，33 个脚本 + README）：README 标题 “Chapter 5: Setting Up the Database”（给本章发数据集：整库 backup 恢复或 admin import 二选一）；脚本族 `explain-global/tonight`、`profile-tonight`、`explain-disconnected`、`disconnected-collect/tracks`、`selective-1..6` 与 `selective-index-1..3`、`access-1/2`、`degrees-1..3`、`eager-1/2`、`sorting-1..5`、`planner-1..4`、`runtime-1/2`。**一个查询调优章配了 33 个可跑脚本**，是全书密度最高的一章。

## 5.1 EXPLAIN 与 PROFILE：看计划，再看真跑

- `EXPLAIN` 出计划不执行；`PROFILE` 执行并给每个算子的 rows/db hits/time。
- 本章的开场姿势（`001-explain-global`、`002-explain-tonight`）：先问“**整个库的计划长什么样**”，再问“今晚这条查询怎么选”——全局统计信息（`DB STORE SCAN` 基数估计）与单查询计划的关系 ⚠️ 细节推定。
- Neo4j 不装不跑 ⚠️：以下算子语义均文档转述 + 脚本名逆推，无本机复现。

## 5.2 起点算子与选择性（selective 系列）

`selective-1..6` 对比“同一逻辑、不同谓词形状”的起点选择：

- 有索引属性起手（NodeIndexSeek）vs 全扫（NodeByLabelScan）；
- 谓词下传时机：`WHERE` 里对属性过滤 vs 模式内联 `{prop: ...}`；
- `selective-index-1..3` 展示**加了索引之后**同一族查询的计划翻转——与 04 章“artistNameIndex”呼应：先有索引决定，后有调优结果。

选择性驱动遍历方向：从“匹配结果少的端点”起手，扩展代价差一个量级。

## 5.3 度数是隐形成本（degrees 系列）

`degrees-1..3` 对应 god node（枢纽节点）议题：

- 一个流派节点挂 10 万曲，任何经过它的模式在扩展时先付出 10 万邻居的代价；
- 诊断：`size((n)-->)` 度分布抽样（02 章体检清单的延续）；
- 缓解：给高度数节点加类型/属性限定扩展、把高频中转关系预聚合（回到 03 章物化决策）、或模型上拆掉超级枢纽（04 章 Genre 的代价回收 ⚠️ 衔接推定）。

GD2e 03 章同名反模式的工程深化版（[../Graph_Databases_2e/03-使用图进行数据建模.md](../Graph_Databases_2e/03-使用图进行数据建模.md)）。

## 5.4 断连查询：模式写错的样子（disconnected 系列）

`004-explain-disconnected` 是神来之笔：**两个不连通的模式部件**（`MATCH (a),(b)` 无连接条件）产生笛卡尔式 `Product` 算子。三连（explain → collect 版 → tracks 版）演示：

- 意图“配对”但漏写连接条件时，计划里 Product 的行数是两段子结果之积；
- 修复靠 `WITH` 重排或补模式连接；
- 教训：**计划树形状是建模意图的 X 光片**——写歪了，算子先知道。

## 5.5 EAGER 算子：物化屏障（eager-1/2）

5.x 经典议题（⚠️ 转述）：Cypher 是行流模型，但**写操作改变读视图**（如 `CREATE` 后再 `MATCH` 会读到刚建的行），优化器在读写交界处插 `Eager`（旧版 `VerifyAllocating`/`Eager` 家族）强制物化当前行流——排序、聚合、DISTINCT 同样形成 pipeline breaker。

- `eager-1/2` 对比“把写放最后”与“读写交错”的计划差异；
- 实践口诀：**读写分离，写置尾部**；必须交错时用 `CALL {子查询} IN TRANSACTIONS` 显式分段。

## 5.6 排序与分页的五重奏（sorting-1..5）

`ORDER BY` 的代价随输入行数与属性可索引性变化：

- `sorting-1/2`：全排序 vs 用索引天然序（RangeIndexSeek 输出已有序时可省 Eager）；
- `sorting-3/4`：`LIMIT` 与 TopN（排序前截断的收益与失效条件——先 `collect` 再排序就吃不到 TopN）；
- `sorting-5`：表达式排序（函数包裹属性 → 索引序作废）。

与关系库同源议题的图库版，对照 [../mysql/00-总览与阅读地图.md](../mysql/00-总览与阅读地图.md) 的 filesort/索引排序章：同构问题（有序性传递），不同算子名。

## 5.7 Planner 与 Runtime 的旋钮（planner-1..4、runtime-1..2、access-1/2）

- Planner 模式：成本基 vs IDP 规则基（5.x 默认 cost planner，`COST`/`IDP` hint 可切 ⚠️）；`planner-1..4` 演示 hint 与统计信息交互；
- Runtime：Slotted（默认）vs Pipelined（大并行读）——`runtime-1/2` 对比同一查询在 `CYpher RUNTIME pipelined` 下的形态 ⚠️ 语法大小写以手册为准；
- `access-1/2`：属性存取方式对计划的影响（索引Seek vs 回表过滤）⚠️ 推定。

## 5.8 方法论总结：调优 SOP（重构）

1. 先测：`PROFILE` 找行数瀑布的“爆炸点”（db hits 集中算子）；
2. 再想模型：这个查询形状是验收查询吗？连接条件漏了吗（Product 预警）？
3. 再想索引：起点端点能不能 Seek？（selective-index 系列的教训）
4. 再想度数：穿过 god node 吗？（degrees 系列）
5. 最后动旋钮：planner/runtime hint、子查询分段、写置尾部（5.5/5.7）。
   顺序不可颠倒——旋钮是最后手段。

## 5.9 计划病理对照表（速查重构）

| 计划签名 | 病理 | 首选药 | 本章证据 |
|---|---|---|---|
| `NodeByLabelScan` 起手 | 查找属性无索引 | 建 range 索引 | selective-index-1..3 |
| `AllNodesScan` | 无标签模式/全局聚合误用 | 补标签或改度缓存 | access-1/2 ⚠️ |
| `Product` 行数≈左×右 | 断连模式漏连接条件 | 补模式或 CALL{UNION} | disconnected 系列 |
| `Eager` 卡管道中段 | 读写交错 | 写置尾/子查询分段 | eager-1/2 |
| `Sort` 输入 ≫ LIMIT | collect 在先毁 TopN | 调整聚合与排序次序 | sorting-3/4 |
| `Expand(Into)` db hits 尖峰 | 穿越 god node | 限类型/预物化/拆枢纽 | degrees-1..3 |

读法：PROFILE 输出从上往下扫，第一处“行数瀑布”即病点——本表是 5.8 SOP 第 1 步的词典。

## 5.10 调优实验记录模板（工程转写）

```
查询编号/业务意图:      （对应 Ch.3 验收查询序号）
基线 PROFILE:           rows/dbHits/time @ 爆炸算子=
假设（SOP 第 2-4 步）:   模型? 索引? 度数?
动作:                   索引|重构|hint（记录 5.11 纪律）
复测:                   ΔdbHits=   Δtime=   计划形状变化=
回滚方式:               （hint 撤除/索引 drop 语句）
```

书的 33 个脚本对本质上就是 33 组“假设-动作-复测”三元组（✅ 命名模式：坏版本在前、修正版在后），模板是把这种节奏制度化。

## 5.11 统计信息与计划翻转（5.x ⚠️ 转述）

成本计划器的输入面：标签/关系类型计数（来自计数存储，Ch.9）、属性存在性与直方图类统计、`planner=`/`runtime=` hint 覆盖。统计滞后或缓存旧计划时，“同一查询不同日子两个样子”的第一嫌疑人就是它——诊断路径：对比 `PROFILE` 的估计行数 vs 实际行数（误差两位数量级即怀疑统计）；万不得已才 `CYPHER planner=idp` 或 `OPTIONAL` hint 锁计划（`planner-1..4` ✅ 脚本族主题 ⚠️ 细节转述）。

hint 三纪律（重构）：**只在计划翻转已被证明后用；hint 写进配置管理而非代码字符串；每条 hint 挂复查到期日**——hint 是止痛药不是手术刀。

## 5.12 本章与兄弟册的坐标系

- 有序性传递/物化屏障/TopN 三件套的关系库版本：[../mysql/00-总览与阅读地图.md](../mysql/00-总览与阅读地图.md)；
- 代价模型与基数估计的通用引擎叙事：[../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md)；
- 🔧 可跑对照（DuckDB 1.5.5，非 Neo4j）：`EXPLAIN ANALYZE` 在 demo 系列里给出“递归 CTE 的行数瀑布”，与 PROFILE 读法同构——本目录用它替代不能跑的 Neo4j PROFILE，结论只做概念校准不做数字对比。

## 核心概念速览（中英对照）

- **执行计划** — Execution Plan：EXPLAIN/PROFILE 输出的算子树
- **db hits** — DB Hits：逻辑读取次数，Neo4j 性能的第一货币
- **NodeIndexSeek** — Index Seek：以索引直接定位起点的算子
- **Product 算子** — Product：断连模式产生的笛卡尔式组合爆炸
- **Eager 算子** — Eager：读写交界/排序聚合处的强制物化屏障
- **TopN** — Top-N Sort：LIMIT 与 ORDER BY 合流的截断排序
- **成本优化器** — Cost Planner：5.x 默认计划生成器，依赖统计信息
- **Pipelined 运行时** — Pipelined Runtime：多线程片算的可选执行引擎
- **god node** — God Node：度数爆炸的枢纽节点，遍历成本黑洞
- **谓词下推** — Predicate Pushdown：把过滤搬进 Seek/Expand 以省行
- **PROFILE 工作流** — Profile-First Tuning：以真实算子计数驱动调优的纪律

## 最新演进与工业实践

- **统计信息常态化**：5.x 起成本计划器依赖自动列统计（`CALL dbms.clearCommittedTx...` 无关；统计刷新过程 ⚠️ 未逐一实抓），2025.x 延续；本书 33 脚本的“计划对照实验”范式官方化为查询调优指南（https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/ 家族，域可达 ✅，逐页未核 ⚠️）。
- **查询洞察产品化**：Ch.11 的 query insights/`SHOW QUERY PARAMETERS` 体系在 2025.x 与 Aura 监控合流——把本章手工 PROFILE 升级为平台常驻能力 ⚠️ 转述。
- **同题异构对照**：关系库侧的“索引决定起点/物化屏障/TopN”三件套在 [../mysql/00-总览与阅读地图.md](../mysql/00-总览与阅读地图.md) 与 [../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md) 有通用版；DuckDB 的 `EXPLAIN ANALYZE` 给🔧可跑对照（本目录 01/02/08 章演示均出自该引擎，1.5.5 ✅）。
- **论文线**：属性图基数估计与子图匹配代价模型近作追踪归 [../../db/db.md](../../db/db.md)。
