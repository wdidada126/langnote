# L11 几何体（二）：表示——曲线、曲面细分、隐式与网格

> 对应 README 讲次 L11；官方 Lecture 09–10。阅读：FCG4 Ch.12–13。实践：projects/p3。

## 1. 曲线：参数化与 Bezier

三次 Bezier 由 4 个控制点定义：
$B(t)=(1-t)^3P_0+3t(1-t)^2P_1+3t^2(1-t)P_2+t^3P_3,\ t\in[0,1]$。
凸包、端点切线等优良性质。**de Casteljau 算法**：控制点多边形递归线性插值，
$t$ 处的点即最后一次插值结果；顺带把曲线在 $t$ 处**分裂**为两段 Bezier —— 
数值稳定、易并行、GPU tessellation 的思想原型。

**样条（spline）**：多段曲线拼接，控制连续性（C0 位置连续、C1 切线连续、
C2 曲率连续）。插值 vs 逼近（控制点不必在曲线上，Bezier 是逼近式）。
动画曲线（UE 的 CurveAsset、Blender 的 F-Curve）就是它的工业形态。

## 2. 曲面：参数曲面与细分

- 参数曲面：$S(u,v)$，Bezier 三角形/矩形片；CAD 的 NURBS 是其有理推广。
- **细分曲面（subdivision）**：从粗网格迭代逼近光滑曲面。
  - Loop（三角面）：1→4 分裂 + 邻域加权模板；
  - Catmull-Clark（四边面）：面点+边点+顶点三点规则，极限曲面在
     extraordinary 点外 C2 连续。
  - 直觉：每轮=低通滤波（L09 的频域视角），特征值分析可证收敛
    （18.06 的特征值在几何处理中的惊艳复用）。
- 用途：建模只需少控制点（"数字黏土"），渲染时细分到所需密度；
  皮克斯 subdivision surface（RenderMan）是历史拐点。

## 3. 隐式表示：函数即形状

形状 = 某函数的零/负水平集：

- **球/椭球/环面**：$f(x,y,z)=0$（L10）。
- **半空间/CSG**：$f=\max(f_A,-f_B)$（交、并、差），布尔运算=函数组合。
  projects/p3 的"瑞士奶酪"即球减若干球孔。
- **SDF（signed distance field）**：$f(p)=$ 到表面的带符号距离。
  强大之处：$\lVert\nabla f\rVert=1$（几乎处处）→ **球步进光线行进
  （sphere tracing）**：从 $p$ 沿射线走 $f(p)$ 距离永不穿过表面 → 秒画任意
  CSG/SDF 场景，且天然抗锯齿（走不满一步时按 $\pm$ 距离做覆盖率）。
- ** metaballs**：多个衰减函数求和取阈值——"液体感"的祖传配方。

## 4. 体素与网格操作

- 体素：规则采样 + 三线性插值；医学成像/雕刻（ZBrush）/Minecraft。
- 网格数据结构：顶点/边/面计数关系 $F-E+V=2$（欧拉公式，闭合流形）；
  **半边结构（half-edge）** 让"下一条边/相邻面"成为 O(1)。
- 网格处理：简化（decimation）、平滑（Laplacian：顶点移向邻域均值=一次低通）、
  参数化（UV 展开，接 L12）。

## 5. 与前后续讲的联系

- 表示决定算法：三角网格→L08 光栅化 / L16 求交；SDF→sphere tracing；
  体素→体绘制。L10 的对照表在本讲展开。
- UV 展开（网格参数化）是 L12 纹理映射的前提；细分密度 ↔ 纹理分辨率
  互相牵制（过细的网格配不上糊纹理）。
- 附录的动画：骨骼蒙皮（线性混合蒙皮）作用在网格顶点上——表示与动画的接口。

## 6. 跨课程联系

- **18.06**：细分的收敛性=迭代矩阵的谱分析；网格拉普拉斯平滑=图拉普拉斯
  （谱聚类同款算子）；二次曲面分类=对称矩阵特征分解。
- **CS231n / 深度生成模型**：神经隐式表示是 2020 年后的 explosion——
  Occupancy Networks、DeepSDF 用 MLP 代替手写 $f$；NeRF 把体素换成坐标+方向
  的网络（L12/L15 处再联）；Dreamer 系世界模型在潜空间维护"可渲染几何"。
- **CS149**：细分是天然的数据并行（每边/每面独立）；体素遍历 = 并行前缀和。
- **GAMES202**：实时全局光照常配 voxel/距离场加速（如 Doom 的 raymarched 体积雾）。

## 7. 开源项目中的应用

- **OpenSubdiv（皮克斯）/ Blender Multires**：细分曲面的生产实现。
- **libigl / MeshLab**：网格处理算法库（拉普拉斯平滑、decimation）。
- **Minecraft / OpenVDB**：体素的两个极端（粗块 vs 影视级稀疏体积）。
- **Inigo Quilez 的 Shadertoy**：全站 SDF raymarching 示范——L11 隐式表示的
  最佳活广告；他的文章《Distances》是 SDF 圣经。
- **graphdeco-inria/gaussian-splatting**：2023 新表示（各向异性高斯基元），
  介于点云与隐式之间——"表示"这条线至今仍在生长。
- **projects/p3**：半空间 CSG + raymarching + .obj 子集加载（v/f）。

## 8. 延伸阅读与自查

- 阅读：FCG4 Ch.12–13；《Computer Graphics: Principles and Practice》Ch.1；
  IQ 的 SDF 教程目录（iquilezles.org）；Loop 1987 / Catmull-Clark 1978 原文。
- 自查：
  1. 用 de Casteljau 手工算 $t=0.5$ 的三次 Bezier 点，并给出分裂后的左半控制点。
  2. 为什么 sphere tracing 中步距取 $f(p)$ 是"安全极大步"？
  3. 一个闭合流形网格 V=4, E=6，F=？（欧拉公式）它是什么形状？
