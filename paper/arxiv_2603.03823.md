# SWE-CI：用持续集成评估智能体维护代码库的能力

> 来源：日常笔记 `2026/202604/20260401.md`
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via Continuous Integration |
| 作者 | Jialong Chen, Xander Xu, Hu Wei, Chuan Chen, Bing Zhao（共 5 人） |
| arXiv | 2603.03823v4 |
| 提交 / 更新 | 2026-03-04 / 2026-04-01 |
| 发表 | 未标注会议 |
| 链接 | https://arxiv.org/abs/2603.03823 |
| 官方代码 | https://github.com/SKYLENAGE-AI/SWE-CI |
| 数据集 | https://huggingface.co/datasets/skylenage-ai/SWE-CI |
| 主题 | 代码智能体 / 基准评测 / 软件可维护性 |

## 一句话结论

首个建立在 **CI 循环**之上的仓库级基准，把代码生成的评测范式从「静态、短期的功能正确性」推向「动态、长期的可维护性」——**100 个任务**取自真实仓库的开发历史，平均跨度 **233 天、71 次连续提交**，要求智能体经过**数十轮分析与编码迭代**来解题。

## 核心要点

- **动机**：LLM 智能体在静态 bug 修复等任务上表现不错，但真实世界的成熟软件开发依赖**复杂的需求变更与长期功能迭代**，静态 one-shot 修复范式无法刻画这一点。
- **核心洞察（一句话）**：**可维护性可以通过追踪功能正确性随时间的变化来揭示**（Maintainability can be revealed by tracking how functional correctness changes over time）。
- **基准构成**：100 个任务，每个都源自真实代码仓库，开发历史平均 **233 天、71 次连续提交**；每个任务由 **base commit + reference commit** 组成。
- **任务形式**：要求智能体从 base commit 出发，通过数十轮分析-编码迭代，最终通过 reference commit 的全部测试。
- **双智能体协作工作流**（README 补充），模拟真实团队的 CI 闭环：**Run Tests → Define Requirements → Modify Code**
  - **Architect Agent**：分析自动化测试系统给出的失败信息，做失败归因、代码定位、需求设计，产出自然语言的高层需求文档。
  - **Programmer Agent**：接收需求文档，将其翻译为具体的代码行为规范，规划维护策略并最终实现改动。
- **价值**：提供系统衡量智能体**长期维护代码库**综合能力的平台。

## 代码仓库

| 仓库 | Star | 语言 | 说明 |
|------|------|------|------|
| [SKYLENAGE-AI/SWE-CI](https://github.com/SKYLENAGE-AI/SWE-CI) | 178 | Python | 官方仓库，创建于 2026-02-09；README 明确引用 `arxiv.org/pdf/2603.03823`，确认为官方实现 |

## 源笔记摘录

> 论文来源：SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via Continuous Integration
> arXiv:2603.03823，视频里转述的内容基本没有偏差

## 勘误与提醒

- ✔ 源笔记记录的标题与 arXiv ID 完全正确，是 2026 年笔记中标注质量最好的几条之一。
- ℹ️ 源笔记后半句「视频里转述的内容基本没有偏差」是对某个视频节目的观感记录，非论文信息。
- ℹ️ 与 SWE-Bench 的关系：SWE-Bench 评测的是**一次性修好某个 issue**（静态正确性）；SWE-CI 评测的是**沿着一段真实开发历史持续保持正确**（可维护性）。两者互补，不是替代关系。

## BibTeX

```bibtex
@misc{sweci2026,
  title  = {SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via Continuous Integration},
  author = {Chen, Jialong and Xu, Xander and Wei, Hu and Chen, Chuan and Zhao, Bing},
  year   = {2026},
  journal= {arXiv preprint arXiv:2603.03823},
  url    = {https://arxiv.org/abs/2603.03823}
}
```
