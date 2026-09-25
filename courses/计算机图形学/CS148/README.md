# Stanford CS148 - 计算机图形学与交互应用入门

## 1. 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | CS148: Introduction to Computer Graphics and Interactive Techniques（Stanford） |
| 所属学校 | Stanford University |
| 主讲教师 | Kayvon Fatahalian 等（Stanford 图形组） |
| 课程教材 | Fundamentals of Computer Graphics（FCG，主教材） |
| csdiy 路径 | `计算机图形学/CS148`（csdiy.wiki，页面日期 2022-06-07） |
| 最新期次 | 春季学期滚动开课；公开资料以 cs148.stanford.edu 当期网站为准（csdiy 参考 2021/2022 班） |
| 状态 | 骨架 |
| 先修要求 | 线性代数、高等数学、Python |
| 难度/学时 | 🌟🌟🌟 / 约 40 小时；8 个 HW + 1 个 Final Project |
| 课程网站 | https://cs148.stanford.edu/ |

## 2. 为什么学

- 图形学入门的"Python 友好"路线：比 GAMES101 浅一些，全程用 Python 写作业，适合不熟 C++ 的同学。
- 从 Blender 建模出发理解底层数学：三角形、法向量、插值、纹理映射、凹凸贴图，先会用再懂原理。
- 系统覆盖成像链路：光与颜色如何影响显示/打印（sRGB、gamma、色彩管理是这门课特色），再到 BRDF 与光照着色模型。
- 课程后段进入光线追踪、反走样与加速结构，与 GAMES101 主干完全同构，可互为讲义补充。
- Final Project 自由创作短片/交互应用，是"以产带学"的图形学第一课。

## 3. 先修与知识联系

- **数学**：18.06 线代（矩阵变换、特征值）、微积分；向量代数要求同 GAMES101。
- **编程**：Python（numpy 为主）；建议先修 CS61A 或同等 Python 能力。
- **对照**：GAMES101 提供同名主题的中文讲解；15-462 提供更深更快的数学。
- **下游**：CS248（进阶图形）、神经渲染/视觉特效（Houdini/Blender 管线）。
- **工具**：Blender（建模与渲染对照）、色彩管理可联系摄影/显示工程。

## 4. 讲义章节目录（按当期官网主题归并，约 10 主题）

> 阅读材料：FCG4 对应章节 + 当期官网 lecture slides。

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L01 | 什么是图形学：应用领域与课程概览 | FCG Ch.1 |
| L02 | Blender 工作流与三维建模基础（网格/编辑/变换） | FCG Ch.3；官方 HW1 指南 |
| L03 | 3D 几何：三角形、法向量、叉积与体积 | FCG Ch.3, Ch.2 |
| L04 | 变换与场景图（scene graph）、层次建模 | FCG Ch.4-5 |
| L05 | 图像与颜色：像素、色彩空间、gamma、显示/打印色域 | FCG Ch.6 |
| L06 | 光照与着色模型：Lambert、Phong、BRDF 初步 | FCG Ch.10-11 |
| L07 | 纹理映射与凹凸贴图：UV、采样、normal/displacement | FCG Ch.12 |
| L08 | 光线投射与光线追踪：相交测试、反射/折射 | FCG Ch.14 |
| L09 | 反走样与蒙特卡洛：超采样、随机采样 | FCG Ch.7-8, Ch.15 |
| L10 | 加速结构：网格与 BVH；课程总结与项目周 | FCG Ch.14-15 |

### 作业

HW1 Blender 场景建模与渲染 ｜ HW2 图像合成/色彩 ｜ HW3 透视相机与光线投射 ｜ HW4 三角形求交与着色的软渲染器 ｜ HW5 纹理/凹凸 ｜ HW6 反射折射与材质 ｜ HW7 BVH 加速 ｜ HW8 蒙特卡洛反走样 ｜ Final Project 短片/交互作品。

## 5. 笔记进度

- [x] notes/outline.md（骨架） ｜ [ ] 逐讲全文 ｜ [x] papers.md ｜ [ ] projects/ 代码
