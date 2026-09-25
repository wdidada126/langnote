# DINOv3：通用视觉基础模型

> 来源：日常笔记 `2026/202603/20260302.md`
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | DINOv3 |
| 作者 | Oriane Siméoni, Huy V. Vo, Maximilian Seitzer, Federico Baldassarre, Maxime Oquab, Cijo Jose 等（共 26 人） |
| arXiv | 2508.10104v1 |
| 提交 / 更新 | 2025-08-13 / 2025-08-13 |
| 发表 | 技术报告（Meta AI） |
| 链接 | https://arxiv.org/abs/2508.10104 |
| 官方代码 | https://github.com/facebookresearch/dinov3 |
| 主题 | 自监督学习 / 视觉基础模型 |

## 一句话结论

DINOv3 靠三件事成为「通用视觉基础模型」里程碑：**数据与模型规模的精细化扩展**、**Gram anchoring**（解决长训练下 dense feature map 退化这一已知未解问题）、**后处理策略**（分辨率/模型尺寸/文本对齐的灵活性）——**无需微调**即在广泛设定上超越各专用 SOTA。

## 核心要点

- **愿景**：自监督学习消除人工标注，使模型能随数据量与架构规模轻松扩展；不针对特定任务/领域设计，用**单一算法**从自然图像到航拍图像学习视觉表征。
- **策略一 规模化**：通过仔细的数据准备、设计与优化，吃透数据集规模与模型规模同时扩展的收益。
- **策略二 Gram anchoring**：专门解决**长训练周期下 dense feature map 退化**这一「已知但长期未解」的问题。
- **策略三 后处理**：进一步增强模型在分辨率、模型尺寸、以及与文本对齐方面的灵活性。
- **结果**：一个通用视觉基础模型，**在不做微调的情况下**，在广泛设定上超越专用 SOTA。
- **产出**：高质量 dense feature，在多种视觉任务上显著超越此前的自监督与弱监督基础模型；同时释出 **DINOv3 视觉模型套件**，覆盖不同资源约束与部署场景。

## 代码仓库

| 仓库 | Star | 语言 | 说明 |
|------|------|------|------|
| [facebookresearch/dinov3](https://github.com/facebookresearch/dinov3) | 11,442 | Jupyter Notebook | 官方 PyTorch 参考实现与模型 |

## 源笔记摘录

> | 7 | 多模态基础模型 | DINOv3 / Perception Encoder (2025) | arXiv:2508.10104 | https://github.com/facebookresearch/perception_models | ★★★☆☆ | 2025视觉表征最强之一 |

## 勘误与提醒

- ⚠️ **仓库给错了**：源笔记给出的 `facebookresearch/perception_models` 是 **Perception Encoder**（另一篇论文，arXiv:2504.13181）的仓库，不是 DINOv3 的。DINOv3 官方仓库是 **`facebookresearch/dinov3`**。
- ⚠️ **「DINOv3 / Perception Encoder」是两篇论文**：源笔记把它们并列当作一条，容易在引用时张冠李戴。本条只覆盖 DINOv3（2508.10104）。
- 复现难度 ★★★☆☆：官方提供预训练权重与 notebook，做特征提取与下游迁移评估很直接，从头自监督预训练门槛高。

## BibTeX

```bibtex
@misc{dinov3,
  title  = {DINOv3},
  author = {Sim{\'e}oni, Oriane and Vo, Huy V. and Seitzer, Maximilian and Baldassarre, Federico and Oquab, Maxime and Jose, Cijo and others},
  year   = {2025},
  journal= {arXiv preprint arXiv:2508.10104},
  url    = {https://arxiv.org/abs/2508.10104}
}
```
