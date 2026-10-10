# 《TensorFlow：实战Google深度学习框架（第2版）》章笔记 04 · CNN与图像识别

> ⚠️ 章名题注：带段划分凭记忆，与书中逐章对应待版权页目录销账。三态标注：✅=官方文档/盘上直证口径；⚠️=凭记忆；🔧=未实测（本机未装 tensorflow）。本册覆盖原书"卷积神经网络与图像识别"主题线 ⚠️：卷积/池化原理、LeNet→AlexNet→Inception 谱系、MNIST/CIFAR-10 实战、迁移学习一瞥（收录组合 ⚠️ 待核）。

## 核心机制

### 卷积层的几何与参数

- 动机：图像输入展平进全连接会参数爆炸且丢空间性；**局部连接+权值共享**把 W 换成小卷积核滑窗。四件套：卷积核大小/步幅(stride)/填充(padding)/通道数——书中以"二维高斯消元式滑窗"叙述 ⚠️ 措辞凭记忆；输出尺寸公式 `(W−F+2P)/S+1` 属 ✅ 通用事实（书中是否给公式 ⚠️ 存疑）。
- 1.x 建层：`tf.layers.conv2d(x, filters=32, kernel_size=5, padding='SAME', activation=tf.nn.relu)`（**2026 已废**：`tf.layers` 死于 TF2 迁移，现行 `tf.keras.layers.Conv2D`；PyTorch 对位 `nn.Conv2d(in, out, k, stride, padding)` ✅）。注意 `SAME/VALID` 填充枚举在 Keras 以 `padding='same'` 存活（✅），是本书 API 少数"改个名还活着"的遗产。
- 池化：`tf.layers.max_pooling2d`（**2026 已废** → `keras.layers.MaxPooling2D` / `nn.MaxPool2d` ✅）——下采样换平移鲁棒、减算力；书中"池化层没有参数"是 ✅ 要点。
- 通道直觉：卷积核深度=输入通道数、核个数=输出通道数；`tf.nn.conv2d` 的 NHWC 数据布局与 Caffe 系 NCHW 之争 ⚠️ 书中立场凭记忆（✅ 事实：GPU 上 NHWC 是 TF 默认，NCHW 更贴 PyTorch 默认）。

### 经典网络谱系与实战线

- 谱系叙事（⚠️ 书中收录深度按印象）：LeNet（手写经典，5 层）→ AlexNet（ReLU+Dropout+GPU，2012 ImageNet 拐点）→ Inception v1/v2/v3（多分支"网络套网络"+辅助分类器）；ResNet 是否入第二版 ⚠️ 存疑（书 2018 年出版，ResNet 2015，理应有 ⚠️ 待目录销账）。概念锚：花书第 9 章给同一谱系的教科书定义（✅ 在盘 [../深度学习_花书.md](../深度学习_花书.md)）。
- 实战双数据集：MNIST（28×28 单通道，LeNet 级网络到 99%+）与 CIFAR-10（32×32×3，Inception 级堆到 ~80% 区间 ⚠️ 具体数字凭记忆不落实）；配套 `tf.train.exponential_decay`+验证集看曲线，复用 03 册军备。
- Inception 辅助损失在 1.x 靠 collection 汇总（`tf.losses.get_total_loss()` 一类，**2026 已废**）；PyTorch 官方实现则把 aux logits 显式返回、手动加权 loss ✅ 对比——"隐式全局 vs 显式数据流"是两代框架的分水岭样本。
- 迁移学习/微调（书中若有 ⚠️ 凭记忆）：加载 ImageNet 预训练权重冻结低层——1.x 靠 saver  checkpoints 手工恢复（**2026 已废**：`tf.train.Saver` → Keras `load_weights` / torch `state_dict` ✅）。

## 批判读法（易错与存疑）

