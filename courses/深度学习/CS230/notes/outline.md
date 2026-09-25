# CS230 (Coursera DL Specialization) 提纲

> 骨架级要点，正文笔记待逐讲展开。

## C1W1 深度学习简介
- 监督学习 + 大规模数据 = 深度学习范式；规模驱动性能（数据/参数/算力）。
- 训练/推理术语：损失、激活、超参数；分布式训练基本概念。
- 掌握 DL 的"思想 + 实现细节 + 组织项目"三件套。

## C1W2 神经网络基础
- 二分类逻辑回归：计算图、向量化（m 个样本一次算完）。
- 梯度下降三形态：批量 / 随机 / 小批量。
- 用 Jupyter + numpy 手推一遍正向与反向。

## C1W3 浅层神经网络
- 激活函数选择：sigmoid/tanh/ReLU 及导数；隐藏层为何必须非线性。
- 反向传播的链式法则与计算图视角（`dZ -> dW -> dA` 模板）。
- 参数初始化策略：零初始化失败的直觉。

## C1W4 深层神经网络
- 前向/反向的维数管理（cache 机制），深层网络的矩阵约定。
- 深度 vs 宽度：为什么更倾向于深层。
- 编程作业：完整搭建 L 层全连接网络。

## C2W1 实用 ML：调参 advice
- 偏差/方差诊断与学习曲线；train/dev/test 划分原则。
- 正则化：L2、Dropout、数据增强；随机搜索优于网格搜索。
- Normalization 输入特征；vanishing/exploding gradients 应对。

## C2W2 优化算法
- Mini-batch 的权衡；指数加权平均与偏差校正。
- Momentum、RMSProp、Adam 的直觉与超参。
- 学习率衰减（分块/离散衰减）。

## C2W3 Batch Norm
- BN 在哪个轴上做均值方差；训练与推理（滑动统计）差异。
- γ/β 仿射参数与"可重参数化"意义。
- 对隐藏单元分布改变的解释 vs 平滑优化的解释。

## C2W4 Softmax 与框架
- Softmax 回归与交叉熵；one-hot 输出层设计。
- 用 TensorFlow/PyTorch 重写 numpy 作业，感受框架自动微分。

## C3W1 ML 策略（一）
- 设定 human-level / oracle 作为指标标尺；可优化误差 vs 不可约误差。
- 单指标（eval single number）优于多指标。
- 满足 ML 假设时加速迭代：误差分析、clear sky 承诺管理。

## C3W2 ML 策略（二）
- train/dev/test 分布错配三种误差：data mismatch、distribution、non-ALH。
- 是否值得更多数据的判断框架；迁移学习/多任务学习。
- 端到端学习何时有效、何时危险。

## C4W1 卷积基础
- 卷积核、padding（valid/same）、stride；1x1 卷积。
- 池化层（max/average）与通道堆叠；卷积参数量计算。
- LeNet-5 结构复现。

## C4W2 经典 CNN
- AlexNet → VGG（重复 3x3 堆叠）→ ResNet（恒等快捷连接、1x1 瓶颈）→ Inception（多分支并置）。
- 网络越深的退化问题与残差学习的解法。
- 实践 advice：迁移学习、数据量与网络深度的匹配。

## C4W3 CNN 应用
- 目标定位：边框标签 (bx,by,bh,bw)、IoU、anchors、Non-Max Suppression。
- FaceNet：triplet loss、One-shot 学习。
- Neural Style Transfer：内容代价 + 风格代价的优化问题化。

## C5W1 序列模型与 RNN
- 语言模型与困惑度（perplexity）；采样生成。
- RNN 梯度消失 → GRU / LSTM 门控机制。
- 双向 RNN 与深度 RNN。

## C5W2 Word Embedding 与 Seq2Seq
- word2vec：目标函数、负采样、软性相似语义。
- t-SNE 可视化 embedding。
- Seq2Seq（encoder-decoder）与 beam search（长度规范化）。

## C5W3 注意力与 Transformer
- Attention 解决长程依赖；self-attention 与多头。
- Transformer 位置编码与并行化优势。
- NLC vs LCN 记号约定。

## C5W4 语音与其他序列应用
- Audio 特征（声谱图）→ 1D 卷积；CTC 标签。
- Wake-word 检测的类不平衡处理（正样本过采样）。
- 项目实战：任选取一方向（如 BabyLM/音乐生成）。
