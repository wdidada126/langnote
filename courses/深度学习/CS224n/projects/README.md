# CS224n 配套项目计划

> 对齐 5 个 Assignment + Final Project；Python（numpy 底层 + PyTorch），本轮只写不编译。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L2 词向量（A1/A2） | Python (numpy) | GloVe 权重训练 + 类比/异常词评测 | `python a2_word2vec/train.py --dim 300` |
| L3 句法（A3） | Python (PyTorch) | 窗口特征+CRF 依存解析器 | `python a3_parser/train.py` |
| L4-L5 NMT（A4） | Python (PyTorch) | BPE + Transformer 翻译（TED-En→De），束搜索 BLEU | `python a4_nmt/translate.py --ckpt best` |
| L6-L7 Transformer | Python (PyTorch) | 多头注意力单测对齐 HF；warmup 调度实现 | `pytest transformer/test_mha.py` |
| L8 BERT（A5） | Python (PyTorch) | 微调 distilbert 做 GLUE 子任务 | `python a5_bert/finetune.py --task mnli` |
| L10 生成 | Python | top-k/top-p/温度对摘要质量对比报告 | `python decoding/run_eval.py` |
| L12 提示 | Python | CoT vs 直接提示在 GSM8K 子集评测 | `python prompting/cot_eval.py` |
| L13 对齐 | Python (TRL) | 小模型 DPO 偏好微调玩具实验 | `python dpo/train.py` |
| L14 PEFT | Python (PEFT) | LoRA vs 全参微调显存/效果对比 | `bash peft/bench.sh` |
| Final Project | Python (PyTorch) | SQuAD 抽取式 QA 系统（含数据增强与消融） | `bash squad/run_all.sh` |
