# CMU 10-414 提纲

> 骨架级要点，正文笔记待逐讲展开。

## L1 导论
- DL Systems 三层：框架（framework）/ 算法（algorithms）/ 硬件（hardware）。
- Needle 项目地图：5 个作业如何逐步长出完整框架。

## L2 前向模式自动微分
- 双数（dual numbers）与导数对象；从标量到向量的雅可比-向量积。
- 前向模式适合输出多、输入少的场景。

## L3 反向模式自动微分
- 计算图 + 链式法则反向传播；显式图 vs 隐式 tape。
- 反向模式适合标量损失对大量参数求梯度（深度学习主场景）。

## L4 AD 应用
- 用 AD 训练逻辑回归/MLP；数值梯度检查。
- 高阶梯度与双反向的直觉。

## L5 ML 基础
- 损失：MSE/交叉熵；优化器：SGD/Momentum/Adam 实现。
- 数据加载器与 mini-batch 策略。

## L6 框架设计
- backend（张量运算）与 autograd（求导记录）解耦。
- 算子 forward/backward 注册范式；与 PyTorch 架构对照。

## L7 反向模式进阶
- 矩阵/卷积等张量算子的反向规则推导。
- 广播（broadcasting）下的梯度规约陷阱。

## L8 实用深度学习 I（HW3）
- 从零实现 CNN 训练 MNIST；池化/卷积反向。
- 框架跑通端到端训练循环。

## L9 实用深度学习 II（HW4）
- RNN/LSTM 单元的反向；梯度裁剪。
- Transformer 块与注意力反向；生成式小任务。

## L10 GPU 加速（HW5）
- cuDNN 后端接入；张量在 host/device 的搬运。
- CUDA kernel 视角看算子执行。

## L11 低精度训练
- FP16/BF16/FP8 数值格式；loss scaling 防梯度下溢。
- 混合精度：master 权重 + 自动转换。

## L12 性能建模
- Roofline：算术强度 × 带宽/峰值算力定界。
- 内存层级、kernel 启动开销、并行策略（data/model pipeline）。

## L13 高级主题
- 分布式训练概览（All-Reduce）；量化推理。
- 编译器（TVM/XLA）在框架中的位置。

## L14 串讲
- needle 全链路：autograd → optim → nn → cuda → 训练 Transformer。
