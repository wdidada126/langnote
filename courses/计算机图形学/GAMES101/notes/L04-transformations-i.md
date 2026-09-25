# L04 变换（上）：平移、缩放、旋转与复合

> 对应 README 讲次 L04；官方 Lecture 03。阅读：FCG4 Ch.4。实践：projects/p1。

## 1. 2D 基本变换的齐次矩阵

$$\text{平移}=\begin{bmatrix}1&0&t_x\\0&1&t_y\\0&0&1\end{bmatrix},\quad
\text{缩放}=\begin{bmatrix}s_x&0&0\\0&s_y&0\\0&0&1\end{bmatrix},\quad
\text{旋转}=\begin{bmatrix}\cos\theta&-\sin\theta&0\\\sin\theta&\cos\theta&0\\0&0&1\end{bmatrix}$$

绕任意点 $(c_x,c_y)$ 旋转 = 先移到原点、旋转、移回：
$T(c)\,R(\theta)\,T(-c)$。这揭示了本讲最重要的心法：**复杂变换 = 基本变换的复合**。

## 2. 复合顺序：从右往左读

$M=T\cdot R\cdot S$ 作用在点上时，**先缩放、再旋转、最后平移**（矩阵从右往左"消费"）：
$M\vec v = T(R(S\vec v))$。等价记忆法：矩阵乘在左边 = 在前一个变换的**外部坐标系**
（fixed frame）中叠加；乘在右边 = 在**内部/当前物体坐标系**（moving frame）中叠加。
游戏引擎里"父节点变换 × 子节点局部变换"正是右边乘（局部系）的产物，
L05 的万向锁也由此解释。

## 3. 3D 变换与绕轴旋转

3D 基本矩阵同构地扩展到 $4\times4$。绕 $z$ 轴旋转只作用于 $x,y$ 分量（与 2D 相同）；
绕 $x,y$ 轴循环置换：

$$R_z(\alpha)=\begin{bmatrix}\cos\alpha&-\sin\alpha&0&0\\\sin\alpha&\cos\alpha&0&0\\0&0&1&0\\0&0&0&1\end{bmatrix},\;
R_x(\alpha)=\begin{bmatrix}1&0&0&0\\0&\cos\alpha&-\sin\alpha&0\\0&\sin\alpha&\cos\alpha&0\\0&0&0&1\end{bmatrix},\;\dots$$

绕任意轴 $\hat n$ 的旋转可分解为：把 $\hat n$ 对齐到某坐标轴 → 绕该轴转 → 逆变换回去
（Rodrigues 公式是它的闭式解，L05 的指数映射 $\exp([\hat n]_\times\theta)$ 是更现代写法，
详见延伸阅读）。

## 4. 仿射变换的一般结构

任何 $4\times4$ 仿射矩阵形如

$$M=\begin{bmatrix}A_{3\times3}&\vec t\\\vec 0^T&1\end{bmatrix},\quad M\vec p=A\vec p+\vec t$$

$A$ 承担旋转/缩放/剪切，$\vec t$ 承担平移。行列式 $\det M=\det A$ 给出体积缩放比
（负值含反射）。这个分块结构在 L05 求逆时立即派上用场。

## 5. 与前后续讲的联系

- 上一讲给语言（矩阵），本讲给词汇（6 种基本变换），L05 给语法难点
  （3D 旋转的参数化、求逆），L06 把变换用于投影。
- 复合矩阵是 L07 管线的第一站：模型矩阵（顶点动画、骨骼）+ 视图矩阵（摄像机移动）
  + 投影矩阵（MVP）。
- 法线变换是易错点：$A$ 作用于向量后法线不再垂直，需用**逆转置** $(A^{-1})^T$——
  预告 L14 着色的正确性前提。

## 6. 跨课程联系

- **18.06**：行列式 = 面积/体积缩放比在此有直观图像；特征向量 = 旋转不动轴。
- **CS149**：每帧为每个实例算一个 MVP 矩阵上传 constant buffer，是典型的
  "CPU 预处理 + GPU 广播"数据并行模式。
- **DDCA/CSAPP**：矩阵乘在 GPU 上以分块 + 循环展开实现；`float4` 对齐（本讲
  $4\times4$ 的第四行/列常为 0/1）正是 SIMD 宽度的反映。
- **CS231n/神经渲染**：摄像机位姿优化（bundle adjustment、NeRF 的 per-image embedding）
  优化的就是本讲的变换矩阵元素。

## 7. 开源项目中的应用

- **Three.js**：`Object3D.matrix.compose(pos,quat,scale)` = 本讲全部内容；
  `matrixAutoUpdate` 每帧重写矩阵。
- **Blender**：物体属性面板的 Loc/Rot/Scale 即 $T,R,S$ 三块，欧拉/四元数切换
  对应 L05 的参数化之争。
- **Filament/Frostbite**：骨骼动画 = 每顶点对 4 个关节的 $M_i\cdot B_i^{-1}$ 加权复合。
- **projects/p1**：从零实现这些矩阵并画"房子变换图"（见 projects/p1_linalg_transforms）。

## 8. 延伸阅读与自查

- 阅读：FCG4 Ch.4.3–4.6；《3D 数学基础：图形与游戏开发》Ch.3；
  经典博客《Common Math for Games: Quaternions》（Epic 官方教程）。
- 自查：
  1. 写"绕点 (1,2) 旋转 90° 再 x 缩放 2 倍"的矩阵（小心顺序！）。
  2. 为什么 $M=T R S$ 不能等价重排成 $S T R$？
  3. 齐次行 $(0,0,0,1)$ 在仿射矩阵下为何不变？投影矩阵会破坏它吗？
