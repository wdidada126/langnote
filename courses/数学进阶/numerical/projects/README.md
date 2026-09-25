# projects/ — MIT 18.330 配套小项目计划（本轮只列计划，不写代码）

语言：**Julia**（本课核心要求，全部算法自己实现一遍再用库对拍）；性能对照可用 C/Fortran 可选。
每个项目独立目录，带 `Project.toml` + `run.jl`。

| 章节 | 建议语言 | 小项目 | 编译 / 运行方式 |
| --- | --- | --- | --- |
| L2–L3 浮点与条件 | Julia | `float_lab.jl`：机器精度测量、二次方程两种求根的误差对比、病态 Vandermonde 条件数曲线 | `julia --project=. -e 'include("float_lab.jl")'` |
| L4–L5 插值 | Julia | `interp_lab.jl`：等距 vs 切比雪夫节点 Runge 现象绘图；三次样条 vs PCHIP | `julia interp_lab.jl` |
| L6 求积 | Julia | `quadrature.jl`：梯形/Simpson/Gauss–Legendre 的收敛阶实验 + Romberg 外推 | `julia quadrature.jl` |
| L8–L9 求根 | Julia | `rootfind.jl`：二分/Newton/割线基准，画出收敛阶与吸引域分形 | `julia rootfind.jl` |
| L10–L12 线性代数 | Julia | `linsolve_bench.jl`：LU vs QR vs CG 解同一稀疏问题，报告残差、耗时与条件数影响 | `julia --threads=8 linsolve_bench.jl` |
| L13–L14 特征值/SVD | Julia | `eig_svd.jl`：手写幂法与 QR 迭代，图像低秩压缩并与 `LinearAlgebra`/`RandomizedSVD` 对拍 | `julia eig_svd.jl` |
| L15–L16 ODE | Julia | `ode_stiff.jl`：Euler/RK4 与隐式方法在刚性问题上的稳定区域实测 | `julia ode_stiff.jl` |
| L17 FFT | Julia | `fft_from_scratch.jl`：递归 FFT + 频域卷积 vs `FFTW.jl` 性能与精度比较 | `julia fft_from_scratch.jl` |
| L18 PDE | Julia | `heat_1d.jl`：显式（CFL 限制）与 Crank–Nicolson 解一维热方程 | `julia heat_1d.jl` |
| L19 蒙特卡洛 | Julia | `mc_integrate.jl`：MC vs QMC 高维积分，方差缩减收益量化 | `julia mc_integrate.jl` |
| 综合 | Julia | `sciml_mini.jl`：把上述 ODE 求解器包成可微层，用 Zygote 反传拟合参数 | `julia --project=. sciml_mini.jl` |

约定：
- 统一 `Manifest.toml` 锁版本以保证可重现（呼应 L20 可重现性）；
- 结果输出到 `out/`（CSV + PNG），便于对比"精度预算表"；
- **本轮不写代码、不编译**，由用户后续集中执行。
