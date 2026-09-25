# CS230 配套项目计划

> 原则：每章一个可运行小项目，本轮只写代码与 build 脚本、不集中编译。语言以 Python 为主（课程原生），部分底层实现用 numpy 手写。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| C1W2-4 神经网络基础 | Python (numpy) | 手写 L 层全连接网络做猫狗二分类 | `python nn_from_scratch/main.py`；`build.sh` 跑单测 |
| C2W1-4 优化与 BN | Python (numpy/PyTorch) | Momentum/RMSProp/Adam 对比实验 + BN 消融 | `python optimizers/run.py --opt adam` |
| C3 ML 策略 | Python | 造一份带分布错配的玩具数据集，做误差分析报告 | `python ml_strategy/analyze.py` |
| C4W1-2 CNN 与经典架构 | Python (PyTorch) | numpy 实现卷积/池化反向；再搭 mini-ResNet 跑 CIFAR-10 子集 | `python cnn_numpy/test.py`、`torchrun` 单卡 |
| C4W3 检测/人脸/风格 | Python (PyTorch) | triplet loss 人脸验证 demo；Gatys 风格迁移脚本 | `python style_transfer/main.py --content --style` |
| C5W1-2 RNN/Seq2Seq | Python (PyTorch) | 字符级语言模型 + beam search 机器翻译小样 | `python seqmodels/train_char_lm.py` |
| C5W3 Transformer | Python (PyTorch) | 从零实现多头注意力与 Transformer 块，对齐 HF 输出 | `python transformer/test_attn.py` |
| 综合 | Python | Kaggle 风格竞赛 baseline（自选数据集） | `kaggle` CLI + `submit.sh` |
