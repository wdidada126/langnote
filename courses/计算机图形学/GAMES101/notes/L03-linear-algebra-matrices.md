# L03 数学基础（下）：矩阵、线性变换与齐次坐标

> 对应 README 讲次 L03；官方 Lecture 02（后半）–03（前半）。阅读：FCG4 Ch.2、Ch.4.2。

## 1. 矩阵 = 向量的线性函数

$m\times n$ 矩阵是 $m$ 行 $n$ 列的数组；对向量作用：

$$M\vec v=\begin{bmatrix}r_1\cdot\vec v\\ r_2\cdot\vec v\\ \vdots\end{bmatrix}
\quad(\text{行的观点：输出第 }i\text{ 个分量}=r_i\cdot\vec v)$$
$$M\vec v=c_1v_1+c_2v_2+\dots\quad(\text{列的观点：输出}=输入分量的列线性组合)$$

两个观点在 L04–L05 会分别兑现价值：**行观点**适合推导矩阵-向量乘法；
**列观点**揭示"矩阵的列 = 基向量的像"——这是理解一切变换矩阵的钥匙。

## 2. 矩阵乘法与变换复合

$$C=AB\iff c_{ij}=a_i\cdot b^j\quad(A\text{ 第 }i\text{ 行}\cdot B\text{ 第 }j\text{ 列})$$

$C\vec x=A(B\vec x)$：先做 $B$ 再做 $A$。矩阵乘法**不交换**（$AB\neq BA$），
因为变换复合不交换：先转后移 ≠ 先移后转（L04 的 MVP 顺序问题根源）。
满足结合律 → 复合变换可以预先乘成一个矩阵，这正是 GPU 每帧只传一个
`mat4 uniform` 的原因。

## 3. 线性变换

$T(\vec a+\vec b)=T\vec a+T\vec b,\;T(c\vec a)=cT\vec a$。任何线性变换都可写成矩阵乘法。
二维线性变换的几何分类（对应 18.06 的特征值视角）：

- **伸缩**（scaling）：对角矩阵。
- **旋转**（rotation）：$R_\theta=\begin{bmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{bmatrix}$，
  保长度保角度；$R_\theta$ 作用在基 $\{1,i\}$ 上等价于复数乘 $e^{i\theta}$（直觉：旋转=乘 $e^{i\theta}$）。
- **剪切**（shear）：$\begin{bmatrix}1&\lambda\\0&1\end{bmatrix}$，面积不变但形状歪斜。
- **反射**（reflection）：行列式为 $-1$ 的正交变换。
- **投影**（projection）：奇异矩阵，把平面压到直线/点（不可逆，L06 透视投影也有此性质）。

## 4. 齐次坐标（homogeneous coordinates）

**平移不是线性变换**（$T(0)\neq0$），只是仿射变换。补救办法：把 2D 点
$(x,y)$ 升到 3D $(x,y,1)$，则

$$\begin{bmatrix}1&0&t_x\\0&1&t_y\\0&0&1\end{bmatrix}\begin{bmatrix}x\\y\\1\end{bmatrix}
=\begin{bmatrix}x+t_x\\y+t_y\\1\end{bmatrix}$$

一般规则：**点 $(x,y,1)$，向量 $(x,y,0)$**。$w$ 分量的意义：

- 点+向量=点、点−点=向量，平移矩阵作用于向量（$w=0$）恰好无效——语义自洽。
- $w\neq1$：$(x,y,w)\equiv(x/w,\,y/w,\,1)$。L06 的透视除法 `z = z/w` 即源于此：
  透视投影把 $w$ 设为 $-z$，除法后完成近大远小的非线性压缩。

## 5. 与前后续讲的联系

- 本讲给出"矩阵语言"，L04–L06 全部用它书写变换；L05 的求逆、
  L11 的四元数（仍属旋转群）都建立在此。
- 齐次坐标 → L06 透视投影矩阵（本质是 $4\times4$ 分块矩阵，右上角的 $-1$ 使 $w=-z$）。
- 列观点预告：视图矩阵的三列就是相机三个轴在世界系下的方向（L05 lookAt）。

## 6. 跨课程联系

- **18.06**：本讲 = Lecture 1–8 的图形学重述。矩阵求逆、行列式、特征值、
  正交矩阵直接复用；L05 的万向锁在数学上是"旋转群 SO(3) ≠ $\mathbb R^3$"的坐标奇异问题。
- **CS231n / 生成模型**：NeRF 的位置编码 $\gamma(x)$ 是对坐标做非线性变换后再喂网络；
  3DGS 的协方差矩阵 $Σ=RR^Tss^T$ 把高斯椭球的"旋转+缩放"写回矩阵乘法（与本讲同一语言）。
- **DDCA/CSAPP**：GPU 的一个 warp 并行做矩阵乘法分块；变换矩阵是顶点着色的
  第一条"指令流"。

## 7. 开源项目中的应用

- **GLM（Three.js/Filament 内部风格）**：`glm::mat4`、`translate/rotate/scale`、
  `perspective/ortho/lookAt` 与本讲公式一一对应，可当作"标准答案"对照。
- **WebGL**：顶点着色器中 `gl_Position = projection * modelView * vec4(pos,1.)` 的
  顺序就是变换复合顺序。
- **PBRT-v4**：`Transform` 类型同时存储正逆矩阵（对应本讲求逆，L05）。

## 8. 延伸阅读与自查

- 阅读：FCG4 Ch.4.2；18.06 Lecture 2/6/21；《游戏引擎架构》Ch.5（数学与物理）。
- 自查：
  1. 为什么 $2\times2$ 矩阵无法表示平移？给出维度计数论证。
  2. 计算 $R_{90^\circ}T_{(1,0)}$ 与 $T_{(1,0)}R_{90^\circ}$ 作用在原点的差别。
  3. $(4,6,2)$ 在齐次坐标下是哪个 2D 点？
