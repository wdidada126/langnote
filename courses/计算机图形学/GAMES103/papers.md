# GAMES103 论文与应用清单

## 1. 经典论文（模拟方向）

| 论文/资料 | 年份 | 主题 | 关联讲次 |
| --- | --- | --- | --- |
| Baraff, Physically Based Modeling: Principles and Practice（SIGGRAPH 课程） | 1997/2001 | 刚体模拟圣经 | L02-L07 |
| Baraff et al., What Can Be Simulated（cloth SIGGRAPH course） | 2003 | 布料模拟 | L08-L10 |
| Provot, Deformation constraints in a mass-spring model of cloth | 1995 | 质点弹簧约束 | L08 |
| Müller et al., Position Based Dynamics | 2007 | PBD | L09 |
| Macklin et al., XPBD / Small Steps in PBD | 2016/2020 | 柔度一致约束 | L09 |
| Terzopoulos et al., Elastically Deformable Models | 1987 | 弹性体动画源头 | L11 |
| Irving et al., Guaranteed Similarity Matrix Positivity / cotetrahedra | 2006-07 | FEM 稳定化 | L12 |
| Sifakis et al., Subspace/Displacement Mesh（SIFD 课程） | 2012 | 实时弹性体 | L13 |
| Stam, Stable Fluids | 1999 | 半拉格朗日流体 | L14 |
| Fedkiw et al., Visual Simulation of Smoke | 2001 | 烟雾特效 | L14 |
| Müller et al., Meshless Methods (SPH) | 2003 | 无网格流体 | L15 |
| Zhu-Bridson, Animating and rendering water bubbles / two-way coupling | 2005 | 流体-刚体耦合 | L15 |
| Li et al., CLF / PIC-FLIP 综述（可选） | 2019 | 混合粒子网格 | L15 |
| Ericson, Real-Time Collision Detection（书） | 2004 | GJK/EPA | L05 |

## 2. 近 5 年论文（2021-2026）

| 论文 | 年份 | 方向 |
| --- | --- | --- |
| Macklin et al., MOSEL/材质优化、IPC（Barrier 方法, Li 2020-2021 延续） | 2021+ | 保证无相交的弹塑性模拟 |
| Hu et al., MLS-MPM 家族拓展（可微 MPM 变体等） | 2021-2023 | 统一物质模拟 GPU 化 |
| Volatile 系列/破碎流体（SIGGRAPH 2022 泡沫/碎裂） | 2022 | 特效流体 |
| NVIDIA Warp / Newton 物理引擎论文与文档 | 2022-2024 | 可微 GPU 物理栈 |
| PhysDreamer / PhysTuner（视频先验学习物理参数） | 2024 | 学习式物理 |
| Gaussian Splashing 等 GS+流体渲染结合 | 2024 | 模拟与神经渲染接口 |
| DiffSim / 可微模拟综述 | 2021-2023 | 梯度可传播模拟器 |

## 3. 知识点在开源项目中的应用

| 知识点 | 开源项目 | 体现 |
| --- | --- | --- |
| 刚体+顺序冲量 | Bullet、Jolt Physics、Rapier | 接触/摩擦求解器核心 |
| PBD/XPBD | NVIDIA FleX 思路、MuJoCo（softbody）、Bevy XPBD | 约束求解、毛发布料 |
| FEM 弹性体 | SOFA（医学仿真）、Wuji/Genesis | 软体机器人、手术模拟 |
| 布料 | Blender Cloth、Marvelous Designer（闭源对照） | 质点弹簧+压力 |
| 流体 | PositionBasedFluids、Taichi MPM/SPH 示例、OpenFOAM（工程侧） | GPU 粒子流体 |
| 可微模拟 | DiffTaichi、Genesis、MuJoCo MJX | RL/机器人 |
| C# 作业栈 | Unity DOTS Physics 对比阅读 | 官方作业语言环境 |
