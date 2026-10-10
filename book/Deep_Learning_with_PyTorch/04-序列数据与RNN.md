# 《Deep Learning with PyTorch》章笔记 04 · 序列数据与 RNN

> ⚠️ 题注：对应书中「深度网络处理序列数据」与「实用 NLP 现代架构」方向（约 ch6 与 ch8），章名与页码凭记忆，逐字目录待购电子版销账。
> 三态标注：✅ = pytorch.org 官方文档级常识口径；⚠️ = 书中位置推定；🔧 = 未实测：本机未装 torch。
> 承接 [03 册](03-计算机视觉与CNN.md)：视觉沿空间维滑窗，序列沿时间维滚状态——两条线共享「参数共享 + 层级堆叠」骨架。

## 核心机制

### RNNCell 到 nn.RNN：沿时间展开的循环层

- `nn.RNN/LSTM/GRU` 接收 `(seq_len, batch, feature)`（默认，`batch_first` 可换向 ✅），返回全序列输出与末状态；内部是共享权重的时间展开（✅）。
- 状态即隐变量：LSTM 用门控（输入/遗忘/输出）在 cell state 上开「恒等高速」缓解梯度消失，GRU 两门简化版（✅ 概念口径）。梯度消失/爆炸的数学本体见花书（[../深度学习_花书.md](../深度学习_花书.md)）循环网络章；本书给的是「`clip_grad_norm_` 挂哪、dropout 进不进循环」的工程位。
- 对照 Kotlin/Java：RNN 的「上一步输出喂下一步」是带状态的迭代器/`Sequence` 语义（对照库内 [../Kotlin_in_Action_2e/03-集合与标准库.md](../Kotlin_in_Action_2e/03-集合与标准库.md)：Sequence 单遍惰性、跨步携带游标状态）；但 PyTorch 把这层隐式状态**外化成张量入参**（hidden/cell state 显式进出），可微分、可搬运——状态外置是「循环」变「网络模块」的关键一步（✅ 概念口径）。

### 变长序列：padding 与 pack

- 批量对齐靠 padding，真实长度信息用 `pack_padded_sequence/pad_packed_sequence` 保住，避免空算与统计污染（✅ 官方文档口径）。书中该节详略 ⚠️ 凭记忆。
- 对照 C++：同「哨兵值 vs 长度元数据」两种变长编码的取舍——padding 是定长槽 + 哨兵，packing 是带长度的紧凑视图。

### Embedding 与文本预处理

- `nn.Embedding` 是查表式线性层（索引→稠密行，✅），词表构建/截断属书中 NLP 项目侧 ⚠️ 位置未核；embedding 语义本体见 Raschka（[../MachineLearningWithPyTorchAndScikitLearn.md](../MachineLearningWithPyTorchAndScikitLearn.md)）对应章。

## 批判读法（易错与存疑）

1. **2020 断代重灾区**：本书序列线收在 RNN/seq2seq/早期 attention ⚠️，2026 视角下 NLP 工程主栈已是 Transformer——本书该线只作机制史读物，现行实操转 [../NaturalLanguageProcessingWithTransformers.md](../NaturalLanguageProcessingWithTransformers.md) 与 [../BuildALargeLanguageModelFromScratch.md](../BuildALargeLanguageModelFromScratch.md)。
2. **batch_first 心智负担**：默认 `(T,B,F)` 与多数教程相反，混用即维度错乱；读代码先盯这个开关（✅ 易错事实）。
3. **状态 detach 与否**：手动多步展开时 `h` 连着图，忘 detach 会让「下一段」的梯度穿回上一段（✅）——书中是否演练 ⚠️ 未核。
4. **双向 LSTM 不是免费午餐**：小语料上收益常被过拟合吃掉，书中项目对比数字基数小 ⚠️ 凭记忆。
5. 书中 ch8「现代 NLP 架构」⚠️ 若涉 attention 仅到 Bahdanau/初阶，勿当 Transformer 教材用。
6. **多层堆叠 RNN 的 dropout 位置**：层间（非时间步内）加 dropout 是稳定训法（✅ 通行工程口径）；书中是否区分两种 dropout ⚠️ 待核——模糊即教材缺口。

## 🔧 微实验位（未实测：本机未装 torch，仅为设计）

- 实验 A：同权重 `nn.RNN` 开/关 `batch_first`，`permute` 后比对输出逐元素一致，祛魅维度开关。
- 实验 B：padding 直喂 vs pack 后喂，比较总计算时长与末状态差异（预期 pack 不受短样本尾部长短影响 ✅ 待验）。
- 实验 C：梯度裁剪 on/off 各训百步，记录 loss 尖峰次数，复现爆炸场景。

## 盘谱互链

- 上一章 [03-计算机视觉与CNN.md](03-计算机视觉与CNN.md)；下一章 [05-性能调优与多GPU.md](05-性能调优与多GPU.md)；项目落地：[06-项目实战与生态延伸.md](06-项目实战与生态延伸.md)。
- 数学底座：[../深度学习_花书.md](../深度学习_花书.md)；在线同伴：[../DiveIntoDeepLearning.md](../DiveIntoDeepLearning.md)；embedding 全景：[../MachineLearningWithPyTorchAndScikitLearn.md](../MachineLearningWithPyTorchAndScikitLearn.md)；时代续命：[../NaturalLanguageProcessingWithTransformers.md](../NaturalLanguageProcessingWithTransformers.md)、[../BuildALargeLanguageModelFromScratch.md](../BuildALargeLanguageModelFromScratch.md)。
- 状态语义对照：[../Kotlin_in_Action_2e/03-集合与标准库.md](../Kotlin_in_Action_2e/03-集合与标准库.md)；入口：[../DeepLearningWithPyTorch.md](../DeepLearningWithPyTorch.md)。

## 核心概念中英对照

- **循环层** — `nn.RNN`：权重共享的时间展开模块，显式进出隐状态。
- **隐状态** — hidden state：沿时间传递的携带向量。
- **门控单元** — LSTM/GRU：以门机制调控状态写入/遗忘。
- **梯度消失/爆炸** — vanishing/exploding gradients：长链乘法导致的训练退化。
- **填充** — padding：定长槽位对齐变长序列。
- **打包序列** — packed sequence：附真实长度、跳过填充位计算。
- **词嵌入** — embedding：索引到稠密向量的查表线性层。

> ⚠️ 欠账：ch6/ch8 章名与页码凭记忆；pack/detach 两节在书中的详略未核；Transformer 断代清单待购电子版逐节销账；微实验未实测（本机无 torch）。
