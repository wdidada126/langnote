# NeuralNets-ZeroToHero 配套项目计划

> 原则：每章一个可运行小项目，本轮只规划代码与 build 方式、不写代码。语言全部 Python（课程原生），复现类项目可选 CUDA/C（对齐 llm.c）。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1-L2 micrograd | Python | 从零实现 micrograd 并解对数回归玩具题，梯度与 torch 核对 | `python micrograd_clone/train.py`；`build.sh` 跑 `pytest test_grad.py` |
| L3-L4 makemore | Python (numpy 起步) | bigram 统计模型 + MLP 语言模型生成中文名字 | `python makemore/train.py --model mlp` |
| L5 手写反向 | Python (numpy) | 给 L4 模型手写 backward，梯度检查误差 < 1e-6 | `pytest test_backward.py` |
| L6 调参与查表 | Python (numpy) | 学习率/宽度消融表 + embedding 可视化（t-SNE 可选） | `python makemore/run_ablation.py` |
| L7 build GPT | Python (PyTorch) | 迷你 GPT（2 层、64 维）在小语料上训练出通顺句子 | `python minigpt/train.py --iters 5000`；CPU 可跑 |
| L8 Tokenizer | Python | BPE 训练器，对同一语料与 GPT-2 tokenizer 对比压缩率 | `python tokenizer/train_bpe.py --corpus names.txt` |
| L9 nanoGPT 实践 | Python (PyTorch) | 在 tiny-shakespeare 上复现 nanoGPT 预训练+SFT 流水线 | `torchrun --nproc_per_node=1 train.py`（单卡/CPU） |
| L10 复现 GPT-2 | Python (PyTorch) | 加载官方 124M 权重核对每层输出 bit 级一致 | `python reproduce/check_layers.py --layer all` |
| L11-L12 延伸 | Python | 用 nanoGPT 权重跑 temperature/top-p 对比 + 简单 DPO 实验 | `python samples/decode_strategies.py` |
