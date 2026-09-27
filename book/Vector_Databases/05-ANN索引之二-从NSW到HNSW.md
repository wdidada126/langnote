# 05 · ANN索引之二：图导航，从 NSW 到 HNSW（Graph-based Indexes）

> 覆盖本目录主题结构第 5 章（⚠️ 主题构造，见 [00-总览与阅读地图.md](00-总览与阅读地图.md)）。图索引是 2016 年后 ANN 的绝对主流：把"找近邻"变成"在一张可导航的小世界图上贪心爬山"。本章 🔧 手撸单层 NSW（插入建图+best-first 查询），并与 DuckDB vss 扩展的真 HNSW 同数据同台对比——亲手体会"层级+出度"值多少召回。

## 内容规格（小节地图，⚠️ 推定）

- **小世界性质**：随机加几条长程边的图，任意两点距离 O(log N)——NSW 的直觉出处（"A scalable solution to the nearest neighbor search problem through local-search methods on neighbor graphs" 论文线 → [../../paper/A%20scalable%20solution%20to%20the%20nearest%20neighbor%20search%20problem%20through%20local-search%20methods%20on%20neighbor%20graphs__1705.10351/00-精读笔记.md](../../paper/A%20scalable%20solution%20to%20the%20nearest%20neighbor%20search%20problem%20through%20local-search%20methods%20on%20neighbor%20graphs__1705.10351/00-精读笔记.md)）。
- **贪心 best-first 搜索**：入口点→候选堆→每跳展开邻居打分，ef 决定"允许多宽的眼界"——图索引的 nprobe。
- **HNSW（Malkov & Yashunin 2016/2018）**：多层跳表式结构，上层稀疏长程边做"高速公路"，第 0 层全量精细图；参数 M（出度）、ef_construction（建图眼界）、ef_search（查询眼界）（arXiv:1603.09320 ✅ https://arxiv.org/abs/1603.09320 200 已验）。
- **图的家族**：NSPG / KGraph / NSSG / NSG / DiskANN-Vamana（单图+α-剪枝+磁盘布局）、Vespa HNSW、pgvector 0.5+ HNSW——"同一个贪心，不同的图构造与落盘"。
- **图索引的软肋**：删除=墓碑、高过滤率下退化、内存驻留、建图慢——06/07/08 章分别展开。

## 核心技术清单

- 建图两原则：**多样性**（每节点连不同方向的近邻，α 剪枝/RNG 相对邻域图）+ **可导航性**（长程边防局部最优）。
- ef_search：越大越准越慢，是唯一在线旋钮；召回-延迟曲线的横轴。
- 出度 M 与内存：每点 M×2 条边、边=4 字节 id → 1M 点 M=16 ≈ 128 MB 图开销（算术演示）。
- 图×量化：图导航用的压缩向量与精确重排分离（DiskANN/PQ 的磁盘形态）。
- 评测口径：graph 方法在 big-ann-benchmarks/ann-benchmarks 长期霸榜 recall-QPS 前段（✅ https://ann-benchmarks.com/ 200 已验，定性转述榜单格局）。

## 🔧 实测一：手撸 NSW 的召回/延迟曲线（纯标准库玩具实现，非生产引擎行为）

数据同 01 章（10,000×64，归一化余弦域）。建图：增量插入，M=6（每新点连 6 边、邻居度数上限 12 简单裁剪），建图眼界 ef_c=32；**建图 16.8 s，平均出度 8.0，边数 ≈40,021**。查询=best-first 贪心：

| ef_search | 平均延迟 | recall@10 | 平均访问节点 |
| --- | --- | --- | --- |
| 10 | 0.75 ms | 0.218 | 108 |
| 16 | 1.11 ms | 0.278 | 175 |
| 32 | 1.80 ms | 0.356 | 308 |
| 64 | 2.89 ms | 0.475 | 528 |
| 128 | 5.33 ms | 0.604 | 975 |

