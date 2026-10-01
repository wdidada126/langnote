# 08 Machine Learning with Spark（Spark 机器学习）

> 原书 Ch8，pp.331–393（63 页）：MLlib 的 DataFrame 时代用法——Pipeline/Transformer/Estimator 抽象、特征工程、回归/分类实操、交叉验证调参。二级小节未实抓 ⚠️，主题簇依章题、页幅与官方 ml-guide 结构推定；属**精读重构**。

## 8.1 两套 MLlib：旧 RDD 线归档，spark.ml 是主线 ⚠️

- 官方口径：`spark.mllib`（RDD[LabeledPoint] 老 API）自 Spark 2.x 起进入维护、3.x 明确弃用；本册只教 `spark.ml`（DataFrame API）——入门者不必考古 ⚠️（本册立场重构）。
- MLlib 的「分布式」边界要诚实：算法核心多是单机模型上做数据并行（如 GBT 逐层、逻辑回归 mini-batch），并非学术分布式学习框架；它的价值在**和 ETL 同栈**——特征管道与训练共用 DataFrame 世界 ⚠️。
- 对照盘上：MLlib 权威章 [../Spark_The_Definitive_Guide/08-机器学习MLlib.md](../Spark_The_Definitive_Guide/08-机器学习MLlib.md)；分析案例纵深（推荐/聚类/图）在 [../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md](../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md)。

## 8.2 Pipeline 抽象：把 ML 工程化成三段式 ⚠️

- 三元组：`Transformer`（fit 后产出 transform，如模型）、`Estimator`（fit 产出 Transformer，如算法+超参）、`Pipeline`（两者串成 DAG，可整体 save/load）。
- 入门价值主张（本册金句重构）：Pipeline 让「特征预处理+模型」成为**一个可部署工件**——测试泄漏防护与上线一致性的最小机制；对比裸 sklearn：DataFrame 语义天然可扩到集群。
- `ParamMap`、PipelineModel 序列化到目录（PMML/原生 export 本册点到 ⚠️）；ML 管道的「可复现」在这里第一次被当作卖点讲。

## 8.3 特征工程：从脏列到向量 ⚠️

- 链条样板（官方 ml-guide 语境，锚点 https://spark.apache.org/docs/latest/ml-guide.html ✅ curl 2026-10-01 200）：`StringIndexer`（类别→序号）→ `OneHotEncoder`（→稀疏二值）→ `VectorAssembler`（→features 向量）→ `StandardScaler/Imputer/ChiSqSelector` 按需插入；`ml-functools` 缺失值策略。
- 教学顺序与 03 章呼应：特征面的一切前置（schema/缺失/类型）都是 Spark SQL 基础——本册有意让 ML 章站在 SQL 章肩上 ⚠️。
- 标签列约定：`label` 列名、二分类 0/1、回归连续值；评估器（`MulticlassClassificationEvaluator/RegressionEvaluator`）吃 DataFrame 吐指标——「指标从数据里算，不从模型里掏」是入门者最该记住的方向感。

## 8.4 模型实操：回归与分类各一例 ⚠️

- 回归线：线性回归（带正则 elasticNetParam 旋钮）→ 决策树回归 → GBT；分类线：逻辑回归（二分类默认）→ 随机森林；每例配 train/test 切分与 `CrossValidator` 或 `TrainValidationSplit` 调参 ⚠️ 具体数据集名依本册（教材常自造样例 CSV）。
- 指标面：回归 rmse/r2；分类 areaUnderROC/precision-recall——本册在 Ch8 给入门解释、Ch9 把它们接进监控（生命周期闭环）。
- 边界诚实：本册**不教**深度学习（Deep Learning 仅在前言出现为「不在范围」⚠️ 推定）、不教图算法；MLlib 之外的训练框架衔接留给 Ch9 生态叙事。

## 8.5 🔧 概念类比登记（本章无 Spark 可测面）

