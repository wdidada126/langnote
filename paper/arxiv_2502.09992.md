# LLaDA：大语言扩散模型

> 来源：日常笔记 `2026/202603/20260302.md`、`2026/202605/20260507.md`
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | Large Language Diffusion Models |
| 作者 | Shen Nie, Fengqi Zhu, Zebin You, Xiaolu Zhang, Jingyang Ou, Jun Hu 等（共 10 人） |
| arXiv | 2502.09992v3 |
| 提交 / 更新 | 2025-02-14 / 2025-10-18 |
| 发表 | arXiv comment 未标注会议；源笔记（20260507）称 NeurIPS 2025 口头报告，人大官方口径亦如此 |
| 链接 | https://arxiv.org/abs/2502.09992 |
| 官方代码 | https://github.com/ML-GSAI/LLaDA |
| 项目页 | https://ml-gsai.github.io/LLaDA-demo/ |
| 主题 | 扩散语言模型 / 非自回归生成 |

## 一句话结论

LLaDA 用「前向加掩 → 反向预测被掩 token」的扩散范式**从零预训练**，证明大模型的核心能力并不必然依赖自回归：8B 版本在上下文学习上与 LLaMA3-8B 竞争，并在 reversal poem 任务上**超过 GPT-4o**，直接打破了 reversal curse。

## 核心要点

- **挑战通行假设**：LLM 的能力被广泛认为依赖自回归模型（ARM），本文正面反驳。
- **机制**：前向数据掩蔽过程 + 反向生成过程，用 Transformer 参数化预测被掩 token；通过优化**似然下界**提供有原则的概率推断框架。
- **训练范式**：pre-training + SFT，从零训练（不是把已有 ARM 改造成扩散）。
- **可扩展性**：在通用任务、数学、代码等大量基准上展现出强可扩展性，与自建 ARM 基线可比。
- **LLaDA 8B**：上下文学习能力与 LLaMA3-8B 竞争；SFT 后在多轮对话等样例中展现出不错的指令跟随能力。
- **reversal curse**：LLaDA 解决了反转诅咒问题，在 reversal poem completion 任务上**超过 GPT-4o**。
- 结论：扩散模型在语言建模规模化上有前景；「核心能力依赖 ARM」这一假设值得重新审视。

## 代码仓库

| 仓库 | Star | 语言 | 说明 |
|------|------|------|------|
| [ML-GSAI/LLaDA](https://github.com/ML-GSAI/LLaDA) | 3,987 | Python | 官方 PyTorch 实现（人民大学 ML-GSAI 组） |

## 源笔记摘录

> | 2 | 扩散语言模型 | LLaDA: Large Language Diffusion Models (2025) | arXiv:2502.09992 | https://github.com/ML-GSAI/LLaDA | ★★★☆☆ | 打破 reversal curse，推理速度潜力巨大 |

> · 中国人民大学 ／ LLaDA 扩散大语言模型：发表于 NeurIPS 2025（口头报告），首个可对话的扩散大语言模型，开源下载量超350万次

## 勘误与提醒

- ✔ 源笔记的标题、arXiv ID、仓库地址、以及「打破 reversal curse」的描述**完全正确**，是本次 2026 整理中标注质量最高的一条。
- ℹ️ 会议信息：arXiv comment 未标注发表会议，源笔记（20260507）记为 NeurIPS 2025 Oral。此处两说并存，以 arXiv 元数据为保守口径。
- 复现难度 ★★★☆☆（源笔记评级）：扩散式训练与采样流程和常规 ARM 差别较大，入门成本主要在这。

## BibTeX

```bibtex
@misc{llada2025,
  title  = {Large Language Diffusion Models},
  author = {Nie, Shen and Zhu, Fengqi and You, Zebin and Zhang, Xiaolu and Ou, Jingyang and Hu, Jun and others},
  year   = {2025},
  journal= {arXiv preprint arXiv:2502.09992},
  url    = {https://arxiv.org/abs/2502.09992}
}
```
