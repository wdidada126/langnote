# 《Programming PyTorch for Deep Learning》章档 03 · 视觉数据与 CNN 任务

> ⚠️ 题注：章名凭记忆推定带段，逐字目录待购电子版销账——本节机制口径标 ✅ 者均为 pytorch.org/torchvision 官方文档级常识，**不承诺本书如此讲**；书中位置全部未核。
> 🔧 未实测：本机未装 torch，微实验仅为设计。上一环 [02 第一个网络](02-构建与训练第一个网络.md)。

## 核心机制

### 数据管线：Dataset / DataLoader / transforms 三件套

- `Dataset` 约定 `__len__`+`__getitem__` 两法（✅），`DataLoader` 负责组批、shuffle、多进程装载（✅），`torchvision.transforms` 做尺寸/张量化的可组合变换（✅）。对照 ../HandsOnMachineLearning3e.md（✅ 在盘）tf.data 的「流水线即数据集」抽象：两家都把「取数」从训练循环里剥出成独立管线（✅ 定性）；差异在 PyTorch 管线是「Python 对象即时求值」、TF 管线偏图化惰性求值（✅ 口径）。
- 图像张量惯例 **NCHW**：batch×通道×高×宽，通道维在前（✅）——对照 TF 默认 NHWC（✅，另见 ../TensorFlow实战Google深度学习框架2.md），跨框架搬运模型第一颗雷是通道序；transforms 的 `ToTensor` 顺手把 HWC→CHW 并归一化到 [0,1]（✅）。
- 切分与子集：`torch.utils.data.random_split` 一行出训练/验证两桶（✅）；自采样不平衡场景用 `WeightedRandomSampler`（✅ 官方工具位）——短书若整书不碰验证切分 ⚠️，登记为补齐位。

### CNN：卷积核共享权重，池化降采样

- `nn.Conv2d(in,out,kernel)` 滑动窗口共享权重（✅），`nn.MaxPool2d` 降维（✅），激活照旧 `ReLU`——与 ../深度学习入门.md 第 7 章（✅ 在盘）NumPy 手搓卷积完全同数学，只是 PyTorch 把反传播交给 autograd（✅）。花书对卷积分层特征学习的原理口径：../DeepLearning.md（✅ 在盘）。
- 全连接头接在展平的末层特征上：`x.flatten(1)` 后进 `nn.Linear`（✅）——「卷积提特征、全连接做分类」的两段式是 2012–2020 视觉网络通用骨架（✅ 定性）。

### 迁移学习：torchvision.models 一行起跳

- `models.resnet18(weights=...)` 载预训练（✅），换末层 `fc` 再微调（✅）——注意 2020 截点：当年 API 是 `pretrained=True`，现行为 `weights=` 枚举、旧参已废弃（✅ 官方文档口径）；书若用旧写法 ⚠️ 未核，入库必换。
- 对照 Raschka（../MachineLearningWithPyTorchAndScikitLearn.md，✅ 在盘）亦有迁移学习章——二选一裁决（见 [00 册](00-总览与阅读地图.md)）时，本节的「谁讲得深」是要素之一。

## 批判读法（Packt 短书质量存疑位）

1. 短书视觉项目大概率停留在 MNIST/简单自建数据集级别 ⚠️——若如此，工程参考价值低于 d2l 的 CIFAR 实战章，本节让位 ../DiveIntoDeepLearning.md（✅ 在盘）。
2. 数据增强、正则化（dropout/weight decay）、学习率调度等「能训好但书未必讲」的项 ⚠️，一律登记为官方文档补齐位，不假定书内有。
3. 2020 后的 torchvision 改名潮（`torchvision.transforms.functional` 参数序、weights 枚举制 ✅）使书例**不可直接照抄运行**——本档所有 ✅ 口径以现行文档为准。
4. 不虚构引文页码；「项目是图像分类还是检测」⚠️ 推定为分类，检测/YOLO 谱系另档处理（见互链）。
5. 短书 CNN 例程常拿单张手写图讲卷积滑窗 ⚠️——若如此，其图示价值≈d2l 同名章，不必为此书购电子版；此条亦入 00 册裁决位证据。

## 🔧 微实验（未实测：本机未装 torch，仅为设计）

- 实验 A：CIFAR-10 两层 CNN（Conv→Pool→Conv→Pool→FC）训 5 epoch，记录与纯 MLP 的准确率差。
- 实验 B：`ToTensor` 前后分别 print 形状，实证 HWC→CHW 与 [0,1] 归一化。
- 实验 C：`num_workers=0 vs 4` 的 DataLoader 吞吐对比，感受装载进程与 GPU 计算解耦。

## 盘谱互链

- 上一章 [02-构建与训练第一个网络.md](02-构建与训练第一个网络.md)；下一章 [04-语言与序列任务.md](04-语言与序列任务.md)。
- 机制纵深版同题：../DeepLearningWithPyTorch.md（✅ 在盘，CNN 章）；在线原理+实战：../DiveIntoDeepLearning.md。
- 检测谱系延伸（本档不覆盖）：../计算机视觉YOLO目标检测原理与实践.md（✅ 在盘）——书若含检测项目 ⚠️，以此档为准。
- 总索引挂靠：../Python系列·总索引.md（✅ 在盘）。

## 核心概念中英对照

- **数据集协议** — Dataset protocol：`__len__`/`__getitem__` 两法取数约定。
- **数据装载器** — DataLoader：组批、打乱、多进程装载的迭代器工厂。
- **通道优先** — NCHW：PyTorch 图像张量轴序惯例，对 TF 系 NHWC。
- **卷积层** — Conv2d：共享权重滑窗提空间特征。
- **迁移学习** — transfer learning：预训练骨干+换头微调。
- **数据增强** — data augmentation：训练期随机变换扩样（补齐位 ⚠️）。
- **随机切分** — random_split：数据集按长度列表切成互斥子集。

> ⚠️ 欠账：本书视觉章逐字章名、所用数据集、是否 pretrained=True 旧 API、有无检测项目——待购电子版验目录销账；🔧 三实验待装 torch 补跑。
