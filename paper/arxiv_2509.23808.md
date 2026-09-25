# VERL：RLVR 中的语义空间探索与利用

> 来源：日常笔记 `2026/202605/20260507.md`（清华大学（深圳国际研究生院）方向条目）
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | Semantic-Space Exploration and Exploitation in RLVR for LLM Reasoning |
| 作者 | Fanding Huang, Guanbo Huang, Xiao Fan, Yi He, Xiao Liang, Xiao Chen 等（共 10 人） |
| arXiv | 2509.23808v5 |
| 提交 / 更新 | 2025-09-28 / 2026-04-20 |
| 发表 | **ACL 2026 Findings**（arXiv comment 标注 Accepted） |
| 链接 | https://arxiv.org/abs/2509.23808 |
| 官方代码 | https://github.com/hf618/VERL |
| 主题 | RLVR / 大模型推理 / 表征分析 |

## 一句话结论

论文指出 RLVR 中被广泛讨论的「探索 vs 利用」权衡**很大程度上是一个测量假象**——token 级指标（输出熵、置信度）只反映 next-token 不确定性，不反映推理在多 token 语义结构上的推进。改到**隐状态空间**度量后（ER / ERV / ERA），两者近零相关、可同时提升；据此提出的 **VERL** 用 ER/ERV 塑形 advantage、以更稳定的 ERA 作元控制变量，多基准一致提升，高考 2024 上 **+21.4%**。

## 核心要点

- **问题诊断**：现有做法在 action space 里用 token 级代理指标（输出熵、置信度）操作探索/利用，但 token 级统计量反映的是**下一个 token 的不确定性**，而非推理如何沿多 token 语义结构推进。
- **视角切换**：改在**响应轨迹的 hidden-state 空间**研究探索与利用。
- **三个度量**：
  - **ER（Effective Rank）**——量化表征层面的探索（representational exploration）
  - **ERV（Effective Rank Velocity）**——ER 的时间一阶导数
  - **ERA（Effective Rank Acceleration）**——ER 的时间二阶导数
  - 用 ERV / ERA 刻画**利用式精炼（exploitative refinement）动力学**
- **关键发现**：实证与理论均显示 **ER 与 ERV 在语义空间中近零相关** → 探索能力与利用能力**可以同时提升**，并不必然此消彼长。
- **方法 VERL（Velocity-Exploiting Rank Learning）**：用 ER/ERV 派生的辅助信号**塑形 RLVR 的 advantage**，并把更稳定的 **ERA 作为元控制变量**自适应平衡激励。
- **效果**：跨多个基座模型、多种 RLVR 算法、多个推理基准一致提升，在困难任务上增益尤大（**Gaokao 2024 +21.4%**）。

## 代码仓库

| 仓库 | Star | 创建 | 说明 |
|------|------|------|------|
| [hf618/VERL](https://github.com/hf618/VERL) | 31 | 2025-09-28 | 论文给出的官方代码地址（arXiv 摘要页链接），为 verl 框架的作者分支 |

> ⚠️ 易混淆：名字与字节跳动的 RL 训练框架 **volcengine/verl** 相同，但两者不是一回事。本文的 VERL 是 **Velocity-Exploiting Rank Learning** 方法名。

## 源笔记摘录

> · 清华大学（深圳国际研究生院）
>   · AI推理突破：黄凡丁、黄冠博等，arXiv:2509.23808v2，解决大模型探索与利用的两难问题

## 勘误与提醒

- ✔ 源笔记的作者指认正确：Fanding Huang / Guanbo Huang 即黄凡丁、黄冠博；「解决大模型探索与利用的两难问题」的概括也贴合。
- ℹ️ 源笔记记的是 **v2**，核验时已到 **v5**（2026-04-20），且已被 **ACL 2026 Findings** 接收——引用时请更新版本与发表信息。
- ℹ️ 论文的核心贡献是**推翻**「探索与利用必须权衡」这一前提（指出它是测量假象），而不是提出更强的权衡策略，这点容易被误解。

## BibTeX

```bibtex
@misc{verl2025semantic,
  title  = {Semantic-Space Exploration and Exploitation in RLVR for LLM Reasoning},
  author = {Huang, Fanding and Huang, Guanbo and Fan, Xiao and He, Yi and Liang, Xiao and Chen, Xiao and others},
  year   = {2025},
  journal= {arXiv preprint arXiv:2509.23808},
  note   = {Accepted as an ACL 2026 Findings paper},
  url    = {https://arxiv.org/abs/2509.23808}
}
```
