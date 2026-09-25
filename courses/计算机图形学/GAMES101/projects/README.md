# GAMES101 配套渐进项目（projects/）

语言：**C++17（仅标准库）**；输出统一为 **PPM 图像文件**（P3 文本/P6 二进制），
不依赖任何图形库；构建脚本 `build.bat`（MSVC `cl`）与 `build.sh`（g++）。
本轮代码完整自洽、按课程口径撰写，**未在本机编译验证**——如遇编译器告警请当作练习修正。

## 总表

| 项目 | 覆盖讲次（本 README 目录） | 官方视频对照 | 产出图像 | 核心算法 |
| --- | --- | --- | --- | --- |
| [p1_linalg_transforms](p1_linalg_transforms/) | L02–L06 | Lecture 02–04 | `transforms_2d.ppm`、`mvp_cube.ppm` | Vec/Mat4 库、2D 仿射 8 宫格、MVP+透视除法线框、刚体求逆自检 |
| [p2_rasterizer](p2_rasterizer/) | L06–L09, L12, L14 | Lecture 04–07、11、13–14 | `cube_raster.ppm`、`cube_compare.ppm`、`cube_ssaa.ppm` | 视锥裁剪、三角形填充（边函数/重心坐标）、z-buffer、透视 correct vs 线性对比、Blinn-Phong、棋盘纹理、4×4 超采样 |
| [p3_geometry](p3_geometry/) | L10–L11 | Lecture 08–10 | `mesh.ppm`、`csg.ppm` | .obj 子集加载（v/f+扇形三角化）、Möller–Trumbore、V−E+F 拓扑自检、半空间 CSG、SDF sphere tracing |
| [p4_raytracer](p4_raytracer/) | L13–L16 | Lecture 12、15–20 | `whitted.ppm`、`path_16/1024.ppm`、`path_16_blur.ppm` | 球/半空间求交、Whitted 反射+Snell 折射+阴影光线、渲染方程 MC 估计（Lambertian+镜面）、cos 加权半球采样、NEE、俄罗斯轮盘赌、箱式降噪对比、tonemap+gamma |

> 讲次号以本目录 `../README.md` 定稿的 16 讲+附录结构为准；"官方对照"列给出 2019 视频
> （约 23 讲制）的大致映射，便于边看视频边做项目。

## 统一构建

Windows（在 "x64 Native Tools Command Prompt" 中，或先 `vcvarsall.bat x64`）：

```bat
cd p2_rasterizer
build.bat
bin\p2
```

Linux / macOS / WSL：

```sh
cd p2_rasterizer
./build.sh && ./bin/p2
```

每个项目的 README 含：覆盖讲次、算法流程图、出图观察点、调参实验与已知局限。

## 与课程 Assignment 的关系

| GAMES101 作业 | 本项目 | 差异说明 |
| --- | --- | --- |
| Project 1（MVP） | p1 | p1 不要求 TGA 解析，直接出 PPM |
| Project 2（光栅化） | p2 | 等价：三角形+z-buffer+纹理；BMP 输出换成 PPM |
| Project 3（Bezier/细分） | 未做（选做方向见 p3 README） | p3 专注表示的隐式/网格两翼 |
| Project 4（光线追踪） | p4（+p3 显式网格求交） | 球体版 Whitted→路径追踪；BVH 为选做练习 |

## 学习顺序建议

1. p1 跑通 → 对照 notes/L02–L06 检查每个矩阵元素。
2. p2 的 `cube_compare.ppm` 是 L06/L12 最难懂两段公式的最好教具，先看懂再改代码。
3. p3 回答"图形学为什么爱三角形、也爱 max() 函数"（L10/L11）。
4. p4 的 16 vs 1024 spp 对比做完，L15–L16 的 $O(1/\sqrt N)$ 就成了肌肉记忆。