- 本册 Spark 不可装（沿用波6 结论），ML 管道的「单机标本」用本目录已有 SQL 实验借位：8.3 的 VectorAssembler 本质是**投影层列合并**——DuckDB 里用 `SELECT` 拼列+`CREATE VIEW` 即可看到同款「管道=视图链」结构（复用 03/04 脚本 `E1/E5` 的表与视图语法；**非本书 Spark 引擎行为**）。
- 说明：本组类比不新增数字测量，只登记机制对应；训练/评估的数值行为（迭代收敛、指标计算）无任何单机替身，全部以官方文档 ⚠️ 转述。

## 8.6 本章练习视角（重构）⚠️

① 把一段 sklearn 风格「先 fit 编码器再切分」改写成 Pipeline，观察泄漏差异（概念题，本机无 Spark 环境 ⚠️）；② 用 `extractParamMap` 打印管道默认值，理解 Param 继承；③ 对随机森林网格 `ParamGridBuilder` 三参数×CrossValidator，估 fold 数与作业数的乘积——这是「调参=批作业放大器」的算术课。

## 8.7 Pipeline 样板逐行讲（重构 ⚠️ 语法示意非原书代码）

```
assemblers = [StringIndexer(inputCol="city", outputCol="city_i"),
              OneHotEncoder(inputCol="city_i", outputCol="city_oh"),
              VectorAssembler(inputCols=["city_oh","age","amt"], outputCol="features")]
model = GBTClassifier(labelCol="label", featuresCol="features", maxDepth=5)
pipe = Pipeline(stages=assemblers + [model])
grid = ParamGridBuilder().addGrid(model.maxDepth, [3,5,7]).build()
cv = CrossValidator(estimator=pipe, estimatorParamMaps=grid,
                    evaluator=MulticlassClassificationEvaluator(), numFolds=3)
best = cv.fit(train_df)          # 整个网格在管道上跑
```

- 三处教学眼：① `Pipeline` 把「拟合编码器」与「拟合模型」锁成同一份数据划分（防泄漏的机制表达）；② `CrossValidator` 的作业数 = 网格×折数——8.6③ 的算术在这里兑现；③ 导出的 `PipelineModel` 含预处理段——上线工件与训练工件同一个，测试环境一致性由此保证。

## 8.8 算法地图：MLlib 给什么、不给什么（重构 ⚠️）

- 给足的：线性/逻辑回归、决策树/随机森林/GBT、K 均值、朴素贝叶斯、ALS（推荐，概念级）、评估与选择器全家桶。
- 给半的：多层感知（MLP，官方标注易不稳定 ⚠️）、保序回归/生存分析（长尾存在感低）。
- 不给的：深度学习（TF/PyTorch 生态）、GBDT 之王 XGBoost（外部包）、AutoML 平台（Databricks 侧产品）。
- 选型直觉：结构化表格+亿级行+同栈 ETL → MLlib 合适；模型复杂度优先 → 把数据（而非模型）搬到专用训练框架，Spark 只做特征供给——2026 的分工线大致如此 ⚠️。
- 盘上案例纵深：ALS/聚类/图的实作在 [../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md](../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md)（波6 在盘册，与本册 Ch8 是「练习册 vs 案例集」关系）。

## 8.9 评估面补刀：指标从哪来、到哪去（重构 ⚠️）

- 评估器的输入输出：吃预测结果 DataFrame（label+prediction+probability 列约定）、吐标量——指标是「查询」不是「库函数返回值」，可审计可重放。
- 二分类列约定：`probability` 为稀疏向量，正类概率取 `[1]`——AUC 曲线直接用 `areaUnderROC` 列名计算。
- 多分类路径：`label` 从 0 起连续整数（StringIndexer 产物直接可用），标签映射要随模型一起版本化（Ch9 的 feature/model 同源纪律）。
- 与监控的接缝：Ch8 的离线指标（rmse/auc）到 Ch9 变成在线告警阈值——同一列名两处出现，是本册刻意缝合的线索 ⚠️ 是否刻意不可考，登记为结构观察。

## 8.10 速自检（答案在上文）

