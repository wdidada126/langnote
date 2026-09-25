# CMU 15-462 - Computer Graphics (Fall 2022)

## 1. 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | 15-462: Computer Graphics（CMU，Keenan Crane 主讲版） |
| 所属学校 | Carnegie Mellon University |
| 主讲教师 | Keenan Crane（近年授课；15-462 传统名课） |
| 课程教材 | 无唯一课本；参考 FCG（Marschini-Shirley）、Computer Graphics: Principles and Practice、PBRT（Pharr-Jakob, 在线版） |
| csdiy 路径 | `计算机图形学/15462`（csdiy.wiki，页面日期 2022-12-15） |
| 最新期次 | Fall 2022（官网 15462.courses.cs.cmu.edu/fall2022；视频 YouTube/B 站） |
| 状态 | 骨架 |
| 先修要求 | 向量微积分、线性代数、基础 C/C++ |
| 难度/学时 | 🌟🌟🌟🌟 / 约 100 小时；作业/项目见官网 |
| 课程网站 | http://15462.courses.cs.cmu.edu/fall2022/ |

## 2. 为什么学

- CMU 招牌图形学课：以"数学统一视角"覆盖渲染、几何、动画、成像四大问题域的交叉。
- Keenan Crane 的讲法把 图形学当作应用数学：采样/混叠、傅里叶视角、变分与微分方程贯穿始终。
- 官方主题清单（csdiy 转录，防缓存清理）：采样、混叠、插值、光栅化、几何变换、参数化、可见性、合成、滤波、卷积、曲线与曲面、几何数据结构、细分、网格划分、空间层次结构、光线追踪、辐射度量、反射率、光场、几何光学、蒙特卡洛渲染、重要性采样、相机模型、高性能光线追踪、微分方程、时间积分、数值微分、基于物理的动画、优化、数值线性代数、逆运动学、傅里叶方法、数据拟合。
- 比 GAMES101 更深更快，是通往 15-463/15-862、SIGGRAPH 论文阅读能力的桥梁。

## 3. 先修与知识联系

- **数学**：线代（18.06/CS70 级别）、向量微积分、ODE；建议补数值分析（numerical）。
- **编程**：C/C++（geometry processing 作业大量用 C++ 与 Eigen）。
- **对照**：GAMES101 入门同主题；GAMES103 深讲本课模拟部分；GAMES102 深讲几何处理。
- **下游**：PBRT 读源码、15-463（高级渲染）、几何处理（15-466? 实为 Crane 的 15-462/几何课程线）。

## 4. 讲义章节目录（Fall 2022 主题制排课，约 22 讲；以官网 schedule 为准）

> 阅读材料：PBRT 在线版对应章 + Crane 讲义（notes 见课程网站）。

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L01 | 课程导论与线性代数回顾 | PBRT App. |
| L02 | 变换与齐次坐标 | FCG Ch.4 |
| L03 | 向量微积分回顾（梯度/散度/旋度） | Crane 向量微积分讲义 |
| L04 | 采样与混叠（图像/信号视角） | PBRT Ch.7；Gortler 光场 |
| L05 | 抗混叠与重建滤波 | PBRT Ch.7-8 |
| L06 | 插值、滤波与卷积 | FCG Ch.8；Crane 讲义 |
| L07 | 光栅化与图形管线 | FCG Ch.9-10 |
| L08 | 可见性：隐线/隐面（z-buffer、BSP、画家算法、模板） | FCG Ch.10 |
| L09 | 多边形网格与几何数据结构（半边结构） | FCG Ch.3 |
| L10 | 曲线（样条/Bézier/B 样条） | FCG Ch.12 |
| L11 | 曲面（参数曲面/patch） | FCG Ch.12 |
| L12 | 形状表示：细分、水平集/SDF、网格划分 | FCG Ch.13 |
| L13 | 辐射度量学 | PBRT Ch.4 |
| L14 | 反射率与 BRDF | PBRT Ch.8-9 |
| L15 | 光线追踪与几何光学 | PBRT Ch.6, 10 |
| L16 | 蒙特卡洛积分 | PBRT Ch.13 |
| L17 | 重要性采样与方差缩减、高性能光追 | PBRT Ch.14 |
| L18 | 相机模型与光场、计算成像 | PBRT Ch.9；Gortler 光场 |
| L19 | 动画与仿真 I：ODE 与时间积分 | 官方 notes |
| L20 | 动画与仿真 II：扩散、弹性与物理动画 | SIFD/Baraff |
| L21 | 优化与数值线性代数：逆运动学 | Nocedal & Wright 精选 |
| L22 | 傅里叶方法与数据拟合、课程总结 | 官方 notes |

### 作业

官方 Assignments 系列（A0 环境与热身，A1 采样/混叠图像实验，A2 光栅化与渲染管线，A3 曲线曲面与形状建模，A4 蒙特卡洛/光追渲染器，A5 模拟或动画专题，Final Project 自选），代码以 C++/Python 混合，具体以当期官网为准。

## 5. 笔记进度

- [x] notes/outline.md（骨架） ｜ [ ] 逐讲全文 ｜ [x] papers.md ｜ [ ] projects/ 代码
