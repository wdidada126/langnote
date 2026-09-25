# DeepSeek-V3 技术报告

> 来源：日常笔记 `2026/202603/20260302.md`
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | DeepSeek-V3 Technical Report |
| 作者 | DeepSeek-AI, Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu 等（共 200 人） |
| arXiv | 2412.19437v2 |
| 提交 / 更新 | 2024-12-27 / 2025-02-18 |
| 发表 | 技术报告（DeepSeek-AI 官方） |
| 链接 | https://arxiv.org/abs/2412.19437 |
| 官方代码 / 权重 | https://github.com/deepseek-ai/DeepSeek-V3 |
| 主题 | 大模型架构 / MoE / 高效训练 |

## 一句话结论

671B 总参数、每 token 仅激活 37B 的 MoE 模型，靠 **MLA + DeepSeekMoE + 无辅助损失负载均衡 + MTP** 四件套，用 **2.788M H800 GPU 小时**完成 14.8T token 预训练，全程**无不可恢复 loss spike、无回滚**，性能追平头部闭源模型。

## 核心要点

- **架构**：Multi-head Latent Attention (MLA) + DeepSeekMoE，两者在 DeepSeek-V2 上已充分验证。
- **首创 auxiliary-loss-free 负载均衡策略**：不依赖辅助损失（辅助损失会损伤模型质量），改用动态偏置项调节专家负载。
- **MTP（Multi-Token Prediction）训练目标**：一次预测多个 token，提升性能并可用于推测解码加速。
- **训练规模**：14.8 万亿高质量多样化 token 预训练 → SFT → RL。
- **成本**：全流程仅 2.788M H800 GPU 小时。
- **稳定性**：整个训练过程**没有出现任何不可恢复的 loss spike，也没有做过任何回滚**——这点在 671B 规模上极其罕见。
- 开源权重释出于 `deepseek-ai/DeepSeek-V3`。

## 代码仓库

| 仓库 | Star | 语言 | 说明 |
|------|------|------|------|
| [deepseek-ai/DeepSeek-V3](https://github.com/deepseek-ai/DeepSeek-V3) | 104,489 | Python | 官方权重与推理代码 |
| [deepseek-ai/DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1) | 91,972 | — | 同源的 R1 推理模型（源笔记把两者并列提及） |

## 源笔记摘录

> | 1 | 开源推理大模型 | DeepSeek-R1 / DeepSeek-V3 (2025) | arXiv:2412.19437 / 2502.02523 | https://github.com/deepseek-ai/DeepSeek-V3 | ★★☆☆☆ | 2025最震撼开源模型之一，性价比极高，MoE+MLA实现 |

## 勘误与提醒

- ⚠️ 源笔记把 `2412.19437` 与 `2502.02523` 并列标为「DeepSeek-R1 / DeepSeek-V3」，**容易误导**：
  - `2412.19437` = DeepSeek-V3 官方技术报告 ✔
  - `2502.02523` = 第三方快评文章《Brief analysis of DeepSeek R1 and its implications for Generative AI》，**不是 DeepSeek 官方论文**，已单独立条见 [arxiv_2502.02523.md](./arxiv_2502.02523.md)。
- 复现难度 ★★☆☆☆（源笔记评级）：官方权重与推理代码齐全，跑通推理不难，从头预训练不可行。

## BibTeX

```bibtex
@misc{deepseekv3,
  title  = {DeepSeek-V3 Technical Report},
  author = {DeepSeek-AI and Liu, Aixin and Feng, Bei and Xue, Bing and Wang, Bingxuan and Wu, Bochao and others},
  year   = {2024},
  journal= {arXiv preprint arXiv:2412.19437},
  url    = {https://arxiv.org/abs/2412.19437}
}
```
