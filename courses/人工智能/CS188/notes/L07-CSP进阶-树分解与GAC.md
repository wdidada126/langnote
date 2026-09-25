# L07 CSP 进阶：树结构分解、GAC、局部推理

> 对应 AIMA Ch.6.5-6.9；Klein 补充讲义 "Tree Decomposition"。回答"什么时候 CSP/推断可以多项式"。

## 1. 核心概念

- **约束图**：变量为点、共现于约束为边。图结构决定难度——**树宽 treewidth 是指数项的真实来源**。
- **树结构 CSP**（约束图是树）：O(n·d²) 精确可解——弧一致性即可完备（无环 ⟹ AC ⟹ 全局一致）。
  - 算法：选根、自底向上删叶（bucket elimination 的 CSP 版）、再自顶向下回填。
- **割点条件化（cutset conditioning）**：给割点赋值后剩余部分是树 → O(d^{c}·poly(n))，c=割集大小。
- **树分解（tree decomposition）**：把图覆盖为"簇（cluster）的树"，满足①每变量至少出现一次②每约束在某簇内③变量出现的簇连通。树宽 w = 最大簇−1。
  - **条件化树分解**：簇间用 separator（父簇子集）做消息，复杂度 O(d^{w+1})。
- **GAC（全局弧一致性）**：对 all-different 等全局约束直接传播（如数独 hidden-pair、匹配理论），远强于二元 AC。

## 2. 关键伪码（树分解求解）

```
# 1) 求近似最小树宽分解（min-fill / 引导搜索）
# 2) 树形 DP：对簇 i，表 T_i[separator_i] = ∃赋值使子树全部满足
solve_cluster(i):
    for assignment of cluster_vars consistent with parent separator:
        check constraints fully inside cluster
        recurse children with new separators
```

- bucket elimination：按消元序把变量所在约束合成新超约束——**诱导宽度 = 实际树宽**，与 L10 变量消元完全同构。

## 3. 直觉例子

- 链式约束（时序排程）树宽 1 → 多项式；网格图（图像像素）树宽 ~√n → 指数但底小可工程化；社交网络小规模聚类近似树。
- all-different（拉丁方/数独区块）用 GAC + Hall 集定理剪枝，AC-3 做不到。

## 4. 前后讲联系

- 前承 L06（AC-3 只在树上完备的缺陷）；后接 L09-L10（贝叶斯网络推断的复杂度 = 道德图树宽——**同一把尺子量两个领域**）、L18（树宽太大 → 采样）。
- 与 L03 呼应：relaxation/结构利用是对付指数性的两大通用武器。

## 5. 跨课程联系

- **6.006**：NP 完全性归约的"受限版本可解"教学案例（2-SAT vs 3-SAT；树上 CSP vs 图 CSP），与 6.006 最后几讲直接互文。
- **CS229**：CRF 链/树结构推断 = 本讲 DP 的概率版（L17 Viterbi 是链特例）。
- **MIT6.824**：树分解的 separator 消息传递 ≈ MapReduce 的 shuffle 边界——簇是 mapper，separator 是 key。
- **DDCA**：FPGA 电路网表划分（cluster LUT 大小 = 树宽+1）用几乎相同的图划分算法。

## 6. 开源项目应用

- **NetworkX**：`nx.min_fill / nx.tree_decomposition`（小图近似树宽）。
- **OR-Tools CP-SAT**、**Gecode**：全局约束传播器（all-different 匹配算法）是 GAC 工业实现。
- **tocs / 数独求解器集合**（如 `sudoku` 类项目）：HR 策略 + GAC 教学演示。

## 7. 延伸阅读

- AIMA 4e §6.5, §6.8；CS188 Note "Tree Decomposition"。
- Dechter & Pearl "Tree Clustering and Cycle Cutset Conditioning" (1989)；Robertson & Seymour Graph Minors（树宽理论）。
- 练习建议：把 `projects/bayes` 的 VE 换成 bucket elimination 观察诱导宽度一致。
