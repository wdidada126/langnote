# GAMES202 - 高质量实时渲染（闫令琪）

## 1. 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | GAMES202: High Quality Real-Time Rendering — 高质量实时渲染 |
| 所属学校 | UCSB（GAMES 公益公开课系列） |
| 主讲教师 | 闫令琪（Ling-Qi Yan） |
| 课程教材 | Real-Time Rendering, 4th edition（RTR4，官方定位为参考书，与课件重合度低） |
| csdiy 路径 | `计算机图形学/GAMES202`（csdiy.wiki，页面日期 2022-05-12） |
| 最新期次 | 2021 春季班（B 站完整视频，15 讲专题制） |
| 状态 | 骨架（notes/papers/projects 待填充） |
| 先修要求 | 线性代数、高等数学、C++、GAMES101 |
| 难度/学时 | 🌟🌟🌟🌟 / 约 60 小时；5 个 Project |
| 课程网站 | https://games-cn.org/games202/ ｜ 视频：B 站 GAMES202 |

## 2. 为什么学

- GAMES101 的进阶课：聚焦实时渲染（>30 FPS）的苛刻时限下，如何打破"速度与质量"的权衡，兼顾实时与照片级真实感。
- 覆盖学术界与工业界前沿专题：实时软阴影、环境光照、全局光照（预计算/无预计算）、基于物理的着色（PBR）、实时光线追踪、抗锯齿与超采样、常用加速手段。
- 不教任何游戏引擎操作、不绑定具体着色器语言，只讲实时渲染背后的科学与知识——学完有能力开发自己的实时渲染引擎。
- 是理解 Unity URP/HDRP、Unreal、BEPU/diligent 等引擎渲染菜单背后原理的最短路径。

## 3. 先修与知识联系

- **先修**：GAMES101（管线、光栅化、光追、着色基础）；C++ 与基本 GPU 编程概念（GLSL/HLSL 可选）。
- **横向**：15-462/CS148 的渲染部分；GPU 体系结构（`courses/体系结构`）解释带宽/并行约束。
- **工业对照**：DLSS/FSR/XeSS 超分、DXR/Vulkan RT、ReSTIR、Nanite——均能对应到本课专题。
- **下游**：实时光追引擎开发、TA（技术美术）科学层、神经渲染加速。

## 4. 讲义章节目录（2021 班，15 讲专题制）

> 阅读材料：官方 PPT + RTR4 对应章节 + 各讲引用论文（详见 papers.md）。

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L01 | 实时渲染概述（Overview of Real-Time Rendering） | 官方 Notes L01 |
| L02 | 回顾：渲染管线、着色语言、渲染方程、微积分基础 | RTR4 Ch.2, Ch.6；FCG Ch.14 |
| L03 | 实时阴影 1：Shadow Mapping 及其变体 | RTR4 Ch.4.9 阴影；Williams1978、Donner-Smith2005 |
| L04 | 实时阴影 2：滤波与软阴影技术（PCSS/VSM/ESSM/方差） | Lauritzen2010、ANN Shadow |
| L05 | 实时环境光照：IBL、辐照度环境贴图、split-sum 预滤波 | RTR4 Ch.8；Kautz07、Epic PBR 文档 |
| L06 | 实时全局光照 1：屏幕空间 GI（SSAO/SSR/SVO） | RTO AO 论文、Schied17 SSGI |
| L07 | 实时全局光照 2：空间类 GI（Light Probe/辐照度探针/SDF GI） | Sunkovsky19、Zenith 距离场 |
| L08 | 实时全局光照 3：预计算与烘焙（SH/PRT/Lightmap/Bake） | Ramamoorthi-Hanrahan01、Sloan PRT |
| L09 | 实时高质量着色 1：表面反射模型（微表面 BRDF/Cook-Torrance/GGX） | Walter07、Karis13 |
| L10 | 实时高质量着色 2：散射与风格化渲染（SSS/各向异性/清漆） | d'Eon SSS、Blinn77 各项异性 |
| L11 | 实时高质量着色 3：复杂材质模拟（涂层/织物/多层材质） | Disney BRDF、Microfacet 拓展 |
| L12 | 实时光线追踪 1：Trace 传播与滤波（DXR/Vulkan RT、硬件光追） | Aila10、DXR 规范 |
| L13 | 实时光线追踪 2：时间累积与降噪（Denoising/ReSTIR） | Bitterli20、Lin17、ReSTIR 2021 |
| L14 | 实时抗锯齿与超采样（TAA/DLSS/MLSS） | Yan-Kang 系列、Kajiya84 |
| L15 | 实时渲染中常用的工业界技术（管线调度、加速结构、引擎实践概念） | 官方 Notes L15 |

### 作业（5 个 Project）

Shadow Mapping/软阴影、IBL+PBR 材质、SSGI/探针 GI、实时光追降噪、综合渲染器（TAA/超分）。

## 5. 笔记进度

- [ ] notes/outline.md（每讲 3-5 条要点骨架，已建）
- [ ] notes/ 逐讲全文笔记
- [x] papers.md（经典 + 近 5 年 + 开源应用对照表）
- [ ] projects/ 配套代码（本轮只建计划表）
