# BitNet b1.58 2B4T 技术报告

> 来源：日常笔记 `2026/202603/20260302.md`
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | BitNet b1.58 2B4T Technical Report |
| 作者 | Shuming Ma, Hongyu Wang, Shaohan Huang, Xingxing Zhang, Ying Hu, Ting Song 等（共 8 人） |
| arXiv | 2504.12285v2 |
| 提交 / 更新 | 2025-04-16 / 2025-04-25 |
| 发表 | 技术报告；arXiv comment 标注 **Work in progress** |
| 链接 | https://arxiv.org/abs/2504.12285 |
| 官方代码 | https://github.com/microsoft/BitNet |
| 主题 | 1-bit 量化 LLM / 高效推理 |

## 一句话结论

首个**开源的、原生的 20 亿参数 1-bit LLM**：在 4 万亿 token 上训练，性能与同规模领先的开源全精度模型相当，但**显存占用、能耗、解码延迟**显著更低。

## 核心要点

- **首个** 2B 规模的开源原生 1-bit LLM（不是后训练量化，是训练时就按 1.58 bit 做）。
- 训练语料 **4 万亿 token**。
- 评测覆盖四个维度：语言理解、数学推理、代码能力、对话能力。
- 结果与同规模领先开源**全精度**权重模型 **on par**（相当）。
- 效率收益三件套：**显存占用**大幅下降、**能耗**下降、**解码延迟**下降。
- 权重通过 Hugging Face 释出，同时开源了 **GPU 与 CPU 两种架构的推理实现**（bitnet.cpp）。

## 代码仓库

| 仓库 | Star | 语言 | 说明 |
|------|------|------|------|
| [microsoft/BitNet](https://github.com/microsoft/BitNet) | 40,346 | C++ | 官方 1-bit LLM 推理框架 |

## 源笔记摘录

> | 3 | 高效小模型推理 | BitNet b1.58 2B4T / Ternary LLM (2025) | arXiv:2504.12285 | https://github.com/microsoft/BitNet (社区版很多) | ★★☆☆☆ | 1-bit/三值量化真正落地，内存占用暴降 |

## 勘误与提醒

- ✔ 源笔记的标题、ID、仓库、推荐理由均正确。
- ℹ️ 源笔记把 `/ Ternary LLM` 并列写在标题里——三值（ternary，即 -1/0/1）正是 b1.58 的含义，属于补充说明而非另一篇论文。
- ℹ️ 论文标注为 **Work in progress**，数值与结论后续可能更新，引用时注意版本。
- 复现难度 ★★☆☆☆：官方提供 CPU 推理实现，普通笔记本即可跑通，是本批里最容易上手的一条。

## BibTeX

```bibtex
@misc{bitnetb158,
  title  = {BitNet b1.58 2B4T Technical Report},
  author = {Ma, Shuming and Wang, Hongyu and Huang, Shaohan and Zhang, Xingxing and Hu, Ying and Song, Ting and others},
  year   = {2025},
  journal= {arXiv preprint arXiv:2504.12285},
  note   = {Work in progress},
  url    = {https://arxiv.org/abs/2504.12285}
}
```
