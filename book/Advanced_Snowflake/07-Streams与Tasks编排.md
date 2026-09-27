# 07 · Streams 与 Tasks 编排进阶（⚠️ 推定主题章，任务书 ★ 关键词）

> **性质声明**：推定主题重构（[00](00-总览与阅读地图.md)）。机制=官方文档转述（⚠️）+✅URL；
> 🔧 类比用 DuckDB 1.5.5 水位表增量装载（**非 Snowflake 行为**）。TDG 对位：
> [../Snowflake_The_Definitive_Guide/03-数据库对象.md](../Snowflake_The_Definitive_Guide/03-数据库对象.md)（流/任务入门面）。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 7.1 | 对象栈定位：流=变更游标，任务=调度器 | 两者合起来才是"增量" |
| 7.2 | 流的三种形态与 offset 语义 | standard/appender/(delta 前沿 ⚠️) |
| 7.3 | 任务原子：单 DML + 仓库上下文 + 调度表达式 | SCHEDULE 即 cron 语义 |
| 7.4 | 多步图与条件触发 | AFTER 依赖 + WHEN 谓词=无外部编排器 |
| 7.5 | 任务家族新成员 | serverless 任务、Python/JVM 任务、错误通知 |
| 7.6 | Dynamic Tables：声明式增量层 | "写查询，平台算增量"的对偶面 |
| 7.7 | 编排选型：何时上外部 DAG 工具 | 平台内图 vs Airflow 的边界 |
| 7.8 | 🔧 类比：水位表+增量 INSERT 两连发 | 批1=19,999 行、批2=0 行 |

## 核心精讲

### 1. 流=变更游标（转述 ⚠️）
流记录源对象（表/视图/另一个流）自**上次偏移**以来的 INSERT/UPDATE(拆两行)/DELETE 行，
`METADATA$ACTION`、`METADATA$ISUPDATE`、`METADATA$ROW_ID` 三伪列消费；读取流的事务完成
offset 推进——**"查了但没推进事务=重放"是最大事故源**。
✅ https://docs.snowflake.com/en/user-guide/streams-intro
✅ https://docs.snowflake.com/en/sql-reference/sql/create-stream
Appender 模式跳过 DELETE 传播（append-only 场景省维护 ⚠️）。
✅ https://docs.snowflake.com/en/user-guide/streams-manage

### 2. 任务：调度原语（转述 ⚠️）
`CREATE TASK … WAREHOUSE=… SCHEDULE='USING CRON …' | 'INTERVAL' AS <single DML>`；
进阶面：**图**（`AFTER a,b`）、**条件**（`WHEN SYSTEM$STREAM_HAS_DATA('S')` 短路空跑）、
错误通知集成、serverless 计算形态（任务框架算力，不占自有仓库 ⚠️）。
✅ https://docs.snowflake.com/en/sql-reference/sql/create-task
✅ https://docs.snowflake.com/en/sql-reference/sql/alter-task
✅ https://docs.snowflake.com/en/user-guide/tasks-graphs
✅ https://docs.snowflake.com/en/user-guide/tasks-python-jvm
✅ https://docs.snowflake.com/en/user-guide/tasks-intro
```sql
-- 教学示意，非书中原文
CREATE TASK load_stg WAREHOUSE=w_etl SCHEDULE='5 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('stg_stream')
  AS MERGE INTO stg USING (SELECT * FROM stg_stream WHERE METADATA$ACTION='INSERT') s
     ON stg.id=s.id WHEN NOT MATCHED THEN INSERT ...;
```
（条件函数名以页内为准 ⚠️；MERGE 吞流的标准姿势是官方示例惯型。）

### 3. 编排语义细节（转述 ⚠️）
- 任务状态机（started/paused）与 **begin/end 时间窗**（`ALLOWING`）控成本；
- 上游失败下游**不自动级联**——空转保护靠图+条件，观测靠 `TASK_HISTORY` 视图
  ✅ https://docs.snowflake.com/en/sql-reference/account-usage/task_history （经索引发现，200 见收口注）
- Snowflake Scripting 过程可作为任务体，替代外部 DAG 的"胶水代码"（第 9 章接口）。

### 4. Dynamic Tables：从"过程式图"到"声明式增量"（转述 ⚠️，2024+ 新面）
`CREATE DYNAMIC TABLE … TARGET_LAG='10 MINUTE' AS SELECT …`：平台自动维持基表→目标表的
增量刷新（内部自建流/任务/管道 ⚠️），人只声明目标新鲜度。官方决策指南明确三者分工：
简单聚合链上动态表、复杂控制流仍用 streams+tasks、重算兜底用 `ALTER … REFRESH`。
✅ https://docs.snowflake.com/en/user-guide/dynamic-tables/decision-guide
✅ https://docs.snowflake.com/en/user-guide/dynamic-tables/design-patterns
✅ https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table
✅ https://docs.snowflake.com/en/user-guide/data-pipelines-intro

