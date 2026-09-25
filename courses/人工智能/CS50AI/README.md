# Harvard CS50's Introduction to AI with Python（CS50AI）学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CS50's Introduction to Artificial Intelligence with Python |
| 学校 | Harvard（CS50 团队，David J. Malan 主持） |
| 主讲 | CS50 团队（Brian Yu 等主讲 2024 版） |
| 教材 | 无指定教材；参考 AIMA（Russell & Norvig）对应章节 |
| csdiy 路径 | `人工智能/CS50's Introduction to AI with Python`（页面更新：2025-06-08） |
| 最新期次 | 2024 版（课程网站/视频/作业均提供 2024 与 2020 两版，推荐 2024） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟，约 30 小时；先修：基本概率论 + Python 基础；语言 Python |

## 为什么学

- 一门非常基础的 AI 入门课，12 个设计精巧的编程作业全部围绕"做出一个会玩游戏的 AI"：强化学习打 Nim、alpha-beta 剪枝扫雷等，成就感极强。
- 广度覆盖经典 AI 主线：搜索、逻辑、不确定性、优化、学习、语言、感知，是 CS188 的轻量平替与先导。
- 全程 Python + 不依赖深度学习框架，适合新手入门或大佬休闲。
- csdiy 收录 @PKUFlyingPig 资源汇总仓库（cs50_ai），作业与实现参考齐全。

## 先修与知识联系

- 先修：CS50P / MIT-Missing-Semester 级别的 Python；基本概率论。
- 后续：CS188（同主题的理论深化版，伯克利官方路线）、NeuralNets-ZeroToHero（本课 L5/L6 涉及的神经网络与 Transformer 的从零实现）。
- 横向：CS189/CS229 承接 L5 机器学习部分；CS285 承接 L5 强化学习部分。
- 知识输出：博弈搜索 → 棋类引擎（Stockfish/python-chess）；HMM/贝叶斯 → 早期 NLP 与概率图模型；CV 感知作业 → OpenCV 生态。

## 讲义章节目录（2024 版，共 8 讲 + 期末项目）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | Search：无信息/ informed 搜索（BFS/DFS/UCS/A*） | AIMA Ch.3；Hart et al. 1968 A* |
| L2 | Logic：命题/谓词逻辑与推理（resolution、forward/backward chaining） | AIMA Ch.7-9；AI for Search and Logic 讲义 |
| L3 | Uncertainty：概率、贝叶斯网络与推断 | AIMA Ch.13-14；Bayes 定理与条件独立 |
| L4 | Optimization：局部搜索、模拟退火、约束优化 | AIMA Ch.4；Kirkpatrick 1983 模拟退火 |
| L5 | Learning：监督学习（决策树/kNN）、神经网络、强化学习（Q-learning） | AIMA Ch.18；Quinlan 1986 ID3；Watkins 1989 Q-Learning |
| L6 | Language：朴素贝叶斯、马尔可夫模型、词嵌入与 Transformer | AIMA Ch.22-23；Vaswani et al. 2017（导读） |
| L7 | Perception：图像检索——边缘检测、Hough 变换、SIFT-like 特征 | AIMA 延伸阅读；Canny 1986 |
| L8 | Ethics：AI 伦理（偏见、隐私、可解释性） | Barocas & Selbst 相关读物 |
| 期末 | Final Project：开放式 AI 应用设计 | 课程网站 spec |

> 注：作业共 12 个 + 期末项目（2024 版含 tiles/crosswords/nim 等游戏 AI 系列），具体题号以课程网站为准，骨架阶段允许微调。

## 课程资源（摘自 csdiy）

- 课程网站：2024 / 2020 版
- 课程视频：2024 / 2020 版（YouTube CS50 频道）
- 课程教材：无
- 课程作业：2024 / 2020，12 个精巧的编程作业
- 资源汇总：PKUFlyingPig/cs50_ai（GitHub）
