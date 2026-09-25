# USTC CG 论文与应用清单

## 1. 经典论文（以课程指定/几何方向为主）

| 论文 | 年份 | 主题 | 关联讲次 |
| --- | --- | --- | --- |
| Bresenham, Algorithm for Computer Control of a Digital Plotter | 1965 | 光栅化绘制 | L03 |
| Sutherland et al., A Character Generator / 扫描线多边形填充 | 1969 | 图元与可见性 | L03-L05 |
| Catmull, A Subdivision Algorithm for Computer Display of Curved Surfaces | 1974 | 细分 | L12 |
| Blinn, Texture and Reflection（凹凸贴图起源） | 1976 | 纹理 | L07 |
| Whitted 光线追踪 | 1980 | 渲染 | L08 |
| Garland-Heckbert, QEM 网格简化 | 1997 | 简化 | L12 |
| Lévy et al., LSCM 参数化 | 2002 | 参数化 | L13 |
| Liu et al., Local / Global Single-Interval Parameterization (LISC) | 2008-2010 | 参数化（本校代表作） | L13 |
| Meyer et al., Discrete Differential-Geometry Operators | 2003 | 离散曲率 | L11 |
| Pérez et al., Poisson Image Editing | 2003 | 图像融合 | L14 |
| Kazhdan et al., Poisson Surface Reconstruction | 2006 | 重建 | L15 |
| Schmid et al., Digital Typography（SDF 字体渲染） | 2012 | 距离场 | L09 |
| Vallet-Lévy, Spectral Quadric Mesh Simplification | 2008 | 简化（延伸） | L12 |

## 2. 近 5 年论文（2021-2026）

| 论文 | 年份 | 方向 | 关联 |
| --- | --- | --- | --- |
| NeRF→3DGS：Gaussian Splatting 及其网格化后续（SuGaR 2023） | 2023 | 神经渲染与几何 | L08/L15 |
| DreamFusion / Zero123 / 生成式 3D（Score Distillation 谱系） | 2022-2024 | 生成 3D | L10/L15 |
| Neural Fields 综述（Xie et al. 2022） | 2022 | 隐式表示 | L09 |
| Differentiable Surface Reconstruction（DNPR? 准确：GPU 可微重建类） | 2021-2023 | 可微几何 | L11-L15 |
| Physically based 单参数化新方法（authalic/等面积进展） | 2021+ | 参数化 | L13 |
| MeshGS/神经网格混合表示 | 2024 | 表示 | L09-L12 |
| SDF 学习式重建（Neural SDF 综述后续） | 2021-2024 | 距离场 | L09 |

## 3. 知识点在开源项目中的应用

| 知识点 | 开源项目 | 体现 |
| --- | --- | --- |
| 光栅化/可见性 | Mesa、Pixman（cairo 底层） | 软光栅与合成 |
| SDF 字体 | Mapbox gl-native SDF 字体、FontForge 管线、tiny-sdf | 工程标准做法 |
| 曲线曲面/NURBS | FreeCAD/OpenCASCADE、Rhino（闭源对照） | CAD 内核 |
| 网格处理/曲率/细分/参数化 | libigl、Geometry Central、MeshLab、CGAL | 几何处理全家桶 |
| 简化 | quadri、Instant Meshes（内部） | 资产管线 |
| 泊松编辑/重建 | OpenCV（seamlessClone 即泊松融合）、CloudCompare/PCL(Poisson) | 图像/点云 |
| 前沿 | Nerfstudio、gsplat | 神经渲染 |
