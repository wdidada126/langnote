# 04 · RNN 与序列

> ⚠️ 题注：章名为本笔记按书中网络类型带段**自拟映射**（对应 RNN/LSTM/GRU 与时序/
> 文本生成食谱段），逐字目录待销账。三态口径：✅=官方文档口径；⚠️=推定书中内容；
> 🔧=未实测：本机未装 tensorflow（tf/torch 均无）。

## 核心机制

1. **循环 = 沿时间共享权重的密层**：`SimpleRNN/LSTM/GRU(units)` 吃 3D 输入
   `(batch, timesteps, features)`，内部携带隐状态 h（LSTM 多一条细胞状态 c）。
   Keras vs PyTorch 对照：

   ```python
   # Keras ✅：层自己管状态，return_sequences 决定输出全部步还是末步
   model.add(LSTM(64, return_sequences=True))     # 堆叠时必 True，🔧 未实测：本机未装 tensorflow

   # PyTorch 对照：nn.LSTM 显式返回 (output, (h_n, c_n))，状态是可见张量
   # out, (h, c) = self.lstm(x, (h0, c0))         # 堆叠要 num_layers=2 参数
   ```
   Keras 把状态藏进层，PyTorch 把状态摊在签名里——调试梯度爆炸时后者占优。
2. **门控是对 vanishing gradient 的工程解**：遗忘门/输入门/输出门让 c 近似恒等路径
   （✅ 机制口径，推导见花书 RNN 章 ✅ [../深度学习_花书.md](../深度学习_花书.md)）。
   GRU 是两门简化版，小数据集常首选。C++/Java 锚：DL4J 的 `LSTM` 顶点级配置在 06 档
   支线里以图式 API 呈现，同机制不同接线。
3. **序列任务两食谱**：时序预测=滑窗成 supervised（`TimeseriesGenerator` ⚠️ 书中若用，
   2026 已 🟡）；文本生成=字符级/词级嵌入 + `TextLoader`/`WordTokenizer` 管道（Keras
   NLP 预处层是 2021 新尝试，2026 存在感低 🟡，HuggingFace tokenizers 才是现行口径 ⚠️
   生态判断，非书内容）。

## 批判读法

- 2026 硬话：书中 RNN 食谱的**机制讲解仍有价值**（状态、门、截断反传播），但
  「RNN 作为生产力」已被 Transformer 全面取代——本章只当序列建模的词法层读，
  下一步必须跳 Transformer 档（../ 索引中 NLP with Transformers 在表，文本提及）。
- 时序预测段若吹了「LSTM 打败统计基线」：自查——naive/differential 基线常打不过 🟡，
  这是食谱带不给反例的典型。

## 🔧 微实验位（未实测：本机未装 tensorflow）

1. 同一滑窗任务 LSTM vs 线性层 vs naive 预测三行对照，破除「循环必神」。
2. `stateful=True` 连续批次 vs 默认每批重置状态：看长依赖任务差异。
3. 梯度裁剪 `clipnorm` 开/负例，捕获 RNN 梯度爆炸手感。

## 中英对照

| 英文 | 中文 | 一句注 |
| --- | --- | --- |
| recurrent layer | 循环层 | 时间维共享权重 |
| hidden state / cell state | 隐状态/细胞状态 | LSTM 双通道记忆 |
| forget/input/output gate | 遗忘/输入/输出门 | 梯度的恒等快路 |
| backprop through time (BPTT) | 时间反向传播 | 截断是常态 |
| return_sequences | 返回全序列 | 堆叠开关，Keras 特有词形 |
| sliding window | 滑窗 | 时序转监督 |
| vanishing/exploding gradient | 梯度消失/爆炸 | RNN 病根 |

## 盘谱互链（均已实测存在）

- 上：[03-CNN图像.md](03-CNN图像.md)；下：[05-GAN与自编码.md](05-GAN与自编码.md)；回 [00 总览](00-总览与阅读地图.md)。
- 推导补链：[../DiveIntoDeepLearning.md](../DiveIntoDeepLearning.md)（从零实现循环层一段）。

## ⚠️ 欠账

书中是否含词嵌入(word2vec/GloVe)食谱段待对书确认；stateful 实验与梯度爆炸负例全未实测。
