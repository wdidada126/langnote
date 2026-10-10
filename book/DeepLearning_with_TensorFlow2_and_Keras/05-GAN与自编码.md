# 05 · GAN 与自编码

> ⚠️ 题注：章名为本笔记按书中网络类型带段**自拟映射**（对应自编码器/VAE/GAN 生成族
> 食谱段），逐字目录待销账。三态口径：✅=官方文档口径；⚠️=推定书中内容；
> 🔧=未实测：本机未装 tensorflow（tf/torch 均无）。本章是全书食谱感最重段，批判读法
> 权重最高。

## 核心机制

1. **自编码 = 压缩-还原两塔**：Encoder → 瓶颈 `latent` → Decoder，损失取重建
   （MSE/BCE）。Keras Functional API 双塔写法 ✅：

   ```python
   # Keras：一个 model 端到端（🔧 未实测：本机未装 tensorflow）
   ae = Model(inputs=inp, outputs=dec(inp(enc(inp))))
   encoder = Model(inp, enc.output)   # 训后单独取用做特征提取

   # PyTorch 对照：enc/dec 常作同一 nn.Module 的两个方法
   # def forward(self, x): z = self.encode(x); return self.decode(z), x, mu, logvar
   ```
   VAE 的增量=瓶颈换 `(z_mean, z_log_var)` + **重参数化技巧** `z = mean + eps*std`
   （✅ 机制口径；推导见花书生成模型章 ✅ [../深度学习_花书.md](../深度学习_花书.md)）。
2. **GAN = 两个网络的极小极大博弈**：生成器把噪声映成样本，判别器打真假分。关键
   机制差异：Keras 高层 `compile/fit` **装不下双优化器**——必须 subclassed `Model`
   重写 `train_step` 或用自定义循环 ✅；这恰好是 PyTorch 的舒适区（两个 optimizer
   手工交替，天然命令式）。本节读法：书里怎么绕开 `fit`，就是 Keras 表达力边界的标本。
3. **训练不稳定是特性不是 bug**：模式崩塌、判别器过强/过弱、label smoothing、
   交替节拍（D 训 k 步 G 训 1 步）⚠️ 书中给了多少调参细节待销账——2026 口径：GAN
   生产应用多被扩散模型替代 🟡（生态判断，非书内容）。

## 批判读法

- 「一章一网络」在本章最伤人：GAN 变体（DCGAN/WGAN）各有生死机制，食谱只给一个
  DCGAN 级样例 ⚠️ 推定——机制纵深请去 d2l/原论文线（欠账：paper 建档）。
- VAE 若略过 KL 项的「正则 vs 似然」张力、GAN 若略过纳稳态叙事，就是两枚「会跑但
  不懂」的模型——本笔记按「跑通≠学会」降级处理。

## 🔧 微实验位（未实测：本机未装 tensorflow）

1. AE 瓶颈维度 2/8/32 消融：MNIST 级数据上重建质量 vs 潜空间聚类可视化。
2. VAE vs GAN 同数据集出图对比：模糊（回归损失主导）vs 锐但假（对抗损失主导）手感。
3. `train_step` 里把 D/G 学习率各乘 0/2x，亲眼制造一次训练崩溃。

## 中英对照

| 英文 | 中文 | 一句注 |
| --- | --- | --- |
| autoencoder (AE) | 自编码器 | 恒等映射+瓶颈 |
| latent representation | 潜表征 | 降维特征/生成种子 |
| VAE / reparameterization trick | 变分自编码器/重参数化 | 把随机性挪出计算图 |
| KL divergence | KL 散度 | VAE 潜分布正则项 |
| generator / discriminator | 生成器/判别器 | GAN 博弈双方 |
| adversarial loss | 对抗损失 | 非重构类损失 |
| mode collapse | 模式崩塌 | 生成器只出一类样本 |
| train_step | 训练步 | Keras 自定义循环挂载点 |

## 盘谱互链（均已实测存在）

- 上：[04-RNN与序列.md](04-RNN与序列.md)；下：[06-强化学习与DL4J支线.md](06-强化学习与DL4J支线.md)；
  回 [00 总览](00-总览与阅读地图.md)。
- 机制补链：[../DiveIntoDeepLearning.md](../DiveIntoDeepLearning.md)。

## ⚠️ 欠账

书中 GAN/VAE 样例的具体数据集与是否含 `train_step` 写法待对书销账；生成模型 2026
现状（扩散线）本档只作生态判断，未展开建档。
