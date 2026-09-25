# Stanford CS224w: Machine Learning with Graphs 学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CS224w: Machine Learning with Graphs（原 CS224R） |
| 学校 | Stanford University |
| 主讲 | Jure Leskovec（斯坦福图学习/网络科学领军人物，SNAP/GraphSAGE/PinSage 作者） |
| 教材 | 无指定教材；配合 Leskovec 团队《Graph Neural Networks: Foundations and Methods》（书稿公开）与论文阅读 |
| csdiy 路径 | `深度学习/CS224w`（页面更新：2022-04-03） |
| 最新期次 | Fall 2024（官网课程页最新一期；YouTube 有完整公开课视频） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟🌟，约 80 小时；先修：深度学习基础 + Python；语言：Python + LaTeX |

## 为什么学

- GNN 领域公认最佳入门课：从节点嵌入到消息传递、图生成、几何深度学习一站式打通。
- 授课人 Jure Leskovec 一系工作（GraphSAGE、PinSage、GNN 解释力理论）就是工业图学习的底座，推荐系统/知识图谱/分子性质的教科书来源。
- 现实世界里"非欧数据"占大头：社交网络、引用网、分子、知识图谱、代码依赖图——本课给你处理它们的统一语言。
- csdiy 推荐语：众多做 GNN 的朋友力荐；6 个编程作业 + 3 个 LaTeX 书面作业训练完整科研工程能力。

## 先修与知识联系

- 先修：CS230/CS229 级别的 ML/DL 基础、Python；线代（谱、特征值）尤其重要。
- 纵向：把 CS224n/CS231n 学到的序列/网格卷积推广到一般图；为几何深度学习（Bronstein 书）与 AlphaFold 类研究铺路。
- 横向：与 LHY 的 RAG 图扩展（GraphRAG）、知识图谱方向应用直接相关。

## 讲义章节目录（按近年 Fall 公开课表整理，以官网为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 图机器学习引言与任务类型 | 课程 notes ch.1；网络科学背景 |
| L2 | 节点嵌入：DeepWalk 与 node2vec | DeepWalk、node2vec 论文 |
| L3 | 消息传递 GNN 基础 | 消息传递框架综述（Gilmer） |
| L4 | GCN/GIN：卷积的谱与空域推导 | GCN、GIN 论文 |
| L5 | 无监督与自监督图学习 | DGK/DGI/GraphCL 论文 |
| L6 | 半监督训练、GAT 与注意力 | GAT 论文 |
| L7 | 高级 GNN 架构：表达力与子图 | WL 检验、PNA、SubgraphGNN |
| L8 | 链接预测与图补全 | 矩阵分解到 GAE 谱系 |
| L9 | 图级任务：图分类与回归 | GraphSAGE、Deep Graph Kernel |
| L10 | 可缩放 GNN：采样与工程 | GraphSAGE/Layer sampling 论文 |
| L11 | 图 pooling 与层次化学习 | DiffPool 论文 |
| L12 | 几何深度学习 | Bronstein 几何 DL 综述节选 |
| L13 | 图生成模型 | GraphRNN、GRAN |
| L14 | 评估与基准 | OGB 基准论文 |
| L15 | 应用讲座：知识图谱/推荐/科学（含 AlphaFold） | GNN 应用综述 |
| L16 | 前沿研究分享（Guest） | 当季 arXiv 列表 |

> 作业线：Colab 编程作业 6 个（嵌入→GCN→GAT→链接预测→图分类→scaling）+ LaTeX 书面作业 3 个 + 期末项目。
