# 12 · 图数据科学与 GDS（Ch.12，章题为 ⚠️ 逆推重构，00 阅读地图口径）

> 取证锚点（✅ 实抓配套仓库 chapter12）：`cypher/commands.md` **全章语句可考**——从 `SET n:ExperimentOne` 打点、共享曲目计数、`CO_OCCURS` 物化（`IN TRANSACTIONS OF 10_000 ROWS`）、`gds.graph.project.estimate`/`gds.graph.project`、`gds.louvain.write.estimate`/`stream`、Community 节点落库（含唯一约束）、阈值 4 的 `CO_OCCURS_TWO`（500 行批）、Cypher projection 第三投影，到**书中实数**：`CommunityThree`  singleton 2246 / 总 4158（✅ commands 注释）；用户分段 `SET u.segment` 收尾。figures 8 张：12-1 workflow、12-2 community、12-3/4 co-occurrences、12-5 gds-internal、12-6 estimation、12-7 storage、12-8 behavioral-results。这是 GDS 2.x 工作流的**全程留痕章**。

## 12.1 GDS 工作流：图的“分析副本”范式（12-1 ✅）

GDS 的标准姿势（✅ commands 实证其每一步）：**投影（project）→ 算法（algorithms）→ 落库（mutate/write/stream）**。算法不在磁盘图上手搓，而是把 (节点, 边, 属性) 投影成内存图执行——Ch.5 的“图即遍历”与数据科学的“图即矩阵”之间放一座桥。本章把整座桥的每个铆钉都跑了一遍。

## 12.2 从查询可得与共现矩阵

```cypher
MATCH (n:Playlist) WHERE 20 <= n.total_tracks <= 25 SET n:ExperimentOne   // ✅ 打点：切片实验域
MATCH (p1:ExperimentOne)-[:HAS_TRACK]->(t:Track)<-[:HAS_TRACK]-(p2)       // ✅ 双遍历共现
WHERE p1 <> p2 RETURN p1.id, p2.id, count(*) AS sharedTracks
```

这就是 [./03-建模：从通用关系到语义关系.md](./03-建模：从通用关系到语义关系.md) 3.10 的代价模型现场：`ExperimentOne` 标签先裁集合（20–25 曲目的中型歌单），再算 sharedTracks——**先选择性后遍历**，Ch.5 SOP 的数据科学版。`WITH sharedTracks > 1` 过滤出 CO_OCCURS 边集，`weight` 属性即共现强度。

## 12.3 物化与批手术（✅ 两阈值实验）

- 第一刀：`MERGE (n)-[r:CO_OCCURS]-(other) SET r.weight=...`，`IN TRANSACTIONS OF 10_000 ROWS`（✅）；
- 第二刀：阈值升到 `>= 4`、批降到 500 行（`CO_OCCURS_TWO` ✅）——**边集变小、批也变小**：稀疏化后每行处理变重（内部双遍历更长），批大小跟着代价走 ⚠️（因果为重构解读）。

两次物化都保留 `weight` 且用无方向 MERGE——3.4“单边存储 + 无方向查询”立场的官方实践。投影时用 `orientation: 'UNDIRECTED', properties: 'weight'`（✅）声明给 Louvain 带权无向图。

## 12.4 估算先行：estimate 家族（12-6 ✅）

```cypher
CALL gds.graph.project.estimate('ExperimentOne', {CO_OCCURS: {orientation:'UNDIRECTED', properties:'weight'}})
YIELD requiredMemory, mapView, heapPercentageMin, heapPercentageMax
```

（拼写以 commands.md 原文为准 ✅；上行示意重构。）投影与算法都有 `.estimate` 变体（`gds.louvain.write.estimate` ✅）：**先问内存再动手**——12-6/12-7 两图讲投影内存账与堆内/外部存储取舍 ⚠️（图名逆推）。这与 Ch.9 的 heap/pagecache 世界观直接衔接：GDS 内存图吃的是 heap，pagecache 帮不了它。

## 12.5 Louvain 三模式与社区落库（✅ 全链）

`gds.louvain.stream` 出 (nodeId, communityId, intermediateCommunityIds)，随后**社区本身节点化**：

```cypher
MERGE (c:Community {id: communityId}) MERGE (c)-[:HAS_PLAYLIST]->(playlist)   // ✅
```

