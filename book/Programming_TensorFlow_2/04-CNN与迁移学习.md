# 04 · CNN 与迁移学习

> 章名 ⚠️ 凭记忆推定带段，逐字目录待购电子版销账。对应 *Programming TensorFlow 2*（Packt·2021 ⚠️）视觉带段：卷积/池化积木 → 经典 CNN 训练 → `keras.applications` 预训练骨干冻结与微调（迁移学习）。
> 时效注：书 API 截点 2021，对照现行官方文档；Keras 3 下 `keras.applications` 权重加载与后端语义有变（见批判读法）。🔧 一律「未实测：本机未装 tensorflow」。

## 一、核心机制

### 1. 卷积积木
- `Conv2D(filters, kernel_size, activation='relu')` + `MaxPooling2D(pool_size)` 交替堆叠，末端 Flatten→Dense 分类头 ⚠️ 教学册标配形状，凭通行口径。
- 心智三问：感受野怎么随层数长大、通道数何时翻倍、空间尺寸何时减半—— pooling 换 stride 卷积的现代做法（2021 书大概率仍是 MaxPooling 传统流 ⚠️ 推定）。
- PyTorch 对照：`nn.Conv2d` 权重形状 (out,in,k,k) vs TF `Conv2D` kernel (k,k,in,out)——**数据格式 NCHW vs NHWC 是两侧默认差**，迁移时 transpose 权重或改 `data_format` 参数，是 CNN 移植第一大坑。Keras `input_shape=(h,w,c)` 声明式 vs PyTorch 首 conv 声明 in_channels 后「跑一个 dummy batch」定型——两种流派。

### 2. 迁移学习三板斧
```python
base = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False)  # ⚠️ 凭通行口径
base.trainable = False                          # 冻结
x = base.input; y = base(x); y = GlobalAveragePooling2D()(y); y = Dense(C, activation='softmax')(y)
model = Model(x, y)                             # 只训新头 → 可解冻顶层 fine-tune
```
- 正序：先冻结骨干只训分类头（防随机头梯度打碎预训练权重）→ 低学习率解冻尾部层微调 ⚠️ 通行打法，书中口径待目录销账。
- 其他语言锚：`keras.applications` ≈ torchvision.models 的 pretrained 参数——但 torchvision 0.13+ 已改 `weights=WeightsEnum` 路线弃用布尔 `pretrained`，两侧在 2021 后走了**相反的权重管理哲学**（Keras 字符串名 vs torch 枚举类），对照阅读时注意 ⚠️ 凭记忆，torchvision 侧亦未实测。

## 二、批判读法
- **「macOS 副题」在本带段的落地毒点**：2021 年 CPU-only MacBook 上做 CNN 教学，书中样例多半是小数据+浅骨干；2026 复刻同样例可行，但据此形成的「训练时长直觉」全部偏保守一档 ⚠️ 推定。
- **权重下载墙**：`weights='imagenet'` 依赖 2021 的 storage.googleapis 权重 URL；Keras 3 迁移后部分旧骨干权重别名与下载路径已变——照抄构造参数前先查现行文档，此为本带段头号时效风险。
- 书中若含 Grad-CAM/可视化归因：属加分带段 ⚠️ 记忆不明；若没有，2026 补位读物另找。
- ResNet 等骨干在 `applications` 里是「调包对象」而非「原理对象」的概率高——残差连接原理请去 [../DiveIntoDeepLearning.md](../DiveIntoDeepLearning.md) 或花书补。

## 三、🔧 微实验位（未实测：本机未装 tensorflow）
- E1：同一小数据集（cats-vs-dogs 级），「自训 4 层 CNN」vs「MobileNetV2 冻结+头」对照，记录达到同等 val acc 的 epoch 数差——量化迁移学习收益。
- E2：解冻全部层 vs 只解冻最后 20 层，各配 lr=1e-3 / 1e-5 跑两 epoch，观察 loss 爆炸组合，坐实「骨干需小 lr」纪律。
- E3：`include_top=False` + `GlobalAveragePooling2D` 换 `Flatten+Dense`，对比参数量与过拟合差异。

## 四、盘谱互链（写前 ls 实测 ✅）
- 本目录：骨干复用 [03-经典网络与训练.md](03-经典网络与训练.md) 三件套；数据侧接 [02-tf.data数据管道.md](02-tf.data数据管道.md)（图像管道/增广）；交付侧归 [06-部署与服务.md](06-部署与服务.md)。
- 书外：[../DeepLearningWithTensorFlow2AndKeras.md](../DeepLearningWithTensorFlow2AndKeras.md)（Apress 同代册的 CNN 食谱可互为对照）、[../DeepLearningWithPython2e.md](../DeepLearningWithPython2e.md)（Chollet 对迁移学习的分类学）、[../DiveIntoDeepLearning.md](../DiveIntoDeepLearning.md)（ResNet/卷积原理中文锚）、[../Python系列·总索引.md](../Python系列·总索引.md)（补编 TensorFlow/YOLO 线全景；YOLO 视觉线本册未覆盖，另档在盘）。

## 五、自测（讲不出=回去重读）
1. TF kernel (k,k,in,out) vs torch (out,in,k,k)：移植一层 conv 需要动什么？
2. 为什么微调必须「先冻骨干训头、再小 lr 解冻」？跳过第一步会怎样？
3. `weights='imagenet'` 在 Keras 3 时代的下载/别名风险点是什么？

## 六、中英对照

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 卷积层 | Conv2D | 空间滤波+通道混合 |
| 池化 | MaxPooling2D | 降空间尺寸保显著响应 |
| 冻结 | freeze (trainable=False) | 预训练权重不参与梯度 |
| 微调 | fine-tune | 小学习率解冻深层续训 |
| 分类头 | classification head | 骨干之上的新建输出层 |
| 全局平均池化 | GlobalAveragePooling2D | 展平的低参数替代 |

## 七、⚠️ 欠账
- 书中具体骨干清单（VGG/MobileNet/ResNet 取哪几个）、有无增广层专节：待逐字目录销账 ⚠️。
- Keras 3 `keras.applications` 新旧权重别名对照表未建 ⚠️。
- torchvision `weights=` 枚举改造细节未实测（本机亦无 torch）——对照段属 ⚠️ 二手记忆。
- 感受野/stride 替代 pooling 的现代做法是否在书中出现：⚠️ 推定无，销账时确认。
- 🔧 E1–E3 未跑（本机未装 tensorflow）。
