# 07 · 用 GraphX 分析伴生网络（Graph Analysis）

> 《Advanced Analytics with Spark, 2e》第 7 章精读重构 ｜ 总览见 [00-总览与阅读地图.md](00-总览与阅读地图.md) ｜ ✅ / ⚠️ / 🔧（DuckDB 1.5.5 类比，非 Spark 行为）

## 章定位

图分析案例：以 **MEDLINE 主题词（MeSH）共现网络**（"伴生网络"）为例讲 GraphX——两个主题词在同一批文献共同出现即连边，用图算法找"相关主题/相关文献"，服务推荐式检索。代码目录 `ch07-graph` ✅；数据 ✅ 仓库 README 指向 `ftp://ftp.nlm.nih.gov/nlmdata/sample/medline/`（**ftp 协议**，2026 年该入口可达性存疑 ⚠️——NLM 现主推 https://ftp.ncbi.nlm.nih.gov/pubmed/ 线性 XML，登记为复现缺口）。

## 7.1 属性图模型与 GraphX 数据结构

- GraphX 核心：`Graph[VD, ED]` = `VertexRDD[(VertexId, VD)]` + `EdgeRDD[ED]`（EdgeTriplet 视图），顶点和边都是 RDD——图=数据的特例而非新系统 ⚠️✅（https://spark.apache.org/docs/latest/graphx-programming-guide.html ）。
- 本章构图流水线 ⚠️：解析 MEDLINE 记录 → (文章, 主题词) 对 → 共现计数（pair RDD `reduceByKey`，见 [02-用Scala和Spark进行数据分析.md](02-用Scala和Spark进行数据分析.md) §2.3）→ 阈值剪枝 → 归一化权重（余弦/PMI）→ 边表。
- 顶点重编号：`EdgeRDD.fromEdges` + `connectedComponents` 拿分量代表后 `persistentVertices`/`join` 重映射，压缩 ID 空间——大图预处理惯例 ⚠️。
- 存储注意：GraphX 用 **`StorageLevel.MEMORY_AND_DISK`+ 序列化混合（Shippable）** 存切割边；routing 策略（EdgePartition2Dto/replicated 等）影响遍历性能 ⚠️✅（同上 guide#internal-graph-representation）。

## 7.2 本章用到的图算子

- **connectedComponents**（CKV/哈希最小传播）：把词网切成语义社区；书用它合并碎片主题 ⚠️。
- **labelPropagation**：软社区（权重驱动）；与 CC 对比讲解同构消息、不同聚合 ⚠️。
- **shortestPaths（landmark）**：少量地标源 BFS，度量词间语义距离 ⚠️。
- **triangleCount**：局部聚集系数输入；伴生网络高聚集=主题抱团 ✅ guide#trianglecount。
- **aggregateMessages**：手写"主题词代表度"（邻居权重和 TopN）——Pregel 原语教学习作 ⚠️。
- Pregel 心智模型：超步（superstep）内顶点收/发/改状态，同步 BSP；GraphX = 顶点视角 API（vs Pregelly 边视角已并入）⚠️✅。
- 🔧 三角计数 SQL 类比（非 Spark）：DuckDB 上 7 边小图（存为 a<b 的无向边表）跑 `edge e1 JOIN e2 ON e1.b=e2.a JOIN e3 ON e1.a=e3.a AND e2.b=e3.b` 枚举三角，按**最小顶点**归并实测：v1=2 个、v3=1 个（总三角数 3）；另测顶点 3 度数=4（两列相加）。GraphX `triangleCount` 返回"每个顶点参与的三角数"（v3 应为 3），本 SQL 只演示枚举原理，逐顶点对齐需三次对称改写——差异如实登记 ⚠️。

## 7.3 图算法的成本图景

- 每次全图迭代=一轮消息 shuffle：CC ~O(log n) 轮、LP 收敛慢易震荡（阻尼系数）⚠️。
- 幂律图的 skew：枢纽主题词（"Humans" 出现在百万文献）→ 超级顶点，消息爆炸；书中对策=共现权重 TopK 截断边，工业对策=子图采样/分桶 ⚠️。
- checkpoint 打断长血缘：迭代算法必做周期 `checkpoint`，否则 DAG 重放灾难 ⚠️→ [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)。
- 内存模型：边被复制到切割分区，边均摊 2-3 份——构图前估字节数是本书反复叮嘱的功课 ⚠️。

## 7.4 结果与解读

- 社区结构可视化：取分量大小分布幂律指数；Top 主题词的邻居表人肉评审（"cancer" 社区含 tumor/oncology）⚠️。
- 检索应用：给一篇文献的主题集，沿边一跳扩召回（伴生词查询扩展）——2e 的"图即特征"观点 ⚠️。

## 7.5 与其他章/盘上笔记的接点

