# Hydra：基于 NDN 的联邦式数据仓储

> 来源：日常笔记 `2026/202603/20260302.md`（分布式存储推荐列表第 4 条）
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | Hydra -- A Federated Data Repository over NDN |
| 作者 | Justin Presley, Xi Wang, Tym Brandel, Xusheng Ai, Proyash Podder, Tianyuan Yu 等（共 11 人） |
| arXiv | 2211.00919v1 |
| 提交 / 更新 | 2022-11-02 / 2022-11-02 |
| 发表 | 技术报告（NDN 项目组） |
| 链接 | https://arxiv.org/abs/2211.00919 |
| 官方代码 | ⚠️ 源笔记给出的 `named-data/hydra` **已 404**；实际可用实现为 https://github.com/justincpresley/ndn-hydra |
| 主题 | 分布式存储 / 命名数据网络（NDN） |

## 一句话结论

Hydra 是一个跑在**命名数据网络（NDN）**上的安全、分布式、去中心化数据仓储：用 **State Vector Sync (SVS)** 让各节点维护系统「全局视图」，靠 NDN 内建的 **data anycast + 网内缓存**实现可扩展分发，用本地计算的 **Favor 值**决定哪些节点复制文件，并由 **NOC** 引导信任与签发证书。

## 核心要点

- **要解决的问题**：大数据科学社区在**应用层**做数据发布与复制，结果是两极分化——
  - 集中式仓储：发布流程繁重，且不接收所有数据集
  - ad-hoc 仓储：因命名、元数据标准、访问方式各异而**难以发现和使用**
- **架构**：由**用户社区提供的存储服务器（节点）组成的松散联邦**。
- **底层**：运行在 NDN 之上，使用 **State Vector Sync (SVS)** 协议，使各节点能维护系统的 global view。
- **可扩展性**：靠 NDN 内建的 **data anycast** 与 **in-network caching**。
- **韧性**：通过**自动故障检测** + **维持特定复制度**，抵御单个服务器失效。
- **复制决策**：用 **Favor**——一个**本地计算出的数值**——决定哪些节点将复制某个文件。
- **安全**：采用 **data-centric security** 做数据发布与节点认证。
- **信任引导**：设 **NOC（Network Operation Center）**，负责分发用户与节点证书、执行 proof-of-possession 挑战。
- **文档定位**：本文是 Hydra 的**参考技术报告**，给出设计决策、决策理由、功能模块与协议规范。

## 代码仓库

| 仓库 | Star | 说明 |
|------|------|------|
| [justincpresley/ndn-hydra](https://github.com/justincpresley/ndn-hydra) | 4 | 实际可用实现（Python 编写的 NDN 分布式仓储）；第一作者 Justin Presley 的个人仓库 |
| ~~named-data/hydra~~ | — | ❌ **404，仓库不存在**（源笔记给出的地址） |

## 源笔记摘录

> | 4 | 2022–2023 | Hydra: NDN-based Federated Data Repository | 基于 Named Data Networking 的去中心化存储 | https://arxiv.org/abs/2211.00919 | https://github.com/named-data/hydra (NDN 项目组) | ★★★★☆ | ★★★☆☆ |

## 勘误与提醒

- ⚠️ **仓库地址失效**：源笔记标注的 `github.com/named-data/hydra`（并注明「NDN 项目组」）经 GitHub API 查询返回 **404，该仓库不存在**。真正可用的实现是 `justincpresley/ndn-hydra`（仅 4 star，Python 实现）。
- ℹ️ 因此源笔记「NDN 项目组官方仓库」的判断不成立——**本条的实际复现难度高于标注的 ★★★★☆**，因为缺少成熟官方实现，需要自行搭建 NDN 环境（NFD / ndn-cxx 等）。
- ℹ️ 源笔记标题写作「Hydra: NDN-based Federated Data Repository」，正式题名是 `Hydra -- A Federated Data Repository over NDN`。

## BibTeX

```bibtex
@misc{hydra2022,
  title  = {Hydra -- A Federated Data Repository over NDN},
  author = {Presley, Justin and Wang, Xi and Brandel, Tym and Ai, Xusheng and Podder, Proyash and Yu, Tianyuan and others},
  year   = {2022},
  journal= {arXiv preprint arXiv:2211.00919},
  url    = {https://arxiv.org/abs/2211.00919}
}
```
