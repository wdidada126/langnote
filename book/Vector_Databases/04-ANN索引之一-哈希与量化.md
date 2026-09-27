# 04 · ANN索引之一：哈希与量化（LSH / PQ / IVF）

> 覆盖本目录主题结构第 4 章（⚠️ 主题构造，见 [00-总览与阅读地图.md](00-总览与阅读地图.md)）。"少算点"的两大古老流派：LSH 用随机哈希把"大概率同桶"当相似性代理；量化/倒排聚类（PQ、IVF、IVFADC）先把空间压扁再扫描。本章 🔧 三件套全部纯标准库复现，并给出各自的召回/延迟曲线。

## 内容规格（小节地图，⚠️ 推定）

- **LSH（Locality Sensitive Hashing）**：随机超平面签名（cosine 域）、多表多桶（L 表 × k bit）、"同桶≈近邻"的概率保证；理论线 Indyk–Motwani 1998（⚠️ 经典出处，标题+会议+年份，未过 DOI 链）。
- **乘积量化 PQ**：d 维切成 m 段、每段 k-means 码本；向量→m 字节码；ADC（非对称距离计算）用查找表把精确距离压成查表求和——Jégou et al. 2011 "Product Quantization for Nearest Neighbor Search"（TPAMI；arXiv:1111.0375 ✅ https://arxiv.org/abs/1111.0375 200 已验）。
- **IVF 粗量化**：全库 k-means 成 nlist 个 Voronoi 胞，查询只扫 nprobe 个倒排队列——"分区剪枝"；IVFADC=IVF+PQ 联合（FAISS 的招牌形态）。
- **两阶段/重排**：近似打分取粗候选 → 原始向量（或缓存）精确重排，nrec 决定精度上限。
- **理论视角**：分布式 ANN 的参数化统一（Kersten/Lemire 一系，本仓库已精读）→ [../../paper/A%20Parametrizable%20Algorithm%20for%20Distributed%20Approximate%20Similarity%20Search%20with%20Arbitrary%20Distances__2405.13795/00-精读笔记.md](../../paper/A%20Parametrizable%20Algorithm%20for%20Distributed%20Approximate%20Similarity%20Search%20with%20Arbitrary%20Distances__2405.13795/00-精读笔记.md)。

## 核心技术清单

- LSH 参数：k（签名位数，桶更细/候选更少）、L（表数，覆盖更多碰撞机会）；查询成本≈候选集大小。
- PQ 参数：m（子空间数）、nbits（每段码本 2^nbits 质心）、nrec（重排池）。
- IVF 参数：nlist（胞数，训练样本量要 ≥30×nlist 的经验法则）、nprobe。
- 量化码=可流式传输的"压缩向量"，磁盘/网络按字节计费时的货币（DiskANN/ES bq 的公共底座）。
- 汉明距离服务 LSH 签名比较（03 章度量谱系的落点）。

## 🔧 实测：三条曲线（10,000×64 玩具数据集；纯标准库，玩具实现，非生产引擎行为）

数据同 01 章；recall@10 对 DuckDB 暴力真值；脚本 `exp_b.py`。

**LSH（随机超平面，cosine）**：
| 配置 | 建索引 | 查询 | 平均候选 | recall@10 |
| --- | --- | --- | --- | --- |
| k=8,L=12（全表） | 1.8 s | 44.1 ms | 9,946 | 0.997 |
| k=8,L=24 | 7.2 s | 53.9 ms | 10,000 | 1.000 |
| k=10,L=24, Lq=4 | 10.3 s | 34.1 ms | 5,278 | 0.811 |
| k=10,L=24, Lq=8 | — | 47.8 ms | 9,540 | 0.972 |
| k=10,L=24, Lq=16 | — | 51.8 ms | 9,929 | 1.000 |

- 读法：本数据集簇间区分度低，**候选集动辄数千→LSH 退化成带税的暴力**（44 ms 还没跑赢 LSH 自己的理论优势）——L/k 调不好时"哈希加速"是幻觉；Lq 从 24 砍到 4 买到 1.5 倍速度、丢掉 19 个点召回（速度换召回的第一现场）。

**PQ（m=8 段×16 质心=4bit）+ 精确重排**：
| nrec 重排池 | 查询 | recall@10 |
| --- | --- | --- |
| 10 | 29.2 ms | 0.182 |
| 32 | 30.6 ms | 0.273 |
| 64 | 29.6 ms | 0.360 |
| 200 | 26.1 ms | 0.537 |

- 读法：4bit 小码本+余弦域错配（PQ 原生 L2 语义）→**即使 10k 库里取 200 候选重排，召回也只有 0.537**；对照真实系统：FAISS 默认 nbits=8、m 常取 d/2~d/8，OPQ 先旋转再量化，把这条曲线整体抬高（⚠️ FAISS wiki 转述，仓库 ✅ https://github.com/facebookresearch/faiss 200 已验）。玩具结论方向不变：**PQ 的召回天花板=粗排保真度×重排池大小**。

