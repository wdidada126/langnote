# 04 — SparkSQL 与 DataFrame 转换（Transforming Data with Spark SQL and the DataFrame API）

> 《Modern Data Engineering with Apache Spark》第 4 章 · Apress 2022 · Scott Haines
> 章题与章序 ✅ Crossref DOI `10.1007/978-1-4842-7452-1_4` 实抓；**章内小节结构 ⚠️ 推定**（依据章题与 Spark SQL 官方文档主题域反推），非原书小节文本。
> 三态标记：✅ 实抓 / ⚠️ 推定或转述 / 🔧 本机实测类比（非本书 Spark 平台行为）。

## 1. 本章定位

全书「变换语义」的正面教学：DataFrame 算子与 SQL 文本两种写法、同一编译管线。对数据工程师而言本章的隐性主题是**表达力分级**——能用内置函数就不写 UDF，能用 SQL 计划调优就不重写上卷；工程册会把重心放在「变换的组织方式」而非 API 穷举。

## 2. 双 API 同构（⚠️ 按章题域重构）

- `df.filter(...).select(...).groupBy(...).agg(...)` 算子链与 `spark.sql("SELECT ...")` 文本互为镜像；本书两种写法并陈是 hands-on 册惯例（⚠️ 推定）。
- Column 表达式体系：内置函数库（when/otherwise、coalesce、正则族、日期族）、别名与类型转换。
- 混合风格工程观：子查询拆解成中间 DataFrame 有利调试（命名即文档），全 SQL 化有利审阅——作者立场大概率偏前者（⚠️ 推定）。

## 3. 语义块清单（本章可预期的变换原语）

1. **行级**：select/project、filter/where、withColumn 列演化、drop/rename/cast。
2. **键级**：groupBy+agg、pivot（配合 12 章）、distinct、cube/rollup（若展开则 ⚠️ 未证实）。
3. **序级**：orderBy/sortWithinPartitions、窗口函数 `Window.partitionBy.orderBy` + rank/lead/lag。
4. **集级**：union/intersect/except、join 全家（内/外/半/反；broadcast hint 点到，深水区留给 12 章流式连接与 14 章性能）。
5. **结构级**：explode/flatten、struct/array/map 访问——TDG 04 盘的纵深对应。

对位精读：聚合与复杂类型 [../Spark_The_Definitive_Guide/04-聚合与复杂数据类型.md](../Spark_The_Definitive_Guide/04-聚合与复杂数据类型.md)；SQL 与 Dataset 关系 [../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md](../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md)。

## 4. Catalyst 一瞥（工程册的「够用深度」，⚠️ 重构）

- 分析计划 → 逻辑优化（谓词/列裁剪/常量折叠）→ 物理策略（含 join 选择、AQE 运行时再优化）→ RDD 管线。
- `explain()` 是本章唯一的「必须会按的按钮」：`df.explain(True)` 看四段计划。
- UDF 的代价叙事：不透明表达式阻断优化下推——2022 年 AQE 时代仍成立（⚠️ 通行立场）。
- 官方校核 ✅ https://spark.apache.org/docs/latest/sql-performance-tuning.html（AQE/join 策略节）。

## 5. 🔧 实测·语义类比组：用 DuckDB 校准「变换即计划」直觉（非 Spark 行为）

```python
import duckdb
con = duckdb.connect()
con.execute("CREATE TABLE e(id INT, dept TEXT, sal INT, entered DATE)")
# ...灌数后：
print(con.sql("SELECT dept, count(*) c, avg(sal) a FROM e GROUP BY dept HAVING count(*)>2").explain())
```

- 观察 1：plan 树里 `HASH_GROUP_BY` 前有 `FILTER`——与 Spark 逻辑优化顺序同理（谓词尽早）。
- 观察 2：把 `HAVING` 改为外层再滤 `c>2`，DuckDB 与 Spark 一样**无法**把 filter 推入聚合前——「聚合后过滤不可下推」跨引擎同构。
- 观察 3：DuckDB 单进程无 shuffle/Stage 概念；Spark 的 `exchange` 节点在此**不可见**，分区重分布的代价感必须回官方文档补（⚠️ https://spark.apache.org/docs/latest/sql-performance-tuning.html）。

