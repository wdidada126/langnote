# 11 · MLflow：管理、部署与扩展机器学习流水线

> 原书第 11 章（Managing, Deploying, and Scaling Machine Learning Pipelines with Apache Spark）。章骨架 ✅ 按 ApacheCN 全译镜像实抓还原：模型管理／MLflow（追踪 Tracking）／用 MLlib 的模型部署选项（批量／流式／实时推理的模型导出模式）／利用 Spark 服务非 MLlib 模型（Pandas UDFs）／Spark 做分布式超参调整（Joblib、Hyperopt）。Spark/MLflow 行为 = ⚠️ 转述 + 官方文档（https://mlflow.org/ ✅ curl 200）。本章与第 10 章构成"从训练到生产"的下半篇，同为 2e 新增题材（1e 无）。对位：[Advanced Analytics with Spark 2e](../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md)。

## 11.1 模型管理问题与 MLflow Tracking

- 问题陈述：实验散、工件野、"谁训的模型用了什么数据/参数"不可考——**模型即数据资产需要登记册**；
- **MLflow 三件套**（书时代口径）：Tracking（run/参数/指标/工件的层级记录，`mlflow.start_run`/`log_param`/`log_metric`/`log_artifact`，本地或远端 tracking store）、Projects（环境可复现的打包约定）、Models（`mlflow.pyfunc` 统一导出格式 + serving）；
- 与 sparkml 保存的关系：`MlflowLogger`/`mlflow.spark.log_model` 把第 10 章的 `model.write.save` 升级为带血缘的登记式落盘（⚠️ 转述 API 语义）；
- 后端形态：local file→tracking server→托管服务（Databricks Managed MLflow）——2026 已扩展为完整 AI/LLM 观测平台（演进节）。

## 11.2 三种部署形态（书给的分类法）

| 形态 | 载体 | 书内姿势（⚠️ 转述） |
| --- | --- | --- |
| 批量（Batch） | Spark 作业 | 模型重载 `PipelineModel.load`/`mlflow.pyfunc.spark_udf`，对湖/仓存量数据全量打分——**Spark 是打分引擎** |
| 流式（Streaming） | Structured Streaming | `foreachBatch`/UDF 内载模型，新段新分——第 8 章管道复用 |
| 实时（Real-time serving） | 导出模型 | MLflow `pyfunc` 导出 + 服务化（serving/REST；书仅给模式，不教运维级方案）|

- 分类法要点：**延迟与吞吐的三角 trade-off**，引擎选择随形态改变，但"模型工件同一份"是统一主张（pyfunc 是黏合剂）。

## 11.3 非 MLlib 模型上 Spark（本章最有辨识度的一节）

- 痛点：sklearn/XGBoost/torch 模型不在 sparkml 体系里，怎么分布式预测？
- **Pandas UDF 批式包装**：`mapInPandas`/grouped mapInPandas——每分区/每组取 `Iterator[pandas.DataFrame]`，模型在 executor 内加载一次、按批 `predict`，结果批返回（⚠️ 转述，官方 Python 文档线）；
- 书强调的三条纪律：模型文件先分发（archive/`--py-files` 或工件库拉取）、内存预算按批大小、分区数=并行打分槽位；
- **分布式超参**：Joblib `parallel_backend(pyspark backend)` 把 `GridSearchCV` 的 folds 摊到集群；Hyperopt `fmin`+Spark Trials——"调参即 embarrassingly parallel 作业"的两件工具实证。

🔧 **概念类比（非本书 Spark/MLflow 行为）**：以 SQLite 模拟"工件登记"最小模型——`CREATE TABLE runs(id, params TEXT, metrics TEXT, model_path TEXT, ts)` 用 ON CONFLICT 保 run 唯一性（结构同 meas.txt G5 的 upsert 组，实测 5 批 1187.1ms 的写入成本谱），说明 Tracking 后端在"最小可用"层面就是**带时间线的事实表**；MLflow 真实存储/并发/ACL 语义 ⚠️ 转述不背书。

## 11.4 工程判断（重构观点）

- 2e 把 MLflow 写进教学主线，比"Spark 书只讲 MLlib"的旧范式前进一大步；但作者身份决定其视角=Databricks 栈内闭环——**开源 MLflow 与湖仓（第 9 章 Delta）在 2023 后被 Unity Catalog 收编为"一个治理面"**，书的三章分立叙事已过时（演进节登记）；
- "批量打分用 Spark、在线推理用服务"的边界在 2024–2026 被 LLM 批量推理重新引爆：`mapInPandas` 包 LLM 的 prompt 批处理正是本章模式的当代复刻——这一节是全章最保值的资产。

## 11.5 章小节骨架总览（✅ 镜像实抓逐节对账）

