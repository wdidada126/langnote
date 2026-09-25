# MIT 6.5940 (EML) 配套项目计划

> 原则：与课程 5 个作业对齐，每章一个可运行小项目；本轮只规划代码与 build 方式、不写代码。语言 Python（PyTorch/HF），部署类可选 C++。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L2 剪枝（作业2） | Python (PyTorch) | CIFAR-10 上迭代幅度剪枝 + 微调，画稀疏度-精度曲线 | `python prune/train_sparsely.py --ratio 0.9` |
| L3 NAS（作业3） | Python | 小型可微 NAS/DARTS 玩具搜索 + 结果可视化 | `python nas/search.py --epochs 20` |
| L4 量化（作业1） | Python (PyTorch) | PTQ vs QAT 对比：INT8 感知训练 MobileNet | `python quant/run_qat.py` |
| L5 TinyML | Python→C++ | 关键词唤醒模型 TFLite-Micro 部署（或 CPU 仿真） | `python tinyml/train.py`；`microTVM/make run` |
| L7 高效注意力 | Python | 手写注意力 + 滑窗/分组近似，测显存与速度 | `python attn/bench.py` |
| L8 LLM 量化（作业4） | Python (HF/autogptq) | LLaMA 小模型 AWQ/GPTQ 量化并算 perplexity 损失 | `python llm_quant/eval_ppl.py --awq` |
| L9 LLM 部署（作业5） | Python | vLLM 部署 7B 模型测吞吐/延迟，对比 naive HF pipeline | `python llm_serve/bench.py --vllm` |
| L12-L13 高效训练 | Python (PyTorch) | DDP+ZeRO 玩具实现：梯度压缩 all-reduce 模拟 | `torchrun --nproc_per_node=2 dist/zero_toy.py` |
| 综合 | Python | 端侧三件套：剪枝+量化+蒸馏训练 1/10 参数小模型 | `python fullstack/compress.py` |