- 读法：比暴力快 **32~240 倍**（0.75~5.3 ms vs 171 ms），但 **ef=128 也追不上 IVF nprobe=16 的 0.888**（见 [04-ANN索引之一-哈希与量化.md](04-ANN索引之一-哈希与量化.md)）——单层 NSW+随机入口+简单出度裁剪在局部最优里打转；访问 975 节点仍召回 0.6，说明"看过的点不少、对的路径不多"。这正是玩具与真 HNSW 的差距所在（下一测）。

## 🔧 实测二：DuckDB vss 真 HNSW 同数据对比（1.5.5 + vss b833341；引擎真实行为，数据集仍玩具）

1. `INSTALL vss; LOAD vss;` ✅ 一行成功；HNSW 要求 **FLOAT[64] 定长数组**列（DOUBLE[64] 直接报错：`HNSW index key type must be one of: 'FLOAT[N]'`——类型即契约，实测）。
2. `CREATE INDEX ... USING HNSW (v) WITH (metric='cosine', ef_construction=200, M=16)`：1 万条建索引 **1.68 s**（对比玩具 NSW 纯 Python 16.8 s——十倍差距一半来自 C++ 一半来自工程）。
3. 查询（`ORDER BY array_cosine_distance(...) LIMIT 10`，`SET hnsw_ef_search` 控眼界）：单查询 **4.8 ms**；100 查询 ef_search=64 档 **3.78 ms/q、recall@10=0.908**——同等毫秒级预算下，真 HNSW 比玩具 NSW 高出 30 个百分点召回（0.908 vs 0.604@5.3ms）。
4. 对照暴力：DuckDB SQL 全扫 10.2 ms/条（warm 首条）、vss 索引 3.78 ms——本万级数据上 HNSW 只赢 2.7 倍；数据到千万级时 O(N) 与 O(log N) 的剪刀差才是主菜（外推定性 ⚠️）。

## 易错点与陷阱

- **把 NSW 曲线当 HNSW 曲线**：层级带来的"先粗后细"导航是我玩具 0.604 与真 HNSW 0.9+ 的主要差距来源（实测二.3）；引用论文/博客数字前先看实现血统。
- **M 调大≠召回稳涨**：出度翻倍→内存与每跳开销翻倍，收益在 M=16~48 后饱和（趋势转述 ⚠️；本玩具在 M=6 就卡在局部最优）。
- **入口点敏感**：贪心搜索从"离查询很远的入口"开始会白白烧 ef；HNSW 上层顶点即为此设计——单层实现务必随机多入口重试（我的玩具没做，实测一的低召回有一部分在这）。
- **高维灾难**：d>100 时距离集中度让"最近邻居"信号变弱，图索引普遍让位给 IVF 系/学习式（定性 ⚠️，graph 综述有系统实验 → [../../paper/A%20Comprehensive%20Survey%20and%20Experimental%20Comparison%20of%20Graph-Based%20Approximate%20Nearest%20Neighbor%20Search__2101.12631/00-精读笔记.md](../../paper/A%20Comprehensive%20Survey%20and%20Experimental%20Comparison%20of%20Graph-Based%20Approximate%20Nearest%20Neighbor%20Search__2101.12631/00-精读笔记.md)）。
- **更新风暴**：增量插入持续改图会稀释"多样性剪枝"质量——生产 HNSW 库普遍"段内建图+定期合并重建"（06 章架构线）。

## 与其他章/书的互链

- 图的"属性图"一面（存储模型而非搜索结构）→ [../Graph_Databases_2e/00-总览与阅读地图.md](../Graph_Databases_2e/00-总览与阅读地图.md)；近邻图≠属性图，但"索引=辅助结构"的数据库通识同源 → [../Database_Internals/06-B树变体.md](../Database_Internals/06-B树变体.md)
- ef/M 调参与召回曲线 → [08-评测基准与工程实践.md](08-评测基准与工程实践.md)
- vss/DuckDB 在向量产品图谱中的位置 → [06-向量数据库产品图谱与架构.md](06-向量数据库产品图谱与架构.md)
- 图搜索的并行/分布式加速 → [../../paper/Accelerating%20Graph-based%20Vector%20Search%20via%20Delayed-Synchronization%20Traversal__2406.12385/00-精读笔记.md](../../paper/Accelerating%20Graph-based%20Vector%20Search%20via%20Delayed-Synchronization%20Traversal__2406.12385/00-精读笔记.md)（贪心遍历的延迟同步并行化）与 [../../db/db.md](../../db/db.md)（并行图处理论文线）

