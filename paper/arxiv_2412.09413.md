# STILL-2：模仿、探索与自我改进（慢思考推理系统复现报告）

> 来源：日常笔记 `2026/202603/20260302.md`
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | Imitate, Explore, and Self-Improve: A Reproduction Report on Slow-thinking Reasoning Systems |
| 作者 | Yingqian Min, Zhipeng Chen, Jinhao Jiang, Jie Chen, Jia Deng, Yiwen Hu 等（共 14 人） |
| arXiv | 2412.09413v2 |
| 提交 / 更新 | 2024-12-12 / 2024-12-22 |
| 发表 | 技术报告；arXiv comment：**Technical Report on Slow Thinking with LLMs: Part II** |
| 链接 | https://arxiv.org/abs/2412.09413 |
| 官方代码 | https://github.com/RUCAIBox/Slow_Thinking_with_LLMs |
| 主题 | 慢思考 / o1 类推理系统复现 |

## 一句话结论

o1 这类慢思考系统由工业界掌握、核心技术不公开；本文给出一套**可复现的三阶段方案 STILL-2**——**模仿**（蒸馏长思维数据微调，让模型进入慢思考模式）→ **探索**（对难题生成多个 rollout，产出更多正确轨迹）→ **自我改进**（迭代精炼训练集）——在三个高难基准上达到与工业级推理系统可比的性能。

## 核心要点

- **动机**：慢思考系统（如 o1）在回答前进行扩展思考，产出更充分、准确、有据的解答；但主要由工业界维护，核心技术未公开。
- **阶段一 Imitate**：用**蒸馏得到的长形式思维数据**微调推理模型，使其能够**唤起 slow-thinking 模式**。
- **阶段二 Explore**：鼓励模型对**有挑战性的问题**生成多个 rollout，从而产出越来越多通向正确答案的高质量轨迹。
- **阶段三 Self-Improve**：通过**迭代精炼训练数据集**实现自我改进。
- **验证**：在三个高难基准上做大量实验，性能与工业级推理系统相比**具有竞争力（competitive）**。
- 属于 "Slow Thinking with LLMs" 技术报告系列的 **Part II**。

## 代码仓库

| 仓库 | Star | 语言 | 说明 |
|------|------|------|------|
| [RUCAIBox/Slow_Thinking_with_LLMs](https://github.com/RUCAIBox/Slow_Thinking_with_LLMs) | 769 | Python | 官方仓库（人民大学高瓴 RUCAIBox），慢思考 LLM 系列技术报告 |

## 源笔记摘录

> | 4 | 慢思考/推理训练 | o1-like Reproduction (STILL / DeepSeek-R1风格) | arXiv:2412.09413 | https://github.com/RUCAIBox/Slow_Thinking_with_LLMs | ★★★★☆ | 复现 o1 思路最完整开源方案之一 |

## 勘误与提醒

- ✔ 源笔记的 ID、仓库与「复现 o1 思路」的定位正确。
- ℹ️ 源笔记标题写作「o1-like Reproduction (STILL / DeepSeek-R1风格)」，是描述性概括；论文正式名是 *Imitate, Explore, and Self-Improve*，方法代号 **STILL-2**。
- 复现难度 ★★★★☆（源笔记评级）：需要长思维链蒸馏数据 + 大规模 rollout 采样，算力门槛是本批中较高的。

## BibTeX

```bibtex
@misc{still2,
  title  = {Imitate, Explore, and Self-Improve: A Reproduction Report on Slow-thinking Reasoning Systems},
  author = {Min, Yingqian and Chen, Zhipeng and Jiang, Jinhao and Chen, Jie and Deng, Jia and Hu, Yiwen and others},
  year   = {2024},
  journal= {arXiv preprint arXiv:2412.09413},
  note   = {Technical Report on Slow Thinking with LLMs: Part II},
  url    = {https://arxiv.org/abs/2412.09413}
}
```
