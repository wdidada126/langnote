# GAMES101 逐讲要点大纲（outline）

> 本文件是全课速览与导航。笔记正文按本目录 README 定稿的 16 讲 + 附录组织；
> 官方 2019 秋季班视频实际为 23 个讲次条目，本目录的讲次合并了官方部分讲次，
> 下方"官方对照"列给出映射关系。

| 本目录讲次 | 主题 | 官方对照（23 讲制） | 笔记文件 |
| --- | --- | --- | --- |
| L01 | 图形学入门：应用版图、光栅化成像、管线预览 | Lecture 01 | L01-introduction.md |
| L02 | 数学基础（上）：向量与向量运算 | Lecture 02 | L02-linear-algebra-vectors.md |
| L03 | 数学基础（下）：矩阵、线性变换、齐次坐标 | Lecture 02–03 | L03-linear-algebra-matrices.md |
| L04 | 变换（上）：平移/缩放/旋转、复合变换 | Lecture 03 | L04-transformations-i.md |
| L05 | 变换（下）：3D 旋转、欧拉角与万向锁、世界坐标、变换求逆 | Lecture 03–04 | L05-transformations-ii.md |
| L06 | 投影变换：视锥体、正交/透视投影 | Lecture 04 | L06-projection-transforms.md |
| L07 | 图形管线概览：可见性、z-buffer、着色流水线 | Lecture 05 | L07-graphics-pipeline.md |
| L08 | 光栅化（一）：采样、像素中心、三角形包含测试、重心坐标 | Lecture 05–06 | L08-rasterization-triangles.md |
| L09 | 光栅化（二）：抗锯齿、超采样、MSAA | Lecture 06–07 | L09-rasterization-antialiasing.md |
| L10 | 几何体：点线面、三角、四边形、圆与球 | Lecture 08 | L10-geometric-primitives.md |
| L11 | 表示：Bezier/样条、曲面细分、SDF/CSG、网格 | Lecture 09–10 | L11-geometry-representation.md |
| L12 | 纹理映射：UV、双线性、Mipmap、凹凸贴图 | Lecture 07、11 | L12-textures.md |
| L13 | 颜色与光照：人眼、色域、gamma、加色/减色系统 | Lecture 12 | L13-color-appearance.md |
| L14 | 几何着色：Lambert、Phong/Blinn-Phong、BRDF 初探 | Lecture 13–14 | L14-shading-materials.md |
| L15 | 光线追踪（一）：辐射度量学、渲染方程、蒙特卡洛 | Lecture 15–17 | L15-raytracing-i-radiometry.md |
| L16 | 光线追踪（二）：Whitted 光追、BVH 加速、路径追踪 | Lecture 18–20 | L16-raytracing-ii-path.md |
| 附 | 动画简介：视觉暂留、运动模糊、摄像机动画、课程总结 | Lecture 21–22 | L17-animation-summary.md |

## 三条主线（全课骨架）

1. **光栅化（L04–L12, L14）**：把三维世界"投影 + 采样 + 着色"成屏幕图像。
   以三角形为基本图元，速度快（现代 GPU 每帧数十亿次着色），是实时渲染（游戏）的基石。
2. **光线追踪与光的传输（L15–L16）**：从相机向场景发射光线求交，天然支持反射/折射/阴影/
   间接光；路径追踪用蒙特卡洛离散化渲染方程，是离线电影渲染（Blender Cycles 等）的黄金标准。
3. **几何表示（L10–L12）**：如何"表示"物体——显式（网格/样条）与隐式（SDF/体素/CSG），
   以及用纹理把细节"贴"回表面。表示决定采样与求交算法，进而决定走光栅化还是光线追踪。

三条主线在"渲染方程"处汇合：光栅化 = 对成像几何与着色的工程近似；光线追踪 = 对可见性
（L14 可见性讲内容并入 L15–L16）的精确求解；路径追踪 = 对光传输积分的蒙特卡洛求解。

## 配套实践

- `projects/p1_linalg_transforms`（L02–L06）：向量/矩阵库 + 变换演示，输出 PPM。
- `projects/p2_rasterizer`（L06–L09, L12, L14）：软件光栅化器：三角形填充 + z-buffer +
  透视 correct 插值 + Blinn-Phong + 棋盘纹理。
- `projects/p3_geometry`（L10–L11）：几何表示：半空间 CSG（光线行进）+ .obj 子集读取渲染。
- `projects/p4_raytracer`（L15–L16）：球体 Whitted 光追 → Lambertian+镜面路径追踪（MC 半球
  采样），含低/高采样数噪声对比与朴素降噪。
- `papers/papers.md`：经典论文（Phong 1975 → Kajiya 1986）与近 5 年（NeRF 2020、
  Gaussian Splatting 2023、ReSTIR、DLSS 3 等）+ 知识点↔开源映射表。
