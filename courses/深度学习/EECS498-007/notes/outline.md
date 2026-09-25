# EECS498-007 提纲

> 骨架级要点；以 Winter 2022 讲次编号，正文待填。

## L1 导论
- CV 的挑战：视角/光照/形变/遮挡/类别内差异。
- 数据驱动范式：图像=像素张量，模型=可微函数。
- 课程路线图与 A1（PyTorch/Colab）预热。

## L2 图像分类 I
- kNN 的度量与维度灾难。
- 线性分类器：W·x+b，损失三选一（SVM/softmax）。
- 可视化权重与最近邻的语义意义。

## L3 优化
- 损失面、局部极小与鞍点。
- SGD→动量→Adam 的直觉链条。
- 学习率是单点最高杠杆超参。

## L4 图像分类 II
- 两层 MLP 与隐藏层表征。
- PyTorch Tensor/autograd/nn.Module 三件套（A2 主线）。
- MNIST 上从线性到非线性的增益量化。

## L5 CNN I
- 卷积=局部权重共享滤波器；stride/padding 形状公式。
- 池化的降采样与不变性直觉。
- 参数量/FLOPs 手算练习。

## L6 CNN II
- AlexNet→VGG→ResNet 演化逻辑；迁移学习。
- 微调策略：冻层、小学习率。
- ImageNet 预训练权重成为公共底座。

## L7 正则化
- 数据增强（裁剪/翻转/颜色抖动）。
- Dropout 与模型平均视角。
- 权重衰减与早停。

## L8 优化 II
- BatchNorm 的位置与推理时行为。
- 学习率调度：阶梯衰减/cosine。
- 混合精度与梯度裁剪初探。

## L9 语义分割 I
- 逐像素分类：全卷积化（FCN）。
- 上采样与跳连（U-Net）。
- mIoU 评估。

## L10 语义分割 II
- 实例分割与全景分割任务定义。
- Mask R-CNN 的掩码头。
- 感受野与多尺度上下文。

## L11 目标检测 I
- 滑窗与候选区域演进史。
- R-CNN→Fast→Faster：ROI pooling 与 RPN。
- 两阶段范式（A4 上半场）。

## L12 目标检测 II
- One-Stage：SSD anchors 与 YOLO 网格。
- IoU 匹配、NMS、损失设计。
- 精度-速度权衡（A4 下半场）。

## L13 RNN
- 时间展开与 BPTT；LSTM 门控。
- 序列 packing 与掩码。

## L14 RNN 用于视觉
- Show-and-Tell：CNN 特征 + LSTM 解码生成 caption。
- teacher forcing 与采样策略（A5 上半场）。

## L15 注意力
- 解码器对特征图的软对齐。
- 可视化 attention map 的解释价值。

## L16 Transformer
- 自注意力、多头、位置编码。
- encoder-decoder 全注意力架构（A5 下半场）。

## L17 ViT
- patch embedding + [CLS]；预训练数据规模依赖。
- 与 CNN 归纳偏置的对比实验。

## L18 图像的其他方式表示
- 像素自回归（PixelCNN）与归一化流。
- 似然视角的生成建模。

## L19 3D 表示
- 点云置换不变（PointNet）、体素、隐式表示。
- NeRF：位置编码 + 体渲染概览。

## L20 VAE
- 重参数化与 ELBO（A6 上半场）。
- 潜空间插值可视化。

## L21 GAN
- 生成器/判别器对抗（A6 下半场）。
- 训练不稳定与模式坍缩观察。

## L22 视觉与语言/总结
- CLIP 对比学习；图文跨模态。
- 网络可视化与风格迁移（A6 收尾）。
- Mini-Project：完整 DL pipeline 自选命题。
