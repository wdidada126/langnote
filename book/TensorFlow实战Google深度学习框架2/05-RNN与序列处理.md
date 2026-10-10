# 《TensorFlow：实战Google深度学习框架（第2版）》章笔记 05 · RNN与序列处理

> ⚠️ 章名题注：带段划分凭记忆，与书中逐章对应待版权页目录销账。三态标注：✅=官方文档/盘上直证口径；⚠️=凭记忆；🔧=未实测（本机未装 tensorflow）。本册覆盖原书"循环神经网络与序列建模"主题线 ⚠️：基本 RNN、LSTM/GRU、双向与深层堆叠、语言模型与词嵌入（章节边界待销账）。

## 核心机制

### 展开的循环与门控记忆

- 基本 RNN：`h_t = tanh(W_h·h_{t-1} + W_x·x_t + b)`——把"上一步状态"当额外输入回灌，参数跨时间步共享；书中用"沿时间展开成深层网络"的标准图示 ⚠️ 凭记忆（✅ 该图式是花书/d2l 通用语言）。
- 梯度消失/爆炸在长序列上的必然性 → 门控三兄弟：LSTM（遗忘/输入/输出门+细胞态）、GRU（重置/更新门）；概念权威在 [../深度学习_花书.md](../深度学习_花书.md) 与 [../DiveIntoDeepLearning.md](../DiveIntoDeepLearning.md)（✅ 均 in盘）。
- 1.x 的 Cell 全家桶：`tf.nn.rnn_cell.BasicLSTMCell/GRUCell/LSTMStateTuple`、`tf.nn.static_rnn(dynamic_rnn)`、`tf.nn.bidirectional_rnn` 一类（**2026 已废**——TF2 收拢为 `tf.keras.layers.LSTM/GRU/Bidirectional`；PyTorch 对位 `nn.LSTM(input, hidden, layers, batch_first=True)` 返回 `(output, (h_n, c_n))` ✅）。Cell+state tuple 手工穿线是 1.x 时代最重的样板，今天一行层调用即代——读本书只保留"**状态是序列维度的隐变量**"这一句。
- 词嵌入：`tf.nn.embedding_lookup(W_emb, ids)`（✅ 这枚原语至今存活，PyTorch `nn.Embedding` 同构）——书中以"one-hot 乘矩阵退化成查表"讲 embedding 的本质，是本章最值钱的三行 ⚠️ 措辞凭记忆。
- 语言模型实战（⚠️ 书中任务凭记忆为 text8/古腾堡新闻语料一类）：按字符或词滑窗预测下一 token，困惑度/perplexity 或 top-k 采样评估；训练技巧带**梯度裁剪** `tf.clip_by_global_norm`（✅ 存活原语；torch 对位 `clip_grad_norm_`）。

### 结构变体与训练口径

- 双向 RNN：前后两遍状态拼接，仅对**静态标注任务**（序列标注）合法——在线/生成场景不能用未来（✅ 通用纪律；书中是否点破 ⚠️ 存疑）。
- 深层堆叠：层间时间维不共享、层内参数共享——"时间共享×深度堆叠"的正交两轴是理解 Transformer 前史的关键（⚠️ 评述）。
- `tf.contrib.rnn.*` 若在本章出现（DropoutWrapper 等 ⚠️ 凭记忆）：**2026 已废**（contrib 随 TF2 整体移除）；对应现行为 Keras `dropout` 参数或包装层。
- seq2seq/注意力若被顺带提及（⚠️ 第二版是否收录待核）：1.x 的 `tf.contrib.seq2seq` 全线 **2026 已废**；该主题 2026 的正当入口是 Transformer 档（见盘谱互链），不在本书。

## 批判读法（易错与存疑）

1. **"RNN 是序列唯一解"时代结束了**：2026 序列建模主答案是 Transformer/注意力；本书 RNN 章的正确用法是读"循环=参数共享的状态机、门控=可学习的记忆策略"，这两句直接迁移到对 SSM/Mamba 类新架构的理解上，其余 API 全弃。
2. **static_rnn vs dynamic_rnn**：书中若展开对比（⚠️ 存疑），注意两者都是 1.x 图原语；dynamic 的名字会误导 2026 读者以为"动态图"——它只是 while_loop 式图内循环，与 PyTorch 动态图不是一回事（✅ TF2 文档口径）。
3. 语言模型 perplexity 数字 ⚠️ 书中量级不落实不引用；字符级与词级混讲是 2018 中文书通病，读时自补 tokenizer 概念（去 d2l 第 8–10 章 ⚠️ 章号推定）。
4. LSTM 初值、stateful 训练、截断 BPTT 等工程细节大概率缺席 ⚠️——本书深度是"会搭会用"，不是"训到 SOTA"。
5. Embedding 与 word2vec 若被混编（⚠️ 记忆不确定），记住：本章 embedding 是**随任务端到端训练**的查表层，非预训练词向量——两代路线的分界。

## 🔧 微实验（未实测：本机未装 tensorflow，pip 冻结，仅为设计）

- 实验 A：PyTorch `nn.LSTM` 在 tiny 字符语料（如 'nlp.txt' 级样本）训下一字符预测，手写采样器；对照书中生成文本的观感。
- 实验 B：造 200 步长序列，去/不加梯度裁剪各跑一轮，记录梯度范数分布，实证爆炸与裁剪效果。
- 实验 C：`tf.compat.v1.nn.static_rnn` 复刻 Cell 穿线考古一遍，写 200 字"为什么它死了"笔记——完成 1.x→Keras 迁移心智建设。

## 盘谱互链

- 上一章 [04-CNN与图像识别.md](04-CNN与图像识别.md)；下一章 [06-分布式训练.md](06-分布式训练.md)。
- RNN/语言模型现代多框架版：[../DiveIntoDeepLearning.md](../DiveIntoDeepLearning.md)（✅ 在盘）；理论：[../深度学习_花书.md](../深度学习_花书.md)。
- Keras 序列 API 现行口径：[../DeepLearningWithTensorFlow2AndKeras.md](../DeepLearningWithTensorFlow2AndKeras.md)、[../ProgrammingTensorFlow2.md](../ProgrammingTensorFlow2.md)。
- NLP 下游（Transformer 时代）：见 [../Python系列·总索引.md](../Python系列·总索引.md) 补编所在主表之 NLP with Transformers 行（✅ 档在盘：../NaturalLanguageProcessingWithTransformers.md）。

## 核心概念中英对照

- **循环神经网络** — RNN：状态回灌、时间步共享参数的序列层。
- **长短期记忆** — LSTM：三门+细胞态的抗消失架构。
- **门控循环单元** — GRU：双门简化版 LSTM。
- **双向** — bidirectional：正反两遍状态拼接（仅限离线任务）。
- **词嵌入** — embedding：ID→稠密向量的可训练查表。
- **困惑度** — perplexity：语言模型标配评估，exp(平均NLL)。
- **梯度裁剪** — gradient clipping：范数上限约束抗爆炸。
- **时间展开** — unrolling：把循环按步复制成深网。
- **截断 BPTT** — truncated backpropagation：只在窗口内回传，控内存与梯度范数。

> ⚠️ 欠账：原书 RNN 章是否含 text8 语言模型全实验、GRU/bi-RNN 收录广度、contrib.rnn 使用位置；本机零实测（无 tensorflow）——购书后销账。
