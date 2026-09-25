# projects/ — 微积分配套小项目计划（本轮只列计划，不写代码）

语言选择原则：数学基础课重在"用代码验证直觉"，统一用 **Python + NumPy/Matplotlib/SymPy**（18.02 场论部分可选 **Julia**，与 18.330 共用工具链）。

| 章节 | 建议语言 | 小项目 | 编译 / 运行方式 |
| --- | --- | --- | --- |
| L1–L3 极限与求导 | Python | `deriv_viz.py`：数值差分近似导数，比较 h→0 时中心差分与前向差分的误差曲线 | `python deriv_viz.py`（无需编译） |
| L6 线性近似 | Python | `newton_root.py`：牛顿法求根，统计收敛阶与失败初值分形图 | `python newton_root.py` |
| L9–L13 积分 | Python | `riemann_quad.py`：Riemann 和 vs 梯形 vs Simpson 求 π/ln2，给出误差阶表 | `python riemann_quad.py` |
| L14–L16 ODE 与级数 | Python | `ode_vibr.py`：阻尼振子三类解绘图 + 泰勒多项式逼近 e^x/sin x 的收敛半径实验 | `python ode_vibr.py` |
| L17–L22 梯度与约束极值 | Python | `grad_descent_lagrange.py`：梯度下降 vs 拉格朗日乘子法求条件极值，画等值面与梯度场 | `python grad_descent_lagrange.py` |
| L23–L24 重积分 | Python / Julia | `montecarlo_vol.py`：Monte Carlo 估计球体积、验证 Jacobi 行列式换元 | `python montecarlo_vol.py` / `julia montecarlo_vol.jl` |
| L25–L28 场论 | Python | `flux_stokes.py`：数值验证 Green/Stokes/散度定理（网格上求线积分与面积分对比） | `python flux_stokes.py` |
| 综合 | Julia | `calculus_check.jl`：用 ForwardDiff/Zygote 对 10 个手工求导结果做自动微分交叉验证 | `julia --project=. calculus_check.jl` |

约定（与全工程一致）：
- 每个项目独立可跑，自带 `run.sh` 或文件头注释写明依赖；
- 依赖统一写在 `projects/requirements.txt`（numpy / scipy / matplotlib / sympy）；
- **本轮不写代码、不编译**，由用户后续集中执行。
