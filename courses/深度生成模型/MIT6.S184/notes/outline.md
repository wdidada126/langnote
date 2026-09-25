# MIT 6.S184 讲义骨架（outline）

> 每讲要点为骨架级摘录，填充笔记时对照课程教材 *An Introduction to Flow Matching and Diffusion Models* 逐条展开推导线。

## L1 生成模型概览与概率背景
- 生成模型目标：学习数据分布 p_data(x)，从而采样、估计密度或操纵分布
- 复习：条件概率、期望、KL 散度、极大似然估计——全课通用语言
- 生成模型四大家族：VAE / GAN / Flow / 扩散与 Score-based，各自的取舍（密度可算性 vs 采样质量）
- 课程主线预告：用 ODE/SDE 把扩散与流匹配统一起来

## L2 深度学习基础回顾
- 神经网络即参数化向量场/函数；SGD/Adam 训练流程
- 潜变量模型视角：p(x)=∫p(x|z)p(z)dz，难解积分是生成建模核心困难
- VAE 的 ELBO 与 amortized inference 简述
- 为后续"网络学习得分函数/速度场"做铺垫

## L3 常微分方程与连续标准化流（CNF）
- ODE 初值问题、解的存在唯一性、数值积分（Euler、RK）
- Instantaneous change of variables 公式：log p 随时间演化由散度 trace 给出
- CNF = 无限深度的归一化流；训练即学习速度场
- 与离散 Flow（RealNVP/Glow）的极限关系

## L4 随机微分方程基础
- 布朗运动/维纳过程性质；离散化视角
- Ito 引理 vs 链式法则（二阶项的来源）
- 前向 SDE 如何把任意数据分布渐变为高斯（Ornstein-Uhlenbeck 例子）
- Fokker-Planck 方程：分布密度的时间演化 PDE

## L5 Score-based 生成模型
- 得分函数 ∇x log p(x)：为何不直接学密度而学得分
- 噪声得分匹配（NSM）：加噪分布的得分更容易估计
- NCSN：多噪声等级退火采样（Langevin dynamics）
- 得分与扩散参数化之间的换算关系（为 L6/L7 铺路）

## L6 扩散模型 DDPM
- 前向加噪马尔可夫链的闭式解 x_t ~ N(√ᾱ_t x_0, (1-ᾱ_t)I)
- 反向链每一步是高斯：参数化均值/方差 → ε-prediction 目标
- 从 VAE/变分下界出发推导 DDPM 损失（简化加权 ELBO）
- 采样即逐步去噪；与 L5 得分估计的等价性预告

## L7 扩散的统一 SDE 视角
- DDPM 离散极限 → 前向 SDE；反向时间 SDE 依赖得分函数
- 概率流 ODE：同一边缘分布的确定性动力学，可用 CNF 工具求解
- 一般 Ornstein-Uhlenbeck / VE / VP 前向过程的统一写法
- 该框架同时涵盖 Score-based、DDPM、DDIM——本课核心贡献点

## L8 采样与推断加速
- DDIM：非马尔可夫反向过程，少步采样与确定性轨迹
- 引导（guidance）：条件生成时得分的线性组合；classifier-free guidance
- ODE/SDE 求解器选择对步数与质量的影响
- 与流匹配采样（少步 Euler）的对比

## L9 流匹配 Flow Matching
- 连续正则化匹配目标：回归条件速度场，避免模拟 ODE
- Conditional Flow Matching (CFM) 定理及其与扩散损失的等价性
- OT-CFM：最优传输直线路径；rectified flow 的迭代直线化
- 与 Diffusion Policy/视频生成（Sora 路线）的联系

## L10 实践实验讲评
- Lab：从零实现前向加噪、网络训练、采样可视化全流程
- ε-prediction 与 v-prediction 参数化对比；噪声调度选择的实操经验
- 流匹配实现：路径、速度场、Euler 采样循环
- PyTorch 调试要点：分布形状约定、时间步嵌入

## L11 应用讲座 I：分子设计与科学应用
- 3D 分子构象生成：等变扩散/流匹配模型
- 蛋白结构预测与生成（RFdiffusion 类思路）
- 物理约束如何注入生成过程
- 骨架级占位，按官网当年讲座补充

## L12 应用讲座 II：机器人与轨迹生成
- Diffusion Policy：把动作轨迹生成建模为条件去噪
- 与自回归策略/RL 基线的对比（多模态动作分布表达力）
- 实时推理的挑战：采样步数 → 控制频率
- 骨架级占位，按官网当年讲座补充