## 6. 变换的组织工程（本章的「数据工程」浓度所在）

- 中间结果命名规范：staging 变量 vs 临时视图（与 6 章 catalog 呼应）。
- 一条铁律的重述：**变换函数应保持纯**（同输入同输出）——第 7 章管道可重放、第 10 章流批同一代码的成立前提。
- 版本化思路：把「业务口径」写进列名与注释而非散落 Python——analytics engineering 前夜的手工形态（⚠️ 推定语境的目录解读）。
- 常见反模式：循环 withColumn 堆叠（计划膨胀）、`collect_list` 无限膨胀列、filter 后再 union 造成的行重复。

## 7. 与流处理的接口预写（9–11 章的伏笔）

本章的 batch DataFrame 代码在 Structured Streaming 中**几乎原样复用**——这是 Spark 流批一体的核心卖点，也是本书副题的支点：

- 唯一要重学的概念是「无界表」下这些算子的增量语义（Append 可行的算子白名单、状态类算子清单）。
- 对位锚点：[../Spark_The_Definitive_Guide/09-结构化流处理.md](../Spark_The_Definitive_Guide/09-结构化流处理.md) 与 [../Streaming_Systems/06-流和表.md](../Streaming_Systems/06-流和表.md)。

## 8. 校读清单

- 作者是否用 `spark.sql` 跑过完整 TPC 式小样例？——检验其对 SQL 受众的诚意。
- UDF 示例是 Python 还是 Scala？——决定 shuffle 序列化讨论深浅。
- 窗口函数是否出现在本章（而非 12 章）？——本目录两种预期都已挂钩点。

## 9. 变换族速查表（本章的「背谱」件，⚠️ 重构）

| 族 | 代表算子 | 状态/代价 | 流式可行 |
|----|----------|-----------|----------|
| 投影/过滤 | select/filter/withColumn | 无状态、可下推 | ✅ Append 友好 |
| 键聚合 | groupBy.agg | 按键状态（窗内/全局） | ✅ Update/Complete |
| 事件时间窗 | window()+groupBy | 窗口状态+水位线 | ✅ Append（配水位） |
| 开窗函数 | rank/lead/lag | 需分区全量有序 | ⚠️ 仅 Update/Complete |
| 去重 | distinct/dropDuplicates | 历史键状态 | ✅（配水位可清） |
| 集合 | union/intersect/except | intersect/except 双全量状态 | ⚠️ 受限 |
| join | 五型 | 静态侧免状态/流流高状态 | ⚠️ 窗口化可行 |
| 结构展平 | explode/flatten | 行放大倍数 | ✅ |

- 用法：给 9–13 章的每一张查询先在表上点「可行列」——Append 是否可用、状态预算多少，两问定 sink 与资源。

## 10. 本章实验卡（⚠️ 非原书代码）

1. 同一段逻辑写两版（算子链 vs `spark.sql`），`EXPLAIN FORMATTED` diff 两计划——验证「同构」的边界（个别 hint 不可达 SQL 文本）。
2. 造一个 Python 行级 UDF 与内置等价表达式对拍：计时 + 观察计划里 UDF 成了不透明黑盒、下推链断裂。
3. 开 `spark.sql.adaptive.enabled`（对照关闭），观察 join 策略在统计下的切换——Catalyst 静态与 AQE 动态的分工一眼。
4. 窗口函数版「同部门薪资排名」：`rank over (partitionBy dept orderBy sal desc)`，为 12 章流式开窗的受限做基线记忆。
5. 把本章全部变换套在 `readStream` 的样例上跑通——Append 白名单的报错会教你哪些算子「欠了状态债」（→ 9/10 章）。

## 11. 校读问答（五问五答）

