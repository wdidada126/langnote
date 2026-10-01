# 07 · 推荐系统与 GraphX 配方（原书 Ch10 Recommender Systems + Ch11 Graph Processing Using GraphX）

> 精读重构笔记，非原书文本。目录取证：微信读书官方电子版目录快照（✅ 实抓）；Spark/GraphX 侧行为 ⚠️ 转述。
> 合并口径见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §3：Ch10（矩阵分解推荐）与 Ch11（图计算）同属「ML 进阶应用域」，且共享「稀疏大规模线性代数」底层。

## 1. 章域定位

Ch10-Ch11 是本书的「高级玩法」双子星：ALS 交替最小二乘做显式/隐式反馈协同过滤，GraphX 用 RDD 上的属性图做 PageRank/连通分量/邻域聚合。两章共同的底色是 **2015 年 Spark 想通吃 ML 与 Graph 两个引擎版图**的雄心——十年后的裁决：ALS 活成推荐基础设施常青树，GraphX 则输给专门图库与 Flink GEC，成为「官方保留、社区冷清」的典型。食谱体裁在 Ch11 尤其珍贵：GraphX 的教材覆盖历来稀薄。

## 2. 食谱地图

| # | 食谱（官方目录逐字） | 配方核心 | 2026 等价物 ⚠️ |
|---|---|---|---|
| 10.1 | Collaborative filtering using explicit feedback | Rating RDD → ALS.train 矩阵因子 → 预测/相似项 | ml.recommendation.Algorithm 同名存活 |
| 10.2 | Collaborative filtering using implicit feedback | ALS.trainImplicit + confidence 权重 α | 同族存活，工业主流范式 |
| 11.1 | Fundamental operations on graphs | Graph(vertices, edges) 构造、subgraph/mapVertices/Triplets | 语义迁移到图库/GEC ⚠️ |
| 11.2 | Using PageRank | graph.pageRank(tol, resetProb) + 静态版 | GraphFrames/Neo4j GDS 承接 |
| 11.3 | Finding connected components | graph.connectedComponents 最小 ID 标签 | Pregel 类框架/图库 API |
| 11.4 | Performing neighborhood aggregation | aggregateMessages(sendMsg, mergeMsg) 消息传递 | BSP/Pregel 范式通用概念 |

## 3. 精读块一：ALS 显式 vs 隐式（10.1/10.2）

**问题**：评分（explicit）与行为流（implicit）两种数据怎么各配一套 ALS。
**配方骨架**：显式——`ALS.train(ratings, rank, iterations, lambda)` 得用户/物品因子，`predictAll/mapUsersProducts` 出 TopN 与相似项；隐式——同一双线性模型但把观测当置信度 `c=1+α·r`，损失含置信加权项，α 是「观测=多大概率喜欢」的旋钮。
**评注 ⚠️**：两食谱把「rank 表达隐语义维度、lambda 防过拟合、iterations 收敛」三参数都做成扫表演示，这是同期书里少见的工程诚意。隐式 ALS 至今仍是召回层基线之一（与双塔/Essen 系神经方法共存）；当年 rank 取 10 级、今天 embedding 动辄 128+ 的尺度差要心里有数。
**冷启动与评估**：食谱未展开 hold-out/NDCG 评估与冷启动策略——姊妹册音乐推荐案例（[../Advanced_Analytics_with_Spark_2e/03-音乐推荐与Audioscrobbler数据集.md](../Advanced_Analytics_with_Spark_2e/03-音乐推荐与Audioscrobbler数据集.md)）恰好补了显式反馈真实数据集的完整管线，两书对读收益最大。

## 4. 精读块二：GraphX 抽象与三大算法（11.1-11.4）

- **属性图基元**：`Graph[VD, ED]` = 顶点 RDD + 边 RDD，方向视图（in/out/both）与 `EdgeTriplet` 三件套；
- **PageRank**：幂迭代到收敛 tol，`resetProb`（阻尼）显式暴露——食谱顺带讲透随机游走语义；静态版给快照查询；
- **连通分量**：CC 以最小顶点 ID 为标签做社区粗化，是「图上的 group by」；
- **aggregateMessages**：全书最难的单题——sendMsg（沿边发消息）+ mergeMsg（顶点归并）组合出三角计数/影响度数等模式，是 Pregel 风格 BSP 的手动挡。
**评注 ⚠️**：GraphX 的 RDD 血统让它每一步都是全图 shuffle，十亿边级迭代代价高昂；3.x 后官方精力转向 GraphFrames 与 ML pipeline 集成，GraphX 文档原地踏步——本目录判定 Ch11 为「思想常青、载体退役」。
**对位阅读**：GraphX 真实伴生网络案例见 [../Advanced_Analytics_with_Spark_2e/07-用GraphX分析伴生网络.md](../Advanced_Analytics_with_Spark_2e/07-用GraphX分析伴生网络.md)；图数据库视角的接班方案索引见 [../数据库系列·总索引.md](../数据库系列·总索引.md) 图/多模条目。

