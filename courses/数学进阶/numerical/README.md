# MIT 18.330 数值分析导论

> 状态：**骨架**

## 一、课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 / 课程号 | MIT 18.330 Introduction to Numerical Analysis（数值分析导论）；数学系应用方向，同名 18.335 为其进阶版 |
| 学校 | Massachusetts Institute of Technology |
| 主讲 | Steven G. Johnson（MIT 数学系/applied math，FFTW/Arpack/MeasureTransport 作者）；课程由 MIT math 数值组维护（同方向讲授者含 Alan Edelman、Ralph Abraham 等） |
| 教材 | Barba, Gervasio, Johnson, Slevinsky 等编写, *Fundamentals of Numerical Computation*（开源教材 fncbook.com，含大量 Julia 实例）；参考 Trefethen & Bau《Numerical Linear Algebra》、Quarteroni《Numerical Mathematics》 |
| csdiy 路径 | `数学进阶/numerical` |
| 最新期次 | 课程仓库 `github.com/mitmath/18330` 持续更新；**2025 年更新版**沿用 Fall 2024/Spring 2025 排期（作业为 10 个 Julia 编程作业，作业仓库 mitmath/18FINL 与 18330 的 `homeworks/`） |
| 先修要求 | 微积分、线性代数、概率论（csdiy 标注） |
| 难度 / 学时 | 🌟🌟🌟🌟🌟 ／ 约 150 小时 |
| 编程语言 | **Julia**（本课最大特色：全部算法自己实现一遍，再用 Julia 的高层抽象组织） |
| 状态 | 骨架 |

## 二、为什么学

1. **把"连续世界"翻译成"离散计算"的必修课**：浮点表示、逼近、误差、稳定性——所有科学计算、图形仿真、机器学习数值稳定性的地基。
2. **三步方法论贯穿全课**：如何建立估计 → 如何估计误差 → 如何用算法实现估计。这套思维方式对写高性能/高可靠代码同样适用。
3. **Julia 语言的最佳教材级实践**：多重派发、类型系统、性能与可读性兼得；学完能直接读懂 DifferentialEquations.jl / SciML 生态源码。
4. 是 18.335、GAMES202/101（几何与仿真）、CMU 10-414（数值后端）、6.5940（高效计算）的先修级准备。

## 三、先修与知识联系

```
18.01/18.02 微积分（泰勒、积分、ODE） + 18.06 线性代数（子空间、正交性、特征值、SVD） + 概率论（蒙特卡洛）
        │
        ▼
   18.330 数值分析（Julia）
        │
        ├──► MIT 18.335 高等数值方法（大规模、并行、PDE）
        ├──► 图形学 GAMES101/202/15-462：插值、几何、刚体与流体求解
        ├──► 深度学习 10-414 / 6.5940：优化器、混合精度、自动微分的数值本质
        ├──► CS229 / EE364A：最小二乘、特征值、迭代法与条件数
        ├──► 体系结构 / 并行 CS61C、15-418：BLAS 层级、缓存、数值可重现性
        └──► SciML / 物理仿真（DifferentialEquations.jl、FluidDyn.jl）
```

| 关联课程 | 用到的本课程内容 |
| --- | --- |
| 数学基础/MITLA | 正交化与 QR、特征值/奇异值、范数与条件数 |
| 数学基础/MITmaths | 泰勒展开（截断误差）、积分、ODE 理论解 |
| 数学进阶/convex | 梯度/牛顿法、最小二乘、KKT 的数值求解 |
| 数学进阶/CS126、6.042J | 随机数、蒙特卡洛积分与方差缩减 |
| 电子基础/signal、6.007 | FFT 的推导与应用（插值 + 谱方法） |
| 机器学习进阶 | Adam/混合精度、可微分编程（differentiable programming） |

## 四、最新年份（2025 更新版 / fncbook 章节顺序）讲义章节目录（骨架）

阅读材料：`FNC` = *Fundamentals of Numerical Computation* 章节；HW = Julia 编程作业（共 10 个）。

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论与 Julia 速览（类型、多重派发、性能） | FNC 前言/Ch.1；HW1 |
| L2 | 浮点数与机器精度：表示、舍入、灾难性消除 | FNC Ch.1；HW1 |
| L3 | 条件数与稳定性：问题与算法要分开评价 | FNC Ch.1 |
| L4 | 多项式插值：Lagrange、Newton、Runge 现象 | FNC Ch.2；HW2 |
| L5 | 样条与分段插值、单调性与形状保持 | FNC Ch.2 |
| L6 | 数值积分（求积）：Newton–Cotes、高斯求积、误差阶 | FNC Ch.3；HW3 |
| L7 | 数值微分：有限差分、Richardson 外推与最优步长 | FNC Ch.7 |
| L8 | 非线性求根：二分、Newton、割线、收敛阶分析 | FNC Ch.4；HW4 |
| L9 | 方程组求解：牛顿法推广、同伦与拟牛顿入门 | FNC Ch.4 |
| L10 | 线性方程组：Gauss 消元、LU、选主元与稳定性 | FNC Ch.5；HW5 |
| L11 | 正交性与最小二乘：QR、Cholesky、正规方程的取舍 | FNC Ch.5 |
| L12 | 迭代法：Jacobi/Gauss–Seidel/共轭梯度与预条件 | FNC Ch.5–6 |
| L13 | 特征值算法：幂法、正交迭代、QR 算法与收缩 | FNC Ch.6；HW6 |
| L14 | SVD 与低秩近似、PCA、伪逆的数值实现 | FNC Ch.6 |
| L15 | 常微分方程初值问题：Euler、Runge–Kutta、局部/全局误差 | FNC Ch.7；HW7 |
| L16 | 刚性问题与稳定性区域、自适应步长与事件检测 | FNC Ch.7 |
| L17 | FFT 与快速多项式运算：Cooley–Tukey、卷积、谱插值 | FNC Ch.8；HW8 |
| L18 | 高维插值、边值问题与偏微分方程离散（有限差分到谱方法） | FNC Ch.9；HW9 |
| L19 | 随机数生成与蒙特卡洛积分、方差缩减 | FNC Ch.10；HW10 |
| L20 | 数据分析与总结：可重现性、精度预算、方法论回顾 | FNC Ch.11 + 复盘 |

## 五、学习产出（待填充时勾选）

- [ ] 每讲笔记展开（含 Julia 代码片段与收敛阶表）
- [ ] 10 个 Julia 作业的完成记录（`projects/` 中列目录）
- [ ] `papers.md` 阅读状态标注
- [ ] 自制一张"方法 → 误差阶 → 稳定性风险"速查表
