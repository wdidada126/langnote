# 05 · MLlib 基础与回归配方（原书 Ch6 Getting Started with Machine Learning Using MLlib + Ch7 Supervised Learning with MLlib – Regression）

> 精读重构笔记，非原书文本。目录取证：微信读书官方电子版目录快照（✅ 实抓）；Spark/MLlib 侧行为 ⚠️ 转述。
> 合并口径见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §3：Ch6（线性代数基元与统计工具）与 Ch7（回归模型）同属「MLlib 地基 + 线性模型」域。

## 1. 章域定位

Ch6-Ch7 承担本书机器学习域的地基：Ch6 教「MLlib 的数据类型与统计工具箱」——Vector、LabeledPoint、Matrix、汇总统计、相关性、假设检验，外加一节前瞻性的 `org.apache.spark.ml` pipeline 起步；Ch7 把地基直接用在回归上：线性回归、代价函数认知、lasso 与 ridge。两章合读能清晰看到 2015 年 MLlib 的**双 API 断层现场**：旧的 `mllib`（RDD 原子算法）与新的 `ml`（DataFrame pipeline）并存，本书恰好站在断层线上，Ch6 末节是全书法式最新鲜的部分。

## 2. 食谱地图

| # | 食谱（官方目录逐字） | 配方核心 | 2026 等价物 ⚠️ |
|---|---|---|---|
| 6.1 | Creating vectors | Vectors.dense/sparse，MLlib 全部算法的输入原语 | 仍存活；ml 系改用 VectorUDT 列 |
| 6.2 | Creating a labeled point | LabeledPoint(label, features) 监督样本对 | 被 DataFrame 标签列取代 |
| 6.3 | Creating matrices | 行列式/坐标式 Matrix 构造 | 面向线性代数旧 API，多已弃用 |
| 6.4 | Calculating summary statistics | ColumnStatistics/Statiliics 类均值方差计数 | DataFrame describe/summary |
| 6.5 | Calculating correlation | corr/cov 皮尔逊矩阵 | DataFrame.stat.corr |
| 6.6 | Doing hypothesis testing | chiSq/卡方、t 检验 | DataFrame.stat + Apache Commons |
| 6.7 | Creating machine learning pipelines using ML | Pipeline/Stage/Param 初体验 | ml 系全面胜出，含 CrossValidator |
| 7.1 | Using linear regression | LinearRegressionWithSGD 梯度下降 | ml.regression.LinearRegression |
| 7.2 | Understanding cost function | MSE/损失地形与步长关系 | 概念长青，教学位 |
| 7.3 | Doing linear regression with lasso | 迭代 L1 惩罚配方 | ml ElasticNetModel(l1Ratio) |
| 7.4 | Doing ridge regression | 迭代 L2 惩罚配方 | ml ElasticNetModel(l2Ratio) |

## 3. 精读块一：向量原语与稀疏表示（6.1-6.3）

**问题**：高维稀疏特征怎么在 RDD 上表示。
**配方骨架**：`Vectors.sparse(n, indices, values)` 只存非零元；LabeledPoint 打包标签；Matrix 给分解类算法。
**评注 ⚠️**：稀疏向量的「维度全存、非零压缩」设计沿用至今（VectorUDT 同构），但外层容器从 RDD[LabeledPoint] 换成 DataFrame 列后，Ch6 的多数构造食谱只剩类型学意义。矩阵类 API（行式 Matrices）在 ml 系中基本蒸发，这是食谱体裁最难察觉的报废——标题看着还活，类已无人 import。
**与 repo 对照**：RDD 载体本身的心智模型见 [../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md](../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md)、[../bigdata/02-Spark核心与RDD模型.md](../bigdata/02-Spark核心与RDD模型.md)。

## 4. 精读块二：统计工具食谱——从手算到统计签名（6.4-6.6）

**要点**：ColumnStatistics 一遍遍历给计数/均值/方差/极大极小（分布式矩聚合）；corr 默认皮尔逊；chiSq 对分类特征做独立性检验，输出 (统计量, p 值, 自由度)。
**2026 姿势 ⚠️**：`df.describe()`、`df.stat.corr/cov/freqItems` 全面接管；统计假设检验更多外包给专门库（scipy/Commons）。食谱价值转移到「为什么卡方适合类别特征筛查」的判断力本身。
**坑**：p 值在超大样本下的过敏现象（任何微小效应都显著）与多重检验校正，两本时代的 MLlib 食谱都不谈，今天仍然要自己补。

