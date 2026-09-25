# CMU 11-667 配套项目计划

> 本轮只登记计划，不写代码；项目对齐六次课程作业主线，每项目独立目录 + 独立 build 脚本，集中编译由用户后续统一执行。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1-L2 架构 | Python | 手写 decoder-only Transformer（GQA+RoPE+SwiGLU 现代配方）并过单元测试 | `pytest -q` |
| L3 预训练数据 | Python | 语料清洗/去重/配比 + BPE tokenizer 训练（课程 A1 主题） | `python build_corpus.py --raw ./data` |
| L4 缩放律 | Python | 多尺寸模型扫描，拟合 loss~(N,D) 幂律并画图 | `python scaling_scan.py` |
| L5 微调 | Python + PEFT | LoRA/QLoRA vs 全参微调在指令集上的质量-成本对比（A2） | `python finetune.py --method {lora,full}` |
| L6 对齐 | Python + trl | SFT→DPO 小模型对齐，偏好数据自造（self-instruct） | `python run_dpo.py` |
| L7 ICL | Python | 探测 ICL 对示例顺序/格式的敏感性实验 | `python icl_probe.py` |
| L8 推理 | Python | CoT/自洽性投票/Best-of-N 在 GSM8K 子集对比 | `python cot_eval.py` |
| L10 RAG | Python | 端到端 RAG：检索器+生成器+事实性评估（课程 A3） | `python rag_e2e.py` |
| L11 评测 | Python | lm-eval-harness 跑多基准 + LLM-as-judge 偏差实验（A4） | `python bench.py && python judge_bias.py` |
| L12 效率 | Python | 量化/蒸馏退化评估 + 训练效率消融（课程 A5/A6） | `python efficiency_ablate.py` |
| L13 解释性 | Python | TransformerLens 定位 induction head；跑一个小型 SAE | `python interp_probe.py` |
| L14 偏见与安全 | Python | 偏见度量 + 越狱攻击/防御红队脚本（A4 偏见部分） | `python bias_eval.py` / `python jailbreak_test.py` |
| L15 多模态 | Python | 投影层接 LLM 的最小 VLM 训练 | `python mini_vlm.py` |
| L16 Agent | Python/TS | ReAct 工具调用小 agent + SWE-bench 子集评测 | `python react_agent.py` / TS 版 `npm i && npm start` |
