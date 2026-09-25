# CS224w 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| DeepWalk | 2014 | L2 | 随机游走+skip-gram 嵌入 |
| node2vec | 2016 | L2 | BFS/DFS 可调游走 |
| LINE | 2015 | L2 | 一阶/二阶邻近联合嵌入 |
| Semi-Supervised Classification with GCN | 2016 | L4 | 一阶谱近似 GCN |
| GAT | 2017 | L6 | 注意力邻居加权 |
| GIN (How Powerful are GNNs) | 2018 | L4/L7 | WL 上界与判别式聚合 |
| GraphSAGE | 2018 | L3/L9/L10 | 归纳式采样聚合，工业推荐底座 |
| PinSage | 2018 | L10 | Pinterest 十亿节点部署 |
| DGI | 2018 | L5 | 互信息最大化自监督 |
| GAE/VGAE | 2016 | L8 | 图（变分）自编码器链接预测 |
| DiffPool | 2018 | L11 | 可微层次聚类 |
| GraphRNN | 2018 | L13 | 自回归图生成 |
| OGB (Benchmarking GNNs) | 2020 | L14 | 标准化大规模基准 |
| Neural Message Passing for Quantum Chemistry (MPNN) | 2017 | L3 | 消息传递统一框架命名者 |
| E（分子几何 GNN） | 2021 | L12 | 等变几何 GNN 代表作 |

## 近 5 年（2021-2026）论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| GraphGPS: Striking the Right Balance | 2022 | L7 图 Transformer 基准 |
| GPS/Graph Transformer 位置编码综述 | 2022-2023 | L7 可扩展位置编码 |
| PNA: Principal Neighbourhood Aggregation | 2021（2022 起普及） | L7 度感知聚合 |
| Edge Directionality Improves Learning on LLM Graph (GraphCodeBert 类) | 2023-2025 | L16 代码图 |
| GraphRAG (Microsoft) | 2024 | L16 图检索增强 |
| GDGDM/EDM 图扩散生成 | 2022-2023 | L13 生成 SOTA |
| Uni-Mol / 分子基础模型 | 2023 | L15 科学应用 |
| GNN-FM / 图基础模型探索 | 2025 | L16 前沿 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 嵌入（L2） | gensim/walklet | 随机游走嵌入工具 |
| 消息传递（L3-L6） | PyTorch Geometric / DGL | scatter/aggregate 算子与模型库 |
| 图 Transformer（L7） | GraphGPS (LaplacianPy/GPS 官方) | 基准实现 |
| 链接预测（L8） | PyG linkproppred / OGB evaluator | 负采样与Hits@K评估 |
| 可缩放训练（L10） | DGL 采样器 / GraphLearn / MariusGNN | 邻居/层采样与分区 |
| 基准（L14） | OGB / GNN-Benchmark | 标准 split 与排行榜 |
| 应用（L15） | deepchem（分子）/ torch geometric 推荐案例 / GraphRAG (MS) | 科学/推荐/RAG 落地 |