前置 `CREATE CONSTRAINT communityIdUnique FOR (n:Community) REQUIRE n.id IS UNIQUE`（✅）——Ch.2 纪律在算法产物上重演：**实体先约束后 MERGE**。Louvain 的 `intermediateCommunityIds` 保留层次（社区内嵌套社区）⚠️（语义转述），也是 Ch.13 选“某个社区 44386”做摘要对象的索引。

书中实数（✅ commands 注释）：第三投影 4158 个社区，其中 2246 个只含 1 个歌单——**54% 是孤点社区**。阈值收紧（>1 → >=4）后图变稀、社区碎化：共现阈值是社区质量的旋钮，也是 singleton 比例的开关。

🔧 概念类比（纯 python，非 Neo4j 行为）：`demo4_ch12.py` 在官方 gnr 6 行真数据上重放“共现→阈值→标签传播”链——4 种流派、6 个候选对、weight>1 仅 1 对、社区 1 个（size 2）；weight>=4 时**无边可投影**（✅ 运行输出）。玩具样本复现的正是 12.3/12.5 的方向感：阈值每收紧一档，图先稀疏后碎裂。

## 12.6 原生投影 vs Cypher 投影（✅ 两写法）

- `gds.graph.project('name', 'ExperimentOne', {CO_OCCURS: {...}})`：按标签/类型声明，快、可估算（12.4）；
- `gds.graph.project('...', source, target, {relationshipProperties: r{.weight}})` 包在 MATCH 里（✅ 原文形态）：任意查询图谱，灵活但把代价前移到投影查询本身，且 `r{.weight}` 投影图属性。

选型（⚠️ 重构）：规则切片用原生；“算法输入本身需要一条查询来定义”用 Cypher 投影——12.3 的 ExperimentOne 标签打点，其实就是**先把 Cypher 投影物化成标签**的中间路线。

## 12.7 行为侧出口：推荐与分段（✅ 两查询）

- 相似推荐：给定歌单 → 沿 `HAS_PLAYLIST` 找同社区兄弟 → `ORDER BY rand()` 抽样 5 条（✅）——社区是粗召回桶，随机是多样性阀；`ORDER BY rand()` 的采样式输出直接喂给了 Ch.13 的摘要管道（✅ 001-community-samples.cypher 同构）；
- 用户分段：`WITH u, collect(communityId)[0] AS topCommunity SET u.segment = topCommunity`（✅）——**图算法结果写回属性、服务查询**，mutate/write 模式的业务意义在这一句里齐全。

GD2e 07 章的图论菜单（[../Graph_Databases_2e/07-图论与预测分析.md](../Graph_Databases_2e/07-图论与预测分析.md)）在本章得到产品化对位：中心性/社区/路径家族 = `gds.*` 命名空间 ⚠️（谱系转述）。

## 12.8 判断力注记

本章的教学序列值得抄作业：**先用纯 Cypher 手搓共现（12.2/12.3），再上 GDS 投影（12.4–12.6）**。手搓阶段建立“算法=查询+物化策略”的祛魅，GDS 阶段只接管内存管理与并行——顺序反过来，读者会把 gds 当黑盒魔法。

## 12.9 GDS 算法选择卡（本章主场 + 家族地图 ⚠️ 家族面转述自 GDS 文档目录）

| 需求 | 本章用的 | 同族备选 | 备注 |
|---|---|---|---|
| 分组/话题发现 | Louvain（✅ stream/write 双用） | WCC（更粗）、Label Propagation | 层次留 intermediateIds |
| 相似度边 | 共现手搓（✅ 12.2/12.3） | `gds.nodeSimilarity`（kNN 版） | 03 章 SIMILAR 的官方化 |
| 重要性排序 | ——未用 | PageRank/Betweenness | GD2e 07 章理论对位 |
| 出圈推荐 | 社区桶 + rand()（✅） | `gds.knn`、triangleCount | Ch.13 用向量接管此格 |
| 路径 | ——本章未用 | shortestPath/Dijkstra family | 01/08 章的遍历侧 |

本章刻意只走“社区”一条纵线，把其余留作练习——**GDS 的入门正确姿势是单算法全程走通**（project→estimate→stream→write→节点化→应用），而不是十种算法各跑一个 hello world。

## 12.10 与写路径的合流（GDS 产物的生产化清单 ⚠️ 重构）

算法结果回到生产要过五关（每关都在前面章节立过案）：

