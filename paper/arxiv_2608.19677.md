# CacheRoute：面向大规模 LLM 服务的规划式前缀亲和路由

> 来源：日常笔记 `2026/202609/20260905.md`（原文是一段 12 条的完整中文精读笔记）
> 整理日期：2026-09-25 ｜ arXiv 元数据经 `export.arxiv.org` API 核验

## 元信息

| 项 | 值 |
|----|-----|
| 标题 | CacheRoute: Planned Prefix-Affinity Routing for Large-Scale LLM Serving |
| 作者 | Huang Cheng（1 人） |
| arXiv | 2608.19677v1 |
| 提交 / 更新 | 2026-08-20 / 2026-08-20 |
| 发表 | 未标注会议 |
| 链接 | https://arxiv.org/abs/2608.19677 |
| 官方代码 | ⚠️ **未见官方仓库**（详见下文勘误） |
| 主题 | LLM 服务 / KV Cache / 负载均衡路由 |

## 一句话结论

Prefix 缓存**只有**在重复请求回到**仍持有该 prefix KV 的节点**时才省掉 prefill；CacheRoute 用一张**周期性更新的路由规划表**，把「高频业务 Key 的缓存局部性」与「服务节点负载」放进同一个优化目标：高频 Key 纳入 warm set，按预计负载用 LPT 放置。Llama-3.3-70B fp8 在 60 张 H100 上，p99 ≤ 3.5s SLO 下达 **176±11 QPS**，是最强对照的 **2.3 倍**；KV 命中率 **64.1% → 93.2%**。

## 核心要点

### 问题

- Prefix caching 的收益依赖「重复请求回到仍持有该 prefix KV 的服务器」。
- **缓存盲（cache-blind）的负载均衡**会把重复前缀打散到多个节点 → 复用消失。
- **固定亲和性**保住了复用，但会把热门业务压在单个队列上 → 过载。
- 节点越多，重复请求在回到同一节点前被淘汰的风险越高。

### 规划流程（周期性路由表）

1. 按业务 Key 的**历史请求速率**，把高频 Key 纳入 **warm set**
2. 按**单节点负载目标**决定目的节点的数量
3. 用 **LPT（最长处理时间优先）**把预计负载从高到低放置到较轻的节点

### 在线请求

- 进入 warm set 的请求：**只在固定的目的节点集合中**选择当前负载较小者
- 长尾请求：继续用 **power-of-two choices**
- 规划表在一个控制周期内保持稳定

### 主实验

- Llama-3.3-70B fp8，**60 张 H100、30 个 TP2 目的节点**
- p99 ≤ 3.5s SLO 下 **176±11 QPS**，约为最强对照的 **2.3 倍**
- 服务端 **token-weighted KV 命中率** 从 Flat-LB 的 **64.1±1.3%** 提升到 **93.2±0.5%**
- 100 QPS 时 **p99 TTFT 为 1.8s** → 命中率提升并没有把队列压成新的瓶颈

### 复制（replication）的真实角色

- 主 70B 分布里**所有 Key 的目的节点数量都是 1**
- 核心结果来自：高频准入 + 稳定的单副本亲和 + 均衡放置
- 复制只在受控的 8B 热点实验中才真正发挥作用

### 机制消融（人为注入超级热门 Key 的 8B 实验）

| 配置 | KV 命中率 | 负载不均衡 | 容量 |
|------|-----------|-----------|------|
| 基线 | 56% | 1.00× | 240 QPS |
| + affinity | 88% | 3.46× | 240 QPS |
| + affinity + 复制 | — | — | 未提高容量 |
| + affinity + 复制 + LPT | — | **1.24×** | **≥500 QPS** |

> 关键读法：**单加亲和性只提命中率、不提容量**；真正把容量做上去的是 **LPT 均衡放置**。

### 失败场景（反例，论文自己给出）

- 两组 32B 负载：命中率虽然从 **1.1% → 11.8%**、**0.8% → 8.5%**
- 但第一组**容量降到 Flat-LB 的 0.50–0.67 倍**，第二组在 5s SLO 下**仅持平**
- 结论：当亲和性回收的 KV 工作量不足以抵消残留的负载倾斜时，收益会被削减甚至抹平

### 部署建议

- 启用前先做 **shadow replay**，对比四个指标：served KV 命中率、节点负载不均衡、p99 延迟、失败率
- **只有 p99 或实际容量确实改善，才安装新的亲和计划**——不要仅凭工作负载统计就开启亲和性

### 适用条件

- 需要：稳定的路由 Key、可复用的 Key-specific prefix、速率估计在一个缓存预热周期内仍有效
- 需重新测量：前缀大小差异很大、业务分布变化快、或重复前缀收益很小

### 系列定位

| 工作 | 解决的问题 |
|------|-----------|
| KVCOMM | 跨前缀的 KV 偏移估计 |
| TokenDance | 多智能体轮次的共享 KV |
| Helium | 工作流级缓存调度 |
| ContextPilot | 输入上下文的对齐与去重 |
| **CacheRoute** | **入口请求如何分配到已有的模型服务节点** |

## 代码仓库

⚠️ **未见官方仓库**。arXiv 摘要页没有给出任何代码链接。

| 仓库 | Star | 说明 |
|------|------|------|
| [AstraNetLab/CacheRoute](https://github.com/AstraNetLab/CacheRoute) | 323 | ⚠️ **同名不同项目，不是本文实现**。它是「基于 vLLM + LMCache 的知识密集型 LLM 服务的 KV 复用方案」，README 未引用 arXiv:2608.19677，且其 roadmap 中 "Paper and citation release" 仍为未勾选状态 |

## 源笔记摘录

> CacheRoute: Planned Prefix-Affinity Routing for Large-Scale LLM Serving
> https://arxiv.org/abs/2608.19677
> （其后为 1–12 条中文精读笔记，已全部并入上文「核心要点」）

## 勘误与提醒

- ⚠️ **不要误认同名仓库**：GitHub 上 `AstraNetLab/CacheRoute`（323 star）创建于 2025-11-17，**早于**本文 2026-08-20 的提交时间，且技术内容（knowledge injection / vLLM + LMCache）与本文（prefix-affinity routing）不同。检索时极易踩坑。
- ✔ 源笔记的 12 条精读与 arXiv 摘要**完全吻合**，无幻觉内容——是 2026 年笔记中质量最高的一篇自撰精读。
- ℹ️ 论文作者仅 1 人署名（Huang Cheng），且无公开代码与会议标注，引用时建议保留「预印本」口径。

## BibTeX

```bibtex
@misc{cacheroute2026,
  title  = {CacheRoute: Planned Prefix-Affinity Routing for Large-Scale LLM Serving},
  author = {Cheng, Huang},
  year   = {2026},
  journal= {arXiv preprint arXiv:2608.19677},
  url    = {https://arxiv.org/abs/2608.19677}
}
```
