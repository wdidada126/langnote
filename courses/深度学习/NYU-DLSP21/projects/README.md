# NYU DLSP21 配套项目计划

> 对齐每周 Assignment 与 Final Project。Python（numpy 底层 + PyTorch 上层）；本轮只写不编译。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1 线性模型 | Python (numpy) | softmax 分类器 + 手写梯度下降 | `python a1_linear/train.py` |
| L2-L3 MLP 与 autodiff | Python (numpy) | 迷你反向模式自动微分库 + MLP | `pytest miniauto/test_ops.py` |
| L4 CNN | Python (PyTorch) | LeNet 训练 MNIST；卷积可视化 | `python cnn/run.py --dataset mnist` |
| L5 无监督嵌入 | Python | word2vec 嵌入 + FAISS 检索玩具 | `python embed/retrieval_demo.py` |
| L6 序列模型 | Python (PyTorch) | GRU 字符语言模型与困惑度报告 | `python rnn/train_char.py` |
| L7-L8 Transformer | Python (PyTorch) | 多头注意力单测对齐 + BERT 掩码 LM 小样 | `pytest transformer/test_attention.py` |
| L9 RL | Python | CartPole DQN 复现 | `python rl/dqn.py` |
| Final Project | Python (PyTorch) | Build GPT-2 Mini：tokenizer→预训练→采样→评估 | `bash gpt2mini/train_124M.sh`、`python gpt2mini/sample.py` |
