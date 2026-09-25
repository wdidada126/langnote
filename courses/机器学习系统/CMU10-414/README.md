# CMU 10-414/714: Deep Learning Systems 学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | 10-414/714: Deep Learning Systems |
| 学校 | CMU（卡内基梅隆大学） |
| 主讲 | Zico Kolter、Tianqi Chen（陈天奇） |
| 教材 | 无；官方讲义 + 课程配套库 needle（从 0 到 1 构建的 DL 库） |
| csdiy 路径 | `机器学习系统/CMU 10-414/714: Deep Learning Systems`（页面更新：2025-06-09） |
| 最新期次 | Fall 2024 版（在线评测账号与论坛注册已结束，仅本地测试可用；csdiy 期待秋季重开在线版） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟，约 100 小时；先修：系统入门(如 15-213)、深度学习入门、基本数学；语言 Python/C++ |

## 为什么学

- 深度学习框架"从调包侠到造轮子"的经典课程：5 个作业从零设计并实现一个完整的 DL 库 Needle——计算图自动微分、各类损失/优化器/数据加载器，再到 CNN/RNN/LSTM/Transformer 等常见网络。
- 覆盖 DL Systems 全栈：框架顶层设计 → 自动微分原理与实现 → 底层硬件加速 → 生产部署。
- 两位授课教师（Kolter/Chen）把所有课程内容开源，配套 jupyter notebook 逐步描述实现细节，对新手友好。
- 是 15-442/642（同一陈天奇的 LLM 时代系统课）的最佳前导，needle 即 micrograd 的工业级放大。

## 先修与知识联系

- 先修：15-213/CSAPP（系统）、任意 DL 入门（CS230/Coursera DL）；C++ 基础（HW3 起需要）。
- 前导：NeuralNets-ZeroToHero（micrograd 是 needle 的标量版前传）。
- 后续：CMU15-442（LLM 系统进阶）、MLC（编译方向）、AICS（同主题中文路线）。
- 知识输出：autograd/反向模式 → PyTorch 引擎认知；GPU 加速作业 → CUDA 开发；性能建模 → 推理引擎优化。

## 讲义章节目录（对应 dlsyscourse.org 公开讲次，Fall 2024）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论：深度学习系统全景 + simple auto-diff | Lecture 1 slides；micrograd 对照 |
| L2 | 自动微分 I：前向模式 AD 与实现 | Lecture 2；HW1 |
| L3 | 自动微分 II：反向模式 AD（tape/显式图） | Lecture 3；HW1 |
| L4 | 自动微分应用：MLP 训练实战 | Lecture 4；HW1 notebooks |
| L5 | 机器学习基础：损失、优化器、数据加载器 | Lecture 5；HW2 |
| L6 | 深度学习框架设计：backend/autograd 分层 | Lecture 6；HW2 |
| L7 | 反向模式 AD 进阶（自定义反向算子） | Lecture 7；HW2 |
| L8 | 实用深度学习 I：神经网络/CNN 与 HW3 | Lecture 8；HW3 |
| L9 | 实用深度学习 II：RNN/LSTM/Transformer 与 HW4 | Lecture 9；HW4 |
| L10 | GPU 加速：cuDNN 集成与并行 | Lecture 10；HW5 相关 |
| L11 | 低精度与混合精度训练 | Lecture 11；Micikevicius 2018 |
| L12 | 系统性能建模：Roofline、内存与并行 | Lecture 12 |
| L13 | 高级主题：分布式、量化、编译器概览 | Lecture 13 |
| L14 | 课程回顾 + needle 全链路串讲 | 全部讲义 |

> 注：课程共 5 个 Homework（Needle 库的 5 次增量），上表讲次与作业映射以官网为准。

## 课程资源（摘自 csdiy）

- 课程网站：https://dlsyscourse.org
- 课程视频：YouTube（官方，L1 示例 https://www.youtube.com/watch?v=qbJqOFMyIwg）
- 课程作业：https://dlsyscourse.org/assignments/（开源，在线评测期已过）
- 资源汇总：PKUFlyingPig/CMU10-714、Crazy-Ryan/CMU-10-714（24 Fall 作业实现）