**IVF（nlist=32）**：建索引 2.3 s（kmeans 训练样本 1500）；簇大小 1~526 不均。
| nprobe | 查询 | 平均候选 | recall@10 |
| --- | --- | --- | --- |
| 1 | 2.19 ms | 464 | 0.181 |
| 4 | 8.87 ms | 1,332 | 0.453 |
| 8 | 16.43 ms | 2,743 | 0.664 |
| 16 | 34.16 ms | 5,506 | 0.888 |

- 读法：nprobe 近似线性换召回，**nprobe=1 时 464 候选里只中 1.8 个真前 10**——"查询落在胞边界"的经典失败模式；簇不均（1 vs 526）进一步放大方差，真实系统的做法是分裂平衡/多副本倒排（⚠️ Milvus 文档转述）。

## 易错点与陷阱

- **LSH 的 k/L 不是越大越好**：k 大桶净但同桶概率暴跌（要更多 L 补）；L 大建索引内存与签名计算线性涨——实测表 1 两列全爆就是反例。
- **PQ 用余弦忘归一化**：码本按 L2 训、查询却想要角度序——先全体归一化（本玩具做了）再考虑截断误差。
- **IVF 训练分布≠全库分布**：只拿头部 1% 数据训练质心→边界胞全错；且插入后质心漂移要重训（nlist 大时 FAISS 用残差编码缓解 ⚠️ 转述）。
- **忘了重排这一步**：nrec≈k 时 PQ 召回=粗排命中率（实测 0.182 档）——"上了量化就要配重排池"是工程默认。
- **把倒排聚类当过滤**：nprobe 语义是"访问最近的胞"，与元数据过滤正交（07 章的组合爆炸来源）。

## 与其他章/书的互链

- 本目录图索引对照实验 → [05-ANN索引之二-从NSW到HNSW.md](05-ANN索引之二-从NSW到HNSW.md)；全家族同场竞技 → [08-评测基准与工程实践.md](08-评测基准与工程实践.md)
- 哈希算法的理论回顾 → [../../paper/A%20Revisit%20of%20Hashing%20Algorithms%20for%20Approximate%20Nearest%20Neighbor%20Search__1612.07545/00-精读笔记.md](../../paper/A%20Revisit%20of%20Hashing%20Algorithms%20for%20Approximate%20Nearest%20Neighbor%20Search__1612.07545/00-精读笔记.md)；整数签名上的相似检索（Sketch Trie）→ [../../paper/$b$-Bit%20Sketch%20Trie-%20Scalable%20Similarity%20Search%20on%20Integer%20Sketches__1910.08278/00-精读笔记.md](../../paper/$b$-Bit%20Sketch%20Trie-%20Scalable%20Similarity%20Search%20on%20Integer%20Sketches__1910.08278/00-精读笔记.md)
- 聚类式 ANN 的学习排序改进（把 nprobe 选择学出来）→ [../../paper/A%20Learning-to-Rank%20Formulation%20of%20Clustering-Based%20Approximate%20Nearest%20Neighbor%20Search__2404.11731/00-精读笔记.md](../../paper/A%20Learning-to-Rank%20Formulation%20of%20Clustering-Based%20Approximate%20Nearest%20Neighbor%20Search__2404.11731/00-精读笔记.md)
- LSM/分区思想的一般化 → [../Database_Internals/07-日志结构存储.md](../Database_Internals/07-日志结构存储.md)（倒排队列≈按空间分区的段）

## 思考题（合上笔记再答）

1. 为什么本玩具数据集上 LSH 候选集动辄数千？LSH 在什么数据分布上才好吃（提示：低内在维度/大间隔簇）？
2. PQ 的 ADC 查找表每次查询要算 m×2^nbits 个距离——据此推导"批量查询时 PQ 摊薄"的直觉。
3. IVF nprobe=1 recall 仅 0.181，而候选有 464 条——解释"很多候选、很少命中"的几何原因（查询在胞边界/簇被切碎跨胞）。
4. 三族索引各自如何做删除？（LSH 墓碑桶、IVF 倒排标记、PQ 码表不变+过滤——引出 06 章产品的增量更新难点）

## 2026 视角补注

- **量化是降本主轴**：2024–2026 各产品把 SQ8/PQ/bq/RaBitQ 写进默认卖点（ES int8/hnsw bq、pgvector 0.7+ quantization、Qdrant scalar/binary quantization、Milvus GPU_IVF_PQ）（⚠️ 各官方文档转述；仓库 ✅ 见 01 章演进节）——本章 PQ/IVF 就是这些功能的祖先。
- **RaBitQ（2024, SIGMOD）**把随机比特量化推到可证误差界，重塑 1-bit 压缩的召回预期（⚠️ 论文标题+会议+年份，未过 DOI 链：Gao & Long, "RaBitQ: Quantizing High-Dimensional Vectors with a Theoretical Error Bound for Approximate Nearest Neighbor Search"）。
- **GPU 线**：RAPIDS cuVS/CAGRA 把 IVF/PQ 图混合搬上 GPU，ann-benchmarks 官方榜仍是 CPU 口径（⚠️ 转述；https://github.com/rapidsai/cuvs 本机未验）。

