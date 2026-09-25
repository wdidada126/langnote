# MIT 6.7960 配套项目计划

> Python 为主；基础组件 numpy 手写、系统组件用 PyTorch。本轮只写不编译。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1-L3 微分与 MLP | Python (numpy) | 手写 autograd + MLP 回归/分类 | `python miniauto/train.py`；`pytest miniauto/test_op.py` |
| L4-L5 优化与泛化 | Python (PyTorch) | 优化器×调度网格对比 + 过拟合/正则消融 | `python opt_gen/run.py --config grid1.yaml` |
| L6 CNN | Python (PyTorch) | mini-ResNet CIFAR-10；感受野可视化 | `python cnn/main.py --epochs 50` |
| L7-L8 序列与注意力 | Python (PyTorch) | LSTM 与 Transformer 字符 LM 对比 | `python seq/task.py --model transformer` |
| L9 大模型 | Python | 小 GPT 预训练+缩放实验（loss-vs-FLOPs 曲线） | `bash llm/scaling_experiment.sh` |
| L10 生成 | Python (PyTorch) | VAE 与 DDPM 在 MNIST 的 FID 对比 | `python gen/train.py --model ddpm` |
| L11 GNN | Python (PyG) | Cora 节点分类 + 过平滑观察 | `python gnn/cora.py --layers 2/8/16` |
| L12 RL | Python | CartPole REINFORCE/PPO；DPO 玩具实验 | `python rl/train.py --algo ppo` |
| L13 效率 | Python | INT8 量化前后精度/吞吐对比报告 | `bash perf/quant_bench.sh` |
| 课程项目 | Python | 自选端到端项目（复现一篇小论文） | `bash project/run_all.sh` |
