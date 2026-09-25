# L08 光栅化（一）：采样、三角形包含测试与重心坐标

> 对应 README 讲次 L08；官方 Lecture 05–06。阅读：FCG4 Ch.7–8。实践：projects/p2。

## 1. 光栅化 = 以像素为中心采样世界

像素 $(i+\tfrac12,\,j+\tfrac12)$ 是**采样点**（像素中心约定）。问题归结为：
每个采样点落在哪些图元内？——"Inside test"。

## 2. 三角形内测试：半平面法

三角形三条边各定义一条**边函数（edge function）**，即二维叉积的 z 分量：

$$E_{AB}(P)=(B-A)\times(P-A)=e_x(P)\cdot(B_y-A_y)-e_y(P)\cdot(B_x-A_x)$$

$P$ 在边 $AB$ 左侧（逆时针绕行约定）$\Rightarrow E>0$。**三角形内 ⟺ 三条边同号**：

$$E_{AB}(P)>0\;\wedge\;E_{BC}(P)>0\;\wedge\;E_{CA}(P)>0$$

实现：先算三角形包围盒（bounding box），只对盒内像素测试——O(盒面积) 而非 O(屏面积)。

## 3. 重心坐标（barycentric coordinates）

三角形内任意点可表为 $\alpha A+\beta B+\gamma C,\ \alpha+\beta+\gamma=1$。解线性方程组得：

$$\alpha=\frac{E_{BC}(P)}{E_{BC}(A)},\quad \beta=\frac{E_{CA}(P)}{E_{CA}(B)},\quad \gamma=\frac{E_{AB}(P)}{E_{AB}(C)}$$

面积直觉：$\alpha=\mathrm{Area}(PBC)/\mathrm{Area}(ABC)$（$P$ 对面顶点的"份额"）。
包含测试与插值参数**是同一套计算**：边函数即重心坐标的分子/分母。

**插值任意属性**（颜色、UV、法线、深度）：

$$\mathrm{attribute}(P)=\alpha\,\mathrm{attribute}(A)+\beta\,\mathrm{attribute}(B)+\gamma\,\mathrm{attribute}(C)$$

屏幕空间线性插值对**深度 z 不成立**（透视除法破坏线性），对纹理/法线必须
用透视 correct 插值（L06 伏笔、L12 公式）：插值 $\frac{a}{z}$ 而非 $a$。

## 4. 为什么是三角形？

- 三点定面：任意三角形必共面、必凸 → 半平面测试普适。
- 任意多边形可三角剖分（L10）。
- 硬件友好：边函数是 2 乘 1 加的 SIMD 明星；GPU 光栅化器按三角形吞吐设计。

## 5. 与前后续讲的联系

- 上一讲管线里"光栅化"格子的展开；本讲解决"谁覆盖此像素"，
  着色插值（重心坐标）为 L12 纹理、L14 逐像素光照供参数。
- 下一讲 L09：像素中心的**点采样**产生锯齿 → 改用覆盖面积（area sampling）。
- 边函数/重心坐标在 L16 光线追踪里变成"求交后再做重心测试（Möller–Trumbore）"——
  两条主线在三角形求交处合流。projects/p2/p3/p4 都用同一组公式。

## 6. 跨课程联系

- **DDCA/CSAPP**：bounding box 提前跳出 = 缓存友好的局部性；边函数的增量计算
  （$E(P+(1,0))=E(P)+c$）是强度削减（strength reduction）的活教材。
- **18.06**：解 $\alpha,\beta,\gamma$ 的方程组 = 2×2 线性系统求逆；面积公式
  即叉积的模（L02 复用）。
- **CS149**：三角形→像素是典型的"散射（scatter）+ 几何膨胀"负载，
  硬件用 tile-based（移动端 GPU）或 wavefront 并行。
- **GAMES202**：TAA/FSR 的重建核依赖采样格子的频率分析（本讲 + L09 的延长线）。

## 7. 开源项目中的应用

- **tinyrenderer / projects/p2**：30 行内完成"三角形填充 + z-buffer + 重心插值"。
- **Mesa llvmpipe**：CPU 光栅化器，边函数 + 增量 SIMD 实现。
- **GPU 固定功能单元**：D3D12/Vulkan 规范规定重心坐标插值精度上限，
  所以游戏里顶点属性插值不必完全一致（移动端尤其明显）。
- **PBRT**：`TriangleMesh::Intersect` 返回重心坐标 $(u,v)$，与本课记号一致。

## 8. 延伸阅读与自查

- 阅读：FCG4 Ch.8；Giesen 管线文第 2 篇（scan conversion）；
  Möller & Trumbore 1997《Fast, Minimum Storage Ray/Triangle Intersection》。
- 自查：
  1. 证明三角形内 $\alpha+\beta+\gamma=1$ 且全为正。
  2. 顺时针给定的顶点序会使半平面测试失败——工业上如何处理（front/back culling）？
  3. 屏幕空间对 $1/z$ 线性、对纹理坐标需除以 $z$——推导透视 correct 插值公式
     （提示：三角形 $ABC$ 投影到 $A'B'C'$，世界权重 $\propto$ 屏幕权重 × $z$）。