## 5. 精读块三：pipeline 初现（6.7）——本书的转折点

**问题**：feature 化、模型、评估怎么可重用地串起来。
**配方骨架**：`Pipeline(stages=[Tokenizer, HashingTF, LogisticRegression])`（书内用回归例）+ PipelineModel.transform 贯穿 train/serve。
**评注 ⚠️**：ml 系（DataFrame-based Pipeline/Transformer/Estimator）自此成为 Spark ML 唯一正道；mllib 旧 API 自 3.x 起进入弃用倒计时（官方 ml-guide 标注 maintenance）。Ch6 末节让本书免于纯考古册的命运。
**对位阅读**：[../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md](../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md)——同年代姊妹案例册，其决策树章（[../Advanced_Analytics_with_Spark_2e/04-用决策树预测森林植被.md](../Advanced_Analytics_with_Spark_2e/04-用决策树预测森林植被.md)）展示了 pipeline 化之后的完整案例形态。

## 6. 精读块四：回归三件套（7.1-7.4）

- **线性回归**：SGD 求解、迭代次数/步长/mini-batch 率三旋钮，食谱逐一试给读者看收敛曲线；
- **代价函数**：MSE 凸地形 → 解释为什么小学习率慢、大学习率震荡，属于「配方中的理论插曲」，本书特色；
- **lasso/ridge**：L1 造稀疏解（特征选择）、L2 平滑收缩（抗共线性），当年靠不同 `RegressionWithSGD` 子类实现；
- **2026 ⚠️**：全部并入 `ml.regression.LinearRegression/Lasso/Ridge/ElasticNet`（参数 regularizationParam + elasticNetParam），并支持 LBFGS 拟牛顿求解器——SGD 单解法时代结束。
- **坑**：特征不标准化时正则化惩罚失衡，7.3/7.4 未强调，StandardScaler 前置是永恒前提。

## 7. 🔧 类比说明

MLlib 线性代数与模型训练语义无单机 SQL 类比面（无矩阵库、无梯度下降算子），本章不设 🔧 组；全书类比实验 8 组集中于 02/03/04/08 章，口径见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §7。

## 8. 互链清单

- 主参照：[../Spark_The_Definitive_Guide/08-机器学习MLlib.md](../Spark_The_Definitive_Guide/08-机器学习MLlib.md)（pipeline 时代的 ML 章）
- 姊妹册：[../Advanced_Analytics_with_Spark_2e/01-大数据分析.md](../Advanced_Analytics_with_Spark_2e/01-大数据分析.md)、[../Advanced_Analytics_with_Spark_2e/04-用决策树预测森林植被.md](../Advanced_Analytics_with_Spark_2e/04-用决策树预测森林植被.md)
- 底座：[../bigdata/02-Spark核心与RDD模型.md](../bigdata/02-Spark核心与RDD模型.md)
- 分类/无监督续章：[06-分类与无监督学习配方.md](06-分类与无监督学习配方.md) ｜ 推荐/图：[07-推荐系统与GraphX配方.md](07-推荐系统与GraphX配方.md)

## 9. 配方骨架速查（考古重构，⚠️ 转述，语法按 1.x 旧 API 惯例）

- **6.1**：`Vectors.dense(1.0, 0.0, 3.0)` / `Vectors.sparse(n, idxArr, valArr)` 是所有下游算法的输入原语 ⚠️。
- **6.2**：`new LabeledPoint(label, features)` 打包监督样本，RDD[LabeledPoint] 即训练集 ⚠️。
- **6.4-6.6**：`Statistics.colStats(rddVectors)`、`Statistics.corr(rdd, method)`、`Statistics.chiSq(observedMatrix)` 三族 ⚠️。
- **6.7**：`new Pipeline().setStages(Array(tokenizer, hashingTF, lr))` → `pipeline.fit(df)` → `model.transform(df)`；DataFrame 侧闭环 ⚠️。
- **7.1**：`LinearRegressionWithSGD.train(parsedData, numIterations, stepSize)`；迭代/步长/子批率三参数同屏演示 ⚠️。
- **7.3/7.4**：`RDDLOMSUpdater` 时代过去后，lasso/ridge 以 `RidgeRegressionWithSGD / LassoWithSGD` 形态各给一题；regularizationParam 即 λ ⚠️。

