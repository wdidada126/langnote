# CMU 11-711 论文清单

## 经典论文（NLP 表征→序列→Transformer→预训练脉络）

| 主题 | 论文 | 年份 | 与本课关系 |
| --- | --- | --- | --- |
| 词向量 | Efficient Estimation of Word Representations (Word2Vec, Mikolov) | 2013 | L2 |
| 词向量 | GloVe: Global Vectors (Pennington et al.) | 2014 | L2 |
| 子词 | Neural MT of Rare Words with Subword BPE (Sennrich) | 2015 | L2 |
| RNN/LM | On the Difficulty of Building a Recurrent Neural Network LM (Grave) | 2013 | L3 |
| 注意力 | Neural Machine Translation by Jointly Learning to Align (Bahdanau) | 2014 | L4 |
| 注意力 | Effective Attention Modeling for NMT (Luong) | 2015 | L4 |
| Transformer | Attention Is All You Need (Vaswani et al.) | 2017 | L5 |
| 上下文 | Deep Contextualized Word Vectors (ELMo, Peters) | 2018 | L6 |
| 预训练 | BERT (Devlin et al.) | 2018 | L6 |
| GPT 系列 | GPT / GPT-2 / GPT-3 (Radford, Brown) | 2018/2019/2020 | L7 |
| 缩放律 | Scaling Laws (Kaplan) / Chinchilla | 2020/2022 | L7 |
| 指令 | FLAN (Wei) / InstructGPT (Ouyang) | 2021/2022 | L9 |
| RLHF/DPO | InstructGPT / DPO | 2022/2023 | L9 |
| CoT | Chain-of-Thought Prompting (Wei) / Self-Consistency | 2022 | L10-L11 |
| ToT | Tree of Thoughts (Yao) | 2023 | L11 |
| ICL | Language Models are Few-Shot Learners (Brown) | 2020 | L10 |
| RAG | Retrieval-Augmented Generation (Lewis) | 2022 | L13 |
| 多模态 | CLIP (Radford) / LLaVA | 2021/2023 | L15 |
| 跨语言 | mBERT / XLM-R | 2019/2020 | L15 |
| 解释性 | A Mathematical Framework for Transformer Circuits (Elhage) | 2021 | L16 |
| LLaMA | LLaMA / Llama 2 / Llama 3 | 2023-24 | L8 现代配方 |
| 评测 | HELM / Chatbot Arena / BLEU 批判 | 2016-2023 | L14 |

## 近 5 年（2021-2026）重要进展

| 论文/系统 | 年份 | 要点 |
| --- | --- | --- |
| GPT-4 | 2023 | 能力跃迁、多模态、对齐 |
| Llama 2 / Llama 3 | 2023-24 | 开源基线与对齐配方 |
| Mistral / Mixtral (MoE) | 2023-24 | 稀疏 MoE 开源化 |
| DeepSeek-V3 / R1 | 2024-25 | 高效 MoE + GRPO 长思维链推理模型 |
| OpenAI o1 | 2024 | 测试时计算缩放推理范式 |
| Sora（视频扩散） | 2024 | 生成模型跨模态（连接 MIT6.S184 流匹配/扩散） |
| Flow Matching / Rectified Flow | 2023-25 | 生成建模新主线 |
| Gemma / Qwen 系列 | 2023-25 | 开源多语言/多模态生态 |
| 稀疏自编码器可解释性（SAE） | 2024 | L16 前沿 |
| 提示自动优化 / DSPy | 2023-25 | L10 程序化提示 |
| LLM-as-judge 偏差研究 | 2023-25 | L14 评测方法论 |
| 长上下文与 RAG 演进 | 2023-25 | L13 应用 |
| Agent / 工具调用（ReAct/Reflexion） | 2022-25 | L11/L13 延伸 |

## 知识点在开源项目中的应用

| 课程知识点 | 开源项目 | 对应实现 |
| --- | --- | --- |
| 词/子词向量 | gensim、fastText、sentencepiece | L2 |
| RNN-LM/Seq2Seq | OpenNMT-py、fairseq | L3-L4 |
| Transformer 实现 | PyTorch nn.Transformer、The Annotated Transformer、nanoGPT | L5 |
| 预训练 | Hugging Face transformers（BERT/GPT） | L6-L7 |
| 缩放律/训练 | nanotron、Megatron-LM、torchtitan | L7-L8 |
| 指令/对齐 | trl、LLaMA-Factory、OpenRLHF | L9 |
| ICL/CoT/提示 | LangChain、DSPy、PromptFlow | L10-L12 |
| 推理/Agent | LangGraph、STaR、SWE-agent | L11 |
| 解码控制 | HF generate、transformers-constrained-decoding | L12 |
| RAG | LlamaIndex、Haystack、FAISS | L13 |
| 评测 | SacreMOS/COMET、HELM、OpenCompass、lm-eval-harness | L13-L14 |
| 多模态/跨语言 | LLaVA、Whisper、XLM-R | L15 |
| 解释性 | TransformerLens、SAELens | L16 |
| 效率 | PEFT、bitsandbytes、AutoGPTQ | L16 |
