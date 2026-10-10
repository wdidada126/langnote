# 《Deep Learning with PyTorch》章笔记 03 · 计算机视觉与 CNN

> ⚠️ 题注：对应书中「卷积网络做视觉」与「实用视觉现代架构」方向（约 ch5 与 ch7），章名与页码凭记忆，逐字目录待购电子版销账。
> 三态标注：✅ = pytorch.org/torchvision 官方文档级常识口径；⚠️ = 书中位置推定；🔧 = 未实测：本机未装 torch。
> 承接 [02 册](02-模型构建与训练循环.md)：循环会跑了，本章把「全连接堆」升级为「卷积主干」并解决真实图像数据。

## 核心机制

### Conv2d：窗口滑动 + 通道求和

- 卷积层输入输出都是 `(N, C, H, W)` 四维：批量、通道、空间；`Conv2d(in_ch, out_ch, kernel, stride, padding)` 权重形状 `(out, in/groups, kh, kw)`（✅）。
- 布局对照 C/C++：torchvision 默认 **channels-first（NCHW）**，而图像库（PIL/OpenCV 产物）与多数 C++ 视觉栈按 **channels-last（行优先 HWC）** 排布——`ToTensor` 一步同时完成 HWC→CHW 转置与 0–255→0–1 归一（✅ 官方文档口径）。后续 `channels_last` 内存格式对 cuDNN 更友好，是 2020 后性能议题 ⚠️ 书中覆盖深度未核。
- 对照 Java：无对位物；最接近的是把「层=张量上的纯函数 + 可学习参数」这套心智迁移到无泛型数组抽象的语言——只能靠库，印证本书「框架内部」视角的不可替代。

### 图像数据流水线

- `Dataset/__getitem__` + `DataLoader` 批取样 + torchvision transforms 组合（✅）；书中 2020 版 transforms 面向 PIL，v2 函数式 API 与张量原生变换是后话 ⚠️。
- 迁移学习定式：预训练 ResNet 换掉末层 `fc`、分组设学习率（✅ torchvision models 文档同构）——本书按记忆在此用力 ⚠️，与 d2l（[../DiveIntoDeepLearning.md](../DiveIntoDeepLearning.md)）细粒度微调章对照。

### BatchNorm：训推分模式的状态层

- BN 有可学习参数 **外加** running stats 缓冲：train 模式用 batch 统计并更新缓冲，eval 模式改用缓冲（✅）。这是 [02 册](02-模型构建与训练循环.md) 反复的 `model.eval()` 与 `no_grad` 正交性的物质根源。
- 对照库内他书：花书（[../深度学习_花书.md](../深度学习_花书.md)）从优化景观讲 BN 为何有效，本书讲「在 PyTorch 里怎么不踩模式切换的坑」——机制书与理论书的天然分工。

## 批判读法（易错与存疑）

1. **归一化均值方差口径漂移**：ImageNet 统计量 `(0.485,0.456,0.406)` 被无数教程抄成万能数（✅ 它只对预训练权重有意义）；书若未点破适用范围即缺口 ⚠️。
2. **eval 忘切**：推理不切 `eval()`，BN/Dropout 仍在更新统计，指标随机抖动——书中该警告位置凭记忆 ⚠️。
3. **padding/stride 心算**：输出尺寸公式若只背不推，改骨干网即翻车；d2l 的逐维手推更扎实。
4. **2020 视觉截点**：书中「现代架构」部停留在 ResNet/Inception 时代 ⚠️，ViT 系不在射程——检测/分割方向请转 [../计算机视觉YOLO目标检测原理与实践.md](../计算机视觉YOLO目标检测原理与实践.md)（本仓 2026 视觉最新锚点），别指望本书给。
5. 项目结论（猫狗二分之类 ⚠️ 凭记忆）的准确率基数小，勿外推为工程指标。

## 🔧 微实验位（未实测：本机未装 torch，仅为设计）

- 实验 A：同一图分别走 `PIL→ToTensor` 与直接 `array→permute`，比对张量逐元素一致，实证 HWC→CHW。
- 实验 B：带 BN 的网络 train/eval 两模式各跑同 batch 两次，打印输出方差差异，复现「不切 eval 抖动」。
- 实验 C：`model(x).shape` 反推 padding 公式 `(H+2p-k)/s+1`，三组超参验证。

## 盘谱互链

- 上一章 [02-模型构建与训练循环.md](02-模型构建与训练循环.md)；下一章 [04-序列数据与RNN.md](04-序列数据与RNN.md)；性能续命：[05-性能调优与多GPU.md](05-性能调优与多GPU.md)。
- 理论：[../深度学习_花书.md](../深度学习_花书.md)；在线同伴：[../DiveIntoDeepLearning.md](../DiveIntoDeepLearning.md)；检测延伸：[../计算机视觉YOLO目标检测原理与实践.md](../计算机视觉YOLO目标检测原理与实践.md)；数据侧：[../PythonDataScienceHandbook2e.md](../PythonDataScienceHandbook2e.md)。
- 入口：[../DeepLearningWithPyTorch.md](../DeepLearningWithPyTorch.md)、[../Python系列·总索引.md](../Python系列·总索引.md)。

## 核心概念中英对照

- **卷积层** — `nn.Conv2d`：滑窗加权求和 + 通道混合的可学习层。
- **通道优先** — NCHW：torch 默认内存布局，对位图像域的 HWC。
- **填充** — padding：边界补零以保尺寸/控感受野。
- **池化** — pooling：局部聚合下采样，空间换不变性。
- **批归一化** — BatchNorm：按 batch 统计标准化 + 可学习仿射，训推分模式。
- **迁移学习** — transfer learning：预训练骨干换头微调。
- **数据增广** — augmentation：transforms 链上的随机变换正则。

> ⚠️ 欠账：ch5/ch7 章名与页码凭记忆；BN 与迁移学习小节在书中的详略未核；v2 transforms/channels_last 覆盖情况待电子版销账；微实验未实测（本机无 torch）。
