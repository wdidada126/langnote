# 04 MLlib 机器学习与特征管道

> **取证态**：对应 Learning Path 主题「applying machine learning ... on Spark using MLlib」与仓库实据：Module_1/Chapter 2（`ANN` 文件夹）、Chapter 7（`K Means` 文件夹）、Module_3/Chapter 10、12（`Chapter N Code + Data`）✅ 目录级；章名 ⚠️ 不可得（00 §3）。ML 在集群上的真实行为不可本机实测 → ⚠️ 转述 + 官方 [ML Guide](https://spark.apache.org/docs/latest/ml-guide.html)（✅ 可达）；🔧 类比复用 01 的 E3 半群视角并标注**非本书 Spark 引擎行为**。对位正读：[../Spark_The_Definitive_Guide/08-机器学习MLlib.md](../Spark_The_Definitive_Guide/08-机器学习MLlib.md)。

## 1. 两代 MLlib：RDD-based 谢幕与 DataFrame-based 上位

Spark 2.0 明确**推荐 `spark.ml`（DataFrame-based）为唯一主轨**，`spark.mllib`（RDD-based）转入维护叙事 ⚠️。本册恰跨在两代 API 的交接带上——读它必须自带这层考古眼镜：

```scala
import org.apache.spark.ml.{Pipeline, PipelineModel}
import org.apache.spark.ml.feature.{Tokenizer, HashingTF, IDF}
import org.apache.spark.ml.clustering.KMeans

val stages = Array(
  new Tokenizer().setInputCol("text").setOutputCol("tokens"),
  new HashingTF(numHashFeatures = 262144).setInputCol("tokens").setOutputCol("tf"),
  new IDF().setInputCol("tf").setOutputCol("tfidf"),
  new KMeans().setK(5).setFeaturesCol("tfidf").setSeed(42L)
)
val pipeline = new Pipeline().setStages(stages)
val model = pipeline.fit(newsDF)        // newsCorpora.csv 类语料的典型用法
model.write.overwrite().save("/models/news-km")   // PMML 之外的事后持久化教义
```

- **Pipeline 三件套** ⚠️：Transformer（`transform` 映射特征空间）/ Estimator（`fit` 产出 Model）/ Stage 序列；交叉验证 `CrossValidator` + `ParamMap` 网格是 2.x 调参的标准姿势。
- **模型持久化**：`ml` 系用 DataFrame 导出的分块格式（mllib 老模型曾以 PMML/序列化示人）；**跨版本兼容不保证** 是 2.x 文档的著名警告 ⚠️——Learning Path 缝合册自身即重灾区（不同单品书的模型年代不一）。

## 2. 聚类：KMeans 的分布式教义（Module_1/Chapter 7 实据）

2.x 的 `KMeans`（ml 包）默认 k-means|| 播种、`distMode` BT 树加速欧氏距离 ⚠️；`setK/setMaxIter/setTol/setSeed` 四参数即全部工程杠杆。E1 之于流的语义、E3 之于聚合的语义在此复用：**每轮迭代的簇心更新 = 分区局部 (sum,count) 聚合 + shuffle 合并**——🔧 E3（4000 行/4 分区，partial→final 均值与全局逐键一致）演示的正是「可组合半群」为什么让 k-means 这类 EM 型算法天然适配 map-side combine。**非 Spark 分布式实现实测**。

## 3. 神经网络：ANN 文件夹的 2.x 分寸（Module_1/Chapter 2 实据）

2.x 本体的神经网络供给只有一块：**MLP 分类器**（`org.apache.spark.ml.classification.MultilayerPerceptronClassifier`）⚠️——全连接、梯度下降、features 向量进/label 出：

```scala
val layers = Array[Int](inputDim, 16, 8, numClasses)
new MultilayerPerceptronClassifier()
  .setLayers(layers).setBlockSize(128).setSeed(1234L).setMaxIter(100)
```

ANN 文件夹的史料价值在于它标出**本册的诚实边界**：2.x 的 MLlib 不做深度网络训练——README 所谓「deep learning techniques on Spark using MLlib and various external tools」的后半句（外接生态）才是时代真相，展开见 05。互见 [../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md](../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md) 的现代谱系分工。

## 4. 特征工程与文本管道（含 ANN 回归对照）

- 特征器矩阵 ⚠️：`VectorAssembler`/`StandardScaler`/`MinMaxScaler`/`StringIndexer`+`OneHotEncoder`（2.3 后有 `OneHotEncoder` 并入 `ml` 主轨的迁移 ⚠️ 不记版本细节以免臆写）/`QuantileDiscretizer`/`Bucketizer`。
- 文本线：`Tokenizer→StopWordsRemover→n-gram→HashingTF/IDF→(LSA)` 的「TF-IDF 谱系管道」是 2.x 教程对新闻语料（本书仓库根 `newsCorpora.csv` ✅ 实抓）的标准吃法；`Word2Vec`/`GloVe` 挂件同期在位 ⚠️。
- 回归/分类全家福：`LinearRegression`、`LogisticRegression`、`DecisionTree/RandomForest/GBT`、`NaiveBayes`、`FMClassifier`（2.2 后新轨 ⚠️ 转述）——本册把它们当「Pipeline 的零件」而非孤立算法讲。

## 5. 选型判语（本书年代 vs 教学价值）

2.x MLlib 的强项=**经典机器学习在 GB 级特征表上的可扩展性**；弱项=模型库新颖度与迭代速度（对 TensorFlow/PyTorch 时代无还手之力 ⚠️）。今天回读的正确姿势：把它当「分布式特征工程 + 可序列化管道」的地层样本——`Transformer/Estimator` 抽象后来被各家批式框架反复致敬。

## 5.5 评估器家族与调参纪律（2.x ml 版）

- 二分类 `BinaryClassificationEvaluator`：`areaUnderROC` 与 `areaUnderPR` 二曲线**选哪条本身就是教义**——正例稀疏时 PR 面信号更强 ⚠️；
- 回归 `RegressionEvaluator`（rmse/mae/mse/r2 四件套）、多分类 `MulticlassClassificationEvaluator`（`weightedMetricParam` 的 macro/weighted 按业务择 ⚠️）；
- 聚类 `ClusteringEvaluator`：silhouette 是 2.x 教参标配，距离度量选择随特征器形态变化（TF-IDF 归一化后 cosine 面更稳 ⚠️ 转述）；
- 网格纪律：`TrainValidationSplit`（单折省钱）vs `CrossValidator`（k 折诚实）；先降维参数空间再上网格——2.x 算例反复演示「全网格爆炸」的反面教材 ⚠️。

## 5.6 特征→serving 的管道闭环（与 06 推荐节互锁）

```scala
// 训练与预测共用同一 stages 定义：管道即合同
val pipeline = new Pipeline().setStages(Array(tokenizer, tf, idf))
val features = pipeline.fit(corpus).transform(corpus)   // 特征面板
val model = new KMeans().setK(5).fit(features)          // 04 §2 主干
model.transform(features).select("id", "prediction").write.parquet("/serving/news-clusters")
```

- **批量打分导出**是 Spark 在推荐/检索链路里的正统位（06 §3 的 ALS 同构）⚠️；
- 模型跨版本脆（§1 警告）→ 2.x 教参的稳妥姿势：**存训练脚本+参数+特征面板，重训而非跨版本 load** ⚠️；
- 特征重放纪律：训练/预测两端的 stages 序列必须逐一对齐——「管道即合同」是本册 ML 部分最值得带走的一句 ⚠️；
- 🔧 呼应 E3：分布式聚类的每轮簇心更新、ALS 的每轮因子更新，都走「局部 (sum,count)/局部梯度 + shuffle 合并」的同一半群轨道——单机可验的是**代数前提**，不是收敛速度 ⚠️。

## 5.7 时代差问答与自测（本章四问）

- **问：本册 ML 章今天还值得读吗？** 答：值的是「管道抽象」——Transformer/Estimator/Stage 这套把 ETL 与训练缝成一条可复现链的设计语言被后世反复借用；不值的是具体算法参数（⚠️ 判语）。
- **问：MLlib 能训深度网络吗？** 答：本册年代的唯一答案是 MLP（§3）；「Spark 做深度学习」在当时的真实语义是外接生态——05 §3 存废表是这句话的审计结果。
- **问：KMeans 的 K 与 seed 哪个更重要？** 答：2.x 教参姿势：seed 先行固定复现、K 由 silhouette 族评估后定（§2/§5.5）——顺序反了会把随机性记成功效。
- **问：模型迁移怎么防脆？** 答：跨版本 load 不做，改「存脚本+存参数+重训」（§5.6）；本册作为缝合书自身就是跨来源格式混龄的反面教材 ⚠️。

自测四题：① 把 §1 新闻管道逐 stage 写成 DataFrame 血缘图；② ROC 与 PR 面积在正例 1% 数据上为何给出相反的选型；③ `CrossValidator` 与 `TrainValidationSplit` 的预算-诚实折中；④ E3 半群条件之于 k-means 每轮更新的必要性（局部统计量必须可合并）。

## 5.8 一分钟带走（本册原声四句）

- 本册承诺位原声：`applying machine learning and deep learning techniques on Spark using MLlib and various external tools`（✅ 官方 README 实抓）——后半句才是 2.x 深度学习的真相（§3）。
- 管道一句断：Stage 序列即训练合同，train/predict 两端同构才谈得上复现（§5.6）。
- 评估一句断：指标选型是业务题不是统计题，ROC 与 PR 各说半边话（§5.5）。
- 版本一句断：2019 年的模型不该被要求活到 2026 年的集群——重训便宜于考古（§1）。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
|---|---|---|
| 管道 | Pipeline | Estimator/Transformer 序列化为一条可复现训练-预测链 |
| 估计器 | Estimator | `fit(df)→Model` 的训练抽象 |
| 变换器 | Transformer | `transform(df)→df` 的特征映射抽象 |
| 参数网格 | ParamMap / CrossValidator | 超参搜索的分布式网格与交叉验证载体 |
| 散列特征 | HashingTF | 词→固定维稀疏计数的哈希技巧 |
| 逆文档频率 | IDF | 按稀有度重权词频的特征变换 |
| 均值漂移聚类 | KMeans(k-means||) | 分布式播种+迭代簇心更新的聚类主干 |
| 多层感知机 | MLP (MultilayerPerceptronClassifier) | 2.x MLlib 唯一「神经网络」本体，全连接浅层为宜 |
| 词向量 | Word2Vec | 嵌入特征器，文本管道的预训练件 |
| 模型持久化 | Model Save/Load | DataFrame 分块格式存模型；跨版本兼容无保证（2.x 警告） |
| 分布式梯度下降 | SGD on RDD/DataFrame | 各分区局部梯度+聚合更新的训练范式（线性族主干） |
| 半群聚合 | Associative Aggregation (sum,count) | 使分区局部+合并语义成立的代数前提（🔧 E3 类比） |
| 参数网格降维 | ParamGrid 纪律 | 先剪参数维再上网格，防组合爆炸的调参次序（§5.5） |
| 批量打分 | Batch Scoring | `transform` 全量推断的 serving 形态（§5.6 代码块） |

## 最新演进与工业实践

| 本书（2.x） | 2026 现状 | 依据 |
|---|---|---|
| `spark.ml` 为「新轨」 | 已成唯一轨；RDD-based `mllib` 长期维护态乃至弃用叙事延续 | ✅ [ml-guide](https://spark.apache.org/docs/latest/ml-guide.html) 在位；⚠️ 逐版本弃用号未在可达页核字 |
| MLP 即「深度学习全部」 | 深度训练彻底让位专用栈（GPU/PyTorch 线）；Spark 侧价值收敛为数据准备+批量推理编排 | ⚠️ 转述行业共识；官方以 [docs/latest](https://spark.apache.org/docs/latest/) 为总锚 |
| Python 2.7/3.4 时代的 PySpark ML | PySpark `spark.ml` 一等公民 + Python 数据科学生态（pandas/arrow 桥）加厚 | ✅ [api/python](https://spark.apache.org/docs/latest/api/python/) 可达 |
| Pipeline 模型跨版本脆 | 模型元数据与持久化格式持续演进；升大版本重训仍是稳妥教义 | ⚠️ 无逐字可达专页，不列细节 |
| 4.x 坐标 | ML 线随 4.0.1/4.2.0 发版带走（函数/参数级增量） | ✅ [4.0.1 文档树](https://spark.apache.org/docs/4.0.1/) + [releases.html](https://spark.apache.org/releases.html) |
| 特征工程归宿 | 「管道进湖仓」：特征存储（feature store）与表格式事务成为批式 ML 数据面的新底座 | 盘上互见 [../Data_Fabric_Architectures/00-总览与阅读地图.md](../Data_Fabric_Architectures/00-总览与阅读地图.md)（治理面分工 ✅ 在盘）；⚠️ 外部专页不赘 |
