# 08 — 机器学习 MLlib

> 原书 Ch 17: Machine Learning with MLlib (ML Pipeline)
> 原书 Ch 18: Feature Engineering
> 原书 Ch 19: Model Tuning and Selection
> 原书 Ch 20-21: Structured Streaming (概述部分；详见 09)

---

## Ch 17 核心：MLlib 概览

### MLlib 的两大 API

| API | 状态 | 基础 | 说明 |
|-----|------|------|------|
| `spark.mllib` | ⚠️ 维护模式 | RDD | 旧版 API，不再推荐 |
| `spark.ml` | ✅ 推荐 | DataFrame | Pipeline API，本书重点 |

✅ **spark.ml 的核心概念**：
- **Transformer**：将 DataFrame 转换为另一个 DataFrame（如模型预测）
- **Estimator**：在 DataFrame 上训练，生成 Transformer（如算法.fit()）
- **Pipeline**：串联多个 Transformer 和 Estimator 的工作流

### ML Pipeline

```python
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier

# 构建 Pipeline
indexer = StringIndexer(inputCol="category", outputCol="categoryIdx")
assembler = VectorAssembler(inputCols=["age", "salary"], outputCol="features")
rf = RandomForestClassifier(featuresCol="features", labelCol="categoryIdx", numTrees=100)

pipeline = Pipeline(stages=[indexer, assembler, rf])

# 训练
model = pipeline.fit(train_df)

# 预测
predictions = model.transform(test_df)
```

### 内置算法

| 类别 | 算法 |
|------|------|
| 分类 | LogisticRegression, DecisionTree, RandomForest, GBT, NaiveBayes |
| 回归 | LinearRegression, GBTRegression, AFTSurvivalRegression |
| 聚类 | KMeans, BisectingKMeans, GaussianMixture |
| 协同过滤 | ALS (Alternating Least Squares) |
| 频繁模式 | FPGrowth, PrefixSpan |

---

## Ch 18 核心：特征工程

### 特征提取

| 转换器 | 功能 | 示例 |
|--------|------|------|
| `Tokenizer` / `RegexTokenizer` | 文本分词 | "Hello World" → ["hello", "world"] |
| `HashingTF` / `CountVectorizer` | 文本→向量 | 词频/词袋表示 |
| `Word2Vec` | 词嵌入 | 词→稠密向量 |
| `StopWordsRemover` | 去停用词 | 过滤常见无意义词 |

### 特征转换

| 转换器 | 功能 |
|--------|------|
| `StringIndexer` | 字符串→索引 (分类编码) |
| `OneHotEncoder` | 索引→独热编码 |
| `VectorAssembler` | 多列合并为特征向量 |
| `StandardScaler` / `MinMaxScaler` | 特征标准化/归一化 |
| `Bucketizer` | 连续值→离散区间 |
| `PCA` | 主成分分析降维 |
| `PolynomialExpansion` | 多项式特征扩展 |

### 特征选择

| 方法 | 说明 |
|------|------|
| `ChiSqSelector` | 卡方检验选择特征 |
| `VectorSlicer` | 手动选择特征子集 |

### ML Pipeline 最佳实践

✅ 使用 `CrossValidator` / `TrainValidationSplit` 进行超参调优
✅ 使用 `MulticlassClassificationEvaluator` 等评估指标
✅ 将特征处理与模型训练封装为 Pipeline（便于复用和部署）

```python
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

paramGrid = ParamGridBuilder() \
    .addGrid(rf.numTrees, [50, 100, 200]) \
    .addGrid(rf.maxDepth, [5, 10]) \
    .build()

evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
cv = CrossValidator(estimator=pipeline, estimatorParamMaps=paramGrid,
                    evaluator=evaluator, numFolds=3)
cvModel = cv.fit(train_df)
```

---

## 🔧 DuckDB / SQLite 类比

> 以下类比均为辅助理解，**非本书引擎行为**。

🔧 **类比 1：VectorAssembler ≈ DuckDB 多列选择 / SQLite 多列选择**
- Spark 将多列合并为 ML 特征向量
- DuckDB/SQLite 可 `SELECT col1, col2 FROM t` 但无向量概念
- ML 框架特有的数据准备步骤 · ⚠️ 非本书引擎行为

🔧 **类比 2：StringIndexer ≈ DuckDB dense_rank / SQLite 手动编码**
- Spark StringIndexer 将字符串映射为数字索引
- DuckDB: `dense_rank() OVER (ORDER BY category)` 类似效果
- SQLite 需手动维护映射表 · ⚠️ 非本书引擎行为

🔧 **类比 3：Tokenizer ≈ DuckDB string_split / SQLite instr+substr**
- Spark: `Tokenizer(inputCol="text", outputCol="words")`
- DuckDB: `string_split(text, ' ')` 功能类似
- SQLite 无内置分词函数（需自定义） · ⚠️ 非本书引擎行为

🔧 **类比 4：Pipeline ≈ DuckDB 宏 / SQLite 视图链**
- Spark Pipeline 串联多个变换步骤
- DuckDB 可用宏或 CTE 链模拟类似流程
- SQLite 可用视图链组合查询 · ⚠️ 非本书引擎行为

---

## 核心概念速览（中英对照）

| 中文 | English | 简述 |
|------|---------|------|
| 转换器 | Transformer | 将 DataFrame 转换为另一个 DataFrame |
| 估计器 | Estimator | 在数据上训练生成 Transformer |
| 流水线 | Pipeline | 串联多个 ML 步骤的工作流 |
| 特征提取 | Feature Extraction | 从原始数据提取特征 |
| 特征转换 | Feature Transformation | 缩放/编码/归一化特征 |
| 交叉验证 | Cross Validation | 多折验证评估模型泛化能力 |
| 超参调优 | Hyperparameter Tuning | 搜索最优参数组合 |
| 词嵌入 | Word Embedding | 将词映射为稠密向量 |

---

## 最新演进与工业实践

**MLlib 的演进（书后发展）：**

| 演进 | 版本 | 影响 |
|------|------|------|
| pandas UDF for ML | 3.0+ | 支持在 ML Pipeline 中使用 Vectorized UDF |
| Spark ML + Horovod | 3.x | 分布式深度学习集成 |
| MLflow 集成 | 3.x+ | 模型版本管理、实验跟踪 |
| Spark Connect + ML | 4.x | ML Pipeline 可通过 Connect 远程执行 |
| 深度学习 | 持续 | Spark 本身不做 DL；通过集成 TensorFlow/PyTorch |

> 来源: spark.apache.org ✅

**工业实践（2026）：**
- MLflow 已成为 Spark ML 项目的标准实验管理工具
- 分布式深度学习更多使用 Horovod / Ray 而非 Spark 原生
- 传统 ML（分类/回归/聚类）仍用 MLlib Pipeline
- 相关参考: [Advanced_Analytics_with_Spark_2e](../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md) 提供了更多 ML 案例
