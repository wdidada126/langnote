# 基于大语言模型融合的多语种全非自回归 ASR：一项综合研究

> 来源：日常笔记 `2026/202603/20260313.md`（ASR 领域「大语言模型融合」方向第 1 条）
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | Multilingual and Fully Non-Autoregressive ASR with Large Language Model Fusion: A Comprehensive Study |
| 作者 | W. Ronny Huang, Cyril Allauzen, Tongzhou Chen, Kilol Gupta, Ke Hu, James Qin 等（共 10 人） |
| arXiv | 2401.12789v1 |
| 提交 / 更新 | 2024-01-23 / 2024-01-23 |
| 发表 | **ICASSP 2024**（arXiv comment 标注） |
| 链接 | https://arxiv.org/abs/2401.12789 |
| 官方代码 | 无（Google 工作） |
| 主题 | 语音识别 / LLM 融合 / 非自回归解码 |

## 一句话结论

提出**非自回归的 LM 融合 ASR 系统**，把 **Universal Speech Model (USM)** 与 **PaLM 2** 以 **per-segment scoring** 模式结合，充分利用加速器的并行能力：**FLEURS 上所有语种平均相对 WER 改善 10.8%**、YouTube 字幕任务 3.6%；并做了覆盖 **LLM 规模（128M→340B）、上下文长度、词表规模、融合方式**的完整消融。

## 核心要点

- **动机**：大模型时代，**自回归解码**的特性使得**延迟成为显著瓶颈**。
- **方案**：非自回归 LM-fused ASR 系统，有效利用加速器硬件的并行化能力。
- **组合方式**：**USM（Universal Speech Model）+ PaLM 2**，采用 **per-segment scoring mode**。
- **效果**：
  - FLEURS：所有语种平均**相对 WER 改善 10.8%**
  - YouTube captioning：**3.6%**
- **消融维度**（本文的主要工程价值）：
  - LLM 规模：文中探索了 **128M 到 340B** 参数对 ASR 性能的影响
  - 上下文长度（context length）
  - 词表规模（vocabulary size）
  - 融合方法论（fusion methodology）
- **意义**：为影响大规模 LM 融合语音识别系统有效性的各类因素提供了有价值的实证洞见。

## 代码仓库

| 仓库 | 说明 |
|------|------|
| 本文 | 无官方代码（Google 内部工作） |
| [modelscope/FunASR](https://github.com/modelscope/FunASR) | 源笔记同节推荐的实践替代品：ModelScope 团队的工业级 ASR 工具包，集成 Paraformer、SenseVoice 等 |

## 源笔记摘录

> 1. 大语言模型融合（LLM-based ASR）
> • 论文标题：Multilingual and Fully Non-Autoregressive ASR with Large Language Model Fusion: A Comprehensive Study
> • 核心内容：提出了一种非自回归的LM融合ASR系统，结合通用语音模型（USM）与PaLM 2语言模型，显著降低了词错误率（WER）。该研究对LLM大小、上下文长度等关键参数进行了全面的消融分析。
> • 论文链接：https://arxiv.org/abs/2401.12789

## 勘误与提醒

- ✔ 源笔记的标题、链接与要点概括**完全准确**（USM + PaLM 2、WER 改善、消融分析都对应得上）。源笔记未提及的 **ICASSP 2024** 发表信息，本次已通过 arXiv comment 字段确认。
- ℹ️ 源笔记未记录「非自回归」这一核心动机（降低解码延迟），此处已补齐。
- ℹ️ 无官方代码，动手请转向 FunASR 等工具包。

## BibTeX

```bibtex
@inproceedings{huang2024multilingual,
  title     = {Multilingual and Fully Non-Autoregressive ASR with Large Language Model Fusion: A Comprehensive Study},
  author    = {Huang, W. Ronny and Allauzen, Cyril and Chen, Tongzhou and Gupta, Kilol and Hu, Ke and Qin, James and others},
  booktitle = {ICASSP 2024},
  year      = {2024},
  eprint    = {2401.12789},
  url       = {https://arxiv.org/abs/2401.12789}
}
```
