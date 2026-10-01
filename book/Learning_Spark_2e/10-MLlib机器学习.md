# 10 · MLlib 机器学习

> 原书第 10 章（Machine Learning with MLlib）。章骨架 ✅ 按 ApacheCN 全译镜像实抓还原：什么是机器学习（监督/无监督）→ 为什么用 Spark 做 ML → 设计机器学习管道（数据获取探索／训练测试切分／转换器造特征／线性回归原理／估计器建模／Pipeline 组装／独热编码／评估 RMSE 与 R²／保存加载模型）→ 超参数调优（树模型：决策树/随机森林／k 折交叉验证／优化管道）。Spark/MLlib 行为 = ⚠️ 转述 + 官方文档（https://spark.apache.org/docs/latest/mllib-guide.html 同族线，见文末核验清单）。对位：[TDG 08 机器学习 MLlib](../Spark_The_Definitive_Guide/08-机器学习MLlib.md)、案例纵深 [Advanced Analytics with Spark 2e](../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md)。

## 10.1 为什么用 Spark 做机器学习（章首立场）

- 数据已在 Spark 湖里：ML 预处理不搬数据（第 3–9 章的 DataFrame/流/湖全栈皆其上游）；
- 分布式训练/预测的规模红利：特征工程与批量打分天然并行；
- 2e 的坦承边界：**算法库深度不及专用库（XGBoost/scikit-learn 单核强）**，Spark 赢在"管道与规模"，不赢在"算子精巧"——这一节把 1e 时代"MLlib 全能"的错觉提前拆掉。

## 10.2 管道词表（本章骨架）

⚠️ 转述 ml pipeline 官方语义：

- **Transformer**：`transform(df)->df` 的已拟合算子（特征变换、训练完成的模型）；
- **Estimator**：`fit()->Model` 的学习算子（回归器、分类器）；Model=Transformer 特例；
- **Pipeline**：Transformer/Estimator 有序链，`fit` 顺序执行产 PipelineModel；
- **PipelineStage/ParamMap**：阶段与参数网格的调优接口（crosser 与 `tuneParamGridBuilder`）；
- **特征地基**：Vector（dense/sparse）+ `VectorAssembler`/`StringIndexer`/`OneHotEncoder`（书用独热编码专节演示旧 DefaultParams 坑与 `inputCols` 批量新 API）。

## 10.3 端到端示例（书的路线）

线性回归打底：取数探索→`randomSplit` 训练/测试→组装特征→`LinearRegression(featuresCol,labelCol)`→Pipeline 拟合→`summary`/预测→**RMSE 与 R² 双指标评估**（RegressionEvaluator/MulticlassMetrics 评估器家族 ⚠️ 转述）→`model.write.overwrite().save(path)` 保存加载。随后升级到决策树/随机森林（`DecisionTreeClassifier`/`RandomForestClassifier`），并用 **k 折交叉验证（CrossValidator）** 与 train-validation-test 三分叙事把"超参调优"讲成流程而非玄学。

## 10.4 规模视角的调优（书与社区共识）

- `numTrees/maxBins` 对 shuffle 与内存的放大效应（树模型的 bins=隐式全局排序成本）；
- 训练采样：`sampleBy`/分层抽样先跑通再放大；
- 与第 7 章复用：缓存特征表（多轮 CV 复读）、分区数与 executor 核数匹配任务数；
- 保存的模型要带元数据（sparkml 格式=参数+schema 可追溯）——生产卫生第一条。

🔧 **类比实测说明（非本书 Spark 引擎行为）**：本章无 Spark 侧性能可实测面（模型训练需真集群）；唯一可迁移直觉用 G6 组数据替代（meas.txt，第 3/7 章已展开）：k 折 CV=同一份数据被反复聚合读取，"物化一次、复读便宜"（DuckDB CTAS 391ms→复读 0.63ms）正是"特征表 persist 供 CV 复用"的成本模型。跨语言 ML 管道本身（pandas/sklearn 单机）不在本波实测纪律内，登记为未做。

## 10.5 工程判断（重构观点）

- 2e 的 ML 章是**管道章不是算法章**——与第 11 章（MLflow 管理部署）合读才是其真实主张："Spark 的 ML 价值 = 从数据到可运维模型的生产线"；
- sparkml（DataFrame 系）vs RDD 系 `mllib.rdd` 算法库：书基本只写 sparkml（RDD 系仅词表遗留）——符合"结构化为中心"的全书宪法；
- 与 Advanced Analytics with Spark 的分工：本册教骨架，那本给 11 个真实案例模式（盘上目录版互链见上）。

## 10.6 章小节骨架总览（✅ 镜像实抓逐节对账）

| 原书小节（回译） | 本文件对应 |
| --- | --- |
| 什么是机器学习？（监督学习／无监督学习） | 10.1 前段 |
| 为什么选择 Spark 进行机器学习？ | 10.1 |
| 设计机器学习管道（总起） | 10.2 |
| 数据获取和探索 | 10.3 步骤 1 |
| 创建训练和测试数据集 | 10.3 步骤 2 |
| 使用转换器准备特征 | 10.2 特征地基 + 10.3 |
| 理解线性回归 | 10.3 打底段 |
| 使用估计器构建模型／创建一个 Pipeline | 10.2 词表、10.3 |
| 独热编码 | 10.2 StringIndexer/OneHot 条 |
| 评估模型：RMSE／R² | 10.3 评估段 |
| 保存和加载模型 | 10.3 末段、10.4 卫生条 |
| 超参数调优 | 10.4 |
| 基于树的模型：决策树／随机森林 | 10.3 升级段 |
| k 折交叉验证／优化管道 | 10.2 crossValidator、10.4 |

