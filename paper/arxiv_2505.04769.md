# VLA 模型综述：概念、进展、应用与挑战

> 来源：日常笔记 `2026/202603/20260302.md`
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | Vision-Language-Action (VLA) Models: Concepts, Progress, Applications and Challenges |
| 作者 | Ranjan Sapkota, Yang Cao, Konstantinos I. Roumeliotis, Manoj Karkee（共 4 人） |
| arXiv | 2505.04769v2 |
| 提交 / 更新 | 2025-05-07 / 2026-01-29 |
| 发表 | 综述（Foundational Review） |
| 链接 | https://arxiv.org/abs/2505.04769 |
| 官方仓库 | https://github.com/Applied-AI-Research-Lab/Vision-Language-Action-Models-Concepts-Progress-Applications-and-Challenges |
| 主题 | 具身智能 / 视觉-语言-动作模型 |

## 一句话结论

一篇系统性综述：在单一计算框架内统一**感知、自然语言理解与具身动作**，覆盖近三年 **80+ 个 VLA 模型**，按五大主题支柱组织，并给出自动驾驶、机器人、精准农业、AR 等应用版图与挑战路线图。

## 核心要点

- **目标**：VLA 模型把视觉-语言模型（VLM）、动作规划器（action planners）与分层控制器（hierarchical controllers）紧耦合为通才智能体。
- **方法论**：采用严格的文献综述框架，覆盖**过去三年发表的 80+ 个 VLA 模型**。
- **五大主题支柱**构成全文骨架（概念基础 → 架构 → 训练 → 推理/应用 → 挑战）。
- **演进脉络**：从跨模态学习架构 → 通才智能体。
- **关键进展三块**：架构创新、高效训练策略、实时推理加速。
- **应用领域**：自动驾驶、医疗机器人、工业机器人、精准农业、人形机器人、增强现实。
- **挑战**：agentic adaptation、跨本体（cross-embodiment）规划，文中给出了对应解法。
- **路线图**：VLA 模型、VLM 与 agentic AI 三者收敛，走向社会化对齐、自适应、通用的具身智能体。

## 代码仓库

| 仓库 | Star | 说明 |
|------|------|------|
| [Applied-AI-Research-Lab/Vision-Language-Action-Models-...](https://github.com/Applied-AI-Research-Lab/Vision-Language-Action-Models-Concepts-Progress-Applications-and-Challenges) | 20 | 综述官方索引仓库（收集文献列表，非模型实现） |
| [openvla/openvla](https://github.com/openvla/openvla) | 7,074 | 开源 VLA 模型实现，动手实践首选（源笔记亦建议搜 OpenVLA） |

## 源笔记摘录

> | 5 | 视觉-语言-动作 | CoA-VLA / Vision-Language-Action (2025) | arXiv:2505.04769 | 搜索 VLA 或 OpenVLA 社区实现 | ★★★☆☆ | 机器人/具身智能最热门方向 |

## 勘误与提醒

- ⚠️ **「CoA-VLA」不是本文内容**：源笔记把标题写成「CoA-VLA / Vision-Language-Action」，但 arXiv:2505.04769 是一篇**综述**，并不提出名为 CoA-VLA 的模型。引用时请直接使用正式题名。
- ℹ️ 本文是综述，本身没有可复现的模型代码；要动手应转向 OpenVLA 等具体实现。
- 复现难度 ★★★☆☆：作为方向入口的阅读成本远低于动手成本。

## BibTeX

```bibtex
@misc{sapkota2025vla,
  title  = {Vision-Language-Action (VLA) Models: Concepts, Progress, Applications and Challenges},
  author = {Sapkota, Ranjan and Cao, Yang and Roumeliotis, Konstantinos I. and Karkee, Manoj},
  year   = {2025},
  journal= {arXiv preprint arXiv:2505.04769},
  url    = {https://arxiv.org/abs/2505.04769}
}
```
