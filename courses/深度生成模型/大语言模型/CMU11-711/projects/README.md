# CMU 11-711 配套项目计划

> 本轮只登记计划，不写代码；每项目独立目录 + 独立 build 脚本，集中编译由用户后续统一执行。期末主线为"复现并改进一篇前沿论文"。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L2 词表征 | Python | 训练 Word2Vec/GloVe 并做类比与可视化（gensim） | `python train_wv.py && python eval_analogy.py` |
| L3-L4 序列+注意力 | Python | LSTM 语言模型 + Bahdanau 注意力翻译小模型 | `python rnnlm.py` / `python seq2seq_attn.py` |
| L5 Transformer | Python | 手写 mini-Transformer 翻译模型并跑 BLEU（nanoGPT 风格） | `python trans_train.py` |
| L6 预训练 | Python + HF | 小语料 MLM 预训练 + 下游分类微调（BERT 复现） | `python mlm_pretrain.py && python ft_classify.py` |
| L7-L8 GPT 训练 | Python | 从零训小型自回归 LM + tokenizer；数据配比消融 | `python train_clm.py --corpus mixA` |
| L9 指令/对齐 | Python + trl | LoRA 指令微调 + DPO 对齐对比（含奖励曲线） | `python sft_lora.py` / `python run_dpo.py` |
| L10-L11 推理 | Python | CoT/自洽性在 GSM8K 子集复现；接工具推理 | `python cot_eval.py` |
| L12 解码控制 | Python | 约束解码 + DoLa 事实性提升实验 | `python constrained_gen.py` |
| L13 RAG/任务 | Python | 检索增强 QA 端到端 + COMET/BERTScore 评测 | `python rag_qa.py` |
| L14 评测 | Python | LLM-as-judge 偏差实验（位置/冗长/自恋） | `python judge_bias.py` |
| L15 多模态/跨语言 | Python | 投影层 VLM 最小实现 + 跨语言 zero-shot 对比 | `python mini_vlm.py` |
| L16 效率/解释性 | Python | LoRA vs 全参消融 + TransformerLens 定位诱导头 | `python peft_ablate.py` / `python interp.py` |
| 期末项目 | Python | 复现一篇前沿论文并做一处改进（随机性/数据/超参分析） | `bash run_repro.sh`（本轮不执行） |