## 10. 自测卡（合卷作答，8 问）

1. 稀疏向量存什么、不存什么？n 的作用？（非零下标与值；0 的个数由维度差推出）
2. LabeledPoint 与 DataFrame 标签列的语义等价与生态差？（同为 (y,x)；后者才有 pipeline 集成 ⚠️）
3. ColumnStatistics 为什么能单遍算方差？（矩聚合并行可结合）
4. 卡方适合什么类型特征？大样本 p 值的坑？（类别独立性；过敏显著）
5. Pipeline 三概念 Stage/Param/fit-transform 各一句话？
6. SGD 三旋钮对收敛曲线各管什么？（速度/稳定/单次数据量）
7. lasso 与 ridge 解形态的本质差？（角点稀疏 vs 平滑收缩）
8. 正则化前必须做的预处理是什么？为何 7.3/7.4 食谱没写？（标准化；λ 惩罚按尺度失衡——食谱盲区）

## 11. 小练习

1. 把 7.1 的三旋钮写成「症状→旋钮→方向」对照表（慢收敛/震荡/抖动各一行）。
2. 用 6.7 伪码把你熟悉的一个分类任务（任意语言生态）改写成 pipeline 三 stage，标出可替换件。
3. 读 [../Spark_The_Definitive_Guide/08-机器学习MLlib.md](../Spark_The_Definitive_Guide/08-机器学习MLlib.md) 的回归节，写五行「与 Ch7 的三处 API 断层」清单。

## 核心概念速览（中英对照）

- **稀疏向量** — sparse vector：只存非零下标的向量表示，高维特征工程的原语。
- **标注样本** — LabeledPoint：(label, features) 二元组，旧 mllib 监督算法统一输入。
- **列统计** — ColumnStatistics：分布式单遍计算的计数/均值/方差/极值聚合。
- **皮尔逊相关** — Pearson correlation：corr 食谱的默认线性相关度量，非线性关系会漏检。
- **卡方检验** — chi-squared test：分类特征与标签独立性筛查工具，6.6 的主角。
- **Pipeline/Stage** — ML pipeline：估计器-变换器串联的复用框架，6.7 前瞻内容。
- **梯度下降** — SGD：7.1 的求解器，步长/迭代/子批率三旋钮决定成败。
- **代价函数** — cost function：MSE 损失面，凸性解释学习率效应的理论支点。
- **L1 正则** — lasso：绝对值惩罚诱导稀疏解，自带特征选择属性。
- **L2 正则** — ridge：平方惩罚收缩系数，抗多重共线性。
- **ElasticNet** — 弹性网络：L1/L2 混合，2026 年以单一估计器接管 7.3/7.4 两食谱 ⚠️。
- **特征缩放** — feature scaling：正则化前置于 StandardScaler 的恒常坑位。

## 最新演进与工业实践

- **API 统一**：`org.apache.spark.ml`（Pipeline/Transformer/Estimator + DataFrame）自 2.x 起为唯一活跃面，旧 mllib  RDD API 处于维护态——官方 ML 指南 ✅ https://spark.apache.org/docs/latest/ml-guide.html （2026-10-01 curl -sI 200）通篇以 pipeline 组织，可与 6.7 逐段对照读。
- **求解器升级**：LinearRegression 默认 LBFGS（迭代式拟牛顿），SGD 退为可选；分布式特征重要性/系数的显著性输出（summary 对象）补齐了当年「只能点估计」的缺口 ⚠️。
- **统计库分工**：描述统计/相关性留在 Spark（df.stat 系），假设检验与多重校正转给 scipy/statsmodels 风格生态或 JDBC 侧数仓统计函数——「MLlib 统计工具箱」章的定位被生态细分稀释。
- **工业实践**：表格特征管道（Spark 做 ETL + 特征存储 + 外部训练平台）与「MLflow 全链路跟踪」成为 2020s 标准栈；MLlib 退守为批式基线与超大规模线性模型（LogisticRegression/Lasso 十亿特征级）的专用工具 ⚠️。中译教材视角的训练案例可对照 [../Spark大数据分析与实战.md](../Spark大数据分析与实战.md)（教学型、非食谱型，辨析见 00 §5）。
- **阅读建议**：Ch6 只精读 6.1/6.4/6.7，Ch7 只精读 7.2（代价函数直觉）——其余以现代 API 文档重建手感即可。