1. **拿 2018 谱系当 2026 架构观**：Inception v3 之后有 ResNet 系、ConvNeXt、ViT；本书价值在"滑窗+通道+堆叠"的几何直觉，不在"该用哪个骨干"。选型请读 YOLO 线（在盘 [../计算机视觉YOLO目标检测原理与实践.md](../计算机视觉YOLO目标检测原理与实践.md) ✅ 谱系到 2026）与官方 model zoo。
2. 书中准确率数字（如 CIFAR-10 改进到某值 ⚠️）**随随机种子与训练预算漂移**，2026 复现不必对齐——把数字读成量级，不读成 KPI。
3. **padding='SAME' 的语义陷阱**：并非总能保持尺寸（偶数核/步幅>1 时不对称），书中是否辨析 ⚠️ 存疑；今天 Keras 文档已明确该细节 ✅。
4. `tf.contrib.slim` 若在本章出现（⚠️ 凭记忆，第二版确有 slim 相关内容待销账）：**contrib 与 slim 双双 2026 已废**（contrib 随 TF2 移除、slim 迁往 TF Addons 后亦衰）；照抄必死，只读其"声明式网络组装"思想。
5. 池化之争：现代 CV 已用 stride-conv/全局池化替代大量 max-pool，本书"池化必配卷积"的教条属 2018 口径 ⚠️ 评述。
6. **可视化与 TensorBoard 归属存疑** ⚠️：CNN 章若配了激活/权重可视化，注意 1.x `tf.summary` 写法与 TF2 已换代（`tensorboard` 库现行 ✅）——图看训练曲线的诉求不变，API 全变。

## 🔧 微实验（未实测：本机未装 tensorflow，pip 冻结，仅为设计）

- 实验 A：PyTorch 搭 3 层 mini-CNN 打 MNIST，手算输出尺寸公式与 `shape` 打印三对照，把 04 册几何账落地。
- 实验 B：同一网络分别 NHWC（TF）/NCHW（torch）跑 CIFAR 子集，记录吞吐差，验证布局之争的现实意义。
- 实验 C：加载 torchvision 预训练 ResNet 冻结前两组卷积 vs 全量微调，对比小数据集收敛——复现书中迁移思想（用现行 API）。

## 盘谱互链

- 上一章 [03-优化算法与正则化.md](03-优化算法与正则化.md)；下一章 [05-RNN与序列处理.md](05-RNN与序列处理.md)。
- 卷积白盒（im2col 展开）：[../深度学习入门.md](../深度学习入门.md) 第 7 章（✅ 目录在盘）；谱系理论：[../深度学习_花书.md](../深度学习_花书.md)。
- 目标检测下游（本书未覆盖的现代 CV 应用面）：[../计算机视觉YOLO目标检测原理与实践.md](../计算机视觉YOLO目标检测原理与实践.md)（✅ 在盘，2026 新锚）。
- 多框架 CNN 实战：[../DiveIntoDeepLearning.md](../DiveIntoDeepLearning.md)；TF2/Keras 口径：[../DeepLearningWithTensorFlow2AndKeras.md](../DeepLearningWithTensorFlow2AndKeras.md)、[../ProgrammingTensorFlow2.md](../ProgrammingTensorFlow2.md)。

## 核心概念中英对照

- **卷积层** — convolutional layer：局部连接+权值共享的滑窗仿射。
- **池化层** — pooling layer：无参数的下采样（max/average）。
- **填充** — padding：SAME/VALID 边界补零策略。
- **步幅** — stride：滑窗步进距离。
- **通道** — channel：特征图深度维度，核深度的乘数。
- **辅助分类器** — auxiliary classifier：Inception 中段分支防梯度流失。
- **迁移学习** — transfer learning：预训练权重+冻结/微调。
- **感受野** — receptive field：输出单元对应的输入区域跨度。
- **全连接头** — fully connected head：卷积特征塔顶部的分类段。

> ⚠️ 欠账：ResNet/slim/迁移学习是否在本章、CIFAR-10 实验的确切网络与数字、TensorBoard 图像可视化深度；本机零实测（无 tensorflow）——购书后销账。