### 5. 🔧 本地镜像实验（DuckDB 1.5.5，**非 Snowflake 行为**）
命题："offset 推进=增量正确性的全部"。水位表 `ck(last_id)` + 增量
`INSERT … SELECT … WHERE id > (SELECT last_id FROM ck) ON CONFLICT DO NOTHING` 连发两班：
**批1 处理 19,999 行、批2 处理 0 行、目标表 19,999 行**——幂等推进成功。反向实验：若第二班前
手动 `UPDATE ck SET last_id=0`，一切重放——这就是"流被两个任务共用/忘记消费偏移"的病灶模型。
（脚本 E5。差异声明：DuckDB 无元数据层 offset 事务耦合，Snowflake 的流推进绑定在刷新事务里，
本实验只类比"水位驱动增量"抽象，不类比 ACID 细节。）

## 常见误区

| 误区 | 事实（转述 ⚠️） |
| --- | --- |
| "流会自己清空" | offset 由消费事务推进；只 SELECT 不推进=下次重放 |
| "任务=定时脚本" | 单语句+图+条件+通知才是完整形态 |
| "一个任务写多条语句" | 任务体是单 SQL/单过程调用，多步要拆图 |
| "空跑不花钱" | 每次唤醒起仓库/耗服务额度，WHEN 短路是省账单件 |
| "Dynamic Table 淘汰了 tasks" | 复杂控制流（重试/分支/外部信号）仍需显式图或外部编排 |

## 与其他章、其他书的联系

- 上游变更源头的装载层 → [08-数据摄入进阶.md](08-数据摄入进阶.md)；流上 VARIANT 展开 →
  [06-VARIANT与半结构化数据.md](06-VARIANT与半结构化数据.md)；任务归因打标 →
  [02-成本模型与计费内核.md](02-成本模型与计费内核.md)；过程体编程面 → [09-Snowpark与编程面.md](09-Snowpark与编程面.md)。
- 入门对读：TDG-03/TDG-06。
- 增量计算谱系（强互链）：[../Streaming_Databases/00-总览与阅读地图.md](../Streaming_Databases/00-总览与阅读地图.md)
  （连续查询/物化视图增量维护的理论线）、[../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)
  （开放表上的流式增量）、[../设计数据密集型应用/11-流处理.md](../设计数据密集型应用/11-流处理.md)。
- 血缘新页（2026）：官方文档已出现 **"Streams on the data lineage graph"** ✅
  https://docs.snowflake.com/en/user-guide/lineage-streams（第 10 章主场，接口预留）。
- 【登记·同波不链】与 `Introduction_to_Apache_Flink`（水位线/Exactly-once 对照）、
  `Advanced_Analytics_with_Spark_2e`（批式编排对照）波尾闭环。

## 核心概念速览（中英对照）

1. **流** — stream：记录上游 DML 变更的游标对象，offset 事务式推进。
2. **伪列** — METADATA$ACTION / $ISUPDATE / $ROW_ID：流消费三件套。
3. **appender 模式** — 忽略 DELETE 传播的流形态，append-only 专用。
4. **任务** — task：绑仓库、cron/固定间隔调度的单语句执行单元。
5. **任务图** — task graph：AFTER 依赖构成的平台内 DAG。
6. **条件任务** — WHEN 谓词（如流有数据才跑）：空转保护。
7. **serverless 任务** — 用任务框架算力执行的形态（不占自有仓库 ⚠️）。
8. **任务历史** — TASK_HISTORY：状态/重试/时长观测面。
9. **动态表** — dynamic table：声明 target lag 的托管增量表。
10. **目标滞后** — target lag：新鲜度 SLA 的唯一旋钮。
11. **水位表** —（🔧类比物）ck(last_id)：手动 offset 的最小模型。
12. **Snowflake Scripting** — 过程语言：任务体的胶水层（第 9 章）。

## 最新演进与工业实践

**2024–2026（URL 均 2026-09-27 curl -L 实测 200 ✅）：**

- **动态表成为默认叙事**：docs 索引中 dynamic tables 相关页 29 条（决策指南/设计模式/克隆/仓库
  选型成套 ✅），"streams+tasks 手工图"退居复杂控制流场景（⚠️ 转述自官方页间定位）。
- **任务可编程面扩张**：Python/Java serverless 任务专页 ✅（tasks-python-jvm）+ 任务错误通知
  云消息集成（✅ /user-guide/tasks-errors-integrate）。
- **血缘可视化接管可观测性**：lineage-streams 页 ✅ 标志"流任务图"并入对象血缘图，运维排障从
  TASK_HISTORY 单点走向图级（与第 10 章共振）。
- **工业实践 ⚠️（转述）**：CDC 中台 2025+ 两条主流——全托管动态表（≤3 层聚合链）或
  外部编排（Airflow/Dagster）+ Snowflake 仅作执行器；中间形态（大手工任务图）被视为技术债。
- 补课：增量计算原理 → [../Streaming_Databases/00-总览与阅读地图.md](../Streaming_Databases/00-总览与阅读地图.md)。

**文献与文档**：streams-intro / create-stream / streams-manage / create-task / alter-task /
tasks-graphs / tasks-intro / tasks-python-jvm / dynamic-tables/decision-guide /
dynamic-tables/design-patterns / create-dynamic-table / data-pipelines-intro / lineage-streams（✅200）。
