# CMU 10-708：Probabilistic Graphical Models（概率图模型）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CMU 10-708: Probabilistic Graphical Models |
| 学校 | Carnegie Mellon University |
| 主讲 | Eric P. Xing（邢波）；后续学期亦有其他教授开设，csdiy 推荐版为 Spring 2019 公开课程版 |
| 教材 | Koller & Friedman《Probabilistic Graphical Models: Principles and Techniques》（主教材）+ 课程 notes |
| csdiy 路径 | 机器学习进阶 → CMU 10-708: Probabilistic Graphical Models |
| 最新期次（csdiy 推荐） | Spring 2019 公开课程版（csdiy 页面 2023-12-16）；CMU 每学期常态开课 |
| 状态 | 骨架已建，待逐讲填充笔记 |
| 课程网站 | https://sailinglab.github.io/pgm-spring-2019/ |
| 难度 | 🌟🌟🌟🌟🌟（约 24 讲 + homework/project，全资源含 slides/notes/video） |

## 为什么学

- 图模型领域的**标准受训课程**：表示（有向/无向/因子图）—推断（精确/近似）—学习（参数/结构）三大块完整覆盖，Koller & Friedman 教材的配套实战。
- 不只是经典：本课特色是把图模型**与深度学习、强化学习连接**——深度生成模型即潜变量图模型+神经参数化，RL 的滤波/规划即图上的推断。
- 非参数方法（GP、DP/IBP）部分讲透"无限维"建模，是理解现代贝叶斯深度学习的前置。
- 对读论文收益直接：VAE/扩散模型的能量视角、LLM 的链式法则、结构化预测的 CRF，都需要图模型语言。

## 先修与知识联系

- 先修：机器学习、深度学习、强化学习方法论上有帮助；核心需要概率论（条件期望、测度直觉）与线性代数。
- 联系：
  - 上游：CS70/CS126（概率）、CS229/10-301（ML）、CS285（RL）。
  - 平行/下游：机器学习进阶/STAT8201（深度生成模型=图模型×神经网络）、STA4273（推断与控制的统一观点）、CS229M（理论保证）；深度生成模型/MIT6.S184（潜变量动力系统的 SDE 视角）。

## 讲义章节目录（按 Spring 2019 公开课程 schedule 整理，以官网为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 导论：不确定性、图模型全景与课程地图 | K&F 第 1-3 章；课程 notes ch1 |
| L2 | 贝叶斯网（DGM）：语义、条件独立、链式分解 | K&F ch3 |
| L3 | 马尔可夫网（UGM）：团势、Hammersley-Clifford、对偶图 | K&F ch4 |
| L4 | 因子图与广义独立：消除顺序即三角化 | K&F ch4.6-9 |
| L5 | 精确推断 I：变量消除与信念传播（BP/sum-product） | K&F ch8-9 |
| L6 | 精确推断 II：junction tree 与聚类树传递 | K&F ch10 |
| L7 | MAP 推断：图割、整数规划 LP 松弛与对偶分解 | K&F ch11 |
| L8 | MRF 参数化：指数族、最大熵与对偶矩匹配 | K&F ch3.7/ch7 |
| L9 | 近似推断 I：变分方法、mean-field 与 ELBO | K&F ch12（Bishop ch10 对照） |
| L10 | 近似推断 II：结构化预测（CRF、结构化 SVM）与线性松弛 | Taskar/Koll 论文；Lafferty CRF |
| L11 | 蒙特卡洛：MC、重要性采样、Gibbs、Metropolis-Hastings | K&F ch13；Geyer 综述 |
| L12 | MCMC 进阶：混合、HMC/NUTS 与连续松弛 | Neal HMC 章节；Stan 文档 |
| L13 | 有向模型参数学习：MLE、贝叶斯、先验共轭与 MAP | K&F ch17-18 |
| L14 | 无监督与潜变量：EM 算法、混合模型、变分 EM | Dempster EM；K&F ch19 |
| L15 | 结构学习 I：评分搜索（BDeu/BIC）与约束基础（PC/IC） | Spirtes 著作选章；K&F ch16 |
| L16 | 结构学习 II：DAG 组合优化、订单搜索与可识别性 | Chickering 等价类；NoteSort 类论文 |
| L17 | 因果推断基础：干预、do 算子、因果发现与图模型 | Pearl 选章 |
| L18 | 时序模型：HMM/卡尔曼滤波/LDS/动态贝叶斯网 | Murphy 综述；Rabiner HMM |
| L19 | 图模型与强化学习：规划即推断、控制推断、逆 RL | Levine "RL as inference" 讲义 |
| L20 | 深度生成模型连接：VAE、深度潜变量模型与 amortized 推断 | Kingma & Welling；Sohn VAE 结构扩展 |
| L21 | 核方法与高斯过程：核回归、GP 分类与稀疏 GP | Rasmussen & Williams ch2-8 |
| L22 | 非参数贝叶斯 I： Dirichlet 过程、CRP 与无限混合 | Ferguson/Teh CRP 教程 |
| L23 | 非参数贝叶斯 II： IBP/Indian Buffet、beta-过程与主题模型 | Griffiths & Ghahramani IBP |
| L24 | 总结与前沿：图模型在 LLM/扩散时代的地位、项目展示 | 综述与当期论文（自选） |

> 注：官网含全部 slides/notes/video/homework/project；作业约 4-5 次（推断编程、结构学习、项目）。