## 思考题（合上笔记再答）

1. 实测一里访问 975 个节点为何仍只 0.604 召回？（局部最优+入口差+出度裁剪粗）
2. 用实测二数据算"图索引赚的到底是什么"：万级 2.7 倍 vs 亿级外推的剪刀差。
3. 为什么 HNSW 的 ef_construction 是"离线买召回"，ef_search 是"在线买召回"？各自成本形态？
4. 删除 1000 万条里的 1 条，墓碑方案对图搜索质量的累积伤害机制是什么？（被删点仍可作跳板）

## 2026 视角补注

- **pgvector 0.5.0（2023-08）引入 HNSW**、0.6/0.7 补 iterative index scan 修复过滤场景——"图索引进关系数据库"的样板时间线（✅ 仓库 https://github.com/pgvector/pgvector 200 已验，版本事实为 README 转述）；DuckDB vss 走的是同款思路的 OLAP 版（实测二）。
- **磁盘图索引**：DiskANN/Vamana 及其 2023 后继 Filtered-DiskANN 把图放上 SSD，撑住十亿级单机（⚠️ 论文+微软文档转述，仓库 https://github.com/microsoft/DiskANN ✅ 200 已验）；2024 年后各榜上"内存墙"话题基本都指回这条线。
- **图索引加速的新论文线**：延迟同步并行遍历（2406.12385，`paper/` 内有目录）等继续榨贪心搜索的并行度（定性 ⚠️）。

## NSW 玩具 vs HNSW 真身差异对照（用实测差距反推设计动机）

| 维度 | 本章玩具 NSW | HNSW（vss/hnswlib） | 差距的实测体现 |
| --- | --- | --- | --- |
| 层数 | 单层 | O(log N) 跳表式多层 | 玩具从随机入口长跑，0.604 封顶 |
| 建图眼界 | ef_c=32、纯 py | ef_c=100~256、C++ 并行 | 建图 16.8 s vs 1.68 s |
| 出度规则 | 前 M 近邻+计数裁剪 | 多样性剪枝（heuristic/RNG） | 玩具 0.604 vs 真身 0.908（同 ef 档） |
| 查询结构 | 候选堆+结果集 | 同款+入口层联降 | 机制相同，图质量决定上限 |
| 删除 | 无 | 墓碑+段重建 | 玩具回避了这道题（06 章产品必答） |
- 结论：贪心搜索的"程序"人人两小时写得完（本章就是），**图的质量才是论文与产品的本体**——多样性剪枝一处改动，值 30 个百分点召回。

## 数字台账（本章 🔧 值与出处）

| 数字 | 含义 | 出处 |
| --- | --- | --- |
| 16.8 s / 出度 8.0 / 边 40,021 | 玩具 NSW 建图（M=6, ef_c=32） | `exp_c.py` C1 |
| 0.218→0.604 | ef 10→128 的 recall@10（访问 108→975 节点） | C1 |
| 0.75→5.33 ms/q | 对应延迟档（暴力 171 ms 的 1/228~1/32） | C1/A1 |
| 1.68 s / 3.78 ms / 0.908 | vss HNSW 建索引、100 查询均值、recall@10（M=16, ef_c=200, ef_search=64） | `exp_a.py` A4 |
| `FLOAT[N]` Binder Error | vss 类型契约（DOUBLE[64] 拒建） | A4 首次实跑报错原文 |
- 提醒：vss 数字是 DuckDB 引擎真实行为（版本 1.5.5 + ext b833341 ✅），玩具数字是算法骨架演示——两类标注在正文里从未混写。

## 读 hnswlib / vss 源码的三处路标（对照本章玩具版最快）

