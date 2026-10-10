# 03 · CNN 图像

> ⚠️ 题注：章名为本笔记按书中网络类型带段**自拟映射**（对应 CNN/图像分类/迁移学习
> 食谱段），逐字目录待销账。三态口径：✅=官方文档口径；⚠️=推定书中内容；
> 🔧=未实测：本机未装 tensorflow（tf/torch 均无）。

## 核心机制

1. **卷积栈的积木语法**：`Conv2D(filters, kernel_size, activation='relu')` →
   `MaxPool2D` → 重复堆叠 → `Flatten`+`Dense` 收尾。Keras vs PyTorch 的**第一分歧是
   张量布局**：

   ```python
   # Keras ✅：NHWC（batch,height,width,channels），TF 传统
   model.add(Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)))

   # PyTorch 对照：NCHW（batch,channels,height,width），input_shape=(1, 28, 28)
   # self.conv = nn.Conv2d(1, 32, kernel_size=3, padding='same')
   ```
   跨框架搬运模型 90% 的第一坑就是通道维位置；`tf.keras` 可 `image_data_format`
   切 NCHW，但慢 🟡。C++ 锚：OpenCV DNN/TFLite 部署时同样要做布局转换，NHWC↔NCHW
   transpose 是引擎层常态开销 ✅。
2. **迁移学习食谱**：`Applications` 预训练塔（VGG/ResNet/MobileNet ⚠️ 书中用了哪些
   待销账）+ `top='classifier'` 去头 + 自有密层头 + 冻结塔（`layer.trainable=False`）
   两段式训练。对照 PyTorch：`torchvision.models` 同思路（weights=... 参数是书后产物 ⚠️
   只作现代口径提及）。
3. **数据增广**：Keras 从 `ImageDataGenerator`（已 🟡 遗老）转向
   `tf.keras.layers.RandomCrop/RandomFlip` 图层化 ✅——书是换代夹缝期写的，读时注意
   两类 API 混出；PyTorch 锚：torchvision transforms 从一开始就是函数式管线。

## 批判读法

- 本章是全书「食谱最能见效」段，但仍不给感受野/参数量的推导——配花书卷积节 ✅
  （[../深度学习_花书.md](../深度学习_花书.md)），d2l 有从零实现 LeNet 段可互补。
- 「预训练塔直接搬」的隐含前提是 ImageNet 分布接近你的数据；医学/遥感等域差大时
  微调层的深度选择书中多半略过——实操按「层越深语义越通用」原则自查。

## 🔧 微实验位（未实测：本机未装 tensorflow）

1. 同一小数据集跑「从零训 CNN」vs「MobileNet 微调」，记录到 90% 准确率所需 epoch 差。
2. `channels_last` vs `channels_first` 在 GPU/CPU 上各测吞吐，验证布局-性能直觉。
3. 冻结塔比例消融：冻前 50%/75%/全冻，看小数据上谁过拟合。

## 中英对照

| 英文 | 中文 | 一句注 |
| --- | --- | --- |
| convolution / filter / kernel | 卷积/滤波器/核 | 滑动窗口共享权重 |
| pooling (max/average) | 池化 | 下采样、平移鲁棒性 |
| stride / padding | 步幅/填充 | same/valid 语义两框架一致 |
| channel dimension | 通道维 | NHWC vs NCHW 之争根源 |
| transfer learning / fine-tuning | 迁移学习/微调 | 去头重训+小 lr 解冻 |
| frozen layers | 冻结层 | trainable=False |
| data augmentation | 数据增广 | 图层化是现行方向 |

## 盘谱互链（均已实测存在）

- 上：[02-前馈与回归.md](02-前馈与回归.md)；下：[04-RNN与序列.md](04-RNN与序列.md)；回 [00 总览](00-总览与阅读地图.md)。
- 视觉纵深（非本书线，文本提及）：YOLO 谱系档在 ../ 索引登记，见
  [../Python系列·总索引.md](../Python系列·总索引.md) 补编 YOLO 线。

## ⚠️ 欠账

书中具体用了哪几个 Applications 塔、增广 API 版本混出程度——待对书销账；
无 GPU 环境，实验 2 连设计稿都未跑。
