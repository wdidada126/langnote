# papers.md — MIT 18.330 数值分析文献

## 一、经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Cooley & Tukey, *An Algorithm for the Machine Calculation of Complex Fourier Series* | 1965 | FFT：把 DFT 从 O(n²) 降到 O(n log n)，数值时代的引擎 | L17 |
| Wilkinson, *The Algebraic Eigenvalue Problem*（与其误差分析论文族） | 1963/1965 | 确立后向误差分析范式；QR 算法的稳定性论证 | L3, L10, L13 |
| Householder, *Unitary Triangularization of a Nonsymmetric Matrix* | 1958 | 反射式正交三角化，QR 分解的数值标准做法 | L11, L13 |
| Golub & Reinsch, *Singular Value Decomposition and Least-Squares Solutions* | 1970 | 实用的 SVD/最小二乘算法（与 Kahan 1965 一同奠基） | L11, L14 |
| Lanczos, *An Iteration Method for the Solution of the Eigenvalue Problem of Linear Differential and Integral Operators* | 1950 | Krylov 子空间方法的起点，现代迭代求解器祖先 | L12, L13 |
| Hestenes & Stiefel, *Methods of Conjugate Gradients for Solving Linear Systems* | 1952 | 共轭梯度法：对称正定系统的 Krylov 最优迭代 | L12 |
| Runge, *Über die empirischen Formeln…* / Kutta 相关工作 | 1895/1901 | 高阶龙格–库塔法与数值误差的早期系统研究 | L15 |
| Levenberg, *A Method for the Solution of Certain Non-Linear Problems in Least Squares* / Marquardt | 1944/1963 | 非线性最小二乘的阻尼牛顿法（LM 算法） | L8–L11 |
| Crank & Nicolson, *A Practical Method for Numerical Evaluation of Solution of Partial Differential Equations* | 1947 | 抛物型 PDE 的隐式差分格式，无条件稳定的经典设计 | L18 |
| Metropolis, Rosenbluth, Rosenbluth, Teller & Teller, *Equation of State Calculations by Fast Computing Machines* | 1953 | MCMC 起点，蒙特卡洛从"随机抽样"走向"构造链" | L19 |
| Kahan, *Further Comments on a Matrix Inversion Algorithm* / 迭代精化 | 1965 | 残差迭代精化与浮点误差的严格记账 | L2, L10 |
| de Boor, *On Calculating with B-Splines* | 1978 | B 样条稳定算法，现代 CAD/仿真插值的基础 | L5 |

## 二、近 5 年（2021–2026）论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Vineyard, Bordas, Flyer 等, *Scalable Nonstiff ODE Solvers in Julia*（JMSS） | 2021 | SciML 生态的大规模/并行 ODE 求解与性能工程化 | L15, L16 |
| *A Unified and Performant GPU Programming Model in Julia*（CUDA.jl/KernelAbstractions 一族, 2023） | 2022–2023 | 用 Julia 抽象获得接近 CUDA 的 GPU 数值性能 | L1, L12, L17 |
| Li et al., *Fourier Neural Operator*（ICLR 2021 及后续 PDE-Bench 等基准） | 2021–2024 | 用谱方法结构学 PDE 解算子，FFT 成为网络层 | L17, L18 |
| 混合精度与可重现性研究（如 *Reproducibility in HPC* 系列、mixed-precision iterative refinement 论文族） | 2021–2025 | 在 bf16/fp16 下重估稳定性与误差控制，FP8 训练落地 | L2, L3, L10 |
| 随机化数值线性代数（randomized NLA / sketching）综述与新算法 | 2022–2024 | 用采样把 SVD/最小二乘降到近线性代价并给概率保证 | L11, L14 |
| Differentiable simulation / adjoint 方法（SciML `DiffEqSensitivity.jl`、`GSFlow`/Brax 一族） | 2021–2024 | ODE/PDE 求解器作为可微层，反向模式伴随给梯度 | L15–L16, L7 |
| LLM 训练的数值稳定性分析（loss spike、bf16 溢出、缩放策略论文族） | 2022–2025 | 把大规模并行下的浮点归约顺序与数值病态联系到训练崩溃 | L2, L3, L12 |

## 三、知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 具体用法 |
| --- | --- | --- |
| 浮点与数值稳定 | `numpy/numpy`（`longdouble`、`errstate`）, `JuliaLang/julia`（`Float16/BFloat16`） | 混合精度训练与数值诊断的底层支持 |
| 插值与样条 | `SciPy/SciPy`（`scipy.interpolate`）, `JuliaMath/Interpolations.jl`, `FINUFFT` | 网格重采样、CFD 插值、地图/影像配准 |
| 求积与数值积分 | `JuliaMath/FastGaussQuadrature.jl`, `scipy.integrate`, `quadpy/autograd` | 有限元质量矩阵、概率归一化常数 |
| 求根与优化 | `JuliaNLSolvers/BlackBoxOptim.jl`, `scipy.optimize`, `nlopt` | 非线性方程组、参数标定、PDE 约束优化 |
| 直接法与稀疏线性代数 | `libigl/eigen`（Eigen）, `PETSc/petsc`, `SuiteSparse/CHOLMOD` | 电路仿真、结构力学、内点法每次迭代的线性求解 |
| 迭代法与预条件 | `JuliaSmoothOptimizers/Krylov.jl`, `ARPACK-ng`, `Ginkgo-project/ginkgo`（GPU） | 大规模特征值与 PDE 求解内核 |
| 特征值与 SVD | `ARPACK-ng/ARPACK-ng`, `lapack`, `RandomizedSVD.jl` | 谱聚类、PCA、振动模态分析 |
| ODE/PDE 求解 | `SciML/DifferentialEquations.jl`, `petsc/petsc`, `FEniCS/dolfinx`, `dealii` | 物理仿真、生物模型、气候与流体 |
| FFT | `FFTW`, `cuFFT`（`NVIDIA/cuda-python`）, `JuliaMath/FFTW.jl`, `pocketfft` | 谱方法、卷积、音频/图像处理 |
| 随机数与蒙特卡洛 | `JuliaRandom/Random123.jl`, `numpy/numpy`（PCG64）, `scipy.stats.qmc` | 可并行可复现的计数器式随机流、QMC 积分 |
| 可微分仿真 | `SciML/SciMLSensitivity.jl`, `google/brax`, `jax-ml/jax` | 梯度式物理参数估计、机器人与科学机器学习 |
