# 李宏毅机器学习 配套项目计划

> 对齐 2025 主线作业；Python + Jupyter，全部提供小 build/运行脚本，本轮不编译。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L0/L1 LLM 原理 | Python (PyTorch) | 字符级 GPT 预训练 + 手写 RLHF 简化版 | `python mini_gpt/train.py`；`run.sh` |
| L2 提示工程 | Python | CoT/自洽性在 GSM8K 子集上的对比实验 | `python prompting/run_eval.py --strategy cot` |
| L3 Transformer | Python (PyTorch) | 从零实现多头注意力并对齐 HF | `pytest transformer/test_attn.py` |
| L4 解码 | Python | greedy/beam/top-p/温度 对生成质量影响报告 | `python decoding/sample.py --config configs/top_p.yaml` |
| L5-L6 RAG | Python | 本地文档 RAG 问答（分块/召回/重排消融） | `python rag/build_index.py && python rag/ask.py` |
| L7 Agent | Python | ReAct 式天气+计算器 Agent；加反思对照 | `python agent/main.py --task math` |
| L8 微调 | Python | LoRA 微调小模型（如 Qwen-0.5B）并评测 | `python finetune/lora.py --config lora.yaml` |
| L9 效率 | Python | KV cache 显存测算 + vLLM vs HF 吞吐对比 | `bash perf/bench.sh` |
| L10 多模态 | Python | CLIP zero-shot 图像分类 demo | `python clip_demo/main.py --images imgs/` |
| L12 安全 | Python | 提示注入攻击与防御小实验 | `python security/prompt_injection_test.py` |
| L13 推理 | Python | 可验证奖励的 GRPO 玩具实验（算术任务） | `python grpo/train.py --task arithmetic` |
