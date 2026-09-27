# 03 · 音乐推荐和 Audioscrobbler 数据集（Music Recommendations）

> 《Advanced Analytics with Spark, 2e》第 3 章精读重构 ｜ 总览见 [00-总览与阅读地图.md](00-总览与阅读地图.md) ｜ ✅ / ⚠️ / 🔧（DuckDB 1.5.5 类比，非 Spark 行为）

## 章定位

全书第一个 ML 案例：在 Last.fm/Audioscrobbler 隐式反馈（"听过"而非"打分"）上训练**ALS 矩阵分解**推荐模型，并给出完整的评估-调参-服务化流程。官方代码 ✅ `2nd-edition` 分支 `ch03-recommender`；数据 ✅ 仓库 README 指向 `storage.googleapis.com/aas-data-sets/profiledata_06-May-2005.tar.gz`（2005 年快照，约 24 万用户 × 36 万曲目，稀疏度 ~0.15% 量级 ⚠️ 具体密度未本机验证）。

## 3.1 数据集与预处理

- profiledata 为 RDF/XML（FOAF/DOAP 类）⚠️——章例第一步即流式解析 XML 提取 (用户, 艺人, 播放次数) 三元组：SAX 式逐行正则/解析器（`javax.xml.stream`），演示"RDD 上处理半结构化文本"的样板 ⚠️。
- 清洗三件套：过滤垃圾用户（匿名/超大列表）、过滤冷门项、按用户抽样测试集——后续所有案例章复用此纪律 ⚠️。
- 🔧 播放事实表聚合语义（非 Spark）：DuckDB 在 8 行模拟播放表上 `GROUP BY artist` 实测：NULL 艺人自成一组（n=2, sum=5）；`sum(cnt) FILTER (cnt>2)` 得 KoL 8 / Radiohead 5 / Muse 4——Spark DataFrame 的 `agg(sum(when(cond)))` 与 `filter().groupBy()` 书写的是同一语义（✅ sql-function-descriptions 口径）。这类"计数去重、过滤聚合"正是本章 (user,artist,play_count) 三元组生成的骨架。

## 3.2 推荐系统方法论（本章理论核心）

- 协同过滤两分：基于邻域（user↔user 相似度）vs **基于模型（矩阵分解）**；书选后者，理由=规模与稀疏性下可并行求解 ⚠️。
- **ALS（交替最小二乘）**：把评分矩阵 R ≈ 用户因子 U × 物品因子 Vᵀ 的非凸问题拆成固定一侧解另一侧的凸最小二乘，两侧交替；每用户/物品的线性系统仅依赖其非零交互——天然分布式（分区按行/列）⚠️✅。
- **隐式反馈公式**（Hu–Koren–Volinsky 2008 ✅ DOI 过 Crossref 200：https://api.crossref.org/works/10.1109/ICDM.2008.26 ，论文 "Collaborative Filtering for Implicit Feedback Datasets", ICDM 2008）：偏好置信度 c_ui = 1 + α·r_ui（播放次数），目标 = 加权平方误差 + λ‖·‖² 正则；输出是"喜好强度序"而非预测评分 ⚠️。
- ALS 论文谱系（给 [../../db/db.md](../../db/db.md) 论文线挂点）：Koren BellKits 2009（Netflix 显式）、Distributed ALS (AWS Polder 等)——2e 用 MLlib `ALS.train`（RDD 版）实现 ⚠️。

## 3.3 MLlib ALS 实操路径（2e 口径）

1. RDD[(Int,Int,Float)] → `MatrixFactorizationModel`：`ALS.train(rdd, rank=k, iterations=n, lambda=λ)` ⚠️（2.x API；`spark.mllib` 包）。
2. 调参三面：rank（10~50 试）、λ（正则）、迭代数（收益递减即停）；用**留出用户 + precision@K** 评估而非 RMSE——隐式无"真分数" ⚠️。
3. 预测：`model.predict(user, topItemsK)` 或全量外积式打分；热门榜（count distinct users 排序）做**冷启动兜底** ⚠️。
4. 🔧 共现/热度类比（非 Spark）：DuckDB 自连接生成艺人共现对（`e1.uid=e2.uid AND e1.artist<e2.artist`）得单对 Muse–Radiohead n=1；热门榜 `count(DISTINCT uid)` 实测 Muse 2 / Radiohead 2 / KoL 1——"邻域法直觉 ↔ 矩阵分解"的教学对照，Spark 侧等价物即早期 ESim/共现基线 vs ALS。
5. 服务化叙事（书 2e）：模型存 HDFS，广播给在线打分进程；"评估-重训-发布"闭环=最小 MLOps 雏形 ⚠️。