1. spark.ml 与 spark.mllib 一字之差差在哪两代 API？
2. Transformer 与 Estimator 的 fit/transform 分工？
3. Pipeline 防测试泄漏的机制是什么（和 sklearn 手动 fit 的差异）？
4. 特征链四件套的名字与顺序？
5. VectorAssembler 的产物列被谁消费？
6. 二分类的 probability 取第几位、为什么？
7. CrossValidator 的作业数算术=？
8. TrainValidationSplit 省的是什么、亏的是什么？
9. MLlib 的「分布式」边界一句：单机模型+____并行。
10. 哪些任务该把数据搬去别的框架而不是硬用 MLlib？
11. 评估器为什么是「对 DataFrame 的查询」？
12. 🔧 8.5 的类比借的是哪个 SQL 概念、缺席的是什么？

## 8.11 训练侧黑话小词典（语境卡 ⚠️）

- 特征列约定（features/label）：MLlib 的世界观列名，管道一切围绕它。
- 稀疏向量（sparse vector）：独热/高频零特征的存储形态，内存税的直接决定者。
- 正则面（regParam/elasticNetParam）：线性系的调参主战场。
- fold 面：交叉验证的划分轴，网格×折是成本的双乘。
- flavor：模型多框架导出形态（Ch9 的主语）。
- 在位场景：数据大、模型小、要同栈——MLlib 的 2026 生存线。

## 8.12 微补：数据划分与随机性

- `randomSplit` 的种子决定可复现性：调参复盘时「同一份切分」是隐含前提——入门者最常在此失去可比性。
- 类别不平衡的最低处理：classWeight/重采样参数位（各算法命名不一）+ 指标选 precision-recall 而非裸 accuracy——本册在此给到概念、留白给练习 ⚠️。
- 一行补充：管道 save/load 走目录格式（`pm.save(path)`/`PipelineModel.load`），跨 Spark 小版本加载可能失败——工件版本纪律自本章起生效（`09` 的前置）。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 转换器 | Transformer | 输入 DataFrame→输出增列 DataFrame 的 fit 产物 |
| 估计器 | Estimator | 在数据上 fit 出 Transformer 的算法对象 |
| 管道 | Pipeline | Estimator/Transformer 的可序列化 DAG |
| 特征向量 | Features Vector | 数值+稀疏编码合成的模型输入列 |
| 索引编码 | StringIndexer | 类别串→序号的默认第一步 |
| 独热编码 | OneHotEncoder | 序号→稀疏二值维度 |
| 向量装配 | VectorAssembler | 多列→单 features 列的 Transformer |
| 交叉验证 | CrossValidator | k 折网格评估 Estimator 选择器 |
| 训练验证切分 | TrainValidationSplit | 单切分省算力的调参近似 |
| 评估器 | Evaluator | 从结果 DataFrame 计算指标的 Transformer |
| 参数图 | ParamGrid | 超参组合的笛卡尔面 |
| RDD 线归档 | spark.mllib deprecated | 旧 API 进入维护的官方定调 |

## 最新演进与工业实践

- **MLlib 官方进入维护模式（3.x 后期→2026）**：Spark 社区公告路线把 MLlib 标为「稳定但不再积极发展」，新算法重心外移（GPU 训练/大模型时代 MLlib 不在叙事中心）⚠️（官方文档+社区通告口径，锚点 https://spark.apache.org/docs/latest/ml-guide.html ✅）；读法修正：本册教的是「**平台内建基线**」而非前沿——工业上 MLlib 仍在「数据大、模型小、要同栈」的场景长期在位（风控评分卡/GBDT 基线/分类回归常规任务）。
- **与 Spark 主线之外框架的分工**：特征工程越来越多交给专用层（Feathr/Featuretools/平台内置 Feature Store，Ch9 续）；训练走 PyTorch/XGBoost（Spark 仅作数据供给与并行调度），`spark.ml` 管道在 2026 更多是「入门理解 ML 工程抽象」的教学载体——抽象（Pipeline/版本化/可部署工件）比 API 更长寿 ⚠️。
- **盘上深读**：算法案例（ALS 推荐、K-means、GBT 植被数据）在 [../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md](../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md)；Spark 作为 AI 平台底座的关系登记于 [../数据库系列·总索引.md](../数据库系列·总索引.md) 引擎条目。
