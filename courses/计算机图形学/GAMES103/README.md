# GAMES103 - 基于物理的计算机动画入门（物理模拟）

## 1. 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | GAMES103: Introduction to Physics-Based Simulation for Computer Animation（csdiy 目录亦以"几何/动画"方向简注） |
| 所属学校 | Style3D / OSU（主讲来自工业界与俄亥俄州立大学体系） |
| 主讲教师 | 薛犇（Binh Xue，Style3D）等；Ge Wenping 团队支持 |
| 课程教材 | 无固定教材；以课程 PPT 与经典讲义/论文为主（参考 Baraff SIGGRAPH 课程、SIFD 课程等） |
| csdiy 路径 | `计算机图形学/GAMES103`（csdiy.wiki，页面日期 2022-09-06） |
| 最新期次 | 2022 春季班（B 站完整视频，约 24 讲/作业 4 次） |
| 状态 | 骨架 |
| 先修要求 | 线性代数、高等数学、大学物理、编程能力、基本图形学知识 |
| 难度/学时 | 🌟🌟🌟🌟 / 约 50 小时；4 次作业（C#） |
| 课程网站 | https://games-cn.org/games103/ ｜ 视频：B 站 GAMES103 |

## 2. 为什么学

- 图形学三分"渲染、模拟、几何"：GAMES101/202 偏渲染，本课是物理模拟方向最系统的中文入门。
- 四大主线专题：刚体模拟；质点弹簧、约束与布料模拟；基于有限元（FEM）的弹性体模拟；流体模拟。
- 不绑定具体商业引擎，而是讲各种引擎（Havok/PhysX/Unity 2D/Blender 刚体布料）背后的技术及其优缺点。
- 开场有必备数学/力学复习（ODE、变分、虚功原理），适合从"会用引擎"进阶到"能写模拟器"。
- 服装数字孪生（Style3D）、游戏物理、机器人仿真（Isaac/MuJoCo）方向的直接基础。

## 3. 先修与知识联系

- **数学**：18.06 线代、ODE、基础变分法；数值分析（隐式积分、线性求解器）建议先了解。
- **物理**：大学物理（牛顿力学、连续介质初步）。
- **图形学**：GAMES101 的变换/四元数/网格表示是前置；动画部分与 L16/附讲衔接。
- **对照**：15-462 后半（simulation）、GAMES102（几何）互补；下游可接 CMU 10-414（RL）做控制+模拟。
- **工业**：PhysX/Havok/MuJoCo 文档与本讲专题一一对应。

## 4. 讲义章节目录（2022 班专题结构，约 24 视频归为 16 主题）

> 阅读材料：官方 PPT + 各主题指定论文（见 papers.md）。

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L01 | 课程概述：计算机动画与物理模拟全景 | 官方 PPT 1 |
| L02 | 数学与力学复习：ODE、能量、动量、虚功原理 | Baraff SIGGRAPH'01 课程 Ch.2 |
| L03 | 刚体运动学：位姿、四元数、角速度 | FCG Ch.4；Shoemake 四元数讲义 |
| L04 | 刚体动力学：惯性张量、欧拉方程 | Baraff'01 Ch.3-4 |
| L05 | 刚体碰撞检测：GJK/EPA、凸体 | Ericson《Real-Time Collision Detection》Ch.5 |
| L06 | 碰撞响应与接触：冲量法、LCP/顺序冲量 | Baraff'01 Ch.7、Catto Sequential Impulse |
| L07 | 显式/隐式积分：半隐式欧拉、辛积分 | 数值分析讲义 |
| L08 | 质点弹簧系统：拉伸/弯曲/剪切弹簧 | Baraff'03（布料课程）Ch.2 |
| L09 | 约束与 PBD/XPBD：位置动力学族 | Müller PBD 2007、XPBD 2020 |
| L10 | 布料模拟：力学模型、摩擦、自碰 | 官方 PPT 10 |
| L11 | 弹性体力学：应力应变、超弹性材料 | SIFD 课程（Displacement Mesh Methods） |
| L12 | 线性 FEM：离散化、刚度矩阵 | SIFD Ch.2-3 |
| L13 | 非线性 FEM 与增量势：共旋、Newton 法加速 | SIFD Ch.4；Displacement Mesh |
| L14 | 流体 I：连续介质与 Navier-Stokes、半拉格朗日平流 | Bridson《Fluid Animation》Ch.3-4 |
| L15 | 流体 II：SPH 粒子法与混合方法 | Bridson Ch.15、SPH 综述 |
| L16 | 高级话题与总结：模型降阶、GPU 化、与渲染/学习的接口 | 官方 PPT 16 |

### 作业（4 次，C#/Unity 风格 starter）

HW1 刚体（弹球塔）、HW2 质点弹簧布料、HW3 FEM 弹性体、HW4 流体（2D/SPH）；非官方参考实现见 GAMES103 HW 汇总（知乎/Repo）。

## 5. 笔记进度

- [x] notes/outline.md（骨架） ｜ [ ] 逐讲全文 ｜ [x] papers.md ｜ [ ] projects/ 代码
