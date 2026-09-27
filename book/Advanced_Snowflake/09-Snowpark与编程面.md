# 09 · Snowpark 与编程面深潜（⚠️ 推定主题章，任务书 ★ 关键词）

> **性质声明**：推定主题重构（[00](00-总览与阅读地图.md)）。**Snowpark 运行时不可连**——全章机制
> 转述（⚠️）+✅URL；无 🔧（进程内编程模型与本机 DuckDB/SQLite 差异过大，不强行类比，如实登记）。
> TDG 对位：[../Snowflake_The_Definitive_Guide/12-数据云工作负载.md](../Snowflake_The_Definitive_Guide/12-数据云工作负载.md)（应用负载入门面）。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 9.1 | Snowpark 定位：把计算拉到数据侧 | DataFrame=惰性计划的下推载体 |
| 9.2 | DataFrame API 语义面 | 转换/行动分离；collect 是账单事件 |
| 9.3 | UDF/UDTF/UDAF/向量化函数 | 扩展 SQL 的四类形态 |
| 9.4 | 存储过程与 Snowflake Scripting | 服务端事务胶水 |
| 9.5 | UDF vs 过程的抉择 | 纯函数/权限上下文/成本三面 |
| 9.6 | Snowpark Container Services | OCI 容器进仓的负载类型学 |
| 9.7 | 工程化：本地测试/依赖/CI（snow CLI） | "数仓代码化"的落地件 |
| 9.8 | Streamlit in Snowflake 与 Notebook | 应用面双子星（登记对位） |

## 核心精讲

### 1. DataFrame 与惰性执行（转述 ⚠️）
Python/Java/Scala 三语言的 DataFrame API 编译为**远程 SQL/计划**在仓库内执行：客户端持有的是
表达式树，`collect()/show()` 才触发计算与 credit 消耗；`execute_if_updated`、缓存算子等细节
以版本化 API 参考为准（官方 llms 索引明示"Snowpark Python API 签名跨版本会变"⚠️✅）。
✅ https://docs.snowflake.com/en/developer-guide/snowpark/index
✅ https://docs.snowflake.com/en/developer-guide/snowpark/python/working-with-dataframes

### 2. 函数族（转述 ⚠️）
- **UDF**（标量，行内并行）：`@udf`/register，第三方包走导入阶段；
- **UDTF**（表值，yield 行流）/ **UDAF**（聚合）；
- **向量化 UDF**（pandas.Series 入参）：批接口摊薄进程开销 ⚠️；
- **存储过程**：可事务、可 DDL，与 UDF 权限上下文不同（DEFINER vs INVOKER ⚠️ 以页内为准）。
✅ https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-udfs
✅ https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-sprocs
✅ https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-udafs （经索引发现 ✅）
```python
# 教学示意，非书中原文
@udf(name="norm_ratio", return_type=FloatType(), input_types=[FloatType(), FloatType()])
def norm_ratio(a, b):
    return 0.0 if b == 0 else a / b
```

### 3. UDF vs 存储过程抉择（方法论 ⚠️）
纯变换+SQL 侧组合→UDF；多语句事务/写回/管理动作→过程；重计算→**先在 DataFrame 里下推，
函数是最后手段**（函数打断裁剪与向量化的代价，第 3/5 章共振：UDF 包裹的谓词列不再 SARGable）。

### 4. Container Services 与应用面（转述 ⚠️）
Snowpark Container Services：OCI 镜像跑在仓库内算力（服务/子图编排），承接"SQL 表达不了"的
负载（自定义推理/长驻服务）；Snowpark-optimized 仓库联动（第 1 章 ✅ 已证 200）。
✅ https://docs.snowflake.com/en/developer-guide/snowpark-container-services/overview
工程化：本地测试框架（mock 数据免连仓 ✅）、`snow` CLI 项目/迁移（CI-CD 化）。
✅ https://docs.snowflake.com/en/developer-guide/snowpark/python/testing-locally

### 5. 与编排/摄入的接线
Python serverless 任务（第 7 章 ✅tasks-python-jvm）+ Snowpark 作业=仓内 ETL 代码化主线；
Snowpipe Streaming 的 SDK 也托管在 Container Services 内运行（✅ 第 8 章
snowpipe-streaming 系列索引中 "Run the Snowpipe Streaming SDK in Snowpark Container Services" 条 ✅）。

## 常见误区

