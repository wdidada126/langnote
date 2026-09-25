# CS148 论文与应用清单

## 1. 经典论文

| 论文 | 年份 | 主题 | 关联讲次 |
| --- | --- | --- | --- |
| Whitted, An Improved Illumination Model for Shaded Display | 1980 | 递归光线追踪 | L08 |
| Blinn, Models of lighting（Specular reflection models） | 1977 | Phong/Blinn 高光 | L06 |
| Cook, Shade Trees | 1984 | 着色程序表示 | L06 |
| Williams, Pyramids for Fast Texture Filtering | 1983 | Mipmap | L07 |
| Heckbert, Survey of Texture Mapping | 1986 | 纹理映射综述 | L07 |
| Blinn, Texture and Reflection in Computer Generated Images | 1976 | 高光贴图/凹凸起源 | L07 |
| Möller-Trumbore, Fast Triangle-Triangle Intersection Test | 1997 | 三角形求交 | L08 |
| Catmull-Clark / Loop 细分曲面 | 1978/1987 | 细分 | L02/L10 |
| Goldsmith-Salmon, Automatic Creation of Object Hierarchies for Ray Tracing | 1987 | BVH 早期 | L10 |
| Wald, Ray Tracing using SAM/KD-tree（RTSys 系列） | 2001-07 | 光追加速 | L10 |
| Cook-Torrance 反射模型 | 1982 | BRDF | L06 |
| 神经渲染前身：Reed? 更合适：Gortler Light Fields / Levoy 数字反光相机 | 1996 | 光场成像 | L05/L08 |

## 2. 近 5 年论文（2021-2026）

| 论文 | 年份 | 方向 | 关联 |
| --- | --- | --- | --- |
| NeRF 后续：Mip-NeRF 360、Nerfstudio 框架论文 | 2022-2023 | 神经渲染 | 光追+体渲染的神经化 |
| 3D Gaussian Splatting（SIGGRAPH 2023） | 2023 | 显式神经表示+光栅化 | L08-L10 混合管线 |
| Instant NeRF（NVIS 2021） | 2022 | 实时 NeRF | 采样与加速结构 |
| MESA/Blender EEVEE Next 技术评审文档 | 2023-2024 | 实时光栅引擎 | L02/L06 工业对照 |
| Physically Based Rendering 工具链（OpenPBR 规范 1.0） | 2023 | 材质标准化 | L06 BRDF |
| DLSS-RR / 神经辐射缓存（NVIDIA 2023-2025） | 2023-2025 | 光追降噪 | L08/L09 |

## 3. 知识点在开源项目中的应用

| 知识点 | 开源项目 | 体现 |
| --- | --- | --- |
| Blender 建模/修改器 | Blender、cloud-Known 插件生态 | 课程工具本体 |
| 色彩管理/gamma | OpenColorIO（影视标准）、Blender Color Management | L05 |
| 透视相机/求交 | three.js（Raycaster、Frustum）、pbrt-v4 | L04/L08 |
| 纹理与 Mipmap | KTX/khronos texture、DirectXTex | L07 |
| BVH |Embree、tinyobjloader+BVH 示例、Mesa Vulkan RT | L10 |
| 蒙特卡洛 | Cycles 积分器（path guiding/低差异序列） | L09 |
