# 用 MDS 码加速分布式存储系统中单节点的数据访问

> 来源：日常笔记 `2026/202603/20260302.md`（分布式存储推荐列表第 5 条）
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | Accelerating Data Access for Single Node in Distributed Storage Systems via MDS Codes |
| 作者 | Hao Shi, Zhengyi Jiang, Zhongyi Huang, Linqi Song, Hanxu Hou（共 5 人） |
| arXiv | 2501.11353v1 |
| 提交 / 更新 | 2025-01-20 / 2025-01-20 |
| 发表 | 未标注会议 |
| 链接 | https://arxiv.org/abs/2501.11353 |
| 官方代码 | 无（理论与仿真为主） |
| 主题 | 分布式存储 / 纠删码 / 访问延迟优化 |

## 一句话结论

既有研究多关注**整个文件**的访问延迟，而本文指出**单节点的数据访问延迟同样重要**：给出两个算法降低 MDS 码下单节点访问延迟，理论上在**均匀分布**下期望降低比例为 **(n-k)(n-k+1) / (n(n+1))**、**移位指数分布**下为 **(n-k)/n**；最坏情况分析显示 **(n,k)=(3,2)** 时降低比例超过 **60%**。

## 核心要点

- **背景**：MDS（Maximum Distance Separable）阵列码在现代分布式存储系统中被广泛使用，以**极小的存储开销**提供高数据可靠性。
- **被忽视的点**：与整个文件的访问延迟相比，**分布式存储系统中单个节点的数据访问延迟同样重要**。
- **贡献**：提出**两个算法**，分别针对不同场景下 MDS 码的单节点数据访问延迟。
- **理论结果**（`n` = 全部节点数，`k` = 数据节点数）：
  - 延迟服从**均匀分布**时，期望降低比例 = **((n-k)(n-k+1)) / (n(n+1))**
  - 延迟服从**移位指数分布（shifted-exponential）**时，期望降低比例 = **(n-k) / n**
- **最坏情况分析**：当 **(n,k) = (3,2)** 时，降低比例**超过 60%**。
- **验证**：用**蒙特卡洛仿真**证明相比基线算法延迟更低。

## 代码仓库

| 仓库 | Star | 说明 |
|------|------|------|
| [tsuraan/Jerasure](https://github.com/tsuraan/Jerasure) | 314 | Jerasure 库主仓库（Reed-Solomon 编码的 C 实现），复现纠删码算法的首选 |
| [ceph/jerasure](https://github.com/ceph/jerasure) | 36 | Ceph 的只读镜像（README 自述 upstream 在别处） |
| Intel ISA-L | — | 源笔记同节提到的高性能 EC 库，适合做性能对比 |

## 源笔记摘录

> | 5 | 2025 | Accelerating Data Access for Single Node via MDS Codes | 单节点访问延迟优化，MDS 码加速 | https://arxiv.org/abs/2501.11353 | 未见官方代码，数学推导为主，可基于 jerasure 复现 | ★★★☆☆ | ★★★☆☆ |

## 勘误与提醒

- ✔ 源笔记的判断**完全准确**：「未见官方代码，数学推导为主，可基于 jerasure 复现」——核验后本文确无官方仓库，正文以理论推导 + 蒙特卡洛仿真为主。
- ℹ️ 源笔记未记录理论公式，此处已补齐两个期望降低比例与最坏情况结论——这是本文最可直接引用的部分。
- ℹ️ 若要用 jerasure 复现，注意 `ceph/jerasure` 只是只读镜像，应克隆 `tsuraan/Jerasure`。

## BibTeX

```bibtex
@misc{shi2025mds,
  title  = {Accelerating Data Access for Single Node in Distributed Storage Systems via MDS Codes},
  author = {Shi, Hao and Jiang, Zhengyi and Huang, Zhongyi and Song, Linqi and Hou, Hanxu},
  year   = {2025},
  journal= {arXiv preprint arXiv:2501.11353},
  url    = {https://arxiv.org/abs/2501.11353}
}
```