| 误区 | 事实（转述 ⚠️） |
| --- | --- |
| "Snowpark=在笔记本里跑的 pandas" | 计划下推仓内执行，collect 才回传数据 |
| "UDF 让 SQL 更灵活" | 每个 UDF 都是裁剪/优化器的黑洞+仓库进程开销 |
| "过程和函数一回事" | 事务/权限/调用上下文三处不同 |
| "容器服务=GKE 搬家" | 它嵌在仓库算力与安全模型内，形态受限但治理免费 |
| "包依赖随便 import" | 非内置包要显式上传/版本对齐，运行时沙箱有约束 ⚠️ |

## 与其他章、其他书的联系

- 函数打断裁剪 → [03-微分区与裁剪引擎.md](03-微分区与裁剪引擎.md)、[05-查询优化与JOIN策略.md](05-查询优化与JOIN策略.md)；
  任务体接线 → [07-Streams与Tasks编排.md](07-Streams与Tasks编排.md)；高内存仓库形态 →
  [01-计算模型与弹性深潜.md](01-计算模型与弹性深潜.md)；容器内管道的账单 →
  [02-成本模型与计费内核.md](02-成本模型与计费内核.md)。
- 入门对读：TDG-12。
- 谱系对照（DataFrame 语义与 JVM 生态）：[../Spark大数据分析与实战.md](../Spark大数据分析与实战.md)
  （盘上单文件，Spark DataFrame 对照——"Snowpark 借鉴 Spark API"是社区通说 ⚠️）、
  [../bigdata/02-Spark核心与RDD模型.md](../bigdata/02-Spark核心与RDD模型.md)、
  [../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)。
- 本地脚本对照（"数据侧编程 vs 进程内编程"边界感）：
  [../DuckDB_in_Action/06-融入Python生态.md](../DuckDB_in_Action/06-融入Python生态.md)。
- 【登记·同波不链】`Advanced_Analytics_with_Spark_2e` 落盘后互挂（Spark↔Snowpark 谱系三角）。

## 本章自测（3 分钟）

1. `df.filter(col("dt")==lit("2026-09-27")).group_by("k").count().collect()`——几次仓库行动？
   哪些算子已下推？
2. 把一段正则清洗逻辑从 Python UDF 迁回 SQL，两条可行路径与各自限制？
3. 本地测试框架（testing-locally）在 CI 里能替你省掉什么、又测不到什么？（提示：真实统计与裁剪）

## 核心概念速览（中英对照）

1. **Snowpark** — 仓内多语言数据编程框架（Python/Java/Scala）。
2. **惰性计划** — lazy evaluation：DataFrame 编译下推，行动算子才执行。
3. **UDF** — 用户定义标量函数：行内并行，谓词黑洞（⚠️）。
4. **UDTF/UDAF** — 表值/聚合扩展函数。
5. **向量化 UDF** — pandas 批接口函数，摊薄调用开销。
6. **存储过程** — 服务端事务单元（Snowflake Scripting/Java/Python 皆可写 ⚠️）。
7. **Snowflake Scripting** — PL 式过程语言：任务/过程的胶水层。
8. **Snowpark Container Services** — 仓内 OCI 容器运行时。
9. **本地测试框架** — testing-locally：mock 化单测，免连仓跑 CI。
10. **snow CLI** — 项目/对象/迁移的命令行工程面。
11. **DEFINER/INVOKER** — 函数过程的权限上下文对（以页内为准 ⚠️）。
12. **包导入** — import stage 压缩依赖：UDF 第三方库通道。

## 最新演进与工业实践

**2024–2026（URL 均 2026-09-27 curl -L 实测 200 ✅）：**

- **Snowpark 多语言页齐备**（java/scala 与 python 三线全套 ✅ 经索引验证），官方明示
  API 版本漂移风险——**钉版本+回归测试**成为 2025+ 工程纪律（✅ llms 索引警示条）。
- **容器服务文档独立成树**（34 页 ✅ 索引），与 Snowpark optimized 仓库、流式 SDK 托管三线合流，
  "仓内跑非 SQL 负载"从尝鲜变默认。
- **Python 任务化**：serverless tasks 支持 Python（第 7 章 ✅），ETL 代码不再需要外部调度器中转。
- **工业实践 ⚠️（转述）**：平台工程团队 2025+ 的"仓内四件套"=snow CLI CI + 本地测试框架 +
  迁移目录 + 函数注册即代码（infra-as-SQL）；UDF 治理（登记+成本审计）并入第 2 章 FinOps 循环。
- Cortex Code（✅ /user-guide/cortex-code/ 索引 76 页）标志"AI 写 Snowpark"进入产品面——第 12 章接口。

**文献与文档**：snowpark/index、python/working-with-dataframes、python/creating-udfs、
python/creating-sprocs、python/creating-udafs、python/testing-locally、
snowpark-container-services/overview、warehouses-snowpark-optimized、tasks-python-jvm（✅200）。
