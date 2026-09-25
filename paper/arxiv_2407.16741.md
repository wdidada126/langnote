# OpenHands：面向 AI 软件开发者的通用智能体开放平台

> 来源：日常笔记 `2026/202603/20260302.md`
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | OpenHands: An Open Platform for AI Software Developers as Generalist Agents |
| 作者 | Xingyao Wang, Boxuan Li, Yufan Song, Frank F. Xu, Xiangru Tang, Mingchen Zhuge 等（共 24 人） |
| arXiv | 2407.16741v3 |
| 提交 / 更新 | 2024-07-23 / 2025-04-18 |
| 发表 | ICLR 2025（arXiv comment 标注 Accepted） |
| 链接 | https://arxiv.org/abs/2407.16741 |
| 官方代码 | https://github.com/OpenHands/OpenHands |
| 主题 | Agentic Coding / 软件工程智能体 |

## 一句话结论

OpenHands（前身 OpenDevin）把「像人一样写代码的 Agent」做成了**通用平台**而不是单个 Agent：统一事件流 + 沙箱运行时 + 多 Agent 协作 + 基准接入，屏蔽底层模型差异，让新 Agent 的实现只需关注策略本身。

## 核心要点

- **OpenHands = f.k.a. OpenDevin**，论文摘要中明确写出这一更名关系。
- 三种与世界的交互方式：**写代码**、**操作命令行**、**浏览网页**——对应人类开发者的核心动作。
- 平台能力四件套：
  1. 实现新 Agent 的抽象与接口
  2. 与沙箱环境的**安全交互**（代码执行隔离）
  3. **多 Agent 之间的协调**
  4. **内置评测基准**的接入
- 评测覆盖 **15 个高难任务**，横跨软件工程（SWE-BENCH）与网页浏览（WEBARENA）两大类。
- MIT 宽松许可；社区项目，**188+ 贡献者、2.1K+ 次贡献**，横跨学界与工业界。

## 代码仓库

| 仓库 | Star | 语言 | 说明 |
|------|------|------|------|
| [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | 89,098 | TypeScript | 官方仓库；组织由 `All-Hands-AI` 更名而来，`All-Hands-AI/OpenHands` 会自动跳转 |

## 源笔记摘录

> | 8 | Agentic Coding | OpenDevin / AutoDev (2024–2025) | arXiv:2407.16741 | https://github.com/OpenDevin/OpenDevin | ★★★☆☆ | 写代码Agent最知名开源框架 |

## 勘误与提醒

- ⚠️ **题名**：源笔记写的「OpenDevin / AutoDev」中，AutoDev 是另一个项目（微软，arXiv:2404.10700），与本文无关。本文题名是 **OpenHands**。
- ⚠️ **仓库地址已变**：`github.com/OpenDevin/OpenDevin` 已随项目更名迁移为 `github.com/OpenHands/OpenHands`，组织名也从 `All-Hands-AI` 改为 `OpenHands`。按旧地址访问会跳转，但引用时建议用新地址。
- 复现难度 ★★★☆☆：本地起 Docker 沙箱跑通 SWE-Bench 子集是可行的入门路径。

## BibTeX

```bibtex
@misc{openhands2024,
  title  = {OpenHands: An Open Platform for AI Software Developers as Generalist Agents},
  author = {Wang, Xingyao and Li, Boxuan and Song, Yufan and Xu, Frank F. and Tang, Xiangru and Zhuge, Mingchen and others},
  year   = {2024},
  journal= {arXiv preprint arXiv:2407.16741},
  note   = {Accepted by ICLR 2025},
  url    = {https://arxiv.org/abs/2407.16741}
}
```
