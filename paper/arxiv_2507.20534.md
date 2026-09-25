# Kimi K2：开放的智能体智能

> 来源：日常笔记 `2026/202603/20260302.md`
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | Kimi K2: Open Agentic Intelligence |
| 作者 | Kimi Team, Yifan Bai, Yiping Bao, Y. Charles, Cheng Chen, Guanduo Chen 等（共 200 人） |
| arXiv | 2507.20534v2 |
| 提交 / 更新 | 2025-07-28 / 2026-02-03 |
| 发表 | 技术报告；arXiv comment：**tech report of Kimi K2, with minor updates** |
| 链接 | https://arxiv.org/abs/2507.20534 |
| 官方代码 / 权重 | https://github.com/MoonshotAI/Kimi-K2 |
| 主题 | MoE 大模型 / Agentic / 优化器 |

## 一句话结论

1T 总参数、**32B 激活**的 MoE 模型，用自研的 **MuonClip** 优化器（Muon + QK-clip）在 **15.5T token** 上做到**零 loss spike** 预训练，非思考模式下在 agentic 与软件工程任务上达到开源 SOTA。

## 核心要点

- **规模**：32B 激活参数 / 1T 总参数的 MoE。
- **MuonClip 优化器**：在 Muon 基础上加入 **QK-clip** 技术，**解决训练不稳定**问题，同时保留 Muon 先进的 **token efficiency**。
- **预训练稳定性**：基于 MuonClip，K2 在 **15.5 万亿 token** 上预训练，**零 loss spike**。
- **后训练**：多阶段流程，两大亮点——① 大规模 **agentic 数据合成管线**；② **联合强化学习**阶段（模型在真实与合成环境中交互提升能力）。
- **智能体/软件工程表现**（非思考模式下超越多数开源与闭源基线）：
  - Tau2-Bench **66.1**、ACEBench (En) **76.5**
  - SWE-Bench Verified **65.8**、SWE-Bench Multilingual **47.3**
- **代码/数学/推理**（均未使用扩展思考）：
  - LiveCodeBench v6 **53.7**、AIME 2025 **49.5**、GPQA-Diamond **75.1**、OJBench **27.1**
- 开源释出 **base 与 post-trained 两版 checkpoint**。

## 代码仓库

| 仓库 | Star | 说明 |
|------|------|------|
| [MoonshotAI/Kimi-K2](https://github.com/MoonshotAI/Kimi-K2) | 11,111 | 官方权重与部署代码 |
| [KellerJordan/Muon](https://github.com/KellerJordan/Muon) | 2,855 | Muon 优化器原始实现（MuonClip 的前身基础） |
| [zichongli5/NorMuon](https://github.com/zichongli5/NorMuon) | 92 | NorMuon 官方实现，见 [arxiv_2510.05491.md](./arxiv_2510.05491.md) |

## 源笔记摘录

> |10 | 高效训练trick合集 | Muon Optimizer / NorMuon (2025) | arXiv:2507.20534 / 2510.05491 | 搜索 muon-optimizer 社区实现 | ★★☆☆☆ | 显著加速大模型训练，Kimi等公司在用 |

## 勘误与提醒

- ⚠️ **题名错位（本批最严重的一处）**：源笔记把 `2507.20534` 标为「Muon Optimizer / NorMuon」，但 arXiv 官方元数据确认 `2507.20534` 的题名是 **Kimi K2: Open Agentic Intelligence**。Muon/NorMuon 对应的论文是 `2510.05491`（[见单独条目](./arxiv_2510.05491.md)），Muon 本身则出自 KellerJordan 的实现。
- ℹ️ 三者的真实关系：**Muon**（正交化更新）→ **MuonClip**（Kimi K2 自研，加 QK-clip 解决不稳定）→ **NorMuon**（学术改进，加 neuron 级自适应学习率）。源笔记「Kimi等公司在用」的说法成立，但归因到了错误的论文编号。
- 复现难度 ★★☆☆☆（源笔记评级）：官方权重开放，跑推理不难。

## BibTeX

```bibtex
@misc{kimik2,
  title  = {Kimi K2: Open Agentic Intelligence},
  author = {Kimi Team and Bai, Yifan and Bao, Yiping and Charles, Y. and Chen, Cheng and Chen, Guanduo and others},
  year   = {2025},
  journal= {arXiv preprint arXiv:2507.20534},
  url    = {https://arxiv.org/abs/2507.20534}
}
```
