# 11 MLlib与机器学习管道（Ch11: Spark MLlib and ML）

> 章题与编号取证 ⚠️ 推定（按 2e 草案第 9 章"Spark MLlib 和 ML"对位推定为终版第 11 章）。节级结构依草案 ✅ 实抓：MLlib 与 ML 的新旧抉择 / 使用 MLlib（组织导入、特征编码与准备、缩放选择、训练、预测、服务与持久化、评估）/ 使用 Spark ML（管道阶段、参数、编码、清洗、模型、整合训练、访问单阶段、持久化、自定义算法扩展、模型服务）/ 一般服务考量。⚠️ 终版或有调整。

## 0. 本章主线

ML 章在"性能书"里的身份是**约束清单**：训练与推理的分布式形态（数据并行 vs 模型并行、迭代算法的 shuffle 模式、特征流水线的物化点）决定上一章章的调优结论哪些能直接用、哪些会翻车。新旧 API 抉择（9.1）在 2026 已是历史问题——RDD 路线退场，Pipeline/DataFrame 路线是唯一活路（回看 [03-Spark升级与迁移](03-Spark升级与迁移.md)）。⚠️

## 11.1 MLlib（旧）与 ML（新）的选择（草案 9.1 ✅）

- 判据史：`mllib`＝RDD 裸接口、性能可控但重造轮子；`ml`＝DataFrame 管道、Catalyst 红利＋可序列化流水线。终版口径 ⚠️ 推定：ml 默认，mllib 只余存量维护。
- 官方权威：https://spark.apache.org/docs/latest/ml-guide.html ✅（含迁移说明族）。
- 谱系分工：算法配方本体（ALS 推荐/决策树/聚类）在 ../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md 那条线，本章只记**性能形状**。

## 11.2 特征流水线的性能解剖（草案 9.2.2/9.2.3、9.3.4/9.3.5 ✅）

- VectorAssembler/StandardScaler/OneHotEncoder 链：每步都是一次宽转换候选；高基数 one-hot 是内存爆炸经典点（稀疏向量＋频截断为解，对应 08 章预聚合母题）。⚠️
- 管道训练＝多次 action 风险：fit 遍历数据 N 轮 ⇒ 血缘重放；persist 特征表与否的划算判定即 07 章 5.7 公式的 ML 实例。⚠️＋ml-guide ✅
- 🔧 概念锚回 [02-Spark运行原理](02-Spark运行原理.md) 的 E1：迭代算法每轮内存峰值与挤出阶梯同源（**类比非 Spark**）。

## 11.3 训练、预测与评估的形状（草案 9.2.4–9.2.7、9.3.6–9.3.9 ✅）

- 训练算子的 shuffle 指纹：基于树的算法多次排序/分位数扫描（RangePartitioner 的工业用户，接 08 章）；线性模型＝窄链＋小聚合。⚠️
- 预测阶段是吞吐主体：模型广播（接 07 章广播变量）＋分区内批式推断；评估指标（areaUnderROC 等）多为可 combine 聚合，成本低。⚠️＋ml-guide ✅

## 11.4 自定义算法与持久化服务（草案 9.3.11/9.3.12/9.4 ✅）

- Transformer/Estimator 契约：写自定义阶段=接入参数系统与序列化，换来 pipeline 可组合与可测（接 10 章计划断言）。⚠️
- 模型持久化：PMML/原生 save-load；"一般服务考量"小节讲离线批量打分 vs 低延迟服务的架构分叉——2026 判读：批量特征＋外部模型服务（模型出库到专用推理面）渐成主流，Spark 退守特征与批量层。⚠️ 趋势观察。

## 11.5 小结自检

1. 特征流水线哪三步最宽？物化点应选在哪？
2. fit 多轮遍历与血缘重放的兑换关系？
3. 树模型与线性模型各自的"shuffle 指纹"是什么形状？

## 11.6 互链

- 升级视角：[03-Spark升级与迁移](03-Spark升级与迁移.md)；内存/物化：[07-高效转换算子](07-高效转换算子.md)、[02-Spark运行原理](02-Spark运行原理.md)
- API 侧 ML：../Spark_The_Definitive_Guide/08-机器学习MLlib.md；配方线：../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md（其 04/05 章算法与本节性能形状互证）
- 图算法近亲：[12-组件打包与附录杂项](12-组件打包与附录杂项.md) 的 GraphX 节

## 核心概念速览（中英对照）

- **Pipeline/Estimator** — 管道与估计器：fit 产出 Transformer 的可组合 ML 抽象。
- **特征流水线** — Feature pipeline：编码/缩放/装配链，宽转换密度最高的地段。
- **稀疏向量** — Sparse vector：高维特征的内存解药，one-hot 爆炸的防线。
- **迭代收敛** — Iterative convergence：多轮遍历数据的训练范式，血缘重放风险源。
- **模型广播** — Model broadcast：小模型上发换分区内自给推断。
- **分位数直方图** — Quantile histogram：树算法分裂点的全局统计成本。
- **ML 迁移** — MLlib old → ml：RDD 路线到 DataFrame 路线的历史单行道。
- **批式打分** — Batch scoring：Spark 最稳的 ML 服务形态。
- **模型序列化** — Model save/load：管道持久化与跨版本兼容（回到断层线）。

## 最新演进与工业实践

- **RDD API 退场落地**：Spark 4.x 推进 old mllib 的移除线（⚠️ 具体版本节点以官方 ml 迁移文档为准，https://spark.apache.org/docs/latest/ml-guide.html ✅ 为权威入口），本章 9.1 的"抉择节"已成历史脚注。
- **ML 函数与 Python 化**：4.x 增 SQL 侧 ML 函数族（预测内联进查询计划）与 PySpark ML 面扩张；"特征在 Spark、训练在外部框架"的混合架构（pandas API 交棒 scikit/XGBoost）是工业默认。⚠️＋sql-performance-tuning 页 UDF 节 ✅
- **特征平台化**：特征库/在线离线一致（feature store）叙事接管草案"服务考量"节——与湖仓线 ../Use_Iceberg_with_Spark/06-维护过程与流式写入.md 的时间旅行/增量读天然咬合（⚠️ 趋势观察）。
- **谱系提醒**：算法配方与案例（协同过滤/异常检测等）归 ../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md，本册守性能与形状。
