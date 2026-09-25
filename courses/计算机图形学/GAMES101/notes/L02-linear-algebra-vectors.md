# L02 数学基础（上）：向量与向量运算

> 对应 README 讲次 L02；官方 Lecture 02（前半）。阅读：FCG4 Ch.2、App. B；18.06 Ch.1–3。

## 1. 向量：几何与代数的一体两面

$\vec{a}=(a_1,a_2,a_3)$ 既是从原点出发的有向线段，也是空间中的元素。
三维向量在 $x,y,z$ 三轴上的投影即分量。

- 加法：平行四边形法则；数乘：伸缩。
- 模长：$\lVert\vec a\rVert=\sqrt{\vec a\cdot\vec a}$；单位化：$\hat a=\vec a/\lVert\vec a\rVert$。
- **两点相减得到向量**：$\vec{PQ}=Q-P$——这是图形学里最高频的构造：
  三角形边向量、视线方向 $-w$、光照方向等全部由它而来。

## 2. 内积（dot product）

$$\vec a\cdot\vec b=\sum_i a_ib_i=\lVert\vec a\rVert\,\lVert\vec b\rVert\cos\theta$$

性质：交换律、分配律、正向量自内积为正；$\vec a\perp\vec b \iff \vec a\cdot\vec b=0$。

两大用途：

1. **判角度**：单位向量内积 = $\cos\theta$，>0 锐角、=0 垂直、<0 钝角。
   L14 的 Lambert 漫反射 $I\propto\cos\theta=\hat n\cdot\hat l$ 就是它。
2. **做投影**：$\vec b$ 在 $\vec a$ 方向上的投影
   $$\mathrm{proj}_{\vec a}\vec b=\frac{\vec a\cdot\vec b}{\vec a\cdot\vec a}\,\vec a$$
   点在直线/平面上的投影、 Gram-Schmidt 正交化（18.06）、L06 透视除法都靠它。

## 3. 外积（cross product）

$$\vec a\times\vec b=(a_2b_3-a_3b_2,\;a_3b_1-a_1b_3,\;a_1b_2-a_2b_1),\quad
\lVert\vec a\times\vec b\rVert=\lVert\vec a\rVert\lVert\vec b\rVert\sin\theta$$

- 结果同时垂直于两输入向量，方向由**右手定则**决定。
- 模长 = 两向量张成平行四边形的**面积** → L08 重心坐标的三角形面积公式、
  L10 法向量计算（三角形两边叉积）都建立在这之上。
- 反交换：$\vec a\times\vec b=-\vec b\times\vec a$；共线时为零向量。
- 叉积只在 3 维（与 7 维）有良好定义，这是它和 2D "伪标量叉积" $a_xb_y-a_yb_x$ 的区别。

## 4. 线性相关、基与 span

$n+1$ 个 $n$ 维向量必线性相关。向量组的 **span** 是它们所有线性组合；
**基（basis）** 是 span 的"最小不冗余表示"——同一空间的基不唯一，
**坐标依赖基的选择**，这句话直接预告了 L04–L05 的"变换 = 换基/换坐标系"观点，
以及 L06 视图变换（世界基 → 相机基）。18.06 的四个基本子空间在此完全复用。

## 5. 与前后续讲的联系

- 向量 → L03 矩阵（矩阵是向量的函数）→ L04–L06 变换（矩阵是坐标系的搬运）。
- 内积判可见性：L16 光线求交中 $\vec d\cdot(\vec o-\vec c)$ 之类的符号判断随处可见。
- 外积造法线：L14 着色、L08 半平面测试（边函数 $e=\vec{AB}\times\vec{AP}$ 的 z 分量）
  本质都是叉积。

## 6. 跨课程联系

- **18.06**：本讲就是 18.06 前四讲的几何化重述；特征值在 L05 旋转矩阵、
  L11 二次曲面分类中复用。
- **CS231n**：图像 = 高维向量，卷积/内积是特征匹配；点积相似度是检索与注意力的原型。
- **DDCA/CSAPP**：GPU 顶点着色器一条指令同时做 3–4 个分量的乘加（SIMD），
  向量运算在硬件上是原生并行——这解释了为什么图形 API 用 vec3/vec4 作为基本类型。
- **CS149**：并行光追把"每像素一条光线"映射到 SIMD lane，向量类型即 SIMD 寄存器布局。

## 7. 开源项目中的应用

- **GLSL/HLSL**：`dot()`、`cross()`、`normalize()`、`reflect()` 为内建函数，
  与本课公式一字不差。
- **Three.js**：`THREE.Vector3` 的 `dot/cross/project` 即本课内容（`project` 用到 L06 投影）。
- **Filament / Blender**：材质节点里的 Dot Product、Cross Product 节点。
- **raytracing-in-one-weekend**：`vec3` 类型只有本讲运算，全书 500 行靠它撑起。

## 8. 延伸阅读与自查

- 阅读：FCG4 App. B；18.06 Lecture 1–4；3Blue1Brown《线性代数的本质》第 1–5 集。
- 自查：
  1. 已知三角形 $A,B,C$，如何用一次叉积同时得到法线方向的二倍有向面积？
  2. 为什么"点减点得向量、向量加向量仍为向量"，但"点加点"在仿射几何中不合法？
     （预告：齐次坐标，L03。）
  3. $\vec a\cdot\vec b$ 与 $\vec a\times\vec b$ 各自丢掉了对方保留的哪些信息？
