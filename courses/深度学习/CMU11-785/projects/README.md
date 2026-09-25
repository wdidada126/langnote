# CMU 11-785 配套项目计划

> 对齐课程 HW 线（手写 BP → CNN → Transformer → 生成模型 → 综合项目）。Python 为主，底层组件 numpy 手写以呼应课程"拒绝套模板"风格；本轮只写不编译。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L2-L3 FFN 与 BP | Python (numpy) | 手写反向传播框架（对标 micrograd）+ MLP 训练 MNIST | `python npnn/train.py`；`pytest npnn/test_grad.py` |
| L4-L6 CNN/ResNet | Python (PyTorch) | 搭建 ResNet-18 跑 CIFAR-10；BN 位置消融 | `torchrun --nproc_per_node=1 resnet/main.py` |
| L5 词嵌入 | Python (numpy) | 负采样 skip-gram 玩具语料实现与类比评测 | `python embeddings/analogy_eval.py` |
| L7-L8 RNN/Transformer | Python (PyTorch) | 从零 Transformer 做字符语言模型 + 对齐 HF | `pytest transformer/test_mha.py` |
| L9 语音/视觉 | Python | ViT 小样 CIFAR 分类；mel+CTC 数字识别 | `python asr/main.py --ckpt exp1` |
| L10-L11 生成模型 | Python (PyTorch) | VAE 潜空间插值 + 小型 DDPM 生成 MNIST | `python vae/interpolate.py`、`python diffusion/sample.py` |
| L12-L13 优化/泛化 | Python | 优化器横评 + 双下降实验报告 | `python opti_bench/run.py --grid lr,wdec` |
| L14 GNN | Python (PyG) | GCN 半监督引文网络节点分类 | `python gnn/cora.py` |
| L15 RL | Python | CartPole 策略梯度 vs DQN 对比 | `python rl/cartpole.py --algo a2c` |
| 综合 | Python | Course Project 复刻：自选论文复现 | `bash project/run_all.sh` |
