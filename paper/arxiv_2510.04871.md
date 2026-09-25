# TRM：用小网络递归推理，少即是多

> 来源：日常笔记 `2026/202603/20260302.md`
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | Less is More: Recursive Reasoning with Tiny Networks |
| 作者 | Alexia Jolicoeur-Martineau（1 人，Samsung SAIL Montreal / Mila） |
| arXiv | 2510.04871v1 |
| 提交 / 更新 | 2025-10-06 / 2025-10-06 |
| 发表 | 未标注会议 |
| 链接 | https://arxiv.org/abs/2510.04871 |
| 官方代码 | https://github.com/SamsungSAILMontreal/TinyRecursiveModels |
| 主题 | 递归推理 / ARC-AGI / 小模型 |

## 一句话结论

TRM 用**单个仅 2 层、7M 参数**的小网络做递归推理，比 HRM 更简单却泛化得更好：ARC-AGI-1 达 **45%**、ARC-AGI-2 达 **8%**，在不到 LLM **0.01%** 参数量的情况下超过 DeepSeek R1、o3-mini、Gemini 2.5 Pro。

## 核心要点

- **前身 HRM**（Hierarchical Reasoning Model）：用**两个以不同频率递归的小网络**（27M 参数、约 1000 条训练样本），在 Sudoku、Maze、ARC-AGI 等困难谜题上击败 LLM。思路受生物启发。
- **HRM 的不足**：机制尚未被充分理解，且可能**次优**。
- **TRM 的简化**：**单个 tiny network、仅 2 层**，递归式推理。更简单，却取得**显著更高的泛化能力**。
- **结果**：**7M 参数**取得 ARC-AGI-1 **45%**、ARC-AGI-2 **8%** 测试准确率。
- **对比**：高于多数 LLM（DeepSeek R1、o3-mini、Gemini 2.5 Pro），而参数量不到其 **0.01%**。

## 代码仓库

| 仓库 | Star | 语言 | 说明 |
|------|------|------|------|
| [SamsungSAILMontreal/TinyRecursiveModels](https://github.com/SamsungSAILMontreal/TinyRecursiveModels) | 6,559 | Python | **官方实现** |
| [lucidrains/tiny-recursive-model](https://github.com/lucidrains/tiny-recursive-model) | 192 | — | 非官方实现（lucidrains 风格复现） |
| [olivkoch/nano-trm](https://github.com/olivkoch/nano-trm) | 127 | — | 非官方实现，nano 系列教学向 |

## 源笔记摘录

> | 6 | 小模型ARC突破 | Less is More: Recursive Reasoning with Tiny Networks (2025) | arXiv:2510.04871 | 社区实现较多，搜索 ARC prize 2025 | ★★★★☆ | 7M 模型打败很多大模型，极致效率路线 |

## 勘误与提醒

- ✔ 源笔记的标题、ID、以及「7M 模型打败很多大模型」的判断**全部正确**。
- ℹ️ 源笔记写「社区实现较多，搜索 ARC prize 2025」，但实际上**存在官方仓库** `SamsungSAILMontreal/TinyRecursiveModels`（6.5k+ star），应优先使用。
- 复现难度 ★★★★☆（源笔记评级）：模型小、单卡可训，但 ARC 数据准备与递归训练细节是主要门槛——本批中「算力门槛最低但工程细节最磨人」的一条。

## BibTeX

```bibtex
@misc{trm2025,
  title  = {Less is More: Recursive Reasoning with Tiny Networks},
  author = {Jolicoeur-Martineau, Alexia},
  year   = {2025},
  journal= {arXiv preprint arXiv:2510.04871},
  url    = {https://arxiv.org/abs/2510.04871}
}
```