- 图论与属性图理论、Pregel/BSP 史 → [../Graph_Databases_2e/00-总览与阅读地图.md](../Graph_Databases_2e/00-总览与阅读地图.md)（在盘 ✅，两谱系互读：数据库侧 vs RDD 侧）。
- 共现矩阵与[03 章](03-音乐推荐与Audioscrobbler数据集.md)、[06 章](06-潜在语义分析与维基百科.md)同族：都是"计数→加权→分解/传播"⚠️。
- Shuffle 机理 → [../bigdata/03-Shuffle与宽依赖.md](../bigdata/03-Shuffle与宽依赖.md)。

## 逐节精读扩展（重构笔记）

1. **MEDLINE/MeSH 语料结构**（本章数据底座 ⚠️✅ 老 ftp 入口存疑见 00 §9.4）：
   - 每条citation：PMID + 标题/摘要 + MeSH 描述词列表（人工标引，年更词表）；
   - "伴生"定义：两词同现一篇文献；共现计数即边权原料；
   - 书用样例集（nlmdata sample）而非全库——PowerPoint 级规模也能演示幂律 ⚠️。
2. **构图管线的 RDD 语法**（对位 [02 章 §2.3](02-用Scala和Spark进行数据分析.md) ⚠️）：
   - citation→(词对)：mapPartitions 内排序词 ID 后生成 (min,max) 规范对（防双向重复边）；
   - `reduceByKey` 计数 → 阈值剪枝（共现≥2）→ 权重 w=共现/√(f₁f₂)（余弦式归一）；
   - `Graph.fromEdgeTuples(edges, defaultVertexAttr)` 一步建图。
3. **connectedComponents 的输出语义**：返回 `Graph[Long, ED]`——顶点属性=所属分量最小 ID；书用它聚"主题族"，再 `vertices.countByKey` 拿社区规模分布（幂律指数目测）⚠️✅ guide#connectedcomponents。
4. **labelPropagation 实操**：源点权重 1、其余 0，迭代阻尼 `α·自身+(1−α)·Σw·邻居`；alpha 0.85~0.9 之间震荡收敛——与 PageRank 的直觉互译 ⚠️。
5. **triangleCount 的用途链**：局部聚集系数 = triangles/可能三角数 → 找"抱团主题核"；本章用它给词网分"核心-边缘"⚠️✅ guide#trianglecount。
6. **Pregel 手写练习**（本章保留节目 ⚠️）："邻居最大属性传播"= 两行 `sendMessages + mergeMsg` 的范例——Pregel API 的最小教学模型；书警告：能不调 Pregel 就不调（内置算子有专门优化）✅ 同 guide。
7. **持久化档位实操** ⚠️：构图后 `graph.cache()` 默认（顶点 MEMORY_ONLY、切割边 MEMORY_AND_DISK_SER_2 口径 ✅ guide 内部表示节）；大图的 2~3 倍边复制是分区数规划起点。
8. **超级顶点治理清单**（书+现代 ⚠️）：TopK 边截断（本章）、节点度上限采样、"枢纽词"黑名单（Humans 类）、按度重分区（GraphFrames 前夜方案）——四招各有语义损失，选择即立场。
9. **结果解释的医学向**：书的示例对（"AIDS Research ↔ Acquired Immunodeficiency Syndrome" 分量内聚）展示"词族发现"对文献检索扩展的价值 ⚠️ 转述。

## 本章自问自答

- **Q1：GraphX 与图库（Neo4j）到底差在哪？** A：批式迭代算法+RDD 血缘 vs 交互查询+索引遍历；盘上两谱系对照见 [../Graph_Databases_2e/00-总览与阅读地图.md](../Graph_Databases_2e/00-总览与阅读地图.md)。
- **Q2：为什么不用 GraphFrames？** A：2019 书写作期 GFrames 算法少、文档糙；2026 年新项目默认 GF——本章读作"图算法 Spark 化原理课" ⚠️（graphframes.io ✅ 已验）。
- **Q3：CC 和 LP 结果能对上吗？** A：LP 软标签≈CC 骨架+权重渗透；分歧处恰是"跨族主题桥"——信息量所在 ⚠️。
- **Q4：有向吗？** A：共现网天然无向；若上引文网则入度/幂律更陡，CC 退化为弱连通——换数据时先重想语义 ⚠️。
- **Q5：图算法需要 checkpoint 吗？** A：≥20 轮迭代必做（血缘重放成本 O(轮²)）→ [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)。
- **Q6：本章和 03 章的"共现"是一回事吗？** A：同一原料两种去向：03 章低秩分解、07 章图传播——"计数矩阵→结构"的孪生示范 ⚠️。

## 书中写法 ↔ 现代写法速查（迁移表）

| 书中（GraphX） | 现代 | 状态 |
|---|---|---|
| `Graph(edges, vertices)` | GraphFrames `GraphFrame(edgesDF, verticesDF)` | ✅ graphframes.io（已验 200） |
| `connectedComponents.run(g)` | GF `connectedComponents` / Pregel 手写 | API 迁移 ⚠️ |
| `labelPropagation` | GF 无同名内建（Pregel 表达） | 反向迁移 ⚠️ |
| `triangleCount` | GF 内建同名 | ✅ |
| `graph.pregel(...)` | GF `pregl` 系闭包（列式 API） | 心智相同 ⚠️ |
| `aggregateMessages` | GF `aggregateMessages`（DataFrame 版） | 换皮 ✅ |
| `graph.cache()` | GF 走 DF 缓存语义 | 兼容 ⚠️ |
| RDD 手写共现建边 | SQL `GROUP BY a,b` + 剪枝 | DF 更短 ✅ |
| GraphX 全家桶 | 交互查询让位图库（Neo4j 谱系） | 分工固化 ⚠️ |