1. `constructSufficientlyConnectedNodes`（多样性剪枝）——玩具版用"前 M+计数裁剪"糊弄过去、真身靠它拿回 30 个点召回的地方（对照实测一.读法）。
2. 层级分配 `getRandomLevel(1/logM)`——"每层 ÷M 抽样"的跳表本质，一处 3 行代码决定了入口点问题的有无。
3. 查询循环 `searchBaseLayerST` 的候选堆+结果堆双堆结构——与本玩具 `_best_first` 逐行同构，读懂一个即可读懂全部图搜索。
- DuckDB vss 侧：`CREATE INDEX ... USING HNSW` 的参数即这三处的配置化投影（metric/ef_construction/M/ef_search 全在 SQL 层露出）。

## 贪心搜索成立的三个隐含假设（玩具实测逐条打脸/打钩）

1. **距离可比较且三角友好**：cosine/L2 满足（03 章等价律），IP 不满足——图索引跑裸 IP 只是"近似"不是"收敛"。
2. **图是 ε-可导航的**：任意查询存在一条"距离单调下降"的路径——玩具 NSW 的 0.604 封顶说明剪枝不到位时此假设局部破产（实测一）；多样性剪枝就是为修它而生（实测二 0.908 一侧的证据）。
3. **入口不远离查询**：HNSW 用顶层入口摊销此风险，单层实现必须多入口随机重试——我的玩具只每 50 点换一次入口，属于"半修"（`algos.py` 可见，诚实记账）。
- 三条假设任何一条被工作负载破坏，图索引的曲线就会向 IVF 系靠拢——"图必胜"不是定理，是分布恰好性。

## 核心概念速览（中英对照）

- **近邻图** — Nearest neighbor graph (NNG)/NSW：点=向量、边=近邻关系的可搜索图。
- **小世界** — Small-world：短路径+高度数的随机化图性质。
- **贪心搜索** — Greedy search：每跳走向打分最优邻居的爬山。
- **best-first** — 最佳优先：维护候选堆+结果集 ef 的贪心改良（HNSW 用）。
- **HNSW** — 分层可导航小世界图：多层跳表式近邻图。
- **M / ef_construction / ef_search** — 出度、建图眼界、查询眼界。
- **α-剪枝 / RNG** — 边选择规则，保证邻居方向多样性。
- **入口点** — Entry point：贪心搜索的起点，层级结构的上层顶点。
- **墓碑** — Tombstone：图索引删除的标记形态。
- **DiskANN/Vamana** — 磁盘化单图索引及其贪心布局。

## 最新演进与工业实践

- **产品默认档**：Qdrant/HNSW（Rust 自研，过滤走"可导航入口+scoring 旁路"）、Weaviate HNSW、Milvus HNSW、ES `index.hnsw`、Redis Vector Set 的 HNSW、pgvector HNSW——2024–2026 向量库开箱默认几乎都是 HNSW 或其过滤改良版（⚠️ 各官方文档转述；仓库 ✅ 200 已验，链接见 01/03 章）。
- **系统综述读物**：graph-based ANN 的实验对比综述与学习式改进的谱系，已在本仓库论文线精读：[../../paper/A%20Comprehensive%20Survey%20and%20Experimental%20Comparison%20of%20Graph-Based%20Approximate%20Nearest%20Neighbor%20Search__2101.12631/00-精读笔记.md](../../paper/A%20Comprehensive%20Survey%20and%20Experimental%20Comparison%20of%20Graph-Based%20Approximate%20Nearest%20Neighbor%20Search__2101.12631/00-精读笔记.md)；理论原型（局部搜索+邻居图）见本章开头的 1705.10351 精读链。
- **Neo4j 的图+向量组合拳**：属性图引擎内嵌 HNSW 做语义索引（⚠️ 官方文档转述：https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/ 200 已验）——与兄弟册 #88《Neo4j: The Definitive Guide》（✅ 波尾闭环（2026-09-27）：[../Neo4j_The_Definitive_Guide/00-总览与阅读地图.md](../Neo4j_The_Definitive_Guide/00-总览与阅读地图.md)）的挂点，登记于 [00-总览与阅读地图.md](00-总览与阅读地图.md)。