- **Q：本章讲不讲 Dataset 类型化 API？** A：2022 工程册多把 Scala Dataset 作边缘件、Python 无此层——⚠️ 书中取向未证实，盘上纵深在 [../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md](../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md)。
- **Q：join 顺序优化归谁？** A：Catalyst 逻辑阶段+AQE 动态兜底；手写「小表先 join」在 3.x 后多为徒劳 ✅（sql-performance-tuning 文档）。
- **Q：本章与第 7 章分工？** A：4 教「怎么变」，7 教「怎么把变组织成可重跑单元」——代码分层线在 7。
- **Q：pandas 用户该看哪节？** A：pandas_api 桥（演进节），本章内不必分叉。
- **Q：SQL 方言兼容模式？** A：3.3+ Spark SQL 方言解析器可插拔（⚠️ 本书之后才普及的话题，见演进）。

## 12. 章末锚点卡（速记三线，⚠️ 目录制）

- 一条主线：**变换=表达式组合**；组合的可读性靠命名，可优化性靠「让开下推的通道」。
- 一条警戒线：UDF/不透明表达式=计划的黑洞——写它前先问内置函数列表三次（✅ programming guide 函数族）。
- 一条接口线：本章每张算子链都是 10 章流查询的定义体——批侧每学一算子，流侧白名单先问一句「可行吗」。
- 记忆钩：`explain` 是本章唯一的「必须会按的按钮」；按下去看到的世界（计划树）决定你是调包侠还是工程师。
- 回望 02：入门的 UI 功夫在此章用于看计划而非只看进度——观测面二连。
- 前瞻 12/13：分析算子的流式受限清单在 12 章兑现；不可声明化的部分 13 章用状态偿还。

## 核心概念速览（中英对照）

- **变换算子** — Transformation：行/键/序/集/结构五级的 DataFrame 组合子。
- **表达式** — Expression/Column：计划树中的类型化节点，非物化值。
- **Catalyst** — Catalyst：逻辑+物理优化器，Spark SQL 的心脏。
- **AQE** — Adaptive Query Execution：运行时按统计改计划的优化框架。
- **explain** — Explain：查看分析/逻辑/物理/执行四段计划的调试入口。
- **谓词下推** — Predicate Pushdown：过滤在数据源或计划早期完成。
- **UDF** — User-Defined Function：不透明表达式，优化盲区，慎用。
- **窗口函数** — Window Function：partitionBy+orderBy 上的排名/偏移/聚合。
- **数据倾斜** — Data Skew：键分布不均导致长尾分区（14 章资源视角再展开）。
- **广播连接** — Broadcast Join：小表复制到大端避免 shuffle 的策略。
- **纯变换** — Pure Transformation：同输入同输出的函数，管道可重放的语义前提。

## 最新演进与工业实践

- **Spark 4.x 变换面增量**（⚠️ 转述 + 官方文档校核 ✅ https://spark.apache.org/docs/latest/sql-programming-guide.html）：ANSI 模式默认开启改变了 cast/除零行为——本书式代码迁 4.x 的第一批行为差异；Variant/对象识别等类型系统扩展增强半结构化变换。
- **PySpark 函数 API**：4.x 的 Python 侧 pandas_udf/向量化 UDF 路线持续替代行级 Python UDF（⚠️ 版本细节以 release note 为准）。
- **SQL 工作台化**：2024–2026 工业实践里「变换」越来越多以 dbt/SQL 物化视图表达，Spark 退居执行引擎；盘上对位 [../Analytics_Engineering_with_SQL_and_dbt 系列登记（见总索引，本目录不链）] 改为文字：dbt 类工具使本章的 withColumn 链变为模型化 SQL（⚠️ 观察性陈述）。
- **AQE 成熟度**：Skew join 处理、合并小 shuffle 分区默认化，使本书若干手动 repartition 建议过时（✅ 文档 URL 同上）。
- **对流侧的持续承诺**：Structured Streaming 与批共享算子白名单的策略未变（Append/Update 语义仍以官方指南为准 ✅ https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html）。
