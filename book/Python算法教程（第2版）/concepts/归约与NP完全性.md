# 概念专篇：归约与 NP 完全性

> 跨章节概念，出现在 [04-归纳递归与规约.md](../04-归纳递归与规约.md) 与 [11-困难问题与近似.md](../11-困难问题与近似.md)。把「把新问题变成旧问题」这一核心武器讲透。

## 一、规约（Reduction）的两种含义

- 算法内规约（第 4 章）：把问题 A 改写成已解问题 B（如最大子数组和 → 前缀和扫描）。
- 复杂性规约（第 11 章）：多项式时间将 A 归约到 B，用于证明 B 至少和 A 一样难（A ≤p B）。

## 二、NP 完全证明套路

1. 证 B ∈ NP（解可多项式验证）。
2. 取一已知 NPC 问题 A（如 3-SAT），构造多项式变换 A → B。
3. 则 B 是 NPC。

## 三、经典 NPC 问题清单

SAT / 3-SAT、顶点覆盖、团、独立集、哈密顿回路、旅行商（决策版）、子集和、划分、图的着色。

## 四、版本演进

- 原书用 Python 写小规模精确搜索演示；今天可用 `@cache`（见 [08-动态规划.md](../08-动态规划.md)）做子集/划分型 DP，用 `ortools`/`python-sat` 做实例求解。

## 五、经典论文与原始文献

- Cook, S. A. *The Complexity of Theorem-Proving Procedures*, STOC 1971（Cook-Levin，SAT 是 NPC）。
- Karp, R. M. *Reducibility Among Combinatorial Problems*, 1972（21 个 NPC 问题）。
- Garey, M. R., Johnson, D. S. *Computers and Intractability*, 1979（NPC 字典）。

## 六、近年研究与工业界前沿（2020–2026）

- 现代 SAT 求解器（`python-sat`/`pysat`）工业实例极快；约束优化用 `ortools`（非同行评审，工业广泛）。
- P vs NP 未解（2026 现状）；神经组合优化是研究热点，但无突破降复杂度结论。

## 七、跨语言对照

- 规约思想语言无关；`ortools` 的 Python 建模 API 比 C++ 更简洁，适合快速验证近似方案。
