# NorMuon：让 Muon 更高效、更可扩展

> 来源：日常笔记 `2026/202603/20260302.md`
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | NorMuon: Making Muon more efficient and scalable |
| 作者 | Zichong Li, Liming Liu, Chen Liang, Weizhu Chen, Tuo Zhao（共 5 人） |
| arXiv | 2510.05491v1 |
| 提交 / 更新 | 2025-10-07 / 2025-10-07 |
| 发表 | 未标注会议 |
| 链接 | https://arxiv.org/abs/2510.05491 |
| 官方代码 | https://github.com/zichongli5/NorMuon |
| 主题 | 优化器 / 大模型训练效率 |

## 一句话结论

Muon 的正交化能改善条件数，但**更新后各 neuron 的范数高度不均**，导致少数 neuron 主导优化；NorMuon 在正交化之后补上 **neuron 级二阶动量 + row-wise 归一化**，在保留 Muon conditioning 收益的同时让参数利用更均衡——1.1B 预训练下训练效率**比 Adam 高 21.74%、比 Muon 高 11.31%**，显存与 Muon 相当。

## 核心要点

- **背景**：优化器选择显著影响 LLM 训练效率与算力成本。Muon 通过**正交化参数更新**改善优化几何（conditioning），被视为 Adam 的潜在继任者。
- **被忽视的空白**：Muon 与 Adam 各自优势如何**联合**利用，此前没有被系统探索。
- **Muon 的缺陷**：分析显示 Muon 虽有效降低 condition number，但**产生的更新在各 neuron 上范数高度不均匀**，导致某些 neuron 主导整个优化过程。
- **NorMuon 的做法**：
  1. 为每个 neuron 维护**二阶动量统计量**
  2. 在正交化之后施加 **row-wise 归一化**
  - 效果：参数利用更均衡，同时保留 Muon 的 conditioning 收益
- **工程落地**：在 **FSDP2** 框架下实现高效分布式版本，把正交化计算**策略性地分布到各设备**。
- **实验结果**：多模型规模下一致优于 Adam 与 Muon；1.1B 预训练设定下训练效率 **+21.74%（vs Adam）**、**+11.31%（vs Muon）**，显存占用与 Muon 相当。
- **结论性判断**：**正交化与自适应学习率是互补关系，而非竞争关系**——为优化器设计打开了新方向。

## 代码仓库

| 仓库 | Star | 语言 | 说明 |
|------|------|------|------|
| [zichongli5/NorMuon](https://github.com/zichongli5/NorMuon) | 92 | Python | 官方实现（第一作者 Zichong Li），创建于 2025-10-07（与论文同日） |
| [KellerJordan/Muon](https://github.com/KellerJordan/Muon) | 2,855 | Python | Muon 优化器原始实现 |

## 源笔记摘录

> |10 | 高效训练trick合集 | Muon Optimizer / NorMuon (2025) | arXiv:2507.20534 / 2510.05491 | 搜索 muon-optimizer 社区实现 | ★★☆☆☆ | 显著加速大模型训练，Kimi等公司在用 |

## 勘误与提醒

- ⚠️ 源笔记把 `2507.20534` 与 `2510.05491` 并列为「Muon Optimizer / NorMuon」：`2510.05491` **确实是 NorMuon** ✔，但 `2507.20534` **不是 Muon 论文**，而是 **Kimi K2 技术报告**（[见单独条目](./arxiv_2507.20534.md)）。
- ℹ️ 优化器谱系澄清：
  - **Muon**（KellerJordan 等，正交化更新）→ 原始实现 `KellerJordan/Muon`
  - **MuonClip**（Kimi K2 自研，Muon + QK-clip）→ 见 2507.20534
  - **NorMuon**（本文，Muon + neuron 级自适应学习率）→ `zichongli5/NorMuon`
- 复现难度 ★★☆☆☆：优化器改动局部、可插拔，在既有训练脚本里替换 optimizer 即可对比，是本批中**投入产出比最高**的一条。

## BibTeX

```bibtex
@misc{normuon,
  title  = {NorMuon: Making Muon more efficient and scalable},
  author = {Li, Zichong and Liu, Liming and Liang, Chen and Chen, Weizhu and Zhao, Tuo},
  year   = {2025},
  journal= {arXiv preprint arXiv:2510.05491},
  url    = {https://arxiv.org/abs/2510.05491}
}
```