## 5. 精读块三：两章的公共数学骨架

ALS 是「用户×物品稀疏矩阵分解」，GraphX 邻域聚合是「稀疏邻接矩阵 × 向量」——两章实为稀疏线性代数的两张应用皮。读通 05 章矩阵食谱（6.3）再看这两章，可见 Rishi Yadav 的编排意图：先给基元、再给三种终局（表格 ML/推荐/图）。这个骨架也解释了为什么 GraphX 在深度图学习时代被「采样 + GNN 训练器」架构替代：矩阵-向量迭代范式没变，变的是调度与存储 ⚠️。

## 6. 🔧 类比说明

ALS 与图迭代算法无单机 SQL 类比面（无矩阵分解/消息传递算子；DuckDB 关系型 JOIN 不能等价复现幂迭代收敛语义），本章不设 🔧 组；全书类比实验口径见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §7。

## 7. 互链清单

- 主参照：[../Spark_The_Definitive_Guide/08-机器学习MLlib.md](../Spark_The_Definitive_Guide/08-机器学习MLlib.md)、[../Spark_The_Definitive_Guide/04-聚合与复杂数据类型.md](../Spark_The_Definitive_Guide/04-聚合与复杂数据类型.md)（聚合直觉底座）
- 姊妹册：[../Advanced_Analytics_with_Spark_2e/03-音乐推荐与Audioscrobbler数据集.md](../Advanced_Analytics_with_Spark_2e/03-音乐推荐与Audioscrobbler数据集.md)、[../Advanced_Analytics_with_Spark_2e/07-用GraphX分析伴生网络.md](../Advanced_Analytics_with_Spark_2e/07-用GraphX分析伴生网络.md)
- 底座：[../bigdata/03-Shuffle与宽依赖.md](../bigdata/03-Shuffle与宽依赖.md)（迭代式全图 shuffle 成本根源）
- 承前启后：[06-分类与无监督学习配方.md](06-分类与无监督学习配方.md) ｜ [08-性能优化与调优配方.md](08-性能优化与调优配方.md)

## 8. 配方骨架速查（考古重构，⚠️ 转述，语法按 1.x 旧 API 惯例）

- **10.1**：`val model = ALS.train(ratings, rank, iterations, lambda)`；`model.mapUsersWithProducts / predictAll` 出推荐位；相似物品走 `model.similarity` 谱系 ⚠️。
- **10.2**：`ALS.trainImplicit(ratings, rank, iterations, lambda, alpha)`——ratings 的行为强度进 confidence `1+α·r`，α 语义食谱专段讲解 ⚠️。
- **11.1**：`Graph(edges).groupVertices(...)` 或顶点 RDD+边 RDD 双入参构造；`subgraph(epred, vpred)` 切片、`mapVertices` 重打标、`triplets()` 遍历 EdgeTriplet ⚠️。
- **11.2/11.3**：`graph.pageRank(tol, resetProb)._2.vertices`、`graph.connectedComponents().vertices`——结果都是顶点属性 RDD ⚠️。
- **11.4**：`graph.aggregateMessages(sendMsg, mergeMsg, TripletFields.All)`——两函数签名 (EdgeContext)→Unit 与 (A,A)→A 即消息传递全部心法 ⚠️。

## 9. 自测卡（合卷作答，8 问）

1. 显式与隐式反馈的损失函数各长什么样？置信度出现在哪一侧？
2. ALS 为什么天然可并行？（固定一侧后另一侧按行独立最小二乘）
3. rank 与 λ 分别控制什么？过拟合症状如何二分？（表达力/收缩强度）
4. 隐式 α 调大会偏向什么行为特征？（高频观测=更强喜欢假设）
5. GraphX 的每轮 PageRank 为什么贵？（全图消息合并即全量 shuffle）
6. CC 的标签策略是什么？（最小顶点 ID 冒泡）
7. aggregateMessages 的 mergeMsg 必须满足什么代数性质？（交换半群，否则不可并行归并）
8. 为什么说 ALS 与邻域聚合共享同一数学骨架？（稀疏矩阵×向量迭代的两种应用皮）

## 10. 小练习

1. 用 10.1/10.2 的参数表设计一个「召回层双通道」实验计划（显式模型冷启动、隐式模型打底），三行即可。
2. 把 11.4 的三角计数改写为你业务图上的一个聚合配方（好友共现/订单共购任选），写出 send/merge 两函数伪码。
3. 对读姊妹册 [../Advanced_Analytics_with_Spark_2e/03-音乐推荐与Audioscrobbler数据集.md](../Advanced_Analytics_with_Spark_2e/03-音乐推荐与Audioscrobbler数据集.md)，列出它在评估面上补的三块内容。

## 11. 易混点辟谣（快问快答）

