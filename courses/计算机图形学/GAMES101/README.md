# GAMES101 - 现代计算机图形学入门（闫令琪）【CORE】

## 1. 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | GAMES101: Modern Computer Graphics — 现代计算机图形学入门 |
| 所属学校 | UCSB（主讲人任职于加州大学圣塔芭芭拉分校；GAMES 国内公益图形学公开课系列） |
| 主讲教师 | 闫令琪（Lingqi Wang / Ling-Qi Yan） |
| 课程教材 | Fundamentals of Computer Graphics（FCG，Steve Marschner & Peter Shirley，第 4 版） |
| csdiy 路径 | `计算机图形学/GAMES101`（csdiy.wiki，页面日期 2022-09-06） |
| 最新期次 | 2019 秋季班（官方完整视频，B 站/官网持续开放） |
| 状态 | CORE 完整笔记由后续专人撰写；本 README 为全章节目录定稿 |
| 先修要求 | 线性代数、高等数学、C++ |
| 难度/学时 | 🌟🌟🌟 / 约 80 小时；8 个 Project |
| 课程网站 | http://games-cn.org/graphics-intro-ppt-talk/ ｜ 视频：B 站 GAMES101 |

## 2. 为什么学

- 国内影响力最大的图形学入门公开课，系统性覆盖现代图形学四大板块：光栅化成像、几何表示、光的传播理论、动画与模拟，从原理讲到前沿。
- 主讲人闫令琪对实时光线追踪（DirectX Raytracing 相关技术路线）有直接推动作用，课程内容"现代化"，是工业界（游戏引擎、渲染器）需要的基础。
- 图形学不等于 OpenGL、不等于光线追踪，而是"生成整个虚拟世界的一套方法"——本课提供自上而下的全局观。
- 每个 Project 代码量不大但有趣：从零实现光栅化渲染器与光线追踪器，含选做拓展（BVH 加速、更高质量渲染）。
- 是 GAMES202（实时渲染）、GAMES103（物理动画）、CS148/15-462/USTC-CG 的先修或对照课程。

## 3. 先修与知识联系

- **数学**：MIT 18.06 线性代数（向量/矩阵/特征值）、微积分基础；向量代数与变换矩阵是全课工具。
- **编程**：C++（Project 语言）；建议先修 CS61A/CS50 级别编程能力与 CMake（见 `courses/计算机系统基础`、必学工具）。
- **下游课程**：
  - GAMES202（实时渲染进阶，本目录 `计算机图形学/GAMES202`）
  - GAMES103（物理模拟，`计算机图形学/GAMES103`）
  - CMU 15-462 / Stanford CS148 / USTC CG（同主题不同侧重，可互补）
  - CS231n / 神经渲染方向：本课的光栅化与光追是 NeRF/3DGS 的背景知识。
- **开源对照**：Blender Cycles/EEVEE、Three.js、Mesa(Vulkan/DX12) 中的管线概念均可回溯到本课文。

## 4. 讲义章节目录（2019 秋季班全 16 讲 + 补充讲）

> 阅读材料以 FCG 第 4 版章节为主，配合官方讲义 PDF（GAMES101 官方 PPT 与 Notes）。

| 讲次 | 标题 | 阅读材料（FCG4 章节/Notes） |
| --- | --- | --- |
| L01 | 图形学入门（Application Areas / Rasterization / Graphics Pipeline 预览） | FCG Ch.1；官方 Notes L01 |
| L02 | 数学基础（上）：向量、向量运算、内积外积、线性相关 | FCG Ch.2, App.B |
| L03 | 数学基础（下）：矩阵、线性变换、齐次坐标 | FCG Ch.2, Ch.4.2 |
| L04 | 变换（上）：平移/缩放/旋转、复合变换 | FCG Ch.4 |
| L05 | 变换（下）：3D 旋转（欧拉角/万向锁）、世界坐标系、变换求逆 | FCG Ch.4 |
| L06 | 投影变换：视锥体、正交/透视投影矩阵 | FCG Ch.5 |
| L07 | 图形管线概览：可见性、z-buffer、着色流水线 | FCG Ch.6, Ch.10 |
| L08 | 光栅化（一）：采样、像素中心、三角形包含测试 | FCG Ch.7-8 |
| L09 | 光栅化（二）：抗锯齿、超采样、MSAA、颜色 | FCG Ch.8-9 |
| L10 | 几何体：图元、点线面三角、四边形、圆与球 | FCG Ch.3 |
| L11 | 表示（Representation）：旋转曲线、样条/Bezier、曲面细分（Loop/Catmull-Clark）、SDF、网格操作 | FCG Ch.12-13 |
| L12 | 纹理映射：UV、双线性插值、Mipmap、凹凸/法线/置换贴图 | FCG Ch.12 |
| L13 | 颜色与光照：人眼、色域、gamma、加法/色相系统 | FCG Ch.6；Notes L13 |
| L14 | 几何着色（Shading and Geometry）：环境/漫反射/镜面、Lambert、Phong/Blinn-Phong、BRDF 初探 | FCG Ch.10-11 |
| L15 | 光线追踪（一）：辐射度量学、渲染方程初探 | FCG Ch.14, 28 |
| L16 | 光线追踪（二）：Whitted 光追、加速结构（BVH/网格）、蒙特卡洛思想 | FCG Ch.14 |
| 附 | 动画简介：运动模糊、插值与摄像机动画、课程总结 | FCG Ch.16 |

### 作业（8 个 Project）

| # | 名称 | 覆盖讲次 |
| --- | --- | --- |
| P1 | 变换矩阵（Rotation/MPII） | L02-L05 |
| P2 | 软件光栅化器（三角形、z-buffer、MSAA） | L07-L09 |
| P3 | 贝塞尔曲线与曲面细分 | L11 |
| P4 | 光线追踪器（球/网格、反射折射、BVH、区域采样） | L12-L16 |
| 拓展 | 各 P 附带选做：更高采样质量、透视纹理校正、Gouraud 着色等 | — |

## 5. 笔记进度

- [ ] notes/outline.md（逐讲要点）
- [ ] notes/L01-L16 全文笔记
- [ ] papers/（经典与近 5 年论文精读）
- [ ] projects/（P1-P4 实现与构建）

> 本课为【CORE】：正文笔记、论文、代码由后续专人完成，本 README 为定稿目录骨架。