**五算子复习卡**（一句话版 ⚠️）：CC=最小 ID 全局投票；LP=阻尼邻居加权和；三角=三元组枚举逐点计数；shortestPaths=多源 BFS 打包；Pregel=顶点程序×消息×聚合三件套。

**构图参数备忘**（书实测口径转述 ⚠️）：共现阈值=2、边权=余弦式归一、每词 TopK 截边≈20——三个数字决定图密度与算法成本；先小样本调密度、再全量跑，是本章工程纪律。

## 延伸阅读与落地检查单

1. 论文线：Pregel(OSDI'10)/GraphLab(UAI'10)/GraphX(SIGMOD'14 系) ⚠️ 题名+会议+年份登记（DOI 未逐一 Crossref）；挂 [../../db/db.md](../../db/db.md)。
2. 语料线：MeSH 年度词表公开（NLM 官网，⚠️ 入口换代见演进 5）；社交/引文网络可作同法替身数据。
3. 实现线：GraphFrames 三角/CC 对照重写本章（✅ graphframes.io 已验）；Neo4j 侧同图入库对比查询型 vs 计算型差异（盘上 [../Graph_Databases_2e/00-总览与阅读地图.md](../Graph_Databases_2e/00-总览与阅读地图.md)）。
4. 上线前检查单：边方向语义评审（共现=无向规范对）□；阈值/TopK 截边的召回损失量化 □；超级顶点处置策略选定 □；迭代轮数与 checkpoint 节奏压测 □；社区结果抽样人审 □。
5. 教学提醒：本章所有"图=两张 RDD"的心智，到 GraphFrames 变成"图=两张 DF"——只换载体不换代数 ⚠️。

## 核心概念速览（中英对照）

1. **属性图** — property graph：顶点/边携类型化属性的图模型。
2. **GraphX** — GraphX：Spark 图组件，Graph[VD,ED]=两 RDD+操作。
3. **EdgeTriplet** — edge triplet：srcId/dstId/属性+两端点属性的视图。
4. **Pregel** — Pregel：顶点程序×消息×聚合的同步迭代框架。
5. **BSP/超步** — bulk synchronous processing：全局屏障式迭代轮。
6. **连通分量** — connected components：CKV 哈希传播划社区。
7. **标签传播** — label propagation：加权邻居投票的软社区。
8. **三角计数** — triangle count：局部聚集性原子指标。
9. **共现边** — co-occurrence edge：伴生网络构边规则。
10. **PMI** — pointwise mutual information：共现归一化权重。
11. **超级顶点** — supernode：幂律枢纽导致的消息热点。
12. **Shippable 存储级** — MEMORY_AND_DISK_SER_2：GraphX 切割边序列化档位。

## 最新演进与工业实践

1. **GraphX 进入维护态**：官方 guide 仍存在 ✅（graphx-programming-guide.html，2026-09 本机 200），但新特性冻结；社区替代 = **GraphFrames**（DataFrame 图，图算法+motif finding+连接预测），官方文档站 ✅ https://graphframes.io/ （本机 curl 200；书时代 graphframes.github.io 路径已 301/404，勘误登记 ⚠️）。
2. **GNN 时代**：本章手工社区发现 → 图神经网络（DGL/PyG）做表征学习；Spark 侧集成多为 `Spark + DGL on GPU` 项目而非内核 ⚠️。
3. **Neo4j/属性图数据库分工固化**：交互查询+ACID 归图库，批量迭代算法归 Spark/GraphFrames——与盘上 [../Neo4j_The_Definitive_Guide/00-总览与阅读地图.md](../Neo4j_The_Definitive_Guide/00-总览与阅读地图.md)（在盘 ✅）互补读。
4. **CDC/实时图**：知识图谱增量构建走"流式+湖仓"（Flink + Paimon 图化建模），与本章批式全量重算形成两代架构：[../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)。
5. **数据入口换代**：MEDLINE ftp 样本目录被 PMC OA / PubMed 线性 XML 取代 ⚠️；MeSH 词表本身改为年度发布，共现语料应按快照年对齐 ⚠️。
6. **论文线**：Malewicz et al. Pregel (OSDI 2010)、Low et al. GraphLab (UAI 2010)、Xin et al. "GraphX" (SIGGRAPH 2014) ✅ OSDI'10 DOI 10.5555/1855511.1855514 ⚠️ 未逐一 Crossref（ACM DL 存款线复杂），仅标题+会议+年份登记；挂 [../../db/db.md](../../db/db.md)。
7. **ANN×图**：HNSW 本身即"图导航结构"——本章的邻域消息传递与 [../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md) 的 ANN 图索引在算法层面同源 ⚠️。