- **误区：ALS=矩阵分解=深度推荐**——它是线性双因子分解，与两塔神经模型是共存而非替代关系。
- **误区：隐式反馈没有标签就不算监督**——隐式 ALS 照样是最小化加权损失的监督式目标，只是「标签」被置信度改写。
- **误区：GraphX 的图就是图数据库**——RDD 值语义快照，没有事务、没有索引、没有即席查询面 ⚠️。
- **误区：PageRank 放任何图都对**——其随机游走语义预设「链接=引用/信任」，社交强关系图上未必是合适中心性。
- **误区：连通分量=社区发现**——CC 只做粗切分，社区粒度要靠模块度/LPA/标签传播家族继续做。
- **误区：aggregateMessages 随旧 API 一起过时**——send/merge 即 BSP 思维本体，在所有图引擎里换名复活。

## 12. 读后行动清单

1. 用 10.1/10.2 设计双通道召回实验计划（冷启动走显式、行为打底走隐式），五行内。
2. 把 11.4 三角计数改写为你业务图（共购/共友任选）的 send/merge 伪码。
3. 列三件现代图计算替代件（GraphFrames/图库 GDS 系/Flink GEC）各自接管了本章哪些场景 ⚠️。
4. 对读姊妹册 [../Advanced_Analytics_with_Spark_2e/03-音乐推荐与Audioscrobbler数据集.md](../Advanced_Analytics_with_Spark_2e/03-音乐推荐与Audioscrobbler数据集.md)，总结评估面三缺口。

### 本章一页纸总结

ALS 四参数：rank（表达力）、λ（收缩）、iterations（收敛）、α（隐式置信放大）。
GraphX 三板斧：构造（Graph/EdgeTriplet）→ 传播（aggregateMessages）→ 迭代收敛（PageRank/CC 类）。
一句话判词：ALS 仍在生产，GraphX 已进博物馆——带着这个落差重读，两章都是好材料。

## 核心概念速览（中英对照）

- **协同过滤** — collaborative filtering：从群体行为矩阵补全个体偏好的推荐范式总称。
- **ALS** — alternating least squares：固定一侧解另一侧的矩阵分解交替求解，天然可并行。
- **显式/隐式反馈** — explicit / implicit feedback：评分 vs 行为流，后者以置信度加权观测。
- **隐语义维度** — latent rank：用户/物品因子向量维度，容量与过拟合的权衡旋钮。
- **confidence/α** — 置信系数：隐式 ALS 把频次映射为「多大概率喜欢」的放大器。
- **属性图** — property graph（GraphX 版）：顶点 RDD + 边 RDD 加类型化属性的图抽象。
- **PageRank** — PageRank：随机游走中心性，阻尼系数 resetProb 的幂迭代实现。
- **连通分量** — connected components：图粗化/社区发现第一步，「图上的 group by」。
- **aggregateMessages** — 邻域聚合：send/merge 双函数表达的消息传递原语，Pregel 手动挡。
- **EdgeTriplet** — 边三元组：src 属性 + dst 属性 + 边属性的联合视图。
- **GraphFrames** — GraphFrames：DataFrame 系图库，GraphX 思想的结构化继任者之一 ⚠️。
- **双塔召回** — two-tower retrieval（本目录对照词）：与 ALS 同占召回层的神经范式，embedding 尺度差十倍。

## 最新演进与工业实践

- **推荐面**：`ml.recommendation`（DataFrame Rating 列）接管 10.x 两食谱；ALS 在 GPU（cuML 版）上迭代时间缩到秒-分级，工业中作为召回基线/评估对照长期驻留；主流增量在「两塔 + 序列模型 + LLM 重排」栈，Spark 退为特征与 embedding 批量生产端 ⚠️。
- **图面**：GraphX 官方文档 ✅ https://spark.apache.org/docs/latest/graphx-programming-guide.html （2026-10-01 curl -sI 200）内容自 2.x 冻结——「文档活着、演进停止」的标本；生产图计算分流向 Neo4j/TigerGraph 等图库与 Flink GEC，聚合/CC/PageRank 语义在 GraphFrames `aggViews` API 中有最贴近的 Spark-native 复刻 ⚠️。
- **评估补课**：ALS 时代的 hold-out 评估、覆盖率/多样性指标（除 RMSE 外）在 2020s 由离线-在线双环 + 多目标重排补齐，食谱未涉的评估面如今是推荐系统主要工作量所在。
- **谱系考古**：ALS 分布式实现源自 UC Berkeley 的 Spark 早期 showcase（GitHub 仓库地址本波不可达 ⚠️ 未引链）；GraphX 论文（GraLSD, NSDI 2014）给出 RDD 图引擎设计动机——DOI 未过 Crossref 校验，仅题录 ⚠️。概念谱系对位可读 [../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)。
- **阅读建议**：Ch10 完整精读（参数扫表方法论至今可迁移），Ch11 读 11.4 一个食谱即可掌握 BSP 思维，其余交给图库文档。