| 原书小节（回译） | 本文件对应 |
| --- | --- |
| 模型管理 | 11.1 问题陈述 |
| MLflow：追踪（Tracking） | 11.1 三件套 |
| 使用 MLlib 的模型部署选项：批量 | 11.2 表行 1 |
| （部署选项）流式处理 | 11.2 表行 2 |
| 实时推理的模型导出模式 | 11.2 表行 3 |
| 利用 Spark 进行非 MLlib 模型：Pandas UDFs | 11.3 首两段 |
| Spark 用于分布式超参数调整：Joblib／Hyperopt | 11.3 末段 |

## 11.6 重建示例：登记一次实验 + 批式打分 + 分布式调参（本目录重做；⚠️ API 形态以 mlflow.org / 官方文档为准）

```python
# ① 训练侧：实验登记（第 10 章末行 model 的"户口本"）
import mlflow.spark
with mlflow.start_run(run_name="linreg-v1"):
    mlflow.log_param("maxIter", 30); mlflow.log_metric("rmse", rmse)
    mlflow.spark.log_model(model, "model")               # sparkml 工件+血缘入册

# ② 批量打分：模型回 DataFrame 世界（11.2 表行 1 的落码）
import mlflow.pyfunc
predict = mlflow.pyfunc.spark_udf(spark, "runs:/<run_id>/model", result_type="double")
scored = big_df.withColumn("pred", predict("features"))  # executor 内加载一次，按分区打分

# ③ 分布式超参：把 sklearn 的 GridSearch 摊到集群（11.3）
from joblib import parallel_backend
with parallel_backend("pyspark"):
    clf.fit(X, y)                                        # folds → Spark tasks（⚠️ 语义）

# ④ 流式打分：q.foreachBatch(lambda b,i: b.write...pred...) 复用 ② 的 UDF（11.2 行 2）
```

## 11.7 课堂问题（答不出回本文件）

1. Tracking 记录的四类对象（run/param/metric/artifact）各回答什么问题？
2. pyfunc 为什么能当"跨框架黏合剂"？它牺牲了什么（性能/依赖）？
3. 批量 vs 流式 vs 实时三形态，模型工件是几份？执行引擎是几套（11.2 主张）？
4. 非 MLlib 模型上集群的三条纪律？各对应哪类事故？
5. Joblib backend 与 Hyperopt Trials 分别适合什么搜索形态？
6. "同一份模型工件"在 UC 治理时代变成了什么（11.4/演进节）？

## 核心概念速览（中英对照）

- **MLflow Tracking** — run/param/metric/artifact 实验登记册。
- **MLflow Models/pyfunc** — 跨框架统一模型工件与导出格式。
- **MLflow Projects** — 环境可复现的作业打包约定。
- **spark_udf（mlflow）** — 模型进 DataFrame 的批量打分把手。
- **foreachBatch（流打分）** — 微批内载模型的流式部署位。
- **实时服务** — Real-time serving：REST/托管端点形态。
- **mapInPandas/applyInPandas** — 批式 Pandas UDF：分布式服务任意 Python 模型。
- **模型分发** — archive/工件拉取：executor 侧可用性前提。
- **Joblib Spark Backend** — GridSearch 并行化到集群。
- **Hyperopt Trials** — 贝叶斯式超参搜索的分布式执行器。
- **训练-服务偏斜** — 同一特征逻辑跨两侧复用的动因（本章隐含主张）。
- **治理统一面** — UC 时代 MLflow+表格式合流（延伸）。

## 最新演进与工业实践

- **MLflow 3.x（2025）**：从"经典 ML 三件套"扩展为 GenAI/LLM 观测与评估平台（traces/evaluation/prompts；✅ 官网 https://mlflow.org/ curl 200，细目以官网文档为准——本处不逐项断言版本特性以避开未核验清单）。
- **Unity Catalog 收编**：Databricks 把 Delta（第 9 章）+ MLflow（本章）+ SQL 资产统一入 UC 治理面（⚠️ 转述公开产品线）；开源对位是 Apache Polaris/Paimon 系 catalog 化——盘上对读见 [../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)（catalog 议题相邻）。
- **Spark 4.0 ML on Connect**：训练/推断入口客户端化（✅ Release Notes 实抓），本章"Driver 进程内 fit"的默认图景需要重画；`pyspark-client` 1.5MB 使"笔记本即客户端"成教学主流。
- **特征与向量检索外扩**：Feature Store 与向量检索（⚠️ 转述各产品）接管本章部分职责；本书模式（UDF 批打分 + Tracking 登记）仍是自建方案的最小骨架。
- **对读**：模型案例与特征工程的模式库在 [../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md](../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md)；训练管道词表本身回看 [10-MLlib机器学习.md](10-MLlib机器学习.md)；本章+第 9 章合读即"Databricks 栈的 2020 蓝图"。