## 3.4 工程要点与坑

- 用户/物品 ID 需**密集重映射**（0..n-1）：字典 RDD `zipWithIndex`——24 万×36 万条的映射表本身用 mapPartitions 批量 join 才不炸 ⚠️。
- ALS 每轮迭代全量 shuffle 因子向量：rank 每 +10，网络成本线性上涨；`persist(STORAGE_ONLY)` 交互 RDD 是硬要求 ⚠️。
- precision@K 实现：预测 top-K 与留出集求交——书中手写；现代用 `MulticlassMetrics`/ranking evaluator 或直接 MLlib `RankingMetrics`（3.x 起在 spark.ml）✅ mllib-evaluation-metrics。
- 可复现性：随机初始化因子用固定 seed；`sampleByKey` 切分测试集要 exact 模式 ⚠️。

## 3.5 与其他章/盘上笔记的接点

- 数据清洗纪律复用于 [05-K均值聚类网络异常检测.md](05-K均值聚类网络异常检测.md) 与 [06-潜在语义分析与维基百科.md](06-潜在语义分析与维基百科.md)。
- 矩阵分解的 Shuffle 成本机理 → [../bigdata/03-Shuffle与宽依赖.md](../bigdata/03-Shuffle与宽依赖.md)。
- 湖仓上的特征表/推荐日志现代落地 → [../Use_Iceberg_with_Spark/03-数据读写与MERGE-INTO.md](../Use_Iceberg_with_Spark/03-数据读写与MERGE-INTO.md)。

## 逐节精读扩展（重构笔记）

1. **XML→三元组的解析策略**（`ch03-recommender` 源码口径 ⚠️）：
   - profiledata 是"一个用户一大坨 RDF"结构，SAX（`XMLStreamReader`）逐元素流式，**绝不可** `DOMBuilder` 全进内存；
   - RDD 切分按"文件块 + 丢弃半条记录"再按用户 ID 二次 group——保证一条用户记录只落一个分区 ⚠️；
   - 解析器实例放 `mapPartitions` 局部 new：SAX 解析器不可序列化，这是本书序列化第一课（见 [02 章扩展 §3](02-用Scala和Spark进行数据分析.md)）。
2. **ALS 数学最小包**（书推导路径 ⚠️✅ HKV 原文 ✅ DOI 200）：
   - 目标 J = Σ_ui c_ui (p_ui − x_uᵀy_i)² + λ(Σ‖x_u‖² + Σ‖y_i‖²)，p_ui∈{0,1}；
   - 固定 y 时对 x_u 是 ridge：解 (YᵀC_uY + λI) x_u = Yᵀ C_u p_u；
   - (YᵀC_uY + λI) 是 rank×rank 小系统——**用户并行解自己的方程组**，这就是"ALS 天然并行"的全部秘密；
   - 稀疏技巧：YᵀC_uY = λI + Y_{u}ᵀY_{u} + diag 修正，只对该用户交互过的行做外积累加。
