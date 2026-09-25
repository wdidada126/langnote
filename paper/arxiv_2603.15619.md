# MoDA：混合深度注意力（Mixture-of-Depths Attention）

> 来源：日常笔记 `2026/202605/20260507.md`（华中科技大学方向条目）
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | Mixture-of-Depths Attention |
| 作者 | Lianghui Zhu, Yuxin Fang, Bencheng Liao, Shijie Wang, Tianheng Cheng, Zilong Huang 等（共 13 人） |
| arXiv | 2603.15619v1 |
| 提交 / 更新 | 2026-03-16 / 2026-03-16 |
| 发表 | 未标注会议 |
| 链接 | https://arxiv.org/abs/2603.15619 |
| 官方代码 | https://github.com/hustvl/MoDA |
| 主题 | LLM 架构 / 深度扩展 / 注意力机制 |

## 一句话结论

针对「模型变深后浅层的有效特征被反复残差更新稀释、深层难以恢复」这一问题，MoDA 让**每个注意力头同时关注当前层的 sequence KV 与前序层的 depth KV**；1.5B 实验下 10 个验证基准困惑度平均降 **0.2**、10 个下游任务平均提升 **2.11%**，而 FLOPs 开销仅 **3.7%**。

## 核心要点

- **问题**：加深（depth scaling）是 LLM 能力的关键驱动，但模型变深后常出现**信号退化**——浅层形成的信息性特征被重复的残差更新逐渐稀释，深层更难恢复。
- **MoDA 机制**：每个注意力头同时 attend 到
  1. **当前层的 sequence KV pairs**
  2. **前序层的 depth KV pairs**
- **硬件高效算法**：解决了非连续内存访问模式问题，在 **64K 序列长度**下达到 **FlashAttention-2 效率的 97.3%**。
- **实验（1.5B 模型）**：
  - 10 个验证基准上**平均困惑度降低 0.2**
  - 10 个下游任务上**平均性能提升 2.11%**
  - **FLOPs 计算开销仅 3.7%**（可忽略）
- **额外发现**：MoDA 搭配 **post-norm** 比搭配 **pre-norm** 效果更好。
- **定位**：一个用于 depth scaling 的、有前景的基础原语（primitive）。

## 代码仓库

| 仓库 | Star | 语言 | 说明 |
|------|------|------|------|
| [hustvl/MoDA](https://github.com/hustvl/MoDA) | 280 | Python | 官方实现（华中科技大学 hustvl）；arXiv comment 直接给出该地址 |

## 源笔记摘录

> · 华中科技大学
>   · MoDA 混合注意力机制：与字节跳动Seed团队合作，arXiv:2603.15619

## 勘误与提醒

- ✔ 源笔记的 ID 与「MoDA 混合注意力机制」的描述正确；「与字节跳动 Seed 团队合作」与作者列表中的 hustvl 成员（Lianghui Zhu、Bencheng Liao 等）情况吻合。
- ℹ️ 源笔记未给仓库地址，arXiv comment 中明确写着 `Code is released at https://github.com/hustvl/MoDA`，此处已补齐。
- ℹ️ 名字易混：MoDA（Mixture-of-**Depths** Attention，本文）与 MoA（Mixture-of-Attention）、MoD（Mixture-of-Depths，DeepMind 的 token 级动态深度）是不同工作，检索时注意区分。

## BibTeX

```bibtex
@misc{moda2026,
  title  = {Mixture-of-Depths Attention},
  author = {Zhu, Lianghui and Fang, Yuxin and Liao, Bencheng and Wang, Shijie and Cheng, Tianheng and Huang, Zilong and others},
  year   = {2026},
  journal= {arXiv preprint arXiv:2603.15619},
  note   = {Code: https://github.com/hustvl/MoDA},
  url    = {https://arxiv.org/abs/2603.15619}
}
```
