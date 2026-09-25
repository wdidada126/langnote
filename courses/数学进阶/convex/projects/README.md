# projects/ — EE364A 配套小项目计划（本轮只列计划，不写代码）

语言：**Python + CVXPY**（与课程作业一致）；算法实现部分用 Python/NumPy，性能敏感处可选 **Julia**（`JuMP.jl`）。

| 章节 | 建议语言 | 小项目 | 编译 / 运行方式 |
| --- | --- | --- | --- |
| L2–L4 建模 | Python | `model_bank.py`：10 个小问题（生产计划、最小包围椭球、稀疏恢复）写成 LP/QP/SOCP，并给出"为什么是凸的"的注释 | `python model_bank.py` |
| L6–L9 对偶与 KKT | Python | `duality_hand.py`：手写拉格朗日对偶并用 SymPy 验证强对偶；打印影子价格随约束右端的变化 | `python duality_hand.py` |
| L10 SVM 对偶 | Python | `svm_from_dual.py`：对偶 QP + 核技巧实现软间隔 SVM，与 `sklearn.svm.SVC` 对比 | `python svm_from_dual.py` |
| L12 梯度法 | Python | `first_order_bench.py`：GD / 动量 / Nesterov / 共轭梯度在条件数扫描下的收敛曲线 | `python first_order_bench.py` |
| L13–L14 牛顿与内点 | Python | `ipm_log_barrier.py`：对数障碍内点法解 LP（自实现 Newton 步），报告中心路径与迭代数 | `python ipm_log_barrier.py` |
| L15 ADMM | Python / Julia | `admm_lasso.py` / `admm_lasso.jl`：Lasso 的近端算子与 ADMM 分解，含分布式（列切分）版本 | `python admm_lasso.py` / `julia --project=. admm_lasso.jl` |
| L16 拟合与正则 | Python | `robust_fit.py`：L2 / Huber / L1 拟合对比，注入异常点观察鲁棒性 | `python robust_fit.py` |
| L17 统计估计 | Python | `mle_convex.py`：逻辑回归/泊松 MLE 的凸性验证与 Newton 求解，画 Fisher 信息椭圆 | `python mle_convex.py` |
| L19 凸松弛 | Python | `maxcut_sdp.py`：Max-Cut 的 SDP 松弛 + 随机超平面舍入，测近似比经验分布 | `python maxcut_sdp.py` |
| 综合 | Python | `mpc_tank.py`：模型预测控制倒立摆/水箱，QP 求解 + 双重循环实时性测试 | `python mpc_tank.py` |

约定：
- 依赖写入 `projects/requirements.txt`（cvxpy、numpy、scipy、matplotlib、scikit-learn、sympy）；
- 求解器统一指定 `ECOS`/`OSQP`/`Clarabel`，失败时打印求解器返回码；
- **本轮不写代码、不编译**，由用户后续集中执行。