3. **调参地图**（书中经验值 ⚠️）：rank 10→20→50 网格、λ∈{0.01,0.1,1}、迭代 5~15 轮即收敛；α（置信斜率）常被拍脑袋设 40 倍中位播放数——书提醒用验证集反推。
4. **评估细节**：留出用户的全部交互为真值，top-K 命中率按用户宏平均——**热门霸榜的退化模型**在此指标下会被识破 ⚠️；precision@10 对稀疏标签敏感，书中同时报 recall@10。
5. **服务化流程（2019 版）**：训练产物 model.saveAsObjectFile(HDFS) → 在线进程 `SparkContext.objectFile` 加载 + `recommendFor` 本地打分 + 热门榜缓存——无特征库、无向量索引的最简闭环 ⚠️。
6. **冷启动三层答**（书立场 ⚠️）：新用户→热门兜底；新物品→内容特征外挂（本章未做，留概念）；新物品且需排序→退回到"共现邻域"（🔧 D8 实测的共现对即此基线的玩具）。
7. **🔧 数字复述（非 Spark）**：聚合面 D1（NULL 组 n=2/sum=5、FILTER 后 KoL 8）、共现面 D8（Muse–Radiohead=1、热度 Muse 2/Radiohead 2/KoL 1）——语义类比完整记录在 `D:\develops\tmp\dbwave_w4_spark\demo.py`。
8. **分布式 ALS vs 单机 ALS**：书附对比——单机 implicit 库同样优秀；上 Spark 的理由只有"用户/物品基数超单机内存"一条 ⚠️（诚实条款）。

## 本章自问自答

- **Q1：为什么隐式反馈不能直接当 5 分制回归？** A：播放≠喜爱（可能跳过），p=1/c 加权结构就是为此设计——显式 RMSE 会系统性高估高频项 ⚠️。
- **Q2：ALS 收敛到全局最优吗？** A：否，非凸交替只保证每步不增；多 seed 重启+验证集择优是工程解 ⚠️。
- **Q3：`spark.ml.ALS` 与书里 `mllib ALS` 差异？** A：DF 输入、`implicitPrefs`/`coldStartStrategy` 参数化、支持 transform 管道化 ✅（recommendation.ALS 页已验 200）。
- **Q4：top-K 暴力点积什么时候崩？** A：物品数×rank×广播内存——百万物品即需 ANN 索引（演进 3）。
- **Q5：评估要不要去重用户？** A：要按用户宏平均，否则重度用户主导指标 ⚠️。
- **Q6： Audioscrobbler 与 Last.fm 关系？** A：Audioscrobbler 是被 Last.fm 收购的 scrobble 服务，2005 快照即其导出 ⚠️。
- **Q7：矩阵分解现在还在工业一线吗？** A：召回层双塔（仍是分解思想）+ 精排深度模型；"分解已死"言过其实，但纯 ALS 独立扛推荐的时代确实结束 ⚠️。

## 书中写法 ↔ 现代写法速查（迁移表）

| 书中（2.x RDD 线） | 现代（spark.ml/3.x-4.x） | 状态 |
|---|---|---|
| `ALS.train(rdd, rank, iter, lambda)` | `ALS(rank=, maxIter=, regParam=).fit(df)` | ✅ recommendation.ALS（已验 200） |
| rating RDD (user,item,r) | DF + userCol/itemCol/ratingCol 参数 | 列名显式化 ✅ |
| 隐式 p=1/c 手加权 | `implicitPrefs=True` 内建 | 书公式=库默认 ⚠️ |
| 手写 top-K 广播打分 | `recommendForAllUsers(k)` | 内建 ✅ |
| 热门兜底手写 | `coldStartStrategy="drop"/"popularity"` | 书经验进库 ⚠️ |
| 手工 split+precision@K | `RankingMetrics`/评估器进管道 | ✅ mllib-evaluation-metrics |
| 因子向量导出 RDD | `transform` 出 DF embedding 列 | 下游接向量库（演进 3） |
| `saveAsObjectFile`(HDFS) | `model.write().overwrite().save()` | 序列化格式换代 ✅ |
| 每日全量重训 | 特征近线化+定期重训 ⚠️ | 工程惯例迭代 |

**复现备忘（教学路径）**：①MovieLens 25M（✅ 00 §7 方法验过）替 Audioscrobbler；②`pyspark.ml` 十行训练；③precision@10 用 pandas API 聚合即可，不再需要 Scala/SAX；④ALS 数学推导仍建议手推一遍（§3.2 即提纲）⚠️。

**易错点补录**：user/item ID 密集映射后必须固化字典版本——离线评估与线上服务 ID 空间错位是经典事故；字典本身也要版本化管理 ⚠️。

