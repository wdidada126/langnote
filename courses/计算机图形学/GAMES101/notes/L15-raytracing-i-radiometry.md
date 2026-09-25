# L15 光线追踪（一）：辐射度量学、蒙特卡洛与渲染方程

> 对应 README 讲次 L15；官方 Lecture 15–17（Radiometry / Monte Carlo / Light Transport I–II）。
> 阅读：FCG4 Ch.14、Ch.26–28。实践：projects/p4。

## 1. 为什么需要"光的会计学"：辐射度量学

渲染 = 能量守恒的记账。一套层层导数的单位体系：

| 量 | 符号 | 单位 | 定义 |
| --- | --- | --- | --- |
| 辐射能 | $Q$ | J | 光子总能量 |
| 辐射通量 | $\Phi=dQ/dt$ | W | 单位时间能量 |
| 辐射强度 | $I=d\Phi/d\Omega$ | W/sr | 点源在某立体角方向的密度 |
| 辐照度 | $E=d\Phi/dA$ | W/m² | 单位**受光面积**收到的通量 |
| 辐射率 | $L=d^2\Phi/(dA^\perp d\Omega)=\frac{d^2\Phi}{\cos\theta\,dA\,d\Omega}$ | W/(m²·sr) | 单位投影面积单位立体角 |

两个关键 $\cos$ 因子：受光面斜放 → 照度衰减（∝$\cos\theta$，Lambert 定律的
物理源头）；发光面斜看 → 投影面积缩小。

**辐射率 L 的杀手级性质：真空中沿光线传播不变**（截面积按 $r^2$ 增大、
立体角按 $1/r^2$ 缩小、介质吸收暂不计 → 两者精确相消）。
正因 L 守恒，**像素颜色 ∝ 从该像素出发沿光线到达的 L** —— 光线追踪
"反向追踪"合法性的全部依据（L16 展开）。这也是为什么亮度（luminance）
是显示器/摄影测量的核心量。

## 2. 立体角与微元

$d\Omega$ = 单位球上截出的面积 = 方向空间的"面积元"。半球积分
$\int_{\Omega}d\omega=2\pi$，全空间 $4\pi$。渲染方程里的 $\int_{\Omega}(\cdots)d\omega$
因此就是"对所有来向加权求和"。

## 3. 蒙特卡洛积分：用随机数算积分

估计 $I=\int_a^b f(x)dx$：均匀采样 $N$ 个 $X_i\sim U[a,b]$：

$$\hat I=\frac{b-a}{N}\sum_{i=1}^N f(X_i),\qquad E[\hat I]=I,\quad
\mathrm{Var}[\hat I]=\frac{(b-a)^2\sigma_f^2}{N}$$

**收敛率 $O(1/\sqrt N)$ 与维数无关** —— 高维积分（渲染方程是 4–5 重嵌套的
半球积分）的唯一可行武器。方差缩减三板斧：

1. **重要性采样**：按 $\propto|f|$ 的密度 $p$ 采样，估计 $\frac{f(x)}{p(x)}$，
   方差 ∝ $\int\frac{(f-p\cdot I)^2}{p}$；$p\propto|f|$ 时为零方差。
   （cos 加权半球采样 → 对 Lambert 积分零方差，L16 实战。）
2. **对偶变量/分层采样**：一张像素内用低差异序列（Latin hypercube / Sobol）
   替代独立随机数，收敛更快。
3. **多采样整合（MI）**：对几个候选密度做平衡启发式加权（Veach）。

## 4. 渲染方程（Kajiya 1986）

平衡态、出射辐射率：

$$L_o(x,\omega_o)=L_e(x,\omega_o)+\int_{\Omega} f_r(x,\omega_i,\omega_o)\,
L_i(x,\omega_i)\,(\hat n\cdot\omega_i)\,d\omega_i$$

- 左出射 = 自发光 + 所有入射方向经材质 $f_r$（L14 的 BRDF）散射后的加权积分。
- **积分嵌套在无穷递归里**：$L_i$ 又是其他表面上同方程的解
  → 全局光照（间接光、反射、焦散）都在这一行公式内。
- 路径积分视角：把逐次反弹展开，亮度 = 所有光路 $\bar x$ 的贡献和
  （L2 norm 形式的积分）；光栅化是它的"只取 0–1 次反弹 + 屏幕空间近似"特例。
- 与**辐射度方法**（Goral 1984，本讲对照）：辐射度只解漫反射互反射的
  线性方程组 $B=E\rho FB$（form factor 是"可见度×几何"的预计算），
  Kajiya 方程统一了一切——但当时无法求解，直到蒙特卡洛成熟（L16）。

## 5. 与前后续讲的联系

- BRDF 来自 L14，可见性（$\hat n\cdot\omega_i$ 之外还要"挡不挡"）归 L16 求交，
  能量与颜色标定回扣 L13。
- 本讲只立方程不给解法 → L16 路径追踪给出工程解：
  $\hat L_o=L_e+\frac{f_r\,L_i\cos\theta}{p(\omega_i)}$ 的均值估计。
- 光栅化管线（L07–L09）在本讲获得"物理正确性"的度量衡：
  为什么 HDR 缓冲、为什么 tonemap（L13）——都是 L 的会计问题。

## 6. 跨课程联系

- **数学（6.042/概率论 CS126）**：期望/方差/大数定律/中心极限定理全数上场；
  低差异序列是数论的意外应用。
- **18.06**：辐射度线性方程组 $B=(I-\rho F)^{-1}E$ 的解 = Neumann 级数
  $\sum(\rho F)^k$，逐项恰好对应"第 k 次反弹"——线性代数与光传输的绝美接口。
- **CS149**：MC 的 N 样本是 embarrassingly parallel；工业路径追踪按
  (pixel, sample, bounce) 三维线程网格组织。
- **DDCA/CSAPP**：MC 对 RNG 质量敏感——`rand()` 的低周期在 1024 spp 下
  出现相关条纹；xorshift/PCG 是图形学出身（CSAPP 浮点/位运算视角）。
- **统计 ML（CS229/10-708）**：重要性采样、MI、MCMC（Veach 的 MLT 就是
  在光路空间做 MCMC）与变分推断共享同一套数学。

## 7. 开源项目中的应用

- **PBRT-v4**：`Integrator` 类层次 = 本讲方程的各种离散化；`Sampler` 即低差异序列。
- **Blender Cycles**：渲染方程的 CPU/GPU 蒙特卡洛求解器，分层采样 + 降噪。
- **raytracing-glass / projects/p4**：最小路径追踪器，cos 半球采样约 60 行。
- **NVIDIA OptiX/DLSS-RR**：光追 + 神经降噪 = "少采样 MC + 学习先验"的现代答案。

## 8. 延伸阅读与自查

- 阅读：FCG4 Ch.27–28；《Physically Based Rendering》(Pharr-Jakob-Humphreys)
  Ch.6–9（本讲的圣经级展开）；Kajiya 1986 原文（papers.md）。
- 自查：
  1. 证明 L 沿光线不变（用两个球壳的立体角/面积相消）。
  2. Lambert 目标 $\int\frac{\cos\theta}{\pi}L\,d\omega$ 用均匀半球/ cos 加权
     两种采样分别写出估计器并比较方差。
  3. 为什么 16 spp 的图像"糊而噪"、256 spp"锐而净"？用 $1/\sqrt N$ 解释，
     并说明降噪器（OPTIX denoiser）为何能"作弊"。
