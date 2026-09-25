# Stanford STATS214 / CS229M：Machine Learning Theory（机器学习理论）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | Stanford STATS 214 / CS 229M: Machine Learning Theory |
| 学校 | Stanford University |
| 主讲 | 曾任教 Percy Liang；现任主讲 Tengyu Ma（马腾宇，深度学习的统计学习理论） |
| 教材 | 无固定教材；课程 notes + 经典理论论文（统计学习理论、凸/非凸优化、深度学习理论） |
| csdiy 路径 | 机器学习进阶 → Stanford STATS214 / CS229M: Machine Learning Theory |
| 最新期次 | csdiy 推荐版记录于 2023-12-16；课程常态每年开课（官网 http://web.stanford.edu/class/stats214/ 查当期） |
| 状态 | 骨架已建，待逐讲填充笔记 |
| 课程网站 | http://web.stanford.edu/class/stats214/ |
| 难度 | 🌟🌟🌟🌟🌟🌟（经典学习理论 + 最新深度学习理论，非常硬核） |

## 为什么学

- 打通**统计学习理论与深度学习理论**两端：一边是 VC/ Rademacher/泛函分析式的经典保证，一边是"过参数化网络为何不遗忘、SGD 为何有效"这类现代之谜。
- Tengyu Ma 是深度学习理论代表人物（NTK/隐式正则化/两时间尺度分析），课程即一手研究视角。
- 是 ML 进阶方向读论文的"数学护照"：没有这套语言，无法评价 STA4273/STAT8201/10-708 中方法的保证与反例。
- 对 LLM 实践也有直接回馈：缩放律、双下降、对齐的分布偏移分析都建立在本课工具上。

## 先修与知识联系

- 先修：机器学习（CS229 级别）、深度学习、统计学基础；实分析/凸优化/概率不等式经验强烈加分。
- 联系：
  - 上游：CS229/CS189（ML）、CS70/CS126（概率）、EE364A（凸优化，数学进阶分类）。
  - 平行：机器学习进阶/STA4273（期望优化的收敛性语言共享）、CMU10-708（变分推断的统计视角）、STAT8201（生成模型理论侧）。
  - 下游：缩放律/推理模型研究（LLM 课）的理论根基；深度学习理论科研方向。

## 讲义章节目录（按官网主题与历年大纲整理，以当期 syllabus 为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 导论：ML 理论的三大问题（泛化/优化/表达力）与记号 | 课程 notes §0；Mohri 第 1-3 章 |
| L2 | 均匀收敛与增长函数：有限假设类的泛化界 | Vapnik-Chervonenkis 1971 选读 |
| L3 | VC 维与 Sauer-Shelah 引理 | VC 1971；Shelah 组合定理 |
| L4 | Rademacher 复杂度与数据相关界 | Bartlett-Mendelson 教程 |
| L5 | PAC-Bayes 界与压缩视角 | McAllester；Dziugaite-Roy 神经网 PAC-Bayes |
| L6 | 线性/凸模型的统计速率：极小极大下界 | Tsybakov 教材 ch2；Hsu-Kakade-Zhang 笔记 |
| L7 | 梯度下降与凸优化：平滑、强凸、收敛率 | Nesterov 教材选章 |
| L8 | 非凸优化 I：SGD 收敛、鞍点逃逸 | Nesterov-Polyak；Ge et al. 严格鞍点 |
| L9 | 非凸优化 II：隐式正则化与良性景观 | Hardt et al.；Arora 隐式偏置 |
| L10 | 两时间尺度分析与神经ODE视角 | Arora et al. Two-Time-Scale；Chaudhari Optimal ML 选章 |
| L11 | 表达力：深度分离与近似率 | Telgarsky deep-shallow；Barron 近似类 |
| L12 | 过参数化与插值：双下降现象 | Belkin double descent；Grohs 记忆论 |
| L13 | NTK 与宽网络线性化 | Jacot NTK；Du et al. 全局收敛 |
| L14 | 宽网络的统计效应：benign overfitting、偏差-方差反直觉 | Belkin benign overfitting；Bartlett 尖峰反例 |
| L15 | 矩阵分解/张量方法：凸松弛到非凸 | Ge et al. 非凸矩阵感引；Bresson 综述 |
| L16 | 分布偏移、鲁棒性与 OOD 泛化 | Arjora; Moosavi-Dezfooli? （经典 robustness 综述）+ 课程当年论文 |
| L17 | 生成模型与统计推断理论：GMM/混合识别、score 一致性 | Huang-Fu; Score matching 分析类 |
| L18 | 强化学习与序列决策理论基础（视当期大纲） | Jin et al. RL 统计理论综述 |
| L19 | 缩放律理论：经验规律 vs 可证速率 | Kaplan/Chinchilla；Hoffmann 理论连接 |
| L20 | 前沿专题与学生展示：LLM 时代开放问题 | 当期论文 |

> 注：每学期主题顺序有调整；上表为近年大纲的稳定骨架（官网页面含 notes/slides）。
