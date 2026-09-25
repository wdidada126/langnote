# 15-462 论文与应用清单

## 1. 经典论文

| 论文 | 年份 | 主题 | 关联讲次 |
| --- | --- | --- | --- |
| Whitted, An Improved Illumination Model | 1980 | 光线追踪 | L15 |
| Kajiya, The Rendering Equation | 1986 | 渲染方程 | L13-L16 |
| Cook, Torrance 反射模型 | 1982 | 微表面 BRDF | L14 |
| Veach, Robust Monte Carlo Methods（博士论文） | 1997 | 重要性采样/MIS | L16-L17 |
| Catmull-Clark 细分曲面 | 1978 | 细分 | L12 |
| Osher-Sethian 水平集 / Lorensen-Nahl 等值面（marching cubes） | 1988/1987 | 隐式形状 | L12 |
| Gortler et al., The Lumigraph / Levoy-Gortler 光场相机 | 1996 | 光场/成像 | L18 |
| Heckbert-Salesin（多重采样）/ Williams（mipmap） | 1983-94 | 采样与滤波 | L04-L06 |
| Naylor BSP 树 | 1980 | 可见性 | L08 |
| Ringach-Hertzberg? 更贴切：Terzopoulos 弹性动画 | 1987 | 物理动画 | L19-L20 |
| Stollnitz et al., Wavelets for Computer Graphics | 1995 | 傅里叶/小波视角 | L22 |
| Aila et al., GPU ray tracing 体系 | 2010 | 高性能光追 | L17 |

## 2. 近 5 年论文（2021-2026）

| 论文 | 年份 | 方向 | 关联 |
| --- | --- | --- | --- |
| Mip-NeRF 360 / NeRF++ 后续神经体渲染 | 2021-2022 | 神经渲染（NeRF 前身谱系续） | L13-L18 |
| 3D Gaussian Splatting | 2023 | 显式表示+可微光栅 | L04/L12/L18 |
| ReSTIR 系列 | 2021-2023 | 重采样实时 MC | L16-L17 |
| Nanite 虚拟化几何（SIGGRAPH 2021 tech papers/演讲） | 2021 | GPU 驱动几何 | L07-L09 |
| PhysDreamer/生成式物理先验 | 2024 | 学习式模拟 | L19-L20 |
| Hash-grid 神经场加速（Instant-NGP） | 2022 | 表示+采样 | L12/L18 |
| LBS/非线性蒙皮与可微 IK 改进 | 2021-2023 | 动画优化 | L21 |
| Fourier 视角下的逆渲染可微分（不同可微渲染综述） | 2021-2023 | 优化/数据拟合 | L21-L22 |

## 3. 知识点在开源项目中的应用

| 知识点 | 开源项目 | 体现 |
| --- | --- | --- |
| 采样/滤波/MC | pbrt-v4（教材同源）、Cycles 积分器 | PBRT 全书实现 |
| 图形管线/光栅化 | Mesa(Vulkan/OpenGL)、bgfx、diligent | 开源驱动/引擎 |
| 半边结构/几何处理 | libigl、Geometry Central(glbasis/cotangent 库) | Crane 团队直接维护 |
| 细分/SDF | OpenVDB、USD/SDF 原语、Meshbooleans | 隐式几何 |
| 微表面 BRDF | Filament、three.js MeshPhysicalMaterial、OpenPBR | 实时 PBR |
| 高性能光追 | Embree、OIDN、VulkanRT(Mesa/DXRL) | 光追内核 |
| ODE/物理 | Genesis、Warp、SOFA | 模拟 |
| 优化/IK | Pinocchio、Tracr? 更准：OPENVRA/MoveIt | 机器人 IK |
| 傅里叶/拟合 | FFTW、scipy.signal | 信号侧 |