## 复现清单与参数台账（想在本机重跑本章全部数字时）

1. `python vgen.py`：DuckDB 造 10,000×64（60 簇，seed 隐含于 random 会话，复跑数值会小幅漂移——结构不变）+100 查询+暴力真值，约 1 s。
2. `python exp_b.py`：B1 四组 LSH（约 35 s）+ B2 的 Lq 扫描 + B3 PQ（建 7.9 s、四档 nrec）。
3. `python exp_c.py` 的 C2 段：IVF nlist=32、kmeans 训练样本 1500、nprobe 五档（约 30 s）。
4. 台账：LSH k=8/L=12→44.1ms/0.997；k=10/L=24/Lq=4→34.1ms/0.811；PQ nrec=200→0.537；IVF nprobe=16→34.2ms/0.888、簇大小 1~526、建索引 2.3 s。
5. 口径警示：全部单线程、100 查询均值、无 p99；与 08 章 G 表同一进程环境，跨进程对比时先看"数字台账纪律"（同表同跑）。
6. 进阶复玩：把 `vgen.py` 的簇噪声从 `±1` 调到 `±0.2`（簇更分离），LSH/IVF 的召回曲线整体左移——"数据分布是隐参数"的 10 分钟实验。

## 三族索引的增删改对照（数据库人最该先问的一栏）

| 操作 | LSH | IVF | PQ |
| --- | --- | --- | --- |
| 插入 | 算签名入各表桶，O(L·k·d) | 找最近胞入倒排 | 编码+入桶（或全桶） |
| 删除 | 桶内摘除即可 | 倒排摘除，胞不缩 | 码表不动，靠墓碑过滤 |
| 重训 | 超平面可换（全库重签名） | 质心漂移后需重建 | 码本换代=全量重编码 |
- 共性：三族"索引更新"都比等值索引贵一个量级——06 章段模型用"批量重建代替逐条更新"消化这一切。

## 家谱速记（三族一句话，防"算法名词晕"）

- LSH 家谱：超平面（cosine）→ 分箱（L2）→ MinHash/LSH Forest/E2LSH——共同信仰"哈希即相似"，本玩具取了最古早的一支。
- 量化家谱：SQ（各维独立标量）→ PQ（子空间联合码本）→ OPQ（先旋转再 PQ）→ AQQ/RaBitQ（带误差界的比特量化）——压缩率与误差可控性是四代进化主线。
- 倒排聚类家谱：IVF（粗量化）→ IVFADC（+PQ 码）→ IVFPQ-refine（+raw 重排）→ GPU/磁盘变体——本章三张表各自站在这三条线的起点上。

## 核心概念速览（中英对照）

- **局部敏感哈希** — LSH：近邻大概率同桶的随机哈希族。
- **签名** — Signature：LSH 的比特桶键。
- **码本** — Codebook：PQ 子空间的 k-means 质心集。
- **乘积量化** — PQ：m 段独立量化的组合压缩。
- **ADC** — Asymmetric Distance Computation：查询不量化、库量化，查表求距离。
- **粗量化** — Coarse quantizer (IVF)：全库 k-means 的分区质心。
- **nlist/nprobe** — IVF 分区数/查询访问分区数。
- **倒排队列** — Inverted list：胞内成员向量表。
- **重排池** — Refetch/rerank pool：精确复算的候选上限。
- **残差编码** — Residual encoding：IVFPQ 里对"减去胞中心"再量化。

## 最新演进与工业实践

- **FAISS 仍是算法集散地**：IVF/PQ/OPQ/HNSW 全部可组合，`index_factory` 一行语法（`IVF65536,PQ32` 等）就是本章概念的对象化（⚠️ 文档转述，仓库 ✅ 200 已验）。
- **产品血统对照**：Milvus 的 IVF_FLAT/IVF_PQ/IVF_SQ8 全家桶、Qdrant 的 scalar quantization+过滤、Weaviate 的 PQ+动态重排——命名直接沿用本章术语（⚠️ 文档转述；仓库 ✅ 200 已验，见 01 章演进节）。
- **论文线**：量化/哈希系算法的统一评测视角见 [08-评测基准与工程实践.md](08-评测基准与工程实践.md) 的 ANN-Benchmarks 互链；分布式化（把倒排/图放到多机）见本章开头 2405.13795 精读链与 [../../db/db.md](../../db/db.md)。
