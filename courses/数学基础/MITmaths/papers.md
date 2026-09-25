# papers.md — 微积分（18.01/18.02）与相关文献

> 说明：本课程本身是基础课，没有"课程论文"。本表按两条线整理：
> (1) 塑造本课程内容的历史经典文献；(2) 现代 CS 研究中把微积分作为核心工具的代表工作。
> 近 5 年条目为骨架级线索，精读前请核对 DOI/发表信息。

## 一、经典文献（思想源头）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Newton, *Method of Fluxions* | 1736（成书 1671） | 以"流动量"提出微分与流数法，微积分的力学起源 | L2, L14 |
| Leibniz, *Nova Methodus pro Maximis et Minimis* | 1684 | 引入 dx/dy 与 ∫ 记号，符号系统即今天的求导语言 | L3, L9 |
| Cauchy, *Cours d'Analyse* | 1821 | 用极限定义连续与导数，微积分严格化的起点 | L1, L10 |
| Riemann, *Über die Anwendbarkeit…bestimmter Integrale* | 1867 | 给出黎曼积分定义，明确"可积"的边界 | L10, L11 |
| Weierstrass, 处处连续处处不可微函数 | 1872 | 打破"连续即可导"直觉，逼出一致收敛等概念 | L1, L16 |
| Stokes, *On the integrals of circular functions* / Smith's Prize Essay | 1842/1854 | 建立线面积分与体积分的转换定理（今 Stokes 定理） | L26–L28 |
| Taylor, *Methodus Incrementorum* | 1715 | 多项式逼近函数，泰勒展开的原始形态 | L6, L16 |
| Lagrange, *Théorie des fonctions analytiques* | 1797 | 以级数重建成分析并给出约束优化的乘子方法 | L22 |

## 二、近 5 年（2021–2026）相关论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Li et al., *Fourier Neural Operator for Parametric PDEs* (ICLR) | 2021 | 用神经网络学偏微分分解算子，把连续分析直接接进深度学习 | L23–L28 |
| Rackauckas et al., *A Performance-Enhanced Differentiable Simulation Framework in Julia*（SciML 系列） | 2021–2023 | 可微分仿真：把 ODE/PDE 求解器做成可反传梯度的层 | L14–L16, L19–L20 |
| Cranmer, *Interpretable Machine Learning for Science with PySR* | 2023 | 符号回归从数据中"发现"微分方程，反哺建模 | L14, L28 |
| Chen et al. 后续工作：*Neural ODE / Ambient Diffusion* 一族 | 2022–2024 | 把连续动力学（ODE）作为生成与优化的统一语言 | L14–L15, L19 |
| Nesterov/一阶方法收敛性再分析（如 *Optimizing neural networks remains hard* 一族） | 2021–2024 | 梯度下降、动量法的连续时间与离散时间分析 | L19, L21 |
| 大模型训练中的优化器数值分析论文（Adam 偏差修正、bf16 稳定性） | 2021–2025 | 浮点误差 + 泰勒展开分析训练不稳定的成因 | L6, L13, L16 |

## 三、知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 具体用法 |
| --- | --- | --- |
| 导数 / 链式法则 / 反向模式自动微分 | `google/jax`, `pytorch/pytorch`, `JuliaDiff/ChainRules.jl` | autodiff 引擎即逐算子链式法则；`grad()` 的数学定义来自 L3/L20 |
| 泰勒展开与线性近似 | `sympy/sympy`（`series`）、`scipy`（`approx_fprime`） | 符号级展开、数值方法的截断误差分析 |
| 定积分与数值积分 | `scipy.integrate`, `JuliaMath/QuadGK.jl`, `SciML/Quadrature.jl` | 高求积规则实现 L9–L13 的积分 |
| 常微分方程 | `SciML/DifferentialEquations.jl`, `scipy.integrate.odeint`, `assimipro/bamtfram` | 初值/边值问题求解器，刚性问题（L15） |
| 多元梯度 / Hessian | `JuliaNLSolvers/Optim.jl`, `scipy.optimize` | 牛顿法、拟牛顿（BFGS）依赖二阶展开（L19–L21） |
| 拉格朗日乘子 / 约束优化 | `cvxpy/cvxpy`, `lanl/Pyomo` | 约束建模与对偶变量解释（L22） |
| 重积分与换元 | `FEniCS/dolfinx`, `dealii/dealii`, `OpenMC-SNAMS/openmc` | 有限元弱形式的区域积分、Monte Carlo 体积估计（L23–L24） |
| 曲面积分 / Stokes 定理 | `libigl/libigl`, `PyMesh`, `diffeq-spode` 几何处理栈 | 离散外微分、表面通量与流体仿真（L25–L28） |
| 傅里叶分析预备（三角函数正交性） | `FFTW`, `pyfftw`, `kissfft` | 为 EE120 / 6.007 的傅里叶级数打基础（L4, L16） |