## 10.7 重建示例：一条 Pipeline 走到底（本目录重做；⚠️ 语义转述官方 ml-guide ✅）

```python
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import StringIndexer, VectorAssembler, OneHotEncoder
from pyspark.ml.regression import LinearRegression
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.evaluation import RegressionEvaluator

train, test = df.randomSplit([0.8, 0.2], seed=7)
stages = [
    StringIndexer(inputCol="city", outputCol="cityIdx"),
    OneHotEncoder(inputCols=["cityIdx"], outputCols=["cityOH"]),   # 批量新 API
    VectorAssembler(inputCols=["price", "cityOH"], outputCol="features"),
    LinearRegression(featuresCol="features", labelCol="sold_price", maxIter=30),
]
model = Pipeline(stages=stages).fit(train)              # Estimator→Model 顺序折叠
preds = model.transform(test)
rmse = RegressionEvaluator(metricName="rmse", labelCol="sold_price",
                           predictionCol="prediction").evaluate(preds)
ParamGridBuilder().addGrid(lr.regParam, [0.01, 0.1]).addGrid(lr.maxIter, [20, 50]) \
                  .build()                              # CV 网格（配 CrossValidator）
model.write.overwrite().save("s3://ml/linreg-v1")       # 带元数据的 sparkml 工件
old = PipelineModel.load("s3://ml/linreg-v1")           # 第 11 章的部署起点
```

## 10.8 课堂问题（答不出回本文件）

1. Spark 做 ML 的两条红利与一条边界（10.1）？
2. Estimator/Transformer 的 fit/transform 类型签名各是什么？
3. OneHot 旧 DefaultParams 的坑与 `inputCols` 批量 API 的修法？
4. RMSE 与 R² 分别回答什么问题？为何书选这对组合？
5. k-fold CV 为什么是"特征表该 persist"的典型场景（🔧 G6 直觉）？
6. 树模型训练里 `maxBins` 为什么暗含全局成本（10.4）？

### MLlib 速记

- Pipeline 是多个 PipelineStage（Transformer/Estimator）的有序组合，fit 产出 Model。
- Pipeline 与 PipelineModel 的区别：未训练与已训练，后者可序列化复用。
- 特征列要求 Vector 类型；多列特征先过 VectorAssembler。
- 评估器在 RDD 与 DataFrame 上均可用，但 API 面不同。
- MLlib 覆盖经典可规模化模型，不覆盖深度学习；深度部分原书交给外部生态。
- ⚠️ 本章 Pipeline 代码为重建示例，未在本机执行。

## 核心概念速览（中英对照）

- **Estimator/Transformer/Model** — 学习算子/变换算子/已拟合变换器三词根。
- **Pipeline/PipelineModel** — 拟合前链/拟合后链。
- **ParamMap/crossValidator** — 参数网格与 k 折自动选优。
- **Vector (dense/sparse)** — 特征向量底座。
- **VectorAssembler** — 多列合一特征列装配器。
- **StringIndexer/OneHotEncoder** — 类别编码二重奏（批量 inputCols 新 API）。
- **randomSplit** — 训练/测试切分。
- **RMSE/R²** — 回归双指标（书选定的评估语汇）。
- **RegressionEvaluator** — 评估器 API。
- **DecisionTree/RandomForest** — 树与森林（maxBins 成本叙事）。
- **sparkml 保存格式** — 元数据可追溯的模型落盘。
- **sampleBy** — 分层抽样：先小后大的规模纪律。
- **MLlib vs scikit-learn** — 规模管道 vs 算法深度的分工判断。

## 最新演进与工业实践

- **Spark 4.0 的 ML 面**（✅ Release Notes 实抓）：ML on Spark Connect（客户端化训练/推断入口）、Swift 客户端实验件——第 10/11 章的"Driver 在进程内"教学模型正在协议化；⚠️ 具体算子清单以官方页为准，本处不展开未核验项。
- **RDD 系算法库冻结**：`mllib.rdd` 长期仅维护（⚠️ 转述社区口径），sparkml+外部库（XGBoost-Spark、MLflow 生态）成为事实组合——书时代判断延续成立。
- **GPU/加速**：RAPIDS cuDF 对 Spark 的插拔（NVIDIA 方案，⚠️ 转述；本书 3.0 预告的"加速器感知调度"见第 12 章）；树模型/ANN 的单机库挤压使 Spark ML 退守"特征工程 + 批量打分"。
- **MLOps 合流**：2024–2026 特征存储（Feast/Tecton）、管道编排（Airflow/Argo）与模型治理已接管本章职责边界——本章保值内容只剩 Pipeline/ParamMap 词表与 CV 流程感。
- **对读**：RDD 系算法全谱见 [../Spark_The_Definitive_Guide/08-机器学习MLlib.md](../Spark_The_Definitive_Guide/08-机器学习MLlib.md)；案例模式库见 [../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md](../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md)；本章文件与第 11 章互为上下篇。