1. 写回形态：`mutate`（内存图属性，临时）vs `write`（落盘，永久）vs `stream`（即席返回 ✅ 本章主用）——先定生命周期再选模式；
2. 落盘纪律：Community 节点走“约束+MERGE+分批”三件套（✅ 12.5 原文即样板，Ch.2 的定理在算法侧复述）；
3. 权限面：算法账号需要 WRITE 元素模式（Ch.6 6.2 的最小权限清单加上它）；
4. 观测面：投影驻留内存是 heap 指标（11.2）的新增嫌疑人，`gds.graph.list`/drop 的卫生习惯 ⚠️（过程名转述）；
5. 失效面：源图一动，投影即旧——重投影频率与业务写入频率对表（03 章“边即缓存”三问的最后一次回响）。

🔧 玩具实测补记（纯 python，非 Neo4j）：demo4_ch12.py 的标签传播 2 轮收敛、社区 1 个/孤点率 0——数据太小无方差，但这恰好演示了 12.5 的对照逻辑：**社区统计量（个数/孤点比）是阈值与数据规模的联合函数**，报结论必须同时报两者（书中 2246/4158 ✅ 即此规范的示范）。

## 12.11 主线位置：一条“派生结构”流水线

把全书的派生数据动作串成一条线看本章的坐标：

```
Ch.3 SIMILAR 边（手动物化） → Ch.8 RESOLVED_AS（解析物化）
→ Ch.12 CO_OCCURS + Community（算法物化） → Ch.13 summary/Question（语义物化）
```

四步同构：**计算产物以节点/边形态回到图中，享受与源数据同款的约束、权限、备份与失效治理**。这条线是本书区别于“算法教材”的立场句——图数据科学不是图的外挂分析层，是图自身的新陈代谢。🔧 demo4 与 GD2e 07 章（[../Graph_Databases_2e/07-图论与预测分析.md](../Graph_Databases_2e/07-图论与预测分析.md)）分别是这条线的最小可跑样本与理论前世。

## 核心概念速览（中英对照）

- **图投影** — Graph Projection：GDS 算法输入的内存图快照
- **stream/mutate/write** — 三运行模式：即席返回/写回属性/落库
- **社区发现** — Community Detection（Louvain）：模块率优化的分层聚类
- **共现边** — Co-occurrence Edge：双遍历计数物化出的带权关系
- **阈值工程** — Threshold Tuning：sharedTracks 界限决定图密度与社区碎度
- **估算** — `.estimate`：投影/写回前的内存与耗时预检 ✅
- **社区节点化** — Community as Node：算法产物升格为图实体（约束先行 ✅）
- **中间社区** — intermediateCommunityIds：Louvain 的层次结构输出 ⚠️
- **Cypher 投影** — Cypher Projection：以查询定义算法输入图 ✅
- **孤点社区** — Singleton Community：书测 2246/4158 ✅ 的碎化指标
- **用户分段** — User Segmentation：top 社区写回 `u.segment` 的应用出口 ✅

## 最新演进与工业实践

- **GDS 谱系**：Louvain/WCC/PageRank/nodeSimilarity 等算法家族在 GDS 2.x 持续扩版（https://neo4j.com/docs/graph-data-science/current/ 200 ✅，此前多章引用过）；新版本算法命名与参数面有漂移，本章 commands 的语句在 5.26 LTS + 配套 GDS 版本上成立 ⚠️（书用版本 ✅ README 5.26 LTS）。
- **GraphSAGE/嵌入线**：GDS 的 ML 侧（节点嵌入、特征管道）是本章“共现手搓”的算法化后继——本书 Ch.13 用外部 embedding 替代了图内嵌入，两条路线并行 ⚠️（趋势判断）。
- **混合推荐语境**：社区桶粗召回 + 向量精排的两级结构（12.7→Ch.13）与工业推荐系统 recall/rank 分层同构，对位可读兄弟册 `Vector_Databases`（已落盘，实链见 [./13-向量检索、LLM摘要与混合推荐.md](./13-向量检索、LLM摘要与混合推荐.md) 与其 [../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md)）。
- **论文线**：模块率/Louvain 原始文献与大规模图分区的学术追踪归 [../../db/db.md](../../db/db.md)（DOI 未在本目录逐一机检，不在此引用）。
- **对位阅读**：PageRank 与链接分析的图库视角在 [../Graph_Databases_2e/07-图论与预测分析.md](../Graph_Databases_2e/07-图论与预测分析.md)；本章是它“从算法描述到 estimate/project/write 流水线”的工程化对照。