## 延伸阅读与落地检查单

1. 原论文路线：HKV2008（✅ DOI 已验）→ Hu 组后续 ALS 工程文 → Koreen-Bell-Koren 显式分解（⚠️ 题名登记）；论文线挂 [../../db/db.md](../../db/db.md)。
2. 库源码路线：`spark/ml/recommendation.py` 的 ALS 文档注释即现代参数表（✅ 00 §7 验法）；MLlib 实现对应 `ALS.scala` 的 YtY 缓存优化值得精读一遍 ⚠️。
3. 数据集替代：MovieLens 25M（✅ 已验）/ Last.fm 公开 1K 用户流（CC 协议，量小）/ Spotify 学术接口（已收紧 ⚠️）。
4. 上线前检查单：ID 字典版本冻结 □；隐式权重 α/λ 在验证集扫过 □；冷启动策略选定 □；top-K 服务延迟预算（ANN 或暴力）□；离线指标与在线曝光一致性回归 □。
5. 与盘上推荐谱系：本章讲"分解"，序列推荐/双塔等留白由演进节与向量库册补位 ⚠️。

## 核心概念速览（中英对照）

1. **协同过滤** — collaborative filtering：以群体行为相似性预测个体偏好。
2. **隐式反馈** — implicit feedback：播放/点击等信号，置信度非评分。
3. **矩阵分解** — matrix factorization：R ≈ U·Vᵀ 低秩近似。
4. **ALS** — alternating least squares：固定一侧解另一侧的交替凸求解。
5. **置信度** — confidence：c=1+α·r，隐式 ALS 的权重项。
6. **rank** — rank / k factors：因子维度，容量-成本主旋钮。
7. **λ 正则** — regularization λ：防过拟合，稀疏数据必调。
8. **precision@K** — precision at K：top-K 推荐命中率评估。
9. **冷启动** — cold start：新用户/物品退回热门或内容特征。
10. **留出集** — holdout：按用户抽样保留的测试交互。
11. **ID 重映射** — dense ID remapping：稀疏字符串键 → 0..n-1 整数。
12. **MatrixFactorizationModel** — MLlib 因子模型载体：userFactors/itemFactors。

## 最新演进与工业实践

1. **API 换代**：`spark.mllib`（RDD）自 Spark 2.0 进入维护，ALS 现代入口 = `spark.ml.ALS`（DataFrame、`implicitPrefs` 开关、`maxIter/regParam/family`）✅ https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.recommendation.ALS.html ；书 2e 的 RDD 写法仅在读旧码时有效。
2. **ALS 之外**：现代推荐主战场已移向深度模型（双塔/Two-Tower、DIN、生成式召回）与传统方法工程化共存；Spark 角色收敛为**特征工程 + 批量打分/重训** ⚠️。
3. **向量检索配套**：top-K ANN 服务（FAISS、Milvus、pgvector）承担在线侧——盘上对照 [../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md)（在盘 ✅）。
4. **评估升级**：离线 precision@K → 多目标（覆盖率/新颖性/去偏）+ 在线 A/B；MLlib 新增 `RankingMetrics`/`RegressionMetrics` 家族 ✅ mllib-guide。
5. **GPU/大规模 ALS**：Spark RAPIDS（NVIDIA）与 cuML 提供加速线 ⚠️；超大规模因子机多改用专用实现（example: Meta/LinkedIn 内部库）⚠️。
6. **数据时效**：Last.fm 2005 快照早已下线授权语境，教学可换 MovieLens 25M（✅ https://grouplens.org/datasets/movielens/ 本机 curl 200，2026-09 在架）。
7. **论文线**：除 ✅ 已验 DOI 的 HKV2008 外，Koren 2009 "Matrix Factorization Techniques for Recommender Systems"（IEEE Computer）与 Rendle 2012 "BPR"（UAI 2009）建议经 [../../db/db.md](../../db/db.md) 论文线补读（DOI 未逐一过 Crossref，标 ⚠️）。
8. **盘上分工**：推荐系统的**数据库侧**（特征存储、近线计算）超出本书，Iceberg+Flink 流式特征见 [../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)（在盘 ✅）。
